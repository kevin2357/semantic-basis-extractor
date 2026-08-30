"""Provider-free runtime qualification for retry lineage and mixed custody."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
import argparse
import json
from pathlib import Path
import tempfile
from typing import Any, Mapping

from .closure import (
    normalized_path, public_run_state, retry_feedback_from_record,
    write_workspace_snapshot,
)
from .retry_lineage_contracts import (
    assert_retry_lineage_forward_dispatch_safe,
    inspect_retry_lineage_lifecycle,
    retry_lineage_inventory_from_state,
    validate_lifecycle_inspection_v08,
)


CONTRACT = "astrowoof.retry_lineage_qualification.v1"
SCHEMA_RESOURCE = "retry-lineage-qualification.v1.schema.json"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def read_retry_lineage_qualification_schema() -> dict[str, Any]:
    return json.loads(files(
        "astrowoof_natal_authoring.resources.contracts"
    ).joinpath(SCHEMA_RESOURCE).read_text(encoding="utf-8"))


def _binding(run_id: str, route: str, revision: int) -> dict[str, Any]:
    return {
        "run_id": run_id, "profile_sha256": "a" * 64,
        "prepared_state_revision": revision, "stage": "creative_retry",
        "route": route, "request_sha256": "b" * 64,
        "model": "scripted-provider", "service_level": "interactive",
        "maximum_output_tokens": 1000, "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def _persist(run_dir: Path, state: Mapping[str, Any]) -> None:
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8",
    )
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(dict(state)), indent=2) + "\n",
        encoding="utf-8",
    )
    write_workspace_snapshot(run_dir)


def _materialize(root: Path, route_family: str) -> tuple[Path, dict[str, Any]]:
    run_dir = root / route_family
    run_dir.mkdir(parents=True)
    run_id = f"retry-lineage-qualification-{route_family}"
    prefix = "bounded_natal.v2:" if route_family == "bounded_natal" else ""
    reported_id = "paid_000000000000000000000201"
    pending_id = "paid_000000000000000000000202"
    prepared_id = "paid_000000000000000000000203"
    actions = [
        {
            "action_id": reported_id, "state": "REPORTED",
            "binding": {**_binding(run_id, f"{prefix}pass-1:attempt-002", 7),
                        "request_sha256": "2" * 64},
            "provider": {"id": "resp_qualification_reported", "kind": "response"},
            "reported": {"estimated_micro_usd": 0},
        },
        {
            "action_id": pending_id, "state": "WAITING",
            "binding": {**_binding(run_id, f"{prefix}pass-1:attempt-002", 7),
                        "request_sha256": "1" * 64},
            "provider": {"id": "resp_qualification_pending", "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-28T06:29:00Z",
                "last_outcome": "pending",
                "resume_not_before": "2026-08-28T06:30:00Z",
            },
            "reported": None,
        },
        {
            "action_id": prepared_id, "state": "PREPARED",
            "binding": {**_binding(run_id, f"{prefix}pass-1:attempt-003", 8),
                        "request_sha256": "2" * 64},
        },
        {
            "action_id": "paid_000000000000000000000204", "state": "AUTHORIZED",
            "binding": {**_binding(run_id, f"{prefix}pass-1:attempt-003", 8),
                        "request_sha256": "3" * 64},
            "authorization": {"document_sha256": "4" * 64},
        },
    ]
    state: dict[str, Any] = {
        "schema_version": (
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal"
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        "run_id": run_id, "state_revision": 8,
        "created_at": "2026-08-28T06:00:00Z",
        "updated_at": "2026-08-28T06:29:00Z", "provider": "scripted",
        "provider_configuration": {}, "max_attempts": 3,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {"policy": {
            "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
            "run_ceiling_micro_usd": 100000000,
            "stage_ceilings_micro_usd": {
                name: 100000000 for name in (
                    "authoring_initial", "creative_retry", "polish",
                    "qualitative_critic", "qualitative_candidate",
                )
            },
            "optional_stage_budget_behavior": {
                "polish": "skip", "qualitative_critic": "skip",
                "qualitative_candidate": "skip",
            },
        }, "actions": actions},
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
    _persist(run_dir, state)
    return run_dir, state


def _projection(value: Mapping[str, Any]) -> dict[str, Any]:
    basis = value["checkpoint_basis"]
    decision = value["temporal_decision"]
    lineage = basis["retry_lineage_inventory"]
    return {
        "route_family": basis["native_route"]["route_family"],
        "selected_command": decision["selected_command"],
        "capacity_disposition": decision["capacity_disposition"],
        "due_action_count": len(decision["due_action_ids"]),
        "custody_action_count": len(basis["provider_custody"]["action_ids"]),
        "lineage_status": lineage["status"],
        "conflict_classification": lineage["conflict_classification"],
        "forward_dispatch_permitted": lineage["forward_dispatch_permitted"],
        "reconciliation_permitted": lineage["reconciliation_permitted"],
    }


def run_retry_lineage_qualification() -> dict[str, Any]:
    routes: list[dict[str, Any]] = []
    crash_matrix: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for route_family in ("exact_natal", "bounded_natal"):
            run_dir, state = _materialize(root, route_family)
            first = validate_lifecycle_inspection_v08(
                inspect_retry_lineage_lifecycle(
                    run_dir, observed_at="2026-08-28T06:31:00Z",
                    native_exclusive_access="declared",
                )
            )
            replay = inspect_retry_lineage_lifecycle(
                run_dir, observed_at="2026-08-28T06:31:00Z",
                native_exclusive_access="declared",
            )
            if first != replay:
                raise RuntimeError("Retry-lineage inspection replay differs")
            pending = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == "paid_000000000000000000000202"
            )
            pending["state"] = "REPORTED"
            pending["reported"] = {"estimated_micro_usd": 0}
            state["state_revision"] += 1
            _persist(run_dir, state)
            successor = validate_lifecycle_inspection_v08(
                inspect_retry_lineage_lifecycle(
                    run_dir, observed_at="2026-08-28T06:32:00Z",
                    native_exclusive_access="declared",
                )
            )
            routes.append({
                "route_family": route_family,
                "before": _projection(first), "after": _projection(successor),
                "exact_replay": True,
            })
        fence_states = {
            "prepared": ("PREPARED", None),
            "authorized": ("AUTHORIZED", None),
            "call_entered": ("SUBMITTING", None),
            "provider_identity_durable": ("PROVIDER_ID_RECORDED", "resp_fenced"),
            "reported": ("REPORTED", "resp_fenced"),
        }
        for boundary, (action_state, provider_id) in fence_states.items():
            _run_dir, source = _materialize(root / boundary, "exact_natal")
            member = source["spend_ledger"]["actions"][1]
            member["state"] = action_state
            if provider_id is not None:
                member["provider"] = {"id": provider_id, "kind": "response"}
            blocked = False
            try:
                assert_retry_lineage_forward_dispatch_safe(source)
            except ValueError:
                blocked = True
            crash_matrix.append({
                "boundary": boundary, "create_permitted": not blocked,
            })

    feedback = retry_feedback_from_record({"attempts": [
        {"attempt_number": 2, "state": "PASS_QA_REJECTED", "qa": {"report": {
            "status": "reject", "editorial_issue_codes": ["generic_qa_reject"],
            "affected_claim_ids": ["claim-1"], "guidance": "repair",
        }}},
        {"attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION", "qa": None},
    ]}, before_attempt_number=3)
    feedback_stable = (
        feedback is not None
        and [item["attempt_number"] for item in feedback["prior_rejections"]] == [2]
    )
    body = {
        "schema_version": CONTRACT, "status": "pass",
        "qualification_only": True, "provider_free": True,
        "package": {
            "name": "astrowoof-natal-authoring", "version": _package_version(),
        },
        "schema_sha256": _digest(read_retry_lineage_qualification_schema()),
        "routes": routes, "crash_matrix": crash_matrix,
        "assertions": {
            "custody_precedes_conflict_review": True,
            "post_custody_conflict_is_non_dispatching": True,
            "same_observation_is_exact_replay": True,
            "whole_ledger_conflict_blocks_create": True,
            "completed_predecessor_feedback_is_stable": feedback_stable,
        },
        "external_network_call_count": 0,
        "provider_create_count": 0, "provider_spend_usd": 0,
    }
    return validate_retry_lineage_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_retry_lineage_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "schema_sha256", "routes",
        "crash_matrix", "assertions",
        "external_network_call_count", "provider_create_count",
        "provider_spend_usd",
    }
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ValueError("Retry-lineage qualification fields are not exact")
    if value.get("schema_version") != CONTRACT:
        raise ValueError("Unsupported retry-lineage qualification")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Retry-lineage qualification digest mismatch")
    if (
        value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
    ):
        raise ValueError("Retry-lineage qualification safety posture is invalid")
    package = value.get("package")
    if (
        not isinstance(package, Mapping)
        or set(package) != {"name", "version"}
        or package.get("name") != "astrowoof-natal-authoring"
        or not isinstance(package.get("version"), str)
        or not package["version"]
    ):
        raise ValueError("Retry-lineage qualification package identity is invalid")
    if value.get("schema_sha256") != _digest(read_retry_lineage_qualification_schema()):
        raise ValueError("Retry-lineage qualification schema identity differs")
    routes = value.get("routes")
    if not isinstance(routes, list) or [item.get("route_family") for item in routes] != [
        "exact_natal", "bounded_natal",
    ]:
        raise ValueError("Retry-lineage qualification route inventory is invalid")
    for route in routes:
        if set(route) != {"route_family", "before", "after", "exact_replay"}:
            raise ValueError("Retry-lineage route evidence is not closed")
        if route["exact_replay"] is not True:
            raise ValueError("Retry-lineage replay assertion failed")
        projection_keys = {
            "route_family", "selected_command", "capacity_disposition",
            "due_action_count", "custody_action_count", "lineage_status",
            "conflict_classification", "forward_dispatch_permitted",
            "reconciliation_permitted",
        }
        before = route.get("before")
        after = route.get("after")
        if (
            not isinstance(before, Mapping) or set(before) != projection_keys
            or not isinstance(after, Mapping) or set(after) != projection_keys
            or before.get("route_family") != route["route_family"]
            or after.get("route_family") != route["route_family"]
        ):
            raise ValueError("Retry-lineage route projections are not exact")
        common = {
            "lineage_status": "conflict",
            "conflict_classification": "retry_lineage_conflict_requires_review",
            "forward_dispatch_permitted": False,
            "reconciliation_permitted": True,
        }
        if any(before.get(key) != item or after.get(key) != item for key, item in common.items()):
            raise ValueError("Retry-lineage projection assertions differ")
        if (
            before["selected_command"] != "provider_reconciliation_cycle"
            or before["capacity_disposition"] != "continue_local_cycle"
            or before["due_action_count"] != 1
            or before["custody_action_count"] != 1
        ):
            raise ValueError("Provider custody did not precede lineage review")
        if (
            after["selected_command"] != "none"
            or after["capacity_disposition"] != "retain_for_review"
            or after["due_action_count"] != 0
            or after["custody_action_count"] != 0
        ):
            raise ValueError("Post-custody lineage review differs")
    expected_boundaries = [
        "prepared", "authorized", "call_entered",
        "provider_identity_durable", "reported",
    ]
    if [item.get("boundary") for item in value.get("crash_matrix") or []] != expected_boundaries or any(
        item.get("create_permitted") is not False
        or set(item) != {"boundary", "create_permitted"}
        for item in value.get("crash_matrix") or []
    ):
        raise ValueError("Retry-lineage crash matrix differs")
    assertions = value.get("assertions")
    if not isinstance(assertions, Mapping) or set(assertions) != {
        "custody_precedes_conflict_review",
        "post_custody_conflict_is_non_dispatching",
        "same_observation_is_exact_replay",
        "whole_ledger_conflict_blocks_create",
        "completed_predecessor_feedback_is_stable",
    } or any(item is not True for item in assertions.values()):
        raise ValueError("Retry-lineage qualification assertions failed")
    return deepcopy(dict(value))


def _inside_native_workspace(path: Path) -> bool:
    target = path.resolve()
    return any(
        (parent / "run.json").exists()
        or (parent / "workspace-snapshot.json").exists()
        for parent in (target.parent, *target.parents)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run installed provider-free retry-lineage qualification.",
    )
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.output and _inside_native_workspace(args.output):
        parser.error("--output must not be inside a native SBE workspace")
    value = (
        read_retry_lineage_qualification_schema()
        if args.schema else run_retry_lineage_qualification()
    )
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
