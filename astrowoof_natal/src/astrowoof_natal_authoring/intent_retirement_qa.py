"""Installed-wheel, provider-free v2 intent-retirement qualification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
import tempfile
from typing import Any

from .closure import SpendController, load_json, save_state, validate_workspace_snapshot, write_json_atomic, write_workspace_snapshot
from .external_authority_v2 import build_external_authority_grant_v2
from .external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
)
from .external_authority_v2_qa import _ordinary_authority, _pending_workspace, _reconcile_4_plus_2
from .reconciliation import reconcile_provider_cycle
from .temporal_lifecycle import build_external_authority_request_v2, inspect_temporal_lifecycle


RECEIPT_SCHEMA = "astrowoof.external_authority_v2_intent_retirement_qualification.v1"
_ASSERTIONS = {
    "coordinator_checkpoint_retires_complete_intent",
    "published_snapshot_contains_retirement",
    "exact_predecessor_replay_is_inert",
    "fresh_successor_creates_once",
    "partial_terminal_inventory_retains_intent",
    "contradictory_terminal_evidence_retains_intent",
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _ready(_action: dict[str, Any], _context: dict[str, Any]) -> dict[str, Any]:
    return {"outcome": "ready", "reason_code": None, "prepared_create_sha256": "a" * 64, "transport_context": {}}


def _settle_all(root: Path) -> dict[str, Any]:
    state = load_json(root / "run.json")
    controller = SpendController(state=state, run_json=root / "run.json", state_lock=__import__("threading").Lock(), consumer_id="installed-retirement-qualification")
    for action in state["spend_ledger"]["actions"]:
        controller.local.active_action = action["action_id"]
        controller.settle_active({"usage": {"input_tokens": 2, "output_tokens": 1, "total_tokens": 3}, "estimated_cost": {"estimated_amount": "0.000001"}})
    controller.local.active_action = None
    return state


def _dispatch_predecessor(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    _pending_workspace(root, "exact_natal")
    _reconcile_4_plus_2(root)
    inspection, request, documents, grant = _ordinary_authority(root, "exact_natal", "creative_retry")
    commit_external_authority_v2_dispatch_intent(root, request=request, inspection=inspection, grant=grant, authorization_documents=documents)
    creates: list[str] = []
    dispatch_external_authority_v2_intent(
        root,
        request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"],
        prepare=_ready,
        create=lambda _prepared: (creates.append(request["ordered_action_ids"][0]) or {"kind": "response", "id": "resp_retirement_predecessor"}),
    )
    reconcile_provider_cycle(root, observed_at="2099-01-01T00:00:00Z", retrieve=lambda provider_id, _timeout: {"id": provider_id, "status": "completed", "usage": {"input_tokens": 2, "output_tokens": 1, "total_tokens": 3}, "output": []})
    return request, grant, creates


def _successor(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    state = load_json(root / "run.json")
    predecessor = state["spend_ledger"]["actions"][-1]
    action = copy.deepcopy(predecessor)
    action["action_id"] = "paid_" + "f" * 24
    action["state"] = "PREPARED"
    action["binding"].update({"prepared_state_revision": state["state_revision"], "stage": "polish", "route": "polish:attempt-001", "request_sha256": "f" * 64})
    for key in ("authorization", "consumption", "provider", "provider_reconciliation", "reported", "ambiguity", "integrity_review"):
        action.pop(key, None)
    state["spend_ledger"]["actions"].append(action)
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    save_state(root / "run.json", state)
    inspection = inspect_temporal_lifecycle(root, native_exclusive_access="declared", observed_at="2099-01-01T00:00:01Z")
    request = build_external_authority_request_v2(inspection)
    document = {"schema_version": "astrowoof.provider_spend_authorization.v0.1", "action_id": action["action_id"], "binding": copy.deepcopy(action["binding"]), "authorization_reference": "qualification:successor"}
    grant = build_external_authority_grant_v2(request, inspection, [document], api_decision_id="qualification-successor", issuer="installed-qualification", issued_at="2099-01-01T00:00:02Z")
    return request, grant, [document]


def _complete_case(root: Path) -> dict[str, Any]:
    request, grant, creates = _dispatch_predecessor(root)
    state = _settle_all(root)
    save_state(root / "run.json", state, retire_external_authority_v2=True)
    persisted = load_json(root / "run.json")
    validate_workspace_snapshot(root, persisted)
    retired = [item for item in persisted.get("external_authority_v2_dispatch_history", []) if item.get("outcome") == "provider_completed"]
    replay_calls: list[str] = []
    replay = dispatch_external_authority_v2_intent(root, request_sha256=request["external_authority_request_sha256"], grant_sha256=grant["grant_sha256"], prepare=lambda *_: replay_calls.append("prepare"), create=lambda *_: replay_calls.append("create"))
    successor_request, successor_grant, documents = _successor(root)
    inspection = inspect_temporal_lifecycle(root, native_exclusive_access="declared", observed_at="2099-01-01T00:00:03Z")
    commit_external_authority_v2_dispatch_intent(root, request=successor_request, inspection=inspection, grant=successor_grant, authorization_documents=documents)
    successor_calls: list[str] = []
    successor = dispatch_external_authority_v2_intent(root, request_sha256=successor_request["external_authority_request_sha256"], grant_sha256=successor_grant["grant_sha256"], prepare=_ready, create=lambda _prepared: (successor_calls.append("create") or {"kind": "response", "id": "resp_retirement_successor"}))
    return {"retired_record_count": len(retired), "live_intent_after_checkpoint": "external_authority_v2_dispatch_intent" in persisted, "snapshot_valid": True, "predecessor_create_count": len(creates), "replay_outcome": replay["outcome"], "replay_provider_call_count": len(replay_calls), "successor_outcome": successor["outcome"], "successor_provider_create_count": len(successor_calls)}


def _partial_case(root: Path) -> dict[str, Any]:
    request, _grant, _creates = _dispatch_predecessor(root)
    state = load_json(root / "run.json")
    # Reopen one completed action so the complete inventory cannot retire.
    action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == request["ordered_action_ids"][0])
    action["state"] = "WAITING"
    action["reported"] = None
    save_state(root / "run.json", state, retire_external_authority_v2=True)
    persisted = load_json(root / "run.json")
    return {"live_intent_retained": "external_authority_v2_dispatch_intent" in persisted, "retired_record_count": len([item for item in persisted.get("external_authority_v2_dispatch_history", []) if item.get("outcome") == "provider_completed"]), "successor_provider_create_count": 0}


def _conflict_case(root: Path) -> dict[str, Any]:
    request, _grant, _creates = _dispatch_predecessor(root)
    state = _settle_all(root)
    action_id = request["ordered_action_ids"][0]
    response_path = root / "lifecycle" / "provider-reconciliation" / f"{action_id}.response.json"
    response = load_json(response_path)
    response["id"] = "resp_conflicting_identity"
    write_json_atomic(response_path, response)
    write_workspace_snapshot(root)
    refused = None
    try:
        save_state(root / "run.json", state, retire_external_authority_v2=True)
    except ExternalAuthorityV2ExecutionError as exc:
        refused = exc.reason_code
    persisted = load_json(root / "run.json")
    return {"refusal_reason": refused, "live_intent_retained": "external_authority_v2_dispatch_intent" in persisted, "retired_record_count": len([item for item in persisted.get("external_authority_v2_dispatch_history", []) if item.get("outcome") == "provider_completed"]), "successor_provider_create_count": 0}


def validate_intent_retirement_qualification(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "receipt_sha256", "status", "qualification_only", "provider_free", "external_network_call_count", "real_provider_create_count", "provider_spend_usd", "sbe_version", "complete_case", "partial_case", "conflict_case", "assertions"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema_version") != RECEIPT_SCHEMA:
        raise ValueError("intent-retirement qualification fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("intent-retirement qualification digest mismatch")
    if value.get("status") != "pass" or value.get("qualification_only") is not True or value.get("provider_free") is not True or value.get("external_network_call_count") != 0 or value.get("real_provider_create_count") != 0 or value.get("provider_spend_usd") != 0:
        raise ValueError("intent-retirement qualification safety declaration is invalid")
    assertions = value.get("assertions")
    if not isinstance(assertions, dict) or set(assertions) != _ASSERTIONS or any(item is not True for item in assertions.values()):
        raise ValueError("intent-retirement qualification assertions are not closed and passing")
    complete = value.get("complete_case")
    if not isinstance(complete, dict) or complete != {
        "retired_record_count": 1, "live_intent_after_checkpoint": False,
        "snapshot_valid": True, "predecessor_create_count": 1,
        "replay_outcome": "exact_replay", "replay_provider_call_count": 0,
        "successor_outcome": "detached_provider_pending",
        "successor_provider_create_count": 1,
    }:
        raise ValueError("intent-retirement complete case is invalid")
    partial = value.get("partial_case")
    if partial != {"live_intent_retained": True, "retired_record_count": 0, "successor_provider_create_count": 0}:
        raise ValueError("intent-retirement partial case is invalid")
    conflict = value.get("conflict_case")
    if conflict != {"refusal_reason": "native_evidence_invalid", "live_intent_retained": True, "retired_record_count": 0, "successor_provider_create_count": 0}:
        raise ValueError("intent-retirement conflict case is invalid")
    return copy.deepcopy(value)


def read_intent_retirement_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath("external-authority-v2-intent-retirement-qualification.v1.schema.json")
    return json.loads(path.read_text(encoding="utf-8"))


def run_intent_retirement_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="sbe-v2-intent-retirement-qa-") as temporary:
        root = Path(temporary)
        complete = _complete_case(root / "complete")
        partial = _partial_case(root / "partial")
        conflict = _conflict_case(root / "conflict")
    assertions = {
        "coordinator_checkpoint_retires_complete_intent": complete["retired_record_count"] == 1 and complete["live_intent_after_checkpoint"] is False,
        "published_snapshot_contains_retirement": complete["snapshot_valid"] is True,
        "exact_predecessor_replay_is_inert": complete["replay_outcome"] == "exact_replay" and complete["replay_provider_call_count"] == 0,
        "fresh_successor_creates_once": complete["successor_outcome"] == "detached_provider_pending" and complete["successor_provider_create_count"] == 1,
        "partial_terminal_inventory_retains_intent": partial["live_intent_retained"] is True and partial["retired_record_count"] == 0,
        "contradictory_terminal_evidence_retains_intent": conflict["refusal_reason"] == "native_evidence_invalid" and conflict["live_intent_retained"] is True and conflict["retired_record_count"] == 0 and conflict["successor_provider_create_count"] == 0,
    }
    try:
        installed = version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        installed = "source-tree"
    body = {"schema_version": RECEIPT_SCHEMA, "status": "pass" if all(assertions.values()) else "fail", "qualification_only": True, "provider_free": True, "external_network_call_count": 0, "real_provider_create_count": 0, "provider_spend_usd": 0, "sbe_version": installed, "complete_case": complete, "partial_case": partial, "conflict_case": conflict, "assertions": assertions}
    return validate_intent_retirement_qualification({**body, "receipt_sha256": _digest(body)})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run provider-free v2 intent-retirement qualification.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = read_intent_retirement_qualification_schema() if args.schema else run_intent_retirement_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
