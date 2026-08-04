"""Run the isolated Phase-4 read-only critic against polished Ella."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
SOURCE_FINAL = (
    REPO
    / "astrowoof_natal/docs/sprints/2026/08/"
    / "20260802-sprint1-editorial-quality/work/"
    / "phase-0035-live-ella-polish/run/final/ella"
)
RUN_DIR = HERE / "run"
FINAL_ROOT = RUN_DIR / "final/ella"

sys.path.insert(0, str(REPO / "astrowoof_natal/src"))

from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider,
    load_json,
    run_qualitative_review,
    sha256_file,
    write_json_atomic,
)


def main() -> int:
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    FINAL_ROOT.mkdir(parents=True)
    names = (
        "natal.ella.cards.json",
        "natal.ella.assembly-report.json",
        "natal.ella.validation-report.json",
        "natal.ella.lint-report.json",
    )
    for name in names:
        shutil.copy2(SOURCE_FINAL / name, FINAL_ROOT / name)

    deck_path = FINAL_ROOT / "natal.ella.cards.json"
    record = {
        "subject": "ella",
        "state": "DELIVERY_COMPLETE",
        "deck": str(deck_path),
        "assembly_report": str(
            FINAL_ROOT / "natal.ella.assembly-report.json"
        ),
        "validation_report": str(
            FINAL_ROOT / "natal.ella.validation-report.json"
        ),
        "lint_report": str(FINAL_ROOT / "natal.ella.lint-report.json"),
        "polish_attempts": [],
        "delivery": None,
    }
    before_sha = sha256_file(deck_path)
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is empty or unavailable")
    critic = OpenAIResponsesProvider(
        api_key=api_key,
        model="gpt-5.6-luna",
        reasoning_effort="medium",
        background=True,
        poll_interval_seconds=2.0,
        response_timeout_seconds=1800.0,
        prompt_cache_mode="explicit",
        prompt_cache_ttl="30m",
        max_output_tokens=20_000,
    )
    run_qualitative_review(
        record=record,
        critic_provider=critic,
        editor_provider=None,
        run_dir=RUN_DIR,
        python_executable=Path(sys.executable),
        max_findings=8,
        max_target_fields=12,
        max_target_cards=6,
    )
    result = {
        "record": record,
        "production_deck": {
            "before_sha256": before_sha,
            "after_sha256": sha256_file(deck_path),
            "unchanged": before_sha == sha256_file(deck_path),
        },
        "critic_findings": load_json(
            Path(record["qualitative_review"]["critic"]["artifact"])
        ),
    }
    write_json_atomic(HERE / "result.json", result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
