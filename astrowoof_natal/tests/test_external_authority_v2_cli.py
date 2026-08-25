from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
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
