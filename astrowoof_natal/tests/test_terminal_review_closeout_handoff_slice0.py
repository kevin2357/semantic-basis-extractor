from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.native_transitions import (
    publish_native_execution_result,
    read_native_transition_result,
)
from astrowoof_natal_authoring.lifecycle import (
    closeout_run,
    deny_providerless_action,
    inspect_lifecycle,
)
from astrowoof_natal_authoring.lifecycle_contracts import (
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    validate_terminal_review_command_result_against_publication,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
)
from astrowoof_natal_authoring.spend import AwaitingSpendAuthorization
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _workspace


def _run_main(run_dir: Path) -> tuple[int, list[dict]]:
    stdout = io.StringIO()
    with patch.object(
        sys,
        "argv",
        [
            "astrowoof-run-semantic-closure",
            "--run-dir",
            str(run_dir),
            "--resume",
            "--provider",
            "fake",
            "--max-attempts",
            "3",
            "--events-stdout-jsonl",
            "--log-level",
            "CRITICAL",
        ],
    ), patch("sys.stdout", stdout):
        try:
            closure.main()
        except SystemExit as exc:
            return int(exc.code), [
                json.loads(line)
                for line in stdout.getvalue().splitlines()
                if line.strip()
            ]
    return 0, [
        json.loads(line)
        for line in stdout.getvalue().splitlines()
        if line.strip()
    ]


def _latest_result(run_dir: Path) -> dict:
    index = json.loads(
        (run_dir / "native-result-index.json").read_text(encoding="utf-8")
    )
    result_id = index["result_ids"][-1]
    return read_native_transition_result(run_dir, result_id)["result"]


def _run_reconciliation_main(
    run_dir: Path, *, observed_at: str, calls: list[tuple[str, str]],
    provider_status: str = "in_progress",
) -> tuple[int, list[dict]]:
    stdout = io.StringIO()

    def request(
        _self, *, method: str, url: str, payload: dict | None,
    ) -> tuple[dict, int]:
        calls.append((method, url))
        if method != "GET" or payload is not None:
            raise AssertionError("Custody-only reconciliation attempted provider create")
        response = {
            "id": url.rsplit("/", 1)[-1],
            "status": provider_status,
        }
        if provider_status == "completed":
            response.update({
                "model": "scripted-provider", "output": [],
                "usage": {
                    "input_tokens": 10, "output_tokens": 2,
                    "total_tokens": 12,
                },
            })
        return response, 1

    argv = [
        "astrowoof-run-semantic-closure", "--run-dir", str(run_dir),
        "--resume", "--provider", "openai", "--provider-reconciliation-cycle",
        "--observed-at", observed_at, "--events-stdout-jsonl",
        "--log-level", "CRITICAL",
    ]
    with patch.object(sys, "argv", argv), patch("sys.stdout", stdout), patch.dict(
        os.environ, {"OPENAI_API_KEY": "provider-free-scripted-sentinel"}
    ), patch.object(
        closure.OpenAIResponsesProvider, "_request_with_retry", request
    ), patch.object(
        closure, "author_pending_passes",
        side_effect=AssertionError("review custody reopened authoring"),
    ), patch.object(
        closure, "finalize_subjects",
        side_effect=AssertionError("review custody reopened finalization"),
    ):
        try:
            closure.main()
        except SystemExit as exc:
            code = int(exc.code)
        else:
            code = 0
    return code, [
        json.loads(line) for line in stdout.getvalue().splitlines() if line.strip()
    ]


class TerminalReviewCloseoutHandoffSlice0Tests(unittest.TestCase):
    def test_already_review_required_public_resume_publishes_before_exit_two(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, retry_two = _workspace(
                Path(temporary), "exact_natal"
            )
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            for action in state["spend_ledger"]["actions"]:
                if action["action_id"] in {retry_one, retry_two}:
                    action["state"] = "REPORTED"
                    action["reported"] = {"estimated_micro_usd": 0}
                    action.setdefault(
                        "provider",
                        {"id": f"resp_{action['action_id']}", "kind": "response"},
                    )
            next(iter(state["passes"].values()))["state"] = (
                "FAILED_REQUIRES_REVIEW"
            )
            closure.save_state(state_path, state)

            with patch.object(
                closure, "author_pending_passes", return_value=None
            ), patch.object(closure, "finalize_subjects", return_value=None):
                exit_code, envelopes = _run_main(run_dir)

            self.assertEqual(2, exit_code)
            result = _latest_result(run_dir)
            self.assertEqual(
                "astrowoof.native_execution_result.v0.2",
                result["schema_version"],
            )
            self.assertEqual("review_required", result["outcome"])
            self.assertEqual("final_qa_requires_review", result["cause_code"])
            self.assertEqual(
                "native.result_published",
                [
                    item["event_name"]
                    for item in envelopes
                    if item.get("envelope_type") == "execution_event"
                    and item.get("event_name") == "native.result_published"
                ][-1],
            )
            self.assertEqual("command_result", envelopes[-1]["envelope_type"])
            command_result = envelopes[-1]["result"]
            self.assertEqual(result["result_id"], command_result["result_id"])
            self.assertEqual(
                result["result_sha256"], command_result["result_sha256"]
            )
            self.assertEqual(
                result["invocation_id"], command_result["native_invocation_id"]
            )

    def test_review_reached_during_local_fan_in_publishes_before_handoff(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, retry_two = _workspace(
                Path(temporary), "exact_natal"
            )
            before = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-08-28T06:19:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "ordinary_resume",
                before["temporal_decision"]["selected_command"],
            )
            prior = publish_native_execution_result(
                run_dir,
                command_kind="provider_reconciliation",
                sbe_release="0.4.27",
                published_at="2026-08-28T06:19:01Z",
            )["result"]
            self.assertEqual("provider_pending", prior["outcome"])

            def review_then_handoff(**kwargs) -> None:
                state = kwargs["state"]
                completed = next(
                    action
                    for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == retry_one
                )
                completed["state"] = "REPORTED"
                completed["reported"] = {"estimated_micro_usd": 0}
                authorized = next(
                    action
                    for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == retry_two
                )
                authorized["state"] = "AUTHORIZED"
                authorized["authorization"] = {"document_sha256": "a" * 64}
                next(iter(state["passes"].values()))["state"] = (
                    "FAILED_REQUIRES_REVIEW"
                )
                closure.save_state(kwargs["run_json"], state)
                raise AwaitingSpendAuthorization(
                    "provider-free terminal handoff characterization",
                    action=authorized,
                )

            with patch.object(
                closure,
                "author_pending_passes",
                side_effect=review_then_handoff,
            ):
                exit_code, envelopes = _run_main(run_dir)

            self.assertEqual(2, exit_code)
            result = _latest_result(run_dir)
            self.assertEqual(
                "astrowoof.native_execution_result.v0.2",
                result["schema_version"],
            )
            self.assertEqual("review_required", result["outcome"])
            self.assertEqual(
                "native_lifecycle_review_required", result["cause_code"]
            )
            dispositions = {
                item["action_id"]: item for item in result["action_dispositions"]
            }
            self.assertIn(retry_one, dispositions)
            self.assertIn(retry_two, dispositions)
            self.assertEqual(
                "terminally_accounted",
                dispositions[retry_one]["custody_disposition"],
            )
            self.assertEqual(
                "providerless_denial_only",
                dispositions[retry_two]["custody_disposition"],
            )
            self.assertFalse(result["new_provider_create_permitted"])
            index = json.loads(
                (run_dir / "native-result-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(2, len(index["result_ids"]))
            self.assertEqual("command_result", envelopes[-1]["envelope_type"])
            command_result = envelopes[-1]["result"]
            self.assertEqual(result["result_id"], command_result["result_id"])
            self.assertEqual(
                result["result_sha256"], command_result["result_sha256"]
            )
            self.assertEqual(
                result["invocation_id"], command_result["native_invocation_id"]
            )

    def test_public_review_handoff_preserves_three_custody_classes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, retry_two = _workspace(
                Path(temporary), "exact_natal"
            )
            pending_id = "paid_000000000000000000000001"

            def review_with_mixed_custody(**kwargs) -> None:
                state = kwargs["state"]
                reported = next(
                    action for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == retry_one
                )
                reported["state"] = "REPORTED"
                reported["reported"] = {"estimated_micro_usd": 0}
                pending = next(
                    action for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == pending_id
                )
                pending["state"] = "WAITING"
                pending["reported"] = None
                pending["provider_reconciliation"] = {
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                    "provider_retrieval_attempt_count": 0,
                    "last_attempt_at": None,
                    "last_outcome": None,
                    "resume_not_before": "2026-08-28T09:00:00Z",
                }
                authorized = next(
                    action for action in state["spend_ledger"]["actions"]
                    if action["action_id"] == retry_two
                )
                authorized["state"] = "AUTHORIZED"
                authorized["authorization"] = {"document_sha256": "a" * 64}
                next(iter(state["passes"].values()))["state"] = (
                    "FAILED_REQUIRES_REVIEW"
                )
                state["status"] = "FAILED_REQUIRES_REVIEW"
                closure.save_state(kwargs["run_json"], state)
                raise AwaitingSpendAuthorization(
                    "mixed-custody review handoff", action=authorized
                )

            with patch.object(
                closure, "author_pending_passes", side_effect=review_with_mixed_custody
            ):
                exit_code, envelopes = _run_main(run_dir)

            self.assertEqual(2, exit_code)
            result = _latest_result(run_dir)
            self.assertEqual("mixed_resolution_required", result["custody_finality"])
            self.assertEqual([pending_id], result["reconciliation_action_ids"])
            self.assertEqual([retry_two], result["providerless_denial_action_ids"])
            self.assertFalse(result["new_provider_create_permitted"])
            dispositions = {
                item["action_id"]: item
                for item in result["action_dispositions"]
            }
            self.assertEqual(
                "terminally_accounted",
                dispositions[retry_one]["custody_disposition"],
            )
            self.assertEqual(
                "provider_reconciliation_only",
                dispositions[pending_id]["custody_disposition"],
            )
            self.assertEqual(
                "providerless_denial_only",
                dispositions[retry_two]["custody_disposition"],
            )
            self.assertEqual("command_result", envelopes[-1]["envelope_type"])
            index = json.loads(
                (run_dir / "native-result-index.json").read_text(encoding="utf-8")
            )
            publication = read_native_transition_result(
                run_dir, index["result_ids"][-1]
            )
            validate_terminal_review_command_result_against_publication(
                envelopes[-1]["result"],
                publication["result"],
                publication["receipt"],
            )

            provider_calls: list[tuple[str, str]] = []
            reconciliation_code, _ = _run_reconciliation_main(
                run_dir,
                observed_at="2026-08-28T09:00:01Z",
                calls=provider_calls,
                provider_status="completed",
            )
            self.assertEqual(3, reconciliation_code)
            self.assertEqual(1, len(provider_calls))
            self.assertEqual("GET", provider_calls[0][0])
            self.assertTrue(provider_calls[0][1].endswith(
                "/responses/resp_exact_natal_initial_1"
            ))
            after_reconciliation = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                "FAILED_REQUIRES_REVIEW",
                next(iter(after_reconciliation["passes"].values()))["state"],
            )
            self.assertEqual(
                "FAILED_REQUIRES_REVIEW", after_reconciliation["status"]
            )
            settled = next(
                item for item in after_reconciliation["spend_ledger"]["actions"]
                if item["action_id"] == pending_id
            )
            self.assertEqual("REPORTED", settled["state"])
            self.assertEqual(
                "provider_usage_reported",
                settled["reported"]["cost_disposition"],
            )

            inspection = inspect_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-28T09:00:02Z",
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == retry_two
            )
            denial = deny_providerless_action(run_dir, {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"],
                "action_id": retry_two,
                "binding": action["binding"],
                "observed": inspection["observation"],
                "denial_reason": "external_authority_denied",
                "external_authority_reference": "api:terminal-review-slice3",
            }, decision_at="2026-08-28T09:00:03Z")
            self.assertEqual("applied", denial["outcome"])
            final_state = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            denied = next(
                item for item in final_state["spend_ledger"]["actions"]
                if item["action_id"] == retry_two
            )
            self.assertEqual("DENIED_PROVIDERLESS", denied["state"])
            self.assertEqual(1, len(provider_calls))
            closeout = closeout_run(
                run_dir, observed_at="2026-08-28T09:00:04Z"
            )
            self.assertTrue(closeout["terminal"]["terminal"])
            self.assertFalse(closeout["terminal"]["provider_continuation_remains"])
            self.assertFalse(closeout["terminal"]["local_continuation_remains"])


if __name__ == "__main__":
    unittest.main()
