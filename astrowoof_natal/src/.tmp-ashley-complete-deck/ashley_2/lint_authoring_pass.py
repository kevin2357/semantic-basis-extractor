#!/usr/bin/env python3
"""Deterministically accept or reject one authored Markdown workspace pass."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from assemble_authoring_workspace import parse_fields
from lint_astrowoof_editorial import (
    HUMOR_FIELDS,
    authoring_pass_acceptance,
)


STORY_PATTERN = re.compile(r"^Story (\d{3}) -- (.+)$")
SUMMARY_PATTERN = re.compile(r"^Summary (\d{2}) -- (.+)$")


def item(
    *,
    location: str,
    claim_id: str,
    field: str,
    kind: str,
    text: str,
) -> dict[str, str]:
    return {
        "location": location,
        "claim_id": claim_id,
        "claim_type": "authoring_workspace",
        "density": "",
        "kind": kind,
        "voice": "",
        "field": field,
        "text": text,
    }


def field_kind(field: str) -> str | None:
    if ".headline." in field:
        return "headline"
    if ".body." in field:
        return "body"
    if field.startswith("dos."):
        return "dos"
    if field.startswith("donts."):
        return "donts"
    if any(field.startswith(f"{name}.") for name in HUMOR_FIELDS):
        return "humor"
    return None


def workspace_items(workspace: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    cards_root = workspace / "cards"
    if cards_root.is_dir():
        for story_dir in sorted(path for path in cards_root.iterdir() if path.is_dir()):
            match = STORY_PATTERN.match(story_dir.name)
            if not match:
                raise ValueError(f"Unexpected story directory: {story_dir.name}")
            claim_id = match.group(2)
            location = f"story:{match.group(1)}:{claim_id}"
            fields = parse_fields(story_dir / "WRITE THIS CARD.md")
            for field, text in fields.items():
                kind = field_kind(field)
                if kind:
                    items.append(item(
                        location=location,
                        claim_id=claim_id,
                        field=field,
                        kind=kind,
                        text=text,
                    ))

    summaries_root = workspace / "summaries"
    if summaries_root.is_dir():
        for summary_dir in sorted(
            path for path in summaries_root.iterdir() if path.is_dir()
        ):
            match = SUMMARY_PATTERN.match(summary_dir.name)
            if not match:
                raise ValueError(
                    f"Unexpected summary directory: {summary_dir.name}"
                )
            claim_id = f"summary:{match.group(1)}"
            fields = parse_fields(summary_dir / "WRITE THIS SUMMARY.md")
            for field, text in fields.items():
                kind = field_kind(field)
                if kind:
                    items.append(item(
                        location=claim_id,
                        claim_id=claim_id,
                        field=field,
                        kind=kind,
                        text=text,
                    ))
    if not items:
        raise ValueError(f"No authored card or summary fields found in {workspace}")
    return items


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report: dict[str, Any] = {
        "schema_version": "astrowoof.authoring_pass_lint.v0.1",
        "workspace": str(args.workspace),
        **authoring_pass_acceptance(workspace_items(args.workspace)),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if report["status"] == "accept" else 2)


if __name__ == "__main__":
    main()
