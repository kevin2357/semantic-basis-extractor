from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import save_state
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
)
from astrowoof_natal_authoring.post_fan_in_retry_qa import _binding, _materialize
from astrowoof_natal_authoring.reconciliation import reconcile_provider_cycle


class MixedProviderCustodySlice4BTests(unittest.TestCase):
    def test_completed_later_retry_selects_local_fan_in_while_first_remains_pending(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, first, _prepared = _materialize(Path(temporary))
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            later = "paid_000000000000000000000103"
            state["spend_ledger"]["actions"].append({
                "action_id": later,
                "state": "WAITING",
                "binding": _binding(state["run_id"], "pass-2:attempt-002", 7),
                "provider": {"id": "resp_fixture_retry_other", "kind": "response"},
                "provider_reconciliation": {
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                    "provider_retrieval_attempt_count": 1,
                    "last_attempt_at": "2026-08-27T11:59:00Z",
                    "last_outcome": "pending",
                    "resume_not_before": "2026-08-27T12:01:00Z",
                },
                "reported": None,
            })
            state["passes"]["pass-2"] = {
                "pass_id": "pass-2",
                "state": "WAITING_FOR_RESPONSE",
                "attempts": [
                    {"attempt_number": 1, "state": "PASS_QA_REJECTED"},
                    {"attempt_number": 2, "state": "WAITING_FOR_RESPONSE"},
                ],
            }
            save_state(state_path, state)
            retrieved: list[str] = []

            def retrieve(provider_id: str, _timeout: float) -> dict:
                retrieved.append(provider_id)
                if provider_id == "resp_fixture_retry_1":
                    return {"id": provider_id, "status": "in_progress"}
                return {"id": provider_id, "status": "completed", "output": []}

            result = reconcile_provider_cycle(
                run_dir,
                observed_at="2026-08-27T12:01:00Z",
                retrieve=retrieve,
            )
            self.assertEqual("progressed_local", result["outcome"])
            self.assertEqual(
                ["resp_fixture_retry_1", "resp_fixture_retry_other"], retrieved,
            )
            inspection = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-08-27T12:01:01Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "ordinary_resume",
                inspection["temporal_decision"]["selected_command"],
            )
            operations = inspection["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ]
            self.assertEqual(1, len(operations))
            self.assertEqual([later], operations[0]["source_action_ids"])
            custody = inspection["checkpoint_basis"]["provider_custody"]
            self.assertEqual("known_operations_pending", custody["state"])
            self.assertEqual([first, later], custody["action_ids"])


if __name__ == "__main__":
    unittest.main()
