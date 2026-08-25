from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_cli import _inputs
from astrowoof_natal_authoring import (
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
)
from astrowoof_natal_authoring.closure import load_json, write_workspace_snapshot
from astrowoof_natal_authoring.external_authority_v2_execution import (
    resolve_external_authority_v2_request_payload,
)
from astrowoof_natal_authoring.cli.external_authority_v2 import main


class AmbiguousProviderSubmissionSlice0(unittest.TestCase):
    """Freeze the 0.4.22 boundary before changing its public semantics."""

    def prepared_intent(self, root: Path):
        run_dir, request, paths = _inputs(root)
        inspection = json.loads(paths["inspection"].read_text(encoding="utf-8"))
        grant = json.loads(paths["grant"].read_text(encoding="utf-8"))
        documents = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in paths["documents"]
        ]
        commit_external_authority_v2_dispatch_intent(
            run_dir,
            request=request,
            inspection=inspection,
            grant=grant,
            authorization_documents=documents,
        )
        return run_dir, request, grant

    def test_failure_before_call_entered_is_safe_and_makes_zero_calls(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            provider_calls: list[str] = []

            def fail(point: str) -> None:
                if point.startswith("before_provider_create:"):
                    raise RuntimeError("proven-before-call-entry")

            with self.assertRaisesRegex(RuntimeError, "proven-before-call-entry"):
                dispatch_external_authority_v2_intent(
                    run_dir,
                    request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"],
                    create=lambda action: provider_calls.append(action["action_id"]),
                    failure_injector=fail,
                )

            state = load_json(run_dir / "run.json")
            intent = state["external_authority_v2_dispatch_intent"]
            self.assertEqual([], provider_calls)
            self.assertIsNone(intent["active_action_id"])
            self.assertIsNone(intent["active_create_state"])
            self.assertEqual("INTENT_COMMITTED", intent["state"])

    def test_local_payload_resolution_failure_is_currently_misclassified_ambiguous(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            first_action_id = request["ordered_action_ids"][0]
            payload = (
                run_dir / "prepared" / first_action_id / "openai-request.json"
            )
            payload.unlink()
            write_workspace_snapshot(run_dir)

            callback_entries: list[str] = []
            provider_calls: list[str] = []

            def production_shaped_create(action):
                callback_entries.append(action["action_id"])
                # This is local deterministic materialization performed by the
                # production CLI callback after CALL_ENTERED is durable.
                resolve_external_authority_v2_request_payload(run_dir, action)
                provider_calls.append(action["action_id"])
                return {"id": "unreachable", "kind": "response"}

            result = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=production_shaped_create,
            )

            self.assertEqual([first_action_id], callback_entries)
            self.assertEqual([], provider_calls)
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual([first_action_id], result["ambiguous_action_ids"])
            self.assertTrue(result["provider_io_performed"])
            state = load_json(run_dir / "run.json")
            first = next(
                item
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == first_action_id
            )
            self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", first["state"])
            self.assertEqual(
                "AMBIGUOUS_PROVIDER_SUBMISSION",
                state["external_authority_v2_dispatch_intent"]["state"],
            )

    def test_public_cli_maps_local_materialization_failure_to_ambiguity_without_transport(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "command-result.json"
            transport_calls: list[str] = []
            argv = [
                "--run-dir", str(run_dir),
                "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]),
                "--grant", str(paths["grant"]),
                "--provider", "openai",
                "--api-key-env", "SBE_QA_KEY",
                "--output", str(output),
            ]
            for document in paths["documents"]:
                argv.extend(("--authorization", str(document)))

            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2."
                "resolve_external_authority_v2_request_payload",
                side_effect=ValueError("local-materialization-failed"),
            ), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: transport_calls.append("POST"),
            ):
                self.assertEqual(3, main(argv))

            command = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual([], transport_calls)
            self.assertEqual("ambiguous_submission", command["outcome"])
            self.assertEqual(
                [request["ordered_action_ids"][0]],
                command["dispatch_result"]["ambiguous_action_ids"],
            )


if __name__ == "__main__":
    unittest.main()
