"""Closed provider-free operator-disposition assessment contract."""

from __future__ import annotations

import hashlib
import json
import os
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "astrowoof.operator_disposition_assessment.v1"

CUSTODY_CLASSES = frozenset({
    "provider_free_quiescent",
    "provider_pending_known_identity",
    "completed_unadopted",
    "native_local_work_ready",
    "providerless_authority",
    "submission_ambiguous",
    "sealed_terminal",
    "unsupported_or_inconsistent",
})
QUARANTINE_POSTURES = frozenset({
    "permitted", "prohibited", "native_prior_action_required",
})
NEXT_ACTIONS = frozenset({
    "provider_reconciliation_cycle", "ordinary_resume",
    "external_authority_v1", "external_authority_v2",
    "providerless_denial", "terminal_result_ingress",
    "operator_retirement_assessment", "operator_review",
    "fresh_disposition_assessment",
})
SUPPORTED_LIFECYCLE_SCHEMAS = frozenset({
    "astrowoof.authoring_lifecycle_inspection.v0.5",
    "astrowoof.authoring_lifecycle_inspection.v0.6",
    "astrowoof.authoring_lifecycle_inspection.v0.7",
    "astrowoof.authoring_lifecycle_inspection.v0.8",
})
EVIDENCE_CATEGORIES = frozenset({
    "contradictory_evidence",
    "external_authority_unjoinable",
    "identity_join_failed",
    "local_work_inventory_unavailable",
    "provider_custody_unjoinable",
    "retry_lineage_conflict",
    "snapshot_invalid",
    "terminal_evidence_unjoinable",
    "unknown_lifecycle_schema",
    "unsupported_provider_mechanism",
    "unsupported_route",
    "writer_exclusivity_unestablished",
})
REASON_CODES = {
    "provider_free_quiescent": "provider_free_quiescent",
    "provider_pending_known_identity": "known_provider_operation_pending",
    "completed_unadopted": "completed_provider_evidence_requires_adoption",
    "native_local_work_ready": "native_local_work_ready",
    "providerless_authority": "providerless_authority_requires_named_action",
    "submission_ambiguous": "provider_submission_ambiguous",
    "sealed_terminal": "sealed_terminal_result_available",
    "unsupported_or_inconsistent": "unsupported_or_inconsistent_evidence",
}
POSTURES = {
    "provider_free_quiescent": "permitted",
    "provider_pending_known_identity": "permitted",
    "completed_unadopted": "native_prior_action_required",
    "native_local_work_ready": "native_prior_action_required",
    "providerless_authority": "permitted",
    "submission_ambiguous": "permitted",
    "sealed_terminal": "permitted",
    "unsupported_or_inconsistent": "prohibited",
}
EXACT_ACTIONS = {
    "provider_free_quiescent": (),
    "provider_pending_known_identity": ("provider_reconciliation_cycle",),
    "completed_unadopted": ("ordinary_resume",),
    "native_local_work_ready": ("ordinary_resume",),
    "submission_ambiguous": (
        "operator_review", "fresh_disposition_assessment",
    ),
    "sealed_terminal": ("terminal_result_ingress",),
    "unsupported_or_inconsistent": (),
}
PROVIDERLESS_ACTIONS = frozenset({
    "external_authority_v1", "external_authority_v2",
    "providerless_denial", "operator_review",
})

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_LOGICAL_ROOT_ID = re.compile(r"^lroot_[0-9a-f]{24}$")
_RESULT_ID = re.compile(r"^nres_[0-9a-f]{24}$")
_RECEIPT_ID = re.compile(r"^nreceipt_[0-9a-f]{24}$")
_SAFE_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
MAX_PROVIDER_OPERATION_REFS = 32
MAX_EVIDENCE_CATEGORIES = 32

_TOP_KEYS = frozenset({
    "schema_version", "assessment_sha256", "native_run_id", "route",
    "compatibility", "checkpoint", "lifecycle_evidence", "terminal_evidence",
    "native_custody_class", "custody_summary", "quarantine_posture",
    "supported_next_actions", "reason_code", "evidence_categories",
    "diagnostic_only", "provider_io_performed", "workspace_mutation_performed",
})
_ROUTE_KEYS = frozenset({"family", "contract"})
_COMPATIBILITY_KEYS = frozenset({"sbe_release", "identity_sha256"})
_CHECKPOINT_KEYS = frozenset({
    "state_revision", "snapshot_sha256", "checkpoint_basis_sha256",
    "logical_workspace_root_id",
})
_LIFECYCLE_KEYS = frozenset({"schema_version", "document_sha256"})
_TERMINAL_KEYS = frozenset({
    "discovery_mode", "availability_document_sha256", "result_id",
    "result_sha256", "receipt_id", "receipt_sha256",
    "snapshot_sha256", "checkpoint_basis_sha256",
})
_SUMMARY_KEYS = frozenset({
    "provider_identity_count", "completed_unadopted_count",
    "ambiguous_submission_count", "local_operation_count",
    "providerless_authority_count", "retry_lineage_conflict",
    "sealed_result_count", "provider_operation_refs",
    "provider_operation_refs_overflow",
})


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def assessment_sha256(value: Mapping[str, Any]) -> str:
    return _digest({
        key: item for key, item in value.items()
        if key != "assessment_sha256"
    })


def logical_workspace_root_id(logical_root: str) -> str:
    if not isinstance(logical_root, str) or not logical_root:
        raise ValueError("Logical workspace root source is invalid")
    return "lroot_" + hashlib.sha256(logical_root.encode("utf-8")).hexdigest()[:24]


def _closed(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} fields are not exact")
    return value


def _sha(value: object, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{label} is not a canonical SHA-256")
    return value


def _count(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} is invalid")
    return value


def validate_operator_disposition_assessment(value: object) -> dict[str, Any]:
    root = _closed(value, _TOP_KEYS, "Operator-disposition assessment")
    if root.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported operator-disposition assessment schema")
    if not isinstance(root.get("native_run_id"), str) or _RUN_ID.fullmatch(
        root["native_run_id"]
    ) is None:
        raise ValueError("Assessment native_run_id is invalid")

    route = _closed(root.get("route"), _ROUTE_KEYS, "Assessment route")
    if route.get("family") not in {"exact_natal", "bounded_natal"}:
        raise ValueError("Assessment route family is unsupported")
    if not isinstance(route.get("contract"), str) or not (
        1 <= len(route["contract"]) <= 256
    ):
        raise ValueError("Assessment route contract is invalid")

    compatibility = _closed(
        root.get("compatibility"), _COMPATIBILITY_KEYS,
        "Assessment compatibility",
    )
    if not isinstance(compatibility.get("sbe_release"), str) or not (
        1 <= len(compatibility["sbe_release"]) <= 64
    ):
        raise ValueError("Assessment SBE release is invalid")
    _sha(compatibility.get("identity_sha256"), "Compatibility identity")

    checkpoint = _closed(
        root.get("checkpoint"), _CHECKPOINT_KEYS, "Assessment checkpoint",
    )
    _count(checkpoint.get("state_revision"), "Checkpoint state revision")
    _sha(checkpoint.get("snapshot_sha256"), "Checkpoint snapshot digest")
    _sha(
        checkpoint.get("checkpoint_basis_sha256"),
        "Checkpoint basis digest",
    )
    logical_id = checkpoint.get("logical_workspace_root_id")
    if not isinstance(logical_id, str) or _LOGICAL_ROOT_ID.fullmatch(logical_id) is None:
        raise ValueError("Logical workspace root ID is invalid or path-like")

    lifecycle = _closed(
        root.get("lifecycle_evidence"), _LIFECYCLE_KEYS,
        "Assessment lifecycle evidence",
    )
    if lifecycle.get("schema_version") not in SUPPORTED_LIFECYCLE_SCHEMAS:
        raise ValueError("Assessment lifecycle schema is unsupported")
    _sha(lifecycle.get("document_sha256"), "Lifecycle document digest")

    terminal = root.get("terminal_evidence")
    if terminal is not None:
        terminal = _closed(terminal, _TERMINAL_KEYS, "Terminal evidence")
        if terminal.get("discovery_mode") not in {
            "invocation_result", "availability_recovery",
        }:
            raise ValueError("Terminal discovery mode is invalid")
        availability_sha = _sha(
            terminal.get("availability_document_sha256"),
            "Availability document digest", nullable=True,
        )
        if (
            terminal["discovery_mode"] == "invocation_result"
            and availability_sha is not None
        ) or (
            terminal["discovery_mode"] == "availability_recovery"
            and availability_sha is None
        ):
            raise ValueError("Terminal discovery provenance is contradictory")
        if _RESULT_ID.fullmatch(str(terminal.get("result_id"))) is None:
            raise ValueError("Terminal result ID is invalid")
        if _RECEIPT_ID.fullmatch(str(terminal.get("receipt_id"))) is None:
            raise ValueError("Terminal receipt ID is invalid")
        _sha(terminal.get("result_sha256"), "Terminal result digest")
        _sha(terminal.get("receipt_sha256"), "Terminal receipt digest")
        _sha(terminal.get("snapshot_sha256"), "Terminal snapshot digest")
        _sha(
            terminal.get("checkpoint_basis_sha256"),
            "Terminal checkpoint-basis digest",
        )

    custody_class = root.get("native_custody_class")
    if custody_class not in CUSTODY_CLASSES:
        raise ValueError("Native custody class is invalid")
    summary = _closed(
        root.get("custody_summary"), _SUMMARY_KEYS, "Custody summary",
    )
    counts = {
        name: _count(summary.get(name), f"Custody {name}")
        for name in (
            "provider_identity_count", "completed_unadopted_count",
            "ambiguous_submission_count", "local_operation_count",
            "providerless_authority_count", "sealed_result_count",
        )
    }
    if not isinstance(summary.get("retry_lineage_conflict"), bool):
        raise ValueError("Retry-lineage conflict assertion is invalid")
    refs = summary.get("provider_operation_refs")
    overflow = summary.get("provider_operation_refs_overflow")
    if (
        not isinstance(refs, list)
        or len(refs) > MAX_PROVIDER_OPERATION_REFS
        or refs != sorted(set(refs))
        or any(not isinstance(item, str) or _SAFE_REF.fullmatch(item) is None for item in refs)
        or not isinstance(overflow, bool)
        or len(refs) != min(
            counts["provider_identity_count"], MAX_PROVIDER_OPERATION_REFS
        )
        or overflow != (
            counts["provider_identity_count"] > MAX_PROVIDER_OPERATION_REFS
        )
    ):
        raise ValueError("Provider-operation reference inventory is invalid")
    if counts["sealed_result_count"] not in {0, 1}:
        raise ValueError("Sealed-result count is invalid")
    if (terminal is not None) != (counts["sealed_result_count"] == 1):
        raise ValueError("Terminal evidence does not join custody summary")

    posture = root.get("quarantine_posture")
    if posture not in QUARANTINE_POSTURES or posture != POSTURES[custody_class]:
        raise ValueError("Custody class and quarantine posture do not join")
    actions = root.get("supported_next_actions")
    if (
        not isinstance(actions, list)
        or actions != list(dict.fromkeys(actions))
        or any(item not in NEXT_ACTIONS for item in actions)
    ):
        raise ValueError("Supported next-action inventory is invalid")
    if custody_class == "providerless_authority":
        if len(actions) != 1 or actions[0] not in PROVIDERLESS_ACTIONS:
            raise ValueError("Providerless authority lacks its exact named action")
    elif tuple(actions) != EXACT_ACTIONS[custody_class]:
        raise ValueError("Custody class and supported next actions do not join")
    if root.get("reason_code") != REASON_CODES[custody_class]:
        raise ValueError("Custody class and reason code do not join")

    categories = root.get("evidence_categories")
    if (
        not isinstance(categories, list)
        or len(categories) > MAX_EVIDENCE_CATEGORIES
        or categories != sorted(set(categories))
        or any(
            item not in EVIDENCE_CATEGORIES
            for item in categories
        )
    ):
        raise ValueError("Evidence categories are invalid")
    if (
        root.get("diagnostic_only") is not True
        or root.get("provider_io_performed") is not False
        or root.get("workspace_mutation_performed") is not False
    ):
        raise ValueError("Assessment side-effect assertions are invalid")

    positive_requirements = {
        "provider_pending_known_identity": counts["provider_identity_count"] > 0,
        "completed_unadopted": counts["completed_unadopted_count"] > 0,
        "native_local_work_ready": counts["local_operation_count"] > 0,
        "providerless_authority": counts["providerless_authority_count"] > 0,
        "submission_ambiguous": counts["ambiguous_submission_count"] > 0,
        "sealed_terminal": terminal is not None,
    }
    if custody_class in positive_requirements and not positive_requirements[custody_class]:
        raise ValueError("Custody class lacks positive native evidence")
    if custody_class == "provider_free_quiescent" and (
        any(counts.values()) or summary["retry_lineage_conflict"]
    ):
        raise ValueError("Provider-free quiescent assessment contains live evidence")
    if custody_class == "sealed_terminal" and (
        counts["provider_identity_count"]
        or counts["completed_unadopted_count"]
        or counts["ambiguous_submission_count"]
        or counts["local_operation_count"]
        or counts["providerless_authority_count"]
        or summary["retry_lineage_conflict"]
    ):
        raise ValueError("Sealed terminal assessment contains contradictory live custody")
    if counts["completed_unadopted_count"] > counts["provider_identity_count"]:
        raise ValueError("Completed evidence exceeds durable provider identities")

    if custody_class == "unsupported_or_inconsistent":
        if not categories:
            raise ValueError("Unsupported assessment lacks a closed evidence category")
    else:
        dominant = (
            "submission_ambiguous"
            if counts["ambiguous_submission_count"] else
            "completed_unadopted"
            if counts["completed_unadopted_count"] else
            "provider_pending_known_identity"
            if counts["provider_identity_count"] else
            "unsupported_or_inconsistent"
            if summary["retry_lineage_conflict"] else
            "native_local_work_ready"
            if counts["local_operation_count"] else
            "providerless_authority"
            if counts["providerless_authority_count"] else
            "sealed_terminal"
            if terminal is not None else
            "provider_free_quiescent"
        )
        if custody_class != dominant:
            raise ValueError("Custody class violates native-evidence precedence")

    _sha(root.get("assessment_sha256"), "Assessment digest")
    if root["assessment_sha256"] != assessment_sha256(root):
        raise ValueError("Assessment digest is invalid")
    return deepcopy(root)


def build_operator_disposition_assessment(**fields: Any) -> dict[str, Any]:
    value = {"schema_version": SCHEMA_VERSION, **deepcopy(fields)}
    value["assessment_sha256"] = assessment_sha256(value)
    return validate_operator_disposition_assessment(value)


@contextmanager
def _read_only_native_fence(run_dir: Path):
    """Take the existing native writer lock without creating or changing it."""
    path = run_dir / "spend-consumption.lock"
    if not path.is_file() or path.stat().st_size < 1:
        yield False
        return
    with path.open("r+b") as handle:
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError):
            yield False
            return
        try:
            yield True
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


_TERMINAL_RESULT_OUTCOMES = frozenset({
    "delivery_complete", "review_required", "terminal_failure",
    "budget_exhausted", "policy_stopped", "native_evidence_invalid",
})


def _normalized_lifecycle(value: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize supported v0.5 or v0.8 evidence for assessment only."""
    if value.get("schema_version") == (
        "astrowoof.authoring_lifecycle_inspection.v0.8"
    ):
        return deepcopy(dict(value))
    if value.get("schema_version") != (
        "astrowoof.authoring_lifecycle_inspection.v0.5"
    ):
        raise ValueError("Unsupported lifecycle evidence for disposition")
    request = value.get("external_authority_request")
    refusal = value.get("external_authority_refusal")
    if request is not None:
        authority = {
            "kind": "request", "request_kind": request["request_kind"],
            "ordered_action_ids": list(request["ordered_action_ids"]),
            "refusal_reason": None, "evidence_categories": [],
        }
    elif refusal is not None:
        authority = {
            "kind": "refusal", "request_kind": None,
            "ordered_action_ids": [],
            "refusal_reason": refusal["reason_code"],
            "evidence_categories": list(refusal["evidence_categories"]),
        }
    else:
        authority = {
            "kind": "none", "request_kind": None,
            "ordered_action_ids": [], "refusal_reason": None,
            "evidence_categories": [],
        }
    basis = {
        "observation": deepcopy(value["observation"]),
        "terminal": deepcopy(value["terminal"]),
        "quiescence": deepcopy(value["quiescence"]),
        "local_dependencies": deepcopy(value["local_dependencies"]),
        "action_inventory": deepcopy(value["action_inventory"]),
        "review_reasons": deepcopy(value["review_reasons"]),
        "provider_custody": deepcopy(value["provider_custody"]),
        "native_route": deepcopy(value["native_route"]),
        "consumer_authority": deepcopy(value["consumer_authority"]),
        "external_authority_state": authority,
        "local_work_inventory": {"operations": []},
        "retry_lineage_inventory": {"status": "coherent"},
    }
    return {
        "schema_version": value["schema_version"],
        "run_id": value["run_id"],
        "checkpoint_basis_sha256": _digest(basis),
        "checkpoint_basis": basis,
    }


def _terminal_evidence(
    run_dir: Path, inspection: Mapping[str, Any], *, result_id: str | None,
    allow_availability_recovery: bool,
) -> tuple[dict[str, Any] | None, list[str]]:
    from .native_transition_availability import (
        NativeTransitionAvailabilityError,
        read_native_transition_result_availability,
    )
    from .native_transitions import read_native_transition_result

    categories: list[str] = []
    availability_sha: str | None = None
    discovery_mode = "invocation_result"
    selected = result_id
    try:
        if selected is None and allow_availability_recovery:
            availability = read_native_transition_result_availability(run_dir)
            availability_sha = availability["availability_document_sha256"]
            selected = availability["latest_result_id"]
            discovery_mode = "availability_recovery"
        if selected is None:
            return None, categories
        view = read_native_transition_result(run_dir, selected)
    except (NativeTransitionAvailabilityError, OSError, ValueError, KeyError, TypeError):
        return None, ["terminal_evidence_unjoinable"]

    result = view["result"]
    receipt = view["receipt"]
    outcome = result.get("outcome")
    post = result.get("post_checkpoint") or {}
    current_revision = inspection["checkpoint_basis"]["observation"][
        "operator_state_revision"
    ]
    if (
        outcome not in _TERMINAL_RESULT_OUTCOMES
        or post.get("native_state_revision") != current_revision
        or receipt.get("snapshot_sha256")
        != hashlib.sha256(
            (run_dir / "workspace-snapshot.json").read_bytes()
        ).hexdigest()
    ):
        # A valid historical/nonterminal result is not the disposition of this
        # exact checkpoint. It remains available through its own reader.
        return None, categories
    return {
        "discovery_mode": discovery_mode,
        "availability_document_sha256": availability_sha,
        "result_id": result["result_id"],
        "result_sha256": result["result_sha256"],
        "receipt_id": receipt["receipt_id"],
        "receipt_sha256": receipt["receipt_sha256"],
        "snapshot_sha256": receipt["snapshot_sha256"],
        "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
    }, categories


def _classify_inspection(
    inspection: Mapping[str, Any], terminal: Mapping[str, Any] | None,
    categories: list[str], *, fenced: bool,
) -> tuple[str, dict[str, Any], str, list[str], str, list[str]]:
    basis = inspection["checkpoint_basis"]
    custody = basis["provider_custody"]
    actions = basis["action_inventory"]["actions"]
    custody_actions = custody["actions"]
    provider_refs = sorted({
        str(item["provider_operation_id"])
        for item in custody_actions if item.get("provider_operation_id")
    })
    provider_count = len(provider_refs)
    completed_count = sum(
        item.get("custody_classification") == "completed_provider_evidence"
        for item in custody_actions
    )
    ambiguous_count = sum(
        item.get("state") in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}
        or bool(item.get("ambiguity_review_reasons"))
        for item in actions
    )
    local_count = len(
        basis.get("local_work_inventory", {}).get("operations", [])
    )
    providerless_count = sum(
        bool(item.get("providerless_denial_eligible")) for item in actions
    )
    lineage_conflict = (
        basis.get("retry_lineage_inventory", {}).get("status") == "conflict"
    )
    review_reasons = set(basis.get("review_reasons") or [])
    if "snapshot_incomplete_or_invalid" in review_reasons:
        categories.append("snapshot_invalid")
    if review_reasons & {
        "local_work_contract_upgrade_required", "local_work_inventory_empty",
    }:
        categories.append("local_work_inventory_unavailable")
    if review_reasons & {
        "initial_wave_lineage_unjoinable", "native_state_inconsistent",
    }:
        categories.append("external_authority_unjoinable")
    known_review_reasons = {
        "authorized_providerless_action_requires_constrained_dispatch",
        "retry_lineage_conflict_requires_review",
        "snapshot_incomplete_or_invalid", "writer_race_possible",
        "local_work_contract_upgrade_required", "local_work_inventory_empty",
        "initial_wave_lineage_unjoinable", "native_state_inconsistent",
    }
    if review_reasons - known_review_reasons:
        categories.append("contradictory_evidence")
    unsupported_custody = any(
        item.get("custody_classification") == "unsupported"
        for item in custody_actions
    )
    if not fenced:
        categories.append("writer_exclusivity_unestablished")
    if unsupported_custody:
        categories.append("provider_custody_unjoinable")
    categories = sorted(set(categories))

    summary = {
        "provider_identity_count": provider_count,
        "completed_unadopted_count": completed_count,
        "ambiguous_submission_count": ambiguous_count,
        "local_operation_count": local_count,
        "providerless_authority_count": providerless_count,
        "retry_lineage_conflict": lineage_conflict,
        "sealed_result_count": 1 if terminal is not None else 0,
        "provider_operation_refs": provider_refs[:MAX_PROVIDER_OPERATION_REFS],
        "provider_operation_refs_overflow": (
            provider_count > MAX_PROVIDER_OPERATION_REFS
        ),
    }
    if categories:
        custody_class = "unsupported_or_inconsistent"
    elif ambiguous_count:
        custody_class = "submission_ambiguous"
    elif completed_count:
        custody_class = "completed_unadopted"
    elif provider_count:
        custody_class = "provider_pending_known_identity"
    elif lineage_conflict:
        categories = ["retry_lineage_conflict"]
        custody_class = "unsupported_or_inconsistent"
    elif local_count:
        custody_class = "native_local_work_ready"
    elif providerless_count:
        custody_class = "providerless_authority"
    elif terminal is not None:
        custody_class = "sealed_terminal"
    else:
        custody_class = "provider_free_quiescent"

    if custody_class == "providerless_authority":
        authority = basis.get("external_authority_state") or {}
        if authority.get("kind") == "request":
            action = (
                "external_authority_v1"
                if authority.get("request_kind") == "initial_wave_admission"
                else "external_authority_v2"
            )
        elif authority.get("kind") == "refusal":
            action = "operator_review"
        elif any(item.get("state") == "AUTHORIZED" for item in actions):
            action = "operator_review"
        else:
            action = "providerless_denial"
        next_actions = [action]
    else:
        next_actions = list(EXACT_ACTIONS[custody_class])
    return (
        custody_class, summary, POSTURES[custody_class], next_actions,
        REASON_CODES[custody_class], categories,
    )


def read_operator_disposition_assessment(
    run_dir: Path | str, *, terminal_result_id: str | None = None,
    allow_availability_recovery: bool = False,
) -> dict[str, Any]:
    """Assess one exact workspace without provider I/O or native mutation."""
    from . import __version__
    from .closure import load_json, sha256_file, validate_workspace_snapshot
    from .lifecycle import inspect_lifecycle
    from .lifecycle_contracts import validate_lifecycle_inspection_v05
    from .retry_lineage_contracts import inspect_retry_lineage_lifecycle

    root = Path(run_dir).resolve()
    state = load_json(root / "run.json")
    validate_workspace_snapshot(root, state)
    raw_observed_at = str(
        state.get("updated_at") or "1970-01-01T00:00:00+00:00"
    )
    parsed_observed_at = datetime.fromisoformat(
        raw_observed_at.replace("Z", "+00:00")
    )
    if parsed_observed_at.tzinfo is None or parsed_observed_at.utcoffset() is None:
        raise ValueError("Native updated_at must be timezone-aware")
    observed_at = parsed_observed_at.astimezone(timezone.utc).replace(
        microsecond=0
    ).isoformat()
    with _read_only_native_fence(root) as fenced:
        access = "established" if fenced else "not_established"
        try:
            raw_inspection = inspect_retry_lineage_lifecycle(
                root, observed_at=observed_at, native_exclusive_access=access,
            )
        except ValueError:
            # Some historical terminal evidence is valid v0.5 but cannot be
            # losslessly widened into later local-work/lineage contracts. The
            # v0.5 fallback is sufficient only for exact terminal/custody facts;
            # absence of local-work proof is handled fail closed below.
            raw_inspection = inspect_lifecycle(
                root, observed_at=observed_at,
                native_exclusive_access=access,
            )
            validate_lifecycle_inspection_v05(raw_inspection)
        inspection = _normalized_lifecycle(raw_inspection)
        terminal, categories = _terminal_evidence(
            root, inspection, result_id=terminal_result_id,
            allow_availability_recovery=allow_availability_recovery,
        )
        classified = _classify_inspection(
            inspection, terminal, categories, fenced=fenced,
        )
        if (
            raw_inspection["schema_version"]
            == "astrowoof.authoring_lifecycle_inspection.v0.5"
            and terminal is None
            and classified[0] == "provider_free_quiescent"
        ):
            classified = _classify_inspection(
                inspection, terminal,
                [*categories, "local_work_inventory_unavailable"],
                fenced=fenced,
            )
        # Revalidate after every read while the native writer fence is held.
        validate_workspace_snapshot(root, state)

    custody_class, summary, posture, actions, reason, categories = classified
    basis = inspection["checkpoint_basis"]
    observation = basis["observation"]
    route = basis["native_route"]
    compatibility_basis = {
        "sbe_release": __version__,
        "route_contract": route["route_contract"],
        "lifecycle_schema": inspection["schema_version"],
    }
    return build_operator_disposition_assessment(
        native_run_id=inspection["run_id"],
        route={
            "family": route["route_family"],
            "contract": route["route_contract"],
        },
        compatibility={
            "sbe_release": __version__,
            "identity_sha256": _digest(compatibility_basis),
        },
        checkpoint={
            "state_revision": observation["operator_state_revision"],
            "snapshot_sha256": sha256_file(root / "workspace-snapshot.json"),
            "checkpoint_basis_sha256": inspection["checkpoint_basis_sha256"],
            "logical_workspace_root_id": logical_workspace_root_id(
                observation["logical_workspace_root"]
            ),
        },
        lifecycle_evidence={
            "schema_version": raw_inspection["schema_version"],
            "document_sha256": _digest(raw_inspection),
        },
        terminal_evidence=terminal,
        native_custody_class=custody_class,
        custody_summary=summary,
        quarantine_posture=posture,
        supported_next_actions=actions,
        reason_code=reason,
        evidence_categories=categories,
        diagnostic_only=True,
        provider_io_performed=False,
        workspace_mutation_performed=False,
    )


def read_operator_disposition_assessment_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "operator-disposition-assessment.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


__all__ = [
    "CUSTODY_CLASSES", "EVIDENCE_CATEGORIES", "NEXT_ACTIONS",
    "QUARANTINE_POSTURES", "SCHEMA_VERSION", "SUPPORTED_LIFECYCLE_SCHEMAS",
    "assessment_sha256", "build_operator_disposition_assessment",
    "logical_workspace_root_id", "read_operator_disposition_assessment_schema",
    "read_operator_disposition_assessment",
    "validate_operator_disposition_assessment",
]
