from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import public_run_state, write_workspace_snapshot
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _workspace


FIXTURE = Path(__file__).resolve().parents[1] / (
    "docs/sprints/2026/08/20260825-post-fan-in-retry-matrix-contract-sprint1/"
    "fixtures/post-fan-in-retry-matrix.v1.json"
)


def _write(run_dir: Path, mutate) -> None:
    state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    mutate(state)
    state["state_revision"] = int(state.get("state_revision") or 0) + 1
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)


def _inspect(run_dir: Path) -> dict:
    result = inspect_post_fan_in_lifecycle(
        run_dir, observed_at="2026-08-25T23:45:00Z",
        native_exclusive_access="declared",
    )
    validate_lifecycle_inspection_v07(result)
    return result


class PostFanInRetryMatrixSlice3Tests(unittest.TestCase):
    def test_packaged_matrix_fixture_is_closed_and_complete(self) -> None:
        value = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(
            {"schema_version", "cases", "provider_create_count", "provider_retrieval_count"},
            set(value),
        )
        self.assertEqual(list("ABCDEFGH"), [item["case_id"] for item in value["cases"]])
        self.assertEqual(0, value["provider_create_count"])
        self.assertEqual(0, value["provider_retrieval_count"])

    def test_cases_a_b_c_and_d_for_exact_and_bounded(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family), tempfile.TemporaryDirectory() as temp:
                # A: accepted/no-retry authoring advances to final assembly.
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def no_retry(state):
                    state["spend_ledger"]["actions"] = [
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] not in {retry_one, retry_two}
                    ]
                    state["status"] = "AUTHORING_COMPLETE"
                _write(run_dir, no_retry)
                result = _inspect(run_dir)
                self.assertEqual("ordinary_resume", result["temporal_decision"]["selected_command"])
                self.assertEqual(
                    "final_assembly_and_qa",
                    result["checkpoint_basis"]["local_work_inventory"]["operations"][0]["kind"],
                )

            with self.subTest(route=route_family, case="B"), tempfile.TemporaryDirectory() as temp:
                # B: no completed custody remains; one prepared retry needs authority.
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def retry_needed(state):
                    state["spend_ledger"]["actions"] = [
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] != retry_one
                    ]
                _write(run_dir, retry_needed)
                result = _inspect(run_dir)
                self.assertEqual("await_external_authority", result["temporal_decision"]["selected_command"])
                self.assertEqual([], result["checkpoint_basis"]["local_work_inventory"]["operations"])
                self.assertIn(retry_two, result["checkpoint_basis"]["external_authority_state"]["ordered_action_ids"])

            with self.subTest(route=route_family, case="C"), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def provider_pending(state):
                    state["spend_ledger"]["actions"] = [
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] != retry_two
                    ]
                    action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == retry_one)
                    action["provider_reconciliation"]["last_outcome"] = "pending"
                    action["provider_reconciliation"]["resume_not_before"] = "2099-01-01T00:00:00Z"
                    state["status"] = "WAITING_FOR_RESPONSE"
                _write(run_dir, provider_pending)
                result = _inspect(run_dir)
                self.assertEqual("provider_reconciliation_cycle", result["temporal_decision"]["selected_command"])
                self.assertFalse(result["temporal_decision"]["eligible_now"])
                self.assertEqual([], result["checkpoint_basis"]["local_work_inventory"]["operations"])
                due = inspect_post_fan_in_lifecycle(
                    run_dir, observed_at="2100-01-01T00:00:00Z",
                    native_exclusive_access="declared",
                )
                self.assertTrue(due["temporal_decision"]["eligible_now"])
                self.assertEqual([retry_one], due["temporal_decision"]["due_action_ids"])

            with self.subTest(route=route_family, case="D"), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, _retry_two = _workspace(Path(temp), route_family)
                result = _inspect(run_dir)
                operation = result["checkpoint_basis"]["local_work_inventory"]["operations"][0]
                self.assertEqual("provider_result_fan_in_and_retry_evaluation", operation["kind"])
                self.assertEqual([retry_one], operation["source_action_ids"])

    def test_cases_e_f_g_and_h_are_non_dispatching(self) -> None:
        # E: retry exhaustion is terminal/review and has no work inventory.
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family, case="E"), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def exhausted(state):
                    for action in state["spend_ledger"]["actions"]:
                        if action["action_id"] in {retry_one, retry_two}:
                            action["state"] = "REPORTED"
                            action["reported"] = {"estimated_micro_usd": 0}
                            action.setdefault("provider", {"id": "resp_exhausted", "kind": "response"})
                    state["status"] = "FAILED_REQUIRES_REVIEW"
                _write(run_dir, exhausted)
                result = _inspect(run_dir)
                self.assertEqual("none", result["temporal_decision"]["selected_command"])
                self.assertEqual([], result["checkpoint_basis"]["local_work_inventory"]["operations"])

        # F: historical initial lineage without its wave is a typed native refusal.
        with tempfile.TemporaryDirectory() as temp:
            run_dir, retry_one, retry_two = _workspace(Path(temp), "exact_natal")
            def unjoinable(state):
                state.pop("initial_authoring_wave", None)
                state["spend_ledger"]["actions"] = [
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] not in {retry_one, retry_two}
                ]
                state["passes"] = {}
                state["status"] = "AWAITING_SPEND_AUTHORIZATION"
            _write(run_dir, unjoinable)
            result = _inspect(run_dir)
            self.assertEqual("none", result["temporal_decision"]["selected_command"])
            self.assertEqual([], result["checkpoint_basis"]["local_work_inventory"]["operations"])
            self.assertEqual(
                "initial_wave_lineage_unjoinable",
                result["checkpoint_basis"]["external_authority_state"]["refusal_reason"],
            )

        # G: AUTHORIZED/providerless is constrained state, never generic resume.
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family, case="G"), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def authorized(state):
                    state["spend_ledger"]["actions"] = [
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] != retry_one
                    ]
                    action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == retry_two)
                    action["state"] = "AUTHORIZED"
                    action["authorization"] = {"document_sha256": "c" * 64}
                _write(run_dir, authorized)
                result = _inspect(run_dir)
                self.assertEqual("none", result["temporal_decision"]["selected_command"])
                self.assertIn(
                    "authorized_providerless_action_requires_constrained_dispatch",
                    result["checkpoint_basis"]["review_reasons"],
                )

        # H: call entered with no identity remains ambiguity/review.
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route_family, case="H"), tempfile.TemporaryDirectory() as temp:
                run_dir, retry_one, retry_two = _workspace(Path(temp), route_family)
                def ambiguous(state):
                    state["spend_ledger"]["actions"] = [
                        item for item in state["spend_ledger"]["actions"]
                        if item["action_id"] != retry_one
                    ]
                    action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == retry_two)
                    action["state"] = "SUBMITTING"
                    action["provider"] = None
                    state["status"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                _write(run_dir, ambiguous)
                result = _inspect(run_dir)
                self.assertEqual("none", result["temporal_decision"]["selected_command"])
                self.assertEqual("retain_for_review", result["temporal_decision"]["capacity_disposition"])


if __name__ == "__main__":
    unittest.main()
