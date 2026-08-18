from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
from importlib.resources import files
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (
    load_json,
    normalized_path,
    persist_state,
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.native_transitions import (
    _record_digest,
    _receipt_digest,
    _result_digest,
    append_transition_record,
    checkpoint_basis,
    journal_range,
    mint_invocation_id,
    publish_native_execution_result,
    read_native_transition_result,
    validate_transition_journal,
    write_immutable_execution_result,
)
from astrowoof_natal_authoring.lifecycle import _exclusive_lifecycle_lock


class TestNativeTransitions(unittest.TestCase):
    def workspace(self, root: Path) -> Path:
        run = root / "run"
        run.mkdir()
        write_json_atomic(run / "run.json", {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_native_fixture",
            "state_revision": 7,
            "status": "FAILED_REQUIRES_REVIEW",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(run),
            },
        })
        write_json_atomic(run / "public-run.json", {
            "run_id": "run_native_fixture", "status": "FAILED_REQUIRES_REVIEW",
        })
        write_workspace_snapshot(run)
        return run

    def route(self) -> dict:
        return {
            "route_family": "exact_natal", "provider_mechanism": "response",
            "native_operation_ref": "semantic_closure.resume",
        }

    def action(self) -> dict:
        return {
            "action_id": "paid_fixture", "stage": "creative_retry",
            "route": "bre_1:attempt-002", "request_sha256": "d" * 64,
            "profile_sha256": "e" * 64, "maximum_output_tokens": 30000,
            "commitment_micro_usd": 500000, "price_book_version": "pb.v1",
        }

    def append(self, run: Path, invocation: str, kind: str, revision: int = 7) -> dict:
        provider = None
        if kind.startswith("provider."):
            provider = {
                "observation_kind": kind.split(".", 1)[1],
                "provider_kind": "response",
                "provider_operation_id": (
                    None if kind == "provider.submission_started" else "resp_fixture"
                ),
                "status": "submitted" if kind.endswith("started") else "completed",
                "cost_disposition": (
                    "no_provider_work_consumed" if kind.endswith("started")
                    else "provider_usage_reported"
                ),
                "price_book_version": None if kind.endswith("started") else "pb.v1",
                "usage_evidence_ref": None if kind.endswith("started") else {
                    "path": "provider-result.json", "sha256": "f" * 64,
                },
                "estimated_micro_usd": None if kind.endswith("started") else 12,
            }
        return append_transition_record(run, {
            "invocation_id": invocation,
            "observed_at": "2026-08-17T22:00:00Z",
            "native_state_revision": revision,
            "record_kind": kind,
            "route_binding": self.route(),
            "action_binding": (self.action() if provider else None),
            "provider_observation": provider,
            "native_transition": (
                {"outcome": "review_required"}
                if kind == "native.transitioned" else None
            ),
        })

    def publish_review_result(self, run: Path) -> dict:
        return publish_native_execution_result(
            run, command_kind="ordinary_authoring", sbe_release="0.4.4",
            published_at="2026-08-17T22:01:00Z",
        )["result"]

    def test_hash_chain_range_and_bounded_public_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            result = self.publish_review_result(run)
            records = validate_transition_journal(run)
            self.assertEqual([1, 2, 3], [item["sequence"] for item in records])
            exported = read_native_transition_result(run, result["result_id"])
            self.assertEqual(result, exported["result"])
            self.assertEqual(3, len(exported["journal_range"]["records"]))
            self.assertNotIn("run.json", json.dumps(exported))

    def test_exact_record_replay_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            invocation = mint_invocation_id()
            request = {
                "invocation_id": invocation,
                "observed_at": "2026-08-17T22:00:00Z",
                "native_state_revision": 7,
                "record_kind": "invocation.started",
                "route_binding": self.route(),
                "action_binding": None,
                "provider_observation": None,
                "native_transition": None,
            }
            first = append_transition_record(run, request)
            replay = append_transition_record(run, request)
            self.assertEqual(first, replay)
            self.assertEqual(1, len(validate_transition_journal(run)))

    def test_journal_corruption_gap_and_unknown_kind_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            invocation = mint_invocation_id()
            self.append(run, invocation, "invocation.started")
            path = run / "native-transition-journal.jsonl"
            record = json.loads(path.read_text(encoding="utf-8"))
            for mutation in (
                lambda item: item.update(sequence=2),
                lambda item: item.update(record_kind="provider.retry_lol"),
                lambda item: item.update(record_sha256="0" * 64),
            ):
                changed = deepcopy(record)
                mutation(changed)
                path.write_text(json.dumps(changed) + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    validate_transition_journal(run)

    def test_provider_id_and_usage_rules_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            invocation = mint_invocation_id()
            started = self.append(run, invocation, "provider.submission_started")
            self.assertIsNone(started["provider_observation"]["provider_operation_id"])
            bad = load_json(run / "run.json")
            self.assertEqual("run_native_fixture", bad["run_id"])
            with self.assertRaises(ValueError):
                append_transition_record(run, {
                    "invocation_id": invocation,
                    "observed_at": "2026-08-17T22:00:01Z",
                    "native_state_revision": 7,
                    "record_kind": "provider.pending",
                    "route_binding": self.route(),
                    "action_binding": self.action(),
                    "provider_observation": {
                        "observation_kind": "pending", "provider_kind": "response",
                        "provider_operation_id": None, "status": "in_progress",
                        "cost_disposition": "not_applicable_provider_pending",
                        "price_book_version": None, "usage_evidence_ref": None,
                        "estimated_micro_usd": None,
                    },
                    "native_transition": None,
                })

    def test_result_is_immutable_and_full_snapshot_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            result = self.publish_review_result(run)
            (run / "native-result-index.json").unlink()
            replay = write_immutable_execution_result(run, result)
            self.assertEqual(result, replay)
            self.assertIn(
                result["result_id"], load_json(run / "native-result-index.json")["result_ids"]
            )
            write_workspace_snapshot(run)
            validate_workspace_snapshot(run, load_json(run / "run.json"))

            result_path = run / "native-results" / f"{result['result_id']}.json"
            result_path.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_native_transition_result(run, result["result_id"])

    def test_package_root_exposes_reader_not_mutator(self) -> None:
        import astrowoof_natal_authoring as package

        self.assertTrue(callable(package.read_native_transition_result))
        self.assertTrue(callable(package.validate_transition_journal))
        self.assertFalse(hasattr(package, "append_transition_record"))

    def test_packaged_schema_and_catalog_publish_current_contracts(self) -> None:
        contracts = files("astrowoof_natal_authoring").joinpath("resources/contracts")
        schema = json.loads(
            contracts.joinpath("native-transition-contracts.schema.json")
            .read_text(encoding="utf-8")
        )
        catalog = json.loads(
            contracts.joinpath("contract-catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
        self.assertEqual(
            "astrowoof.native_transition_journal_record.v0.1",
            catalog["contracts"]["native_transition_journal_record"],
        )
        self.assertEqual(
            "astrowoof.native_execution_result.v0.1",
            catalog["contracts"]["native_execution_result"],
        )
        self.assertEqual(
            "astrowoof.native_publication_receipt.v0.1",
            catalog["contracts"]["native_publication_receipt"],
        )
        fixtures = files("astrowoof_natal_authoring").joinpath(
            "resources/fixtures/native_transition"
        )
        record = json.loads(
            fixtures.joinpath("review-terminal-record.v0.1.json").read_text("utf-8")
        )
        result = json.loads(
            fixtures.joinpath("review-terminal-result.v0.1.json").read_text("utf-8")
        )
        receipt = json.loads(
            fixtures.joinpath("review-terminal-receipt.v0.1.json").read_text("utf-8")
        )
        self.assertEqual(record["record_sha256"], _record_digest(record))
        self.assertEqual(result["result_sha256"], _result_digest(result))
        self.assertEqual(receipt["receipt_sha256"], _receipt_digest(receipt))

    def test_cross_process_writer_contention_fails_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            request = {
                "invocation_id": mint_invocation_id(),
                "observed_at": "2026-08-17T22:00:00Z",
                "native_state_revision": 7,
                "record_kind": "invocation.started",
                "route_binding": self.route(),
                "action_binding": None,
                "provider_observation": None,
                "native_transition": None,
            }
            code = (
                "import json,sys; from pathlib import Path; "
                "from astrowoof_natal_authoring.native_transitions import "
                "append_transition_record; "
                "append_transition_record(Path(sys.argv[1]),json.loads(sys.argv[2]))"
            )
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(ROOT / "src")
            with _exclusive_lifecycle_lock(run):
                completed = subprocess.run(
                    [sys.executable, "-c", code, str(run), json.dumps(request)],
                    capture_output=True, text=True, env=environment, check=False,
                )
            self.assertNotEqual(0, completed.returncode)
            self.assertEqual([], validate_transition_journal(run))

    def test_partial_publication_and_relocation_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = self.workspace(root)
            result = self.publish_review_result(run)
            (run / "untracked-after-snapshot.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_native_transition_result(run, result["result_id"])

            (run / "untracked-after-snapshot.json").unlink()
            relocated = root / "relocated"
            run.rename(relocated)
            with self.assertRaises(ValueError):
                read_native_transition_result(relocated, result["result_id"])

    def test_record_size_and_unbounded_export_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            invocation = mint_invocation_id()
            with self.assertRaises(ValueError):
                append_transition_record(run, {
                    "invocation_id": invocation,
                    "observed_at": "2026-08-17T22:00:00Z",
                    "native_state_revision": 7,
                    "record_kind": "native.transitioned",
                    "route_binding": self.route(),
                    "action_binding": None,
                    "provider_observation": None,
                    "native_transition": {"detail": "x" * (33 * 1024)},
                })
            with self.assertRaises(ValueError):
                journal_range(run, 1, 513)

    def test_checkpoint_basis_ignores_publication_namespace_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            before = checkpoint_basis(run, 7)["checkpoint_basis_sha256"]
            (run / "native-results").mkdir()
            (run / "native-results" / "ignored.json").write_text("{}", encoding="utf-8")
            write_json_atomic(run / "native-result-index.json", {
                "schema_version": "astrowoof.native_result_index.v0.1",
                "result_ids": [],
            })
            self.assertEqual(before, checkpoint_basis(run, 7)["checkpoint_basis_sha256"])
            (run / "authoritative.json").write_text("{}", encoding="utf-8")
            self.assertNotEqual(before, checkpoint_basis(run, 7)["checkpoint_basis_sha256"])

    def test_paid_action_lifecycle_is_projected_once_from_durable_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            state = load_json(run / "run.json")
            state.update({
                "schema_version": "astrowoof.semantic_closure_run.v0.9",
                "updated_at": "2026-08-17T22:00:00Z",
                "spend_ledger": {"actions": []}, "passes": {}, "subjects": {},
            })
            action = {
                "action_id": "paid_123456789012345678901234", "state": "PREPARED",
                "binding": {
                    "run_id": state["run_id"], "profile_sha256": "a" * 64,
                    "prepared_state_revision": 7, "stage": "creative_retry",
                    "route": "dog:creative_retry:002", "request_sha256": "b" * 64,
                    "model": "gpt-5.6-luna", "service_level": "interactive",
                    "maximum_output_tokens": 1000, "commitment_micro_usd": 42000,
                    "price_book_version": "openai-public-2026-08-07.v1",
                },
                "authorization": None, "provider": None, "reported": None,
                "reconciliation_reference_ids": [],
            }
            state["spend_ledger"]["actions"].append(action)
            phases = (
                ("PREPARED", {}),
                ("AUTHORIZED", {"authorization": {"authorization_reference": "api:1"}}),
                ("SUBMITTING", {"consumption": {"consumer_id": "worker", "state_revision": 9}}),
                ("PROVIDER_ID_RECORDED", {"provider": {"kind": "response", "id": "resp_1"}}),
                ("WAITING", {}),
                ("REPORTED", {"reported": {"usage": {"input_tokens": 10}, "estimated_micro_usd": 77}}),
            )
            for offset, (action_state, additions) in enumerate(phases):
                action["state"] = action_state
                action.update(additions)
                state["updated_at"] = f"2026-08-17T22:00:0{offset}Z"
                persist_state(run / "run.json", state)
            first = validate_transition_journal(run)
            persist_state(run / "run.json", state)
            replay = validate_transition_journal(run)
            self.assertEqual(first, replay)
            self.assertEqual([
                "action.prepared", "action.authorized", "action.consumed",
                "provider.submission_started", "provider.identity_recorded",
                "provider.pending", "provider.completed", "provider.usage_reported",
            ], [item["record_kind"] for item in replay])
            self.assertEqual(
                "provider_usage_reported",
                replay[-1]["provider_observation"]["cost_disposition"],
            )

    def test_route_stage_matrix_batch_bounded_ambiguity_and_unavailable_usage(self) -> None:
        stages = (
            "authoring_initial", "creative_retry", "polish",
            "qualitative_critic", "qualitative_candidate",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for index, stage in enumerate(stages):
                case_root = root / f"case-{index}"
                case_root.mkdir()
                run = self.workspace(case_root)
                state = load_json(run / "run.json")
                state.update({
                    "schema_version": "astrowoof.semantic_closure_run.v0.9",
                    "updated_at": "2026-08-17T22:10:00Z", "spend_ledger": {"actions": []},
                })
                service = "batch" if index == 0 else "interactive"
                action = {
                    "action_id": f"paid_{index:024d}", "state": "REPORTED",
                    "binding": {
                        "profile_sha256": "a" * 64, "stage": stage,
                        "route": "batch-round-001" if service == "batch" else f"dog:{stage}:001",
                        "request_sha256": f"{index + 1:x}" * 64,
                        "maximum_output_tokens": 10, "commitment_micro_usd": 20,
                        "price_book_version": "openai-public-2026-08-07.v1",
                        "service_level": service,
                    },
                    "authorization": {"authorization_reference": "api"},
                    "consumption": {"consumer_id": "worker"},
                    "provider": {"kind": service if service == "batch" else "response", "id": f"op_{index}"},
                    "reported": {"usage": None, "estimated_micro_usd": None},
                }
                state["spend_ledger"]["actions"] = [action]
                write_json_atomic(run / "run.json", state)
                from astrowoof_natal_authoring.native_transitions import sync_provider_transition_journal
                sync_provider_transition_journal(run, state)
                records = validate_transition_journal(run)
                self.assertEqual(
                    "batch" if service == "batch" else "response",
                    records[0]["route_binding"]["provider_mechanism"],
                )
                self.assertEqual("provider.usage_unavailable", records[-1]["record_kind"])

            bounded_root = root / "bounded"
            bounded_root.mkdir()
            bounded = self.workspace(bounded_root)
            state = load_json(bounded / "run.json")
            state.update({
                "schema_version": "astrowoof.bounded_natal.authoring_run.v1",
                "route_contract": "astrowoof.bounded_natal.authoring_run.v1",
                "route": "bounded_natal.v1", "updated_at": "2026-08-17T22:20:00Z",
            })
            action = deepcopy(action)
            action["action_id"] = "paid_bounded00000000000000000"
            action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
            action["binding"]["service_level"] = "interactive"
            action["binding"]["route"] = "bounded_natal.v1:authoring_initial:001"
            action["provider"] = None
            action["ambiguity"] = {"reason": "interrupted after request bytes left process"}
            action["reported"] = None
            state["spend_ledger"] = {"actions": [action]}
            write_json_atomic(bounded / "run.json", state)
            sync_provider_transition_journal(bounded, state)
            records = validate_transition_journal(bounded)
            self.assertEqual("bounded_natal", records[0]["route_binding"]["route_family"])
            self.assertEqual("provider.submission_ambiguous", records[-1]["record_kind"])

    def test_interrupted_projection_recovers_from_durable_ledger_without_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            state = load_json(run / "run.json")
            state.update({
                "schema_version": "astrowoof.semantic_closure_run.v0.9",
                "passes": {}, "subjects": {}, "updated_at": "2026-08-17T23:00:00Z",
                "spend_ledger": {"actions": [{
                    "action_id": "paid_recovery00000000000000", "state": "SUBMITTING",
                    "binding": {
                        "profile_sha256": "a" * 64, "stage": "authoring_initial",
                        "route": "dog:authoring_initial:001", "request_sha256": "b" * 64,
                        "maximum_output_tokens": 10, "commitment_micro_usd": 20,
                        "price_book_version": "openai-public-2026-08-07.v1",
                        "service_level": "interactive",
                    },
                    "authorization": {"authorization_reference": "api"},
                    "consumption": {"consumer_id": "worker"},
                    "provider": None, "reported": None,
                }]},
            })
            with patch(
                "astrowoof_natal_authoring.native_transitions._append_transition_record_internal",
                side_effect=OSError("injected journal publication interruption"),
            ):
                with self.assertRaisesRegex(OSError, "journal publication"):
                    persist_state(run / "run.json", state)
            self.assertEqual(
                "SUBMITTING",
                load_json(run / "run.json")["spend_ledger"]["actions"][0]["state"],
            )
            self.assertEqual([], validate_transition_journal(run))
            from astrowoof_natal_authoring.native_transitions import sync_provider_transition_journal
            sync_provider_transition_journal(run, load_json(run / "run.json"))
            first = validate_transition_journal(run)
            sync_provider_transition_journal(run, load_json(run / "run.json"))
            self.assertEqual(first, validate_transition_journal(run))
            self.assertEqual(
                ["action.prepared", "action.authorized", "action.consumed", "provider.submission_started"],
                [item["record_kind"] for item in first],
            )

    def test_result_snapshot_receipt_interruption_repairs_exact_orphan(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            with patch(
                "astrowoof_natal_authoring.closure.write_workspace_snapshot",
                side_effect=OSError("injected snapshot interruption"),
            ):
                with self.assertRaisesRegex(OSError, "snapshot interruption"):
                    publish_native_execution_result(
                        run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                        published_at="2026-08-17T23:30:00Z",
                    )
            result_id = load_json(run / "native-result-index.json")["result_ids"][0]
            self.assertFalse(
                (run / "native-publication-receipts" / f"{result_id}.json").exists()
            )
            repaired = publish_native_execution_result(
                run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                published_at="2026-08-17T23:31:00Z",
            )
            self.assertEqual(result_id, repaired["result"]["result_id"])
            self.assertEqual(1, len(load_json(run / "native-result-index.json")["result_ids"]))
            self.assertEqual(
                result_id, read_native_transition_result(run, result_id)["result"]["result_id"]
            )

    def test_snapshot_manifest_must_validate_before_receipt_is_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            run_json = run / "run.json"
            original_run = run_json.read_bytes()

            def write_then_change_workspace(target: Path) -> None:
                write_workspace_snapshot(target)
                run_json.write_bytes(original_run + b" ")

            with patch(
                "astrowoof_natal_authoring.closure.write_workspace_snapshot",
                side_effect=write_then_change_workspace,
            ):
                with self.assertRaisesRegex(ValueError, "snapshot is incomplete or changed"):
                    publish_native_execution_result(
                        run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                        published_at="2026-08-17T23:35:00Z",
                    )
            result_id = load_json(run / "native-result-index.json")["result_ids"][0]
            self.assertFalse(
                (run / "native-publication-receipts" / f"{result_id}.json").exists()
            )
            run_json.write_bytes(original_run)
            repaired = publish_native_execution_result(
                run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                published_at="2026-08-17T23:36:00Z",
            )
            self.assertEqual(result_id, repaired["result"]["result_id"])
            self.assertTrue(
                (run / "native-publication-receipts" / f"{result_id}.json").is_file()
            )

    def test_reader_rejects_missing_or_changed_publication_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            result = self.publish_review_result(run)
            receipt_path = (
                run / "native-publication-receipts" / f"{result['result_id']}.json"
            )
            receipt = load_json(receipt_path)
            receipt_path.unlink()
            with self.assertRaisesRegex(ValueError, "no immutable publication receipt"):
                read_native_transition_result(run, result["result_id"])
            write_json_atomic(receipt_path, {**receipt, "snapshot_sha256": "0" * 64})
            with self.assertRaisesRegex(ValueError, "receipt binding"):
                read_native_transition_result(run, result["result_id"])

    def test_historical_result_remains_bound_after_later_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            first = self.publish_review_result(run)
            state = load_json(run / "run.json")
            state["status"] = "DELIVERY_COMPLETE"
            state["state_revision"] = 8
            write_json_atomic(run / "run.json", state)
            write_workspace_snapshot(run)
            second = publish_native_execution_result(
                run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                published_at="2026-08-17T23:45:00Z",
            )["result"]
            self.assertNotEqual(first["result_id"], second["result_id"])
            self.assertEqual(
                first["result_id"],
                read_native_transition_result(run, first["result_id"])["result"]["result_id"],
            )

    def test_external_denial_terminal_cause_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            state = load_json(run / "run.json")
            state.update({
                "status": "BUDGET_EXHAUSTED",
                "terminal_transition": {
                    "outcome": "terminalized", "terminal_outcome": "budget_exhausted",
                    "terminal_reason": "external_spend_authority_denied",
                },
            })
            write_json_atomic(run / "run.json", state)
            sealed = publish_native_execution_result(
                run, command_kind="ordinary_authoring", sbe_release="0.4.4",
                published_at="2026-08-17T23:50:00Z",
            )
            self.assertEqual("budget_exhausted", sealed["result"]["outcome"])
            self.assertEqual(
                "external_spend_authority_denied", sealed["result"]["cause_code"]
            )

    def test_public_cli_explicit_and_latest_are_read_only_and_identical(self) -> None:
        from astrowoof_natal_authoring.cli.native_transition import main as cli_main

        with tempfile.TemporaryDirectory() as temporary:
            run = self.workspace(Path(temporary))
            result = self.publish_review_result(run)

            def all_bytes() -> dict[str, bytes]:
                return {
                    path.relative_to(run).as_posix(): path.read_bytes()
                    for path in run.rglob("*") if path.is_file()
                }

            before = all_bytes()
            outputs = []
            for selection in (["--result-id", result["result_id"]], ["--latest"]):
                stream = io.StringIO()
                with patch(
                    "sys.argv", ["astrowoof-native-transition", "--run-dir", str(run), *selection]
                ), patch(
                    "urllib.request.urlopen", side_effect=AssertionError("provider call")
                ), redirect_stdout(stream):
                    cli_main()
                outputs.append(json.loads(stream.getvalue()))
            self.assertEqual(outputs[0], outputs[1])
            self.assertEqual(result["result_id"], outputs[0]["result"]["result_id"])
            self.assertEqual(before, all_bytes())

    def test_public_cli_output_must_resolve_outside_workspace(self) -> None:
        from astrowoof_natal_authoring.cli.native_transition import main as cli_main

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = self.workspace(root)
            result = self.publish_review_result(run)

            def all_bytes() -> dict[str, bytes]:
                return {
                    path.relative_to(run).as_posix(): path.read_bytes()
                    for path in run.rglob("*") if path.is_file()
                }

            before = all_bytes()
            external_output = root / "consumer-export.json"
            stream = io.StringIO()
            with patch(
                "sys.argv", [
                    "astrowoof-native-transition", "--run-dir", str(run),
                    "--result-id", result["result_id"], "--output", str(external_output),
                ]
            ), redirect_stdout(stream):
                cli_main()
            self.assertEqual(json.loads(stream.getvalue()), json.loads(external_output.read_text()))
            self.assertEqual(before, all_bytes())

            for refused_output in (run, run / "exports" / "result.json"):
                stderr = io.StringIO()
                with patch(
                    "sys.argv", [
                        "astrowoof-native-transition", "--run-dir", str(run),
                        "--result-id", result["result_id"], "--output", str(refused_output),
                    ]
                ), redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
                    cli_main()
                self.assertEqual(2, raised.exception.code)
                self.assertIn("--output must resolve outside --run-dir", stderr.getvalue())
                self.assertEqual(before, all_bytes())
            self.assertFalse((run / "exports" / "result.json").exists())

    def test_packaged_consumer_fixture_matrix_has_canonical_identities(self) -> None:
        fixtures = files("astrowoof_natal_authoring").joinpath(
            "resources/fixtures/native_transition"
        )
        catalog = json.loads(
            fixtures.joinpath("consumer-ingestion-cases.v0.1.json").read_text("utf-8")
        )
        self.assertEqual(
            {
                "exact_response_delivery", "exact_response_review",
                "exact_batch_provider_failure", "exact_response_pending",
                "bounded_response_ambiguity", "malformed_result_refusal",
                "exact_replay", "conflicting_second_operation_refusal",
            },
            {item["case_id"] for item in catalog["cases"]},
        )
        for case in catalog["cases"]:
            view = case["view"]
            record = view["journal_range"]["records"][0]
            self.assertEqual(record["record_sha256"], _record_digest(record))
            self.assertEqual(
                view["receipt"]["receipt_sha256"], _receipt_digest(view["receipt"])
            )
            if case["expected_disposition"] == "refused":
                self.assertNotEqual(
                    view["result"]["result_sha256"], _result_digest(view["result"])
                )
            else:
                self.assertEqual(
                    view["result"]["result_sha256"], _result_digest(view["result"])
                )
                self.assertEqual(
                    view["result"]["result_sha256"],
                    view["receipt"]["result_sha256"],
                )


if __name__ == "__main__":
    unittest.main()
