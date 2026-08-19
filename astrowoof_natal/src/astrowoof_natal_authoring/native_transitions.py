"""Append-only native transition journal and immutable invocation results."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
import uuid
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, TypedDict

from .closure import (
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    snapshot_inventory,
    validate_workspace_snapshot,
    write_json_atomic,
)
from .lifecycle import _exclusive_lifecycle_lock
from .application_logging import bind_logging_context


logger = logging.getLogger(__name__)


JOURNAL_RECORD_SCHEMA = "astrowoof.native_transition_journal_record.v0.1"
EXECUTION_RESULT_SCHEMA = "astrowoof.native_execution_result.v0.1"
RESULT_INDEX_SCHEMA = "astrowoof.native_result_index.v0.1"
JOURNAL_NAME = "native-transition-journal.jsonl"
RESULT_DIRECTORY = "native-results"
RESULT_INDEX_NAME = "native-result-index.json"
RECEIPT_SCHEMA = "astrowoof.native_publication_receipt.v0.1"
RECEIPT_DIRECTORY = "native-publication-receipts"
MAX_RECORD_BYTES = 32 * 1024
MAX_RESULT_BYTES = 256 * 1024
MAX_EXPORT_RECORDS = 512


class NativeTransitionResultView(TypedDict):
    result: dict[str, Any]
    journal_range: dict[str, Any]
    receipt: dict[str, Any]

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
    "external_spend_reservation_unavailable", "external_product_policy_denied",
    "run_cancelled_before_submission", "ambiguous_provider_submission",
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


def _receipt_digest(receipt: dict[str, Any]) -> str:
    basis = {k: v for k, v in receipt.items() if k not in {"receipt_id", "receipt_sha256"}}
    return _digest(basis)


def mint_invocation_id() -> str:
    return f"ninv_{uuid.uuid4().hex[:24]}"


@contextmanager
def _journal_writer_lock(run_dir: Path):
    """Serialize journal publication without recursively taking the spend lock."""
    path = run_dir / "native-transition-journal.lock"
    with path.open("a+b") as handle:
        if path.stat().st_size == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


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
        action_binding = record["action_binding"]
        if action_binding is not None:
            _validate_action(action_binding)
        provider = record["provider_observation"]
        if provider is not None:
            if action_binding is None:
                raise ValueError("Provider observation requires action binding")
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
            if kind in {"identity_recorded", "pending", "completed", "failed", "cancelled", "expired", "usage_reported", "usage_unavailable", "identity_conflict_refused"} and not external_id:
                raise ValueError("Known provider observation requires external ID")
            disposition = provider["cost_disposition"]
            if disposition == "provider_usage_reported":
                if provider.get("estimated_micro_usd") is None or not provider.get("price_book_version") or not isinstance(provider.get("usage_evidence_ref"), dict):
                    raise ValueError("Reported usage requires amount, price book, and evidence")
            elif provider.get("estimated_micro_usd") is not None:
                raise ValueError("Unavailable/pending usage cannot fabricate an amount")
        previous = digest
    return records


def _append_transition_record_internal(run_dir: Path, value: dict[str, Any]) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    with _journal_writer_lock(run_dir):
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


def append_transition_record(run_dir: Path, value: dict[str, Any]) -> dict[str, Any]:
    """Append one record under the public native cross-process writer lock."""
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        return _append_transition_record_internal(run_dir, value)


def _route_binding(state: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    binding = action["binding"]
    bounded = (
        state.get("route_contract")
        in {
            "astrowoof.bounded_natal.authoring_run.v1",
            "astrowoof.bounded_natal.authoring_run.v2",
        }
        and state.get("route") in {"bounded_natal.v1", "bounded_natal.v2"}
    )
    exact = (
        state.get("schema_version") == "astrowoof.semantic_closure_run.v0.9"
        and state.get("route_contract") is None
    )
    if not bounded and not exact:
        raise ValueError("Paid action has no supported native transition route")
    mechanism = "batch" if binding.get("service_level") == "batch" else "response"
    return {
        "route_family": "bounded_natal" if bounded else "exact_natal",
        "provider_mechanism": mechanism,
        "native_operation_ref": str(binding["route"]),
    }


def _action_binding(action: dict[str, Any]) -> dict[str, Any]:
    binding = action["binding"]
    return {
        "action_id": action["action_id"], "stage": binding["stage"],
        "route": binding["route"], "request_sha256": binding["request_sha256"],
        "profile_sha256": binding["profile_sha256"],
        "maximum_output_tokens": binding["maximum_output_tokens"],
        "commitment_micro_usd": binding["commitment_micro_usd"],
        "price_book_version": binding["price_book_version"],
    }


def _provider_observation(
    action: dict[str, Any], observation_kind: str, *, status: str,
) -> dict[str, Any]:
    provider = action.get("provider") or {}
    reported = action.get("reported") or {}
    usage = reported.get("usage")
    amount = reported.get("estimated_micro_usd")
    if observation_kind == "submission_started":
        disposition, provider_id = "not_applicable_provider_pending", None
    elif observation_kind in {"identity_recorded", "pending", "identity_conflict_refused"}:
        disposition, provider_id = "not_applicable_provider_pending", provider.get("id")
    elif isinstance(usage, dict) and amount is not None:
        disposition, provider_id = "provider_usage_reported", provider.get("id")
    else:
        disposition = "provider_usage_unavailable_billing_reconciliation_pending"
        provider_id = provider.get("id")
    return {
        "observation_kind": observation_kind,
        "provider_kind": provider.get("kind") or (
            "batch" if action["binding"].get("service_level") == "batch" else "response"
        ),
        "provider_operation_id": provider_id, "status": status,
        "cost_disposition": disposition,
        "price_book_version": action["binding"]["price_book_version"] if disposition == "provider_usage_reported" else None,
        "usage_evidence_ref": (
            {"action_id": action["action_id"], "ledger_field": "reported.usage"}
            if disposition == "provider_usage_reported" else None
        ),
        "estimated_micro_usd": amount if disposition == "provider_usage_reported" else None,
    }


def _desired_action_records(
    state: dict[str, Any], action: dict[str, Any], observed_at: str,
) -> list[dict[str, Any]]:
    base = {
        "invocation_id": f"ninv_{action['action_id'][5:29]}",
        "observed_at": observed_at,
        "native_state_revision": int(state.get("state_revision") or 0),
        "route_binding": _route_binding(state, action),
        "action_binding": _action_binding(action), "native_transition": None,
    }
    desired = [{**base, "record_kind": "action.prepared", "provider_observation": None}]
    action_state = str(action.get("state") or "")
    if action.get("authorization") is not None or action_state in {
        "AUTHORIZED", "SUBMITTING", "PROVIDER_ID_RECORDED", "WAITING", "REPORTED",
        "AMBIGUOUS_PROVIDER_SUBMISSION",
    }:
        desired.append({**base, "record_kind": "action.authorized", "provider_observation": None})
    if action_state == "DENIED_PROVIDERLESS":
        denial = action.get("negative_authorization") or {}
        desired.append({
            **base, "record_kind": "action.denied_providerless",
            "provider_observation": None,
            "native_transition": {
                "denial_reason": denial.get("denial_reason"),
                "external_authority_reference": denial.get("external_authority_reference"),
                "run_transition": denial.get("run_transition"),
            },
        })
    if action.get("consumption") is not None:
        desired.extend([
            {**base, "record_kind": "action.consumed", "provider_observation": None},
            {**base, "record_kind": "provider.submission_started",
             "provider_observation": _provider_observation(action, "submission_started", status="submitting")},
        ])
    if (action.get("provider") or {}).get("id"):
        desired.append({
            **base, "record_kind": "provider.identity_recorded",
            "provider_observation": _provider_observation(action, "identity_recorded", status="identity_recorded"),
        })
    if action_state in {"PROVIDER_ID_RECORDED", "WAITING"}:
        desired.append({
            **base, "record_kind": "provider.pending",
            "provider_observation": _provider_observation(action, "pending", status="pending"),
        })
    if action_state == "AMBIGUOUS_PROVIDER_SUBMISSION":
        reason = str((action.get("ambiguity") or {}).get("reason") or "")
        if "identity" in reason.lower() and (action.get("provider") or {}).get("id"):
            desired.append({
                **base, "record_kind": "provider.identity_conflict_refused",
                "provider_observation": _provider_observation(action, "identity_conflict_refused", status="identity_conflict_refused"),
            })
        desired.append({
            **base, "record_kind": "provider.submission_ambiguous",
            "provider_observation": None,
            "native_transition": {"reason": reason or "provider submission outcome is ambiguous"},
        })
    if action_state == "REPORTED":
        provider_status = str((action.get("integrity_review") or {}).get("provider_status") or "completed")
        kind = provider_status if provider_status in {"failed", "cancelled", "expired"} else "completed"
        desired.append({
            **base, "record_kind": f"provider.{kind}",
            "provider_observation": _provider_observation(action, kind, status=provider_status),
        })
        usage_kind = "usage_reported" if (
            isinstance((action.get("reported") or {}).get("usage"), dict)
            and (action.get("reported") or {}).get("estimated_micro_usd") is not None
        ) else "usage_unavailable"
        desired.append({
            **base, "record_kind": f"provider.{usage_kind}",
            "provider_observation": _provider_observation(action, usage_kind, status=provider_status),
        })
    return desired


def sync_provider_transition_journal(run_dir: Path, state: dict[str, Any]) -> list[dict[str, Any]]:
    """Project durable paid-action state into append-only provider observations."""
    supported = (
        state.get("schema_version") == "astrowoof.semantic_closure_run.v0.9"
        or (
            state.get("route_contract")
            in {
                "astrowoof.bounded_natal.authoring_run.v1",
                "astrowoof.bounded_natal.authoring_run.v2",
            }
            and state.get("route") in {"bounded_natal.v1", "bounded_natal.v2"}
        )
    )
    if not supported:
        return []
    actions = (state.get("spend_ledger") or {}).get("actions")
    if not isinstance(actions, list):
        return []
    observed_at = str(state.get("updated_at") or "1970-01-01T00:00:00Z")
    appended: list[dict[str, Any]] = []
    for action in actions:
        existing = validate_transition_journal(run_dir)
        for candidate in _desired_action_records(state, action, observed_at):
            semantic = {
                key: candidate.get(key) for key in (
                    "record_kind", "route_binding", "action_binding",
                    "provider_observation", "native_transition",
                )
            }
            if any(all(record.get(key) == value for key, value in semantic.items()) for record in existing):
                continue
            record = _append_transition_record_internal(run_dir, candidate)
            existing.append(record)
            appended.append(record)
    return appended


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


def _write_immutable_execution_result_internal(run_dir: Path, result: dict[str, Any]) -> dict[str, Any]:
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


def write_immutable_execution_result(run_dir: Path, result: dict[str, Any]) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        return _write_immutable_execution_result_internal(run_dir, result)


def _native_route(state: dict[str, Any]) -> dict[str, Any]:
    bounded = state.get("route") in {"bounded_natal.v1", "bounded_natal.v2"}
    mechanism = "batch" if state.get("service_level") == "batch" else "response"
    return {
        "route_family": "bounded_natal" if bounded else "exact_natal",
        "provider_mechanism": mechanism,
        "native_operation_ref": str(state.get("route")) if bounded else "semantic_closure",
    }


def _outcome(state: dict[str, Any]) -> tuple[str, str]:
    status = str(state.get("status") or "")
    actions = (state.get("spend_ledger") or {}).get("actions") or []
    terminal = state.get("terminal_transition") or {}
    if terminal.get("outcome") == "terminalized":
        return str(terminal["terminal_outcome"]), str(terminal["terminal_reason"])
    if any((item.get("integrity_review") or {}).get("provider_status") for item in actions):
        return "terminal_failure", "provider_terminal_failure"
    if any(
        item.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION"
        and "identity" in str((item.get("ambiguity") or {}).get("reason") or "").lower()
        for item in actions
    ):
        return "ambiguous_submission", "provider_identity_conflict"
    terminal = state.get("terminal_transition") or {}
    if terminal.get("outcome") == "terminalized":
        return str(terminal["terminal_outcome"]), str(terminal["terminal_reason"])
    terminal = state.get("terminal_transition") or {}
    if terminal.get("outcome") == "terminalized":
        return str(terminal["terminal_outcome"]), str(terminal["terminal_reason"])
    if status == "DELIVERY_COMPLETE": return "delivery_complete", "delivery_complete"
    if status == "DELIVERY_COMPLETE_WITH_WARNINGS": return "delivery_complete", "delivery_complete_with_warnings"
    if status in {"FAILED_REQUIRES_REVIEW", "FINAL_QA_FAILED", "FINAL_QA_REQUIRES_REVIEW"}: return "review_required", "final_qa_requires_review"
    if status == "BUDGET_EXHAUSTED": return "budget_exhausted", "native_budget_ceiling_exhausted"
    if status == "POLICY_STOPPED": return "policy_stopped", "external_product_policy_denied"
    if status == "AMBIGUOUS_PROVIDER_SUBMISSION": return "ambiguous_submission", "ambiguous_provider_submission"
    if any(item.get("state") in {"PROVIDER_ID_RECORDED", "WAITING"} for item in actions): return "provider_pending", "provider_operation_pending"
    if any(item.get("state") == "PREPARED" for item in actions): return "awaiting_external_authority", "spend_authorization_required"
    return "continuation_required", "local_continuation_ready"


def _publish_receipt(
    run_dir: Path, result: dict[str, Any], *, snapshot_sha256: str,
    basis: dict[str, Any],
) -> dict[str, Any]:
    receipt_root = run_dir / RECEIPT_DIRECTORY
    snapshot_copy = receipt_root / f"{result['result_id']}.workspace-snapshot.json"
    basis_copy = receipt_root / f"{result['result_id']}.checkpoint-basis.json"
    snapshot_bytes = (run_dir / SNAPSHOT_NAME).read_bytes()
    if hashlib.sha256(snapshot_bytes).hexdigest() != snapshot_sha256:
        raise ValueError("Complete snapshot changed before publication receipt")
    if snapshot_copy.exists() and snapshot_copy.read_bytes() != snapshot_bytes:
        raise ValueError("Immutable retained snapshot identity conflict")
    snapshot_copy.parent.mkdir(parents=True, exist_ok=True)
    if not snapshot_copy.exists():
        with snapshot_copy.open("wb") as handle:
            handle.write(snapshot_bytes)
            handle.flush()
            os.fsync(handle.fileno())
    if basis.get("checkpoint_basis_sha256") != result["post_checkpoint"]["checkpoint_basis_sha256"]:
        raise ValueError("Publication checkpoint basis does not match result")
    if basis_copy.exists() and load_json(basis_copy) != basis:
        raise ValueError("Immutable retained checkpoint basis conflict")
    if not basis_copy.exists():
        write_json_atomic(basis_copy, basis)
    receipt = {
        "schema_version": RECEIPT_SCHEMA, "receipt_id": "", "receipt_sha256": "",
        "run_id": result["run_id"], "invocation_id": result["invocation_id"],
        "result_id": result["result_id"], "result_sha256": result["result_sha256"],
        "snapshot_sha256": snapshot_sha256,
        "checkpoint_basis_sha256": result["post_checkpoint"]["checkpoint_basis_sha256"],
        "journal_range_sha256": result["journal_range"]["range_sha256"],
        "logical_workspace_root": normalized_path(run_dir),
    }
    digest = _receipt_digest(receipt)
    receipt["receipt_sha256"] = digest
    receipt["receipt_id"] = f"nreceipt_{digest[:24]}"
    receipt_path = run_dir / RECEIPT_DIRECTORY / f"{result['result_id']}.json"
    if receipt_path.exists() and load_json(receipt_path) != receipt:
        raise ValueError("Immutable native publication receipt identity conflict")
    write_json_atomic(receipt_path, receipt)
    return receipt


def publish_native_execution_result(
    run_dir: Path, *, command_kind: str, sbe_release: str, published_at: str,
    event_emitter: Any = None,
) -> dict[str, Any]:
    """Seal current native meaning as result + full snapshot + immutable receipt."""
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        state = load_json(run_dir / "run.json")
        bind_logging_context(
            run_id=state.get("run_id"), current_state=state.get("status")
        )
        logger.info(
            "native_publication_start command_kind=%s state_revision=%s release=%s",
            command_kind, state.get("state_revision"), sbe_release,
        )
        records = validate_transition_journal(run_dir)
        prior_end = 0
        index_path = run_dir / RESULT_INDEX_NAME
        indexed_results: list[dict[str, Any]] = []
        if index_path.exists():
            for result_id in load_json(index_path).get("result_ids", []):
                prior = load_json(run_dir / RESULT_DIRECTORY / f"{result_id}.json")
                indexed_results.append(prior)
                prior_end = max(prior_end, int(prior["journal_range"]["end_sequence"]))
        incomplete = [
            item for item in indexed_results
            if not (run_dir / RECEIPT_DIRECTORY / f"{item['result_id']}.json").is_file()
        ]
        if incomplete:
            if len(incomplete) != 1 or incomplete[0] != indexed_results[-1]:
                raise ValueError("Native result publication history has multiple incomplete seals")
            orphan = incomplete[0]
            logger.warning(
                "native_publication_repair result_id=%s reason=incomplete_receipt",
                orphan.get("result_id"),
            )
            expected = orphan["journal_range"]
            observed = journal_range(run_dir, expected["start_sequence"], expected["end_sequence"])
            if expected["range_sha256"] != observed["range_sha256"]:
                raise ValueError("Incomplete native result journal range changed")
            basis = checkpoint_basis(
                run_dir, int(orphan["post_checkpoint"]["native_state_revision"])
            )
            if basis["checkpoint_basis_sha256"] != orphan["post_checkpoint"]["checkpoint_basis_sha256"]:
                raise ValueError("Incomplete native result checkpoint basis changed")
            from .closure import write_workspace_snapshot, sha256_file
            write_workspace_snapshot(run_dir)
            validate_workspace_snapshot(run_dir, state)
            receipt = _publish_receipt(
                run_dir, orphan, snapshot_sha256=sha256_file(run_dir / SNAPSHOT_NAME),
                basis=basis,
            )
            sealed = {"result": orphan, "receipt": receipt}
            if event_emitter is not None:
                event_emitter.emit("native.result_published", data={
                    "result_id": orphan["result_id"],
                    "receipt_id": receipt["receipt_id"], "outcome": orphan["outcome"],
                })
            logger.info(
                "native_publication_repaired result_id=%s receipt_id=%s outcome=%s",
                orphan["result_id"], receipt["receipt_id"], orphan["outcome"],
            )
            return sealed
        invocation_id = mint_invocation_id()
        bind_logging_context(invocation_id=invocation_id)
        logger.info(
            "native_invocation_started command_kind=%s state_revision=%s",
            command_kind, state.get("state_revision"),
        )
        route = _native_route(state)
        outcome, cause = _outcome(state)
        revision = int(state.get("state_revision") or 0)
        common = {
            "invocation_id": invocation_id, "observed_at": published_at,
            "native_state_revision": revision, "route_binding": route,
            "action_binding": None, "provider_observation": None,
        }
        for kind, transition in (
            ("invocation.started", None),
            ("native.transitioned", {"outcome": outcome, "cause_code": cause, "native_status": state.get("status")}),
            ("invocation.closed", {"outcome": outcome, "cause_code": cause}),
        ):
            _append_transition_record_internal(run_dir, {
                **common, "record_kind": kind, "native_transition": transition,
            })
        selected = journal_range(run_dir, prior_end + 1, len(validate_transition_journal(run_dir)))
        basis = checkpoint_basis(run_dir, revision)
        pre_snapshot = run_dir / SNAPSHOT_NAME
        result = _write_immutable_execution_result_internal(run_dir, {
            "invocation_id": invocation_id, "run_id": state["run_id"],
            "sbe_release": sbe_release, "published_at": published_at,
            "command_kind": command_kind, "route_binding": route,
            "pre_checkpoint": ({"snapshot_sha256": hashlib.sha256(pre_snapshot.read_bytes()).hexdigest()} if pre_snapshot.exists() else None),
            "post_checkpoint": {
                "native_state_revision": revision,
                "checkpoint_basis_sha256": basis["checkpoint_basis_sha256"],
                "logical_workspace_root": normalized_path(run_dir),
            },
            "journal_range": {
                key: selected[key] for key in ("start_sequence", "end_sequence", "record_count", "range_sha256")
            } | {"closing_record_id": selected["records"][-1]["record_id"]},
            "outcome": outcome, "cause_code": cause,
            "action_ids": [item["action_id"] for item in (state.get("spend_ledger") or {}).get("actions", [])],
            "provider_operations": [deepcopy(item.get("provider")) for item in (state.get("spend_ledger") or {}).get("actions", []) if item.get("provider")],
            "projection_refs": {},
        })
        from .closure import write_workspace_snapshot, sha256_file
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, state)
        snapshot_sha256 = sha256_file(run_dir / SNAPSHOT_NAME)
        receipt = _publish_receipt(
            run_dir, result, snapshot_sha256=snapshot_sha256, basis=basis,
        )
        sealed = {"result": result, "receipt": receipt}
        if event_emitter is not None:
            event_emitter.emit("native.result_published", data={
                "result_id": result["result_id"],
                "receipt_id": receipt["receipt_id"], "outcome": result["outcome"],
            })
        logger.info(
            "native_publication_complete invocation_id=%s result_id=%s "
            "receipt_id=%s outcome=%s journal_records=%s snapshot_sha256=%s",
            invocation_id, result["result_id"], receipt["receipt_id"],
            result["outcome"], selected["record_count"], snapshot_sha256,
        )
        return sealed


def read_native_transition_result(
    run_dir: Path, result_id: str,
) -> NativeTransitionResultView:
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
    receipt_path = run_dir / RECEIPT_DIRECTORY / f"{result_id}.json"
    if not receipt_path.is_file():
        raise ValueError("Native execution result has no immutable publication receipt")
    receipt = load_json(receipt_path)
    receipt_digest = _receipt_digest(receipt)
    if (
        receipt.get("schema_version") != RECEIPT_SCHEMA
        or receipt.get("receipt_sha256") != receipt_digest
        or receipt.get("receipt_id") != f"nreceipt_{receipt_digest[:24]}"
        or receipt.get("result_id") != result_id
        or receipt.get("result_sha256") != result["result_sha256"]
        or receipt.get("journal_range_sha256") != observed["range_sha256"]
        or receipt.get("logical_workspace_root") != normalized_path(run_dir)
    ):
        raise ValueError("Native publication receipt binding is invalid")
    retained_snapshot = (
        run_dir / RECEIPT_DIRECTORY / f"{result_id}.workspace-snapshot.json"
    )
    retained_basis = run_dir / RECEIPT_DIRECTORY / f"{result_id}.checkpoint-basis.json"
    if (
        not retained_snapshot.is_file() or not retained_basis.is_file()
        or hashlib.sha256(retained_snapshot.read_bytes()).hexdigest()
        != receipt.get("snapshot_sha256")
    ):
        raise ValueError("Native publication receipt retained evidence is invalid")
    basis = load_json(retained_basis)
    if basis.get("checkpoint_basis_sha256") != _digest({
        key: basis[key] for key in (
            "snapshot_schema", "logical_root", "native_state_revision", "members"
        )
    }):
        raise ValueError("Retained checkpoint basis identity is invalid")
    if (
        result["post_checkpoint"].get("checkpoint_basis_sha256") != basis["checkpoint_basis_sha256"]
        or receipt.get("checkpoint_basis_sha256") != basis["checkpoint_basis_sha256"]
    ):
        raise ValueError("Native execution result checkpoint basis is invalid")
    return {"result": result, "journal_range": observed, "receipt": receipt}


def latest_native_transition_result(run_dir: Path) -> NativeTransitionResultView:
    """Derived convenience only; consumers should persist and request explicit IDs."""
    index = load_json(run_dir.resolve() / RESULT_INDEX_NAME)
    result_ids = index.get("result_ids")
    if not isinstance(result_ids, list) or not result_ids:
        raise ValueError("Native result index contains no published result")
    return read_native_transition_result(run_dir, result_ids[-1])


__all__ = [
    "EXECUTION_RESULT_SCHEMA", "JOURNAL_RECORD_SCHEMA", "append_transition_record",
    "checkpoint_basis", "journal_range", "mint_invocation_id",
    "NativeTransitionResultView", "latest_native_transition_result",
    "publish_native_execution_result", "read_native_transition_result",
    "validate_transition_journal",
    "sync_provider_transition_journal", "write_immutable_execution_result",
]
