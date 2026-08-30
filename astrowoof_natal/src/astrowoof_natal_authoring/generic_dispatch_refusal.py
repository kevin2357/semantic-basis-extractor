"""Closed nonmutating refusal for legacy generic provider dispatch."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.resources import files
import json
import re
from typing import Any, Mapping, Sequence


SCHEMA = "astrowoof.generic_provider_dispatch_refusal.v1"
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_KEYS = {
    "schema_version", "result_sha256", "outcome", "reason_code",
    "provider_io_disposition", "new_provider_create_permitted", "run_id",
    "checkpoint_basis_sha256", "ordered_action_ids", "state_revision",
    "snapshot_sha256", "next_step",
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def build_generic_provider_dispatch_refusal(
    *, run_id: str, checkpoint_basis_sha256: str,
    ordered_action_ids: Sequence[str], state_revision: int,
    snapshot_sha256: str,
) -> dict[str, Any]:
    body = {
        "schema_version": SCHEMA,
        "outcome": "pre_provider_refusal",
        "reason_code": "external_authority_v2_dispatch_required",
        "provider_io_disposition": "not_attempted",
        "new_provider_create_permitted": False,
        "run_id": run_id,
        "checkpoint_basis_sha256": checkpoint_basis_sha256,
        "ordered_action_ids": list(ordered_action_ids),
        "state_revision": state_revision,
        "snapshot_sha256": snapshot_sha256,
        "next_step": "fresh_lifecycle_inspection",
    }
    return validate_generic_provider_dispatch_refusal({
        **body, "result_sha256": _digest(body),
    })


def validate_generic_provider_dispatch_refusal(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _KEYS:
        raise ValueError("Generic provider-dispatch refusal fields are not exact")
    if (
        value.get("schema_version") != SCHEMA
        or value.get("outcome") != "pre_provider_refusal"
        or value.get("reason_code") != "external_authority_v2_dispatch_required"
        or value.get("provider_io_disposition") != "not_attempted"
        or value.get("new_provider_create_permitted") is not False
        or value.get("next_step") != "fresh_lifecycle_inspection"
    ):
        raise ValueError("Generic provider-dispatch refusal semantics are invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Generic provider-dispatch refusal run identity is invalid")
    for key in ("checkpoint_basis_sha256", "snapshot_sha256"):
        if not isinstance(value.get(key), str) or _DIGEST.fullmatch(value[key]) is None:
            raise ValueError(f"Generic provider-dispatch refusal {key} is invalid")
    action_ids = value.get("ordered_action_ids")
    if (
        not isinstance(action_ids, list) or not action_ids
        or action_ids != sorted(action_ids) or len(action_ids) != len(set(action_ids))
        or any(not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None for item in action_ids)
    ):
        raise ValueError("Generic provider-dispatch refusal action inventory is invalid")
    revision = value.get("state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError("Generic provider-dispatch refusal revision is invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("Generic provider-dispatch refusal digest mismatch")
    return deepcopy(value)


def read_generic_provider_dispatch_refusal_schema() -> dict[str, Any]:
    return json.loads(files(
        "astrowoof_natal_authoring.resources.contracts"
    ).joinpath("generic-provider-dispatch-refusal.v1.schema.json").read_text(
        encoding="utf-8"
    ))


def generic_create_capable_action_ids(
    state: Mapping[str, Any], documents: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Return exact ordinary interactive actions that require v2 dispatch."""
    if state.get("schema_version") != "astrowoof.semantic_closure_run.v0.9":
        return []
    actions = {
        item.get("action_id"): item
        for item in (state.get("spend_ledger") or {}).get("actions") or []
    }
    selected: list[str] = []
    for document in documents:
        action_id = document.get("action_id")
        action = actions.get(action_id)
        binding = (action or {}).get("binding") or {}
        if (
            isinstance(action_id, str)
            and action is not None
            and action.get("state") in {"PREPARED", "AUTHORIZED"}
            and action.get("provider") is None
            and binding.get("service_level") == "interactive"
            and binding.get("stage") != "authoring_initial"
        ):
            selected.append(action_id)
    return sorted(set(selected))
