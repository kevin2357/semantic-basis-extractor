"""Closed post-fan-in local-work and lifecycle v0.7 contracts."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.resources import files
import json
import logging
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence

from .temporal_lifecycle import (
    build_lifecycle_inspection_v06,
    validate_lifecycle_inspection_v06,
)


LOCAL_WORK_INVENTORY_SCHEMA = "astrowoof.local_work_inventory.v1"
LIFECYCLE_INSPECTION_SCHEMA_V0_7 = "astrowoof.authoring_lifecycle_inspection.v0.7"

LOCAL_OPERATION_KINDS = frozenset({
    "provider_result_fan_in_and_retry_evaluation",
    "final_assembly_and_qa",
    "delivery_construction",
})
LOCAL_OPERATION_REASONS = frozenset({
    "provider_evidence_ingestion_required",
    "final_assembly_required",
    "delivery_not_constructed",
})
ROUTE_FAMILIES = frozenset({"exact_natal", "bounded_natal"})
PAID_STAGES = frozenset({
    "authoring_initial", "creative_retry", "polish",
    "qualitative_critic", "qualitative_candidate",
})

logger = logging.getLogger(__name__)


class LocalWorkProgressContradiction(ValueError):
    """Advertised local work survived the command's purported consumption."""

    def __init__(self, message: str, *, sealed: dict[str, Any] | None = None):
        super().__init__(message)
        self.sealed = sealed

_INVENTORY_KEYS = frozenset({
    "schema_version", "run_id", "state_revision", "snapshot_sha256",
    "logical_workspace_root", "ordering_semantics", "operations",
    "consumed_operation_keys", "inventory_sha256",
})
_OPERATION_KEYS = frozenset({
    "operation_id", "operation_key", "kind", "route_family", "stage",
    "source_action_ids", "reason_code", "basis_state_revision",
    "basis_snapshot_sha256",
})


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _require_sha(value: Any, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"{field} must be lowercase SHA-256")


def build_local_work_inventory(
    *, run_id: str, state_revision: int, snapshot_sha256: str,
    logical_workspace_root: str, operations: Sequence[Mapping[str, Any]],
    consumed_operation_keys: Sequence[str] = (),
) -> dict[str, Any]:
    """Build one snapshot-bound SBE-selected local-work inventory."""
    prepared = []
    for original in operations:
        semantic = {
            "kind": original["kind"],
            "route_family": original["route_family"],
            "stage": original.get("stage"),
            "source_action_ids": list(original.get("source_action_ids") or []),
            "reason_code": original["reason_code"],
        }
        member = {
            **semantic,
            "operation_key": "work_" + _sha(semantic)[:24],
            "basis_state_revision": state_revision,
            "basis_snapshot_sha256": snapshot_sha256,
        }
        member["operation_id"] = "local_" + _sha(member)[:24]
        prepared.append(member)
    body = {
        "schema_version": LOCAL_WORK_INVENTORY_SCHEMA,
        "run_id": run_id,
        "state_revision": state_revision,
        "snapshot_sha256": snapshot_sha256,
        "logical_workspace_root": logical_workspace_root,
        "ordering_semantics": "sbe_selected_execution_order",
        "operations": prepared,
        "consumed_operation_keys": list(consumed_operation_keys),
    }
    body["inventory_sha256"] = _sha(body)
    return validate_local_work_inventory(body)


def validate_local_work_inventory(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _INVENTORY_KEYS:
        raise ValueError("Local-work inventory fields are not exact")
    if value.get("schema_version") != LOCAL_WORK_INVENTORY_SCHEMA:
        raise ValueError("Unsupported local-work inventory schema")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Local-work run_id is invalid")
    revision = value.get("state_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise ValueError("Local-work state_revision is invalid")
    _require_sha(value.get("snapshot_sha256"), "snapshot_sha256")
    if not isinstance(value.get("logical_workspace_root"), str) or not value[
        "logical_workspace_root"
    ]:
        raise ValueError("Local-work logical root is invalid")
    if value.get("ordering_semantics") != "sbe_selected_execution_order":
        raise ValueError("Local-work ordering semantics are invalid")
    operations = value.get("operations")
    if not isinstance(operations, list) or len(operations) > 32:
        raise ValueError("Local-work operation inventory is invalid")
    consumed = value.get("consumed_operation_keys")
    if (
        not isinstance(consumed, list) or len(consumed) > 32
        or len(consumed) != len(set(consumed))
        or any(
            not isinstance(item, str)
            or re.fullmatch(r"work_[0-9a-f]{24}", item) is None
            for item in consumed
        )
    ):
        raise ValueError("Consumed local-work identity inventory is invalid")
    operation_ids: list[str] = []
    operation_keys: list[str] = []
    for member in operations:
        if not isinstance(member, dict) or set(member) != _OPERATION_KEYS:
            raise ValueError("Local-work operation fields are not exact")
        if member.get("kind") not in LOCAL_OPERATION_KINDS:
            raise ValueError("Local-work operation kind is invalid")
        if member.get("route_family") not in ROUTE_FAMILIES:
            raise ValueError("Local-work route family is invalid")
        stage = member.get("stage")
        if stage is not None and stage not in PAID_STAGES:
            raise ValueError("Local-work stage is invalid")
        if member.get("reason_code") not in LOCAL_OPERATION_REASONS:
            raise ValueError("Local-work reason is invalid")
        action_ids = member.get("source_action_ids")
        if (
            not isinstance(action_ids, list) or not action_ids
            or len(action_ids) > 32 or len(action_ids) != len(set(action_ids))
            or any(
                not isinstance(item, str)
                or re.fullmatch(r"paid_[0-9a-f]{24}", item) is None
                for item in action_ids
            )
        ):
            raise ValueError("Local-work source action inventory is invalid")
        semantic = {
            key: member[key]
            for key in (
                "kind", "route_family", "stage", "source_action_ids", "reason_code"
            )
        }
        expected_key = "work_" + _sha(semantic)[:24]
        if member.get("operation_key") != expected_key:
            raise ValueError("Local-work semantic operation identity is invalid")
        if (
            member.get("basis_state_revision") != revision
            or member.get("basis_snapshot_sha256") != value["snapshot_sha256"]
        ):
            raise ValueError("Local-work member basis does not join its inventory")
        expected_id = "local_" + _sha({
            key: item for key, item in member.items() if key != "operation_id"
        })[:24]
        if member.get("operation_id") != expected_id:
            raise ValueError("Local-work operation identity is invalid")
        operation_ids.append(expected_id)
        operation_keys.append(expected_key)
    if len(operation_ids) != len(set(operation_ids)):
        raise ValueError("Local-work operation identities are duplicated")
    if len(operation_keys) != len(set(operation_keys)):
        raise ValueError("Local-work semantic operation identities are duplicated")
    if set(operation_keys) & set(consumed):
        raise ValueError("Consumed semantic local work cannot be advertised again")
    body = {key: item for key, item in value.items() if key != "inventory_sha256"}
    if value.get("inventory_sha256") != _sha(body):
        raise ValueError("Local-work inventory digest mismatch")
    return deepcopy(value)


def validate_local_work_inventory_against_v05(
    inventory: Mapping[str, Any], inspection: Mapping[str, Any],
) -> None:
    validate_local_work_inventory(dict(inventory))
    observation = inspection.get("observation") or {}
    if (
        inventory.get("run_id") != inspection.get("run_id")
        or inventory.get("state_revision") != observation.get("operator_state_revision")
        or inventory.get("snapshot_sha256") != observation.get("snapshot_sha256")
        or inventory.get("logical_workspace_root") != observation.get("logical_workspace_root")
    ):
        raise ValueError("Local-work inventory does not join lifecycle inspection")


def _runtime_local_operations(
    state: Mapping[str, Any], inspection_v05: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Derive only presently executable local work from validated native facts."""
    branch = inspection_v05.get("execution_branch") or {}
    if branch.get("command") != "ordinary_resume" or not branch.get("eligible_now"):
        return []
    actions = list((state.get("spend_ledger") or {}).get("actions") or [])
    completed = [
        action for action in actions
        if action.get("state") in {"PROVIDER_ID_RECORDED", "WAITING"}
        and (action.get("provider") or {}).get("id")
        and (action.get("provider_reconciliation") or {}).get("last_outcome")
        == "completed"
    ]
    route_family = (inspection_v05.get("native_route") or {}).get(
        "route_family", "exact_natal"
    )
    operations: list[dict[str, Any]] = []
    if completed:
        stages = sorted({
            str((action.get("binding") or {}).get("stage") or "")
            for action in completed
        })
        operations.append({
            "kind": "provider_result_fan_in_and_retry_evaluation",
            "route_family": route_family,
            "stage": stages[0] if len(stages) == 1 and stages[0] else None,
            "source_action_ids": sorted(
                str(action.get("action_id") or "") for action in completed
            ),
            "reason_code": "provider_evidence_ingestion_required",
        })
        return operations
    dependencies = inspection_v05.get("local_dependencies") or []
    reason_codes = {item.get("reason_code") for item in dependencies}
    terminal_actions = sorted(
        str(action.get("action_id") or "") for action in actions
        if action.get("state") in {
            "REPORTED", "DENIED_PROVIDERLESS", "SKIPPED_BUDGET_EXHAUSTED",
        }
    )
    if not terminal_actions:
        return []
    if "final_assembly_required" in reason_codes:
        operations.append({
            "kind": "final_assembly_and_qa", "route_family": route_family,
            "stage": None, "source_action_ids": terminal_actions,
            "reason_code": "final_assembly_required",
        })
    elif "delivery_not_constructed" in reason_codes:
        operations.append({
            "kind": "delivery_construction", "route_family": route_family,
            "stage": None, "source_action_ids": terminal_actions,
            "reason_code": "delivery_not_constructed",
        })
    return operations


def inspect_post_fan_in_lifecycle(
    run_dir: Path | str, *, observed_at: str,
    native_exclusive_access: str = "not_established",
    event_emitter: Any | None = None,
) -> dict[str, Any]:
    """Return strict v0.7 lifecycle evidence derived from one native workspace."""
    from .closure import load_json
    from .lifecycle import inspect_lifecycle

    root = Path(run_dir).resolve()
    state = load_json(root / "run.json")
    legacy = inspect_lifecycle(
        root, observed_at=observed_at,
        native_exclusive_access=native_exclusive_access,
    )
    actions = list((state.get("spend_ledger") or {}).get("actions") or [])
    authorized_providerless = [
        action for action in actions
        if action.get("state") == "AUTHORIZED"
        and not (action.get("provider") or {}).get("id")
    ]
    if authorized_providerless:
        # Native authorization without a durable call-entry/provider identity is
        # fenced state. It is neither fresh external authority nor generic local
        # work; only its exact constrained executor may advance it.
        legacy = deepcopy(legacy)
        legacy["review_reasons"] = sorted({
            *legacy["review_reasons"],
            "authorized_providerless_action_requires_constrained_dispatch",
        })
        legacy["execution_capacity"].update({
            "disposition": "retain_for_review",
            "local_work_ready_now": False,
            "resume_not_before": None,
            "reason_code": "native_review_required",
        })
        legacy["execution_branch"] = {
            "command": "none", "eligible_now": False,
            "reason_code": "native_review_or_ambiguity",
            "action_ids": [], "not_before": None,
        }
    observation = legacy["observation"]
    consumed = list(
        (state.get("local_work_progress") or {}).get("consumed_operation_keys")
        or []
    )
    operations = _runtime_local_operations(state, legacy)
    if (
        (legacy.get("execution_branch") or {}).get("command") == "ordinary_resume"
        and not operations
    ):
        # v0.7 never repeats the released status-only fallback when no concrete
        # executable operation can be constructed from native evidence.
        legacy = deepcopy(legacy)
        if (legacy.get("terminal") or {}).get("terminal"):
            legacy["execution_capacity"].update({
                "disposition": "terminal", "local_work_ready_now": False,
                "resume_not_before": None, "reason_code": "terminal_native_outcome",
            })
            reason = "terminal_or_no_continuation"
        else:
            legacy["review_reasons"] = sorted({
                *legacy["review_reasons"], "local_work_inventory_empty",
            })
            legacy["execution_capacity"].update({
                "disposition": "retain_for_review", "local_work_ready_now": False,
                "resume_not_before": None, "reason_code": "native_review_required",
            })
            reason = "native_review_or_ambiguity"
        legacy["execution_branch"] = {
            "command": "none", "eligible_now": False, "reason_code": reason,
            "action_ids": [], "not_before": None,
        }
    inventory = build_local_work_inventory(
        run_id=legacy["run_id"],
        state_revision=observation["operator_state_revision"],
        snapshot_sha256=observation["snapshot_sha256"],
        logical_workspace_root=observation["logical_workspace_root"],
        operations=operations,
        consumed_operation_keys=consumed,
    )
    result = build_lifecycle_inspection_v07(legacy, inventory)
    if event_emitter is not None:
        try:
            event_emitter.emit(
                "lifecycle.local_work_selected",
                data={
                    "selected_command": result["temporal_decision"][
                        "selected_command"
                    ],
                    "operation_count": len(operations),
                    "inventory_sha256": inventory["inventory_sha256"],
                },
                correlation={"native_run_id": result["run_id"]},
            )
        except Exception:
            logger.warning("local_work_inventory_event_failed", exc_info=True)
    return result


def commit_local_work_progress(
    run_dir: Path | str, *, prior: Mapping[str, Any], observed_at: str,
    event_emitter: Any | None = None,
    contradiction_publisher: Callable[[], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Seal consumed semantic work after the command changed native truth."""
    from .closure import load_json, save_state, validate_workspace_snapshot
    from .lifecycle import _exclusive_lifecycle_lock

    validate_lifecycle_inspection_v07(dict(prior))
    old_inventory = prior["checkpoint_basis"]["local_work_inventory"]
    old_keys = [item["operation_key"] for item in old_inventory["operations"]]
    root = Path(run_dir).resolve()
    with _exclusive_lifecycle_lock(root):
        state = load_json(root / "run.json")
        validate_workspace_snapshot(root, state)
        history = list(
            (state.get("local_work_progress") or {}).get(
                "consumed_operation_keys"
            ) or []
        )
        if set(old_keys) & set(history):
            logger.warning(
                "local_work_progress_refused reason=operation_already_consumed "
                "operation_count=%s", len(old_keys),
            )
            raise ValueError("ordinary_resume operation was already consumed")
        current = inspect_post_fan_in_lifecycle(
            root, observed_at=observed_at, native_exclusive_access="declared",
        )
        current_inventory = current["checkpoint_basis"]["local_work_inventory"]
        current_keys = {
            item["operation_key"] for item in current_inventory["operations"]
        }
        if (
            current["checkpoint_basis_sha256"]
            == prior["checkpoint_basis_sha256"]
            or set(old_keys) & current_keys
        ):
            logger.warning(
                "local_work_progress_refused reason=semantic_work_not_consumed "
                "operation_count=%s", len(old_keys),
            )
            sealed = (
                contradiction_publisher()
                if contradiction_publisher is not None else None
            )
            raise LocalWorkProgressContradiction(
                "ordinary_resume did not consume advertised local work",
                sealed=sealed,
            )
        for operation_key in old_keys:
            if operation_key not in history:
                history.append(operation_key)
        state["local_work_progress"] = {
            "schema_version": "astrowoof.local_work_progress.v1",
            "consumed_operation_keys": history,
        }
        save_state(root / "run.json", state)
        successor = inspect_post_fan_in_lifecycle(
            root, observed_at=observed_at, native_exclusive_access="declared",
        )
        validate_local_work_progress(prior, successor)
        if event_emitter is not None:
            try:
                event_emitter.emit(
                    "lifecycle.local_work_consumed",
                    data={
                        "consumed_count": len(old_keys),
                        "cumulative_consumed_count": len(history),
                        "successor_command": successor["temporal_decision"][
                            "selected_command"
                        ],
                    },
                    correlation={"native_run_id": successor["run_id"]},
                )
            except Exception:
                logger.warning("local_work_consumption_event_failed", exc_info=True)
        return successor


def build_lifecycle_inspection_v07(
    inspection_v05: Mapping[str, Any], inventory: Mapping[str, Any],
) -> dict[str, Any]:
    """Project released lifecycle v0.6 plus immutable local-work truth as v0.7."""
    validate_local_work_inventory_against_v05(inventory, inspection_v05)
    prior = build_lifecycle_inspection_v06(dict(inspection_v05))
    basis = deepcopy(prior["checkpoint_basis"])
    basis["local_work_inventory"] = deepcopy(dict(inventory))
    basis_sha = _sha(basis)
    decision = deepcopy(prior["temporal_decision"])
    decision["checkpoint_basis_sha256"] = basis_sha
    decision["local_work_inventory_sha256"] = inventory["inventory_sha256"]
    result = {
        "schema_version": LIFECYCLE_INSPECTION_SCHEMA_V0_7,
        "run_id": prior["run_id"],
        "checkpoint_basis_sha256": basis_sha,
        "checkpoint_basis": basis,
        "temporal_decision_sha256": _sha(decision),
        "temporal_decision": decision,
    }
    return validate_lifecycle_inspection_v07(result)


def validate_lifecycle_inspection_v07(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "run_id", "checkpoint_basis_sha256",
        "checkpoint_basis", "temporal_decision_sha256", "temporal_decision",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Lifecycle v0.7 fields are not exact")
    if value.get("schema_version") != LIFECYCLE_INSPECTION_SCHEMA_V0_7:
        raise ValueError("Unsupported lifecycle v0.7 schema")
    basis = value.get("checkpoint_basis")
    if not isinstance(basis, dict) or "local_work_inventory" not in basis:
        raise ValueError("Lifecycle v0.7 lacks local-work inventory")
    inventory = validate_local_work_inventory(basis["local_work_inventory"])
    if value.get("checkpoint_basis_sha256") != _sha(basis):
        raise ValueError("Lifecycle v0.7 basis digest mismatch")
    decision = value.get("temporal_decision")
    if not isinstance(decision, dict) or set(decision) != {
        "observed_at", "checkpoint_basis_sha256", "capacity_disposition",
        "local_work_ready_now", "reason_code", "selected_command",
        "eligible_now", "due_action_ids", "not_before",
        "local_work_inventory_sha256",
    }:
        raise ValueError("Lifecycle v0.7 temporal decision fields are not exact")
    if (
        decision.get("checkpoint_basis_sha256") != value["checkpoint_basis_sha256"]
        or decision.get("local_work_inventory_sha256") != inventory["inventory_sha256"]
        or value.get("temporal_decision_sha256") != _sha(decision)
    ):
        raise ValueError("Lifecycle v0.7 temporal decision does not join")
    command = decision.get("selected_command")
    operations = inventory["operations"]
    if command == "ordinary_resume":
        if not operations or decision.get("local_work_ready_now") is not True:
            raise ValueError("ordinary_resume lacks concrete local work")
    elif operations:
        raise ValueError("Non-local lifecycle branch carries local work")
    # Reconstruct and strictly validate the released v0.6 projection.
    prior_basis = {
        key: item for key, item in basis.items() if key != "local_work_inventory"
    }
    prior_basis_sha = _sha(prior_basis)
    prior_decision = {
        key: item for key, item in decision.items()
        if key != "local_work_inventory_sha256"
    }
    prior_decision["checkpoint_basis_sha256"] = prior_basis_sha
    prior = {
        "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.6",
        "run_id": value["run_id"],
        "checkpoint_basis_sha256": prior_basis_sha,
        "checkpoint_basis": prior_basis,
        "temporal_decision_sha256": _sha(prior_decision),
        "temporal_decision": prior_decision,
    }
    validate_lifecycle_inspection_v06(prior)
    observation = basis.get("observation") or {}
    if (
        inventory["run_id"] != value["run_id"]
        or inventory["state_revision"] != observation.get("operator_state_revision")
        or inventory["snapshot_sha256"] != observation.get("snapshot_sha256")
        or inventory["logical_workspace_root"] != observation.get("logical_workspace_root")
    ):
        raise ValueError("Lifecycle v0.7 inventory basis does not join")
    return deepcopy(value)


def validate_local_work_progress(
    prior: Mapping[str, Any], successor: Mapping[str, Any],
) -> None:
    """Reject replay of an advertised local operation after ordinary resume."""
    validate_lifecycle_inspection_v07(dict(prior))
    validate_lifecycle_inspection_v07(dict(successor))
    if prior["run_id"] != successor["run_id"]:
        raise ValueError("Lifecycle progress run identity changed")
    decision = prior["temporal_decision"]
    if decision["selected_command"] != "ordinary_resume" or not decision["eligible_now"]:
        raise ValueError("Prior lifecycle decision did not advertise ordinary resume")
    if prior["checkpoint_basis_sha256"] == successor["checkpoint_basis_sha256"]:
        raise ValueError("ordinary_resume did not advance its checkpoint basis")
    old_keys = {
        item["operation_key"]
        for item in prior["checkpoint_basis"]["local_work_inventory"]["operations"]
    }
    successor_inventory = successor["checkpoint_basis"]["local_work_inventory"]
    new_keys = {
        item["operation_key"]
        for item in successor_inventory["operations"]
    }
    if old_keys & new_keys:
        raise ValueError("ordinary_resume replayed a prior semantic local-work operation")
    prior_consumed = set(
        prior["checkpoint_basis"]["local_work_inventory"]["consumed_operation_keys"]
    )
    successor_consumed = set(successor_inventory["consumed_operation_keys"])
    if not prior_consumed <= successor_consumed:
        raise ValueError("Local-work consumption history is not append-only")
    successor_command = successor["temporal_decision"]["selected_command"]
    if successor_command == "ordinary_resume" and not (
        old_keys & successor_consumed
    ):
        raise ValueError("ordinary_resume successor lacks semantic consumption evidence")


def read_local_work_inventory_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "local-work-inventory.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def read_lifecycle_inspection_v07_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "temporal-lifecycle-contracts.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))
