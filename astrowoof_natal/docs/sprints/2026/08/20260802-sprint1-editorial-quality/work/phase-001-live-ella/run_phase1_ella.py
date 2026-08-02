#!/usr/bin/env python3
"""Run the cross-subject Phase-1 Ella summary-authoring experiment."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
SRC = REPO / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC))

from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider, author_pending_passes, create_run,
    finalize_subjects, load_json, save_state, write_json_atomic,
)

EXPERIMENT = Path(__file__).resolve().parent
RUN_DIR = EXPERIMENT / "run"
INPUT_PACKAGE = Path(r"C:\tmp\ella-semantic-closure-input")
BASELINE_RUN = Path(r"C:\tmp\ella-semantic-closure-batch-recovery-live-20260801")
BASELINE_DECK = REPO / "astrowoof_natal/qa/reference_decks/ella/20260801-batch-optimized-final/natal.ella.cards.json"
KEVIN_GOLD_DECK = REPO / "astrowoof_natal/qa/reference_decks/kevin/20260730-six-pass-final/natal.kevin.cards.json"
PYTHON = Path(sys.executable)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_diff_paths(left: object, right: object, prefix: str = "") -> list[str]:
    if type(left) is not type(right):
        return [prefix or "$"]
    if isinstance(left, dict):
        paths: list[str] = []
        for key in sorted(set(left) | set(right)):
            child = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                paths.append(child)
            else:
                paths.extend(json_diff_paths(left[key], right[key], child))
        return paths
    if isinstance(left, list):
        if len(left) != len(right):
            return [prefix]
        paths = []
        for index, (a, b) in enumerate(zip(left, right, strict=True)):
            paths.extend(json_diff_paths(a, b, f"{prefix}.{index}"))
        return paths
    return [] if left == right else [prefix]


def main() -> None:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is empty")
    provider = OpenAIResponsesProvider(
        api_key=key, model="gpt-5.6-terra", reasoning_effort="medium",
        background=True, prompt_cache_mode="explicit", prompt_cache_ttl="30m",
    )
    if (RUN_DIR / "run.json").is_file():
        raise FileExistsError(f"Experiment already initialized: {RUN_DIR / 'run.json'}")
    state, run_json = create_run(
        input_package=INPUT_PACKAGE, run_dir=RUN_DIR, subject="ella",
        provider=provider, max_attempts=3,
        sbe_script=SRC / "build_projected_semantic_basis.py",
        python_executable=PYTHON,
    )
    reuse_manifest = {
        "source_run": str(BASELINE_RUN), "reused_passes": {},
        "experimental_pass": "ella_6", "gold_subject": "kevin",
        "target_subject": "ella",
        "assembly_control": "The new summaries are retained, but the accepted Ella baseline theme assignment is restored before assembly.",
    }
    for number in range(1, 6):
        pass_id = f"ella_{number}"
        source = BASELINE_RUN / "passes" / pass_id / "accepted"
        target = RUN_DIR / "passes" / pass_id / "accepted"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
        record = state["passes"][pass_id]
        record.update({
            "state": "PASS_QA_ACCEPTED",
            "accepted_workspace": str(target.resolve()),
            "accepted_attempt": "reused-20260801",
        })
        reuse_manifest["reused_passes"][pass_id] = {"source": str(source), "destination": str(target)}
    save_state(run_json, state)
    write_json_atomic(EXPERIMENT / "reuse-and-isolation-manifest.json", reuse_manifest)

    author_pending_passes(
        state=state, provider=provider, run_dir=RUN_DIR, max_attempts=3,
        python_executable=PYTHON, run_json=run_json, max_workers=1,
    )
    pass6 = state["passes"]["ella_6"]
    if pass6["state"] != "PASS_QA_ACCEPTED":
        raise RuntimeError(f"Ella pass 6 was not accepted: {pass6['state']}")
    accepted6 = Path(pass6["accepted_workspace"])
    new_theme = accepted6 / "ASSIGN THEME GROUPS.md"
    shutil.copy2(new_theme, EXPERIMENT / "phase1-authored-theme-groups.md")
    baseline_theme = BASELINE_RUN / "passes/ella_6/accepted/ASSIGN THEME GROUPS.md"
    shutil.copy2(baseline_theme, new_theme)
    write_json_atomic(EXPERIMENT / "assembly-isolation.json", {
        "new_theme_group_sha256": digest(EXPERIMENT / "phase1-authored-theme-groups.md"),
        "baseline_theme_group_sha256": digest(baseline_theme),
        "assembled_theme_group_sha256": digest(new_theme),
        "baseline_theme_restored": digest(new_theme) == digest(baseline_theme),
    })
    save_state(run_json, state)
    finalize_subjects(
        state=state, run_dir=RUN_DIR, python_executable=PYTHON,
        allow_lint_warnings=True, polish=False,
    )
    save_state(run_json, state)
    final_record = state["subjects"]["ella"]
    candidate_path = Path(final_record["deck"])
    candidate = load_json(candidate_path)
    baseline = load_json(BASELINE_DECK)
    changed = json_diff_paths(baseline, candidate)
    non_summary = [path for path in changed if not path.startswith("summary.")]
    comparison = {
        "candidate": str(candidate_path), "automated_baseline": str(BASELINE_DECK),
        "kevin_gold_reference": str(KEVIN_GOLD_DECK),
        "candidate_sha256": digest(candidate_path),
        "automated_baseline_sha256": digest(BASELINE_DECK),
        "changed_value_path_count": len(changed),
        "non_summary_changed_paths": non_summary,
        "reader_facing_card_payloads_identical": all(
            left["card"] == right["card"]
            for left, right in zip(baseline["cards"], candidate["cards"], strict=True)
        ),
        "summary_sets": {"automated_baseline": baseline["summary"], "phase1_candidate": candidate["summary"]},
        "final_state": final_record["state"],
        "validation_report": final_record.get("validation_report"),
        "lint_report": final_record.get("lint_report"),
    }
    write_json_atomic(EXPERIMENT / "cross-subject-summary-comparison.json", comparison)
    write_json_atomic(EXPERIMENT / "live-result.json", {
        "status": "complete", "run_state": state["status"],
        "pass6_attempts": pass6["attempts"], "final_record": final_record,
        "comparison": {key: value for key, value in comparison.items() if key != "summary_sets"},
    })
    print(json.dumps(load_json(EXPERIMENT / "live-result.json"), indent=2))


if __name__ == "__main__":
    main()
