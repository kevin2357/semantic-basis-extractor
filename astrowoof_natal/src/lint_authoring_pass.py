#!/usr/bin/env python3
"""Deterministically accept or reject one authored Markdown workspace pass."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

from assemble_authoring_workspace import parse_fields
from lint_astrowoof_editorial import (
    HUMOR_FIELDS,
    authoring_pass_acceptance,
)


STORY_PATTERN = re.compile(r"^Story (\d{3}) -- (.+)$")
SUMMARY_PATTERN = re.compile(r"^Summary (\d{2}) -- (.+)$")
CONTEXT_FILTER_VOCABULARY = {
    "context_filter_groups.high_level": {
        "Personality", "Learning", "Play", "Adventure", "Communication",
        "Trust", "Training", "Pack",
    },
    "context_filter_groups.detail_level": {
        "Core Personality", "Mind & Intelligence",
        "Emotions & Inner World", "Energy & Motivation",
        "Strengths & Talents", "Growth & Potential", "Play & Adventure",
        "Learning & Training", "Communication", "Social & Pack Life",
        "Trust & Security", "Stress & Resilience",
    },
}


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


def invalid_context_filter_claim_ids(workspace: Path) -> list[str]:
    """Return cards whose authored filter lists use unregistered labels."""
    invalid: set[str] = set()
    cards_root = workspace / "cards"
    if not cards_root.is_dir():
        return []
    for story_dir in sorted(path for path in cards_root.iterdir() if path.is_dir()):
        match = STORY_PATTERN.match(story_dir.name)
        if not match:
            continue
        fields = parse_fields(story_dir / "WRITE THIS CARD.md")
        for field, allowed in CONTEXT_FILTER_VOCABULARY.items():
            values = {
                re.sub(r"^\s*[-*]\s+", "", line).strip()
                for line in fields.get(field, "").splitlines()
                if re.sub(r"^\s*[-*]\s+", "", line).strip()
            }
            if not values <= allowed:
                invalid.add(match.group(2))
    return sorted(invalid)


def invalid_theme_group_claim_ids(workspace: Path) -> tuple[list[str], str | None]:
    """Enforce the same chapter-count and balance contract as final QA."""
    assignment = workspace / "ASSIGN THEME GROUPS.md"
    if not assignment.is_file():
        return [], None
    fields = parse_fields(assignment)
    assignments = {
        field.removeprefix("theme_group."): value.strip()
        for field, value in fields.items()
        if field.startswith("theme_group.") and value.strip()
    }
    counts = Counter(assignments.values())
    claim_ids = sorted(assignments, key=lambda value: int(value))
    if not counts:
        return claim_ids, "missing_theme_group_plan"
    sizes = list(counts.values())
    if len(counts) not in {3, 4}:
        return claim_ids, "theme_group_count"
    if min(sizes) < 2 or max(sizes) - min(sizes) > 2:
        return claim_ids, "theme_group_balance"
    return [], None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    full_report: dict[str, Any] = {
        "schema_version": "astrowoof.authoring_pass_lint.v0.1",
        "workspace": str(args.workspace),
        **authoring_pass_acceptance(workspace_items(args.workspace)),
    }
    invalid_filter_claim_ids = invalid_context_filter_claim_ids(args.workspace)
    if invalid_filter_claim_ids:
        full_report["status"] = "reject"
        full_report["rejection_reasons"].append({
            "code": "invalid_context_filter",
            "message": "One or more cards use an unregistered context filter.",
            "claim_ids": invalid_filter_claim_ids,
        })
    invalid_theme_claim_ids, theme_issue = invalid_theme_group_claim_ids(
        args.workspace
    )
    if theme_issue:
        full_report["status"] = "reject"
        full_report["rejection_reasons"].append({
            "code": theme_issue,
            "message": (
                "The aspect and synthesis chapter plan must contain three or "
                "four approximately balanced groups."
            ),
            "claim_ids": invalid_theme_claim_ids,
        })
    if os.environ.get("ASTROWOOF_OPAQUE_ACCEPTANCE") == "1":
        affected_claim_ids = sorted({
            claim_id
            for group in (
                full_report["exact_duplicate_groups"]
                + full_report["repeated_ngrams"]
                + full_report["suspicious_artifacts"]
                + full_report["dominant_openings"]
            )
            for claim_id in group.get("claim_ids", [])
        } | set(invalid_filter_claim_ids) | set(invalid_theme_claim_ids))
        issue_codes = [
            reason["code"]
            for reason in full_report["rejection_reasons"]
        ]
        report: dict[str, Any] = {
            "schema_version": "astrowoof.authoring_pass_gate.v0.1",
            "workspace": str(args.workspace),
            "status": full_report["status"],
            "editorial_issue_codes": issue_codes,
            "affected_claim_ids": affected_claim_ids,
            "guidance": (
                "Treat this result as an editorial signal rather than a puzzle "
                "about the checker. Return to the affected plans and rewrite "
                "the cards as natural, memorable, genuinely independent "
                "pieces. Follow GUIDING LIGHTS.md, then rerun this check."
                if issue_codes
                else "The pass cleared the bundled editorial gate."
            ),
        }
    else:
        report = full_report
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if report["status"] == "accept" else 2)


if __name__ == "__main__":
    main()
