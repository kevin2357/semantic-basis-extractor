from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import retry_feedback_from_record
from astrowoof_natal_authoring.retry_lineage_contracts import (
    assert_retry_lineage_forward_dispatch_safe,
    inspect_retry_lineage_lifecycle,
)
from astrowoof_natal.tests.test_review_required_pending_retries_investigation_slice2 import (
    _persist, _retained_topology,
)


class RetryLineageRuntimeSlice45Tests(unittest.TestCase):
    def test_public_cli_emits_valid_mixed_custody_v08(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _ids = _retained_topology(
                Path(temporary), "generic_qa_reject",
            )
            environment = dict(os.environ)
            source = str(Path(__file__).resolve().parents[1] / "src")
            environment["PYTHONPATH"] = source + os.pathsep + environment.get("PYTHONPATH", "")
            completed = subprocess.run([
                sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
                "--run-dir", str(run_dir), "inspect-retry-lineage",
                "--native-exclusive-access", "declared",
                "--observed-at", "2026-08-28T06:31:00Z",
            ], check=True, capture_output=True, text=True, env=environment)
            result = json.loads(completed.stdout)
            self.assertEqual("astrowoof.authoring_lifecycle_inspection.v0.8", result["schema_version"])
            self.assertEqual("provider_reconciliation_cycle", result["temporal_decision"]["selected_command"])

    def test_mixed_conflict_reconciles_then_becomes_typed_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, ids = _retained_topology(
                Path(temporary), "generic_qa_reject",
            )
            due = inspect_retry_lineage_lifecycle(
                run_dir, observed_at="2026-08-28T06:31:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                due["temporal_decision"]["selected_command"],
            )
            lineage = due["checkpoint_basis"]["retry_lineage_inventory"]
            self.assertEqual("conflict", lineage["status"])
            self.assertFalse(lineage["forward_dispatch_permitted"])
            self.assertTrue(lineage["reconciliation_permitted"])
            self.assertIn(
                ids["pending_attempt_two"],
                due["checkpoint_basis"]["provider_custody"]["action_ids"],
            )

            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            pending = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == ids["pending_attempt_two"]
            )
            pending["state"] = "REPORTED"
            pending["reported"] = {"estimated_micro_usd": 0}
            _persist(run_dir, state)
            review = inspect_retry_lineage_lifecycle(
                run_dir, observed_at="2026-08-28T06:32:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual("none", review["temporal_decision"]["selected_command"])
            self.assertEqual(
                "retain_for_review",
                review["temporal_decision"]["capacity_disposition"],
            )
            self.assertEqual(
                "retry_lineage_conflict_requires_review",
                review["checkpoint_basis"]["retry_lineage_inventory"][
                    "conflict_classification"
                ],
            )

    def test_whole_ledger_conflict_blocks_forward_dispatch_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _ids = _retained_topology(
                Path(temporary), "generic_qa_reject",
            )
            before = (run_dir / "run.json").read_bytes()
            state = json.loads(before)
            with self.assertRaisesRegex(ValueError, "conflict blocks"):
                assert_retry_lineage_forward_dispatch_safe(state)
            self.assertEqual(before, (run_dir / "run.json").read_bytes())

    def test_feedback_uses_completed_predecessors_not_current_row(self) -> None:
        rejected = {
            "attempt_number": 2, "state": "PASS_QA_REJECTED",
            "finished_at": "2026-08-28T06:02:00Z",
            "qa": {"report": {
                "status": "reject", "editorial_issue_codes": ["generic_qa_reject"],
                "affected_claim_ids": ["fixture-claim"], "guidance": "repair it",
            }},
        }
        current = {
            "attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION",
            "finished_at": None, "qa": None,
        }
        record = {"attempts": [copy.deepcopy(rejected), current]}
        feedback = retry_feedback_from_record(record, before_attempt_number=3)
        self.assertEqual("editorial_qa_rejection", feedback["kind"])
        self.assertEqual(["generic_qa_reject"], feedback["editorial_issue_codes"])
        self.assertEqual([2], [item["attempt_number"] for item in feedback["prior_rejections"]])


if __name__ == "__main__":
    unittest.main()
