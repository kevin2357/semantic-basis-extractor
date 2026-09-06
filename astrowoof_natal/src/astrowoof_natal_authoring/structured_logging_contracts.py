"""Closed diagnostic contract for structured SBE application logs."""

from __future__ import annotations

import json
import math
import re
from importlib.resources import files
from typing import Any, Mapping


SCHEMA_VERSION = "astrowoof.sbe_worker_log.v1"
RECORD_TYPE = "application_log"
CORRELATION_KEYS = {
    "api_run_id", "native_run_id", "subject_id", "invocation_id",
    "action_id", "provider_operation_id", "checkpoint_object_id",
}
PRODUCER_KEYS = {"service", "host_id", "runtime_version"}
EXCEPTION_KEYS = {
    "exception_class", "classification_code", "fingerprint",
    "sanitized_message",
}
RECORD_KEYS = {
    "schema_version", "record_type", "timestamp", "level", "event_name",
    "message", "logger", "function", "current_state", "correlation",
    "payload", "producer", "exception",
}
LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
_EVENT_NAME = re.compile(r"^[a-z][a-z0-9_]{1,79}$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{16}$")
_PROHIBITED_FIELD_PARTS = {
    "authorization_secret", "credential", "full_payload", "full_prompt",
    "prompt_text", "provider_response_body", "raw_response", "secret",
    "source_archive", "source_zip", "workspace_path",
}
_SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{8,}"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*\S+"),
)


def read_sbe_worker_log_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        "contracts/sbe-worker-log.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def read_sbe_worker_log_event_catalog() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        "contracts/sbe-worker-log-event-catalog.v1.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def _validate_json_value(
    value: Any, *, depth: int = 0, maximum_string_length: int = 512,
) -> None:
    if depth > 3:
        raise ValueError("Structured log payload exceeds maximum depth")
    if value is None or type(value) in {bool, int}:
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Structured log number must be finite")
        return
    if isinstance(value, str):
        if len(value) > maximum_string_length or "\n" in value or "\r" in value:
            raise ValueError("Structured log string is invalid or unbounded")
        for pattern in _SENSITIVE_VALUE_PATTERNS:
            match = pattern.search(value)
            if match is not None and "[REDACTED]" not in match.group(0):
                raise ValueError("Structured log contains sensitive content")
        return
    if isinstance(value, list):
        if len(value) > 128:
            raise ValueError("Structured log array is unbounded")
        for item in value:
            _validate_json_value(item, depth=depth + 1)
        return
    if isinstance(value, dict):
        if len(value) > 64:
            raise ValueError("Structured log object is unbounded")
        for key, item in value.items():
            if not isinstance(key, str) or not key or len(key) > 80:
                raise ValueError("Structured log field name is invalid")
            normalized = key.lower()
            if any(part in normalized for part in _PROHIBITED_FIELD_PARTS):
                raise ValueError("Structured log field is prohibited")
            _validate_json_value(item, depth=depth + 1)
        return
    raise ValueError("Structured log value is not a JSON primitive/container")


def validate_sbe_worker_log(value: Mapping[str, Any]) -> None:
    """Validate the closed envelope and event-specific bounded payload."""
    if not isinstance(value, dict) or set(value) != RECORD_KEYS:
        raise ValueError("Structured log record shape is invalid")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Structured log schema version is invalid")
    if value.get("record_type") != RECORD_TYPE:
        raise ValueError("Structured log record type is invalid")
    if not _TIMESTAMP.fullmatch(str(value.get("timestamp"))):
        raise ValueError("Structured log timestamp is invalid")
    if value.get("level") not in LOG_LEVELS:
        raise ValueError("Structured log level is invalid")
    event_name = value.get("event_name")
    if not isinstance(event_name, str) or not _EVENT_NAME.fullmatch(event_name):
        raise ValueError("Structured log event name is invalid")
    for key, maximum in (("message", 2048), ("logger", 256), ("function", 256)):
        item = value.get(key)
        if not isinstance(item, str) or not item or len(item) > maximum:
            raise ValueError(f"Structured log {key} is invalid")
        _validate_json_value(item, maximum_string_length=maximum)
    if not value["message"].startswith("✨🐶 "):
        raise ValueError("Structured log message lacks the readable marker")
    state = value.get("current_state")
    if state is not None and (not isinstance(state, str) or not state or len(state) > 128):
        raise ValueError("Structured log current state is invalid")
    correlation = value.get("correlation")
    if not isinstance(correlation, dict) or set(correlation) != CORRELATION_KEYS:
        raise ValueError("Structured log correlation shape is invalid")
    for item in correlation.values():
        if item is not None and (not isinstance(item, str) or not item or len(item) > 256):
            raise ValueError("Structured log correlation identity is invalid")
    producer = value.get("producer")
    if not isinstance(producer, dict) or set(producer) != PRODUCER_KEYS:
        raise ValueError("Structured log producer shape is invalid")
    if producer.get("service") != "sbe-worker":
        raise ValueError("Structured log producer service is invalid")
    for key in ("host_id", "runtime_version"):
        item = producer.get(key)
        if item is not None and (not isinstance(item, str) or not item or len(item) > 128):
            raise ValueError("Structured log producer identity is invalid")
    exception = value.get("exception")
    if exception is not None:
        if not isinstance(exception, dict) or set(exception) != EXCEPTION_KEYS:
            raise ValueError("Structured log exception shape is invalid")
        if not isinstance(exception.get("exception_class"), str):
            raise ValueError("Structured log exception class is invalid")
        code = exception.get("classification_code")
        if code is not None and (not isinstance(code, str) or not _EVENT_NAME.fullmatch(code)):
            raise ValueError("Structured log exception classification is invalid")
        if not _FINGERPRINT.fullmatch(str(exception.get("fingerprint"))):
            raise ValueError("Structured log exception fingerprint is invalid")
        message = exception.get("sanitized_message")
        if not isinstance(message, str) or not message or len(message) > 240:
            raise ValueError("Structured log exception message is invalid")
        _validate_json_value(message)
    payload = value.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("Structured log payload must be an object")
    catalog = read_sbe_worker_log_event_catalog()
    definition = catalog["events"].get(event_name)
    if not isinstance(definition, dict):
        raise ValueError("Structured log event is not in the closed vocabulary")
    allowed = set(definition["required_fields"]) | set(definition["optional_fields"])
    if set(payload) - allowed or not set(definition["required_fields"]).issubset(payload):
        raise ValueError("Structured log event payload shape is invalid")
    _validate_json_value(payload)


__all__ = [
    "SCHEMA_VERSION", "RECORD_TYPE", "validate_sbe_worker_log",
    "read_sbe_worker_log_schema", "read_sbe_worker_log_event_catalog",
]
