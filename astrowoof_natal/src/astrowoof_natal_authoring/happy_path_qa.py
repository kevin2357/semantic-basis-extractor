"""Provider-free public witnesses for representative ordinary-v2 happy paths."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
import threading
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from .closure import (
    AwaitingSpendAuthorization,
    SpendController,
    persist_provider_request_payload,
    save_state,
    write_workspace_snapshot,
)
from .external_authority_v2 import build_external_authority_grant_v2
from .external_authority_v2_execution import (
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
)
from .lifecycle import inspect_lifecycle
from .post_fan_in_contracts import (
    commit_local_work_progress,
    inspect_post_fan_in_lifecycle,
)
from .post_fan_in_retry_qa import _binding, _digest, _materialize, _phase_projection
from .reconciliation import reconcile_provider_cycle
from .temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
)


CONTRACT = "astrowoof.ordinary_v2_happy_path_qualification.v1"
BUNDLE_CONTRACT = "astrowoof.ordinary_v2_happy_path_bundle.v1"
FIXTURE_CONTRACT = "astrowoof.ordinary_v2_happy_path_fixture.v1"
SCHEMA_RESOURCE = "ordinary-v2-happy-path-qualification.v1.schema.json"
BUNDLE_SCHEMA_RESOURCE = "ordinary-v2-happy-path-bundle.v1.schema.json"
FIXTURE_RESOURCE = "ordinary-v2-happy-paths.v1.json"


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def read_ordinary_v2_happy_path_fixture() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(FIXTURE_RESOURCE)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "witnesses", "privacy", "authority_rule",
    }:
        raise ValueError("Happy-path fixture fields are not exact")
    if value.get("schema_version") != FIXTURE_CONTRACT:
        raise ValueError("Unsupported happy-path fixture")
    if value.get("witnesses") != [
        "two_retries_out_of_order", "retry_then_qualitative_critic",
    ]:
        raise ValueError("Happy-path fixture witness inventory differs")
    if value.get("authority_rule") != "one_ordinary_action_set_for_co_ready_actions":
        raise ValueError("Happy-path fixture authority rule differs")
    if value.get("privacy") != "public_projection_only":
        raise ValueError("Happy-path fixture privacy rule differs")
    return value


def read_ordinary_v2_happy_path_qualification_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources.contracts").joinpath(
        SCHEMA_RESOURCE,
    ).read_text(encoding="utf-8"))


def read_ordinary_v2_happy_path_bundle_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources.contracts").joinpath(
        BUNDLE_SCHEMA_RESOURCE,
    ).read_text(encoding="utf-8"))


def _load_state(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "run.json").read_text(encoding="utf-8"))


def _action(state: Mapping[str, Any], action_id: str) -> dict[str, Any]:
    return next(
        item for item in state["spend_ledger"]["actions"]
        if item["action_id"] == action_id
    )


def _set_due(action: dict[str, Any], at: str) -> None:
    action["provider_reconciliation"] = {
        "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
        "provider_retrieval_attempt_count": 1,
        "last_attempt_at": "2026-08-27T11:59:00Z",
        "last_outcome": "pending",
        "resume_not_before": at,
    }


def _mark_reported_and_prepare_successor(
    run_dir: Path, *, completed_id: str, successor_id: str, route: str,
) -> None:
    state = _load_state(run_dir)
    completed = _action(state, completed_id)
    completed["state"] = "REPORTED"
    completed["reported"] = {"estimated_micro_usd": 0}
    binding = _binding(state["run_id"], route, int(state["state_revision"]) + 1)
    payload = {"model": "scripted-provider", "input": f"sanitized {route}"}
    artifact = persist_provider_request_payload(
        run_dir / f"{successor_id}.private.json", payload,
    )
    binding["request_sha256"] = artifact["canonical_request_sha256"]
    state["spend_ledger"]["actions"].append({
        "action_id": successor_id,
        "state": "PREPARED",
        "binding": binding,
        "authorization": None,
        "provider": None,
        "reported": None,
        "reconciliation_reference_ids": [],
        "request_payload_artifact": artifact,
    })
    state["status"] = "WAITING_FOR_RESPONSE"
    save_state(run_dir / "run.json", state)


def _authority_projection(
    request: Mapping[str, Any], grant: Mapping[str, Any],
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    members = []
    for action_id, document in zip(request["ordered_action_ids"], documents, strict=True):
        binding = document["binding"]
        members.append({
            "action_id": action_id,
            "stage": binding["stage"],
            "route": binding["route"],
            "binding_sha256": _digest(binding),
            "authorization_document_sha256": _digest(document),
        })
    request_semantics = {
        "request_kind": request["request_kind"],
        "ordered_action_ids": list(request["ordered_action_ids"]),
    }
    grant_semantics = {
        "request_semantic_sha256": _digest(request_semantics),
        "api_decision_id": grant["api_decision_id"],
        "ordered_authorization_document_sha256s": [
            _digest(document) for document in documents
        ],
    }
    body = {
        **request_semantics,
        "request_semantic_sha256": _digest(request_semantics),
        "grant_semantic_sha256": _digest(grant_semantics),
        "aggregate_action_count": len(request["ordered_action_ids"]),
        "members": members,
    }
    return {**body, "authority_sha256": _digest(body)}


def _authorize_and_dispatch(
    run_dir: Path, *, observed_at: str, provider_prefix: str,
) -> tuple[dict[str, Any], list[str], str]:
    inspection = inspect_temporal_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at,
    )
    request = build_external_authority_request_v2(inspection)
    state = _load_state(run_dir)
    documents = []
    for action_id in request["ordered_action_ids"]:
        item = _action(state, action_id)
        documents.append({
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": action_id,
            "binding": copy.deepcopy(item["binding"]),
            "authorization_reference": f"fixture:{action_id}",
        })
    grant = build_external_authority_grant_v2(
        request, inspection, documents,
        api_decision_id=f"fixture:{provider_prefix}",
        issuer="astrowoof-api-provider-free",
        issued_at=observed_at,
    )
    commit_external_authority_v2_dispatch_intent(
        run_dir, request=request, inspection=inspection, grant=grant,
        authorization_documents=documents,
    )
    creates: list[str] = []
    dispatched = dispatch_external_authority_v2_intent(
        run_dir,
        request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"],
        create=lambda selected: (
            creates.append(selected["action_id"])
            or {"id": f"{provider_prefix}_{len(creates)}", "kind": "response"}
        ),
    )
    if dispatched["outcome"] != "detached_provider_pending":
        raise ValueError("Happy-path dispatch did not detach provider pending")
    replay = dispatch_external_authority_v2_intent(
        run_dir,
        request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"],
        create=lambda selected: creates.append(selected["action_id"]) or {},
    )
    if replay["outcome"] != "exact_replay":
        raise ValueError("Happy-path dispatch replay was not exact")
    return _authority_projection(request, grant, documents), creates, replay["outcome"]


def _two_retries(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True)
    run_dir, first, prepared = _materialize(root)
    state = _load_state(run_dir)
    second = prepared
    second_action = _action(state, second)
    second_action["state"] = "WAITING"
    second_action["provider"] = {"id": "resp_fixture_retry_2", "kind": "response"}
    second_action.pop("request_payload_artifact", None)
    _set_due(_action(state, first), "2026-08-27T12:01:00Z")
    _set_due(second_action, "2026-08-27T12:01:00Z")
    state["passes"]["pass-1"]["attempts"][2]["state"] = "WAITING_FOR_RESPONSE"
    save_state(run_dir / "run.json", state)

    phases: list[dict[str, Any]] = []
    retrieves: list[str] = []
    first_cycle = reconcile_provider_cycle(
        run_dir, observed_at="2026-08-27T12:01:00Z",
        retrieve=lambda provider_id, _timeout: (
            retrieves.append(provider_id)
            or ({"id": provider_id, "status": "completed", "output": []}
                if provider_id == "resp_fixture_retry_2"
                else {"id": provider_id, "status": "in_progress"})
        ),
    )
    if first_cycle["outcome"] != "progressed_local":
        raise ValueError("Out-of-order witness did not expose later completion")
    local_two = inspect_post_fan_in_lifecycle(
        run_dir, observed_at="2026-08-27T12:01:01Z",
        native_exclusive_access="declared",
    )
    if local_two["temporal_decision"]["selected_command"] != "ordinary_resume":
        raise ValueError("Out-of-order witness did not select completed local work")
    phases.append(_phase_projection("later_retry_local", local_two))
    successor_two = "paid_000000000000000000000104"
    _mark_reported_and_prepare_successor(
        run_dir, completed_id=second, successor_id=successor_two,
        route="pass-2:attempt-003",
    )
    after_two = commit_local_work_progress(
        run_dir, prior=local_two, observed_at="2026-08-27T12:01:02Z",
    )
    if after_two["temporal_decision"]["selected_command"] != "provider_reconciliation_cycle":
        raise ValueError("Retained custody did not outrank successor authority")
    phases.append(_phase_projection("retained_custody", after_two))

    second_cycle = reconcile_provider_cycle(
        run_dir, observed_at="2026-08-27T12:02:00Z",
        retrieve=lambda provider_id, _timeout: (
            retrieves.append(provider_id)
            or {"id": provider_id, "status": "completed", "output": []}
        ),
    )
    if second_cycle["outcome"] != "progressed_local":
        raise ValueError("Out-of-order witness did not complete earlier retry")
    local_one = inspect_post_fan_in_lifecycle(
        run_dir, observed_at="2026-08-27T12:02:01Z",
        native_exclusive_access="declared",
    )
    phases.append(_phase_projection("earlier_retry_local", local_one))
    successor_one = "paid_000000000000000000000103"
    _mark_reported_and_prepare_successor(
        run_dir, completed_id=first, successor_id=successor_one,
        route="pass-1:attempt-003",
    )
    authority_ready = commit_local_work_progress(
        run_dir, prior=local_one, observed_at="2026-08-27T12:02:02Z",
    )
    if authority_ready["temporal_decision"]["selected_command"] != "await_external_authority":
        raise ValueError("Co-ready successors did not expose external authority")
    phases.append(_phase_projection("aggregate_authority_ready", authority_ready))
    authority, creates, replay = _authorize_and_dispatch(
        run_dir, observed_at="2026-08-27T12:02:02Z",
        provider_prefix="resp_fixture_successor",
    )
    if creates != sorted([successor_one, successor_two]):
        raise ValueError("Aggregate successor dispatch order differs")
    return {
        "witness_id": "two_retries_out_of_order",
        "phases": phases,
        "retrieval_order": ["later_submission_completed_first", "earlier_submission_completed_second"],
        "authority": authority,
        "scripted_retrieval_count": len(retrieves),
        "scripted_create_count": len(creates),
        "duplicate_create_count": 0,
        "duplicate_local_consumption_count": 0,
        "replay_outcome": replay,
        "endpoint": "detached_provider_pending",
    }


def _prepare_critic_via_spend_controller(run_dir: Path) -> str:
    state = _load_state(run_dir)
    payload = {"model": "gpt-5.6-luna", "input": "sanitized critic qualification"}
    artifact = persist_provider_request_payload(run_dir / "critic.private.json", payload)
    controller = SpendController(
        state=state, run_json=run_dir / "run.json", state_lock=threading.Lock(),
        consumer_id="provider-free-qualification",
    )
    before_submit, _provider_created = controller.callbacks(
        stage="qualitative_critic", route="qualitative_critic",
        model="gpt-5.6-luna", service_level="interactive",
        maximum_output_tokens=1000,
    )
    try:
        before_submit(payload, request_payload_artifact=artifact)
    except AwaitingSpendAuthorization as exc:
        write_workspace_snapshot(run_dir)
        return exc.action["action_id"]
    raise ValueError("Production spend callback did not prepare critic authority")


def _retry_then_critic(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True)
    run_dir, first, unused = _materialize(root)
    state = _load_state(run_dir)
    state["spend_ledger"]["actions"] = [
        item for item in state["spend_ledger"]["actions"] if item["action_id"] != unused
    ]
    state["passes"]["pass-1"]["attempts"] = state["passes"]["pass-1"]["attempts"][:2]
    state["authoring_profile"] = {
        "qa": {
            "polish": False,
            "qualitative_critic": True,
            "qualitative_candidate": False,
        },
    }
    _set_due(_action(state, first), "2026-08-27T13:01:00Z")
    save_state(run_dir / "run.json", state)
    retrieves: list[str] = []
    result = reconcile_provider_cycle(
        run_dir, observed_at="2026-08-27T13:01:00Z",
        retrieve=lambda provider_id, _timeout: (
            retrieves.append(provider_id)
            or {"id": provider_id, "status": "completed", "output": []}
        ),
    )
    if result["outcome"] != "progressed_local":
        raise ValueError("Retry-to-critic witness did not retrieve retry")
    local = inspect_post_fan_in_lifecycle(
        run_dir, observed_at="2026-08-27T13:01:01Z",
        native_exclusive_access="declared",
    )
    state = _load_state(run_dir)
    completed = _action(state, first)
    completed["state"] = "REPORTED"
    completed["reported"] = {"estimated_micro_usd": 0}
    state["passes"]["pass-1"]["attempts"][1]["state"] = "PASS_QA_ACCEPTED"
    state["passes"]["pass-1"]["state"] = "ACCEPTED"
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    save_state(run_dir / "run.json", state)
    consumed = commit_local_work_progress(
        run_dir, prior=local, observed_at="2026-08-27T13:01:02Z",
    )
    critic_id = _prepare_critic_via_spend_controller(run_dir)
    ready = inspect_post_fan_in_lifecycle(
        run_dir, observed_at="2026-08-27T13:01:03Z",
        native_exclusive_access="declared",
    )
    if ready["temporal_decision"]["selected_command"] != "await_external_authority":
        critic_state = _action(_load_state(run_dir), critic_id)
        legacy = inspect_lifecycle(
            run_dir, native_exclusive_access="declared",
            observed_at="2026-08-27T13:01:03Z",
        )
        raise ValueError(
            "Production critic preparation did not expose authority: "
            f"{ready['temporal_decision']} / "
            f"{ready['checkpoint_basis']['external_authority_state']} / "
            f"{ready['checkpoint_basis']['provider_custody']} / {critic_state} / "
            f"{legacy['review_reasons']}"
        )
    authority, creates, replay = _authorize_and_dispatch(
        run_dir, observed_at="2026-08-27T13:01:03Z",
        provider_prefix="resp_fixture_critic",
    )
    if creates != [critic_id] or authority["members"][0]["stage"] != "qualitative_critic":
        raise ValueError("Retry-to-critic dispatch identity differs")
    return {
        "witness_id": "retry_then_qualitative_critic",
        "phases": [
            _phase_projection("retry_local", local),
            _phase_projection("retry_consumed", consumed),
            _phase_projection("critic_authority_ready", ready),
        ],
        "retrieval_order": ["retry_completed"],
        "authority": authority,
        "scripted_retrieval_count": len(retrieves),
        "scripted_create_count": len(creates),
        "duplicate_create_count": 0,
        "duplicate_local_consumption_count": 0,
        "replay_outcome": replay,
        "endpoint": "detached_provider_pending",
    }


def _build_artifacts() -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = read_ordinary_v2_happy_path_fixture()
    with tempfile.TemporaryDirectory(prefix="astrowoof-happy-path-") as temporary:
        root = Path(temporary)
        witnesses = [_two_retries(root / "a"), _retry_then_critic(root / "b")]
    witness_receipts = []
    witness_projections = []
    for witness in witnesses:
        projection = copy.deepcopy(witness)
        body = {"witness_id": witness["witness_id"], "evidence_sha256": _digest(projection)}
        witness_receipts.append({**body, "witness_receipt_sha256": _digest(body)})
        witness_projections.append(projection)
    receipt_body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "package": {"name": "astrowoof-natal-authoring", "version": _package_version()},
        "fixture_sha256": _digest(fixture),
        "witnesses": witness_receipts,
        "scripted_retrieval_count": sum(item["scripted_retrieval_count"] for item in witnesses),
        "scripted_create_count": sum(item["scripted_create_count"] for item in witnesses),
        "duplicate_create_count": 0,
        "duplicate_local_consumption_count": 0,
        "external_network_call_count": 0,
        "provider_spend_usd": 0,
        "privacy": "public_projection_only",
    }
    receipt = {**receipt_body, "receipt_sha256": _digest(receipt_body)}
    bundle_body = {
        "schema_version": BUNDLE_CONTRACT,
        "fixture_sha256": receipt["fixture_sha256"],
        "qualification_receipt_sha256": receipt["receipt_sha256"],
        "witnesses": witness_projections,
    }
    bundle = {**bundle_body, "bundle_sha256": _digest(bundle_body)}
    return validate_ordinary_v2_happy_path_qualification(receipt), _validate_bundle(bundle, receipt)


def validate_ordinary_v2_happy_path_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "fixture_sha256", "witnesses",
        "scripted_retrieval_count", "scripted_create_count",
        "duplicate_create_count", "duplicate_local_consumption_count",
        "external_network_call_count", "provider_spend_usd", "privacy",
    }
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ValueError("Happy-path qualification fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("schema_version") != CONTRACT or value.get("receipt_sha256") != _digest(body):
        raise ValueError("Happy-path qualification identity differs")
    if value.get("status") != "pass" or value.get("qualification_only") is not True or value.get("provider_free") is not True:
        raise ValueError("Happy-path qualification posture differs")
    if value.get("fixture_sha256") != _digest(read_ordinary_v2_happy_path_fixture()):
        raise ValueError("Happy-path fixture digest differs")
    if value.get("external_network_call_count") != 0 or value.get("provider_spend_usd") != 0:
        raise ValueError("Happy-path qualification was not provider free")
    if value.get("duplicate_create_count") != 0 or value.get("duplicate_local_consumption_count") != 0:
        raise ValueError("Happy-path qualification duplicated work")
    package = value.get("package")
    if not isinstance(package, Mapping) or set(package) != {"name", "version"} or package.get("name") != "astrowoof-natal-authoring" or not isinstance(package.get("version"), str):
        raise ValueError("Happy-path qualification package identity differs")
    if value.get("privacy") != "public_projection_only" or value.get("scripted_retrieval_count") != 4 or value.get("scripted_create_count") != 3:
        raise ValueError("Happy-path qualification bounded counts differ")
    witnesses = value.get("witnesses")
    if not isinstance(witnesses, list) or [item.get("witness_id") for item in witnesses] != read_ordinary_v2_happy_path_fixture()["witnesses"]:
        raise ValueError("Happy-path receipt witness inventory differs")
    for item in witnesses:
        if not isinstance(item, Mapping) or set(item) != {"witness_id", "evidence_sha256", "witness_receipt_sha256"}:
            raise ValueError("Happy-path witness receipt shape differs")
        witness_body = {key: member for key, member in item.items() if key != "witness_receipt_sha256"}
        if item["witness_receipt_sha256"] != _digest(witness_body):
            raise ValueError("Happy-path witness receipt digest differs")
    return copy.deepcopy(dict(value))


def _validate_bundle(value: Any, receipt: Mapping[str, Any]) -> dict[str, Any]:
    keys = {"schema_version", "bundle_sha256", "fixture_sha256", "qualification_receipt_sha256", "witnesses"}
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ValueError("Happy-path bundle fields are not exact")
    body = {key: item for key, item in value.items() if key != "bundle_sha256"}
    if value.get("schema_version") != BUNDLE_CONTRACT or value.get("bundle_sha256") != _digest(body):
        raise ValueError("Happy-path bundle identity differs")
    canonical_receipt = validate_ordinary_v2_happy_path_qualification(receipt)
    if value.get("qualification_receipt_sha256") != canonical_receipt["receipt_sha256"]:
        raise ValueError("Happy-path bundle receipt binding differs")
    if value.get("fixture_sha256") != canonical_receipt["fixture_sha256"]:
        raise ValueError("Happy-path bundle fixture binding differs")
    witnesses = value.get("witnesses")
    if not isinstance(witnesses, list) or [item.get("witness_id") for item in witnesses] != read_ordinary_v2_happy_path_fixture()["witnesses"]:
        raise ValueError("Happy-path bundle witness inventory differs")
    for projection, witness_receipt in zip(witnesses, canonical_receipt["witnesses"], strict=True):
        witness_keys = {
            "witness_id", "phases", "retrieval_order", "authority",
            "scripted_retrieval_count", "scripted_create_count",
            "duplicate_create_count", "duplicate_local_consumption_count",
            "replay_outcome", "endpoint",
        }
        if not isinstance(projection, Mapping) or set(projection) != witness_keys:
            raise ValueError("Happy-path witness projection fields are not exact")
        if _digest(projection) != witness_receipt["evidence_sha256"]:
            raise ValueError("Happy-path bundle witness evidence differs")
        if projection.get("endpoint") != "detached_provider_pending" or projection.get("replay_outcome") != "exact_replay":
            raise ValueError("Happy-path witness endpoint differs")
        if projection.get("duplicate_create_count") != 0 or projection.get("duplicate_local_consumption_count") != 0:
            raise ValueError("Happy-path witness duplicated work")
        authority = projection.get("authority")
        authority_keys = {
            "request_kind", "request_semantic_sha256", "grant_semantic_sha256",
            "ordered_action_ids", "aggregate_action_count", "members",
            "authority_sha256",
        }
        if not isinstance(authority, Mapping) or set(authority) != authority_keys or authority.get("request_kind") != "ordinary_action_set" or authority.get("aggregate_action_count") != len(authority.get("ordered_action_ids", [])):
            raise ValueError("Happy-path authority projection differs")
        if authority["ordered_action_ids"] != sorted(authority["ordered_action_ids"]):
            raise ValueError("Happy-path authority inventory is not lexical")
        members = authority.get("members")
        if not isinstance(members, list) or len(members) != authority["aggregate_action_count"]:
            raise ValueError("Happy-path authority member inventory differs")
        for action_id, member in zip(authority["ordered_action_ids"], members, strict=True):
            if not isinstance(member, Mapping) or set(member) != {
                "action_id", "stage", "route", "binding_sha256",
                "authorization_document_sha256",
            } or member.get("action_id") != action_id:
                raise ValueError("Happy-path authority member differs")
            for field in ("binding_sha256", "authorization_document_sha256"):
                digest_value = member.get(field)
                if not isinstance(digest_value, str) or len(digest_value) != 64:
                    raise ValueError("Happy-path authority member digest differs")
        authority_body = {key: item for key, item in authority.items() if key != "authority_sha256"}
        if authority.get("authority_sha256") != _digest(authority_body):
            raise ValueError("Happy-path authority digest differs")
        phases = projection.get("phases")
        if not isinstance(phases, list) or not phases:
            raise ValueError("Happy-path phase inventory differs")
        phase_keys = {
            "phase", "phase_sha256", "schema_version", "run_id",
            "route_family", "provider_mechanism", "selected_command",
            "capacity_disposition", "reason_code", "eligible_now",
            "due_action_ids", "not_before", "provider_custody",
            "local_operations", "consumed_operation_count",
            "external_authority_action_ids",
        }
        for phase in phases:
            if not isinstance(phase, Mapping) or set(phase) != phase_keys:
                raise ValueError("Happy-path phase fields are not exact")
            phase_body = {key: item for key, item in phase.items() if key != "phase_sha256"}
            if phase.get("phase_sha256") != _digest(phase_body):
                raise ValueError("Happy-path phase digest differs")
    return copy.deepcopy(dict(value))


def run_ordinary_v2_happy_path_qualification() -> dict[str, Any]:
    receipt, _bundle = _build_artifacts()
    return receipt


def run_ordinary_v2_happy_path_bundle() -> dict[str, Any]:
    _receipt, bundle = _build_artifacts()
    return bundle


def validate_ordinary_v2_happy_path_bundle(value: Any) -> dict[str, Any]:
    receipt, _bundle = _build_artifacts()
    return _validate_bundle(value, receipt)


def _inside_native_workspace(path: Path) -> bool:
    target = path.resolve()
    return any(
        (parent / "run.json").exists() or (parent / "workspace-snapshot.json").exists()
        for parent in (target.parent, *target.parents)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run provider-free ordinary-v2 happy-path witnesses.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--bundle-schema", action="store_true")
    args = parser.parse_args(argv)
    if sum(bool(item) for item in (args.schema, args.fixture, args.bundle, args.bundle_schema)) > 1:
        parser.error("public artifact selectors are mutually exclusive")
    if args.output and _inside_native_workspace(args.output):
        parser.error("--output must not be inside a native SBE workspace")
    value = (
        read_ordinary_v2_happy_path_qualification_schema() if args.schema
        else read_ordinary_v2_happy_path_bundle_schema() if args.bundle_schema
        else read_ordinary_v2_happy_path_fixture() if args.fixture
        else run_ordinary_v2_happy_path_bundle() if args.bundle
        else run_ordinary_v2_happy_path_qualification()
    )
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
