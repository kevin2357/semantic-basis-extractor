from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import astrowoof_natal_authoring as public

from astrowoof_natal_authoring.closure import (
    normalized_path, write_workspace_snapshot,
)
from astrowoof_natal_authoring.operator_disposition import (
    read_operator_disposition_assessment,
    validate_operator_disposition_assessment,
)
from astrowoof_natal.tests import test_provider_pending_observation_idempotency as pending_fixtures
from astrowoof_natal.tests import test_operator_retirement_contract as retirement_fixtures
from astrowoof_natal_authoring.operator_retirement import (
    build_operator_retirement_request, execute_operator_retirement,
)


def _bytes(root: Path) -> dict[str, bytes]:
    return {
        item.relative_to(root).as_posix(): item.read_bytes()
        for item in root.rglob("*") if item.is_file()
    }


def _ensure_lock(root: Path) -> None:
    lock = root / "spend-consumption.lock"
    if not lock.exists():
        lock.write_bytes(b"0")


class OperatorDispositionReaderSlice2Tests(unittest.TestCase):
    def test_root_level_public_reader_surface_is_exported(self):
        for name in (
            "build_operator_disposition_assessment",
            "logical_workspace_root_id",
            "read_operator_disposition_assessment",
            "read_operator_disposition_assessment_schema",
            "validate_operator_disposition_assessment",
        ):
            self.assertTrue(callable(getattr(public, name)))

    def test_provider_pending_reader_is_snapshot_bound_and_nonmutating(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            pending_fixtures.TestProviderPendingObservationIdempotencySlice0().materialize(root)
            _ensure_lock(root)
            write_workspace_snapshot(root)
            before = _bytes(root)
            first = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            second = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual(first, second)
            self.assertEqual("provider_pending_known_identity", first["native_custody_class"])
            self.assertEqual("permitted", first["quarantine_posture"])
            self.assertEqual(["provider_reconciliation_cycle"], first["supported_next_actions"])
            self.assertEqual(6, first["custody_summary"]["provider_identity_count"])
            self.assertEqual(before, _bytes(root))
            validate_operator_disposition_assessment(first)

    def test_missing_existing_writer_fence_fails_closed_without_creating_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = {
                "schema_version": "astrowoof.semantic_closure_run.v0.9",
                "run_id": "run_quarantine_fixture_1",
                "state_revision": 3,
                "status": "POLICY_STOPPED",
                "updated_at": "2026-08-31T12:00:00+00:00",
                "workspace_contract": {
                    "mode": "stable_logical_absolute_path",
                    "logical_root": normalized_path(root),
                },
                "terminal_transition": {
                    "outcome": "terminalized",
                    "terminal_outcome": "policy_stopped",
                    "terminal_reason": "native_policy_stop",
                },
                "spend_ledger": {"actions": []},
                "passes": {}, "subjects": {},
            }
            root.mkdir(parents=True, exist_ok=True)
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            write_workspace_snapshot(root)
            before = _bytes(root)
            result = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual("unsupported_or_inconsistent", result["native_custody_class"])
            self.assertEqual("prohibited", result["quarantine_posture"])
            self.assertEqual([], result["supported_next_actions"])
            self.assertIn("writer_exclusivity_unestablished", result["evidence_categories"])
            self.assertFalse((root / "spend-consumption.lock").exists())
            self.assertEqual(before, _bytes(root))

    def test_existing_fence_allows_provider_free_quiescent_assessment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = {
                "schema_version": "astrowoof.semantic_closure_run.v0.9",
                "run_id": "run_quarantine_fixture_2",
                "state_revision": 3,
                "status": "POLICY_STOPPED",
                "updated_at": "2026-08-31T12:00:00+00:00",
                "workspace_contract": {
                    "mode": "stable_logical_absolute_path",
                    "logical_root": normalized_path(root),
                },
                "terminal_transition": {
                    "outcome": "terminalized",
                    "terminal_outcome": "policy_stopped",
                    "terminal_reason": "native_policy_stop",
                },
                "spend_ledger": {"actions": []},
                "passes": {}, "subjects": {},
            }
            root.mkdir(parents=True, exist_ok=True)
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            _ensure_lock(root)
            write_workspace_snapshot(root)
            before = _bytes(root)
            result = read_operator_disposition_assessment(
                root, allow_availability_recovery=False,
            )
            self.assertEqual("provider_free_quiescent", result["native_custody_class"])
            self.assertEqual("permitted", result["quarantine_posture"])
            self.assertEqual([], result["supported_next_actions"])
            self.assertEqual(before, _bytes(root))

    def test_exact_result_reader_join_selects_sealed_terminal_ingress(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = retirement_fixtures.TestOperatorRetirementContract().materialize(
                Path(temporary) / "run"
            )
            request = build_operator_retirement_request(
                root, operator_audit_reference="api:quarantine-fixture:001",
            )
            retired = execute_operator_retirement(
                root, request, committed_at="2026-08-31T13:00:00+00:00",
            )
            result_id = retired["native_result"]["result_id"]
            before = _bytes(root)
            assessment = read_operator_disposition_assessment(
                root, terminal_result_id=result_id,
                allow_availability_recovery=False,
            )
            self.assertEqual("sealed_terminal", assessment["native_custody_class"])
            self.assertEqual(["terminal_result_ingress"], assessment["supported_next_actions"])
            self.assertEqual(result_id, assessment["terminal_evidence"]["result_id"])
            self.assertEqual("invocation_result", assessment["terminal_evidence"]["discovery_mode"])
            self.assertEqual(before, _bytes(root))

    def test_default_reader_does_not_discover_terminal_result_availability(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = retirement_fixtures.TestOperatorRetirementContract().materialize(
                Path(temporary) / "run"
            )
            request = build_operator_retirement_request(
                root, operator_audit_reference="api:quarantine-fixture:default",
            )
            execute_operator_retirement(
                root, request, committed_at="2026-08-31T13:00:00+00:00",
            )
            before = _bytes(root)
            with patch(
                "astrowoof_natal_authoring.native_transition_availability."
                "read_native_transition_result_availability"
            ) as availability_reader:
                assessment = read_operator_disposition_assessment(root)
            availability_reader.assert_not_called()
            self.assertIsNone(assessment["terminal_evidence"])
            self.assertEqual(
                "unsupported_or_inconsistent",
                assessment["native_custody_class"],
            )
            self.assertEqual("prohibited", assessment["quarantine_posture"])
            self.assertEqual([], assessment["supported_next_actions"])
            self.assertEqual(before, _bytes(root))


if __name__ == "__main__":
    unittest.main()
