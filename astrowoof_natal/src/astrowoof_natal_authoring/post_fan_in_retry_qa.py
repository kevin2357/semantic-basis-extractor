"""Provider-free installed qualification for post-fan-in retry routing."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from .closure import (
    normalized_path,
    persist_provider_request_payload,
    public_run_state,
    save_state,
    write_workspace_snapshot,
)
from .post_fan_in_contracts import (
    commit_local_work_progress,
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from .reconciliation import reconcile_provider_cycle
from .external_authority_v2 import build_external_authority_grant_v2
from .external_authority_v2_execution import (
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
)
from .temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
)


CONTRACT = "astrowoof.post_fan_in_retry_qualification.v1"
SCHEMA_RESOURCE = "post-fan-in-retry-qualification.v1.schema.json"
FIXTURE_RESOURCE = "post-fan-in-retry-routing.v1.json"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _lifecycle_projection(value: Mapping[str, Any]) -> dict[str, Any]:
    """Return stable public semantics without ephemeral checkpoint/path identity."""

    validated = validate_lifecycle_inspection_v07(dict(value))
    decision = validated["temporal_decision"]
    basis = validated["checkpoint_basis"]
    inventory = basis["local_work_inventory"]
    custody = basis["provider_custody"]
    authority = basis["external_authority_state"]
    return {
        "schema_version": validated["schema_version"],
        "run_id": validated["run_id"],
        "route_family": basis["native_route"]["route_family"],
        "provider_mechanism": (
            custody["actions"][0]["provider_operation_kind"]
            if custody["actions"] else "none"
        ),
        "selected_command": decision["selected_command"],
        "capacity_disposition": decision["capacity_disposition"],
        "reason_code": decision["reason_code"],
        "eligible_now": decision["eligible_now"],
        "due_action_ids": list(decision["due_action_ids"]),
        "not_before_present": decision["not_before"] is not None,
        "provider_custody": {
            "classification": custody["state"],
            "action_ids": list(custody["action_ids"]),
        },
        "local_operations": [{
            "kind": item["kind"],
            "stage": item["stage"],
            "source_action_ids": list(item["source_action_ids"]),
            "reason_code": item["reason_code"],
        } for item in inventory["operations"]],
        "consumed_operation_count": len(inventory["consumed_operation_keys"]),
        "external_authority_action_ids": list(authority["ordered_action_ids"]),
    }


def _binding(run_id: str, route: str, revision: int) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "profile_sha256": "a" * 64,
        "prepared_state_revision": revision,
        "stage": "creative_retry",
        "route": route,
        "request_sha256": "b" * 64,
        "model": "scripted-provider",
        "service_level": "interactive",
        "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def read_post_fan_in_retry_fixture() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        FIXTURE_RESOURCE,
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "scenario_id", "route_family", "provider_mechanism",
        "historical_incident", "corrected_sequence", "endpoint",
        "prohibited_public_fields",
    }:
        raise ValueError("Post-fan-in retry fixture fields are not exact")
    if value.get("schema_version") != "astrowoof.post_fan_in_retry_fixture.v1":
        raise ValueError("Unsupported post-fan-in retry fixture")
    if value.get("scenario_id") != "post_fan_in_retry_ordinary_v2":
        raise ValueError("Post-fan-in retry scenario identity differs")
    if value.get("route_family") != "exact_natal" or value.get("provider_mechanism") != "response":
        raise ValueError("Post-fan-in retry fixture route differs")
    expected = [
        "provider_not_due", "provider_retrieval", "local_fan_in",
        "local_operation_consumed", "ordinary_v2_authority", "one_dispatch",
        "exact_replay",
    ]
    if value.get("corrected_sequence") != expected:
        raise ValueError("Post-fan-in retry corrected sequence differs")
    if value.get("endpoint") != "detached_provider_pending":
        raise ValueError("Post-fan-in retry endpoint differs")
    prohibited = value.get("prohibited_public_fields")
    if prohibited != [
        "private_selector", "prompt", "provider_payload", "raw_run_state",
        "retained_qa_data", "workspace_path",
    ]:
        raise ValueError("Post-fan-in retry privacy inventory differs")
    return value


def read_post_fan_in_retry_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        SCHEMA_RESOURCE,
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _materialize(root: Path) -> tuple[Path, str, str]:
    run_dir = root / "post-fan-in-retry"
    run_dir.mkdir()
    run_id = "fixture-post-fan-in-retry"
    first = "paid_000000000000000000000101"
    second = "paid_000000000000000000000102"
    actions: list[dict[str, Any]] = []
    for number in range(1, 7):
        actions.append({
            "action_id": f"paid_{number:024x}",
            "state": "REPORTED",
            "binding": {
                **_binding(run_id, f"pass-{number}:attempt-001", 1),
                "stage": "authoring_initial",
            },
            "provider": {"id": f"resp_fixture_initial_{number}", "kind": "response"},
            "reported": {"estimated_micro_usd": 0},
        })
    actions.extend((
        {
            "action_id": first,
            "state": "WAITING",
            "binding": _binding(run_id, "pass-1:attempt-002", 7),
            "provider": {"id": "resp_fixture_retry_1", "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-27T11:59:00Z",
                "last_outcome": "pending",
                "resume_not_before": "2026-08-27T12:01:00Z",
            },
            "reported": None,
        },
        {
            "action_id": second,
            "state": "PREPARED",
            "binding": _binding(run_id, "pass-1:attempt-003", 8),
        },
    ))
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": run_id,
        "state_revision": 8,
        "created_at": "2026-08-27T11:58:00Z",
        "updated_at": "2026-08-27T12:00:00Z",
        "provider": "fake",
        "provider_configuration": {},
        "max_attempts": 3,
        "status": "WAITING_FOR_RESPONSE",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "policy": {
                "currency": "USD",
                "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 100_000_000,
                "stage_ceilings_micro_usd": {
                    "authoring_initial": 100_000_000,
                    "creative_retry": 100_000_000,
                    "polish": 100_000_000,
                    "qualitative_critic": 100_000_000,
                    "qualitative_candidate": 100_000_000,
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip", "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            },
            "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {
            "pass-1": {
                "pass_id": "pass-1", "state": "WAITING_FOR_RESPONSE",
                "attempts": [
                    {"attempt_number": 1, "state": "PASS_QA_REJECTED"},
                    {"attempt_number": 2, "state": "WAITING_FOR_RESPONSE"},
                    {"attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION"},
                ],
            },
        },
        "subjects": {},
        "provenance": {},
    }
    payload = {"model": "scripted-provider", "input": "sanitized qualification"}
    artifact = persist_provider_request_payload(run_dir / "retry.private.json", payload)
    actions[-1]["binding"]["request_sha256"] = artifact["canonical_request_sha256"]
    actions[-1]["request_payload_artifact"] = artifact
    (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8",
    )
    write_workspace_snapshot(run_dir)
    return run_dir, first, second


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def run_post_fan_in_retry_qualification() -> dict[str, Any]:
    fixture = read_post_fan_in_retry_fixture()
    with tempfile.TemporaryDirectory(prefix="astrowoof-post-fan-in-") as temporary:
        run_dir, first, second = _materialize(Path(temporary))
        phases: list[dict[str, Any]] = []
        not_due = inspect_post_fan_in_lifecycle(
            run_dir, observed_at="2026-08-27T12:00:00Z",
            native_exclusive_access="declared",
        )
        validate_lifecycle_inspection_v07(not_due)
        phases.append({"phase": "provider_not_due", "evidence_sha256": _digest(_lifecycle_projection(not_due))})
        retrievals: list[str] = []
        no_op = reconcile_provider_cycle(
            run_dir, observed_at="2026-08-27T12:00:00Z",
            retrieve=lambda provider_id, _timeout: retrievals.append(provider_id) or {},
        )
        if no_op["outcome"] != "not_due" or retrievals:
            raise ValueError("Post-fan-in qualification not-due boundary failed")
        due = reconcile_provider_cycle(
            run_dir, observed_at="2026-08-27T12:01:00Z",
            retrieve=lambda provider_id, _timeout: (
                retrievals.append(provider_id)
                or {"id": provider_id, "status": "completed", "output": []}
            ),
        )
        if due["outcome"] != "progressed_local" or retrievals != ["resp_fixture_retry_1"]:
            raise ValueError("Post-fan-in qualification retrieval boundary failed")
        phases.append({
            "phase": "provider_retrieval",
            "evidence_sha256": _digest({
                "outcome": due["outcome"],
                "completed_action_ids": due["cycle"]["completed_action_ids"],
                "retrieved_provider_operation_count": len(retrievals),
            }),
        })
        local = inspect_post_fan_in_lifecycle(
            run_dir, observed_at="2026-08-27T12:01:01Z",
            native_exclusive_access="declared",
        )
        validate_lifecycle_inspection_v07(local)
        if local["temporal_decision"]["selected_command"] != "ordinary_resume":
            raise ValueError("Post-fan-in qualification did not expose local fan-in")
        phases.append({"phase": "local_fan_in", "evidence_sha256": _digest(_lifecycle_projection(local))})

        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        completed = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == first)
        completed["state"] = "REPORTED"
        completed["reported"] = {"estimated_micro_usd": 0}
        state["status"] = "AWAITING_SPEND_AUTHORIZATION"
        save_state(state_path, state)
        successor = commit_local_work_progress(
            run_dir, prior=local, observed_at="2026-08-27T12:01:02Z",
        )
        if successor["temporal_decision"]["selected_command"] != "await_external_authority":
            raise ValueError("Post-fan-in qualification did not consume local work")
        phases.append({"phase": "local_operation_consumed", "evidence_sha256": _digest(_lifecycle_projection(successor))})

        inspection = inspect_temporal_lifecycle(
            run_dir, native_exclusive_access="declared",
            observed_at="2026-08-27T12:01:02Z",
        )
        request = build_external_authority_request_v2(inspection)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == second)
        document = {
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": second,
            "binding": copy.deepcopy(action["binding"]),
            "authorization_reference": "fixture:ordinary-v2",
        }
        grant = build_external_authority_grant_v2(
            request, inspection, [document], api_decision_id="fixture:ordinary-v2",
            issuer="astrowoof-api-provider-free", issued_at="2026-08-27T12:01:03Z",
        )
        intent = commit_external_authority_v2_dispatch_intent(
            run_dir, request=request, inspection=inspection, grant=grant,
            authorization_documents=[document],
        )
        phases.append({
            "phase": "ordinary_v2_authority",
            "evidence_sha256": _digest({
                "request_kind": request["request_kind"],
                "ordered_action_ids": request["ordered_action_ids"],
                "intent_outcome": intent["outcome"],
            }),
        })
        creates: list[str] = []
        dispatched = dispatch_external_authority_v2_intent(
            run_dir,
            request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"],
            create=lambda selected: (
                creates.append(selected["action_id"])
                or {"id": "resp_fixture_retry_2", "kind": "response"}
            ),
        )
        if dispatched["outcome"] != "detached_provider_pending" or creates != [second]:
            raise ValueError("Post-fan-in qualification dispatch failed")
        phases.append({
            "phase": "one_dispatch",
            "evidence_sha256": _digest({
                "outcome": dispatched["outcome"],
                "created_action_ids": list(creates),
            }),
        })
        replay = dispatch_external_authority_v2_intent(
            run_dir,
            request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"],
            create=lambda selected: creates.append(selected["action_id"]) or {},
        )
        if replay["outcome"] != "exact_replay" or creates != [second]:
            raise ValueError("Post-fan-in qualification replay duplicated create")
        phases.append({
            "phase": "exact_replay",
            "evidence_sha256": _digest({
                "outcome": replay["outcome"],
                "created_action_ids": list(creates),
                "duplicate_create_count": 0,
            }),
        })
        endpoint = inspect_post_fan_in_lifecycle(
            run_dir, observed_at="2026-08-27T12:01:04Z",
            native_exclusive_access="declared",
        )
        validate_lifecycle_inspection_v07(endpoint)
        if endpoint["temporal_decision"]["selected_command"] != "provider_reconciliation_cycle":
            raise ValueError("Post-fan-in qualification endpoint is not provider pending")

    body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "package": {"name": "astrowoof-natal-authoring", "version": _package_version()},
        "fixture_sha256": _digest(fixture),
        "historical_incident": fixture["historical_incident"],
        "phases": phases,
        "endpoint": "detached_provider_pending",
        "endpoint_evidence_sha256": _digest(_lifecycle_projection(endpoint)),
        "scripted_retrieval_count": len(retrievals),
        "scripted_create_count": len(creates),
        "duplicate_create_count": 0,
        "external_network_call_count": 0,
        "provider_spend_usd": 0,
        "privacy": {
            "contains_prompt": False,
            "contains_provider_payload": False,
            "contains_raw_run_state": False,
            "contains_workspace_path": False,
            "contains_retained_qa_data": False,
        },
    }
    return validate_post_fan_in_retry_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_post_fan_in_retry_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "fixture_sha256", "historical_incident",
        "phases", "endpoint", "endpoint_evidence_sha256",
        "scripted_retrieval_count", "scripted_create_count",
        "duplicate_create_count", "external_network_call_count",
        "provider_spend_usd", "privacy",
    }
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != CONTRACT:
        raise ValueError("Post-fan-in qualification receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Post-fan-in qualification receipt digest mismatch")
    if value.get("status") != "pass" or value.get("qualification_only") is not True or value.get("provider_free") is not True:
        raise ValueError("Post-fan-in qualification declaration is invalid")
    if value.get("fixture_sha256") != _digest(read_post_fan_in_retry_fixture()):
        raise ValueError("Post-fan-in qualification fixture digest mismatch")
    package = value.get("package")
    if not isinstance(package, Mapping) or set(package) != {"name", "version"} or package.get("name") != "astrowoof-natal-authoring" or not isinstance(package.get("version"), str) or not package["version"]:
        raise ValueError("Post-fan-in qualification package identity is invalid")
    if value.get("historical_incident") != read_post_fan_in_retry_fixture()["historical_incident"]:
        raise ValueError("Post-fan-in qualification incident identity differs")
    endpoint_digest = value.get("endpoint_evidence_sha256")
    if not isinstance(endpoint_digest, str) or len(endpoint_digest) != 64 or any(character not in "0123456789abcdef" for character in endpoint_digest):
        raise ValueError("Post-fan-in endpoint evidence digest is invalid")
    expected_phases = read_post_fan_in_retry_fixture()["corrected_sequence"]
    phases = value.get("phases")
    if not isinstance(phases, list) or [item.get("phase") for item in phases if isinstance(item, Mapping)] != expected_phases:
        raise ValueError("Post-fan-in qualification phases differ")
    for item in phases:
        if set(item) != {"phase", "evidence_sha256"} or not isinstance(item["evidence_sha256"], str) or len(item["evidence_sha256"]) != 64:
            raise ValueError("Post-fan-in qualification phase evidence is invalid")
    if value.get("endpoint") != "detached_provider_pending" or value.get("scripted_retrieval_count") != 1 or value.get("scripted_create_count") != 1:
        raise ValueError("Post-fan-in qualification endpoint/counts differ")
    if value.get("duplicate_create_count") != 0 or value.get("external_network_call_count") != 0 or value.get("provider_spend_usd") != 0:
        raise ValueError("Post-fan-in qualification safety counts differ")
    privacy = value.get("privacy")
    if not isinstance(privacy, Mapping) or set(privacy) != {
        "contains_prompt", "contains_provider_payload", "contains_raw_run_state",
        "contains_workspace_path", "contains_retained_qa_data",
    } or any(item is not False for item in privacy.values()):
        raise ValueError("Post-fan-in qualification privacy declaration differs")
    return dict(value)


def _inside_native_workspace(path: Path) -> bool:
    target = path.resolve()
    return any(
        (parent / "run.json").exists() or (parent / "workspace-snapshot.json").exists()
        for parent in (target.parent, *target.parents)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run provider-free post-fan-in retry qualification.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args(argv)
    if args.schema and args.fixture:
        parser.error("--schema and --fixture are mutually exclusive")
    if args.output and _inside_native_workspace(args.output):
        parser.error("--output must not be inside a native SBE workspace")
    value = (
        read_post_fan_in_retry_qualification_schema() if args.schema
        else read_post_fan_in_retry_fixture() if args.fixture
        else run_post_fan_in_retry_qualification()
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
