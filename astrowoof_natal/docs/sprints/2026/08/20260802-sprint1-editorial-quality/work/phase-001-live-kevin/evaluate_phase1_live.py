#!/usr/bin/env python3
"""Evaluate the completed Phase-1 call with historical and same-code controls."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[8]
SRC = REPO / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC))

from assemble_authoring_workspace import assemble  # noqa: E402
from author_semantic_closure import (  # noqa: E402
    finalize_subjects,
    load_json,
    save_state,
    write_json_atomic,
)
from run_phase1_live import (  # noqa: E402
    BASELINE_DECK,
    BASELINE_RUN,
    MANUAL_DECK,
    RUN_DIR,
    json_diff_paths,
)


def copy_workspace(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def main() -> None:
    run_json = RUN_DIR / "run.json"
    state = load_json(run_json)
    packet_path = (
        RUN_DIR / "sbe" / "semantic-basis-output" / "kevin"
        / "kevin.selected-authoring-packet.json"
    )
    packet = load_json(packet_path)
    historical = load_json(BASELINE_DECK)
    manual = load_json(MANUAL_DECK)

    isolation_deck_path = HERE / "natal.kevin.phase1-isolation.cards.json"
    if not isolation_deck_path.exists():
        shutil.copy2(Path(state["subjects"]["kevin"]["deck"]), isolation_deck_path)
    isolation = load_json(isolation_deck_path)

    control_root = HERE / "same-code-control-workspaces"
    control_root.mkdir(parents=True, exist_ok=True)
    for number in range(1, 7):
        copy_workspace(
            BASELINE_RUN / "passes" / f"kevin_{number}" / "accepted",
            control_root / f"kevin_{number}",
        )
    control, control_report = assemble(packet, control_root, allow_partial=False)
    control_path = HERE / "natal.kevin.same-code-control.cards.json"
    write_json_atomic(control_path, control)
    write_json_atomic(HERE / "same-code-control-assembly-report.json", control_report)

    same_code_changes = json_diff_paths(control, isolation)
    same_code_non_summary = [
        path for path in same_code_changes if not path.startswith("summary.")
    ]
    expected_sanitizer_changes = {
        "cards.5.context_filter_groups.high_level",
        "cards.14.context_filter_groups.high_level",
    }
    unexpected_same_code_changes = [
        path for path in same_code_non_summary
        if path not in expected_sanitizer_changes
    ]
    historical_control_changes = json_diff_paths(historical, control)

    accepted6 = Path(state["passes"]["kevin_6"]["accepted_workspace"])
    shutil.copy2(
        HERE / "phase1-authored-theme-groups.md",
        accepted6 / "ASSIGN THEME GROUPS.md",
    )
    state["subjects"].pop("kevin", None)
    save_state(run_json, state)
    finalize_subjects(
        state=state,
        run_dir=RUN_DIR,
        python_executable=Path(sys.executable),
        allow_lint_warnings=True,
        polish=False,
    )
    save_state(run_json, state)
    production_record = state["subjects"]["kevin"]
    production_path = Path(production_record["deck"])
    production = load_json(production_path)
    production_copy = HERE / "natal.kevin.phase1-production.cards.json"
    shutil.copy2(production_path, production_copy)

    production_vs_isolation = json_diff_paths(isolation, production)
    expected_theme_changes = [
        path for path in production_vs_isolation if path.endswith(".theme_group")
    ]
    unexpected_production_changes = [
        path for path in production_vs_isolation
        if not path.endswith(".theme_group")
    ]
    validation_errors = production_record["validation"]["report"].get("errors", [])
    theme_balance_only = bool(validation_errors) and all(
        error.startswith(
            "Selected aspects and syntheses theme groups are not approximately balanced:"
        )
        for error in validation_errors
    )
    isolation_passed = not unexpected_same_code_changes and not unexpected_production_changes
    status = (
        "summary_isolation_pass_full_qa_blocked_by_theme_balance"
        if isolation_passed and theme_balance_only
        else "pass" if isolation_passed and not validation_errors
        else "fail"
    )
    comparison = {
        "status": status,
        "controls": {
            "historical_automated_baseline": str(BASELINE_DECK),
            "manual_reference": str(MANUAL_DECK),
            "same_code_control": str(control_path),
            "phase1_isolation_candidate": str(isolation_deck_path),
            "phase1_production_candidate": str(production_copy),
        },
        "same_code_isolation": {
            "changed_value_path_count": len(same_code_changes),
            "non_summary_changed_paths": same_code_non_summary,
            "expected_post_assembly_sanitizer_changes": sorted(expected_sanitizer_changes),
            "unexpected_changed_paths": unexpected_same_code_changes,
            "reader_facing_card_payloads_identical": all(
                control_card["card"] == isolation_card["card"]
                for control_card, isolation_card in zip(
                    control["cards"], isolation["cards"], strict=True
                )
            ),
        },
        "historical_assembler_drift": {
            "changed_value_path_count": len(historical_control_changes),
            "changed_value_paths": historical_control_changes,
        },
        "production_theme_group_update": {
            "theme_group_changed_paths": expected_theme_changes,
            "unexpected_changed_paths": unexpected_production_changes,
        },
        "qa": {
            "state": production_record["state"],
            "theme_group_balance_is_only_validation_error": theme_balance_only,
            "validation": production_record["validation"],
            "lint": production_record["lint"],
        },
        "summary_sets": {
            "historical_automated_baseline": historical["summary"],
            "manual_reference": manual["summary"],
            "same_code_control": control["summary"],
            "phase1_candidate": production["summary"],
        },
    }
    write_json_atomic(HERE / "three-way-summary-comparison.json", comparison)
    write_json_atomic(
        HERE / "live-result.json",
        {
            "status": comparison["status"],
            "run_state": state["status"],
            "pass6_attempts": state["passes"]["kevin_6"]["attempts"],
            "final_record": production_record,
            "comparison_summary": {
                key: value for key, value in comparison.items()
                if key != "summary_sets"
            },
        },
    )
    print(json.dumps(load_json(HERE / "live-result.json"), indent=2))


if __name__ == "__main__":
    main()
