"""Assemble an authored Markdown story workspace into a locked cards JSON deck."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any


FIELD_PATTERN = re.compile(
    r"<!-- BEGIN FIELD: ([a-zA-Z0-9_.]+) -->\s*\n"
    r"(.*?)\n"
    r"<!-- END FIELD: \1 -->",
    re.DOTALL,
)
STORY_DIR_PATTERN = re.compile(r"^Story (\d{3}) -- (.+)$")
SUMMARY_DIR_PATTERN = re.compile(r"^Summary (\d{2}) -- (.+)$")
DENSITIES = {"no_astro", "light_astro", "full_astro"}
HUMOR_FIELDS = {
    "funny_dog_quotes",
    "imperative_dog_quotes",
    "applicable_canine_jokes",
}


def normalized_chapter_title(value: str) -> tuple[str, tuple[str, ...]]:
    words = re.findall(r"[a-z0-9]+", value.casefold().replace("&", " and "))
    return " ".join(words), tuple(sorted(word for word in words if word != "and"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_fields(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for match in FIELD_PATTERN.finditer(text):
        field_path = match.group(1)
        value = match.group(2).strip()
        if field_path in fields:
            raise ValueError(f"{path}: duplicate field marker {field_path}")
        fields[field_path] = value
    if not fields:
        raise ValueError(f"{path}: no field markers found")
    unfinished = [
        field_path
        for field_path, value in fields.items()
        if not value or "__WRITE__" in value
    ]
    if unfinished:
        raise ValueError(
            f"{path}: unfinished fields: {', '.join(sorted(unfinished))}"
        )
    begin_count = text.count("<!-- BEGIN FIELD:")
    end_count = text.count("<!-- END FIELD:")
    if begin_count != end_count or begin_count != len(fields):
        raise ValueError(
            f"{path}: damaged or unmatched field markers "
            f"(begin={begin_count}, end={end_count}, parsed={len(fields)})"
        )
    return fields


def parse_list(value: str) -> list[str]:
    lines = []
    for line in value.splitlines():
        item = re.sub(r"^\s*[-*]\s+", "", line).strip()
        if item:
            lines.append(item)
    return lines


def theme_section(card: dict[str, Any]) -> str | None:
    if card.get("claim_type") == "system_interaction":
        return "interdogpendence"
    if card.get("claim_type") == "synthesized_theme":
        return "takeaways"
    return None


def parse_theme_registry(value: str, *, section: str, source: Path) -> list[dict[str, Any]]:
    try:
        registry = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{source}: {section} registry is not valid JSON: {exc}"
        ) from exc
    if not isinstance(registry, list) or not 3 <= len(registry) <= 5:
        raise ValueError(
            f"{source}: {section} registry must contain three to five chapters"
        )
    required = {"id", "title", "short_title", "emoji", "order"}
    allowed = required | {"subtitle"}
    ids: list[str] = []
    titles: list[str] = []
    for index, item in enumerate(registry, 1):
        if (
            not isinstance(item, dict)
            or not required <= set(item)
            or not set(item) <= allowed
        ):
            raise ValueError(
                f"{source}: {section} registry entry {index} must contain "
                f"{sorted(required)} and may contain subtitle"
            )
        if item["order"] != index:
            raise ValueError(
                f"{source}: {section} registry orders must be consecutive "
                "integers starting at 1"
            )
        for field in ("id", "title", "short_title", "emoji"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(
                    f"{source}: {section} entry {index} has invalid {field}"
                )
        if "subtitle" in item and not (
            item["subtitle"] is None or isinstance(item["subtitle"], str)
        ):
            raise ValueError(
                f"{source}: {section} entry {index} has invalid subtitle"
            )
        if not re.fullmatch(r"[a-z][a-z0-9_]*", item["id"]):
            raise ValueError(
                f"{source}: {section} entry {index} has invalid snake_case id"
            )
        ids.append(item["id"])
        titles.append(item["title"].casefold().strip())
    if len(ids) != len(set(ids)) or len(titles) != len(set(titles)):
        raise ValueError(f"{source}: {section} registry repeats an ID or title")
    return registry


def assign_path(target: dict[str, Any], path: str, value: str) -> None:
    parts = path.split(".")
    current: Any = target
    for part in parts[:-1]:
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current[part]
    last = parts[-1]
    parsed_value: Any = value
    if path in {
        "context_filter_groups.high_level",
        "context_filter_groups.detail_level",
    }:
        parsed_value = parse_list(value)
    if isinstance(current, list):
        current[int(last)] = parsed_value
    else:
        current[last] = parsed_value


def card_target_path(field_path: str) -> str:
    first = field_path.split(".", 1)[0]
    if first in DENSITIES or first in HUMOR_FIELDS:
        return f"card.{field_path}"
    return field_path


def apply_writing_file(
    item: dict[str, Any],
    writing_path: Path,
    *,
    summary: bool,
) -> dict[str, Any]:
    result = deepcopy(item)
    fields = parse_fields(writing_path)
    for field_path, value in fields.items():
        if field_path.startswith("plan."):
            continue
        target_path = field_path if summary else card_target_path(field_path)
        try:
            assign_path(result, target_path, value)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ValueError(
                f"{writing_path}: field {field_path} does not match target schema"
            ) from exc
    return result


def assemble(
    packet: dict[str, Any],
    workspace: Path,
    *,
    allow_partial: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    deck = deepcopy(packet)
    if (workspace / "WRITE WHOLE DOG PROFILE.md").is_file():
        workspaces = [workspace]
    else:
        workspaces = sorted(
            path
            for path in workspace.iterdir()
            if path.is_dir()
            and (path / "WRITE WHOLE DOG PROFILE.md").is_file()
        )
        if not workspaces:
            raise ValueError(
                f"{workspace} is neither an authored workspace nor a directory "
                "containing authored pass workspaces"
            )
    whole_dog_profiles = {
        path.name: parse_fields(path / "WRITE WHOLE DOG PROFILE.md")
        for path in workspaces
    }
    cards_by_priority = {
        card["priority_id"]: card for card in packet["cards"]
    }
    authored_priorities: list[int] = []
    for pass_workspace in workspaces:
        cards_root = pass_workspace / "cards"
        if not cards_root.exists():
            continue
        if not cards_root.is_dir():
            raise ValueError(f"Cards path is not a directory: {cards_root}")
        for story_dir in sorted(
            path for path in cards_root.iterdir() if path.is_dir()
        ):
            match = STORY_DIR_PATTERN.match(story_dir.name)
            if not match:
                raise ValueError(
                    f"Unexpected story directory name: {story_dir.name}"
                )
            priority_id = int(match.group(1))
            claim_id = match.group(2)
            if priority_id in authored_priorities:
                raise ValueError(
                    f"Story priority {priority_id} appears in more than one pass"
                )
            source_card = cards_by_priority.get(priority_id)
            if source_card is None:
                raise ValueError(
                    f"Unknown priority ID in workspace: {priority_id}"
                )
            if claim_id != source_card["claim_id"]:
                raise ValueError(
                    f"Story {priority_id}: directory claim ID {claim_id} does "
                    f"not match packet {source_card['claim_id']}"
                )
            writing_path = story_dir / "WRITE THIS CARD.md"
            deck["cards"][priority_id - 1] = apply_writing_file(
                source_card,
                writing_path,
                summary=False,
            )
            authored_priorities.append(priority_id)

    authored_priorities.sort()
    expected_sequence = list(range(1, len(authored_priorities) + 1))
    if authored_priorities != expected_sequence:
        raise ValueError(
            "Story directories must form a continuous sequence beginning at 001; "
            f"found {authored_priorities}"
        )
    if not allow_partial and len(authored_priorities) != len(packet["cards"]):
        raise ValueError(
            f"Full assembly requires {len(packet['cards'])} stories; "
            f"found {len(authored_priorities)}"
        )

    authored_summaries: list[int] = []
    for pass_workspace in workspaces:
        summaries_root = pass_workspace / "summaries"
        if summaries_root.exists():
            for summary_dir in sorted(
                path for path in summaries_root.iterdir() if path.is_dir()
            ):
                match = SUMMARY_DIR_PATTERN.match(summary_dir.name)
                if not match:
                    raise ValueError(
                        f"Unexpected summary directory name: {summary_dir.name}"
                    )
                index = int(match.group(1))
                if index in authored_summaries:
                    raise ValueError(
                        f"Summary {index} appears in more than one pass"
                    )
                key = f"card{index}"
                if key not in packet["summary"]:
                    raise ValueError(f"Unknown Summary index: {index}")
                deck["summary"][key] = apply_writing_file(
                    packet["summary"][key],
                    summary_dir / "WRITE THIS SUMMARY.md",
                    summary=True,
                )
                authored_summaries.append(index)
    authored_summaries.sort()
    if not allow_partial and authored_summaries != [1, 2, 3, 4]:
        raise ValueError(
            "Full assembly requires Summary directories 01 through 04"
        )

    theme_plan_paths = [
        pass_workspace / "ASSIGN THEME GROUPS.md"
        for pass_workspace in workspaces
        if (pass_workspace / "ASSIGN THEME GROUPS.md").is_file()
    ]
    if len(theme_plan_paths) > 1:
        raise ValueError("Theme-group assignment appears in more than one pass")
    authored_theme_priorities: list[int] = []
    if theme_plan_paths:
        theme_fields = parse_fields(theme_plan_paths[0])
        registries: dict[str, list[dict[str, Any]]] = {}
        for section in ("interdogpendence", "takeaways"):
            field = f"theme_group_registry.{section}"
            if field not in theme_fields:
                raise ValueError(f"{theme_plan_paths[0]}: missing field {field}")
            registries[section] = parse_theme_registry(
                theme_fields.pop(field),
                section=section,
                source=theme_plan_paths[0],
            )
        deck["theme_group_registry"] = registries
        registry_ids = {
            section: {entry["id"] for entry in entries}
            for section, entries in registries.items()
        }
        for field_path, value in theme_fields.items():
            match = re.fullmatch(
                r"theme_group\.(interdogpendence|takeaways)\.(\d+)",
                field_path,
            )
            if not match:
                raise ValueError(
                    f"{theme_plan_paths[0]}: unexpected field {field_path}"
                )
            section = match.group(1)
            priority_id = int(match.group(2))
            if not 1 <= priority_id <= len(deck["cards"]):
                raise ValueError(
                    f"{theme_plan_paths[0]}: unknown priority {priority_id}"
                )
            card = deck["cards"][priority_id - 1]
            if "theme_group_id" not in card:
                raise ValueError(
                    f"{theme_plan_paths[0]}: Story {priority_id} does not accept "
                    "a theme group"
                )
            expected_section = theme_section(card)
            if section != expected_section:
                raise ValueError(
                    f"{theme_plan_paths[0]}: Story {priority_id} belongs to "
                    f"{expected_section}, not {section}"
                )
            if value not in registry_ids[section]:
                raise ValueError(
                    f"{theme_plan_paths[0]}: Story {priority_id} references "
                    f"unknown {section} chapter {value!r}"
                )
            card["theme_group_id"] = value
            authored_theme_priorities.append(priority_id)
        normalized_titles = {
            section: {
                normalized_chapter_title(entry["title"])
                for entry in entries
            }
            for section, entries in registries.items()
        }
        if normalized_titles["interdogpendence"] & normalized_titles["takeaways"]:
            raise ValueError(
                "Interdogpendence and Takeaways may not repeat or trivially "
                "reorder chapter titles"
            )
        for section, ids in registry_ids.items():
            counts = Counter(
                card.get("theme_group_id")
                for card in deck["cards"]
                if theme_section(card) == section
            )
            if set(counts) != ids:
                raise ValueError(
                    f"{section} assignments must use every registered chapter"
                )
            sizes = list(counts.values())
            if min(sizes) < 2 or max(sizes) > 2 * min(sizes):
                raise ValueError(
                    f"{section} chapters violate the two-claim minimum or "
                    f"2:1 balance boundary: {dict(counts)}"
                )
    expected_theme_priorities = [
        card["priority_id"]
        for card in deck["cards"]
        if "theme_group_id" in card
    ]
    authored_theme_priorities.sort()
    if (
        not allow_partial
        and len(workspaces) > 1
        and expected_theme_priorities
        and not theme_plan_paths
    ):
        raise ValueError(
            "Multi-pass assembly requires ASSIGN THEME GROUPS.md"
        )
    if (
        not allow_partial
        and authored_theme_priorities
        and authored_theme_priorities != expected_theme_priorities
    ):
        raise ValueError(
            "Theme-group assignment does not cover every aspect and synthesis "
            f"story; found {authored_theme_priorities}"
        )

    report = {
        "schema_version": "astrowoof.story_workspace_assembly.v0.1",
        "status": "pass",
        "subject": (
            packet["subject"].get("subject_id")
            if isinstance(packet["subject"], dict)
            else packet["subject"]
        ),
        "allow_partial": allow_partial,
        "authored_card_count": len(authored_priorities),
        "authored_priority_ids": authored_priorities,
        "next_unfinished_priority_id": (
            len(authored_priorities) + 1
            if len(authored_priorities) < len(packet["cards"])
            else None
        ),
        "authored_summary_ids": authored_summaries,
        "authored_theme_group_priority_ids": authored_theme_priorities,
        "workspace_count": len(workspaces),
        "workspace_names": [path.name for path in workspaces],
        "whole_dog_profile_field_counts": {
            name: len(fields)
            for name, fields in whole_dog_profiles.items()
        },
        "whole_dog_profile_field_count": sum(
            len(fields) for fields in whole_dog_profiles.values()
        ),
        "placeholder_free": "__WRITE__" not in json.dumps(
            {
                "cards": [
                    deck["cards"][priority_id - 1]
                    for priority_id in authored_priorities
                ],
                "summary": [
                    deck["summary"][f"card{index}"]
                    for index in authored_summaries
                ],
            },
            ensure_ascii=False,
        ),
    }
    return deck, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Assemble the continuous authored prefix and leave later packet placeholders.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional assembly-report path; defaults beside the output deck.",
    )
    args = parser.parse_args()
    packet = load_json(args.packet)
    deck, report = assemble(
        packet,
        args.workspace,
        allow_partial=args.allow_partial,
    )
    write_json(args.output, deck)
    report_path = args.report or args.output.with_suffix(
        ".assembly-report.json"
    )
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
