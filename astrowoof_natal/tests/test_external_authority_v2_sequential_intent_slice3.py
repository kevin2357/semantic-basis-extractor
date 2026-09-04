from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_external_authority_v2_contract import authority_inputs
from astrowoof_natal_authoring import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
)
from astrowoof_natal_authoring.closure import (
    load_json,
    persist_state,
    validate_workspace_snapshot,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.cli import external_authority_v2 as cli


def _authorization_inputs(inspection, request, *, decision: str):
    inventory = {
        item["action_id"]: item
        for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [
        {
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": action_id,
            "binding": copy.deepcopy(inventory[action_id]["binding"]),
            "authorization_reference": f"api-auth:{decision}:{index}",
        }
        for index, action_id in enumerate(request["ordered_action_ids"], 1)
    ]
    grant = build_external_authority_grant_v2(
        request,
        inspection,
        documents,
        api_decision_id=decision,
        issuer="astrowoof-api",
        issued_at="2026-08-31T12:00:01Z",
    )
    return documents, grant


def _make_prior_actions_terminal_and_prepare_successor(run_dir: Path) -> str:
    """Model the already-durable facts found in Delerium generation 11.

    The first action set has complete provider/report evidence, but its live
    singleton intent remains.  A later ordinary action is independently
    prepared and otherwise eligible for a fresh v2 authority decision.
    """
    state = load_json(run_dir / "run.json")
    prior = state["spend_ledger"]["actions"]
    intent = state["external_authority_v2_dispatch_intent"]
    # The direct provider-free dispatch helper intentionally skips prepared
    # payload materialization. Model the already-durable prepared records that
    # production v2 dispatch checkpoints before response creation.
    intent["prepared_create_records"] = [
        {
            "action_id": action_id,
            "prepared_create_sha256": f"{index:064x}",
        }
        for index, action_id in enumerate(intent["ordered_action_ids"], 1)
    ]
    reconciliation_dir = run_dir / "lifecycle" / "provider-reconciliation"
    reconciliation_dir.mkdir(parents=True, exist_ok=True)
    for action in prior:
        action["state"] = "REPORTED"
        action["reported"] = {
            "usage": {"input_tokens": 10, "output_tokens": 4},
            "estimated_micro_usd": 12,
            "cost_disposition": "provider_usage_reported",
        }
        action["provider_reconciliation"]["last_outcome"] = "completed"
        action["provider_reconciliation"]["resume_not_before"] = None
        provider_id = action["provider"]["id"]
        (reconciliation_dir / f"{action['action_id']}.response.json").write_text(
            json.dumps({"id": provider_id, "status": "completed"}),
            encoding="utf-8",
        )

    successor = copy.deepcopy(prior[0])
    successor_id = f"paid_{'f' * 24}"
    successor["action_id"] = successor_id
    successor["state"] = "PREPARED"
    successor["binding"]["prepared_state_revision"] = state["state_revision"] + 1
    successor["binding"]["stage"] = "polish"
    successor["binding"]["route"] = "polish:attempt-002"
    successor["binding"]["request_sha256"] = "f" * 64
    for field in (
        "provider",
        "provider_reconciliation",
        "authorization",
        "consumption",
        "reported",
        "ambiguity",
        "integrity_review",
    ):
        successor.pop(field, None)
    prior.append(successor)
    state["state_revision"] += 1
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    persist_state(run_dir / "run.json", state)
    write_workspace_snapshot(run_dir)
    return successor_id


class ExternalAuthorityV2SequentialIntentSlice3(unittest.TestCase):
    def test_cli_does_not_misclassify_live_intent_action_state_mismatch(self):
        """A live submitting intent is not the completed-intent refusal case."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, inspection, request, documents, grant = authority_inputs(root)
            commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=request,
                inspection=inspection,
                grant=grant,
                authorization_documents=documents,
            )
            inputs = root / "public-inputs"
            inputs.mkdir()
            paths = {}
            for name, value in (
                ("inspection", inspection), ("request", request), ("grant", grant),
            ):
                paths[name] = inputs / f"{name}.json"
                paths[name].write_text(json.dumps(value), encoding="utf-8")
            authorization = inputs / "authorization.json"
            authorization.write_text(json.dumps(documents[0]), encoding="utf-8")
            output = inputs / "result.json"
            argv = [
                "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]), "--grant", str(paths["grant"]),
                "--provider", "openai", "--api-key-env", "SBE_QA_KEY",
                "--authorization", str(authorization), "--output", str(output),
                "--log-level", "CRITICAL",
            ]
            with patch.dict(os.environ, {"SBE_QA_KEY": "provider-free"}), patch.object(
                cli, "commit_external_authority_v2_dispatch_intent",
                side_effect=ExternalAuthorityV2ExecutionError(
                    "action_state_or_custody_mismatch",
                    "action is not providerless PREPARED work",
                ),
            ), patch.object(
                cli, "resolve_external_authority_v2_request_payload",
                side_effect=AssertionError("non-retirement mismatch reached payload"),
            ):
                with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                    cli.main(argv)
            self.assertEqual("action_state_or_custody_mismatch", caught.exception.reason_code)
            self.assertFalse(output.exists())

    def test_public_cli_refuses_unretired_completed_intent_without_dispatch(self):
        """Hound's stale-intent boundary remains provider-free and typed.

        The successor grant is independently valid.  The first refusal comes
        from the still-live predecessor intent. The CLI must return the
        explicit unresolved-retirement result rather than attempting dispatch
        with fresh successor identities.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, inspection, request, documents, grant = authority_inputs(root)
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
                create=lambda action: {
                    "kind": "response", "id": f"resp_{action['action_id']}",
                },
            )
            successor_id = _make_prior_actions_terminal_and_prepare_successor(run_dir)
            successor_inspection = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-31T12:00:00Z",
            )
            successor_request = build_external_authority_request_v2(
                successor_inspection
            )
            self.assertEqual([successor_id], successor_request["ordered_action_ids"])
            successor_documents, successor_grant = _authorization_inputs(
                successor_inspection, successor_request,
                decision="api-decision-successor",
            )

            inputs = root / "public-inputs"
            inputs.mkdir()
            paths = {}
            for name, value in (
                ("inspection", successor_inspection),
                ("request", successor_request),
                ("grant", successor_grant),
            ):
                paths[name] = inputs / f"{name}.json"
                paths[name].write_text(json.dumps(value), encoding="utf-8")
            authorization_paths = []
            for index, document in enumerate(successor_documents):
                path = inputs / f"authorization-{index}.json"
                path.write_text(json.dumps(document), encoding="utf-8")
                authorization_paths.append(path)
            argv = [
                "--run-dir", str(run_dir),
                "--inspection", str(paths["inspection"]),
                "--request", str(paths["request"]),
                "--grant", str(paths["grant"]),
                "--provider", "openai", "--api-key-env", "SBE_QA_KEY",
                "--output", str(inputs / "result.json"),
                "--log-level", "CRITICAL",
            ]
            for path in authorization_paths:
                argv.extend(("--authorization", str(path)))

            with patch.dict(os.environ, {"SBE_QA_KEY": "provider-free"}), patch.object(
                cli, "dispatch_external_authority_v2_intent",
                wraps=dispatch_external_authority_v2_intent,
            ) as dispatch, patch.object(
                cli, "resolve_external_authority_v2_request_payload",
                side_effect=AssertionError("stale intent reached payload resolution"),
            ), patch.object(
                cli.OpenAIResponsesProvider,
                "create_response_only",
                side_effect=AssertionError("stale intent reached provider create"),
            ):
                self.assertEqual(3, cli.main(argv))
            self.assertEqual(0, dispatch.call_count)
            from astrowoof_natal_authoring import (
                validate_external_authority_v2_command_result_v4,
            )
            result = validate_external_authority_v2_command_result_v4(
                json.loads((inputs / "result.json").read_text(encoding="utf-8"))
            )
            self.assertEqual("pre_provider_refusal", result["outcome"])
            self.assertEqual(
                "completed_intent_retirement_required",
                result["dispatch_result"]["reason_code"],
            )
            self.assertEqual(
                "not_attempted",
                result["dispatch_result"]["provider_io_disposition"],
            )
            persisted = load_json(run_dir / "run.json")
            self.assertEqual(
                request["external_authority_request_sha256"],
                persisted["external_authority_v2_dispatch_intent"]["request_sha256"],
            )

    def test_terminal_predecessor_intent_blocks_fresh_successor_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(
                Path(temporary)
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir,
                request=request,
                inspection=inspection,
                grant=grant,
                authorization_documents=documents,
            )
            creates: list[str] = []
            dispatched = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: (
                    creates.append(action["action_id"])
                    or {
                        "kind": "response",
                        "id": f"resp_{action['action_id']}",
                    }
                ),
            )
            self.assertEqual("detached_provider_pending", dispatched["outcome"])
            self.assertEqual(request["ordered_action_ids"], creates)

            successor_id = _make_prior_actions_terminal_and_prepare_successor(run_dir)
            validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))
            successor_inspection = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-31T12:00:00Z",
            )
            successor_request = build_external_authority_request_v2(
                successor_inspection
            )
            self.assertEqual([successor_id], successor_request["ordered_action_ids"])
            successor_documents, successor_grant = _authorization_inputs(
                successor_inspection,
                successor_request,
                decision="api-decision-successor",
            )

            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                commit_external_authority_v2_dispatch_intent(
                    run_dir,
                    request=successor_request,
                    inspection=successor_inspection,
                    grant=successor_grant,
                    authorization_documents=successor_documents,
                )
            self.assertEqual(
                "action_state_or_custody_mismatch", caught.exception.reason_code
            )
            self.assertEqual(request["external_authority_request_sha256"], (
                load_json(run_dir / "run.json")
                ["external_authority_v2_dispatch_intent"]
                ["request_sha256"]
            ))
            self.assertEqual(request["ordered_action_ids"], creates)

            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                dispatch_external_authority_v2_intent(
                    run_dir,
                    request_sha256=successor_request[
                        "external_authority_request_sha256"
                    ],
                    grant_sha256=successor_grant["grant_sha256"],
                    create=lambda action: self.fail(
                        "stale predecessor intent permitted a successor create"
                    ),
                )
            self.assertEqual("authorization_mismatch", caught.exception.reason_code)
            self.assertEqual(request["ordered_action_ids"], creates)

if __name__ == "__main__":
    unittest.main()
