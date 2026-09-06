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
from ..run_timeline import (
    build_run_cohort_timeline,
    read_run_cohort_timeline,
    render_run_cohort_timeline_html,
)


def _local_path(value: str) -> Path:
    if "://" in value:
        raise argparse.ArgumentTypeError("network URLs are not supported; use a local file")
    return Path(value)


def _read_report(path: Path) -> dict:
    return read_run_evolution_report(path)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    parse = subparsers.add_parser("parse", help="Normalize and reduce one exported log")
    parse.add_argument("--input", type=_local_path, required=True)
    parse.add_argument("--output", type=_local_path, required=True)
    render = subparsers.add_parser("render", help="Render one validated report")
    render.add_argument("--report", type=_local_path, required=True)
    render.add_argument("--format", choices=("md", "html", "mermaid", "timeline-html"), required=True)
    render.add_argument("--output", type=_local_path, required=True)
    render.add_argument("--display-timezone", default="UTC")
    build = subparsers.add_parser(
        "build", help="Create existing report outputs and cohort timeline when evidence permits",
    )
    build.add_argument("--input", type=_local_path, required=True)
    build.add_argument("--output-dir", type=_local_path, required=True)
    build.add_argument("--display-timezone", default="UTC")
    timeline = subparsers.add_parser("timeline", help="Create a shared-time cohort timeline from one exported log")
    timeline.add_argument("--input", type=_local_path, required=True)
    timeline.add_argument("--output-dir", type=_local_path, required=True)
    timeline.add_argument("--display-timezone", default="UTC")
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
        if args.format == "timeline-html":
            timeline = read_run_cohort_timeline(args.report)
            _write(args.output, render_run_cohort_timeline_html(
                timeline, display_timezone=args.display_timezone,
            ))
            return 0
        report = _read_report(args.report)
        renderer = {
            "md": render_report_markdown,
            "html": render_report_html,
            "mermaid": render_report_mermaid,
        }[args.format]
        _write(args.output, renderer(report))
        return 0
    if args.command == "timeline":
        text = args.input.read_text(encoding="utf-8-sig")
        report = build_report_from_text(text, source_name=args.input.name)
        projection = build_run_cohort_timeline(report, text, source_name=args.input.name)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write(args.output_dir / "report.timeline.json", json.dumps(
            projection, indent=2, sort_keys=True,
        ) + "\n")
        _write(args.output_dir / "report.timeline.html", render_run_cohort_timeline_html(
            projection, display_timezone=args.display_timezone,
        ))
        return 0
    report = build_report_from_text(
        args.input.read_text(encoding="utf-8-sig"), source_name=args.input.name,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write(args.output_dir / "report.json", json.dumps(report, indent=2, sort_keys=True) + "\n")
    _write(args.output_dir / "report.md", render_report_markdown(report))
    _write(args.output_dir / "report.html", render_report_html(report))
    _write(args.output_dir / "report.mmd", render_report_mermaid(report))
    try:
        projection = build_run_cohort_timeline(report, args.input.read_text(
            encoding="utf-8-sig",
        ), source_name=args.input.name)
    except ValueError as error:
        if "at least one run" not in str(error):
            raise
    else:
        _write(args.output_dir / "report.timeline.json", json.dumps(
            projection, indent=2, sort_keys=True,
        ) + "\n")
        _write(args.output_dir / "report.timeline.html", render_run_cohort_timeline_html(
            projection, display_timezone=args.display_timezone,
        ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
