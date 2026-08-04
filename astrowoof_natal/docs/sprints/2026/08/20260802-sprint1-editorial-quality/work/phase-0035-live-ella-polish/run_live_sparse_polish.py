"""Run one isolated live sparse-polish attempt against the preserved Ella deck."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
SOURCE_RUN = (
    REPO
    / "astrowoof_natal/docs/sprints/2026/08/"
    / "20260802-sprint1-editorial-quality/work/phase-003-live-ella-planning/run"
)
RUN_DIR = HERE / "run"
SOURCE_FINAL = SOURCE_RUN / "final/ella"
FINAL_ROOT = RUN_DIR / "final/ella"

sys.path.insert(0, str(REPO / "astrowoof_natal/src"))

from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider,
    lint_finding_count,
    load_json,
    polish_subject,
    polish_target_paths,
    sha256_file,
    write_json_atomic,
)


def main() -> int:
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    shutil.copytree(SOURCE_FINAL, FINAL_ROOT)

    deck_path = FINAL_ROOT / "natal.ella.cards.json"
    assembly_path = FINAL_ROOT / "natal.ella.assembly-report.json"
    validation_path = FINAL_ROOT / "natal.ella.validation-report.json"
    lint_path = FINAL_ROOT / "natal.ella.lint-report.json"
    before_copy = HERE / "natal.ella.cards.before.json"
    shutil.copy2(deck_path, before_copy)

    baseline_deck = load_json(deck_path)
    baseline_lint = load_json(lint_path)
    baseline_validation = load_json(validation_path)
    targets = polish_target_paths(
        baseline_deck,
        lint_report=baseline_lint,
        validation_report=baseline_validation,
        include_theme_groups=False,
        expand_related=False,
    )
    control = {
        "source_run": str(SOURCE_RUN),
        "source_deck_sha256": sha256_file(deck_path),
        "baseline_lint_warning_count": baseline_lint.get("warning_count"),
        "baseline_composite_finding_count": lint_finding_count(baseline_lint),
        "baseline_authoring_rejections": (
            baseline_lint.get("checks", {})
            .get("authoring_pass_acceptance", {})
            .get("rejection_reasons", [])
        ),
        "editable_target_count": len(targets),
        "editable_targets": targets,
        "maximum_polish_attempts": 1,
        "model": "gpt-5.6-luna",
        "reasoning_effort": "low",
    }
    write_json_atomic(HERE / "input-control.json", control)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is empty or unavailable")
    provider = OpenAIResponsesProvider(
        api_key=api_key,
        model="gpt-5.6-luna",
        reasoning_effort="low",
        background=True,
        poll_interval_seconds=2.0,
        response_timeout_seconds=1800.0,
        prompt_cache_mode="explicit",
        prompt_cache_ttl="30m",
        max_output_tokens=20_000,
    )
    record = {
        "subject": "ella",
        "state": "FINAL_QA_WARN",
        "deck": str(deck_path),
        "assembly_report": str(assembly_path),
        "validation_report": str(validation_path),
        "lint_report": str(lint_path),
        "baseline_warning_count": lint_finding_count(baseline_lint),
        "baseline_warning_components": {
            "validation": len(baseline_validation.get("warnings") or []),
            "lint": int(baseline_lint.get("warning_count") or 0),
            "authoring_rejections": (
                lint_finding_count(baseline_lint)
                - int(baseline_lint.get("warning_count") or 0)
            ),
        },
        "polish_attempts": [],
        "delivery": None,
    }
    polish_subject(
        record=record,
        provider=provider,
        run_dir=RUN_DIR,
        python_executable=Path(sys.executable),
        max_attempts=1,
    )

    after_deck = load_json(deck_path)
    after_lint = load_json(lint_path)
    after_validation = load_json(validation_path)
    result = {
        "record": record,
        "before": {
            "deck": str(before_copy),
            "sha256": control["source_deck_sha256"],
            "validation_status": baseline_validation.get("status"),
            "lint_warning_count": baseline_lint.get("warning_count"),
            "composite_finding_count": lint_finding_count(baseline_lint),
        },
        "after": {
            "deck": str(deck_path),
            "sha256": sha256_file(deck_path),
            "changed": baseline_deck != after_deck,
            "validation_status": after_validation.get("status"),
            "validation_errors": after_validation.get("errors", []),
            "lint_warning_count": after_lint.get("warning_count"),
            "composite_finding_count": lint_finding_count(after_lint),
            "authoring_pass_acceptance": (
                after_lint.get("checks", {}).get("authoring_pass_acceptance")
            ),
        },
    }
    write_json_atomic(HERE / "result.json", result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
