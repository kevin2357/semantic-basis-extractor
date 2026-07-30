"""Validate an LLM-edited AstroWoof deck against its locked authoring packet."""

import argparse
import json
import re
from pathlib import Path


LOCKED_TOP_LEVEL = ["subject", "source", "coverage", "categories", "behavioral_domains"]
LOCKED_CARD_FIELDS = [
    "claim_id", "claim_type", "category", "importance", "confidence", "strength",
    "priority_id", "selection", "behavioral_domains", "tags", "evidence", "relations",
]
ASTRO_TERMS = re.compile(
    r"\b(?:sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto|"
    r"node|ascendant|descendant|midheaven|astrolog|zodiac|house|doghouse|"
    r"conjunction|opposition|square|trine|sextile|quincunx|chart)\b",
    re.IGNORECASE,
)
BAD_SECOND_PERSON = re.compile(r"\byou\s+(?:is|has|does|regulates|needs|wants|prefers)\b", re.IGNORECASE)


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
    for index, (before, after) in enumerate(zip(original_cards, edited_cards), 1):
        for field in LOCKED_CARD_FIELDS:
            if before.get(field) != after.get(field):
                errors.append(f"Card {index} changed locked field {field}.")
        serialized = json.dumps(after, ensure_ascii=False)
        if "__LLM_FILL__" in serialized:
            errors.append(f"Card {index} retains an editorial placeholder.")
        if len(after.get("dos", [])) < 2 or len(after.get("donts", [])) < 2:
            errors.append(f"Card {index} needs at least two dos and two donts.")
        renderings = after.get("card", {})
        for density in ["no_astro", "light_astro", "full_astro"]:
            branch = renderings.get(density, {})
            for part in ["headline", "body"]:
                voice_map = branch.get(part, {})
                for voice in ["handler", "direct_to_dog", "hybrid"]:
                    text = voice_map.get(voice, "")
                    if not isinstance(text, str) or not text.strip():
                        errors.append(f"Card {index} missing {density}.{part}.{voice}.")
                    if voice == "direct_to_dog" and BAD_SECOND_PERSON.search(text):
                        errors.append(f"Card {index} has invalid second-person grammar in {density}.{part}.")
                    if density == "no_astro" and ASTRO_TERMS.search(text):
                        warnings.append(f"Card {index} may contain astrology in no_astro.{part}.{voice}.")
            for collection in [
                "funny_dog_quotes", "imperative_dog_quotes", "applicable_canine_jokes"
            ]:
                if not branch.get(collection):
                    errors.append(f"Card {index} missing {density}.{collection}.")

    report = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "card_count": len(edited.get("cards", [])),
            "locked_top_level_fields_checked": LOCKED_TOP_LEVEL,
            "locked_card_fields_checked": LOCKED_CARD_FIELDS,
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
