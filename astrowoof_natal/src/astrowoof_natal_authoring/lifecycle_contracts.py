"""Public vocabulary for lifecycle inspection, denial, closeout, and events.

This module defines wire vocabulary only.  It deliberately does not inspect or
mutate a run; those operations are introduced by later sprint slices.
"""

from __future__ import annotations

import json
from typing import Any


NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA = (
    "astrowoof.provider_negative_authorization_request.v0.1"
)
NEGATIVE_AUTHORIZATION_RESULT_SCHEMA = (
    "astrowoof.provider_negative_authorization_result.v0.1"
)
OUTSTANDING_ACTION_INVENTORY_SCHEMA = (
    "astrowoof.provider_action_inventory.v0.1"
)
LIFECYCLE_INSPECTION_SCHEMA = "astrowoof.authoring_lifecycle_inspection.v0.1"
CLOSEOUT_RESULT_SCHEMA = "astrowoof.authoring_closeout_result.v0.1"
EXECUTION_EVENT_SCHEMA = "sbe.execution_event.v1"

PROVIDER_ACTION_STATES = (
    "PREPARED",
    "AUTHORIZED",
    "SUBMITTING",
    "PROVIDER_ID_RECORDED",
    "WAITING",
    "REPORTED",
    "DENIED_PROVIDERLESS",
    "BUDGET_EXHAUSTED",
    "SKIPPED_BUDGET_EXHAUSTED",
    "AMBIGUOUS_PROVIDER_SUBMISSION",
)

DENIAL_REASONS = (
    "external_authority_denied",
    "reservation_unavailable",
    "product_policy_denied",
    "run_cancelled_before_submission",
)

TERMINAL_REASONS = (
    "delivery_complete",
    "native_policy_stop",
    "native_qa_failure",
    "budget_exhausted",
    "providerless_denial",
    "review_required",
    "ambiguous_provider_submission",
    "native_failure",
)

AMBIGUITY_REVIEW_REASONS = (
    "submitting_without_provider_identity",
    "provider_identity_present",
    "provider_consumption_present",
    "provider_evidence_present",
    "immutable_binding_mismatch",
    "operator_revision_mismatch",
    "snapshot_identity_mismatch",
    "snapshot_incomplete_or_invalid",
    "native_state_inconsistent",
    "writer_race_possible",
)

LOCAL_DEPENDENCY_KINDS = (
    "deterministic_qa",
    "local_assembly",
    "provider_submission_ambiguity",
    "provider_result_reconciliation",
    "retry_preparation",
    "polish",
    "critic_execution",
    "delivery_construction",
    "native_state_repair_review",
    "other_versioned_native_continuation",
)

PROVIDERLESS_ELIGIBILITY_REASONS = (
    "eligible_prepared",
    "eligible_authorized_unconsumed",
    "already_denied_providerless",
    "state_not_providerless",
    "submission_ambiguous",
    "consumption_evidence_present",
    "provider_identity_present",
    "provider_evidence_present",
    "binding_mismatch",
    "revision_mismatch",
    "snapshot_mismatch",
    "action_superseded",
    "action_no_longer_necessary",
    "native_state_inconsistent",
)

NEGATIVE_AUTHORIZATION_OUTCOMES = (
    "applied",
    "idempotent_replay",
    "stale_observation",
    "immutable_binding_mismatch",
    "provider_identity_appeared",
    "provider_evidence_appeared",
    "consumption_evidence_appeared",
    "ambiguous_submission_boundary",
    "native_state_inconsistent",
    "exclusivity_not_established",
    "writer_race_possible",
    "review_required",
)

QUIESCENCE_STATES = ("quiescent", "not_quiescent", "unknown_review_required")
QUIESCENCE_REASONS = (
    "no_provider_or_local_continuation",
    "provider_continuation_remains",
    "local_continuation_remains",
    "snapshot_invalid",
    "writer_race_possible",
    "native_state_inconsistent",
)

NEGATIVE_AUTHORIZATION_OUTCOMES = (
    "applied",
    "idempotent_replay",
    "stale_observation",
    "immutable_binding_mismatch",
    "provider_identity_appeared",
    "provider_evidence_appeared",
    "consumption_evidence_appeared",
    "ambiguous_submission_boundary",
    "native_state_inconsistent",
    "exclusivity_not_established",
    "writer_race_possible",
    "review_required",
)

QUIESCENCE_STATES = ("quiescent", "not_quiescent", "unknown_review_required")
QUIESCENCE_REASONS = (
    "no_provider_or_local_continuation",
    "provider_continuation_remains",
    "local_continuation_remains",
    "snapshot_invalid",
    "writer_race_possible",
    "native_state_inconsistent",
)

ACTION_RELATIONSHIPS = ("independent", "superseded", "blocking")
TERMINAL_OUTCOMES = (
    "nonterminal",
    "delivery_complete",
    "policy_stopped",
    "review_required",
    "budget_exhausted",
    "ambiguous",
    "failed",
)
CLOSEOUT_DISPOSITIONS = (
    "closed",
    "continuation_required",
    "review_required",
    "ambiguous",
)

EVENT_NAMES = (
    "run.started",
    "run.resumed",
    "run.detached",
    "pass.prepared",
    "authorization.awaiting",
    "authorization.granted",
    "authorization.denied_providerless",
    "provider.submission_started",
    "provider.identity_recorded",
    "provider.waiting",
    "provider.completed",
    "qa.started",
    "qa.completed",
    "retry.decided",
    "polish.decided",
    "critic.decided",
    "checkpoint.committed",
    "terminal.transitioned",
    "closeout.completed",
    "execution.failed",
    "event_sink.warning",
)

EVENT_SEVERITIES = ("debug", "info", "warning", "error")

# This is presentation order only. It does not authorize or imply execution.
ACTION_STATE_PRESENTATION_ORDER = {
    state: index for index, state in enumerate(PROVIDER_ACTION_STATES)
}

# Payload-bearing fields are forbidden from every public event envelope.
PROHIBITED_EVENT_FIELDS = frozenset({
    "prompt",
    "request_body",
    "response_body",
    "provider_response",
    "birth_date",
    "birth_datetime",
    "birth_latitude",
    "birth_longitude",
    "birth_location",
    "lease_token",
    "api_key",
    "authorization_token",
})


def action_presentation_key(action: dict[str, Any]) -> tuple[Any, ...]:
    """Return stable display order without expressing execution dependency."""
    binding = action.get("binding") or {}
    return (
        str(binding.get("route", "")),
        int(action.get("attempt", 0)),
        ACTION_STATE_PRESENTATION_ORDER.get(str(action.get("state")), 999),
        str(action.get("action_id", "")),
    )


def canonical_contract_json(value: Any) -> str:
    """Serialize a contract deterministically for fixtures and hashing."""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def observation_transition_errors(
    requested: dict[str, Any], decision_basis: dict[str, Any]
) -> list[str]:
    """Validate permitted strengthening from API observation to SBE decision basis.

    Revision, snapshot, logical root, and validation facts cannot change. The
    decision may have a later timestamp and may strengthen declared exclusivity to
    established exclusivity. It may never weaken exclusivity or introduce a race.
    """
    errors: list[str] = []
    invariant_fields = (
        "operator_state_revision",
        "snapshot_sha256",
        "logical_workspace_root",
        "snapshot_complete",
        "inventory_valid",
    )
    for field in invariant_fields:
        if requested.get(field) != decision_basis.get(field):
            errors.append(field)
    requested_access = requested.get("native_exclusive_access")
    decision_access = decision_basis.get("native_exclusive_access")
    permitted_access = {
        "established": {"established"},
        "declared": {"declared", "established"},
        "not_established": {"not_established", "established"},
        "unknown": {"unknown", "declared", "established"},
    }
    if decision_access not in permitted_access.get(requested_access, set()):
        errors.append("native_exclusive_access")
    if decision_basis.get("writer_race_possible"):
        errors.append("writer_race_possible")
    return errors


def observation_transition_errors(
    requested: dict[str, Any], decision_basis: dict[str, Any]
) -> list[str]:
    """Validate permitted strengthening from API observation to SBE decision basis.

    Revision, snapshot, logical root, and validation facts cannot change. The
    decision may have a later timestamp and may strengthen declared exclusivity to
    established exclusivity. It may never weaken exclusivity or introduce a race.
    """
    errors: list[str] = []
    invariant_fields = (
        "operator_state_revision",
        "snapshot_sha256",
        "logical_workspace_root",
        "snapshot_complete",
        "inventory_valid",
    )
    for field in invariant_fields:
        if requested.get(field) != decision_basis.get(field):
            errors.append(field)
    requested_access = requested.get("native_exclusive_access")
    decision_access = decision_basis.get("native_exclusive_access")
    permitted_access = {
        "established": {"established"},
        "declared": {"declared", "established"},
        "not_established": {"not_established", "established"},
        "unknown": {"unknown", "declared", "established"},
    }
    if decision_access not in permitted_access.get(requested_access, set()):
        errors.append("native_exclusive_access")
    if decision_basis.get("writer_race_possible"):
        errors.append("writer_race_possible")
    return errors


def prohibited_event_paths(value: Any, prefix: str = "$") -> list[str]:
    """Return paths whose field names are prohibited in event envelopes."""
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            if str(key).lower() in PROHIBITED_EVENT_FIELDS:
                findings.append(path)
            findings.extend(prohibited_event_paths(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(prohibited_event_paths(child, f"{prefix}[{index}]"))
    return findings
