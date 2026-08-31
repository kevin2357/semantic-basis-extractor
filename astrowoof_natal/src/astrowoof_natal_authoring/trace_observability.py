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
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,255}$")
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
