"""Sanitized packaged fixture matrix for operator-disposition consumers."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .operator_disposition import (
    CUSTODY_CLASSES,
    build_operator_disposition_assessment,
    logical_workspace_root_id,
    validate_operator_disposition_assessment,
)


CONTRACT = "astrowoof.operator_disposition_fixture_bundle.v1"
_SHA = [character * 64 for character in "abcd"]


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _summary(**updates: Any) -> dict[str, Any]:
    value = {
        "provider_identity_count": 0,
        "completed_unadopted_count": 0,
        "ambiguous_submission_count": 0,
        "local_operation_count": 0,
        "providerless_authority_count": 0,
        "retry_lineage_conflict": False,
        "sealed_result_count": 0,
        "provider_operation_refs": [],
        "provider_operation_refs_overflow": False,
    }
    value.update(updates)
    return value


def _fixture(custody_class: str) -> dict[str, Any]:
    cases = {
        "provider_free_quiescent": (
            _summary(), "permitted", [], "provider_free_quiescent", None, [],
        ),
        "provider_pending_known_identity": (
            _summary(provider_identity_count=1, provider_operation_refs=["resp_fixture_pending_1"]),
            "permitted", ["provider_reconciliation_cycle"],
            "known_provider_operation_pending", None, [],
        ),
        "completed_unadopted": (
            _summary(provider_identity_count=1, completed_unadopted_count=1,
                     provider_operation_refs=["resp_fixture_completed_1"]),
            "native_prior_action_required", ["ordinary_resume"],
            "completed_provider_evidence_requires_adoption", None, [],
        ),
        "native_local_work_ready": (
            _summary(local_operation_count=1), "native_prior_action_required",
            ["ordinary_resume"], "native_local_work_ready", None, [],
        ),
        "providerless_authority": (
            _summary(providerless_authority_count=1), "permitted",
            ["external_authority_v2"],
            "providerless_authority_requires_named_action", None, [],
        ),
        "submission_ambiguous": (
            _summary(ambiguous_submission_count=1), "permitted",
            ["operator_review", "fresh_disposition_assessment"],
            "provider_submission_ambiguous", None, [],
        ),
        "sealed_terminal": (
            _summary(sealed_result_count=1), "permitted",
            ["terminal_result_ingress"], "sealed_terminal_result_available",
            {
                "discovery_mode": "invocation_result",
                "availability_document_sha256": None,
                "result_id": "nres_" + "1" * 24,
                "result_sha256": _SHA[2],
                "receipt_id": "nreceipt_" + "2" * 24,
                "receipt_sha256": _SHA[3],
                "snapshot_sha256": _SHA[0],
                "checkpoint_basis_sha256": _SHA[1],
            }, [],
        ),
        "unsupported_or_inconsistent": (
            _summary(retry_lineage_conflict=True), "prohibited", [],
            "unsupported_or_inconsistent_evidence", None,
            ["retry_lineage_conflict"],
        ),
    }
    summary, posture, actions, reason, terminal, categories = cases[custody_class]
    return build_operator_disposition_assessment(
        native_run_id=f"run_fixture_{custody_class}",
        route={"family": "exact_natal", "contract": "astrowoof.semantic_closure_run.v0.9"},
        compatibility={"sbe_release": "fixture-v1", "identity_sha256": _SHA[0]},
        checkpoint={
            "state_revision": 7, "snapshot_sha256": _SHA[1],
            "checkpoint_basis_sha256": _SHA[2],
            "logical_workspace_root_id": logical_workspace_root_id(
                f"sanitized-fixture/{custody_class}"
            ),
        },
        lifecycle_evidence={
            "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.8",
            "document_sha256": _SHA[3],
        },
        terminal_evidence=terminal, native_custody_class=custody_class,
        custody_summary=summary, quarantine_posture=posture,
        supported_next_actions=actions, reason_code=reason,
        evidence_categories=categories,
        diagnostic_only=True,
        provider_io_performed=False,
        workspace_mutation_performed=False,
    )


def read_operator_disposition_fixtures() -> dict[str, Any]:
    fixtures = [_fixture(item) for item in sorted(CUSTODY_CLASSES)]
    body = {"schema_version": CONTRACT, "sanitized": True, "fixtures": fixtures}
    return validate_operator_disposition_fixtures({
        **body, "bundle_sha256": _digest(body),
    })


def validate_operator_disposition_fixtures(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "bundle_sha256", "sanitized", "fixtures",
    }:
        raise ValueError("Operator-disposition fixture bundle shape is invalid")
    body = {key: item for key, item in value.items() if key != "bundle_sha256"}
    fixtures = value.get("fixtures")
    if (
        value.get("schema_version") != CONTRACT
        or value.get("bundle_sha256") != _digest(body)
        or value.get("sanitized") is not True
        or not isinstance(fixtures, list)
        or len(fixtures) != len(CUSTODY_CLASSES)
        or [item.get("native_custody_class") for item in fixtures]
        != sorted(CUSTODY_CLASSES)
    ):
        raise ValueError("Operator-disposition fixture bundle semantics are invalid")
    for fixture in fixtures:
        validate_operator_disposition_assessment(fixture)
        rendered = _canonical(fixture).decode("utf-8").lower()
        for forbidden in ("prompt", "payload", "credential", "secret", "api_key"):
            if forbidden in rendered:
                raise ValueError("Operator-disposition fixture contains protected data")
    return dict(value)


__all__ = ["read_operator_disposition_fixtures", "validate_operator_disposition_fixtures"]
