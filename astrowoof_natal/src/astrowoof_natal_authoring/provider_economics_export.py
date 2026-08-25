"""Snapshot-validating, provider-free provider-economics export."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import Any, Iterable, Mapping

from .closure import load_json, sha256_file, validate_workspace_snapshot
from .provider_economics import (
    project_bounded_provider_economics_revision,
    project_exact_provider_economics_revision,
    validate_provider_economics_revision,
    validate_provider_economics_revision_sequence,
)


EXPORT_SCHEMA_VERSION = "astrowoof.provider_economics_export.v1"
_EXPORT_KEYS = {
    "schema_version", "export_sha256", "native_run_id", "route_family",
    "snapshot_sha256", "observed_at", "revision_count", "revisions",
}
_HEX64 = set("0123456789abcdef")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _canonical_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("observed_at must be a nonempty UTC timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observed_at must include a UTC offset")
    normalized = parsed.astimezone(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")
    if normalized != value:
        raise ValueError("observed_at must use canonical UTC whole-second Z form")
    return normalized


def validate_provider_economics_export(value: Mapping[str, Any]) -> dict[str, Any]:
    export = dict(value)
    if set(export) != _EXPORT_KEYS:
        raise ValueError("provider economics export fields are not exact")
    if export.get("schema_version") != EXPORT_SCHEMA_VERSION:
        raise ValueError("unsupported provider economics export schema")
    if not isinstance(export.get("native_run_id"), str) or not export["native_run_id"]:
        raise ValueError("provider economics export run identity is invalid")
    if export.get("route_family") not in {"exact_natal", "bounded_natal"}:
        raise ValueError("provider economics export route is invalid")
    snapshot = export.get("snapshot_sha256")
    if (
        not isinstance(snapshot, str) or len(snapshot) != 64
        or any(char not in _HEX64 for char in snapshot)
    ):
        raise ValueError("provider economics export snapshot digest is invalid")
    _canonical_timestamp(export.get("observed_at"))
    revisions = export.get("revisions")
    if not isinstance(revisions, list):
        raise ValueError("provider economics export revisions must be an array")
    if export.get("revision_count") != len(revisions):
        raise ValueError("provider economics export revision count mismatch")
    validated = [validate_provider_economics_revision(item) for item in revisions]
    action_ids = [item["native_action_id"] for item in validated]
    if action_ids != sorted(action_ids) or len(action_ids) != len(set(action_ids)):
        raise ValueError("provider economics export revisions are not canonical")
    if any(item["native_run_id"] != export["native_run_id"] for item in validated):
        raise ValueError("provider economics export revision run mismatch")
    body = {key: item for key, item in export.items() if key != "export_sha256"}
    if export.get("export_sha256") != _digest(body):
        raise ValueError("provider economics export digest mismatch")
    return deepcopy(export)


def read_provider_economics_export_schema() -> dict[str, Any]:
    path = resources.files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "provider-economics-export.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _predecessors(
    revisions: Iterable[Mapping[str, Any]], *, run_id: str,
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for raw in revisions:
        value = validate_provider_economics_revision(raw)
        if value["native_run_id"] != run_id:
            raise ValueError("predecessor revision belongs to another native run")
        groups.setdefault(value["transaction_id"], []).append(value)
    latest: dict[str, dict[str, Any]] = {}
    for transaction_id, sequence in groups.items():
        sequence.sort(key=lambda item: item["revision_number"])
        accepted = validate_provider_economics_revision_sequence(sequence)
        latest[transaction_id] = accepted[-1]
    return latest


def read_provider_economics_export(
    run_dir: Path, *, observed_at: str,
    previous_revisions: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Return only newly durable revisions from one complete native snapshot."""
    root = run_dir.resolve()
    state = load_json(root / "run.json")
    validate_workspace_snapshot(root, state)
    run_id = state.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("native run identity is invalid")
    if state.get("schema_version") == "astrowoof.semantic_closure_run.v0.9" \
            and state.get("route_contract") is None:
        route = "exact_natal"
        projector = project_exact_provider_economics_revision
    elif state.get("route_contract") == "astrowoof.bounded_natal.authoring_run.v2":
        route = "bounded_natal"
        projector = project_bounded_provider_economics_revision
    else:
        raise ValueError("provider economics export requires exact v0.9 or bounded v2")
    observed = _canonical_timestamp(observed_at)
    prior = _predecessors(previous_revisions, run_id=run_id)
    revisions: list[dict[str, Any]] = []
    actions = (state.get("spend_ledger") or {}).get("actions")
    if not isinstance(actions, list):
        raise ValueError("native spend action inventory is unavailable")
    ordered = sorted(actions, key=lambda item: str((item or {}).get("action_id") or ""))
    if any(not isinstance(item, Mapping) for item in ordered):
        raise ValueError("native spend action inventory is malformed")
    for action in ordered:
        native_action_id = action.get("action_id")
        predecessor = next(
            (
                item for item in prior.values()
                if item["native_action_id"] == native_action_id
            ),
            None,
        )
        revision = projector(
            state, action, observed_at=observed, previous_revision=predecessor,
        )
        if revision is not None:
            revisions.append(revision)
    body = {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "native_run_id": run_id,
        "route_family": route,
        "snapshot_sha256": sha256_file(root / "workspace-snapshot.json"),
        "observed_at": observed,
        "revision_count": len(revisions),
        "revisions": revisions,
    }
    return validate_provider_economics_export({
        **body, "export_sha256": _digest(body),
    })
