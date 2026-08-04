"""Resume the saved Ella critic diagnosis into one sparse candidate call."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
RUN_DIR = HERE / "run"
sys.path.insert(0, str(REPO / "astrowoof_natal/src"))

from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider,
    load_json,
    run_qualitative_review,
    sha256_file,
    write_json_atomic,
)


def main() -> int:
    diagnosis = load_json(HERE / "result.json")
    record = diagnosis["record"]
    deck_path = Path(record["deck"])
    before_sha = sha256_file(deck_path)
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
    run_qualitative_review(
        record=record,
        critic_provider=provider,
        editor_provider=provider,
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
    }
    write_json_atomic(HERE / "candidate-result.json", result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
