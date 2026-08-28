"""Provider-free installed-runtime smoke for public lifecycle contracts."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any

from .closure import normalized_path, write_workspace_snapshot
from .execution_events import ExecutionEventEmitter
from .lifecycle import (
    closeout_run,
    deny_providerless_action,
    deny_providerless_actions,
    inspect_lifecycle,
)
from .lifecycle_contracts import (
    BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from .resource_access import read_resource_text


SMOKE_SCHEMA = "astrowoof.authoring_lifecycle_smoke.v0.1"


def _state(run_dir: Path) -> dict[str, Any]:
    binding = {
        "run_id": "lifecycle-smoke-run", "profile_sha256": "1" * 64,
        "prepared_state_revision": 1, "stage": "polish",
        "route": "fixture:polish:001", "request_sha256": "2" * 64,
        "model": "gpt-5.6-luna", "service_level": "batch",
        "maximum_output_tokens": 1000, "commitment_micro_usd": 1000,
        "price_book_version": "openai-public-2026-08-07.v1",
    }
    actions = [{
        "action_id": "paid_0123456789abcdef01234567",
        "state": "PREPARED", "binding": binding,
        "authorization": None, "provider": None, "reported": None,
    }]
    for attempt, action_id in (
        (1, "paid_111111111111111111111111"),
        (2, "paid_222222222222222222222222"),
    ):
        retry_binding = copy.deepcopy(binding)
        retry_binding.update({
            "prepared_state_revision": attempt + 1,
            "stage": "creative_retry",
            "route": f"fixture:creative_retry:{attempt:03d}",
            "request_sha256": str(attempt + 2) * 64,
        })
        actions.append({
            "action_id": action_id,
            "state": "AUTHORIZED",
            "binding": retry_binding,
            "authorization": {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": copy.deepcopy(retry_binding),
                "authorization_reference": f"lifecycle-smoke-slot-{attempt}",
            },
            "provider": None,
            "reported": None,
        })
    return {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "lifecycle-smoke-run", "state_revision": 1,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "created_at": "2026-08-13T00:00:00Z",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {"actions": actions},
        "passes": {}, "subjects": {}, "provenance": {},
    }


def run_lifecycle_smoke(work_dir: Path, *, require_installed: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    package_root = Path(__file__).resolve().parent
    if require_installed and not any(
        part.lower() == "site-packages" for part in package_root.parts
    ):
        errors.append(f"runtime did not load from site-packages: {package_root}")
    # Prove installed package resources, not source-relative files, are available.
    for resource_name in (
        "contracts/authoring-lifecycle-contracts.schema.json",
        "contracts/contract-catalog.json",
        "contracts/native-transition-contracts.schema.json",
        "contracts/terminal-review-result-v0.2.schema.json",
        "contracts/terminal-review-command-result-v0.1.schema.json",
        "contracts/terminal-review-qualification.v1.schema.json",
        "contracts/execution-event-payload-catalog.v1.json",
        "contracts/initial-wave-contracts.v1.schema.json",
        "contracts/initial-wave-result.v1.schema.json",
        "contracts/initial-authoring-wave-binding-bundle.v1.schema.json",
        "contracts/initial-authoring-wave-authority-inputs.v1.schema.json",
        "contracts/deployed-qa-four-route-qualification.v1.schema.json",
        "contracts/response-retrieval-diagnostic.v1.schema.json",
        "fixtures/lifecycle/negative-authorization-request.v0.1.json",
        "fixtures/lifecycle/batch-negative-authorization-request.v0.1.json",
        "fixtures/lifecycle/batch-negative-authorization-result.v0.1.json",
        "fixtures/lifecycle/negative-authorization-result.v0.2.json",
        "fixtures/lifecycle/batch-negative-authorization-result.v0.2.json",
        "fixtures/lifecycle/inspection.v0.2.json",
        "fixtures/lifecycle/reconciliation-policy.v0.1.json",
        "fixtures/lifecycle/reconciliation-cycle-not-due.v0.1.json",
        "fixtures/lifecycle/response-retrieval-transport-warning.v1.json",
        "fixtures/lifecycle/terminal-review-qualification.v1.json",
        "fixtures/lifecycle/route-parity-transition-oracle.v1.json",
        "fixtures/lifecycle/route-parity-transition-oracle.v2.json",
        "fixtures/lifecycle/bounded-route-parity-traces.v1.json",
        "fixtures/initial_wave/prepared-wave.v1.json",
        "fixtures/initial_wave/wave-authorization.v1.json",
        "fixtures/initial_wave/six-id-detach.v1.json",
        "fixtures/initial_wave/partial-ambiguity.v1.json",
        "fixtures/initial_wave/exact-binding-bundle.v1.json",
        "fixtures/initial_wave/bounded-binding-bundle.v1.json",
        "fixtures/native_transition/review-terminal-receipt.v0.1.json",
        "fixtures/native_transition/consumer-ingestion-cases.v0.1.json",
    ):
        try:
            json.loads(read_resource_text(resource_name))
        except Exception as exc:
            errors.append(f"packaged resource unavailable: {resource_name}: {exc}")

    run_dir = work_dir / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    state = _state(run_dir)
    (run_dir / "run.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)
    observed_at = "2026-08-13T00:00:00Z"
    inspection = inspect_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at
    )
    action = inspection["action_inventory"]["actions"][0]
    request = {
        "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
        "run_id": state["run_id"], "action_id": action["action_id"],
        "binding": action["binding"], "observed": inspection["observation"],
        "denial_reason": "reservation_unavailable",
        "external_authority_reference": "lifecycle-smoke-authority",
    }
    events: list[dict[str, Any]] = []
    emitter = ExecutionEventEmitter(
        release="installed-smoke", sink=events.append,
        base_correlation={"native_run_id": state["run_id"]},
    )
    denial = deny_providerless_action(run_dir, request, event_emitter=emitter)
    after_denial = inspect_lifecycle(
        run_dir, native_exclusive_access="declared",
        observed_at="2026-08-13T00:00:01Z",
    )
    batch_actions = [
        item for item in after_denial["action_inventory"]["actions"]
        if item["providerless_denial_eligible"]
    ]
    batch_request = {
        "schema_version": BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
        "run_id": state["run_id"],
        "observed": after_denial["observation"],
        "actions": [{
            "action_id": item["action_id"],
            "binding": item["binding"],
            "denial_reason": "reservation_unavailable",
            "external_authority_reference": f"lifecycle-smoke-batch:{index}",
        } for index, item in enumerate(batch_actions, start=1)],
    }
    batch_denial = deny_providerless_actions(
        run_dir, batch_request, event_emitter=emitter
    )
    batch_replay = deny_providerless_actions(
        run_dir, batch_request, event_emitter=emitter
    )
    closeout = closeout_run(
        run_dir, observed_at="2026-08-13T00:00:02Z", event_emitter=emitter
    )
    replay = closeout_run(run_dir)
    checks = {
        "public_reconciliation_surface": False,
        "public_native_result_surface": False,
        "prepared_eligible": action["providerless_denial_eligible"],
        "denial_applied": denial.get("applied"),
        "denial_disposition": denial.get("disposition"),
        "post_denial_reason": next(
            item["eligibility_reason"]
            for item in after_denial["action_inventory"]["actions"]
            if item["action_id"] == action["action_id"]
        ),
        "denial_result_schema": denial.get("schema_version"),
        "denial_terminal_outcome": (denial.get("run_transition") or {}).get("outcome"),
        "inspection_terminal": after_denial["terminal"]["terminal"],
        "inspection_terminal_outcome": after_denial["terminal"]["outcome"],
        "inspection_local_dependency_count": len(after_denial["local_dependencies"]),
        "batch_denial_applied": batch_denial.get("applied"),
        "batch_action_count": len(batch_denial.get("actions") or []),
        "batch_replay_outcome": batch_replay.get("outcome"),
        "batch_replay_stable": (
            batch_denial.get("result_checkpoint") == batch_replay.get("result_checkpoint")
        ),
        "closeout_disposition": closeout.get("disposition"),
        "closeout_replay_stable": (
            closeout.get("semantic_result_sha256") == replay.get("semantic_result_sha256")
            and closeout.get("result_checkpoint") == replay.get("result_checkpoint")
        ),
        "event_names": [item["event_name"] for item in events],
        "snapshot_valid": inspect_lifecycle(
            run_dir, native_exclusive_access="declared"
        )["observation"]["inventory_valid"],
    }
    try:
        from . import (
            NativeTransitionResultView,
            ProviderReconciliationAdapters,
            latest_native_transition_result,
            read_native_transition_result,
            reconcile_authoring_provider_cycle,
            read_bounded_route_parity_traces,
            read_route_parity_oracle,
        )
        checks["public_reconciliation_surface"] = bool(
            ProviderReconciliationAdapters
            and reconcile_authoring_provider_cycle.__annotations__
        )
        checks["public_native_result_surface"] = bool(
            NativeTransitionResultView
            and callable(read_native_transition_result)
            and callable(latest_native_transition_result)
        )
        checks["route_parity_resources"] = bool(
            read_route_parity_oracle()["scenarios"]
            and read_bounded_route_parity_traces()["traces"]
        )
    except Exception as exc:
        errors.append(f"public reconciliation surface unavailable: {exc}")
    expected = {
        "public_reconciliation_surface": True,
        "public_native_result_surface": True,
        "route_parity_resources": True,
        "prepared_eligible": True,
        "denial_applied": True,
        "denial_disposition": "DENIED_PROVIDERLESS",
        "post_denial_reason": "already_denied_providerless",
        "denial_result_schema": "astrowoof.provider_negative_authorization_result.v0.2",
        "denial_terminal_outcome": "terminalized",
        "inspection_terminal": True,
        "inspection_terminal_outcome": "budget_exhausted",
        "inspection_local_dependency_count": 0,
        "batch_denial_applied": True,
        "batch_action_count": 2,
        "batch_replay_outcome": "idempotent_replay",
        "batch_replay_stable": True,
        "closeout_disposition": "closed",
        "closeout_replay_stable": True,
        "snapshot_valid": True,
    }
    for name, expected_value in expected.items():
        if checks[name] != expected_value:
            errors.append(f"{name}: expected {expected_value!r}, got {checks[name]!r}")
    if checks["event_names"] != [
        "authorization.denied_providerless",
        "terminal.transitioned",
        "authorization.denied_providerless",
        "authorization.denied_providerless",
        "authorization.denied_providerless_batch",
        "authorization.denied_providerless_batch",
        "closeout.completed",
    ]:
        errors.append(f"unexpected lifecycle events: {checks['event_names']!r}")
    return {
        "schema_version": SMOKE_SCHEMA,
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "runtime_module": str(package_root),
        "require_installed": require_installed,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-installed", action="store_true")
    args = parser.parse_args()
    if args.work_dir:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        report = run_lifecycle_smoke(
            args.work_dir, require_installed=args.require_installed
        )
    else:
        with tempfile.TemporaryDirectory(prefix="astrowoof-lifecycle-smoke-") as temp:
            report = run_lifecycle_smoke(
                Path(temp), require_installed=args.require_installed
            )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if report["status"] != "pass":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
