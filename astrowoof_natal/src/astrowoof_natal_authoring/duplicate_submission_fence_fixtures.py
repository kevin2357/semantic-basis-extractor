"""Packaged API-shaped fixtures for the ordinary duplicate-create fence."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from importlib.resources import files
from typing import Any

from .generic_dispatch_refusal import validate_generic_provider_dispatch_refusal
from .terminal_review_contracts import (
    validate_terminal_review_command_result_against_publication,
    validate_terminal_review_result_v02,
)


FIXTURE_BUNDLE_SCHEMA = "astrowoof.duplicate_submission_fence_fixtures.v1"
_FIXTURE_NAME = "duplicate-submission-fence-fixtures.v1.json"


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def validate_duplicate_submission_fence_fixtures(value: dict[str, Any]) -> None:
    """Validate the closed consumer bundle and all nested publication joins."""
    keys = {
        "schema_version", "generic_provider_dispatch_refusal",
        "local_work_progress_contradiction", "bundle_sha256",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Duplicate-submission fence fixture shape is invalid")
    if value.get("schema_version") != FIXTURE_BUNDLE_SCHEMA:
        raise ValueError("Duplicate-submission fence fixture schema is invalid")
    basis = {key: item for key, item in value.items() if key != "bundle_sha256"}
    if value.get("bundle_sha256") != _digest(basis):
        raise ValueError("Duplicate-submission fence fixture digest is invalid")

    refusal = value.get("generic_provider_dispatch_refusal")
    validate_generic_provider_dispatch_refusal(refusal)
    if (
        refusal.get("reason_code") != "external_authority_v2_dispatch_required"
        or refusal.get("outcome") != "pre_provider_refusal"
        or refusal.get("provider_io_disposition") != "not_attempted"
        or refusal.get("next_step") != "fresh_lifecycle_inspection"
        or refusal.get("new_provider_create_permitted") is not False
    ):
        raise ValueError("Generic refusal fixture semantics are invalid")

    contradiction = value.get("local_work_progress_contradiction")
    contradiction_keys = {"command_result", "native_result", "publication_receipt"}
    if not isinstance(contradiction, dict) or set(contradiction) != contradiction_keys:
        raise ValueError("Local-progress contradiction fixture shape is invalid")
    result = contradiction.get("native_result")
    receipt = contradiction.get("publication_receipt")
    command = contradiction.get("command_result")
    validate_terminal_review_result_v02(result)
    validate_terminal_review_command_result_against_publication(
        command, result, receipt,
    )
    provider_rows = [
        row for row in result["action_dispositions"]
        if row["custody_disposition"] == "provider_reconciliation_only"
    ]
    if (
        result.get("cause_code") != "local_work_progress_contradiction"
        or result.get("outcome") != "review_required"
        or result.get("new_provider_create_permitted") is not False
        or not provider_rows
        or not all(row.get("provider_operation_id") for row in provider_rows)
        or result.get("reconciliation_action_ids")
        != [row["action_id"] for row in provider_rows]
    ):
        raise ValueError("Local-progress contradiction fixture semantics are invalid")


def read_duplicate_submission_fence_fixtures() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        f"fixtures/lifecycle/{_FIXTURE_NAME}"
    )
    value = json.loads(resource.read_text(encoding="utf-8"))
    validate_duplicate_submission_fence_fixtures(value)
    return deepcopy(value)


def read_duplicate_submission_fence_fixtures_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        "contracts/duplicate-submission-fence-fixtures.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))
