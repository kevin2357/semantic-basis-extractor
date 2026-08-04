#!/usr/bin/env python3
"""Run an isolated Ella pass-1 live checkpoint with compact-v2."""

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
    OpenAIResponsesProvider,
    author_pending_passes,
    create_run,
    finalize_subjects,
    save_state,
    write_json_atomic,
)

EXPERIMENT = Path(__file__).resolve().parent
RUN_DIR = EXPERIMENT / "run"
INPUT_PACKAGE = Path(r"C:\tmp\ella-semantic-closure-input")
BASELINE = (
    EXPERIMENT.parent
    / "phase-003-live-ella-compact-basis"
    / "run"
    / "final"
    / "ella"
    / "accepted-passes"
)
PYTHON = Path(sys.executable)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is empty")
    if (RUN_DIR / "run.json").is_file():
        raise FileExistsError(f"Experiment already initialized: {RUN_DIR}")
    if not BASELINE.is_dir():
        raise FileNotFoundError(f"Missing accepted-pass baseline: {BASELINE}")

    provider = OpenAIResponsesProvider(
        api_key=key,
        model="gpt-5.6-terra",
        reasoning_effort="medium",
        background=True,
        prompt_cache_mode="explicit",
        prompt_cache_ttl="30m",
    )
    state, run_json = create_run(
        input_package=INPUT_PACKAGE,
        run_dir=RUN_DIR,
        subject="ella",
        provider=provider,
        max_attempts=3,
        sbe_script=SRC / "build_projected_semantic_basis.py",
        python_executable=PYTHON,
        split_assignment_policy="contiguous",
        full_chart_basis_format="compact-v2",
    )

    reuse_manifest = {
        "source_accepted_passes": str(BASELINE.resolve()),
        "reused_passes": {},
        "experimental_pass": "ella_1",
        "independent_variable": "full_chart_basis_format=compact-v2",
    }
    for number in range(2, 7):
        pass_id = f"ella_{number}"
        source = BASELINE / pass_id
        target = RUN_DIR / "passes" / pass_id / "accepted"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
        state["passes"][pass_id].update({
            "state": "PASS_QA_ACCEPTED",
            "accepted_workspace": str(target.resolve()),
            "accepted_attempt": "reused-compact-v1-baseline",
        })
        reuse_manifest["reused_passes"][pass_id] = {
            "source": str(source.resolve()),
            "source_sha256": {
                str(path.relative_to(source)): digest(path)
                for path in sorted(source.rglob("*")) if path.is_file()
            },
            "destination": str(target.resolve()),
        }
    write_json_atomic(EXPERIMENT / "reuse-manifest.json", reuse_manifest)
    save_state(run_json, state)

    author_pending_passes(
        state=state,
        provider=provider,
        run_dir=RUN_DIR,
        max_attempts=3,
        python_executable=PYTHON,
        run_json=run_json,
        max_workers=1,
    )
    pass1 = state["passes"]["ella_1"]
    if pass1["state"] != "PASS_QA_ACCEPTED":
        raise RuntimeError(f"Ella compact-v2 pass 1 was not accepted: {pass1['state']}")

    finalize_subjects(
        state=state,
        run_dir=RUN_DIR,
        python_executable=PYTHON,
        allow_lint_warnings=True,
        polish=False,
    )
    save_state(run_json, state)
    final = state["subjects"]["ella"]
    result = {
        "status": "complete",
        "run_state": state["status"],
        "pass1_state": pass1["state"],
        "pass1_attempts": pass1["attempts"],
        "final_record": final,
    }
    write_json_atomic(EXPERIMENT / "live-result.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
