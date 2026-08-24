"""Strict checkpoint-basis and temporal-decision lifecycle contract."""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any
from importlib.resources import files
from pathlib import Path
from importlib.resources import files
from pathlib import Path

from .lifecycle_contracts import (
    CONSUMER_AUTHORITY_RETENTION_REASONS,
    CONSUMER_AUTHORITY_STATES,
    COST_DISPOSITIONS,
    PROVIDER_CUSTODY_CLASSIFICATIONS,
    PROVIDER_CUSTODY_STAGES,
    PROVIDER_CUSTODY_STATES,
    PROVIDER_OPERATION_KINDS,
    PROVIDER_ACTION_STATES,
    PROVIDER_ROUTE_FAMILIES,
    canonical_contract_json,
    validate_lifecycle_inspection_v05,
)


LIFECYCLE_INSPECTION_SCHEMA_V0_6 = (
    "astrowoof.authoring_lifecycle_inspection.v0.6"
)
EXTERNAL_AUTHORITY_REQUEST_SCHEMA_V2 = "astrowoof.external_authority_request.v2"
_TOP_KEYS = {
    "schema_version", "run_id", "checkpoint_basis_sha256",
    "checkpoint_basis", "temporal_decision_sha256", "temporal_decision",
}
_BASIS_KEYS = {
    "observation", "terminal", "quiescence", "local_dependencies",
    "action_inventory", "review_reasons", "provider_custody", "native_route",
    "consumer_authority", "checkpoint_safe_for_worker_release",
    "reconciliation_policy_version", "external_authority_state",
}
_DECISION_KEYS = {
    "observed_at", "checkpoint_basis_sha256", "capacity_disposition",
    "local_work_ready_now", "reason_code", "selected_command", "eligible_now",
    "due_action_ids", "not_before",
}
_OBSERVATION_KEYS = {
    "operator_state_revision", "snapshot_sha256", "logical_workspace_root",
    "snapshot_complete", "inventory_valid", "native_exclusive_access",
    "writer_race_possible",
}
_INVENTORY_KEYS = {"schema_version", "run_id", "ordering_semantics", "actions"}
_CUSTODY_KEYS = {
    "state", "provider_action_count", "reservation_retention_action_count",
    "action_ids", "earliest_resume_not_before", "actions",
}
_AUTHORITY_KEYS = {
    "kind", "request_kind", "ordered_action_ids", "refusal_reason",
    "evidence_categories",
}
_TERMINAL_KEYS = {
    "outcome", "terminal", "terminal_reason", "deck_bytes_exist",
    "native_qa_passed", "assembly_lint_validation_accepted",
    "delivery_package_complete", "delivery_publishable",
    "provider_continuation_remains", "local_continuation_remains",
}
_INVENTORY_ACTION_KEYS = {
    "action_id", "route", "pass_id", "attempt", "state", "binding",
    "necessary", "relationship", "providerless_denial_eligible",
    "eligibility_reason", "authorization_previously_recorded",
    "provider_operation_id", "provider_identity_present",
    "provider_evidence_present", "consumption_evidence_present",
    "blocking_action_ids", "ambiguity_review_reasons",
}
_BINDING_KEYS = {
    "run_id", "profile_sha256", "prepared_state_revision", "stage", "route",
    "request_sha256", "model", "service_level", "maximum_output_tokens",
    "commitment_micro_usd", "price_book_version",
}
_CUSTODY_ACTION_KEYS = {
    "action_id", "route_family", "stage", "service_level",
    "provider_operation_kind", "provider_operation_id", "native_operation_ref",
    "custody_classification", "resume_not_before", "reason_code",
}
_CONSUMER_KEYS = {"state", "action_count", "action_ids", "actions"}
_CONSUMER_ACTION_KEYS = {"action_id", "retention_reason", "cost_disposition"}
_TERMINAL_OUTCOMES = {
    "nonterminal", "delivery_complete", "policy_stopped", "review_required",
    "budget_exhausted", "ambiguous", "failed",
}
_TERMINAL_REASONS = {
    None, "delivery_complete", "native_policy_stop", "native_qa_failure",
    "budget_exhausted", "providerless_denial", "review_required",
    "ambiguous_provider_submission", "native_failure",
    "external_spend_authority_denied",
    "external_spend_reservation_unavailable", "external_product_policy_denied",
    "run_cancelled_before_submission",
}
_QUIESCENCE_REASONS = {
    "no_provider_or_local_continuation", "provider_continuation_remains",
    "local_continuation_remains", "snapshot_invalid", "writer_race_possible",
    "native_state_inconsistent",
}
_LOCAL_DEPENDENCY_KINDS = {
    "deterministic_qa", "local_assembly", "provider_submission_ambiguity",
    "provider_result_reconciliation", "retry_preparation", "polish",
    "critic_execution", "delivery_construction", "native_state_repair_review",
    "other_versioned_native_continuation",
}
_ROUTE_CONTRACTS = {
    "astrowoof.semantic_closure_run.v0.9",
    "astrowoof.bounded_natal.authoring_run.v1",
    "astrowoof.bounded_natal.authoring_run.v2",
}
_ACTION_ID_PATTERN = re.compile(r"^paid_[0-9a-f]{24}$")
_REQUEST_KINDS = {"ordinary_action_set", "initial_wave_admission"}


def canonical_utc_instant(value: str) -> str:
    """Normalize an aware whole-second instant to canonical UTC ``...Z``."""
    if not isinstance(value, str) or not value:
        raise ValueError("observed_at must be a nonempty timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("observed_at is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observed_at must include an offset")
    parsed = parsed.astimezone(timezone.utc)
    if parsed.microsecond:
        raise ValueError("observed_at must use whole-second precision")
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(value: Any) -> str:
    return hashlib.sha256(canonical_contract_json(value).encode("utf-8")).hexdigest()


def _without_observed_at(observation: dict[str, Any]) -> dict[str, Any]:
    projected = deepcopy(observation)
    projected.pop("observed_at", None)
    return projected


def _authority_state(value: dict[str, Any]) -> dict[str, Any]:
    request = value.get("external_authority_request")
    refusal = value.get("external_authority_refusal")
    if request is not None:
        return {
            "kind": "request",
            "request_kind": request["request_kind"],
            "ordered_action_ids": deepcopy(request["ordered_action_ids"]),
            "refusal_reason": None,
            "evidence_categories": [],
        }
    if refusal is not None:
        return {
            "kind": "refusal",
            "request_kind": None,
            "ordered_action_ids": [],
            "refusal_reason": refusal["reason_code"],
            "evidence_categories": deepcopy(refusal["evidence_categories"]),
        }
    return {
        "kind": "none", "request_kind": None, "ordered_action_ids": [],
        "refusal_reason": None, "evidence_categories": [],
    }


def build_lifecycle_inspection_v06(value: dict[str, Any]) -> dict[str, Any]:
    """Project one validated v0.5 inspection into the explicit v0.6 split."""
    validate_lifecycle_inspection_v05(value)
    inventory = deepcopy(value["action_inventory"])
    inventory.pop("observation", None)
    custody = deepcopy(value["provider_custody"])
    custody.pop("next_due_action_ids", None)
    capacity = value["execution_capacity"]
    branch = value["execution_branch"]
    basis = {
        "observation": _without_observed_at(value["observation"]),
        "terminal": deepcopy(value["terminal"]),
        "quiescence": deepcopy(value["quiescence"]),
        "local_dependencies": deepcopy(value["local_dependencies"]),
        "action_inventory": inventory,
        "review_reasons": deepcopy(value["review_reasons"]),
        "provider_custody": custody,
        "native_route": deepcopy(value["native_route"]),
        "consumer_authority": deepcopy(value["consumer_authority"]),
        "checkpoint_safe_for_worker_release": capacity[
            "checkpoint_safe_for_worker_release"
        ],
        "reconciliation_policy_version": capacity["policy_version"],
        "external_authority_state": _authority_state(value),
    }
    basis_sha256 = _sha256(basis)
    decision = {
        "observed_at": canonical_utc_instant(value["observation"]["observed_at"]),
        "checkpoint_basis_sha256": basis_sha256,
        "capacity_disposition": capacity["disposition"],
        "local_work_ready_now": capacity["local_work_ready_now"],
        "reason_code": branch["reason_code"],
        "selected_command": branch["command"],
        "eligible_now": branch["eligible_now"],
        "due_action_ids": (
            deepcopy(value["provider_custody"]["next_due_action_ids"])
            if branch["reason_code"] == "provider_reconciliation_due" else []
        ),
        "not_before": branch["not_before"],
    }
    result = {
        "schema_version": LIFECYCLE_INSPECTION_SCHEMA_V0_6,
        "run_id": value["run_id"],
        "checkpoint_basis_sha256": basis_sha256,
        "checkpoint_basis": basis,
        "temporal_decision_sha256": _sha256(decision),
        "temporal_decision": decision,
    }
    validate_lifecycle_inspection_v06(result)
    return result


def inspect_temporal_lifecycle(
    run_dir: Path | str,
    *,
    observed_at: str,
    native_exclusive_access: str = "not_established",
) -> dict[str, Any]:
    """Read one workspace and return strict v0.6 evidence without mutation."""
    canonical = canonical_utc_instant(observed_at)
    from .lifecycle import inspect_lifecycle

    legacy = inspect_lifecycle(
        Path(run_dir), native_exclusive_access=native_exclusive_access,
        observed_at=canonical,
    )
    return build_lifecycle_inspection_v06(legacy)


def read_temporal_lifecycle_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring").joinpath(
        "resources/contracts/temporal-lifecycle-contracts.v1.schema.json"
    )
    import json
    return json.loads(path.read_text(encoding="utf-8"))


def read_temporal_external_authority_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring").joinpath(
        "resources/contracts/temporal-external-authority-contracts.v2.schema.json"
    )
    import json
    return json.loads(path.read_text(encoding="utf-8"))


def _exact_dict(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} fields are not exact")
    return value


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str) and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_action_id(value: Any) -> bool:
    return isinstance(value, str) and _ACTION_ID_PATTERN.fullmatch(value) is not None


def _validate_binding(binding: Any, *, run_id: str, route: str) -> None:
    item = _exact_dict(binding, _BINDING_KEYS, "Checkpoint action binding")
    if (
        item["run_id"] != run_id or item["route"] != route
        or not _valid_sha256(item["profile_sha256"])
        or not _valid_sha256(item["request_sha256"])
        or not isinstance(item["prepared_state_revision"], int)
        or item["prepared_state_revision"] < 0
        or item["stage"] not in PROVIDER_CUSTODY_STAGES
        or item["service_level"] not in {"interactive", "batch"}
        or not isinstance(item["model"], str) or not item["model"]
        or not isinstance(item["maximum_output_tokens"], int)
        or item["maximum_output_tokens"] < 1
        or not isinstance(item["commitment_micro_usd"], int)
        or item["commitment_micro_usd"] < 0
        or not isinstance(item["price_book_version"], str)
        or not item["price_book_version"]
    ):
        raise ValueError("Checkpoint action binding is invalid")


def _validate_checkpoint_basis(value: dict[str, Any], *, run_id: str) -> None:
    """Close every projected basis child and its cross-object joins."""
    basis = _exact_dict(value, _BASIS_KEYS, "Lifecycle checkpoint basis")
    observation = _exact_dict(
        basis["observation"], _OBSERVATION_KEYS, "Checkpoint observation"
    )
    if (
        not isinstance(observation["operator_state_revision"], int)
        or observation["operator_state_revision"] < 0
        or not _valid_sha256(observation["snapshot_sha256"])
        or not isinstance(observation["logical_workspace_root"], str)
        or not observation["logical_workspace_root"]
        or not all(isinstance(observation[key], bool) for key in (
            "snapshot_complete", "inventory_valid", "writer_race_possible"
        ))
        or observation["native_exclusive_access"] not in {
            "established", "declared", "not_established", "unknown"
        }
    ):
        raise ValueError("Checkpoint observation is invalid")
    terminal = _exact_dict(basis["terminal"], _TERMINAL_KEYS, "Checkpoint terminal")
    boolean_terminal = _TERMINAL_KEYS - {"outcome", "terminal_reason"}
    if (
        not all(isinstance(terminal[key], bool) for key in boolean_terminal)
        or terminal["outcome"] not in _TERMINAL_OUTCOMES
        or terminal["terminal_reason"] not in _TERMINAL_REASONS
        or terminal["terminal"] != (terminal["outcome"] != "nonterminal")
        or (terminal["outcome"] == "nonterminal")
        != (terminal["terminal_reason"] is None)
    ):
        raise ValueError("Checkpoint terminal facts are invalid")
    quiescence = _exact_dict(
        basis["quiescence"], {"state", "reasons"}, "Checkpoint quiescence"
    )
    if (
        quiescence["state"] not in {
            "quiescent", "not_quiescent", "unknown_review_required"
        }
        or not isinstance(quiescence["reasons"], list)
        or len(quiescence["reasons"]) != len(set(quiescence["reasons"]))
        or not quiescence["reasons"]
        or any(item not in _QUIESCENCE_REASONS for item in quiescence["reasons"])
    ):
        raise ValueError("Checkpoint quiescence is invalid")
    dependencies = basis["local_dependencies"]
    if not isinstance(dependencies, list):
        raise ValueError("Checkpoint local dependencies are invalid")
    for dependency in dependencies:
        item = _exact_dict(
            dependency, {"kind", "blocking", "reason_code"},
            "Checkpoint local dependency",
        )
        if (
            item["kind"] not in _LOCAL_DEPENDENCY_KINDS
            or not isinstance(item["blocking"], bool)
            or not isinstance(item["reason_code"], str)
            or not item["reason_code"]
        ):
            raise ValueError("Checkpoint local dependency is invalid")
    review_reasons = basis["review_reasons"]
    if (
        not isinstance(review_reasons, list)
        or len(review_reasons) != len(set(review_reasons))
        or any(not isinstance(item, str) or not item for item in review_reasons)
    ):
        raise ValueError("Checkpoint review reasons are invalid")
    inventory = _exact_dict(
        basis["action_inventory"], _INVENTORY_KEYS, "Checkpoint action inventory"
    )
    if (
        inventory["schema_version"] != "astrowoof.provider_action_inventory.v0.1"
        or inventory["run_id"] != run_id
        or inventory["ordering_semantics"] != (
            "deterministic_presentation_only_not_execution_order"
        )
        or not isinstance(inventory["actions"], list)
    ):
        raise ValueError("Checkpoint action inventory is invalid")
    inventory_by_id: dict[str, dict[str, Any]] = {}
    for raw in inventory["actions"]:
        action = _exact_dict(raw, _INVENTORY_ACTION_KEYS, "Checkpoint action")
        action_id = action["action_id"]
        if not _valid_action_id(action_id) or action_id in inventory_by_id:
            raise ValueError("Checkpoint action identity is invalid")
        _validate_binding(action["binding"], run_id=run_id, route=action["route"])
        if (
            action["binding"]["stage"] not in PROVIDER_CUSTODY_STAGES
            or not isinstance(action["attempt"], int) or action["attempt"] < 1
            or action["state"] not in PROVIDER_ACTION_STATES
            # This is the closed v0.5 action-inventory vocabulary.  A resolved
            # provider action is normally ``independent``; treating it as an
            # invented ``nonblocking`` value made valid retained checkpoints
            # impossible to project through temporal v0.6 inspection.
            or action["relationship"] not in {
                "blocking", "independent", "superseded"
            }
            or not isinstance(action["route"], str) or not action["route"]
            or not all(isinstance(action[key], bool) for key in (
                "necessary", "providerless_denial_eligible",
                "authorization_previously_recorded", "provider_identity_present",
                "provider_evidence_present", "consumption_evidence_present",
            ))
            or action["provider_identity_present"]
            != (action["provider_operation_id"] is not None)
            or not isinstance(action["blocking_action_ids"], list)
            or any(
                not _valid_action_id(item) for item in action["blocking_action_ids"]
            )
            or not isinstance(action["ambiguity_review_reasons"], list)
        ):
            raise ValueError("Checkpoint action metadata is invalid")
        inventory_by_id[action_id] = action
    custody = _exact_dict(
        basis["provider_custody"], _CUSTODY_KEYS, "Checkpoint provider custody"
    )
    custody_ids = custody["action_ids"]
    custody_actions = custody["actions"]
    if (
        custody["state"] not in PROVIDER_CUSTODY_STATES
        or not isinstance(custody_ids, list)
        or len(custody_ids) != len(set(custody_ids))
        or any(not _valid_action_id(item) for item in custody_ids)
        or not isinstance(custody_actions, list)
        or custody["provider_action_count"] != len(custody_actions)
        or custody["reservation_retention_action_count"] != len(custody_actions)
        or custody_ids != [item.get("action_id") for item in custody_actions]
    ):
        raise ValueError("Checkpoint provider custody is invalid")
    for raw in custody_actions:
        action = _exact_dict(
            raw, _CUSTODY_ACTION_KEYS, "Checkpoint custody action"
        )
        source = inventory_by_id.get(action["action_id"])
        if (
            not _valid_action_id(action["action_id"])
            or source is None
            or action["route_family"] not in PROVIDER_ROUTE_FAMILIES
            or action["provider_operation_kind"] not in PROVIDER_OPERATION_KINDS
            or action["stage"] not in PROVIDER_CUSTODY_STAGES
            or action["custody_classification"]
            not in PROVIDER_CUSTODY_CLASSIFICATIONS
            or action["stage"] != source["binding"]["stage"]
            or action["service_level"] != source["binding"]["service_level"]
            or action["provider_operation_id"] != source["provider_operation_id"]
            or not isinstance(action["provider_operation_id"], str)
            or not action["provider_operation_id"]
            or not isinstance(action["native_operation_ref"], str)
            or not action["native_operation_ref"]
            or action["resume_not_before"] is not None
            and canonical_utc_instant(action["resume_not_before"])
            != action["resume_not_before"]
        ):
            raise ValueError("Checkpoint custody/action join is invalid")
    scheduled = [
        item["resume_not_before"] for item in custody_actions
        if item["resume_not_before"] is not None
    ]
    earliest = min(scheduled) if scheduled else None
    if custody["earliest_resume_not_before"] != earliest:
        raise ValueError("Checkpoint custody schedule is inconsistent")
    route = _exact_dict(
        basis["native_route"], {"route_family", "route_contract"},
        "Checkpoint native route",
    )
    if (
        route["route_family"] not in PROVIDER_ROUTE_FAMILIES
        or route["route_contract"] not in _ROUTE_CONTRACTS
        or any(item["route_family"] != route["route_family"] for item in custody_actions)
    ):
        raise ValueError("Checkpoint native route is invalid")
    consumer = _exact_dict(
        basis["consumer_authority"], _CONSUMER_KEYS,
        "Checkpoint consumer authority",
    )
    if (
        consumer["state"] not in CONSUMER_AUTHORITY_STATES
        or not isinstance(consumer["action_ids"], list)
        or any(not _valid_action_id(item) for item in consumer["action_ids"])
        or not isinstance(consumer["actions"], list)
        or consumer["action_count"] != len(consumer["actions"])
        or consumer["action_ids"]
        != [item.get("action_id") for item in consumer["actions"]]
    ):
        raise ValueError("Checkpoint consumer authority is invalid")
    if consumer["state"] != ("retain" if consumer["action_count"] else "none"):
        raise ValueError("Checkpoint consumer-authority state is inconsistent")
    for raw in consumer["actions"]:
        action = _exact_dict(
            raw, _CONSUMER_ACTION_KEYS, "Checkpoint consumer-authority action"
        )
        if (
            not _valid_action_id(action["action_id"])
            or action["action_id"] not in inventory_by_id
            or action["retention_reason"]
            not in CONSUMER_AUTHORITY_RETENTION_REASONS
            or action["cost_disposition"] not in COST_DISPOSITIONS
        ):
            raise ValueError("Checkpoint consumer-authority action is invalid")
    if not isinstance(basis["checkpoint_safe_for_worker_release"], bool):
        raise ValueError("Checkpoint release-safety fact is invalid")
    if basis["reconciliation_policy_version"] != (
        "astrowoof.provider_reconciliation_policy.v0.2"
    ):
        raise ValueError("Checkpoint reconciliation policy is invalid")


def validate_lifecycle_inspection_v06(value: dict[str, Any]) -> None:
    """Validate exact shape, digests, canonical time, joins, and due subset."""
    if not isinstance(value, dict) or set(value) != _TOP_KEYS:
        raise ValueError("Lifecycle v0.6 top-level fields are not exact")
    if value.get("schema_version") != LIFECYCLE_INSPECTION_SCHEMA_V0_6:
        raise ValueError("Unsupported lifecycle inspection schema")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Lifecycle run_id is invalid")
    if not _valid_sha256(value.get("checkpoint_basis_sha256")):
        raise ValueError("Lifecycle checkpoint-basis digest is invalid")
    if not _valid_sha256(value.get("temporal_decision_sha256")):
        raise ValueError("Lifecycle temporal-decision digest is invalid")
    basis = value.get("checkpoint_basis")
    decision = value.get("temporal_decision")
    if not isinstance(basis, dict) or set(basis) != _BASIS_KEYS:
        raise ValueError("Lifecycle checkpoint-basis fields are not exact")
    if not isinstance(decision, dict) or set(decision) != _DECISION_KEYS:
        raise ValueError("Lifecycle temporal-decision fields are not exact")
    _validate_checkpoint_basis(basis, run_id=value.get("run_id"))
    if value.get("checkpoint_basis_sha256") != _sha256(basis):
        raise ValueError("Lifecycle checkpoint-basis digest mismatch")
    if decision.get("checkpoint_basis_sha256") != value["checkpoint_basis_sha256"]:
        raise ValueError("Lifecycle temporal decision does not join its basis")
    if value.get("temporal_decision_sha256") != _sha256(decision):
        raise ValueError("Lifecycle temporal-decision digest mismatch")
    if canonical_utc_instant(decision.get("observed_at")) != decision["observed_at"]:
        raise ValueError("Lifecycle observed_at is not canonical UTC")
    if (
        decision.get("not_before") is not None
        and canonical_utc_instant(decision["not_before"]) != decision["not_before"]
    ):
        raise ValueError("Lifecycle not_before is not canonical UTC")
    observation = basis.get("observation")
    inventory = basis.get("action_inventory")
    custody = basis.get("provider_custody")
    if not isinstance(observation, dict) or set(observation) != _OBSERVATION_KEYS:
        raise ValueError("Checkpoint observation contains temporal input")
    if not isinstance(inventory, dict) or set(inventory) != _INVENTORY_KEYS:
        raise ValueError("Checkpoint action inventory contains temporal observation")
    if not isinstance(custody, dict) or set(custody) != _CUSTODY_KEYS:
        raise ValueError("Checkpoint custody contains temporal due subset")
    authority = basis.get("external_authority_state")
    if not isinstance(authority, dict) or set(authority) != _AUTHORITY_KEYS:
        raise ValueError("Checkpoint external-authority fields are not exact")
    if authority.get("kind") == "request":
        if (
            authority.get("request_kind") not in _REQUEST_KINDS
            or not authority.get("ordered_action_ids")
            or any(
                not _valid_action_id(item)
                for item in authority.get("ordered_action_ids", [])
            )
            or authority.get("refusal_reason") is not None
            or authority.get("evidence_categories")
        ):
            raise ValueError("Checkpoint external-authority request is invalid")
        if any(
            action_id not in {
                item["action_id"] for item in inventory["actions"]
            }
            for action_id in authority["ordered_action_ids"]
        ):
            raise ValueError("Checkpoint external-authority inventory does not join")
    elif authority.get("kind") == "refusal":
        if (
            authority.get("request_kind") is not None
            or authority.get("ordered_action_ids")
            or not authority.get("refusal_reason")
            or not authority.get("evidence_categories")
        ):
            raise ValueError("Checkpoint external-authority refusal is invalid")
    elif authority != {
        "kind": "none", "request_kind": None, "ordered_action_ids": [],
        "refusal_reason": None, "evidence_categories": [],
    }:
        raise ValueError("Checkpoint external-authority state is invalid")
    if value.get("run_id") != inventory.get("run_id"):
        raise ValueError("Lifecycle run identity does not join")
    due_ids = decision.get("due_action_ids")
    if not isinstance(due_ids, list) or len(due_ids) != len(set(due_ids)):
        raise ValueError("Lifecycle due-action subset is invalid")
    if any(not _valid_action_id(item) for item in due_ids):
        raise ValueError("Lifecycle due-action identity is invalid")
    action_ids = custody.get("action_ids") if isinstance(custody, dict) else None
    if not isinstance(action_ids, list) or any(item not in action_ids for item in due_ids):
        raise ValueError("Lifecycle due-action subset is outside custody")
    if len(due_ids) > 4:
        raise ValueError("Lifecycle due-action subset exceeds native bound")
    custody_actions = custody.get("actions") if isinstance(custody, dict) else None
    if not isinstance(custody_actions, list):
        raise ValueError("Lifecycle custody actions are invalid")
    observed = datetime.fromisoformat(
        decision["observed_at"].replace("Z", "+00:00")
    )
    expected_due = [
        item.get("action_id") for item in custody_actions
        if item.get("resume_not_before") is not None
        and datetime.fromisoformat(
            item["resume_not_before"].replace("Z", "+00:00")
        ) <= observed
    ][:4]
    if due_ids != expected_due:
        raise ValueError("Lifecycle due-action subset is not the native selection")
    if decision.get("reason_code") == "provider_reconciliation_due":
        if (
            not due_ids or decision.get("eligible_now") is not True
            or decision.get("selected_command") != "provider_reconciliation_cycle"
            or decision.get("not_before") is not None
        ):
            raise ValueError("Due reconciliation decision lacks eligible subset")
    elif decision.get("reason_code") == "provider_reconciliation_not_due":
        if (
            decision.get("eligible_now") is not False
            or decision.get("selected_command") != "provider_reconciliation_cycle"
            or decision.get("not_before") is None
        ):
            raise ValueError("Not-due reconciliation decision is invalid")
    elif due_ids:
        raise ValueError("Non-due temporal decision contains due actions")


def temporal_transition_errors(
    prior: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    """Return closed reasons for an invalid same-basis temporal transition."""
    validate_lifecycle_inspection_v06(prior)
    validate_lifecycle_inspection_v06(current)
    errors: list[str] = []
    if prior["checkpoint_basis_sha256"] != current["checkpoint_basis_sha256"]:
        return ["checkpoint_basis_changed"]
    left = prior["temporal_decision"]
    right = current["temporal_decision"]
    left_time = datetime.fromisoformat(left["observed_at"].replace("Z", "+00:00"))
    right_time = datetime.fromisoformat(right["observed_at"].replace("Z", "+00:00"))
    if right_time < left_time:
        errors.append("clock_regression")
    if right_time == left_time and left != right:
        errors.append("same_time_changed_decision")
    if left.get("eligible_now") is True and right.get("eligible_now") is False:
        errors.append("eligibility_regression")
    if (
        left.get("reason_code") == "provider_reconciliation_due"
        and right.get("reason_code") == "provider_reconciliation_not_due"
    ):
        errors.append("due_to_not_due")
    return sorted(set(errors))


def validate_temporal_transition(
    prior: dict[str, Any], current: dict[str, Any]
) -> None:
    errors = temporal_transition_errors(prior, current)
    if errors:
        raise ValueError("Invalid lifecycle temporal transition: " + ", ".join(errors))


def build_external_authority_request_v2(value: dict[str, Any]) -> dict[str, Any]:
    """Build stable authority identity from basis and exact ordered inventory."""
    validate_lifecycle_inspection_v06(value)
    authority = value["checkpoint_basis"]["external_authority_state"]
    if authority["kind"] != "request":
        raise ValueError("Lifecycle checkpoint has no external-authority request")
    request = {
        "schema_version": EXTERNAL_AUTHORITY_REQUEST_SCHEMA_V2,
        "run_id": value["run_id"],
        "checkpoint_basis_sha256": value["checkpoint_basis_sha256"],
        "request_kind": authority["request_kind"],
        "ordered_action_ids": deepcopy(authority["ordered_action_ids"]),
    }
    request["external_authority_request_sha256"] = _sha256(request)
    validate_external_authority_request_v2(request)
    return request


def validate_external_authority_request_v2(value: dict[str, Any]) -> None:
    keys = {
        "schema_version", "external_authority_request_sha256", "run_id",
        "checkpoint_basis_sha256", "request_kind", "ordered_action_ids",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("External-authority request v2 fields are not exact")
    if value.get("schema_version") != EXTERNAL_AUTHORITY_REQUEST_SCHEMA_V2:
        raise ValueError("Unsupported external-authority request schema")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("External-authority request run_id is invalid")
    if not _valid_sha256(value.get("checkpoint_basis_sha256")):
        raise ValueError("External-authority checkpoint digest is invalid")
    if not _valid_sha256(value.get("external_authority_request_sha256")):
        raise ValueError("External-authority request digest is invalid")
    if value.get("request_kind") not in _REQUEST_KINDS:
        raise ValueError("External-authority request kind is invalid")
    ids = value.get("ordered_action_ids")
    if (
        not isinstance(ids, list) or not 1 <= len(ids) <= 32
        or len(ids) != len(set(ids))
        or any(not _valid_action_id(item) for item in ids)
    ):
        raise ValueError("External-authority request action inventory is invalid")
    body = {
        key: item for key, item in value.items()
        if key != "external_authority_request_sha256"
    }
    if value.get("external_authority_request_sha256") != _sha256(body):
        raise ValueError("External-authority request digest mismatch")


def validate_external_authority_request_v2_against_inspection(
    request: dict[str, Any], inspection: dict[str, Any]
) -> None:
    """Join a reference request to one strict basis and all member bindings."""
    validate_external_authority_request_v2(request)
    validate_lifecycle_inspection_v06(inspection)
    authority = inspection["checkpoint_basis"]["external_authority_state"]
    errors: list[str] = []
    if request["run_id"] != inspection["run_id"]:
        errors.append("run_id")
    if request["checkpoint_basis_sha256"] != inspection["checkpoint_basis_sha256"]:
        errors.append("checkpoint_basis_sha256")
    if authority["kind"] != "request":
        errors.append("authority_kind")
    if request["request_kind"] != authority.get("request_kind"):
        errors.append("request_kind")
    if request["ordered_action_ids"] != authority.get("ordered_action_ids"):
        errors.append("ordered_action_ids")
    inventory = inspection["checkpoint_basis"]["action_inventory"]["actions"]
    by_id = {item["action_id"]: item for item in inventory}
    for action_id in request["ordered_action_ids"]:
        action = by_id.get(action_id)
        if action is None:
            errors.append(f"binding_missing:{action_id}")
            continue
        try:
            _validate_binding(
                action["binding"], run_id=inspection["run_id"],
                route=action["route"],
            )
        except ValueError:
            errors.append(f"binding_invalid:{action_id}")
    if errors:
        raise ValueError(
            "External-authority request does not join inspection: "
            + ", ".join(sorted(set(errors)))
        )
