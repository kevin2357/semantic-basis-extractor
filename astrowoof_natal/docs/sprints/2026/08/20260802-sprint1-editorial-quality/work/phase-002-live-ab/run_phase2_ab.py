#!/usr/bin/env python3
"""Run the Phase-2 contiguous-versus-stratified live Kevin A/B."""
from __future__ import annotations
import hashlib, json, os, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
SRC = REPO / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC))
from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider, author_pending_passes, create_run,
    finalize_subjects, load_json, resume_run, save_state, write_json_atomic,
)

EXPERIMENT = Path(__file__).resolve().parent
INPUT_PACKAGE = Path(r"C:\tmp\kevin-semantic-closure-batch-input")
PYTHON = Path(sys.executable)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def make_provider(key: str) -> OpenAIResponsesProvider:
    return OpenAIResponsesProvider(
        api_key=key, model="gpt-5.6-terra", reasoning_effort="medium",
        background=True, prompt_cache_mode="explicit", prompt_cache_ttl="30m",
    )

def initialize(policy: str, provider: OpenAIResponsesProvider):
    run_dir = EXPERIMENT / policy
    state, run_json = create_run(
        input_package=INPUT_PACKAGE, run_dir=run_dir, subject="kevin",
        provider=provider, max_attempts=3,
        sbe_script=SRC / "build_projected_semantic_basis.py",
        python_executable=PYTHON, split_assignment_policy=policy,
    )
    return run_dir, state, run_json

def author_and_finalize(run_dir, state, run_json, provider) -> None:
    author_pending_passes(
        state=state, provider=provider, run_dir=run_dir, max_attempts=3,
        python_executable=PYTHON, run_json=run_json, max_workers=6,
    )
    save_state(run_json, state)
    finalize_subjects(
        state=state, run_dir=run_dir, python_executable=PYTHON,
        allow_lint_warnings=True, polish=False,
    )
    save_state(run_json, state)

def main() -> None:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is empty")
    control_provider = make_provider(key)
    control_dir = EXPERIMENT / "contiguous"
    if (control_dir / "run.json").is_file():
        control, control_json = resume_run(
            run_dir=control_dir, provider=control_provider, max_attempts=3,
            service_level="interactive",
        )
    else:
        control_dir, control, control_json = initialize("contiguous", control_provider)
    author_and_finalize(control_dir, control, control_json, control_provider)
    control_pass6 = control["passes"]["kevin_6"]
    if control_pass6["state"] != "PASS_QA_ACCEPTED":
        raise RuntimeError(f"Control pass 6 was not accepted: {control_pass6['state']}")

    treatment_provider = make_provider(key)
    treatment_dir = EXPERIMENT / "stratified-v1"
    if (treatment_dir / "run.json").is_file():
        treatment, treatment_json = resume_run(
            run_dir=treatment_dir, provider=treatment_provider, max_attempts=3,
            service_level="interactive",
        )
    else:
        treatment_dir, treatment, treatment_json = initialize(
            "stratified-v1", treatment_provider
        )
        source = Path(control_pass6["accepted_workspace"])
        target = treatment_dir / "passes" / "kevin_6" / "accepted"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
        treatment_pass6 = treatment["passes"]["kevin_6"]
        treatment_pass6.update({
            "state": "PASS_QA_ACCEPTED", "accepted_workspace": str(target.resolve()),
            "accepted_attempt": "reused-from-contiguous-control",
        })
        save_state(treatment_json, treatment)
        write_json_atomic(EXPERIMENT / "shared-pass6-manifest.json", {
            "source": str(source), "destination": str(target),
            "files": {
                str(path.relative_to(source)).replace("\\", "/"): digest(path)
                for path in sorted(source.rglob("*")) if path.is_file()
            },
        })
    author_and_finalize(treatment_dir, treatment, treatment_json, treatment_provider)

    # Finalization persists authoritative subject records; reload them so a
    # resumed harness never relies on a stale pre-finalization in-memory view.
    control = load_json(control_json)
    treatment = load_json(treatment_json)
    records = {name: state["subjects"]["kevin"] for name, state in (
        ("contiguous", control), ("stratified-v1", treatment))}
    decks = {name: load_json(Path(record["deck"])) for name, record in records.items()}
    if decks["contiguous"]["summary"] != decks["stratified-v1"]["summary"]:
        raise AssertionError("Shared pass 6 did not produce identical summaries")
    result = {
        "status": "complete", "subject": "kevin", "model": "gpt-5.6-terra",
        "reasoning_effort": "medium", "polish": False, "shared_pass6": True,
        "summary_identical": True,
        "runs": {
            name: {
                "state": state["status"], "deck": record["deck"],
                "validation_report": record.get("validation_report"),
                "lint_report": record.get("lint_report"),
                "usage": state.get("usage"), "cost": state.get("cost"),
                "passes": {pid: item.get("attempts", []) for pid, item in state["passes"].items()},
            }
            for name, state, record in (
                ("contiguous", control, records["contiguous"]),
                ("stratified-v1", treatment, records["stratified-v1"]),
            )
        },
    }
    write_json_atomic(EXPERIMENT / "live-result.json", result)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
