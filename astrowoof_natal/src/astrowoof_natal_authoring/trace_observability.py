"""Bounded, non-authoritative operational trace summaries.

These helpers project already-durable or already-validated native facts into
human-searchable logs.  They never grant authority and must never be allowed to
alter execution when projection or logging fails.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit


TRACE_SCHEMA = "astrowoof.sbe_operational_trace.v1"
DEFAULT_INVENTORY_LIMIT = 8
DEFAULT_CODE_LIMIT = 4
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,255}$")
_SAFE_CODE = re.compile(r"^[a-z][a-z0-9_]{0,31}$")
_SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+"),
)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str | None:
    try:
        if not path.is_file():
            return None
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except Exception:
        return None


def _safe_scalar(value: Any, *, default: str = "unknown") -> str:
    if value is None:
        return default
    rendered = str(value)
    return rendered if _SAFE_ID.fullmatch(rendered) else default


def _safe_digest(value: Any) -> str:
    rendered = str(value or "")
    return rendered if _DIGEST.fullmatch(rendered) else "unknown"


def _distribution(values: Iterable[Any]) -> str:
    counts = Counter(str(value or "unknown") for value in values)
    return ",".join(f"{key}:{counts[key]}" for key in sorted(counts)) or "none"


def bounded_identifiers(
    values: Iterable[Any], *, limit: int = DEFAULT_INVENTORY_LIMIT,
) -> dict[str, Any]:
    """Return a stable bounded inventory without leaking arbitrary strings."""
    normalized = [
        rendered for value in values
        if (rendered := _safe_scalar(value, default=""))
    ]
    prefix = normalized[:limit]
    return {
        "count": len(normalized),
        "values": prefix,
        "truncated": len(normalized) > limit,
        "overflow_count": max(len(normalized) - len(prefix), 0),
        "inventory_sha256": _canonical_sha256(normalized),
    }


def _code_distribution(
    values: Iterable[Any], *, limit: int = DEFAULT_CODE_LIMIT,
) -> dict[str, Any]:
    """Return counts for closed-looking reason codes, never arbitrary prose."""
    counts = Counter(
        rendered for value in values
        if (rendered := str(value or "")) and _SAFE_CODE.fullmatch(rendered)
    )
    ordered = {key: counts[key] for key in sorted(counts)}
    prefix_keys = list(ordered)[:limit]
    prefix = {key: ordered[key] for key in prefix_keys}
    return {
        "counts": prefix,
        "count": sum(ordered.values()),
        "unique_code_count": len(ordered),
        "truncated": len(ordered) > limit,
        "overflow_code_count": max(len(ordered) - len(prefix), 0),
        "codes_sha256": _canonical_sha256(ordered),
    }


def _report_digest(value: Any) -> str:
    return _canonical_sha256(value) if isinstance(value, Mapping) else "unknown"


def stage_evidence_summary(
    attempt: Mapping[str, Any], *, stage: str, subject_id: Any = None,
) -> dict[str, Any]:
    """Project one durably classified optional-stage attempt."""
    error = attempt.get("error")
    error = error if isinstance(error, Mapping) else {}
    provider = attempt.get("provider_metadata")
    provider = provider if isinstance(provider, Mapping) else {}
    warning_components = attempt.get("warning_components")
    warning_components = (
        warning_components if isinstance(warning_components, Mapping) else {}
    )
    result = {
        "trace_schema": TRACE_SCHEMA,
        "stage": _safe_scalar(stage),
        "subject_id": _safe_scalar(subject_id),
        "attempt_number": (
            attempt.get("attempt_number")
            if isinstance(attempt.get("attempt_number"), int)
            and not isinstance(attempt.get("attempt_number"), bool) else None
        ),
        "attempt_state": _safe_scalar(attempt.get("state")),
        "action_id": _safe_scalar(attempt.get("paid_action_id")),
        "provider_operation_id": _safe_scalar(
            provider.get("response_id") or provider.get("provider_operation_id")
        ),
        "accepted": attempt.get("accepted")
        if isinstance(attempt.get("accepted"), bool) else None,
        "improved": attempt.get("improved")
        if isinstance(attempt.get("improved"), bool) else None,
        "warning_count": attempt.get("warning_count")
        if isinstance(attempt.get("warning_count"), int) else None,
        "validation_error_count": attempt.get("validation_error_count")
        if isinstance(attempt.get("validation_error_count"), int) else None,
        "warning_components": {
            key: warning_components.get(key)
            if isinstance(warning_components.get(key), int) else None
            for key in ("validation", "lint", "authoring_rejections")
        },
        "edited_field_count": attempt.get("edited_field_count")
        if isinstance(attempt.get("edited_field_count"), int) else None,
        "omitted_target_count": attempt.get("omitted_target_count")
        if isinstance(attempt.get("omitted_target_count"), int) else None,
        "validation_report_present": isinstance(
            attempt.get("validation_report"), str
        ),
        "lint_report_present": isinstance(attempt.get("lint_report"), str),
        "error_class": _safe_scalar(error.get("type")),
        "error_fingerprint": (
            sanitize_exception(Exception(str(error.get("message") or "unknown")))[
                "fingerprint"
            ] if error else "unknown"
        ),
    }
    result["summary_sha256"] = _canonical_sha256(result)
    return result


def validation_evidence_summary(
    *, validation_report: Mapping[str, Any] | None,
    lint_report: Mapping[str, Any] | None, subject_id: Any = None,
) -> dict[str, Any]:
    """Project bounded codes/counts from reports already consumed by SBE."""
    validation = validation_report if isinstance(validation_report, Mapping) else {}
    lint = lint_report if isinstance(lint_report, Mapping) else {}
    validation_errors = validation.get("errors")
    validation_errors = validation_errors if isinstance(validation_errors, list) else []
    validation_warnings = validation.get("warnings")
    validation_warnings = validation_warnings if isinstance(validation_warnings, list) else []
    decks = lint.get("decks")
    decks = decks if isinstance(decks, list) else []
    lint_warnings: list[Any] = []
    rejection_reasons: list[Any] = []
    acceptance_states: list[Any] = []
    for deck in decks:
        if not isinstance(deck, Mapping):
            continue
        warnings = deck.get("warnings")
        if isinstance(warnings, list):
            lint_warnings.extend(
                item.get("code") for item in warnings if isinstance(item, Mapping)
            )
        acceptance = deck.get("authoring_pass_acceptance")
        if isinstance(acceptance, Mapping):
            acceptance_states.append(acceptance.get("status"))
            reasons = acceptance.get("rejection_reasons")
            if isinstance(reasons, list):
                rejection_reasons.extend(
                    item.get("code") for item in reasons if isinstance(item, Mapping)
                )
    result = {
        "trace_schema": TRACE_SCHEMA,
        "subject_id": _safe_scalar(subject_id),
        "validation_present": bool(validation),
        "validation_status": _safe_scalar(validation.get("status")),
        "validation_error_count": len(validation_errors) if validation else None,
        "validation_warning_count": len(validation_warnings) if validation else None,
        "validation_report_sha256": _report_digest(validation_report),
        "lint_present": bool(lint),
        "lint_status": _safe_scalar(lint.get("status")),
        "lint_warning_count": lint.get("warning_count")
        if isinstance(lint.get("warning_count"), int) else None,
        "lint_warning_codes": _code_distribution(lint_warnings),
        "acceptance_states": _code_distribution(acceptance_states),
        "rejection_codes": _code_distribution(rejection_reasons),
        "lint_report_sha256": _report_digest(lint_report),
    }
    result["summary_sha256"] = _canonical_sha256(result)
    return result


def publication_evidence_summary(
    state: Mapping[str, Any], result: Mapping[str, Any], receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Join one sealed publication to bounded native evidence totals."""
    ledger = state.get("spend_ledger")
    actions = ledger.get("actions", []) if isinstance(ledger, Mapping) else []
    actions = [item for item in actions if isinstance(item, Mapping)]
    subjects = state.get("subjects")
    subjects = subjects if isinstance(subjects, Mapping) else {}
    attempt_states: list[Any] = []
    for record in subjects.values():
        if not isinstance(record, Mapping):
            continue
        for key in ("polish_attempts", "creative_retry_attempts"):
            attempts = record.get(key)
            if isinstance(attempts, list):
                attempt_states.extend(
                    item.get("state") for item in attempts if isinstance(item, Mapping)
                )
        review = record.get("qualitative_review")
        if isinstance(review, Mapping):
            attempt_states.append(review.get("state"))
    result_value = {
        "trace_schema": TRACE_SCHEMA,
        "native_run_id": _safe_scalar(result.get("run_id")),
        "result_schema_version": _safe_scalar(result.get("schema_version")),
        "command_kind": _safe_scalar(result.get("command_kind")),
        "outcome": _safe_scalar(result.get("outcome")),
        "cause_code": _safe_scalar(result.get("cause_code")),
        "native_status": _safe_scalar(state.get("status")),
        "state_revision": state.get("state_revision")
        if isinstance(state.get("state_revision"), int) else None,
        "result_id": _safe_scalar(result.get("result_id")),
        "result_sha256": _safe_digest(result.get("result_sha256")),
        "receipt_id": _safe_scalar(receipt.get("receipt_id")),
        "receipt_sha256": _safe_digest(receipt.get("receipt_sha256")),
        "invocation_id": _safe_scalar(result.get("invocation_id")),
        "checkpoint_basis_sha256": _safe_digest(
            receipt.get("checkpoint_basis_sha256")
        ),
        "snapshot_sha256": _safe_digest(receipt.get("snapshot_sha256")),
        "action_count": len(actions),
        "action_state_counts": _distribution(item.get("state") for item in actions),
        "provider_identity_count": sum(
            1 for item in actions if isinstance(item.get("provider"), Mapping)
        ),
        "subject_state_counts": _distribution(
            item.get("state") for item in subjects.values()
            if isinstance(item, Mapping)
        ),
        "optional_stage_state_counts": _distribution(attempt_states),
    }
    result_value["summary_sha256"] = _canonical_sha256(result_value)
    return result_value


def sanitize_exception(
    exc: BaseException, *, endpoint: str | None = None, maximum_length: int = 240,
) -> dict[str, str]:
    """Create a bounded diagnostic without credentials or URL query material."""
    message = " ".join(str(exc).split())
    for pattern in _SECRET_PATTERNS:
        message = pattern.sub("[REDACTED]", message)
    message = message[:maximum_length]
    endpoint_identity = "unknown"
    if endpoint:
        try:
            parsed = urlsplit(endpoint)
            if parsed.scheme in {"http", "https"} and parsed.netloc:
                endpoint_identity = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        except Exception:
            endpoint_identity = "unknown"
    return {
        "exception_class": type(exc).__name__,
        "sanitized_message": message or type(exc).__name__,
        "fingerprint": hashlib.sha256(
            f"{type(exc).__name__}:{message}".encode("utf-8")
        ).hexdigest()[:16],
        "endpoint": endpoint_identity,
    }


def workspace_fingerprint(
    run_dir: Path,
    state: Mapping[str, Any],
    *,
    validation_outcome: str,
    sbe_release: str,
) -> dict[str, Any]:
    """Project the exact safe identity of one validated restored workspace."""
    workspace = state.get("workspace_contract")
    workspace = workspace if isinstance(workspace, Mapping) else {}
    logical_root = workspace.get("logical_root")
    ledger = state.get("spend_ledger")
    ledger = ledger if isinstance(ledger, Mapping) else {}
    actions = ledger.get("actions", [])
    actions = actions if isinstance(actions, list) else []
    route_family = state.get("route_family") or state.get("authoring_route")
    if not route_family:
        for action in actions:
            binding = action.get("binding") if isinstance(action, Mapping) else None
            route = binding.get("route") if isinstance(binding, Mapping) else None
            if isinstance(route, str) and route.startswith("bounded_natal"):
                route_family = "bounded_natal"
                break
        else:
            route_family = "exact_natal" if actions else None
    snapshot_path = run_dir / "workspace-snapshot.json"
    snapshot_sha256 = _file_sha256(snapshot_path)
    member_count: int | None = None
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        members = snapshot.get("members")
        member_count = len(members) if isinstance(members, list) else None
    except Exception:
        pass
    try:
        spc_release = importlib.metadata.version("semantic-projection-core")
    except importlib.metadata.PackageNotFoundError:
        spc_release = "unknown"
    result = {
        "trace_schema": TRACE_SCHEMA,
        "native_run_id": _safe_scalar(state.get("run_id")),
        "native_schema": _safe_scalar(state.get("schema_version")),
        "route_family": _safe_scalar(route_family),
        "native_status": _safe_scalar(state.get("status")),
        "state_revision": (
            state.get("state_revision")
            if isinstance(state.get("state_revision"), int)
            else None
        ),
        "logical_root_sha256": (
            hashlib.sha256(str(logical_root).encode("utf-8")).hexdigest()
            if isinstance(logical_root, str) and logical_root else "unknown"
        ),
        "snapshot_sha256": snapshot_sha256 or "unknown",
        "snapshot_member_count": member_count,
        "checkpoint_generation": (
            state.get("checkpoint_generation")
            if isinstance(state.get("checkpoint_generation"), int)
            else None
        ),
        "checkpoint_object_id": _safe_scalar(state.get("checkpoint_object_id")),
        "checkpoint_basis_sha256": _safe_digest(
            state.get("checkpoint_basis_sha256")
        ),
        "validation_outcome": _safe_scalar(validation_outcome),
        "sbe_release": _safe_scalar(sbe_release),
        "spc_release": _safe_scalar(spc_release),
    }
    result["fingerprint_sha256"] = _canonical_sha256(result)
    return result


def native_state_summary(state: Mapping[str, Any]) -> dict[str, Any]:
    ledger = state.get("spend_ledger")
    actions = ledger.get("actions", []) if isinstance(ledger, Mapping) else []
    actions = [item for item in actions if isinstance(item, Mapping)]
    action_inventory = bounded_identifiers(
        item.get("action_id") for item in actions
    )
    provider_ids = bounded_identifiers(
        provider.get("id")
        for item in actions
        if isinstance((provider := item.get("provider")), Mapping)
    )
    intent = state.get("external_authority_v2_dispatch_intent")
    intent = intent if isinstance(intent, Mapping) else {}
    return {
        "native_status": _safe_scalar(state.get("status")),
        "state_revision": (
            state.get("state_revision")
            if isinstance(state.get("state_revision"), int) else None
        ),
        "action_inventory": action_inventory,
        "action_state_counts": _distribution(
            item.get("state") for item in actions
        ),
        "action_stage_counts": _distribution(
            (item.get("binding") or {}).get("stage")
            if isinstance(item.get("binding"), Mapping) else None
            for item in actions
        ),
        "provider_inventory": provider_ids,
        "provider_custody_count": sum(
            1 for item in actions
            if isinstance(item.get("provider"), Mapping)
            and item.get("state") in {
                "PROVIDER_ID_RECORDED", "WAITING", "PROVIDER_PENDING",
                "COMPLETED_PROVIDER_EVIDENCE",
            }
        ),
        "prepared_count": sum(1 for item in actions if item.get("state") == "PREPARED"),
        "ambiguous_count": sum(
            1 for item in actions
            if item.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION"
        ),
        "v2_intent_present": bool(intent),
        "v2_intent_state": _safe_scalar(intent.get("state")),
        "v2_intent_request_sha256": _safe_digest(intent.get("request_sha256")),
        "v2_intent_grant_sha256": _safe_digest(intent.get("grant_sha256")),
        "v2_intent_action_inventory": bounded_identifiers(
            intent.get("ordered_action_ids", [])
            if isinstance(intent.get("ordered_action_ids"), list) else []
        ),
    }


def decision_summary(
    document: Mapping[str, Any], *, command: str, operation: str | None = None,
) -> dict[str, Any]:
    """Project common safe fields from a validated public result/inspection."""
    basis = document.get("checkpoint_basis")
    basis = basis if isinstance(basis, Mapping) else document
    branch = document.get("execution_branch")
    branch = branch if isinstance(branch, Mapping) else {}
    temporal = document.get("temporal_decision")
    temporal = temporal if isinstance(temporal, Mapping) else {}
    capacity = document.get("execution_capacity")
    capacity = capacity if isinstance(capacity, Mapping) else {}
    custody = basis.get("provider_custody")
    custody = custody if isinstance(custody, Mapping) else {}
    custody_actions = custody.get("actions", [])
    custody_actions = custody_actions if isinstance(custody_actions, list) else []
    inventory = basis.get("action_inventory")
    inventory = inventory if isinstance(inventory, Mapping) else {}
    actions = inventory.get("actions", [])
    actions = actions if isinstance(actions, list) else []
    local_work = basis.get("local_work_inventory")
    local_work = local_work if isinstance(local_work, Mapping) else {}
    local_operations = local_work.get("operations", [])
    local_operations = local_operations if isinstance(local_operations, list) else []
    consumed_keys = local_work.get("consumed_operation_keys", [])
    consumed_keys = consumed_keys if isinstance(consumed_keys, list) else []
    retry_lineage = basis.get("retry_lineage_inventory")
    retry_lineage = retry_lineage if isinstance(retry_lineage, Mapping) else {}
    retry_attempts = retry_lineage.get("attempts", [])
    retry_attempts = retry_attempts if isinstance(retry_attempts, list) else []
    terminal = basis.get("terminal")
    terminal = terminal if isinstance(terminal, Mapping) else {}
    selected = (
        branch.get("command") or temporal.get("selected_command")
        or document.get("selected_command") or "unknown"
    )
    reason = (
        branch.get("reason_code") or temporal.get("reason_code")
        or capacity.get("reason_code") or document.get("reason_code") or "unknown"
    )
    action_ids = branch.get("action_ids")
    if not isinstance(action_ids, list):
        action_ids = temporal.get("selected_action_ids")
    if not isinstance(action_ids, list):
        action_ids = document.get("ordered_action_ids")
    if not isinstance(action_ids, list):
        action_ids = [
            item.get("action_id") for item in actions if isinstance(item, Mapping)
        ]
    provider_ids = [
        item.get("provider_operation_id") or item.get("provider_response_id")
        for item in custody_actions if isinstance(item, Mapping)
    ]
    result = {
        "trace_schema": TRACE_SCHEMA,
        "command": _safe_scalar(command),
        "operation": _safe_scalar(operation),
        "schema_version": _safe_scalar(document.get("schema_version")),
        "native_run_id": _safe_scalar(document.get("run_id")),
        "outcome": _safe_scalar(
            document.get("outcome") or document.get("disposition")
        ),
        "selected_command": _safe_scalar(selected),
        "reason_code": _safe_scalar(reason),
        "capacity_disposition": _safe_scalar(capacity.get("disposition")),
        "eligible_now": branch.get("eligible_now", temporal.get("eligible_now")),
        "action_inventory": bounded_identifiers(action_ids),
        "provider_custody_inventory": bounded_identifiers(provider_ids),
        "provider_custody_count": len(custody_actions),
        "provider_custody_state": _safe_scalar(custody.get("state")),
        "local_dependency_count": len(basis.get("local_dependencies", []))
        if isinstance(basis.get("local_dependencies"), list) else None,
        "local_work_inventory": bounded_identifiers(
            item.get("operation_key") or item.get("operation_id")
            for item in local_operations if isinstance(item, Mapping)
        ),
        "consumed_local_work_count": len(consumed_keys),
        "retry_attempt_count": len(retry_attempts),
        "retry_lineage_status": _safe_scalar(retry_lineage.get("status")),
        "retry_conflict_classification": _safe_scalar(
            retry_lineage.get("conflict_classification")
        ),
        "terminal_outcome": _safe_scalar(terminal.get("outcome")),
        "terminal": terminal.get("terminal"),
        "external_authority_request_sha256": _safe_digest(
            (document.get("external_authority_request") or {}).get(
                "external_authority_request_sha256"
            ) if isinstance(document.get("external_authority_request"), Mapping)
            else document.get("request_sha256")
        ),
        "result_id": _safe_scalar(document.get("result_id")),
        "receipt_id": _safe_scalar(document.get("receipt_id")),
    }
    result["summary_sha256"] = _canonical_sha256(result)
    return result


def _render_inventory(value: Mapping[str, Any]) -> str:
    items = ",".join(str(item) for item in value.get("values", [])) or "none"
    return (
        f"count:{value.get('count', 0)};values:{items};"
        f"truncated:{str(bool(value.get('truncated'))).lower()};"
        f"overflow:{value.get('overflow_count', 0)};"
        f"sha256:{value.get('inventory_sha256', 'unknown')}"
    )


def _render_code_distribution(value: Mapping[str, Any]) -> str:
    counts = value.get("counts")
    counts = counts if isinstance(counts, Mapping) else {}
    rendered = ",".join(
        f"{key}:{counts[key]}" for key in sorted(counts)
    ) or "none"
    return (
        f"count:{value.get('count', 0)};unique:{value.get('unique_code_count', 0)};"
        f"codes:{rendered};truncated:{str(bool(value.get('truncated'))).lower()};"
        f"overflow:{value.get('overflow_code_count', 0)};"
        f"sha256:{value.get('codes_sha256', 'unknown')}"
    )


def log_workspace_fingerprint(
    logger: logging.Logger, run_dir: Path, state: Mapping[str, Any],
    *, validation_outcome: str, sbe_release: str,
) -> dict[str, Any] | None:
    try:
        value = workspace_fingerprint(
            run_dir, state, validation_outcome=validation_outcome,
            sbe_release=sbe_release,
        )
        logger.info(
            "workspace_fingerprint validation=%s native_schema=%s route=%s status=%s "
            "revision=%s logical_root_sha256=%s snapshot_sha256=%s "
            "snapshot_members=%s checkpoint_generation=%s "
            "checkpoint_object_id=%s checkpoint_basis_sha256=%s "
            "sbe_release=%s spc_release=%s fingerprint_sha256=%s",
            value["validation_outcome"], value["native_schema"],
            value["route_family"],
            value["native_status"], value["state_revision"],
            value["logical_root_sha256"], value["snapshot_sha256"],
            value["snapshot_member_count"], value["checkpoint_generation"],
            value["checkpoint_object_id"], value["checkpoint_basis_sha256"],
            value["sbe_release"], value["spc_release"],
            value["fingerprint_sha256"],
        )
        return value
    except Exception:
        return None


def log_native_state_summary(
    logger: logging.Logger, state: Mapping[str, Any], *, phase: str,
) -> dict[str, Any] | None:
    try:
        value = native_state_summary(state)
        logger.info(
            "native_state_summary phase=%s status=%s revision=%s actions=%s "
            "action_states=%s action_stages=%s providers=%s custody_count=%s "
            "prepared_count=%s ambiguous_count=%s v2_intent_present=%s "
            "v2_intent_state=%s v2_request_sha256=%s v2_grant_sha256=%s "
            "v2_actions=%s",
            _safe_scalar(phase), value["native_status"], value["state_revision"],
            _render_inventory(value["action_inventory"]),
            value["action_state_counts"], value["action_stage_counts"],
            _render_inventory(value["provider_inventory"]),
            value["provider_custody_count"], value["prepared_count"],
            value["ambiguous_count"], value["v2_intent_present"],
            value["v2_intent_state"], value["v2_intent_request_sha256"],
            value["v2_intent_grant_sha256"],
            _render_inventory(value["v2_intent_action_inventory"]),
        )
        return value
    except Exception:
        return None


def log_decision_summary(
    logger: logging.Logger, document: Mapping[str, Any], *, command: str,
    operation: str | None = None,
) -> dict[str, Any] | None:
    try:
        value = decision_summary(document, command=command, operation=operation)
        logger.info(
            "native_decision_summary command=%s operation=%s schema=%s outcome=%s "
            "selected_command=%s reason=%s capacity=%s eligible_now=%s "
            "actions=%s provider_custody=%s local_dependency_count=%s "
            "custody_state=%s local_work=%s consumed_local_work_count=%s "
            "retry_attempt_count=%s retry_lineage_status=%s "
            "retry_conflict=%s terminal_outcome=%s terminal=%s "
            "authority_request_sha256=%s result_id=%s receipt_id=%s "
            "summary_sha256=%s",
            value["command"], value["operation"], value["schema_version"],
            value["outcome"], value["selected_command"], value["reason_code"],
            value["capacity_disposition"], value["eligible_now"],
            _render_inventory(value["action_inventory"]),
            _render_inventory(value["provider_custody_inventory"]),
            value["local_dependency_count"],
            value["provider_custody_state"],
            _render_inventory(value["local_work_inventory"]),
            value["consumed_local_work_count"], value["retry_attempt_count"],
            value["retry_lineage_status"],
            value["retry_conflict_classification"],
            value["terminal_outcome"], value["terminal"],
            value["external_authority_request_sha256"], value["result_id"],
            value["receipt_id"], value["summary_sha256"],
        )
        return value
    except Exception:
        return None


def log_stage_evidence_summary(
    logger: logging.Logger, attempt: Mapping[str, Any], *, stage: str,
    subject_id: Any = None,
) -> dict[str, Any] | None:
    try:
        value = stage_evidence_summary(
            attempt, stage=stage, subject_id=subject_id,
        )
        logger.info(
            "native_stage_evidence_summary stage=%s subject=%s attempt=%s "
            "state=%s action_id=%s provider_id=%s accepted=%s improved=%s "
            "warning_count=%s validation_error_count=%s warning_components=%s "
            "edited_field_count=%s omitted_target_count=%s "
            "validation_report_present=%s lint_report_present=%s "
            "error_class=%s error_fingerprint=%s summary_sha256=%s",
            value["stage"], value["subject_id"], value["attempt_number"],
            value["attempt_state"], value["action_id"],
            value["provider_operation_id"], value["accepted"],
            value["improved"], value["warning_count"],
            value["validation_error_count"], value["warning_components"],
            value["edited_field_count"], value["omitted_target_count"],
            value["validation_report_present"], value["lint_report_present"],
            value["error_class"], value["error_fingerprint"],
            value["summary_sha256"],
        )
        return value
    except Exception:
        return None


def log_validation_evidence_summary(
    logger: logging.Logger, *, validation_report: Mapping[str, Any] | None,
    lint_report: Mapping[str, Any] | None, subject_id: Any = None,
) -> dict[str, Any] | None:
    try:
        value = validation_evidence_summary(
            validation_report=validation_report, lint_report=lint_report,
            subject_id=subject_id,
        )
        logger.info(
            "native_validation_evidence_summary subject=%s validation_present=%s "
            "validation_status=%s validation_errors=%s validation_warnings=%s "
            "validation_sha256=%s lint_present=%s lint_status=%s "
            "lint_warnings=%s lint_warning_codes=%s acceptance_states=%s "
            "rejection_codes=%s lint_sha256=%s summary_sha256=%s",
            value["subject_id"], value["validation_present"],
            value["validation_status"], value["validation_error_count"],
            value["validation_warning_count"],
            value["validation_report_sha256"], value["lint_present"],
            value["lint_status"], value["lint_warning_count"],
            _render_code_distribution(value["lint_warning_codes"]),
            _render_code_distribution(value["acceptance_states"]),
            _render_code_distribution(value["rejection_codes"]),
            value["lint_report_sha256"],
            value["summary_sha256"],
        )
        return value
    except Exception:
        return None


def log_publication_evidence_summary(
    logger: logging.Logger, state: Mapping[str, Any], result: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any] | None:
    try:
        value = publication_evidence_summary(state, result, receipt)
        logger.info(
            "native_publication_evidence_summary run_id=%s result_schema=%s "
            "command_kind=%s outcome=%s cause=%s "
            "native_status=%s revision=%s result_id=%s result_sha256=%s "
            "receipt_id=%s receipt_sha256=%s invocation_id=%s "
            "checkpoint_basis_sha256=%s snapshot_sha256=%s action_count=%s "
            "action_states=%s provider_identity_count=%s subject_states=%s "
            "optional_stage_states=%s summary_sha256=%s",
            value["native_run_id"], value["result_schema_version"],
            value["command_kind"], value["outcome"], value["cause_code"],
            value["native_status"], value["state_revision"],
            value["result_id"], value["result_sha256"], value["receipt_id"],
            value["receipt_sha256"], value["invocation_id"],
            value["checkpoint_basis_sha256"], value["snapshot_sha256"],
            value["action_count"], value["action_state_counts"],
            value["provider_identity_count"], value["subject_state_counts"],
            value["optional_stage_state_counts"], value["summary_sha256"],
        )
        return value
    except Exception:
        return None


def log_cli_exit(
    logger: logging.Logger, *, command: str, operation: str | None,
    exit_code: int, outcome: Any, result_id: Any = None,
    receipt_id: Any = None, authoritative_transport: str,
    exception: BaseException | None = None,
) -> None:
    try:
        diagnostic = sanitize_exception(exception) if exception is not None else None
        logger.info(
            "command_exit command=%s operation=%s exit_code=%s outcome=%s "
            "result_id=%s receipt_id=%s authoritative_transport=%s "
            "exception_class=%s exception_fingerprint=%s",
            _safe_scalar(command), _safe_scalar(operation), int(exit_code),
            _safe_scalar(outcome), _safe_scalar(result_id), _safe_scalar(receipt_id),
            _safe_scalar(authoritative_transport),
            diagnostic["exception_class"] if diagnostic else "none",
            diagnostic["fingerprint"] if diagnostic else "none",
        )
    except Exception:
        return
