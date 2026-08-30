from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.native_transitions import (
    read_native_transition_result,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    commit_local_work_progress,
    inspect_post_fan_in_lifecycle,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    validate_terminal_review_result_v02_against_api_actions,
)
from astrowoof_natal.tests import (
    test_post_fan_in_retry_authority_routing_slice0 as routing,
)
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _binding
from astrowoof_natal.tests.test_semantic_closure import (
    SemanticClosureFixture,
    authored_field_payload,
    completed_response,
)


class _AfterFanIn(RuntimeError):
    pass


class MoxieTerminalReviewInventorySlice3Tests(SemanticClosureFixture):
    def _workspace(self, root: Path) -> tuple[Path, str, str, str]:
        run_dir, completed_action_id, successor_action_id = (
            routing.PostFanInRetryAuthorityRoutingSlice0Tests._openai_workspace(
                self, root,
            )
        )
        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        specs = {item.pass_id: item for item in closure.specs_from_state(state)}
        for member in state["initial_authoring_wave"]["ordered_members"]:
            member_pass_id = member["pass_id"]
            record = state["passes"][member_pass_id]
            source = closure.prepare_source_workspace(
                specs[member_pass_id], run_dir / "passes" / member_pass_id,
            )
            accepted = run_dir / "passes" / member_pass_id / "accepted"
            if accepted.exists():
                shutil.rmtree(accepted)
            shutil.copytree(source, accepted)
            record["state"] = "PASS_QA_ACCEPTED"
            record["accepted_workspace"] = closure.normalized_path(accepted)
            record["accepted_attempt"] = 1
        state["spend_ledger"]["actions"] = [
            action for action in state["spend_ledger"]["actions"]
            if action["action_id"] != successor_action_id
        ]
        pass_id = next(iter(state["passes"]))
        record = state["passes"][pass_id]
        record["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
        record["attempts"][0]["state"] = "PASS_QA_REJECTED"
        record["attempts"][0]["accepted"] = False
        record.pop("accepted_workspace", None)
        record.pop("accepted_attempt", None)
        record["attempts"].append({
            "attempt_number": 2,
            "state": "AMBIGUOUS_PROVIDER_SUBMISSION",
            "started_at": "2026-08-30T18:47:58Z",
            "finished_at": None,
            "response_workspace": None,
            "provider_metadata": None,
            "qa": None,
            "error": None,
            "paid_action_id": completed_action_id,
        })
        state["state_revision"] = 65
        state["status"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
        completed_action = next(
            item for item in state["spend_ledger"]["actions"]
            if item["action_id"] == completed_action_id
        )
        completed_action["binding"]["route"] = f"{pass_id}:attempt-002"
        completed_action["binding"]["model"] = "gpt-5.6-luna"
        completed_action["binding"]["maximum_output_tokens"] = 30_000
        closure.save_state(state_path, state)
        return run_dir, pass_id, completed_action_id, successor_action_id

    def _write_completed_response(
        self, run_dir: Path, pass_id: str, action_id: str, response_id: str,
    ) -> None:
        spec = next(
            item for item in closure.specs_from_state(
                json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            )
            if item.pass_id == pass_id
        )
        source = closure.prepare_source_workspace(
            spec, run_dir / "passes" / pass_id
        )
        response_path = (
            run_dir / "lifecycle" / "provider-reconciliation"
            / f"{action_id}.response.json"
        )
        response_path.parent.mkdir(parents=True, exist_ok=True)
        closure.write_json_atomic(
            response_path,
            completed_response(
                authored_field_payload(source), response_id=response_id,
            ),
        )
        state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        closure.save_state(run_dir / "run.json", state)

    @staticmethod
    def _api_join(state: dict) -> list[dict]:
        return [{
            "native_run_id": state["run_id"],
            "action_id": action["action_id"],
            "binding": action["binding"],
            "route_family": "exact_natal",
            "stage": action["binding"]["stage"],
            "provider_operation_id": (action.get("provider") or {}).get("id"),
        } for action in state["spend_ledger"]["actions"]]

    @staticmethod
    def _prepare_retry_three(
        *, state: dict, run_json: Path, pass_id: str,
        action_id: str, completed_action_id: str,
    ) -> None:
        state["spend_ledger"]["actions"].append({
            "action_id": action_id,
            "state": "PREPARED",
            "binding": _binding(
                state["run_id"], "creative_retry",
                f"{pass_id}:attempt-003", 67,
            ),
        })
        state["passes"][pass_id]["attempts"].append({
            "attempt_number": 3,
            "state": "AWAITING_SPEND_AUTHORIZATION",
            "started_at": "2026-08-30T18:51:34Z",
            "finished_at": None,
            "response_workspace": None,
            "provider_metadata": None,
            "qa": None,
            "error": None,
            "paid_action_id": action_id,
        })
        state["passes"][pass_id]["state"] = "AWAITING_SPEND_AUTHORIZATION"
        state["state_revision"] = 67
        state["status"] = "AWAITING_SPEND_AUTHORIZATION"
        closure.save_state(run_json, state)

    def _invoke(self, run_dir: Path) -> tuple[int, dict]:
        stdout = io.StringIO()
        code = 0
        with patch.object(sys, "argv", routing._resume_arguments(run_dir)), patch.dict(
            os.environ, {"OPENAI_API_KEY": "moxie-slice-3-no-network"}
        ), patch("sys.stdout", stdout):
            try:
                closure.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, json.loads(stdout.getvalue())

    def test_retained_ordering_prepares_eighth_action_then_seals_truthful_review(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            state_path = run_dir / "run.json"
            seven_action_state = json.loads(state_path.read_text(encoding="utf-8"))
            api_join = self._api_join(seven_action_state)
            self.assertEqual(7, len(api_join))

            def retained_bad_order(**kwargs):
                self._prepare_retry_three(
                    state=kwargs["state"], run_json=kwargs["run_json"],
                    pass_id=pass_id, action_id=retry_three,
                    completed_action_id=completed,
                )

            with patch.object(
                closure, "author_pending_passes", side_effect=retained_bad_order,
            ), patch.object(
                closure.OpenAIResponsesProvider, "create_response_only",
                side_effect=AssertionError("provider create forbidden"),
            ):
                code, command_result = self._invoke(run_dir)

            self.assertEqual(2, code)
            self.assertEqual("review_required", command_result["outcome"])
            publication = read_native_transition_result(
                run_dir, command_result["result_id"]
            )
            result = publication["result"]
            self.assertEqual(
                "local_work_progress_contradiction", result["cause_code"]
            )
            self.assertEqual(8, len(result["action_dispositions"]))
            self.assertEqual(
                retry_three, result["providerless_denial_action_ids"][-1]
            )
            self.assertIn(completed, result["reconciliation_action_ids"])
            with self.assertRaisesRegex(ValueError, "does not cover"):
                validate_terminal_review_result_v02_against_api_actions(
                    result, api_join,
                )
            persisted = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(8, len(persisted["spend_ledger"]["actions"]))
            self.assertFalse(result["new_provider_create_permitted"])

    def test_completed_result_adopted_before_successor_selection_needs_no_retry(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-30T18:51:02Z",
                native_exclusive_access="declared",
            )
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            completed_action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            completed_action["state"] = "REPORTED"
            completed_action["reported"] = {"estimated_micro_usd": 0}
            attempt = state["passes"][pass_id]["attempts"][-1]
            attempt["state"] = "PASS_QA_ACCEPTED"
            attempt["finished_at"] = "2026-08-30T18:51:34Z"
            state["passes"][pass_id]["state"] = "PASS_QA_ACCEPTED"
            closure.save_state(state_path, state)

            successor = commit_local_work_progress(
                run_dir, prior=prior, observed_at="2026-08-30T18:51:35Z",
            )
            persisted = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertNotIn(
                retry_three,
                [item["action_id"] for item in persisted["spend_ledger"]["actions"]],
            )
            self.assertNotEqual(
                "await_external_authority",
                successor["temporal_decision"]["selected_command"],
            )
            self.assertEqual(
                prior["checkpoint_basis"]["local_work_inventory"]["operations"][0][
                    "operation_key"
                ],
                persisted["local_work_progress"]["consumed_operation_keys"][-1],
            )

    def test_legitimate_retry_is_published_only_after_completed_result_adoption(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            prior = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-30T18:51:02Z",
                native_exclusive_access="declared",
            )
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            completed_action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            completed_action["state"] = "REPORTED"
            completed_action["reported"] = {"estimated_micro_usd": 0}
            attempt = state["passes"][pass_id]["attempts"][-1]
            attempt["state"] = "PASS_QA_REJECTED"
            attempt["finished_at"] = "2026-08-30T18:51:34Z"
            self._prepare_retry_three(
                state=state, run_json=state_path, pass_id=pass_id,
                action_id=retry_three, completed_action_id=completed,
            )

            successor = commit_local_work_progress(
                run_dir, prior=prior, observed_at="2026-08-30T18:51:35Z",
            )
            self.assertEqual(
                "await_external_authority",
                successor["temporal_decision"]["selected_command"],
            )
            self.assertEqual(
                [retry_three],
                successor["checkpoint_basis"]["external_authority_state"][
                    "ordered_action_ids"
                ],
            )
            persisted = json.loads(state_path.read_text(encoding="utf-8"))
            retry = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == retry_three
            )
            self.assertEqual("PREPARED", retry["state"])
            self.assertIsNone(retry.get("provider"))

    def test_runtime_adopts_completed_response_and_accepts_without_successor(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                item["provider"]["id"]
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self._write_completed_response(
                run_dir, pass_id, completed, response_id,
            )
            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "finalize_subjects", side_effect=_AfterFanIn,
            ), patch.object(sys, "argv", routing._resume_arguments(run_dir)), patch.dict(
                os.environ, {"OPENAI_API_KEY": "moxie-slice-5-no-network"},
            ), patch("sys.stdout", io.StringIO()), self.assertRaises(_AfterFanIn):
                closure.main()

            persisted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            action = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self.assertEqual("REPORTED", action["state"])
            self.assertNotIn(
                retry_three,
                [item["action_id"] for item in persisted["spend_ledger"]["actions"]],
            )
            attempt = persisted["passes"][pass_id]["attempts"][-1]
            self.assertEqual("PASS_QA_ACCEPTED", attempt["state"])
            self.assertEqual(response_id, attempt["provider_metadata"]["response_id"])

    def test_runtime_adopts_rejection_before_preparing_exact_successor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, _fixture_successor = self._workspace(
                Path(temporary)
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                item["provider"]["id"]
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self._write_completed_response(
                run_dir, pass_id, completed, response_id,
            )
            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "run_pass_acceptance",
                return_value=(False, {"accepted": False, "report": {"status": "reject"}}),
            ):
                code, _result = self._invoke(run_dir)
            debug_state = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            self.assertEqual(0, code, {
                "result": _result,
                "actions": [
                    (item["action_id"], item["state"], item["binding"]["route"])
                    for item in debug_state["spend_ledger"]["actions"]
                ],
                "pass": debug_state["passes"][pass_id],
            })

            inspection = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-30T18:52:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "await_external_authority",
                inspection["temporal_decision"]["selected_command"],
            )
            successor_ids = inspection["checkpoint_basis"][
                "external_authority_state"
            ]["ordered_action_ids"]
            persisted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            prepared_ids = [
                item["action_id"] for item in persisted["spend_ledger"]["actions"]
                if item["state"] == "PREPARED"
            ]
            self.assertEqual(
                1, len(successor_ids),
                {"successor_ids": successor_ids, "prepared_ids": prepared_ids,
                 "wave": persisted.get("initial_authoring_wave")},
            )
            completed_action = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self.assertEqual("REPORTED", completed_action["state"])
            successor = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == successor_ids[0]
            )
            self.assertEqual("PREPARED", successor["state"])
            self.assertIsNone(successor.get("provider"))

    def test_invalid_completed_response_prepares_no_successor_and_consumes_nothing(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                item["provider"]["id"]
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self._write_completed_response(
                run_dir, pass_id, completed, response_id,
            )
            response_path = (
                run_dir / "lifecycle" / "provider-reconciliation"
                / f"{completed}.response.json"
            )
            response = json.loads(response_path.read_text(encoding="utf-8"))
            response["id"] = "resp_conflicting_identity"
            closure.write_json_atomic(response_path, response)
            closure.write_workspace_snapshot(run_dir)

            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), self.assertLogs(
                "astrowoof_natal_authoring.closure", level="WARNING",
            ) as captured:
                code, command_result = self._invoke(run_dir)
            self.assertTrue(any(
                "completed_provider_result_adoption_unavailable" in item
                and f"action_id={completed}" in item
                for item in captured.output
            ))
            self.assertEqual(2, code)
            self.assertEqual("review_required", command_result["outcome"])
            persisted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            self.assertNotIn(
                retry_three,
                [item["action_id"] for item in persisted["spend_ledger"]["actions"]],
            )
            self.assertEqual(
                [],
                (persisted.get("local_work_progress") or {}).get(
                    "consumed_operation_keys", []
                ),
            )

    def test_interruption_before_coherent_adoption_prepares_no_successor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, retry_three = self._workspace(
                Path(temporary)
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                item["provider"]["id"]
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self._write_completed_response(run_dir, pass_id, completed, response_id)
            real_save = closure.save_state

            def interrupt_adoption(path, value):
                attempt = value["passes"][pass_id]["attempts"][-1]
                if attempt["state"] == "WAITING_FOR_RESPONSE":
                    raise RuntimeError("injected before coherent adoption checkpoint")
                return real_save(path, value)

            with patch.object(
                closure, "save_state", side_effect=interrupt_adoption,
            ), patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(sys, "argv", routing._resume_arguments(run_dir)), patch.dict(
                os.environ, {"OPENAI_API_KEY": "moxie-slice-5-no-network"},
            ), patch("sys.stdout", io.StringIO()), self.assertRaisesRegex(
                RuntimeError, "before coherent adoption"
            ):
                closure.main()

            persisted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            self.assertNotIn(
                retry_three,
                [item["action_id"] for item in persisted["spend_ledger"]["actions"]],
            )
            self.assertEqual(
                [],
                (persisted.get("local_work_progress") or {}).get(
                    "consumed_operation_keys", []
                ),
            )
            with self.assertRaises(ValueError):
                closure.validate_workspace_snapshot(run_dir, persisted)

    def test_interruption_after_adoption_replays_without_provider_or_duplicate_retry(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, completed, _fixture_successor = self._workspace(
                Path(temporary)
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            response_id = next(
                item["provider"]["id"]
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == completed
            )
            self._write_completed_response(run_dir, pass_id, completed, response_id)
            real_save = closure.save_state
            interrupted_once = False

            def interrupt_after_rejection(path, value):
                nonlocal interrupted_once
                result = real_save(path, value)
                record = value["passes"][pass_id]
                if (
                    not interrupted_once
                    and record["state"] == "PASS_QA_REJECTED"
                    and record["attempts"][-1]["attempt_number"] == 2
                    and record["attempts"][-1]["finished_at"] is not None
                ):
                    interrupted_once = True
                    raise KeyboardInterrupt("injected after adoption")
                return result

            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "run_pass_acceptance",
                return_value=(False, {"accepted": False, "report": {"status": "reject"}}),
            ), patch.object(
                closure, "save_state", side_effect=interrupt_after_rejection,
            ), patch.object(sys, "argv", routing._resume_arguments(run_dir)), patch.dict(
                os.environ, {"OPENAI_API_KEY": "moxie-slice-5-no-network"},
            ), patch("sys.stdout", io.StringIO()), self.assertRaises(
                KeyboardInterrupt
            ):
                closure.main()

            interrupted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            self.assertEqual(7, len(interrupted["spend_ledger"]["actions"]))
            self.assertEqual(
                "REPORTED",
                next(
                    item for item in interrupted["spend_ledger"]["actions"]
                    if item["action_id"] == completed
                )["state"],
            )
            # Raising in-process writes test-harness diagnostics after the
            # checkpoint.  Re-seal the already durable adoption bytes to model
            # restoring that exact post-adoption checkpoint in a fresh worker.
            closure.write_workspace_snapshot(run_dir)

            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "run_pass_acceptance",
                return_value=(False, {"accepted": False, "report": {"status": "reject"}}),
            ):
                code, _result = self._invoke(run_dir)
            self.assertEqual(0, code)
            replayed = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            retries = [
                item for item in replayed["spend_ledger"]["actions"]
                if item["binding"]["stage"] == "creative_retry"
                and item["binding"]["route"].endswith("attempt-003")
            ]
            self.assertEqual(1, len(retries))
            self.assertEqual("PREPARED", retries[0]["state"])
            inspection = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-30T18:53:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                [retries[0]["action_id"]],
                inspection["checkpoint_basis"]["external_authority_state"][
                    "ordered_action_ids"
                ],
            )


if __name__ == "__main__":
    unittest.main()
