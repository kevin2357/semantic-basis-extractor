from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_contract import authority_inputs
from astrowoof_natal.tests import (
    test_moxie_terminal_review_inventory_slice3 as moxie_fixture,
)
from astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 import (
    _resume_arguments,
)
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture
from astrowoof_natal_authoring import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
)
from astrowoof_natal_authoring.closure import (
    SpendController,
    load_json,
    save_state,
    validate_workspace_snapshot,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.reconciliation import reconcile_provider_cycle


def _ready(_action, _context):
    return {
        "outcome": "ready",
        "reason_code": None,
        "prepared_create_sha256": "a" * 64,
        "transport_context": {},
    }


def _dispatch_and_reconcile(root: Path):
    run_dir, inspection, request, documents, grant = authority_inputs(root)
    commit_external_authority_v2_dispatch_intent(
        run_dir,
        request=request,
        inspection=inspection,
        grant=grant,
        authorization_documents=documents,
    )
    creates: list[str] = []
    dispatch = dispatch_external_authority_v2_intent(
        run_dir,
        request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"],
        prepare=_ready,
        create=lambda prepared: {
            "kind": "response",
            "id": f"resp_{request['ordered_action_ids'][len(creates)]}",
            "created": creates.append(request["ordered_action_ids"][len(creates)]),
        },
    )
    # The extra scripted key is ignored by the production identity boundary.
    self_ids = request["ordered_action_ids"]
    self_provider = {
        action_id: f"resp_{action_id}" for action_id in self_ids
    }
    cycle = reconcile_provider_cycle(
        run_dir,
        observed_at="2099-01-01T00:00:00Z",
        retrieve=lambda provider_id, _timeout: {
            "id": provider_id,
            "status": "completed",
            "usage": {
                "input_tokens": 20,
                "output_tokens": 5,
                "total_tokens": 25,
            },
            "output": [],
        },
    )
    if set(self_provider.values()) != set(
        item["provider_operation_id"] for item in cycle["provider_operations"]
    ):
        raise AssertionError("scripted reconciliation provider inventory drifted")
    return run_dir, request, grant, creates, dispatch, cycle


def _report_all(run_dir: Path) -> dict:
    state = load_json(run_dir / "run.json")
    controller = SpendController(
        state=state,
        run_json=run_dir / "run.json",
        state_lock=__import__("threading").Lock(),
        consumer_id="provider-free-retirement-test",
    )
    for action in state["spend_ledger"]["actions"]:
        controller.local.active_action = action["action_id"]
        controller.settle_active({
            "usage": {
                "input_tokens": 20,
                "output_tokens": 5,
                "total_tokens": 25,
            },
            "estimated_cost": {"estimated_amount": "0.000012"},
        })
    controller.local.active_action = None
    return state


def _prepare_successor(run_dir: Path):
    state = load_json(run_dir / "run.json")
    predecessor = state["spend_ledger"]["actions"][0]
    successor = copy.deepcopy(predecessor)
    successor["action_id"] = f"paid_{'f' * 24}"
    successor["state"] = "PREPARED"
    successor["binding"]["prepared_state_revision"] = state["state_revision"]
    successor["binding"]["stage"] = "polish"
    successor["binding"]["route"] = "polish:attempt-002"
    successor["binding"]["request_sha256"] = "f" * 64
    for key in (
        "authorization", "consumption", "provider", "provider_reconciliation",
        "reported", "ambiguity", "integrity_review",
    ):
        successor.pop(key, None)
    state["spend_ledger"]["actions"].append(successor)
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    save_state(run_dir / "run.json", state)
    inspection = inspect_temporal_lifecycle(
        run_dir,
        native_exclusive_access="declared",
        observed_at="2099-01-01T00:00:01Z",
    )
    request = build_external_authority_request_v2(inspection)
    inventory = {
        item["action_id"]: item
        for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": successor["action_id"],
        "binding": copy.deepcopy(inventory[successor["action_id"]]["binding"]),
        "authorization_reference": "api-auth:successor",
    }]
    grant = build_external_authority_grant_v2(
        request,
        inspection,
        documents,
        api_decision_id="api-decision-successor",
        issuer="astrowoof-api",
        issued_at="2099-01-01T00:00:02Z",
    )
    return successor["action_id"], inspection, request, documents, grant


class ExternalAuthorityV2IntentRetirementSlice5(unittest.TestCase):
    def test_real_reconciliation_reporting_checkpoint_retires_and_replays(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant, creates, dispatch, cycle = (
                _dispatch_and_reconcile(Path(temporary))
            )
            self.assertEqual("detached_provider_pending", dispatch["outcome"])
            self.assertEqual(request["ordered_action_ids"], creates)
            self.assertEqual(
                request["ordered_action_ids"], cycle["cycle"]["completed_action_ids"]
            )

            state = _report_all(run_dir)
            self.assertIn("external_authority_v2_dispatch_intent", state)
            save_state(
                run_dir / "run.json", state,
                retire_external_authority_v2=True,
            )
            persisted = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, persisted)
            self.assertNotIn("external_authority_v2_dispatch_intent", persisted)
            history = persisted["external_authority_v2_dispatch_history"]
            retired = [
                item for item in history
                if item.get("outcome") == "provider_completed"
            ]
            self.assertEqual(1, len(retired))
            serialized_retirement = json.dumps(retired[0], sort_keys=True)
            for protected in (
                "prompt", "response_text", "subject_params", "api_key",
                "authorization: bearer",
            ):
                self.assertNotIn(protected, serialized_retirement.lower())
            self.assertEqual(
                request["ordered_action_ids"], retired[0]["ordered_action_ids"]
            )
            self.assertEqual(
                request["ordered_action_ids"],
                [item["action_id"] for item in retired[0]["terminal_action_records"]],
            )

            replay = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                prepare=lambda *_args: self.fail("replay prepared provider work"),
                create=lambda _action: self.fail("replay created provider work"),
            )
            self.assertEqual("exact_replay", replay["outcome"])
            self.assertEqual("replayed", replay["grant_invocation_disposition"])
            self.assertEqual(
                "provider_identity_durable", replay["provider_io_disposition"]
            )
            self.assertEqual(request["ordered_action_ids"], creates)

            successor_id, inspection, successor_request, documents, successor_grant = (
                _prepare_successor(run_dir)
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=successor_request,
                inspection=inspection,
                grant=successor_grant,
                authorization_documents=documents,
            )
            successor_creates: list[str] = []
            successor_result = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=successor_request[
                    "external_authority_request_sha256"
                ],
                grant_sha256=successor_grant["grant_sha256"],
                prepare=_ready,
                create=lambda _prepared: (
                    successor_creates.append(successor_id)
                    or {"kind": "response", "id": f"resp_{successor_id}"}
                ),
            )
            self.assertEqual(
                "detached_provider_pending", successor_result["outcome"]
            )
            self.assertEqual([successor_id], successor_creates)
            restored = load_json(run_dir / "run.json")
            self.assertEqual(
                successor_request["external_authority_request_sha256"],
                restored["external_authority_v2_dispatch_intent"]["request_sha256"],
            )

    def test_partial_terminal_inventory_keeps_live_intent(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, _grant, creates, _dispatch, _cycle = (
                _dispatch_and_reconcile(Path(temporary))
            )
            state = load_json(run_dir / "run.json")
            controller = SpendController(
                state=state,
                run_json=run_dir / "run.json",
                state_lock=__import__("threading").Lock(),
                consumer_id="provider-free-retirement-test",
            )
            controller.local.active_action = request["ordered_action_ids"][0]
            controller.settle_active({
                "usage": {"input_tokens": 1, "output_tokens": 1},
                "estimated_cost": {"estimated_amount": "0.000001"},
            })
            save_state(
                run_dir / "run.json", state,
                retire_external_authority_v2=True,
            )
            persisted = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, persisted)
            self.assertIn("external_authority_v2_dispatch_intent", persisted)
            self.assertFalse(any(
                item.get("outcome") == "provider_completed"
                for item in persisted.get("external_authority_v2_dispatch_history", [])
            ))
            self.assertEqual(request["ordered_action_ids"], creates)

    def test_terminal_identity_conflict_refuses_without_retirement(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _request, _grant, creates, _dispatch, _cycle = (
                _dispatch_and_reconcile(Path(temporary))
            )
            state = _report_all(run_dir)
            action_id = state["spend_ledger"]["actions"][0]["action_id"]
            response_path = (
                run_dir / "lifecycle" / "provider-reconciliation"
                / f"{action_id}.response.json"
            )
            response = load_json(response_path)
            response["id"] = "resp_conflicting_identity"
            from astrowoof_natal_authoring.closure import write_json_atomic
            write_json_atomic(response_path, response)
            write_workspace_snapshot(run_dir)
            before = (run_dir / "run.json").read_bytes()
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                save_state(
                    run_dir / "run.json", state,
                    retire_external_authority_v2=True,
                )
            self.assertEqual("native_evidence_invalid", caught.exception.reason_code)
            self.assertEqual(before, (run_dir / "run.json").read_bytes())
            self.assertIn(
                "external_authority_v2_dispatch_intent",
                load_json(run_dir / "run.json"),
            )
            self.assertEqual(2, len(creates))

    def test_retirement_checkpoint_interruption_classification(self):
        class Injected(RuntimeError):
            pass

        for point, valid_snapshot, live_intent in (
            ("before_retirement_state_persistence", True, True),
            ("after_retirement_state_before_snapshot", False, False),
            ("after_retirement_snapshot_publication", True, False),
        ):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temporary:
                run_dir, _request, _grant, _creates, _dispatch, _cycle = (
                    _dispatch_and_reconcile(Path(temporary))
                )
                state = _report_all(run_dir)
                # Establish a complete pre-retirement checkpoint for the
                # before-persistence comparison.
                write_workspace_snapshot(run_dir)

                def fail(actual):
                    if actual == point:
                        raise Injected(point)

                with self.assertRaisesRegex(Injected, point):
                    save_state(
                        run_dir / "run.json", state,
                        retire_external_authority_v2=True,
                        _failure_injector=fail,
                    )
                persisted = load_json(run_dir / "run.json")
                self.assertEqual(
                    live_intent,
                    "external_authority_v2_dispatch_intent" in persisted,
                )
                if valid_snapshot:
                    validate_workspace_snapshot(run_dir, persisted)
                else:
                    with self.assertRaises(ValueError):
                        validate_workspace_snapshot(run_dir, persisted)


class ExternalAuthorityV2RealAdoptionRetirementSlice5(SemanticClosureFixture):
    def test_real_creative_retry_adoption_reports_and_retires_at_checkpoint(self):
        from astrowoof_natal_authoring import closure

        with tempfile.TemporaryDirectory() as temporary:
            run_dir, pass_id, action_id, _successor = (
                moxie_fixture.MoxieTerminalReviewInventorySlice3Tests._workspace(
                self, Path(temporary)
                )
            )
            state_path = run_dir / "run.json"
            state = load_json(state_path)
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == action_id
            )
            request_sha = "1" * 64
            grant_sha = "2" * 64
            authorization = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": copy.deepcopy(action["binding"]),
                "authorization_reference": "api-auth:real-adoption",
            }
            auth_digest = hashlib.sha256(json.dumps(
                authorization, ensure_ascii=False, sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
            action["authorization"] = authorization
            action["consumption"] = {
                "consumer_id": "external-grant-v2:real-adoption-decision",
                "state_revision": state["state_revision"],
            }
            response_id = action["provider"]["id"]
            state["external_authority_v2_dispatch_intent"] = {
                "schema_version": "astrowoof.external_authority_dispatch_intent.v2",
                "request_schema_version": "astrowoof.external_authority_request.v2",
                "request_sha256": request_sha,
                "checkpoint_basis_sha256": "3" * 64,
                "grant_schema_version": "astrowoof.external_authority_grant.v2",
                "grant_sha256": grant_sha,
                "api_decision_id": "real-adoption-decision",
                "ordering_semantics": "lexical_action_id_ascending",
                "ordered_action_ids": [action_id],
                "ordered_authorization_document_sha256s": [auth_digest],
                "state": "PROVIDER_PENDING",
                "next_action_index": 1,
                "provider_bound_action_ids": [action_id],
                "provider_operation_ids": [response_id],
                "prepared_create_records": [{
                    "action_id": action_id,
                    "prepared_create_sha256": "4" * 64,
                }],
                "active_action_id": None,
                "active_create_state": None,
                "provider_io_performed": True,
            }
            save_state(state_path, state)
            moxie_fixture.MoxieTerminalReviewInventorySlice3Tests._write_completed_response(
                self, run_dir, pass_id, action_id, response_id,
            )

            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ), patch.object(
                closure, "finalize_subjects", return_value=None,
            ), patch.object(
                sys, "argv", _resume_arguments(run_dir),
            ), patch.dict(
                os.environ, {"OPENAI_API_KEY": "retirement-no-network"},
            ), patch("sys.stdout", __import__("io").StringIO()):
                try:
                    closure.main()
                except SystemExit as exc:
                    # The retained Moxie-shaped fixture may independently seal
                    # its local-work progress contradiction. Retirement must
                    # already be durable before that later decision.
                    self.assertEqual(2, exc.code)

            persisted = load_json(state_path)
            validate_workspace_snapshot(run_dir, persisted)
            completed = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == action_id
            )
            self.assertEqual("REPORTED", completed["state"])
            self.assertNotIn("external_authority_v2_dispatch_intent", persisted)
            retired = [
                item for item in persisted["external_authority_v2_dispatch_history"]
                if item.get("outcome") == "provider_completed"
            ]
            self.assertEqual(1, len(retired))
            self.assertEqual(request_sha, retired[0]["request_sha256"])
            self.assertEqual([response_id], retired[0]["provider_operation_ids"])


if __name__ == "__main__":
    unittest.main()
