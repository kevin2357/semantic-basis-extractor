"""Bounded, non-authoritative structured execution events."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable
from pathlib import Path
import threading
import sys

from .lifecycle_contracts import (
    EVENT_NAMES,
    EVENT_SEVERITIES,
    EXECUTION_EVENT_SCHEMA,
    prohibited_event_paths,
)


EVENT_PAYLOAD_CATALOG_SCHEMA = "sbe.execution_event_payload_catalog.v1"
COMMAND_RESULT_SCHEMA = "sbe.command_result.v1"

# Closed required fields for each v1 event name. Additional bounded event data is
# permitted only for observational enrichment and cannot become execution authority.
EVENT_PAYLOAD_REQUIRED: dict[str, tuple[str, ...]] = {
    "run.started": ("state_revision",),
    "run.resumed": ("state_revision",),
    "run.detached": ("state_revision", "reason_code"),
    "pass.prepared": ("route", "attempt"),
    "authorization.awaiting": ("action_id", "stage", "commitment_micro_usd"),
    "authorization.granted": ("action_id", "stage", "commitment_micro_usd"),
    "authorization.denied_providerless": ("action_id", "denial_reason", "outcome"),
    "provider.submission_started": ("action_id", "stage", "attempt"),
    "provider.identity_recorded": ("action_id", "provider_operation_id"),
    "provider.waiting": ("action_id", "provider_operation_id"),
    "provider.completed": ("action_id", "provider_operation_id", "duration_ms"),
    "qa.started": ("scope", "attempt"),
    "qa.completed": ("scope", "attempt", "outcome"),
    "retry.decided": ("route", "attempt", "decision", "reason_code"),
    "polish.decided": ("attempt", "decision", "reason_code"),
    "critic.decided": ("decision", "reason_code"),
    "checkpoint.committed": ("state_revision", "snapshot_sha256"),
    "terminal.transitioned": ("outcome", "terminal_reason"),
    "closeout.completed": ("disposition", "semantic_result_sha256"),
    "execution.failed": ("reason_code", "failure_class"),
    "event_sink.warning": ("warning_code", "dropped_event_count"),
    "bounded.admission.completed": ("admission_id", "input_contract"),
    "bounded.family.validated": ("context_count", "certainty_class"),
    "bounded.selection.completed": ("claim_count", "selection_contract"),
    "bounded.disposition.completed": ("selected_count", "suppressed_count"),
    "bounded.artifact.committed": ("artifact_kind", "schema_version", "sha256"),
}


def payload_catalog() -> dict[str, Any]:
    return {
        "schema_version": EVENT_PAYLOAD_CATALOG_SCHEMA,
        "events": {
            name: {"required_fields": list(EVENT_PAYLOAD_REQUIRED[name])}
            for name in EVENT_NAMES
        },
    }


def validate_event_payload(event_name: str, data: dict[str, Any]) -> None:
    if event_name not in EVENT_PAYLOAD_REQUIRED:
        raise ValueError(f"Unsupported execution event name: {event_name}")
    if not isinstance(data, dict):
        raise ValueError("Execution event data must be an object")
    missing = set(EVENT_PAYLOAD_REQUIRED[event_name]) - set(data)
    if missing:
        raise ValueError(f"Execution event {event_name} lacks {sorted(missing)}")
    prohibited = prohibited_event_paths(data)
    if prohibited:
        raise ValueError(f"Execution event contains prohibited fields: {prohibited}")


@dataclass
class EventDeliveryStats:
    emitted: int = 0
    dropped: int = 0
    serialization_warnings: int = 0
    sink_warnings: int = 0


class JsonlEventSink:
    """Append typed envelopes to a JSONL file outside the native workspace."""

    def __init__(self, path: Path) -> None:
        self.path = path.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def __call__(self, envelope: dict[str, Any]) -> None:
        rendered = json.dumps(
            envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ) + "\n"
        with self._lock, self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)


class StdoutJsonlSink:
    """Write one typed envelope per stdout line."""

    def __init__(self, stream=None) -> None:
        self.stream = stream or sys.stdout
        self._lock = threading.Lock()

    def __call__(self, envelope: dict[str, Any]) -> None:
        rendered = json.dumps(
            envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        with self._lock:
            self.stream.write(rendered + "\n")
            self.stream.flush()


def command_result_envelope(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": COMMAND_RESULT_SCHEMA,
        "envelope_type": "command_result",
        "result": result,
    }


class ExecutionEventEmitter:
    """Deliver observations without allowing sink failure to affect execution."""

    def __init__(
        self,
        *,
        release: str,
        sink: Callable[[dict[str, Any]], None] | None = None,
        base_correlation: dict[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.release = release
        self.sink = sink
        self.base_correlation = dict(base_correlation or {})
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.id_factory = id_factory or (lambda: f"evt_{uuid.uuid4().hex}")
        self.stats = EventDeliveryStats()

    def emit(
        self,
        event_name: str,
        *,
        data: dict[str, Any],
        severity: str = "info",
        correlation: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        try:
            if severity not in EVENT_SEVERITIES:
                raise ValueError(f"Unsupported event severity: {severity}")
            validate_event_payload(event_name, data)
            joined = {**self.base_correlation, **(correlation or {})}
            envelope = {
                "schema_version": EXECUTION_EVENT_SCHEMA,
                "envelope_type": "execution_event",
                "event_id": self.id_factory(),
                "event_time": self.clock().isoformat().replace("+00:00", "Z"),
                "event_name": event_name,
                "severity": severity,
                "component": "astrowoof-natal-authoring",
                "release": self.release,
                "correlation": joined,
                "data": data,
            }
            json.dumps(envelope, ensure_ascii=False)
        except (TypeError, ValueError):
            self.stats.dropped += 1
            self.stats.serialization_warnings += 1
            return None
        if self.sink is not None:
            try:
                self.sink(envelope)
            except Exception:
                self.stats.dropped += 1
                self.stats.sink_warnings += 1
                return None
        self.stats.emitted += 1
        return envelope
