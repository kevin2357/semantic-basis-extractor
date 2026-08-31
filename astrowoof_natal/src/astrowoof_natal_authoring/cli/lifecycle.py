"""Supported lifecycle inspection, denial, and closeout consumer CLI."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from ..execution_events import (
    ExecutionEventEmitter,
    JsonlEventSink,
    StdoutJsonlSink,
    command_result_envelope,
)
from ..lifecycle import (
    closeout_run,
    deny_providerless_action,
    deny_providerless_actions,
    inspect_lifecycle,
    reconcile_required_providerless_denial,
)
from ..closure import load_json
from ..temporal_lifecycle import inspect_temporal_lifecycle
from ..post_fan_in_contracts import inspect_post_fan_in_lifecycle
from ..retry_lineage_contracts import inspect_retry_lineage_lifecycle
from .. import __version__
from ..application_logging import (
    add_logging_arguments,
    bind_logging_context,
    configure_logging_from_args,
)
from ..trace_observability import log_cli_exit, log_decision_summary


logger = logging.getLogger(__name__)


def _outside_workspace(path: Path, run_dir: Path, parser: argparse.ArgumentParser) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(run_dir.resolve())
    except ValueError:
        return resolved
    parser.error("event JSONL must be outside the authoritative run workspace")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--events-jsonl", type=Path)
    parser.add_argument("--stdout-jsonl", action="store_true")
    add_logging_arguments(parser)
    subparsers = parser.add_subparsers(dest="operation", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument(
        "--native-exclusive-access",
        choices=("established", "declared", "not_established", "unknown"),
        default="not_established",
    )
    inspect_parser.add_argument("--observed-at")

    temporal_parser = subparsers.add_parser("inspect-temporal")
    temporal_parser.add_argument(
        "--native-exclusive-access",
        choices=("established", "declared", "not_established", "unknown"),
        default="not_established",
    )
    temporal_parser.add_argument("--observed-at", required=True)

    local_parser = subparsers.add_parser("inspect-local-work")
    local_parser.add_argument(
        "--native-exclusive-access",
        choices=("established", "declared", "not_established", "unknown"),
        default="not_established",
    )
    local_parser.add_argument("--observed-at", required=True)

    lineage_parser = subparsers.add_parser("inspect-retry-lineage")
    lineage_parser.add_argument(
        "--native-exclusive-access",
        choices=("established", "declared", "not_established", "unknown"),
        default="not_established",
    )
    lineage_parser.add_argument("--observed-at", required=True)

    deny_parser = subparsers.add_parser("deny-providerless")
    deny_parser.add_argument("--request", required=True, type=Path)
    deny_parser.add_argument("--decision-at")

    batch_deny_parser = subparsers.add_parser("deny-providerless-batch")
    batch_deny_parser.add_argument("--request", required=True, type=Path)
    batch_deny_parser.add_argument("--decision-at")

    reconcile_parser = subparsers.add_parser("reconcile-required-denial")
    reconcile_parser.add_argument("--reconciled-at")

    closeout_parser = subparsers.add_parser("closeout")
    closeout_parser.add_argument("--observed-at")

    args = parser.parse_args()
    configure_logging_from_args(args)
    if (args.run_dir / "run.json").is_file():
        existing = load_json(args.run_dir / "run.json")
        bind_logging_context(
            run_id=existing.get("run_id"), current_state=existing.get("status")
        )
    logger.info("command_start command=lifecycle operation=%s", args.operation)
    if args.events_jsonl and args.stdout_jsonl:
        parser.error("choose only one event transport")
    sink = None
    if args.stdout_jsonl:
        sink = StdoutJsonlSink()
    elif args.events_jsonl:
        sink = JsonlEventSink(_outside_workspace(args.events_jsonl, args.run_dir, parser))
    emitter = (
        ExecutionEventEmitter(release=__version__, sink=sink)
        if sink is not None else None
    )

    if args.operation == "inspect":
        result = inspect_lifecycle(
            args.run_dir,
            native_exclusive_access=args.native_exclusive_access,
            observed_at=args.observed_at,
            event_emitter=emitter,
            allow_unversioned_local_resume=False,
        )
    elif args.operation == "inspect-temporal":
        result = inspect_temporal_lifecycle(
            args.run_dir,
            native_exclusive_access=args.native_exclusive_access,
            observed_at=args.observed_at,
        )
    elif args.operation == "inspect-local-work":
        result = inspect_post_fan_in_lifecycle(
            args.run_dir,
            native_exclusive_access=args.native_exclusive_access,
            observed_at=args.observed_at,
            event_emitter=emitter,
        )
    elif args.operation == "inspect-retry-lineage":
        result = inspect_retry_lineage_lifecycle(
            args.run_dir,
            native_exclusive_access=args.native_exclusive_access,
            observed_at=args.observed_at,
        )
    elif args.operation == "deny-providerless":
        result = deny_providerless_action(
            args.run_dir, load_json(args.request),
            decision_at=args.decision_at, event_emitter=emitter,
        )
    elif args.operation == "deny-providerless-batch":
        result = deny_providerless_actions(
            args.run_dir, load_json(args.request),
            decision_at=args.decision_at, event_emitter=emitter,
        )
    elif args.operation == "reconcile-required-denial":
        reconcile_required_providerless_denial(
            args.run_dir, reconciled_at=args.reconciled_at,
            event_emitter=emitter,
        )
        result = inspect_lifecycle(
            args.run_dir, native_exclusive_access="declared",
            observed_at=args.reconciled_at,
        )
    else:
        result = closeout_run(
            args.run_dir, observed_at=args.observed_at, event_emitter=emitter,
        )
    logger.info(
        "command_complete command=lifecycle operation=%s outcome=%s",
        args.operation, result.get("outcome", result.get("disposition", "complete")),
    )
    log_decision_summary(
        logger, result, command="lifecycle", operation=args.operation,
    )
    log_cli_exit(
        logger, command="lifecycle", operation=args.operation, exit_code=0,
        outcome=result.get("outcome", result.get("disposition", "complete")),
        result_id=result.get("result_id"), receipt_id=result.get("receipt_id"),
        authoritative_transport="stdout_jsonl" if args.stdout_jsonl else "stdout_json",
    )
    if args.stdout_jsonl:
        StdoutJsonlSink()(command_result_envelope(result))
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
