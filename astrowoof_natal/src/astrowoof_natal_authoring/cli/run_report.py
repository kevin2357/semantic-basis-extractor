"""Build deterministic diagnostic reports from exported SBE worker logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..run_report import (
    build_report_from_text,
    render_report_html,
    render_report_markdown,
    render_report_mermaid,
    read_run_evolution_report,
    validate_run_evolution_report,
)


def _read_report(path: Path) -> dict:
    return read_run_evolution_report(path)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    parse = subparsers.add_parser("parse", help="Normalize and reduce one exported log")
    parse.add_argument("--input", type=Path, required=True)
    parse.add_argument("--output", type=Path, required=True)
    render = subparsers.add_parser("render", help="Render one validated report")
    render.add_argument("--report", type=Path, required=True)
    render.add_argument("--format", choices=("md", "html", "mermaid"), required=True)
    render.add_argument("--output", type=Path, required=True)
    build = subparsers.add_parser("build", help="Create JSON, Markdown, HTML, and Mermaid")
    build.add_argument("--input", type=Path, required=True)
    build.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "parse":
        report = build_report_from_text(
            args.input.read_text(encoding="utf-8-sig"), source_name=args.input.name,
        )
        _write(args.output, json.dumps(report, indent=2, sort_keys=True) + "\n")
        return 0
    if args.command == "render":
        report = _read_report(args.report)
        renderer = {
            "md": render_report_markdown,
            "html": render_report_html,
            "mermaid": render_report_mermaid,
        }[args.format]
        _write(args.output, renderer(report))
        return 0
    report = build_report_from_text(
        args.input.read_text(encoding="utf-8-sig"), source_name=args.input.name,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write(args.output_dir / "report.json", json.dumps(report, indent=2, sort_keys=True) + "\n")
    _write(args.output_dir / "report.md", render_report_markdown(report))
    _write(args.output_dir / "report.html", render_report_html(report))
    _write(args.output_dir / "report.mmd", render_report_mermaid(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
