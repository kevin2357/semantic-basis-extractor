"""Submit Round 2 only when explicitly invoked with --execute."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
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
ROUND1_BASELINE = (
    ROUND_ROOT.parent / "round-001" / "request"
    / "natal.kevin.cards.normalized-baseline.json"
)
sys.path.insert(0, str(SRC_ROOT))

from author_semantic_closure import OpenAIResponsesProvider  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def assign_path(root, path: str, value: str) -> None:
    current = root
    parts = path.split(".")
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    last = parts[-1]
    if isinstance(current, list):
        current[int(last)] = value
    else:
        current[last] = value


def apply_decisions(baseline: dict, targets: dict, authored: dict) -> tuple[dict, dict]:
    decisions = authored.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != len(targets):
        raise ValueError("Response must contain one decision per target")
    result = deepcopy(baseline)
    seen = set()
    counts = {"keep": 0, "replace": 0}
    for item in decisions:
        path = item.get("field_path")
        action = item.get("action")
        replacement = item.get("replacement")
        if path not in targets or path in seen:
            raise ValueError(f"Invalid or duplicate field path: {path}")
        if action not in counts:
            raise ValueError(f"Invalid action for {path}: {action}")
        if not isinstance(replacement, str) or not replacement.strip():
            raise ValueError(f"Replacement must be nonempty for {path}")
        if action == "keep" and replacement != targets[path]:
            raise ValueError(f"Keep decision must copy current value verbatim: {path}")
        assign_path(result, path, replacement if action == "replace" else targets[path])
        counts[action] += 1
        seen.add(path)
    if seen != set(targets):
        raise ValueError(f"Missing target decisions: {sorted(set(targets) - seen)}")
    return result, counts


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
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", default="medium")
    args = parser.parse_args()

    targets = load(REQUEST_ROOT / "editable-targets.json")
    schema = load(REQUEST_ROOT / "response-schema.json")
    system = (REQUEST_ROOT / "SYSTEM_PROMPT.txt").read_text(encoding="utf-8")
    user = (REQUEST_ROOT / "OPENAI_USER_MESSAGE.txt").read_text(encoding="utf-8")
    print(json.dumps({
        "execute": args.execute,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "target_count": len(targets),
        "system_prompt_chars": len(system),
        "user_message_chars": len(user),
    }, indent=2))
    if not args.execute:
        print("DRY RUN ONLY: add --execute after review and approval.")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is empty or unavailable")
    provider = OpenAIResponsesProvider(
        api_key=api_key,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        background=True,
        max_output_tokens=100_000,
        prompt_cache_mode="disabled",
    )
    identity = hashlib.sha256(
        (system + user + json.dumps(schema, sort_keys=True) + args.model
         + args.reasoning_effort).encode("utf-8")
    ).hexdigest()
    authored, metadata = provider.complete_json(
        system=system,
        user=user,
        schema=schema,
        schema_name="astrowoof_polish_keep_replace_round_002",
        attempt_root=RESPONSE_ROOT / "openai-attempt",
        idempotency_material=identity,
    )
    write_json(RESPONSE_ROOT / "editorial-decisions.json", authored)
    write_json(RESPONSE_ROOT / "openai-metadata.json", metadata)
    candidate, counts = apply_decisions(load(ROUND1_BASELINE), targets, authored)
    candidate_path = RESPONSE_ROOT / "natal.kevin.cards.phase0-round002.json"
    write_json(candidate_path, candidate)

    packet = (
        REPO_ROOT / "astrowoof_natal" / "qa" / "reference_decks" / "kevin"
        / "selected-authoring-packet.json"
    )
    validator_rc = run_qa(
        SRC_ROOT / "validate_astrowoof_editorial.py",
        [str(packet), str(candidate_path)],
        EVALUATION_ROOT / "candidate-validation-report.log",
    )
    linter_rc = run_qa(
        SRC_ROOT / "lint_astrowoof_editorial.py",
        [str(candidate_path)],
        EVALUATION_ROOT / "candidate-lint-report.log",
    )
    write_json(EVALUATION_ROOT / "submission-result.json", {
        "candidate": str(candidate_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "decision_counts": counts,
        "validator_returncode": validator_rc,
        "linter_returncode": linter_rc,
        "api_request_completed": True,
    })
    return 0 if validator_rc == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
