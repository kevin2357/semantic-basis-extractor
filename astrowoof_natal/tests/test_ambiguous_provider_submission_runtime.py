from __future__ import annotations

import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_cli import _inputs
from astrowoof_natal_authoring import (
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
    validate_external_authority_v2_command_result_v2,
)
from astrowoof_natal_authoring.cli.external_authority_v2 import main
from astrowoof_natal_authoring.closure import (
    load_json, validate_workspace_snapshot, write_workspace_snapshot,
)
from astrowoof_natal_authoring.external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_prepared_create,
    build_external_authority_prepared_create_basis,
)


def cli_argv(run_dir: Path, paths: dict, output: Path) -> list[str]:
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
    return argv


class AmbiguousProviderSubmissionRuntimeWaypoint2(unittest.TestCase):
    def test_pre_provider_refusal_seals_invocation_and_requires_fresh_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, old_request, paths = _inputs(root)
            output = root / "result.json"
            argv = cli_argv(run_dir, paths, output)
            provider_calls: list[str] = []

            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2."
                "resolve_external_authority_v2_request_payload",
                side_effect=ExternalAuthorityV2ExecutionError(
                    "request_payload_unavailable", "scripted missing payload",
                ),
            ), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: provider_calls.append("POST"),
            ):
                self.assertEqual(3, main(argv))
                first = validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                )
                self.assertEqual(3, main(argv))
                replay = validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                )

            self.assertEqual([], provider_calls)
            self.assertEqual("pre_provider_refusal", first["outcome"])
            self.assertEqual("not_attempted", first["dispatch_result"]["provider_io_disposition"])
            self.assertEqual(first["dispatch_result"], replay["dispatch_result"])
            self.assertIsNotNone(first["intent_result"])
            self.assertIsNone(replay["intent_result"])

            state = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, state)
            refused_id = old_request["ordered_action_ids"][0]
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == refused_id
            )
            self.assertEqual("PREPARED", action["state"])
            self.assertIsNone(action["authorization"])
            self.assertNotIn("consumption", action)
            self.assertEqual(1, len(action["external_authority_v2_refused_invocations"]))
            self.assertEqual(1, len(state["external_authority_v2_dispatch_history"]))
            self.assertNotIn("external_authority_v2_dispatch_intent", state)

            fresh_inspection = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T15:10:00Z",
            )
            fresh_request = build_external_authority_request_v2(fresh_inspection)
            self.assertNotEqual(
                old_request["external_authority_request_sha256"],
                fresh_request["external_authority_request_sha256"],
            )
            self.assertEqual(old_request["ordered_action_ids"], fresh_request["ordered_action_ids"])
            inventory = {
                item["action_id"]: item
                for item in fresh_inspection["checkpoint_basis"]["action_inventory"]["actions"]
            }
            fresh_documents = [{
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": inventory[action_id]["binding"],
                "authorization_reference": f"fresh:{index}",
            } for index, action_id in enumerate(fresh_request["ordered_action_ids"], 1)]
            fresh_grant = build_external_authority_grant_v2(
                fresh_request, fresh_inspection, fresh_documents,
                api_decision_id="fresh-decision", issuer="astrowoof-api",
                issued_at="2026-08-25T15:10:01Z",
            )
            fresh_intent = commit_external_authority_v2_dispatch_intent(
                run_dir, request=fresh_request, inspection=fresh_inspection,
                grant=fresh_grant, authorization_documents=fresh_documents,
            )
            self.assertEqual("intent_committed", fresh_intent["outcome"])

    def test_each_closed_pre_provider_reason_is_zero_io_and_seals_one_invocation(self):
        reasons = (
            "request_payload_unavailable", "request_payload_ambiguous",
            "request_payload_digest_mismatch",
        )
        for reason in reasons:
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                run_dir, request, paths = _inputs(root)
                output = root / "result.json"
                calls: list[str] = []
                with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                    "astrowoof_natal_authoring.cli.external_authority_v2."
                    "resolve_external_authority_v2_request_payload",
                    side_effect=ExternalAuthorityV2ExecutionError(reason, "scripted"),
                ), patch(
                    "astrowoof_natal_authoring.closure."
                    "OpenAIResponsesProvider.create_response_only",
                    side_effect=lambda *_args, **_kwargs: calls.append("POST"),
                ):
                    self.assertEqual(3, main(cli_argv(run_dir, paths, output)))
                result = validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                )
                self.assertEqual([], calls)
                self.assertEqual(reason, result["dispatch_result"]["reason_code"])
                state = load_json(run_dir / "run.json")
                self.assertEqual(1, len(state["external_authority_v2_dispatch_history"]))
                self.assertTrue(all(
                    action["state"] == "PREPARED"
                    and action.get("authorization") is None
                    and "consumption" not in action
                    for action in state["spend_ledger"]["actions"]
                    if action["action_id"] in request["ordered_action_ids"]
                ))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "result.json"
            calls: list[str] = []
            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2.OpenAIResponsesProvider",
                side_effect=ValueError("scripted invalid configuration"),
            ), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: calls.append("POST"),
            ):
                self.assertEqual(3, main(cli_argv(run_dir, paths, output)))
            result = validate_external_authority_v2_command_result_v2(
                json.loads(output.read_text(encoding="utf-8"))
            )
            self.assertEqual([], calls)
            self.assertEqual(
                "provider_configuration_invalid",
                result["dispatch_result"]["reason_code"],
            )
            state = load_json(run_dir / "run.json")
            self.assertEqual(1, len(state["external_authority_v2_dispatch_history"]))
            self.assertTrue(all(
                action["state"] == "PREPARED"
                for action in state["spend_ledger"]["actions"]
                if action["action_id"] in request["ordered_action_ids"]
            ))

    def test_provider_bound_prefix_is_preserved_and_later_member_is_not_entered(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "result.json"
            prepared: list[str] = []
            calls: list[str] = []

            from astrowoof_natal_authoring.external_authority_v2_execution import (
                resolve_external_authority_v2_request_payload as real_resolver,
            )
            def resolve(run_root, action):
                prepared.append(action["action_id"])
                if len(prepared) == 2:
                    raise ExternalAuthorityV2ExecutionError(
                        "request_payload_unavailable", "scripted second-member refusal",
                    )
                return real_resolver(run_root, action)

            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2."
                "resolve_external_authority_v2_request_payload", side_effect=resolve,
            ), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: (
                    calls.append("POST") or ({"id": "resp_prefix", "status": "in_progress"}, 1)
                ),
            ):
                self.assertEqual(3, main(cli_argv(run_dir, paths, output)))
            result = validate_external_authority_v2_command_result_v2(
                json.loads(output.read_text(encoding="utf-8"))
            )["dispatch_result"]
            self.assertEqual(["POST"], calls)
            self.assertEqual(request["ordered_action_ids"], prepared)
            self.assertEqual(request["ordered_action_ids"][:1], result["provider_bound_action_ids"])
            self.assertEqual(request["ordered_action_ids"][1:], result["refused_action_ids"])
            state = load_json(run_dir / "run.json")
            actions = {item["action_id"]: item for item in state["spend_ledger"]["actions"]}
            self.assertEqual("WAITING", actions[request["ordered_action_ids"][0]]["state"])
            self.assertEqual("PREPARED", actions[request["ordered_action_ids"][1]]["state"])

    def test_three_member_refusal_preserves_prefix_and_never_prepares_suffix(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _, _ = _inputs(root)
            state = load_json(run_dir / "run.json")
            third = deepcopy(state["spend_ledger"]["actions"][0])
            third["action_id"] = "paid_00000000000000000000000c"
            third["binding"]["stage"] = "qualitative_candidate"
            third["binding"]["route"] = "qualitative_candidate:attempt-001"
            third["binding"]["request_sha256"] = "c" * 64
            state["spend_ledger"]["actions"].append(third)
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            write_workspace_snapshot(run_dir)
            inspection = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T15:20:00Z",
            )
            request = build_external_authority_request_v2(inspection)
            self.assertEqual(3, len(request["ordered_action_ids"]))
            inventory = {
                item["action_id"]: item
                for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
            }
            documents = [{
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": inventory[action_id]["binding"],
                "authorization_reference": f"three-member:{index}",
            } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="three-member-decision", issuer="astrowoof-api",
                issued_at="2026-08-25T15:20:01Z",
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            prepared: list[str] = []
            calls: list[str] = []

            def prepare(action, context):
                prepared.append(action["action_id"])
                refused = len(prepared) == 2
                basis = build_external_authority_prepared_create_basis(
                    action, run_id=context["run_id"],
                    request_sha256=context["request_sha256"],
                    grant_sha256=context["grant_sha256"],
                    checkpoint_snapshot_sha256=context["checkpoint_snapshot_sha256"],
                    local_request_key_sha256="1" * 64,
                    provider_configuration_sha256="2" * 64,
                    outcome="refused" if refused else "ready",
                    reason_code="request_payload_unavailable" if refused else None,
                )
                return build_external_authority_prepared_create(
                    basis=basis,
                    transport_context=None if refused else {"scripted": True},
                )

            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], prepare=prepare,
                create=lambda _prepared: (
                    calls.append(prepared[-1])
                    or {"kind": "response", "id": "resp_three_member_prefix"}
                ),
            )
            first, second, third_id = request["ordered_action_ids"]
            self.assertEqual([first, second], prepared)
            self.assertEqual([first], calls)
            self.assertEqual([first], result["provider_bound_action_ids"])
            self.assertEqual([second], result["refused_action_ids"])
            current = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, current)
            actions = {item["action_id"]: item for item in current["spend_ledger"]["actions"]}
            self.assertEqual("WAITING", actions[first]["state"])
            self.assertEqual("PREPARED", actions[second]["state"])
            self.assertEqual("PREPARED", actions[third_id]["state"])
            self.assertEqual(
                "not_entered_after_refusal",
                actions[third_id]["external_authority_v2_refused_invocations"][0][
                    "member_disposition"
                ],
            )
            self.assertIsNone(actions[third_id]["authorization"])
            self.assertNotIn("consumption", actions[third_id])

    def test_checkpoint_change_after_preparation_is_typed_refusal_without_create(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            inspection = json.loads(paths["inspection"].read_text(encoding="utf-8"))
            grant = json.loads(paths["grant"].read_text(encoding="utf-8"))
            documents = [json.loads(path.read_text(encoding="utf-8")) for path in paths["documents"]]
            commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            mutated = False
            def prepare(action, context):
                nonlocal mutated
                basis = build_external_authority_prepared_create_basis(
                    action, run_id=context["run_id"], request_sha256=context["request_sha256"],
                    grant_sha256=context["grant_sha256"],
                    checkpoint_snapshot_sha256=context["checkpoint_snapshot_sha256"],
                    local_request_key_sha256="1" * 64,
                    provider_configuration_sha256="2" * 64,
                    outcome="ready", reason_code=None,
                )
                if not mutated:
                    state = load_json(run_dir / "run.json")
                    state["test_checkpoint_marker"] = "changed after preparation"
                    from astrowoof_natal_authoring.closure import persist_state, write_workspace_snapshot
                    persist_state(run_dir / "run.json", state)
                    write_workspace_snapshot(run_dir)
                    mutated = True
                return build_external_authority_prepared_create(
                    basis=basis, transport_context={"scripted": True},
                )
            calls: list[str] = []
            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], prepare=prepare,
                create=lambda _prepared: calls.append("POST"),
            )
            self.assertEqual([], calls)
            self.assertEqual("pre_provider_refusal", result["outcome"])
            self.assertEqual("checkpoint_changed_before_create", result["reason_code"])
            replay = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], prepare=prepare,
                create=lambda _prepared: calls.append("POST"),
            )
            self.assertEqual(result, replay)
            self.assertEqual([], calls)

    def test_transport_failure_is_durable_ambiguity_and_replay_makes_no_second_call(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            output = root / "result.json"
            argv = cli_argv(run_dir, paths, output)
            calls: list[str] = []

            def fail_transport(*_args, **_kwargs):
                calls.append("POST")
                raise TimeoutError("scripted transport uncertainty")

            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=fail_transport,
            ):
                self.assertEqual(3, main(argv))
                first = validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                )
                self.assertEqual(3, main(argv))
                replay = validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                )

            self.assertEqual(["POST"], calls)
            self.assertEqual("ambiguous_submission", first["outcome"])
            self.assertEqual(
                "create_entered_unknown",
                first["dispatch_result"]["provider_io_disposition"],
            )
            self.assertEqual(first["dispatch_result"], replay["dispatch_result"])
            state = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, state)
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == request["ordered_action_ids"][0]
            )
            self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", action["state"])

    def test_malformed_returned_identity_is_ambiguous_not_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, _, paths = _inputs(root)
            output = root / "result.json"
            argv = cli_argv(run_dir, paths, output)
            calls: list[str] = []
            with patch.dict(os.environ, {"SBE_QA_KEY": "qualification"}), patch(
                "astrowoof_natal_authoring.closure."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: (
                    calls.append("POST") or ({"status": "in_progress"}, 1)
                ),
            ):
                self.assertEqual(3, main(argv))
            result = validate_external_authority_v2_command_result_v2(
                json.loads(output.read_text(encoding="utf-8"))
            )
            self.assertEqual(["POST"], calls)
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual(
                "provider_returned_invalid_identity",
                result["dispatch_result"]["reason_code"],
            )

    def test_interrupted_after_fence_is_recovered_as_ambiguity_without_create(self):
        class SimulatedExit(BaseException):
            pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, paths = _inputs(root)
            inspection = json.loads(paths["inspection"].read_text(encoding="utf-8"))
            grant = json.loads(paths["grant"].read_text(encoding="utf-8"))
            documents = [json.loads(path.read_text(encoding="utf-8")) for path in paths["documents"]]
            from astrowoof_natal_authoring import commit_external_authority_v2_dispatch_intent
            commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )

            def prepare(action, context):
                basis = build_external_authority_prepared_create_basis(
                    action, run_id=context["run_id"],
                    request_sha256=context["request_sha256"],
                    grant_sha256=context["grant_sha256"],
                    checkpoint_snapshot_sha256=context["checkpoint_snapshot_sha256"],
                    local_request_key_sha256="1" * 64,
                    provider_configuration_sha256="2" * 64,
                    outcome="ready", reason_code=None,
                )
                return build_external_authority_prepared_create(
                    basis=basis, transport_context={"scripted": True},
                )

            def interrupt(point):
                if point.startswith("after_call_fence_before_transport:"):
                    raise SimulatedExit()

            with self.assertRaises(SimulatedExit):
                dispatch_external_authority_v2_intent(
                    run_dir,
                    request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"],
                    prepare=prepare,
                    create=lambda _prepared: self.fail("provider create should not run"),
                    failure_injector=interrupt,
                )
            calls: list[str] = []
            recovered = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                prepare=prepare,
                create=lambda _prepared: calls.append("POST"),
            )
            self.assertEqual([], calls)
            self.assertEqual("ambiguous_submission", recovered["outcome"])
            self.assertEqual(
                "provider_call_interrupted_after_fence", recovered["reason_code"]
            )
            validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))


if __name__ == "__main__":
    unittest.main()
