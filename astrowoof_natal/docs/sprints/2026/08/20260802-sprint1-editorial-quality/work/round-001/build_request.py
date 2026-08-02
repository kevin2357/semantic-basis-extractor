"""Build the reproducible, pre-submission request for Phase 0 round 001.

This script performs no network activity. It derives an explicit sparse edit
allowlist, diagnoses, source basis, context, and strict response schema from
the normalized automated Kevin deck.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROUND_ROOT = Path(__file__).resolve().parent
REQUEST_ROOT = ROUND_ROOT / "request"
REPO_ROOT = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "astrowoof_natal" / "src").is_dir()
)
SRC_ROOT = REPO_ROOT / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC_ROOT))

from author_semantic_closure import (  # noqa: E402
    editable_deck_fields,
    sparse_polish_basis,
    sparse_polish_context,
    sparse_polish_output_schema,
)
from build_projected_semantic_basis import (  # noqa: E402
    render_dog_details,
    render_full_chart_basis,
)


BASELINE = REQUEST_ROOT / "natal.kevin.cards.normalized-baseline.json"
PACKET = (
    REPO_ROOT
    / "astrowoof_natal"
    / "qa"
    / "reference_decks"
    / "kevin"
    / "selected-authoring-packet.json"
)
REPEATED_OPENING = [1, 4, 8, 12, 34, 39]
WEAK_HEADLINES = [5, 20, 25, 30, 37, 41, 43, 45, 47, 49]
LONG_HANDLER_BODIES = [1, 6, 10, 21, 41]
ADVISORY_FIELDS = {
    12: ("no_astro", "body", "hybrid"),
    13: ("no_astro", "body", "handler"),
    35: ("no_astro", "body", "hybrid"),
}
COMPOUND_CARDS = [40, 50]
HUMOR_FIELDS = {
    1: ["funny_quote", "joke"],
    3: ["joke"],
    5: ["funny_quote", "joke"],
    7: ["joke"],
    10: ["joke"],
    12: ["imperative", "joke"],
    15: ["funny_quote", "joke"],
    20: ["funny_quote", "joke"],
    21: ["joke"],
    22: ["funny_quote"],
    30: ["joke"],
    33: ["funny_quote"],
    37: ["imperative"],
    38: ["joke"],
    41: ["joke"],
    45: ["funny_quote"],
    47: ["joke"],
    49: ["joke"],
    50: ["joke"],
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, value: object) -> None:
    (REQUEST_ROOT / name).write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def card_path(card_number: int, suffix: str) -> str:
    return f"cards.{card_number - 1}.{suffix}"


def add(
    diagnoses: dict[str, dict[str, str]],
    path: str,
    code: str,
    observation: str,
    objective: str,
) -> None:
    entry = diagnoses.setdefault(
        path,
        {"field_path": path, "observation": "", "objective": "", "reason_codes": []},
    )
    entry["reason_codes"].append(code)
    if observation not in entry["observation"]:
        entry["observation"] = " ".join(filter(None, [entry["observation"], observation]))
    if objective not in entry["objective"]:
        entry["objective"] = " ".join(filter(None, [entry["objective"], objective]))


def main() -> None:
    deck = load(BASELINE)
    packet = load(PACKET)
    all_fields = editable_deck_fields(deck, include_theme_groups=False)
    diagnoses: dict[str, dict[str, str]] = {}

    for path in sorted(p for p in all_fields if p.startswith("summary.")):
        add(
            diagnoses,
            path,
            "summary_coherence",
            "The four summaries are the deck's front door and should work as a coordinated whole-chart portrait, not as generic recaps or lists of traits.",
            "Make this field specific, memorable, warm, non-astrology-centric, faithful to its lens, and complementary rather than redundant with the other three summaries.",
        )

    for number in REPEATED_OPENING:
        add(
            diagnoses,
            card_path(number, "card.no_astro.body.direct_to_dog"),
            "repeated_opening",
            "This field belongs to a six-card cluster whose bodies begin with the same 'Kevin, you do...' architecture.",
            "Give this claim its own natural direct-to-dog doorway and sentence movement while preserving meaning and affection.",
        )

    for number in WEAK_HEADLINES:
        add(
            diagnoses,
            card_path(number, "card.no_astro.headline.handler"),
            "generic_or_administrative_headline",
            "The headline reads more like a label, instruction, or administrative summary than a memorable insight about this dog.",
            "Write a concise, claim-specific headline with human editorial character; avoid merely renaming the claim.",
        )

    for number in LONG_HANDLER_BODIES:
        add(
            diagnoses,
            card_path(number, "card.no_astro.body.handler"),
            "overexplained_body",
            "The body is unusually long for this deck and risks explaining the mechanism after the reader already understands it.",
            "Preserve the piercing behavioral insight and useful guidance while improving pace, selectivity, and natural prose.",
        )

    for number, (density, field, audience) in ADVISORY_FIELDS.items():
        add(
            diagnoses,
            card_path(number, f"card.{density}.{field}.{audience}"),
            "validator_prose_advisory",
            "The deterministic validator flagged this field as stylistically suspect despite the deck passing structural validation.",
            "Rewrite it as fluent, complete, natural human prose appropriate to the audience and claim.",
        )

    for number, fields in HUMOR_FIELDS.items():
        for field in fields:
            collection = {
                "funny_quote": "funny_dog_quotes",
                "imperative": "imperative_dog_quotes",
                "joke": "applicable_canine_jokes",
            }[field]
            add(
                diagnoses,
                card_path(number, f"card.{collection}.0"),
                "administrative_humor_cluster",
                "Across the deck, comic material overuses office, policy, procedural, inspection, management, and contractual metaphors.",
                "Find humor in this particular trait and lived dog behavior. Preserve an administrative joke only if it is genuinely the sharpest premise here; diversify the deck rather than performing word substitution.",
            )

    for number in COMPOUND_CARDS:
        for density in ("no_astro", "full_astro"):
            for audience in ("handler", "hybrid"):
                add(
                    diagnoses,
                    card_path(number, f"card.{density}.body.{audience}"),
                    "compound_semantic_flattening",
                    "This card's compound claim contains a meaningful interaction among multiple behavioral forces, but the prose risks collapsing it into one broad trait.",
                    "Preserve the relationship among the forces and show how the combination behaves in life; do not add astrology absent from the supplied evidence.",
                )

    target_paths = sorted(diagnoses)
    unknown = sorted(set(target_paths) - set(all_fields))
    if unknown:
        raise ValueError(f"Unknown target paths: {unknown}")

    targets = {path: all_fields[path] for path in target_paths}
    context = sparse_polish_context(deck, target_paths)
    read_only_context = {path: value for path, value in context.items() if path not in targets}
    basis = sparse_polish_basis(deck, target_paths)
    schema = sparse_polish_output_schema(target_paths)
    schema["properties"]["edits"]["minItems"] = len(target_paths)

    write_json("editable-targets.json", targets)
    write_json("diagnosis-ledger.json", [diagnoses[path] for path in target_paths])
    write_json("read-only-context.json", read_only_context)
    write_json("repair-basis.json", basis)
    write_json("response-schema.json", schema)
    (REQUEST_ROOT / "DOG DETAILS.md").write_text(render_dog_details(packet), encoding="utf-8")
    (REQUEST_ROOT / "FULL CHART BASIS.md").write_text(render_full_chart_basis(packet), encoding="utf-8")
    polish_guide = """# AstroWoof Claim-Deck Polish Guide

## What the deck is

An AstroWoof natal claim deck turns a dog's selected astrological and projected-semantic claims into approachable reader-facing cards. Each claim card is a bounded interpretation supported by its own claim and evidence. The complete deck should describe one recognizable dog while allowing each card to make a distinct, memorable point.

The source claim and evidence determine what a claim card may say. Read-only neighboring prose helps you understand continuity and detect repetition, but it is not additional evidence for the target card. Do not import a neighboring card's facts into a target.

The four summary cards are different: they synthesize the whole chart and may use the complete full-chart basis. Together they form the reader's friendly, non-astrological introduction:

- **Who He Is:** temperament, identity, and core personality at a glance.
- **How He Lives:** routines, lifestyle, comfort, environment, and his natural way of moving through daily life.
- **What He Needs:** emotional support, enrichment, handling, security, and practical help for thriving.
- **How He Grows:** learning, development, challenges, and how potential unfolds over time.

These are four lenses, not four paraphrases of one personality paragraph.

## What a sparse polish pass is

You receive an explicit map of editable field paths and their current values. Return one replacement for every path and no others. All unlisted prose and all structural, semantic, evidentiary, categorical, and identity data are locked.

The diagnosis ledger explains why each field was selected and what the revision should accomplish. It does not prescribe replacement language. Preserve strong material when it already serves the field; make a deeper change when the diagnosed problem cannot be repaired cosmetically.

Read-only context may include other fields from the same card, neighboring cards, or the other summaries. Use it to maintain characterization, avoid duplication, and understand the local role of the target. Do not rewrite it or treat it as permission to broaden a claim.

## The three audiences

- **Handler:** helps a person recognize, understand, and respond to the dog. It may teach, clarify a misconception, or give practical guidance.
- **Direct to dog:** addresses the dog with dignity, affection, reassurance, encouragement, or an honest challenge. It should not merely convert handler prose into second person.
- **Hybrid:** depicts dog and human making meaning together. Its center is the interaction, shared moment, negotiation, or mutual adjustment—not a handler paragraph with both parties named.

Audience changes purpose, not mandatory grammar. Handler need not always be observation/explanation/advice. Direct-to-dog should not become repeated sentences beginning with “you.” Hybrid should not become “dog does X; human does Y; together they do Z.”

## The three astrology-density levels

- **No astrology:** describes recognizable behavior and useful meaning without signs, planets, houses, aspects, angles, nodes, astrological jargon, or references to “the chart.”
- **Light astrology:** names the most useful astrological factor or two and translates them quickly into ordinary dog life. Astrology supports the insight rather than dominating it.
- **Full astrology:** may explain the relevant placement, aspect, house, angle, operator, or relationship in greater detail, but must remain readable, behaviorally grounded, and limited to supplied evidence.

The levels should not be identical prose with labels inserted or removed. They teach the same supported claim at genuinely different levels of astrological visibility.

## Card-level supporting fields

Funny dog quotes, imperative dog quotes, jokes, dos, and don'ts belong to the card as a whole. They should fit the claim across audiences and astrology levels. Quotes should sound speakable in the dog's imagined voice. Dos and don'ts should be concrete enough to guide a handler. Humor should arise from this trait and recognizable dog life rather than from a generic stock premise.

## Creative standard

Keep characterization consistent and expression diverse. The dog should remain recognizable; the prose architecture should not become uniform.

For each target, identify the one idea the reader should remember an hour later. Write toward that idea rather than translating a source label or inventorying evidence. Prefer lived behavior, a precise contrast, a generous reinterpretation, a useful handling insight, or a memorable image over abstract explanation.

Headlines should be inseparable from their fields: if a headline could move to another claim without obviously becoming wrong, sharpen it.

When humor is targeted, ask what is funny about this particular behavioral mechanism. Do not repair a repeated comic mechanism by changing only its vocabulary.

When prose is overexplained, preserve the piercing insight and useful guidance, then remove the conceptual lap taken after the reader already understands it.

When a compound claim is targeted, preserve the interaction among its forces. Do not flatten a tension, reinforcement, sequence, or behavioral tradeoff into one broad personality adjective.

Natural writing outranks visible effort. Revise for specificity, rhythm, warmth, clarity, and semantic faithfulness—not for uniform polish or conspicuous cleverness.
"""
    (REQUEST_ROOT / "ASTROWOOF POLISH GUIDE.md").write_text(
        polish_guide, encoding="utf-8"
    )
    obsolete_guide = REQUEST_ROOT / "AUTHORING GUIDING LIGHTS.md"
    if obsolete_guide.exists():
        obsolete_guide.unlink()

    system = (
        "You are an editorial revision agent for AstroWoof. "
        "Revise only the explicitly allowlisted prose fields, using the supplied current deck, diagnoses, evidence, full-chart basis, and guiding principles. "
        "Preserve factual meaning, dog identity, audience, astrology density, and all locked data. "
        "Return only strict JSON matching the response schema."
    )
    (REQUEST_ROOT / "SYSTEM_PROMPT.txt").write_text(system + "\n", encoding="utf-8")

    instructions = """Perform one targeted editorial polish pass on the supplied Kevin AstroWoof claim deck. Improve only the allowlisted fields for their diagnosed reasons; do not perform a wholesale rewrite or make every field sound uniform.

Required method
1. Read DOG DETAILS, FULL CHART BASIS, and ASTROWOOF POLISH GUIDE to understand Kevin, the deck, and the editorial standard.
2. Read the current editable values, diagnosis ledger, relevant claim/evidence basis, and read-only neighboring context.
3. Treat each target as a real editorial decision. Preserve good material when possible; rewrite deeply when the diagnosed weakness requires it.
4. Keep summaries coordinated across four distinct lenses: Who He Is, How He Lives, What He Needs, and How He Grows. Summaries alone may use the full chart. Claim-card edits must remain grounded in that card's supplied claim/evidence.
5. For humor, solve the repeated comic mechanism rather than swapping office vocabulary for synonyms. Humor should arise from the individual trait and recognizable dog life.
6. Preserve audience distinctions: handler teaches the person; direct-to-dog addresses Kevin; hybrid depicts the relationship or shared moment. Audience changes purpose, not a mandatory sentence template.
7. Preserve astrology-density distinctions. No-astro fields must not introduce astrology. Full-astro fields may use only supported astrology.
8. Return exactly one nonempty replacement for every allowlisted field_path, no duplicates and no extra paths. reason_codes must copy the applicable codes from the diagnosis ledger.

Do not alter facts, claim identity, evidence, categories, tags, filters, structure, or any read-only prose. Passing a mechanical checker is not the objective; the objective is natural, specific, varied writing that repairs the stated weakness without semantic drift.
"""
    (REQUEST_ROOT / "USER_PROMPT.txt").write_text(instructions, encoding="utf-8")

    sections = [
        instructions,
        "\n\n===== DOG DETAILS =====\n" + (REQUEST_ROOT / "DOG DETAILS.md").read_text(encoding="utf-8"),
        "\n\n===== FULL CHART BASIS =====\n" + (REQUEST_ROOT / "FULL CHART BASIS.md").read_text(encoding="utf-8"),
        "\n\n===== ASTROWOOF POLISH GUIDE =====\n" + (REQUEST_ROOT / "ASTROWOOF POLISH GUIDE.md").read_text(encoding="utf-8"),
        "\n\n===== EDITABLE TARGETS (current values) =====\n" + json.dumps(targets, ensure_ascii=False, indent=2),
        "\n\n===== DIAGNOSIS LEDGER =====\n" + json.dumps([diagnoses[p] for p in target_paths], ensure_ascii=False, indent=2),
        "\n\n===== RELEVANT CLAIM AND EVIDENCE BASIS =====\n" + json.dumps(basis, ensure_ascii=False, indent=2),
        "\n\n===== READ-ONLY NEIGHBORING PROSE =====\n" + json.dumps(read_only_context, ensure_ascii=False, indent=2),
    ]
    rendered_user = "".join(sections)
    (REQUEST_ROOT / "OPENAI_USER_MESSAGE.txt").write_text(rendered_user, encoding="utf-8")

    manifest = {
        "experiment": "20260802-sprint1 phase-0 round-001",
        "baseline": str(BASELINE.relative_to(REPO_ROOT)).replace("\\", "/"),
        "target_count": len(target_paths),
        "summary_target_count": sum(path.startswith("summary.") for path in target_paths),
        "card_target_count": sum(path.startswith("cards.") for path in target_paths),
        "controls": {
            "fresh_stateless_response": True,
            "gold_examples_supplied": False,
            "prior_manual_kevin_prose_supplied": False,
            "sparse_allowlist": True,
            "all_non_allowlisted_fields_locked": True,
            "api_submission_performed": False,
        },
        "planned_api": {
            "model": "gpt-5.6-terra",
            "reasoning_effort": "medium",
            "background": True,
            "max_output_tokens": 100000,
            "structured_output": "response-schema.json",
        },
        "request_files": sorted(path.name for path in REQUEST_ROOT.iterdir() if path.is_file()),
    }
    write_json("request-manifest.json", manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
