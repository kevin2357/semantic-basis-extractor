from __future__ import annotations

import json
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.initial_wave import InitialWaveError
from astrowoof_natal_authoring.post_fan_in_contracts import inspect_post_fan_in_lifecycle
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _binding
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture


class _ReachedOrdinaryAuthoring(RuntimeError):
    pass


def _resume_arguments(run_dir: Path, authorization: Path | None = None) -> list[str]:
    values = [
        "astrowoof-run-semantic-closure", "--run-dir", str(run_dir), "--resume",
        "--provider", "openai", "--max-attempts", "3", "--model", "gpt-5.6-luna",
        "--max-output-tokens", "30000", "--prompt-cache-mode", "disabled",
        "--log-level", "CRITICAL",
    ]
    if authorization is not None:
        values.extend(("--spend-authorization", str(authorization)))
    return values


class PostFanInRetryAuthorityRoutingSlice0Tests(SemanticClosureFixture):
    def _openai_workspace(self, root: Path) -> tuple[Path, str, str]:
        provider = closure.OpenAIResponsesProvider(
            api_key="slice-0-no-network", model="gpt-5.6-luna",
            max_output_tokens=30_000, prompt_cache_mode="disabled",
            require_spend_authorization=True,
        )
        state, state_path = self.make_state(root, provider)
        run_dir = state_path.parent
        closure.prepare_exact_interactive_initial_wave(
            state=state, provider=provider, run_dir=run_dir, run_json=state_path,
        )
        for number, member in enumerate(
            state["initial_authoring_wave"]["ordered_members"], 1
        ):
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == member["action_id"]
            )
            action["state"] = "REPORTED"
            action["provider"] = {
                "id": f"resp_exact_natal_initial_{number}", "kind": "response",
            }
            action["reported"] = {"estimated_micro_usd": 0}
            attempt = state["passes"][member["pass_id"]]["attempts"][0]
            attempt["state"] = "PASS_QA_ACCEPTED"
            attempt["accepted"] = True
        state["initial_authoring_wave"]["state"] = "DETACHED"
        retry_one = "paid_000000000000000000000101"
        retry_two = "paid_000000000000000000000102"
        state["spend_ledger"]["actions"].extend((
            {
                "action_id": retry_one, "state": "WAITING",
                "binding": _binding(
                    state["run_id"], "creative_retry", "pass-1:attempt-002", 7,
                ),
                "provider": {"id": "resp_exact_natal_retry_1", "kind": "response"},
                "provider_reconciliation": {
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                    "provider_retrieval_attempt_count": 1,
                    "last_attempt_at": "2026-08-27T11:59:00Z",
                    "last_outcome": "completed", "resume_not_before": None,
                },
                "reported": None,
            },
            {
                "action_id": retry_two, "state": "PREPARED",
                "binding": _binding(
                    state["run_id"], "creative_retry", "pass-1:attempt-003", 8,
                ),
            },
        ))
        retry_payload = {
            "model": "scripted-provider",
            "input": "provider-free post-fan-in retry qualification",
        }
        retry_payload_path = run_dir / "ordinary-retry-request.private.json"
        retry_artifact = closure.persist_provider_request_payload(
            retry_payload_path, retry_payload,
        )
        retry_action = next(
            action for action in state["spend_ledger"]["actions"]
            if action["action_id"] == retry_two
        )
        retry_action["binding"]["request_sha256"] = retry_artifact[
            "canonical_request_sha256"
        ]
        retry_action["request_payload_artifact"] = retry_artifact
        state["state_revision"] = 8
        state["status"] = "AWAITING_SPEND_AUTHORIZATION"
        closure.save_state(state_path, state)
        return run_dir, retry_one, retry_two

    def _run_main(self, argv: list[str]) -> None:
        with patch.object(sys, "argv", argv), patch.dict(
            os.environ, {"OPENAI_API_KEY": "slice-0-no-network"}
        ), patch("sys.stdout", io.StringIO()), patch.object(
            closure.OpenAIResponsesProvider,
            "create_response_only",
            side_effect=AssertionError("provider create is forbidden in Slice 0"),
        ):
            closure.main()

    def test_public_resume_routes_completed_retry_past_initial_wave_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = self._openai_workspace(Path(temporary))
            authorization = Path(temporary) / "ordinary-authorization.json"
            authorization.write_text("{}\n", encoding="utf-8")
            inspection = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-27T12:00:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "ordinary_resume", inspection["temporal_decision"]["selected_command"],
            )
            operation = inspection["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]
            self.assertEqual(
                "provider_result_fan_in_and_retry_evaluation", operation["kind"],
            )
            self.assertEqual([retry_one], operation["source_action_ids"])
            self.assertEqual(
                [], inspection["checkpoint_basis"]["external_authority_state"][
                    "ordered_action_ids"
                ],
            )
            with patch.object(
                closure, "apply_spend_authorizations", return_value=[]
            ), patch.object(
                closure, "author_pending_passes",
                side_effect=_ReachedOrdinaryAuthoring("ordinary path reached"),
            ), self.assertRaises(_ReachedOrdinaryAuthoring):
                self._run_main(_resume_arguments(run_dir, authorization))

    def test_stored_detached_wave_alone_reactivates_initial_wave_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _retry_one, _retry_two = self._openai_workspace(Path(temporary))
            with patch.object(
                closure, "author_pending_passes",
                side_effect=_ReachedOrdinaryAuthoring("ordinary path reached"),
            ), self.assertRaises(_ReachedOrdinaryAuthoring):
                self._run_main(_resume_arguments(run_dir))
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual("DETACHED", state["initial_authoring_wave"]["state"])
            self.assertFalse((run_dir / "native-results").exists())

    def test_active_initial_wave_still_requires_aggregate_grant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _retry_one, _retry_two = self._openai_workspace(Path(temporary))
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["initial_authoring_wave"]["state"] = "AWAITING_SPEND_AUTHORIZATION"
            closure.save_state(state_path, state)
            authorization = Path(temporary) / "ordinary-authorization.json"
            authorization.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(InitialWaveError) as raised:
                self._run_main(_resume_arguments(run_dir, authorization))
            self.assertEqual("aggregate_grant_required", raised.exception.reason_code)


if __name__ == "__main__":
    unittest.main()
