"""Seeded state-aware campaigns and deterministic counterexample shrinking."""

from __future__ import annotations

import json
import random
from copy import deepcopy
from hashlib import sha256
from typing import Any, Mapping

from .adversarial_explorer import (
    advance_explorer_clock,
    build_action_binding_projection,
    validate_action_binding_projection,
    validate_explorer_clock_state,
)


CONTRACT = "astrowoof.adversarial_seeded_campaign_qualification.v1"
_ROUTES = ("exact_natal", "bounded_natal")


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _member(ordinal: int, *, durable: bool) -> dict[str, Any]:
    ref = f"fixture:action-{ordinal:02d}"
    return {
        "action_ref": ref,
        "binding_sha256": _digest({"action": ref}),
        "create_state": "provider_identity_durable" if durable else "not_entered",
        "create_count": 1 if durable else 0,
        "provider_identity_sha256": _digest({"provider": ref}) if durable else None,
        "retrieval_count": 0,
    }


def _initial_state(route: str) -> dict[str, Any]:
    if route not in _ROUTES:
        raise ValueError("Campaign route is unsupported")
    return {
        "route_family": route,
        "projection": build_action_binding_projection([
            _member(index, durable=index <= 4) for index in range(1, 7)
        ]),
        "clock": validate_explorer_clock_state({
            "current_time": "2026-08-27T12:00:00Z",
            "next_boundary": "2026-08-27T12:05:00Z",
            "base_unit_seconds": 1,
        }),
    }


def _fingerprint(state: Mapping[str, Any]) -> str:
    return _digest({
        "route_family": state["route_family"],
        "projection_sha256": state["projection"]["projection_sha256"],
        "clock": state["clock"],
    })


def _enabled_events(state: Mapping[str, Any]) -> list[str]:
    events: list[str] = []
    for member in state["projection"]["members"]:
        if member["create_state"] == "not_entered":
            events.append(f"create:{member['action_ref']}")
        elif member["create_state"] == "provider_identity_durable":
            events.append(f"retrieve:{member['action_ref']}")
    if state["clock"]["current_time"] != state["clock"]["next_boundary"]:
        events.extend(("clock:advance_base_unit", "clock:advance_to_boundary"))
    return sorted(events)


def _apply_event(state: Mapping[str, Any], event: str) -> dict[str, Any]:
    successor = deepcopy(dict(state))
    if event.startswith("clock:"):
        successor["clock"] = advance_explorer_clock(
            successor["clock"], event.removeprefix("clock:"),
        )
        return successor
    kind, action_ref = event.split(":", 1)
    members = deepcopy(successor["projection"]["members"])
    selected = next((item for item in members if item["action_ref"] == action_ref), None)
    if selected is None:
        raise ValueError("event_not_enabled")
    if kind == "create" and selected["create_state"] == "not_entered":
        selected["create_state"] = "provider_identity_durable"
        selected["create_count"] = 1
        selected["provider_identity_sha256"] = _digest({"provider": action_ref})
    elif kind == "retrieve" and selected["create_state"] == "provider_identity_durable":
        selected["retrieval_count"] += 1
    else:
        raise ValueError("event_not_enabled")
    successor["projection"] = build_action_binding_projection(members)
    return successor


def run_seeded_walk(*, seed: int, route_family: str, steps: int = 12) -> dict[str, Any]:
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("Campaign seed is invalid")
    if isinstance(steps, bool) or not isinstance(steps, int) or not 1 <= steps <= 64:
        raise ValueError("Campaign step bound is invalid")
    rng = random.Random(seed)
    state = _initial_state(route_family)
    transitions: list[dict[str, Any]] = []
    coverage: set[str] = set()
    for index in range(steps):
        enabled = _enabled_events(state)
        if not enabled:
            break
        event = enabled[rng.randrange(len(enabled))]
        before = _fingerprint(state)
        successor = _apply_event(state, event)
        after = _fingerprint(successor)
        classification = "productive" if before != after else "stutter"
        transitions.append({
            "step": index, "event": event, "before_sha256": before,
            "after_sha256": after, "classification": classification,
        })
        coverage.add(event.split(":", 1)[0])
        state = successor
    body = {
        "seed": seed,
        "route_family": route_family,
        "requested_steps": steps,
        "executed_steps": len(transitions),
        "transitions": transitions,
        "coverage": sorted(coverage),
        "final_state_sha256": _fingerprint(state),
    }
    return {**body, "walk_sha256": _digest(body)}


def replay_seeded_walk(value: Mapping[str, Any]) -> dict[str, Any]:
    replay = run_seeded_walk(
        seed=value["seed"], route_family=value["route_family"],
        steps=value["requested_steps"],
    )
    if replay != value:
        raise ValueError("Seeded campaign replay differs")
    return replay


def shrink_stutter_counterexample(events: list[str]) -> list[str]:
    """Shrink a known stutter-containing event list to its minimal witness."""

    if "adversarial:noop_checkpoint_republish" not in events:
        raise ValueError("Counterexample does not contain a stutter")
    candidate = list(events)
    changed = True
    while changed:
        changed = False
        for index in range(len(candidate)):
            trial = candidate[:index] + candidate[index + 1:]
            if "adversarial:noop_checkpoint_republish" in trial:
                candidate = trial
                changed = True
                break
    return candidate


def run_seeded_campaign_qualification() -> dict[str, Any]:
    walks = [
        run_seeded_walk(seed=7, route_family="exact_natal"),
        run_seeded_walk(seed=19, route_family="bounded_natal"),
        run_seeded_walk(seed=41, route_family="exact_natal"),
    ]
    for walk in walks:
        replay_seeded_walk(walk)
    original = [
        "clock:advance_base_unit", "retrieve:fixture:action-01",
        "adversarial:noop_checkpoint_republish", "retrieve:fixture:action-02",
    ]
    shrunk = shrink_stutter_counterexample(original)
    coverage = sorted({item for walk in walks for item in walk["coverage"]})
    assertions = {
        "fixed_seed_replay_exact": all(replay_seeded_walk(item) == item for item in walks),
        "both_routes_walked": {item["route_family"] for item in walks} == set(_ROUTES),
        "state_aware_events_only": all(
            transition["classification"] == "productive"
            for walk in walks for transition in walk["transitions"]
        ),
        "counterexample_shrinks_to_one_event": shrunk == ["adversarial:noop_checkpoint_republish"],
        "transition_coverage_reported": bool({"create", "retrieve"} <= set(coverage)),
    }
    body = {
        "schema_version": CONTRACT,
        "status": "pass" if all(assertions.values()) else "fail",
        "qualification_only": True, "provider_free": True,
        "external_network_call_count": 0, "real_provider_create_count": 0,
        "provider_spend_usd": 0, "walks": walks,
        "coverage": coverage,
        "counterexample": {
            "original_events": original, "shrunk_events": shrunk,
            "violation": "stutter",
        },
        "assertions": assertions,
    }
    return validate_seeded_campaign_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_seeded_campaign_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "real_provider_create_count",
        "provider_spend_usd", "walks", "coverage", "counterexample", "assertions",
    }
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != CONTRACT:
        raise ValueError("Seeded campaign receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Seeded campaign receipt digest mismatch")
    if (
        value.get("status") != "pass" or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("real_provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
    ):
        raise ValueError("Seeded campaign safety declaration is invalid")
    walks = value.get("walks")
    if not isinstance(walks, list) or len(walks) != 3:
        raise ValueError("Seeded campaign walk inventory is invalid")
    for walk in walks:
        replay_seeded_walk(walk)
    if value.get("coverage") != sorted(set(value.get("coverage") or [])):
        raise ValueError("Seeded campaign coverage is invalid")
    counterexample = value.get("counterexample")
    if not isinstance(counterexample, Mapping) or set(counterexample) != {
        "original_events", "shrunk_events", "violation",
    } or counterexample.get("violation") != "stutter" or counterexample.get("shrunk_events") != [
        "adversarial:noop_checkpoint_republish"
    ]:
        raise ValueError("Seeded campaign counterexample is invalid")
    assertions = value.get("assertions")
    if not isinstance(assertions, Mapping) or set(assertions) != {
        "fixed_seed_replay_exact", "both_routes_walked", "state_aware_events_only",
        "counterexample_shrinks_to_one_event", "transition_coverage_reported",
    } or any(item is not True for item in assertions.values()):
        raise ValueError("Seeded campaign assertions are invalid")
    return deepcopy(dict(value))
