"""Read-only lifecycle inspection for semantic-closure workspaces."""

from __future__ import annotations

import hashlib
import json
import os
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
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from .lifecycle_contracts import (
    CLOSEOUT_RESULT_SCHEMA,
    DENIAL_REASONS,
    LIFECYCLE_INSPECTION_SCHEMA,
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
    NEGATIVE_AUTHORIZATION_RESULT_SCHEMA,
    OUTSTANDING_ACTION_INVENTORY_SCHEMA,
    action_presentation_key,
    observation_transition_errors,
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


def deny_providerless_action(
    run_dir: Path,
    request: dict[str, Any],
    *,
    decision_at: str | None = None,
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
            return {
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
        return {
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


def closeout_run(
    run_dir: Path,
    *,
    observed_at: str | None = None,
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
        validate_workspace_snapshot(run_dir, state)
        existing = state.get("lifecycle_closeout")
        if (
            isinstance(existing, dict)
            and existing.get("result_state_revision") == state.get("state_revision")
        ):
            artifact_path = run_dir / existing["result_artifact"]
            if not artifact_path.is_file():
                raise ValueError("Durable closeout result artifact is missing")
            return {
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
        artifact = {
            "schema_version": "astrowoof.authoring_closeout_record.v0.1",
            "run_id": state["run_id"],
            "decision_basis": deepcopy(inspection["observation"]),
            "semantic": semantic,
            "semantic_result_sha256": semantic_sha256,
        }
        anticipated_revision = int(state.get("state_revision") or 0) + 1
        state["lifecycle_closeout"] = {
            "result_state_revision": anticipated_revision,
            "result_artifact": artifact_relative.as_posix(),
            "decision_basis": deepcopy(inspection["observation"]),
            "semantic": deepcopy(semantic),
            "semantic_result_sha256": semantic_sha256,
        }
        write_json_atomic(artifact_path, artifact)
        persist_state(run_dir / "run.json", state)
        if state["state_revision"] != anticipated_revision:
            raise RuntimeError("Unexpected closeout state revision advance")
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, state)
        return {
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
    finally:
        lock.__exit__(None, None, None)
