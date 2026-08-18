"""Append-only native transition journal and immutable invocation results."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from copy import deepcopy
from pathlib import Path
from typing import Any

from .closure import (
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    snapshot_inventory,
    validate_workspace_snapshot,
    write_json_atomic,
)
from .lifecycle import _exclusive_lifecycle_lock


JOURNAL_RECORD_SCHEMA = "astrowoof.native_transition_journal_record.v0.1"
EXECUTION_RESULT_SCHEMA = "astrowoof.native_execution_result.v0.1"
RESULT_INDEX_SCHEMA = "astrowoof.native_result_index.v0.1"
JOURNAL_NAME = "native-transition-journal.jsonl"
RESULT_DIRECTORY = "native-results"
RESULT_INDEX_NAME = "native-result-index.json"
MAX_RECORD_BYTES = 32 * 1024
MAX_RESULT_BYTES = 256 * 1024
MAX_EXPORT_RECORDS = 512

RECORD_KINDS = {
    "invocation.started", "action.prepared", "action.authorized",
    "action.consumed", "action.denied_providerless",
    "provider.submission_started", "provider.identity_recorded",
    "provider.pending", "provider.completed", "provider.failed",
    "provider.cancelled", "provider.expired", "provider.usage_reported",
    "provider.usage_unavailable", "provider.submission_ambiguous",
    "provider.identity_conflict_refused", "native.transitioned",
    "invocation.closed",
}
OUTCOMES = {
    "delivery_complete", "review_required", "terminal_failure",
    "provider_pending", "continuation_required",
    "awaiting_external_authority", "budget_exhausted", "policy_stopped",
    "ambiguous_submission", "native_evidence_invalid",
}
CAUSE_CODES = {
    "delivery_complete", "delivery_complete_with_warnings",
    "final_qa_requires_review", "authoring_attempts_exhausted",
    "provider_terminal_failure", "provider_output_invalid",
    "provider_identity_conflict", "provider_operation_pending",
    "local_continuation_ready", "spend_authorization_required",
    "external_spend_authority_denied", "native_budget_ceiling_exhausted",
    "external_product_policy_denied", "ambiguous_provider_submission",
    "snapshot_or_journal_invalid", "unsupported_route_or_legacy_evidence",
}
COST_DISPOSITIONS = {
    "provider_usage_reported",
    "provider_usage_unavailable_billing_reconciliation_pending",
    "no_provider_work_consumed", "not_applicable_provider_pending",
}
PUBLICATION_PREFIXES = (f"{RESULT_DIRECTORY}/",)
PUBLICATION_NAMES = {RESULT_INDEX_NAME}


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _record_digest(record: dict[str, Any]) -> str:
    basis = {k: v for k, v in record.items() if k not in {"record_id", "record_sha256"}}
    return _digest(basis)


def _result_digest(result: dict[str, Any]) -> str:
    basis = {k: v for k, v in result.items() if k not in {"result_id", "result_sha256"}}
    return _digest(basis)


def mint_invocation_id() -> str:
    return f"ninv_{uuid.uuid4().hex[:24]}"


def _validate_route(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {
        "route_family", "provider_mechanism", "native_operation_ref",
    }:
        raise ValueError("Native route binding fields are invalid")
    if value["route_family"] not in {"exact_natal", "bounded_natal"}:
        raise ValueError("Unknown native route family")
    if value["provider_mechanism"] not in {"response", "batch"}:
        raise ValueError("Unknown provider mechanism")
    if not isinstance(value["native_operation_ref"], str) or not value["native_operation_ref"]:
        raise ValueError("Native operation reference is required")


def _validate_action(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {
        "action_id", "stage", "route", "request_sha256", "profile_sha256",
        "maximum_output_tokens", "commitment_micro_usd", "price_book_version",
    }:
        raise ValueError("Native action binding fields are invalid")
    if value["stage"] not in {"authoring_initial", "creative_retry", "polish", "qualitative_critic", "qualitative_candidate"}:
        raise ValueError("Unknown native action stage")
    for name in ("request_sha256", "profile_sha256"):
        if not isinstance(value[name], str) or len(value[name]) != 64:
            raise ValueError("Native action digest is invalid")


def _read_journal(run_dir: Path) -> list[dict[str, Any]]:
    path = run_dir / JOURNAL_NAME
    if not path.exists():
        return []
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"Native transition journal has blank line {number}")
        if len(line.encode("utf-8")) > MAX_RECORD_BYTES:
            raise ValueError(f"Native transition record {number} exceeds size bound")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"Native transition record {number} is not an object")
        records.append(value)
    return records


def validate_transition_journal(run_dir: Path) -> list[dict[str, Any]]:
    records = _read_journal(run_dir)
    previous = None
    run_id = None
    for sequence, record in enumerate(records, 1):
        if set(record) != {
            "schema_version", "record_id", "record_sha256", "run_id",
            "invocation_id", "sequence", "previous_record_sha256",
            "observed_at", "native_state_revision", "record_kind",
            "route_binding", "action_binding", "provider_observation",
            "native_transition",
        }:
            raise ValueError(f"Native transition record {sequence} has invalid fields")
        if record["schema_version"] != JOURNAL_RECORD_SCHEMA:
            raise ValueError("Unsupported native transition journal schema")
        if record["sequence"] != sequence or record["previous_record_sha256"] != previous:
            raise ValueError("Native transition journal sequence/hash chain is invalid")
        digest = _record_digest(record)
        if record["record_sha256"] != digest or record["record_id"] != f"ntr_{digest[:24]}":
            raise ValueError("Native transition record identity is invalid")
        if record["record_kind"] not in RECORD_KINDS:
            raise ValueError("Unknown native transition record kind")
        _validate_route(record["route_binding"])
        if run_id is None:
            run_id = record["run_id"]
        elif record["run_id"] != run_id:
            raise ValueError("Native transition journal crosses run identity")
        provider = record["provider_observation"]
        if provider is not None:
            _validate_action(record["action_binding"])
            if set(provider) != {
                "observation_kind", "provider_kind", "provider_operation_id",
                "status", "cost_disposition", "price_book_version",
                "usage_evidence_ref", "estimated_micro_usd",
            }:
                raise ValueError("Provider observation fields are invalid")
            if provider.get("cost_disposition") not in COST_DISPOSITIONS:
                raise ValueError("Unknown provider cost disposition")
            kind = provider.get("observation_kind")
            external_id = provider.get("provider_operation_id")
            if kind == "submission_started" and external_id is not None:
                raise ValueError("Provider ID cannot exist before identity recording")
            if kind in {"identity_recorded", "pending", "completed", "failed", "cancelled", "expired", "usage_reported", "usage_unavailable"} and not external_id:
                raise ValueError("Known provider observation requires external ID")
            disposition = provider["cost_disposition"]
            if disposition == "provider_usage_reported":
                if provider.get("estimated_micro_usd") is None or not provider.get("price_book_version") or not isinstance(provider.get("usage_evidence_ref"), dict):
                    raise ValueError("Reported usage requires amount, price book, and evidence")
            elif provider.get("estimated_micro_usd") is not None:
                raise ValueError("Unavailable/pending usage cannot fabricate an amount")
        previous = digest
    return records


def append_transition_record(run_dir: Path, value: dict[str, Any]) -> dict[str, Any]:
    """Append one record under the native cross-process writer lock."""
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        records = validate_transition_journal(run_dir)
        state = load_json(run_dir / "run.json")
        replay_basis = {
            key: deepcopy(value.get(key)) for key in (
                "invocation_id", "observed_at", "native_state_revision",
                "record_kind", "route_binding", "action_binding",
                "provider_observation", "native_transition",
            )
        }
        for existing in records:
            if all(existing[key] == replay_basis[key] for key in replay_basis):
                return deepcopy(existing)
        sequence = len(records) + 1
        record = {
            "schema_version": JOURNAL_RECORD_SCHEMA,
            "record_id": "",
            "record_sha256": "",
            "run_id": state["run_id"],
            "invocation_id": value["invocation_id"],
            "sequence": sequence,
            "previous_record_sha256": records[-1]["record_sha256"] if records else None,
            "observed_at": value["observed_at"],
            "native_state_revision": int(value["native_state_revision"]),
            "record_kind": value["record_kind"],
            "route_binding": deepcopy(value["route_binding"]),
            "action_binding": deepcopy(value.get("action_binding")),
            "provider_observation": deepcopy(value.get("provider_observation")),
            "native_transition": deepcopy(value.get("native_transition")),
        }
        digest = _record_digest(record)
        record["record_sha256"] = digest
        record["record_id"] = f"ntr_{digest[:24]}"
        rendered = b"".join(_canonical(item) + b"\n" for item in [*records, record])
        if len(_canonical(record)) > MAX_RECORD_BYTES:
            raise ValueError("Native transition record exceeds size bound")
        path = run_dir / JOURNAL_NAME
        with tempfile.NamedTemporaryFile("wb", dir=run_dir, prefix=f".{JOURNAL_NAME}.", suffix=".tmp", delete=False) as handle:
            staged = Path(handle.name)
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        staged.replace(path)
        validate_transition_journal(run_dir)
        return deepcopy(record)


def journal_range(run_dir: Path, start: int, end: int) -> dict[str, Any]:
    records = validate_transition_journal(run_dir)
    if start < 1 or end < start or end > len(records) or end - start + 1 > MAX_EXPORT_RECORDS:
        raise ValueError("Requested native journal range is invalid or unbounded")
    selected = records[start - 1:end]
    return {
        "start_sequence": start, "end_sequence": end,
        "record_count": len(selected),
        "range_sha256": _digest([item["record_sha256"] for item in selected]),
        "records": deepcopy(selected),
    }


def checkpoint_basis(run_dir: Path, state_revision: int) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    members = [
        item for item in snapshot_inventory(run_dir, use_process_cache=False)
        if item["path"] != SNAPSHOT_NAME
        and item["path"] not in PUBLICATION_NAMES
        and not item["path"].startswith(PUBLICATION_PREFIXES)
    ]
    basis = {
        "snapshot_schema": "astrowoof.semantic_closure_snapshot.v0.1",
        "logical_root": normalized_path(run_dir),
        "native_state_revision": int(state_revision),
        "members": members,
    }
    return {"checkpoint_basis_sha256": _digest(basis), **basis}


def write_immutable_execution_result(run_dir: Path, result: dict[str, Any]) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    value = deepcopy(result)
    value["schema_version"] = EXECUTION_RESULT_SCHEMA
    value.pop("result_id", None)
    value.pop("result_sha256", None)
    required = {
        "schema_version", "invocation_id", "run_id", "sbe_release",
        "published_at", "command_kind", "route_binding", "pre_checkpoint",
        "post_checkpoint", "journal_range", "outcome", "cause_code",
        "action_ids", "provider_operations", "projection_refs",
    }
    if (
        set(value) != required
        or value.get("outcome") not in OUTCOMES
        or value.get("cause_code") not in CAUSE_CODES
    ):
        raise ValueError("Native execution result fields/outcome are invalid")
    _validate_route(value["route_binding"])
    digest = _result_digest(value)
    value["result_sha256"] = digest
    value["result_id"] = f"nres_{digest[:24]}"
    if len(_canonical(value)) > MAX_RESULT_BYTES:
        raise ValueError("Native execution result exceeds size bound")
    with _exclusive_lifecycle_lock(run_dir):
        path = run_dir / RESULT_DIRECTORY / f"{value['result_id']}.json"
        if path.exists():
            existing = load_json(path)
            if existing != value:
                raise ValueError("Immutable native execution result identity conflict")
        else:
            write_json_atomic(path, value)
        index_path = run_dir / RESULT_INDEX_NAME
        index = load_json(index_path) if index_path.exists() else {
            "schema_version": RESULT_INDEX_SCHEMA, "result_ids": [],
        }
        if value["result_id"] not in index["result_ids"]:
            index["result_ids"].append(value["result_id"])
        write_json_atomic(index_path, index)
    return value


def read_native_transition_result(run_dir: Path, result_id: str) -> dict[str, Any]:
    """Return one immutable result and only its validated bounded journal range."""
    if not result_id.startswith("nres_") or len(result_id) != 29:
        raise ValueError("Invalid native execution result ID")
    run_dir = run_dir.resolve()
    path = run_dir / RESULT_DIRECTORY / f"{result_id}.json"
    result = load_json(path)
    if result.get("schema_version") != EXECUTION_RESULT_SCHEMA:
        raise ValueError("Unsupported native execution result schema")
    digest = _result_digest(result)
    if result.get("result_sha256") != digest or result.get("result_id") != f"nres_{digest[:24]}":
        raise ValueError("Native execution result identity is invalid")
    if result.get("outcome") not in OUTCOMES:
        raise ValueError("Unknown native execution outcome")
    expected = result["journal_range"]
    observed = journal_range(run_dir, expected["start_sequence"], expected["end_sequence"])
    for key in ("start_sequence", "end_sequence", "record_count", "range_sha256"):
        if expected[key] != observed[key]:
            raise ValueError("Native execution result journal binding is invalid")
    state = load_json(run_dir / "run.json")
    validate_workspace_snapshot(run_dir, state)
    basis = checkpoint_basis(run_dir, int(result["post_checkpoint"]["native_state_revision"]))
    if result["post_checkpoint"].get("checkpoint_basis_sha256") != basis["checkpoint_basis_sha256"]:
        raise ValueError("Native execution result checkpoint basis is invalid")
    return {"result": result, "journal_range": observed}


__all__ = [
    "EXECUTION_RESULT_SCHEMA", "JOURNAL_RECORD_SCHEMA", "append_transition_record",
    "checkpoint_basis", "journal_range", "mint_invocation_id",
    "read_native_transition_result", "validate_transition_journal",
    "write_immutable_execution_result",
]
