from __future__ import annotations

import copy
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.generic_dispatch_refusal import (
    read_generic_provider_dispatch_refusal_schema,
    validate_generic_provider_dispatch_refusal,
)
from astrowoof_natal_authoring.native_transitions import read_native_transition_result
from astrowoof_natal_authoring.terminal_review_contracts import (
    validate_terminal_review_command_result_against_publication,
)
from astrowoof_natal.tests import test_post_fan_in_retry_authority_routing_slice0 as _routing
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture


class CompletedRetryDuplicateSubmissionSlice2Tests(SemanticClosureFixture):
    def _workspace(self, root: Path) -> tuple[Path, str, str]:
        return _routing.PostFanInRetryAuthorityRoutingSlice0Tests._openai_workspace(
            self, root,
        )

    def _invoke(self, argv: list[str]) -> tuple[int, dict]:
        stdout = io.StringIO()
        code = 0
        with patch.object(sys, "argv", argv), patch.dict(
            os.environ, {"OPENAI_API_KEY": "slice-2-no-network"}
        ), patch("sys.stdout", stdout):
            try:
                closure.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, json.loads(stdout.getvalue())

    def _authorization(self, run_dir: Path, action_id: str, path: Path) -> Path:
        state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        action = next(
            item for item in state["spend_ledger"]["actions"]
            if item["action_id"] == action_id
        )
        path.write_text(json.dumps({
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": action_id,
            "binding": action["binding"],
            "authorization_reference": "slice-2-generic-refusal",
        }), encoding="utf-8")
        return path

    def test_generic_authorization_returns_typed_nonmutating_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _predecessor, successor = self._workspace(root)
            authorization = self._authorization(
                run_dir, successor, root / "authorization.json",
            )
            before_run = (run_dir / "run.json").read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()
            before_results = sorted((run_dir / "native-results").glob("*.json")) if (
                run_dir / "native-results"
            ).exists() else []
            with patch.object(
                closure.OpenAIResponsesProvider, "create_response_only",
                side_effect=AssertionError("provider create forbidden"),
            ):
                code, result = self._invoke(
                    _routing._resume_arguments(run_dir, authorization)
                )
            self.assertEqual(0, code)
            validate_generic_provider_dispatch_refusal(result)
            self.assertEqual("pre_provider_refusal", result["outcome"])
            self.assertEqual("external_authority_v2_dispatch_required", result["reason_code"])
            self.assertEqual([successor], result["ordered_action_ids"])
            self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
            self.assertEqual(before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes())
            after_results = sorted((run_dir / "native-results").glob("*.json")) if (
                run_dir / "native-results"
            ).exists() else []
            self.assertEqual(before_results, after_results)

    def test_refusal_python_validator_is_strict_without_jsonschema(self) -> None:
        schema = read_generic_provider_dispatch_refusal_schema()
        self.assertEqual(
            "astrowoof.generic_provider_dispatch_refusal.v1", schema["$id"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _predecessor, successor = self._workspace(root)
            authorization = self._authorization(
                run_dir, successor, root / "authorization.json",
            )
            _code, result = self._invoke(
                _routing._resume_arguments(run_dir, authorization)
            )
            mutated = copy.deepcopy(result)
            mutated["provider_io_disposition"] = "provider_identity_durable"
            with self.assertRaises(ValueError):
                validate_generic_provider_dispatch_refusal(mutated)

    def test_local_progress_contradiction_seals_review_result_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _predecessor, successor = self._workspace(root)
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == successor
            )
            action["state"] = "REPORTED"
            action["provider"] = {"id": "resp_slice_2_completed", "kind": "response"}
            action["reported"] = {"estimated_micro_usd": 1}
            for record in state["passes"].values():
                for attempt in record.get("attempts") or []:
                    if attempt.get("paid_action_id") == successor:
                        attempt["state"] = "PASS_QA_ACCEPTED"
                        attempt["finished_at"] = "2026-08-30T04:17:01Z"
            closure.save_state(state_path, state)

            with patch.object(closure, "author_pending_passes", return_value=None), patch.object(
                closure.OpenAIResponsesProvider, "create_response_only",
                side_effect=AssertionError("provider create forbidden"),
            ):
                code, command_result = self._invoke(
                    _routing._resume_arguments(run_dir)
                )
            self.assertEqual(2, code)
            self.assertEqual("review_required", command_result["outcome"])
            result_id = command_result["result_id"]
            publication = read_native_transition_result(run_dir, result_id)
            self.assertEqual(
                "local_work_progress_contradiction",
                publication["result"]["cause_code"],
            )
            self.assertFalse(publication["result"]["new_provider_create_permitted"])
            validate_terminal_review_command_result_against_publication(
                command_result, publication["result"], publication["receipt"],
            )
            self.assertEqual(
                publication["result"]["result_sha256"],
                publication["receipt"]["result_sha256"],
            )


if __name__ == "__main__":
    unittest.main()
