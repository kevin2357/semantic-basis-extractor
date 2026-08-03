#!/usr/bin/env python3
"""Run the isolated Ella compact-full-chart pass-6 treatment."""

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
BASELINE_RUN = Path(r"C:\tmp\ella-semantic-closure-batch-recovery-live-20260801")
CONTROL = (
    EXPERIMENT.parent
    / "phase-003-live-ella-chapters"
    / "run"
    / "final"
    / "ella"
    / "natal.ella.cards.json"
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
    if not CONTROL.is_file():
        raise FileNotFoundError(f"Missing legacy control deck: {CONTROL}")

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
        full_chart_basis_format="compact-v1",
    )

    reuse_manifest = {
        "source_run": str(BASELINE_RUN),
        "legacy_control_deck": str(CONTROL),
        "legacy_control_sha256": digest(CONTROL),
        "reused_passes": {},
        "experimental_pass": "ella_6",
        "independent_variable": "full_chart_basis_format=compact-v1",
        "known_incidental_change": (
            "The authoring brief now says projected-term decoder rather than "
            "projected-term registry so it accurately names both transports."
        ),
    }
    for number in range(1, 6):
        pass_id = f"ella_{number}"
        source = BASELINE_RUN / "passes" / pass_id / "accepted"
        target = RUN_DIR / "passes" / pass_id / "accepted"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
        state["passes"][pass_id].update({
            "state": "PASS_QA_ACCEPTED",
            "accepted_workspace": str(target.resolve()),
            "accepted_attempt": "reused-20260801",
        })
        reuse_manifest["reused_passes"][pass_id] = {
            "source": str(source),
            "destination": str(target),
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
    pass6 = state["passes"]["ella_6"]
    if pass6["state"] != "PASS_QA_ACCEPTED":
        raise RuntimeError(f"Ella compact pass 6 was not accepted: {pass6['state']}")

    accepted = Path(pass6["accepted_workspace"])
    for name in (
        "WRITE WHOLE DOG PROFILE.md",
        "WRITE SUMMARY THESIS PLAN.md",
        "ASSIGN THEME GROUPS.md",
    ):
        shutil.copy2(accepted / name, EXPERIMENT / f"treatment-{name}")

    finalize_subjects(
        state=state,
        run_dir=RUN_DIR,
        python_executable=PYTHON,
        allow_lint_warnings=True,
        polish=False,
    )
    save_state(run_json, state)
    final = state["subjects"]["ella"]
    treatment = Path(final["deck"])
    result = {
        "status": "complete",
        "run_state": state["status"],
        "pass6_state": pass6["state"],
        "pass6_attempts": pass6["attempts"],
        "control_deck": str(CONTROL.resolve()),
        "control_sha256": digest(CONTROL),
        "treatment_deck": str(treatment.resolve()),
        "treatment_sha256": digest(treatment),
        "final_record": final,
    }
    write_json_atomic(EXPERIMENT / "live-result.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
