"""Submit Phase 0 round 001 only when explicitly invoked with --execute."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROUND_ROOT = Path(__file__).resolve().parent
REQUEST_ROOT = ROUND_ROOT / "request"
RESPONSE_ROOT = ROUND_ROOT / "response"
EVALUATION_ROOT = ROUND_ROOT / "evaluation"
REPO_ROOT = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "astrowoof_natal" / "src").is_dir()
)
SRC_ROOT = REPO_ROOT / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC_ROOT))

from author_semantic_closure import (  # noqa: E402
    OpenAIResponsesProvider,
    apply_sparse_polish,
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def run_qa(script: Path, args: list[str], output: Path) -> int:
    completed = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        completed.stdout + ("\nSTDERR:\n" + completed.stderr if completed.stderr else ""),
        encoding="utf-8",
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually submit a paid OpenAI Responses API request.",
    )
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", default="medium")
    args = parser.parse_args()

    manifest = load(REQUEST_ROOT / "request-manifest.json")
    targets = load(REQUEST_ROOT / "editable-targets.json")
    schema = load(REQUEST_ROOT / "response-schema.json")
    system = (REQUEST_ROOT / "SYSTEM_PROMPT.txt").read_text(encoding="utf-8")
    user = (REQUEST_ROOT / "OPENAI_USER_MESSAGE.txt").read_text(encoding="utf-8")
    summary = {
        "execute": args.execute,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "target_count": len(targets),
        "system_prompt_chars": len(system),
        "user_message_chars": len(user),
        "gold_examples_supplied": False,
        "prior_manual_kevin_prose_supplied": False,
    }
    print(json.dumps(summary, indent=2))
    if not args.execute:
        print("DRY RUN ONLY: add --execute after the human review gate.")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is empty or unavailable")

    RESPONSE_ROOT.mkdir(parents=True, exist_ok=True)
    provider = OpenAIResponsesProvider(
        api_key=api_key,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        background=True,
        max_output_tokens=100_000,
        prompt_cache_mode="disabled",
    )
    idempotency_material = hashlib.sha256(
        (
            manifest["experiment"]
            + system
            + user
            + json.dumps(schema, sort_keys=True)
            + args.model
            + args.reasoning_effort
        ).encode("utf-8")
    ).hexdigest()
    authored, metadata = provider.complete_json(
        system=system,
        user=user,
        schema=schema,
        schema_name="astrowoof_context_naive_polish_round_001",
        attempt_root=RESPONSE_ROOT / "openai-attempt",
        idempotency_material=idempotency_material,
    )
    write_json(RESPONSE_ROOT / "authored-sparse-patch.json", authored)
    write_json(RESPONSE_ROOT / "openai-metadata.json", metadata)

    baseline = load(REQUEST_ROOT / "natal.kevin.cards.normalized-baseline.json")
    target_paths = sorted(targets)
    candidate = apply_sparse_polish(
        baseline,
        authored,
        target_paths=target_paths,
        include_theme_groups=False,
    )
    edited = {edit["field_path"] for edit in authored["edits"]}
    if edited != set(target_paths):
        missing = sorted(set(target_paths) - edited)
        extra = sorted(edited - set(target_paths))
        raise ValueError(f"Sparse response mismatch; missing={missing}, extra={extra}")
    candidate_path = RESPONSE_ROOT / "natal.kevin.cards.phase0-round001.json"
    write_json(candidate_path, candidate)

    validator_rc = run_qa(
        SRC_ROOT / "validate_astrowoof_editorial.py",
        [str(REPO_ROOT / "astrowoof_natal" / "qa" / "reference_decks" / "kevin" / "selected-authoring-packet.json"), str(candidate_path)],
        EVALUATION_ROOT / "candidate-validation-report.log",
    )
    linter_rc = run_qa(
        SRC_ROOT / "lint_astrowoof_editorial.py",
        [str(candidate_path)],
        EVALUATION_ROOT / "candidate-lint-report.log",
    )
    write_json(
        EVALUATION_ROOT / "submission-result.json",
        {
            "candidate": str(candidate_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "edited_field_count": len(edited),
            "validator_returncode": validator_rc,
            "linter_returncode": linter_rc,
            "api_request_completed": True,
        },
    )
    return 0 if validator_rc == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
