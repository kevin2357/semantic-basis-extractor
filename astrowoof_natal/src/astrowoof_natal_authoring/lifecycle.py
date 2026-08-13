"""Read-only lifecycle inspection for semantic-closure workspaces."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .closure import (
    FINAL_SUCCESS_STATES,
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    validate_workspace_snapshot,
)
from .lifecycle_contracts import (
    LIFECYCLE_INSPECTION_SCHEMA,
    OUTSTANDING_ACTION_INVENTORY_SCHEMA,
    action_presentation_key,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _observation(
    run_dir: Path,
    state: dict[str, Any],
    *,
    native_exclusive_access: str,
    observed_at: str,
) -> tuple[dict[str, Any], list[str]]:
    manifest_path = run_dir / SNAPSHOT_NAME
    snapshot_sha256 = _file_sha256(manifest_path) if manifest_path.is_file() else "0" * 64
    valid = True
    reasons: list[str] = []
    try:
        validate_workspace_snapshot(run_dir, state)
    except (OSError, ValueError, TypeError, KeyError):
        valid = False
        reasons.append("snapshot_incomplete_or_invalid")
    race_possible = native_exclusive_access not in {"established", "declared"}
    if race_possible:
        reasons.append("writer_race_possible")
    contract = state.get("workspace_contract") or {}
    return {
        "operator_state_revision": int(state.get("state_revision") or 0),
        "snapshot_sha256": snapshot_sha256,
        "logical_workspace_root": str(
            contract.get("logical_root") or normalized_path(run_dir)
        ),
        "snapshot_complete": valid,
        "inventory_valid": valid,
        "observed_at": observed_at,
        "native_exclusive_access": native_exclusive_access,
        "writer_race_possible": race_possible,
    }, reasons


def _eligibility(action: dict[str, Any], *, snapshot_valid: bool) -> tuple[bool, str]:
    state = str(action.get("state"))
    if not snapshot_valid:
        return False, "native_state_inconsistent"
    if state == "DENIED_PROVIDERLESS":
        return False, "already_denied_providerless"
    if action.get("consumption"):
        return False, "consumption_evidence_present"
    if action.get("provider"):
        return False, "provider_identity_present"
    if action.get("reported"):
        return False, "provider_evidence_present"
    if state == "SUBMITTING" or state == "AMBIGUOUS_PROVIDER_SUBMISSION":
        return False, "submission_ambiguous"
    if state == "PREPARED":
        return True, "eligible_prepared"
    if state == "AUTHORIZED":
        return True, "eligible_authorized_unconsumed"
    return False, "state_not_providerless"


def _action_record(action: dict[str, Any], *, snapshot_valid: bool) -> dict[str, Any]:
    provider = action.get("provider") or {}
    eligible, reason = _eligibility(action, snapshot_valid=snapshot_valid)
    state = str(action.get("state"))
    necessary = state in {
        "PREPARED", "AUTHORIZED", "SUBMITTING", "PROVIDER_ID_RECORDED",
        "WAITING", "AMBIGUOUS_PROVIDER_SUBMISSION",
    }
    ambiguity_reasons: list[str] = []
    if state == "SUBMITTING" and not provider.get("id"):
        ambiguity_reasons.append("submitting_without_provider_identity")
    if not snapshot_valid:
        ambiguity_reasons.append("snapshot_incomplete_or_invalid")
    route = str((action.get("binding") or {}).get("route") or "")
    parts = route.split(":")
    attempt = 1
    if parts and parts[-1].isdigit():
        attempt = max(1, int(parts[-1]))
    return {
        "action_id": str(action.get("action_id") or ""),
        "route": route,
        "pass_id": action.get("pass_id"),
        "attempt": attempt,
        "state": state,
        "binding": action.get("binding") or {},
        "necessary": necessary,
        "relationship": "blocking" if necessary else "independent",
        "providerless_denial_eligible": eligible,
        "eligibility_reason": reason,
        "authorization_previously_recorded": bool(action.get("authorization")),
        "provider_operation_id": provider.get("id"),
        "provider_identity_present": bool(provider.get("id")),
        "provider_evidence_present": bool(action.get("reported") or provider),
        "consumption_evidence_present": bool(action.get("consumption")),
        "blocking_action_ids": [],
        "ambiguity_review_reasons": ambiguity_reasons,
    }


def _local_dependencies(state: dict[str, Any]) -> list[dict[str, Any]]:
    status = str(state.get("status") or "")
    dependencies: list[dict[str, Any]] = []
    mapping = {
        "AUTHORING": ("retry_preparation", "authoring_continuation"),
        "AUTHORING_COMPLETE": ("local_assembly", "final_assembly_required"),
        "WAITING_FOR_RESPONSE": (
            "provider_result_reconciliation", "provider_result_pending"
        ),
        "AWAITING_SPEND_AUTHORIZATION": (
            "retry_preparation", "prepared_action_authorization_pending"
        ),
        "AMBIGUOUS_PROVIDER_SUBMISSION": (
            "provider_submission_ambiguity", "provider_submission_uncertain"
        ),
        "FINAL_QA_REQUIRES_REVIEW": (
            "native_state_repair_review", "final_qa_review_required"
        ),
        "FINAL_QA_FAILED": (
            "native_state_repair_review", "final_qa_failed"
        ),
        "FAILED_REQUIRES_REVIEW": (
            "native_state_repair_review", "native_failure_review_required"
        ),
    }
    if status in mapping:
        kind, reason = mapping[status]
        dependencies.append({"kind": kind, "blocking": True, "reason_code": reason})
    for subject in (state.get("subjects") or {}).values():
        subject_state = str(subject.get("state") or "")
        if subject_state == "FINAL_QA_PASSED":
            dependencies.append({
                "kind": "delivery_construction",
                "blocking": True,
                "reason_code": "delivery_not_constructed",
            })
    unique = {(item["kind"], item["reason_code"]): item for item in dependencies}
    return [unique[key] for key in sorted(unique)]


def inspect_lifecycle(
    run_dir: Path,
    *,
    native_exclusive_access: str = "not_established",
    observed_at: str | None = None,
) -> dict[str, Any]:
    """Inspect exact native evidence without mutating any workspace member."""
    run_dir = run_dir.resolve()
    state = load_json(run_dir / "run.json")
    observation, review_reasons = _observation(
        run_dir,
        state,
        native_exclusive_access=native_exclusive_access,
        observed_at=observed_at or _utc_now(),
    )
    actions = [
        _action_record(action, snapshot_valid=observation["inventory_valid"])
        for action in ((state.get("spend_ledger") or {}).get("actions") or [])
    ]
    actions.sort(key=action_presentation_key)
    inventory = {
        "schema_version": OUTSTANDING_ACTION_INVENTORY_SCHEMA,
        "run_id": str(state.get("run_id") or ""),
        "observation": observation,
        "ordering_semantics": "deterministic_presentation_only_not_execution_order",
        "actions": actions,
    }
    dependencies = _local_dependencies(state)
    provider_continuation = any(item["necessary"] for item in actions)
    local_continuation = bool(dependencies)
    status = str(state.get("status") or "")
    subjects = list((state.get("subjects") or {}).values())
    complete = bool(subjects) and all(
        item.get("state") in FINAL_SUCCESS_STATES for item in subjects
    ) and status in FINAL_SUCCESS_STATES
    deck_exists = bool(subjects) and all(
        Path(str(item.get("deck") or "")).is_file() for item in subjects
    )
    qa_passed = bool(subjects) and all(
        item.get("state") in FINAL_SUCCESS_STATES or
        item.get("state") == "FINAL_QA_PASSED"
        for item in subjects
    )
    terminal = complete or status in {
        "FINAL_QA_FAILED", "FINAL_QA_REQUIRES_REVIEW",
        "FAILED_REQUIRES_REVIEW", "BUDGET_EXHAUSTED",
        "AMBIGUOUS_PROVIDER_SUBMISSION",
    }
    if complete:
        outcome, terminal_reason = "delivery_complete", "delivery_complete"
    elif status == "BUDGET_EXHAUSTED":
        outcome, terminal_reason = "budget_exhausted", "budget_exhausted"
    elif status == "AMBIGUOUS_PROVIDER_SUBMISSION":
        outcome, terminal_reason = "ambiguous", "ambiguous_provider_submission"
    elif terminal:
        outcome, terminal_reason = "review_required", "review_required"
    else:
        outcome, terminal_reason = "nonterminal", None
    terminal_summary = {
        "outcome": outcome,
        "terminal": terminal,
        "terminal_reason": terminal_reason,
        "deck_bytes_exist": deck_exists,
        "native_qa_passed": qa_passed,
        "assembly_lint_validation_accepted": qa_passed,
        "delivery_package_complete": complete,
        "delivery_publishable": complete,
        "provider_continuation_remains": provider_continuation,
        "local_continuation_remains": local_continuation,
    }
    if review_reasons:
        quiescence = {"state": "unknown_review_required", "reasons": [
            "snapshot_invalid" if "snapshot_incomplete_or_invalid" in review_reasons
            else "writer_race_possible"
        ]}
    elif provider_continuation or local_continuation:
        reasons = []
        if provider_continuation:
            reasons.append("provider_continuation_remains")
        if local_continuation:
            reasons.append("local_continuation_remains")
        quiescence = {"state": "not_quiescent", "reasons": reasons}
    else:
        quiescence = {
            "state": "quiescent",
            "reasons": ["no_provider_or_local_continuation"],
        }
    return {
        "schema_version": LIFECYCLE_INSPECTION_SCHEMA,
        "run_id": str(state.get("run_id") or ""),
        "observation": observation,
        "terminal": terminal_summary,
        "quiescence": quiescence,
        "local_dependencies": dependencies,
        "action_inventory": inventory,
        "review_reasons": sorted(set(review_reasons)),
    }
