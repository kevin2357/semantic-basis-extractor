"""Supported lifecycle inspection, denial, and closeout consumer CLI."""

from __future__ import annotations

import argparse
import json
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
from .. import __version__


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
    subparsers = parser.add_subparsers(dest="operation", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument(
        "--native-exclusive-access",
        choices=("established", "declared", "not_established", "unknown"),
        default="not_established",
    )
    inspect_parser.add_argument("--observed-at")

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
    if args.stdout_jsonl:
        StdoutJsonlSink()(command_result_envelope(result))
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
