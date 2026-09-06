"""Small stdlib logging setup and scoped operational context."""

from __future__ import annotations

import argparse
import contextvars
import hashlib
import importlib.metadata
import json
import logging
import os
import re
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator, Mapping

from .structured_logging_contracts import validate_sbe_worker_log


LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
_SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{8,}"),
    re.compile(r"(?i)((?:api[_-]?key|secret|token|password)\s*[:=]\s*)\S+"),
)

_host_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_host_id", default=None
)
_api_run_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_api_run_id", default=None
)
_native_run_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_native_run_id", default=None
)
_subject_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_subject_id", default=None
)
_invocation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_invocation_id", default=None
)
_action_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_action_id", default=None
)
_provider_operation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_provider_operation_id", default=None
)
_checkpoint_object_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_checkpoint_object_id", default=None
)
_current_state: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "astrowoof_log_current_state", default=None
)


class OperationalContextFilter(logging.Filter):
    """Populate stable defaults without changing the normal LogRecord contract."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.host_id = _host_id.get()
        record.api_run_id = _api_run_id.get()
        record.native_run_id = _native_run_id.get()
        # Retain the old LogRecord attribute for embedding code that inspects it.
        record.run_id = record.native_run_id
        record.subject_id = _subject_id.get()
        record.invocation_id = _invocation_id.get()
        record.action_id = _action_id.get()
        record.provider_operation_id = _provider_operation_id.get()
        record.checkpoint_object_id = _checkpoint_object_id.get()
        record.current_state = _current_state.get()
        return True


def _utc_timestamp(created: float) -> str:
    instant = datetime.fromtimestamp(created, timezone.utc)
    return instant.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _runtime_version() -> str | None:
    try:
        return importlib.metadata.version("astrowoof-natal-authoring")
    except importlib.metadata.PackageNotFoundError:
        return None


def _clean_text(value: Any, *, maximum_length: int) -> str:
    text = " ".join(str(value).split())
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub(lambda match: (
            f"{match.group(1)}[REDACTED]" if match.lastindex else "[REDACTED]"
        ), text)
    return text[:maximum_length]


def _nullable(value: Any) -> str | None:
    if value is None or value == "-":
        return None
    cleaned = _clean_text(value, maximum_length=256)
    return cleaned or None


class StructuredApplicationLogFormatter(logging.Formatter):
    """Emit one closed diagnostic JSON object without failing native work."""

    def _fallback(self, record: logging.LogRecord, exc: BaseException) -> str:
        exception_class = type(exc).__name__
        diagnostic = _clean_text(exc, maximum_length=240) or exception_class
        fingerprint = hashlib.sha256(
            f"{exception_class}:{diagnostic}".encode("utf-8")
        ).hexdigest()[:16]
        value = {
            "schema_version": "astrowoof.sbe_worker_log.v1",
            "record_type": "application_log",
            "timestamp": _utc_timestamp(getattr(record, "created", 0.0)),
            "level": "ERROR",
            "event_name": "application_message",
            "message": "✨🐶 logging serialization failed",
            "logger": _clean_text(getattr(record, "name", "sbe"), maximum_length=256) or "sbe",
            "function": _clean_text(getattr(record, "funcName", "unknown"), maximum_length=256) or "unknown",
            "current_state": None,
            "correlation": {
                "api_run_id": None, "native_run_id": None, "subject_id": None,
                "invocation_id": None, "action_id": None,
                "provider_operation_id": None, "checkpoint_object_id": None,
            },
            "payload": {},
            "producer": {"service": "sbe-worker", "host_id": None, "runtime_version": _runtime_version()},
            "exception": {
                "exception_class": exception_class,
                "classification_code": "logging_serialization_failed",
                "fingerprint": fingerprint,
                "sanitized_message": diagnostic,
            },
        }
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

    def format(self, record: logging.LogRecord) -> str:
        try:
            rendered_message = _clean_text(record.getMessage(), maximum_length=2045)
            if not rendered_message.startswith("✨🐶 "):
                rendered_message = f"✨🐶 {rendered_message}"
            exception = None
            if record.exc_info and record.exc_info[1] is not None:
                from .trace_observability import sanitize_exception

                diagnostic = sanitize_exception(record.exc_info[1])
                exception = {
                    "exception_class": diagnostic["exception_class"],
                    "classification_code": _nullable(getattr(record, "exception_code", None)),
                    "fingerprint": diagnostic["fingerprint"],
                    "sanitized_message": diagnostic["sanitized_message"],
                }
            payload = getattr(record, "event_payload", {})
            if not isinstance(payload, Mapping):
                raise ValueError("event_payload must be an object")
            value = {
                "schema_version": "astrowoof.sbe_worker_log.v1",
                "record_type": "application_log",
                "timestamp": _utc_timestamp(record.created),
                "level": record.levelname,
                "event_name": getattr(record, "event_name", "application_message"),
                "message": rendered_message,
                "logger": record.name,
                "function": record.funcName,
                "current_state": _nullable(getattr(record, "current_state", None)),
                "correlation": {
                    "api_run_id": _nullable(getattr(record, "api_run_id", None)),
                    "native_run_id": _nullable(getattr(record, "native_run_id", None)),
                    "subject_id": _nullable(getattr(record, "subject_id", None)),
                    "invocation_id": _nullable(getattr(record, "invocation_id", None)),
                    "action_id": _nullable(getattr(record, "action_id", None)),
                    "provider_operation_id": _nullable(getattr(record, "provider_operation_id", None)),
                    "checkpoint_object_id": _nullable(getattr(record, "checkpoint_object_id", None)),
                },
                "payload": dict(payload),
                "producer": {
                    "service": "sbe-worker",
                    "host_id": _nullable(getattr(record, "host_id", None)),
                    "runtime_version": _runtime_version(),
                },
                "exception": exception,
            }
            validate_sbe_worker_log(value)
            return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        except Exception as exc:
            return self._fallback(record, exc)


def default_host_id() -> str | None:
    return (
        os.environ.get("ASTROWOOF_HOST_ID")
        or os.environ.get("HOSTNAME")
        or os.environ.get("COMPUTERNAME")
        or None
    )


def configure_logging(
    *,
    level: str = "INFO",
    host_id: str | None = None,
    api_run_id: str | None = None,
    invocation_id: str | None = None,
    stream: Any = None,
    force: bool = False,
) -> logging.Handler:
    """Configure the root logger once for an SBE CLI process."""
    normalized = str(level).upper()
    if normalized not in LOG_LEVELS:
        raise ValueError(f"Unsupported log level: {level}")
    _host_id.set(_nullable(host_id or default_host_id()))
    _api_run_id.set(_nullable(api_run_id or os.environ.get("ASTROWOOF_API_RUN_ID")))
    _invocation_id.set(_nullable(invocation_id or os.environ.get("ASTROWOOF_INVOCATION_ID")))
    _native_run_id.set(None)
    _subject_id.set(None)
    _action_id.set(None)
    _provider_operation_id.set(None)
    _checkpoint_object_id.set(None)
    _current_state.set(None)
    root = logging.getLogger()
    if force:
        for handler in list(root.handlers):
            root.removeHandler(handler)
    else:
        for existing in list(root.handlers):
            if getattr(existing, "_astrowoof_sbe_handler", False):
                root.removeHandler(existing)
    handler = logging.StreamHandler(stream or sys.stderr)
    handler._astrowoof_sbe_handler = True  # type: ignore[attr-defined]
    handler.setFormatter(StructuredApplicationLogFormatter())
    handler.addFilter(OperationalContextFilter())
    root.addHandler(handler)
    root.setLevel(normalized)
    return handler


def add_logging_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--api-run-id",
        help="Caller-supplied API run identity; never derived from native state.",
    )
    parser.add_argument(
        "--log-level", choices=LOG_LEVELS, default="INFO",
        help="Ordinary application log verbosity; records are written to stderr.",
    )
    parser.add_argument(
        "--host-id", help="Worker/container identity (default: ASTROWOOF_HOST_ID).",
    )
    parser.add_argument(
        "--invocation-id",
        help="Optional API/worker invocation correlation identity.",
    )


def configure_logging_from_args(args: argparse.Namespace) -> logging.Handler:
    return configure_logging(
        level=getattr(args, "log_level", "INFO"),
        host_id=getattr(args, "host_id", None),
        api_run_id=getattr(args, "api_run_id", None),
        invocation_id=getattr(args, "invocation_id", None),
    )


def bind_logging_context(
    *,
    api_run_id: str | None = None,
    run_id: str | None = None,
    native_run_id: str | None = None,
    subject_id: str | None = None,
    invocation_id: str | None = None,
    current_state: str | None = None,
    action_id: str | None = None,
    provider_operation_id: str | None = None,
    checkpoint_object_id: str | None = None,
) -> None:
    """Bind context for the remainder of the current execution context."""
    if api_run_id is not None:
        _api_run_id.set(str(api_run_id))
    chosen_native_run = native_run_id if native_run_id is not None else run_id
    if chosen_native_run is not None:
        _native_run_id.set(str(chosen_native_run))
    if subject_id is not None:
        _subject_id.set(str(subject_id))
    if invocation_id is not None:
        _invocation_id.set(str(invocation_id))
    if current_state is not None:
        _current_state.set(str(current_state))
    if action_id is not None:
        _action_id.set(str(action_id))
    if provider_operation_id is not None:
        _provider_operation_id.set(str(provider_operation_id))
    if checkpoint_object_id is not None:
        _checkpoint_object_id.set(str(checkpoint_object_id))


def current_logging_context() -> dict[str, str | None]:
    """Return the current safe correlation fields for explicit thread handoff."""
    return {
        "host_id": _host_id.get(),
        "api_run_id": _api_run_id.get(),
        "run_id": _native_run_id.get(),
        "native_run_id": _native_run_id.get(),
        "subject_id": _subject_id.get(),
        "invocation_id": _invocation_id.get(),
        "action_id": _action_id.get(),
        "provider_operation_id": _provider_operation_id.get(),
        "checkpoint_object_id": _checkpoint_object_id.get(),
        "current_state": _current_state.get(),
    }


@contextmanager
def logging_context(
    *,
    host_id: str | None = None,
    api_run_id: str | None = None,
    run_id: str | None = None,
    native_run_id: str | None = None,
    subject_id: str | None = None,
    invocation_id: str | None = None,
    current_state: str | None = None,
    action_id: str | None = None,
    provider_operation_id: str | None = None,
    checkpoint_object_id: str | None = None,
) -> Iterator[None]:
    """Temporarily bind safe context across threads/tasks that copy contextvars."""
    tokens = []
    try:
        if host_id is not None:
            tokens.append((_host_id, _host_id.set(str(host_id))))
        if api_run_id is not None:
            tokens.append((_api_run_id, _api_run_id.set(str(api_run_id))))
        chosen_native_run = native_run_id if native_run_id is not None else run_id
        if chosen_native_run is not None:
            tokens.append((_native_run_id, _native_run_id.set(str(chosen_native_run))))
        if subject_id is not None:
            tokens.append((_subject_id, _subject_id.set(str(subject_id))))
        if invocation_id is not None:
            tokens.append((_invocation_id, _invocation_id.set(str(invocation_id))))
        if current_state is not None:
            tokens.append((_current_state, _current_state.set(str(current_state))))
        if action_id is not None:
            tokens.append((_action_id, _action_id.set(str(action_id))))
        if provider_operation_id is not None:
            tokens.append((_provider_operation_id, _provider_operation_id.set(str(provider_operation_id))))
        if checkpoint_object_id is not None:
            tokens.append((_checkpoint_object_id, _checkpoint_object_id.set(str(checkpoint_object_id))))
        yield
    finally:
        for variable, token in reversed(tokens):
            variable.reset(token)
