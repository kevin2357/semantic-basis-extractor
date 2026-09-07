"""Replay retained polish candidates with released production semantics."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from astrowoof_natal_authoring.assembly import assemble
from astrowoof_natal_authoring.closure import (
    apply_sparse_polish,
    sanitize_context_filters,
)
from astrowoof_natal_authoring.editorial_lint import lint_deck


TARGET_MARKER = "EDITABLE TARGETS (only these paths may be replaced):\n"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def set_path(value: Any, field_path: str, replacement: str) -> None:
    current = value
    parts = field_path.split(".")
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    last = parts[-1]
    if isinstance(current, list):
        current[int(last)] = replacement
    else:
        current[last] = replacement


def request_targets(path: Path) -> dict[str, str]:
    request = load(path)
    messages = request.get("input")
    if not isinstance(messages, list):
        raise ValueError(f"request has no input messages: {path}")
    user_text = next(
        (
            item.get("content")
            for item in messages
            if isinstance(item, dict) and item.get("role") == "user"
        ),
        None,
    )
    if not isinstance(user_text, str) or TARGET_MARKER not in user_text:
        raise ValueError(f"request has no exact editable-target section: {path}")
    targets, _ = json.JSONDecoder().raw_decode(
        user_text.split(TARGET_MARKER, 1)[1]
    )
    if not isinstance(targets, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in targets.items()
    ):
        raise ValueError(f"editable-target section is not a string map: {path}")
    return targets


def normalized_lint(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("path", None)
    return result


def rerun_validation(
    *,
    predecessor: dict[str, Any],
    candidate: Path,
    source_root: Path,
    allow_summary_edits: bool,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-editorial-replay-") as raw:
        prior = Path(raw) / "predecessor.json"
        report = Path(raw) / "validation.json"
        prior.write_bytes(canonical(predecessor))
        env = os.environ.copy()
        env["PYTHONPATH"] = str(source_root)
        command = [
                sys.executable,
                "-m",
                "astrowoof_natal_authoring.validation",
                str(prior),
                str(candidate),
                "--phase",
                "polish",
                "--report",
                str(report),
            ]
        if allow_summary_edits:
            command.append("--allow-summary-edits")
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        if completed.returncode not in (0, 1) or not report.is_file():
            raise RuntimeError(
                f"validation replay failed unexpectedly for {candidate}: "
                f"exit={completed.returncode} stderr={completed.stderr!r}"
            )
        return load(report)


def warning_texts(deck: dict[str, Any], lint: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for finding in lint.get("warnings", []):
        details = finding.get("details") if isinstance(finding, dict) else None
        if not isinstance(details, dict):
            continue
        field = details.get("field")
        claim_ids = details.get("claim_ids")
        if not isinstance(field, str) or not isinstance(claim_ids, list):
            continue
        values: list[dict[str, str]] = []
        for claim_id in claim_ids:
            if not isinstance(claim_id, str):
                continue
            if claim_id.startswith("summary:"):
                current: Any = deck.get("summary", {}).get(claim_id.split(":", 1)[1], {})
            else:
                current = next(
                    (item.get("card", {}) for item in deck.get("cards", []) if item.get("claim_id") == claim_id),
                    {},
                )
            try:
                for part in field.split("."):
                    current = current[part]
            except (KeyError, TypeError):
                continue
            if isinstance(current, str):
                values.append({"claim_id": claim_id, "text": current})
        result.append(
            {
                "code": finding.get("code"),
                "field": field,
                "opening": details.get("opening"),
                "declared_count": details.get("count"),
                "values": values,
            }
        )
    return result


def replay(label: str, workspace: Path, source_root: Path) -> dict[str, Any]:
    run = load(workspace / "run.json")
    subject_id, subject = next(iter(run["subjects"].items()))
    final_root = workspace / "final" / subject_id
    selected_packet_path = (
        workspace
        / "sbe"
        / "semantic-basis-output"
        / subject_id
        / f"{subject_id}.selected-authoring-packet.json"
    )
    attempts: list[dict[str, Any]] = []
    first_predecessor: dict[str, Any] | None = None
    for native in subject.get("polish_attempts", []):
        number = int(native["attempt_number"])
        root = final_root / "polish" / f"attempt-{number:03d}"
        candidate_path = root / f"natal.{subject_id}.cards.json"
        request_path = root / "openai-request.json"
        sparse_path = root / "polished-deck.json"
        entry: dict[str, Any] = {
            "attempt": number,
            "native_state": native.get("state"),
            "accepted": native.get("accepted"),
            "candidate_present": candidate_path.is_file(),
            "error": native.get("error"),
        }
        if candidate_path.is_file() and request_path.is_file() and sparse_path.is_file():
            candidate = load(candidate_path)
            targets = request_targets(request_path)
            predecessor = copy.deepcopy(candidate)
            for field_path, prior_value in targets.items():
                set_path(predecessor, field_path, prior_value)
            if first_predecessor is None:
                first_predecessor = predecessor
            applied = apply_sparse_polish(
                predecessor,
                load(sparse_path),
                target_paths=list(targets),
                include_theme_groups=False,
            )
            stored_lint = load(root / "lint-report.json")["decks"][0]
            replay_lint = lint_deck(candidate_path, candidate)
            stored_validation = load(root / "validation-report.json")
            replay_validation = rerun_validation(
                predecessor=predecessor,
                candidate=candidate_path,
                source_root=source_root,
                allow_summary_edits=bool(
                    stored_validation.get("checks", {})
                    .get("polish_edit_overrides", {})
                    .get("summary")
                ),
            )
            entry.update(
                {
                    "editable_target_count": len(targets),
                    "edit_count": len(load(sparse_path).get("edits", [])),
                    "predecessor_semantic_sha256": digest(predecessor),
                    "candidate_semantic_sha256": digest(candidate),
                    "reapplied_semantic_sha256": digest(applied),
                    "reapplied_equals_candidate": applied == candidate,
                    "lint_replay_equal": normalized_lint(replay_lint) == normalized_lint(stored_lint),
                    "validation_replay_equal": replay_validation == stored_validation,
                    "validation_difference": (
                        None
                        if replay_validation == stored_validation
                        else {
                            "stored": stored_validation,
                            "replayed": replay_validation,
                        }
                    ),
                    "lint_status": replay_lint.get("authoring_pass_acceptance", {}).get("status"),
                    "warning_count": replay_lint.get("warning_count"),
                    "warning_evidence": warning_texts(candidate, replay_lint),
                    "validation_status": replay_validation.get("status"),
                    "validation_errors": replay_validation.get("errors", []),
                }
            )
        attempts.append(entry)

    assembly_result: dict[str, Any] = {"available": False}
    if first_predecessor is not None:
        with tempfile.TemporaryDirectory(prefix="astrowoof-assembly-replay-") as raw:
            accepted_root = Path(raw) / "accepted-passes"
            accepted_root.mkdir()
            records = sorted(
                run["passes"].values(), key=lambda item: int(item["pass_number"])
            )
            for record in records:
                source = workspace / "passes" / record["pass_id"] / "accepted"
                shutil.copytree(source, accepted_root / record["pass_id"])
            assembled, report = assemble(
                load(selected_packet_path), accepted_root, allow_partial=False
            )
            repairs = sanitize_context_filters(assembled)
            assembly_result = {
                "available": True,
                "pass_count": len(records),
                "assembled_semantic_sha256": digest(assembled),
                "pre_polish_semantic_sha256": digest(first_predecessor),
                "assembled_equals_pre_polish": assembled == first_predecessor,
                "context_filter_repairs": repairs,
                "assembly_report_semantic_sha256": digest(report),
            }

    final_deck_path = final_root / f"natal.{subject_id}.cards.json"
    final_deck = load(final_deck_path)
    final_lint = lint_deck(final_deck_path, final_deck)
    return {
        "label": label,
        "native_run_id": run.get("run_id"),
        "subject_id": subject_id,
        "run_status": run.get("status"),
        "subject_state": subject.get("state"),
        "initial_assembly": assembly_result,
        "polish_attempts": attempts,
        "final": {
            "deck_semantic_sha256": digest(final_deck),
            "lint_status": final_lint.get("authoring_pass_acceptance", {}).get("status"),
            "warning_count": final_lint.get("warning_count"),
            "warning_evidence": warning_texts(final_deck, final_lint),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[6] / "src"
    cases = {
        "doughmeat": "doughmeat-generation-11-restored",
        "macaron": "macaron-generation-11-restored",
        "madeleine": "madeleine-generation-9-restored",
        "frisbee": "frisbee-generation-11-restored",
        "ordinary-success-control": "ordinary-success-generation-10-restored",
    }
    result = {
        "schema_version": "astrowoof.private_editorial_replay.v1",
        "cases": [
            replay(label, args.root / directory / "workspace", source_root)
            for label, directory in cases.items()
        ],
    }
    result["receipt_sha256"] = digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps({"output": str(args.output), "receipt_sha256": result["receipt_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
