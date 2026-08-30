"""Provider-free discovery of one exact sealed native transition result ID."""

from __future__ import annotations

import hashlib
import json
import re
from importlib.resources import files
from pathlib import Path
from typing import Any, TypedDict

from .closure import (
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    validate_workspace_snapshot,
)
from .native_transitions import (
    RECEIPT_DIRECTORY,
    RESULT_DIRECTORY,
    RESULT_INDEX_NAME,
    RESULT_INDEX_SCHEMA,
    read_native_transition_result,
)


AVAILABILITY_SCHEMA_VERSION = (
    "astrowoof.native_transition_result_availability.v1"
)
AVAILABILITY_OUTCOMES = {"none_available", "available"}
MAX_RESULT_IDS = 512
_RESULT_ID = re.compile(r"^nres_[0-9a-f]{24}$")


class NativeTransitionAvailabilityError(ValueError):
    """Typed fail-closed error for invalid result-discovery evidence."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


class NativeTransitionAvailabilityView(TypedDict):
    schema_version: str
    native_run_id: str
    logical_workspace_root: str
    workspace_snapshot_sha256: str
    availability: str
    result_count: int
    latest_result_id: str | None
    result_index_sha256: str | None
    availability_document_sha256: str


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: dict[str, Any]) -> str:
    basis = {
        key: item
        for key, item in value.items()
        if key != "availability_document_sha256"
    }
    return hashlib.sha256(_canonical(basis)).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_native_transition_result_availability(
    value: object,
) -> NativeTransitionAvailabilityView:
    required = {
        "schema_version", "native_run_id", "logical_workspace_root",
        "workspace_snapshot_sha256", "availability", "result_count",
        "latest_result_id", "result_index_sha256",
        "availability_document_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise NativeTransitionAvailabilityError(
            "availability_shape_invalid",
            "Native transition availability fields are invalid",
        )
    if value.get("schema_version") != AVAILABILITY_SCHEMA_VERSION:
        raise NativeTransitionAvailabilityError(
            "availability_schema_unsupported",
            "Native transition availability schema is unsupported",
        )
    for name in ("native_run_id", "logical_workspace_root"):
        item = value.get(name)
        if not isinstance(item, str) or not item:
            raise NativeTransitionAvailabilityError(
                "availability_identity_invalid",
                f"Native transition availability {name} is invalid",
            )
    for name in (
        "workspace_snapshot_sha256", "availability_document_sha256",
    ):
        item = value.get(name)
        if not isinstance(item, str) or not re.fullmatch(r"[0-9a-f]{64}", item):
            raise NativeTransitionAvailabilityError(
                "availability_digest_invalid",
                f"Native transition availability {name} is invalid",
            )
    index_sha = value.get("result_index_sha256")
    if index_sha is not None and (
        not isinstance(index_sha, str)
        or not re.fullmatch(r"[0-9a-f]{64}", index_sha)
    ):
        raise NativeTransitionAvailabilityError(
            "availability_digest_invalid",
            "Native transition result-index digest is invalid",
        )
    availability = value.get("availability")
    count = value.get("result_count")
    latest = value.get("latest_result_id")
    if availability not in AVAILABILITY_OUTCOMES:
        raise NativeTransitionAvailabilityError(
            "availability_outcome_invalid",
            "Native transition availability outcome is invalid",
        )
    if (
        not isinstance(count, int) or isinstance(count, bool)
        or count < 0 or count > MAX_RESULT_IDS
    ):
        raise NativeTransitionAvailabilityError(
            "availability_count_invalid",
            "Native transition result count is invalid",
        )
    if availability == "none_available":
        if count != 0 or latest is not None:
            raise NativeTransitionAvailabilityError(
                "availability_semantics_invalid",
                "No-result availability contains a result identity",
            )
    elif (
        count < 1 or not isinstance(latest, str)
        or _RESULT_ID.fullmatch(latest) is None or index_sha is None
    ):
        raise NativeTransitionAvailabilityError(
            "availability_semantics_invalid",
            "Available result discovery is incomplete",
        )
    if value.get("availability_document_sha256") != _digest(value):
        raise NativeTransitionAvailabilityError(
            "availability_digest_invalid",
            "Native transition availability document digest is invalid",
        )
    return value  # type: ignore[return-value]


def _publication_files(run_dir: Path) -> tuple[set[str], set[str]]:
    results = run_dir / RESULT_DIRECTORY
    receipts = run_dir / RECEIPT_DIRECTORY
    return (
        {item.name for item in results.iterdir() if item.is_file()}
        if results.is_dir() else set(),
        {item.name for item in receipts.iterdir() if item.is_file()}
        if receipts.is_dir() else set(),
    )


def read_native_transition_result_availability(
    run_dir: Path,
) -> NativeTransitionAvailabilityView:
    """Discover one exact sealed result ID without granting transition authority."""
    run_dir = run_dir.resolve()
    try:
        state = load_json(run_dir / "run.json")
        validate_workspace_snapshot(run_dir, state)
        run_id = state.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("Native run identity is invalid")
        snapshot_sha = _sha256_file(run_dir / SNAPSHOT_NAME)
        index_path = run_dir / RESULT_INDEX_NAME
        result_files, receipt_files = _publication_files(run_dir)
        index_sha: str | None = None
        if not index_path.exists():
            if result_files or receipt_files:
                raise ValueError("Native result publication artifacts have no index")
            result_ids: list[str] = []
        else:
            index = load_json(index_path)
            if not isinstance(index, dict) or set(index) != {
                "schema_version", "result_ids",
            } or index.get("schema_version") != RESULT_INDEX_SCHEMA:
                raise ValueError("Native result index shape/schema is invalid")
            raw_ids = index.get("result_ids")
            if not isinstance(raw_ids, list) or len(raw_ids) > MAX_RESULT_IDS:
                raise ValueError("Native result index inventory is invalid")
            if any(
                not isinstance(item, str) or _RESULT_ID.fullmatch(item) is None
                for item in raw_ids
            ) or len(raw_ids) != len(set(raw_ids)):
                raise ValueError("Native result index identities are invalid")
            result_ids = list(raw_ids)
            index_sha = _sha256_file(index_path)

        expected_results = {f"{result_id}.json" for result_id in result_ids}
        expected_receipts = {
            name
            for result_id in result_ids
            for name in (
                f"{result_id}.json",
                f"{result_id}.workspace-snapshot.json",
                f"{result_id}.checkpoint-basis.json",
            )
        }
        if result_files != expected_results or receipt_files != expected_receipts:
            raise ValueError("Native result publication inventory is unjoinable")
        for result_id in result_ids:
            read_native_transition_result(run_dir, result_id)

        value: dict[str, Any] = {
            "schema_version": AVAILABILITY_SCHEMA_VERSION,
            "native_run_id": run_id,
            "logical_workspace_root": normalized_path(run_dir),
            "workspace_snapshot_sha256": snapshot_sha,
            "availability": "available" if result_ids else "none_available",
            "result_count": len(result_ids),
            "latest_result_id": result_ids[-1] if result_ids else None,
            "result_index_sha256": index_sha,
        }
        value["availability_document_sha256"] = _digest(value)
        return validate_native_transition_result_availability(value)
    except NativeTransitionAvailabilityError:
        raise
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise NativeTransitionAvailabilityError(
            "availability_evidence_invalid",
            "Native transition result availability evidence is invalid",
        ) from error


def read_native_transition_result_availability_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring").joinpath(
        "resources/contracts/native-transition-result-availability.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "AVAILABILITY_SCHEMA_VERSION", "NativeTransitionAvailabilityError",
    "NativeTransitionAvailabilityView",
    "read_native_transition_result_availability",
    "read_native_transition_result_availability_schema",
    "validate_native_transition_result_availability",
]
