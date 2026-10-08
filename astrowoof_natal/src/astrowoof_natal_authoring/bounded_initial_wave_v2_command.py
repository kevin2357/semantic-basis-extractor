"""Public result contract for bounded initial-wave v2 command execution."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from importlib.resources import files
from typing import Any, Mapping


BOUNDED_INITIAL_WAVE_V2_COMMAND_RESULT_SCHEMA = (
    "astrowoof.bounded_initial_wave_v2_command_result.v1"
)
_KEYS = {
    "schema_version", "result_sha256", "outcome", "reason_code",
    "native_run_id", "checkpoint_basis_sha256", "request_sha256",
    "grant_sha256", "api_decision_id", "request_kind", "ordering_semantics",
    "ordered_action_ids", "initial_wave", "intent_result", "wave_result",
    "native_mutation_performed", "provider_io_performed", "checkpoint_published",
}


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def validate_bounded_initial_wave_v2_command_result(value: Any) -> dict[str, Any]:
    """Validate a closed, safe API handoff from the bounded v2 command."""
    if not isinstance(value, dict) or set(value) != _KEYS:
        raise ValueError("bounded initial-wave command result fields are not exact")
    if (
        value.get("schema_version") != BOUNDED_INITIAL_WAVE_V2_COMMAND_RESULT_SCHEMA
        or value.get("outcome") not in {
            "pre_provider_refusal", "detached_provider_pending", "exact_replay",
            "ambiguous_custody_refusal",
        }
        or value.get("request_kind") != "initial_wave_admission"
        or value.get("ordering_semantics") != "prepared_wave_semantic_member_order"
        or not isinstance(value.get("native_run_id"), str) or not value["native_run_id"]
        or any(
            not isinstance(value.get(key), str) or len(value[key]) != 64
            for key in ("checkpoint_basis_sha256", "request_sha256", "result_sha256")
        )
        or not isinstance(value.get("ordered_action_ids"), list)
        or len(value["ordered_action_ids"]) != 6
        or len(set(value["ordered_action_ids"])) != 6
        or not isinstance(value.get("initial_wave"), dict)
        or any(not isinstance(value.get(key), bool) for key in (
            "native_mutation_performed", "provider_io_performed", "checkpoint_published",
        ))
    ):
        raise ValueError("bounded initial-wave command result semantics are invalid")
    if value["outcome"] == "pre_provider_refusal" and any(value[key] for key in (
        "native_mutation_performed", "provider_io_performed", "checkpoint_published",
    )):
        raise ValueError("pre-provider refusal must be nonmutating")
    if value["outcome"] == "exact_replay" and any(value[key] for key in (
        "native_mutation_performed", "provider_io_performed", "checkpoint_published",
    )):
        raise ValueError("exact replay cannot claim a new invocation side effect")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value["result_sha256"] != _digest(body):
        raise ValueError("bounded initial-wave command result digest mismatch")
    return deepcopy(value)


def build_bounded_initial_wave_v2_command_result(
    *, request: Mapping[str, Any], grant: Mapping[str, Any] | None,
    intent_result: dict[str, Any] | None, wave_result: dict[str, Any] | None,
    outcome: str, reason_code: str | None, native_mutation_performed: bool,
    provider_io_performed: bool, checkpoint_published: bool,
) -> dict[str, Any]:
    body = {
        "schema_version": BOUNDED_INITIAL_WAVE_V2_COMMAND_RESULT_SCHEMA,
        "outcome": outcome,
        "reason_code": reason_code,
        "native_run_id": request["run_id"],
        "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "request_sha256": request["external_authority_request_sha256"],
        "grant_sha256": None if grant is None else grant["grant_sha256"],
        "api_decision_id": None if grant is None else grant["api_decision_id"],
        "request_kind": "initial_wave_admission",
        "ordering_semantics": "prepared_wave_semantic_member_order",
        "ordered_action_ids": list(request["ordered_action_ids"]),
        "initial_wave": deepcopy(request["initial_wave"]),
        "intent_result": deepcopy(intent_result),
        "wave_result": deepcopy(wave_result),
        "native_mutation_performed": native_mutation_performed,
        "provider_io_performed": provider_io_performed,
        "checkpoint_published": checkpoint_published,
    }
    return validate_bounded_initial_wave_v2_command_result({
        **body, "result_sha256": _digest(body),
    })


def read_bounded_initial_wave_v2_command_result_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "bounded-initial-wave-v2-command-result.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))
