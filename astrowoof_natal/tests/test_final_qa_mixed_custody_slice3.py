from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_contract import (
    authority_inputs,
)
from astrowoof_natal_authoring import (
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
)
from astrowoof_natal_authoring.closure import (
    load_json,
    persist_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle


POLISH_ACTION = "paid_00000000000000000000000a"
SECONDARY_ACTION = "paid_00000000000000000000000b"


def _final_qa_warning_authority(root: Path):
    run_dir, _, _, _, _ = authority_inputs(root)
    state = load_json(run_dir / "run.json")
    state["spend_ledger"]["actions"] = [
        action
        for action in state["spend_ledger"]["actions"]
        if (action.get("binding") or {}).get("stage") == "polish"
    ]
    state["spend_ledger"]["actions"][0]["action_id"] = POLISH_ACTION
    state["subjects"] = {
        "glimmer-fixture": {
            "subject": "glimmer-fixture",
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
    # This is the valid authority checkpoint: the prepared action outranks the
    # provisional subject warning.
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8",
    )
    write_workspace_snapshot(run_dir)
    inspection = inspect_temporal_lifecycle(
        run_dir,
        native_exclusive_access="declared",
        observed_at="2026-08-31T12:00:00Z",
    )
    from astrowoof_natal_authoring import (
        build_external_authority_grant_v2,
        build_external_authority_request_v2,
    )

    request = build_external_authority_request_v2(inspection)
    inventory = {
        action["action_id"]: action
        for action in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action_id,
        "binding": copy.deepcopy(inventory[action_id]["binding"]),
        "authorization_reference": "api-auth:glimmer-fixture",
    } for action_id in request["ordered_action_ids"]]
    grant = build_external_authority_grant_v2(
        request,
        inspection,
        documents,
        api_decision_id="api-decision-glimmer-fixture",
        issuer="astrowoof-api",
        issued_at="2026-08-31T12:00:01Z",
    )
    return run_dir, inspection, request, documents, grant


class FinalQaMixedCustodySlice3Characterization(unittest.TestCase):
    def _provider_bound_with_secondary(self, root: Path, secondary_state: str):
        run_dir, inspection, request, documents, grant = (
            _final_qa_warning_authority(root)
        )
        commit_external_authority_v2_dispatch_intent(
            run_dir,
            request=request,
            inspection=inspection,
            grant=grant,
            authorization_documents=documents,
        )
        dispatch_external_authority_v2_intent(
            run_dir,
            request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"],
            create=lambda _action: {
                "kind": "response", "id": "resp_mixed_inventory",
            },
        )
        state = load_json(run_dir / "run.json")
        secondary = copy.deepcopy(state["spend_ledger"]["actions"][0])
        secondary["action_id"] = SECONDARY_ACTION
        secondary["state"] = secondary_state
        secondary["provider"] = None
        secondary["authorization"] = None
        secondary["consumption"] = None
        secondary["attempts"] = []
        state["spend_ledger"]["actions"].append(secondary)
        persist_state(run_dir / "run.json", state)
        write_workspace_snapshot(run_dir)
        return run_dir

    def test_durable_custody_outranks_different_prepared_action(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self._provider_bound_with_secondary(
                Path(temporary), "PREPARED",
            )
            state = load_json(run_dir / "run.json")
            self.assertEqual("WAITING_FOR_RESPONSE", state["status"])
            lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
            )
            self.assertFalse(lifecycle["terminal"]["terminal"])
            self.assertEqual(
                [POLISH_ACTION], lifecycle["provider_custody"]["action_ids"],
            )
            self.assertNotEqual(
                "await_external_authority",
                lifecycle["execution_branch"]["command"],
            )
            temporal = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2099-01-01T00:00:00Z",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                temporal["temporal_decision"]["selected_command"],
            )

            state["spend_ledger"]["actions"] = [
                action for action in state["spend_ledger"]["actions"]
                if action["action_id"] == SECONDARY_ACTION
            ]
            persist_state(run_dir / "run.json", state)
            self.assertEqual(
                "AWAITING_SPEND_AUTHORIZATION",
                load_json(run_dir / "run.json")["status"],
            )

    def test_durable_custody_outranks_different_budget_refusal(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self._provider_bound_with_secondary(
                Path(temporary), "BUDGET_EXHAUSTED",
            )
            state = load_json(run_dir / "run.json")
            self.assertEqual("WAITING_FOR_RESPONSE", state["status"])
            lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
            )
            self.assertFalse(lifecycle["terminal"]["terminal"])
            self.assertEqual(
                [POLISH_ACTION], lifecycle["provider_custody"]["action_ids"],
            )
            temporal = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2099-01-01T00:00:00Z",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                temporal["temporal_decision"]["selected_command"],
            )

            state["spend_ledger"]["actions"] = [
                action for action in state["spend_ledger"]["actions"]
                if action["action_id"] == SECONDARY_ACTION
            ]
            persist_state(run_dir / "run.json", state)
            self.assertEqual(
                "BUDGET_EXHAUSTED", load_json(run_dir / "run.json")["status"],
            )

    def test_public_v2_command_returns_typed_post_intent_refusal(self):
        from astrowoof_natal_authoring import (
            validate_external_authority_v2_command_result_v3,
        )
        from astrowoof_natal_authoring.cli import external_authority_v2 as cli

        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            run_dir, inspection, request, documents, grant = (
                _final_qa_warning_authority(outer)
            )
            inputs = outer / "refusal-inputs"
            inputs.mkdir()
            values = {
                "inspection": inspection,
                "request": request,
                "grant": grant,
            }
            paths = {}
            for name, value in values.items():
                paths[name] = inputs / f"{name}.json"
                paths[name].write_text(json.dumps(value), encoding="utf-8")
            authorization_paths = []
            for index, document in enumerate(documents):
                path = inputs / f"authorization-{index}.json"
                path.write_text(json.dumps(document), encoding="utf-8")
                authorization_paths.append(path)
            output = inputs / "result.json"
            argv = [
                "--run-dir", str(run_dir),
                "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]),
                "--grant", str(paths["grant"]),
                "--provider", "openai",
                "--output", str(output),
                "--log-level", "CRITICAL",
            ]
            for path in authorization_paths:
                argv.extend(["--authorization", str(path)])

            def commit_then_corrupt(*args, **kwargs):
                result = commit_external_authority_v2_dispatch_intent(
                    *args, **kwargs
                )
                state = load_json(run_dir / "run.json")
                state["status"] = "FINAL_QA_REQUIRES_REVIEW"
                (run_dir / "run.json").write_text(
                    json.dumps(state, indent=2) + "\n", encoding="utf-8",
                )
                write_workspace_snapshot(run_dir)
                return result

            calls: list[str] = []
            with patch.dict(os.environ, {"OPENAI_API_KEY": "provider-free"}), patch.object(
                cli,
                "commit_external_authority_v2_dispatch_intent",
                side_effect=commit_then_corrupt,
            ), patch.object(
                cli,
                "resolve_external_authority_v2_request_payload",
                side_effect=AssertionError("refusal reached payload resolution"),
            ), patch.object(
                cli.OpenAIResponsesProvider,
                "create_response_only",
                side_effect=lambda *_args, **_kwargs: calls.append("POST"),
            ):
                self.assertEqual(3, cli.main(argv))
            command = json.loads(output.read_text(encoding="utf-8"))
            validate_external_authority_v2_command_result_v3(command)
            self.assertEqual(
                "astrowoof.external_authority_v2_command_result.v3",
                command["schema_version"],
            )
            self.assertEqual("pre_provider_refusal", command["outcome"])
            self.assertEqual(
                "post_intent_lifecycle_contradiction",
                command["dispatch_result"]["reason_code"],
            )
            self.assertEqual([], calls)

    def test_public_v2_command_keeps_pending_polish_nonterminal(self):
        from astrowoof_natal_authoring.cli import external_authority_v2 as cli

        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            run_dir, inspection, request, documents, grant = (
                _final_qa_warning_authority(outer)
            )
            inputs = outer / "public-inputs"
            inputs.mkdir()
            inspection_path = inputs / "inspection.json"
            request_path = inputs / "request.json"
            grant_path = inputs / "grant.json"
            output_path = inputs / "command-result.json"
            inspection_path.write_text(json.dumps(inspection), encoding="utf-8")
            request_path.write_text(json.dumps(request), encoding="utf-8")
            grant_path.write_text(json.dumps(grant), encoding="utf-8")
            authorization_paths = []
            for index, document in enumerate(documents):
                path = inputs / f"authorization-{index}.json"
                path.write_text(json.dumps(document), encoding="utf-8")
                authorization_paths.append(path)
            argv = [
                "--run-dir", str(run_dir),
                "--inspection", str(inspection_path),
                "--request", str(request_path),
                "--grant", str(grant_path),
                "--provider", "openai",
                "--output", str(output_path),
                "--log-level", "CRITICAL",
            ]
            for path in authorization_paths:
                argv.extend(["--authorization", str(path)])
            calls: list[str] = []
            with patch.dict(os.environ, {"OPENAI_API_KEY": "provider-free"}), patch.object(
                cli,
                "resolve_external_authority_v2_request_payload",
                return_value={"model": "scripted", "input": []},
            ), patch.object(
                cli.OpenAIResponsesProvider,
                "create_response_only",
                side_effect=lambda *_args, **_kwargs: (
                    calls.append("POST")
                    or ({"id": "resp_public_glimmer", "status": "queued"}, 1)
                ),
            ):
                self.assertEqual(0, cli.main(argv))
            command = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("detached_provider_pending", command["outcome"])
            self.assertEqual(["POST"], calls)
            state = load_json(run_dir / "run.json")
            self.assertEqual("WAITING_FOR_RESPONSE", state["status"])
            self.assertEqual(
                "PROVIDER_PENDING",
                state["external_authority_v2_dispatch_intent"]["state"],
            )
            lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
            )
            self.assertFalse(lifecycle["terminal"]["terminal"])
            self.assertTrue(lifecycle["terminal"]["provider_continuation_remains"])
            temporal = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2099-01-01T00:00:00Z",
            )
            self.assertFalse(temporal["checkpoint_basis"]["terminal"]["terminal"])
            self.assertEqual(
                "provider_reconciliation_cycle",
                temporal["temporal_decision"]["selected_command"],
            )
            self.assertEqual(
                [POLISH_ACTION], temporal["temporal_decision"]["due_action_ids"]
            )
            self.assertFalse((run_dir / "native-result-index.json").exists())

    def test_real_v2_path_preserves_nonterminal_provider_custody(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = (
                _final_qa_warning_authority(Path(temporary))
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=request,
                inspection=inspection,
                grant=grant,
                authorization_documents=documents,
            )
            after_intent = load_json(run_dir / "run.json")
            self.assertEqual("AUTHORING", after_intent["status"])
            self.assertEqual(
                "INTENT_COMMITTED",
                after_intent["external_authority_v2_dispatch_intent"]["state"],
            )

            creates: list[str] = []
            result = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: (
                    creates.append(action["action_id"])
                    or {"kind": "response", "id": "resp_glimmer_fixture"}
                ),
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual([POLISH_ACTION], creates)
            state = load_json(run_dir / "run.json")
            self.assertEqual("WAITING_FOR_RESPONSE", state["status"])
            self.assertEqual("WAITING", state["spend_ledger"]["actions"][0]["state"])
            self.assertEqual(
                "resp_glimmer_fixture",
                state["spend_ledger"]["actions"][0]["provider"]["id"],
            )
            self.assertEqual(
                "PROVIDER_PENDING",
                state["external_authority_v2_dispatch_intent"]["state"],
            )
            lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
            )
            self.assertFalse(lifecycle["terminal"]["terminal"])
            self.assertTrue(lifecycle["terminal"]["provider_continuation_remains"])
            self.assertFalse((run_dir / "native-result-index.json").exists())

    def test_call_entry_ambiguity_outranks_review_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = (
                _final_qa_warning_authority(Path(temporary))
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=request,
                inspection=inspection,
                grant=grant,
                authorization_documents=documents,
            )
            result = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda _action: (_ for _ in ()).throw(
                    TimeoutError("provider acceptance unknown")
                ),
            )
            self.assertEqual("ambiguous_submission", result["outcome"])
            state = load_json(run_dir / "run.json")
            self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", state["status"])
            self.assertEqual(
                "AMBIGUOUS_PROVIDER_SUBMISSION",
                state["spend_ledger"]["actions"][0]["state"],
            )
            self.assertFalse((run_dir / "native-result-index.json").exists())

    def test_providerless_authorized_polish_remains_nonterminal(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _, _, _, _ = _final_qa_warning_authority(Path(temporary))
            state = load_json(run_dir / "run.json")
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "AUTHORIZED"
            action["authorization"] = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "authorization_reference": "api-auth:providerless-control",
            }
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            persisted = load_json(run_dir / "run.json")
            self.assertEqual("AUTHORING", persisted["status"])
            self.assertIsNone(action.get("provider"))
            self.assertFalse((run_dir / "native-result-index.json").exists())

    def test_post_intent_terminal_contradiction_refuses_before_provider_io(self):
        from astrowoof_natal_authoring import (
            ExternalAuthorityV2ExecutionError,
            build_external_authority_grant_v2,
            build_external_authority_request_v2,
            build_external_authority_v2_command_result_v3,
            read_external_authority_provider_dispatch_result_v4_schema,
            read_external_authority_v2_command_result_v3_schema,
            validate_external_authority_provider_dispatch_result_v4,
            validate_external_authority_v2_command_result_v3,
        )

        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = (
                _final_qa_warning_authority(Path(temporary))
            )
            intent_result = commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=request,
                inspection=inspection,
                grant=grant,
                authorization_documents=documents,
            )
            state = load_json(run_dir / "run.json")
            state["status"] = "FINAL_QA_REQUIRES_REVIEW"
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            write_workspace_snapshot(run_dir)
            calls: list[str] = []
            result = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                prepare=lambda *_args: self.fail("refusal reached preparation"),
                create=lambda _action: calls.append("POST"),
            )
            validate_external_authority_provider_dispatch_result_v4(result)
            command = build_external_authority_v2_command_result_v3(
                intent_result=intent_result, dispatch_result=result,
            )
            validate_external_authority_v2_command_result_v3(command)
            self.assertEqual(
                "astrowoof.external_authority_provider_dispatch_result.v4",
                read_external_authority_provider_dispatch_result_v4_schema()["$id"],
            )
            self.assertEqual(
                "astrowoof.external_authority_v2_command_result.v3",
                read_external_authority_v2_command_result_v3_schema()["$id"],
            )
            self.assertEqual("pre_provider_refusal", result["outcome"])
            self.assertEqual(
                "post_intent_lifecycle_contradiction", result["reason_code"]
            )
            self.assertEqual("not_attempted", result["provider_io_disposition"])
            self.assertEqual([], calls)
            mutated = copy.deepcopy(result)
            mutated["refused_action_ids"] = []
            body = {
                key: value for key, value in mutated.items()
                if key != "result_sha256"
            }
            mutated["result_sha256"] = hashlib.sha256(json.dumps(
                body, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
            with self.assertRaises(ValueError):
                validate_external_authority_provider_dispatch_result_v4(mutated)
            refused = load_json(run_dir / "run.json")
            self.assertNotIn("external_authority_v2_dispatch_intent", refused)
            self.assertEqual("AWAITING_SPEND_AUTHORIZATION", refused["status"])
            self.assertEqual(
                "PREPARED", refused["spend_ledger"]["actions"][0]["state"]
            )
            history = refused["external_authority_v2_dispatch_history"][-1]
            self.assertEqual(
                "post_intent_lifecycle_contradiction", history["reason_code"]
            )
            replay = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                prepare=lambda *_args: self.fail("replay reached preparation"),
                create=lambda _action: calls.append("POST"),
            )
            self.assertEqual(result, replay)
            self.assertEqual([], calls)

            fresh_inspection = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-31T12:00:02Z",
            )
            fresh_request = build_external_authority_request_v2(fresh_inspection)
            self.assertNotEqual(
                request["external_authority_request_sha256"],
                fresh_request["external_authority_request_sha256"],
            )
            with self.assertRaises(ExternalAuthorityV2ExecutionError):
                commit_external_authority_v2_dispatch_intent(
                    run_dir,
                    request=request,
                    inspection=inspection,
                    grant=grant,
                    authorization_documents=documents,
                )
            inventory = {
                item["action_id"]: item
                for item in fresh_inspection["checkpoint_basis"][
                    "action_inventory"
                ]["actions"]
            }
            fresh_documents = [{
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": copy.deepcopy(inventory[action_id]["binding"]),
                "authorization_reference": "api-auth:fresh-after-refusal",
            } for action_id in fresh_request["ordered_action_ids"]]
            fresh_grant = build_external_authority_grant_v2(
                fresh_request,
                fresh_inspection,
                fresh_documents,
                api_decision_id="api-decision-fresh-after-refusal",
                issuer="astrowoof-api",
                issued_at="2026-08-31T12:00:03Z",
            )
            committed = commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=fresh_request,
                inspection=fresh_inspection,
                grant=fresh_grant,
                authorization_documents=fresh_documents,
            )
            self.assertEqual("intent_committed", committed["outcome"])

    def test_no_custody_final_qa_warning_is_a_legitimate_terminal_shape(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _, _, _, _ = _final_qa_warning_authority(Path(temporary))
            state = load_json(run_dir / "run.json")
            state["spend_ledger"]["actions"] = []
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
            )
            self.assertEqual("FINAL_QA_REQUIRES_REVIEW", load_json(
                run_dir / "run.json"
            )["status"])
            self.assertTrue(lifecycle["terminal"]["terminal"])
            self.assertFalse(lifecycle["terminal"]["provider_continuation_remains"])
            self.assertEqual([], lifecycle["provider_custody"]["action_ids"])


if __name__ == "__main__":
    unittest.main()
