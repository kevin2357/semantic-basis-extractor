"""Provider-free contract tests for finalization terminal dominance."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.closure import finalization_conclusion  # noqa: E402
from astrowoof_natal_authoring.lifecycle import _capacity_and_custody  # noqa: E402


class TestTerminalDominanceSlice1(unittest.TestCase):
    def _state(self, subject_state: str) -> dict:
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "terminal-dominance-fixture",
            "route_contract": "astrowoof.semantic_closure_run.v0.9",
            "status": "AUTHORING",
            "subjects": {"fixture": {"state": subject_state}},
            "spend_ledger": {"actions": []},
        }

    @staticmethod
    def _observation() -> dict:
        return {
            "snapshot_complete": True,
            "inventory_valid": True,
            "native_exclusive_access": "established",
            "writer_race_possible": False,
        }

    def test_complete_delivery_and_final_qa_failure_are_evidence_conclusions(self) -> None:
        self.assertEqual(
            "delivery_complete",
            finalization_conclusion(self._state("DELIVERY_COMPLETE")),
        )
        self.assertEqual(
            "review_required",
            finalization_conclusion(self._state("FINAL_QA_FAILED")),
        )

    def test_completed_finalization_refuses_local_successor_work(self) -> None:
        capacity, custody, _route, _authority = _capacity_and_custody(
            self._state("DELIVERY_COMPLETE"),
            self._observation(),
            [{"kind": "post_finalization_local_successor", "reason_code": "fixture"}],
            observed_at="2026-09-04T14:00:00Z",
        )
        self.assertEqual("retain_for_review", capacity["disposition"])
        self.assertFalse(capacity["local_work_ready_now"])
        self.assertEqual("native_review_required", capacity["reason_code"])
        self.assertEqual("none", custody["state"])

    def test_completed_finalization_without_custody_is_terminal(self) -> None:
        capacity, _custody, _route, _authority = _capacity_and_custody(
            self._state("FINAL_QA_FAILED"), self._observation(), [],
            observed_at="2026-09-04T14:00:00Z",
        )
        self.assertEqual("terminal", capacity["disposition"])
        self.assertFalse(capacity["local_work_ready_now"])


if __name__ == "__main__":
    unittest.main()
