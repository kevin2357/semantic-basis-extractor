"""Strict provider-free transition traces for joint lifecycle simulation."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from importlib import resources
from typing import Any, Mapping


SCHEMA_VERSION = "astrowoof.lifecycle_adversarial_trace.v1"
SCHEMA_RESOURCE = "lifecycle-adversarial-trace.v1.schema.json"
FIXTURE_NAMES = {
    "review-no-action-cycle.v1.json",
    "provider-not-due-legitimate-wait.v1.json",
    "contradictory-command-custody.v1.json",
}

CONSTRUCTION_CLASSES = {
    "legally_reached", "historical_shape", "synthetic_invalid_state",
}
ROUTES = {"exact_natal", "bounded_natal"}
MECHANISMS = {"response", "batch", "none"}
STAGES = {
    "authoring_initial", "creative_retry", "polish", "qualitative_critic",
    "qualitative_candidate", "closeout",
}
SUPPORT_CLASSES = {"supported", "explicitly_refused", "deferred"}
COMMANDS = {
    "ordinary_resume", "provider_reconciliation_cycle",
    "await_external_authority", "none",
}
CAPACITY_DISPOSITIONS = {
    "continue_local_cycle", "release_until_due", "await_external_authority",
    "retain_for_review", "terminal", "unsupported_retain_capacity",
}
PROVIDER_CUSTODY = {
    "none", "known_operations_pending", "completed_local_work",
    "ambiguous_or_conflicting", "terminal",
}
EXTERNAL_AUTHORITY = {"none", "awaiting", "granted", "refused"}
RUN_DISPOSITIONS = {"queued", "running", "succeeded", "failed", "review_required"}
JOB_DISPOSITIONS = {"available", "leased", "deferred", "succeeded", "failed"}
LEASE_DISPOSITIONS = {"none", "active", "released", "expired"}
CAPACITY_STATES = {"none", "allocated", "released"}
RESERVATION_STATES = {"none", "retained", "releasable", "settled", "review"}
PROVIDER_STATES = {
    "not_entered", "entered_identity_unknown", "pending", "completed", "failed",
    "cancelled", "expired", "malformed", "identity_conflict",
}
ACTORS = {
    "scheduler", "claimed_worker", "replacement_worker", "sbe_command",
    "external_authority_service", "fake_provider", "lease_clock_reaper",
    "storage_publisher", "operator", "crash_injector",
}
EVENT_KINDS = {
    "inspect_lifecycle", "ingest_native_result", "ordinary_resume",
    "provider_reconciliation_cycle", "await_external_authority", "advance_time",
    "claim_job", "release_capacity", "expire_lease", "provider_transition",
    "publish", "operator_command", "interrupt",
}
TIME_EVENTS = {"none", "advance_base_unit", "advance_duration", "advance_to_boundary"}
CLASSIFICATIONS = {
    "productive", "legitimate_wait", "idempotent_replay", "stutter", "cycle",
    "refused", "contradictory_evidence",
}
CONTRADICTIONS = {
    "command_local_inventory_mismatch", "command_custody_mismatch",
    "custody_operation_mismatch", "wait_schedule_mismatch",
    "terminal_command_mismatch", "review_command_mismatch",
}
REFUSAL_REASONS = {
    "event_not_enabled", "stale_observation", "unsupported_route",
    "invalid_input", "contradictory_input",
}
REASON_CODES = {
    "native_review_or_ambiguity", "provider_reconciliation_not_due",
    "local_work_ready", "spend_authorization_required", "terminal",
    "unsupported_contract",
}
SEMANTIC_FENCE_KINDS = {
    "checkpoint_basis", "action_inventory", "authority_request",
    "provider_custody", "publication",
}
EVIDENCE_KINDS = {
    "lifecycle_inspection", "native_result", "publication_receipt",
    "qualification_fixture",
}

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_TRACE_ID = re.compile(r"^simtrace_[0-9a-f]{24}$")
_OPAQUE_REF = re.compile(r"^fixture:[a-z0-9][a-z0-9._-]{2,95}$")
_OPERATION_KEY = re.compile(r"^opkey_[0-9a-f]{24}$")
_SIM_OPERATION = re.compile(r"^simop_[0-9a-f]{24}$")

TOP_KEYS = {
    "schema_version", "trace_id", "trace_sha256", "construction_class",
    "package", "clock", "route_cell", "public_evidence", "before", "event",
    "after", "expected", "privacy",
}
PACKAGE_KEYS = {"name", "version", "schema_resource"}
CLOCK_KEYS = {
    "logical_step_before", "logical_step_after", "simulated_time_before",
    "simulated_time_after", "time_event",
}
ROUTE_KEYS = {"route_family", "provider_mechanism", "stage", "support"}
EVIDENCE_KEYS = {"kind", "schema_version", "sha256", "opaque_ref"}
STATE_KEYS = {
    "raw_evidence_sha256", "semantic_fingerprint_sha256", "native",
    "api_fixture", "provider_fixture",
}
NATIVE_KEYS = {
    "native_run_ref", "route_contract", "checkpoint_basis_sha256",
    "snapshot_sha256", "state_revision", "selected_command",
    "capacity_disposition", "reason_code", "local_operation_keys",
    "consumed_operation_keys", "provider_custody", "resume_not_before",
    "external_authority", "terminal", "review_required", "delivery_publishable",
    "semantic_fences",
}
SEMANTIC_FENCE_KEYS = {"kind", "sha256"}
API_KEYS = {
    "run_ref", "run_disposition", "job_disposition", "lease_disposition",
    "capacity_state", "reservation_state", "competing_eligible_run_count",
}
PROVIDER_KEYS = {"network_capability", "credential_capability", "operations"}
PROVIDER_OPERATION_KEYS = {"correlation_id", "state"}
EVENT_KEYS = {"actor", "kind", "enabled", "refusal_reason"}
EXPECTED_KEYS = {
    "classification", "declared_contradictions", "progress_witness",
    "starvation_witness", "side_effects",
}
PROGRESS_WITNESS_KEYS = {
    "prior_semantic_fingerprint_sha256", "prior_logical_step",
}
STARVATION_KEYS = {"victim_run_ref", "blocker_run_ref", "eligible_since_step", "witness_steps"}
SIDE_EFFECT_KEYS = {
    "scripted_provider_creates", "scripted_provider_retrievals",
    "external_network_calls", "lease_released", "capacity_released",
}
PRIVACY_KEYS = {
    "contains_prompt", "contains_provider_payload", "contains_raw_provider_id",
    "contains_workspace_path", "contains_credentials",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _trace_core(value: Mapping[str, Any]) -> dict[str, Any]:
    body = deepcopy(dict(value))
    body.pop("trace_id", None)
    body.pop("trace_sha256", None)
    return body


def derive_trace_sha256(value: Mapping[str, Any]) -> str:
    return canonical_sha256(_trace_core(value))


def derive_trace_id(value: Mapping[str, Any]) -> str:
    return "simtrace_" + derive_trace_sha256(value)[:24]


def semantic_fingerprint(state: Mapping[str, Any]) -> str:
    native = state["native"]
    semantic_native = {
        key: native[key]
        for key in NATIVE_KEYS - {
            "checkpoint_basis_sha256", "snapshot_sha256", "state_revision"
        }
    }
    return canonical_sha256({
        "api_fixture": state["api_fixture"],
        "native": semantic_native,
        "provider_fixture": state["provider_fixture"],
    })


def native_contradictions(state: Mapping[str, Any]) -> list[str]:
    """Return closed native contradictions without trusting a trace declaration."""

    if not isinstance(state, Mapping) or "native" not in state:
        raise ValueError("state must contain native evidence")
    return _validate_native(state["native"], "state.native")


def finalize_adversarial_trace(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    for label in ("before", "after"):
        state = result[label]
        state["semantic_fingerprint_sha256"] = semantic_fingerprint(state)
    result["trace_sha256"] = derive_trace_sha256(result)
    result["trace_id"] = derive_trace_id(result)
    validate_adversarial_trace(result)
    return result


def canonical_adversarial_trace_bytes(value: Mapping[str, Any]) -> bytes:
    validate_adversarial_trace(value)
    return _canonical_bytes(value)


def _exact(value: Mapping[str, Any], keys: set[str], label: str) -> None:
    if set(value) != keys:
        raise ValueError(f"{label} keys differ: missing={sorted(keys-set(value))} extra={sorted(set(value)-keys)}")


def _member(value: Any, options: set[str], label: str) -> str:
    if not isinstance(value, str) or value not in options:
        raise ValueError(f"{label} is unsupported")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _hex64(value: Any, label: str) -> str:
    if not isinstance(value, str) or _HEX64.fullmatch(value) is None:
        raise ValueError(f"{label} must be lowercase SHA-256")
    return value


def _uint(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer")
    return value


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _instant(value: Any, label: str) -> str:
    text = _string(value, label)
    if not text.endswith("Z"):
        raise ValueError(f"{label} must use canonical UTC Z form")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} is invalid") from exc
    canonical = parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    if text != canonical:
        raise ValueError(f"{label} is not canonical to whole UTC seconds")
    return text


def _optional_instant(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _instant(value, label)


def _unique_strings(values: Any, pattern: re.Pattern[str], label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(item, str) or pattern.fullmatch(item) is None for item in values):
        raise ValueError(f"{label} contains invalid identities")
    if len(values) != len(set(values)):
        raise ValueError(f"{label} contains duplicates")
    return values


def _validate_route_cell(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("route_cell must be an object")
    _exact(value, ROUTE_KEYS, "route_cell")
    _member(value["route_family"], ROUTES, "route_family")
    mechanism = _member(value["provider_mechanism"], MECHANISMS, "provider_mechanism")
    stage = _member(value["stage"], STAGES, "stage")
    support = _member(value["support"], SUPPORT_CLASSES, "support")
    expected = "supported"
    if mechanism == "batch" and stage not in {"authoring_initial", "creative_retry", "closeout"}:
        expected = "explicitly_refused"
    if mechanism == "none" and stage != "closeout":
        expected = "explicitly_refused"
    if mechanism in {"response", "batch"} and stage == "closeout":
        expected = "supported"
    if support != expected:
        raise ValueError("route_cell support contradicts the frozen v1 matrix")


def _validate_native(value: Any, label: str) -> list[str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    _exact(value, NATIVE_KEYS, label)
    native_run_ref = _string(value["native_run_ref"], f"{label}.native_run_ref")
    if _OPAQUE_REF.fullmatch(native_run_ref) is None:
        raise ValueError(f"{label}.native_run_ref must be an opaque fixture reference")
    _string(value["route_contract"], f"{label}.route_contract")
    _hex64(value["checkpoint_basis_sha256"], f"{label}.checkpoint_basis_sha256")
    _hex64(value["snapshot_sha256"], f"{label}.snapshot_sha256")
    _uint(value["state_revision"], f"{label}.state_revision")
    command = _member(value["selected_command"], COMMANDS, f"{label}.selected_command")
    disposition = _member(value["capacity_disposition"], CAPACITY_DISPOSITIONS, f"{label}.capacity_disposition")
    _member(value["reason_code"], REASON_CODES, f"{label}.reason_code")
    local = _unique_strings(value["local_operation_keys"], _OPERATION_KEY, f"{label}.local_operation_keys")
    consumed = _unique_strings(value["consumed_operation_keys"], _OPERATION_KEY, f"{label}.consumed_operation_keys")
    custody = _member(value["provider_custody"], PROVIDER_CUSTODY, f"{label}.provider_custody")
    due = _optional_instant(value["resume_not_before"], f"{label}.resume_not_before")
    authority = _member(value["external_authority"], EXTERNAL_AUTHORITY, f"{label}.external_authority")
    terminal = _bool(value["terminal"], f"{label}.terminal")
    review = _bool(value["review_required"], f"{label}.review_required")
    _bool(value["delivery_publishable"], f"{label}.delivery_publishable")
    fences = value["semantic_fences"]
    if not isinstance(fences, list) or not fences:
        raise ValueError(f"{label}.semantic_fences must be nonempty")
    fence_kinds: list[str] = []
    for index, fence in enumerate(fences):
        if not isinstance(fence, Mapping):
            raise ValueError(f"{label}.semantic_fences[{index}] must be an object")
        _exact(fence, SEMANTIC_FENCE_KEYS, f"{label}.semantic_fences[{index}]")
        fence_kinds.append(_member(
            fence["kind"], SEMANTIC_FENCE_KINDS,
            f"{label}.semantic_fences[{index}].kind",
        ))
        _hex64(fence["sha256"], f"{label}.semantic_fences[{index}].sha256")
    if fence_kinds != sorted(fence_kinds) or len(fence_kinds) != len(set(fence_kinds)):
        raise ValueError(f"{label}.semantic_fences must have unique lexical kind order")
    checkpoint_fences = [
        item for item in fences if item["kind"] == "checkpoint_basis"
    ]
    if len(checkpoint_fences) != 1 or checkpoint_fences[0]["sha256"] != value["checkpoint_basis_sha256"]:
        raise ValueError(f"{label}.semantic_fences must bind the checkpoint basis")
    errors: list[str] = []
    if set(local) & set(consumed):
        errors.append("command_local_inventory_mismatch")
    if (command == "ordinary_resume") != bool(local):
        errors.append("command_local_inventory_mismatch")
    if (command == "provider_reconciliation_cycle") != (custody == "known_operations_pending"):
        errors.append("command_custody_mismatch")
    if (custody == "known_operations_pending") != (due is not None):
        errors.append("wait_schedule_mismatch")
    if (command == "await_external_authority") != (authority == "awaiting"):
        errors.append("command_custody_mismatch")
    if terminal and command != "none":
        errors.append("terminal_command_mismatch")
    if review and command != "none":
        errors.append("review_command_mismatch")
    if disposition == "release_until_due" and custody != "known_operations_pending":
        errors.append("wait_schedule_mismatch")
    return sorted(set(errors))


def _validate_api(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    _exact(value, API_KEYS, label)
    run_ref = _string(value["run_ref"], f"{label}.run_ref")
    if _OPAQUE_REF.fullmatch(run_ref) is None:
        raise ValueError(f"{label}.run_ref must be an opaque fixture reference")
    _member(value["run_disposition"], RUN_DISPOSITIONS, f"{label}.run_disposition")
    job = _member(value["job_disposition"], JOB_DISPOSITIONS, f"{label}.job_disposition")
    lease = _member(value["lease_disposition"], LEASE_DISPOSITIONS, f"{label}.lease_disposition")
    capacity = _member(value["capacity_state"], CAPACITY_STATES, f"{label}.capacity_state")
    _member(value["reservation_state"], RESERVATION_STATES, f"{label}.reservation_state")
    _uint(value["competing_eligible_run_count"], f"{label}.competing_eligible_run_count")
    if (job == "leased") != (lease == "active"):
        raise ValueError(f"{label} lease/job contradiction")
    if capacity == "allocated" and job != "leased":
        raise ValueError(f"{label} capacity/job contradiction")


def _validate_provider(value: Any, label: str, custody: str) -> list[str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    _exact(value, PROVIDER_KEYS, label)
    if _bool(value["network_capability"], f"{label}.network_capability"):
        raise ValueError("provider-free trace cannot have network capability")
    if _bool(value["credential_capability"], f"{label}.credential_capability"):
        raise ValueError("provider-free trace cannot have credential capability")
    operations = value["operations"]
    if not isinstance(operations, list):
        raise ValueError(f"{label}.operations must be an array")
    correlations: list[str] = []
    for index, operation in enumerate(operations):
        if not isinstance(operation, Mapping):
            raise ValueError(f"{label}.operations[{index}] must be an object")
        _exact(operation, PROVIDER_OPERATION_KEYS, f"{label}.operations[{index}]")
        correlation = _string(operation["correlation_id"], "provider correlation")
        if _SIM_OPERATION.fullmatch(correlation) is None:
            raise ValueError("provider correlation must be an opaque simulation identity")
        correlations.append(correlation)
        _member(operation["state"], PROVIDER_STATES, "provider operation state")
    if len(correlations) != len(set(correlations)):
        raise ValueError("provider fixture contains duplicate correlations")
    errors: list[str] = []
    states = {operation["state"] for operation in operations}
    if custody == "none" and operations:
        errors.append("custody_operation_mismatch")
    elif custody == "known_operations_pending" and (
        not operations or not states <= {"pending"}
    ):
        errors.append("custody_operation_mismatch")
    elif custody == "completed_local_work" and (
        not operations or not states <= {"completed"}
    ):
        errors.append("custody_operation_mismatch")
    elif custody == "ambiguous_or_conflicting" and (
        not operations or not states <= {
            "entered_identity_unknown", "malformed", "identity_conflict"
        }
    ):
        errors.append("custody_operation_mismatch")
    elif custody == "terminal" and (
        not operations or not states <= {"failed", "cancelled", "expired"}
    ):
        errors.append("custody_operation_mismatch")
    return errors


def _validate_state(value: Any, label: str) -> list[str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    _exact(value, STATE_KEYS, label)
    _hex64(value["raw_evidence_sha256"], f"{label}.raw_evidence_sha256")
    _hex64(value["semantic_fingerprint_sha256"], f"{label}.semantic_fingerprint_sha256")
    native_errors = _validate_native(value["native"], f"{label}.native")
    _validate_api(value["api_fixture"], f"{label}.api_fixture")
    provider_errors = _validate_provider(
        value["provider_fixture"], f"{label}.provider_fixture", value["native"]["provider_custody"]
    )
    if value["semantic_fingerprint_sha256"] != semantic_fingerprint(value):
        raise ValueError(f"{label} semantic fingerprint mismatch")
    return sorted(set(native_errors + provider_errors))


def validate_adversarial_trace(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("adversarial trace must be an object")
    _exact(value, TOP_KEYS, "trace")
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported adversarial trace schema")
    if not isinstance(value["trace_id"], str) or _TRACE_ID.fullmatch(value["trace_id"]) is None:
        raise ValueError("invalid trace_id")
    _hex64(value["trace_sha256"], "trace_sha256")
    if value["trace_sha256"] != derive_trace_sha256(value) or value["trace_id"] != derive_trace_id(value):
        raise ValueError("trace identity mismatch")
    construction = _member(value["construction_class"], CONSTRUCTION_CLASSES, "construction_class")
    package = value["package"]
    if not isinstance(package, Mapping):
        raise ValueError("package must be an object")
    _exact(package, PACKAGE_KEYS, "package")
    if package["name"] != "astrowoof-natal-authoring" or package["schema_resource"] != SCHEMA_RESOURCE:
        raise ValueError("package identity mismatch")
    _string(package["version"], "package.version")
    clock = value["clock"]
    if not isinstance(clock, Mapping):
        raise ValueError("clock must be an object")
    _exact(clock, CLOCK_KEYS, "clock")
    before_step = _uint(clock["logical_step_before"], "clock.logical_step_before")
    if _uint(clock["logical_step_after"], "clock.logical_step_after") != before_step + 1:
        raise ValueError("logical step must advance exactly once")
    before_time = _instant(clock["simulated_time_before"], "clock.simulated_time_before")
    after_time = _instant(clock["simulated_time_after"], "clock.simulated_time_after")
    time_event = _member(clock["time_event"], TIME_EVENTS, "clock.time_event")
    if (time_event == "none") != (before_time == after_time):
        raise ValueError("clock event contradicts simulated time")
    if time_event != "none" and after_time <= before_time:
        raise ValueError("simulated time must advance")
    _validate_route_cell(value["route_cell"])
    evidence = value["public_evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("public_evidence must be nonempty")
    refs: list[str] = []
    for index, item in enumerate(evidence):
        if not isinstance(item, Mapping):
            raise ValueError("public evidence member must be an object")
        _exact(item, EVIDENCE_KEYS, f"public_evidence[{index}]")
        _member(item["kind"], EVIDENCE_KINDS, "public evidence kind")
        _string(item["schema_version"], "public evidence schema")
        _hex64(item["sha256"], "public evidence sha256")
        ref = _string(item["opaque_ref"], "public evidence opaque_ref")
        if _OPAQUE_REF.fullmatch(ref) is None:
            raise ValueError("public evidence reference is not opaque")
        refs.append(ref)
    if len(refs) != len(set(refs)):
        raise ValueError("public evidence references must be unique")
    before_errors = _validate_state(value["before"], "before")
    after_errors = _validate_state(value["after"], "after")
    event = value["event"]
    if not isinstance(event, Mapping):
        raise ValueError("event must be an object")
    _exact(event, EVENT_KEYS, "event")
    _member(event["actor"], ACTORS, "event.actor")
    _member(event["kind"], EVENT_KINDS, "event.kind")
    enabled = _bool(event["enabled"], "event.enabled")
    if event["refusal_reason"] is not None:
        _member(event["refusal_reason"], REFUSAL_REASONS, "event.refusal_reason")
    expected = value["expected"]
    if not isinstance(expected, Mapping):
        raise ValueError("expected must be an object")
    _exact(expected, EXPECTED_KEYS, "expected")
    classification = _member(expected["classification"], CLASSIFICATIONS, "expected.classification")
    if classification == "refused":
        if enabled or event["refusal_reason"] is None:
            raise ValueError("refused classification requires a disabled event and closed refusal reason")
    elif not enabled or event["refusal_reason"] is not None:
        raise ValueError("non-refused classification requires an enabled event without refusal reason")
    contradictions = expected["declared_contradictions"]
    if not isinstance(contradictions, list) or any(item not in CONTRADICTIONS for item in contradictions):
        raise ValueError("declared contradictions are invalid")
    if len(contradictions) != len(set(contradictions)):
        raise ValueError("declared contradictions contain duplicates")
    actual_errors = sorted(set(before_errors + after_errors))
    if construction == "synthetic_invalid_state":
        if classification != "contradictory_evidence" or sorted(contradictions) != actual_errors or not actual_errors:
            raise ValueError("synthetic invalid trace must declare its exact contradictions")
    elif actual_errors or contradictions or classification == "contradictory_evidence":
        raise ValueError("legal/historical trace cannot contain contradictory state")
    before_fp = value["before"]["semantic_fingerprint_sha256"]
    after_fp = value["after"]["semantic_fingerprint_sha256"]
    progress_witness = expected["progress_witness"]
    if classification == "cycle":
        if not isinstance(progress_witness, Mapping):
            raise ValueError("cycle requires a progress recurrence witness")
        _exact(progress_witness, PROGRESS_WITNESS_KEYS, "progress_witness")
        if progress_witness["prior_semantic_fingerprint_sha256"] != before_fp:
            raise ValueError("cycle recurrence witness fingerprint mismatch")
        prior_step = _uint(progress_witness["prior_logical_step"], "progress_witness.prior_logical_step")
        if prior_step >= before_step:
            raise ValueError("cycle recurrence witness must precede the transition")
    elif progress_witness is not None:
        raise ValueError("only cycle may carry a progress recurrence witness")
    starvation = expected["starvation_witness"]
    if starvation is not None:
        if not isinstance(starvation, Mapping):
            raise ValueError("starvation_witness must be an object or null")
        _exact(starvation, STARVATION_KEYS, "starvation_witness")
        for field in ("victim_run_ref", "blocker_run_ref"):
            reference = _string(starvation[field], f"starvation {field}")
            if _OPAQUE_REF.fullmatch(reference) is None:
                raise ValueError(f"starvation {field} must be an opaque fixture reference")
        _uint(starvation["eligible_since_step"], "starvation eligible_since_step")
        if _uint(starvation["witness_steps"], "starvation witness_steps") < 1:
            raise ValueError("starvation witness must span at least one step")
    side_effects = expected["side_effects"]
    if not isinstance(side_effects, Mapping):
        raise ValueError("side_effects must be an object")
    _exact(side_effects, SIDE_EFFECT_KEYS, "side_effects")
    _uint(side_effects["scripted_provider_creates"], "scripted_provider_creates")
    _uint(side_effects["scripted_provider_retrievals"], "scripted_provider_retrievals")
    if _uint(side_effects["external_network_calls"], "external_network_calls") != 0:
        raise ValueError("provider-free trace cannot perform external network calls")
    _bool(side_effects["lease_released"], "lease_released")
    _bool(side_effects["capacity_released"], "capacity_released")
    if classification in {"cycle", "stutter", "idempotent_replay"} and before_fp != after_fp:
        raise ValueError(f"{classification} requires equal semantic fingerprints")
    if classification == "productive" and before_fp == after_fp:
        raise ValueError("productive transition requires semantic change")
    if classification == "legitimate_wait":
        native = value["after"]["native"]
        api = value["after"]["api_fixture"]
        if native["capacity_disposition"] != "release_until_due" or native["resume_not_before"] is None:
            raise ValueError("legitimate wait requires declared native due boundary")
        if api["lease_disposition"] != "released" or api["capacity_state"] != "released":
            raise ValueError("legitimate wait requires released API lease and capacity")
    privacy = value["privacy"]
    if not isinstance(privacy, Mapping):
        raise ValueError("privacy must be an object")
    _exact(privacy, PRIVACY_KEYS, "privacy")
    if any(_bool(privacy[key], f"privacy.{key}") for key in PRIVACY_KEYS):
        raise ValueError("provider-free trace contains prohibited private material")


def read_adversarial_trace_schema() -> dict[str, Any]:
    path = resources.files("astrowoof_natal_authoring").joinpath(
        "resources", "contracts", SCHEMA_RESOURCE
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _native_state(
    *,
    command: str,
    disposition: str,
    custody: str,
    due: str | None,
    review: bool = False,
) -> dict[str, Any]:
    return {
        "native_run_ref": "fixture:native-simulation-run",
        "route_contract": "astrowoof.semantic_closure_run.v0.9",
        "checkpoint_basis_sha256": "1" * 64,
        "snapshot_sha256": "2" * 64,
        "state_revision": 7,
        "selected_command": command,
        "capacity_disposition": disposition,
        "reason_code": (
            "native_review_or_ambiguity" if review else "provider_reconciliation_not_due"
        ),
        "local_operation_keys": [],
        "consumed_operation_keys": [],
        "provider_custody": custody,
        "resume_not_before": due,
        "external_authority": "none",
        "terminal": False,
        "review_required": review,
        "delivery_publishable": False,
        "semantic_fences": [{"kind": "checkpoint_basis", "sha256": "1" * 64}],
    }


def _api_state(
    *, job: str, lease: str, capacity: str, competing: int,
) -> dict[str, Any]:
    return {
        "run_ref": "fixture:api-simulation-run",
        "run_disposition": "running",
        "job_disposition": job,
        "lease_disposition": lease,
        "capacity_state": capacity,
        "reservation_state": "none",
        "competing_eligible_run_count": competing,
    }


def _state(
    *,
    raw: str,
    native: Mapping[str, Any],
    api: Mapping[str, Any],
    provider_operations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "raw_evidence_sha256": raw,
        "semantic_fingerprint_sha256": "0" * 64,
        "native": deepcopy(dict(native)),
        "api_fixture": deepcopy(dict(api)),
        "provider_fixture": {
            "network_capability": False,
            "credential_capability": False,
            "operations": deepcopy(provider_operations or []),
        },
    }


def _fixture_base(name: str) -> dict[str, Any]:
    base = {
        "schema_version": SCHEMA_VERSION,
        "trace_id": "simtrace_" + "0" * 24,
        "trace_sha256": "0" * 64,
        "construction_class": "legally_reached",
        "package": {
            "name": "astrowoof-natal-authoring",
            "version": "0.4.25",
            "schema_resource": SCHEMA_RESOURCE,
        },
        "clock": {
            "logical_step_before": 0,
            "logical_step_after": 1,
            "simulated_time_before": "2026-08-27T12:00:00Z",
            "simulated_time_after": "2026-08-27T12:00:00Z",
            "time_event": "none",
        },
        "route_cell": {
            "route_family": "exact_natal",
            "provider_mechanism": "response",
            "stage": "creative_retry",
            "support": "supported",
        },
        "public_evidence": [{
            "kind": "lifecycle_inspection",
            "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.7",
            "sha256": "3" * 64,
            "opaque_ref": "fixture:lifecycle-inspection",
        }],
        "before": {},
        "event": {
            "actor": "claimed_worker",
            "kind": "ingest_native_result",
            "enabled": True,
            "refusal_reason": None,
        },
        "after": {},
        "expected": {
            "classification": "productive",
            "declared_contradictions": [],
            "progress_witness": None,
            "starvation_witness": None,
            "side_effects": {
                "scripted_provider_creates": 0,
                "scripted_provider_retrievals": 0,
                "external_network_calls": 0,
                "lease_released": False,
                "capacity_released": False,
            },
        },
        "privacy": {
            "contains_prompt": False,
            "contains_provider_payload": False,
            "contains_raw_provider_id": False,
            "contains_workspace_path": False,
            "contains_credentials": False,
        },
    }
    if name == "review-no-action-cycle.v1.json":
        native = _native_state(
            command="none", disposition="retain_for_review", custody="none",
            due=None, review=True,
        )
        api = _api_state(job="leased", lease="active", capacity="allocated", competing=1)
        base["construction_class"] = "historical_shape"
        base["clock"]["logical_step_before"] = 1
        base["clock"]["logical_step_after"] = 2
        base["before"] = _state(raw="4" * 64, native=native, api=api)
        base["after"] = _state(raw="5" * 64, native=native, api=api)
        base["expected"]["classification"] = "cycle"
        base["expected"]["progress_witness"] = {
            "prior_semantic_fingerprint_sha256": semantic_fingerprint(base["before"]),
            "prior_logical_step": 0,
        }
        base["expected"]["starvation_witness"] = {
            "victim_run_ref": "fixture:api-competing-run",
            "blocker_run_ref": "fixture:api-simulation-run",
            "eligible_since_step": 0,
            "witness_steps": 1,
        }
    elif name == "provider-not-due-legitimate-wait.v1.json":
        due = "2026-08-27T12:05:00Z"
        native = _native_state(
            command="provider_reconciliation_cycle", disposition="release_until_due",
            custody="known_operations_pending", due=due,
        )
        operation = [{"correlation_id": "simop_" + "6" * 24, "state": "pending"}]
        base["before"] = _state(
            raw="7" * 64, native=native,
            api=_api_state(job="leased", lease="active", capacity="allocated", competing=1),
            provider_operations=operation,
        )
        base["after"] = _state(
            raw="8" * 64, native=native,
            api=_api_state(job="deferred", lease="released", capacity="released", competing=1),
            provider_operations=operation,
        )
        base["expected"]["classification"] = "legitimate_wait"
        base["expected"]["side_effects"]["lease_released"] = True
        base["expected"]["side_effects"]["capacity_released"] = True
    elif name == "contradictory-command-custody.v1.json":
        native = _native_state(
            command="provider_reconciliation_cycle", disposition="retain_for_review",
            custody="none", due=None,
        )
        state = _state(
            raw="9" * 64, native=native,
            api=_api_state(job="available", lease="none", capacity="none", competing=0),
        )
        base["construction_class"] = "synthetic_invalid_state"
        base["before"] = state
        base["after"] = deepcopy(state)
        base["event"] = {
            "actor": "sbe_command", "kind": "inspect_lifecycle", "enabled": True,
            "refusal_reason": None,
        }
        base["expected"]["classification"] = "contradictory_evidence"
        base["expected"]["declared_contradictions"] = ["command_custody_mismatch"]
    else:
        raise ValueError(f"unsupported adversarial trace fixture: {name}")
    return base


def build_adversarial_trace_fixture(name: str) -> dict[str, Any]:
    if name not in FIXTURE_NAMES:
        raise ValueError(f"unsupported adversarial trace fixture: {name}")
    return finalize_adversarial_trace(_fixture_base(name))


def read_adversarial_trace_fixture(name: str) -> dict[str, Any]:
    if name not in FIXTURE_NAMES:
        raise ValueError(f"unsupported adversarial trace fixture: {name}")
    path = resources.files("astrowoof_natal_authoring").joinpath(
        "resources", "fixtures", "adversarial-traces", name
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_adversarial_trace(value)
    if value != build_adversarial_trace_fixture(name):
        raise ValueError("packaged adversarial trace fixture differs from its canonical builder")
    return value
