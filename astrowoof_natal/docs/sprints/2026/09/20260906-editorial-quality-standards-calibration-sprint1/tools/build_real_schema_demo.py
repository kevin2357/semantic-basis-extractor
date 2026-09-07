"""Materialize private real-corpus fixtures in three query experiment shapes."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

from replay_polish_lineage import load, request_targets


CASES = {
    "doughmeat": "doughmeat-generation-11-restored",
    "macaron": "macaron-generation-11-restored",
    "madeleine": "madeleine-generation-9-restored",
    "frisbee": "frisbee-generation-11-restored",
    "ordinary-success-control": "ordinary-success-generation-10-restored",
}
EXPERIMENT = "sprint87-editorial-schema-zeroalpha-real-v1"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def get_path(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def safe_load(path: Path) -> Any | None:
    return load(path) if path.is_file() else None


def event(shape: str, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "message": f"Sprint 87 real private {kind}",
        "schema_experiment": EXPERIMENT,
        "shape": shape,
        "row_kind": kind,
        **payload,
    }


def build_packet(label: str, workspace: Path) -> dict[str, Any]:
    run = load(workspace / "run.json")
    subject_id, subject = next(iter(run["subjects"].items()))
    final_root = workspace / "final" / subject_id
    final_deck_path = final_root / f"natal.{subject_id}.cards.json"
    decisions: list[dict[str, Any]] = []
    for record in sorted(run["passes"].values(), key=lambda item: int(item["pass_number"])):
        for attempt in record.get("attempts", []):
            number = int(attempt["attempt_number"])
            root = workspace / "passes" / record["pass_id"] / f"attempt-{number:03d}"
            metadata = attempt.get("provider_metadata") or {}
            decisions.append({
                "decision_id": f"{record['pass_id']}:attempt-{number:03d}",
                "decision_ordinal": len(decisions) + 1,
                "stage": "initial_pass" if number == 1 else "creative_retry",
                "pass_number": int(record["pass_number"]),
                "attempt": number,
                "action_kind": "authoring_initial" if number == 1 else "creative_retry",
                "action_id": attempt.get("paid_action_id"),
                "response_id": metadata.get("response_id"),
                "native_state": attempt.get("state"),
                "candidate_materialized": bool(attempt.get("response_workspace")),
                "acceptance": safe_load(root / "authoring-pass-acceptance.json"),
                "provider_response": safe_load(root / "openai-response.json"),
            })
    for attempt in subject.get("polish_attempts", []):
        number = int(attempt["attempt_number"])
        root = final_root / "polish" / f"attempt-{number:03d}"
        candidate_path = root / f"natal.{subject_id}.cards.json"
        candidate = safe_load(candidate_path)
        targets = request_targets(root / "openai-request.json") if (root / "openai-request.json").is_file() else {}
        transitions = []
        for path, before in sorted(targets.items()):
            after = None
            if isinstance(candidate, dict):
                try:
                    after = get_path(candidate, path)
                except (KeyError, IndexError, TypeError, ValueError):
                    after = None
            transitions.append({"field_path": path, "before": before, "after": after})
        metadata = attempt.get("provider_metadata") or {}
        decisions.append({
            "decision_id": f"polish:attempt-{number:03d}",
            "decision_ordinal": len(decisions) + 1,
            "stage": f"polish{number}",
            "attempt": number,
            "action_kind": "ordinary_v2_polish",
            "action_id": attempt.get("paid_action_id"),
            "response_id": metadata.get("response_id"),
            "native_state": attempt.get("state"),
            "candidate_materialized": candidate is not None,
            "historical_accepted": attempt.get("accepted"),
            "historical_improved": attempt.get("improved"),
            "construction_failure": attempt.get("error"),
            "selected_predecessor_retained": attempt.get("accepted") is False,
            "field_transitions": transitions,
            "provider_response": safe_load(root / "openai-response.json"),
            "validation": safe_load(root / "validation-report.json"),
            "lint": safe_load(root / "lint-report.json"),
        })
    result_ids = load(workspace / "native-result-index.json")["result_ids"]
    result = load(workspace / "native-results" / f"{result_ids[-1]}.json")
    packet = {
        "schema_version": "astrowoof.private_editorial_schema_demo.v1",
        "source_label": label,
        "packet_id": f"real-{run['run_id'][:24]}",
        "native_run_id": run["run_id"],
        "subject_id": subject_id,
        "terminal_run_status": run.get("status"),
        "terminal_subject_state": subject.get("state"),
        "release": run.get("provenance", {}).get("runtime", {}).get("version"),
        "profile_id": run.get("authoring_profile", {}).get("profile_id"),
        "selected_deck": load(final_deck_path),
        "selected_deck_sha256": hashlib.sha256(final_deck_path.read_bytes()).hexdigest(),
        "final_validation": safe_load(final_root / f"natal.{subject_id}.validation-report.json"),
        "final_lint": safe_load(final_root / f"natal.{subject_id}.lint-report.json"),
        "native_result": result,
        "decisions": decisions,
    }
    packet["canonical_packet_sha256"] = sha(packet)
    return packet


def strip_artifacts(decision: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in decision.items() if key not in {"provider_response", "acceptance", "validation", "lint"}}


def correlated(packet: dict[str, Any]) -> list[dict[str, Any]]:
    packet_id = packet["packet_id"]
    rows = [event("correlated_row", "packet", {
        key: packet.get(key) for key in (
            "packet_id", "canonical_packet_sha256", "native_run_id", "subject_id",
            "terminal_run_status", "terminal_subject_state", "release", "profile_id",
            "selected_deck_sha256",
        )
    })]
    rows.append(event("correlated_row", "selected_deck", {"packet_id": packet_id, "content": packet["selected_deck"]}))
    for kind in ("final_validation", "final_lint", "native_result"):
        rows.append(event("correlated_row", kind, {"packet_id": packet_id, "content": packet[kind]}))
    for decision in packet["decisions"]:
        decision_id = decision["decision_id"]
        rows.append(event("correlated_row", "decision", {"packet_id": packet_id, **strip_artifacts(decision)}))
        for kind in ("provider_response", "acceptance", "validation", "lint"):
            if decision.get(kind) is not None:
                rows.append(event("correlated_row", kind, {"packet_id": packet_id, "decision_id": decision_id, "content": decision[kind]}))
        for position, transition in enumerate(decision.get("field_transitions", []), start=1):
            rows.append(event("correlated_row", "field_transition", {"packet_id": packet_id, "decision_id": decision_id, "field_ordinal": position, **transition}))
    return rows


def projection(packet: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    validation = decision.get("validation") or {}
    lint = decision.get("lint") or {}
    acceptance = lint.get("decks", [{}])[0].get("authoring_pass_acceptance", {}) if isinstance(lint.get("decks"), list) and lint.get("decks") else {}
    return event("hybrid_projection", "decision_projection", {
        "packet_id": packet["packet_id"],
        "canonical_packet_sha256": packet["canonical_packet_sha256"],
        "decision_id": decision["decision_id"],
        "decision_ordinal": decision["decision_ordinal"],
        "stage": decision["stage"],
        "action_kind": decision.get("action_kind"),
        "action_id": decision.get("action_id"),
        "response_id": decision.get("response_id"),
        "candidate_materialized": decision.get("candidate_materialized"),
        "historical_accepted": decision.get("historical_accepted"),
        "construction_failure": decision.get("construction_failure"),
        "selected_predecessor_retained": decision.get("selected_predecessor_retained"),
        "field_transitions": decision.get("field_transitions", []),
        "validation_status": validation.get("status"),
        "whole_deck_acceptance": acceptance.get("status"),
        "editorial_issue_codes": acceptance.get("editorial_issue_codes", []),
        "advisory_issue_codes": acceptance.get("advisory_issue_codes", []),
        "terminal_run_status": packet["terminal_run_status"],
        "release": packet["release"],
    })


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    data = b"".join(canonical(row) for row in rows)
    path.write_bytes(data)
    compressed = gzip.compress(data, mtime=0)
    return {
        "path": path.name,
        "records": len(rows),
        "utf8_bytes": len(data),
        "gzip_bytes": len(compressed),
        "sha256": hashlib.sha256(data).hexdigest(),
        "gzip_sha256": hashlib.sha256(compressed).hexdigest(),
    }


def packet_size_layers(packet: dict[str, Any]) -> dict[str, Any]:
    core = copy.deepcopy(packet)
    deck = core.pop("selected_deck")
    final_reports = {
        key: core.pop(key) for key in ("final_validation", "final_lint", "native_result")
    }
    responses = []
    decision_reports = []
    for decision in core["decisions"]:
        response = decision.pop("provider_response", None)
        if response is not None:
            responses.append(response)
        reports = {
            key: decision.pop(key)
            for key in ("acceptance", "validation", "lint")
            if decision.get(key) is not None
        }
        if reports:
            decision_reports.append(reports)
    layers = {
        "core": core,
        "selected_deck": deck,
        "provider_responses": responses,
        "reports_and_result": {"final": final_reports, "decisions": decision_reports},
    }
    return {
        "packet_id": packet["packet_id"],
        "layers": {
            name: {
                "utf8_bytes": len(canonical(value)),
                "gzip_bytes": len(gzip.compress(canonical(value), mtime=0)),
            }
            for name, value in layers.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    packets = [build_packet(label, args.root / directory / "workspace") for label, directory in CASES.items()]
    nested = [event("nested_packet", "packet", {"editorial_packet": packet}) for packet in packets]
    correlated_rows = [row for packet in packets for row in correlated(packet)]
    hybrid_rows = nested + [projection(packet, decision) for packet in packets for decision in packet["decisions"]]
    metrics = {
        "schema_version": "astrowoof.private_editorial_schema_demo_measurements.v1",
        "experiment": EXPERIMENT,
        "lineages": len(packets),
        "decisions": sum(len(packet["decisions"]) for packet in packets),
        "creative_retry_decisions": sum(decision["stage"] == "creative_retry" for packet in packets for decision in packet["decisions"]),
        "packet_size_layers": [packet_size_layers(packet) for packet in packets],
        "shapes": [
            write_jsonl(args.output / "nested-packet.jsonl", nested),
            write_jsonl(args.output / "correlated-rows.jsonl", correlated_rows),
            write_jsonl(args.output / "hybrid-packet-and-projections.jsonl", hybrid_rows),
        ],
    }
    metrics["receipt_sha256"] = sha(metrics)
    (args.output / "measurements.json").write_bytes(canonical(metrics))
    print(json.dumps(metrics, sort_keys=True))


if __name__ == "__main__":
    main()
