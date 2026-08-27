"""Derived progress/safety oracle for adversarial lifecycle traces."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping

from .adversarial_trace import (
    canonical_sha256,
    native_contradictions,
    validate_adversarial_trace,
)


def oracle_semantic_fingerprint(state: Mapping[str, Any]) -> str:
    """Fingerprint future-relevant truth while excluding publication churn."""

    projected = deepcopy(dict(state))
    projected.pop("raw_evidence_sha256", None)
    projected.pop("semantic_fingerprint_sha256", None)
    return canonical_sha256({
        "api_fixture": projected["api_fixture"],
        "native": {
            key: value for key, value in projected["native"].items()
            if key not in {"checkpoint_basis_sha256", "snapshot_sha256", "state_revision"}
        } | {
            "semantic_fences": [
                item for item in projected["native"]["semantic_fences"]
                if item["kind"] != "checkpoint_basis"
            ],
        },
        "provider_fixture": projected["provider_fixture"],
    })


def classify_adversarial_transition(
    trace: Mapping[str, Any],
    *,
    prior_semantic_fingerprints: Iterable[str] = (),
) -> dict[str, Any]:
    """Derive one transition classification from public evidence.

    The trace's declared expected classification is deliberately ignored while the
    result is derived. It is consulted only by ``assert_adversarial_oracle``.
    """

    validate_adversarial_trace(trace)
    validated = deepcopy(dict(trace))
    event = validated["event"]
    before = validated["before"]
    after = validated["after"]
    before_fp = oracle_semantic_fingerprint(before)
    after_fp = oracle_semantic_fingerprint(after)
    contradictions = sorted(set(
        native_contradictions(before) + native_contradictions(after)
    ))
    history = list(prior_semantic_fingerprints)

    if contradictions:
        classification = "contradictory_evidence"
    elif event["enabled"] is False:
        classification = "refused"
    elif (
        after["native"]["capacity_disposition"] == "release_until_due"
        and after["native"]["provider_custody"] == "known_operations_pending"
        and after["native"]["resume_not_before"] is not None
        and after["api_fixture"]["lease_disposition"] == "released"
        and after["api_fixture"]["capacity_state"] == "released"
    ):
        classification = "legitimate_wait"
    elif before_fp != after_fp:
        classification = "cycle" if after_fp in history else "productive"
    elif event["kind"] == "inspect_lifecycle":
        classification = "idempotent_replay"
    elif after_fp in history:
        classification = "cycle"
    else:
        classification = "stutter"

    return {
        "classification": classification,
        "before_semantic_fingerprint_sha256": before_fp,
        "after_semantic_fingerprint_sha256": after_fp,
        "contradictions": contradictions,
        "refusal_reason": event["refusal_reason"],
    }


def assert_adversarial_oracle(
    trace: Mapping[str, Any],
    *,
    prior_semantic_fingerprints: Iterable[str] = (),
) -> dict[str, Any]:
    """Require the independently derived result to equal the trace expectation."""

    result = classify_adversarial_transition(
        trace, prior_semantic_fingerprints=prior_semantic_fingerprints,
    )
    expected = trace["expected"]
    if result["classification"] != expected["classification"]:
        raise ValueError(
            "Adversarial oracle mismatch: "
            f"expected={expected['classification']} observed={result['classification']}"
        )
    if result["contradictions"] != expected["declared_contradictions"]:
        raise ValueError("Adversarial oracle contradiction inventory mismatch")
    return deepcopy(result)


def evaluate_adversarial_history(traces: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Evaluate an ordered history and retain prior semantic recurrence evidence."""

    history: list[str] = []
    results: list[dict[str, Any]] = []
    for trace in traces:
        result = assert_adversarial_oracle(
            trace, prior_semantic_fingerprints=history,
        )
        history.append(result["before_semantic_fingerprint_sha256"])
        history.append(result["after_semantic_fingerprint_sha256"])
        results.append(result)
    return results


def adversarial_safety_violations(trace: Mapping[str, Any]) -> list[str]:
    """Derive closed safety violations expressible by trace v1 public evidence."""

    validate_adversarial_trace(trace)
    before = trace["before"]
    after = trace["after"]
    effects = trace["expected"]["side_effects"]
    violations: list[str] = []
    if effects["external_network_calls"]:
        violations.append("external_network_capability_used")
    prior_provider_states = {
        item["state"] for item in before["provider_fixture"]["operations"]
    }
    if prior_provider_states & {
        "pending", "completed", "failed", "cancelled", "expired",
        "malformed", "identity_conflict",
    } and effects["scripted_provider_creates"]:
        violations.append("provider_identity_recreated")
    if (
        "entered_identity_unknown" in prior_provider_states
        and (
            effects["scripted_provider_creates"]
            or effects["scripted_provider_retrievals"]
            or after["native"]["review_required"] is not True
        )
    ):
        violations.append("ambiguous_submission_not_fenced")
    before_local = set(before["native"]["local_operation_keys"])
    after_local = set(after["native"]["local_operation_keys"])
    after_consumed = set(after["native"]["consumed_operation_keys"])
    if trace["event"]["kind"] == "ordinary_resume" and trace["event"]["enabled"]:
        consumed = bool(before_local & after_consumed)
        disposition_changed = (
            before["native"]["selected_command"],
            before["native"]["capacity_disposition"],
        ) != (
            after["native"]["selected_command"],
            after["native"]["capacity_disposition"],
        )
        if before_local and not consumed and not disposition_changed:
            violations.append("advertised_local_work_not_consumed")
    if after_local & after_consumed:
        violations.append("consumed_local_work_readvertised")
    return sorted(set(violations))


def assert_adversarial_safety(trace: Mapping[str, Any]) -> None:
    violations = adversarial_safety_violations(trace)
    if violations:
        raise ValueError("Adversarial safety violation: " + ",".join(violations))
