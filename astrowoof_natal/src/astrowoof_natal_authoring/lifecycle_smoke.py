"""Provider-free installed-runtime smoke for public lifecycle contracts."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from .closure import normalized_path, write_workspace_snapshot
from .execution_events import ExecutionEventEmitter
from .lifecycle import closeout_run, deny_providerless_action, inspect_lifecycle
from .lifecycle_contracts import NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA
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
    return {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "lifecycle-smoke-run", "state_revision": 1,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "created_at": "2026-08-13T00:00:00Z",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {"actions": [{
            "action_id": "paid_0123456789abcdef01234567",
            "state": "PREPARED", "binding": binding,
            "authorization": None, "provider": None, "reported": None,
        }]},
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
        "contracts/execution-event-payload-catalog.v1.json",
        "fixtures/lifecycle/negative-authorization-request.v0.1.json",
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
    closeout = closeout_run(
        run_dir, observed_at="2026-08-13T00:00:02Z", event_emitter=emitter
    )
    replay = closeout_run(run_dir)
    checks = {
        "prepared_eligible": action["providerless_denial_eligible"],
        "denial_applied": denial.get("applied"),
        "denial_disposition": denial.get("disposition"),
        "post_denial_reason": after_denial["action_inventory"]["actions"][0]["eligibility_reason"],
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
    expected = {
        "prepared_eligible": True,
        "denial_applied": True,
        "denial_disposition": "DENIED_PROVIDERLESS",
        "post_denial_reason": "already_denied_providerless",
        "closeout_replay_stable": True,
        "snapshot_valid": True,
    }
    for name, expected_value in expected.items():
        if checks[name] != expected_value:
            errors.append(f"{name}: expected {expected_value!r}, got {checks[name]!r}")
    if checks["event_names"] != [
        "authorization.denied_providerless", "closeout.completed"
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
