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


def normalized_chapter_title(value: str) -> tuple[str, tuple[str, ...]]:
    words = re.findall(
        r"[a-z0-9]+",
        value.casefold().replace("&", " and "),
    )
    normalized = " ".join(words)
    return normalized, tuple(sorted(word for word in words if word != "and"))


def theme_group_plan_issues(
    workspace: Path,
) -> list[dict[str, Any]]:
    """Validate independent aspect and synthesis chapter plans."""
    assignment = workspace / "ASSIGN THEME GROUPS.md"
    if not assignment.is_file():
        return []
    fields = parse_fields(assignment)
    issues: list[dict[str, Any]] = []
    titles_by_section: dict[str, list[str]] = {}
    for section in ("interdogpendence", "takeaways"):
        registry_field = f"theme_group_registry.{section}"
        affected = sorted(
            (
                field.rsplit(".", 1)[-1]
                for field in fields
                if field.startswith(f"theme_group.{section}.")
            ),
            key=int,
        )
        try:
            registry = json.loads(fields.get(registry_field, ""))
        except json.JSONDecodeError:
            registry = None
        if not isinstance(registry, list) or not 3 <= len(registry) <= 5:
            issues.append({
                "code": "theme_group_registry",
                "message": (
                    f"{section} must define a valid registry with three to "
                    "five chapters."
                ),
                "claim_ids": affected,
            })
            continue
        required = {
            "id", "title", "short_title", "emoji", "subtitle", "order"
        }
        valid_registry = all(
            isinstance(item, dict)
            and set(item) == required
            and item.get("order") == index
            and all(
                isinstance(item.get(field), str) and item[field].strip()
                for field in (
                    "id", "title", "short_title", "emoji", "subtitle"
                )
            )
            and re.fullmatch(r"[a-z][a-z0-9_]*", item["id"])
            for index, item in enumerate(registry, 1)
        )
        ids = [item.get("id") for item in registry if isinstance(item, dict)]
        titles = [
            item.get("title", "") for item in registry if isinstance(item, dict)
        ]
        if (
            not valid_registry
            or len(ids) != len(set(ids))
            or len(titles) != len(set(title.casefold() for title in titles))
        ):
            issues.append({
                "code": "theme_group_registry",
                "message": f"{section} contains invalid chapter metadata.",
                "claim_ids": affected,
            })
            continue
        titles_by_section[section] = titles
        assignments = {
            field.rsplit(".", 1)[-1]: value.strip()
            for field, value in fields.items()
            if field.startswith(f"theme_group.{section}.") and value.strip()
        }
        counts = Counter(assignments.values())
        if set(counts) != set(ids):
            issues.append({
                "code": "theme_group_coverage",
                "message": (
                    f"{section} assignments must use every registered chapter "
                    "and no unregistered chapter."
                ),
                "claim_ids": affected,
            })
            continue
        sizes = list(counts.values())
        if min(sizes) < 2 or max(sizes) > 2 * min(sizes):
            issues.append({
                "code": "theme_group_balance",
                "message": (
                    f"{section} chapters must contain at least two claims and "
                    "the largest may not exceed twice the smallest."
                ),
                "claim_ids": affected,
            })
    if set(titles_by_section) == {"interdogpendence", "takeaways"}:
        first = {
            normalized_chapter_title(title)
            for title in titles_by_section["interdogpendence"]
        }
        second = {
            normalized_chapter_title(title)
            for title in titles_by_section["takeaways"]
        }
        if first & second:
            affected = sorted(
                (
                    field.rsplit(".", 1)[-1]
                    for field in fields
                    if field.startswith("theme_group.interdogpendence.")
                    or field.startswith("theme_group.takeaways.")
                ),
                key=int,
            )
            issues.append({
                "code": "cross_section_theme_mirroring",
                "message": (
                    "Interdogpendence and Takeaways may not reuse or trivially "
                    "reorder chapter titles."
                ),
                "claim_ids": affected,
            })
    return issues


def invalid_theme_group_claim_ids(workspace: Path) -> tuple[list[str], str | None]:
    """Backward-compatible first-issue view used by callers and tests."""
    issues = theme_group_plan_issues(workspace)
    if not issues:
        return [], None
    return issues[0]["claim_ids"], issues[0]["code"]


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
    theme_issues = theme_group_plan_issues(args.workspace)
    invalid_theme_claim_ids = sorted({
        claim_id
        for issue in theme_issues
        for claim_id in issue["claim_ids"]
    })
    for theme_issue in theme_issues:
        full_report["status"] = "reject"
        full_report["rejection_reasons"].append(theme_issue)
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
