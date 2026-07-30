"""Validate an LLM-edited AstroWoof deck against its locked authoring packet."""

import argparse
import json
import re
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
    r"node|ascendant|descendant|midheaven|astrolog|zodiac|house|doghouse|"
    r"conjunction|opposition|square|trine|sextile|quincunx|chart)\b",
    re.IGNORECASE,
)
BAD_SECOND_PERSON = re.compile(r"\byou\s+(?:is|has|does|regulates|needs|wants|prefers)\b", re.IGNORECASE)


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
    args = parser.parse_args()

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
        if "theme_group" in before:
            theme_group = after.get("theme_group")
            if not isinstance(theme_group, str) or not theme_group.strip():
                errors.append(f"Card {index} needs a nonempty theme_group.")
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
                or not assignments
                or len(assignments) != len(set(assignments))
                or not set(assignments) <= registered_filters[registry_level]
            ):
                errors.append(f"Card {index} has invalid {key} context filters.")
        serialized = json.dumps(after, ensure_ascii=False)
        if "__LLM_FILL__" in serialized:
            errors.append(f"Card {index} retains an editorial placeholder.")
        if len(after.get("dos", [])) < 2 or len(after.get("donts", [])) < 2:
            errors.append(f"Card {index} needs at least two dos and two donts.")
        validate_editorial_card(
            after.get("card", {}), f"Card {index}", errors, warnings
        )

    summary = edited.get("summary", {})
    if list(summary) != ["card1", "card2", "card3", "card4"]:
        errors.append("Edited deck must contain summary.card1 through summary.card4.")
    for key, summary_card in summary.items():
        if len(summary_card.get("dos", [])) < 2 or len(summary_card.get("donts", [])) < 2:
            errors.append(f"Summary {key} needs at least two dos and two donts.")
        validate_editorial_card(
            summary_card, f"Summary {key}", errors, warnings
        )

    report = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "card_count": len(edited.get("cards", [])),
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
