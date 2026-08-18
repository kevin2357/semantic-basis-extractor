"""Validate and export one immutable native transition result without mutation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..native_transitions import (
    latest_native_transition_result,
    read_native_transition_result,
)


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
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    output = args.output.resolve() if args.output is not None else None
    if output is not None and (output == run_dir or run_dir in output.parents):
        parser.error("--output must resolve outside --run-dir")
    value = (
        latest_native_transition_result(run_dir)
        if args.latest else read_native_transition_result(run_dir, args.result_id)
    )
    rendered = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
