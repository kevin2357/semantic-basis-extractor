"""Build private blinded editorial-review packets and a separate answer key."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from astrowoof_natal_authoring.editorial_lint import lint_deck

from replay_polish_lineage import (
    digest,
    load,
    request_targets,
    rerun_validation,
    set_path,
    warning_texts,
)


CASES = {
    "doughmeat": "doughmeat-generation-11-restored",
    "macaron": "macaron-generation-11-restored",
    "madeleine": "madeleine-generation-9-restored",
    "frisbee": "frisbee-generation-11-restored",
    "ordinary-success-control": "ordinary-success-generation-10-restored",
}


def get_path(value: Any, field_path: str) -> Any:
    current = value
    for part in field_path.split("."):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: Any) -> int:
    data = canonical_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def finding_projection(deck: dict[str, Any], lint: dict[str, Any]) -> dict[str, Any]:
    acceptance = lint.get("authoring_pass_acceptance", {})
    return {
        "status": acceptance.get("status"),
        "editorial_issue_codes": acceptance.get("editorial_issue_codes", []),
        "advisory_issue_codes": acceptance.get("advisory_issue_codes", []),
        "warning_count": lint.get("warning_count"),
        "findings": warning_texts(deck, lint),
    }


def build_case(label: str, workspace: Path, source_root: Path) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    run = load(workspace / "run.json")
    subject_id, subject = next(iter(run["subjects"].items()))
    final_root = workspace / "final" / subject_id
    packets: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for native in subject.get("polish_attempts", []):
        number = int(native["attempt_number"])
        root = final_root / "polish" / f"attempt-{number:03d}"
        candidate_path = root / f"natal.{subject_id}.cards.json"
        request_path = root / "openai-request.json"
        sparse_path = root / "polished-deck.json"
        if not (candidate_path.is_file() and request_path.is_file() and sparse_path.is_file()):
            continue
        candidate = load(candidate_path)
        targets = request_targets(request_path)
        predecessor = copy.deepcopy(candidate)
        for field_path, prior_value in targets.items():
            set_path(predecessor, field_path, prior_value)
        prior_lint = lint_deck(Path("blinded-prior.json"), predecessor)
        candidate_lint = lint_deck(candidate_path, candidate)
        stored_validation = load(root / "validation-report.json")
        validation = rerun_validation(
            predecessor=predecessor,
            candidate=candidate_path,
            source_root=source_root,
            allow_summary_edits=bool(
                stored_validation.get("checks", {})
                .get("polish_edit_overrides", {})
                .get("summary")
            ),
        )
        transition = [
            {
                "path": path,
                "before": before,
                "after": get_path(candidate, path),
            }
            for path, before in sorted(targets.items())
        ]
        evidence = {
            "schema_version": "astrowoof.private_blinded_editorial_review.v1",
            "rubric_version": "astrowoof.editorial_calibration_rubric.v1-draft",
            "candidate_position": number,
            "transition": transition,
            "prior_findings": finding_projection(predecessor, prior_lint),
            "candidate_findings": finding_projection(candidate, candidate_lint),
            "candidate_validation": {
                "status": validation.get("status"),
                "errors": validation.get("errors", []),
            },
            "provenance": {
                "predecessor_semantic_sha256": digest(predecessor),
                "candidate_semantic_sha256": digest(candidate),
                "request_targets_sha256": digest(targets),
                "sparse_edits_sha256": digest(load(sparse_path)),
            },
        }
        blind_digest = hashlib.sha256(canonical_bytes(evidence)).hexdigest()
        evidence["packet_id"] = f"editorial-{blind_digest[:24]}"
        answer = {
            "packet_id": evidence["packet_id"],
            "source_label": label,
            "native_run_id": run.get("run_id"),
            "subject_id": subject_id,
            "attempt": number,
            "historical_native_state": native.get("state"),
            "historical_accepted": native.get("accepted"),
            "historical_improved": native.get("improved"),
            "historical_error": native.get("error"),
            "terminal_run_status": run.get("status"),
            "terminal_subject_state": subject.get("state"),
        }
        packets.append((evidence, answer))
    return packets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[6] / "src"
    measurements: list[dict[str, Any]] = []
    answer_key: list[dict[str, Any]] = []
    for label, directory in CASES.items():
        workspace = args.root / directory / "workspace"
        for packet, answer in build_case(label, workspace, source_root):
            packet_id = packet["packet_id"]
            finding_bytes = write_json(args.output / "finding-local" / f"{packet_id}.json", packet)
            subject_id = answer["subject_id"]
            final_deck = load(workspace / "final" / subject_id / f"natal.{subject_id}.cards.json")
            full_packet = copy.deepcopy(packet)
            full_packet["complete_selected_deck"] = final_deck
            full_bytes = write_json(args.output / "full-deck" / f"{packet_id}.json", full_packet)
            answer_key.append(answer)
            measurements.append({
                "packet_id": packet_id,
                "finding_local_utf8_bytes": finding_bytes,
                "full_deck_utf8_bytes": full_bytes,
                "complete_deck_increment_utf8_bytes": full_bytes - finding_bytes,
            })
    write_json(args.output / "answer-key.json", {"answers": answer_key})
    manifest = {
        "schema_version": "astrowoof.private_editorial_packet_measurements.v1",
        "packet_count": len(measurements),
        "measurements": measurements,
        "finding_local_max_utf8_bytes": max(item["finding_local_utf8_bytes"] for item in measurements),
        "full_deck_max_utf8_bytes": max(item["full_deck_utf8_bytes"] for item in measurements),
    }
    manifest["receipt_sha256"] = digest(manifest)
    write_json(args.output / "measurements.json", manifest)
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
