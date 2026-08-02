#!/usr/bin/env python3
"""Produce deterministic comparison metrics for the Phase-1 Kevin summaries."""

from __future__ import annotations

import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[8]
AUTOMATED = REPO / "astrowoof_natal/qa/reference_decks/kevin/20260801-automated-live-base/natal.kevin.cards.json"
MANUAL = REPO / "astrowoof_natal/qa/reference_decks/kevin/20260730-six-pass-final/natal.kevin.cards.json"
CANDIDATE = HERE / "natal.kevin.phase1-production.cards.json"

DENSITIES = ("no_astro", "light_astro", "full_astro")
AUDIENCES = ("handler", "direct_to_dog", "hybrid")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?", text.lower())


def summary_fields(deck: dict):
    for card_id, card in deck["summary"].items():
        for density in DENSITIES:
            for kind in ("headline", "body"):
                for audience in AUDIENCES:
                    yield (
                        f"{card_id}.{density}.{kind}.{audience}",
                        card[density][kind][audience],
                    )


def summary_bodies(deck: dict):
    for card_id, card in deck["summary"].items():
        for density in DENSITIES:
            for audience in AUDIENCES:
                yield (
                    f"{card_id}.{density}.body.{audience}",
                    card[density]["body"][audience],
                )


def ngrams(text: str, size: int) -> set[tuple[str, ...]]:
    tokens = words(text)
    return {tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1)}


def longest_word_match(left: str, right: str) -> dict:
    left_words = words(left)
    right_words = words(right)
    match = SequenceMatcher(None, left_words, right_words).find_longest_match()
    return {
        "word_count": match.size,
        "text": " ".join(left_words[match.a:match.a + match.size]),
    }


def main() -> None:
    decks = {
        "historical_automated": load(AUTOMATED),
        "manual_reference": load(MANUAL),
        "phase1_candidate": load(CANDIDATE),
    }
    field_maps = {name: dict(summary_fields(deck)) for name, deck in decks.items()}
    body_maps = {name: dict(summary_bodies(deck)) for name, deck in decks.items()}

    word_counts = {}
    for name, fields in body_maps.items():
        counts = {path: len(words(text)) for path, text in fields.items()}
        word_counts[name] = {
            "total": sum(counts.values()),
            "mean": round(sum(counts.values()) / len(counts), 2),
            "minimum": min(counts.values()),
            "maximum": max(counts.values()),
            "by_field": counts,
        }

    similarities = {}
    candidate_fields = field_maps["phase1_candidate"]
    for reference_name in ("historical_automated", "manual_reference"):
        reference = field_maps[reference_name]
        ratios = {
            path: round(SequenceMatcher(None, text, reference[path]).ratio(), 4)
            for path, text in candidate_fields.items()
        }
        similarities[reference_name] = {
            "mean": round(sum(ratios.values()) / len(ratios), 4),
            "maximum": max(ratios.values()),
            "maximum_path": max(ratios, key=ratios.get),
            "by_field": ratios,
        }

    manual_body_matches = {
        path: longest_word_match(text, body_maps["manual_reference"][path])
        for path, text in body_maps["phase1_candidate"].items()
    }
    manual_body_matches = dict(sorted(
        manual_body_matches.items(),
        key=lambda item: item[1]["word_count"],
        reverse=True,
    ))

    candidate_text = "\n".join(candidate_fields.values())
    manual_text = "\n".join(field_maps["manual_reference"].values())
    overlap = {}
    for size in (6, 8, 10, 12):
        shared = sorted(ngrams(candidate_text, size) & ngrams(manual_text, size))
        overlap[str(size)] = {
            "shared_distinct_ngram_count": len(shared),
            "examples": [" ".join(item) for item in shared[:20]],
        }

    headline_sets = {
        name: [
            text for path, text in fields.items() if ".headline." in path
        ]
        for name, fields in field_maps.items()
    }
    candidate_headlines = set(headline_sets["phase1_candidate"])
    headline_reuse = {
        name: sorted(candidate_headlines & set(headlines))
        for name, headlines in headline_sets.items()
        if name != "phase1_candidate"
    }

    lens_vocabulary = {}
    for name, deck in decks.items():
        lens_tokens = {
            card_id: Counter(
                token
                for density in DENSITIES
                for audience in AUDIENCES
                for token in words(card[density]["body"][audience])
                if len(token) > 4
            )
            for card_id, card in deck["summary"].items()
        }
        overlaps = {}
        ids = list(lens_tokens)
        for index, left in enumerate(ids):
            for right in ids[index + 1:]:
                left_set = set(lens_tokens[left])
                right_set = set(lens_tokens[right])
                union = left_set | right_set
                overlaps[f"{left}__{right}"] = round(
                    len(left_set & right_set) / len(union), 4
                ) if union else 0.0
        lens_vocabulary[name] = overlaps

    output = {
        "word_counts": word_counts,
        "candidate_similarity": similarities,
        "candidate_manual_ngram_overlap": overlap,
        "candidate_manual_longest_body_matches": manual_body_matches,
        "candidate_exact_headline_reuse": headline_reuse,
        "cross_lens_vocabulary_jaccard": lens_vocabulary,
        "candidate_headlines": {
            card_id: {
                density: card[density]["headline"]
                for density in DENSITIES
            }
            for card_id, card in decks["phase1_candidate"]["summary"].items()
        },
    }
    (HERE / "summary-quality-metrics.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "word_counts": word_counts,
        "candidate_similarity": {
            key: {k: v for k, v in value.items() if k != "by_field"}
            for key, value in similarities.items()
        },
        "candidate_manual_ngram_overlap": overlap,
        "candidate_manual_longest_body_matches_top_12": dict(
            list(manual_body_matches.items())[:12]
        ),
        "candidate_exact_headline_reuse": headline_reuse,
        "cross_lens_vocabulary_jaccard": lens_vocabulary,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
