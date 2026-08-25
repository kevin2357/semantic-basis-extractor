from __future__ import annotations

import tempfile
import threading
import unittest
import json
import os
import shutil
from unittest.mock import patch
from copy import deepcopy
from pathlib import Path

from astrowoof_natal.tests.test_semantic_closure import (
    ScriptedTransport,
    SemanticClosureFixture,
    authored_field_payload,
    completed_response,
)
from astrowoof_natal_authoring.closure import (
    AwaitingSpendAuthorization,
    OpenAIResponsesProvider,
    SpendController,
    build_interactive_authoring_request,
    load_json,
    prepare_source_workspace,
    save_state,
    specs_from_state,
)
from astrowoof_natal_authoring.external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    resolve_external_authority_v2_request_payload,
)
from astrowoof_natal_authoring import (
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
    validate_external_authority_v2_command_result_v2,
)
from astrowoof_natal_authoring.cli.external_authority_v2 import main as v2_main
from astrowoof_natal_authoring.spend import digest
from astrowoof_natal_authoring.provenance import resource_set_provenance


PLACEHOLDER = "[workspace prompt persisted separately as openai-workspace-prompt.txt]"


def _occurrences(value: object, target: str) -> int:
    if isinstance(value, dict):
        return sum(_occurrences(item, target) for item in value.values())
    if isinstance(value, list):
        return sum(_occurrences(item, target) for item in value)
    return int(value == target)


class ExternalAuthorityV2PayloadDigestSlice0(SemanticClosureFixture):
    def _authority_files(
        self, root: Path, run_dir: Path, *, observed_at: str, label: str,
    ) -> tuple[dict, dict[str, object]]:
        inspection = inspect_temporal_lifecycle(
            run_dir, native_exclusive_access="declared", observed_at=observed_at,
        )
        request = build_external_authority_request_v2(inspection)
        inventory = {
            item["action_id"]: item
            for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
        }
        documents = [{
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": action_id,
            "binding": deepcopy(inventory[action_id]["binding"]),
            "authorization_reference": f"api:{label}:{index}",
        } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
        grant = build_external_authority_grant_v2(
            request, inspection, documents,
            api_decision_id=f"decision:{label}", issuer="astrowoof-api",
            issued_at=observed_at,
        )
        authority = root / f"authority-{label}"
        authority.mkdir()
        paths: dict[str, object] = {}
        for name, value in (("inspection", inspection), ("request", request), ("grant", grant)):
            path = authority / f"{name}.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            paths[name] = path
        paths["documents"] = []
        for index, document in enumerate(documents, 1):
            path = authority / f"authorization-{index}.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            paths["documents"].append(path)
        return request, paths

    @staticmethod
    def _cli_argv(run_dir: Path, paths: dict[str, object], output: Path) -> list[str]:
        argv = [
            "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
            "--request", str(paths["request"]), "--grant", str(paths["grant"]),
            "--provider", "openai", "--api-key-env", "SBE_QA_KEY",
            "--output", str(output),
        ]
        for document in paths["documents"]:
            argv.extend(("--authorization", str(document)))
        return argv

    def test_production_exact_authoring_persists_redacted_digest_mismatch_and_loses_block_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, specs, _ = self.make_passes(root)
            spec = specs[0]
            source = root / spec.pass_id
            transport = ScriptedTransport([
                completed_response(authored_field_payload(source))
            ])
            provider = OpenAIResponsesProvider(
                api_key="provider-free", background=False,
                prompt_cache_mode="disabled", transport=transport,
                sleep=lambda _seconds: None,
            )
            complete_payload, _, segments = build_interactive_authoring_request(
                provider, spec=spec, workspace=source,
                feedback=None, attempt_number=2,
            )
            response_workspace = (
                root / "run" / "passes" / spec.pass_id / "attempt-002"
                / "response" / spec.pass_id
            )
            provider.author(
                source, response_workspace, spec, 2,
                feedback=None,
            )

            attempt_root = response_workspace.parents[1]
            redacted = load_json(attempt_root / "openai-request.json")
            prompt_path = attempt_root / "openai-workspace-prompt.txt"
            prompt = prompt_path.read_text(encoding="utf-8")
            expected_digest = digest(complete_payload)

            self.assertEqual(1, _occurrences(redacted, PLACEHOLDER))
            self.assertEqual(PLACEHOLDER, redacted["input"][1]["content"])
            self.assertEqual("\n\n".join(segments.values()), prompt)
            self.assertEqual(
                [
                    provider._input_text_block(segments["static_prefix"], breakpoint=True),
                    provider._input_text_block(segments["subject_prefix"], breakpoint=True),
                    provider._input_text_block(segments["pass_assignment"]),
                ],
                complete_payload["input"][1]["content"],
            )
            self.assertNotEqual(
                [{"type": "input_text", "text": prompt}],
                complete_payload["input"][1]["content"],
            )
            self.assertNotEqual(expected_digest, digest(redacted))

            reconstructed = deepcopy(redacted)
            reconstructed["input"][1]["content"] = [
                provider._input_text_block(segments["static_prefix"], breakpoint=True),
                provider._input_text_block(segments["subject_prefix"], breakpoint=True),
                provider._input_text_block(segments["pass_assignment"]),
            ]
            self.assertEqual(complete_payload, reconstructed)
            self.assertEqual(expected_digest, digest(reconstructed))
            self.assertEqual(1, len(transport.calls))

    def _prepared_creative_retry(self, root: Path) -> tuple[Path, dict, dict]:
        provider = OpenAIResponsesProvider(
            api_key="provider-free", background=False,
            prompt_cache_mode="disabled", require_spend_authorization=True,
        )
        state, run_json = self.make_state(root, provider)
        state["provenance"] = {
            "runtime": {
                "distribution": "astrowoof-natal-authoring",
                "version": "0.4.23",
            },
            "resources": resource_set_provenance(),
        }
        run_dir = run_json.parent
        record = state["passes"]["bre_1"]
        spec = next(item for item in specs_from_state(state) if item.pass_id == "bre_1")
        retained_inputs = run_dir / "retained-inputs"
        retained_inputs.mkdir()
        retained_source_zip = retained_inputs / spec.source_zip.name
        shutil.copyfile(spec.source_zip, retained_source_zip)
        record["source_zip"] = str(retained_source_zip.resolve()).replace("\\", "/")
        spec = type(spec)(
            pass_id=spec.pass_id, subject=spec.subject,
            pass_number=spec.pass_number, source_zip=retained_source_zip,
            source_sha256=spec.source_sha256,
        )
        source = prepare_source_workspace(spec, run_dir / "passes" / spec.pass_id)
        attempt = {
            "attempt_number": 2,
            "state": "SUBMITTED",
            "started_at": "2026-08-25T16:00:00Z",
            "finished_at": None,
            "response_workspace": str(
                (run_dir / "passes" / spec.pass_id / "attempt-002" / "response" / spec.pass_id).resolve()
            ).replace("\\", "/"),
            "provider_metadata": None,
            "qa": None,
            "error": None,
        }
        record["attempts"].append(attempt)
        record["state"] = "SUBMITTED"
        save_state(run_json, state)
        controller = SpendController(
            state=state, run_json=run_json, state_lock=threading.Lock(),
            consumer_id="slice1-fixture",
        )
        before_submit, provider_created = controller.callbacks(
            stage="creative_retry", route="bre_1:attempt-002",
            model=provider.model, service_level="interactive",
            maximum_output_tokens=provider.max_output_tokens,
        )
        response_workspace = Path(attempt["response_workspace"])
        with self.assertRaises(AwaitingSpendAuthorization) as caught:
            provider.author(
                source, response_workspace, spec, 2, None,
                before_submit, provider_created,
            )
        action = caught.exception.action
        self.assertIsNotNone(action)
        attempt["state"] = "AWAITING_SPEND_AUTHORIZATION"
        attempt["paid_action_id"] = action["action_id"]
        record["state"] = "AWAITING_SPEND_AUTHORIZATION"
        state["initial_authoring_wave"] = {"state": "DETACHED"}
        save_state(run_json, state)
        return run_dir, state, action

    @staticmethod
    def _record_digest_mismatch_refusal(action: dict) -> None:
        action["external_authority_v2_refused_invocations"] = [{
            "schema_version": "astrowoof.external_authority_v2_refused_invocation.v1",
            "outcome": "pre_provider_refusal",
            "reason_code": "request_payload_digest_mismatch",
            "refused_action_id": action["action_id"],
        }]

    def test_new_action_resolves_only_its_binding_owned_direct_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _state, action = self._prepared_creative_retry(Path(temporary))
            artifact = action.get("request_payload_artifact")
            self.assertIsInstance(artifact, dict)
            payload = resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual(action["binding"]["request_sha256"], digest(payload))

            # Unreferenced lookalikes are not candidates and are never discovered.
            (run_dir / "competing-openai-request-payload.private.json").write_text(
                json.dumps(payload), encoding="utf-8",
            )
            save_state(run_dir / "run.json", _state)
            self.assertEqual(
                action["binding"]["request_sha256"],
                digest(resolve_external_authority_v2_request_payload(run_dir, action)),
            )

    def test_historical_0423_action_rebuilds_from_snapshot_bound_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, state, action = self._prepared_creative_retry(Path(temporary))
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            self._record_digest_mismatch_refusal(action)
            save_state(run_dir / "run.json", state)
            payload = resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual(action["binding"]["request_sha256"], digest(payload))

    def test_direct_payload_reference_fails_closed_on_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, state, action = self._prepared_creative_retry(root)
            outside = root / "outside.json"
            outside.write_text("{}\n", encoding="utf-8")
            action["request_payload_artifact"]["logical_path"] = str(outside.resolve()).replace("\\", "/")
            save_state(run_dir / "run.json", state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual("request_payload_digest_mismatch", caught.exception.reason_code)

    def test_historical_rebuild_fails_closed_for_changed_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, state, action = self._prepared_creative_retry(Path(temporary))
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            self._record_digest_mismatch_refusal(action)
            prompt = run_dir / "passes" / "bre_1" / "attempt-002" / "openai-workspace-prompt.txt"
            prompt.write_text(prompt.read_text(encoding="utf-8") + "\nchanged", encoding="utf-8")
            save_state(run_dir / "run.json", state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual("request_payload_digest_mismatch", caught.exception.reason_code)

    def test_historical_rebuild_fails_closed_for_wrong_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, state, action = self._prepared_creative_retry(Path(temporary))
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            self._record_digest_mismatch_refusal(action)
            redacted_path = run_dir / "passes" / "bre_1" / "attempt-002" / "openai-request.json"
            redacted = load_json(redacted_path)
            redacted["input"][1]["content"] = "[different placeholder]"
            redacted_path.write_text(json.dumps(redacted, indent=2) + "\n", encoding="utf-8")
            save_state(run_dir / "run.json", state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual("request_payload_digest_mismatch", caught.exception.reason_code)

    def test_historical_rebuild_fails_closed_without_compatible_resources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, state, action = self._prepared_creative_retry(Path(temporary))
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            self._record_digest_mismatch_refusal(action)
            state["provenance"]["resources"]["aggregate_sha256"] = "0" * 64
            save_state(run_dir / "run.json", state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual("request_payload_unavailable", caught.exception.reason_code)

    def test_historical_refusal_requires_fresh_authority_then_dispatches_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, state, action = self._prepared_creative_retry(root)
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            save_state(run_dir / "run.json", state)

            old_request, old_paths = self._authority_files(
                root, run_dir, observed_at="2026-08-25T16:01:00Z", label="old",
            )
            old_output = root / "old-result.json"
            calls: list[str] = []
            with patch.dict(os.environ, {"SBE_QA_KEY": "provider-free"}), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: calls.append("POST"),
            ):
                self.assertEqual(3, v2_main(self._cli_argv(run_dir, old_paths, old_output)))
                first_refusal = load_json(old_output)
                self.assertEqual(3, v2_main(self._cli_argv(run_dir, old_paths, old_output)))
            old_result = validate_external_authority_v2_command_result_v2(
                load_json(old_output)
            )
            self.assertEqual("pre_provider_refusal", old_result["outcome"])
            self.assertEqual(
                "request_payload_digest_mismatch",
                old_result["dispatch_result"]["reason_code"],
            )
            self.assertEqual(
                "not_attempted",
                old_result["dispatch_result"]["provider_io_disposition"],
            )
            self.assertEqual(first_refusal["dispatch_result"], old_result["dispatch_result"])
            self.assertEqual([], calls)
            refused_before = deepcopy(
                load_json(run_dir / "run.json")["external_authority_v2_dispatch_history"]
            )

            fresh_request, fresh_paths = self._authority_files(
                root, run_dir, observed_at="2026-08-25T16:02:00Z", label="fresh",
            )
            self.assertNotEqual(
                old_request["external_authority_request_sha256"],
                fresh_request["external_authority_request_sha256"],
            )
            fresh_output = root / "fresh-result.json"

            def create(*_args, **_kwargs):
                calls.append("POST")
                return ({"id": "resp_fresh_payload_recovery", "status": "in_progress"}, 1)

            with patch.dict(os.environ, {"SBE_QA_KEY": "provider-free"}), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only", new=create,
            ):
                self.assertEqual(0, v2_main(self._cli_argv(run_dir, fresh_paths, fresh_output)))
                self.assertEqual(0, v2_main(self._cli_argv(run_dir, fresh_paths, fresh_output)))
            fresh_result = validate_external_authority_v2_command_result_v2(
                load_json(fresh_output)
            )
            self.assertEqual("exact_replay", fresh_result["outcome"])
            self.assertEqual(["POST"], calls)
            final_state = load_json(run_dir / "run.json")
            self.assertEqual(
                refused_before,
                final_state["external_authority_v2_dispatch_history"][:len(refused_before)],
            )

    def test_historical_rebuild_refuses_source_archive_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, state, action = self._prepared_creative_retry(root)
            artifact = action.pop("request_payload_artifact")
            Path(artifact["logical_path"]).unlink()
            self._record_digest_mismatch_refusal(action)
            record = state["passes"]["bre_1"]
            retained = Path(record["source_zip"])
            outside = root / "same-bytes-outside-workspace.zip"
            shutil.copyfile(retained, outside)
            record["source_zip"] = str(outside.resolve()).replace("\\", "/")
            save_state(run_dir / "run.json", state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                resolve_external_authority_v2_request_payload(run_dir, action)
            self.assertEqual("request_payload_unavailable", caught.exception.reason_code)


if __name__ == "__main__":
    unittest.main()
