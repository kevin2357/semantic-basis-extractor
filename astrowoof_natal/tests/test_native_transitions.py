from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from importlib.resources import files
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (
    load_json,
    normalized_path,
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.native_transitions import (
    _record_digest,
    _result_digest,
    append_transition_record,
    checkpoint_basis,
    journal_range,
    mint_invocation_id,
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
        invocation = mint_invocation_id()
        self.append(run, invocation, "invocation.started")
        self.append(run, invocation, "native.transitioned")
        self.append(run, invocation, "invocation.closed")
        selected = journal_range(run, 1, 3)
        basis = checkpoint_basis(run, 7)
        result = write_immutable_execution_result(run, {
            "invocation_id": invocation,
            "run_id": "run_native_fixture",
            "sbe_release": "0.4.4",
            "published_at": "2026-08-17T22:01:00Z",
            "command_kind": "ordinary_authoring",
            "route_binding": self.route(),
            "pre_checkpoint": None,
            "post_checkpoint": {
                "native_state_revision": 7,
                "checkpoint_basis_sha256": basis["checkpoint_basis_sha256"],
                "logical_workspace_root": normalized_path(run),
            },
            "journal_range": {
                key: selected[key] for key in (
                    "start_sequence", "end_sequence", "record_count", "range_sha256"
                )
            } | {"closing_record_id": selected["records"][-1]["record_id"]},
            "outcome": "review_required",
            "cause_code": "authoring_attempts_exhausted",
            "action_ids": [],
            "provider_operations": [],
            "projection_refs": {},
        })
        write_workspace_snapshot(run)
        return result

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
        fixtures = files("astrowoof_natal_authoring").joinpath(
            "resources/fixtures/native_transition"
        )
        record = json.loads(
            fixtures.joinpath("review-terminal-record.v0.1.json").read_text("utf-8")
        )
        result = json.loads(
            fixtures.joinpath("review-terminal-result.v0.1.json").read_text("utf-8")
        )
        self.assertEqual(record["record_sha256"], _record_digest(record))
        self.assertEqual(result["result_sha256"], _result_digest(result))

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


if __name__ == "__main__":
    unittest.main()
