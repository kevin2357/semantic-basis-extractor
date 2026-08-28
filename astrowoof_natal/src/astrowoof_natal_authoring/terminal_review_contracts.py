"""Closed terminal-review result and mixed-custody public contract."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from importlib.resources import files
from typing import Any


RESULT_SCHEMA = "astrowoof.native_execution_result.v0.2"
COMMAND_RESULT_SCHEMA = "astrowoof.terminal_review_command_result.v0.1"
ACTION_STATES = frozenset({
    "PREPARED", "AUTHORIZED", "SUBMITTING", "PROVIDER_ID_RECORDED", "WAITING",
    "REPORTED", "DENIED_PROVIDERLESS", "BUDGET_EXHAUSTED",
    "SKIPPED_BUDGET_EXHAUSTED", "AMBIGUOUS_PROVIDER_SUBMISSION",
})
CUSTODY_DISPOSITIONS = frozenset({
    "terminally_accounted", "provider_reconciliation_only",
    "providerless_denial_only", "ambiguity_review_only",
})
CUSTODY_FINALITIES = frozenset({
    "final", "provider_reconciliation_required", "providerless_denial_required",
    "mixed_resolution_required", "ambiguity_review_required",
})
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_RESULT_ID = re.compile(r"^nres_[0-9a-f]{24}$")
_INVOCATION_ID = re.compile(r"^ninv_[0-9a-f]{24}$")
_STAGES = frozenset({
    "authoring_initial", "creative_retry", "polish", "qualitative_critic",
    "qualitative_candidate",
})
_REVIEW_CAUSES = frozenset({
    "final_qa_requires_review", "authoring_attempts_exhausted",
    "provider_terminal_failure", "provider_output_invalid",
    "provider_identity_conflict", "ambiguous_provider_submission",
    "snapshot_or_journal_invalid",
    "native_lifecycle_review_required",
})


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _binding(action: dict[str, Any]) -> dict[str, Any]:
    binding = action.get("binding")
    if not isinstance(binding, dict):
        raise ValueError("Terminal action has no complete binding")
    value = {
        "action_id": action.get("action_id"),
        "stage": binding.get("stage"),
        "route": binding.get("route"),
        "request_sha256": binding.get("request_sha256"),
        "profile_sha256": binding.get("profile_sha256"),
        "maximum_output_tokens": binding.get("maximum_output_tokens"),
        "commitment_micro_usd": binding.get("commitment_micro_usd"),
        "price_book_version": binding.get("price_book_version"),
    }
    if (
        not _ACTION_ID.fullmatch(str(value["action_id"]))
        or value["stage"] not in _STAGES
        or not isinstance(value["route"], str) or not value["route"]
        or not _DIGEST.fullmatch(str(value["request_sha256"]))
        or not _DIGEST.fullmatch(str(value["profile_sha256"]))
        or not isinstance(value["maximum_output_tokens"], int)
        or value["maximum_output_tokens"] < 1
        or not isinstance(value["commitment_micro_usd"], int)
        or value["commitment_micro_usd"] < 0
        or not isinstance(value["price_book_version"], str)
        or not value["price_book_version"]
    ):
        raise ValueError("Terminal action binding is invalid")
    return value


def _route_family(state: dict[str, Any]) -> str:
    return "bounded_natal" if state.get("route") in {"bounded_natal.v1", "bounded_natal.v2"} else "exact_natal"


def build_terminal_action_dispositions(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Project every paid action in ledger order into one closed custody row."""
    actions = (state.get("spend_ledger") or {}).get("actions")
    if not isinstance(actions, list):
        raise ValueError("Terminal result requires a paid-action inventory")
    result: list[dict[str, Any]] = []
    for ordinal, action in enumerate(actions, 1):
        binding = _binding(action)
        action_state = action.get("state")
        if action_state not in ACTION_STATES:
            raise ValueError("Terminal action state is unsupported")
        provider = action.get("provider")
        provider_id = provider.get("id") if isinstance(provider, dict) else None
        consumption_present = isinstance(action.get("consumption"), dict)
        reported_present = isinstance(action.get("reported"), dict)
        usage_reported = isinstance((action.get("reported") or {}).get("usage"), dict)
        if action_state in {"PROVIDER_ID_RECORDED", "WAITING"}:
            custody = "provider_reconciliation_only"
        elif action_state in {"PREPARED", "AUTHORIZED"}:
            custody = "providerless_denial_only"
        elif action_state in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}:
            custody = "ambiguity_review_only"
        else:
            custody = "terminally_accounted"
        row = {
            "ordinal": ordinal,
            "action_id": binding["action_id"],
            "binding_sha256": _digest(binding),
            "stage": binding["stage"],
            "route": binding["route"],
            "route_family": _route_family(state),
            "provider_mechanism": "batch" if (action.get("binding") or {}).get("service_level") == "batch" else "response",
            "native_action_state": action_state,
            "provider_operation_id": provider_id,
            "provider_status": (action.get("integrity_review") or {}).get("provider_status"),
            "consumption_present": consumption_present,
            "reported_present": reported_present,
            "usage_reported": usage_reported,
            "custody_disposition": custody,
            "denial_evidence_sha256": (
                _digest(action["negative_authorization"])
                if isinstance(action.get("negative_authorization"), dict) else None
            ),
        }
        result.append(row)
    _validate_actions(result)
    return result


def _finality(actions: list[dict[str, Any]]) -> str:
    custody = {item["custody_disposition"] for item in actions}
    if "ambiguity_review_only" in custody:
        return "ambiguity_review_required"
    provider = "provider_reconciliation_only" in custody
    providerless = "providerless_denial_only" in custody
    if provider and providerless:
        return "mixed_resolution_required"
    if provider:
        return "provider_reconciliation_required"
    if providerless:
        return "providerless_denial_required"
    return "final"


def build_terminal_review_result_v02(
    base_result: dict[str, Any], state: dict[str, Any],
) -> dict[str, Any]:
    """Upgrade a pre-identity result basis into the v0.2 review contract."""
    actions = build_terminal_action_dispositions(state)
    value = deepcopy(base_result)
    for key in ("result_id", "result_sha256", "action_ids", "provider_operations"):
        value.pop(key, None)
    value["schema_version"] = RESULT_SCHEMA
    value["outcome"] = "review_required"
    value["action_dispositions"] = actions
    value["action_inventory_sha256"] = _digest(actions)
    value["custody_finality"] = _finality(actions)
    value["reconciliation_action_ids"] = [
        item["action_id"] for item in actions
        if item["custody_disposition"] == "provider_reconciliation_only"
    ]
    value["providerless_denial_action_ids"] = [
        item["action_id"] for item in actions
        if item["custody_disposition"] == "providerless_denial_only"
    ]
    value["new_provider_create_permitted"] = False
    value["result_sha256"] = _digest(value)
    value["result_id"] = f"nres_{value['result_sha256'][:24]}"
    validate_terminal_review_result_v02(value)
    return value


def _validate_actions(actions: Any) -> None:
    if not isinstance(actions, list) or len(actions) > 128:
        raise ValueError("Terminal action inventory is invalid")
    seen: set[str] = set()
    keys = {
        "ordinal", "action_id", "binding_sha256", "stage", "route", "route_family",
        "provider_mechanism", "native_action_state", "provider_operation_id",
        "provider_status", "consumption_present", "reported_present", "usage_reported",
        "custody_disposition", "denial_evidence_sha256",
    }
    for ordinal, item in enumerate(actions, 1):
        if not isinstance(item, dict) or set(item) != keys or item.get("ordinal") != ordinal:
            raise ValueError("Terminal action projection shape/order is invalid")
        action_id = item.get("action_id")
        if not isinstance(action_id, str) or not _ACTION_ID.fullmatch(action_id) or action_id in seen:
            raise ValueError("Terminal action identity is invalid or duplicated")
        seen.add(action_id)
        if not _DIGEST.fullmatch(str(item.get("binding_sha256"))):
            raise ValueError("Terminal action binding digest is invalid")
        if item.get("stage") not in _STAGES or item.get("route_family") not in {"exact_natal", "bounded_natal"}:
            raise ValueError("Terminal action route/stage is invalid")
        if not isinstance(item.get("route"), str) or not item["route"]:
            raise ValueError("Terminal action route is invalid")
        if item.get("provider_mechanism") not in {"response", "batch"} or item.get("native_action_state") not in ACTION_STATES:
            raise ValueError("Terminal action mechanism/state is invalid")
        if item.get("custody_disposition") not in CUSTODY_DISPOSITIONS:
            raise ValueError("Terminal action custody is invalid")
        if any(type(item.get(key)) is not bool for key in ("consumption_present", "reported_present", "usage_reported")):
            raise ValueError("Terminal action evidence flags are invalid")
        provider_id = item.get("provider_operation_id")
        if provider_id is not None and (not isinstance(provider_id, str) or not provider_id):
            raise ValueError("Terminal provider identity is invalid")
        provider_status = item.get("provider_status")
        if provider_status is not None and (not isinstance(provider_status, str) or not provider_status):
            raise ValueError("Terminal provider status is invalid")
        denial = item.get("denial_evidence_sha256")
        if denial is not None and not _DIGEST.fullmatch(str(denial)):
            raise ValueError("Terminal denial evidence digest is invalid")
        custody = item["custody_disposition"]
        state = item["native_action_state"]
        if custody == "provider_reconciliation_only" and (not provider_id or state not in {"PROVIDER_ID_RECORDED", "WAITING"}):
            raise ValueError("Reconciliation custody lacks durable provider identity")
        if custody == "providerless_denial_only" and (provider_id is not None or state not in {"PREPARED", "AUTHORIZED"}):
            raise ValueError("Providerless custody is contradictory")
        if custody == "ambiguity_review_only" and state not in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}:
            raise ValueError("Ambiguity custody is contradictory")
        if state == "DENIED_PROVIDERLESS" and (custody != "terminally_accounted" or denial is None):
            raise ValueError("Providerless denial evidence is incomplete")
        if state != "DENIED_PROVIDERLESS" and denial is not None:
            raise ValueError("Denial evidence cannot attach to a non-denied action")
        if item["usage_reported"] and not item["reported_present"]:
            raise ValueError("Usage evidence requires a reported action")
        if state == "REPORTED" and not item["reported_present"]:
            raise ValueError("Reported action lacks reported evidence")


def validate_terminal_review_result_v02(value: dict[str, Any]) -> None:
    keys = {
        "schema_version", "result_id", "result_sha256", "invocation_id", "run_id",
        "sbe_release", "published_at", "command_kind", "route_binding", "pre_checkpoint",
        "post_checkpoint", "journal_range", "outcome", "cause_code", "action_dispositions",
        "action_inventory_sha256", "custody_finality", "reconciliation_action_ids",
        "providerless_denial_action_ids", "new_provider_create_permitted", "projection_refs",
    }
    if not isinstance(value, dict) or set(value) != keys or value.get("schema_version") != RESULT_SCHEMA:
        raise ValueError("Terminal review result shape/schema is invalid")
    if value.get("outcome") != "review_required" or value.get("new_provider_create_permitted") is not False:
        raise ValueError("Terminal review result semantic disposition is invalid")
    if not _INVOCATION_ID.fullmatch(str(value.get("invocation_id"))) or not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Terminal review invocation/run identity is invalid")
    if value.get("command_kind") not in {"ordinary_authoring", "provider_reconciliation"}:
        raise ValueError("Terminal review command kind is invalid")
    if not isinstance(value.get("sbe_release"), str) or not value["sbe_release"]:
        raise ValueError("Terminal review release identity is invalid")
    if not isinstance(value.get("published_at"), str) or not value["published_at"]:
        raise ValueError("Terminal review publication time is invalid")
    if value.get("cause_code") not in _REVIEW_CAUSES:
        raise ValueError("Terminal review cause is invalid")
    route = value.get("route_binding")
    if not isinstance(route, dict) or set(route) != {"route_family", "provider_mechanism", "native_operation_ref"}:
        raise ValueError("Terminal review route binding is invalid")
    if route.get("route_family") not in {"exact_natal", "bounded_natal"} or route.get("provider_mechanism") not in {"response", "batch"}:
        raise ValueError("Terminal review route vocabulary is invalid")
    if not isinstance(route.get("native_operation_ref"), str) or not route["native_operation_ref"]:
        raise ValueError("Terminal review native operation is invalid")
    pre = value.get("pre_checkpoint")
    if pre is not None and (
        not isinstance(pre, dict) or set(pre) != {"snapshot_sha256"}
        or not _DIGEST.fullmatch(str(pre.get("snapshot_sha256")))
    ):
        raise ValueError("Terminal review pre-checkpoint is invalid")
    post = value.get("post_checkpoint")
    if (
        not isinstance(post, dict)
        or set(post) != {"native_state_revision", "checkpoint_basis_sha256", "logical_workspace_root"}
        or not isinstance(post.get("native_state_revision"), int)
        or post["native_state_revision"] < 0
        or not _DIGEST.fullmatch(str(post.get("checkpoint_basis_sha256")))
        or not isinstance(post.get("logical_workspace_root"), str)
        or not post["logical_workspace_root"]
    ):
        raise ValueError("Terminal review post-checkpoint is invalid")
    journal = value.get("journal_range")
    if (
        not isinstance(journal, dict)
        or set(journal) != {"start_sequence", "end_sequence", "record_count", "range_sha256", "closing_record_id"}
        or not all(isinstance(journal.get(key), int) for key in ("start_sequence", "end_sequence", "record_count"))
        or journal["start_sequence"] < 1
        or journal["end_sequence"] < journal["start_sequence"]
        or journal["record_count"] != journal["end_sequence"] - journal["start_sequence"] + 1
        or not _DIGEST.fullmatch(str(journal.get("range_sha256")))
        or not re.fullmatch(r"^ntr_[0-9a-f]{24}$", str(journal.get("closing_record_id")))
    ):
        raise ValueError("Terminal review journal range is invalid")
    if not isinstance(value.get("projection_refs"), dict) or value["projection_refs"]:
        raise ValueError("Terminal review v0.2 projection refs must be empty")
    actions = value.get("action_dispositions")
    _validate_actions(actions)
    if value.get("action_inventory_sha256") != _digest(actions):
        raise ValueError("Terminal action inventory digest is invalid")
    reconciliation = [item["action_id"] for item in actions if item["custody_disposition"] == "provider_reconciliation_only"]
    providerless = [item["action_id"] for item in actions if item["custody_disposition"] == "providerless_denial_only"]
    if value.get("reconciliation_action_ids") != reconciliation or value.get("providerless_denial_action_ids") != providerless:
        raise ValueError("Terminal custody inventories do not join action dispositions")
    if value.get("custody_finality") not in CUSTODY_FINALITIES or value["custody_finality"] != _finality(actions):
        raise ValueError("Terminal custody finality is invalid")
    result_sha = value.get("result_sha256")
    basis = {key: item for key, item in value.items() if key not in {"result_id", "result_sha256"}}
    expected = _digest(basis)
    if result_sha != expected or value.get("result_id") != f"nres_{expected[:24]}":
        raise ValueError("Terminal review result content identity is invalid")


def validate_terminal_review_result_v02_against_receipt(
    result: dict[str, Any], receipt: dict[str, Any],
) -> None:
    from .native_transitions import validate_native_publication_receipt
    validate_native_publication_receipt(receipt, result)


def validate_terminal_review_result_v02_against_api_actions(
    result: dict[str, Any], api_actions: list[dict[str, Any]],
) -> None:
    """Join result rows to API-owned immutable action/authorization evidence.

    The result's binding digest is a compact identity, not standalone authority.
    API ingress supplies its complete persisted binding for each native action.
    """
    validate_terminal_review_result_v02(result)
    if not isinstance(api_actions, list) or len(api_actions) != len(result["action_dispositions"]):
        raise ValueError("API action inventory does not cover the terminal result")
    expected_keys = {
        "native_run_id", "action_id", "binding", "route_family", "stage",
        "provider_operation_id",
    }
    by_id: dict[str, dict[str, Any]] = {}
    for item in api_actions:
        if not isinstance(item, dict) or set(item) != expected_keys:
            raise ValueError("API action join document shape is invalid")
        action_id = item.get("action_id")
        if not isinstance(action_id, str) or action_id in by_id:
            raise ValueError("API action join identity is invalid or duplicated")
        by_id[action_id] = item
    if set(by_id) != {item["action_id"] for item in result["action_dispositions"]}:
        raise ValueError("API action inventory differs from the terminal result")
    for row in result["action_dispositions"]:
        supplied = by_id[row["action_id"]]
        binding = _binding({"action_id": row["action_id"], "binding": supplied["binding"]})
        if (
            supplied["native_run_id"] != result["run_id"]
            or supplied["route_family"] != row["route_family"]
            or supplied["stage"] != row["stage"]
            or _digest(binding) != row["binding_sha256"]
            or supplied["provider_operation_id"] != row["provider_operation_id"]
        ):
            raise ValueError("Terminal result does not join immutable API action evidence")


def build_terminal_review_command_result(
    result: dict[str, Any], receipt: dict[str, Any],
) -> dict[str, Any]:
    validate_terminal_review_result_v02_against_receipt(result, receipt)
    value = {
        "schema_version": COMMAND_RESULT_SCHEMA,
        "outcome": "review_required",
        "exit_code": 2,
        "native_invocation_id": result["invocation_id"],
        "result_id": result["result_id"],
        "result_sha256": result["result_sha256"],
        "receipt_id": receipt["receipt_id"],
        "receipt_sha256": receipt["receipt_sha256"],
        "custody_finality": result["custody_finality"],
        "new_provider_create_permitted": False,
    }
    validate_terminal_review_command_result(value)
    return value


def validate_terminal_review_command_result(value: dict[str, Any]) -> None:
    keys = {
        "schema_version", "outcome", "exit_code", "native_invocation_id",
        "result_id", "result_sha256", "receipt_id", "receipt_sha256",
        "custody_finality", "new_provider_create_permitted",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Terminal review command result fields are invalid")
    if (
        value.get("schema_version") != COMMAND_RESULT_SCHEMA
        or value.get("outcome") != "review_required"
        or value.get("exit_code") != 2
        or value.get("new_provider_create_permitted") is not False
        or not _INVOCATION_ID.fullmatch(str(value.get("native_invocation_id")))
        or not _RESULT_ID.fullmatch(str(value.get("result_id")))
        or not _DIGEST.fullmatch(str(value.get("result_sha256")))
        or not re.fullmatch(r"^nreceipt_[0-9a-f]{24}$", str(value.get("receipt_id")))
        or not _DIGEST.fullmatch(str(value.get("receipt_sha256")))
        or value.get("custody_finality") not in CUSTODY_FINALITIES
    ):
        raise ValueError("Terminal review command result is invalid")


def validate_terminal_review_command_result_against_publication(
    command_result: dict[str, Any], result: dict[str, Any], receipt: dict[str, Any],
) -> None:
    """Join one exit-2 command result to its exact sealed publication."""
    validate_terminal_review_command_result(command_result)
    validate_terminal_review_result_v02_against_receipt(result, receipt)
    expected = build_terminal_review_command_result(result, receipt)
    if command_result != expected:
        raise ValueError(
            "Terminal review command result does not join exact publication"
        )


def read_terminal_review_result_v02_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        "contracts/terminal-review-result-v0.2.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def read_terminal_review_command_result_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        "contracts/terminal-review-command-result-v0.1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


__all__ = [
    "RESULT_SCHEMA", "COMMAND_RESULT_SCHEMA", "build_terminal_action_dispositions",
    "build_terminal_review_command_result",
    "build_terminal_review_result_v02", "read_terminal_review_result_v02_schema",
    "validate_terminal_review_result_v02",
    "validate_terminal_review_result_v02_against_receipt",
    "validate_terminal_review_result_v02_against_api_actions",
    "validate_terminal_review_command_result",
    "validate_terminal_review_command_result_against_publication",
    "read_terminal_review_command_result_schema",
]
