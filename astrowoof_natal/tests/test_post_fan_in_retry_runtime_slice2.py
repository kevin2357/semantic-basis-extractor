from __future__ import annotations

import json
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.cli import lifecycle as lifecycle_cli
from astrowoof_natal_authoring.closure import save_state
from astrowoof_natal_authoring.post_fan_in_contracts import (
    commit_local_work_progress,
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _workspace
from astrowoof_natal_authoring.spend import AwaitingSpendAuthorization


class _FailingEmitter:
    def emit(self, *args, **kwargs):
        raise RuntimeError("sentinel event sink failure")


class PostFanInRetryRuntimeSlice2Tests(unittest.TestCase):
    def test_public_cli_emits_v07_and_real_resume_advances_to_retry_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir, retry_one, retry_two = _workspace(Path(temp), "exact_natal")
            legacy_stdout = io.StringIO()
            with patch.object(sys, "argv", [
                "astrowoof-lifecycle", "--run-dir", str(run_dir), "inspect",
                "--native-exclusive-access", "declared", "--observed-at",
                "2026-08-25T23:43:00Z",
            ]), patch("sys.stdout", legacy_stdout):
                lifecycle_cli.main()
            legacy = json.loads(legacy_stdout.getvalue())
            self.assertEqual("astrowoof.authoring_lifecycle_inspection.v0.5", legacy["schema_version"])
            self.assertEqual("none", legacy["execution_branch"]["command"])
            self.assertIn("local_work_contract_upgrade_required", legacy["review_reasons"])

            stdout = io.StringIO()
            with patch.object(sys, "argv", [
                "astrowoof-lifecycle", "--run-dir", str(run_dir),
                "inspect-local-work", "--native-exclusive-access", "declared",
                "--observed-at", "2026-08-25T23:43:00Z",
            ]), patch("sys.stdout", stdout):
                lifecycle_cli.main()
            before = json.loads(stdout.getvalue())
            self.assertEqual(
                "astrowoof.authoring_lifecycle_inspection.v0.7",
                before["schema_version"],
            )
            self.assertEqual("ordinary_resume", before["temporal_decision"]["selected_command"])
            operation_key = before["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]["operation_key"]

            def real_local_fan_in(**kwargs):
                state = kwargs["state"]
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == retry_one
                )
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
                save_state(kwargs["run_json"], state)
                raise AwaitingSpendAuthorization(
                    "fresh retry authority required",
                    action=next(
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] == retry_two
                    ),
                )

            with patch.object(sys, "argv", [
                "astrowoof-run-semantic-closure", "--run-dir", str(run_dir),
                "--resume", "--provider", "fake", "--max-attempts", "3",
            ]), patch.object(
                closure, "author_pending_passes", side_effect=real_local_fan_in,
            ), self.assertRaises(AwaitingSpendAuthorization):
                closure.main()

            after = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-25T23:44:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual("await_external_authority", after["temporal_decision"]["selected_command"])
            self.assertEqual(
                [operation_key], after["checkpoint_basis"]["local_work_inventory"]["consumed_operation_keys"]
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            prepared = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == retry_two
            )
            self.assertEqual("PREPARED", prepared["state"])
            self.assertIsNone(prepared.get("provider"))

    def test_real_inventory_selects_completed_retry_for_exact_and_bounded(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, _retry_two = _workspace(Path(temp), route_family)
                inspection = inspect_post_fan_in_lifecycle(
                    run_dir, observed_at="2026-08-25T23:43:00Z",
                    native_exclusive_access="declared",
                )
                validate_lifecycle_inspection_v07(inspection)
                inventory = inspection["checkpoint_basis"]["local_work_inventory"]
                self.assertEqual("ordinary_resume", inspection["temporal_decision"]["selected_command"])
                self.assertEqual(1, len(inventory["operations"]))
                self.assertEqual(
                    "provider_result_fan_in_and_retry_evaluation",
                    inventory["operations"][0]["kind"],
                )
                self.assertEqual([retry_one], inventory["operations"][0]["source_action_ids"])

    def test_noop_progress_refuses_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir, _retry_one, _retry_two = _workspace(Path(temp), "exact_natal")
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-25T23:43:00Z",
                native_exclusive_access="declared",
            )
            run_before = (run_dir / "run.json").read_bytes()
            snapshot_before = (run_dir / "workspace-snapshot.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "did not consume"):
                commit_local_work_progress(
                    run_dir, prior=prior, observed_at="2026-08-25T23:43:01Z",
                )
            self.assertEqual(run_before, (run_dir / "run.json").read_bytes())
            self.assertEqual(snapshot_before, (run_dir / "workspace-snapshot.json").read_bytes())

    def test_completed_fan_in_seals_consumption_then_selects_retry_authority(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                prior = inspect_post_fan_in_lifecycle(
                    run_dir, observed_at="2026-08-25T23:43:00Z",
                    native_exclusive_access="declared",
                )
                operation_key = prior["checkpoint_basis"]["local_work_inventory"][
                    "operations"
                ][0]["operation_key"]
                state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
                reconciled = next(
                    action for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == retry_one
                )
                reconciled["state"] = "REPORTED"
                reconciled["reported"] = {"estimated_micro_usd": 0}
                save_state(run_dir / "run.json", state)
                successor = commit_local_work_progress(
                    run_dir, prior=prior, observed_at="2026-08-25T23:44:00Z",
                    event_emitter=_FailingEmitter(),
                )
                self.assertEqual(
                    "await_external_authority",
                    successor["temporal_decision"]["selected_command"],
                )
                inventory = successor["checkpoint_basis"]["local_work_inventory"]
                self.assertEqual([], inventory["operations"])
                self.assertEqual([operation_key], inventory["consumed_operation_keys"])
                persisted = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
                self.assertEqual(
                    [operation_key],
                    persisted["local_work_progress"]["consumed_operation_keys"],
                )
                prepared = next(
                    action for action in persisted["spend_ledger"]["actions"]
                    if action["action_id"] == retry_two
                )
                self.assertEqual("PREPARED", prepared["state"])
                self.assertIsNone(prepared.get("provider"))

    def test_pending_provider_custody_never_advertises_local_work(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir, retry_one, _retry_two = _workspace(Path(temp), "exact_natal")
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == retry_one
            )
            action["provider_reconciliation"]["last_outcome"] = "pending"
            action["provider_reconciliation"]["resume_not_before"] = "2099-01-01T00:00:00Z"
            save_state(run_dir / "run.json", state)
            inspection = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-25T23:43:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                inspection["temporal_decision"]["selected_command"],
            )
            self.assertEqual(
                [], inspection["checkpoint_basis"]["local_work_inventory"]["operations"]
            )


if __name__ == "__main__":
    unittest.main()
