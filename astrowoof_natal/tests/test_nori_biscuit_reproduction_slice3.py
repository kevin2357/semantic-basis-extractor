from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests import test_moxie_terminal_review_inventory_slice3 as moxie
from astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 import (
    _resume_arguments,
)
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture
from astrowoof_natal.tests.test_semantic_closure import completed_response
from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.native_transitions import (
    read_native_transition_result,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
)


class NoriBiscuitProductionBoundarySlice3Tests(SemanticClosureFixture):
    def _invoke(self, run_dir: Path, *, polish: bool = False) -> tuple[int, dict]:
        stdout = io.StringIO()
        code = 0
        argv = _resume_arguments(run_dir)
        if polish:
            argv.extend(["--polish", "--max-polish-attempts", "1"])
        with patch.object(sys, "argv", argv), patch.dict(
            os.environ, {"OPENAI_API_KEY": "slice-3-provider-free"}
        ), patch("sys.stdout", stdout):
            try:
                closure.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, json.loads(stdout.getvalue())

    def _nori_polish_workspace(
        self, root: Path, *, completed: bool = True,
    ) -> tuple[Path, str]:
        run_dir, _pass_id, polish_action_id, _successor = (
            moxie.MoxieTerminalReviewInventorySlice3Tests._workspace(self, root)
        )
        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        polish = next(
            action for action in state["spend_ledger"]["actions"]
            if action["action_id"] == polish_action_id
        )
        polish["binding"]["stage"] = "polish"
        polish["binding"]["route"] = "nori-fixture:polish:001"
        polish["state"] = "WAITING"
        polish["provider"] = {"kind": "response", "id": "resp_nori_slice_3"}
        polish["provider_reconciliation"] = {
            "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
            "provider_retrieval_attempt_count": 1,
            "last_attempt_at": "2026-08-31T15:00:00Z",
            "last_outcome": "completed" if completed else "pending",
            "resume_not_before": None if completed else "2099-01-01T00:00:00Z",
        }
        polish["consumption"] = {
            "authorization_reference": "api-auth:nori-slice-3",
            "consumed_at": "2026-08-31T14:59:00Z",
        }
        # The reused production-shaped fixture originally models a creative
        # retry.  Close that pass-local ambiguity so this cell isolates the
        # independent polish-stage action, as Nori's retained state did.
        for record in state["passes"].values():
            for attempt in record.get("attempts") or []:
                if attempt.get("paid_action_id") == polish_action_id:
                    attempt.update({
                        "state": "PASS_QA_ACCEPTED",
                        "accepted": True,
                        "finished_at": "2026-08-31T14:30:00Z",
                        "provider_metadata": {
                            "response_id": "resp_prior_pass_complete",
                        },
                    })
                    record["state"] = "PASS_QA_ACCEPTED"
                    record["accepted_attempt"] = attempt["attempt_number"]
        state["subjects"] = {
            "nori-fixture": {
                "subject": "nori-fixture",
                "state": "FINAL_QA_WARN",
                "polish_attempts": [{
                    "attempt_number": 1,
                    "state": "SUBMITTED",
                    "provider_metadata": None,
                    "accepted": False,
                }],
                "delivery": None,
            },
        }
        state.setdefault("authoring_profile", {}).setdefault("qa", {})[
            "polish"
        ] = True
        provider = closure.OpenAIResponsesProvider(
            api_key="slice-3-provider-free", model="gpt-5.6-luna",
            max_output_tokens=30_000, prompt_cache_mode="disabled",
            require_spend_authorization=True,
        )
        state["provider"] = "openai"
        state["service_level"] = "interactive"
        state["max_attempts"] = 3
        state["provider_configuration"] = closure.provider_configuration(provider)
        state["status"] = "WAITING_FOR_RESPONSE"
        closure.save_state(state_path, state)
        return run_dir, polish_action_id

    def _materialize_real_polish_record(
        self, run_dir: Path, polish_action_id: str,
    ) -> None:
        final_root = run_dir / "final" / "bre"
        final_root.mkdir(parents=True, exist_ok=True)
        deck_path = final_root / "natal.bre.cards.json"
        validation_path = final_root / "validation.json"
        lint_path = final_root / "lint.json"
        assembly_path = final_root / "assembly.json"
        closure.write_json_atomic(deck_path, self.packet)
        closure.write_json_atomic(validation_path, {
            "status": "pass", "errors": [], "warnings": [],
        })
        closure.write_json_atomic(lint_path, {
            "status": "warn",
            "warning_count": 1,
            "decks": [{"warnings": [{
                "code": "failure_signature",
                "details": {
                    "location": "card:" + self.packet["cards"][0]["claim_id"],
                    "field": "no_astro.headline.handler",
                },
            }]}],
        })
        closure.write_json_atomic(assembly_path, {})
        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["subjects"] = {
            "bre": {
                "subject": "bre",
                "state": "FINAL_QA_WARN",
                "deck": closure.normalized_path(deck_path),
                "assembly_report": closure.normalized_path(assembly_path),
                "validation_report": closure.normalized_path(validation_path),
                "lint_report": closure.normalized_path(lint_path),
                "baseline_warning_count": 1,
                "polish_attempts": [{
                    "attempt_number": 1,
                    "state": "SUBMITTED",
                    "started_at": "2026-08-31T14:59:00Z",
                    "finished_at": None,
                    "provider_metadata": None,
                    "accepted": False,
                }],
                "delivery": None,
            },
        }
        action = next(
            item for item in state["spend_ledger"]["actions"]
            if item["action_id"] == polish_action_id
        )
        action["binding"]["route"] = "bre:polish:001"
        response_id = action["provider"]["id"]
        attempt_root = final_root / "polish" / "attempt-001"
        attempt_root.mkdir(parents=True, exist_ok=True)
        closure.write_json_atomic(
            attempt_root / "openai-background-response.json",
            {"id": response_id, "status": "completed"},
        )
        response_path = (
            run_dir / "lifecycle" / "provider-reconciliation"
            / f"{polish_action_id}.response.json"
        )
        response_path.parent.mkdir(parents=True, exist_ok=True)
        closure.write_json_atomic(
            response_path,
            completed_response({"edits": []}, response_id=response_id),
        )
        closure.save_state(state_path, state)

    def test_nori_completed_polish_is_sealed_before_polish_consumer_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, polish_action_id = self._nori_polish_workspace(Path(temporary))
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:00:01Z",
                native_exclusive_access="declared",
            )
            operation = prior["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]
            self.assertEqual("polish", operation["stage"])
            self.assertEqual([polish_action_id], operation["source_action_ids"])
            consumer_calls: list[str] = []

            with patch.object(
                closure, "author_pending_passes", return_value=None,
            ), patch.object(
                closure,
                "finalize_subjects",
                side_effect=lambda **_kwargs: consumer_calls.append("polish"),
            ), patch.object(
                closure.OpenAIResponsesProvider,
                "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                code, command = self._invoke(run_dir)

            self.assertEqual(2, code)
            self.assertEqual(["polish"], consumer_calls)
            self.assertEqual("review_required", command["outcome"])
            publication = read_native_transition_result(run_dir, command["result_id"])
            self.assertEqual(
                "local_work_progress_contradiction",
                publication["result"]["cause_code"],
            )
            self.assertEqual(
                [polish_action_id], publication["result"]["reconciliation_action_ids"]
            )
            self.assertFalse(publication["result"]["new_provider_create_permitted"])

    def test_nori_control_consumes_polish_before_progress_is_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, polish_action_id = self._nori_polish_workspace(Path(temporary))
            state_path = run_dir / "run.json"

            def consume_polish(**kwargs):
                state = kwargs["state"]
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == polish_action_id
                )
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
                attempt = state["subjects"]["nori-fixture"]["polish_attempts"][0]
                attempt.update({
                    "state": "POLISH_ACCEPTED",
                    "accepted": True,
                    "provider_metadata": {"response_id": "resp_nori_slice_3"},
                })
                closure.save_state(state_path, state)
                return True

            with patch.object(
                closure, "author_pending_passes", side_effect=consume_polish,
            ), patch.object(closure, "finalize_subjects", return_value=None), patch.object(
                closure.OpenAIResponsesProvider,
                "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                self._invoke(run_dir)

            persisted = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "REPORTED",
                next(
                    item for item in persisted["spend_ledger"]["actions"]
                    if item["action_id"] == polish_action_id
                )["state"],
            )
            self.assertEqual(
                1,
                len(persisted["local_work_progress"]["consumed_operation_keys"]),
            )

    def test_real_finalize_subjects_adopts_completed_polish_before_seal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, polish_action_id = self._nori_polish_workspace(Path(temporary))
            self._materialize_real_polish_record(run_dir, polish_action_id)
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:00:01Z",
                native_exclusive_access="declared",
            )
            prior_operation = prior["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]

            with patch.object(
                closure.OpenAIResponsesProvider,
                "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                code, result = self._invoke(run_dir, polish=True)

            self.assertEqual(2, code, result)
            self.assertEqual("review_required", result["outcome"])
            publication = read_native_transition_result(run_dir, result["result_id"])
            self.assertNotEqual(
                "local_work_progress_contradiction",
                publication["result"]["cause_code"],
            )
            self.assertEqual("final", publication["result"]["custody_finality"])
            persisted = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == polish_action_id
            )
            self.assertEqual("REPORTED", action["state"])
            self.assertIn(
                prior_operation["operation_key"],
                persisted["local_work_progress"]["consumed_operation_keys"],
            )
            successor = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:00:02Z",
                native_exclusive_access="declared",
            )
            self.assertNotIn(
                prior_operation["operation_key"],
                [
                    operation["operation_key"]
                    for operation in successor["checkpoint_basis"][
                        "local_work_inventory"
                    ]["operations"]
                ],
            )
            self.assertEqual(
                "none", successor["temporal_decision"]["selected_command"]
            )

    def test_not_due_polish_remains_provider_custody_not_local_work(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _polish_action_id = self._nori_polish_workspace(
                Path(temporary), completed=False,
            )
            inspection = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:00:01Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                [], inspection["checkpoint_basis"]["local_work_inventory"]["operations"]
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                inspection["temporal_decision"]["selected_command"],
            )
            self.assertFalse(inspection["temporal_decision"]["eligible_now"])

    def test_biscuit_shaped_completed_retry_is_adopted_and_advances(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, _successor = (
                moxie.MoxieTerminalReviewInventorySlice3Tests._workspace(
                    self, Path(temporary),
                )
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                action["provider"]["id"]
                for action in state["spend_ledger"]["actions"]
                if action["action_id"] == completed
            )
            moxie.MoxieTerminalReviewInventorySlice3Tests._write_completed_response(
                self, run_dir, pass_id, completed, response_id,
            )
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:10:00Z",
                native_exclusive_access="declared",
            )
            prior_key = prior["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]["operation_key"]

            with patch.object(
                closure.OpenAIResponsesProvider,
                "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "run_pass_acceptance",
                return_value=(False, {"accepted": False, "report": {"status": "reject"}}),
            ):
                code, _result = self._invoke(run_dir)

            self.assertEqual(0, code)
            persisted = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            successor = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-31T15:10:01Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "await_external_authority",
                successor["temporal_decision"]["selected_command"],
            )
            self.assertNotEqual(
                prior["checkpoint_basis_sha256"], successor["checkpoint_basis_sha256"]
            )
            self.assertNotIn(
                prior_key,
                [
                    operation["operation_key"]
                    for operation in successor["checkpoint_basis"][
                        "local_work_inventory"
                    ]["operations"]
                ],
            )


if __name__ == "__main__":
    unittest.main()
