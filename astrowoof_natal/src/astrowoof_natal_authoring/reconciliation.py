"""Durable scheduling evidence for known provider-operation reconciliation."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any

from .lifecycle_contracts import (
    PROVIDER_RECONCILIATION_POLICY,
    PROVIDER_RECONCILIATION_POLICY_SCHEMA,
)


RECONCILIABLE_PROVIDER_STATES = {
    "PROVIDER_ID_RECORDED", "WAITING",
}


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
        parse_utc_instant(timing["resume_not_before"])
        if timing["last_attempt_at"] is not None:
            parse_utc_instant(timing["last_attempt_at"])
    except (TypeError, ValueError):
        return None
    return deepcopy(timing)
