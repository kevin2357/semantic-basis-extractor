"""Closed retry-lineage and mixed-custody lifecycle v0.8 contracts.

This module is intentionally projection-only in its first slice.  Runtime
preparation and mutation continue to use the released paths until the v0.8
consumer contract has passed its cross-repository review gate.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.resources import files
import json
import re
from typing import Any, Mapping, Sequence

from .post_fan_in_contracts import validate_lifecycle_inspection_v07


RETRY_LINEAGE_SCHEMA = "astrowoof.retry_lineage_inventory.v1"
LIFECYCLE_INSPECTION_SCHEMA_V0_8 = "astrowoof.authoring_lifecycle_inspection.v0.8"
ATTEMPT_KEY_SERIALIZATION = "canonical_json_utf8_sorted_compact.v1"

ROUTE_FAMILIES = frozenset({"exact_natal", "bounded_natal"})
STAGES = frozenset({
    "authoring_initial", "creative_retry", "polish",
    "qualitative_critic", "qualitative_candidate",
})
MECHANISMS = frozenset({"response", "batch"})
ACTION_STATES = frozenset({
    "PREPARED", "AUTHORIZED", "SUBMITTING", "PROVIDER_ID_RECORDED",
    "WAITING", "REPORTED", "DENIED_PROVIDERLESS", "BUDGET_EXHAUSTED",
    "SKIPPED_BUDGET_EXHAUSTED", "AMBIGUOUS_PROVIDER_SUBMISSION",
})
CONFLICT_REASONS = frozenset({
    "multiple_actions_for_attempt", "request_binding_conflict",
    "pass_attempt_pointer_conflict", "multiple_active_actions_for_attempt",
})

_INVENTORY_KEYS = frozenset({
    "schema_version", "run_id", "ordering_semantics", "attempts", "status",
    "conflict_classification", "forward_dispatch_permitted",
    "reconciliation_permitted", "inventory_sha256",
})
_ATTEMPT_KEYS = frozenset({
    "attempt_key", "coordinates", "resolution", "selected_action_id",
    "actions", "reason_codes",
})
_COORDINATE_KEYS = frozenset({
    "native_run_id", "route_family", "stage", "pass_id", "attempt_number",
})
_ACTION_KEYS = frozenset({
    "action_id", "binding_sha256", "request_sha256", "state",
    "provider_mechanism", "provider_operation_id", "pass_attempt_pointer",
})


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _is_action_id(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"paid_[0-9a-f]{24}", value) is not None


def derive_retry_attempt_key(
    *, native_run_id: str, route_family: str, stage: str,
    pass_id: str, attempt_number: int,
) -> str:
    """Derive identity from logical coordinates, deliberately excluding binding."""
    coordinates = {
        "native_run_id": native_run_id, "route_family": route_family,
        "stage": stage, "pass_id": pass_id, "attempt_number": attempt_number,
    }
    _validate_coordinates(coordinates)
    return "attempt_" + _sha(coordinates)[:24]


def _validate_coordinates(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COORDINATE_KEYS:
        raise ValueError("Retry-attempt coordinates are not exact")
    if not isinstance(value["native_run_id"], str) or not value["native_run_id"]:
        raise ValueError("Retry-attempt native run identity is invalid")
    if value["route_family"] not in ROUTE_FAMILIES:
        raise ValueError("Retry-attempt route family is invalid")
    if value["stage"] not in STAGES:
        raise ValueError("Retry-attempt stage is invalid")
    if not isinstance(value["pass_id"], str) or not value["pass_id"]:
        raise ValueError("Retry-attempt pass identity is invalid")
    attempt = value["attempt_number"]
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
        raise ValueError("Retry-attempt number is invalid")
    return value


def build_retry_lineage_inventory(
    *, run_id: str, actions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Group public action evidence by basis-independent logical attempt."""
    grouped: dict[str, dict[str, Any]] = {}
    for raw in actions:
        coordinates = {
            key: raw[key] for key in _COORDINATE_KEYS
        }
        _validate_coordinates(coordinates)
        if coordinates["native_run_id"] != run_id:
            raise ValueError("Retry-lineage action belongs to another run")
        key = derive_retry_attempt_key(**coordinates)
        evidence = {key: raw.get(key) for key in _ACTION_KEYS}
        grouped.setdefault(key, {"coordinates": coordinates, "actions": []})[
            "actions"
        ].append(evidence)

    attempts: list[dict[str, Any]] = []
    for attempt_key, group in sorted(grouped.items()):
        members = sorted(group["actions"], key=lambda item: item["action_id"])
        reasons: set[str] = set()
        if len(members) > 1:
            reasons.add("multiple_actions_for_attempt")
        if len({(item["binding_sha256"], item["request_sha256"]) for item in members}) > 1:
            reasons.add("request_binding_conflict")
        if len({item["pass_attempt_pointer"] for item in members}) > 1:
            reasons.add("pass_attempt_pointer_conflict")
        active = [item for item in members if item["state"] not in {
            "REPORTED", "DENIED_PROVIDERLESS", "BUDGET_EXHAUSTED",
            "SKIPPED_BUDGET_EXHAUSTED",
        }]
        if len(active) > 1:
            reasons.add("multiple_active_actions_for_attempt")
        attempts.append({
            "attempt_key": attempt_key,
            "coordinates": group["coordinates"],
            "resolution": "conflict" if reasons else "consistent",
            "selected_action_id": members[0]["action_id"] if len(members) == 1 else None,
            "actions": members,
            "reason_codes": sorted(reasons),
        })
    conflict = any(item["resolution"] == "conflict" for item in attempts)
    provider_identity = any(
        member["provider_operation_id"] is not None
        for item in attempts for member in item["actions"]
    )
    body = {
        "schema_version": RETRY_LINEAGE_SCHEMA,
        "run_id": run_id,
        "ordering_semantics": "lexical_attempt_key_then_action_id",
        "attempts": attempts,
        "status": "conflict" if conflict else "consistent",
        "conflict_classification": (
            "retry_lineage_conflict_requires_review" if conflict else None
        ),
        "forward_dispatch_permitted": not conflict,
        "reconciliation_permitted": provider_identity,
    }
    body["inventory_sha256"] = _sha(body)
    return validate_retry_lineage_inventory(body)


def retry_lineage_inventory_from_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Project exact public lineage evidence from one native action ledger."""
    run_id = str(state.get("run_id") or "")
    route_family = (
        "bounded_natal"
        if state.get("schema_version") == "astrowoof.bounded_natal.authoring_run.v2"
        else "exact_natal"
    )
    projected: list[dict[str, Any]] = []
    for action in (state.get("spend_ledger") or {}).get("actions") or []:
        binding = action.get("binding") or {}
        if binding.get("stage") != "creative_retry":
            continue
        route = str(binding.get("route") or "")
        pass_id, attempt_number = _route_coordinates(route)
        mechanism = "batch" if binding.get("service_level") == "batch" else "response"
        projected.append({
            "native_run_id": run_id, "route_family": route_family,
            "stage": "creative_retry", "pass_id": pass_id,
            "attempt_number": attempt_number,
            "action_id": action.get("action_id"),
            "binding_sha256": _sha(binding),
            "request_sha256": binding.get("request_sha256"),
            "state": action.get("state"), "provider_mechanism": mechanism,
            "provider_operation_id": (action.get("provider") or {}).get("id"),
            "pass_attempt_pointer": (
                f"passes/{pass_id}/attempts/{attempt_number}"
            ),
        })
    return build_retry_lineage_inventory(run_id=run_id, actions=projected)


def assert_retry_lineage_forward_dispatch_safe(state: Mapping[str, Any]) -> None:
    inventory = retry_lineage_inventory_from_state(state)
    if not inventory["forward_dispatch_permitted"]:
        raise ValueError("Retry lineage conflict blocks forward provider dispatch")


def validate_retry_lineage_inventory(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _INVENTORY_KEYS:
        raise ValueError("Retry-lineage inventory fields are not exact")
    if value.get("schema_version") != RETRY_LINEAGE_SCHEMA:
        raise ValueError("Unsupported retry-lineage schema")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Retry-lineage run identity is invalid")
    if value.get("ordering_semantics") != "lexical_attempt_key_then_action_id":
        raise ValueError("Retry-lineage ordering is invalid")
    attempts = value.get("attempts")
    if not isinstance(attempts, list) or len(attempts) > 64:
        raise ValueError("Retry-lineage attempt inventory is invalid")
    seen: list[str] = []
    has_conflict = False
    has_provider_identity = False
    for item in attempts:
        if not isinstance(item, dict) or set(item) != _ATTEMPT_KEYS:
            raise ValueError("Retry-lineage attempt fields are not exact")
        coordinates = _validate_coordinates(item["coordinates"])
        if coordinates["native_run_id"] != value["run_id"]:
            raise ValueError("Retry-lineage run identity does not join")
        expected_key = derive_retry_attempt_key(**coordinates)
        if item.get("attempt_key") != expected_key:
            raise ValueError("Retry-attempt key is invalid")
        seen.append(expected_key)
        members = item.get("actions")
        if not isinstance(members, list) or not members:
            raise ValueError("Retry-attempt action evidence is invalid")
        action_ids: list[str] = []
        for member in members:
            if not isinstance(member, dict) or set(member) != _ACTION_KEYS:
                raise ValueError("Retry-attempt action fields are not exact")
            if not _is_action_id(member["action_id"]):
                raise ValueError("Retry-attempt action identity is invalid")
            if not _is_sha(member["binding_sha256"]) or not _is_sha(member["request_sha256"]):
                raise ValueError("Retry-attempt binding evidence is invalid")
            if member["state"] not in ACTION_STATES:
                raise ValueError("Retry-attempt action state is invalid")
            if member["provider_mechanism"] not in MECHANISMS:
                raise ValueError("Retry-attempt provider mechanism is invalid")
            provider_id = member["provider_operation_id"]
            if provider_id is not None and (not isinstance(provider_id, str) or not provider_id):
                raise ValueError("Retry-attempt provider identity is invalid")
            if not isinstance(member["pass_attempt_pointer"], str) or not member["pass_attempt_pointer"]:
                raise ValueError("Retry-attempt pointer is invalid")
            action_ids.append(member["action_id"])
            has_provider_identity = has_provider_identity or provider_id is not None
        if action_ids != sorted(action_ids) or len(action_ids) != len(set(action_ids)):
            raise ValueError("Retry-attempt actions are not canonically ordered")
        reasons = item.get("reason_codes")
        if not isinstance(reasons, list) or reasons != sorted(set(reasons)) or any(
            reason not in CONFLICT_REASONS for reason in reasons
        ):
            raise ValueError("Retry-attempt conflict reasons are invalid")
        expected_reasons: set[str] = set()
        if len(members) > 1:
            expected_reasons.add("multiple_actions_for_attempt")
        if len({(member["binding_sha256"], member["request_sha256"]) for member in members}) > 1:
            expected_reasons.add("request_binding_conflict")
        if len({member["pass_attempt_pointer"] for member in members}) > 1:
            expected_reasons.add("pass_attempt_pointer_conflict")
        if len([
            member for member in members if member["state"] not in {
                "REPORTED", "DENIED_PROVIDERLESS", "BUDGET_EXHAUSTED",
                "SKIPPED_BUDGET_EXHAUSTED",
            }
        ]) > 1:
            expected_reasons.add("multiple_active_actions_for_attempt")
        if reasons != sorted(expected_reasons):
            raise ValueError("Retry-attempt conflict evidence is inconsistent")
        expected_resolution = "conflict" if reasons else "consistent"
        if item.get("resolution") != expected_resolution:
            raise ValueError("Retry-attempt resolution is inconsistent")
        selected = item.get("selected_action_id")
        if (expected_resolution == "consistent" and selected != action_ids[0]) or (
            expected_resolution == "conflict" and selected is not None
        ):
            raise ValueError("Retry-attempt selected action is inconsistent")
        has_conflict = has_conflict or expected_resolution == "conflict"
    if seen != sorted(seen) or len(seen) != len(set(seen)):
        raise ValueError("Retry attempts are not canonically ordered")
    if value.get("status") != ("conflict" if has_conflict else "consistent"):
        raise ValueError("Retry-lineage status is inconsistent")
    if value.get("conflict_classification") != (
        "retry_lineage_conflict_requires_review" if has_conflict else None
    ):
        raise ValueError("Retry-lineage conflict classification is inconsistent")
    if value.get("forward_dispatch_permitted") is not (not has_conflict):
        raise ValueError("Retry-lineage forward-dispatch assertion is inconsistent")
    if value.get("reconciliation_permitted") is not has_provider_identity:
        raise ValueError("Retry-lineage reconciliation assertion is inconsistent")
    body = {key: item for key, item in value.items() if key != "inventory_sha256"}
    if not _is_sha(value.get("inventory_sha256")) or value["inventory_sha256"] != _sha(body):
        raise ValueError("Retry-lineage inventory digest mismatch")
    return deepcopy(value)


def build_lifecycle_inspection_v08(
    inspection_v07: Mapping[str, Any], lineage: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind lineage safety evidence into a new closed lifecycle version."""
    prior = validate_lifecycle_inspection_v07(dict(inspection_v07))
    inventory = validate_retry_lineage_inventory(dict(lineage))
    if inventory["run_id"] != prior["run_id"]:
        raise ValueError("Retry lineage does not join lifecycle run")
    basis = deepcopy(prior["checkpoint_basis"])
    basis["retry_lineage_inventory"] = inventory
    basis_sha = _sha(basis)
    decision = deepcopy(prior["temporal_decision"])
    decision["checkpoint_basis_sha256"] = basis_sha
    decision["retry_lineage_inventory_sha256"] = inventory["inventory_sha256"]
    result = {
        "schema_version": LIFECYCLE_INSPECTION_SCHEMA_V0_8,
        "run_id": prior["run_id"], "checkpoint_basis_sha256": basis_sha,
        "checkpoint_basis": basis, "temporal_decision_sha256": _sha(decision),
        "temporal_decision": decision,
    }
    return validate_lifecycle_inspection_v08(result)


def validate_lifecycle_inspection_v08(value: Any) -> dict[str, Any]:
    top = {"schema_version", "run_id", "checkpoint_basis_sha256", "checkpoint_basis", "temporal_decision_sha256", "temporal_decision"}
    if not isinstance(value, dict) or set(value) != top:
        raise ValueError("Lifecycle v0.8 fields are not exact")
    if value.get("schema_version") != LIFECYCLE_INSPECTION_SCHEMA_V0_8:
        raise ValueError("Unsupported lifecycle v0.8 schema")
    basis = value.get("checkpoint_basis")
    decision = value.get("temporal_decision")
    if not isinstance(basis, dict) or not isinstance(decision, dict):
        raise ValueError("Lifecycle v0.8 bodies are invalid")
    lineage = validate_retry_lineage_inventory(basis.get("retry_lineage_inventory"))
    if lineage["run_id"] != value.get("run_id"):
        raise ValueError("Lifecycle v0.8 lineage run does not join")
    if value.get("checkpoint_basis_sha256") != _sha(basis):
        raise ValueError("Lifecycle v0.8 basis digest mismatch")
    if decision.get("checkpoint_basis_sha256") != value["checkpoint_basis_sha256"] or decision.get("retry_lineage_inventory_sha256") != lineage["inventory_sha256"] or value.get("temporal_decision_sha256") != _sha(decision):
        raise ValueError("Lifecycle v0.8 temporal decision does not join")
    prior_basis = {key: item for key, item in basis.items() if key != "retry_lineage_inventory"}
    prior_basis_sha = _sha(prior_basis)
    prior_decision = {key: item for key, item in decision.items() if key != "retry_lineage_inventory_sha256"}
    prior_decision["checkpoint_basis_sha256"] = prior_basis_sha
    prior = {
        "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.7",
        "run_id": value["run_id"], "checkpoint_basis_sha256": prior_basis_sha,
        "checkpoint_basis": prior_basis,
        "temporal_decision_sha256": _sha(prior_decision),
        "temporal_decision": prior_decision,
    }
    validate_lifecycle_inspection_v07(prior)
    _validate_lineage_against_checkpoint(lineage, basis)
    custody = basis["provider_custody"]
    custody_ids = custody["action_ids"]
    command = decision["selected_command"]
    due_ids = decision["due_action_ids"]
    if lineage["status"] == "conflict":
        if lineage["forward_dispatch_permitted"]:
            raise ValueError("Conflicted lineage permits forward dispatch")
        if custody_ids:
            if command != "provider_reconciliation_cycle" or not lineage["reconciliation_permitted"]:
                raise ValueError("Provider custody must select reconciliation despite lineage conflict")
            if any(action_id not in custody_ids for action_id in due_ids):
                raise ValueError("Due reconciliation subset does not join provider custody")
        elif command != "none" or decision["capacity_disposition"] != "retain_for_review" or due_ids:
            raise ValueError("Post-custody lineage conflict must retain for review")
    return deepcopy(value)


def _route_coordinates(route: str) -> tuple[str, int]:
    normalized = route
    if normalized.startswith("bounded_natal.v2:"):
        normalized = normalized[len("bounded_natal.v2:"):]
    if ":attempt-" not in normalized:
        raise ValueError("Retry action route lacks canonical attempt coordinates")
    pass_id, raw_attempt = normalized.rsplit(":attempt-", 1)
    if not pass_id or not raw_attempt.isdigit() or int(raw_attempt) < 1:
        raise ValueError("Retry action route coordinates are invalid")
    return pass_id, int(raw_attempt)


def _validate_lineage_against_checkpoint(
    lineage: Mapping[str, Any], basis: Mapping[str, Any],
) -> None:
    """Join every retry action to authoritative v0.7 inventory/custody facts."""
    native_route = basis["native_route"]["route_family"]
    checkpoint_actions = {
        item["action_id"]: item for item in basis["action_inventory"]["actions"]
    }
    retry_actions = {
        action_id: item for action_id, item in checkpoint_actions.items()
        if item["binding"]["stage"] == "creative_retry"
    }
    lineage_actions: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for attempt in lineage["attempts"]:
        coordinates = attempt["coordinates"]
        for member in attempt["actions"]:
            action_id = member["action_id"]
            if action_id in lineage_actions:
                raise ValueError("Retry-lineage action appears more than once")
            lineage_actions[action_id] = (coordinates, member)
    if set(lineage_actions) != set(retry_actions):
        raise ValueError("Retry lineage does not exactly cover checkpoint retry actions")
    custody_by_id = {
        item["action_id"]: item for item in basis["provider_custody"]["actions"]
    }
    for action_id, source in retry_actions.items():
        coordinates, member = lineage_actions[action_id]
        binding = source["binding"]
        pass_id, route_attempt = _route_coordinates(source["route"])
        mechanism = "batch" if binding["service_level"] == "batch" else "response"
        comparisons = {
            "route_family": coordinates["route_family"] == native_route,
            "stage": coordinates["stage"] == binding["stage"],
            "route_pass": coordinates["pass_id"] == pass_id,
            "inventory_pass": source["pass_id"] in {None, coordinates["pass_id"]},
            "route_attempt": coordinates["attempt_number"] == route_attempt,
            "state": member["state"] == source["state"],
            "request": member["request_sha256"] == binding["request_sha256"],
            "binding": member["binding_sha256"] == _sha(binding),
            "mechanism": member["provider_mechanism"] == mechanism,
            "provider": member["provider_operation_id"] == source["provider_operation_id"],
            "pointer": member["pass_attempt_pointer"] == (
                f"passes/{coordinates['pass_id']}/attempts/"
                f"{coordinates['attempt_number']}"
            ),
        }
        failed = sorted(name for name, matches in comparisons.items() if not matches)
        if failed:
            raise ValueError(
                "Retry lineage does not join checkpoint action evidence: "
                + ",".join(failed)
            )
        custody = custody_by_id.get(action_id)
        if custody is not None and (
            member["provider_operation_id"] != custody["provider_operation_id"]
            or member["provider_mechanism"] != custody["provider_operation_kind"]
        ):
            raise ValueError("Retry lineage does not join checkpoint custody evidence")


def read_retry_lineage_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "retry-lineage-contracts.v1.schema.json"
    ).read_text(encoding="utf-8"))


def read_lifecycle_inspection_v08_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "temporal-lifecycle-contracts.v3.schema.json"
    ).read_text(encoding="utf-8"))


def read_lifecycle_inspection_v08_fixture() -> dict[str, Any]:
    value = json.loads(files("astrowoof_natal_authoring.resources.fixtures.lifecycle").joinpath(
        "retry-lineage-mixed-custody.v0.8.json"
    ).read_text(encoding="utf-8"))
    return validate_lifecycle_inspection_v08(value)


def inspect_retry_lineage_lifecycle(
    run_dir: Any, *, observed_at: str,
    native_exclusive_access: str = "not_established",
) -> dict[str, Any]:
    """Return v0.8 with custody precedence and closed lineage review facts."""
    from pathlib import Path
    from .closure import load_json
    from .lifecycle import inspect_lifecycle
    from .post_fan_in_contracts import (
        _runtime_local_operations, build_lifecycle_inspection_v07,
        build_local_work_inventory,
    )

    root = Path(run_dir).resolve()
    state = load_json(root / "run.json")
    legacy = inspect_lifecycle(
        root, observed_at=observed_at,
        native_exclusive_access=native_exclusive_access,
    )
    lineage = retry_lineage_inventory_from_state(state)
    custody_ids = legacy["provider_custody"]["action_ids"]
    if lineage["status"] == "conflict" and not custody_ids:
        legacy = deepcopy(legacy)
        legacy["review_reasons"] = sorted({
            *legacy["review_reasons"],
            "retry_lineage_conflict_requires_review",
        })
        legacy["execution_capacity"].update({
            "disposition": "retain_for_review", "local_work_ready_now": False,
            "resume_not_before": None, "reason_code": "native_review_required",
        })
        legacy["execution_branch"] = {
            "command": "none", "eligible_now": False,
            "reason_code": "native_review_or_ambiguity",
            "action_ids": [], "not_before": None,
        }
        legacy["external_authority_request"] = None
        legacy["external_authority_refusal"] = None
    observation = legacy["observation"]
    operations = _runtime_local_operations(state, legacy)
    inventory = build_local_work_inventory(
        run_id=legacy["run_id"],
        state_revision=observation["operator_state_revision"],
        snapshot_sha256=observation["snapshot_sha256"],
        logical_workspace_root=observation["logical_workspace_root"],
        operations=operations,
        consumed_operation_keys=list(
            (state.get("local_work_progress") or {}).get(
                "consumed_operation_keys"
            ) or []
        ),
    )
    return build_lifecycle_inspection_v08(
        build_lifecycle_inspection_v07(legacy, inventory), lineage,
    )
