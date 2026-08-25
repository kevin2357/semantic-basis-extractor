from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..provider_economics_export import read_provider_economics_export


def _outside_workspace(output: Path, run_dir: Path) -> None:
    resolved = output.resolve()
    root = run_dir.resolve()
    if resolved == root or root in resolved.parents:
        raise ValueError("provider economics output must be outside the native workspace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export snapshot-validated provider economics revisions"
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--observed-at", required=True)
    parser.add_argument("--previous-revisions", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    previous = []
    if args.previous_revisions is not None:
        value = json.loads(args.previous_revisions.read_text(encoding="utf-8"))
        previous = value.get("revisions") if isinstance(value, dict) else value
        if not isinstance(previous, list):
            raise ValueError("previous revisions must be an array or export object")
    export = read_provider_economics_export(
        args.run_dir, observed_at=args.observed_at, previous_revisions=previous,
    )
    rendered = json.dumps(export, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        _outside_workspace(args.output, args.run_dir)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
