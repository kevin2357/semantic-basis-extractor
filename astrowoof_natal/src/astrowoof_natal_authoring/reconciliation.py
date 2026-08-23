"""Durable scheduling evidence for known provider-operation reconciliation."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import logging
import os
import threading
import time
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from .lifecycle_contracts import (
    PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
    PROVIDER_RECONCILIATION_POLICY,
    PROVIDER_RECONCILIATION_POLICY_SCHEMA,
    PROVIDER_RECONCILIATION_POLICY_SCHEMA_V0_1,
)
from .response_diagnostics import (
    build_response_retrieval_diagnostic,
    sanitize_error_message,
)
from .application_logging import (
    bind_logging_context,
    current_logging_context,
    logging_context,
)


logger = logging.getLogger(__name__)


RECONCILIABLE_PROVIDER_STATES = {
    "PROVIDER_ID_RECORDED", "WAITING",
}
EXACT_RUN_CONTRACT = "astrowoof.semantic_closure_run.v0.9"
BOUNDED_RUN_CONTRACT = "astrowoof.bounded_natal.authoring_run.v2"
LEGACY_BOUNDED_RUN_CONTRACT = "astrowoof.bounded_natal.authoring_run.v1"


@dataclass(frozen=True)
class ProviderReconciliationAdapters:
    """Configured provider adapters for one route-neutral reconciliation cycle."""

    exact_interactive_provider: Any = None
    exact_batch_provider: Any = None
    exact_batch_transport: Any = None
    bounded_interactive_provider: Any = None
    bounded_batch_provider: Any = None
    bounded_batch_transport: Any = None
    max_attempts: int = 3
    python_executable: Path = Path(os.sys.executable)
    polish_provider: Any = None
    critic_provider: Any = None
    qualitative_editor_provider: Any = None


def native_provider_route_identity(
    state: dict[str, Any], action: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return strict native route/mechanism identity and adapter classification."""
    route_contract = state.get("route_contract")
    if (
        route_contract in {BOUNDED_RUN_CONTRACT, LEGACY_BOUNDED_RUN_CONTRACT}
        and state.get("route") in {"bounded_natal.v1", "bounded_natal.v2"}
    ):
        route_family = "bounded_natal"
        contract = str(route_contract)
    elif route_contract is None and state.get("schema_version") == EXACT_RUN_CONTRACT:
        route_family = "exact_natal"
        contract = EXACT_RUN_CONTRACT
    else:
        return {
            "route_family": None, "route_contract": str(route_contract or ""),
            "provider_operation_kind": None, "native_operation_ref": None,
            "valid": False, "adapter": "unsupported",
            "reason_code": "route_or_stage_not_supported",
        }
    if action is None:
        return {
            "route_family": route_family, "route_contract": contract,
            "provider_operation_kind": None, "native_operation_ref": None,
            "valid": True, "adapter": None, "reason_code": None,
        }
    binding = action.get("binding") or {}
    provider = action.get("provider") or {}
    kind = str(provider.get("kind") or "")
    service = str(binding.get("service_level") or "")
    stage = str(binding.get("stage") or "")
    native_ref = str(binding.get("route") or "")
    stages = {
        "authoring_initial", "creative_retry", "polish",
        "qualitative_critic", "qualitative_candidate",
    }
    valid = bool(kind in {"response", "batch"} and stage in stages and native_ref)
    adapter = "unsupported"
    if route_family == "exact_natal" and kind == "response" and service == "interactive":
        adapter = "exact_interactive"
    elif (
        route_family == "exact_natal" and kind == "batch" and service == "batch"
        and stage in {"authoring_initial", "creative_retry"}
    ):
        adapter = "exact_batch"
        rounds = (state.get("batch_service") or {}).get("rounds") or []
        matches = [
            item for item in rounds
            if f"batch-round-{int(item.get('round_number') or 0):03d}" == native_ref
            and item.get("batch_id") == provider.get("id")
        ]
        valid = bool(valid and len(matches) == 1)
    elif (
        route_family == "bounded_natal" and kind == "response"
        and service == "interactive"
        and native_ref.startswith(("bounded_natal.v1:", "bounded_natal.v2:"))
    ):
        adapter = "bounded_interactive"
    elif (
        route_family == "bounded_natal" and kind == "batch"
        and service == "batch"
        and contract == BOUNDED_RUN_CONTRACT
        and stage in {"authoring_initial", "creative_retry"}
        and native_ref.startswith("bounded_natal.v2:batch-round-")
    ):
        adapter = "bounded_batch"
        rounds = (state.get("batch_service") or {}).get("rounds") or []
        matches = [
            item for item in rounds
            if f"bounded_natal.v2:batch-round-{int(item.get('round_number') or 0):03d}"
            == native_ref
            and item.get("batch_id") == provider.get("id")
        ]
        valid = bool(valid and len(matches) == 1)
    elif route_family == "bounded_natal" and (kind == "batch" or service == "batch"):
        adapter = "bounded_batch_unsupported"
        valid = False
    else:
        valid = False
    return {
        "route_family": route_family, "route_contract": contract,
        "provider_operation_kind": kind or None,
        "native_operation_ref": native_ref or None,
        "valid": valid, "adapter": adapter,
        "reason_code": None if valid else "route_or_stage_not_supported",
    }


class ProviderRetrievalIdentityMismatch(ValueError):
    """A GET response did not match the already durable provider identity."""


def parse_utc_instant(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Reconciliation instants must be UTC timestamps")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("Reconciliation instants must be UTC")
    return parsed.astimezone(timezone.utc)


def utc_instant(value: datetime) -> str:
    normalized = value.astimezone(timezone.utc)
    return normalized.isoformat(timespec="seconds").replace("+00:00", "Z")


def delay_seconds(attempt_count: int, *, mechanism: str = "response") -> int:
    """Return the frozen lower-bound delay after ``attempt_count`` retrievals."""
    if not isinstance(attempt_count, int) or isinstance(attempt_count, bool):
        raise ValueError("Reconciliation attempt count must be an integer")
    if attempt_count < 0:
        raise ValueError("Reconciliation attempt count cannot be negative")
    if mechanism not in {"response", "batch"}:
        raise ValueError(f"Unsupported provider reconciliation mechanism: {mechanism}")
    policy = PROVIDER_RECONCILIATION_POLICY["mechanisms"][mechanism]
    delays = policy["delays_seconds"]
    return delays[min(attempt_count, len(delays) - 1)]


def initial_timing(*, recorded_at: str, mechanism: str = "response") -> dict[str, Any]:
    recorded = parse_utc_instant(recorded_at)
    return {
        "policy_version": PROVIDER_RECONCILIATION_POLICY_SCHEMA,
        "provider_retrieval_attempt_count": 0,
        "last_attempt_at": None,
        "last_outcome": "provider_identity_recorded",
        "resume_not_before": utc_instant(
            recorded + timedelta(seconds=delay_seconds(0, mechanism=mechanism))
        ),
    }


def record_attempt(
    timing: dict[str, Any], *, attempted_at: str, outcome: str,
    mechanism: str = "response",
) -> dict[str, Any]:
    if outcome not in {"pending", "completed", "transport_warning", "provider_failed"}:
        raise ValueError(f"Unsupported reconciliation outcome: {outcome}")
    if timing.get("policy_version") not in {
        PROVIDER_RECONCILIATION_POLICY_SCHEMA,
        PROVIDER_RECONCILIATION_POLICY_SCHEMA_V0_1,
    }:
        raise ValueError("Unsupported reconciliation timing policy")
    attempted = parse_utc_instant(attempted_at)
    previous = timing.get("last_attempt_at")
    if previous is not None and attempted < parse_utc_instant(previous):
        raise ValueError("Reconciliation attempt time cannot move backwards")
    count = int(timing.get("provider_retrieval_attempt_count") or 0) + 1
    timing["provider_retrieval_attempt_count"] = count
    timing["last_attempt_at"] = utc_instant(attempted)
    timing["last_outcome"] = outcome
    timing["resume_not_before"] = (
        None if outcome in {"completed", "provider_failed"}
        else utc_instant(
            attempted + timedelta(seconds=delay_seconds(count, mechanism=mechanism))
        )
    )
    return timing


def validated_timing(action: dict[str, Any]) -> dict[str, Any] | None:
    if action.get("state") not in RECONCILIABLE_PROVIDER_STATES:
        return None
    service = (action.get("binding") or {}).get("service_level")
    kind = (action.get("provider") or {}).get("kind")
    if (service, kind) not in {("interactive", "response"), ("batch", "batch")}:
        return None
    provider = action.get("provider") or {}
    if not provider.get("id"):
        return None
    timing = action.get("provider_reconciliation")
    if not isinstance(timing, dict):
        return None
    required = {
        "policy_version", "provider_retrieval_attempt_count", "last_attempt_at",
        "last_outcome", "resume_not_before",
    }
    if set(timing) != required:
        return None
    if timing["policy_version"] not in {
        PROVIDER_RECONCILIATION_POLICY_SCHEMA,
        PROVIDER_RECONCILIATION_POLICY_SCHEMA_V0_1,
    }:
        return None
    count = timing["provider_retrieval_attempt_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        return None
    try:
        if timing["resume_not_before"] is not None:
            parse_utc_instant(timing["resume_not_before"])
        elif timing["last_outcome"] != "completed":
            return None
        if timing["last_attempt_at"] is not None:
            parse_utc_instant(timing["last_attempt_at"])
    except (TypeError, ValueError):
        return None
    return deepcopy(timing)


@contextmanager
def _single_writer(run_dir: Path):
    """Use the paid-action byte lock for one native reconciliation mutation."""
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


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconcile_provider_cycle(
    run_dir: Path,
    *,
    retrieve: Callable[[str, float], dict[str, Any]],
    observed_at: str,
    endpoint_base_url: str | None = None,
    provider_secret: str | None = None,
) -> dict[str, Any]:
    """Poll one bounded wave of due known interactive provider operations.

    ``retrieve`` is retrieval-only: this operation never supplies a request body
    and never calls a provider submission route.
    """
    from .closure import (
        SNAPSHOT_NAME,
        load_json,
        persist_state,
        sha256_file,
        validate_workspace_snapshot,
        write_json_atomic,
        write_workspace_snapshot,
    )
    from .lifecycle import inspect_lifecycle

    run_dir = run_dir.resolve()
    instant = utc_instant(parse_utc_instant(observed_at))
    with _single_writer(run_dir):
        state = load_json(run_dir / "run.json")
        bind_logging_context(
            run_id=state.get("run_id"), current_state=state.get("status")
        )
        logger.info(
            "reconciliation_cycle_start state_revision=%s observed_at=%s",
            state.get("state_revision"), instant,
        )
        validate_workspace_snapshot(run_dir, state)
        before = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=instant,
        )
        capacity = before["execution_capacity"]
        completed_evidence = [
            item for item in before["provider_custody"]["actions"]
            if item["custody_classification"] == "completed_provider_evidence"
        ]
        if capacity["disposition"] == "continue_local_cycle" and completed_evidence:
            completed_ids = [item["action_id"] for item in completed_evidence]
            operation_summaries = [{
                "action_id": item["action_id"],
                "route_family": item["route_family"],
                "provider_operation_kind": "response",
                "provider_operation_id": item["provider_operation_id"],
                "retrieval_outcome": "completed",
                "cost_disposition": (
                    "provider_usage_reported"
                    if json.loads((
                        run_dir / "lifecycle" / "provider-reconciliation" /
                        f"{item['action_id']}.response.json"
                    ).read_text(encoding="utf-8")).get("usage") is not None
                    else "provider_usage_unavailable_billing_reconciliation_pending"
                ),
                "member_count": None, "ingested_member_count": None,
                "failed_member_count": None,
            } for item in completed_evidence]
            cycle = {
                "started_at": instant, "finished_at": instant,
                "wall_clock_limit_seconds": 20,
                "provider_retrieval_count": 0, "retrieved_action_ids": [],
                "completed_action_ids": completed_ids,
                "still_pending_action_ids": [],
                "transport_warning_action_ids": [],
            }
            evidence_root = run_dir / "lifecycle" / "provider-reconciliation"
            artifact = evidence_root / f"cycle-{state['state_revision']:08d}-local.json"
            write_json_atomic(artifact, {
                "schema_version": "astrowoof.provider_reconciliation_cycle_record.v0.1",
                "run_id": state["run_id"], "decision_basis": before["observation"],
                "cycle": cycle, "provider_operations": operation_summaries,
            })
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            return {
                "schema_version": PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
                "run_id": state["run_id"], "outcome": "progressed_local",
                "decision_basis": before["observation"], "cycle": cycle,
                "inspection": after, "provider_operations": operation_summaries,
                "result_checkpoint": {
                    "operator_state_revision": state["state_revision"],
                    "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                    "result_artifact": {
                        "logical_path": artifact.relative_to(run_dir).as_posix(),
                        "bytes": artifact.stat().st_size,
                        "sha256": _file_sha256(artifact),
                    },
                },
            }
        if capacity["disposition"] == "release_until_due":
            return {
                "schema_version": PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
                "run_id": state["run_id"],
                "outcome": "not_due",
                "decision_basis": before["observation"],
                "cycle": {
                    "started_at": instant,
                    "finished_at": instant,
                    "wall_clock_limit_seconds": 20,
                    "provider_retrieval_count": 0,
                    "retrieved_action_ids": [],
                    "completed_action_ids": [],
                    "still_pending_action_ids": before["provider_custody"]["action_ids"],
                    "transport_warning_action_ids": [],
                },
                "inspection": before,
                "provider_operations": [],
            }
        if capacity["disposition"] in {
            "unsupported_retain_capacity", "retain_for_review",
            "await_external_authority", "terminal",
        }:
            return {
                "schema_version": PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
                "run_id": state["run_id"],
                "outcome": {
                    "unsupported_retain_capacity": "unsupported",
                    "retain_for_review": "review_required",
                    "await_external_authority": "awaiting_external_authority",
                    "terminal": "terminal",
                }[capacity["disposition"]],
                "decision_basis": before["observation"],
                "cycle": {
                    "started_at": instant, "finished_at": instant,
                    "wall_clock_limit_seconds": 20,
                    "provider_retrieval_count": 0,
                    "retrieved_action_ids": [], "completed_action_ids": [],
                    "still_pending_action_ids": before["provider_custody"]["action_ids"],
                    "transport_warning_action_ids": [],
                },
                "inspection": before,
                "provider_operations": [],
                "result_checkpoint": {
                    "operator_state_revision": before["observation"]["operator_state_revision"],
                    "snapshot_sha256": before["observation"]["snapshot_sha256"],
                    "result_artifact": {
                        "logical_path": SNAPSHOT_NAME,
                        "bytes": (run_dir / SNAPSHOT_NAME).stat().st_size,
                        "sha256": before["observation"]["snapshot_sha256"],
                    },
                },
            }
        due_ids = set(before["provider_custody"]["next_due_action_ids"])
        now = parse_utc_instant(instant)
        actions: list[dict[str, Any]] = []
        for action in (state.get("spend_ledger") or {}).get("actions", []):
            timing = validated_timing(action)
            if (
                action.get("action_id") in due_ids
                and timing is not None
                and timing["resume_not_before"] is not None
                and parse_utc_instant(timing["resume_not_before"]) <= now
            ):
                actions.append(action)
        actions.sort(key=lambda item: (
            item["provider_reconciliation"]["resume_not_before"],
            item["action_id"],
        ))
        response_policy = PROVIDER_RECONCILIATION_POLICY["mechanisms"]["response"]
        actions = actions[:response_policy["maximum_due_actions_per_cycle"]]
        if not actions:
            raise ValueError(
                "No due known interactive provider operation is eligible for retrieval"
            )
        logger.info(
            "reconciliation_wave_selected due_count=%s selected_count=%s "
            "deferred_count=%s action_ids=%s",
            len(due_ids), len(actions), max(len(due_ids) - len(actions), 0),
            [item["action_id"] for item in actions],
        )
        parent_log_context = current_logging_context()

        def get(action: dict[str, Any]) -> tuple[
            str, dict[str, Any] | Exception, str, str, int
        ]:
            action_id = action["action_id"]
            provider_id = action["provider"]["id"]
            with logging_context(
                host_id=parent_log_context["host_id"],
                run_id=state.get("run_id"),
                invocation_id=parent_log_context["invocation_id"],
                current_state=action.get("state"),
            ):
                logger.info(
                    "provider_retrieval_start action_id=%s provider_id=%s timeout_s=%s",
                    action_id, provider_id,
                    response_policy["provider_request_timeout_seconds"],
                )
                started_at = datetime.now(timezone.utc).isoformat(
                    timespec="milliseconds"
                ).replace("+00:00", "Z")
                started = time.monotonic()
                try:
                    response = retrieve(
                        provider_id,
                        float(response_policy["provider_request_timeout_seconds"]),
                    )
                    value: dict[str, Any] | Exception = response
                except Exception as exc:
                    logger.warning(
                        "provider_retrieval_exception action_id=%s provider_id=%s "
                        "error_class=%s error=%s",
                        action_id, provider_id, type(exc).__name__,
                        sanitize_error_message(exc, secret=provider_secret),
                    )
                    value = exc
                finished_at = datetime.now(timezone.utc).isoformat(
                    timespec="milliseconds"
                ).replace("+00:00", "Z")
                duration_ms = round((time.monotonic() - started) * 1000)
                logger.info(
                    "provider_retrieval_returned action_id=%s provider_id=%s "
                    "duration_ms=%s result_class=%s",
                    action_id, provider_id, duration_ms, type(value).__name__,
                )
                return action_id, value, started_at, finished_at, duration_ms

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=response_policy["maximum_parallel_requests"],
            thread_name_prefix="astrowoof-retrieve",
        ) as executor:
            results = list(executor.map(get, actions))

        retrieved: list[str] = []
        completed: list[str] = []
        warnings: list[str] = []
        identity_conflicts: list[str] = []
        provider_failures: list[str] = []
        operation_summaries: list[dict[str, Any]] = []
        diagnostic_artifacts: list[dict[str, Any]] = []
        by_id = {item["action_id"]: item for item in actions}
        evidence_root = run_dir / "lifecycle" / "provider-reconciliation"
        for action_id, value, started_at, finished_at, duration_ms in results:
            retrieved.append(action_id)
            action = by_id[action_id]
            provider_id = action["provider"]["id"]
            attempt_ordinal = int(
                action["provider_reconciliation"].get(
                    "provider_retrieval_attempt_count"
                ) or 0
            ) + 1
            action_route_family = str(
                native_provider_route_identity(state, action).get("route_family")
                or "exact_natal"
            )
            timing = action["provider_reconciliation"]
            diagnostic_error: Exception | None = (
                value if isinstance(value, Exception) else None
            )
            provider_status = value.get("status") if isinstance(value, dict) else None
            if not isinstance(provider_status, str):
                provider_status = None
            if isinstance(value, Exception):
                if isinstance(value, ProviderRetrievalIdentityMismatch):
                    identity_conflicts.append(action_id)
                    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                    action["ambiguity"] = {
                        "reason": "provider retrieval identity mismatch"
                    }
                    retrieval_outcome = "identity_conflict"
                    cost_disposition = "not_applicable_provider_pending"
                    operation_summaries.append({
                        "action_id": action_id, "route_family": action_route_family,
                        "provider_operation_kind": "response",
                        "provider_operation_id": action["provider"]["id"],
                        "retrieval_outcome": retrieval_outcome,
                        "cost_disposition": cost_disposition,
                        "member_count": None, "ingested_member_count": None,
                        "failed_member_count": None,
                    })
                else:
                    logger.warning(
                        "reconciliation_transport_warning action_id=%s "
                        "provider_id=%s error_class=%s error=%s",
                        action_id, provider_id, type(value).__name__,
                        sanitize_error_message(value, secret=provider_secret),
                    )
                    warnings.append(action_id)
                    record_attempt(
                        timing, attempted_at=instant, outcome="transport_warning"
                    )
                    retrieval_outcome = "transport_warning"
                    cost_disposition = "not_applicable_provider_pending"
                    operation_summaries.append({
                        "action_id": action_id, "route_family": action_route_family,
                        "provider_operation_kind": "response",
                        "provider_operation_id": provider_id,
                        "retrieval_outcome": retrieval_outcome,
                        "cost_disposition": cost_disposition,
                        "member_count": None, "ingested_member_count": None,
                        "failed_member_count": None,
                    })
            elif not isinstance(value, dict) or not isinstance(value.get("id"), str):
                logger.error(
                    "reconciliation_malformed_response action_id=%s provider_id=%s",
                    action_id, provider_id,
                )
                warnings.append(action_id)
                diagnostic_error = ValueError(
                    "Provider returned a malformed Response object"
                )
                record_attempt(timing, attempted_at=instant, outcome="transport_warning")
                retrieval_outcome = "transport_warning"
                cost_disposition = "not_applicable_provider_pending"
                operation_summaries.append({
                    "action_id": action_id, "route_family": action_route_family,
                    "provider_operation_kind": "response",
                    "provider_operation_id": provider_id,
                    "retrieval_outcome": retrieval_outcome,
                    "cost_disposition": cost_disposition,
                    "member_count": None, "ingested_member_count": None,
                    "failed_member_count": None,
                })
            elif value["id"] != provider_id:
                logger.error(
                    "reconciliation_identity_conflict action_id=%s expected_id=%s "
                    "returned_id=%s",
                    action_id, provider_id, value.get("id"),
                )
                diagnostic_error = ProviderRetrievalIdentityMismatch(
                    "Provider retrieval identity mismatch"
                )
                identity_conflicts.append(action_id)
                action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                action["ambiguity"] = {
                    "reason": "provider retrieval identity mismatch"
                }
                retrieval_outcome = "identity_conflict"
                cost_disposition = "not_applicable_provider_pending"
                operation_summaries.append({
                    "action_id": action_id, "route_family": action_route_family,
                    "provider_operation_kind": "response",
                    "provider_operation_id": provider_id,
                    "retrieval_outcome": retrieval_outcome,
                    "cost_disposition": cost_disposition,
                    "member_count": None, "ingested_member_count": None,
                    "failed_member_count": None,
                })
            elif provider_status in {"queued", "in_progress"}:
                logger.info(
                    "reconciliation_pending action_id=%s provider_id=%s status=%s",
                    action_id, provider_id, provider_status,
                )
                record_attempt(timing, attempted_at=instant, outcome="pending")
                retrieval_outcome = "pending"
                cost_disposition = "not_applicable_provider_pending"
            elif provider_status == "completed":
                logger.info(
                    "reconciliation_completed action_id=%s provider_id=%s usage=%s",
                    action_id, provider_id, isinstance(value.get("usage"), dict),
                )
                record_attempt(timing, attempted_at=instant, outcome="completed")
                completed.append(action_id)
                write_json_atomic(evidence_root / f"{action_id}.response.json", value)
                retrieval_outcome = "completed"
                cost_disposition = (
                    "provider_usage_reported" if isinstance(value.get("usage"), dict)
                    else "provider_usage_unavailable_billing_reconciliation_pending"
                )
            elif provider_status in {"failed", "cancelled", "incomplete"}:
                logger.error(
                    "reconciliation_provider_failed action_id=%s provider_id=%s "
                    "provider_status=%s",
                    action_id, provider_id, provider_status,
                )
                record_attempt(timing, attempted_at=instant, outcome="provider_failed")
                completed.append(action_id)
                provider_failures.append(action_id)
                write_json_atomic(evidence_root / f"{action_id}.response.json", value)
                cost_disposition = (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                )
                action["reported"] = {
                    "usage": value.get("usage"),
                    "estimated_micro_usd": None,
                    "cost_disposition": cost_disposition,
                }
                action["integrity_review"] = {
                    "reason": f"Provider Response ended with status {provider_status}",
                    "provider_status": provider_status,
                }
                action["state"] = "REPORTED"
                retrieval_outcome = "provider_failed"
            else:
                warnings.append(action_id)
                diagnostic_error = ValueError(
                    "Provider returned an unsupported Response status"
                )
                record_attempt(
                    timing, attempted_at=instant, outcome="transport_warning"
                )
                retrieval_outcome = "transport_warning"
                cost_disposition = "not_applicable_provider_pending"
            if not isinstance(value, Exception) and isinstance(value, dict) \
                    and isinstance(value.get("id"), str) \
                    and value.get("id") == provider_id:
                if not operation_summaries or operation_summaries[-1]["action_id"] != action_id:
                    operation_summaries.append({
                        "action_id": action_id, "route_family": action_route_family,
                        "provider_operation_kind": "response",
                        "provider_operation_id": provider_id,
                        "retrieval_outcome": retrieval_outcome,
                        "cost_disposition": cost_disposition,
                        "member_count": None, "ingested_member_count": None,
                        "failed_member_count": None,
                    })
            diagnostic = build_response_retrieval_diagnostic(
                provider_response_id=provider_id,
                outcome=(
                    "completed" if retrieval_outcome == "provider_failed"
                    else retrieval_outcome
                ),
                started_at=started_at, finished_at=finished_at,
                duration_ms=duration_ms, run_id=state["run_id"],
                action_id=action_id, attempt_ordinal=attempt_ordinal,
                base_url=endpoint_base_url, provider_status=provider_status,
                exception=diagnostic_error, secret=provider_secret,
            )
            diagnostic_path = evidence_root / (
                f"{action_id}.attempt-{attempt_ordinal:04d}.json"
            )
            write_json_atomic(diagnostic_path, diagnostic)
            diagnostic_artifacts.append({
                "action_id": action_id,
                "attempt_id": diagnostic["attempt_id"],
                "logical_path": diagnostic_path.relative_to(run_dir).as_posix(),
                "bytes": diagnostic_path.stat().st_size,
                "sha256": _file_sha256(diagnostic_path),
            })

        persist_state(run_dir / "run.json", state)
        cycle = {
            "started_at": instant,
            "finished_at": instant,
            "wall_clock_limit_seconds": 20,
            "provider_retrieval_count": len(retrieved),
            "retrieved_action_ids": retrieved,
            "completed_action_ids": completed,
            "still_pending_action_ids": [
                item["action_id"] for item in actions
                if item["action_id"] not in completed
            ],
            "transport_warning_action_ids": warnings,
        }
        artifact = evidence_root / f"cycle-{state['state_revision']:08d}.json"
        write_json_atomic(artifact, {
            "schema_version": "astrowoof.provider_reconciliation_cycle_record.v0.1",
            "run_id": state["run_id"],
            "decision_basis": before["observation"],
            "cycle": cycle,
            "provider_operations": operation_summaries,
            "diagnostic_artifacts": diagnostic_artifacts,
        })
        write_workspace_snapshot(run_dir)
        after = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=instant,
        )
        logger.info(
            "reconciliation_cycle_checkpoint state_revision=%s completed=%s "
            "pending=%s warnings=%s conflicts=%s capacity_disposition=%s",
            state.get("state_revision"), len(completed),
            len(cycle["still_pending_action_ids"]), len(warnings),
            len(identity_conflicts), after["execution_capacity"]["disposition"],
        )
        return {
            "schema_version": PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
            "run_id": state["run_id"],
            "outcome": (
                "review_required" if identity_conflicts or provider_failures
                else "progressed_local" if completed
                else "detached_provider_pending"
            ),
            "decision_basis": before["observation"],
            "cycle": cycle,
            "inspection": after,
            "provider_operations": operation_summaries,
            "result_checkpoint": {
                "operator_state_revision": state["state_revision"],
                "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                "result_artifact": {
                    "logical_path": artifact.relative_to(run_dir).as_posix(),
                    "bytes": artifact.stat().st_size,
                    "sha256": _file_sha256(artifact),
                },
            },
        }


def reconcile_batch_provider_cycle(
    run_dir: Path,
    *,
    provider: Any,
    transport: Any,
    max_attempts: int,
    python_executable: Path,
    observed_at: str,
    event_emitter: Any = None,
    polish_provider: Any = None,
    critic_provider: Any = None,
    qualitative_editor_provider: Any = None,
    _failure_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Retrieve and ingest at most one known exact or bounded Batch round."""
    from .closure import (
        SNAPSHOT_NAME,
        SpendController,
        _batch_jsonl_records,
        author_pending_passes_batch,
        finalize_subjects,
        load_json,
        persist_state,
        save_state,
        sha256_file,
        update_run_status,
        run_qualitative_review,
        write_json_atomic,
        write_workspace_snapshot,
    )
    from .lifecycle import inspect_lifecycle

    run_dir = run_dir.resolve()
    instant = utc_instant(parse_utc_instant(observed_at))
    batch_policy = PROVIDER_RECONCILIATION_POLICY["mechanisms"]["batch"]

    def empty_result(
        state: dict[str, Any], inspection: dict[str, Any], outcome: str,
    ) -> dict[str, Any]:
        result = {
            "schema_version": PROVIDER_RECONCILIATION_CYCLE_RESULT_SCHEMA,
            "run_id": state["run_id"], "outcome": outcome,
            "decision_basis": inspection["observation"],
            "cycle": {
                "started_at": instant, "finished_at": instant,
                "wall_clock_limit_seconds": 40,
                "provider_retrieval_count": 0, "retrieved_action_ids": [],
                "completed_action_ids": [],
                "still_pending_action_ids": inspection["provider_custody"]["action_ids"],
                "transport_warning_action_ids": [],
            },
            "inspection": inspection, "provider_operations": [],
        }
        if outcome != "not_due":
            result["result_checkpoint"] = {
                "operator_state_revision": inspection["observation"]["operator_state_revision"],
                "snapshot_sha256": inspection["observation"]["snapshot_sha256"],
                "result_artifact": {
                    "logical_path": SNAPSHOT_NAME,
                    "bytes": (run_dir / SNAPSHOT_NAME).stat().st_size,
                    "sha256": inspection["observation"]["snapshot_sha256"],
                },
            }
        return result

    def exhaust_local_continuation(
        state: dict[str, Any], controller: Any,
    ) -> None:
        from .spend import (
            AmbiguousProviderSubmission,
            AwaitingSpendAuthorization,
            BudgetExhausted,
        )
        qa = (state.get("authoring_profile") or {}).get("qa") or {}
        try:
            finalize_subjects(
                state=state, run_dir=run_dir,
                python_executable=python_executable,
                allow_lint_warnings=bool(qa.get("allow_lint_warnings")),
                polish=bool(qa.get("polish")),
                polish_provider=polish_provider,
                max_polish_attempts=int(qa.get("max_polish_attempts") or 2),
                spend_controller=controller,
            )
            if bool(qa.get("qualitative_critic")) and critic_provider is not None:
                for subject_record in state.get("subjects", {}).values():
                    if subject_record.get("state") in {
                        "DELIVERY_COMPLETE", "DELIVERY_COMPLETE_WITH_WARNINGS",
                    }:
                        run_qualitative_review(
                            record=subject_record,
                            critic_provider=critic_provider,
                            editor_provider=(
                                qualitative_editor_provider
                                if bool(qa.get("qualitative_candidate")) else None
                            ),
                            run_dir=run_dir, python_executable=python_executable,
                            max_findings=int(qa.get("max_critic_findings") or 8),
                            max_target_fields=int(
                                qa.get("max_qualitative_target_fields") or 12
                            ),
                            max_target_cards=int(
                                qa.get("max_qualitative_target_cards") or 6
                            ),
                            spend_controller=controller, run_state=state,
                        )
        except (
            AwaitingSpendAuthorization, BudgetExhausted,
            AmbiguousProviderSubmission,
        ):
            pass

    with _single_writer(run_dir):
        state = load_json(run_dir / "run.json")
        from .closure import validate_workspace_snapshot
        validate_workspace_snapshot(run_dir, state)
        before = inspect_lifecycle(
            run_dir, native_exclusive_access="established", observed_at=instant,
        )
        route_family = before["native_route"]["route_family"]
        bounded_batch = route_family == "bounded_natal"
        replayed_rounds = [
            item for item in (state.get("batch_service") or {}).get("rounds", [])
            if item.get("state") == "INGESTED" and item.get("batch_id")
        ]
        if replayed_rounds:
            replayed = replayed_rounds[-1]
            action = next((
                item for item in (state.get("spend_ledger") or {}).get("actions", [])
                if (item.get("provider") or {}).get("id") == replayed["batch_id"]
            ), None)
            if action is not None and action.get("state") == "REPORTED":
                controller = SpendController(
                    state=state, run_json=run_dir / "run.json",
                    state_lock=threading.Lock(),
                    consumer_id=f"batch-reconcile:{os.getpid()}",
                    event_emitter=event_emitter, reconciliation_only=True,
                )
                if bounded_batch:
                    from .bounded_lifecycle import resume_bounded_run
                    try:
                        resume_bounded_run(
                            run_dir, provider=provider,
                            consumer_id=f"batch-reconcile:{os.getpid()}",
                            reconciliation_only=True,
                        )
                    except Exception as exc:
                        from .spend import (
                            AmbiguousProviderSubmission,
                            AwaitingSpendAuthorization,
                            BudgetExhausted,
                        )
                        if not isinstance(exc, (
                            AwaitingSpendAuthorization, BudgetExhausted,
                            AmbiguousProviderSubmission,
                        )):
                            raise
                    state = load_json(run_dir / "run.json")
                else:
                    exhaust_local_continuation(state, controller)
                save_state(run_dir / "run.json", state)
                after = inspect_lifecycle(
                    run_dir, native_exclusive_access="established",
                    observed_at=instant,
                )
                result = empty_result(state, after, "progressed_local")
                result["cycle"]["completed_action_ids"] = [action["action_id"]]
                member_count = len(replayed["requests"])
                failed_count = sum(
                    1 for request in replayed["requests"]
                    if state["passes"][request["pass_id"]]["attempts"]
                    [request["attempt_number"] - 1].get("state") == "ATTEMPT_ERROR"
                )
                result["provider_operations"] = [{
                    "action_id": action["action_id"],
                    "route_family": route_family,
                    "provider_operation_kind": "batch",
                    "provider_operation_id": replayed["batch_id"],
                    "retrieval_outcome": "completed",
                    "cost_disposition": str(
                        ((action.get("reported") or {}).get("cost_disposition"))
                        or "provider_usage_reported"
                    ),
                    "member_count": member_count,
                    "ingested_member_count": member_count - failed_count,
                    "failed_member_count": failed_count,
                }]
                return result
        disposition = before["execution_capacity"]["disposition"]
        if disposition == "release_until_due":
            return empty_result(state, before, "not_due")
        if disposition in {
            "unsupported_retain_capacity", "retain_for_review",
            "await_external_authority", "terminal",
        }:
            return empty_result(state, before, {
                "unsupported_retain_capacity": "unsupported",
                "retain_for_review": "review_required",
                "await_external_authority": "awaiting_external_authority",
                "terminal": "terminal",
            }[disposition])
        due_ids = before["provider_custody"]["next_due_action_ids"]
        actions = [
            item for item in (state.get("spend_ledger") or {}).get("actions", [])
            if item.get("action_id") in due_ids
            and native_provider_route_identity(state, item).get("adapter")
            == ("bounded_batch" if bounded_batch else "exact_batch")
        ]
        if len(actions) != 1:
            raise ValueError("Exactly one due native Batch action is required")
        action = actions[0]
        identity = native_provider_route_identity(state, action)
        if not identity["valid"]:
            raise ValueError("Native Batch operation binding is invalid")
        timing = validated_timing(action)
        if (
            timing is None or timing.get("resume_not_before") is None
            or parse_utc_instant(timing["resume_not_before"])
            > parse_utc_instant(instant)
        ):
            return empty_result(state, before, "not_due")
        round_record = next(
            item for item in state["batch_service"]["rounds"]
            if (
                f"bounded_natal.v2:batch-round-{int(item['round_number']):03d}"
                if bounded_batch else f"batch-round-{int(item['round_number']):03d}"
            ) == identity["native_operation_ref"]
        )
        batch_id = action["provider"]["id"]
        try:
            batch = transport.retrieve_batch(batch_id)
        except Exception:
            record_attempt(
                action["provider_reconciliation"], attempted_at=instant,
                outcome="transport_warning", mechanism="batch",
            )
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "detached_provider_pending")
            result["cycle"]["provider_retrieval_count"] = 1
            result["cycle"]["retrieved_action_ids"] = [action["action_id"]]
            result["cycle"]["transport_warning_action_ids"] = [action["action_id"]]
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id,
                "retrieval_outcome": "transport_warning",
                "cost_disposition": "not_applicable_provider_pending",
                "member_count": len(round_record["requests"]),
                "ingested_member_count": 0, "failed_member_count": 0,
            }]
            return result
        if not isinstance(batch, dict) or batch.get("id") != batch_id:
            action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
            action["ambiguity"] = {"reason": "Batch retrieval identity mismatch"}
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "review_required")
            result["cycle"]["provider_retrieval_count"] = 1
            result["cycle"]["retrieved_action_ids"] = [action["action_id"]]
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id,
                "retrieval_outcome": "identity_conflict",
                "cost_disposition": "not_applicable_provider_pending",
                "member_count": len(round_record["requests"]),
                "ingested_member_count": 0, "failed_member_count": 0,
            }]
            return result
        status = str(batch.get("status") or "")
        round_record["batch_status"] = status
        round_record["request_counts"] = batch.get("request_counts")
        pending_statuses = {"validating", "in_progress", "finalizing"}
        if status in pending_statuses:
            record_attempt(
                action["provider_reconciliation"], attempted_at=instant,
                outcome="pending", mechanism="batch",
            )
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "detached_provider_pending")
            result["cycle"].update({
                "provider_retrieval_count": 1,
                "retrieved_action_ids": [action["action_id"]],
            })
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id, "retrieval_outcome": "pending",
                "cost_disposition": "not_applicable_provider_pending",
                "member_count": len(round_record["requests"]),
                "ingested_member_count": 0, "failed_member_count": 0,
            }]
            return result
        terminal_statuses = {"completed", "failed", "expired", "cancelled"}
        if status not in terminal_statuses:
            record_attempt(
                action["provider_reconciliation"], attempted_at=instant,
                outcome="transport_warning", mechanism="batch",
            )
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            return empty_result(state, after, "detached_provider_pending")

        round_root = Path(round_record["input_path"]).parent
        write_json_atomic(round_root / "batch-object.json", batch)
        persist_state(run_dir / "run.json", state)
        write_workspace_snapshot(run_dir)
        if _failure_injector:
            _failure_injector("after_batch_terminal_object")
        member_count = len(round_record["requests"])
        if status != "completed":
            round_record["state"] = "FAILED"
            round_record["finished_at"] = instant
            for request in round_record["requests"]:
                record = state["passes"][request["pass_id"]]
                attempt = record["attempts"][request["attempt_number"] - 1]
                attempt["state"] = (
                    "PASS_QA_REJECTED" if bounded_batch else "ATTEMPT_ERROR"
                )
                attempt["finished_at"] = instant
                attempt["error"] = {
                    "type": "OpenAIBatchError",
                    "message": f"Batch ended with status {status}",
                }
                record["state"] = attempt["state"]
            action["reported"] = {
                "usage": None, "estimated_micro_usd": None,
                "cost_disposition": (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                ),
            }
            action["state"] = "REPORTED"
            update_run_status(state)
            save_state(run_dir / "run.json", state)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "progressed_local")
            result["cycle"].update({
                "provider_retrieval_count": 1,
                "retrieved_action_ids": [action["action_id"]],
                "completed_action_ids": [action["action_id"]],
                "still_pending_action_ids": [],
            })
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id,
                "retrieval_outcome": "provider_failed",
                "cost_disposition": (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                ),
                "member_count": member_count, "ingested_member_count": 0,
                "failed_member_count": member_count,
            }]
            return result

        try:
            output_text = (
                transport.download_file(batch["output_file_id"])
                if batch.get("output_file_id") else ""
            )
            error_text = (
                transport.download_file(batch["error_file_id"])
                if batch.get("error_file_id") else ""
            )
        except Exception:
            record_attempt(
                action["provider_reconciliation"], attempted_at=instant,
                outcome="transport_warning", mechanism="batch",
            )
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "detached_provider_pending")
            result["cycle"].update({
                "provider_retrieval_count": 1,
                "retrieved_action_ids": [action["action_id"]],
                "transport_warning_action_ids": [action["action_id"]],
            })
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id,
                "retrieval_outcome": "transport_warning",
                "cost_disposition": "not_applicable_provider_pending",
                "member_count": member_count, "ingested_member_count": 0,
                "failed_member_count": 0,
            }]
            return result
        (round_root / "batch-output.jsonl").write_text(output_text, encoding="utf-8")
        if error_text:
            (round_root / "batch-errors.jsonl").write_text(error_text, encoding="utf-8")
        parse_error = None
        supplied_sequence: list[str] = []
        try:
            for text in (output_text, error_text):
                for line in text.splitlines():
                    if line.strip():
                        item = json.loads(line)
                        custom_id = item.get("custom_id")
                        if not isinstance(custom_id, str) or not custom_id:
                            raise ValueError("Batch member custom_id is missing")
                        supplied_sequence.append(custom_id)
            outputs = _batch_jsonl_records(output_text)
            errors = _batch_jsonl_records(error_text)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            outputs, errors, parse_error = {}, {}, str(exc)
        expected = [item["custom_id"] for item in round_record["requests"]]
        supplied = set(outputs) | set(errors)
        duplicate_ids = sorted({
            item for item in supplied_sequence
            if supplied_sequence.count(item) > 1
        })
        if (
            parse_error or duplicate_ids or set(outputs) & set(errors)
            or supplied != set(expected)
        ):
            integrity_evidence = {
                "reason": (
                    "Batch output JSONL invalid" if parse_error
                    else "Batch output membership mismatch"
                ),
                "expected_custom_ids": expected,
                "output_custom_ids": sorted(outputs),
                "error_custom_ids": sorted(errors),
            }
            if duplicate_ids:
                integrity_evidence["duplicate_custom_ids"] = duplicate_ids
            if parse_error:
                integrity_evidence["parse_error"] = parse_error
            round_record["integrity_review"] = integrity_evidence
            action["integrity_review"] = integrity_evidence
            action["reported"] = {
                "usage": None, "estimated_micro_usd": None,
                "cost_disposition": (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                ),
            }
            action["state"] = "REPORTED"
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=instant,
            )
            result = empty_result(state, after, "review_required")
            result["cycle"].update({
                "provider_retrieval_count": 1,
                "retrieved_action_ids": [action["action_id"]],
                "still_pending_action_ids": [],
            })
            result["provider_operations"] = [{
                "action_id": action["action_id"], "route_family": route_family,
                "provider_operation_kind": "batch",
                "provider_operation_id": batch_id,
                "retrieval_outcome": "output_invalid",
                "cost_disposition": (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                ),
                "member_count": member_count, "ingested_member_count": 0,
                "failed_member_count": 0,
            }]
            return result
        persist_state(run_dir / "run.json", state)
        write_workspace_snapshot(run_dir)
        if _failure_injector:
            _failure_injector("after_batch_files_durable")

        class CachedBatchTransport:
            def retrieve_batch(self, requested_id: str) -> dict[str, Any]:
                if requested_id != batch_id:
                    raise ValueError("Cached Batch ID mismatch")
                return batch

            def download_file(self, file_id: str) -> str:
                if file_id == batch.get("output_file_id"):
                    return output_text
                if file_id == batch.get("error_file_id"):
                    return error_text
                raise ValueError("Cached Batch File ID mismatch")

            def upload_jsonl(self, content: bytes, filename: str) -> dict[str, Any]:
                raise AssertionError("Reconciliation cannot upload Batch input")

            def create_batch(self, payload: dict[str, Any]) -> dict[str, Any]:
                raise AssertionError("Reconciliation cannot create a Batch")

        controller = SpendController(
            state=state, run_json=run_dir / "run.json", state_lock=threading.Lock(),
            consumer_id=f"batch-reconcile:{os.getpid()}",
            event_emitter=event_emitter, reconciliation_only=True,
        )
        if bounded_batch:
            from .bounded_lifecycle import (
                _bounded_batch_authoring_cycle,
                resume_bounded_run,
            )
            provider.batch_transport = CachedBatchTransport()
            _bounded_batch_authoring_cycle(state, run_dir, provider, controller)
        else:
            author_pending_passes_batch(
                state=state, provider=provider, transport=CachedBatchTransport(),
                run_dir=run_dir, max_attempts=max_attempts,
                python_executable=python_executable, run_json=run_dir / "run.json",
                detach=True, sleep=lambda _: None, spend_controller=controller,
                reconciliation_only=True,
            )
        if _failure_injector:
            _failure_injector("after_batch_member_ingestion")
        if not bounded_batch:
            update_run_status(state)
        if bounded_batch:
            try:
                resume_bounded_run(
                    run_dir, provider=provider, event_emitter=event_emitter,
                    consumer_id=f"batch-reconcile:{os.getpid()}",
                    reconciliation_only=True,
                )
            except Exception as exc:
                from .spend import (
                    AmbiguousProviderSubmission,
                    AwaitingSpendAuthorization,
                    BudgetExhausted,
                )
                if not isinstance(exc, (
                    AwaitingSpendAuthorization, BudgetExhausted,
                    AmbiguousProviderSubmission,
                )):
                    raise
            state = load_json(run_dir / "run.json")
        else:
            exhaust_local_continuation(state, controller)
        save_state(run_dir / "run.json", state)
        if _failure_injector:
            _failure_injector("after_batch_local_continuation")
        if _failure_injector:
            _failure_injector("after_batch_state_persistence")
        after = inspect_lifecycle(
            run_dir, native_exclusive_access="established", observed_at=instant,
        )
        result = empty_result(state, after, "progressed_local")
        result["cycle"].update({
            "provider_retrieval_count": 1,
            "retrieved_action_ids": [action["action_id"]],
            "completed_action_ids": [action["action_id"]],
            "still_pending_action_ids": [],
        })
        failed_count = sum(1 for item in expected if item in errors)
        result["provider_operations"] = [{
            "action_id": action["action_id"], "route_family": route_family,
            "provider_operation_kind": "batch", "provider_operation_id": batch_id,
            "retrieval_outcome": "completed",
            "cost_disposition": "provider_usage_reported",
            "member_count": member_count,
            "ingested_member_count": member_count - failed_count,
            "failed_member_count": failed_count,
        }]
        result["local_continuation"] = {
            "pass_ids": sorted(item["pass_id"] for item in round_record["requests"]),
            "stages": [action["binding"]["stage"]],
            "completed_action_ids": [action["action_id"]],
            "exhausted_before_detach": True,
        }
        return result


def run_bounded_authoring_reconciliation(
    run_dir: Path,
    *,
    provider: Any,
    max_attempts: int,
    python_executable: Path,
    observed_at: str,
    event_emitter: Any = None,
    polish_provider: Any = None,
    critic_provider: Any = None,
    qualitative_editor_provider: Any = None,
    _failure_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Retrieve one due interactive wave and exhaust route-local continuation."""
    from .closure import (
        SNAPSHOT_NAME,
        SpendController,
        author_pending_passes,
        finalize_subjects,
        load_json,
        run_qualitative_review,
        save_state,
        sha256_file,
        write_json_atomic,
        write_workspace_snapshot,
    )
    from .lifecycle import inspect_lifecycle

    def emit_checkpoint_events(value: dict[str, Any]) -> None:
        checkpoint = value.get("result_checkpoint")
        if event_emitter is None or not isinstance(checkpoint, dict):
            return
        retrieved = set(value["cycle"]["retrieved_action_ids"])
        if not retrieved:
            return
        for operation in value.get("provider_operations", []):
            if operation["action_id"] not in retrieved:
                continue
            event_emitter.emit("provider.reconciliation_observed", data={
                "action_id": operation["action_id"],
                "route_family": operation["route_family"],
                "provider_operation_kind": operation["provider_operation_kind"],
                "outcome": operation["retrieval_outcome"],
                "member_count": operation.get("member_count"),
            })
        event_emitter.emit("run.detached", data={
            "state_revision": checkpoint["operator_state_revision"],
            "reason_code": value["outcome"],
        })
        event_emitter.emit("checkpoint.committed", data={
            "state_revision": checkpoint["operator_state_revision"],
            "snapshot_sha256": checkpoint["snapshot_sha256"],
        })

    if getattr(provider, "name", None) != "openai":
        raise ValueError("Bounded authoring reconciliation requires OpenAI provider")
    retrieval_provider = getattr(
        provider, "responses", getattr(provider, "initial", provider)
    )
    original_timeout = retrieval_provider.http_timeout_seconds
    original_retries = retrieval_provider.max_transport_retries

    def retrieve(provider_id: str, timeout: float) -> dict[str, Any]:
        # GET-only use of the existing provider transport. The bounded cycle never
        # supplies request material or invokes the POST path.
        response, _attempts = retrieval_provider._request_with_retry(
            method="GET",
            url=f"{retrieval_provider.base_url}/responses/{provider_id}",
            payload=None,
        )
        return response

    try:
        retrieval_provider.http_timeout_seconds = min(float(original_timeout), 15.0)
        retrieval_provider.max_transport_retries = 0
        result = reconcile_provider_cycle(
            run_dir, retrieve=retrieve, observed_at=observed_at,
            endpoint_base_url=getattr(retrieval_provider, "base_url", None),
            provider_secret=getattr(retrieval_provider, "api_key", None),
        )
    finally:
        retrieval_provider.http_timeout_seconds = original_timeout
        retrieval_provider.max_transport_retries = original_retries
    if _failure_injector:
        _failure_injector("after_provider_retrieval_checkpoint")
    completed_ids = set(result["cycle"]["completed_action_ids"])
    if not completed_ids or result["outcome"] == "review_required":
        emit_checkpoint_events(result)
        return result

    route_family = result["inspection"]["native_route"]["route_family"]
    if route_family == "bounded_natal":
        from .bounded_lifecycle import resume_bounded_run
        from .spend import (
            AmbiguousProviderSubmission,
            AwaitingSpendAuthorization,
            BudgetExhausted,
        )
        try:
            resume_bounded_run(
                run_dir, provider=provider, event_emitter=event_emitter,
                consumer_id=f"reconcile:{os.getpid()}",
                reconciliation_only=True,
            )
        except (
            AwaitingSpendAuthorization, BudgetExhausted,
            AmbiguousProviderSubmission,
        ):
            pass
        if _failure_injector:
            _failure_injector("after_bounded_local_continuation")
        state = load_json(run_dir / "run.json")
        completed_actions = [
            item for item in (state.get("spend_ledger") or {}).get("actions", [])
            if item.get("action_id") in completed_ids
        ]
        def bounded_pass_id(item: dict[str, Any]) -> str:
            native_ref = str((item.get("binding") or {}).get("route") or "")
            parts = native_ref.split(":")
            return (
                parts[1]
                if len(parts) >= 3 and parts[0] == "bounded_natal.v2"
                else native_ref
            )

        local_continuation = {
            "pass_ids": sorted({
                bounded_pass_id(item)
                for item in completed_actions
                if (item.get("binding") or {}).get("stage")
                in {"authoring_initial", "creative_retry"}
            }),
            "stages": sorted({
                str((item.get("binding") or {}).get("stage") or "")
                for item in completed_actions
            }),
            "completed_action_ids": sorted(completed_ids),
            "exhausted_before_detach": True,
        }
        artifact = run_dir / result["result_checkpoint"]["result_artifact"]["logical_path"]
        record = json.loads(artifact.read_text(encoding="utf-8"))
        record["local_continuation"] = local_continuation
        write_json_atomic(artifact, record)
        write_workspace_snapshot(run_dir)
        if _failure_injector:
            _failure_injector("after_bounded_result_snapshot")
        inspection = inspect_lifecycle(
            run_dir, native_exclusive_access="established",
            observed_at=utc_instant(parse_utc_instant(observed_at)),
        )
        result["outcome"] = {
            "release_until_due": "detached_provider_pending",
            "await_external_authority": "awaiting_external_authority",
            "terminal": "terminal",
            "retain_for_review": "review_required",
            "unsupported_retain_capacity": "unsupported",
            "continue_local_cycle": "progressed_local",
        }[inspection["execution_capacity"]["disposition"]]
        result["inspection"] = inspection
        result["local_continuation"] = local_continuation
        result["result_checkpoint"] = {
            "operator_state_revision": inspection["observation"]["operator_state_revision"],
            "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
            "result_artifact": {
                "logical_path": artifact.relative_to(run_dir).as_posix(),
                "bytes": artifact.stat().st_size,
                "sha256": _file_sha256(artifact),
            },
        }
        emit_checkpoint_events(result)
        return result

    state = load_json(run_dir / "run.json")
    completed_actions = [
        item for item in (state.get("spend_ledger") or {}).get("actions", [])
        if item.get("action_id") in completed_ids
    ]
    stages = {
        str((item.get("binding") or {}).get("stage") or "")
        for item in completed_actions
    }
    unsupported = [
        item["action_id"] for item in completed_actions
        if (item.get("binding") or {}).get("stage")
        not in {
            "authoring_initial", "creative_retry", "polish",
            "qualitative_critic", "qualitative_candidate",
        }
    ]
    if unsupported:
        raise ValueError(
            "Bounded exact-interactive reconciliation does not support stages: "
            + ", ".join(unsupported)
        )
    if "polish" in stages and polish_provider is None:
        raise ValueError("Polish reconciliation requires the frozen polish provider")
    if "qualitative_critic" in stages and critic_provider is None:
        raise ValueError("Critic reconciliation requires the frozen critic provider")
    if (
        "qualitative_candidate" in stages
        and qualitative_editor_provider is None
    ):
        raise ValueError(
            "Qualitative-candidate reconciliation requires the frozen editor provider"
        )
    pass_ids = {
        str(item["binding"]["route"]).rsplit(":attempt-", 1)[0]
        for item in completed_actions
        if (item.get("binding") or {}).get("stage")
        in {"authoring_initial", "creative_retry"}
    }
    controller = SpendController(
        state=state,
        run_json=run_dir / "run.json",
        state_lock=threading.Lock(),
        consumer_id=f"reconcile:{os.getpid()}",
        event_emitter=event_emitter,
        reconciliation_only=True,
    )
    if pass_ids:
        author_pending_passes(
            state=state,
            provider=provider,
            run_dir=run_dir,
            max_attempts=max_attempts,
            python_executable=python_executable,
            run_json=run_dir / "run.json",
            max_workers=min(
                PROVIDER_RECONCILIATION_POLICY["mechanisms"]["response"][
                    "maximum_parallel_requests"
                ],
                max(len(pass_ids), 1),
            ),
            spend_controller=controller,
            only_pass_ids=pass_ids,
        )
    qa = (state.get("authoring_profile") or {}).get("qa") or {}
    try:
        finalize_subjects(
            state=state,
            run_dir=run_dir,
            python_executable=python_executable,
            allow_lint_warnings=bool(qa.get("allow_lint_warnings")),
            polish=bool(qa.get("polish")),
            polish_provider=polish_provider,
            max_polish_attempts=int(qa.get("max_polish_attempts") or 2),
            spend_controller=controller,
        )
        if bool(qa.get("qualitative_critic")) and critic_provider is not None:
            for subject_record in state.get("subjects", {}).values():
                if subject_record.get("state") in {
                    "DELIVERY_COMPLETE", "DELIVERY_COMPLETE_WITH_WARNINGS",
                }:
                    run_qualitative_review(
                        record=subject_record,
                        critic_provider=critic_provider,
                        editor_provider=(
                            qualitative_editor_provider
                            if bool(qa.get("qualitative_candidate")) else None
                        ),
                        run_dir=run_dir,
                        python_executable=python_executable,
                        max_findings=int(qa.get("max_critic_findings") or 8),
                        max_target_fields=int(
                            qa.get("max_qualitative_target_fields") or 12
                        ),
                        max_target_cards=int(
                            qa.get("max_qualitative_target_cards") or 6
                        ),
                        spend_controller=controller,
                        run_state=state,
                    )
    except Exception as exc:
        from .spend import (
            AmbiguousProviderSubmission,
            AwaitingSpendAuthorization,
            BudgetExhausted,
        )
        if not isinstance(exc, (
            AwaitingSpendAuthorization,
            BudgetExhausted,
            AmbiguousProviderSubmission,
        )):
            raise
    finally:
        save_state(run_dir / "run.json", state)
    artifact = run_dir / result["result_checkpoint"]["result_artifact"]["logical_path"]
    record = json.loads(artifact.read_text(encoding="utf-8"))
    local_continuation = {
        "pass_ids": sorted(pass_ids),
        "stages": sorted(stages),
        "completed_action_ids": sorted(completed_ids),
        "exhausted_before_detach": True,
    }
    record["local_continuation"] = local_continuation
    write_json_atomic(artifact, record)
    write_workspace_snapshot(run_dir)
    inspection = inspect_lifecycle(
        run_dir,
        native_exclusive_access="established",
        observed_at=utc_instant(parse_utc_instant(observed_at)),
    )
    disposition = inspection["execution_capacity"]["disposition"]
    result["outcome"] = {
        "release_until_due": "detached_provider_pending",
        "await_external_authority": "awaiting_external_authority",
        "terminal": "terminal",
        "retain_for_review": "review_required",
        "unsupported_retain_capacity": "unsupported",
        "continue_local_cycle": "progressed_local",
    }[disposition]
    result["inspection"] = inspection
    result["local_continuation"] = local_continuation
    result["result_checkpoint"] = {
        "operator_state_revision": inspection["observation"]["operator_state_revision"],
        "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
        "result_artifact": {
            "logical_path": artifact.relative_to(run_dir).as_posix(),
            "bytes": artifact.stat().st_size,
            "sha256": _file_sha256(artifact),
        },
    }
    emit_checkpoint_events(result)
    return result


def reconcile_authoring_provider_cycle(
    run_dir: Path,
    *,
    observed_at: str,
    provider_adapters: ProviderReconciliationAdapters,
    event_emitter: Any = None,
) -> dict[str, Any]:
    """Dispatch one bounded provider cycle from validated native route evidence."""
    from .closure import load_json
    from .lifecycle import inspect_lifecycle

    run_dir = run_dir.resolve()
    state = load_json(run_dir / "run.json")
    inspection = inspect_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at,
    )
    route = inspection["native_route"]["route_family"]
    operation_kinds = {
        item["provider_operation_kind"]
        for item in inspection["provider_custody"]["actions"]
        if item["custody_classification"] != "unsupported"
    }
    if len(operation_kinds) > 1:
        raise ValueError("Mixed provider mechanisms cannot share one reconciliation cycle")
    mechanism = next(iter(operation_kinds), None)
    if mechanism is None and route == "exact_natal":
        mechanism = "batch" if state.get("service_level") == "batch" else "response"
    elif mechanism is None and route == "bounded_natal":
        mechanism = "batch" if state.get("service_level") == "batch" else "response"

    if route == "bounded_natal" and mechanism == "batch":
        if (
            provider_adapters.bounded_batch_provider is None
            or provider_adapters.bounded_batch_transport is None
        ):
            raise ValueError("Bounded Batch reconciliation adapters are required")
        result = reconcile_batch_provider_cycle(
            run_dir,
            provider=provider_adapters.bounded_batch_provider,
            transport=provider_adapters.bounded_batch_transport,
            max_attempts=provider_adapters.max_attempts,
            python_executable=provider_adapters.python_executable,
            observed_at=observed_at, event_emitter=event_emitter,
        )
        return result
    if route == "exact_natal" and mechanism == "batch":
        if (
            provider_adapters.exact_batch_provider is None
            or provider_adapters.exact_batch_transport is None
        ):
            raise ValueError("Exact Batch reconciliation adapters are required")
        result = reconcile_batch_provider_cycle(
            run_dir,
            provider=provider_adapters.exact_batch_provider,
            transport=provider_adapters.exact_batch_transport,
            max_attempts=provider_adapters.max_attempts,
            python_executable=provider_adapters.python_executable,
            observed_at=observed_at,
            event_emitter=event_emitter,
            polish_provider=provider_adapters.polish_provider,
            critic_provider=provider_adapters.critic_provider,
            qualitative_editor_provider=(
                provider_adapters.qualitative_editor_provider
            ),
        )
        if event_emitter is not None and result["outcome"] != "not_due":
            retrieved = set(result["cycle"]["retrieved_action_ids"])
            for operation in result.get("provider_operations", []):
                if operation["action_id"] in retrieved:
                    event_emitter.emit("provider.reconciliation_observed", data={
                        "action_id": operation["action_id"],
                        "route_family": operation["route_family"],
                        "provider_operation_kind": operation["provider_operation_kind"],
                        "outcome": operation["retrieval_outcome"],
                        "member_count": operation.get("member_count"),
                    })
            checkpoint = result.get("result_checkpoint")
            if isinstance(checkpoint, dict):
                event_emitter.emit("run.detached", data={
                    "state_revision": checkpoint["operator_state_revision"],
                    "reason_code": result["outcome"],
                })
                event_emitter.emit("checkpoint.committed", data={
                    "state_revision": checkpoint["operator_state_revision"],
                    "snapshot_sha256": checkpoint["snapshot_sha256"],
                })
        if result["outcome"] != "not_due":
            from . import __version__
            from .native_transitions import publish_native_execution_result
            publish_native_execution_result(
                run_dir, command_kind="provider_reconciliation",
                sbe_release=__version__, published_at=observed_at,
                event_emitter=event_emitter,
            )
        return result
    if route == "exact_natal" and mechanism == "response":
        provider = provider_adapters.exact_interactive_provider
    elif route == "bounded_natal" and mechanism == "response":
        provider = provider_adapters.bounded_interactive_provider
    else:
        raise ValueError("Native route/provider mechanism is unsupported")
    if provider is None:
        raise ValueError(f"{route} interactive reconciliation adapter is required")
    result = run_bounded_authoring_reconciliation(
        run_dir,
        provider=provider,
        max_attempts=provider_adapters.max_attempts,
        python_executable=provider_adapters.python_executable,
        observed_at=observed_at,
        event_emitter=event_emitter,
        polish_provider=provider_adapters.polish_provider,
        critic_provider=provider_adapters.critic_provider,
        qualitative_editor_provider=provider_adapters.qualitative_editor_provider,
    )
    if result["outcome"] != "not_due":
        from . import __version__
        from .native_transitions import publish_native_execution_result
        publish_native_execution_result(
            run_dir, command_kind="provider_reconciliation",
            sbe_release=__version__, published_at=observed_at,
            event_emitter=event_emitter,
        )
    return result
