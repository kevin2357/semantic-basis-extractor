"""Read-only lifecycle inspection for semantic-closure workspaces."""

from __future__ import annotations

import hashlib
import json
import os
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .closure import (
    FINAL_SUCCESS_STATES,
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    persist_state,
    sha256_file,
    snapshot_inventory,
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from .lifecycle_contracts import (
    BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS,
    BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
    BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
    CLOSEOUT_RESULT_SCHEMA,
    DENIAL_REASONS,
    LIFECYCLE_INSPECTION_SCHEMA,
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
    NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
    OUTSTANDING_ACTION_INVENTORY_SCHEMA,
    action_presentation_key,
    batch_negative_authorization_request_sha256,
    observation_transition_errors,
)
from .execution_events import ExecutionEventEmitter


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


@contextmanager
def _exclusive_lifecycle_lock(run_dir: Path):
    """Acquire the same cross-process single-writer boundary as spend consumption."""
    path = run_dir / "spend-consumption.lock"
    with path.open("a+b") as handle:
        if path.stat().st_size == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _refusal(
    request: dict[str, Any],
    *,
    outcome: str,
    review_reasons: list[str],
    actual_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "schema_version": NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
        "run_id": request.get("run_id"),
        "action_id": request.get("action_id"),
        "binding": deepcopy(request.get("binding") or {}),
        "applied": False,
        "outcome": outcome,
        "release_eligible": False,
        "external_authority_reference": request.get("external_authority_reference"),
        "request_observation": deepcopy(request.get("observed") or {}),
        "review_reasons": review_reasons,
    }
    if actual_observation is not None:
        result["actual_observation"] = actual_observation
    return result


def _artifact_descriptor(path: Path, run_dir: Path) -> dict[str, Any]:
    return {
        "logical_path": path.relative_to(run_dir).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


_BATCH_REQUEST_FIELDS = frozenset({"schema_version", "run_id", "observed", "actions"})
_BATCH_MEMBER_FIELDS = frozenset({
    "action_id", "binding", "denial_reason", "external_authority_reference",
})
_BINDING_FIELDS = frozenset({
    "run_id", "profile_sha256", "prepared_state_revision", "stage", "route",
    "request_sha256", "model", "service_level", "maximum_output_tokens",
    "commitment_micro_usd", "price_book_version",
})
_OBSERVATION_FIELDS = frozenset({
    "operator_state_revision", "snapshot_sha256", "logical_workspace_root",
    "snapshot_complete", "inventory_valid", "observed_at",
    "native_exclusive_access", "writer_race_possible",
})


def _validate_batch_denial_request(request: dict[str, Any]) -> None:
    if not isinstance(request, dict):
        raise ValueError("Batch negative-authorization request must be an object")
    if set(request) != _BATCH_REQUEST_FIELDS:
        raise ValueError("Batch negative-authorization request has unsupported shape")
    if request.get("schema_version") != BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA:
        raise ValueError("Unsupported batch negative-authorization request schema")
    if not isinstance(request.get("run_id"), str) or not request["run_id"]:
        raise ValueError("A non-empty batch run_id is required")
    observed = request.get("observed")
    if not isinstance(observed, dict) or set(observed) != _OBSERVATION_FIELDS:
        raise ValueError("Batch observed identity has unsupported shape")
    if (
        not isinstance(observed["operator_state_revision"], int)
        or isinstance(observed["operator_state_revision"], bool)
        or observed["operator_state_revision"] < 0
        or not isinstance(observed["snapshot_sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", observed["snapshot_sha256"])
        or not isinstance(observed["logical_workspace_root"], str)
        or not observed["logical_workspace_root"]
        or not isinstance(observed["snapshot_complete"], bool)
        or not isinstance(observed["inventory_valid"], bool)
        or not isinstance(observed["observed_at"], str)
        or not observed["observed_at"]
        or observed["native_exclusive_access"] not in {
            "established", "declared", "not_established", "unknown",
        }
        or not isinstance(observed["writer_race_possible"], bool)
    ):
        raise ValueError("Batch observed identity contains invalid values")
    actions = request.get("actions")
    if not isinstance(actions, list) or not 1 <= len(actions) <= BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS:
        raise ValueError(
            f"Batch actions must contain 1..{BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS} members"
        )
    for member in actions:
        if not isinstance(member, dict) or set(member) != _BATCH_MEMBER_FIELDS:
            raise ValueError("Batch action member has unsupported shape")
        action_id = member.get("action_id")
        if not isinstance(action_id, str) or not re.fullmatch(r"paid_[0-9a-f]{24}", action_id):
            raise ValueError("Batch action_id has unsupported shape")
        binding = member.get("binding")
        if not isinstance(binding, dict) or set(binding) != _BINDING_FIELDS:
            raise ValueError("Batch immutable binding has unsupported shape")
        if (
            not isinstance(binding["run_id"], str) or not binding["run_id"]
            or not isinstance(binding["profile_sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", binding["profile_sha256"])
            or not isinstance(binding["prepared_state_revision"], int)
            or isinstance(binding["prepared_state_revision"], bool)
            or binding["prepared_state_revision"] < 0
            or binding["stage"] not in {
                "authoring_initial", "creative_retry", "polish",
                "qualitative_critic", "qualitative_candidate",
            }
            or not isinstance(binding["route"], str) or not binding["route"]
            or not isinstance(binding["request_sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", binding["request_sha256"])
            or not isinstance(binding["model"], str) or not binding["model"]
            or binding["service_level"] not in {"interactive", "batch"}
            or not isinstance(binding["maximum_output_tokens"], int)
            or isinstance(binding["maximum_output_tokens"], bool)
            or binding["maximum_output_tokens"] < 1
            or not isinstance(binding["commitment_micro_usd"], int)
            or isinstance(binding["commitment_micro_usd"], bool)
            or binding["commitment_micro_usd"] < 0
            or not isinstance(binding["price_book_version"], str)
            or not binding["price_book_version"]
        ):
            raise ValueError("Batch immutable binding contains invalid values")
        if member.get("denial_reason") not in DENIAL_REASONS:
            raise ValueError("Unsupported batch negative-authorization denial_reason")
        authority = member.get("external_authority_reference")
        if (
            not isinstance(authority, str) or not authority or len(authority) > 512
            or "\n" in authority or "\r" in authority
        ):
            raise ValueError("A bounded single-line external_authority_reference is required")


def _batch_member_refusal(
    member: dict[str, Any], outcome: str, review_reasons: list[str],
) -> dict[str, Any]:
    return {
        "action_id": member["action_id"],
        "binding": deepcopy(member["binding"]),
        "outcome": outcome,
        "release_eligible": False,
        "external_authority_reference": member["external_authority_reference"],
        "review_reasons": review_reasons,
    }


def _batch_refusal_result(
    request: dict[str, Any], *, outcome: str,
    member_results: list[dict[str, Any]], review_reasons: list[str],
    actual_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "schema_version": BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
        "run_id": request["run_id"],
        "batch_request_sha256": batch_negative_authorization_request_sha256(request),
        "applied": False,
        "outcome": outcome,
        "request_observation": deepcopy(request["observed"]),
        "actions": member_results,
        "review_reasons": sorted(set(review_reasons)),
    }
    if actual_observation is not None:
        result["actual_observation"] = deepcopy(actual_observation)
    return result


def _batch_preflight_under_lock(
    state: dict[str, Any], request: dict[str, Any], actual: dict[str, Any],
) -> tuple[list[dict[str, Any]] | None, dict[str, Any] | None]:
    """Validate every batch member against one locked decision basis.

    Returns resolved native actions on success or a typed all-or-none refusal.
    This function performs no mutation.
    """
    observation = actual["observation"]
    members = request["actions"]
    if not observation["inventory_valid"]:
        results = [
            _batch_member_refusal(
                member, "not_evaluated", ["shared_precondition_not_evaluated"]
            ) for member in members
        ]
        return None, _batch_refusal_result(
            request, outcome="native_state_inconsistent", member_results=results,
            review_reasons=["snapshot_incomplete_or_invalid"],
            actual_observation=observation,
        )
    native_actions = (state.get("spend_ledger") or {}).get("actions") or []
    by_id = {item.get("action_id"): item for item in native_actions}
    inventory = {
        item["action_id"]: item for item in actual["action_inventory"]["actions"]
    }
    seen: set[str] = set()
    resolved: list[dict[str, Any]] = []
    assessments: list[tuple[dict[str, Any], str, list[str]]] = []
    for member in members:
        action_id = member["action_id"]
        if action_id in seen:
            assessments.append((member, "duplicate_action", ["duplicate_action"]))
            continue
        seen.add(action_id)
        action = by_id.get(action_id)
        if action is None:
            assessments.append((member, "unknown_action", ["unknown_action"]))
            continue
        if request["run_id"] != state.get("run_id") or member["binding"] != action.get("binding"):
            assessments.append((
                member, "immutable_binding_mismatch", ["immutable_binding_mismatch"]
            ))
            continue
        if action.get("consumption"):
            assessments.append((
                member, "consumption_evidence_appeared", ["provider_consumption_present"]
            ))
            continue
        provider = action.get("provider") or {}
        if provider.get("id"):
            assessments.append((
                member, "provider_identity_appeared", ["provider_identity_present"]
            ))
            continue
        if action.get("reported") or provider:
            assessments.append((
                member, "provider_evidence_appeared", ["provider_evidence_present"]
            ))
            continue
        if action.get("state") in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}:
            assessments.append((
                member, "ambiguous_submission_boundary",
                ["submitting_without_provider_identity"],
            ))
            continue
        eligibility = inventory[action_id]
        if not eligibility["providerless_denial_eligible"]:
            assessments.append((member, "action_ineligible", ["action_ineligible"]))
            continue
        assessments.append((member, "eligible", []))
        resolved.append(action)

    action_failures = [item for item in assessments if item[1] != "eligible"]
    transition_errors = observation_transition_errors(request["observed"], observation)
    if not action_failures and transition_errors:
        reason_map = {
            "operator_state_revision": "operator_revision_mismatch",
            "snapshot_sha256": "snapshot_identity_mismatch",
            "logical_workspace_root": "snapshot_identity_mismatch",
            "snapshot_complete": "snapshot_incomplete_or_invalid",
            "inventory_valid": "snapshot_incomplete_or_invalid",
            "native_exclusive_access": "writer_race_possible",
            "writer_race_possible": "writer_race_possible",
        }
        reasons = sorted({reason_map[item] for item in transition_errors})
        results = [
            _batch_member_refusal(
                member, "not_evaluated", ["shared_precondition_not_evaluated"]
            ) for member in members
        ]
        return None, _batch_refusal_result(
            request, outcome="stale_observation", member_results=results,
            review_reasons=reasons, actual_observation=observation,
        )
    if action_failures:
        precedence = (
            "duplicate_action", "unknown_action", "immutable_binding_mismatch",
            "consumption_evidence_appeared", "provider_identity_appeared",
            "provider_evidence_appeared", "ambiguous_submission_boundary",
            "action_ineligible", "native_state_inconsistent",
        )
        outcomes = {item[1] for item in action_failures}
        batch_outcome = next(item for item in precedence if item in outcomes)
        results = [
            _batch_member_refusal(
                member,
                member_outcome,
                reasons if member_outcome != "eligible" else ["batch_refused_by_other_member"],
            )
            for member, member_outcome, reasons in assessments
        ]
        review_reasons = [reason for _, _, reasons in action_failures for reason in reasons]
        return None, _batch_refusal_result(
            request, outcome=batch_outcome, member_results=results,
            review_reasons=review_reasons, actual_observation=observation,
        )
    return resolved, None


def _locked_batch_denial_preflight(
    run_dir: Path, request: dict[str, Any], *, decision_at: str | None = None,
) -> dict[str, Any]:
    """Exercise the Slice 2 locked preflight without exposing a public operation."""
    _validate_batch_denial_request(request)
    run_dir = run_dir.resolve()
    try:
        lock = _exclusive_lifecycle_lock(run_dir)
        lock.__enter__()
    except (OSError, BlockingIOError):
        members = [
            _batch_member_refusal(
                member, "not_evaluated", ["shared_precondition_not_evaluated"]
            ) for member in request["actions"]
        ]
        return _batch_refusal_result(
            request, outcome="exclusivity_not_established", member_results=members,
            review_reasons=["writer_race_possible"],
        )
    try:
        state = load_json(run_dir / "run.json")
        actual = inspect_lifecycle(
            run_dir, native_exclusive_access="established",
            observed_at=decision_at or _utc_now(),
        )
        resolved, refusal = _batch_preflight_under_lock(state, request, actual)
        if refusal is not None:
            return refusal
        return {
            "eligible": True,
            "run_id": state["run_id"],
            "batch_request_sha256": batch_negative_authorization_request_sha256(request),
            "decision_basis": actual["observation"],
            "action_ids": [item["action_id"] for item in resolved or []],
        }
    finally:
        lock.__exit__(None, None, None)


def _batch_denial_artifact_content(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "astrowoof.provider_negative_authorization_batch_record.v0.1",
        "run_id": record["request"]["run_id"],
        "batch_request_sha256": record["batch_request_sha256"],
        "request": deepcopy(record["request"]),
        "decision_basis": deepcopy(record["decision_basis"]),
        "result_state_revision": record["result_state_revision"],
        "committed_at": record["committed_at"],
        "actions": deepcopy(record["actions"]),
    }


def _batch_success_result(
    run_dir: Path, state: dict[str, Any], record: dict[str, Any], *, replay: bool,
) -> dict[str, Any]:
    artifact_path = run_dir / record["result_artifact"]
    if not artifact_path.is_file() or load_json(artifact_path) != _batch_denial_artifact_content(record):
        raise ValueError("Durable batch negative-authorization result is missing or changed")
    post = inspect_lifecycle(
        run_dir, native_exclusive_access="established",
        observed_at=record["committed_at"],
    )["observation"]
    outcome = "idempotent_replay" if replay else "applied"
    return {
        "schema_version": BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
        "run_id": state["run_id"],
        "batch_request_sha256": record["batch_request_sha256"],
        "applied": not replay,
        "outcome": outcome,
        "request_observation": deepcopy(record["request"]["observed"]),
        "decision_basis": deepcopy(record["decision_basis"]),
        "actions": [{**deepcopy(item), "outcome": outcome} for item in record["actions"]],
        "post_mutation_observation": post,
        "result_checkpoint": {
            "operator_state_revision": state["state_revision"],
            "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
            "result_artifact": _artifact_descriptor(artifact_path, run_dir),
        },
    }


def deny_providerless_actions(
    run_dir: Path,
    request: dict[str, Any],
    *,
    decision_at: str | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
) -> dict[str, Any]:
    """Atomically deny one ordered batch of exact provider-less actions.

    All members are preflighted under one native single-writer lock before any
    semantic mutation. No provider client is accepted or reachable.
    """
    del event_emitter  # Slice 5 wires the approved observational event policy.
    _validate_batch_denial_request(request)
    run_dir = run_dir.resolve()
    digest = batch_negative_authorization_request_sha256(request)
    try:
        lock = _exclusive_lifecycle_lock(run_dir)
        lock.__enter__()
    except (OSError, BlockingIOError):
        members = [
            _batch_member_refusal(
                member, "not_evaluated", ["shared_precondition_not_evaluated"]
            ) for member in request["actions"]
        ]
        return _batch_refusal_result(
            request, outcome="exclusivity_not_established", member_results=members,
            review_reasons=["writer_race_possible"],
        )
    try:
        state = load_json(run_dir / "run.json")
        validate_workspace_snapshot(run_dir, state)
        batches = state.get("providerless_denial_batches") or {}
        existing = batches.get(digest)
        if isinstance(existing, dict):
            if existing.get("request") != request:
                raise ValueError("Batch request digest collision or changed durable request")
            for member in existing.get("actions") or []:
                action = next(
                    (item for item in (state.get("spend_ledger") or {}).get("actions", [])
                     if item.get("action_id") == member.get("action_id")),
                    None,
                )
                denial = (action or {}).get("negative_authorization") or {}
                if (
                    (action or {}).get("state") != "DENIED_PROVIDERLESS"
                    or denial.get("batch_request_sha256") != digest
                ):
                    raise ValueError("Durable batch denial action evidence is inconsistent")
            return _batch_success_result(run_dir, state, existing, replay=True)

        actual = inspect_lifecycle(
            run_dir, native_exclusive_access="established",
            observed_at=decision_at or _utc_now(),
        )
        resolved, refusal = _batch_preflight_under_lock(state, request, actual)
        if refusal is not None:
            return refusal
        members_by_id = {item["action_id"]: item for item in request["actions"]}
        artifact_relative = (
            Path("lifecycle") / "negative-authorization-batches" / f"{digest}.json"
        )
        artifact_path = run_dir / artifact_relative
        committed_at = decision_at or _utc_now()
        anticipated_revision = int(state.get("state_revision") or 0) + 1
        action_results: list[dict[str, Any]] = []
        for action in resolved or []:
            member = members_by_id[action["action_id"]]
            authorization_previously_recorded = bool(action.get("authorization"))
            action_result = {
                "action_id": action["action_id"],
                "binding": deepcopy(action["binding"]),
                "disposition": "DENIED_PROVIDERLESS",
                "denial_reason": member["denial_reason"],
                "authorization_previously_recorded": authorization_previously_recorded,
                "release_eligible": True,
                "external_authority_reference": member["external_authority_reference"],
            }
            action_results.append(action_result)
            action["state"] = "DENIED_PROVIDERLESS"
            action["negative_authorization"] = {
                "denial_reason": member["denial_reason"],
                "authorization_previously_recorded": authorization_previously_recorded,
                "external_authority_reference": member["external_authority_reference"],
                "decision_basis": deepcopy(actual["observation"]),
                "request_observation": deepcopy(request["observed"]),
                "result_artifact": artifact_relative.as_posix(),
                "batch_request_sha256": digest,
            }
        record = {
            "batch_request_sha256": digest,
            "request": deepcopy(request),
            "decision_basis": deepcopy(actual["observation"]),
            "result_state_revision": anticipated_revision,
            "result_artifact": artifact_relative.as_posix(),
            "committed_at": committed_at,
            "actions": action_results,
        }
        state.setdefault("providerless_denial_batches", {})[digest] = record
        staged_path = artifact_path.with_name(f".{artifact_path.name}.tmp")
        write_json_atomic(staged_path, _batch_denial_artifact_content(record))
        persist_state(run_dir / "run.json", state)
        if state["state_revision"] != anticipated_revision:
            raise RuntimeError("Unexpected batch denial state revision advance")
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        staged_path.replace(artifact_path)
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, state)
        return _batch_success_result(run_dir, state, record, replay=False)
    finally:
        lock.__exit__(None, None, None)


def deny_providerless_action(
    run_dir: Path,
    request: dict[str, Any],
    *,
    decision_at: str | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
) -> dict[str, Any]:
    """Durably deny one exact provider-less action or return typed refusal.

    No provider client is accepted or reachable from this operation.
    """
    run_dir = run_dir.resolve()
    if request.get("schema_version") != NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA:
        raise ValueError("Unsupported negative-authorization request schema")
    authority = request.get("external_authority_reference")
    if not isinstance(authority, str) or not authority or len(authority) > 512:
        raise ValueError("A bounded external_authority_reference is required")
    if "\n" in authority or "\r" in authority:
        raise ValueError("external_authority_reference cannot contain newlines")
    if request.get("denial_reason") not in DENIAL_REASONS:
        raise ValueError("Unsupported negative-authorization denial_reason")
    try:
        lock = _exclusive_lifecycle_lock(run_dir)
        lock.__enter__()
    except (OSError, BlockingIOError):
        return _refusal(
            request,
            outcome="exclusivity_not_established",
            review_reasons=["writer_race_possible"],
        )
    try:
        state = load_json(run_dir / "run.json")
        actual = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=decision_at or _utc_now(),
        )
        observation = actual["observation"]
        if not observation["inventory_valid"]:
            return _refusal(
                request,
                outcome="native_state_inconsistent",
                review_reasons=["snapshot_incomplete_or_invalid"],
                actual_observation=observation,
            )
        actions = (state.get("spend_ledger") or {}).get("actions") or []
        action = next(
            (item for item in actions if item.get("action_id") == request.get("action_id")),
            None,
        )
        if action is None or request.get("run_id") != state.get("run_id"):
            return _refusal(
                request,
                outcome="immutable_binding_mismatch",
                review_reasons=["immutable_binding_mismatch"],
                actual_observation=observation,
            )
        if request.get("binding") != action.get("binding"):
            return _refusal(
                request,
                outcome="immutable_binding_mismatch",
                review_reasons=["immutable_binding_mismatch"],
                actual_observation=observation,
            )
        existing = action.get("negative_authorization")
        if action.get("state") == "DENIED_PROVIDERLESS" and isinstance(existing, dict):
            if (
                request.get("denial_reason") != existing.get("denial_reason")
                or request.get("external_authority_reference")
                != existing.get("external_authority_reference")
                or request.get("observed") != existing.get("request_observation")
            ):
                return _refusal(
                    request,
                    outcome="native_state_inconsistent",
                    review_reasons=["native_state_inconsistent"],
                    actual_observation=observation,
                )
            artifact_path = run_dir / existing["result_artifact"]
            result = {
                "schema_version": NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
                "run_id": state["run_id"],
                "action_id": action["action_id"],
                "binding": deepcopy(action["binding"]),
                "applied": False,
                "outcome": "idempotent_replay",
                "disposition": "DENIED_PROVIDERLESS",
                "denial_reason": existing["denial_reason"],
                "authorization_previously_recorded": existing["authorization_previously_recorded"],
                "release_eligible": True,
                "external_authority_reference": existing["external_authority_reference"],
                "request_observation": deepcopy(request["observed"]),
                "decision_basis": deepcopy(existing["decision_basis"]),
                "result_checkpoint": {
                    "operator_state_revision": int(state.get("state_revision") or 0),
                    "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                    "result_artifact": _artifact_descriptor(artifact_path, run_dir),
                },
            }
            if event_emitter is not None:
                event_emitter.emit("authorization.denied_providerless", data={
                    "action_id": action["action_id"],
                    "denial_reason": existing["denial_reason"],
                    "outcome": "idempotent_replay",
                }, correlation={"action_id": action["action_id"]})
            return result
        # Provider-bound evidence takes precedence over a generic stale-observation
        # refusal so a race across submission is machine-distinguishable.
        if action.get("consumption"):
            return _refusal(
                request,
                outcome="consumption_evidence_appeared",
                review_reasons=["provider_consumption_present"],
                actual_observation=observation,
            )
        if action.get("provider"):
            return _refusal(
                request,
                outcome="provider_identity_appeared",
                review_reasons=["provider_identity_present"],
                actual_observation=observation,
            )
        if action.get("reported"):
            return _refusal(
                request,
                outcome="provider_evidence_appeared",
                review_reasons=["provider_evidence_present"],
                actual_observation=observation,
            )
        if action.get("state") in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}:
            return _refusal(
                request,
                outcome="ambiguous_submission_boundary",
                review_reasons=["submitting_without_provider_identity"],
                actual_observation=observation,
            )
        transition_errors = observation_transition_errors(
            request.get("observed") or {}, observation
        )
        if transition_errors:
            reason_map = {
                "operator_state_revision": "operator_revision_mismatch",
                "snapshot_sha256": "snapshot_identity_mismatch",
                "logical_workspace_root": "snapshot_identity_mismatch",
                "snapshot_complete": "snapshot_incomplete_or_invalid",
                "inventory_valid": "snapshot_incomplete_or_invalid",
                "native_exclusive_access": "writer_race_possible",
                "writer_race_possible": "writer_race_possible",
            }
            return _refusal(
                request,
                outcome="stale_observation",
                review_reasons=sorted({reason_map[item] for item in transition_errors}),
                actual_observation=observation,
            )
        eligibility_action = next(
            item for item in actual["action_inventory"]["actions"]
            if item["action_id"] == action["action_id"]
        )
        if not eligibility_action["providerless_denial_eligible"]:
            eligibility = eligibility_action["eligibility_reason"]
            outcomes = {
                "provider_identity_present": "provider_identity_appeared",
                "provider_evidence_present": "provider_evidence_appeared",
                "consumption_evidence_present": "consumption_evidence_appeared",
                "submission_ambiguous": "ambiguous_submission_boundary",
            }
            review = {
                "provider_identity_present": "provider_identity_present",
                "provider_evidence_present": "provider_evidence_present",
                "consumption_evidence_present": "provider_consumption_present",
                "submission_ambiguous": "submitting_without_provider_identity",
            }
            return _refusal(
                request,
                outcome=outcomes.get(eligibility, "native_state_inconsistent"),
                review_reasons=[review.get(eligibility, "native_state_inconsistent")],
                actual_observation=observation,
            )
        artifact_relative = (
            Path("lifecycle") / "negative-authorizations" /
            f"{action['action_id']}.json"
        )
        artifact_path = run_dir / artifact_relative
        authorization_previously_recorded = bool(action.get("authorization"))
        native_record = {
            "schema_version": "astrowoof.provider_negative_authorization_record.v0.1",
            "run_id": state["run_id"],
            "action_id": action["action_id"],
            "binding": deepcopy(action["binding"]),
            "disposition": "DENIED_PROVIDERLESS",
            "denial_reason": request["denial_reason"],
            "authorization_previously_recorded": authorization_previously_recorded,
            "external_authority_reference": authority,
            "request_observation": deepcopy(request["observed"]),
            "decision_basis": deepcopy(observation),
        }
        action["state"] = "DENIED_PROVIDERLESS"
        action["negative_authorization"] = {
            "denial_reason": request["denial_reason"],
            "authorization_previously_recorded": authorization_previously_recorded,
            "external_authority_reference": authority,
            "decision_basis": deepcopy(observation),
            "request_observation": deepcopy(request["observed"]),
            "result_artifact": artifact_relative.as_posix(),
        }
        persist_state(run_dir / "run.json", state)
        write_json_atomic(artifact_path, native_record)
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, state)
        result = {
            "schema_version": NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
            "run_id": state["run_id"],
            "action_id": action["action_id"],
            "binding": deepcopy(action["binding"]),
            "applied": True,
            "outcome": "applied",
            "disposition": "DENIED_PROVIDERLESS",
            "denial_reason": request["denial_reason"],
            "authorization_previously_recorded": authorization_previously_recorded,
            "release_eligible": True,
            "external_authority_reference": authority,
            "request_observation": deepcopy(request["observed"]),
            "decision_basis": observation,
            "result_checkpoint": {
                "operator_state_revision": state["state_revision"],
                "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                "result_artifact": _artifact_descriptor(artifact_path, run_dir),
            },
        }
        if event_emitter is not None:
            event_emitter.emit("authorization.denied_providerless", data={
                "action_id": action["action_id"],
                "denial_reason": request["denial_reason"],
                "outcome": "applied",
            }, correlation={"action_id": action["action_id"]})
        return result
    finally:
        lock.__exit__(None, None, None)


def _semantic_closeout_content(inspection: dict[str, Any]) -> dict[str, Any]:
    terminal = inspection["terminal"]
    if terminal["outcome"] == "ambiguous":
        disposition = "ambiguous"
    elif terminal["outcome"] in {"review_required", "failed"}:
        disposition = "review_required"
    elif (
        terminal["provider_continuation_remains"]
        or terminal["local_continuation_remains"]
    ):
        disposition = "continuation_required"
    elif inspection["quiescence"]["state"] == "quiescent":
        disposition = "closed"
    else:
        disposition = "review_required"
    unresolved = [
        item["action_id"] for item in inspection["action_inventory"]["actions"]
        if item["necessary"]
    ]
    return {
        "disposition": disposition,
        "terminal": deepcopy(terminal),
        "quiescence": deepcopy(inspection["quiescence"]),
        "local_dependencies": deepcopy(inspection["local_dependencies"]),
        "unresolved_action_ids": unresolved,
    }


def _closeout_artifact(state: dict[str, Any]) -> dict[str, Any]:
    existing = state["lifecycle_closeout"]
    return {
        "schema_version": "astrowoof.authoring_closeout_record.v0.1",
        "run_id": state["run_id"],
        "decision_basis": deepcopy(existing["decision_basis"]),
        "semantic": deepcopy(existing["semantic"]),
        "semantic_result_sha256": existing["semantic_result_sha256"],
    }


def _recover_interrupted_closeout(run_dir: Path, state: dict[str, Any]) -> bool:
    """Finish only the exact, cryptographically verified closeout write set."""
    existing = state.get("lifecycle_closeout")
    if not isinstance(existing, dict):
        return False
    if existing.get("result_state_revision") != state.get("state_revision"):
        return False
    artifact_path = run_dir / existing["result_artifact"]
    staged_path = artifact_path.with_name(f".{artifact_path.name}.tmp")
    expected_artifact = _closeout_artifact(state)
    candidate = artifact_path if artifact_path.is_file() else staged_path
    if not candidate.is_file() or load_json(candidate) != expected_artifact:
        return False
    manifest_path = run_dir / SNAPSHOT_NAME
    if not manifest_path.is_file():
        return False
    manifest = load_json(manifest_path)
    expected_members = {
        item["path"]: item for item in manifest.get("members", [])
    }
    actual_members = {
        item["path"]: item
        for item in snapshot_inventory(run_dir, use_process_cache=False)
    }
    allowed_changed = {
        "run.json", "public-run.json", "spend-authorization-requests.json",
        existing["result_artifact"],
    }
    all_paths = set(expected_members) | set(actual_members)
    changed = {
        path for path in all_paths
        if expected_members.get(path) != actual_members.get(path)
    }
    if not changed or not changed <= allowed_changed or "run.json" not in changed:
        return False
    if candidate == staged_path:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        staged_path.replace(artifact_path)
    write_workspace_snapshot(run_dir)
    validate_workspace_snapshot(run_dir, state)
    return True


def closeout_run(
    run_dir: Path,
    *,
    observed_at: str | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
    _failure_injector: Any | None = None,
) -> dict[str, Any]:
    """Persist and return one idempotent native lifecycle closeout result."""
    run_dir = run_dir.resolve()
    try:
        lock = _exclusive_lifecycle_lock(run_dir)
        lock.__enter__()
    except (OSError, BlockingIOError):
        raise RuntimeError("Closeout could not establish native exclusive access")
    try:
        state = load_json(run_dir / "run.json")
        try:
            validate_workspace_snapshot(run_dir, state)
        except ValueError:
            if not _recover_interrupted_closeout(run_dir, state):
                raise
            state = load_json(run_dir / "run.json")
        existing = state.get("lifecycle_closeout")
        if (
            isinstance(existing, dict)
            and existing.get("result_state_revision") == state.get("state_revision")
        ):
            artifact_path = run_dir / existing["result_artifact"]
            if not artifact_path.is_file():
                raise ValueError("Durable closeout result artifact is missing")
            result = {
                "schema_version": CLOSEOUT_RESULT_SCHEMA,
                "run_id": state["run_id"],
                "disposition": existing["semantic"]["disposition"],
                "decision_basis": deepcopy(existing["decision_basis"]),
                "terminal": deepcopy(existing["semantic"]["terminal"]),
                "quiescence": deepcopy(existing["semantic"]["quiescence"]),
                "local_dependencies": deepcopy(existing["semantic"]["local_dependencies"]),
                "unresolved_action_ids": list(existing["semantic"]["unresolved_action_ids"]),
                "result_checkpoint": {
                    "operator_state_revision": state["state_revision"],
                    "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                    "result_artifact": _artifact_descriptor(artifact_path, run_dir),
                },
                "semantic_result_sha256": existing["semantic_result_sha256"],
            }
            if event_emitter is not None:
                event_emitter.emit("closeout.completed", data={
                    "disposition": result["disposition"],
                    "semantic_result_sha256": result["semantic_result_sha256"],
                })
            return result
        inspection = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=observed_at or _utc_now(),
        )
        if not inspection["observation"]["inventory_valid"]:
            raise ValueError("Closeout requires one complete validated workspace snapshot")
        semantic = _semantic_closeout_content(inspection)
        semantic_sha256 = hashlib.sha256(
            json.dumps(
                semantic, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        artifact_relative = Path("lifecycle") / "closeout-result.json"
        artifact_path = run_dir / artifact_relative
        anticipated_revision = int(state.get("state_revision") or 0) + 1
        state["lifecycle_closeout"] = {
            "result_state_revision": anticipated_revision,
            "result_artifact": artifact_relative.as_posix(),
            "decision_basis": deepcopy(inspection["observation"]),
            "semantic": deepcopy(semantic),
            "semantic_result_sha256": semantic_sha256,
        }
        staged_path = artifact_path.with_name(f".{artifact_path.name}.tmp")
        write_json_atomic(staged_path, _closeout_artifact(state))
        if _failure_injector:
            _failure_injector("after_artifact_staged")
        persist_state(run_dir / "run.json", state)
        if state["state_revision"] != anticipated_revision:
            raise RuntimeError("Unexpected closeout state revision advance")
        if _failure_injector:
            _failure_injector("after_state_persisted")
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        staged_path.replace(artifact_path)
        if _failure_injector:
            _failure_injector("after_artifact_promoted")
        write_workspace_snapshot(run_dir)
        if _failure_injector:
            _failure_injector("after_snapshot_published")
        validate_workspace_snapshot(run_dir, state)
        result = {
            "schema_version": CLOSEOUT_RESULT_SCHEMA,
            "run_id": state["run_id"],
            "disposition": semantic["disposition"],
            "decision_basis": inspection["observation"],
            "terminal": semantic["terminal"],
            "quiescence": semantic["quiescence"],
            "local_dependencies": semantic["local_dependencies"],
            "unresolved_action_ids": semantic["unresolved_action_ids"],
            "result_checkpoint": {
                "operator_state_revision": state["state_revision"],
                "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                "result_artifact": _artifact_descriptor(artifact_path, run_dir),
            },
            "semantic_result_sha256": semantic_sha256,
        }
        if event_emitter is not None:
            event_emitter.emit("closeout.completed", data={
                "disposition": result["disposition"],
                "semantic_result_sha256": result["semantic_result_sha256"],
            })
        return result
    finally:
        lock.__exit__(None, None, None)
