"""Slice 0 characterization for the Frisbee/Hype polish handoff seam."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.temporal_lifecycle import (  # noqa: E402
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
)


class TestPolishAuthorityHandoffSlice0(unittest.TestCase):
    def _state(self, root: Path, *, prepared_polish: bool) -> dict:
        actions = []
        status = "FINAL_QA_REQUIRES_REVIEW"
        if prepared_polish:
            status = "AWAITING_SPEND_AUTHORIZATION"
            actions.append({
                "action_id": "paid_0123456789abcdef01234567",
                "state": "PREPARED",
                "binding": {
                    "run_id": "run_polish_handoff_001",
                    "profile_sha256": "1" * 64,
                    "prepared_state_revision": 53,
                    "stage": "polish",
                    "route": "fixture:polish:001",
                    "request_sha256": "2" * 64,
                    "model": "gpt-5.6-luna",
                    "service_level": "interactive",
                    "maximum_output_tokens": 100000,
                    "commitment_micro_usd": 1,
                    "price_book_version": "openai-public-2026-08-07.v1",
                },
                "authorization": None,
                "provider": None,
                "reported": None,
            })
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_polish_handoff_001",
            "state_revision": 53,
            "updated_at": "2026-09-04T23:41:59Z",
            "status": status,
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": actions},
            "passes": {},
            "subjects": {"fixture": {
                "subject": "fixture",
                "state": "FINAL_QA_WARN",
                "polish_attempts": ([{
                    "attempt_number": 1,
                    "state": "SUBMITTED",
                    "paid_action_id": "paid_0123456789abcdef01234567",
                }] if prepared_polish else []),
            }},
        }

    @staticmethod
    def _inspect(root: Path, state: dict) -> dict:
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        return inspect_lifecycle(
            root,
            native_exclusive_access="established",
            observed_at="2026-09-04T23:42:00Z",
        )

    def test_exact_prepared_polish_projects_one_v2_authority_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            result = self._inspect(root, self._state(root, prepared_polish=True))

            self.assertEqual(
                "await_external_authority",
                result["execution_capacity"]["disposition"],
            )
            self.assertEqual(
                "await_external_authority", result["execution_branch"]["command"]
            )
            self.assertEqual(
                "spend_authorization_required",
                result["execution_branch"]["reason_code"],
            )
            request = result["external_authority_request"]
            self.assertIsNotNone(request)
            self.assertEqual(
                ["paid_0123456789abcdef01234567"], request["ordered_action_ids"]
            )
            self.assertEqual(1, len(result["local_dependencies"]))
            temporal = inspect_temporal_lifecycle(
                root,
                native_exclusive_access="established",
                observed_at="2026-09-04T23:42:00Z",
            )
            request_v2 = build_external_authority_request_v2(temporal)
            self.assertEqual(
                "astrowoof.external_authority_request.v2",
                request_v2["schema_version"],
            )
            self.assertEqual(
                ["paid_0123456789abcdef01234567"],
                request_v2["ordered_action_ids"],
            )

    def test_warning_without_elected_polish_remains_review_closeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            result = self._inspect(root, self._state(root, prepared_polish=False))

        self.assertTrue(result["terminal"]["terminal"])
        self.assertEqual("review_required", result["terminal"]["outcome"])
        self.assertEqual(
            "retain_for_review", result["execution_capacity"]["disposition"]
        )
        self.assertEqual("none", result["execution_branch"]["command"])
        self.assertIsNone(result["external_authority_request"])

    def test_mismatched_subject_does_not_make_warning_provisional(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self._state(root, prepared_polish=True)
            state["spend_ledger"]["actions"][0]["binding"]["route"] = (
                "other:polish:001"
            )
            result = self._inspect(root, state)

        self.assertEqual("retain_for_review", result["execution_capacity"]["disposition"])
        self.assertIsNone(result["external_authority_request"])

    def test_mismatched_attempt_action_id_does_not_make_warning_provisional(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self._state(root, prepared_polish=True)
            state["subjects"]["fixture"]["polish_attempts"][0]["paid_action_id"] = (
                "paid_ffffffffffffffffffffffff"
            )
            result = self._inspect(root, state)

        self.assertEqual("retain_for_review", result["execution_capacity"]["disposition"])
        self.assertIsNone(result["external_authority_request"])

    def test_stale_or_unrelated_action_does_not_make_warning_provisional(self) -> None:
        for field, value in (
            ("state", "REPORTED"),
            ("stage", "creative_retry"),
            ("service_level", "batch"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                state = self._state(root, prepared_polish=True)
                action = state["spend_ledger"]["actions"][0]
                if field == "state":
                    action["state"] = value
                    action["reported"] = {"usage": {}, "estimated_micro_usd": 0}
                else:
                    action["binding"][field] = value
                result = self._inspect(root, state)

            self.assertNotEqual(
                "await_external_authority", result["execution_capacity"]["disposition"]
            )
            self.assertIsNone(result["external_authority_request"])

    def test_committed_terminal_transition_dominates_matching_polish(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self._state(root, prepared_polish=True)
            state["terminal_transition"] = {
                "outcome": "terminalized",
                "terminal_outcome": "review_required",
                "resulting_status": "FAILED_REQUIRES_REVIEW",
            }
            state["status"] = "FAILED_REQUIRES_REVIEW"
            result = self._inspect(root, state)

        self.assertEqual("retain_for_review", result["execution_capacity"]["disposition"])
        self.assertIsNone(result["external_authority_request"])


if __name__ == "__main__":
    unittest.main()
