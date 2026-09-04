"""Writer-fenced preparation for external-authority v2 provider dispatch."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import logging
from importlib.resources import files
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence

from .external_authority_v2 import validate_external_authority_grant_v2
from .temporal_lifecycle import (
    inspect_temporal_lifecycle,
    validate_external_authority_request_v2_against_inspection,
)


logger = logging.getLogger(__name__)


INTENT_SCHEMA_V2 = "astrowoof.external_authority_dispatch_intent.v2"
INTENT_RESULT_SCHEMA_V2 = "astrowoof.external_authority_intent_result.v2"
PROVIDER_DISPATCH_RESULT_SCHEMA_V2 = "astrowoof.external_authority_provider_dispatch_result.v2"
COMMAND_RESULT_SCHEMA_V1 = "astrowoof.external_authority_v2_command_result.v1"
PROVIDER_DISPATCH_RESULT_SCHEMA_V3 = "astrowoof.external_authority_provider_dispatch_result.v3"
COMMAND_RESULT_SCHEMA_V2 = "astrowoof.external_authority_v2_command_result.v2"
PROVIDER_DISPATCH_RESULT_SCHEMA_V4 = "astrowoof.external_authority_provider_dispatch_result.v4"
COMMAND_RESULT_SCHEMA_V3 = "astrowoof.external_authority_v2_command_result.v3"
PROVIDER_DISPATCH_RESULT_SCHEMA_V5 = "astrowoof.external_authority_provider_dispatch_result.v5"
COMMAND_RESULT_SCHEMA_V4 = "astrowoof.external_authority_v2_command_result.v4"
RETIRED_INVOCATION_SCHEMA_V1 = (
    "astrowoof.external_authority_v2_retired_invocation.v1"
)
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_RESULT_KEYS = {
    "schema_version", "result_sha256", "outcome", "run_id", "request_sha256",
    "grant_sha256", "ordered_action_ids", "pre_state_revision",
    "post_state_revision", "post_snapshot_sha256", "provider_io_performed",
}
_PROVIDER_RESULT_KEYS = {
    "schema_version", "result_sha256", "outcome", "run_id", "request_sha256",
    "grant_sha256", "ordered_action_ids", "provider_bound_action_ids",
    "ambiguous_action_ids", "provider_operation_ids", "post_state_revision",
    "post_snapshot_sha256", "provider_io_performed",
}
_COMMAND_RESULT_KEYS = {
    "schema_version", "command_result_sha256", "outcome", "intent_result",
    "dispatch_result",
}
_PROVIDER_RESULT_V3_KEYS = {
    "schema_version", "result_sha256", "outcome", "reason_code",
    "provider_io_disposition", "grant_invocation_disposition", "run_id",
    "request_sha256", "grant_sha256", "ordered_action_ids",
    "provider_bound_action_ids", "ambiguous_action_ids", "refused_action_ids",
    "provider_operation_ids", "prepared_create_records", "post_state_revision",
    "post_snapshot_sha256",
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def validate_external_authority_intent_result_v2(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _RESULT_KEYS:
        raise ValueError("v2 intent result fields are not exact")
    if (
        value.get("schema_version") != INTENT_RESULT_SCHEMA_V2
        or value.get("outcome") != "intent_committed"
        or value.get("provider_io_performed") is not False
    ):
        raise ValueError("v2 intent result semantics are invalid")
    for key in ("run_id",):
        if not isinstance(value.get(key), str) or not value[key]:
            raise ValueError(f"v2 intent result {key} is invalid")
    for key in ("request_sha256", "grant_sha256", "post_snapshot_sha256"):
        item = value.get(key)
        if not isinstance(item, str) or len(item) != 64 or any(char not in "0123456789abcdef" for char in item):
            raise ValueError(f"v2 intent result {key} is invalid")
    ids = value.get("ordered_action_ids")
    if (
        not isinstance(ids, list) or not ids or ids != sorted(ids)
        or len(ids) != len(set(ids))
        or any(not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None for item in ids)
    ):
        raise ValueError("v2 intent result action order is invalid")
    before, after = value.get("pre_state_revision"), value.get("post_state_revision")
    if any(isinstance(item, bool) or not isinstance(item, int) or item < 0 for item in (before, after)) or after <= before:
        raise ValueError("v2 intent result revision transition is invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v2 intent result digest mismatch")
    return deepcopy(value)


def read_external_authority_intent_result_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-intent-result.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_authority_provider_dispatch_result_v2(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _PROVIDER_RESULT_KEYS:
        raise ValueError("v2 provider dispatch result fields are not exact")
    if value.get("schema_version") != PROVIDER_DISPATCH_RESULT_SCHEMA_V2:
        raise ValueError("v2 provider dispatch result schema is invalid")
    if value.get("outcome") not in {"detached_provider_pending", "ambiguous_submission", "exact_replay"}:
        raise ValueError("v2 provider dispatch outcome is invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("v2 provider dispatch run_id is invalid")
    for key in ("request_sha256", "grant_sha256", "post_snapshot_sha256"):
        item = value.get(key)
        if not isinstance(item, str) or len(item) != 64 or any(char not in "0123456789abcdef" for char in item):
            raise ValueError(f"v2 provider dispatch {key} is invalid")
    ordered = value.get("ordered_action_ids")
    bound = value.get("provider_bound_action_ids")
    ambiguous = value.get("ambiguous_action_ids")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
        or any(not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None for item in ordered)
        or not isinstance(bound, list) or not isinstance(ambiguous, list)
        or bound != ordered[:len(bound)]
        or any(item not in ordered for item in bound + ambiguous)
        or len(set(bound + ambiguous)) != len(bound + ambiguous)
    ):
        raise ValueError("v2 provider dispatch action inventory is invalid")
    operations = value.get("provider_operation_ids")
    if (
        not isinstance(operations, list) or len(operations) != len(bound)
        or len(operations) != len(set(operations))
        or any(not isinstance(item, str) or not item for item in operations)
    ):
        raise ValueError("v2 provider dispatch operation inventory is invalid")
    if value["outcome"] == "detached_provider_pending":
        if bound != ordered or ambiguous or value.get("provider_io_performed") is not True:
            raise ValueError("completed v2 provider dispatch semantics are invalid")
    elif value["outcome"] == "exact_replay":
        if bound != ordered or ambiguous or value.get("provider_io_performed") is not False:
            raise ValueError("replayed v2 provider dispatch semantics are invalid")
    elif (
        len(ambiguous) != 1 or value.get("provider_io_performed") is not True
        or ordered.index(ambiguous[0]) != len(bound)
    ):
        raise ValueError("ambiguous v2 provider dispatch semantics are invalid")
    revision = value.get("post_state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise ValueError("v2 provider dispatch revision is invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v2 provider dispatch result digest mismatch")
    return deepcopy(value)


def read_external_authority_provider_dispatch_result_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-provider-dispatch-result.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def build_external_authority_v2_command_result(
    *, intent_result: dict[str, Any] | None, dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    if intent_result is not None:
        validate_external_authority_intent_result_v2(intent_result)
    validate_external_authority_provider_dispatch_result_v2(dispatch_result)
    body = {
        "schema_version": COMMAND_RESULT_SCHEMA_V1,
        "outcome": dispatch_result["outcome"],
        "intent_result": deepcopy(intent_result),
        "dispatch_result": deepcopy(dispatch_result),
    }
    return validate_external_authority_v2_command_result({
        **body, "command_result_sha256": _digest(body),
    })


def validate_external_authority_v2_command_result(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COMMAND_RESULT_KEYS:
        raise ValueError("v2 command result fields are not exact")
    if value.get("schema_version") != COMMAND_RESULT_SCHEMA_V1:
        raise ValueError("v2 command result schema is invalid")
    dispatch = validate_external_authority_provider_dispatch_result_v2(
        value.get("dispatch_result")
    )
    intent = value.get("intent_result")
    if intent is not None:
        validate_external_authority_intent_result_v2(intent)
        if (
            intent["request_sha256"] != dispatch["request_sha256"]
            or intent["grant_sha256"] != dispatch["grant_sha256"]
            or intent["ordered_action_ids"] != dispatch["ordered_action_ids"]
        ):
            raise ValueError("v2 command intent and dispatch do not join")
    if value.get("outcome") != dispatch["outcome"]:
        raise ValueError("v2 command outcome does not join dispatch")
    body = {key: item for key, item in value.items() if key != "command_result_sha256"}
    if value.get("command_result_sha256") != _digest(body):
        raise ValueError("v2 command result digest mismatch")
    return deepcopy(value)


def read_external_authority_v2_command_result_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-command-result.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_authority_provider_dispatch_result_v3(value: Any) -> dict[str, Any]:
    """Validate the proposed phase-aware provider dispatch result contract."""
    if not isinstance(value, dict) or set(value) != _PROVIDER_RESULT_V3_KEYS:
        raise ValueError("v3 provider dispatch result fields are not exact")
    if value.get("schema_version") != PROVIDER_DISPATCH_RESULT_SCHEMA_V3:
        raise ValueError("v3 provider dispatch result schema is invalid")
    outcome = value.get("outcome")
    if outcome not in {
        "pre_provider_refusal", "ambiguous_submission",
        "detached_provider_pending", "exact_replay",
    }:
        raise ValueError("v3 provider dispatch outcome is invalid")
    if value.get("provider_io_disposition") not in {
        "not_attempted", "create_entered_unknown", "provider_identity_durable",
    }:
        raise ValueError("v3 provider I/O disposition is invalid")
    if value.get("grant_invocation_disposition") not in {
        "refused", "create_entered_unknown", "provider_pending", "replayed",
    }:
        raise ValueError("v3 grant invocation disposition is invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("v3 provider dispatch run_id is invalid")
    for key in ("request_sha256", "grant_sha256", "post_snapshot_sha256"):
        item = value.get(key)
        if (
            not isinstance(item, str) or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
        ):
            raise ValueError(f"v3 provider dispatch {key} is invalid")
    ordered = value.get("ordered_action_ids")
    bound = value.get("provider_bound_action_ids")
    ambiguous = value.get("ambiguous_action_ids")
    refused = value.get("refused_action_ids")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
        or any(not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None for item in ordered)
        or not isinstance(bound, list) or bound != ordered[:len(bound)]
        or not isinstance(ambiguous, list) or len(ambiguous) > 1
        or not isinstance(refused, list) or len(refused) > 1
        or any(item not in ordered for item in bound + ambiguous + refused)
        or len(set(bound + ambiguous + refused)) != len(bound + ambiguous + refused)
    ):
        raise ValueError("v3 provider dispatch action inventory is invalid")
    operations = value.get("provider_operation_ids")
    if (
        not isinstance(operations, list) or len(operations) != len(bound)
        or len(operations) != len(set(operations))
        or any(not isinstance(item, str) or not item for item in operations)
    ):
        raise ValueError("v3 provider dispatch operation inventory is invalid")
    prepared = value.get("prepared_create_records")
    attempted = bound + ambiguous + refused
    if not isinstance(prepared, list) or len(prepared) != len(attempted):
        raise ValueError("v3 prepared-create inventory is invalid")
    for index, record in enumerate(prepared):
        if not isinstance(record, dict) or set(record) != {
            "action_id", "prepared_create_sha256",
        }:
            raise ValueError("v3 prepared-create record fields are not exact")
        digest_value = record.get("prepared_create_sha256")
        if (
            record.get("action_id") != attempted[index]
            or not isinstance(digest_value, str) or len(digest_value) != 64
            or any(char not in "0123456789abcdef" for char in digest_value)
        ):
            raise ValueError("v3 prepared-create record is invalid")
    revision = value.get("post_state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise ValueError("v3 provider dispatch revision is invalid")
    reason = value.get("reason_code")
    closed_refusals = {
        "request_payload_unavailable", "request_payload_ambiguous",
        "request_payload_digest_mismatch", "provider_configuration_invalid",
        "checkpoint_changed_before_create",
    }
    closed_ambiguities = {
        "provider_call_interrupted_after_fence",
        "provider_transport_failed_without_identity",
        "provider_returned_invalid_identity", "provider_identity_conflict",
    }
    io = value["provider_io_disposition"]
    grant_disposition = value["grant_invocation_disposition"]
    if outcome == "pre_provider_refusal":
        if (
            io != "not_attempted" or grant_disposition != "refused"
            or reason not in closed_refusals or len(refused) != 1 or ambiguous
            or refused[0] != ordered[len(bound)]
        ):
            raise ValueError("v3 pre-provider refusal semantics are invalid")
    elif outcome == "ambiguous_submission":
        if (
            io != "create_entered_unknown"
            or grant_disposition != "create_entered_unknown"
            or reason not in closed_ambiguities or len(ambiguous) != 1 or refused
            or ambiguous[0] != ordered[len(bound)]
        ):
            raise ValueError("v3 ambiguous submission semantics are invalid")
    elif outcome == "detached_provider_pending":
        if (
            io != "provider_identity_durable" or grant_disposition != "provider_pending"
            or reason is not None or bound != ordered or ambiguous or refused
        ):
            raise ValueError("v3 detached provider-pending semantics are invalid")
    elif (
        io != "provider_identity_durable" or grant_disposition != "replayed"
        or reason is not None or bound != ordered or ambiguous or refused
    ):
        raise ValueError("v3 exact replay semantics are invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v3 provider dispatch result digest mismatch")
    return deepcopy(value)


def build_external_authority_provider_dispatch_result_v3(**fields: Any) -> dict[str, Any]:
    body = {"schema_version": PROVIDER_DISPATCH_RESULT_SCHEMA_V3, **deepcopy(fields)}
    return validate_external_authority_provider_dispatch_result_v3({
        **body, "result_sha256": _digest(body),
    })


def read_external_authority_provider_dispatch_result_v3_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-provider-dispatch-result.v3.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_authority_provider_dispatch_result_v4(
    value: Any,
) -> dict[str, Any]:
    """Validate the post-intent lifecycle-refusal result.

    V4 is deliberately narrow: it represents an all-member refusal after the
    aggregate intent checkpoint but before any provider call is entered.
    """
    if not isinstance(value, dict) or set(value) != _PROVIDER_RESULT_V3_KEYS:
        raise ValueError("v4 provider dispatch result fields are not exact")
    if value.get("schema_version") != PROVIDER_DISPATCH_RESULT_SCHEMA_V4:
        raise ValueError("v4 provider dispatch result schema is invalid")
    if (
        value.get("outcome") != "pre_provider_refusal"
        or value.get("reason_code") != "post_intent_lifecycle_contradiction"
        or value.get("provider_io_disposition") != "not_attempted"
        or value.get("grant_invocation_disposition") != "refused"
    ):
        raise ValueError("v4 provider dispatch result semantics are invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("v4 provider dispatch run_id is invalid")
    for key in ("request_sha256", "grant_sha256", "post_snapshot_sha256"):
        item = value.get(key)
        if (
            not isinstance(item, str) or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
        ):
            raise ValueError(f"v4 provider dispatch {key} is invalid")
    ordered = value.get("ordered_action_ids")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
        or any(
            not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None
            for item in ordered
        )
        or value.get("provider_bound_action_ids") != []
        or value.get("ambiguous_action_ids") != []
        or value.get("refused_action_ids") != ordered
        or value.get("provider_operation_ids") != []
        or value.get("prepared_create_records") != []
    ):
        raise ValueError("v4 provider dispatch action inventory is invalid")
    revision = value.get("post_state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise ValueError("v4 provider dispatch revision is invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v4 provider dispatch result digest mismatch")
    return deepcopy(value)


def build_external_authority_provider_dispatch_result_v4(
    **fields: Any,
) -> dict[str, Any]:
    body = {"schema_version": PROVIDER_DISPATCH_RESULT_SCHEMA_V4, **deepcopy(fields)}
    return validate_external_authority_provider_dispatch_result_v4({
        **body, "result_sha256": _digest(body),
    })


def read_external_authority_provider_dispatch_result_v4_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-provider-dispatch-result.v4.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_authority_provider_dispatch_result_v5(
    value: Any,
) -> dict[str, Any]:
    """Validate the no-dispatch result for an unresolved completed intent.

    This is deliberately distinct from v4: v4 follows a newly committed
    intent whose lifecycle changed, whereas v5 reports that an older completed
    intent still occupies the singleton slot. The presented grant is refused
    without changing native state or entering provider I/O.
    """
    if not isinstance(value, dict) or set(value) != _PROVIDER_RESULT_V3_KEYS:
        raise ValueError("v5 provider dispatch result fields are not exact")
    if (
        value.get("schema_version") != PROVIDER_DISPATCH_RESULT_SCHEMA_V5
        or value.get("outcome") != "pre_provider_refusal"
        or value.get("reason_code") != "completed_intent_retirement_required"
        or value.get("provider_io_disposition") != "not_attempted"
        or value.get("grant_invocation_disposition") != "refused"
    ):
        raise ValueError("v5 provider dispatch result semantics are invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("v5 provider dispatch run_id is invalid")
    for key in ("request_sha256", "grant_sha256", "post_snapshot_sha256"):
        item = value.get(key)
        if (
            not isinstance(item, str) or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
        ):
            raise ValueError(f"v5 provider dispatch {key} is invalid")
    ordered = value.get("ordered_action_ids")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
        or any(
            not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None
            for item in ordered
        )
        or value.get("provider_bound_action_ids") != []
        or value.get("ambiguous_action_ids") != []
        or value.get("refused_action_ids") != ordered
        or value.get("provider_operation_ids") != []
        or value.get("prepared_create_records") != []
    ):
        raise ValueError("v5 provider dispatch action inventory is invalid")
    revision = value.get("post_state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise ValueError("v5 provider dispatch revision is invalid")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value.get("result_sha256") != _digest(body):
        raise ValueError("v5 provider dispatch result digest mismatch")
    return deepcopy(value)


def build_external_authority_provider_dispatch_result_v5(
    **fields: Any,
) -> dict[str, Any]:
    body = {"schema_version": PROVIDER_DISPATCH_RESULT_SCHEMA_V5, **deepcopy(fields)}
    return validate_external_authority_provider_dispatch_result_v5({
        **body, "result_sha256": _digest(body),
    })


def read_external_authority_provider_dispatch_result_v5_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-provider-dispatch-result.v5.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def build_external_authority_v2_command_result_v2(
    *, intent_result: dict[str, Any] | None, dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    if intent_result is not None:
        validate_external_authority_intent_result_v2(intent_result)
    validate_external_authority_provider_dispatch_result_v3(dispatch_result)
    body = {
        "schema_version": COMMAND_RESULT_SCHEMA_V2,
        "outcome": dispatch_result["outcome"],
        "intent_result": deepcopy(intent_result),
        "dispatch_result": deepcopy(dispatch_result),
    }
    return validate_external_authority_v2_command_result_v2({
        **body, "command_result_sha256": _digest(body),
    })


def validate_external_authority_v2_command_result_v2(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COMMAND_RESULT_KEYS:
        raise ValueError("v2 command result fields are not exact")
    if value.get("schema_version") != COMMAND_RESULT_SCHEMA_V2:
        raise ValueError("v2 command result schema is invalid")
    dispatch = validate_external_authority_provider_dispatch_result_v3(
        value.get("dispatch_result")
    )
    intent = value.get("intent_result")
    if intent is not None:
        validate_external_authority_intent_result_v2(intent)
        if (
            intent["request_sha256"] != dispatch["request_sha256"]
            or intent["grant_sha256"] != dispatch["grant_sha256"]
            or intent["ordered_action_ids"] != dispatch["ordered_action_ids"]
        ):
            raise ValueError("v2 command intent and dispatch do not join")
    if value.get("outcome") != dispatch["outcome"]:
        raise ValueError("v2 command outcome does not join dispatch")
    body = {key: item for key, item in value.items() if key != "command_result_sha256"}
    if value.get("command_result_sha256") != _digest(body):
        raise ValueError("v2 command result digest mismatch")
    return deepcopy(value)


def read_external_authority_v2_command_result_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-command-result.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def build_external_authority_v2_command_result_v3(
    *, intent_result: dict[str, Any] | None, dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    if intent_result is not None:
        validate_external_authority_intent_result_v2(intent_result)
    validate_external_authority_provider_dispatch_result_v4(dispatch_result)
    body = {
        "schema_version": COMMAND_RESULT_SCHEMA_V3,
        "outcome": dispatch_result["outcome"],
        "intent_result": deepcopy(intent_result),
        "dispatch_result": deepcopy(dispatch_result),
    }
    return validate_external_authority_v2_command_result_v3({
        **body, "command_result_sha256": _digest(body),
    })


def build_external_authority_v2_command_result_v4(
    *, dispatch_result: dict[str, Any],
) -> dict[str, Any]:
    validate_external_authority_provider_dispatch_result_v5(dispatch_result)
    body = {
        "schema_version": COMMAND_RESULT_SCHEMA_V4,
        "outcome": dispatch_result["outcome"],
        "intent_result": None,
        "dispatch_result": deepcopy(dispatch_result),
    }
    return validate_external_authority_v2_command_result_v4({
        **body, "command_result_sha256": _digest(body),
    })


def validate_external_authority_v2_command_result_v4(
    value: Any,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "command_result_sha256", "outcome", "intent_result",
        "dispatch_result",
    }:
        raise ValueError("v4 command result fields are not exact")
    if value.get("schema_version") != COMMAND_RESULT_SCHEMA_V4:
        raise ValueError("v4 command result schema is invalid")
    dispatch = validate_external_authority_provider_dispatch_result_v5(
        value.get("dispatch_result")
    )
    if value.get("intent_result") is not None:
        raise ValueError("v4 unresolved-intent result cannot carry an intent result")
    if value.get("outcome") != dispatch["outcome"]:
        raise ValueError("v4 command outcome does not join dispatch")
    body = {key: item for key, item in value.items() if key != "command_result_sha256"}
    if value.get("command_result_sha256") != _digest(body):
        raise ValueError("v4 command result digest mismatch")
    return deepcopy(value)


def read_external_authority_v2_command_result_v4_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-command-result.v4.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_authority_v2_command_result_v3(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COMMAND_RESULT_KEYS:
        raise ValueError("v3 command result fields are not exact")
    if value.get("schema_version") != COMMAND_RESULT_SCHEMA_V3:
        raise ValueError("v3 command result schema is invalid")
    dispatch = validate_external_authority_provider_dispatch_result_v4(
        value.get("dispatch_result")
    )
    intent = value.get("intent_result")
    if intent is not None:
        validate_external_authority_intent_result_v2(intent)
        if (
            intent["request_sha256"] != dispatch["request_sha256"]
            or intent["grant_sha256"] != dispatch["grant_sha256"]
            or intent["ordered_action_ids"] != dispatch["ordered_action_ids"]
        ):
            raise ValueError("v3 command intent and dispatch do not join")
    if value.get("outcome") != dispatch["outcome"]:
        raise ValueError("v3 command outcome does not join dispatch")
    body = {
        key: item for key, item in value.items()
        if key != "command_result_sha256"
    }
    if value.get("command_result_sha256") != _digest(body):
        raise ValueError("v3 command result digest mismatch")
    return deepcopy(value)


def read_external_authority_v2_command_result_v3_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-command-result.v3.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_ambiguous_provider_submission_fixture_v1(
    value: Any,
) -> dict[str, Any]:
    """Strictly validate a packaged or caller-supplied fixture bundle."""
    if (
        not isinstance(value, dict)
        or set(value) != {"schema_version", "cases"}
        or value.get("schema_version")
        != "astrowoof.ambiguous_provider_submission_fixtures.v1"
        or not isinstance(value.get("cases"), list)
        or not value["cases"]
    ):
        raise ValueError("ambiguous provider submission fixture bundle is invalid")
    names: list[str] = []
    for case in value["cases"]:
        if (
            not isinstance(case, dict)
            or set(case) != {"name", "expected_valid", "result"}
            or not isinstance(case.get("name"), str) or not case["name"]
            or not isinstance(case.get("expected_valid"), bool)
        ):
            raise ValueError("ambiguous provider submission fixture case is invalid")
        names.append(case["name"])
        if case["expected_valid"]:
            validate_external_authority_provider_dispatch_result_v3(case["result"])
        else:
            try:
                validate_external_authority_provider_dispatch_result_v3(case["result"])
            except ValueError:
                pass
            else:
                raise ValueError("negative ambiguous provider fixture unexpectedly validates")
    if len(names) != len(set(names)):
        raise ValueError("ambiguous provider fixture names are not unique")
    return deepcopy(value)


def read_ambiguous_provider_submission_fixture_v1() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "external-authority-v2/ambiguous-provider-submission.v1.json"
    )
    return validate_ambiguous_provider_submission_fixture_v1(
        json.loads(path.read_text(encoding="utf-8"))
    )


class ExternalAuthorityV2ExecutionError(ValueError):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code


_PREPARED_CREATE_KEYS = {
    "outcome", "reason_code", "prepared_create_sha256", "transport_context",
}
_PREPARED_CREATE_BASIS_SCHEMA = "astrowoof.external_authority_prepared_create_basis.v1"


def build_external_authority_prepared_create_basis(
    action: Mapping[str, Any], *, run_id: str, request_sha256: str,
    grant_sha256: str, checkpoint_snapshot_sha256: str,
    local_request_key_sha256: str, provider_configuration_sha256: str,
    outcome: str, reason_code: str | None,
) -> dict[str, Any]:
    """Build the safe canonical digest basis shared by ready/refused preparation."""
    binding = action.get("binding")
    if not isinstance(binding, Mapping):
        raise ValueError("prepared-create action binding is unavailable")
    if outcome not in {"ready", "refused"}:
        raise ValueError("prepared-create outcome is invalid")
    closed_refusals = {
        "request_payload_unavailable", "request_payload_ambiguous",
        "request_payload_digest_mismatch", "provider_configuration_invalid",
    }
    if (outcome == "ready" and reason_code is not None) or (
        outcome == "refused" and reason_code not in closed_refusals
    ):
        raise ValueError("prepared-create reason is invalid")
    value = {
        "schema_version": _PREPARED_CREATE_BASIS_SCHEMA,
        "run_id": run_id,
        "action_id": action.get("action_id"),
        "request_sha256": request_sha256,
        "grant_sha256": grant_sha256,
        "binding_sha256": _digest(dict(binding)),
        "checkpoint_snapshot_sha256": checkpoint_snapshot_sha256,
        "local_request_key_sha256": local_request_key_sha256,
        "provider_configuration_sha256": provider_configuration_sha256,
        "outcome": outcome,
        "reason_code": reason_code,
    }
    if (
        not isinstance(run_id, str) or not run_id
        or not isinstance(value["action_id"], str)
        or _ACTION_ID.fullmatch(value["action_id"]) is None
    ):
        raise ValueError("prepared-create native identity is invalid")
    for key in (
        "request_sha256", "grant_sha256", "binding_sha256",
        "checkpoint_snapshot_sha256", "local_request_key_sha256",
        "provider_configuration_sha256",
    ):
        item = value[key]
        if (
            not isinstance(item, str) or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
        ):
            raise ValueError(f"prepared-create {key} is invalid")
    return value


def build_external_authority_prepared_create(
    *, basis: Mapping[str, Any], transport_context: Any,
) -> dict[str, Any]:
    value = {
        "outcome": basis.get("outcome"),
        "reason_code": basis.get("reason_code"),
        "prepared_create_sha256": _digest(dict(basis)),
        "transport_context": transport_context,
    }
    return _validate_prepared_create(value)


def _validate_prepared_create(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _PREPARED_CREATE_KEYS:
        raise ValueError("prepared-create fields are not exact")
    if value.get("outcome") not in {"ready", "refused"}:
        raise ValueError("prepared-create outcome is invalid")
    reason = value.get("reason_code")
    if (value["outcome"] == "ready" and reason is not None) or (
        value["outcome"] == "refused" and reason not in {
            "request_payload_unavailable", "request_payload_ambiguous",
            "request_payload_digest_mismatch", "provider_configuration_invalid",
        }
    ):
        raise ValueError("prepared-create reason is invalid")
    digest_value = value.get("prepared_create_sha256")
    if (
        not isinstance(digest_value, str) or len(digest_value) != 64
        or any(char not in "0123456789abcdef" for char in digest_value)
    ):
        raise ValueError("prepared-create digest is invalid")
    return value


def _inject(callback: Callable[[str], None] | None, point: str) -> None:
    if callback is not None:
        callback(point)


def _current_actions(state: Mapping[str, Any], action_ids: list[str]) -> list[dict[str, Any]]:
    actions = (state.get("spend_ledger") or {}).get("actions")
    if not isinstance(actions, list):
        raise ExternalAuthorityV2ExecutionError(
            "action_state_or_custody_mismatch", "native spend ledger is unavailable",
        )
    by_id = {item.get("action_id"): item for item in actions if isinstance(item, dict)}
    if len(by_id) != len(actions) or any(action_id not in by_id for action_id in action_ids):
        raise ExternalAuthorityV2ExecutionError(
            "member_inventory_mismatch", "native action inventory is missing or duplicated",
        )
    return [by_id[action_id] for action_id in action_ids]


def _strict_sha256(value: Any, *, label: str) -> str:
    if (
        not isinstance(value, str) or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", f"{label} is invalid",
        )
    return value


def _validate_retired_invocation(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "outcome", "request_schema_version",
        "request_sha256", "checkpoint_basis_sha256", "grant_schema_version",
        "grant_sha256", "api_decision_id", "ordering_semantics",
        "ordered_action_ids", "ordered_authorization_document_sha256s",
        "provider_bound_action_ids", "provider_operation_ids",
        "prepared_create_records", "terminal_action_records",
        "terminal_evidence_sha256", "retirement_state_revision",
        "retirement_record_sha256",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired invocation fields are not exact",
        )
    if (
        value.get("schema_version") != RETIRED_INVOCATION_SCHEMA_V1
        or value.get("outcome") != "provider_completed"
        or value.get("request_schema_version")
        != "astrowoof.external_authority_request.v2"
        or value.get("grant_schema_version")
        != "astrowoof.external_authority_grant.v2"
        or value.get("ordering_semantics") != "lexical_action_id_ascending"
        or not isinstance(value.get("api_decision_id"), str)
        or not value["api_decision_id"]
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired invocation identity is invalid",
        )
    for key in (
        "request_sha256", "checkpoint_basis_sha256", "grant_sha256",
        "terminal_evidence_sha256", "retirement_record_sha256",
    ):
        _strict_sha256(value.get(key), label=f"retired invocation {key}")
    ordered = value.get("ordered_action_ids")
    bound = value.get("provider_bound_action_ids")
    operations = value.get("provider_operation_ids")
    authorization_digests = value.get(
        "ordered_authorization_document_sha256s"
    )
    prepared = value.get("prepared_create_records")
    terminal = value.get("terminal_action_records")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
        or any(
            not isinstance(item, str) or _ACTION_ID.fullmatch(item) is None
            for item in ordered
        )
        or bound != ordered
        or not isinstance(operations, list) or len(operations) != len(ordered)
        or len(operations) != len(set(operations))
        or any(not isinstance(item, str) or not item for item in operations)
        or not isinstance(authorization_digests, list)
        or len(authorization_digests) != len(ordered)
        or not isinstance(prepared, list) or len(prepared) != len(ordered)
        or not isinstance(terminal, list) or len(terminal) != len(ordered)
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired invocation inventory is invalid",
        )
    for digest_value in authorization_digests:
        _strict_sha256(
            digest_value, label="retired authorization document digest",
        )
    for index, record in enumerate(prepared):
        if (
            not isinstance(record, dict)
            or set(record) != {"action_id", "prepared_create_sha256"}
            or record.get("action_id") != ordered[index]
        ):
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid", "retired prepared-create join is invalid",
            )
        _strict_sha256(
            record.get("prepared_create_sha256"),
            label="retired prepared-create digest",
        )
    terminal_keys = {
        "action_id", "binding_sha256", "authorization_document_sha256",
        "authorization_reference", "consumption_sha256", "provider_kind",
        "provider_operation_id", "reconciliation_evidence_sha256",
        "reported_evidence_sha256", "response_artifact",
    }
    for index, record in enumerate(terminal):
        if (
            not isinstance(record, dict) or set(record) != terminal_keys
            or record.get("action_id") != ordered[index]
            or record.get("provider_operation_id") != operations[index]
            or record.get("provider_kind") != "response"
            or not isinstance(record.get("authorization_reference"), str)
            or not record["authorization_reference"]
        ):
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid", "retired terminal-action join is invalid",
            )
        for key in (
            "binding_sha256", "authorization_document_sha256",
            "consumption_sha256", "reconciliation_evidence_sha256",
            "reported_evidence_sha256",
        ):
            _strict_sha256(record.get(key), label=f"retired action {key}")
        artifact = record.get("response_artifact")
        if (
            not isinstance(artifact, dict)
            or set(artifact) != {"logical_path", "bytes", "sha256"}
            or not isinstance(artifact.get("logical_path"), str)
            or not artifact["logical_path"]
            or isinstance(artifact.get("bytes"), bool)
            or not isinstance(artifact.get("bytes"), int)
            or artifact["bytes"] < 1
        ):
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid", "retired response artifact is invalid",
            )
        _strict_sha256(
            artifact.get("sha256"), label="retired response artifact digest",
        )
    if value["terminal_evidence_sha256"] != _digest(terminal):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired terminal evidence digest mismatch",
        )
    revision = value.get("retirement_state_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired invocation revision is invalid",
        )
    body = {
        key: item for key, item in value.items()
        if key != "retirement_record_sha256"
    }
    if value["retirement_record_sha256"] != _digest(body):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "retired invocation digest mismatch",
        )
    return deepcopy(value)


def retire_completed_external_authority_v2_intent(
    state: dict[str, Any], run_dir: Path | str,
) -> dict[str, Any] | None:
    """Retire one completely terminal ordinary-v2 intent without persistence.

    The caller owns the native writer and must persist state plus publish and
    validate one workspace snapshot before exposing the mutation.
    """
    from .closure import load_json, sha256_file

    intent = state.get("external_authority_v2_dispatch_intent")
    if intent is None:
        return None
    if not isinstance(intent, dict):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "live v2 dispatch intent is malformed",
        )
    ordered = intent.get("ordered_action_ids")
    if (
        not isinstance(ordered, list) or not ordered or ordered != sorted(ordered)
        or len(ordered) != len(set(ordered))
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "live v2 dispatch inventory is invalid",
        )
    actions = _current_actions(state, ordered)
    if any(action.get("state") != "REPORTED" for action in actions):
        return None
    if (
        intent.get("schema_version") != INTENT_SCHEMA_V2
        or intent.get("state") != "PROVIDER_PENDING"
        or intent.get("next_action_index") != len(ordered)
        or intent.get("active_action_id") is not None
        or intent.get("active_create_state") is not None
        or intent.get("provider_io_performed") is not True
        or intent.get("provider_bound_action_ids") != ordered
        or not isinstance(intent.get("provider_operation_ids"), list)
        or len(intent["provider_operation_ids"]) != len(ordered)
        or not isinstance(intent.get("prepared_create_records"), list)
        or len(intent["prepared_create_records"]) != len(ordered)
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid",
            "terminal actions do not join one complete live v2 intent",
        )
    root = Path(run_dir).resolve()
    authorization_digests = intent.get(
        "ordered_authorization_document_sha256s"
    )
    if (
        not isinstance(authorization_digests, list)
        or len(authorization_digests) != len(ordered)
    ):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "intent authorization inventory is invalid",
        )
    terminal_records: list[dict[str, Any]] = []
    for index, action in enumerate(actions):
        binding = action.get("binding")
        authorization = action.get("authorization")
        consumption = action.get("consumption")
        provider = action.get("provider")
        reconciliation = action.get("provider_reconciliation")
        reported = action.get("reported")
        provider_id = intent["provider_operation_ids"][index]
        if (
            not isinstance(binding, dict)
            or not isinstance(authorization, dict)
            or _digest(authorization) != authorization_digests[index]
            or authorization.get("action_id") != action["action_id"]
            or authorization.get("binding") != binding
            or not isinstance(
                authorization.get("authorization_reference"), str
            )
            or not authorization["authorization_reference"]
            or not isinstance(consumption, dict)
            or consumption.get("consumer_id")
            != f"external-grant-v2:{intent.get('api_decision_id')}"
            or not isinstance(consumption.get("state_revision"), int)
            or not isinstance(provider, dict)
            or provider != {"kind": "response", "id": provider_id}
            or not isinstance(reconciliation, dict)
            or reconciliation.get("last_outcome") != "completed"
            or reconciliation.get("resume_not_before") is not None
            or action.get("ambiguity") is not None
            or not isinstance(reported, dict)
            or (
                not isinstance(reported.get("usage"), dict)
                and reported.get("cost_disposition")
                != "provider_usage_unavailable_billing_reconciliation_pending"
            )
        ):
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid",
                "reported action does not join complete terminal intent evidence",
            )
        response_path = (
            root / "lifecycle" / "provider-reconciliation"
            / f"{action['action_id']}.response.json"
        )
        if not response_path.is_file():
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid",
                "terminal intent response artifact is unavailable",
            )
        try:
            response = load_json(response_path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid",
                "terminal intent response artifact is invalid",
            ) from exc
        if response.get("id") != provider_id or response.get("status") != "completed":
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid",
                "terminal response identity or status conflicts with intent",
            )
        terminal_records.append({
            "action_id": action["action_id"],
            "binding_sha256": _digest(binding),
            "authorization_document_sha256": _digest(authorization),
            "authorization_reference": authorization["authorization_reference"],
            "consumption_sha256": _digest(consumption),
            "provider_kind": "response",
            "provider_operation_id": provider_id,
            "reconciliation_evidence_sha256": _digest(reconciliation),
            "reported_evidence_sha256": _digest(reported),
            "response_artifact": {
                "logical_path": response_path.relative_to(root).as_posix(),
                "bytes": response_path.stat().st_size,
                "sha256": sha256_file(response_path),
            },
        })
    body = {
        "schema_version": RETIRED_INVOCATION_SCHEMA_V1,
        "outcome": "provider_completed",
        "request_schema_version": intent.get("request_schema_version"),
        "request_sha256": intent.get("request_sha256"),
        "checkpoint_basis_sha256": intent.get("checkpoint_basis_sha256"),
        "grant_schema_version": intent.get("grant_schema_version"),
        "grant_sha256": intent.get("grant_sha256"),
        "api_decision_id": intent.get("api_decision_id"),
        "ordering_semantics": intent.get("ordering_semantics"),
        "ordered_action_ids": deepcopy(ordered),
        "ordered_authorization_document_sha256s": deepcopy(
            authorization_digests
        ),
        "provider_bound_action_ids": deepcopy(
            intent["provider_bound_action_ids"]
        ),
        "provider_operation_ids": deepcopy(intent["provider_operation_ids"]),
        "prepared_create_records": deepcopy(intent["prepared_create_records"]),
        "terminal_action_records": terminal_records,
        "terminal_evidence_sha256": _digest(terminal_records),
        "retirement_state_revision": int(state.get("state_revision") or 0) + 1,
    }
    record = _validate_retired_invocation({
        **body, "retirement_record_sha256": _digest(body),
    })
    history = state.setdefault("external_authority_v2_dispatch_history", [])
    if not isinstance(history, list):
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "v2 dispatch history is malformed",
        )
    matches = [
        item for item in history
        if isinstance(item, dict)
        and item.get("request_sha256") == record["request_sha256"]
        and item.get("grant_sha256") == record["grant_sha256"]
    ]
    if matches:
        raise ExternalAuthorityV2ExecutionError(
            "native_evidence_invalid", "terminal v2 intent history is duplicated",
        )
    history.append(record)
    state.pop("external_authority_v2_dispatch_intent", None)
    logger.info(
        "external_authority_intent_retired request=%s grant=%s actions=%s "
        "retirement_revision=%s",
        record["request_sha256"], record["grant_sha256"], len(ordered),
        record["retirement_state_revision"],
    )
    return deepcopy(record)


def is_completed_external_authority_v2_intent_stale(
    state: Mapping[str, Any], run_dir: Path | str, *, request_sha256: str,
    grant_sha256: str,
) -> bool:
    """Return whether a different, fully completed live v2 intent blocks a grant.

    This is deliberately narrower than ``action_state_or_custody_mismatch``.
    It reuses the retirement proof on an isolated copy: only an intent that
    could be retired safely *now*, and whose request/grant differ from the
    presented authority, is the stale-completed-intent CLI refusal.  Invalid,
    pending, ambiguous, or otherwise incomplete live intent evidence remains
    on its existing fail-closed path.
    """
    try:
        record = retire_completed_external_authority_v2_intent(
            deepcopy(dict(state)), run_dir,
        )
    except ExternalAuthorityV2ExecutionError:
        return False
    return bool(
        record is not None
        and (
            record["request_sha256"] != request_sha256
            or record["grant_sha256"] != grant_sha256
        )
    )


def _validate_dispatchable(actions: Sequence[Mapping[str, Any]]) -> None:
    for action in actions:
        if action.get("provider") is not None:
            raise ExternalAuthorityV2ExecutionError(
                "provider_evidence_present", "provider identity already exists; reconciliation only",
            )
        if action.get("state") in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}:
            raise ExternalAuthorityV2ExecutionError(
                "provider_submission_ambiguous", "action is already submitting or ambiguous",
            )
        if action.get("consumption") is not None:
            raise ExternalAuthorityV2ExecutionError(
                "action_state_or_custody_mismatch", "authorization consumption already exists",
            )
        if action.get("state") != "PREPARED":
            raise ExternalAuthorityV2ExecutionError(
                "action_state_or_custody_mismatch", "action is not providerless PREPARED work",
            )


def _validate_supported_ordinary_dispatch(
    state: Mapping[str, Any], actions: Sequence[Mapping[str, Any]],
) -> None:
    bounded = (
        state.get("route_contract") == "astrowoof.bounded_natal.authoring_run.v2"
        and state.get("route") == "bounded_natal.v2"
    )
    exact = (
        state.get("schema_version") == "astrowoof.semantic_closure_run.v0.9"
        and state.get("route_contract") is None
    )
    if not (exact or bounded):
        raise ExternalAuthorityV2ExecutionError(
            "unsupported_contract", "v2 ordinary dispatch route family is unsupported",
        )
    supported_stages = {
        "creative_retry", "polish", "qualitative_critic", "qualitative_candidate",
    }
    for action in actions:
        binding = action.get("binding") or {}
        route = str(binding.get("route") or "")
        if (
            binding.get("service_level") != "interactive"
            or binding.get("stage") not in supported_stages
            or not route
            or (bounded and not route.startswith("bounded_natal.v2:"))
        ):
            raise ExternalAuthorityV2ExecutionError(
                "unsupported_contract",
                "v2 ordinary dispatch adapter is unsupported for this route/stage/mechanism",
            )


def commit_external_authority_v2_dispatch_intent(
    run_dir: Path | str, *, request: dict[str, Any], inspection: dict[str, Any],
    grant: dict[str, Any], authorization_documents: Sequence[Mapping[str, Any]],
    failure_injector: Callable[[str], None] | None = None,
    event_emitter: Any | None = None,
) -> dict[str, Any]:
    """Atomically publish grant+inventory+authorization+intent before provider I/O."""
    from .closure import (
        load_json, normalized_path, persist_state, sha256_file,
        validate_workspace_snapshot, write_workspace_snapshot,
    )
    from .lifecycle import _exclusive_lifecycle_lock
    from .spend import authorize_action, begin_submission

    root = Path(run_dir).resolve()
    run_json = root / "run.json"
    _inject(failure_injector, "before_writer_acquisition")
    with _exclusive_lifecycle_lock(root):
        state = load_json(run_json)
        try:
            validate_workspace_snapshot(root, state)
        except ValueError as exc:
            raise ExternalAuthorityV2ExecutionError("snapshot_invalid", str(exc)) from exc
        _inject(failure_injector, "after_snapshot_validation")
        if normalized_path(root) != inspection["checkpoint_basis"]["observation"]["logical_workspace_root"]:
            raise ExternalAuthorityV2ExecutionError(
                "stale_checkpoint_basis", "logical workspace root does not join inspection",
            )
        ids = request.get("ordered_action_ids") or []
        # Provider-safety evidence takes precedence over generic basis staleness.
        current_actions = _current_actions(state, ids)
        _validate_dispatchable(current_actions)
        _validate_supported_ordinary_dispatch(state, current_actions)
        observation = inspection["temporal_decision"]["observed_at"]
        access = inspection["checkpoint_basis"]["observation"]["native_exclusive_access"]
        current = inspect_temporal_lifecycle(
            root, native_exclusive_access=access, observed_at=observation,
        )
        try:
            validate_external_authority_request_v2_against_inspection(request, current)
        except ValueError as exc:
            raise ExternalAuthorityV2ExecutionError(
                "stale_checkpoint_basis", str(exc),
            ) from exc
        if current != inspection:
            raise ExternalAuthorityV2ExecutionError(
                "stale_checkpoint_basis", "supplied inspection is not the current exact inspection",
            )
        try:
            validate_external_authority_grant_v2(
                request, current, grant, authorization_documents,
            )
        except ValueError as exc:
            raise ExternalAuthorityV2ExecutionError(
                "authorization_mismatch", str(exc),
            ) from exc
        if event_emitter is not None:
            event_emitter.emit("external_authority.request_selected", data={
                "request_sha256": request["external_authority_request_sha256"],
                "request_kind": request["request_kind"],
                "action_count": len(ids),
                "selected_command": "external_authority_v2_dispatch",
            }, correlation={"native_run_id": str(state.get("run_id") or "")})
            event_emitter.emit("external_authority.fence_validated", data={
                "request_sha256": request["external_authority_request_sha256"],
                "grant_sha256": grant["grant_sha256"],
                "action_count": len(ids),
            }, correlation={"native_run_id": str(state.get("run_id") or "")})
        _inject(failure_injector, "after_request_and_grant_validation")
        if request["request_kind"] != "ordinary_action_set":
            raise ExternalAuthorityV2ExecutionError(
                "unsupported_contract", "v2 intent supports ordinary_action_set only",
            )
        existing = state.get("external_authority_v2_dispatch_intent")
        if existing is not None:
            raise ExternalAuthorityV2ExecutionError(
                "exact_replay" if (
                    existing.get("request_sha256") == request["external_authority_request_sha256"]
                    and existing.get("grant_sha256") == grant["grant_sha256"]
                ) else "action_state_or_custody_mismatch",
                "a native v2 dispatch intent already exists",
            )
        ids = request["ordered_action_ids"]
        candidate = deepcopy(state)
        candidate_actions = _current_actions(candidate, ids)
        for document in authorization_documents:
            authorize_action(candidate["spend_ledger"], dict(document))
        _inject(failure_injector, "after_candidate_authorization")
        consumer_id = f"external-grant-v2:{grant['api_decision_id']}"
        for action in candidate_actions:
            begin_submission(
                action, consumer_id=consumer_id,
                state_revision=int(candidate.get("state_revision") or 0),
            )
        candidate["external_authority_v2_dispatch_intent"] = {
            "schema_version": INTENT_SCHEMA_V2,
            "request_schema_version": request["schema_version"],
            "request_sha256": request["external_authority_request_sha256"],
            "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
            "grant_schema_version": grant["schema_version"],
            "grant_sha256": grant["grant_sha256"],
            "api_decision_id": grant["api_decision_id"],
            "ordering_semantics": grant["ordering_semantics"],
            "ordered_action_ids": deepcopy(ids),
            "ordered_authorization_document_sha256s": [
                item["authorization_document_sha256"]
                for item in grant["ordered_member_authorizations"]
            ],
            "state": "INTENT_COMMITTED",
            "next_action_index": 0,
            "provider_bound_action_ids": [],
            "provider_operation_ids": [],
            "prepared_create_records": [],
            "active_action_id": None,
            "active_create_state": None,
            "provider_io_performed": False,
        }
        _inject(failure_injector, "before_intent_persistence")
        persist_state(run_json, candidate)
        _inject(failure_injector, "after_state_before_snapshot")
        write_workspace_snapshot(root)
        validate_workspace_snapshot(root, candidate)
        _inject(failure_injector, "after_complete_intent_checkpoint")
        if event_emitter is not None:
            event_emitter.emit("external_authority.intent_committed", data={
                "request_sha256": request["external_authority_request_sha256"],
                "grant_sha256": grant["grant_sha256"],
                "action_count": len(ids),
                "state_revision": int(candidate["state_revision"]),
            }, correlation={"native_run_id": str(candidate.get("run_id") or "")})
        result = {
            "schema_version": INTENT_RESULT_SCHEMA_V2,
            "result_sha256": "pending",
            "outcome": "intent_committed",
            "run_id": candidate["run_id"],
            "request_sha256": request["external_authority_request_sha256"],
            "grant_sha256": grant["grant_sha256"],
            "ordered_action_ids": deepcopy(ids),
            "pre_state_revision": int(state.get("state_revision") or 0),
            "post_state_revision": int(candidate["state_revision"]),
            "post_snapshot_sha256": sha256_file(root / "workspace-snapshot.json"),
            "provider_io_performed": False,
        }
        result["result_sha256"] = _digest({
            key: item for key, item in result.items() if key != "result_sha256"
        })
        return validate_external_authority_intent_result_v2(result)


def dispatch_external_authority_v2_intent(
    run_dir: Path | str, *, request_sha256: str, grant_sha256: str,
    create: Callable[[dict[str, Any]], Mapping[str, Any]],
    prepare: Callable[[dict[str, Any], dict[str, Any]], Mapping[str, Any]] | None = None,
    failure_injector: Callable[[str], None] | None = None,
    event_emitter: Any | None = None,
) -> dict[str, Any]:
    """Dispatch a frozen ordinary-action intent, checkpointing each ID in order.

    The caller supplies transport only. The persisted intent selects the complete
    lexical inventory; callers cannot choose a subset. Provider output is not
    retrieved or ingested here.
    """
    from .closure import (
        load_json, persist_state, sha256_file, validate_workspace_snapshot,
        write_workspace_snapshot,
    )
    from .lifecycle import _exclusive_lifecycle_lock
    from .reconciliation import initial_timing
    from .spend import mark_ambiguous, record_provider_id

    root = Path(run_dir).resolve()
    run_json = root / "run.json"
    phase_aware = prepare is not None

    def emit(name: str, *, data: dict[str, Any], action_id: str | None = None) -> None:
        if event_emitter is None:
            return
        correlation = {"native_run_id": str(state.get("run_id") or "")}
        if action_id is not None:
            correlation["action_id"] = action_id
        try:
            event_emitter.emit(name, data=data, correlation=correlation)
        except Exception as exc:
            logger.warning(
                "provider_dispatch_diagnostic_sink_failed event=%s error_class=%s",
                name, type(exc).__name__,
            )

    def now() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def load_intent_state() -> tuple[dict[str, Any], dict[str, Any], list[str]]:
        state = load_json(run_json)
        validate_workspace_snapshot(root, state)
        intent = state.get("external_authority_v2_dispatch_intent")
        if not isinstance(intent, dict) or intent.get("state") not in {
            "INTENT_COMMITTED", "DISPATCHING", "PROVIDER_PENDING",
            "AMBIGUOUS_PROVIDER_SUBMISSION",
        }:
            raise ExternalAuthorityV2ExecutionError(
                "dispatch_intent_unavailable", "a complete v2 dispatch intent is unavailable",
            )
        if (
            intent.get("request_sha256") != request_sha256
            or intent.get("grant_sha256") != grant_sha256
        ):
            raise ExternalAuthorityV2ExecutionError(
                "authorization_mismatch", "dispatch identity does not match native intent",
            )
        ids = intent.get("ordered_action_ids")
        if not isinstance(ids, list) or ids != sorted(ids) or not ids:
            raise ExternalAuthorityV2ExecutionError(
                "member_inventory_mismatch", "native intent inventory is invalid",
            )
        return state, intent, ids

    def replay_history(state: dict[str, Any]) -> dict[str, Any] | None:
        history = state.get("external_authority_v2_dispatch_history") or []
        matches = [
            item for item in history
            if isinstance(item, dict)
            and item.get("request_sha256") == request_sha256
            and item.get("grant_sha256") == grant_sha256
        ]
        if not matches:
            return None
        if len(matches) != 1:
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid", "dispatch invocation history is duplicated",
            )
        item = matches[0]
        if item.get("outcome") == "provider_completed":
            retired = _validate_retired_invocation(item)
            if phase_aware:
                return build_external_authority_provider_dispatch_result_v3(
                    outcome="exact_replay",
                    reason_code=None,
                    provider_io_disposition="provider_identity_durable",
                    grant_invocation_disposition="replayed",
                    run_id=state["run_id"],
                    request_sha256=request_sha256,
                    grant_sha256=grant_sha256,
                    ordered_action_ids=deepcopy(retired["ordered_action_ids"]),
                    provider_bound_action_ids=deepcopy(
                        retired["provider_bound_action_ids"]
                    ),
                    ambiguous_action_ids=[],
                    refused_action_ids=[],
                    provider_operation_ids=deepcopy(
                        retired["provider_operation_ids"]
                    ),
                    prepared_create_records=deepcopy(
                        retired["prepared_create_records"]
                    ),
                    post_state_revision=int(state["state_revision"]),
                    post_snapshot_sha256=sha256_file(
                        root / "workspace-snapshot.json"
                    ),
                )
            body = {
                "schema_version": PROVIDER_DISPATCH_RESULT_SCHEMA_V2,
                "outcome": "exact_replay",
                "run_id": state["run_id"],
                "request_sha256": request_sha256,
                "grant_sha256": grant_sha256,
                "ordered_action_ids": deepcopy(retired["ordered_action_ids"]),
                "provider_bound_action_ids": deepcopy(
                    retired["provider_bound_action_ids"]
                ),
                "ambiguous_action_ids": [],
                "provider_operation_ids": deepcopy(
                    retired["provider_operation_ids"]
                ),
                "post_state_revision": int(state["state_revision"]),
                "post_snapshot_sha256": sha256_file(
                    root / "workspace-snapshot.json"
                ),
                "provider_io_performed": False,
            }
            return validate_external_authority_provider_dispatch_result_v2({
                **body, "result_sha256": _digest(body),
            })
        if not phase_aware or item.get("outcome") != "pre_provider_refusal":
            raise ExternalAuthorityV2ExecutionError(
                "native_evidence_invalid", "dispatch history outcome is unsupported",
            )
        if item.get("reason_code") == "post_intent_lifecycle_contradiction":
            refused_ids = item.get("refused_action_ids")
            if refused_ids != item.get("ordered_action_ids"):
                raise ExternalAuthorityV2ExecutionError(
                    "native_evidence_invalid",
                    "post-intent refusal inventory is invalid",
                )
            return build_external_authority_provider_dispatch_result_v4(
                outcome="pre_provider_refusal",
                reason_code=item["reason_code"],
                provider_io_disposition="not_attempted",
                grant_invocation_disposition="refused",
                run_id=state["run_id"],
                request_sha256=request_sha256,
                grant_sha256=grant_sha256,
                ordered_action_ids=deepcopy(item["ordered_action_ids"]),
                provider_bound_action_ids=[],
                ambiguous_action_ids=[],
                refused_action_ids=deepcopy(refused_ids),
                provider_operation_ids=[],
                prepared_create_records=[],
                post_state_revision=int(item["post_state_revision"]),
                post_snapshot_sha256=sha256_file(root / "workspace-snapshot.json"),
            )
        return build_external_authority_provider_dispatch_result_v3(
            outcome="pre_provider_refusal",
            reason_code=item["reason_code"],
            provider_io_disposition="not_attempted",
            grant_invocation_disposition="refused",
            run_id=state["run_id"],
            request_sha256=request_sha256,
            grant_sha256=grant_sha256,
            ordered_action_ids=deepcopy(item["ordered_action_ids"]),
            provider_bound_action_ids=deepcopy(item["provider_bound_action_ids"]),
            ambiguous_action_ids=[],
            refused_action_ids=[item["refused_action_id"]],
            provider_operation_ids=deepcopy(item["provider_operation_ids"]),
            prepared_create_records=deepcopy(item["prepared_create_records"]),
            post_state_revision=int(item["post_state_revision"]),
            post_snapshot_sha256=sha256_file(root / "workspace-snapshot.json"),
        )

    with _exclusive_lifecycle_lock(root):
        replay_state = load_json(run_json)
        validate_workspace_snapshot(root, replay_state)
        historical_replay = replay_history(replay_state)
        if historical_replay is not None:
            return historical_replay
        state, intent, ordered_ids = load_intent_state()
        if phase_aware and (
            intent.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION"
            or intent.get("active_create_state") == "CALL_ENTERED"
        ):
            active_id = intent.get("active_action_id")
            if active_id not in ordered_ids:
                raise ExternalAuthorityV2ExecutionError(
                    "native_evidence_invalid", "ambiguous intent action identity is invalid",
                )
            if intent.get("active_create_state") == "CALL_ENTERED":
                action = _current_actions(state, ordered_ids)[ordered_ids.index(active_id)]
                if action.get("provider") is not None:
                    raise ExternalAuthorityV2ExecutionError(
                        "provider_identity_conflict", "entered action now has provider identity",
                    )
                if action.get("state") == "SUBMITTING":
                    mark_ambiguous(
                        action, reason="durable provider call fence has no durable identity",
                    )
                elif action.get("state") != "AMBIGUOUS_PROVIDER_SUBMISSION":
                    raise ExternalAuthorityV2ExecutionError(
                        "native_evidence_invalid", "entered action state is contradictory",
                    )
                prepared_digest = intent.get("active_prepared_create_sha256")
                records = deepcopy(intent.get("prepared_create_records") or [])
                if (
                    not isinstance(prepared_digest, str)
                    or len(prepared_digest) != 64
                    or any(char not in "0123456789abcdef" for char in prepared_digest)
                ):
                    raise ExternalAuthorityV2ExecutionError(
                        "native_evidence_invalid", "entered call lacks prepared-create identity",
                    )
                records.append({
                    "action_id": active_id,
                    "prepared_create_sha256": prepared_digest,
                })
                intent["prepared_create_records"] = records
                intent["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                intent["active_create_state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                intent["ambiguity_reason_code"] = "provider_call_interrupted_after_fence"
                intent["provider_io_performed"] = True
                persist_state(run_json, state)
                write_workspace_snapshot(root)
                validate_workspace_snapshot(root, state)
            reason = intent.get("ambiguity_reason_code")
            bound = deepcopy(intent.get("provider_bound_action_ids") or [])
            operations = deepcopy(intent.get("provider_operation_ids") or [])
            records = deepcopy(intent.get("prepared_create_records") or [])
            return build_external_authority_provider_dispatch_result_v3(
                outcome="ambiguous_submission",
                reason_code=reason,
                provider_io_disposition="create_entered_unknown",
                grant_invocation_disposition="create_entered_unknown",
                run_id=state["run_id"],
                request_sha256=request_sha256,
                grant_sha256=grant_sha256,
                ordered_action_ids=deepcopy(ordered_ids),
                provider_bound_action_ids=bound,
                ambiguous_action_ids=[active_id],
                refused_action_ids=[],
                provider_operation_ids=operations,
                prepared_create_records=records,
                post_state_revision=int(state["state_revision"]),
                post_snapshot_sha256=sha256_file(root / "workspace-snapshot.json"),
            )
        actions = _current_actions(state, ordered_ids)
        for action in actions:
            mechanism = (action.get("binding") or {}).get("service_level")
            if mechanism != "interactive":
                raise ExternalAuthorityV2ExecutionError(
                    "unsupported_contract", "v2 ordinary dispatch currently supports interactive response actions only",
                )
            if action.get("provider") is not None:
                continue
            if action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION":
                raise ExternalAuthorityV2ExecutionError(
                    "provider_submission_ambiguous", "native intent contains ambiguous provider submission",
                )
            if action.get("state") != "SUBMITTING" or action.get("consumption") is None:
                raise ExternalAuthorityV2ExecutionError(
                    "action_state_or_custody_mismatch", "native intent member is not durably submitting",
                )

        terminal_statuses = {
            "DELIVERY_COMPLETE", "DELIVERY_COMPLETE_WITH_WARNINGS",
            "FINAL_QA_FAILED", "FINAL_QA_REQUIRES_REVIEW",
            "FAILED_REQUIRES_REVIEW", "BUDGET_EXHAUSTED",
            "POLICY_STOPPED",
        }
        if str(state.get("status") or "") in terminal_statuses:
            if not phase_aware:
                raise ExternalAuthorityV2ExecutionError(
                    "native_evidence_invalid",
                    "post-intent lifecycle is terminal before provider call-entry",
                )
            if (
                intent.get("next_action_index") != 0
                or intent.get("provider_bound_action_ids")
                or intent.get("provider_operation_ids")
                or intent.get("active_action_id") is not None
                or any(action.get("provider") is not None for action in actions)
            ):
                raise ExternalAuthorityV2ExecutionError(
                    "native_evidence_invalid",
                    "terminal post-intent lifecycle conflicts with existing provider custody",
                )
            archived = {
                "schema_version": "astrowoof.external_authority_v2_refused_invocation.v1",
                "outcome": "pre_provider_refusal",
                "request_sha256": request_sha256,
                "grant_sha256": grant_sha256,
                "ordered_action_ids": deepcopy(ordered_ids),
                "provider_bound_action_ids": [],
                "provider_operation_ids": [],
                "refused_action_id": ordered_ids[0],
                "refused_action_ids": deepcopy(ordered_ids),
                "unentered_action_ids": deepcopy(ordered_ids),
                "reason_code": "post_intent_lifecycle_contradiction",
                "prepared_create_records": [],
                "unentered_action_evidence": [
                    {
                        "action_id": action["action_id"],
                        "authorization": deepcopy(action.get("authorization")),
                        "consumption": deepcopy(action.get("consumption")),
                    }
                    for action in actions
                ],
                "post_state_revision": int(state.get("state_revision") or 0) + 1,
            }
            state.setdefault("external_authority_v2_dispatch_history", []).append(
                archived
            )
            for action in actions:
                member_history = deepcopy(archived)
                member_history["member_disposition"] = "not_entered_after_refusal"
                action.setdefault(
                    "external_authority_v2_refused_invocations", []
                ).append(member_history)
                action["state"] = "PREPARED"
                action["authorization"] = None
                action.pop("consumption", None)
            state.pop("external_authority_v2_dispatch_intent", None)
            persist_state(run_json, state)
            write_workspace_snapshot(root)
            validate_workspace_snapshot(root, state)
            emit("external_authority.refused", data={
                "reason_code": "post_intent_lifecycle_contradiction",
                "category": "pre_provider_refusal",
                "selected_command": "external_authority_v2_dispatch",
                "action_count": len(ordered_ids),
            })
            logger.info(
                "provider_dispatch_classified outcome=pre_provider_refusal "
                "reason=post_intent_lifecycle_contradiction action_count=%s "
                "provider_io=not_attempted",
                len(ordered_ids),
            )
            return build_external_authority_provider_dispatch_result_v4(
                outcome="pre_provider_refusal",
                reason_code="post_intent_lifecycle_contradiction",
                provider_io_disposition="not_attempted",
                grant_invocation_disposition="refused",
                run_id=state["run_id"],
                request_sha256=request_sha256,
                grant_sha256=grant_sha256,
                ordered_action_ids=deepcopy(ordered_ids),
                provider_bound_action_ids=[],
                ambiguous_action_ids=[],
                refused_action_ids=deepcopy(ordered_ids),
                provider_operation_ids=[],
                prepared_create_records=[],
                post_state_revision=int(state["state_revision"]),
                post_snapshot_sha256=sha256_file(root / "workspace-snapshot.json"),
            )

        cursor = intent.get("next_action_index")
        if isinstance(cursor, bool) or not isinstance(cursor, int) or not 0 <= cursor <= len(ordered_ids):
            raise ExternalAuthorityV2ExecutionError(
                "action_state_or_custody_mismatch", "native dispatch cursor is invalid",
            )
        durable_bound = [item["action_id"] for item in actions if (item.get("provider") or {}).get("id")]
        if durable_bound != ordered_ids[:cursor]:
            raise ExternalAuthorityV2ExecutionError(
                "provider_identity_conflict", "durable identity inventory does not match dispatch cursor",
            )
        replay = cursor == len(ordered_ids)
        if intent.get("active_action_id") is not None:
            raise ExternalAuthorityV2ExecutionError(
                "provider_submission_ambiguous",
                "a provider create boundary was entered without a durable identity",
            )

    if not replay:
        emit("external_authority.provider_create_permitted", data={
            "request_sha256": request_sha256,
            "action_count": len(ordered_ids) - cursor,
            "selected_command": "external_authority_v2_dispatch",
        })

    bound_ids: list[str] = deepcopy(intent.get("provider_bound_action_ids") or [])
    provider_ids: list[str] = deepcopy(intent.get("provider_operation_ids") or [])
    prepared_records: list[dict[str, str]] = deepcopy(
        intent.get("prepared_create_records") or []
    )
    ambiguous_ids: list[str] = []
    refused_ids: list[str] = []
    result_reason: str | None = None
    provider_io_performed = False
    for action_id in ordered_ids[cursor:]:
        # A failure before this point proves the provider call was not entered.
        _inject(failure_injector, f"before_provider_create:{action_id}")
        prepared_create: dict[str, Any] | None = None
        preparation_snapshot_sha256: str | None = None
        if prepare is not None:
            with _exclusive_lifecycle_lock(root):
                state, intent, current_ids = load_intent_state()
                if intent.get("active_action_id") is not None:
                    raise ExternalAuthorityV2ExecutionError(
                        "provider_submission_ambiguous", "another dispatch entered provider create",
                    )
                action = _current_actions(state, current_ids)[current_ids.index(action_id)]
                preparation_snapshot_sha256 = sha256_file(root / "workspace-snapshot.json")
                preparation_context = {
                    "run_id": state["run_id"],
                    "request_sha256": request_sha256,
                    "grant_sha256": grant_sha256,
                    "checkpoint_snapshot_sha256": preparation_snapshot_sha256,
                }
                action_for_prepare = deepcopy(action)
            prepared_create = _validate_prepared_create(dict(prepare(
                action_for_prepare, preparation_context,
            )))
            _inject(failure_injector, f"after_provider_prepare:{action_id}")
        with _exclusive_lifecycle_lock(root):
            state, intent, current_ids = load_intent_state()
            if current_ids != ordered_ids:
                raise ExternalAuthorityV2ExecutionError(
                    "member_inventory_mismatch", "native intent inventory changed during dispatch",
                )
            action = _current_actions(state, ordered_ids)[ordered_ids.index(action_id)]
            if action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION":
                ambiguous_ids.append(action_id)
                break
            if action.get("state") != "SUBMITTING":
                raise ExternalAuthorityV2ExecutionError(
                    "action_state_or_custody_mismatch", "dispatch member is not SUBMITTING",
                )
            if intent.get("active_action_id") is not None:
                raise ExternalAuthorityV2ExecutionError(
                    "provider_submission_ambiguous", "another dispatch entered provider create",
                )
            checkpoint_changed = bool(
                phase_aware
                and sha256_file(root / "workspace-snapshot.json")
                != preparation_snapshot_sha256
            )
            if prepared_create is not None and (
                prepared_create["outcome"] == "refused" or checkpoint_changed
            ):
                record = {
                    "action_id": action_id,
                    "prepared_create_sha256": prepared_create["prepared_create_sha256"],
                }
                refused_ids.append(action_id)
                prepared_records.append(record)
                result_reason = (
                    "checkpoint_changed_before_create"
                    if checkpoint_changed else prepared_create["reason_code"]
                )
                refusal_index = ordered_ids.index(action_id)
                unentered_ids = ordered_ids[refusal_index:]
                current_actions = _current_actions(state, ordered_ids)
                unentered_evidence = []
                for unentered_id in unentered_ids:
                    unentered_action = current_actions[ordered_ids.index(unentered_id)]
                    if (
                        unentered_action.get("provider") is not None
                        or unentered_action.get("state") != "SUBMITTING"
                    ):
                        raise ExternalAuthorityV2ExecutionError(
                            "native_evidence_invalid",
                            "an unentered refusal-suffix member has provider custody",
                        )
                    unentered_evidence.append({
                        "action_id": unentered_id,
                        "authorization": deepcopy(unentered_action.get("authorization")),
                        "consumption": deepcopy(unentered_action.get("consumption")),
                    })
                archived = {
                    "schema_version": "astrowoof.external_authority_v2_refused_invocation.v1",
                    "outcome": "pre_provider_refusal",
                    "request_sha256": request_sha256,
                    "grant_sha256": grant_sha256,
                    "ordered_action_ids": deepcopy(ordered_ids),
                    "provider_bound_action_ids": deepcopy(bound_ids),
                    "provider_operation_ids": deepcopy(provider_ids),
                    "refused_action_id": action_id,
                    "unentered_action_ids": deepcopy(unentered_ids),
                    "reason_code": result_reason,
                    "prepared_create_records": deepcopy(prepared_records),
                    "unentered_action_evidence": unentered_evidence,
                    "post_state_revision": int(state.get("state_revision") or 0) + 1,
                }
                state.setdefault("external_authority_v2_dispatch_history", []).append(archived)
                for unentered_id in unentered_ids:
                    unentered_action = current_actions[ordered_ids.index(unentered_id)]
                    member_history = deepcopy(archived)
                    member_history["member_disposition"] = (
                        "preparation_refused"
                        if unentered_id == action_id else "not_entered_after_refusal"
                    )
                    unentered_action.setdefault(
                        "external_authority_v2_refused_invocations", []
                    ).append(member_history)
                    unentered_action["state"] = "PREPARED"
                    unentered_action["authorization"] = None
                    unentered_action.pop("consumption", None)
                state.pop("external_authority_v2_dispatch_intent", None)
                persist_state(run_json, state)
                write_workspace_snapshot(root)
                validate_workspace_snapshot(root, state)
                emit("external_authority.refused", data={
                    "reason_code": result_reason,
                    "category": "pre_provider_refusal",
                    "selected_command": "external_authority_v2_dispatch",
                    "action_count": len(unentered_ids),
                }, action_id=action_id)
                logger.info(
                    "provider_dispatch_classified outcome=pre_provider_refusal "
                    "reason=%s action_id=%s provider_io=not_attempted",
                    result_reason, action_id,
                )
                return build_external_authority_provider_dispatch_result_v3(
                    outcome="pre_provider_refusal",
                    reason_code=result_reason,
                    provider_io_disposition="not_attempted",
                    grant_invocation_disposition="refused",
                    run_id=state["run_id"],
                    request_sha256=request_sha256,
                    grant_sha256=grant_sha256,
                    ordered_action_ids=deepcopy(ordered_ids),
                    provider_bound_action_ids=deepcopy(bound_ids),
                    ambiguous_action_ids=[],
                    refused_action_ids=deepcopy(refused_ids),
                    provider_operation_ids=deepcopy(provider_ids),
                    prepared_create_records=deepcopy(prepared_records),
                    post_state_revision=int(state["state_revision"]),
                    post_snapshot_sha256=sha256_file(root / "workspace-snapshot.json"),
                )
            intent["active_action_id"] = action_id
            intent["active_create_state"] = "CALL_ENTERED"
            if prepared_create is not None:
                intent["active_prepared_create_sha256"] = prepared_create[
                    "prepared_create_sha256"
                ]
            persist_state(run_json, state)
            write_workspace_snapshot(root)
            validate_workspace_snapshot(root, state)
            action_for_create = (
                prepared_create if prepared_create is not None else deepcopy(action)
            )

        provider_io_performed = True
        try:
            _inject(failure_injector, f"after_call_fence_before_transport:{action_id}")
            provider_result = create(action_for_create)
            _inject(failure_injector, f"after_provider_create_before_identity:{action_id}")
            if not isinstance(provider_result, Mapping):
                result_reason = "provider_returned_invalid_identity"
                raise ValueError("provider create did not return an object")
            provider_id = provider_result.get("id")
            provider_kind = provider_result.get("kind", "response")
            if not isinstance(provider_id, str) or not provider_id or provider_kind != "response":
                result_reason = "provider_returned_invalid_identity"
                raise ValueError("provider create returned no valid Response identity")
        except Exception as exc:
            # Once create is entered, no local signal proves provider non-acceptance.
            with _exclusive_lifecycle_lock(root):
                state, intent, current_ids = load_intent_state()
                action = _current_actions(state, current_ids)[current_ids.index(action_id)]
                if action.get("provider") is None and action.get("state") == "SUBMITTING":
                    mark_ambiguous(action, reason=f"provider create entered without durable identity: {type(exc).__name__}")
                    intent["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                    intent["active_create_state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                    intent["provider_io_performed"] = True
                    intent["ambiguity_reason_code"] = (
                        result_reason or "provider_transport_failed_without_identity"
                    )
                    if prepared_create is not None:
                        record = {
                            "action_id": action_id,
                            "prepared_create_sha256": prepared_create[
                                "prepared_create_sha256"
                            ],
                        }
                        intent["prepared_create_records"] = [
                            *deepcopy(intent.get("prepared_create_records") or []),
                            record,
                        ]
                    persist_state(run_json, state)
                    write_workspace_snapshot(root)
                    validate_workspace_snapshot(root, state)
            ambiguous_ids.append(action_id)
            result_reason = result_reason or "provider_transport_failed_without_identity"
            if prepared_create is not None:
                prepared_records.append({
                    "action_id": action_id,
                    "prepared_create_sha256": prepared_create["prepared_create_sha256"],
                })
            break

        with _exclusive_lifecycle_lock(root):
            state, intent, current_ids = load_intent_state()
            action = _current_actions(state, current_ids)[current_ids.index(action_id)]
            if (
                intent.get("active_action_id") != action_id
                or intent.get("active_create_state") != "CALL_ENTERED"
            ):
                raise ExternalAuthorityV2ExecutionError(
                    "provider_identity_conflict", "native create boundary changed before identity checkpoint",
                )
            if action.get("provider") is not None or action.get("state") != "SUBMITTING":
                raise ExternalAuthorityV2ExecutionError(
                    "provider_identity_conflict", "native action changed before identity checkpoint",
                )
            if any(
                (item.get("provider") or {}).get("id") == provider_id
                for item in _current_actions(state, current_ids)
                if item.get("action_id") != action_id
            ):
                mark_ambiguous(action, reason="provider returned an identity already bound to another action")
                action["ambiguity"]["provider_id"] = provider_id
                intent["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                intent["active_create_state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                intent["provider_io_performed"] = True
                intent["ambiguity_reason_code"] = "provider_identity_conflict"
                if prepared_create is not None:
                    intent["prepared_create_records"] = [
                        *deepcopy(intent.get("prepared_create_records") or []),
                        {
                            "action_id": action_id,
                            "prepared_create_sha256": prepared_create[
                                "prepared_create_sha256"
                            ],
                        },
                    ]
                persist_state(run_json, state)
                write_workspace_snapshot(root)
                validate_workspace_snapshot(root, state)
                ambiguous_ids.append(action_id)
                result_reason = "provider_identity_conflict"
                if prepared_create is not None:
                    prepared_records.append({
                        "action_id": action_id,
                        "prepared_create_sha256": prepared_create["prepared_create_sha256"],
                    })
                break
            record_provider_id(action, provider_id=provider_id, kind="response")
            action["provider_reconciliation"] = initial_timing(recorded_at=now(), mechanism="response")
            action["state"] = "WAITING"
            bound_ids.append(action_id)
            provider_ids.append(provider_id)
            intent["provider_bound_action_ids"] = deepcopy(bound_ids)
            intent["provider_operation_ids"] = deepcopy(provider_ids)
            if prepared_create is not None:
                prepared_records.append({
                    "action_id": action_id,
                    "prepared_create_sha256": prepared_create["prepared_create_sha256"],
                })
                intent["prepared_create_records"] = deepcopy(prepared_records)
            intent["next_action_index"] = len(bound_ids)
            intent["active_action_id"] = None
            intent["active_create_state"] = None
            intent.pop("active_prepared_create_sha256", None)
            intent["state"] = "PROVIDER_PENDING" if len(bound_ids) == len(ordered_ids) else "DISPATCHING"
            intent["provider_io_performed"] = True
            persist_state(run_json, state)
            write_workspace_snapshot(root)
            validate_workspace_snapshot(root, state)
            if event_emitter is not None:
                emit("provider.identity_recorded", data={
                    "action_id": action_id,
                    "provider_operation_id": provider_id,
                }, action_id=action_id)
                emit("provider.waiting", data={
                    "action_id": action_id,
                    "provider_operation_id": provider_id,
                }, action_id=action_id)
            _inject(failure_injector, f"after_identity_checkpoint:{action_id}")

    with _exclusive_lifecycle_lock(root):
        state, intent, current_ids = load_intent_state()
        snapshot_sha256 = sha256_file(root / "workspace-snapshot.json")
        if phase_aware:
            return build_external_authority_provider_dispatch_result_v3(
                outcome=(
                    "ambiguous_submission" if ambiguous_ids
                    else "exact_replay" if replay
                    else "detached_provider_pending"
                ),
                reason_code=result_reason,
                provider_io_disposition=(
                    "create_entered_unknown" if ambiguous_ids
                    else "provider_identity_durable"
                ),
                grant_invocation_disposition=(
                    "create_entered_unknown" if ambiguous_ids
                    else "replayed" if replay
                    else "provider_pending"
                ),
                run_id=state["run_id"],
                request_sha256=request_sha256,
                grant_sha256=grant_sha256,
                ordered_action_ids=deepcopy(current_ids),
                provider_bound_action_ids=deepcopy(bound_ids),
                ambiguous_action_ids=deepcopy(ambiguous_ids),
                refused_action_ids=[],
                provider_operation_ids=deepcopy(provider_ids),
                prepared_create_records=deepcopy(prepared_records),
                post_state_revision=int(state["state_revision"]),
                post_snapshot_sha256=snapshot_sha256,
            )
        result = {
            "schema_version": PROVIDER_DISPATCH_RESULT_SCHEMA_V2,
            "result_sha256": "pending",
            "outcome": (
                "ambiguous_submission" if ambiguous_ids
                else "exact_replay" if replay
                else "detached_provider_pending"
            ),
            "run_id": state["run_id"],
            "request_sha256": request_sha256,
            "grant_sha256": grant_sha256,
            "ordered_action_ids": deepcopy(current_ids),
            "provider_bound_action_ids": deepcopy(bound_ids),
            "ambiguous_action_ids": deepcopy(ambiguous_ids),
            "provider_operation_ids": deepcopy(provider_ids),
            "post_state_revision": int(state["state_revision"]),
            "post_snapshot_sha256": snapshot_sha256,
            "provider_io_performed": provider_io_performed,
        }
        result["result_sha256"] = _digest({
            key: item for key, item in result.items() if key != "result_sha256"
        })
        return validate_external_authority_provider_dispatch_result_v2(result)


def resolve_external_authority_v2_request_payload(
    run_dir: Path | str, action: Mapping[str, Any],
) -> dict[str, Any]:
    """Resolve one exact snapshot-bound prepared payload without recursive discovery."""
    from .closure import (
        OpenAIResponsesProvider, PassSpec, build_interactive_authoring_request,
        find_workspace_root, load_json, normalized_path,
        retry_feedback_from_record, sha256_file, validate_workspace_snapshot,
    )
    from .provenance import resource_set_provenance
    from .spend import digest as spend_digest, profile_digest

    root = Path(run_dir).resolve()
    state = load_json(root / "run.json")
    validate_workspace_snapshot(root, state)
    action_id = action.get("action_id")
    ledger_actions = (state.get("spend_ledger") or {}).get("actions") or []
    matches = [
        item for item in ledger_actions
        if isinstance(item, dict) and item.get("action_id") == action_id
    ]
    if len(matches) != 1 or matches[0].get("binding") != action.get("binding"):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "the action does not join one snapshot-bound ledger member",
        )
    native_action = matches[0]
    expected = str((action.get("binding") or {}).get("request_sha256") or "")
    if len(expected) != 64:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_mismatch", "action request digest is invalid",
        )
    artifact = native_action.get("request_payload_artifact")
    if artifact is not None:
        required = {
            "schema_version", "logical_path", "file_sha256",
            "canonical_request_sha256", "representation",
        }
        if (
            not isinstance(artifact, dict) or set(artifact) != required
            or artifact.get("schema_version")
            != "astrowoof.provider_request_payload_artifact.v1"
            or artifact.get("representation") != "canonical_json_object"
            or artifact.get("canonical_request_sha256") != expected
        ):
            raise ExternalAuthorityV2ExecutionError(
                "request_payload_digest_mismatch",
                "the binding-owned request payload reference is invalid",
            )
        payload_path = Path(str(artifact.get("logical_path") or "")).resolve()
        try:
            payload_path.relative_to(root)
        except ValueError as exc:
            raise ExternalAuthorityV2ExecutionError(
                "request_payload_digest_mismatch",
                "the binding-owned request payload path escapes the workspace",
            ) from exc
        if (
            normalized_path(payload_path) != artifact["logical_path"]
            or not payload_path.is_file()
            or sha256_file(payload_path) != artifact.get("file_sha256")
        ):
            raise ExternalAuthorityV2ExecutionError(
                "request_payload_digest_mismatch",
                "the binding-owned request payload artifact changed",
            )
        payload = load_json(payload_path)
        if not isinstance(payload, dict) or spend_digest(payload) != expected:
            raise ExternalAuthorityV2ExecutionError(
                "request_payload_digest_mismatch",
                "the direct request payload does not match the action binding",
            )
        return deepcopy(payload)

    binding = native_action.get("binding") or {}
    if binding.get("stage") != "creative_retry":
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "this historical action has no binding-owned request payload",
        )
    refusal_history = native_action.get("external_authority_v2_refused_invocations")
    if not isinstance(refusal_history, list) or not any(
        isinstance(item, dict)
        and item.get("schema_version")
        == "astrowoof.external_authority_v2_refused_invocation.v1"
        and item.get("outcome") == "pre_provider_refusal"
        and item.get("reason_code") == "request_payload_digest_mismatch"
        and item.get("refused_action_id") == action_id
        for item in refusal_history
    ):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "the lossy historical exact artifact cannot satisfy this invocation",
        )
    route_match = re.fullmatch(r"([^:]+):attempt-(\d{3})", str(binding.get("route") or ""))
    if route_match is None:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "the historical exact route cannot be rebuilt",
        )
    pass_id, attempt_text = route_match.groups()
    attempt_number = int(attempt_text)
    if attempt_number < 2:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical rebuild is limited to ordinary creative retries",
        )
    runtime = ((state.get("provenance") or {}).get("runtime") or {})
    if (
        runtime.get("distribution") != "astrowoof-natal-authoring"
        or runtime.get("version") != "0.4.23"
        or state.get("schema_version") != "astrowoof.semantic_closure_run.v0.9"
        or (state.get("provenance") or {}).get("resources")
        != resource_set_provenance()
    ):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "no compatible historical exact request builder is available",
        )
    if profile_digest(state.get("authoring_profile")) != binding.get("profile_sha256"):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "the retained authoring profile does not match the action binding",
        )
    record = (state.get("passes") or {}).get(pass_id)
    if not isinstance(record, dict):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable", "the retained pass record is unavailable",
        )
    attempts = record.get("attempts") or []
    positions = [
        index for index, item in enumerate(attempts)
        if isinstance(item, dict)
        and item.get("attempt_number") == attempt_number
        and item.get("paid_action_id") == action_id
    ]
    if len(positions) != 1:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_ambiguous",
            "the historical action does not join one retained pass attempt",
        )
    position = positions[0]
    attempt_root = root / "passes" / pass_id / f"attempt-{attempt_number:03d}"
    redacted_path = attempt_root / "openai-request.json"
    prompt_path = attempt_root / "openai-workspace-prompt.txt"
    if not redacted_path.is_file() or not prompt_path.is_file():
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical exact request evidence is incomplete",
        )
    try:
        prompt = prompt_path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "historical exact prompt is not valid UTF-8",
        ) from exc
    redacted = load_json(redacted_path)
    placeholder = "[workspace prompt persisted separately as openai-workspace-prompt.txt]"
    if (
        not isinstance(redacted, dict)
        or not isinstance(redacted.get("input"), list)
        or len(redacted["input"]) != 2
        or not isinstance(redacted["input"][1], dict)
        or redacted["input"][1].get("content") != placeholder
        or json.dumps(redacted, ensure_ascii=False).count(placeholder) != 1
    ):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "historical exact redaction shape is invalid",
        )
    source_zip = Path(str(record.get("source_zip") or "")).resolve()
    source_root = root / "passes" / pass_id / "source"
    try:
        source_zip.relative_to(root)
    except ValueError as exc:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical exact source archive escapes the restored workspace",
        ) from exc
    if (
        not source_zip.is_file()
        or sha256_file(source_zip) != record.get("source_sha256")
        or not source_root.is_dir()
    ):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical exact source evidence is incomplete",
        )
    source_workspace = find_workspace_root(source_root, pass_id)
    config = state.get("provider_configuration") or {}
    if "creative_retry" in config:
        config = config.get("creative_retry") or {}
    allowed_config = {
        "model", "reasoning_effort", "background", "base_url",
        "max_output_tokens", "prompt_cache_mode", "prompt_cache_ttl",
        "require_spend_authorization",
    }
    if not isinstance(config, dict) or any(key not in allowed_config for key in config):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical provider configuration is incompatible",
        )
    try:
        provider = OpenAIResponsesProvider(api_key="snapshot-bound-rebuild", **config)
    except (TypeError, ValueError) as exc:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_unavailable",
            "historical provider configuration cannot be rebuilt",
        ) from exc
    if (
        provider.model != binding.get("model")
        or provider.max_output_tokens != binding.get("maximum_output_tokens")
        or binding.get("service_level") != "interactive"
    ):
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "historical provider configuration does not match the action binding",
        )
    prior_record = deepcopy(record)
    prior_record["attempts"] = deepcopy(attempts[:position])
    feedback = retry_feedback_from_record(prior_record)
    spec = PassSpec(
        pass_id=pass_id,
        subject=str(record.get("subject") or ""),
        pass_number=int(record.get("pass_number")),
        source_zip=source_zip,
        source_sha256=str(record.get("source_sha256") or ""),
    )
    rebuilt, _layout, segments = build_interactive_authoring_request(
        provider, spec=spec, workspace=source_workspace,
        feedback=feedback, attempt_number=attempt_number,
    )
    if "\n\n".join(segments.values()) != prompt:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "rebuilt historical prompt does not match persisted prompt evidence",
        )
    expected_redacted = deepcopy(rebuilt)
    expected_redacted["input"] = [
        rebuilt["input"][0],
        {"role": "user", "content": placeholder},
    ]
    if expected_redacted != redacted or spend_digest(rebuilt) != expected:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_digest_mismatch",
            "rebuilt historical request does not match retained binding evidence",
        )
    return rebuilt
