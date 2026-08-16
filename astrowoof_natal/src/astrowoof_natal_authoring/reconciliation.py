"""Durable scheduling evidence for known provider-operation reconciliation."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import threading
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from .lifecycle_contracts import (
    PROVIDER_RECONCILIATION_POLICY,
    PROVIDER_RECONCILIATION_POLICY_SCHEMA,
)


RECONCILIABLE_PROVIDER_STATES = {
    "PROVIDER_ID_RECORDED", "WAITING",
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


def delay_seconds(attempt_count: int) -> int:
    """Return the frozen lower-bound delay after ``attempt_count`` retrievals."""
    if not isinstance(attempt_count, int) or isinstance(attempt_count, bool):
        raise ValueError("Reconciliation attempt count must be an integer")
    if attempt_count < 0:
        raise ValueError("Reconciliation attempt count cannot be negative")
    initial = PROVIDER_RECONCILIATION_POLICY["initial_delay_seconds"]
    multiplier = PROVIDER_RECONCILIATION_POLICY["backoff_multiplier"]
    maximum = PROVIDER_RECONCILIATION_POLICY["maximum_delay_seconds"]
    return min(initial * (multiplier ** attempt_count), maximum)


def initial_timing(*, recorded_at: str) -> dict[str, Any]:
    recorded = parse_utc_instant(recorded_at)
    return {
        "policy_version": PROVIDER_RECONCILIATION_POLICY_SCHEMA,
        "provider_retrieval_attempt_count": 0,
        "last_attempt_at": None,
        "last_outcome": "provider_identity_recorded",
        "resume_not_before": utc_instant(
            recorded + timedelta(seconds=delay_seconds(0))
        ),
    }


def record_attempt(
    timing: dict[str, Any], *, attempted_at: str, outcome: str,
) -> dict[str, Any]:
    if outcome not in {"pending", "completed", "transport_warning", "provider_failed"}:
        raise ValueError(f"Unsupported reconciliation outcome: {outcome}")
    if timing.get("policy_version") != PROVIDER_RECONCILIATION_POLICY_SCHEMA:
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
        else utc_instant(attempted + timedelta(seconds=delay_seconds(count)))
    )
    return timing


def validated_timing(action: dict[str, Any]) -> dict[str, Any] | None:
    if action.get("state") not in RECONCILIABLE_PROVIDER_STATES:
        return None
    if (action.get("binding") or {}).get("service_level") != "interactive":
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
    if timing["policy_version"] != PROVIDER_RECONCILIATION_POLICY_SCHEMA:
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
        validate_workspace_snapshot(run_dir, state)
        before = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=instant,
        )
        capacity = before["execution_capacity"]
        if capacity["disposition"] == "release_until_due":
            return {
                "schema_version": "astrowoof.provider_reconciliation_cycle_result.v0.1",
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
        actions = actions[:PROVIDER_RECONCILIATION_POLICY["maximum_due_actions_per_cycle"]]
        if not actions:
            raise ValueError(
                "No due known interactive provider operation is eligible for retrieval"
            )

        def get(action: dict[str, Any]) -> tuple[str, dict[str, Any] | Exception]:
            action_id = action["action_id"]
            provider_id = action["provider"]["id"]
            try:
                response = retrieve(
                    provider_id,
                    float(PROVIDER_RECONCILIATION_POLICY[
                        "provider_retrieval_timeout_seconds"
                    ]),
                )
                if not isinstance(response, dict) or response.get("id") != provider_id:
                    raise ProviderRetrievalIdentityMismatch(
                        "Provider retrieval identity mismatch"
                    )
                return action_id, response
            except Exception as exc:
                return action_id, exc

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=PROVIDER_RECONCILIATION_POLICY["maximum_parallel_retrievals"],
            thread_name_prefix="astrowoof-retrieve",
        ) as executor:
            results = list(executor.map(get, actions))

        retrieved: list[str] = []
        completed: list[str] = []
        warnings: list[str] = []
        identity_conflicts: list[str] = []
        by_id = {item["action_id"]: item for item in actions}
        evidence_root = run_dir / "lifecycle" / "provider-reconciliation"
        for action_id, value in results:
            retrieved.append(action_id)
            action = by_id[action_id]
            timing = action["provider_reconciliation"]
            if isinstance(value, Exception):
                if isinstance(value, ProviderRetrievalIdentityMismatch):
                    identity_conflicts.append(action_id)
                    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                    action["ambiguity"] = {
                        "reason": "provider retrieval identity mismatch"
                    }
                    continue
                warnings.append(action_id)
                record_attempt(
                    timing, attempted_at=instant, outcome="transport_warning"
                )
                continue
            status = value.get("status")
            if status in {"queued", "in_progress"}:
                record_attempt(timing, attempted_at=instant, outcome="pending")
            elif status == "completed":
                record_attempt(timing, attempted_at=instant, outcome="completed")
                completed.append(action_id)
                write_json_atomic(evidence_root / f"{action_id}.response.json", value)
            else:
                warnings.append(action_id)
                record_attempt(
                    timing, attempted_at=instant, outcome="transport_warning"
                )

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
        })
        write_workspace_snapshot(run_dir)
        after = inspect_lifecycle(
            run_dir,
            native_exclusive_access="established",
            observed_at=instant,
        )
        return {
            "schema_version": "astrowoof.provider_reconciliation_cycle_result.v0.1",
            "run_id": state["run_id"],
            "outcome": (
                "review_required" if identity_conflicts
                else "progressed_local" if completed
                else "detached_provider_pending"
            ),
            "decision_basis": before["observation"],
            "cycle": cycle,
            "inspection": after,
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


def run_bounded_authoring_reconciliation(
    run_dir: Path,
    *,
    provider: Any,
    max_attempts: int,
    python_executable: Path,
    observed_at: str,
    event_emitter: Any = None,
) -> dict[str, Any]:
    """Retrieve one due wave and exhaust its newly unblocked pass-local work."""
    from .closure import (
        SNAPSHOT_NAME,
        SpendController,
        author_pending_passes,
        load_json,
        sha256_file,
        write_json_atomic,
        write_workspace_snapshot,
    )
    from .lifecycle import inspect_lifecycle

    if getattr(provider, "name", None) != "openai":
        raise ValueError("Bounded authoring reconciliation requires OpenAI provider")
    retrieval_provider = getattr(provider, "initial", provider)
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
        )
    finally:
        retrieval_provider.http_timeout_seconds = original_timeout
        retrieval_provider.max_transport_retries = original_retries
    completed_ids = set(result["cycle"]["completed_action_ids"])
    if not completed_ids:
        return result

    state = load_json(run_dir / "run.json")
    completed_actions = [
        item for item in (state.get("spend_ledger") or {}).get("actions", [])
        if item.get("action_id") in completed_ids
    ]
    unsupported = [
        item["action_id"] for item in completed_actions
        if (item.get("binding") or {}).get("stage")
        not in {"authoring_initial", "creative_retry"}
    ]
    if unsupported:
        raise ValueError(
            "Slice 3 pass-local reconciliation does not support stages: "
            + ", ".join(unsupported)
        )
    pass_ids = {
        str(item["binding"]["route"]).rsplit(":attempt-", 1)[0]
        for item in completed_actions
    }
    controller = SpendController(
        state=state,
        run_json=run_dir / "run.json",
        state_lock=threading.Lock(),
        consumer_id=f"reconcile:{os.getpid()}",
        event_emitter=event_emitter,
        reconciliation_only=True,
    )
    author_pending_passes(
        state=state,
        provider=provider,
        run_dir=run_dir,
        max_attempts=max_attempts,
        python_executable=python_executable,
        run_json=run_dir / "run.json",
        max_workers=min(
            PROVIDER_RECONCILIATION_POLICY["maximum_parallel_retrievals"],
            max(len(pass_ids), 1),
        ),
        spend_controller=controller,
        only_pass_ids=pass_ids,
    )
    artifact = run_dir / result["result_checkpoint"]["result_artifact"]["logical_path"]
    record = json.loads(artifact.read_text(encoding="utf-8"))
    record["local_continuation"] = {
        "pass_ids": sorted(pass_ids),
        "completed_action_ids": sorted(completed_ids),
        "exhausted_before_detach": True,
    }
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
    result["result_checkpoint"] = {
        "operator_state_revision": inspection["observation"]["operator_state_revision"],
        "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
        "result_artifact": {
            "logical_path": artifact.relative_to(run_dir).as_posix(),
            "bytes": artifact.stat().st_size,
            "sha256": _file_sha256(artifact),
        },
    }
    return result
