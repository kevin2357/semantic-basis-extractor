"""Sanitized operational diagnostics for read-only OpenAI Response retrieval."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

from .application_logging import add_logging_arguments, configure_logging_from_args


RESPONSE_RETRIEVAL_DIAGNOSTIC = "astrowoof.response_retrieval_diagnostic.v1"
MAX_MESSAGE_CHARS = 512
_SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[a-z0-9._~+\-/=]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s,;]+"),
)
_DIAGNOSTIC_KEYS = {
    "schema_version", "attempt_id", "run_id", "action_id",
    "provider_response_id", "endpoint", "started_at", "finished_at",
    "duration_ms", "http_status", "provider_request_id", "provider_status",
    "exception_class", "error_message", "error_fingerprint", "outcome",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def sanitized_host(base_url: str | None) -> str | None:
    if not base_url:
        return None
    try:
        parsed = urlsplit(base_url)
    except ValueError:
        return None
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    try:
        parsed_port = parsed.port
    except ValueError:
        return None
    port = f":{parsed_port}" if parsed_port is not None else ""
    return f"{parsed.scheme}://{parsed.hostname.lower()}{port}"


def sanitized_endpoint(url: str) -> str:
    """Return scheme/host/port/path only, excluding userinfo and query data."""
    try:
        parsed = urlsplit(url)
        host = sanitized_host(url)
    except (TypeError, ValueError):
        return "[invalid-endpoint]"
    if host is None:
        return "[invalid-endpoint]"
    return f"{host}{parsed.path or '/'}"


def sanitize_error_message(value: object, *, secret: str | None = None) -> str:
    text = " ".join(str(value).split())
    if secret:
        text = text.replace(secret, "[REDACTED]")
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub(
            lambda match: (
                f"{match.group(1)}[REDACTED]"
                if match.lastindex else "[REDACTED]"
            ),
            text,
        )
    # Query strings and userinfo are never useful diagnostic evidence.
    text = re.sub(r"https?://[^\s/@]+@", "https://[REDACTED]@", text)
    text = re.sub(r"(https?://[^\s?]+)\?[^\s]+", r"\1?[REDACTED]", text)
    return text[:MAX_MESSAGE_CHARS]


def _exception_metadata(exc: BaseException, *, secret: str | None) -> dict[str, Any]:
    message = sanitize_error_message(exc, secret=secret)
    exception_class = type(exc).__name__
    status = getattr(exc, "status_code", None)
    if not isinstance(status, int) or isinstance(status, bool):
        status = None
    request_id = getattr(exc, "request_id", None)
    if not isinstance(request_id, str) or not re.fullmatch(
        r"[A-Za-z0-9._:-]{1,200}", request_id
    ):
        request_id = None
    fingerprint_basis = json.dumps(
        [exception_class, status, message], separators=(",", ":"), ensure_ascii=True
    )
    return {
        "http_status": status,
        "provider_request_id": request_id,
        "exception_class": exception_class,
        "error_message": message,
        "error_fingerprint": hashlib.sha256(
            fingerprint_basis.encode("utf-8")
        ).hexdigest(),
    }


def build_response_retrieval_diagnostic(
    *,
    provider_response_id: str,
    outcome: str,
    started_at: str,
    finished_at: str,
    duration_ms: int,
    run_id: str | None = None,
    action_id: str | None = None,
    attempt_ordinal: int = 1,
    base_url: str | None = None,
    provider_status: str | None = None,
    exception: BaseException | None = None,
    secret: str | None = None,
) -> dict[str, Any]:
    if outcome not in {
        "completed", "pending", "transport_warning", "identity_conflict"
    }:
        raise ValueError(f"Unsupported Response retrieval outcome: {outcome}")
    if attempt_ordinal < 1:
        raise ValueError("Response retrieval attempt ordinal must be positive")
    identity = "\n".join((
        run_id or "probe", action_id or "probe", provider_response_id,
        str(attempt_ordinal),
    ))
    error = {
        "http_status": None, "provider_request_id": None,
        "exception_class": None, "error_message": None,
        "error_fingerprint": None,
    }
    if exception is not None:
        error = _exception_metadata(exception, secret=secret)
    value = {
        "schema_version": RESPONSE_RETRIEVAL_DIAGNOSTIC,
        "attempt_id": "response-get-" + hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()[:24],
        "run_id": run_id,
        "action_id": action_id,
        "provider_response_id": provider_response_id,
        "endpoint": {
            "method": "GET",
            "route": "/responses/{response_id}",
            "configured_host": sanitized_host(base_url),
        },
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_ms": max(0, int(duration_ms)),
        **error,
        "provider_status": provider_status,
        "outcome": outcome,
    }
    validate_response_retrieval_diagnostic(value)
    return value


def read_response_retrieval_diagnostic_schema() -> dict[str, Any]:
    return json.loads(
        files("astrowoof_natal_authoring").joinpath(
            "resources/contracts/response-retrieval-diagnostic.v1.schema.json"
        ).read_text(encoding="utf-8")
    )


def validate_response_retrieval_diagnostic(value: Mapping[str, Any]) -> None:
    if set(value) != _DIAGNOSTIC_KEYS:
        raise ValueError("Response retrieval diagnostic fields are not closed")
    if value.get("schema_version") != RESPONSE_RETRIEVAL_DIAGNOSTIC:
        raise ValueError("Unsupported Response retrieval diagnostic")
    if value.get("outcome") not in {
        "completed", "pending", "transport_warning", "identity_conflict"
    }:
        raise ValueError("Invalid Response retrieval diagnostic outcome")
    endpoint = value.get("endpoint")
    if not isinstance(endpoint, Mapping) or set(endpoint) != {
        "method", "route", "configured_host"
    } or endpoint.get("method") != "GET" \
            or endpoint.get("route") != "/responses/{response_id}":
        raise ValueError("Invalid Response retrieval endpoint identity")
    if endpoint.get("configured_host") is not None \
            and not isinstance(endpoint["configured_host"], str):
        raise ValueError("Invalid configured provider host identity")
    for key in ("attempt_id", "provider_response_id", "started_at", "finished_at"):
        if not isinstance(value.get(key), str) or not value[key]:
            raise ValueError(f"Invalid Response retrieval diagnostic field: {key}")
    if not isinstance(value.get("duration_ms"), int) or value["duration_ms"] < 0:
        raise ValueError("Invalid Response retrieval duration")
    if not re.fullmatch(r"response-get-[0-9a-f]{24}", value["attempt_id"]):
        raise ValueError("Invalid Response retrieval attempt ID")
    for key in ("run_id", "action_id", "provider_status", "exception_class"):
        if value.get(key) is not None and not isinstance(value[key], str):
            raise ValueError(f"Invalid Response retrieval diagnostic field: {key}")
    status = value.get("http_status")
    if status is not None and (
        not isinstance(status, int) or isinstance(status, bool)
        or status < 100 or status > 599
    ):
        raise ValueError("Invalid Response retrieval HTTP status")
    request_id = value.get("provider_request_id")
    if request_id is not None and (
        not isinstance(request_id, str)
        or not re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", request_id)
    ):
        raise ValueError("Invalid provider request ID")
    fingerprint = value.get("error_fingerprint")
    if fingerprint is not None and (
        not isinstance(fingerprint, str)
        or not re.fullmatch(r"[0-9a-f]{64}", fingerprint)
    ):
        raise ValueError("Invalid Response retrieval error fingerprint")
    message = value.get("error_message")
    if message is not None and (
        not isinstance(message, str) or len(message) > MAX_MESSAGE_CHARS
    ):
        raise ValueError("Invalid sanitized Response retrieval message")


def inspect_response(
    response_id: str,
    *,
    api_key: str,
    base_url: str = "https://api.openai.com/v1",
    timeout_seconds: float = 15.0,
    transport: Any = None,
    clock: Callable[[], str] = _utc_now,
    monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Perform exactly one GET and return only its sanitized diagnostic."""
    from .closure import OpenAIResponsesProvider

    if not isinstance(response_id, str) or not response_id.startswith("resp_"):
        raise ValueError("A provider Response ID beginning with 'resp_' is required")
    provider = OpenAIResponsesProvider(
        api_key=api_key, base_url=base_url, http_timeout_seconds=timeout_seconds,
        max_transport_retries=0, transport=transport,
    )
    started_at = clock()
    started = monotonic()
    response: Any = None
    error: BaseException | None = None
    try:
        response, _ = provider._request_with_retry(
            method="GET", url=f"{provider.base_url}/responses/{response_id}",
            payload=None, timeout_seconds=timeout_seconds,
        )
    except Exception as exc:  # diagnostic boundary intentionally catches transport failures
        error = exc
    duration_ms = round((monotonic() - started) * 1000)
    finished_at = clock()
    provider_status = response.get("status") if isinstance(response, dict) else None
    if not isinstance(provider_status, str):
        provider_status = None
    if error is not None:
        outcome = "transport_warning"
    elif not isinstance(response, dict) or not isinstance(response.get("id"), str):
        error = ValueError("Provider returned a malformed Response object")
        outcome = "transport_warning"
    elif response["id"] != response_id:
        error = ValueError("Provider retrieval identity mismatch")
        outcome = "identity_conflict"
    elif provider_status in {"completed", "failed", "cancelled", "incomplete"}:
        outcome = "completed"
    elif provider_status in {"queued", "in_progress"}:
        outcome = "pending"
    else:
        error = ValueError("Provider returned an unsupported Response status")
        outcome = "transport_warning"
    return build_response_retrieval_diagnostic(
        provider_response_id=response_id, outcome=outcome,
        started_at=started_at, finished_at=finished_at, duration_ms=duration_ms,
        base_url=provider.base_url, provider_status=provider_status,
        exception=error, secret=api_key,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Issue one read-only OpenAI Response GET and print sanitized diagnostics."
    )
    parser.add_argument("--response-id")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--openai-base-url", default="https://api.openai.com/v1")
    parser.add_argument("--timeout-seconds", type=float, default=15.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    add_logging_arguments(parser)
    args = parser.parse_args(argv)
    configure_logging_from_args(args)
    if args.schema:
        value = read_response_retrieval_diagnostic_schema()
    else:
        if not args.response_id:
            parser.error("--response-id is required unless --schema is used")
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            parser.error(f"API key environment variable is not set: {args.api_key_env}")
        value = inspect_response(
            args.response_id, api_key=api_key,
            base_url=args.openai_base_url, timeout_seconds=args.timeout_seconds,
        )
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output.resolve()
        for parent in (output.parent, *output.parents):
            if (parent / "run.json").is_file() \
                    and (parent / "workspace-snapshot.json").is_file():
                parser.error("--output must not resolve inside a native run workspace")
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0
