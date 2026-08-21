"""Public vocabulary for lifecycle inspection, denial, closeout, and events.

This module defines wire vocabulary only.  It deliberately does not inspect or
mutate a run; those operations are introduced by later sprint slices.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA = (
    "astrowoof.provider_negative_authorization_request.v0.1"
)
NEGATIVE_AUTHORIZATION_RESULT_SCHEMA = (
    "astrowoof.provider_negative_authorization_result.v0.1"
)
NEGATIVE_AUTHORIZATION_RESULT_SCHEMA_V0_2 = (
    "astrowoof.provider_negative_authorization_result.v0.2"
)
NEGATIVE_AUTHORIZATION_RESULT_SCHEMA_V0_2 = (
    "astrowoof.provider_negative_authorization_result.v0.2"
)
BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA = (
    "astrowoof.provider_negative_authorization_batch_request.v0.1"
)
BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA = (
    "astrowoof.provider_negative_authorization_batch_result.v0.1"
)
BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA_V0_2 = (
    "astrowoof.provider_negative_authorization_batch_result.v0.2"
)
BATCH_NEGATIVE_AUTHORIZATION_RESULT_SCHEMA_V0_2 = (
    "astrowoof.provider_negative_authorization_batch_result.v0.2"
)
BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS = 32
OUTSTANDING_ACTION_INVENTORY_SCHEMA = (
    "astrowoof.provider_action_inventory.v0.1"
)
LIFECYCLE_INSPECTION_SCHEMA = "astrowoof.authoring_lifecycle_inspection.v0.5"
LIFECYCLE_INSPECTION_SCHEMA_V0_4 = (
    "astrowoof.authoring_lifecycle_inspection.v0.4"
)
LIFECYCLE_INSPECTION_SCHEMA_V0_3 = (
    "astrowoof.authoring_lifecycle_inspection.v0.3"
)
LIFECYCLE_INSPECTION_SCHEMA_V0_2 = (
    "astrowoof.authoring_lifecycle_inspection.v0.2"
)
LIFECYCLE_INSPECTION_SCHEMA_HISTORICAL = (
    "astrowoof.authoring_lifecycle_inspection.v0.1"
)
PROVIDER_RECONCILIATION_POLICY_SCHEMA = (
    "astrowoof.provider_reconciliation_policy.v0.2"
)
PROVIDER_RECONCILIATION_POLICY_SCHEMA_V0_1 = (
    "astrowoof.provider_reconciliation_policy.v0.1"
)
PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA = (
    "astrowoof.provider_reconciliation_cycle_result.v0.2"
)
PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA_V0_1 = (
    "astrowoof.provider_reconciliation_cycle_result.v0.1"
)
PROVIDER_RECONCILIATION_POLICY = {
    "schema_version": PROVIDER_RECONCILIATION_POLICY_SCHEMA,
    "mechanisms": {
        "response": {
            "delays_seconds": [15, 30, 60, 120, 240, 300],
            "maximum_delay_seconds": 300,
            "provider_io_wall_clock_limit_seconds": 20,
            "provider_request_timeout_seconds": 15,
            "maximum_due_actions_per_cycle": 4,
            "maximum_parallel_requests": 4,
        },
        "batch": {
            "delays_seconds": [60, 120, 300, 600, 900, 1800],
            "maximum_delay_seconds": 1800,
            "provider_io_wall_clock_limit_seconds": 40,
            "provider_request_timeout_seconds": 15,
            "maximum_due_actions_per_cycle": 1,
            "maximum_parallel_requests": 2,
        },
    },
    "jitter": "none",
}
PROVIDER_ROUTE_FAMILIES = ("exact_natal", "bounded_natal")
PROVIDER_OPERATION_KINDS = ("response", "batch")
COST_DISPOSITIONS = (
    "provider_usage_reported",
    "provider_usage_unavailable_billing_reconciliation_pending",
    "no_provider_work_consumed",
    "not_applicable_provider_pending",
)
CONSUMER_AUTHORITY_STATES = ("none", "retain")
CONSUMER_AUTHORITY_RETENTION_REASONS = (
    "provider_operation_pending",
    "provider_output_integrity_review",
    "provider_submission_ambiguous",
    "billing_reconciliation_pending",
)
EXECUTION_CAPACITY_DISPOSITIONS = (
    "continue_local_cycle",
    "release_until_due",
    "await_external_authority",
    "retain_for_review",
    "terminal",
    "unsupported_retain_capacity",
)
EXECUTION_CAPACITY_REASON_CODES = (
    "local_work_ready",
    "provider_reconciliation_due",
    "known_provider_work_pending",
    "provider_reconciliation_not_due",
    "spend_authorization_required",
    "terminal_native_outcome",
    "snapshot_invalid",
    "writer_or_lease_not_exclusive",
    "provider_submission_ambiguous",
    "provider_identity_conflict",
    "native_review_required",
    "route_or_stage_not_supported",
    "reconciliation_timing_missing",
)
EXECUTION_BRANCH_COMMANDS = (
    "ordinary_resume",
    "provider_reconciliation_cycle",
    "await_external_authority",
    "none",
)
EXECUTION_BRANCH_REASON_CODES = (
    "ordinary_local_continuation_ready",
    "provider_reconciliation_not_due",
    "provider_reconciliation_due",
    "spend_authorization_required",
    "terminal_or_no_continuation",
    "native_review_or_ambiguity",
    "unsupported_native_evidence",
)
PROVIDER_CUSTODY_STATES = (
    "none",
    "known_operations_pending",
    "completed_evidence_pending_local_work",
    "ambiguous_or_conflicting",
    "unsupported",
    "terminal_no_custody",
)
PROVIDER_CUSTODY_CLASSIFICATIONS = (
    "retain_consumer_authority",
    "completed_provider_evidence",
    "no_provider_custody",
    "ambiguous_review",
    "unsupported",
)
PROVIDER_CUSTODY_STAGES = (
    "authoring_initial",
    "creative_retry",
    "polish",
    "qualitative_critic",
    "qualitative_candidate",
)
PROVIDER_RECONCILIATION_CYCLE_OUTCOMES = (
    "not_due",
    "detached_provider_pending",
    "progressed_local",
    "awaiting_external_authority",
    "terminal",
    "review_required",
    "unsupported",
)
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
    "external_spend_authority_denied",
    "external_spend_reservation_unavailable",
    "external_product_policy_denied",
    "run_cancelled_before_submission",
)

DENIAL_TERMINAL_REASONS = (
    "external_spend_authority_denied",
    "external_spend_reservation_unavailable",
    "external_product_policy_denied",
    "run_cancelled_before_submission",
    "optional_stage_skipped",
    "delivery_complete",
    "no_run_transition",
)

RUN_TRANSITION_OUTCOMES = (
    "terminalized",
    "optional_stage_skipped",
    "delivery_status_preserved",
    "no_run_transition",
)

RUN_TRANSITION_TRIGGERS = (
    "required_action_providerless_denial",
    "optional_action_providerless_denial",
    "accepted_delivery_precedence",
)

DENIAL_TERMINAL_REASONS = (
    "external_spend_authority_denied",
    "external_spend_reservation_unavailable",
    "external_product_policy_denied",
    "run_cancelled_before_submission",
    "optional_stage_skipped",
    "delivery_complete",
    "no_run_transition",
)

RUN_TRANSITION_OUTCOMES = (
    "terminalized",
    "optional_stage_skipped",
    "delivery_status_preserved",
    "no_run_transition",
)

RUN_TRANSITION_TRIGGERS = (
    "required_action_providerless_denial",
    "optional_action_providerless_denial",
    "accepted_delivery_precedence",
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

BATCH_NEGATIVE_AUTHORIZATION_OUTCOMES = (
    "applied",
    "idempotent_replay",
    "stale_observation",
    "immutable_binding_mismatch",
    "unknown_action",
    "duplicate_action",
    "provider_identity_appeared",
    "provider_evidence_appeared",
    "consumption_evidence_appeared",
    "ambiguous_submission_boundary",
    "action_ineligible",
    "native_state_inconsistent",
    "exclusivity_not_established",
    "writer_race_possible",
    "review_required",
)

BATCH_ACTION_VALIDATION_OUTCOMES = (
    "eligible",
    "applied",
    "idempotent_replay",
    "not_evaluated",
    "immutable_binding_mismatch",
    "unknown_action",
    "duplicate_action",
    "provider_identity_appeared",
    "provider_evidence_appeared",
    "consumption_evidence_appeared",
    "ambiguous_submission_boundary",
    "action_ineligible",
    "native_state_inconsistent",
)

BATCH_NEGATIVE_AUTHORIZATION_REVIEW_REASONS = (
    "batch_refused_by_other_member",
    "shared_precondition_not_evaluated",
    "unknown_action",
    "duplicate_action",
    "action_ineligible",
    *AMBIGUITY_REVIEW_REASONS,
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
    "authorization.denied_providerless_batch",
    "provider.submission_started",
    "provider.identity_recorded",
    "provider.waiting",
    "provider.completed",
    "provider.reconciliation_observed",
    "lifecycle.branch_selected",
    "external_authority.request_selected",
    "external_authority.fence_validated",
    "external_authority.intent_committed",
    "external_authority.provider_create_permitted",
    "external_authority.refused",
    "native.result_published",
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
    "bounded.admission.completed",
    "bounded.family.validated",
    "bounded.selection.completed",
    "bounded.disposition.completed",
    "bounded.artifact.committed",
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


def validate_lifecycle_inspection_v04(value: dict[str, Any]) -> None:
    """Reject contradictory v0.4 branch/capacity/continuation projections."""
    if value.get("schema_version") != LIFECYCLE_INSPECTION_SCHEMA_V0_4:
        raise ValueError("Unsupported lifecycle inspection schema")
    branch = value.get("execution_branch") or {}
    capacity = value.get("execution_capacity") or {}
    custody = value.get("provider_custody") or {}
    terminal = value.get("terminal") or {}
    dependencies = value.get("local_dependencies") or []
    command = branch.get("command")
    reason = branch.get("reason_code")
    errors: list[str] = []
    if command == "provider_reconciliation_cycle":
        if not terminal.get("provider_continuation_remains"):
            errors.append("provider_continuation_remains")
        if terminal.get("local_continuation_remains") or dependencies:
            errors.append("local_continuation_must_be_false")
        if reason == "provider_reconciliation_due":
            if not branch.get("eligible_now"):
                errors.append("eligible_now")
            if capacity.get("reason_code") != "provider_reconciliation_due":
                errors.append("capacity_reason_code")
            if branch.get("not_before") is not None:
                errors.append("not_before")
            if branch.get("action_ids") != custody.get("next_due_action_ids"):
                errors.append("next_due_action_ids")
            if not branch.get("action_ids") or len(branch["action_ids"]) > 4:
                errors.append("bounded_due_subset")
        elif reason == "provider_reconciliation_not_due":
            if branch.get("eligible_now"):
                errors.append("eligible_now")
            if capacity.get("disposition") != "release_until_due":
                errors.append("capacity_disposition")
            if branch.get("not_before") != capacity.get("resume_not_before"):
                errors.append("resume_not_before")
            if branch.get("action_ids") != custody.get("action_ids"):
                errors.append("provider_action_ids")
        else:
            errors.append("provider_reconciliation_reason")
    elif command == "ordinary_resume":
        if not terminal.get("local_continuation_remains") or not dependencies:
            errors.append("ordinary_local_continuation")
        if capacity.get("disposition") != "continue_local_cycle":
            errors.append("capacity_disposition")
        if not branch.get("eligible_now") or branch.get("action_ids"):
            errors.append("ordinary_branch_shape")
    elif command == "await_external_authority":
        if capacity.get("disposition") != "await_external_authority":
            errors.append("capacity_disposition")
        if branch.get("eligible_now"):
            errors.append("eligible_now")
    elif command != "none":
        errors.append("command")
    if errors:
        raise ValueError(
            "Contradictory lifecycle inspection fields: " + ", ".join(errors)
        )


def external_authority_branch_predicate_failures(
    value: dict[str, Any],
) -> list[str]:
    """Return deterministic safe names for violated v0.5 authority predicates."""
    request = value.get("external_authority_request")
    refusal = value.get("external_authority_refusal")
    branch = value.get("execution_branch") or {}
    capacity = value.get("execution_capacity") or {}
    command = branch.get("command")
    errors: list[str] = []
    if request is not None and refusal is not None:
        errors.extend(("request_presence", "refusal_presence"))
    if command == "await_external_authority":
        if branch.get("eligible_now") is not False:
            errors.append("eligible_now")
        if branch.get("reason_code") != "spend_authorization_required":
            errors.append("branch_reason_code")
        if capacity.get("disposition") != "await_external_authority":
            errors.append("capacity_disposition")
        if capacity.get("reason_code") != "spend_authorization_required":
            errors.append("capacity_reason_code")
        if capacity.get("local_work_ready_now") is not False:
            errors.append("local_work_ready_now")
        if capacity.get("resume_not_before") is not None:
            errors.append("capacity_resume_not_before")
        if not branch.get("action_ids"):
            errors.append("branch_action_inventory")
        if branch.get("not_before") is not None:
            errors.append("branch_not_before")
        if request is None:
            errors.append("request_presence")
        if refusal is not None:
            errors.append("refusal_presence")
        if isinstance(request, dict) and (
            value.get("run_id") != request.get("run_id")
            or value.get("observation") != request.get("observation")
            or branch.get("action_ids") != request.get("ordered_action_ids")
        ):
            errors.append("outer_request_join")
    elif refusal is not None:
        if command != "none":
            errors.append("refusal_presence")
        if branch.get("eligible_now") is not False:
            errors.append("eligible_now")
        if branch.get("reason_code") != "native_review_or_ambiguity":
            errors.append("branch_reason_code")
        if branch.get("action_ids"):
            errors.append("branch_action_inventory")
        if branch.get("not_before") is not None:
            errors.append("branch_not_before")
        if capacity.get("disposition") != "retain_for_review":
            errors.append("capacity_disposition")
        if capacity.get("reason_code") != "native_review_required":
            errors.append("capacity_reason_code")
        if capacity.get("local_work_ready_now") is not False:
            errors.append("local_work_ready_now")
        if capacity.get("resume_not_before") is not None:
            errors.append("capacity_resume_not_before")
        if request is not None:
            errors.append("request_presence")
        if isinstance(refusal, dict) and (
            value.get("run_id") != refusal.get("run_id")
            or value.get("observation") != refusal.get("observation")
        ):
            errors.append("outer_refusal_join")
    elif request is not None:
        errors.append("request_presence")
    return sorted(set(errors))


def validate_lifecycle_inspection_v05(value: dict[str, Any]) -> None:
    """Validate v0.5 plus its exact embedded external-authority decision."""
    if value.get("schema_version") != LIFECYCLE_INSPECTION_SCHEMA:
        raise ValueError("Unsupported lifecycle inspection schema")
    base = {
        key: item for key, item in value.items()
        if key not in {"external_authority_request", "external_authority_refusal"}
    }
    base["schema_version"] = LIFECYCLE_INSPECTION_SCHEMA_V0_4
    validate_lifecycle_inspection_v04(base)
    request = value.get("external_authority_request")
    refusal = value.get("external_authority_refusal")
    if request is not None and refusal is not None:
        raise ValueError("Lifecycle request and refusal are mutually exclusive")
    branch = value.get("execution_branch") or {}
    command = branch.get("command")
    conditional_errors = external_authority_branch_predicate_failures(value)
    if conditional_errors:
        raise ValueError(
            "Contradictory lifecycle external-authority fields: "
            + ", ".join(conditional_errors)
        )
    if request is not None:
        from .external_authority import validate_external_authority_request

        validate_external_authority_request(request)
        if (
            value.get("run_id") != request.get("run_id")
            or value.get("observation") != request.get("observation")
            or branch.get("command") != "await_external_authority"
            or branch.get("action_ids") != request.get("ordered_action_ids")
        ):
            raise ValueError("Lifecycle external-authority request does not join")
    if refusal is not None:
        from .external_authority import validate_external_authority_refusal

        validate_external_authority_refusal(refusal)
        if (
            value.get("run_id") != refusal.get("run_id")
            or value.get("observation") != refusal.get("observation")
            or branch.get("command") != "none"
            or branch.get("eligible_now")
            or branch.get("action_ids")
        ):
            raise ValueError("Lifecycle external-authority refusal does not join")
    if command == "await_external_authority" and request is None:
        raise ValueError("Await-external-authority branch lacks its exact request")


def canonical_contract_json(value: Any) -> str:
    """Serialize a contract deterministically for fixtures and hashing."""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def batch_negative_authorization_request_sha256(request: dict[str, Any]) -> str:
    """Hash the exact versioned batch request using canonical contract JSON.

    Array order is deliberately preserved. Object-key order and insignificant JSON
    whitespace are deliberately ignored.
    """
    return hashlib.sha256(canonical_contract_json(request).encode("utf-8")).hexdigest()


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
