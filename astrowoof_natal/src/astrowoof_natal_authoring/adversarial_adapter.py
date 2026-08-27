"""Qualification-only adapter from real SBE lifecycle evidence to trace v1."""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from .adversarial_trace import (
    build_adversarial_trace_fixture,
    finalize_adversarial_trace,
)
from .closure import normalized_path, public_run_state, write_workspace_snapshot
from .post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)


OBSERVED_AT = "2026-08-27T12:00:00Z"


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def materialize_review_no_action_workspace(root: Path | str) -> Path:
    """Create a disposable exact-Natal review workspace via production persistence.

    This is qualification setup, not a generic native-state editor. The fixed,
    sanitized fixture contains no subject, prompt, request payload, provider identity,
    credential, or spend-capable transport.
    """

    run_dir = Path(root).resolve() / "review-no-action"
    run_dir.mkdir(parents=True, exist_ok=False)
    actions = []
    for ordinal in range(1, 7):
        actions.append({
            "action_id": f"paid_{ordinal:024x}",
            "state": "REPORTED",
            "binding": {
                "run_id": "fixture-review-no-action",
                "profile_sha256": "a" * 64,
                "prepared_state_revision": 1,
                "stage": "authoring_initial",
                "route": f"pass-{ordinal}:attempt-001",
                "request_sha256": "b" * 64,
                "model": "scripted-provider",
                "service_level": "interactive",
                "maximum_output_tokens": 1000,
                "commitment_micro_usd": 1,
                "price_book_version": "openai-public-2026-08-07.v1",
            },
            "reported": {"estimated_micro_usd": 0},
        })
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "fixture-review-no-action",
        "state_revision": 1,
        "created_at": "2026-08-27T11:59:00Z",
        "updated_at": "2026-08-27T12:00:00Z",
        "provider": "fake",
        "provider_configuration": {},
        "max_attempts": 3,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "policy": {
                "currency": "USD",
                "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 1_000_000,
                "stage_ceilings_micro_usd": {
                    "authoring_initial": 1_000_000,
                    "creative_retry": 1_000_000,
                    "polish": 1_000_000,
                    "qualitative_critic": 1_000_000,
                    "qualitative_candidate": 1_000_000,
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip",
                    "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            },
            "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {},
        "subjects": {},
        "provenance": {},
    }
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8",
    )
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8",
    )
    write_workspace_snapshot(run_dir)
    return run_dir


def inspect_review_no_action_workspace(
    run_dir: Path | str, *, observed_at: str = OBSERVED_AT,
) -> dict[str, Any]:
    """Invoke the real v0.7 runtime inspection boundary for the fixture."""

    from .lifecycle import _exclusive_lifecycle_lock

    root = Path(run_dir).resolve()
    with _exclusive_lifecycle_lock(root):
        result = inspect_post_fan_in_lifecycle(
            root, observed_at=observed_at,
            native_exclusive_access="established",
        )
    validate_lifecycle_inspection_v07(result)
    decision = result["temporal_decision"]
    inventory = result["checkpoint_basis"]["local_work_inventory"]
    if (
        decision["selected_command"] != "none"
        or decision["capacity_disposition"] != "retain_for_review"
        or decision["local_work_ready_now"] is not False
        or inventory["operations"]
    ):
        raise ValueError("review/no-action fixture did not reach its frozen boundary")
    return result


def build_review_no_action_runtime_trace(
    inspection: Mapping[str, Any], *, api_translation: str,
) -> dict[str, Any]:
    """Project one validated v0.7 result through a modeled API translation.

    `historical` reproduces the lossy capacity-retaining wrapper. `corrected` models
    the API-owned typed non-local disposition. These API facts are qualification
    inputs, not SBE runtime assertions.
    """

    validated = validate_lifecycle_inspection_v07(dict(inspection))
    if api_translation not in {"historical", "corrected"}:
        raise ValueError("api_translation is unsupported")
    decision = validated["temporal_decision"]
    basis = validated["checkpoint_basis"]
    observation = basis["observation"]
    trace = build_adversarial_trace_fixture("review-no-action-cycle.v1.json")
    trace["public_evidence"] = [{
        "kind": "lifecycle_inspection",
        "schema_version": validated["schema_version"],
        "sha256": _canonical_sha256(validated),
        "opaque_ref": "fixture:review-no-action-lifecycle",
    }]
    native = deepcopy(trace["before"]["native"])
    native.update({
        "checkpoint_basis_sha256": validated["checkpoint_basis_sha256"],
        "snapshot_sha256": observation["snapshot_sha256"],
        "state_revision": observation["operator_state_revision"],
        "selected_command": decision["selected_command"],
        "capacity_disposition": decision["capacity_disposition"],
        "reason_code": decision["reason_code"],
        "semantic_fences": [{
            "kind": "checkpoint_basis",
            "sha256": validated["checkpoint_basis_sha256"],
        }],
    })
    trace["before"]["native"] = deepcopy(native)
    trace["after"]["native"] = deepcopy(native)
    trace["before"]["raw_evidence_sha256"] = _canonical_sha256(validated)
    trace["after"]["raw_evidence_sha256"] = _canonical_sha256(validated)
    trace["clock"].update({"logical_step_before": 0, "logical_step_after": 1})
    trace["expected"]["progress_witness"] = None
    if api_translation == "historical":
        trace["expected"]["classification"] = "stutter"
        trace["expected"]["starvation_witness"] = {
            "victim_run_ref": "fixture:api-competing-run",
            "blocker_run_ref": "fixture:api-simulation-run",
            "eligible_since_step": 0,
            "witness_steps": 1,
        }
    else:
        trace["after"]["api_fixture"].update({
            "job_disposition": "deferred",
            "lease_disposition": "released",
            "capacity_state": "released",
        })
        trace["expected"]["classification"] = "productive"
        trace["expected"]["starvation_witness"] = None
        trace["expected"]["side_effects"].update({
            "lease_released": True,
            "capacity_released": True,
        })
    return finalize_adversarial_trace(trace)
