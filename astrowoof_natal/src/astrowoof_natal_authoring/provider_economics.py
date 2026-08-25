from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata, resources
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = "astrowoof.provider_economics_transaction_revision.v1"
MAX_RETRIEVAL_REFERENCES = 16
PROVIDER_ECONOMICS_FIXTURE_NAMES = {
    "interactive-settlement.v1.json",
    "interactive-editorial-finalization.v1.json",
    "interactive-native-finalization.v1.json",
    "batch-partial-usage.v1.json",
    "providerless-no-work.v1.json",
    "ambiguous-submission.v1.json",
    "legacy-unknown.v1.json",
}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_TRANSACTION_ID = re.compile(r"^pe_txn_[0-9a-f]{24}$")
_REVISION_ID = re.compile(r"^pe_rev_[0-9a-f]{24}$")

ROUTES = {"exact_natal", "bounded_natal"}
STAGES = {
    "authoring_initial",
    "creative_retry",
    "polish",
    "qualitative_critic",
    "qualitative_candidate",
}
MECHANISMS = {"response", "batch"}
SETTLEMENTS = {
    "provider_pending",
    "provider_usage_reported",
    "provider_usage_unavailable_billing_reconciliation_pending",
    "no_provider_work_consumed",
    "submission_ambiguous",
}
PROVIDER_STATUSES = {
    "not_created", "pending", "completed", "failed", "cancelled", "expired",
    "ambiguous", "identity_conflict",
}
EDITORIAL_STATUSES = {
    "not_yet_evaluated", "accepted", "rejected_invalid", "retry_prepared",
    "advisory_only", "skipped",
}
NATIVE_STATUSES = {
    "in_progress", "delivery_complete", "delivery_with_warning", "review_held",
    "budget_exhausted", "policy_stopped", "failed",
}

TOP_KEYS = {
    "schema_version", "transaction_id", "native_run_id", "native_action_id",
    "revision_number", "previous_revision_id", "revision_id", "observed_at",
    "transaction_identity", "cohort_identity", "authority_and_commitment",
    "provider_operation", "usage_and_cost", "timing", "editorial_outcome",
    "native_outcome", "provenance",
}
TRANSACTION_KEYS = {
    "route_family", "paid_stage", "provider_mechanism", "native_operation_ref",
    "pass_id", "attempt_number", "round_id", "cardinality_kind", "members",
}
MEMBER_KEYS = {
    "member_id", "ordinal", "pass_id", "attempt_number", "paid_stage",
    "request_sha256", "provider_member_id", "provider_status",
    "usage_disposition", "usage", "provider_reported_micro_usd",
}
COHORT_KEYS = {
    "cohort_completeness", "sbe_release", "route_contract",
    "generation_profile_id", "profile_manifest_sha256", "resource_bundle_sha256",
    "request_geometry_version", "request_geometry_sha256",
    "execution_topology_version", "execution_topology_sha256", "model",
    "reasoning_effort", "service_level", "maximum_output_tokens",
    "price_book_version", "cohort_identity_sha256",
}
AUTHORITY_KEYS = {
    "commitment_micro_usd", "authorization_reference", "consumption_reference",
}
PROVIDER_KEYS = {"provider", "operation_kind", "operation_id", "status"}
USAGE_KEYS = {
    "settlement_disposition", "usage", "sbe_estimated_micro_usd",
    "sbe_estimate_price_book_version", "provider_reported_micro_usd",
}
TOKEN_KEYS = {
    "input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens",
}
TIMING_KEYS = {
    "prepared_at", "authorized_at", "submission_intent_at",
    "provider_identity_durable_at", "provider_terminal_observed_at",
    "reconciliation_completed_at", "native_settled_at", "create_http_duration_ms",
    "observed_provider_pending_ms", "native_action_span_ms",
    "provider_reported_duration_ms", "retrieval_attempt_count",
    "first_retrieval_observed_at", "last_retrieval_observed_at",
    "retrieval_http_duration_total_ms", "retrieval_attempt_refs",
    "retrieval_attempt_ref_overflow_count",
}
EDITORIAL_KEYS = {"status", "retry_reason_category"}
NATIVE_KEYS = {"status", "delivery_publishable"}
PROVENANCE_KEYS = {
    "action_binding_sha256", "request_sha256", "native_result_id",
    "native_result_sha256", "journal_range_sha256", "snapshot_sha256",
    "publication_receipt_id", "publication_receipt_sha256", "usage_evidence_ref",
    "batch_round_manifest_sha256", "api_reconciliation_join",
}
JOIN_KEYS = {"native_run_id", "native_action_id"}

_EXACT_RUN_SCHEMA = "astrowoof.semantic_closure_run.v0.9"
_ACTION_STAGE = {
    "authoring_initial": "authoring_initial",
    "creative_retry": "creative_retry",
    "polish": "polish",
    "qualitative_critic": "qualitative_critic",
    "qualitative_candidate": "qualitative_candidate",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def derive_transaction_id(native_run_id: str, native_action_id: str) -> str:
    return "pe_txn_" + canonical_sha256(
        {"native_action_id": native_action_id, "native_run_id": native_run_id}
    )[:24]


def derive_cohort_identity_sha256(cohort_identity: Mapping[str, Any]) -> str:
    body = dict(cohort_identity)
    body.pop("cohort_identity_sha256", None)
    return canonical_sha256(body)


def derive_revision_id(revision: Mapping[str, Any]) -> str:
    body = deepcopy(dict(revision))
    body.pop("revision_id", None)
    return "pe_rev_" + canonical_sha256(body)[:24]


def _canonical_timestamp(value: Any, fallback: str) -> str:
    candidate = value if isinstance(value, str) else fallback
    parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _usage(raw: Any) -> dict[str, int] | None:
    if not isinstance(raw, Mapping):
        return None
    aliases = {
        "input_tokens": ("input_tokens",),
        "cached_input_tokens": ("cached_input_tokens", "input_cached_tokens"),
        "output_tokens": ("output_tokens",),
        "reasoning_tokens": ("reasoning_tokens", "output_reasoning_tokens"),
    }
    result: dict[str, int] = {}
    for target, names in aliases.items():
        found = next((raw[name] for name in names if isinstance(raw.get(name), int)), 0)
        result[target] = max(0, found)
    return result if any(result.values()) else None


def _native_status(state: Mapping[str, Any]) -> tuple[str, bool]:
    status = str(state.get("status") or "")
    mapping = {
        "DELIVERY_COMPLETE": ("delivery_complete", True),
        "DELIVERY_WITH_WARNING": ("delivery_with_warning", True),
        "FINAL_QA_REQUIRES_REVIEW": ("review_held", False),
        "AMBIGUOUS_PROVIDER_SUBMISSION": ("review_held", False),
        "BUDGET_EXHAUSTED": ("budget_exhausted", False),
        "POLICY_STOPPED": ("policy_stopped", False),
        "FAILED": ("failed", False),
    }
    return mapping.get(status, ("in_progress", False))


def _provider_status(action: Mapping[str, Any]) -> str:
    state = action.get("state")
    provider = action.get("provider") if isinstance(action.get("provider"), Mapping) else {}
    explicit = str(provider.get("status") or "").lower()
    if explicit in PROVIDER_STATUSES:
        return explicit
    if state == "AMBIGUOUS_PROVIDER_SUBMISSION":
        return "ambiguous"
    if state in {"REPORTED", "COMPLETED"}:
        return "completed"
    if provider.get("id"):
        return "pending"
    return "not_created"


def _settlement(action: Mapping[str, Any], provider_status: str) -> tuple[str, dict[str, int] | None, int | None, str | None]:
    reported = action.get("reported") if isinstance(action.get("reported"), Mapping) else {}
    usage = _usage(reported.get("usage"))
    estimated = reported.get("estimated_micro_usd")
    price_book = reported.get("price_book_version")
    disposition = reported.get("cost_disposition")
    if action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION":
        return "submission_ambiguous", None, None, None
    if action.get("state") in {"DENIED_PROVIDERLESS", "SKIPPED_OPTIONAL", "BUDGET_EXHAUSTED"} and not (action.get("provider") or {}).get("id"):
        return "no_provider_work_consumed", None, None, None
    if disposition == "provider_usage_unavailable_billing_reconciliation_pending":
        return disposition, None, None, None
    if usage is not None and isinstance(estimated, int):
        return "provider_usage_reported", usage, estimated, price_book if isinstance(price_book, str) else None
    if provider_status in {"completed", "failed", "cancelled", "expired", "identity_conflict"}:
        return "provider_usage_unavailable_billing_reconciliation_pending", None, None, None
    return "provider_pending", None, None, None


def _exact_pass_attempt(state: Mapping[str, Any], action: Mapping[str, Any]) -> tuple[str | None, int | None, Mapping[str, Any] | None]:
    provider_id = ((action.get("provider") or {}).get("id") if isinstance(action.get("provider"), Mapping) else None)
    request_sha = ((action.get("binding") or {}).get("request_sha256") if isinstance(action.get("binding"), Mapping) else None)
    for pass_id, record in (state.get("passes") or {}).items():
        for number, attempt in enumerate(record.get("attempts") or [], 1):
            metadata = attempt.get("provider_metadata") if isinstance(attempt.get("provider_metadata"), Mapping) else {}
            if provider_id and provider_id in {metadata.get("response_id"), metadata.get("batch_id")}:
                return pass_id, number, attempt
            if request_sha and request_sha in {attempt.get("prompt_sha256"), metadata.get("prompt_sha256")}:
                return pass_id, number, attempt
    return None, None, None


def _batch_round(state: Mapping[str, Any], action: Mapping[str, Any]) -> Mapping[str, Any] | None:
    provider_id = ((action.get("provider") or {}).get("id") if isinstance(action.get("provider"), Mapping) else None)
    for round_record in ((state.get("authoring_service") or {}).get("rounds") or []):
        if provider_id and round_record.get("batch_id") == provider_id:
            return round_record
        if (action.get("binding") or {}).get("route") == f"batch-round-{int(round_record.get('round_number', 0)):03d}":
            return round_record
    return None


def _cohort(state: Mapping[str, Any], action: Mapping[str, Any], *, mechanism: str) -> dict[str, Any]:
    binding = action.get("binding") if isinstance(action.get("binding"), Mapping) else {}
    profile = state.get("authoring_profile") if isinstance(state.get("authoring_profile"), Mapping) else {}
    config = state.get("provider_configuration") if isinstance(state.get("provider_configuration"), Mapping) else {}
    manifest = profile.get("manifest_sha256")
    resource = profile.get("resource_bundle_sha256")
    completeness = "complete" if all(isinstance(v, str) and _HEX64.fullmatch(v) for v in (manifest, resource)) else "legacy_unknown"
    geometry = {
        "route": binding.get("route"), "stage": binding.get("stage"),
        "request_sha256": binding.get("request_sha256"), "mechanism": mechanism,
    }
    topology = {"mechanism": mechanism, "initial_wave_members": len((state.get("initial_authoring_wave") or {}).get("members") or [])}
    return {
        "cohort_completeness": completeness, "sbe_release": metadata.version("astrowoof-natal-authoring"),
        "route_contract": _EXACT_RUN_SCHEMA,
        "generation_profile_id": profile.get("generation_profile_id"),
        "profile_manifest_sha256": manifest if completeness == "complete" else None,
        "resource_bundle_sha256": resource if completeness == "complete" else None,
        "request_geometry_version": "exact-provider-action.v1",
        "request_geometry_sha256": canonical_sha256(geometry),
        "execution_topology_version": "six-pass-wave.v1" if binding.get("stage") == "authoring_initial" else "stage-action.v1",
        "execution_topology_sha256": canonical_sha256(topology),
        "model": str(binding.get("model") or config.get("model") or "unknown"),
        "reasoning_effort": str(config.get("reasoning_effort") or "unknown"),
        "service_level": "batch" if mechanism == "batch" else "default",
        "maximum_output_tokens": int(binding.get("maximum_output_tokens") or config.get("max_output_tokens") or 0),
        "price_book_version": str(binding.get("price_book_version") or "unknown"),
        "cohort_identity_sha256": "pending",
    }


def project_exact_provider_economics_revision(
    state: Mapping[str, Any], action: Mapping[str, Any], *, observed_at: str,
    previous_revision: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Project one exact-Natal paid action without mutating native state.

    Returns ``None`` when the durable consumer facts are unchanged from the supplied
    predecessor. Publication observation time alone never creates a revision.
    """
    if state.get("schema_version") != _EXACT_RUN_SCHEMA or state.get("route_contract"):
        raise ValueError("exact provider economics projection requires an exact v0.9 run")
    run_id = state.get("run_id")
    action_id = action.get("action_id")
    if not isinstance(run_id, str) or not isinstance(action_id, str) or not _ACTION_ID.fullmatch(action_id):
        raise ValueError("native run/action identity is invalid")
    binding = action.get("binding") if isinstance(action.get("binding"), Mapping) else {}
    if binding.get("run_id") != run_id:
        raise ValueError("action binding does not join the native run")
    stage = _ACTION_STAGE.get(binding.get("stage"))
    if stage is None:
        raise ValueError("unsupported exact paid stage")
    mechanism = "batch" if binding.get("service_level") == "batch" or str(binding.get("route", "")).startswith("batch-round-") else "response"
    pass_id, attempt_number, attempt = _exact_pass_attempt(state, action)
    round_record = _batch_round(state, action) if mechanism == "batch" else None
    provider_status = _provider_status(action)
    disposition, usage, estimate, estimate_book = _settlement(action, provider_status)
    provider = action.get("provider") if isinstance(action.get("provider"), Mapping) else {}
    members = []
    if mechanism == "batch":
        for ordinal, request in enumerate((round_record or {}).get("requests") or [], 1):
            member_attempt = None
            record = (state.get("passes") or {}).get(request.get("pass_id"), {})
            for candidate in record.get("attempts") or []:
                metadata = candidate.get("provider_metadata") or {}
                if metadata.get("custom_id") == request.get("custom_id"):
                    member_attempt = candidate; break
            metadata = (member_attempt or {}).get("provider_metadata") or {}
            member_usage = _usage(metadata.get("usage"))
            members.append({
                "member_id": str(request.get("custom_id") or f"member-{ordinal}"), "ordinal": ordinal,
                "pass_id": request.get("pass_id"), "attempt_number": request.get("attempt_number"),
                "paid_stage": stage, "request_sha256": request.get("prompt_sha256") or binding.get("request_sha256"),
                "provider_member_id": metadata.get("response_id") or request.get("custom_id"),
                "provider_status": str(metadata.get("response_status") or ("completed" if member_usage else "pending")),
                "usage_disposition": "reported" if member_usage else "unavailable",
                "usage": member_usage, "provider_reported_micro_usd": None,
            })
    native_status, publishable = _native_status(state)
    auth = action.get("authorization") if isinstance(action.get("authorization"), Mapping) else {}
    consumption = action.get("consumption") if isinstance(action.get("consumption"), Mapping) else {}
    observed = _canonical_timestamp(observed_at, str(observed_at))
    timing_source = attempt.get("provider_metadata", {}) if isinstance(attempt, Mapping) else {}
    value = {
        "schema_version": SCHEMA_VERSION, "transaction_id": "pending", "native_run_id": run_id,
        "native_action_id": action_id, "revision_number": 1 if previous_revision is None else previous_revision["revision_number"] + 1,
        "previous_revision_id": None if previous_revision is None else previous_revision["revision_id"], "revision_id": "pending", "observed_at": observed,
        "transaction_identity": {"route_family": "exact_natal", "paid_stage": stage, "provider_mechanism": mechanism,
            "native_operation_ref": str((round_record or {}).get("round_id") or binding.get("route") or action_id),
            "pass_id": pass_id if mechanism == "response" else None, "attempt_number": attempt_number,
            "round_id": str((round_record or {}).get("round_id") or binding.get("route")) if mechanism == "batch" else None,
            "cardinality_kind": "batch_round" if mechanism == "batch" else "single_action", "members": members},
        "cohort_identity": _cohort(state, action, mechanism=mechanism),
        "authority_and_commitment": {"commitment_micro_usd": int(binding.get("commitment_micro_usd") or 0),
            "authorization_reference": auth.get("authorization_reference"), "consumption_reference": consumption.get("consumer_id")},
        "provider_operation": {"provider": "openai", "operation_kind": mechanism, "operation_id": provider.get("id"), "status": provider_status},
        "usage_and_cost": {"settlement_disposition": disposition, "usage": usage, "sbe_estimated_micro_usd": estimate,
            "sbe_estimate_price_book_version": estimate_book, "provider_reported_micro_usd": None},
        "timing": {"prepared_at": None, "authorized_at": None, "submission_intent_at": None, "provider_identity_durable_at": None,
            "provider_terminal_observed_at": None, "reconciliation_completed_at": None, "native_settled_at": None,
            "create_http_duration_ms": timing_source.get("create_http_duration_ms"), "observed_provider_pending_ms": None,
            "native_action_span_ms": None, "provider_reported_duration_ms": timing_source.get("provider_reported_duration_ms"),
            "retrieval_attempt_count": 0, "first_retrieval_observed_at": None, "last_retrieval_observed_at": None,
            "retrieval_http_duration_total_ms": None, "retrieval_attempt_refs": [], "retrieval_attempt_ref_overflow_count": 0},
        "editorial_outcome": {"status": "accepted" if isinstance(attempt, Mapping) and attempt.get("state") == "ACCEPTED" else "not_yet_evaluated", "retry_reason_category": None},
        "native_outcome": {"status": native_status, "delivery_publishable": publishable},
        "provenance": {"action_binding_sha256": canonical_sha256(binding), "request_sha256": binding.get("request_sha256"),
            "native_result_id": None, "native_result_sha256": None, "journal_range_sha256": None, "snapshot_sha256": None,
            "publication_receipt_id": None, "publication_receipt_sha256": None,
            "usage_evidence_ref": f"spend-ledger:{action_id}:reported" if action.get("reported") else None,
            "batch_round_manifest_sha256": canonical_sha256(round_record) if mechanism == "batch" and round_record else (canonical_sha256({"route": binding.get("route"), "request_sha256": binding.get("request_sha256")}) if mechanism == "batch" else None),
            "api_reconciliation_join": {"native_run_id": run_id, "native_action_id": action_id}},
    }
    candidate = finalize_provider_economics_revision(value)
    if previous_revision is not None:
        validate_provider_economics_revision_sequence([previous_revision, candidate])
        old = deepcopy(dict(previous_revision)); new = deepcopy(candidate)
        for item in (old, new):
            item.pop("revision_id", None); item.pop("observed_at", None); item.pop("revision_number", None); item.pop("previous_revision_id", None)
        if old == new:
            return None
    return candidate


def finalize_provider_economics_revision(revision: Mapping[str, Any]) -> dict[str, Any]:
    value = deepcopy(dict(revision))
    cohort = value.get("cohort_identity")
    if isinstance(cohort, dict):
        cohort["cohort_identity_sha256"] = derive_cohort_identity_sha256(cohort)
    value["transaction_id"] = derive_transaction_id(
        value.get("native_run_id"), value.get("native_action_id")
    )
    value["revision_id"] = derive_revision_id(value)
    validate_provider_economics_revision(value)
    return value


def read_provider_economics_schema() -> dict[str, Any]:
    path = resources.files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "provider-economics-transaction-revision.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def read_provider_economics_fixture(name: str) -> dict[str, Any]:
    if name not in PROVIDER_ECONOMICS_FIXTURE_NAMES:
        raise ValueError(f"unsupported provider economics fixture: {name}")
    path = resources.files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "provider-economics", name
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    return validate_provider_economics_revision(value)


def read_provider_economics_mutation_corpus() -> dict[str, Any]:
    path = resources.files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "provider-economics", "mutation-corpus.v1.json"
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {"schema_version", "mutations"}
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError("provider economics mutation corpus has an invalid shape")
    if value["schema_version"] != "astrowoof.provider_economics_mutation_corpus.v1":
        raise ValueError("unsupported provider economics mutation corpus")
    if not isinstance(value["mutations"], list) or not value["mutations"]:
        raise ValueError("provider economics mutation corpus is empty")
    return value


def _fail(message: str) -> None:
    raise ValueError(message)


def _closed(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        _fail(f"{label} must have exact keys {sorted(keys)}")
    return value


def _string(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value:
        _fail(f"{label} must be a nonempty string")
    return value


def _integer(value: Any, label: str, *, nullable: bool = False) -> int | None:
    if value is None and nullable:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _fail(f"{label} must be a nonnegative integer")
    return value


def _timestamp(value: Any, label: str, *, nullable: bool = True) -> datetime | None:
    if value is None and nullable:
        return None
    text = _string(value, label)
    if not text.endswith("Z"):
        _fail(f"{label} must use canonical UTC Z form")
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid timestamp") from exc
    if parsed.tzinfo != timezone.utc or parsed.isoformat(timespec="seconds").replace("+00:00", "Z") != text:
        _fail(f"{label} must be canonical UTC to whole seconds")
    return parsed


def _digest(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        _fail(f"{label} must be lowercase SHA-256")
    return value


def _tokens(value: Any, label: str) -> None:
    token = _closed(value, TOKEN_KEYS, label)
    for key in TOKEN_KEYS:
        _integer(token[key], f"{label}.{key}")
    if token["cached_input_tokens"] > token["input_tokens"]:
        _fail(f"{label}.cached_input_tokens exceeds input_tokens")


def validate_provider_economics_revision(value: Mapping[str, Any]) -> dict[str, Any]:
    revision = _closed(dict(value), TOP_KEYS, "revision")
    if revision["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported provider economics schema_version")
    run_id = _string(revision["native_run_id"], "native_run_id")
    action_id = _string(revision["native_action_id"], "native_action_id")
    if not _ACTION_ID.fullmatch(action_id):
        _fail("native_action_id is not canonical")
    expected_txn = derive_transaction_id(run_id, action_id)
    if revision["transaction_id"] != expected_txn or not _TRANSACTION_ID.fullmatch(revision["transaction_id"]):
        _fail("transaction_id does not match native identity")
    number = _integer(revision["revision_number"], "revision_number")
    if number < 1:
        _fail("revision_number must begin at 1")
    previous = revision["previous_revision_id"]
    if number == 1:
        if previous is not None:
            _fail("revision 1 previous_revision_id must be null")
    elif not isinstance(previous, str) or not _REVISION_ID.fullmatch(previous):
        _fail("later revision requires canonical previous_revision_id")
    _timestamp(revision["observed_at"], "observed_at", nullable=False)

    identity = _closed(revision["transaction_identity"], TRANSACTION_KEYS, "transaction_identity")
    if identity["route_family"] not in ROUTES or identity["paid_stage"] not in STAGES:
        _fail("invalid route or paid stage")
    mechanism = identity["provider_mechanism"]
    if mechanism not in MECHANISMS:
        _fail("invalid provider mechanism")
    _string(identity["native_operation_ref"], "native_operation_ref")
    _string(identity["pass_id"], "pass_id", nullable=True)
    _integer(identity["attempt_number"], "attempt_number", nullable=True)
    _string(identity["round_id"], "round_id", nullable=True)
    members = identity["members"]
    if not isinstance(members, list):
        _fail("members must be an array")
    if identity["cardinality_kind"] == "single_action":
        if mechanism != "response" or members or identity["round_id"] is not None:
            _fail("single_action cardinality is inconsistent")
    elif identity["cardinality_kind"] == "batch_round":
        if mechanism != "batch" or not members or identity["round_id"] is None:
            _fail("batch_round cardinality is inconsistent")
    else:
        _fail("invalid cardinality_kind")
    for ordinal, raw in enumerate(members, 1):
        member = _closed(raw, MEMBER_KEYS, f"members[{ordinal}]")
        if member["ordinal"] != ordinal:
            _fail("Batch member ordinals must be contiguous and ordered")
        _string(member["member_id"], "member_id")
        _string(member["pass_id"], "member.pass_id", nullable=True)
        _integer(member["attempt_number"], "member.attempt_number", nullable=True)
        if member["paid_stage"] not in STAGES or member["provider_status"] not in PROVIDER_STATUSES:
            _fail("invalid Batch member stage/status")
        _digest(member["request_sha256"], "member.request_sha256")
        _string(member["provider_member_id"], "member.provider_member_id", nullable=True)
        if member["usage_disposition"] not in {"reported", "unavailable"}:
            _fail("invalid Batch member usage_disposition")
        if member["usage_disposition"] == "reported":
            _tokens(member["usage"], "member.usage")
            _integer(member["provider_reported_micro_usd"], "member.provider_reported_micro_usd", nullable=True)
        elif member["usage"] is not None or member["provider_reported_micro_usd"] is not None:
            _fail("unavailable member usage/cost must remain null; allocation is forbidden")

    cohort = _closed(revision["cohort_identity"], COHORT_KEYS, "cohort_identity")
    if cohort["cohort_completeness"] not in {"complete", "legacy_unknown"}:
        _fail("invalid cohort_completeness")
    for key in ("sbe_release", "route_contract", "request_geometry_version", "execution_topology_version", "model", "reasoning_effort", "service_level", "price_book_version"):
        _string(cohort[key], f"cohort_identity.{key}")
    _string(cohort["generation_profile_id"], "generation_profile_id", nullable=True)
    for key in ("profile_manifest_sha256", "resource_bundle_sha256", "request_geometry_sha256", "execution_topology_sha256"):
        _digest(cohort[key], f"cohort_identity.{key}", nullable=cohort["cohort_completeness"] == "legacy_unknown")
    _integer(cohort["maximum_output_tokens"], "maximum_output_tokens")
    if cohort["cohort_identity_sha256"] != derive_cohort_identity_sha256(cohort):
        _fail("cohort_identity_sha256 mismatch")

    authority = _closed(revision["authority_and_commitment"], AUTHORITY_KEYS, "authority_and_commitment")
    _integer(authority["commitment_micro_usd"], "commitment_micro_usd")
    _string(authority["authorization_reference"], "authorization_reference", nullable=True)
    _string(authority["consumption_reference"], "consumption_reference", nullable=True)
    provider = _closed(revision["provider_operation"], PROVIDER_KEYS, "provider_operation")
    if provider["provider"] != "openai" or provider["operation_kind"] not in MECHANISMS or provider["status"] not in PROVIDER_STATUSES:
        _fail("invalid provider operation")
    if provider["operation_kind"] != mechanism:
        _fail("provider mechanism mismatch")
    _string(provider["operation_id"], "operation_id", nullable=True)

    economics = _closed(revision["usage_and_cost"], USAGE_KEYS, "usage_and_cost")
    settlement = economics["settlement_disposition"]
    if settlement not in SETTLEMENTS:
        _fail("invalid settlement_disposition")
    if economics["usage"] is not None:
        _tokens(economics["usage"], "usage")
    _integer(economics["sbe_estimated_micro_usd"], "sbe_estimated_micro_usd", nullable=True)
    _string(economics["sbe_estimate_price_book_version"], "sbe_estimate_price_book_version", nullable=True)
    _integer(economics["provider_reported_micro_usd"], "provider_reported_micro_usd", nullable=True)
    if settlement == "provider_usage_reported":
        if economics["usage"] is None or economics["sbe_estimated_micro_usd"] is None:
            _fail("reported settlement requires usage and SBE estimate")
        if members and any(m["usage_disposition"] != "reported" for m in members):
            _fail("partial Batch member usage cannot settle the round")
    elif settlement in {"provider_usage_unavailable_billing_reconciliation_pending", "no_provider_work_consumed", "submission_ambiguous"}:
        if economics["usage"] is not None or economics["sbe_estimated_micro_usd"] is not None:
            _fail("unavailable/no-work/ambiguous settlement cannot invent usage or estimated cost")
    if settlement == "no_provider_work_consumed" and provider["operation_id"] is not None:
        _fail("no-work settlement cannot carry provider identity")

    timing = _closed(revision["timing"], TIMING_KEYS, "timing")
    times = {}
    for key in TIMING_KEYS & {
        "prepared_at", "authorized_at", "submission_intent_at", "provider_identity_durable_at",
        "provider_terminal_observed_at", "reconciliation_completed_at", "native_settled_at",
        "first_retrieval_observed_at", "last_retrieval_observed_at",
    }:
        times[key] = _timestamp(timing[key], f"timing.{key}")
    for key in TIMING_KEYS & {
        "create_http_duration_ms", "observed_provider_pending_ms", "native_action_span_ms",
        "provider_reported_duration_ms", "retrieval_http_duration_total_ms",
    }:
        _integer(timing[key], f"timing.{key}", nullable=True)
    count = _integer(timing["retrieval_attempt_count"], "retrieval_attempt_count")
    refs = timing["retrieval_attempt_refs"]
    if not isinstance(refs, list) or len(refs) > MAX_RETRIEVAL_REFERENCES or any(not isinstance(item, str) or not item for item in refs):
        _fail("invalid bounded retrieval reference inventory")
    overflow = _integer(timing["retrieval_attempt_ref_overflow_count"], "retrieval_attempt_ref_overflow_count")
    if count != len(refs) + overflow:
        _fail("retrieval count must equal retained references plus overflow")
    if count == 0 and any(timing[k] is not None for k in ("first_retrieval_observed_at", "last_retrieval_observed_at", "retrieval_http_duration_total_ms")):
        _fail("zero retrievals cannot carry retrieval timing")
    if count and (times["first_retrieval_observed_at"] is None or times["last_retrieval_observed_at"] is None):
        _fail("retrieval observations require first/last timestamps")
    if count and times["first_retrieval_observed_at"] > times["last_retrieval_observed_at"]:
        _fail("retrieval timestamp order is invalid")

    editorial = _closed(revision["editorial_outcome"], EDITORIAL_KEYS, "editorial_outcome")
    if editorial["status"] not in EDITORIAL_STATUSES:
        _fail("invalid editorial outcome")
    _string(editorial["retry_reason_category"], "retry_reason_category", nullable=True)
    native = _closed(revision["native_outcome"], NATIVE_KEYS, "native_outcome")
    if native["status"] not in NATIVE_STATUSES or not isinstance(native["delivery_publishable"], bool):
        _fail("invalid native outcome")
    provenance = _closed(revision["provenance"], PROVENANCE_KEYS, "provenance")
    for key in ("action_binding_sha256", "request_sha256", "native_result_sha256", "journal_range_sha256", "snapshot_sha256", "publication_receipt_sha256", "batch_round_manifest_sha256"):
        _digest(provenance[key], f"provenance.{key}", nullable=True)
    for key in ("native_result_id", "publication_receipt_id", "usage_evidence_ref"):
        _string(provenance[key], f"provenance.{key}", nullable=True)
    join = _closed(provenance["api_reconciliation_join"], JOIN_KEYS, "api_reconciliation_join")
    if join != {"native_run_id": run_id, "native_action_id": action_id}:
        _fail("API reconciliation join mismatch")
    if mechanism == "batch" and provenance["batch_round_manifest_sha256"] is None:
        _fail("Batch transaction requires round manifest digest")
    if revision["revision_id"] != derive_revision_id(revision):
        _fail("revision_id mismatch")
    return deepcopy(revision)


def validate_provider_economics_revision_sequence(revisions: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    accepted = [validate_provider_economics_revision(item) for item in revisions]
    if not accepted:
        _fail("revision sequence must not be empty")
    immutable_fields = {"transaction_id", "native_run_id", "native_action_id", "cohort_identity", "authority_and_commitment"}
    provider_progress = {
        "not_created": PROVIDER_STATUSES,
        "pending": PROVIDER_STATUSES - {"not_created"},
        "completed": {"completed", "identity_conflict"},
        "failed": {"failed", "identity_conflict"},
        "cancelled": {"cancelled", "identity_conflict"},
        "expired": {"expired", "identity_conflict"},
        "ambiguous": {"ambiguous", "identity_conflict"},
        "identity_conflict": {"identity_conflict"},
    }
    editorial_progress = {
        "not_yet_evaluated": EDITORIAL_STATUSES,
        "accepted": {"accepted"}, "rejected_invalid": {"rejected_invalid", "retry_prepared"},
        "retry_prepared": {"retry_prepared"}, "advisory_only": {"advisory_only"}, "skipped": {"skipped"},
    }
    native_progress = {
        "in_progress": NATIVE_STATUSES,
        **{status: {status} for status in NATIVE_STATUSES - {"in_progress"}},
    }

    def monotonic(before: Any, after: Any, label: str) -> None:
        if before is None:
            return
        if after is None:
            _fail(f"accepted fact disappeared: {label}")
        if isinstance(before, dict) and isinstance(after, dict):
            if set(before) != set(after):
                _fail(f"accepted fact shape changed: {label}")
            for key in before:
                monotonic(before[key], after[key], f"{label}.{key}")
        elif isinstance(before, list) and isinstance(after, list):
            if len(before) != len(after):
                _fail(f"accepted inventory changed: {label}")
            for index, item in enumerate(before):
                monotonic(item, after[index], f"{label}[{index}]")
        elif before != after:
            _fail(f"accepted fact contradicted: {label}")
    previous = None
    for index, current in enumerate(accepted, 1):
        if current["revision_number"] != index:
            _fail("revision sequence has a predecessor gap")
        if previous is not None:
            if current["previous_revision_id"] != previous["revision_id"]:
                _fail("previous_revision_id mismatch")
            for key in immutable_fields:
                if current[key] != previous[key]:
                    _fail(f"immutable revision field changed: {key}")
            before_identity = previous["transaction_identity"]
            after_identity = current["transaction_identity"]
            for key in TRANSACTION_KEYS - {"members"}:
                if before_identity[key] != after_identity[key]:
                    _fail(f"immutable transaction identity changed: {key}")
            before_members, after_members = before_identity["members"], after_identity["members"]
            if len(before_members) != len(after_members):
                _fail("Batch member inventory changed")
            for pos, (before_member, after_member) in enumerate(zip(before_members, after_members)):
                for key in MEMBER_KEYS - {"provider_status", "usage_disposition", "usage", "provider_reported_micro_usd"}:
                    if before_member[key] != after_member[key]:
                        _fail(f"Batch member identity changed at {pos}: {key}")
                if after_member["provider_status"] not in provider_progress[before_member["provider_status"]]:
                    _fail("Batch member provider status regressed")
                monotonic(before_member["usage"], after_member["usage"], f"member[{pos}].usage")
                monotonic(before_member["provider_reported_micro_usd"], after_member["provider_reported_micro_usd"], f"member[{pos}].provider_reported_micro_usd")
            if _timestamp(current["observed_at"], "observed_at", nullable=False) < _timestamp(previous["observed_at"], "observed_at", nullable=False):
                _fail("observed_at regressed")
            if current["provider_operation"]["status"] not in provider_progress[previous["provider_operation"]["status"]]:
                _fail("provider status regressed")
            for key in PROVIDER_KEYS - {"status"}:
                monotonic(previous["provider_operation"][key], current["provider_operation"][key], f"provider_operation.{key}")
            for key in USAGE_KEYS - {"settlement_disposition"}:
                monotonic(previous["usage_and_cost"][key], current["usage_and_cost"][key], f"usage_and_cost.{key}")
            old_settlement = previous["usage_and_cost"]["settlement_disposition"]
            new_settlement = current["usage_and_cost"]["settlement_disposition"]
            if old_settlement != "provider_pending" and old_settlement != new_settlement:
                _fail("settlement disposition contradicted")
            cumulative_durations = {"observed_provider_pending_ms", "native_action_span_ms"}
            for key in TIMING_KEYS - {"retrieval_attempt_count", "retrieval_http_duration_total_ms", "retrieval_attempt_refs", "retrieval_attempt_ref_overflow_count", "last_retrieval_observed_at"} - cumulative_durations:
                monotonic(previous["timing"][key], current["timing"][key], f"timing.{key}")
            for key in cumulative_durations:
                old, new = previous["timing"][key], current["timing"][key]
                if old is not None and (new is None or new < old):
                    _fail(f"cumulative timing regressed: timing.{key}")
            if current["timing"]["retrieval_attempt_count"] < previous["timing"]["retrieval_attempt_count"]:
                _fail("retrieval attempt count regressed")
            if (current["timing"]["retrieval_http_duration_total_ms"] or 0) < (previous["timing"]["retrieval_http_duration_total_ms"] or 0):
                _fail("retrieval duration regressed")
            old_refs, new_refs = previous["timing"]["retrieval_attempt_refs"], current["timing"]["retrieval_attempt_refs"]
            if new_refs[:len(old_refs)] != old_refs:
                _fail("retrieval reference inventory contradicted")
            old_last = _timestamp(previous["timing"]["last_retrieval_observed_at"], "last_retrieval_observed_at")
            new_last = _timestamp(current["timing"]["last_retrieval_observed_at"], "last_retrieval_observed_at")
            if old_last is not None and (new_last is None or new_last < old_last):
                _fail("last retrieval observation regressed")
            if current["editorial_outcome"]["status"] not in editorial_progress[previous["editorial_outcome"]["status"]]:
                _fail("editorial outcome regressed")
            monotonic(previous["editorial_outcome"]["retry_reason_category"], current["editorial_outcome"]["retry_reason_category"], "editorial_outcome.retry_reason_category")
            if current["native_outcome"]["status"] not in native_progress[previous["native_outcome"]["status"]]:
                _fail("native outcome regressed")
            if previous["native_outcome"]["delivery_publishable"] and not current["native_outcome"]["delivery_publishable"]:
                _fail("delivery publishability regressed")
            monotonic(previous["provenance"], current["provenance"], "provenance")
        previous = current
    return accepted
