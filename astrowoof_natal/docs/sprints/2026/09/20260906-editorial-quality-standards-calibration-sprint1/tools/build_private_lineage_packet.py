"""Build a deterministic private editorial lineage packet from a validated restore."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_sha(path: Path) -> str:
    value = load(path)
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def report_projection(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    value = load(path)
    warnings: list[dict[str, Any]] = []
    for deck in value.get("decks", []) if isinstance(value.get("decks"), list) else []:
        if isinstance(deck, dict):
            warnings.extend(item for item in deck.get("warnings", []) if isinstance(item, dict))
    warnings.extend(item for item in value.get("cross_subject_warnings", []) if isinstance(item, dict))
    return {
        "path": path.as_posix(),
        "byte_sha256": sha(path),
        "semantic_sha256": semantic_sha(path),
        "status": value.get("status"),
        "errors": value.get("errors", []),
        "warnings": value.get("warnings", []),
        "warning_count": value.get("warning_count", len(warnings)),
        "lint_findings": warnings,
        "authoring_pass_acceptance": (
            value.get("decks", [{}])[0].get("authoring_pass_acceptance")
            if isinstance(value.get("decks"), list) and value.get("decks")
            else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    run = load(args.workspace / "run.json")
    if len(run.get("subjects", {})) != 1:
        raise ValueError("expected exactly one subject")
    subject_id, subject_state = next(iter(run["subjects"].items()))
    final_dir = args.workspace / "final" / subject_id
    final_deck = final_dir / f"natal.{subject_id}.cards.json"
    pass_reports = []
    for number in range(1, 7):
        path = args.workspace / "passes" / f"{subject_id}_{number}" / "attempt-001" / "authoring-pass-acceptance.json"
        value = load(path)
        pass_reports.append({
            "pass": number,
            "byte_sha256": sha(path),
            "semantic_sha256": semantic_sha(path),
            "status": value.get("status"),
            "editorial_issue_codes": value.get("editorial_issue_codes", []),
            "advisory_issue_codes": value.get("advisory_issue_codes", []),
        })

    attempts = []
    for attempt in subject_state.get("polish_attempts", []):
        number = attempt["attempt_number"]
        directory = final_dir / "polish" / f"attempt-{number:03d}"
        response = directory / "openai-response.json"
        sparse = directory / "polished-deck.json"
        candidate = directory / f"natal.{subject_id}.cards.json"
        sparse_value = load(sparse) if sparse.is_file() else None
        attempts.append({
            "attempt": number,
            "native_state": attempt.get("state"),
            "accepted": attempt.get("accepted"),
            "improved": attempt.get("improved"),
            "warning_count": attempt.get("warning_count"),
            "warning_components": attempt.get("warning_components"),
            "validation_error_count": attempt.get("validation_error_count"),
            "edited_field_count": attempt.get("edited_field_count"),
            "omitted_target_count": attempt.get("omitted_target_count"),
            "error": attempt.get("error"),
            "paid_action_id": attempt.get("paid_action_id"),
            "response_id": (attempt.get("provider_metadata") or {}).get("response_id"),
            "response_byte_sha256": sha(response) if response.is_file() else None,
            "sparse_edit_byte_sha256": sha(sparse) if sparse.is_file() else None,
            "sparse_edits": sparse_value.get("edits", []) if isinstance(sparse_value, dict) else None,
            "candidate_byte_sha256": sha(candidate) if candidate.is_file() else None,
            "candidate_semantic_sha256": semantic_sha(candidate) if candidate.is_file() else None,
            "validation": report_projection(directory / "validation-report.json"),
            "lint": report_projection(directory / "lint-report.json"),
        })

    result_ids = load(args.workspace / "native-result-index.json").get("result_ids")
    if not isinstance(result_ids, list) or not result_ids or not all(isinstance(item, str) for item in result_ids):
        raise ValueError("native result index has no closed result sequence")
    latest_result_id = result_ids[-1]
    result_path = args.workspace / "native-results" / f"{latest_result_id}.json"
    final_byte_sha = sha(final_deck)
    final_semantic_sha = semantic_sha(final_deck)
    last_candidate = next((item for item in reversed(attempts) if item["candidate_byte_sha256"]), None)
    packet = {
        "schema_version": "astrowoof.private_editorial_lineage_packet.v1",
        "label": args.label,
        "native_run_id": run.get("run_id"),
        "state_revision": run.get("state_revision"),
        "run_status": run.get("status"),
        "subject_id": subject_id,
        "subject_state": subject_state.get("state"),
        "initial_passes": pass_reports,
        "baseline_warning_count": subject_state.get("baseline_warning_count"),
        "baseline_warning_components": subject_state.get("baseline_warning_components"),
        "polish_attempts": attempts,
        "final": {
            "deck_byte_sha256": final_byte_sha,
            "deck_semantic_sha256": final_semantic_sha,
            "validation": report_projection(final_dir / f"natal.{subject_id}.validation-report.json"),
            "lint": report_projection(final_dir / f"natal.{subject_id}.lint-report.json"),
            "equals_last_materialized_candidate_bytes": bool(last_candidate and final_byte_sha == last_candidate["candidate_byte_sha256"]),
            "equals_last_materialized_candidate_semantics": bool(last_candidate and final_semantic_sha == last_candidate["candidate_semantic_sha256"]),
        },
        "native_result": {
            "result_id": latest_result_id,
            "byte_sha256": sha(result_path),
            "semantic_sha256": semantic_sha(result_path),
            "value": load(result_path),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"label": args.label, "output": str(args.output), "polish_attempts": len(attempts), "result_id": latest_result_id}, sort_keys=True))


if __name__ == "__main__":
    main()
