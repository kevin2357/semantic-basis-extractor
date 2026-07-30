#!/usr/bin/env python3
"""Deterministic repetition and failure-signature lint for AstroWoof decks."""

from __future__ import annotations

import argparse
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


DENSITIES = ("no_astro", "light_astro", "full_astro")
VOICES = ("handler", "direct_to_dog", "hybrid")
HUMOR_FIELDS = (
    "funny_dog_quotes",
    "imperative_dog_quotes",
    "applicable_canine_jokes",
)
PROCESS_PATTERNS = {
    "selected claim": r"\bselected claim\b",
    "retained evidence": r"\bretained evidence\b",
    "semantic profile": r"\bsemantic profile\b",
    "projected reading": r"\bprojected reading\b",
    "graph processing": r"\bgraph processing\b",
    "unspecified pattern": r"\bunspecified pattern\b",
    "whole personality": r"\bwhole personality\b",
    "mode mode": r"\bmode mode\b",
    "recurring pattern pattern": r"\brecurring pattern pattern\b",
}
TEMPLATE_PATTERNS = {
    "filing-system humor": r"\b(?:filed it under|filed a .* report)\b",
    "numbered observation padding": r"\bobservation\s+\d+\s+in\s+the\b",
    "stock matter suffix": r"\bthis is specifically an?\b",
    "household department": r"\bhousehold department\b",
    "protocol humor": r"\brespect the .* protocol\b",
    "fine-print humor": r"\bthe fine print\b",
}
GRAMMAR_PATTERNS = {
    "invalid ordinal": r"\b(?:1th|2th|3th)\b",
    "article before vowel sound": (
        r"\ba\s+(?:emotional|expansive|intense|investigative|immediate|"
        r"awkward|easy|unusual|active|open|exact)\b"
    ),
}
PASS_NGRAM_WORDS = 12
PASS_NGRAM_MIN_CLAIMS = 3


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", text.lower())


def sentences(text: str) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"(?<=[.!?])\s+", text)
        if item.strip()
    ]


def rendering_items(
    container: dict[str, Any],
    location: str,
    claim_id: str,
    claim_type: str,
) -> Iterable[dict[str, str]]:
    for density in DENSITIES:
        branch = container.get(density, {})
        for kind in ("headline", "body"):
            voice_map = branch.get(kind, {})
            for voice in VOICES:
                text = voice_map.get(voice)
                if isinstance(text, str) and text.strip():
                    yield {
                        "location": location,
                        "claim_id": claim_id,
                        "claim_type": claim_type,
                        "density": density,
                        "kind": kind,
                        "voice": voice,
                        "field": f"{density}.{kind}.{voice}",
                        "text": text.strip(),
                    }


def reader_facing_items(deck: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for card in deck.get("cards", []):
        claim_id = str(card.get("claim_id", ""))
        claim_type = str(card.get("claim_type", ""))
        location = f"card:{claim_id}"
        items.extend(
            rendering_items(
                card.get("card", {}),
                location,
                claim_id,
                claim_type,
            )
        )
        for field in ("dos", "donts"):
            for index, text in enumerate(card.get(field, [])):
                if isinstance(text, str) and text.strip():
                    items.append({
                        "location": location,
                        "claim_id": claim_id,
                        "claim_type": claim_type,
                        "density": "",
                        "kind": field,
                        "voice": "",
                        "field": f"{field}[{index}]",
                        "text": text.strip(),
                    })
        card_container = card.get("card", {})
        for field in HUMOR_FIELDS:
            for index, text in enumerate(card_container.get(field, [])):
                if isinstance(text, str) and text.strip():
                    items.append({
                        "location": location,
                        "claim_id": claim_id,
                        "claim_type": claim_type,
                        "density": "",
                        "kind": "humor",
                        "voice": "",
                        "field": f"{field}[{index}]",
                        "text": text.strip(),
                    })
    for summary_key, summary in deck.get("summary", {}).items():
        location = f"summary:{summary_key}"
        items.extend(
            rendering_items(summary, location, location, "summary")
        )
        for field in ("dos", "donts", *HUMOR_FIELDS):
            for index, text in enumerate(summary.get(field, [])):
                if isinstance(text, str) and text.strip():
                    items.append({
                        "location": location,
                        "claim_id": location,
                        "claim_type": "summary",
                        "density": "",
                        "kind": field,
                        "voice": "",
                        "field": f"{field}[{index}]",
                        "text": text.strip(),
                    })
    return items


def warning(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, "details": details}


def authoring_pass_acceptance(
    items: list[dict[str, str]],
) -> dict[str, Any]:
    """Return a deterministic accept/reject verdict for an authored pass.

    Comparisons are made across distinct claims or summaries. Related density
    and voice renderings within one card are deliberately treated as one
    location so their expected semantic overlap cannot reject a pass.
    """
    reasons: list[dict[str, Any]] = []
    exact_duplicate_groups: list[dict[str, Any]] = []

    for kind in ("headline", "body", "dos", "donts", "humor"):
        occurrences: dict[str, set[str]] = defaultdict(set)
        fields: dict[str, list[str]] = defaultdict(list)
        for item in items:
            if item["kind"] != kind:
                continue
            normalized = " ".join(item["text"].lower().split())
            occurrences[normalized].add(item["claim_id"])
            fields[normalized].append(
                f"{item['location']}:{item['field']}"
            )
        for text, claim_ids in occurrences.items():
            if len(claim_ids) < 2:
                continue
            exact_duplicate_groups.append({
                "kind": kind,
                "claim_count": len(claim_ids),
                "claim_ids": sorted(claim_ids),
                "locations": fields[text],
                "excerpt": text[:240],
            })

    if exact_duplicate_groups:
        reasons.append({
            "code": "cross_card_exact_duplicate",
            "message": (
                "Reader-facing text is reused exactly across distinct cards "
                "or summaries."
            ),
            "group_count": len(exact_duplicate_groups),
        })

    ngram_claims: dict[str, set[str]] = defaultdict(set)
    for item in items:
        if item["kind"] != "body":
            continue
        tokens = words(item["text"])
        item_ngrams = {
            " ".join(tokens[index:index + PASS_NGRAM_WORDS])
            for index in range(len(tokens) - PASS_NGRAM_WORDS + 1)
        }
        for ngram in item_ngrams:
            ngram_claims[ngram].add(item["claim_id"])

    repeated_ngrams = [
        {
            "claim_count": len(claim_ids),
            "claim_ids": sorted(claim_ids),
            "text": ngram,
        }
        for ngram, claim_ids in ngram_claims.items()
        if len(claim_ids) >= PASS_NGRAM_MIN_CLAIMS
    ]
    repeated_ngrams.sort(
        key=lambda item: (-item["claim_count"], item["text"])
    )
    if repeated_ngrams:
        reasons.append({
            "code": "cross_card_repeated_passage",
            "message": (
                f"A {PASS_NGRAM_WORDS}-word passage occurs in "
                f"{PASS_NGRAM_MIN_CLAIMS} or more distinct cards or summaries."
            ),
            "group_count": len(repeated_ngrams),
            "maximum_claim_count": repeated_ngrams[0]["claim_count"],
        })

    suspicious_artifacts: list[dict[str, Any]] = []
    for item in items:
        if item["kind"] not in {"headline", "body", "dos", "donts", "humor"}:
            continue
        bracketed = sorted(set(re.findall(r"\[[^\]\n]{1,80}\]", item["text"])))
        if bracketed:
            suspicious_artifacts.append({
                "claim_id": item["claim_id"],
                "field": item["field"],
                "kind": "bracketed_editorial_insertion",
                "examples": bracketed[:5],
            })
        if item["kind"] == "body":
            tokens = words(item["text"])
            four_grams = Counter(
                " ".join(tokens[index:index + 4])
                for index in range(len(tokens) - 3)
            )
            repeated_inside = [
                {"text": phrase, "count": count}
                for phrase, count in four_grams.items()
                if count >= 4
            ]
            if repeated_inside:
                repeated_inside.sort(
                    key=lambda value: (-value["count"], value["text"])
                )
                suspicious_artifacts.append({
                    "claim_id": item["claim_id"],
                    "field": item["field"],
                    "kind": "repeated_insertion_within_field",
                    "examples": repeated_inside[:5],
                })
    if suspicious_artifacts:
        reasons.append({
            "code": "editorial_artifact_insertion",
            "message": (
                "Reader-facing prose contains repeated or bracketed insertion "
                "artifacts inconsistent with natural card writing."
            ),
            "occurrence_count": len(suspicious_artifacts),
        })

    opening_locations: dict[tuple[str, str], set[str]] = defaultdict(set)
    for item in items:
        if item["kind"] != "body":
            continue
        opening = " ".join(words(item["text"])[:3])
        if opening:
            opening_locations[(item["field"], opening)].add(item["claim_id"])
    dominant_openings = [
        {
            "field": field,
            "opening": opening,
            "claim_count": len(claim_ids),
            "claim_ids": sorted(claim_ids),
        }
        for (field, opening), claim_ids in opening_locations.items()
        if len(claim_ids) >= 8
    ]
    dominant_openings.sort(
        key=lambda value: (
            -value["claim_count"],
            value["field"],
            value["opening"],
        )
    )
    if len(dominant_openings) >= 2:
        reasons.append({
            "code": "multi_field_opening_template",
            "message": (
                "The same opening dominates nearly every card in multiple "
                "reader-facing field positions."
            ),
            "group_count": len(dominant_openings),
        })

    return {
        "status": "accept" if not reasons else "reject",
        "deterministic": True,
        "thresholds": {
            "ngram_words": PASS_NGRAM_WORDS,
            "ngram_min_distinct_claims": PASS_NGRAM_MIN_CLAIMS,
        },
        "reader_facing_field_count": len(items),
        "distinct_location_count": len({
            item["claim_id"] for item in items
        }),
        "exact_duplicate_group_count": len(exact_duplicate_groups),
        "exact_duplicate_groups": exact_duplicate_groups,
        "repeated_ngram_group_count": len(repeated_ngrams),
        "repeated_ngrams": repeated_ngrams,
        "suspicious_artifact_count": len(suspicious_artifacts),
        "suspicious_artifacts": suspicious_artifacts,
        "dominant_opening_group_count": len(dominant_openings),
        "dominant_openings": dominant_openings,
        "rejection_reasons": reasons,
    }


def lint_deck(path: Path, deck: dict[str, Any]) -> dict[str, Any]:
    items = reader_facing_items(deck)
    warnings: list[dict[str, Any]] = []

    bodies = [x for x in items if x["kind"] == "body"]
    body_locations: dict[str, list[str]] = defaultdict(list)
    for item in bodies:
        body_locations[item["text"]].append(
            f"{item['location']}:{item['field']}"
        )
    for text, locations in body_locations.items():
        claim_locations = {x.split(":", 2)[1] for x in locations}
        if len(claim_locations) > 1:
            warnings.append(warning(
                "duplicate_body",
                "An exact body is reused across claims.",
                occurrences=len(locations),
                locations=locations,
                excerpt=text[:240],
            ))

    sentence_locations: dict[str, set[str]] = defaultdict(set)
    for item in bodies:
        for sentence in sentences(item["text"]):
            if len(words(sentence)) >= 7:
                sentence_locations[sentence].add(item["claim_id"])
    for text, claim_ids in sentence_locations.items():
        if len(claim_ids) >= 3:
            warnings.append(warning(
                "repeated_sentence",
                "A complete sentence appears under three or more claims.",
                claim_count=len(claim_ids),
                claim_ids=sorted(claim_ids),
                excerpt=text[:240],
            ))

    openings: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for item in bodies:
        opening = " ".join(words(item["text"])[:3])
        openings[(item["field"], opening)].append(item)
    for (field, opening), matches in openings.items():
        if opening and len(matches) >= 6:
            warnings.append(warning(
                "repeated_opening",
                "A three-word body opening is used six or more times.",
                field=field,
                opening=opening,
                count=len(matches),
                claim_ids=[x["claim_id"] for x in matches],
            ))

    by_claim_type: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    type_sizes: Counter[tuple[str, str, str]] = Counter()
    for item in bodies:
        key = (item["claim_type"], item["density"], item["voice"])
        by_claim_type[key][" ".join(words(item["text"])[:3])] += 1
        type_sizes[key] += 1
    for key, counts in by_claim_type.items():
        opening, count = counts.most_common(1)[0]
        size = type_sizes[key]
        if size >= 4 and count >= 4 and count / size >= 0.5:
            warnings.append(warning(
                "claim_type_template",
                "One opening dominates a claim type, suggesting a renderer template.",
                claim_type=key[0],
                density=key[1],
                voice=key[2],
                opening=opening,
                count=count,
                group_size=size,
            ))

    for kind in ("dos", "donts", "humor"):
        field_items = [x for x in items if x["kind"] == kind]
        reused: dict[str, set[str]] = defaultdict(set)
        for item in field_items:
            reused[item["text"]].add(item["claim_id"])
        for text, claim_ids in reused.items():
            if len(claim_ids) > 1:
                warnings.append(warning(
                    f"duplicate_{kind}",
                    f"Exact {kind} text is reused across claims.",
                    claim_count=len(claim_ids),
                    claim_ids=sorted(claim_ids),
                    excerpt=text[:240],
                ))

    for item in items:
        for label, pattern in {**PROCESS_PATTERNS, **GRAMMAR_PATTERNS}.items():
            if re.search(pattern, item["text"], re.IGNORECASE):
                warnings.append(warning(
                    "failure_signature",
                    f"Reader-facing text matches the '{label}' failure signature.",
                    location=item["location"],
                    field=item["field"],
                    excerpt=item["text"][:240],
                ))
    for label, pattern in TEMPLATE_PATTERNS.items():
        matches = [
            item for item in items
            if re.search(pattern, item["text"], re.IGNORECASE)
        ]
        if len(matches) >= 3:
            warnings.append(warning(
                "repeated_failure_signature",
                f"The '{label}' mechanism appears three or more times.",
                count=len(matches),
                locations=[
                    f"{item['location']}:{item['field']}"
                    for item in matches
                ],
                excerpts=[item["text"][:160] for item in matches[:5]],
            ))

    return {
        "path": str(path),
        "subject": deck.get("subject", {}).get("subject_id"),
        "reader_facing_field_count": len(items),
        "warning_count": len(warnings),
        "warnings": warnings,
        "authoring_pass_acceptance": authoring_pass_acceptance(items),
    }


def cross_subject_warnings(
    records: list[tuple[Path, dict[str, Any]]],
) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    item_sets: dict[str, dict[str, list[str]]] = {}
    for path, deck in records:
        subject = str(deck.get("subject", {}).get("subject_id") or path.stem)
        values: dict[str, list[str]] = defaultdict(list)
        for item in reader_facing_items(deck):
            values[item["text"]].append(
                f"{item['location']}:{item['field']}"
            )
        item_sets[subject] = values
    for left, right in itertools.combinations(sorted(item_sets), 2):
        overlap = sorted(set(item_sets[left]) & set(item_sets[right]))
        for text in overlap:
            warnings.append(warning(
                "cross_subject_duplicate",
                "Exact reader-facing text appears in two subject decks.",
                subjects=[left, right],
                left_locations=item_sets[left][text],
                right_locations=item_sets[right][text],
                excerpt=text[:240],
            ))
    return warnings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("decks", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in args.decks
    ]
    deck_reports = [lint_deck(path, deck) for path, deck in records]
    cross = cross_subject_warnings(records) if len(records) > 1 else []
    total = sum(x["warning_count"] for x in deck_reports) + len(cross)
    report = {
        "schema_version": "astrowoof.editorial_lint.v0.1",
        "status": "pass" if total == 0 else "warn",
        "warning_count": total,
        "decks": deck_reports,
        "cross_subject_warnings": cross,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if total == 0 else 2)


if __name__ == "__main__":
    main()
