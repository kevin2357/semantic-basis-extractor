"""Discover whether an exact sealed native transition result is available."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..application_logging import add_logging_arguments, configure_logging_from_args
from ..native_transition_availability import (
    read_native_transition_result_availability,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    add_logging_arguments(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging_from_args(args)
    run_dir = args.run_dir.resolve()
    output = args.output.resolve() if args.output is not None else None
    if output is not None and (output == run_dir or run_dir in output.parents):
        parser.error("--output must resolve outside --run-dir")
    value = read_native_transition_result_availability(run_dir)
    rendered = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
