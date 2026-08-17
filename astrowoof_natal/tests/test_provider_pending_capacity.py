from __future__ import annotations

import hashlib
import copy
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    public_run_state,
    reconciled_response_evidence,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    closeout_run,
    inspect_lifecycle,
)
from astrowoof_natal_authoring.reconciliation import (  # noqa: E402
    delay_seconds,
    initial_timing,
    native_provider_route_identity,
    reconcile_provider_cycle,
    record_attempt,
    run_bounded_authoring_reconciliation,
)
from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter  # noqa: E402


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


class TestProviderPendingCapacityBaseline(unittest.TestCase):
    """Freeze the 0.4.2 projection before adding capacity-release authority."""

    def materialize(self, root: Path) -> dict:
        run_id = "run_provider_pending_capacity_001"
        actions = []
        passes = {}
        for index in range(1, 4):
            action_id = f"paid_{index:024d}"
            response_id = f"resp_provider_pending_{index}"
            route = f"kevin:authoring_initial:{index:03d}"
            binding = {
                "run_id": run_id,
                "profile_sha256": "1" * 64,
                "prepared_state_revision": index,
                "stage": "authoring_initial",
                "route": route,
                "request_sha256": str(index) * 64,
                "model": "gpt-5.6-terra",
                "service_level": "interactive",
                "maximum_output_tokens": 4000,
                "commitment_micro_usd": 50000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            actions.append({
                "action_id": action_id,
                "state": "WAITING",
                "binding": binding,
                "authorization": {
                    "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                    "action_id": action_id,
                    "binding": binding,
                    "authorization_reference": f"api-reservation-{index}",
                },
                "consumption": {
                    "consumer_id": f"worker-{index}",
                    "consumed_at": f"2026-08-15T20:0{index}:00Z",
                },
                "provider": {"id": response_id, "kind": "response"},
                "provider_reconciliation": {
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.1",
                    "provider_retrieval_attempt_count": 0,
                    "last_attempt_at": None,
                    "last_outcome": "provider_identity_recorded",
                    "resume_not_before": f"2026-08-15T20:{14 + index:02d}:00Z",
                },
                "reported": None,
            })
            passes[f"pass-{index}"] = {
                "pass_id": f"pass-{index}",
                "state": "WAITING_FOR_RESPONSE",
                "attempts": [{
                    "attempt": 1,
                    "state": "WAITING_FOR_RESPONSE",
                    "provider_metadata": {
                        "provider": "openai",
                        "response_id": response_id,
                        "response_status": "in_progress",
                        "last_polled_at": f"2026-08-15T20:0{index}:30Z",
                    },
                }],
            }
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": run_id,
            "state_revision": 12,
            "status": "WAITING_FOR_RESPONSE",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": actions},
            "passes": passes,
            "subjects": {},
            "provenance": {},
        }
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        return state

    def test_known_provider_wait_projects_safe_release_and_earliest_due(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.materialize(root)
            before = hashes(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertEqual(before, hashes(root))
            self.assertTrue(inspection["observation"]["inventory_valid"])
            self.assertFalse(inspection["terminal"]["terminal"])
            self.assertTrue(
                inspection["terminal"]["provider_continuation_remains"]
            )
            self.assertTrue(inspection["terminal"]["local_continuation_remains"])
            self.assertEqual(
                ["provider_continuation_remains", "local_continuation_remains"],
                inspection["quiescence"]["reasons"],
            )
            self.assertEqual("not_quiescent", inspection["quiescence"]["state"])
            self.assertEqual(
                [{
                    "kind": "provider_result_reconciliation",
                    "blocking": True,
                    "reason_code": "provider_result_pending",
                }],
                inspection["local_dependencies"],
            )
            self.assertEqual(
                "astrowoof.authoring_lifecycle_inspection.v0.3",
                inspection["schema_version"],
            )
            self.assertEqual(
                {
                    "disposition": "release_until_due",
                    "local_work_ready_now": False,
                    "checkpoint_safe_for_worker_release": True,
                    "resume_not_before": "2026-08-15T20:15:00Z",
                    "reason_code": "known_provider_work_pending",
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                },
                inspection["execution_capacity"],
            )
            custody = inspection["provider_custody"]
            self.assertEqual("known_operations_pending", custody["state"])
            self.assertEqual(3, custody["reservation_retention_action_count"])
            self.assertEqual("2026-08-15T20:15:00Z", custody["earliest_resume_not_before"])
            self.assertEqual(
                [
                    "paid_000000000000000000000001",
                    "paid_000000000000000000000002",
                    "paid_000000000000000000000003",
                ],
                custody["next_due_action_ids"],
            )
            action_ids = inspection["action_inventory"]["actions"]
            self.assertEqual(3, len(action_ids))
            self.assertTrue(all(item["necessary"] for item in action_ids))
            self.assertEqual(
                sorted(item["provider"]["id"] for item in state["spend_ledger"]["actions"]),
                sorted(item["provider_operation_id"] for item in action_ids),
            )

    def test_fresh_process_reads_same_pending_authority_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = hashes(root)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir",
                    str(root),
                    "inspect",
                    "--native-exclusive-access",
                    "declared",
                    "--observed-at",
                    "2026-08-15T20:11:00Z",
                ],
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            inspection = json.loads(completed.stdout)
            self.assertEqual(before, hashes(root))
            self.assertTrue(inspection["observation"]["inventory_valid"])
            self.assertEqual("not_quiescent", inspection["quiescence"]["state"])
            self.assertEqual(
                "release_until_due",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual(
                3,
                sum(
                    item["provider_identity_present"]
                    for item in inspection["action_inventory"]["actions"]
                ),
            )

    def test_closeout_preserves_provider_custody_but_requires_continuation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            result = closeout_run(root, observed_at="2026-08-15T20:12:00Z")
            self.assertEqual("continuation_required", result["disposition"])
            self.assertFalse(result["terminal"]["terminal"])
            self.assertTrue(result["terminal"]["provider_continuation_remains"])
            self.assertTrue(result["terminal"]["local_continuation_remains"])
            self.assertEqual(
                [
                    "paid_000000000000000000000001",
                    "paid_000000000000000000000002",
                    "paid_000000000000000000000003",
                ],
                result["unresolved_action_ids"],
            )
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                [
                    "resp_provider_pending_1",
                    "resp_provider_pending_2",
                    "resp_provider_pending_3",
                ],
                [item["provider"]["id"] for item in persisted["spend_ledger"]["actions"]],
            )

    def test_due_time_makes_local_cycle_runnable_without_releasing_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:15:00Z",
            )
            self.assertEqual(
                "continue_local_cycle",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertTrue(inspection["execution_capacity"]["local_work_ready_now"])
            self.assertIsNone(inspection["execution_capacity"]["resume_not_before"])
            self.assertEqual(
                3,
                inspection["provider_custody"]["reservation_retention_action_count"],
            )

    def test_legacy_pending_action_without_timing_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            for action in state["spend_ledger"]["actions"]:
                action.pop("provider_reconciliation")
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertEqual(
                "unsupported_retain_capacity",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual("unsupported", inspection["provider_custody"]["state"])
            self.assertEqual(3, inspection["provider_custody"]["reservation_retention_action_count"])

    def test_terminal_usage_unavailable_retains_authority_without_polling(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            for action in state["spend_ledger"]["actions"]:
                action["state"] = "REPORTED"
                action["reported"] = {
                    "cost_disposition": (
                        "provider_usage_unavailable_billing_reconciliation_pending"
                    )
                }
                action.pop("provider_reconciliation", None)
            state["status"] = "FINAL_QA_REQUIRES_REVIEW"
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertEqual([], inspection["provider_custody"]["action_ids"])
            self.assertEqual("retain", inspection["consumer_authority"]["state"])
            self.assertEqual(3, inspection["consumer_authority"]["action_count"])
            self.assertTrue(all(
                item["retention_reason"] == "billing_reconciliation_pending"
                and item["cost_disposition"] == (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                )
                for item in inspection["consumer_authority"]["actions"]
            ))
            self.assertNotEqual(
                "release_until_due",
                inspection["execution_capacity"]["disposition"],
            )

    def test_batch_timing_cannot_accidentally_claim_interactive_parity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["binding"]["service_level"] = "batch"
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertEqual(
                "unsupported_retain_capacity",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual("unsupported", inspection["provider_custody"]["state"])

    def test_route_dispatch_identity_is_closed_and_fail_closed(self) -> None:
        exact = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
        }
        response = {
            "binding": {
                "stage": "authoring_initial", "service_level": "interactive",
                "route": "kevin:authoring_initial:001",
            },
            "provider": {"kind": "response", "id": "resp_exact"},
        }
        identity = native_provider_route_identity(exact, response)
        self.assertTrue(identity["valid"])
        self.assertEqual("exact_interactive", identity["adapter"])
        bounded = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "route_contract": "astrowoof.bounded_natal.authoring_run.v1",
            "route": "bounded_natal.v1",
        }
        bounded_response = copy.deepcopy(response)
        bounded_response["binding"]["route"] = "bounded_natal.v1:authoring_initial:1"
        identity = native_provider_route_identity(bounded, bounded_response)
        self.assertTrue(identity["valid"])
        self.assertEqual("bounded_interactive_deferred", identity["adapter"])
        bounded_response["binding"]["service_level"] = "batch"
        bounded_response["provider"]["kind"] = "batch"
        identity = native_provider_route_identity(bounded, bounded_response)
        self.assertFalse(identity["valid"])
        self.assertEqual("bounded_batch_unsupported", identity["adapter"])
        unknown = native_provider_route_identity({"schema_version": "future.v9"})
        self.assertFalse(unknown["valid"])

    def test_exact_interactive_stage_support_and_disabled_optional_guard(self) -> None:
        optional = {"polish", "qualitative_critic", "qualitative_candidate"}
        for stage in (
            "authoring_initial", "creative_retry", "polish",
            "qualitative_critic", "qualitative_candidate",
        ):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                self.materialize(root)
                state = json.loads((root / "run.json").read_text(encoding="utf-8"))
                state["authoring_profile"] = {"qa": {
                    "polish": True,
                    "qualitative_critic": True,
                    "qualitative_candidate": True,
                }}
                for action in state["spend_ledger"]["actions"]:
                    action["binding"]["stage"] = stage
                (root / "run.json").write_text(
                    json.dumps(state, indent=2) + "\n", encoding="utf-8"
                )
                write_workspace_snapshot(root)
                inspection = inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-15T20:10:00Z",
                )
                self.assertEqual(
                    "release_until_due",
                    inspection["execution_capacity"]["disposition"],
                )
                if stage in optional:
                    state["authoring_profile"]["qa"][stage] = False
                    (root / "run.json").write_text(
                        json.dumps(state, indent=2) + "\n", encoding="utf-8"
                    )
                    write_workspace_snapshot(root)
                    disabled = inspect_lifecycle(
                        root, native_exclusive_access="declared",
                        observed_at="2026-08-15T20:10:00Z",
                    )
                    self.assertEqual(
                        "unsupported_retain_capacity",
                        disabled["execution_capacity"]["disposition"],
                    )

    def test_bounded_natal_never_inherits_exact_interactive_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["schema_version"] = "astrowoof.bounded_natal.authoring_run.v1"
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            calls: list[str] = []
            result = reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z",
                retrieve=lambda provider_id, _timeout: calls.append(provider_id) or {},
            )
            self.assertEqual("unsupported", result["outcome"])
            self.assertEqual([], calls)
            self.assertEqual(
                "unsupported_retain_capacity",
                result["inspection"]["execution_capacity"]["disposition"],
            )

    def test_optional_stage_attempt_roots_find_native_completed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            action = state["spend_ledger"]["actions"][0]
            action["provider_reconciliation"].update({
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-15T20:18:00Z",
                "last_outcome": "completed",
                "resume_not_before": None,
            })
            response = {
                "id": action["provider"]["id"],
                "status": "completed",
                "output": [],
            }
            evidence = (
                root / "lifecycle" / "provider-reconciliation" /
                f"{action['action_id']}.response.json"
            )
            evidence.parent.mkdir(parents=True)
            evidence.write_text(json.dumps(response), encoding="utf-8")
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            for attempt_root in (
                root / "final" / "kevin" / "polish" / "attempt-001",
                root / "final" / "kevin" / "qualitative" / "critic",
                root / "final" / "kevin" / "qualitative" / "candidate",
            ):
                with self.subTest(attempt_root=attempt_root):
                    self.assertEqual(
                        response,
                        reconciled_response_evidence(
                            attempt_root, action["provider"]["id"]
                        ),
                    )

    def test_publishable_delivery_can_release_while_nonblocking_critic_is_pending(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["authoring_profile"] = {"qa": {
                "polish": False,
                "qualitative_critic": True,
                "qualitative_candidate": False,
            }}
            for action in state["spend_ledger"]["actions"]:
                action["binding"]["stage"] = "qualitative_critic"
            deck = root / "final" / "kevin" / "deck.json"
            deck.parent.mkdir(parents=True)
            deck.write_text("{}", encoding="utf-8")
            state["status"] = "DELIVERY_COMPLETE"
            state["subjects"] = {"kevin": {
                "state": "DELIVERY_COMPLETE", "deck": str(deck),
            }}
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertTrue(inspection["terminal"]["delivery_publishable"])
            self.assertEqual(
                "release_until_due",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual(
                3,
                inspection["provider_custody"]["reservation_retention_action_count"],
            )

    def test_frozen_backoff_and_monotonic_attempt_evidence(self) -> None:
        self.assertEqual(
            [15, 30, 60, 120, 240, 300, 300],
            [delay_seconds(attempt) for attempt in range(7)],
        )
        timing = initial_timing(recorded_at="2026-08-15T20:00:00Z")
        self.assertEqual("2026-08-15T20:00:15Z", timing["resume_not_before"])
        record_attempt(
            timing, attempted_at="2026-08-15T20:00:15Z", outcome="pending"
        )
        self.assertEqual(1, timing["provider_retrieval_attempt_count"])
        self.assertEqual("2026-08-15T20:00:45Z", timing["resume_not_before"])
        previous = json.loads(json.dumps(timing))
        with self.assertRaises(ValueError):
            record_attempt(
                timing,
                attempted_at="2026-08-15T20:00:14Z",
                outcome="pending",
            )
        self.assertEqual(previous, timing)

    def test_incomplete_checkpoint_can_never_be_declared_releasable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["provider_reconciliation"][
                "resume_not_before"
            ] = "2026-08-15T20:30:00Z"
            # Simulate state persistence succeeding before snapshot publication.
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertFalse(inspection["observation"]["snapshot_complete"])
            self.assertFalse(
                inspection["execution_capacity"]["checkpoint_safe_for_worker_release"]
            )
            self.assertEqual(
                "retain_for_review",
                inspection["execution_capacity"]["disposition"],
            )

    def test_early_cycle_is_strictly_nonmutating_not_due(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = hashes(root)
            calls: list[tuple[str, float]] = []
            result = reconcile_provider_cycle(
                root,
                observed_at="2026-08-15T20:10:00Z",
                retrieve=lambda provider_id, timeout: calls.append(
                    (provider_id, timeout)
                ) or {},
            )
            self.assertEqual("not_due", result["outcome"])
            self.assertEqual([], calls)
            self.assertNotIn("result_checkpoint", result)
            self.assertEqual(before, hashes(root))

    def test_one_due_wave_polls_known_ids_only_and_detaches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            calls: list[tuple[str, float]] = []

            def retrieve(provider_id: str, timeout: float) -> dict:
                calls.append((provider_id, timeout))
                return {"id": provider_id, "status": "in_progress"}

            result = reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z", retrieve=retrieve
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(3, result["cycle"]["provider_retrieval_count"])
            self.assertEqual(
                ["resp_provider_pending_1", "resp_provider_pending_2", "resp_provider_pending_3"],
                sorted(item[0] for item in calls),
            )
            self.assertTrue(all(timeout == 15.0 for _, timeout in calls))
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            for action in persisted["spend_ledger"]["actions"]:
                timing = action["provider_reconciliation"]
                self.assertEqual(1, timing["provider_retrieval_attempt_count"])
                self.assertEqual("pending", timing["last_outcome"])
                self.assertEqual("2026-08-15T20:18:30Z", timing["resume_not_before"])
            self.assertEqual(
                "release_until_due",
                result["inspection"]["execution_capacity"]["disposition"],
            )
            self.assertEqual(13, result["result_checkpoint"]["operator_state_revision"])
            self.assertTrue(result["result_checkpoint"]["result_artifact"]["logical_path"].endswith("cycle-00000013.json"))

    def test_mixed_completed_pending_persists_response_and_requests_local_work(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)

            def retrieve(provider_id: str, _timeout: float) -> dict:
                status = "completed" if provider_id.endswith("_1") else "in_progress"
                return {"id": provider_id, "status": status, "output": []}

            result = reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z", retrieve=retrieve
            )
            self.assertEqual("progressed_local", result["outcome"])
            self.assertEqual(
                ["paid_000000000000000000000001"],
                result["cycle"]["completed_action_ids"],
            )
            self.assertTrue((
                root / "lifecycle" / "provider-reconciliation" /
                "paid_000000000000000000000001.response.json"
            ).is_file())
            cached = reconciled_response_evidence(
                root / "passes" / "pass-1" / "attempt-001",
                "resp_provider_pending_1",
            )
            self.assertEqual("completed", cached["status"])
            self.assertEqual(
                "continue_local_cycle",
                result["inspection"]["execution_capacity"]["disposition"],
            )
            action = next(
                item for item in result["inspection"]["provider_custody"]["actions"]
                if item["action_id"] == "paid_000000000000000000000001"
            )
            self.assertEqual("completed_provider_evidence", action["custody_classification"])
            self.assertIsNone(action["resume_not_before"])

    def test_cycle_limit_retrieves_only_four_of_six_due_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            template = state["spend_ledger"]["actions"][0]
            for index in range(4, 7):
                action = json.loads(json.dumps(template))
                action["action_id"] = f"paid_{index:024d}"
                action["provider"]["id"] = f"resp_provider_pending_{index}"
                action["binding"]["route"] = f"kevin:authoring_initial:{index:03d}"
                action["provider_reconciliation"]["resume_not_before"] = "2026-08-15T20:15:00Z"
                state["spend_ledger"]["actions"].append(action)
            (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(root)
            calls: list[str] = []
            result = reconcile_provider_cycle(
                root,
                observed_at="2026-08-15T20:18:00Z",
                retrieve=lambda provider_id, _timeout: calls.append(provider_id) or {
                    "id": provider_id, "status": "in_progress"
                },
            )
            self.assertEqual(4, len(calls))
            self.assertEqual(4, result["cycle"]["provider_retrieval_count"])
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            untouched = [
                item for item in persisted["spend_ledger"]["actions"]
                if item["provider_reconciliation"]["provider_retrieval_attempt_count"] == 0
            ]
            self.assertEqual(2, len(untouched))

    def test_transport_warning_backs_off_without_losing_provider_custody(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = json.loads((root / "run.json").read_text(encoding="utf-8"))
            result = reconcile_provider_cycle(
                root,
                observed_at="2026-08-15T20:18:00Z",
                retrieve=lambda _provider_id, _timeout: (_ for _ in ()).throw(
                    TimeoutError("fixture transport timeout")
                ),
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(3, len(result["cycle"]["transport_warning_action_ids"]))
            after = json.loads((root / "run.json").read_text(encoding="utf-8"))
            for old, new in zip(
                before["spend_ledger"]["actions"],
                after["spend_ledger"]["actions"],
            ):
                self.assertEqual(old["provider"], new["provider"])
                self.assertEqual(old["authorization"], new["authorization"])
                self.assertEqual(old["consumption"], new["consumption"])
                self.assertEqual("transport_warning", new["provider_reconciliation"]["last_outcome"])

    def test_provider_identity_mismatch_fails_closed_for_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            result = reconcile_provider_cycle(
                root,
                observed_at="2026-08-15T20:18:00Z",
                retrieve=lambda provider_id, _timeout: {
                    "id": provider_id + "-wrong", "status": "in_progress"
                },
            )
            self.assertEqual("review_required", result["outcome"])
            self.assertEqual(
                "retain_for_review",
                result["inspection"]["execution_capacity"]["disposition"],
            )
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertTrue(all(
                item["state"] == "AMBIGUOUS_PROVIDER_SUBMISSION"
                for item in persisted["spend_ledger"]["actions"]
            ))

    def test_four_due_retrievals_run_in_one_parallel_wave(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            rendezvous = threading.Barrier(3, timeout=1.0)
            arrivals: list[str] = []
            guard = threading.Lock()

            def retrieve(provider_id: str, _timeout: float) -> dict:
                with guard:
                    arrivals.append(provider_id)
                rendezvous.wait()
                return {"id": provider_id, "status": "in_progress"}

            reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z", retrieve=retrieve
            )
            self.assertEqual(3, len(arrivals))

    def test_snapshot_publication_failure_never_advertises_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            with patch(
                "astrowoof_natal_authoring.closure.write_workspace_snapshot",
                side_effect=OSError("injected snapshot failure"),
            ):
                with self.assertRaisesRegex(OSError, "injected snapshot failure"):
                    reconcile_provider_cycle(
                        root,
                        observed_at="2026-08-15T20:18:00Z",
                        retrieve=lambda provider_id, _timeout: {
                            "id": provider_id, "status": "in_progress"
                        },
                    )
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:01Z",
            )
            self.assertFalse(inspection["observation"]["snapshot_complete"])
            self.assertFalse(
                inspection["execution_capacity"]["checkpoint_safe_for_worker_release"]
            )
            self.assertEqual(
                "retain_for_review",
                inspection["execution_capacity"]["disposition"],
            )

    def test_public_cli_advertises_bounded_reconciliation(self) -> None:
        completed = subprocess.run(
            [
                sys.executable, "-c",
                "from astrowoof_natal_authoring.closure import main; main()",
                "--help",
            ],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("--bounded-provider-reconciliation", completed.stdout)

    def test_high_level_pending_cycle_emits_checkpoint_observations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)

            class RetrievalProvider:
                name = "openai"
                base_url = "https://api.openai.invalid/v1"
                http_timeout_seconds = 60.0
                max_transport_retries = 4

                def _request_with_retry(inner_self, **_kwargs):
                    return {
                        "id": "resp_provider_pending_1",
                        "status": "in_progress",
                    }, 1

            # Give each lookup its exact durable ID while retaining one bounded
            # scripted transport and no provider submission surface.
            provider = RetrievalProvider()
            def retrieve(**kwargs):
                response_id = str(kwargs["url"]).rsplit("/", 1)[-1]
                return {"id": response_id, "status": "in_progress"}, 1

            provider._request_with_retry = retrieve  # type: ignore[method-assign]
            events: list[dict] = []
            emitter = ExecutionEventEmitter(
                release="test", sink=events.append,
                base_correlation={"native_run_id": "run_provider_pending_capacity_001"},
            )
            result = run_bounded_authoring_reconciliation(
                root,
                provider=provider,
                max_attempts=3,
                python_executable=Path(sys.executable),
                observed_at="2026-08-15T20:18:00Z",
                event_emitter=emitter,
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(
                ["run.detached", "checkpoint.committed"],
                [item["event_name"] for item in events],
            )

    def test_parallel_pending_cohort_has_no_cross_run_process_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cohort = Path(temporary).resolve()
            roots = [cohort / name for name in ("aster", "bramble", "clover")]
            for root in roots:
                root.mkdir()
                self.materialize(root)

            def one_cycle(root: Path) -> dict:
                return reconcile_provider_cycle(
                    root,
                    observed_at="2026-08-15T20:18:00Z",
                    retrieve=lambda provider_id, _timeout: {
                        "id": provider_id, "status": "in_progress"
                    },
                )

            with ThreadPoolExecutor(max_workers=2) as pool:
                waiting = list(pool.map(one_cycle, roots[:2]))
            self.assertTrue(all(
                item["outcome"] == "detached_provider_pending"
                and item["inspection"]["execution_capacity"]["disposition"]
                == "release_until_due"
                for item in waiting
            ))
            third = inspect_lifecycle(
                roots[2],
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:00Z",
            )
            self.assertEqual(
                "continue_local_cycle",
                third["execution_capacity"]["disposition"],
            )
            for root in roots[:2]:
                persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
                self.assertTrue(all(
                    action["provider"]["id"].startswith("resp_provider_pending_")
                    and action["authorization"]["authorization_reference"].startswith(
                        "api-reservation-"
                    )
                    for action in persisted["spend_ledger"]["actions"]
                ))


if __name__ == "__main__":
    unittest.main()
