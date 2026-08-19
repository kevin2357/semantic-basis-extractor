"""Constrained inspection and repair for the SBE 0.2.1 polish checkpoint defect."""

from __future__ import annotations

import argparse
import json
import os
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator

from .application_logging import (
    add_logging_arguments,
    bind_logging_context,
    configure_logging_from_args,
)

from .closure import (
    SNAPSHOT_NAME,
    lint_finding_count,
    load_json,
    normalized_path,
    persist_state,
    sha256_file,
    snapshot_inventory,
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from .spend import AUTHORIZATION_SCHEMA, digest as spend_digest


REPAIR_SCHEMA = "astrowoof.polish_checkpoint_repair.v0.1"
SUPPORTED_RUN_SCHEMA = "astrowoof.semantic_closure_run.v0.9"
SUPPORTED_PROFILE_SCHEMA = "astrowoof.authoring_profile.v0.1"


def _refuse(message: str) -> ValueError:
    return ValueError(f"Unsupported repair shape: {message}")


def _members(value: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = value.get("members")
    if not isinstance(records, list):
        raise _refuse("snapshot members are unavailable")
    return {str(item.get("path")): item for item in records}


def _action_for(
    state: dict[str, Any], *, route: str, expected_state: str
) -> dict[str, Any]:
    matches = [
        action
        for action in (state.get("spend_ledger") or {}).get("actions", [])
        if (action.get("binding") or {}).get("route") == route
    ]
    if len(matches) != 1 or matches[0].get("state") != expected_state:
        raise _refuse(f"expected one {expected_state} action for {route}")
    return matches[0]


def inspect_polish_checkpoint(
    run_dir: Path, *, authorization_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a repair plan and repaired state for the one proven 0.2.1 shape."""
    run_dir = run_dir.resolve()
    run_json = run_dir / "run.json"
    snapshot_path = run_dir / SNAPSHOT_NAME
    if not run_json.is_file() or not snapshot_path.is_file():
        raise _refuse("run.json and workspace-snapshot.json are required")
    state = load_json(run_json)
    snapshot = load_json(snapshot_path)
    if state.get("schema_version") != SUPPORTED_RUN_SCHEMA:
        raise _refuse("run schema is not the affected v0.9 schema")
    if (state.get("authoring_profile") or {}).get("schema_version") != SUPPORTED_PROFILE_SCHEMA:
        raise _refuse("authoring profile is not the qualified v0.1 profile")
    if state.get("status") != "AWAITING_SPEND_AUTHORIZATION":
        raise _refuse("run is not awaiting spend authorization")
    if state.get("subjects"):
        raise _refuse("subject state is not the affected empty mapping")
    contract = state.get("workspace_contract") or {}
    if (
        contract.get("mode") != "stable_logical_absolute_path"
        or contract.get("logical_root") != normalized_path(run_dir)
        or snapshot.get("logical_root") != normalized_path(run_dir)
    ):
        raise _refuse("stable logical workspace identity does not match")

    expected = _members(snapshot)
    actual_records = snapshot_inventory(run_dir, use_process_cache=False)
    actual = {item["path"]: item for item in actual_records}
    if set(expected) != set(actual):
        raise _refuse("snapshot has missing or additional authoritative members")
    changed = sorted(path for path in expected if expected[path] != actual[path])
    subjects = {path.split("/")[1] for path in changed if path.startswith("final/")}
    if len(subjects) != 1:
        raise _refuse("mismatches do not identify exactly one final subject")
    subject = subjects.pop()
    final_root = run_dir / "final" / subject
    expected_changed = sorted([
        f"final/{subject}/natal.{subject}.cards.json",
        f"final/{subject}/natal.{subject}.lint-report.json",
        f"final/{subject}/natal.{subject}.validation-report.json",
    ])
    if changed != expected_changed:
        raise _refuse(
            "mismatch set is not the exact three-file polish shape: "
            f"found {changed!r}"
        )

    attempt_root = final_root / "polish" / "attempt-001"
    pairs = {
        expected_changed[0]: attempt_root / f"natal.{subject}.cards.json",
        expected_changed[1]: attempt_root / "lint-report.json",
        expected_changed[2]: attempt_root / "validation-report.json",
    }
    for relative, retained in pairs.items():
        if not retained.is_file() or sha256_file(run_dir / relative) != sha256_file(retained):
            raise _refuse(f"{relative} is not proven by retained attempt 1 output")

    response_marker = load_json(attempt_root / "openai-background-response.json")
    response = load_json(attempt_root / "openai-response.json")
    request_2_path = final_root / "polish" / "attempt-002" / "openai-request.json"
    if not request_2_path.is_file():
        raise _refuse("prepared attempt 2 request is missing")
    action_1 = _action_for(
        state, route=f"{subject}:polish:001", expected_state="REPORTED"
    )
    action_2 = _action_for(
        state, route=f"{subject}:polish:002", expected_state="PREPARED"
    )
    provider = action_1.get("provider") or {}
    if (
        provider.get("kind") != "response"
        or provider.get("id") != response_marker.get("id")
        or provider.get("id") != response.get("id")
        or not action_1.get("reported")
    ):
        raise _refuse("attempt 1 provider identity or reported cost is inconsistent")
    if any(action_2.get(key) for key in ("authorization", "provider", "consumption", "reported")):
        raise _refuse("attempt 2 is authorized, consumed, submitted, or reported")
    if spend_digest(load_json(request_2_path)) != action_2["binding"].get("request_sha256"):
        raise _refuse("attempt 2 request digest does not match its action binding")
    authorization = load_json(authorization_path)
    if (
        authorization.get("schema_version") != AUTHORIZATION_SCHEMA
        or authorization.get("action_id") != action_2.get("action_id")
        or authorization.get("binding") != action_2.get("binding")
    ):
        raise _refuse("external authorization is not exactly bound to attempt 2")

    validation_path = final_root / f"natal.{subject}.validation-report.json"
    lint_path = final_root / f"natal.{subject}.lint-report.json"
    validation = load_json(validation_path)
    lint = load_json(lint_path)
    assembly_path = final_root / f"natal.{subject}.assembly-report.json"
    packet_path = (
        run_dir / "sbe" / "semantic-basis-output" / subject
        / f"{subject}.selected-authoring-packet.json"
    )
    if not assembly_path.is_file() or not packet_path.is_file():
        raise _refuse("native assembly report or selected packet is missing")
    warning_count = lint_finding_count(lint)
    usage = deepcopy((action_1.get("reported") or {}).get("usage") or {})
    repaired = deepcopy(state)
    repaired["subjects"] = {
        subject: {
            "subject": subject,
            "state": "FINAL_QA_WARN" if validation.get("status") == "pass" else "FINAL_QA_FAILED",
            "packet": normalized_path(packet_path),
            "deck": normalized_path(final_root / f"natal.{subject}.cards.json"),
            "assembly_report": normalized_path(assembly_path),
            "validation_report": normalized_path(validation_path),
            "lint_report": normalized_path(lint_path),
            "validation": {"accepted": validation.get("status") == "pass", "report": validation},
            "lint": {"accepted": True, "report": lint},
            "baseline_warning_count": None,
            "baseline_warning_components": None,
            "polish_attempts": [{
                "attempt_number": 1,
                "state": "POLISH_IMPROVED_PARTIAL",
                "finished_at": response.get("completed_at"),
                "provider_metadata": {
                    "provider": "openai",
                    "response_id": provider["id"],
                    "model": response.get("model"),
                    "requested_model": action_1["binding"].get("model"),
                    "service_level": action_1["binding"].get("service_level"),
                    "usage": usage,
                    "estimated_cost": {
                        "currency": "USD",
                        "estimated_amount": int(action_1["reported"]["estimated_micro_usd"]) / 1_000_000,
                    },
                    "recovered_from": "retained_sbe_polish_artifacts",
                },
                "validation_report": normalized_path(attempt_root / "validation-report.json"),
                "lint_report": normalized_path(attempt_root / "lint-report.json"),
                "warning_count": warning_count,
                "accepted": False,
                "improved": True,
                "error": None,
            }, {
                "attempt_number": 2,
                "state": "SUBMITTED",
                "started_at": None,
                "finished_at": None,
                "provider_metadata": None,
                "validation_report": None,
                "lint_report": None,
                "warning_count": None,
                "accepted": False,
                "transport": {
                    "recovered_prepared_request": normalized_path(request_2_path),
                },
                "error": None,
            }],
            "delivery": None,
            "checkpoint_repair": {
                "schema_version": REPAIR_SCHEMA,
                "source_release": "0.2.1",
                "action_1_id": action_1["action_id"],
                "action_2_id": action_2["action_id"],
            },
        }
    }
    plan = {
        "schema_version": REPAIR_SCHEMA,
        "mode": "dry_run",
        "eligible": True,
        "run_id": state["run_id"],
        "subject": subject,
        "before_state_revision": state.get("state_revision"),
        "before_snapshot_sha256": sha256_file(snapshot_path),
        "accepted_passes_sha256": spend_digest(state.get("passes") or {}),
        "spend_ledger_sha256": spend_digest(state.get("spend_ledger") or {}),
        "changed_members": [
            {
                "path": path,
                "snapshot_sha256": expected[path]["sha256"],
                "actual_sha256": actual[path]["sha256"],
                "retained_attempt_sha256": sha256_file(pairs[path]),
            }
            for path in changed
        ],
        "provider_response_id": provider["id"],
        "reported_micro_usd": action_1["reported"]["estimated_micro_usd"],
        "prepared_action_id": action_2["action_id"],
        "prepared_action_remains_unused": True,
        "authorization_binding_verified": True,
        "changes": [
            "restore subject and attempts 1-2 state",
            "publish complete workspace snapshot",
        ],
    }
    return plan, repaired


def _same_copy(source: Path, backup: Path) -> bool:
    if source.resolve() == backup.resolve() or not backup.is_dir():
        return False
    source_snapshot = source / SNAPSHOT_NAME
    backup_snapshot = backup / SNAPSHOT_NAME
    if (
        not source_snapshot.is_file()
        or not backup_snapshot.is_file()
        or sha256_file(source_snapshot) != sha256_file(backup_snapshot)
    ):
        return False
    return snapshot_inventory(source, use_process_cache=False) == snapshot_inventory(
        backup, use_process_cache=False
    )


@contextmanager
def _exclusive_lock(run_dir: Path) -> Iterator[None]:
    path = run_dir / "spend-consumption.lock"
    with path.open("a+b") as handle:
        handle.seek(0)
        if path.stat().st_size == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def repair_polish_checkpoint(
    run_dir: Path, *, authorization_path: Path, backup_path: Path,
    owner_reference: str,
) -> dict[str, Any]:
    if not owner_reference.strip():
        raise _refuse("exclusive owner reference is required")
    plan, repaired = inspect_polish_checkpoint(
        run_dir, authorization_path=authorization_path
    )
    if not _same_copy(run_dir.resolve(), backup_path.resolve()):
        raise _refuse("backup is not a separate byte-identical complete copy")
    with _exclusive_lock(run_dir):
        second_plan, repaired = inspect_polish_checkpoint(
            run_dir, authorization_path=authorization_path
        )
        if second_plan != plan:
            raise _refuse("workspace changed between inspection and repair lock")
        persist_state(run_dir / "run.json", repaired)
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, repaired)
    plan["mode"] = "apply"
    plan["after_state_revision"] = repaired["state_revision"]
    plan["after_snapshot_sha256"] = sha256_file(run_dir / SNAPSHOT_NAME)
    plan["after_run_sha256"] = sha256_file(run_dir / "run.json")
    plan["backup_path"] = normalized_path(backup_path.resolve())
    plan["exclusive_owner_reference"] = owner_reference
    plan["snapshot_member_count"] = len(snapshot_inventory(run_dir, use_process_cache=False))
    plan["repaired_snapshot_valid"] = True
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--authorization", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-path", type=Path)
    parser.add_argument("--exclusive-owner-reference")
    parser.add_argument("--report", type=Path)
    add_logging_arguments(parser)
    args = parser.parse_args()
    configure_logging_from_args(args)
    run_state_path = args.run_dir / "run.json"
    if run_state_path.is_file():
        existing = load_json(run_state_path)
        bind_logging_context(
            run_id=existing.get("native_run_id") or existing.get("run_id"),
            current_state=(existing.get("machine") or {}).get("state")
            or existing.get("status"),
        )
    if args.apply:
        if args.backup_path is None or not args.exclusive_owner_reference:
            parser.error(
                "--apply requires --backup-path and --exclusive-owner-reference"
            )
        report = repair_polish_checkpoint(
            args.run_dir,
            authorization_path=args.authorization,
            backup_path=args.backup_path,
            owner_reference=args.exclusive_owner_reference,
        )
    else:
        report, _state = inspect_polish_checkpoint(
            args.run_dir, authorization_path=args.authorization
        )
    if args.report:
        report_path = args.report.resolve()
        try:
            report_path.relative_to(args.run_dir.resolve())
        except ValueError:
            pass
        else:
            parser.error("--report must be outside the repaired workspace")
        write_json_atomic(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
