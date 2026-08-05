"""Deterministic provenance capture for authoring runs and deliveries."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any


PROVENANCE_SCHEMA = "astrowoof.natal_authoring_provenance.v0.1"
RESOURCE_SET_SCHEMA = "astrowoof.natal_authoring_resource_set.v0.1"
DECLARED_METADATA_FIELDS = (
    "package_type", "projection_id", "engine_version", "profile_id",
    "profile_version", "context_id", "context_version",
    "projected_term_registry_id", "projected_term_registry_version",
    "materialization_mode",
)
DECLARED_SOURCE_REF_FIELDS = ("graph_type", "graph_version", "source_graph_hash")
DECLARED_IDENTITY_FIELDS = ("source_chart_id", "source_chart_ids", "sensor_instance_id")
DECLARED_AUDIT_FIELDS = (
    "request_hash", "source_graph_hash", "context_hash", "mapping_execution_count",
    "unmapped_source_count", "fallback_count",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_descriptor(path: Path, *, role: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    if role:
        result["role"] = role
    return result


def _distribution_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def runtime_provenance() -> dict[str, Any]:
    return {
        "distribution": "astrowoof-natal-authoring",
        "version": _distribution_version(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": sys.platform,
    }


def _resource_files() -> list[Any]:
    root = files("astrowoof_natal_authoring").joinpath("resources")
    found: list[Any] = []
    stack = [(root, "")]
    while stack:
        directory, prefix = stack.pop()
        for item in directory.iterdir():
            relative = f"{prefix}{item.name}"
            if item.is_dir():
                stack.append((item, f"{relative}/"))
            elif not relative.endswith((".pyc",)) and "__pycache__" not in relative:
                found.append((relative, item))
    return sorted(found, key=lambda pair: pair[0])


def resource_set_provenance() -> dict[str, Any]:
    records = []
    aggregate = hashlib.sha256()
    for relative, item in _resource_files():
        payload = item.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        records.append({"path": relative, "bytes": len(payload), "sha256": digest})
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {
        "schema_version": RESOURCE_SET_SCHEMA,
        "aggregate_sha256": aggregate.hexdigest(),
        "resource_count": len(records),
        "resources": records,
    }


def _selected(source: Any, names: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(source, dict):
        return {}
    return {name: source[name] for name in names if name in source}


def projected_input_provenance(
    input_root: Path,
    normalized_contract: dict[str, Any],
) -> dict[str, Any]:
    subjects = []
    for subject in normalized_contract.get("subjects", []):
        contexts = []
        for context, relative in sorted(subject.get("contexts", {}).items()):
            path = (input_root / relative).resolve()
            graph = json.loads(path.read_text(encoding="utf-8"))
            contexts.append({
                "context": context,
                "artifact": artifact_descriptor(path),
                "declared": {
                    "metadata": _selected(graph.get("metadata"), DECLARED_METADATA_FIELDS),
                    "source_identity": _selected(graph.get("source_identity"), DECLARED_IDENTITY_FIELDS),
                    "source_graph_ref": _selected(graph.get("source_graph_ref"), DECLARED_SOURCE_REF_FIELDS),
                    "target_ontology": graph.get("target_ontology"),
                    "audit": _selected(graph.get("audit"), DECLARED_AUDIT_FIELDS),
                },
            })
        params_relative = subject.get("params")
        params = (
            artifact_descriptor((input_root / params_relative).resolve())
            if params_relative else None
        )
        subjects.append({
            "subject_id": subject.get("subject_id"),
            "contexts": contexts,
            "params_artifact": params,
        })
    return {
        "contract_schema": normalized_contract.get("schema_version"),
        "source_format": normalized_contract.get("source_format"),
        "subjects": subjects,
    }


def initial_provenance(
    *,
    input_root: Path,
    input_contract: dict[str, Any],
    authoring_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "schema_version": PROVENANCE_SCHEMA,
        "runtime": runtime_provenance(),
        "resources": resource_set_provenance(),
        "input": projected_input_provenance(input_root, input_contract),
        "authoring_profile": authoring_profile,
        "execution": {},
    }


def migrated_run_provenance(
    *,
    previous_schema: str,
    authoring_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    """Describe exactly what can and cannot be recovered for an old run."""
    return {
        "schema_version": PROVENANCE_SCHEMA,
        "runtime": runtime_provenance(),
        "resources": resource_set_provenance(),
        "input": {
            "status": "unavailable_from_legacy_run",
            "reason": "normalized input hashes were not captured at creation",
        },
        "authoring_profile": authoring_profile,
        "migration": {"from_run_schema": previous_schema},
        "execution": {},
    }


def refresh_execution_provenance(state: dict[str, Any]) -> None:
    accounting = state.get("accounting", {})
    provider_records: list[dict[str, Any]] = []
    for record in state.get("passes", {}).values():
        provider_records.extend(
            attempt.get("provider_metadata") or {}
            for attempt in record.get("attempts", [])
        )
    for record in state.get("subjects", {}).values():
        provider_records.extend(
            attempt.get("provider_metadata") or {}
            for attempt in record.get("polish_attempts", [])
        )
        review = record.get("qualitative_review") or {}
        for item in (review.get("critic"), review.get("candidate")):
            if isinstance(item, dict) and item.get("provider_metadata"):
                provider_records.append(item["provider_metadata"])
    actual_models = sorted({
        str(item["model"])
        for item in provider_records
        if item.get("model")
    })
    requested_models = sorted({
        str(item.get("requested_model") or item["model"])
        for item in provider_records
        if item.get("requested_model") or item.get("model")
    })
    response_ids = sorted({
        str(item["response_id"])
        for item in provider_records
        if item.get("response_id")
    })
    subjects = {}
    for subject, record in sorted(state.get("subjects", {}).items()):
        reports = {}
        for role, key in (("validation", "validation_report"), ("lint", "lint_report")):
            path_value = record.get(key)
            if path_value and Path(path_value).is_file():
                report = json.loads(Path(path_value).read_text(encoding="utf-8"))
                reports[role] = {
                    "schema_version": report.get("schema_version"),
                    "status": report.get("status"),
                    "artifact": artifact_descriptor(Path(path_value), role=role),
                }
        subjects[subject] = {
            "status": record.get("state"),
            "qa_reports": reports,
            "delivery": (
                artifact_descriptor(Path(record["delivery"]), role="delivery_zip")
                if record.get("delivery") and Path(record["delivery"]).is_file()
                else None
            ),
        }
    state.setdefault("provenance", {})["execution"] = {
        "provider": state.get("provider"),
        "service_level": state.get("service_level"),
        "requested_models": requested_models,
        "observed_models": actual_models,
        "response_ids": response_ids,
        "attempt_count": accounting.get("attempt_count", 0),
        "subjects": subjects,
    }
