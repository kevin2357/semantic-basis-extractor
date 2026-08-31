"""Validate and export one immutable native transition result without mutation."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from ..native_transitions import (
    latest_native_transition_result,
    read_native_transition_result,
)
from ..application_logging import add_logging_arguments, configure_logging_from_args
from ..trace_observability import log_cli_exit, log_decision_summary


logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--result-id")
    selection.add_argument(
        "--latest", action="store_true",
        help="Derived convenience only; explicit --result-id is authoritative.",
    )
    parser.add_argument("--output", type=Path)
    add_logging_arguments(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging_from_args(args)
    logger.info(
        "command_start command=native_transition selection=%s",
        "latest" if args.latest else "explicit",
    )
    run_dir = args.run_dir.resolve()
    output = args.output.resolve() if args.output is not None else None
    if output is not None and (output == run_dir or run_dir in output.parents):
        parser.error("--output must resolve outside --run-dir")
    value = (
        latest_native_transition_result(run_dir)
        if args.latest else read_native_transition_result(run_dir, args.result_id)
    )
    public_result = value.get("result") if isinstance(value.get("result"), dict) else value
    log_decision_summary(
        logger, public_result, command="native_transition",
        operation="latest" if args.latest else "explicit",
    )
    logger.info(
        "native_result_read result_id=%s outcome=%s",
        value.get("result_id") or public_result.get("result_id"),
        public_result.get("outcome"),
    )
    rendered = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    log_cli_exit(
        logger, command="native_transition",
        operation="latest" if args.latest else "explicit", exit_code=0,
        outcome=public_result.get("outcome"),
        result_id=value.get("result_id") or public_result.get("result_id"),
        receipt_id=(value.get("receipt") or {}).get("receipt_id")
        if isinstance(value.get("receipt"), dict) else value.get("receipt_id"),
        authoritative_transport="output_file_and_stdout" if output else "stdout_json",
    )


if __name__ == "__main__":
    main()
