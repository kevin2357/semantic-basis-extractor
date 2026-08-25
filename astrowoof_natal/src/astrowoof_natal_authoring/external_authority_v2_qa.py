"""Installed-wheel, provider-free external-authority v2 bridge qualification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
import shutil
import tempfile
from typing import Any

from .closure import normalized_path, persist_state, public_run_state, write_workspace_snapshot, load_json
from .deployed_qa import _wave
from .external_authority_v2 import build_external_authority_grant_v2
from .external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
)
from .initial_wave import ProviderCreateResult, build_wave_authorization, execute_initial_wave_creates
from .reconciliation import reconcile_provider_cycle
from .spend import prepare_action
from .temporal_lifecycle import build_external_authority_request_v2, inspect_temporal_lifecycle


RECEIPT_SCHEMA = "astrowoof.external_authority_v2_qualification.v1"
_ASSERTIONS = {
    "exact_holistic_4_plus_2_bridge", "bounded_holistic_4_plus_2_bridge",
    "ordinary_response_stage_matrix", "ordinary_batch_explicitly_deferred",
    "identity_before_next_create", "reconciliation_only_after_dispatch",
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _policy() -> dict[str, Any]:
    ceiling = 100_000_000
    return {
        "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
        "run_ceiling_micro_usd": ceiling,
        "stage_ceilings_micro_usd": {stage: ceiling for stage in (
            "authoring_initial", "creative_retry", "polish",
            "qualitative_critic", "qualitative_candidate",
        )},
        "optional_stage_budget_behavior": {
            "polish": "skip", "qualitative_critic": "skip", "qualitative_candidate": "skip",
        },
    }


def _pending_workspace(root: Path, route_family: str) -> list[str]:
    root.mkdir(parents=True, exist_ok=True)
    wave, documents = _wave(route_family)
    envelope = build_wave_authorization(
        wave, documents, reservation_set_reference="qualification:no-reservation",
        issuer="sbe-installed-qualification", authorized_at="1970-01-01T00:00:00Z",
    )
    creates: list[str] = []
    outcomes: list[dict[str, Any]] = []

    def submit(member: dict[str, Any], _timeout: int) -> ProviderCreateResult:
        provider_id = f"resp_{route_family}_{member['pass_number']:02d}"
        creates.append(provider_id)
        return ProviderCreateResult(provider_id)

    result = execute_initial_wave_creates(
        wave, authorization=envelope, member_authorizations=documents, submit=submit,
        persist_member_outcome=lambda _member, outcome: outcomes.append(copy.deepcopy(outcome)),
    )
    if result["outcome"] != "detached_provider_pending":
        raise RuntimeError("qualification initial wave did not detach")
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
    state: dict[str, Any] = {
        "schema_version": (
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal" else "astrowoof.semantic_closure_run.v0.9"
        ),
        "run_id": wave["run_id"], "state_revision": 1,
        "status": "WAITING_FOR_RESPONSE", "passes": passes, "subjects": {},
        "authoring_profile": {
            "qa": {"polish": True, "qualitative_critic": True, "qualitative_candidate": True},
            "optional_stages": {"polish": True, "qualitative_critic": True, "qualitative_candidate": True},
        },
        "workspace_contract": {"mode": "stable_logical_absolute_path", "logical_root": normalized_path(root)},
        "spend_ledger": {"schema_version": "astrowoof.provider_spend_ledger.v0.1", "policy": _policy(), "actions": actions},
        "initial_authoring_wave": {"state": "DETACHED"},
    }
    if route_family == "bounded_natal":
        state.update({
            "route": "bounded_natal.v2", "route_contract": "astrowoof.bounded_natal.authoring_run.v2",
            "service_level": "interactive",
        })
    (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
    write_workspace_snapshot(root)
    return creates


def _reconcile_4_plus_2(root: Path) -> tuple[list[int], list[str]]:
    retrievals: list[str] = []

    def retrieve(provider_id: str, _timeout: float) -> dict[str, Any]:
        retrievals.append(provider_id)
        return {"id": provider_id, "status": "completed", "output": []}

    counts = []
    for observed_at in ("1970-01-01T00:00:15Z", "1970-01-01T00:01:00Z"):
        cycle = reconcile_provider_cycle(root, observed_at=observed_at, retrieve=retrieve)
        counts.append(cycle["cycle"]["provider_retrieval_count"])
        state = load_json(root / "run.json")
        completed = set(cycle["cycle"]["completed_action_ids"])
        for action in state["spend_ledger"]["actions"]:
            if action["action_id"] in completed:
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
        persist_state(root / "run.json", state)
        write_workspace_snapshot(root)
    return counts, retrievals


def _ordinary_authority(root: Path, route_family: str, stage: str, service_level: str = "interactive"):
    state = load_json(root / "run.json")
    route = f"bounded_natal.v2:{stage}:attempt-001" if route_family == "bounded_natal" else f"{stage}:attempt-001"
    binding = {
        "run_id": state["run_id"], "profile_sha256": "a" * 64,
        "prepared_state_revision": state["state_revision"], "stage": stage,
        "route": route, "request_sha256": _digest({"stage": stage, "route": route}),
        "model": "scripted-provider", "service_level": service_level,
        "maximum_output_tokens": 1000, "commitment_micro_usd": 1,
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


def _route(root: Path, route_family: str) -> dict[str, Any]:
    initial = _pending_workspace(root, route_family)
    cycles, retrievals = _reconcile_4_plus_2(root)
    stage_outcomes: dict[str, str] = {}
    next_commands: dict[str, str] = {}
    ordinary_count = 0
    for stage in ("creative_retry", "polish", "qualitative_critic", "qualitative_candidate"):
        case = root.parent / f"{route_family}-{stage}"
        shutil.copytree(root, case)
        state = load_json(case / "run.json")
        state["workspace_contract"]["logical_root"] = normalized_path(case)
        (case / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        write_workspace_snapshot(case)
        inspection, request, documents, grant = _ordinary_authority(case, route_family, stage)
        commit_external_authority_v2_dispatch_intent(
            case, request=request, inspection=inspection, grant=grant,
            authorization_documents=documents,
        )
        ordinary: list[str] = []
        result = dispatch_external_authority_v2_intent(
            case, request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"],
            create=lambda action, selected_stage=stage: (
                ordinary.append(action["action_id"])
                or {"id": f"resp_v2_{route_family}_{selected_stage}", "kind": "response"}
            ),
        )
        due = inspect_temporal_lifecycle(
            case, native_exclusive_access="established", observed_at="2099-01-01T00:00:00Z",
        )
        stage_outcomes[stage] = result["outcome"]
        next_commands[stage] = due["temporal_decision"]["selected_command"]
        ordinary_count += len(ordinary)
    return {
        "route_family": route_family, "initial_create_count": len(initial),
        "initial_create_unique_count": len(set(initial)),
        "retrieval_cycle_counts": cycles, "retrieval_count": len(retrievals),
        "retrieval_unique_count": len(set(retrievals)),
        "ordinary_create_count": ordinary_count, "stage_outcomes": stage_outcomes,
        "next_commands": next_commands,
    }


def validate_external_authority_v2_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "real_provider_create_count",
        "real_provider_retrieval_count", "provider_spend_usd", "sbe_version",
        "routes", "assertions",
    }
    if not isinstance(value, dict) or set(value) != keys or value.get("schema_version") != RECEIPT_SCHEMA:
        raise ValueError("v2 qualification receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("v2 qualification receipt digest mismatch")
    if (
        value.get("status") != "pass" or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "real_provider_create_count",
            "real_provider_retrieval_count", "provider_spend_usd",
        ))
    ):
        raise ValueError("v2 qualification safety declaration is invalid")
    routes = value.get("routes")
    if not isinstance(routes, dict) or set(routes) != {"exact_natal", "bounded_natal"}:
        raise ValueError("v2 qualification route inventory is invalid")
    route_keys = {
        "route_family", "initial_create_count", "initial_create_unique_count",
        "retrieval_cycle_counts", "retrieval_count", "retrieval_unique_count",
        "ordinary_create_count", "stage_outcomes", "next_commands",
    }
    stages = {"creative_retry", "polish", "qualitative_critic", "qualitative_candidate"}
    for name, route in routes.items():
        if (
            not isinstance(route, dict) or set(route) != route_keys
            or route.get("route_family") != name
            or route.get("initial_create_count") != 6
            or route.get("initial_create_unique_count") != 6
            or route.get("retrieval_cycle_counts") != [4, 2]
            or route.get("retrieval_count") != 6
            or route.get("retrieval_unique_count") != 6
            or route.get("ordinary_create_count") != 4
            or set(route.get("stage_outcomes") or {}) != stages
            or any(item != "detached_provider_pending" for item in route["stage_outcomes"].values())
            or set(route.get("next_commands") or {}) != stages
            or any(item != "provider_reconciliation_cycle" for item in route["next_commands"].values())
        ):
            raise ValueError(f"v2 qualification route evidence is invalid for {name}")
    assertions = value.get("assertions")
    if not isinstance(assertions, dict) or set(assertions) != _ASSERTIONS or any(item is not True for item in assertions.values()):
        raise ValueError("v2 qualification assertions are not closed and passing")
    return copy.deepcopy(value)


def read_external_authority_v2_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-qualification.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def run_external_authority_v2_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="sbe-external-authority-v2-qa-") as temporary:
        outer = Path(temporary)
        routes = {
            route: _route(outer / route, route)
            for route in ("exact_natal", "bounded_natal")
        }
        # The complete stage matrix is enforced by the same closed adapter predicate;
        # exercise its unsupported Batch boundary in a separate exact workspace.
        deferred = outer / "deferred"
        _pending_workspace(deferred, "exact_natal")
        _reconcile_4_plus_2(deferred)
        inspection, request, documents, grant = _ordinary_authority(
            deferred, "exact_natal", "polish", "batch",
        )
        batch_refused = False
        try:
            commit_external_authority_v2_dispatch_intent(
                deferred, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
        except ExternalAuthorityV2ExecutionError as exc:
            batch_refused = exc.reason_code == "unsupported_contract"
        assertions = {
            "exact_holistic_4_plus_2_bridge": routes["exact_natal"]["retrieval_cycle_counts"] == [4, 2],
            "bounded_holistic_4_plus_2_bridge": routes["bounded_natal"]["retrieval_cycle_counts"] == [4, 2],
            "ordinary_response_stage_matrix": all(
                item["ordinary_create_count"] == 4
                and all(outcome == "detached_provider_pending" for outcome in item["stage_outcomes"].values())
                for item in routes.values()
            ),
            "ordinary_batch_explicitly_deferred": batch_refused,
            "identity_before_next_create": all(item["initial_create_unique_count"] == 6 for item in routes.values()),
            "reconciliation_only_after_dispatch": all(
                all(command == "provider_reconciliation_cycle" for command in item["next_commands"].values())
                for item in routes.values()
            ),
        }
    try:
        installed = version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        installed = "source-tree"
    body = {
        "schema_version": RECEIPT_SCHEMA,
        "status": "pass" if all(assertions.values()) else "fail",
        "qualification_only": True, "provider_free": True,
        "external_network_call_count": 0, "real_provider_create_count": 0,
        "real_provider_retrieval_count": 0, "provider_spend_usd": 0,
        "sbe_version": installed, "routes": routes, "assertions": assertions,
    }
    return validate_external_authority_v2_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run provider-free external-authority v2 qualification.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = read_external_authority_v2_qualification_schema() if args.schema else run_external_authority_v2_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
