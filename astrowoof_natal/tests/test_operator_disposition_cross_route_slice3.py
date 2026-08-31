from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import write_workspace_snapshot
from astrowoof_natal_authoring.operator_disposition import (
    read_operator_disposition_assessment,
)
from astrowoof_natal.tests import test_provider_pending_observation_idempotency as lifecycle_fixtures


def _files(root: Path) -> dict[str, bytes]:
    return {
        item.relative_to(root).as_posix(): item.read_bytes()
        for item in root.rglob("*") if item.is_file()
    }


def _lock_and_snapshot(root: Path) -> None:
    lock = root / "spend-consumption.lock"
    if not lock.exists():
        lock.write_bytes(b"0")
    write_workspace_snapshot(root)


class OperatorDispositionCrossRouteSlice3Tests(unittest.TestCase):
    def test_exact_bounded_interactive_and_batch_pending_routes(self):
        fixture = lifecycle_fixtures.TestTemporalLifecycleCrossRouteSlice3()
        for route in (
            "exact_interactive", "exact_batch", "bounded_interactive",
            "bounded_batch",
        ):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                fixture.materialize_route(root, route)
                _lock_and_snapshot(root)
                before = _files(root)
                value = read_operator_disposition_assessment(
                    root, allow_availability_recovery=False,
                )
                self.assertEqual(
                    "bounded_natal" if route.startswith("bounded") else "exact_natal",
                    value["route"]["family"],
                )
                self.assertEqual("provider_pending_known_identity", value["native_custody_class"])
                self.assertEqual(["provider_reconciliation_cycle"], value["supported_next_actions"])
                self.assertEqual(before, _files(root))

    def test_completed_evidence_dominates_separate_pending_custody(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            lifecycle_fixtures.TestProviderPendingObservationIdempotencySlice0().materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["provider_reconciliation"].update({
                "last_outcome": "completed",
                "resume_not_before": "2026-08-15T20:30:00Z",
            })
            state["state_revision"] += 1
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            _lock_and_snapshot(root)
            result = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual("completed_unadopted", result["native_custody_class"])
            self.assertEqual("native_prior_action_required", result["quarantine_posture"])
            self.assertEqual(1, result["custody_summary"]["completed_unadopted_count"])
            self.assertEqual(6, result["custody_summary"]["provider_identity_count"])

    def test_ambiguity_dominates_known_provider_custody(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            lifecycle_fixtures.TestProviderPendingObservationIdempotencySlice0().materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "SUBMITTING"
            action["provider"] = None
            action["provider_reconciliation"] = None
            state["state_revision"] += 1
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            _lock_and_snapshot(root)
            result = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual("submission_ambiguous", result["native_custody_class"])
            self.assertEqual(["operator_review", "fresh_disposition_assessment"], result["supported_next_actions"])
            self.assertEqual(1, result["custody_summary"]["ambiguous_submission_count"])
            self.assertGreater(result["custody_summary"]["provider_identity_count"], 0)

    def test_legacy_bounded_batch_is_explicitly_unsupported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            fixture = lifecycle_fixtures.TestTemporalLifecycleCrossRouteSlice3()
            fixture.materialize_route(root, "bounded_batch")
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v1"
            state["route"] = "bounded_natal.v1"
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            _lock_and_snapshot(root)
            value = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual("unsupported_or_inconsistent", value["native_custody_class"])
            self.assertEqual("prohibited", value["quarantine_posture"])
            self.assertIn("provider_custody_unjoinable", value["evidence_categories"])


if __name__ == "__main__":
    unittest.main()
