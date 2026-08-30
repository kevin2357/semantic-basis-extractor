from __future__ import annotations

import copy
import io
import json
import os
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_execution_gap import make_ordinary_run
from astrowoof_natal_authoring import (
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
    validate_external_authority_v2_command_result_v2,
)
from astrowoof_natal_authoring.cli.external_authority_v2 import main
from astrowoof_natal_authoring.closure import (
    load_json, provider_request_payload_artifact, write_workspace_snapshot,
)
from astrowoof_natal_authoring.spend import digest as spend_digest


def _inputs(root: Path):
    run_dir = make_ordinary_run(root / "native")
    state = load_json(run_dir / "run.json")
    for index, action in enumerate(state["spend_ledger"]["actions"], 1):
        payload = {
            "model": action["binding"]["model"],
            "input": f"qualification request {index}",
            "max_output_tokens": action["binding"]["maximum_output_tokens"],
        }
        action["binding"]["request_sha256"] = spend_digest(payload)
        target = run_dir / "prepared" / action["action_id"] / "openai-request.json"
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(payload), encoding="utf-8")
        action["request_payload_artifact"] = provider_request_payload_artifact(
            target, payload,
        )
    (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    write_workspace_snapshot(run_dir)
    inspection = inspect_temporal_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at="2026-08-24T15:00:00Z",
    )
    request = build_external_authority_request_v2(inspection)
    inventory = {item["action_id"]: item for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]}
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action_id, "binding": copy.deepcopy(inventory[action_id]["binding"]),
        "authorization_reference": f"api-cli:{index}",
    } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
    grant = build_external_authority_grant_v2(
        request, inspection, documents, api_decision_id="api-cli-decision",
        issuer="astrowoof-api", issued_at="2026-08-24T15:00:01Z",
    )
    authority = root / "authority"
    authority.mkdir()
    paths = {}
    for name, value in (("inspection", inspection), ("request", request), ("grant", grant)):
        paths[name] = authority / f"{name}.json"
        paths[name].write_text(json.dumps(value), encoding="utf-8")
    paths["documents"] = []
    for index, document in enumerate(documents, 1):
        path = authority / f"authorization-{index}.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        paths["documents"].append(path)
    return run_dir, request, paths


class ExternalAuthorityV2CliSlice5(unittest.TestCase):
    def test_public_cli_emits_safe_ordered_execution_trace(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "result.json"
            event_stdout = io.StringIO()
            calls = []

            def create(_provider, payload, **_kwargs):
                calls.append(copy.deepcopy(payload))
                return ({"id": f"resp_trace_{len(calls)}", "status": "in_progress"}, 1)

            argv = [
                "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]), "--grant", str(paths["grant"]),
                "--provider", "openai", "--output", str(output),
                "--events-stdout-jsonl", "--invocation-id", "inv_trace_safe",
            ]
            for path in paths["documents"]:
                argv.extend(("--authorization", str(path)))
            with patch.dict(os.environ, {
                "SBE_QA_KEY": "protected-api-key-sentinel",
            }), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2."
                "OpenAIResponsesProvider.create_response_only", new=create,
            ), patch("sys.stdout", event_stdout):
                argv.extend(("--api-key-env", "SBE_QA_KEY"))
                self.assertEqual(0, main(argv))

            envelopes = [
                json.loads(line) for line in event_stdout.getvalue().splitlines()
            ]
            names = [item["event_name"] for item in envelopes]
            self.assertEqual(
                [
                    "external_authority.request_selected",
                    "external_authority.fence_validated",
                    "external_authority.intent_committed",
                ],
                names[:3],
            )
            self.assertEqual(1, names.count(
                "external_authority.provider_create_permitted"
            ))
            permission = next(
                item for item in envelopes
                if item["event_name"] == "external_authority.provider_create_permitted"
            )
            self.assertEqual(
                len(request["ordered_action_ids"]), permission["data"]["action_count"],
            )
            self.assertEqual(len(request["ordered_action_ids"]), names.count(
                "provider.identity_recorded"
            ))
            rendered = event_stdout.getvalue()
            self.assertNotIn("protected-api-key-sentinel", rendered)
            self.assertNotIn("qualification request", rendered)
            self.assertNotIn("authorization_reference", rendered)

    def test_refusal_event_is_typed_and_event_sink_failure_cannot_change_dispatch(self):
        from astrowoof_natal_authoring.external_authority_v2_execution import (
            ExternalAuthorityV2ExecutionError,
        )

        for failing_sink in (False, True):
            with self.subTest(failing_sink=failing_sink), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                run_dir, _, paths = _inputs(root)
                output = root / "result.json"
                events = root / "events.jsonl"
                argv = [
                    "--run-dir", str(run_dir),
                    "--inspection", str(paths["inspection"]),
                    "--request", str(paths["request"]),
                    "--grant", str(paths["grant"]),
                    "--provider", "openai", "--api-key-env", "SBE_QA_KEY",
                    "--output", str(output), "--events-jsonl", str(events),
                ]
                for path in paths["documents"]:
                    argv.extend(("--authorization", str(path)))
                sink_patch = (
                    patch(
                        "astrowoof_natal_authoring.execution_events."
                        "JsonlEventSink.__call__",
                        side_effect=OSError("scripted diagnostic sink failure"),
                    )
                    if failing_sink else nullcontext()
                )
                captured_stderr = io.StringIO()
                with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                    "astrowoof_natal_authoring.cli.external_authority_v2."
                    "resolve_external_authority_v2_request_payload",
                    side_effect=ExternalAuthorityV2ExecutionError(
                        "request_payload_unavailable", "protected-payload-sentinel",
                    ),
                ), patch("sys.stderr", captured_stderr), sink_patch:
                    self.assertEqual(3, main(argv))
                result = validate_external_authority_v2_command_result_v2(load_json(output))
                self.assertEqual("pre_provider_refusal", result["outcome"])
                self.assertEqual("not_attempted", result["dispatch_result"][
                    "provider_io_disposition"
                ])
                self.assertNotIn("protected-payload-sentinel", captured_stderr.getvalue())
                self.assertNotIn("qualification request", captured_stderr.getvalue())
                if not failing_sink:
                    envelopes = [
                        json.loads(line)
                        for line in events.read_text(encoding="utf-8").splitlines()
                    ]
                    refusal = next(
                        item for item in envelopes
                        if item["event_name"] == "external_authority.refused"
                    )
                    self.assertEqual("request_payload_unavailable", refusal["data"][
                        "reason_code"
                    ])
                    self.assertNotIn("protected-payload-sentinel", json.dumps(envelopes))

    def test_provider_capable_cli_dispatch_and_exact_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "result.json"
            calls = []

            def create(_provider, payload, **_kwargs):
                calls.append(copy.deepcopy(payload))
                return ({"id": f"resp_cli_{len(calls)}", "status": "in_progress"}, 1)

            argv = [
                "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]), "--grant", str(paths["grant"]),
                "--provider", "openai", "--output", str(output),
            ]
            for path in paths["documents"]:
                argv.extend(("--authorization", str(path)))
            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2.OpenAIResponsesProvider.create_response_only",
                new=create,
            ):
                argv.extend(("--api-key-env", "SBE_QA_KEY"))
                self.assertEqual(0, main(argv))
                first = validate_external_authority_v2_command_result_v2(load_json(output))
                self.assertEqual("detached_provider_pending", first["outcome"])
                self.assertEqual(len(request["ordered_action_ids"]), len(calls))
                self.assertEqual(0, main(argv))
                replay = validate_external_authority_v2_command_result_v2(load_json(output))
                self.assertEqual("exact_replay", replay["outcome"])
                self.assertIsNone(replay["intent_result"])
                self.assertEqual(len(request["ordered_action_ids"]), len(calls))

    def test_grant_free_cli_is_passive_and_output_cannot_enter_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _, paths = _inputs(root)
            before = (run_dir / "run.json").read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()
            output = root / "passive.json"
            self.assertEqual(3, main([
                "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]), "--output", str(output),
            ]))
            self.assertEqual("awaiting_compatible_grant", load_json(output)["outcome"])
            self.assertEqual(before, ((run_dir / "run.json").read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()))
            with self.assertRaisesRegex(ValueError, "outside"):
                main([
                    "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                    "--request", str(paths["request"]),
                    "--output", str(run_dir / "forbidden.json"),
                ])


if __name__ == "__main__":
    unittest.main()
