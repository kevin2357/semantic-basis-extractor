"""Closed provider-free result for a bounded source below the product floor."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping


SCHEMA_VERSION = "astrowoof.bounded_eligibility_command_result.v2"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_COMMAND_ATTEMPT_ID = re.compile(r"^bca_[0-9a-f]{24}$")
_RESULT_ID = re.compile(r"^belig_[0-9a-f]{24}$")
_SOURCE_KEYS = {
    "canonical_semantic_identity_sha256",
    "projection_set_evidence_sha256",
}
_BINDING_KEYS = {
    "schema_version",
    "processing_profile_id",
    "processing_profile_sha256",
    "generation_manifest_sha256",
    "route_family",
    "worker_role",
    "worker_compatibility_sha256",
}
_RESULT_KEYS = {
    "schema_version", "outcome", "reason_code", "retryable_for_same_sealed_input",
    "provider_activity", "native_run_id", "command_attempt_id", "source_binding",
    "processing_profile_binding", "result_id", "result_sha256",
}


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _require_digest(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _validate_source_binding(value: Mapping[str, object]) -> dict[str, str]:
    if set(value) != _SOURCE_KEYS:
        raise ValueError("bounded eligibility source binding fields are invalid")
    return {
        key: _require_digest(value.get(key), label=f"source binding {key}")
        for key in sorted(_SOURCE_KEYS)
    }


def _validate_processing_profile_binding(value: Mapping[str, object]) -> dict[str, str]:
    if set(value) != _BINDING_KEYS:
        raise ValueError("bounded eligibility processing profile binding fields are invalid")
    for key in (
        "processing_profile_sha256", "generation_manifest_sha256", "worker_compatibility_sha256",
    ):
        _require_digest(value.get(key), label=f"processing profile binding {key}")
    if (
        value.get("schema_version") != "astrowoof.processing_profile_binding.v1"
        or value.get("route_family") != "bounded_natal"
        or value.get("worker_role") != "sbe_authoring"
        or not isinstance(value.get("processing_profile_id"), str)
        or not value["processing_profile_id"]
    ):
        raise ValueError("bounded eligibility processing profile binding is invalid")
    return {key: str(value[key]) for key in sorted(_BINDING_KEYS)}


def _result_id_material(value: Mapping[str, object]) -> dict[str, object]:
    return {key: value[key] for key in sorted(value) if key not in {"result_id", "result_sha256"}}


def _result_sha_material(value: Mapping[str, object]) -> dict[str, object]:
    return {key: value[key] for key in sorted(value) if key != "result_sha256"}


def build_bounded_eligibility_command_result(
    *,
    native_run_id: str,
    command_attempt_id: str,
    source_binding: Mapping[str, object],
    processing_profile_binding: Mapping[str, object],
) -> dict[str, object]:
    """Build the sole pre-workspace terminal result for an under-50 source."""
    _require_digest(native_run_id, label="native run ID")
    if not isinstance(command_attempt_id, str) or not _COMMAND_ATTEMPT_ID.fullmatch(command_attempt_id):
        raise ValueError("command attempt ID is invalid")
    value: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "outcome": "ineligible",
        "reason_code": "insufficient_invariant_basis",
        "retryable_for_same_sealed_input": False,
        "provider_activity": "not_attempted",
        "native_run_id": native_run_id,
        "command_attempt_id": command_attempt_id,
        "source_binding": _validate_source_binding(source_binding),
        "processing_profile_binding": _validate_processing_profile_binding(processing_profile_binding),
    }
    value["result_id"] = "belig_" + _canonical_sha256(_result_id_material(value))[:24]
    value["result_sha256"] = _canonical_sha256(_result_sha_material(value))
    validate_bounded_eligibility_command_result(value)
    return value


def validate_bounded_eligibility_command_result(value: Mapping[str, object]) -> None:
    """Refuse every variation outside the intentionally tiny public contract."""
    if set(value) != _RESULT_KEYS:
        raise ValueError("bounded eligibility result fields are invalid")
    if (
        value.get("schema_version") != SCHEMA_VERSION
        or value.get("outcome") != "ineligible"
        or value.get("reason_code") != "insufficient_invariant_basis"
        or value.get("retryable_for_same_sealed_input") is not False
        or value.get("provider_activity") != "not_attempted"
    ):
        raise ValueError("bounded eligibility result disposition is invalid")
    _require_digest(value.get("native_run_id"), label="native run ID")
    if not isinstance(value.get("command_attempt_id"), str) or not _COMMAND_ATTEMPT_ID.fullmatch(value["command_attempt_id"]):
        raise ValueError("command attempt ID is invalid")
    source_binding = value.get("source_binding")
    profile_binding = value.get("processing_profile_binding")
    if not isinstance(source_binding, Mapping) or not isinstance(profile_binding, Mapping):
        raise ValueError("bounded eligibility result binding is invalid")
    _validate_source_binding(source_binding)
    _validate_processing_profile_binding(profile_binding)
    if not isinstance(value.get("result_id"), str) or not _RESULT_ID.fullmatch(value["result_id"]):
        raise ValueError("bounded eligibility result ID is invalid")
    id_material = _result_id_material(value)
    if value["result_id"] != "belig_" + _canonical_sha256(id_material)[:24]:
        raise ValueError("bounded eligibility result ID does not match content")
    if value.get("result_sha256") != _canonical_sha256(_result_sha_material(value)):
        raise ValueError("bounded eligibility result digest does not match content")
