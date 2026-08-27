"""Bounded provider-free systematic exploration for lifecycle invariants."""

from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from .adversarial_adapter import (
    build_review_no_action_runtime_trace,
    inspect_review_no_action_workspace,
    materialize_review_no_action_workspace,
)
from .adversarial_oracle import classify_adversarial_transition


CONTRACT = "astrowoof.adversarial_systematic_explorer_qualification.v1"
_ACTION_REF_PREFIX = "fixture:action-"
_CREATE_STATES = {"not_entered", "call_entered_unknown", "provider_identity_durable"}


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("Explorer time must be canonical UTC")
    canonical = parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    if canonical != value:
        raise ValueError("Explorer time must use canonical whole-second Z form")
    return parsed


def validate_action_binding_projection(value: Any) -> dict[str, Any]:
    """Validate the exact redacted member join used by create-once checks."""

    if not isinstance(value, Mapping) or set(value) != {"members", "projection_sha256"}:
        raise ValueError("Action-binding projection fields are not exact")
    members = value.get("members")
    if not isinstance(members, list) or not members:
        raise ValueError("Action-binding projection members must be nonempty")
    identities: list[tuple[str, str]] = []
    for member in members:
        keys = {
            "action_ref", "binding_sha256", "create_state", "create_count",
            "provider_identity_sha256", "retrieval_count",
        }
        if not isinstance(member, Mapping) or set(member) != keys:
            raise ValueError("Action-binding projection member fields are not exact")
        action_ref = member.get("action_ref")
        binding = member.get("binding_sha256")
        state = member.get("create_state")
        create_count = member.get("create_count")
        retrieval_count = member.get("retrieval_count")
        provider = member.get("provider_identity_sha256")
        if not isinstance(action_ref, str) or not action_ref.startswith(_ACTION_REF_PREFIX):
            raise ValueError("Action reference is not an opaque fixture identity")
        if not isinstance(binding, str) or len(binding) != 64 or any(c not in "0123456789abcdef" for c in binding):
            raise ValueError("Binding digest is invalid")
        if state not in _CREATE_STATES:
            raise ValueError("Create state is invalid")
        if isinstance(create_count, bool) or create_count not in {0, 1}:
            raise ValueError("Create-at-most-once violated for action/binding")
        if isinstance(retrieval_count, bool) or not isinstance(retrieval_count, int) or retrieval_count < 0:
            raise ValueError("Retrieval count is invalid")
        if state == "not_entered" and (create_count != 0 or provider is not None):
            raise ValueError("Unentered member has create/provider evidence")
        if state == "call_entered_unknown" and (create_count != 1 or provider is not None):
            raise ValueError("Ambiguous member evidence is contradictory")
        if state == "provider_identity_durable" and (
            create_count != 1 or not isinstance(provider, str) or len(provider) != 64
            or any(c not in "0123456789abcdef" for c in provider)
        ):
            raise ValueError("Durable provider member evidence is incomplete")
        if retrieval_count and state != "provider_identity_durable":
            raise ValueError("Retrieval lacks durable provider identity")
        identities.append((action_ref, binding))
    if identities != sorted(identities) or len(identities) != len(set(identities)):
        raise ValueError("Action/binding inventory must be unique lexical order")
    body = {"members": members}
    if value.get("projection_sha256") != _digest(body):
        raise ValueError("Action-binding projection digest mismatch")
    return deepcopy(dict(value))


def build_action_binding_projection(members: list[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted((deepcopy(dict(item)) for item in members), key=lambda item: (
        item["action_ref"], item["binding_sha256"],
    ))
    body = {"members": ordered}
    return validate_action_binding_projection({
        **body, "projection_sha256": _digest(body),
    })


def _member(ordinal: int, *, durable: bool) -> dict[str, Any]:
    action_ref = f"{_ACTION_REF_PREFIX}{ordinal:02d}"
    binding = _digest({"action_ref": action_ref, "route": "exact_natal"})
    return {
        "action_ref": action_ref,
        "binding_sha256": binding,
        "create_state": "provider_identity_durable" if durable else "not_entered",
        "create_count": 1 if durable else 0,
        "provider_identity_sha256": _digest({"provider": action_ref}) if durable else None,
        "retrieval_count": 0,
    }


def _create_member(projection: Mapping[str, Any], action_ref: str) -> dict[str, Any]:
    current = validate_action_binding_projection(projection)
    members = deepcopy(current["members"])
    selected = next((item for item in members if item["action_ref"] == action_ref), None)
    if selected is None:
        raise ValueError("event_not_enabled: unknown action")
    if selected["create_state"] != "not_entered":
        raise ValueError("event_not_enabled: create already entered")
    selected["create_state"] = "provider_identity_durable"
    selected["create_count"] = 1
    selected["provider_identity_sha256"] = _digest({"provider": action_ref})
    return build_action_binding_projection(members)


def _projection_fingerprint(projection: Mapping[str, Any], now: str) -> str:
    _instant(now)
    return _digest({
        "projection_sha256": projection["projection_sha256"],
        "simulated_time": now,
    })


def _explore_member_wave(max_depth: int) -> dict[str, Any]:
    initial = build_action_binding_projection([
        _member(index, durable=index <= 4) for index in range(1, 7)
    ])
    queue: list[tuple[dict[str, Any], list[str]]] = [(initial, [])]
    visited = {_projection_fingerprint(initial, "2026-08-27T12:00:00Z")}
    distinct_witness: list[str] | None = None
    duplicate_refusal: list[str] | None = None
    explored = 0
    deduplicated_successors = 0
    while queue:
        state, path = queue.pop(0)
        explored += 1
        if len(path) >= max_depth:
            continue
        for member in state["members"]:
            event = f"create:{member['action_ref']}"
            if member["create_state"] == "not_entered":
                successor = _create_member(state, member["action_ref"])
                next_path = path + [event]
                if distinct_witness is None:
                    distinct_witness = next_path
                fingerprint = _projection_fingerprint(
                    successor, "2026-08-27T12:00:00Z",
                )
                if fingerprint not in visited:
                    visited.add(fingerprint)
                    queue.append((successor, next_path))
                else:
                    deduplicated_successors += 1
            elif duplicate_refusal is None:
                try:
                    _create_member(state, member["action_ref"])
                except ValueError:
                    duplicate_refusal = path + [event]
    return {
        "initial_projection_sha256": initial["projection_sha256"],
        "explored_state_count": explored,
        "deduplicated_state_count": len(visited),
        "deduplicated_successor_count": deduplicated_successors,
        "distinct_member_create_witness": distinct_witness,
        "duplicate_create_refusal_witness": duplicate_refusal,
    }


def run_systematic_explorer_qualification(*, max_depth: int = 2) -> dict[str, Any]:
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or not 2 <= max_depth <= 8:
        raise ValueError("Explorer max_depth must be between 2 and 8")
    with tempfile.TemporaryDirectory(prefix="sbe-adversarial-explorer-") as temporary:
        lifecycle = inspect_review_no_action_workspace(
            materialize_review_no_action_workspace(Path(temporary)),
        )
        muffin = build_review_no_action_runtime_trace(
            lifecycle, api_translation="historical",
        )
    muffin_result = classify_adversarial_transition(muffin)
    wave = _explore_member_wave(max_depth)
    base = "2026-08-27T12:00:00Z"
    repeated = (
        datetime.fromisoformat(base.replace("Z", "+00:00")) + timedelta(seconds=300)
    ).isoformat(timespec="seconds").replace("+00:00", "Z")
    accelerated = "2026-08-27T12:05:00Z"
    assertions = {
        "muffin_minimal_stutter_found": muffin_result["classification"] == "stutter",
        "partial_wave_distinct_create_allowed": wave["distinct_member_create_witness"] is not None,
        "same_action_binding_duplicate_refused": wave["duplicate_create_refusal_witness"] is not None,
        "semantic_state_deduplicated": wave["deduplicated_successor_count"] > 0,
        "accelerated_time_matches_unit_steps": repeated == accelerated,
    }
    body = {
        "schema_version": CONTRACT,
        "status": "pass" if all(assertions.values()) else "fail",
        "qualification_only": True,
        "provider_free": True,
        "max_depth": max_depth,
        "external_network_call_count": 0,
        "real_provider_create_count": 0,
        "provider_spend_usd": 0,
        "muffin_trace_sha256": muffin["trace_sha256"],
        "wave": wave,
        "assertions": assertions,
    }
    return validate_systematic_explorer_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_systematic_explorer_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "max_depth", "external_network_call_count",
        "real_provider_create_count", "provider_spend_usd", "muffin_trace_sha256",
        "wave", "assertions",
    }
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != CONTRACT:
        raise ValueError("Systematic explorer receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Systematic explorer receipt digest mismatch")
    if (
        value.get("status") != "pass" or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("real_provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
    ):
        raise ValueError("Systematic explorer safety declaration is invalid")
    if isinstance(value.get("max_depth"), bool) or not isinstance(value.get("max_depth"), int):
        raise ValueError("Systematic explorer depth is invalid")
    if not isinstance(value.get("muffin_trace_sha256"), str) or len(value["muffin_trace_sha256"]) != 64:
        raise ValueError("Systematic explorer Muffin trace identity is invalid")
    wave = value.get("wave")
    if not isinstance(wave, Mapping) or set(wave) != {
        "initial_projection_sha256", "explored_state_count", "deduplicated_state_count",
        "deduplicated_successor_count",
        "distinct_member_create_witness", "duplicate_create_refusal_witness",
    }:
        raise ValueError("Systematic explorer wave evidence is invalid")
    for key in ("explored_state_count", "deduplicated_state_count", "deduplicated_successor_count"):
        if isinstance(wave.get(key), bool) or not isinstance(wave.get(key), int) or wave[key] < 0:
            raise ValueError("Systematic explorer wave count is invalid")
    for key in ("distinct_member_create_witness", "duplicate_create_refusal_witness"):
        witness = wave.get(key)
        if not isinstance(witness, list) or not witness or any(
            not isinstance(item, str) or not item.startswith("create:fixture:action-")
            for item in witness
        ):
            raise ValueError("Systematic explorer witness is invalid")
    assertions = value.get("assertions")
    if not isinstance(assertions, Mapping) or set(assertions) != {
        "muffin_minimal_stutter_found", "partial_wave_distinct_create_allowed",
        "same_action_binding_duplicate_refused", "semantic_state_deduplicated",
        "accelerated_time_matches_unit_steps",
    } or any(item is not True for item in assertions.values()):
        raise ValueError("Systematic explorer assertions are not closed and passing")
    return deepcopy(dict(value))
