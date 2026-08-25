"""Closed v2 grant and provider-free dispatch-decision contracts."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from importlib.resources import files
from typing import Any, Mapping, Sequence

from .temporal_lifecycle import (
    build_external_authority_request_v2,
    canonical_utc_instant,
    validate_external_authority_request_v2,
    validate_external_authority_request_v2_against_inspection,
    validate_lifecycle_inspection_v06,
)


GRANT_SCHEMA_V2 = "astrowoof.external_authority_grant.v2"
DISPATCH_RESULT_SCHEMA_V2 = "astrowoof.external_authority_dispatch_result.v2"
AUTHORIZATION_SCHEMA = "astrowoof.provider_spend_authorization.v0.1"
ORDERING_SEMANTICS = "lexical_action_id_ascending"
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_BINDING_KEYS = {
    "run_id", "profile_sha256", "prepared_state_revision", "stage", "route",
    "request_sha256", "model", "service_level", "maximum_output_tokens",
    "commitment_micro_usd", "price_book_version",
}
_AUTHORIZATION_KEYS = {
    "schema_version", "action_id", "binding", "authorization_reference",
}
_MEMBER_KEYS = {
    "action_id", "binding_sha256", "authorization_document_sha256",
    "authorization_reference",
}
_GRANT_KEYS = {
    "schema_version", "grant_sha256", "decision", "api_decision_id", "issuer",
    "issued_at", "external_authority_request_sha256", "run_id",
    "checkpoint_basis_sha256", "request_schema_version", "request_kind", "ordering_semantics",
    "route_family", "provider_mechanism", "action_count",
    "ordered_action_ids", "ordered_member_authorizations",
}
_RESULT_KEYS = {
    "schema_version", "result_sha256", "outcome", "run_id",
    "checkpoint_basis_sha256", "external_authority_request_sha256",
    "request_kind", "ordering_semantics", "ordered_action_ids", "reason_code",
    "selected_command", "dispatch_permitted", "native_mutation_performed",
    "provider_io_performed", "checkpoint_published",
}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError(f"{label} must be lowercase SHA-256")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _validate_binding(binding: Any, *, run_id: str) -> dict[str, Any]:
    if not isinstance(binding, dict) or set(binding) != _BINDING_KEYS:
        raise ValueError("authorization binding fields are not exact")
    if binding.get("run_id") != run_id:
        raise ValueError("authorization binding run_id mismatch")
    for field in ("profile_sha256", "request_sha256"):
        _require_digest(binding.get(field), f"binding.{field}")
    for field in ("stage", "route", "model", "service_level", "price_book_version"):
        _require_string(binding.get(field), f"binding.{field}")
    for field in (
        "prepared_state_revision", "maximum_output_tokens", "commitment_micro_usd",
    ):
        value = binding.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"binding.{field} must be a nonnegative integer")
    return binding


def validate_authorization_document_v2(value: Any, *, run_id: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _AUTHORIZATION_KEYS:
        raise ValueError("authorization document fields are not exact")
    if value.get("schema_version") != AUTHORIZATION_SCHEMA:
        raise ValueError("unsupported authorization document")
    action_id = value.get("action_id")
    if not isinstance(action_id, str) or not _ACTION_ID.fullmatch(action_id):
        raise ValueError("authorization action_id is not canonical")
    _validate_binding(value.get("binding"), run_id=run_id)
    _require_string(value.get("authorization_reference"), "authorization_reference")
    return deepcopy(value)


def _inspection_actions(inspection: dict[str, Any], action_ids: list[str]) -> list[dict[str, Any]]:
    inventory = inspection["checkpoint_basis"]["action_inventory"]["actions"]
    by_id = {item["action_id"]: item for item in inventory}
    if any(action_id not in by_id for action_id in action_ids):
        raise ValueError("grant action is absent from current inspection")
    return [by_id[action_id] for action_id in action_ids]


def _mechanism(actions: Sequence[Mapping[str, Any]]) -> str:
    mechanisms = {
        "batch" if item["binding"]["service_level"] == "batch" else "response"
        for item in actions
    }
    if len(mechanisms) != 1:
        raise ValueError("v2 ordinary action set must use one provider mechanism")
    return next(iter(mechanisms))


def build_external_authority_grant_v2(
    request: dict[str, Any], inspection: dict[str, Any],
    authorization_documents: Sequence[Mapping[str, Any]], *,
    api_decision_id: str, issuer: str, issued_at: str,
) -> dict[str, Any]:
    validate_external_authority_request_v2_against_inspection(request, inspection)
    if request["request_kind"] != "ordinary_action_set":
        raise ValueError("v2 execution supports ordinary_action_set only")
    ids = request["ordered_action_ids"]
    if ids != sorted(ids):
        raise ValueError("ordinary v2 action IDs must use canonical lexical order")
    if len(authorization_documents) != len(ids):
        raise ValueError("v2 grant must authorize the complete ordered inventory")
    actions = _inspection_actions(inspection, ids)
    members = []
    for action_id, action, raw in zip(ids, actions, authorization_documents, strict=True):
        document = validate_authorization_document_v2(dict(raw), run_id=request["run_id"])
        if document["action_id"] != action_id or document["binding"] != action["binding"]:
            raise ValueError("authorization document does not join inspection binding")
        members.append({
            "action_id": action_id,
            "binding_sha256": _digest(document["binding"]),
            "authorization_document_sha256": _digest(document),
            "authorization_reference": document["authorization_reference"],
        })
    grant = {
        "schema_version": GRANT_SCHEMA_V2, "grant_sha256": "pending",
        "decision": "granted", "api_decision_id": _require_string(api_decision_id, "api_decision_id"),
        "issuer": _require_string(issuer, "issuer"),
        "issued_at": canonical_utc_instant(issued_at),
        "external_authority_request_sha256": request["external_authority_request_sha256"],
        "run_id": request["run_id"],
        "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "request_schema_version": request["schema_version"],
        "request_kind": request["request_kind"], "ordering_semantics": ORDERING_SEMANTICS,
        "route_family": inspection["checkpoint_basis"]["native_route"]["route_family"],
        "provider_mechanism": _mechanism(actions), "action_count": len(ids),
        "ordered_action_ids": deepcopy(ids), "ordered_member_authorizations": members,
    }
    grant["grant_sha256"] = _digest({key: item for key, item in grant.items() if key != "grant_sha256"})
    return validate_external_authority_grant_v2(request, inspection, grant, authorization_documents)


def validate_external_authority_grant_v2(
    request: dict[str, Any], inspection: dict[str, Any], grant: Any,
    authorization_documents: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validate_external_authority_request_v2_against_inspection(request, inspection)
    if request["request_kind"] != "ordinary_action_set":
        raise ValueError("v2 execution supports ordinary_action_set only")
    if request["ordered_action_ids"] != sorted(request["ordered_action_ids"]):
        raise ValueError("ordinary v2 action IDs must use canonical lexical order")
    if not isinstance(grant, dict) or set(grant) != _GRANT_KEYS:
        raise ValueError("v2 grant fields are not exact")
    if grant.get("schema_version") != GRANT_SCHEMA_V2 or grant.get("decision") != "granted":
        raise ValueError("unsupported v2 grant")
    ids = request["ordered_action_ids"]
    actions = _inspection_actions(inspection, ids)
    expected = {
        "external_authority_request_sha256": request["external_authority_request_sha256"],
        "run_id": request["run_id"], "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "request_schema_version": "astrowoof.external_authority_request.v2",
        "request_kind": "ordinary_action_set", "ordering_semantics": ORDERING_SEMANTICS,
        "route_family": inspection["checkpoint_basis"]["native_route"]["route_family"],
        "provider_mechanism": _mechanism(actions), "action_count": len(ids),
        "ordered_action_ids": ids,
    }
    if any(grant.get(key) != value for key, value in expected.items()):
        raise ValueError("v2 grant does not join request and inspection")
    _require_string(grant.get("api_decision_id"), "api_decision_id")
    _require_string(grant.get("issuer"), "issuer")
    if grant.get("issued_at") != canonical_utc_instant(grant.get("issued_at")):
        raise ValueError("issued_at is not canonical UTC")
    members = grant.get("ordered_member_authorizations")
    if not isinstance(members, list) or len(members) != len(ids) or len(authorization_documents) != len(ids):
        raise ValueError("v2 grant is partial")
    for action_id, action, member, raw in zip(ids, actions, members, authorization_documents, strict=True):
        if not isinstance(member, dict) or set(member) != _MEMBER_KEYS:
            raise ValueError("v2 grant member fields are not exact")
        document = validate_authorization_document_v2(dict(raw), run_id=request["run_id"])
        if (
            member["action_id"] != action_id or document["action_id"] != action_id
            or document["binding"] != action["binding"]
            or member["binding_sha256"] != _digest(document["binding"])
            or member["authorization_document_sha256"] != _digest(document)
            or member["authorization_reference"] != document["authorization_reference"]
        ):
            raise ValueError("v2 grant member/document/binding join failed")
    body = {key: item for key, item in grant.items() if key != "grant_sha256"}
    if grant.get("grant_sha256") != _digest(body):
        raise ValueError("v2 grant digest mismatch")
    return deepcopy(grant)


def build_no_grant_dispatch_result_v2(inspection: dict[str, Any]) -> dict[str, Any]:
    validate_lifecycle_inspection_v06(inspection)
    request = build_external_authority_request_v2(inspection)
    result = {
        "schema_version": DISPATCH_RESULT_SCHEMA_V2, "result_sha256": "pending",
        "outcome": "awaiting_compatible_grant", "run_id": request["run_id"],
        "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "external_authority_request_sha256": request["external_authority_request_sha256"],
        "request_kind": request["request_kind"], "ordering_semantics": ORDERING_SEMANTICS,
        "ordered_action_ids": deepcopy(request["ordered_action_ids"]),
        "reason_code": "compatible_grant_required", "selected_command": "none",
        "dispatch_permitted": False, "native_mutation_performed": False,
        "provider_io_performed": False, "checkpoint_published": False,
    }
    result["result_sha256"] = _digest({key: item for key, item in result.items() if key != "result_sha256"})
    return validate_no_grant_dispatch_result_v2(result)


def validate_no_grant_dispatch_result_v2(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _RESULT_KEYS:
        raise ValueError("v2 dispatch result fields are not exact")
    expected = {
        "schema_version": DISPATCH_RESULT_SCHEMA_V2,
        "outcome": "awaiting_compatible_grant", "request_kind": "ordinary_action_set",
        "ordering_semantics": ORDERING_SEMANTICS, "reason_code": "compatible_grant_required",
        "selected_command": "none", "dispatch_permitted": False,
        "native_mutation_performed": False, "provider_io_performed": False,
        "checkpoint_published": False,
    }
    if any(value.get(key) != item for key, item in expected.items()):
        raise ValueError("no-grant result is not strictly non-dispatching")
    _require_string(value.get("run_id"), "run_id")
    for key in ("checkpoint_basis_sha256", "external_authority_request_sha256"):
        _require_digest(value.get(key), key)
    ids = value.get("ordered_action_ids")
    if not isinstance(ids, list) or not ids or ids != sorted(ids) or len(ids) != len(set(ids)) or any(not isinstance(item, str) or not _ACTION_ID.fullmatch(item) for item in ids):
        raise ValueError("no-grant action IDs are not canonical lexical order")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v2 dispatch result digest mismatch")
    return deepcopy(value)


def read_external_authority_grant_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-grant.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def read_external_authority_dispatch_result_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-dispatch-result.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def read_external_authority_v2_fixture() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "external-authority-v2", "ordinary-action-set.v1.json"
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version", "inspection", "request", "grant",
        "authorization_documents", "no_grant_result",
    }
    if not isinstance(value, dict) or set(value) != expected or value.get(
        "schema_version"
    ) != "astrowoof.external_authority_v2_contract_fixture.v1":
        raise ValueError("external authority v2 fixture fields are not exact")
    inspection = value["inspection"]
    request = value["request"]
    documents = value["authorization_documents"]
    validate_lifecycle_inspection_v06(inspection)
    validate_external_authority_request_v2_against_inspection(request, inspection)
    validate_external_authority_grant_v2(
        request, inspection, value["grant"], documents,
    )
    validate_no_grant_dispatch_result_v2(value["no_grant_result"])
    return deepcopy(value)
