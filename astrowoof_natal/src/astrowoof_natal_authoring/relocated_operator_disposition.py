"""Additive contracts for read-only relocated operator assessment."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping, cast
from uuid import UUID

from .operator_disposition import validate_operator_disposition_assessment


AUTHORITY_SCHEMA = "astrowoof.operator_disposition_relocation_authority.v1"
WRAPPER_SCHEMA = "astrowoof.relocated_operator_disposition_assessment.v1"
OPERATION = "read_operator_disposition_assessment"
ASSESSMENT_MODE = "relocated_read_only_checkpoint"

_SHA = re.compile(r"^[0-9a-f]{64}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_OPAQUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@/-]{0,127}$")
_AUTHORITY_KEYS = {
    "schema_version", "operation", "request_id", "api_run_id", "job_id",
    "native_run_id", "checkpoint_id", "checkpoint_generation",
    "checkpoint_contract", "compatibility_identity", "archive_sha256",
    "inventory_sha256", "original_logical_root_sha256",
    "restored_root_sha256", "terminal_result_id", "issued_at", "expires_at",
    "provider_io_permitted", "workspace_mutation_permitted",
    "authority_sha256",
}
_WRAPPER_KEYS = {
    "schema_version", "authority_sha256", "request_id", "native_run_id",
    "checkpoint_id", "checkpoint_generation", "archive_sha256",
    "inventory_sha256", "original_logical_root_sha256",
    "restored_root_sha256", "assessment_mode", "assessed_at",
    "provider_io_performed", "workspace_mutation_performed", "assessment",
    "wrapper_sha256",
}


def _canonical(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def canonical_root_sha256(value: str) -> str:
    """Hash a platform-independent canonical logical-root identity."""
    canonical = canonical_logical_root(value)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def canonical_logical_root(value: str) -> str:
    """Normalize POSIX/Windows absolute path spelling without filesystem access."""
    if not isinstance(value, str) or not value or len(value) > 512:
        raise ValueError("Canonical logical root is invalid")
    if value != value.strip() or any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        raise ValueError("Canonical logical root is invalid")
    text = value.replace("\\", "/")
    drive = re.fullmatch(r"([A-Za-z]):/(.*)", text)
    if drive:
        prefix = f"windows:{drive.group(1).lower()}:/"
        tail = drive.group(2) or ""
        casefold = True
    elif text.startswith("/") and not text.startswith("//"):
        prefix = "posix:/"
        tail = text[1:]
        casefold = False
    else:
        raise ValueError("Logical root must be an absolute POSIX or drive path")
    parts: list[str] = []
    for raw in tail.split("/"):
        if raw in {"", "."}:
            continue
        if raw == "..":
            if not parts:
                raise ValueError("Logical root escapes its root")
            parts.pop()
            continue
        if any(ord(character) < 32 or ord(character) == 127 for character in raw):
            raise ValueError("Canonical logical root is invalid")
        parts.append(raw.casefold() if casefold else raw)
    return prefix + "/".join(parts)


def _uuid(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} is invalid")
    try:
        parsed = UUID(value)
    except (ValueError, AttributeError) as error:
        raise ValueError(f"{label} is invalid") from error
    if str(parsed) != value:
        raise ValueError(f"{label} is not canonical")
    return value


def _sha(value: object, label: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        raise ValueError(f"{label} is invalid")
    return value


def _opaque(value: object, label: str) -> str:
    if not isinstance(value, str) or not _OPAQUE.fullmatch(value):
        raise ValueError(f"{label} is invalid")
    return value


def _instant(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not _UTC.fullmatch(value):
        raise ValueError(f"{label} must be canonical UTC RFC 3339")
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return parsed


def validate_relocation_authority(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _AUTHORITY_KEYS:
        raise ValueError("Relocation authority shape is invalid")
    result = cast(dict[str, Any], deepcopy(value))
    if result["schema_version"] != AUTHORITY_SCHEMA or result["operation"] != OPERATION:
        raise ValueError("Relocation authority contract is unsupported")
    for key in ("request_id", "api_run_id", "job_id", "checkpoint_id"):
        _uuid(result[key], key)
    _opaque(result["native_run_id"], "native_run_id")
    _opaque(result["checkpoint_contract"], "checkpoint_contract")
    _opaque(result["compatibility_identity"], "compatibility_identity")
    if result["terminal_result_id"] is not None:
        _opaque(result["terminal_result_id"], "terminal_result_id")
    generation = result["checkpoint_generation"]
    if not isinstance(generation, int) or isinstance(generation, bool) or generation < 1:
        raise ValueError("checkpoint_generation is invalid")
    for key in (
        "archive_sha256", "inventory_sha256", "original_logical_root_sha256",
        "restored_root_sha256", "authority_sha256",
    ):
        _sha(result[key], key)
    issued = _instant(result["issued_at"], "issued_at")
    expires = _instant(result["expires_at"], "expires_at")
    if issued >= expires:
        raise ValueError("Relocation authority window is invalid")
    if result["provider_io_permitted"] is not False or result["workspace_mutation_permitted"] is not False:
        raise ValueError("Relocation authority capabilities are invalid")
    unsigned = {key: item for key, item in result.items() if key != "authority_sha256"}
    if result["authority_sha256"] != _digest(unsigned):
        raise ValueError("Relocation authority digest is invalid")
    return result


def build_relocation_authority(**fields: Any) -> dict[str, Any]:
    body = {"schema_version": AUTHORITY_SCHEMA, "operation": OPERATION, **fields}
    body["authority_sha256"] = _digest(body)
    return validate_relocation_authority(body)


def validate_relocated_assessment(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _WRAPPER_KEYS:
        raise ValueError("Relocated assessment wrapper shape is invalid")
    result = cast(dict[str, Any], deepcopy(value))
    if result["schema_version"] != WRAPPER_SCHEMA or result["assessment_mode"] != ASSESSMENT_MODE:
        raise ValueError("Relocated assessment wrapper is unsupported")
    for key in ("request_id", "checkpoint_id"):
        _uuid(result[key], key)
    _opaque(result["native_run_id"], "native_run_id")
    generation = result["checkpoint_generation"]
    if not isinstance(generation, int) or isinstance(generation, bool) or generation < 1:
        raise ValueError("checkpoint_generation is invalid")
    for key in (
        "authority_sha256", "archive_sha256", "inventory_sha256",
        "original_logical_root_sha256", "restored_root_sha256", "wrapper_sha256",
    ):
        _sha(result[key], key)
    _instant(result["assessed_at"], "assessed_at")
    if result["provider_io_performed"] is not False or result["workspace_mutation_performed"] is not False:
        raise ValueError("Relocated assessment side-effect assertions are invalid")
    assessment = validate_operator_disposition_assessment(result["assessment"])
    if assessment["native_run_id"] != result["native_run_id"]:
        raise ValueError("Relocated assessment native identity changed")
    unsigned = {key: item for key, item in result.items() if key != "wrapper_sha256"}
    if result["wrapper_sha256"] != _digest(unsigned):
        raise ValueError("Relocated assessment wrapper digest is invalid")
    return result


def build_relocated_assessment(*, authority: Mapping[str, Any], assessed_at: str,
                               assessment: Mapping[str, Any]) -> dict[str, Any]:
    auth = validate_relocation_authority(dict(authority))
    nested = validate_operator_disposition_assessment(dict(assessment))
    assessed = _instant(assessed_at, "assessed_at")
    issued = _instant(auth["issued_at"], "issued_at")
    expires = _instant(auth["expires_at"], "expires_at")
    if not issued <= assessed <= expires:
        raise ValueError("Relocated assessment time is outside authority window")
    body = {
        "schema_version": WRAPPER_SCHEMA,
        "authority_sha256": auth["authority_sha256"],
        "request_id": auth["request_id"],
        "native_run_id": auth["native_run_id"],
        "checkpoint_id": auth["checkpoint_id"],
        "checkpoint_generation": auth["checkpoint_generation"],
        "archive_sha256": auth["archive_sha256"],
        "inventory_sha256": auth["inventory_sha256"],
        "original_logical_root_sha256": auth["original_logical_root_sha256"],
        "restored_root_sha256": auth["restored_root_sha256"],
        "assessment_mode": ASSESSMENT_MODE,
        "assessed_at": assessed_at,
        "provider_io_performed": False,
        "workspace_mutation_performed": False,
        "assessment": nested,
    }
    body["wrapper_sha256"] = _digest(body)
    return validate_relocated_assessment(body)


def validate_relocated_assessment_pair(
    authority: object, wrapper: object,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Re-establish exact authority/wrapper identity and freshness joins."""
    auth = validate_relocation_authority(authority)
    result = validate_relocated_assessment(wrapper)
    joined = {
        "authority_sha256", "request_id", "native_run_id", "checkpoint_id",
        "checkpoint_generation", "archive_sha256", "inventory_sha256",
        "original_logical_root_sha256", "restored_root_sha256",
    }
    if any(result[key] != auth[key] for key in joined):
        raise ValueError("Relocated assessment does not match its authority")
    assessed = _instant(result["assessed_at"], "assessed_at")
    if not _instant(auth["issued_at"], "issued_at") <= assessed <= _instant(
        auth["expires_at"], "expires_at"
    ):
        raise ValueError("Relocated assessment time is outside authority window")
    return auth, result


def validate_relocated_workspace_snapshot(
    run_dir: Path | str, state: Mapping[str, Any], authority: Mapping[str, Any],
) -> None:
    """Validate exact copied bytes while preserving the original logical root."""
    from .closure import (
        SNAPSHOT_NAME, SNAPSHOT_SCHEMA, load_json, normalized_path,
        snapshot_inventory,
    )

    auth = validate_relocation_authority(dict(authority))
    root = Path(run_dir).resolve()
    actual_root = normalized_path(root)
    contract = state.get("workspace_contract") or {}
    original_root = contract.get("logical_root")
    if contract.get("mode") != "stable_logical_absolute_path" or not isinstance(
        original_root, str
    ):
        raise ValueError("Run lacks the durable stable-path workspace contract")
    if canonical_logical_root(original_root) == canonical_logical_root(actual_root):
        raise ValueError("Relocated workspace must differ from its original root")
    if canonical_root_sha256(original_root) != auth["original_logical_root_sha256"]:
        raise ValueError("Original logical root does not match relocation authority")
    if canonical_root_sha256(actual_root) != auth["restored_root_sha256"]:
        raise ValueError("Restored root does not match relocation authority")
    manifest_path = root / SNAPSHOT_NAME
    if not manifest_path.is_file():
        raise ValueError("Relocated workspace snapshot is missing")
    manifest = load_json(manifest_path)
    if (
        manifest.get("schema_version") != SNAPSHOT_SCHEMA
        or manifest.get("logical_root") != original_root
    ):
        raise ValueError("Relocated snapshot does not preserve logical identity")
    expected = manifest.get("members")
    actual = snapshot_inventory(root, use_process_cache=False)
    if expected != actual:
        raise ValueError("Relocated workspace snapshot is incomplete or changed")


def read_relocated_operator_disposition_assessment(
    run_dir: Path | str, *, authority: Mapping[str, Any], assessed_at: str,
) -> dict[str, Any]:
    """Assess one API-isolated immutable checkpoint copy without native mutation."""
    from .closure import load_json
    from .operator_disposition import _read_operator_disposition_assessment

    auth = validate_relocation_authority(dict(authority))
    assessed = _instant(assessed_at, "assessed_at")
    if not _instant(auth["issued_at"], "issued_at") <= assessed <= _instant(
        auth["expires_at"], "expires_at"
    ):
        raise ValueError("Relocated assessment time is outside authority window")
    root = Path(run_dir).resolve()
    state = load_json(root / "run.json")
    if state.get("run_id") != auth["native_run_id"]:
        raise ValueError("Relocated workspace native identity does not match authority")

    def validator(candidate: Path, candidate_state: Mapping[str, Any]) -> None:
        validate_relocated_workspace_snapshot(candidate, candidate_state, auth)

    validator(root, state)
    assessment = _read_operator_disposition_assessment(
        root,
        terminal_result_id=auth["terminal_result_id"],
        allow_availability_recovery=False,
        workspace_validator=validator,
        native_exclusive_access="declared",
        require_exact_terminal_result=True,
    )
    # Revalidate authority freshness and copied bytes after all native reads.
    validate_relocation_authority(auth)
    if not _instant(auth["issued_at"], "issued_at") <= assessed <= _instant(
        auth["expires_at"], "expires_at"
    ):
        raise ValueError("Relocated assessment time is outside authority window")
    validator(root, load_json(root / "run.json"))
    return build_relocated_assessment(
        authority=auth, assessed_at=assessed_at, assessment=assessment,
    )


def read_relocation_authority_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "operator-disposition-relocation-authority.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def read_relocated_assessment_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "relocated-operator-disposition-assessment.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


__all__ = [
    "ASSESSMENT_MODE", "AUTHORITY_SCHEMA", "OPERATION", "WRAPPER_SCHEMA",
    "build_relocated_assessment", "build_relocation_authority",
    "canonical_logical_root", "canonical_root_sha256", "read_relocated_assessment_schema",
    "read_relocated_operator_disposition_assessment", "read_relocation_authority_schema",
    "validate_relocated_assessment", "validate_relocated_workspace_snapshot",
    "validate_relocated_assessment_pair", "validate_relocation_authority",
]
