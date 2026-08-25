"""Writer-fenced preparation for external-authority v2 provider dispatch."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from importlib.resources import files
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence

from .external_authority_v2 import validate_external_authority_grant_v2
from .temporal_lifecycle import (
    inspect_temporal_lifecycle,
    validate_external_authority_request_v2_against_inspection,
)


INTENT_SCHEMA_V2 = "astrowoof.external_authority_dispatch_intent.v2"
INTENT_RESULT_SCHEMA_V2 = "astrowoof.external_authority_intent_result.v2"
PROVIDER_DISPATCH_RESULT_SCHEMA_V2 = "astrowoof.external_authority_provider_dispatch_result.v2"
COMMAND_RESULT_SCHEMA_V1 = "astrowoof.external_authority_v2_command_result.v1"
PROVIDER_DISPATCH_RESULT_SCHEMA_V3 = "astrowoof.external_authority_provider_dispatch_result.v3"
COMMAND_RESULT_SCHEMA_V2 = "astrowoof.external_authority_v2_command_result.v2"
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


def read_ambiguous_provider_submission_fixture_v1() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "external-authority-v2/ambiguous-provider-submission.v1.json"
    )
    value = json.loads(path.read_text(encoding="utf-8"))
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


class ExternalAuthorityV2ExecutionError(ValueError):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code


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

    with _exclusive_lifecycle_lock(root):
        state, intent, ordered_ids = load_intent_state()
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

    if event_emitter is not None and not replay:
        event_emitter.emit("external_authority.provider_create_permitted", data={
            "request_sha256": request_sha256,
            "action_count": len(ordered_ids) - cursor,
            "selected_command": "external_authority_v2_dispatch",
        }, correlation={"native_run_id": str(state.get("run_id") or "")})

    bound_ids: list[str] = deepcopy(intent.get("provider_bound_action_ids") or [])
    provider_ids: list[str] = deepcopy(intent.get("provider_operation_ids") or [])
    ambiguous_ids: list[str] = []
    provider_io_performed = False
    for action_id in ordered_ids[cursor:]:
        # A failure before this point proves the provider call was not entered.
        _inject(failure_injector, f"before_provider_create:{action_id}")
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
            intent["active_action_id"] = action_id
            intent["active_create_state"] = "CALL_ENTERED"
            persist_state(run_json, state)
            write_workspace_snapshot(root)
            validate_workspace_snapshot(root, state)
            action_for_create = deepcopy(action)

        provider_io_performed = True
        try:
            provider_result = create(action_for_create)
            _inject(failure_injector, f"after_provider_create_before_identity:{action_id}")
            if not isinstance(provider_result, Mapping):
                raise ValueError("provider create did not return an object")
            provider_id = provider_result.get("id")
            provider_kind = provider_result.get("kind", "response")
            if not isinstance(provider_id, str) or not provider_id or provider_kind != "response":
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
                    persist_state(run_json, state)
                    write_workspace_snapshot(root)
                    validate_workspace_snapshot(root, state)
            ambiguous_ids.append(action_id)
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
                persist_state(run_json, state)
                write_workspace_snapshot(root)
                validate_workspace_snapshot(root, state)
                ambiguous_ids.append(action_id)
                break
            record_provider_id(action, provider_id=provider_id, kind="response")
            action["provider_reconciliation"] = initial_timing(recorded_at=now(), mechanism="response")
            action["state"] = "WAITING"
            bound_ids.append(action_id)
            provider_ids.append(provider_id)
            intent["provider_bound_action_ids"] = deepcopy(bound_ids)
            intent["provider_operation_ids"] = deepcopy(provider_ids)
            intent["next_action_index"] = len(bound_ids)
            intent["active_action_id"] = None
            intent["active_create_state"] = None
            intent["state"] = "PROVIDER_PENDING" if len(bound_ids) == len(ordered_ids) else "DISPATCHING"
            intent["provider_io_performed"] = True
            persist_state(run_json, state)
            write_workspace_snapshot(root)
            validate_workspace_snapshot(root, state)
            if event_emitter is not None:
                event_emitter.emit("provider.identity_recorded", data={
                    "action_id": action_id,
                    "provider_operation_id": provider_id,
                }, correlation={"native_run_id": str(state.get("run_id") or ""), "action_id": action_id})
                event_emitter.emit("provider.waiting", data={
                    "action_id": action_id,
                    "provider_operation_id": provider_id,
                }, correlation={"native_run_id": str(state.get("run_id") or ""), "action_id": action_id})
            _inject(failure_injector, f"after_identity_checkpoint:{action_id}")

    with _exclusive_lifecycle_lock(root):
        state, intent, current_ids = load_intent_state()
        snapshot_sha256 = sha256_file(root / "workspace-snapshot.json")
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
    """Resolve one exact snapshot-bound prepared payload without private inference."""
    from .closure import load_json
    from .spend import digest as spend_digest

    root = Path(run_dir).resolve()
    expected = str((action.get("binding") or {}).get("request_sha256") or "")
    if len(expected) != 64:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_mismatch", "action request digest is invalid",
        )
    candidates: list[dict[str, Any]] = []
    for name in ("openai-request.json", "openai-request-payload.private.json"):
        for path in root.rglob(name):
            try:
                payload = load_json(path)
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict) and spend_digest(payload) == expected:
                candidates.append(payload)
    if len(candidates) != 1:
        raise ExternalAuthorityV2ExecutionError(
            "request_payload_mismatch",
            "exactly one snapshot-bound prepared provider request payload is required",
        )
    return deepcopy(candidates[0])
