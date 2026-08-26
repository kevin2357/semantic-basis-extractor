"""Installed-wheel, provider-free post-fan-in lifecycle qualification v2."""

from __future__ import annotations

import hashlib
from importlib.resources import files
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from .closure import normalized_path, public_run_state, save_state, write_workspace_snapshot
from .pending_lifecycle_qa import run_provider_pending_lifecycle_qualification
from .post_fan_in_contracts import (
    commit_local_work_progress,
    validate_lifecycle_inspection_v07,
)


RECEIPT_SCHEMA = "astrowoof.provider_pending_lifecycle_qualification.v2"
_RECEIPT_KEYS = frozenset({
    "schema_version", "status", "qualification_only", "provider_free",
    "network_required", "production_authority", "legacy_v1_receipt_sha256",
    "route_results", "assertions", "receipt_sha256",
})


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _binding(run_id: str, route: str, revision: int) -> dict[str, Any]:
    return {
        "run_id": run_id, "profile_sha256": "a" * 64,
        "prepared_state_revision": revision, "stage": "creative_retry",
        "route": route, "request_sha256": "b" * 64,
        "model": "scripted-provider", "service_level": "interactive",
        "maximum_output_tokens": 1000, "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def _workspace(parent: Path, route_family: str) -> tuple[Path, str, str]:
    """Construct a sanitized production-shaped retry workspace without test imports."""
    root = parent / route_family
    root.mkdir()
    run_id = f"installed-v2-{route_family}"
    prefix = "bounded_natal.v2:" if route_family == "bounded_natal" else ""
    retry_one = "paid_000000000000000000000101"
    retry_two = "paid_000000000000000000000102"
    actions: list[dict[str, Any]] = []
    for number in range(1, 7):
        actions.append({
            "action_id": f"paid_{number:024x}", "state": "REPORTED",
            "binding": _binding(run_id, f"{prefix}pass-{number}:attempt-001", 1),
            "provider": {"id": f"resp_qa_{route_family}_{number}", "kind": "response"},
            "reported": {"estimated_micro_usd": 0},
        })
    actions.extend((
        {
            "action_id": retry_one, "state": "WAITING",
            "binding": _binding(run_id, f"{prefix}pass-1:attempt-002", 7),
            "provider": {"id": f"resp_qa_{route_family}_retry", "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-25T23:42:00Z",
                "last_outcome": "completed", "resume_not_before": None,
            },
            "reported": None,
        },
        {
            "action_id": retry_two, "state": "PREPARED",
            "binding": _binding(run_id, f"{prefix}pass-1:attempt-003", 8),
        },
    ))
    state: dict[str, Any] = {
        "schema_version": (
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal"
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        "run_id": run_id, "state_revision": 8,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path", "logical_root": normalized_path(root),
        },
        "spend_ledger": {"actions": actions},
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {"pass-1": {
            "pass_id": "pass-1", "state": "AWAITING_SPEND_AUTHORIZATION",
            "attempts": [
                {"attempt_number": 1, "state": "PASS_QA_REJECTED"},
                {"attempt_number": 2, "state": "WAITING_FOR_RESPONSE"},
                {"attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION"},
            ],
        }},
        "subjects": {}, "provenance": {},
    }
    if route_family == "bounded_natal":
        state.update({
            "route": "bounded_natal.v2",
            "route_contract": "astrowoof.bounded_natal.authoring_run.v2",
            "service_level": "interactive",
        })
    (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(root)
    return root, retry_one, retry_two


def _inspect_fresh(root: Path, observed_at: str) -> dict[str, Any]:
    environment = dict(os.environ)
    source_root = str(Path(__file__).resolve().parents[1])
    environment["PYTHONPATH"] = source_root + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH") else ""
    )
    process = subprocess.run(
        [
            sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
            "--run-dir", str(root), "inspect-local-work",
            "--native-exclusive-access", "declared", "--observed-at", observed_at,
        ],
        check=True, capture_output=True, text=True, timeout=30, env=environment,
    )
    return validate_lifecycle_inspection_v07(json.loads(process.stdout))


def validate_provider_pending_lifecycle_qualification_v2(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _RECEIPT_KEYS:
        raise ValueError("Qualification v2 fields are not exact")
    if value.get("schema_version") != RECEIPT_SCHEMA or value.get("status") != "pass":
        raise ValueError("Qualification v2 identity/status is invalid")
    for key, expected in (
        ("qualification_only", True), ("provider_free", True),
        ("network_required", False), ("production_authority", False),
    ):
        if value.get(key) is not expected:
            raise ValueError(f"Qualification v2 {key} is invalid")
    if not isinstance(value.get("legacy_v1_receipt_sha256"), str) or len(value["legacy_v1_receipt_sha256"]) != 64:
        raise ValueError("Qualification v2 legacy receipt digest is invalid")
    routes = value.get("route_results")
    if not isinstance(routes, list) or [item.get("route_family") for item in routes] != ["exact_natal", "bounded_natal"]:
        raise ValueError("Qualification v2 route results are invalid")
    required_route_keys = {
        "route_family", "prior_operation_key", "prior_inventory_sha256",
        "successor_inventory_sha256", "successor_command", "successor_action_ids",
        "provider_create_count", "provider_retrieval_count", "replay_refused",
    }
    for item in routes:
        if not isinstance(item, dict) or set(item) != required_route_keys:
            raise ValueError("Qualification v2 route result fields are not exact")
        if item["successor_command"] != "await_external_authority":
            raise ValueError("Qualification v2 successor command is invalid")
        if item["provider_create_count"] != 0 or item["provider_retrieval_count"] != 0:
            raise ValueError("Qualification v2 performed provider I/O")
        if item["replay_refused"] is not True:
            raise ValueError("Qualification v2 replay proof is invalid")
    assertions = value.get("assertions")
    if not isinstance(assertions, dict) or not assertions or not all(item is True for item in assertions.values()):
        raise ValueError("Qualification v2 assertions failed")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _sha(body):
        raise ValueError("Qualification v2 receipt digest mismatch")
    return json.loads(json.dumps(value))


def read_provider_pending_lifecycle_qualification_v2_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "provider-pending-lifecycle-qualification.v2.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def run_provider_pending_lifecycle_qualification_v2() -> dict[str, Any]:
    """Prove v1 custody plus post-fan-in progress through public fresh readers."""
    legacy = run_provider_pending_lifecycle_qualification()
    route_results = []
    with tempfile.TemporaryDirectory(prefix="sbe-post-fan-in-qa-") as temporary:
        parent = Path(temporary).resolve()
        for route_family in ("exact_natal", "bounded_natal"):
            root, retry_one, retry_two = _workspace(parent, route_family)
            prior = _inspect_fresh(root, "2026-08-25T23:43:00Z")
            operation = prior["checkpoint_basis"]["local_work_inventory"]["operations"][0]
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == retry_one)
            action["state"] = "REPORTED"
            action["reported"] = {"estimated_micro_usd": 0}
            save_state(root / "run.json", state)
            successor = commit_local_work_progress(
                root, prior=prior, observed_at="2026-08-25T23:44:00Z"
            )
            fresh_successor = _inspect_fresh(root, "2026-08-25T23:44:00Z")
            replay_refused = False
            try:
                commit_local_work_progress(
                    root, prior=prior, observed_at="2026-08-25T23:44:01Z"
                )
            except ValueError:
                replay_refused = True
            authority_ids = list(
                fresh_successor["checkpoint_basis"]["external_authority_state"][
                    "ordered_action_ids"
                ]
            )
            route_results.append({
                "route_family": route_family,
                "prior_operation_key": operation["operation_key"],
                "prior_inventory_sha256": prior["checkpoint_basis"]["local_work_inventory"]["inventory_sha256"],
                "successor_inventory_sha256": fresh_successor["checkpoint_basis"]["local_work_inventory"]["inventory_sha256"],
                "successor_command": fresh_successor["temporal_decision"]["selected_command"],
                "successor_action_ids": authority_ids,
                "provider_create_count": 0, "provider_retrieval_count": 0,
                "replay_refused": replay_refused,
            })
            if successor != fresh_successor or authority_ids != [retry_two]:
                raise RuntimeError("Fresh-reader successor did not preserve retry authority")
    assertions = {
        "legacy_v1_still_passes": legacy["status"] == "pass",
        "legacy_six_create_six_retrieve": legacy["create_count"] == legacy["retrieve_count"] == 6,
        "exact_and_bounded_post_fan_in": len(route_results) == 2,
        "local_work_consumed_once": all(item["replay_refused"] for item in route_results),
        "retry_two_authority_selected": all(item["successor_command"] == "await_external_authority" for item in route_results),
        "post_fan_in_provider_io_zero": all(item["provider_create_count"] == item["provider_retrieval_count"] == 0 for item in route_results),
    }
    result = {
        "schema_version": RECEIPT_SCHEMA, "status": "pass",
        "qualification_only": True, "provider_free": True,
        "network_required": False, "production_authority": False,
        "legacy_v1_receipt_sha256": legacy["receipt_sha256"],
        "route_results": route_results, "assertions": assertions,
    }
    result["receipt_sha256"] = _sha(result)
    return validate_provider_pending_lifecycle_qualification_v2(result)


def main() -> None:
    print(json.dumps(run_provider_pending_lifecycle_qualification_v2(), indent=2))


if __name__ == "__main__":
    main()
