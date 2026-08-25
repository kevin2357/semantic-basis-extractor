from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
)
from astrowoof_natal_authoring.closure import (
    load_json, normalized_path, persist_state, public_run_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.deployed_qa import _wave
from astrowoof_natal_authoring.initial_wave import (
    ProviderCreateResult, build_wave_authorization, execute_initial_wave_creates,
)
from astrowoof_natal_authoring.reconciliation import reconcile_provider_cycle
from astrowoof_natal_authoring.spend import prepare_action


def _spend_policy():
    return {
        "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
        "run_ceiling_micro_usd": 100000000,
        "stage_ceilings_micro_usd": {
            "authoring_initial": 100000000, "creative_retry": 100000000,
            "polish": 100000000, "qualitative_critic": 100000000,
            "qualitative_candidate": 100000000,
        },
        "optional_stage_budget_behavior": {
            "polish": "skip", "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


def _six_member_pending_workspace(root: Path, route_family: str):
    wave, documents = _wave(route_family)
    authorization = build_wave_authorization(
        wave, documents, reservation_set_reference="qualification:no-reservation",
        issuer="sbe-source-qualification", authorized_at="1970-01-01T00:00:00Z",
    )
    creates = []
    outcomes = []

    def submit(member, _timeout):
        provider_id = f"resp_{route_family}_{member['pass_number']:02d}"
        creates.append(provider_id)
        return ProviderCreateResult(provider_id)

    result = execute_initial_wave_creates(
        wave, authorization=authorization, member_authorizations=documents,
        submit=submit,
        persist_member_outcome=lambda _member, outcome: outcomes.append(copy.deepcopy(outcome)),
    )
    by_action = {item["action_id"]: item for item in outcomes}
    actions = []
    passes = {}
    for number, original in enumerate(documents, 1):
        document = copy.deepcopy(original)
        if route_family == "bounded_natal":
            document["binding"]["route"] = f"bounded_natal.v2:qualification-pass-{number:02d}:attempt-001"
        action_id = document["action_id"]
        actions.append({
            "action_id": action_id, "state": "WAITING",
            "binding": copy.deepcopy(document["binding"]), "authorization": document,
            "consumption": {"consumer_id": "qualification", "state_revision": 1},
            "provider": {"id": by_action[action_id]["provider"]["id"], "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 0, "last_attempt_at": None,
                "last_outcome": "provider_identity_recorded",
                "resume_not_before": "1970-01-01T00:00:15Z",
            },
            "reported": None,
        })
        passes[f"pass-{number}"] = {
            "pass_id": f"pass-{number}", "state": "WAITING_FOR_RESPONSE",
            "attempts": [{"attempt": 1, "state": "WAITING_FOR_RESPONSE"}],
        }
    state = {
        "schema_version": (
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal"
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        "run_id": wave["run_id"], "state_revision": 1,
        "status": "WAITING_FOR_RESPONSE", "passes": passes, "subjects": {},
        "authoring_profile": {
            "qa": {"polish": True, "qualitative_critic": True, "qualitative_candidate": True},
            "optional_stages": {"polish": True, "qualitative_critic": True, "qualitative_candidate": True},
        },
        "workspace_contract": {
            "mode": "stable_logical_absolute_path", "logical_root": normalized_path(root),
        },
        "spend_ledger": {
            "schema_version": "astrowoof.provider_spend_ledger.v0.1",
            "policy": _spend_policy(), "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
    }
    if route_family == "bounded_natal":
        state.update({
            "route": "bounded_natal.v2",
            "route_contract": "astrowoof.bounded_natal.authoring_run.v2",
            "service_level": "interactive",
        })
    (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
    write_workspace_snapshot(root)
    return result, creates


def _complete_4_plus_2(root: Path):
    retrievals = []

    def retrieve(provider_id, _timeout):
        retrievals.append(provider_id)
        return {"id": provider_id, "status": "completed", "output": []}

    cycles = []
    for observed_at in ("1970-01-01T00:00:15Z", "1970-01-01T00:01:00Z"):
        cycle = reconcile_provider_cycle(root, observed_at=observed_at, retrieve=retrieve)
        cycles.append(cycle)
        state = load_json(root / "run.json")
        completed = set(cycle["cycle"]["completed_action_ids"])
        for action in state["spend_ledger"]["actions"]:
            if action["action_id"] in completed:
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
        persist_state(root / "run.json", state)
        write_workspace_snapshot(root)
    return cycles, retrievals


def _prepare_v2_ordinary(
    root: Path, route_family: str, *, service_level="interactive", stage="polish",
):
    state = load_json(root / "run.json")
    route = (
        f"bounded_natal.v2:{stage}:attempt-001"
        if route_family == "bounded_natal" else f"{stage}:attempt-001"
    )
    binding = {
        "run_id": state["run_id"], "profile_sha256": "a" * 64,
        "prepared_state_revision": state["state_revision"], "stage": stage,
        "route": route, "request_sha256": "f" * 64, "model": "scripted-provider",
        "service_level": service_level, "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }
    action = prepare_action(state["spend_ledger"], binding)
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    persist_state(root / "run.json", state)
    write_workspace_snapshot(root)
    inspection = inspect_temporal_lifecycle(
        root, native_exclusive_access="declared", observed_at="2026-08-24T12:00:00Z",
    )
    request = build_external_authority_request_v2(inspection)
    document = {
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action["action_id"], "binding": copy.deepcopy(binding),
        "authorization_reference": "qualification:v2",
    }
    grant = build_external_authority_grant_v2(
        request, inspection, [document], api_decision_id="qualification:v2",
        issuer="astrowoof-api-qualification", issued_at="2026-08-24T12:00:01Z",
    )
    return inspection, request, [document], grant


class ExternalAuthorityV2RouteQualificationSlice4(unittest.TestCase):
    def test_exact_and_bounded_interactive_holistic_4_plus_2_to_v2_dispatch(self):
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route_family=route_family), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                wave_result, initial_creates = _six_member_pending_workspace(root, route_family)
                cycles, retrievals = _complete_4_plus_2(root)
                self.assertEqual("detached_provider_pending", wave_result["outcome"])
                self.assertEqual([4, 2], [item["cycle"]["provider_retrieval_count"] for item in cycles])
                self.assertEqual(6, len(set(initial_creates)))
                self.assertEqual(6, len(set(retrievals)))

                inspection, request, documents, grant = _prepare_v2_ordinary(root, route_family)
                commit_external_authority_v2_dispatch_intent(
                    root, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents,
                )
                ordinary_creates = []
                result = dispatch_external_authority_v2_intent(
                    root, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"],
                    create=lambda action: (
                        ordinary_creates.append(action["action_id"])
                        or {"id": f"resp_v2_{route_family}", "kind": "response"}
                    ),
                )
                self.assertEqual("detached_provider_pending", result["outcome"])
                self.assertEqual(request["ordered_action_ids"], ordinary_creates)
                due = inspect_temporal_lifecycle(
                    root, native_exclusive_access="established",
                    observed_at="2099-01-01T00:00:00Z",
                )
                self.assertEqual("provider_reconciliation_cycle", due["temporal_decision"]["selected_command"])
                self.assertEqual(request["ordered_action_ids"], due["temporal_decision"]["due_action_ids"])

    def test_all_supported_response_stages_on_exact_and_bounded_routes(self):
        stages = ("creative_retry", "polish", "qualitative_critic", "qualitative_candidate")
        for route_family in ("exact_natal", "bounded_natal"):
            with tempfile.TemporaryDirectory() as temporary:
                outer = Path(temporary)
                base = outer / "base"
                base.mkdir()
                _six_member_pending_workspace(base, route_family)
                _complete_4_plus_2(base)
                for stage in stages:
                    with self.subTest(route_family=route_family, stage=stage):
                        case = outer / stage
                        shutil.copytree(base, case)
                        state = load_json(case / "run.json")
                        state["workspace_contract"]["logical_root"] = normalized_path(case)
                        (case / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                        write_workspace_snapshot(case)
                        inspection, request, documents, grant = _prepare_v2_ordinary(
                            case, route_family, stage=stage,
                        )
                        commit_external_authority_v2_dispatch_intent(
                            case, request=request, inspection=inspection, grant=grant,
                            authorization_documents=documents,
                        )
                        calls = []
                        result = dispatch_external_authority_v2_intent(
                            case,
                            request_sha256=request["external_authority_request_sha256"],
                            grant_sha256=grant["grant_sha256"],
                            create=lambda action: (
                                calls.append(action["action_id"])
                                or {"id": f"resp_{stage}", "kind": "response"}
                            ),
                        )
                        self.assertEqual("detached_provider_pending", result["outcome"])
                        self.assertEqual(request["ordered_action_ids"], calls)

    def test_optional_batch_refuses_before_intent_or_provider_work(self):
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route_family=route_family), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _six_member_pending_workspace(root, route_family)
                _complete_4_plus_2(root)
                inspection, request, documents, grant = _prepare_v2_ordinary(
                    root, route_family, service_level="batch",
                )
                before = (root / "run.json").read_bytes(), (root / "workspace-snapshot.json").read_bytes()
                with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                    commit_external_authority_v2_dispatch_intent(
                        root, request=request, inspection=inspection, grant=grant,
                        authorization_documents=documents,
                    )
                self.assertEqual("unsupported_contract", caught.exception.reason_code)
                self.assertEqual(before, ((root / "run.json").read_bytes(), (root / "workspace-snapshot.json").read_bytes()))


if __name__ == "__main__":
    unittest.main()
