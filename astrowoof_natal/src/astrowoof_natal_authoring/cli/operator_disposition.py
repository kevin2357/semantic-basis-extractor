"""Read one snapshot-bound native operator-disposition assessment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..operator_disposition import read_operator_disposition_assessment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    run_dir = args.run_dir.resolve()
    output = args.output.resolve() if args.output is not None else None
    if output is not None and (output == run_dir or run_dir in output.parents):
        parser.error("--output must resolve outside --run-dir")
    value = read_operator_disposition_assessment(run_dir)
    rendered = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
