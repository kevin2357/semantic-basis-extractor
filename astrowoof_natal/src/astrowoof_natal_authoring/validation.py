"""Validate an LLM-edited AstroWoof deck against its locked authoring packet."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


LOCKED_TOP_LEVEL = [
    "subject",
    "source",
    "coverage",
    "categories",
    "behavioral_domains",
    "context_filter_groups",
    "unselected_claims",
    "projected_term_registry",
]
LOCKED_CARD_FIELDS = [
    "claim_id", "claim_type", "categories", "importance", "confidence", "strength",
    "priority_id", "selection", "behavioral_domains", "tags", "evidence", "relations",
]
ASTRO_TERMS = re.compile(
    r"\b(?:sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto|"
    r"node|ascendant|descendant|midheaven|astrolog|zodiac|doghouse|"
    r"conjunction|opposition|trine|sextile|quincunx)\b|"
    r"\bhouse\s+(?:[1-9]|1[0-2])\b|"
    r"\b(?:[1-9]|1[0-2])(?:st|nd|rd|th)?\s+house\b|"
    r"\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|"
    r"tenth|eleventh|twelfth)\s+house\b|"
    r"\b(?:your|her|his|their|the|\w+['’]s)\s+chart\b|"
    r"\b(?:the|this|that)\s+square(?:['’]s)?\b|\bsquare\s+aspect\b",
    re.IGNORECASE,
)
BAD_SECOND_PERSON = re.compile(
    r"(?<!of )(?<!in )(?<!for )(?<!with )(?<!within )(?<!through )"
    r"(?<!around )(?<!beside )\byou\s+"
    r"(?:is|has|does|regulates|needs|wants|prefers)\b",
    re.IGNORECASE,
)


def theme_section(card: dict) -> str | None:
    if card.get("claim_type") == "system_interaction":
        return "interdogpendence"
    if card.get("claim_type") == "synthesized_theme":
        return "takeaways"
    return None


def normalized_chapter_title(value: str) -> tuple[str, tuple[str, ...]]:
    words = re.findall(
        r"[a-z0-9]+", value.casefold().replace("&", " and ")
    )
    return (
        " ".join(words),
        tuple(sorted(word for word in words if word != "and")),
    )


def validate_theme_group_registry(
    value: object,
    errors: list[str],
) -> tuple[dict[str, set[str]], dict[str, set[tuple[str, tuple[str, ...]]]]]:
    ids_by_section: dict[str, set[str]] = {}
    titles_by_section: dict[str, set[tuple[str, tuple[str, ...]]]] = {}
    if not isinstance(value, dict) or set(value) != {
        "interdogpendence", "takeaways"
    }:
        errors.append(
            "theme_group_registry must contain interdogpendence and takeaways."
        )
        return ids_by_section, titles_by_section
    required = {"id", "title", "short_title", "emoji", "order"}
    allowed = required | {"subtitle"}
    for section in ("interdogpendence", "takeaways"):
        entries = value.get(section)
        if not isinstance(entries, list) or not 3 <= len(entries) <= 5:
            errors.append(
                f"{section} must define three to five theme-group entries."
            )
            continue
        ids: list[str] = []
        titles: list[tuple[str, tuple[str, ...]]] = []
        for index, item in enumerate(entries, 1):
            if (
                not isinstance(item, dict)
                or not required <= set(item)
                or not set(item) <= allowed
            ):
                errors.append(
                    f"{section} theme-group entry {index} has invalid fields."
                )
                continue
            if item.get("order") != index:
                errors.append(
                    f"{section} theme-group orders must be consecutive from 1."
                )
            for field in ("id", "title", "short_title", "emoji"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(
                        f"{section} theme-group entry {index} has invalid {field}."
                    )
            if "subtitle" in item and not (
                item["subtitle"] is None
                or isinstance(item["subtitle"], str)
            ):
                errors.append(
                    f"{section} theme-group entry {index} has invalid subtitle."
                )
            if isinstance(item.get("id"), str):
                if not re.fullmatch(r"[a-z][a-z0-9_]*", item["id"]):
                    errors.append(
                        f"{section} theme-group entry {index} has invalid ID."
                    )
                ids.append(item["id"])
            if isinstance(item.get("title"), str):
                titles.append(normalized_chapter_title(item["title"]))
        if len(ids) != len(set(ids)):
            errors.append(f"{section} repeats a theme-group ID.")
        if len(titles) != len(set(titles)):
            errors.append(f"{section} repeats or trivially reorders a title.")
        ids_by_section[section] = set(ids)
        titles_by_section[section] = set(titles)
    return ids_by_section, titles_by_section


def validate_editorial_card(
    value: dict,
    label: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    for collection in [
        "funny_dog_quotes", "imperative_dog_quotes", "applicable_canine_jokes"
    ]:
        items = value.get(collection)
        if not isinstance(items, list) or not items or not all(
            isinstance(item, str) and item.strip() for item in items
        ):
            errors.append(f"{label} missing card-level {collection}.")
    for density in ["no_astro", "light_astro", "full_astro"]:
        branch = value.get(density, {})
        for obsolete in [
            "funny_dog_quotes", "imperative_dog_quotes", "applicable_canine_jokes"
        ]:
            if obsolete in branch:
                errors.append(f"{label} retains obsolete {density}.{obsolete}.")
        for part in ["headline", "body"]:
            voice_map = branch.get(part, {})
            for voice in ["handler", "direct_to_dog", "hybrid"]:
                text = voice_map.get(voice, "")
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{label} missing {density}.{part}.{voice}.")
                    continue
                if voice == "direct_to_dog" and BAD_SECOND_PERSON.search(text):
                    errors.append(
                        f"{label} has invalid second-person grammar in "
                        f"{density}.{part}."
                    )
                if density == "no_astro" and ASTRO_TERMS.search(text):
                    warnings.append(
                        f"{label} may contain astrology in no_astro.{part}.{voice}."
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("authoring_packet", type=Path)
    parser.add_argument("edited_deck", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--phase",
        choices=["authoring", "polish"],
        default="authoring",
        help=(
            "authoring allows initial population of filters, theme groups, and "
            "summaries; polish locks them to the completed baseline by default."
        ),
    )
    parser.add_argument(
        "--allow-context-filter-edits",
        action="store_true",
        help="In polish phase, explicitly permit context-filter reassignment.",
    )
    parser.add_argument(
        "--allow-theme-group-edits",
        action="store_true",
        help="In polish phase, explicitly permit chapter/theme regrouping.",
    )
    parser.add_argument(
        "--allow-summary-edits",
        action="store_true",
        help="In polish phase, explicitly permit summary-card changes.",
    )
    args = parser.parse_args()
    if args.phase == "authoring" and any([
        args.allow_context_filter_edits,
        args.allow_theme_group_edits,
        args.allow_summary_edits,
    ]):
        parser.error("Polish edit overrides may only be used with --phase polish.")

    original = json.loads(args.authoring_packet.read_text(encoding="utf-8"))
    edited = json.loads(args.edited_deck.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if len(original.get("cards", [])) != 50 or len(edited.get("cards", [])) != 50:
        errors.append("Both input and output must contain exactly 50 cards.")
    for field in LOCKED_TOP_LEVEL:
        if original.get(field) != edited.get(field):
            errors.append(f"Locked top-level field changed: {field}")

    original_cards = original.get("cards", [])
    edited_cards = edited.get("cards", [])
    registered_filters = {
        level: {
            item["name"]
            for item in edited.get("context_filter_groups", [])
            if item.get("level") == level
        }
        for level in ["high", "detail"]
    }
    registered_categories = set(edited.get("categories", []))
    new_theme_contract = "theme_group_registry" in original
    theme_group_counts = Counter()
    theme_group_counts_by_section = {
        "interdogpendence": Counter(),
        "takeaways": Counter(),
    }
    theme_group_ids: dict[str, set[str]] = {}
    if new_theme_contract:
        theme_group_ids, _ = validate_theme_group_registry(
            edited.get("theme_group_registry"), errors
        )
        if (
            args.phase == "polish"
            and not args.allow_theme_group_edits
            and original.get("theme_group_registry")
            != edited.get("theme_group_registry")
        ):
            errors.append("Polish changed locked theme_group_registry.")
    for index, (before, after) in enumerate(zip(original_cards, edited_cards), 1):
        for field in LOCKED_CARD_FIELDS:
            if before.get(field) != after.get(field):
                errors.append(f"Card {index} changed locked field {field}.")
        categories = after.get("categories")
        if (
            not isinstance(categories, list)
            or not categories
            or len(categories) != len(set(categories))
            or not set(categories) <= registered_categories
        ):
            errors.append(f"Card {index} has invalid categories.")
        if "category" in after:
            errors.append(f"Card {index} retains obsolete category field.")
        if new_theme_contract and "theme_group_id" in before:
            section = theme_section(after)
            theme_group_id = after.get("theme_group_id")
            if (
                section is None
                or not isinstance(theme_group_id, str)
                or theme_group_id not in theme_group_ids.get(section, set())
            ):
                errors.append(f"Card {index} has invalid theme_group_id.")
            else:
                theme_group_counts_by_section[section][theme_group_id] += 1
            if (
                args.phase == "polish"
                and not args.allow_theme_group_edits
                and before.get("theme_group_id") != after.get("theme_group_id")
            ):
                errors.append(
                    f"Card {index} changed locked polish-phase theme_group_id."
                )
            if "theme_group" in after:
                errors.append(f"Card {index} retains legacy theme_group.")
        elif new_theme_contract and "theme_group_id" in after:
            errors.append(f"Card {index} unexpectedly added theme_group_id.")
        elif not new_theme_contract and "theme_group" in before:
            theme_group = after.get("theme_group")
            if not isinstance(theme_group, str) or not theme_group.strip():
                errors.append(f"Card {index} needs a nonempty theme_group.")
            else:
                theme_group_counts[theme_group.strip()] += 1
            if (
                args.phase == "polish"
                and not args.allow_theme_group_edits
                and before.get("theme_group") != after.get("theme_group")
            ):
                errors.append(f"Card {index} changed locked polish-phase theme_group.")
        elif "theme_group" in after:
            errors.append(f"Card {index} unexpectedly added theme_group.")
        filters = after.get("context_filter_groups", {})
        for key, registry_level in [
            ("high_level", "high"),
            ("detail_level", "detail"),
        ]:
            assignments = filters.get(key)
            if (
                not isinstance(assignments, list)
                or len(assignments) != len(set(assignments))
                or not set(assignments) <= registered_filters[registry_level]
            ):
                errors.append(f"Card {index} has invalid {key} context filters.")
            elif len(assignments) > len(registered_filters[registry_level]) / 2:
                warnings.append(
                    f"Card {index} assigns more than half of all {key} filters; "
                    "review for tangential or indiscriminate matches."
                )
        if (
            args.phase == "polish"
            and not args.allow_context_filter_edits
            and before.get("context_filter_groups")
            != after.get("context_filter_groups")
        ):
            errors.append(
                f"Card {index} changed locked polish-phase context filters."
            )
        serialized = json.dumps(after, ensure_ascii=False)
        if "__LLM_FILL__" in serialized:
            errors.append(f"Card {index} retains an editorial placeholder.")
        if len(after.get("dos", [])) != 3 or len(after.get("donts", [])) != 3:
            errors.append(f"Card {index} needs exactly three dos and three donts.")
        validate_editorial_card(
            after.get("card", {}), f"Card {index}", errors, warnings
        )

    if not new_theme_contract:
        group_count = len(theme_group_counts)
        if group_count not in {3, 4}:
            errors.append(
                "Selected aspects and syntheses together must use three or four "
                f"theme groups; found {group_count}."
            )
        if theme_group_counts:
            sizes = list(theme_group_counts.values())
            if min(sizes) < 2 or max(sizes) - min(sizes) > 2:
                errors.append(
                    "Selected aspects and syntheses theme groups are not "
                    f"approximately balanced: {dict(theme_group_counts)}."
                )

    summary = edited.get("summary", {})
    if list(summary) != ["card1", "card2", "card3", "card4"]:
        errors.append("Edited deck must contain summary.card1 through summary.card4.")
    for key, summary_card in summary.items():
        if (
            len(summary_card.get("dos", [])) != 3
            or len(summary_card.get("donts", [])) != 3
        ):
            errors.append(
                f"Summary {key} needs exactly three dos and three donts."
            )
        validate_editorial_card(
            summary_card, f"Summary {key}", errors, warnings
        )
    if (
        args.phase == "polish"
        and not args.allow_summary_edits
        and original.get("summary") != edited.get("summary")
    ):
        errors.append("Polish phase changed locked summary content.")

    report = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "card_count": len(edited.get("cards", [])),
            "phase": args.phase,
            "polish_edit_overrides": {
                "context_filters": args.allow_context_filter_edits,
                "theme_groups": args.allow_theme_group_edits,
                "summary": args.allow_summary_edits,
            },
            "locked_top_level_fields_checked": LOCKED_TOP_LEVEL,
            "locked_card_fields_checked": LOCKED_CARD_FIELDS,
            "summary_card_count": len(edited.get("summary", {})),
            "unselected_claim_count": len(edited.get("unselected_claims", [])),
            "placeholder_free": "__LLM_FILL__" not in json.dumps(edited),
        },
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
