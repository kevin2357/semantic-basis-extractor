"""Small stdlib logging setup and scoped operational context."""

from __future__ import annotations

import argparse
import contextvars
import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator


DEFAULT_LOG_FORMAT = (
    "✨🐶 %(asctime)s | %(levelname)s | %(host_id)s | %(run_id)s | "
    "%(invocation_id)s | %(funcName)s | %(current_state)s : %(message)s"
)
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

_host_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "astrowoof_log_host_id", default="-"
)
_run_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "astrowoof_log_run_id", default="-"
)
_invocation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "astrowoof_log_invocation_id", default="-"
)
_current_state: contextvars.ContextVar[str] = contextvars.ContextVar(
    "astrowoof_log_current_state", default="-"
)


class OperationalContextFilter(logging.Filter):
    """Populate stable defaults without changing the normal LogRecord contract."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.host_id = _host_id.get()
        record.run_id = _run_id.get()
        record.invocation_id = _invocation_id.get()
        record.current_state = _current_state.get()
        return True


class UtcIsoFormatter(logging.Formatter):
    """Render stdlib timestamps as UTC ISO-8601 with milliseconds."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        instant = datetime.fromtimestamp(record.created, timezone.utc)
        return instant.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def default_host_id() -> str:
    return (
        os.environ.get("ASTROWOOF_HOST_ID")
        or os.environ.get("HOSTNAME")
        or os.environ.get("COMPUTERNAME")
        or "-"
    )


def configure_logging(
    *,
    level: str = "INFO",
    host_id: str | None = None,
    invocation_id: str | None = None,
    stream: Any = None,
    force: bool = False,
) -> logging.Handler:
    """Configure the root logger once for an SBE CLI process."""
    normalized = str(level).upper()
    if normalized not in LOG_LEVELS:
        raise ValueError(f"Unsupported log level: {level}")
    _host_id.set(str(host_id or default_host_id()))
    _invocation_id.set(str(invocation_id or os.environ.get(
        "ASTROWOOF_INVOCATION_ID", "-"
    )))
    _run_id.set("-")
    _current_state.set("-")
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
    handler.setFormatter(UtcIsoFormatter(DEFAULT_LOG_FORMAT))
    handler.addFilter(OperationalContextFilter())
    root.addHandler(handler)
    root.setLevel(normalized)
    return handler


def add_logging_arguments(parser: argparse.ArgumentParser) -> None:
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
        invocation_id=getattr(args, "invocation_id", None),
    )


def bind_logging_context(
    *,
    run_id: str | None = None,
    invocation_id: str | None = None,
    current_state: str | None = None,
) -> None:
    """Bind context for the remainder of the current execution context."""
    if run_id is not None:
        _run_id.set(str(run_id))
    if invocation_id is not None:
        _invocation_id.set(str(invocation_id))
    if current_state is not None:
        _current_state.set(str(current_state))


def current_logging_context() -> dict[str, str]:
    """Return the current safe correlation fields for explicit thread handoff."""
    return {
        "host_id": _host_id.get(),
        "run_id": _run_id.get(),
        "invocation_id": _invocation_id.get(),
        "current_state": _current_state.get(),
    }


@contextmanager
def logging_context(
    *,
    host_id: str | None = None,
    run_id: str | None = None,
    invocation_id: str | None = None,
    current_state: str | None = None,
) -> Iterator[None]:
    """Temporarily bind safe context across threads/tasks that copy contextvars."""
    tokens = []
    try:
        if host_id is not None:
            tokens.append((_host_id, _host_id.set(str(host_id))))
        if run_id is not None:
            tokens.append((_run_id, _run_id.set(str(run_id))))
        if invocation_id is not None:
            tokens.append((_invocation_id, _invocation_id.set(str(invocation_id))))
        if current_state is not None:
            tokens.append((_current_state, _current_state.set(str(current_state))))
        yield
    finally:
        for variable, token in reversed(tokens):
            variable.reset(token)
