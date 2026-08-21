from __future__ import annotations

import hashlib
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
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal.tests.test_lifecycle_contracts import validate  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestLifecycleInspection(unittest.TestCase):
    def state(self, root: Path, *, status: str = "AWAITING_SPEND_AUTHORIZATION") -> dict:
        binding = {
            "run_id": "run_inspection_001",
            "profile_sha256": "1" * 64,
            "prepared_state_revision": 7,
            "stage": "polish",
            "route": "ella:polish:002",
            "request_sha256": "2" * 64,
            "model": "gpt-5.6",
            "service_level": "batch",
            "maximum_output_tokens": 8000,
            "commitment_micro_usd": 125000,
            "price_book_version": "openai-public-2026-08-07.v1",
        }
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_inspection_001",
            "state_revision": 7,
            "status": status,
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "PREPARED",
                "binding": binding,
                "authorization": None,
                "provider": None,
                "reported": None,
            }]},
            "passes": {},
            "subjects": {},
        }

    def materialize(self, root: Path, state: dict) -> None:
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)

    def test_valid_inspection_is_schema_valid_and_byte_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root))
            before = {
                path.relative_to(root).as_posix(): sha256(path)
                for path in root.rglob("*") if path.is_file()
            }
            result = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:00Z",
            )
            after = {
                path.relative_to(root).as_posix(): sha256(path)
                for path in root.rglob("*") if path.is_file()
            }
            self.assertEqual(before, after)
            self.assertEqual("not_quiescent", result["quiescence"]["state"])
            action = result["action_inventory"]["actions"][0]
            self.assertTrue(action["providerless_denial_eligible"])
            self.assertFalse(action["provider_identity_present"])
            schema = json.loads(read_resource_text(
                "contracts/authoring-lifecycle-contracts.schema.json"
            ))
            validate(result, schema, schema)

    def test_snapshot_mismatch_returns_fail_closed_inspection_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root))
            (root / "unexpected.json").write_text("{}\n", encoding="utf-8")
            before = sha256(root / "workspace-snapshot.json")
            result = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:00Z",
            )
            self.assertEqual(before, sha256(root / "workspace-snapshot.json"))
            self.assertFalse(result["observation"]["inventory_valid"])
            self.assertEqual(
                "unknown_review_required", result["quiescence"]["state"]
            )
            self.assertIn(
                "snapshot_incomplete_or_invalid", result["review_reasons"]
            )
            action = result["action_inventory"]["actions"][0]
            self.assertFalse(action["providerless_denial_eligible"])
            self.assertEqual("native_state_inconsistent", action["eligibility_reason"])

    def test_known_provider_identity_is_exposed_and_denial_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.state(root)
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "WAITING"
            action["provider"] = {"kind": "response", "id": "resp_fixture_123"}
            action["consumption"] = {"consumer_id": "worker", "state_revision": 8}
            self.materialize(root, state)
            result = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:00Z",
            )
            observed = result["action_inventory"]["actions"][0]
            self.assertEqual("resp_fixture_123", observed["provider_operation_id"])
            self.assertTrue(observed["provider_identity_present"])
            self.assertTrue(observed["provider_evidence_present"])
            self.assertTrue(observed["consumption_evidence_present"])
            self.assertFalse(observed["providerless_denial_eligible"])

    def test_reported_action_is_evidence_but_not_remaining_provider_work(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.state(root)
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "REPORTED"
            action["provider"] = {"kind": "response", "id": "resp_reported"}
            action["reported"] = {
                "usage": {"input_tokens": 100, "output_tokens": 20},
                "estimated_micro_usd": 5000,
            }
            state["status"] = "AUTHORING_COMPLETE"
            self.materialize(root, state)
            result = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:00Z",
            )
            observed = result["action_inventory"]["actions"][0]
            self.assertFalse(observed["necessary"])
            self.assertTrue(observed["provider_evidence_present"])
            self.assertFalse(result["terminal"]["provider_continuation_remains"])
            self.assertEqual("local_assembly", result["local_dependencies"][0]["kind"])

    def test_completed_delivery_is_terminal_publishable_and_quiescent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            deck = root / "final" / "ella" / "deck.json"
            deck.parent.mkdir(parents=True)
            deck.write_text("{}\n", encoding="utf-8")
            state = self.state(root, status="DELIVERY_COMPLETE")
            state["spend_ledger"]["actions"][0]["state"] = "REPORTED"
            state["spend_ledger"]["actions"][0]["reported"] = {
                "usage": {}, "estimated_micro_usd": 0,
            }
            state["subjects"] = {"ella": {
                "state": "DELIVERY_COMPLETE", "deck": str(deck)
            }}
            self.materialize(root, state)
            result = inspect_lifecycle(
                root, native_exclusive_access="established",
                observed_at="2026-08-13T20:00:00Z",
            )
            self.assertTrue(result["terminal"]["terminal"])
            self.assertTrue(result["terminal"]["delivery_publishable"])
            self.assertEqual("quiescent", result["quiescence"]["state"])

    def test_review_budget_and_ambiguity_states_are_machine_distinct(self) -> None:
        cases = (
            ("FINAL_QA_REQUIRES_REVIEW", "review_required", "review_required"),
            ("FINAL_QA_FAILED", "review_required", "review_required"),
            ("FAILED_REQUIRES_REVIEW", "review_required", "review_required"),
            ("BUDGET_EXHAUSTED", "budget_exhausted", "budget_exhausted"),
            ("AMBIGUOUS_PROVIDER_SUBMISSION", "ambiguous", "ambiguous_provider_submission"),
        )
        for status, outcome, reason in cases:
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                state = self.state(root, status=status)
                action = state["spend_ledger"]["actions"][0]
                if status == "BUDGET_EXHAUSTED":
                    action["state"] = "BUDGET_EXHAUSTED"
                elif status == "AMBIGUOUS_PROVIDER_SUBMISSION":
                    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                else:
                    action["state"] = "REPORTED"
                    action["reported"] = {"usage": {}, "estimated_micro_usd": 0}
                self.materialize(root, state)
                result = inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-13T20:00:00Z",
                )
                self.assertEqual(outcome, result["terminal"]["outcome"])
                self.assertEqual(reason, result["terminal"]["terminal_reason"])

    def test_observation_time_changes_only_documented_observation_bound_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root))
            first = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:00Z",
            )
            second = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T20:00:01Z",
            )
            first["observation"]["observed_at"] = "volatile"
            first["action_inventory"]["observation"]["observed_at"] = "volatile"
            second["observation"]["observed_at"] = "volatile"
            second["action_inventory"]["observation"]["observed_at"] = "volatile"
            for inspection in (first, second):
                for field, digest_field in (
                    ("external_authority_request", "external_authority_request_sha256"),
                    ("external_authority_refusal", "refusal_sha256"),
                ):
                    projection = inspection.get(field)
                    if projection is not None:
                        projection["observation"]["observed_at"] = "volatile"
                        projection[digest_field] = "observation-bound"
            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
