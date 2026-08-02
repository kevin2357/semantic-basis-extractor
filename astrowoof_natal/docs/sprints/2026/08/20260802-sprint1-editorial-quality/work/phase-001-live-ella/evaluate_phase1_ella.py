#!/usr/bin/env python3
"""Restore Ella's baseline theme plan, assemble, and measure gold transfer."""

from __future__ import annotations

import json
import re
import shutil
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[8]
SRC = REPO / "astrowoof_natal/src"
sys.path.insert(0, str(SRC))

from assemble_authoring_workspace import assemble  # noqa: E402
from author_semantic_closure import finalize_subjects, load_json, save_state, write_json_atomic  # noqa: E402
from run_phase1_ella import BASELINE_DECK, BASELINE_RUN, KEVIN_GOLD_DECK, RUN_DIR, json_diff_paths  # noqa: E402

DENSITIES = ("no_astro", "light_astro", "full_astro")
AUDIENCES = ("handler", "direct_to_dog", "hybrid")


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?", text.lower())


def fields(deck: dict, bodies_only: bool = False) -> dict[str, str]:
    result = {}
    for card_id, card in deck["summary"].items():
        for density in DENSITIES:
            kinds = ("body",) if bodies_only else ("headline", "body")
            for kind in kinds:
                for audience in AUDIENCES:
                    result[f"{card_id}.{density}.{kind}.{audience}"] = card[density][kind][audience]
    return result


def ngrams(text: str, size: int) -> set[tuple[str, ...]]:
    tokens = words(text)
    return {tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1)}


def longest_match(left: str, right: str) -> dict:
    a, b = words(left), words(right)
    match = SequenceMatcher(None, a, b).find_longest_match()
    return {"word_count": match.size, "text": " ".join(a[match.a:match.a + match.size])}


def main() -> None:
    run_json = RUN_DIR / "run.json"
    state = load_json(run_json)
    accepted6 = Path(state["passes"]["ella_6"]["accepted_workspace"])
    authored_theme = HERE / "phase1-authored-theme-groups.md"
    if not authored_theme.exists():
        shutil.copy2(accepted6 / "ASSIGN THEME GROUPS.md", authored_theme)
    baseline_theme = BASELINE_RUN / "passes/ella_6/accepted/ASSIGN THEME GROUPS.md"
    shutil.copy2(baseline_theme, accepted6 / "ASSIGN THEME GROUPS.md")
    state["subjects"].pop("ella", None)
    save_state(run_json, state)
    finalize_subjects(
        state=state, run_dir=RUN_DIR, python_executable=Path(sys.executable),
        allow_lint_warnings=True, polish=False,
    )
    save_state(run_json, state)

    record = state["subjects"]["ella"]
    candidate = load_json(Path(record["deck"]))
    baseline = load_json(BASELINE_DECK)
    gold = load_json(KEVIN_GOLD_DECK)
    candidate_path = HERE / "natal.ella.phase1-cross-subject.cards.json"
    write_json_atomic(candidate_path, candidate)

    packet = load_json(RUN_DIR / "sbe/semantic-basis-output/ella/ella.selected-authoring-packet.json")
    control_root = HERE / "same-code-control-workspaces"
    if control_root.exists():
        shutil.rmtree(control_root)
    control_root.mkdir(parents=True)
    for number in range(1, 7):
        shutil.copytree(
            BASELINE_RUN / "passes" / f"ella_{number}" / "accepted",
            control_root / f"ella_{number}",
        )
    control, control_report = assemble(packet, control_root, allow_partial=False)
    write_json_atomic(HERE / "natal.ella.same-code-control.cards.json", control)
    write_json_atomic(HERE / "same-code-control-assembly-report.json", control_report)

    changed = json_diff_paths(control, candidate)
    non_summary = [path for path in changed if not path.startswith("summary.")]
    candidate_fields, baseline_fields, gold_fields = fields(candidate), fields(baseline), fields(gold)
    candidate_bodies, baseline_bodies, gold_bodies = fields(candidate, True), fields(baseline, True), fields(gold, True)

    longest = {
        candidate_path: max(
            (longest_match(candidate_text, gold_text) for gold_text in gold_bodies.values()),
            key=lambda item: item["word_count"],
        )
        for candidate_path, candidate_text in candidate_bodies.items()
    }
    longest = dict(sorted(longest.items(), key=lambda item: item[1]["word_count"], reverse=True))
    candidate_text = "\n".join(candidate_fields.values())
    gold_text = "\n".join(gold_fields.values())
    shared_ngrams = {
        str(size): sorted(" ".join(item) for item in ngrams(candidate_text, size) & ngrams(gold_text, size))
        for size in (6, 8, 10, 12)
    }
    word_counts = {
        "automated_baseline": sum(len(words(text)) for text in baseline_bodies.values()),
        "phase1_candidate": sum(len(words(text)) for text in candidate_bodies.values()),
        "kevin_gold": sum(len(words(text)) for text in gold_bodies.values()),
    }
    transferred_devices = {
        device: [path for path, text in candidate_fields.items() if re.search(pattern, text, re.I)]
        for device, pattern in {
            "chapter_or_act": r"\b(chapter|chapters|acts?)\b",
            "spark_and_return_or_landing": r"\bspark\b|\blanding\b|\btrain(?:ing)? the return\b",
            "anchor_gate_laboratory_stage": r"\b(anchor|gate|laboratory|stage)\b",
            "office_hours": r"office hours",
        }.items()
    }
    comparison = {
        "status": record["state"],
        "isolation": {
            "changed_value_path_count": len(changed),
            "non_summary_changed_paths": non_summary,
            "reader_facing_card_payloads_identical": all(
                a["card"] == b["card"] for a, b in zip(control["cards"], candidate["cards"], strict=True)
            ),
        },
        "historical_optimized_drift": {
            "changed_value_paths": json_diff_paths(control, baseline),
            "note": "Includes historical polish and postprocessing changes; not caused by Phase 1.",
        },
        "qa": {"validation": record["validation"], "lint": record["lint"]},
        "word_counts": word_counts,
        "exact_headline_reuse_from_kevin": sorted(
            {text for path, text in candidate_fields.items() if ".headline." in path}
            & {text for path, text in gold_fields.items() if ".headline." in path}
        ),
        "kevin_gold_ngram_overlap": {
            size: {"count": len(items), "examples": items[:20]}
            for size, items in shared_ngrams.items()
        },
        "longest_gold_body_matches": dict(list(longest.items())[:12]),
        "transferred_device_mentions": transferred_devices,
        "candidate_headlines": {
            card_id: {density: card[density]["headline"] for density in DENSITIES}
            for card_id, card in candidate["summary"].items()
        },
        "baseline_headlines": {
            card_id: {density: card[density]["headline"] for density in DENSITIES}
            for card_id, card in baseline["summary"].items()
        },
    }
    write_json_atomic(HERE / "cross-subject-quality-metrics.json", comparison)
    write_json_atomic(HERE / "live-result.json", {
        "status": record["state"],
        "pass6_attempts": state["passes"]["ella_6"]["attempts"],
        "final_record": record,
        "quality_summary": {
            "word_counts": word_counts,
            "gold_ngram_counts": {size: len(items) for size, items in shared_ngrams.items()},
            "maximum_gold_body_match_words": next(iter(longest.values()))["word_count"],
            "transferred_device_mentions": transferred_devices,
        },
    })
    print(json.dumps(load_json(HERE / "live-result.json"), indent=2))


if __name__ == "__main__":
    main()
