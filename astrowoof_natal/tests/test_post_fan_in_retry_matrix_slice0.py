from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import (
    SpendController,
    normalized_path,
    public_run_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.lifecycle_contracts import (
    validate_lifecycle_inspection_v05,
)
from astrowoof_natal_authoring.temporal_lifecycle import (
    build_lifecycle_inspection_v06,
)
from astrowoof_natal_authoring.spend import AwaitingSpendAuthorization, digest


def _binding(run_id: str, stage: str, route: str, revision: int) -> dict:
    return {
        "run_id": run_id,
        "profile_sha256": "a" * 64,
        "prepared_state_revision": revision,
        "stage": stage,
        "route": route,
        "request_sha256": "b" * 64,
        "model": "scripted-provider",
        "service_level": "interactive",
        "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def _workspace(root: Path, route_family: str) -> tuple[Path, str, str]:
    run_dir = root / route_family
    run_dir.mkdir()
    run_id = f"slice0-{route_family}"
    prefix = "bounded_natal.v2:" if route_family == "bounded_natal" else ""
    actions = []
    for number in range(1, 7):
        actions.append({
            "action_id": f"paid_{number:024x}",
            "state": "REPORTED",
            "binding": _binding(
                run_id, "authoring_initial",
                f"{prefix}pass-{number}:attempt-001", 1,
            ),
            "provider": {
                "id": f"resp_{route_family}_initial_{number}",
                "kind": "response",
            },
            "reported": {"estimated_micro_usd": 0},
        })
    retry_one = "paid_000000000000000000000101"
    retry_two = "paid_000000000000000000000102"
    actions.extend((
        {
            "action_id": retry_one,
            "state": "WAITING",
            "binding": _binding(
                run_id, "creative_retry",
                f"{prefix}pass-1:attempt-002", 7,
            ),
            "provider": {"id": f"resp_{route_family}_retry_1", "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-25T23:42:00Z",
                "last_outcome": "completed",
                "resume_not_before": None,
            },
            "reported": None,
        },
        {
            "action_id": retry_two,
            "state": "PREPARED",
            "binding": _binding(
                run_id, "creative_retry",
                f"{prefix}pass-1:attempt-003", 8,
            ),
        },
    ))
    state = {
        "schema_version": (
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal"
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        "run_id": run_id,
        "state_revision": 8,
        "created_at": "2026-08-25T23:38:00Z",
        "updated_at": "2026-08-25T23:42:52Z",
        "provider": "fake",
        "provider_configuration": {},
        "max_attempts": 3,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "policy": {
                "currency": "USD",
                "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 100000000,
                "stage_ceilings_micro_usd": {
                    "authoring_initial": 100000000,
                    "creative_retry": 100000000,
                    "polish": 100000000,
                    "qualitative_critic": 100000000,
                    "qualitative_candidate": 100000000,
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip",
                    "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            },
            "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {
            "pass-1": {
                "pass_id": "pass-1",
                "state": "AWAITING_SPEND_AUTHORIZATION",
                "attempts": [
                    {"attempt_number": 1, "state": "PASS_QA_REJECTED"},
                    {"attempt_number": 2, "state": "WAITING_FOR_RESPONSE"},
                    {"attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION"},
                ],
            }
        },
        "subjects": {},
        "provenance": {},
    }
    if route_family == "bounded_natal":
        state.update({
            "route": "bounded_natal.v2",
            "route_contract": "astrowoof.bounded_natal.authoring_run.v2",
            "service_level": "interactive",
        })
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)
    return run_dir, retry_one, retry_two


class PostFanInRetrySlice0Tests(unittest.TestCase):
    def test_ordinary_retry_cycle_can_republish_same_decision_without_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _retry_one, retry_two = _workspace(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            payload = {"model": "scripted-provider", "input": "slice-0-retry"}
            retry = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == retry_two
            )
            retry["binding"]["request_sha256"] = digest(payload)
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(
                json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)
            before = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            controller = SpendController(
                state=state, run_json=run_json, state_lock=threading.Lock(),
                consumer_id="slice-0-characterization",
            )
            before_submit, _provider_created = controller.callbacks(
                stage="creative_retry", route="pass-1:attempt-003",
                model="scripted-provider", service_level="interactive",
                maximum_output_tokens=1000,
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                before_submit(payload)
            self.assertEqual("PREPARED", retry["state"])
            self.assertIsNone(retry.get("provider"))
            state["state_revision"] += 1
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(
                json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:01Z",
            )
            self.assertEqual("ordinary_resume", before["execution_branch"]["command"])
            self.assertEqual("ordinary_resume", after["execution_branch"]["command"])
            self.assertEqual(before["local_dependencies"], after["local_dependencies"])
            self.assertNotEqual(
                before["observation"]["snapshot_sha256"],
                after["observation"]["snapshot_sha256"],
            )
            self.assertEqual([], after["provider_custody"]["next_due_action_ids"])

    def test_completed_retry_masks_prepared_retry_with_unqualified_local_resume(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family), tempfile.TemporaryDirectory() as temporary:
                run_dir, retry_one, retry_two = _workspace(Path(temporary), route_family)
                first = inspect_lifecycle(
                    run_dir, native_exclusive_access="declared",
                    observed_at="2026-08-25T23:43:00Z",
                )
                second = inspect_lifecycle(
                    run_dir, native_exclusive_access="declared",
                    observed_at="2026-08-25T23:43:00Z",
                )
                validate_lifecycle_inspection_v05(first)
                validate_lifecycle_inspection_v05(second)
                self.assertEqual("ordinary_resume", first["execution_branch"]["command"])
                self.assertEqual("ordinary_local_continuation_ready", first["execution_branch"]["reason_code"])
                self.assertEqual([], first["execution_branch"]["action_ids"])
                self.assertEqual([], first["provider_custody"]["next_due_action_ids"])
                self.assertEqual(
                    [retry_one], first["provider_custody"]["action_ids"]
                )
                self.assertEqual(
                    "completed_evidence_pending_local_work",
                    first["provider_custody"]["state"],
                )
                self.assertEqual(
                    [{
                        "kind": "local_assembly", "blocking": True,
                        "reason_code": "provider_evidence_ingestion_required",
                    }],
                    first["local_dependencies"],
                )
                self.assertEqual(first, second)
                self.assertEqual(
                    build_lifecycle_inspection_v06(first)["checkpoint_basis_sha256"],
                    build_lifecycle_inspection_v06(second)["checkpoint_basis_sha256"],
                )
                prepared = next(
                    action for action in first["action_inventory"]["actions"]
                    if action["action_id"] == retry_two
                )
                self.assertEqual("PREPARED", prepared["state"])

    def test_completed_retry_ingestion_exposes_exact_next_retry_authority(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family), tempfile.TemporaryDirectory() as temporary:
                run_dir, retry_one, retry_two = _workspace(Path(temporary), route_family)
                state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == retry_one
                )
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
                state["state_revision"] += 1
                (run_dir / "run.json").write_text(
                    json.dumps(state, indent=2) + "\n", encoding="utf-8"
                )
                (run_dir / "public-run.json").write_text(
                    json.dumps(public_run_state(state), indent=2) + "\n",
                    encoding="utf-8",
                )
                write_workspace_snapshot(run_dir)
                inspection = inspect_lifecycle(
                    run_dir, native_exclusive_access="declared",
                    observed_at="2026-08-25T23:44:00Z",
                )
                validate_lifecycle_inspection_v05(inspection)
                self.assertEqual(
                    "await_external_authority",
                    inspection["execution_branch"]["command"],
                )
                self.assertEqual(
                    [retry_two], inspection["execution_branch"]["action_ids"]
                )

    def test_pending_and_ambiguous_retry_precedence_remains_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            first = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == retry_one
            )
            first["provider_reconciliation"]["last_outcome"] = "pending"
            first["provider_reconciliation"]["resume_not_before"] = "2099-01-01T00:00:00Z"
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            pending = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:44:00Z",
            )
            self.assertEqual("provider_reconciliation_cycle", pending["execution_branch"]["command"])
            self.assertFalse(pending["execution_branch"]["eligible_now"])

            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            first = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == retry_one)
            first["state"] = "SUBMITTING"
            first["provider"] = None
            state["status"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
            state["state_revision"] += 1
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            ambiguous = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:45:00Z",
            )
            self.assertEqual("none", ambiguous["execution_branch"]["command"])
            self.assertEqual("retain_for_review", ambiguous["execution_capacity"]["disposition"])


if __name__ == "__main__":
    unittest.main()
