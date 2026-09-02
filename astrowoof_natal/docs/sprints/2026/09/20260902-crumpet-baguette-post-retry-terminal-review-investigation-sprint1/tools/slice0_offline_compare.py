"""Validate and summarize two restored terminal-review checkpoints offline."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from astrowoof_natal_authoring.native_transitions import (
    journal_range,
    validate_native_publication_receipt,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    _binding,
    _digest,
    validate_terminal_review_result_v02,
)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def summarize(label: str, root: Path, result_id: str) -> dict[str, Any]:
    state = load(root / "run.json")
    snapshot = load(root / "workspace-snapshot.json")
    result = load(root / "native-results" / f"{result_id}.json")
    receipt_root = root / "native-publication-receipts"
    receipt = load(receipt_root / f"{result_id}.json")
    retained_snapshot_path = receipt_root / f"{result_id}.workspace-snapshot.json"
    retained_snapshot = load(retained_snapshot_path)
    basis = load(receipt_root / f"{result_id}.checkpoint-basis.json")

    validate_terminal_review_result_v02(result)
    validate_native_publication_receipt(receipt, result)
    expected_range = result["journal_range"]
    observed_range = journal_range(
        root, expected_range["start_sequence"], expected_range["end_sequence"]
    )
    for key in ("start_sequence", "end_sequence", "record_count", "range_sha256"):
        if observed_range[key] != expected_range[key]:
            raise ValueError(f"{label}: journal range mismatch")
    if observed_range["records"][-1]["record_id"] != expected_range["closing_record_id"]:
        raise ValueError(f"{label}: journal closing record mismatch")
    if sha256(retained_snapshot_path) != receipt["snapshot_sha256"]:
        raise ValueError(f"{label}: retained snapshot digest mismatch")
    basis_body = {
        key: basis[key]
        for key in ("snapshot_schema", "logical_root", "native_state_revision", "members")
    }
    if basis["checkpoint_basis_sha256"] != digest(basis_body):
        raise ValueError(f"{label}: retained checkpoint basis mismatch")
    if not (
        result["post_checkpoint"]["checkpoint_basis_sha256"]
        == receipt["checkpoint_basis_sha256"]
        == basis["checkpoint_basis_sha256"]
    ):
        raise ValueError(f"{label}: result/receipt/basis join mismatch")
    if not (
        receipt["logical_workspace_root"]
        == retained_snapshot["logical_root"]
        == snapshot["logical_root"]
    ):
        raise ValueError(f"{label}: logical workspace identity mismatch")
    if result["run_id"] != state["run_id"]:
        raise ValueError(f"{label}: native run identity mismatch")

    ledger = state["spend_ledger"]["actions"]
    ledger_by_id = {item["action_id"]: item for item in ledger}
    dispositions = result["action_dispositions"]
    if [item["ordinal"] for item in dispositions] != list(
        range(1, len(dispositions) + 1)
    ):
        raise ValueError(f"{label}: terminal action ordinals are invalid")
    if {item["action_id"] for item in dispositions} != set(ledger_by_id):
        raise ValueError(f"{label}: terminal and ledger action inventories differ")
    for item in dispositions:
        action = ledger_by_id[item["action_id"]]
        if item["binding_sha256"] != _digest(_binding(action)):
            raise ValueError(f"{label}: terminal action binding mismatch")

    passes: list[dict[str, Any]] = []
    for pass_id, record in state["passes"].items():
        attempts = []
        for attempt in record["attempts"]:
            report = attempt.get("qa", {}).get("report") or {}
            attempts.append({
                "attempt": attempt["attempt_number"],
                "state": attempt["state"],
                "accepted": attempt.get("qa", {}).get("accepted"),
                "editorial_issue_codes": report.get("editorial_issue_codes") or [],
                "affected_claim_count": len(report.get("affected_claim_ids") or []),
                "paid_action_id": attempt.get("paid_action_id"),
                "provider_response_id": (attempt.get("provider_metadata") or {}).get(
                    "response_id"
                ),
            })
        passes.append({
            "pass_number": record["pass_number"],
            "state": record["state"],
            "accepted_attempt": record.get("accepted_attempt"),
            "accepted_workspace_present": bool(record.get("accepted_workspace")),
            "attempts": attempts,
        })

    return {
        "label": label,
        "native_run_id": state["run_id"],
        "native_status": state["status"],
        "state_revision": state["state_revision"],
        "result_id": result_id,
        "receipt_id": receipt["receipt_id"],
        "result_outcome": result["outcome"],
        "result_cause_code": result["cause_code"],
        "custody_finality": result["custody_finality"],
        "action_count": len(dispositions),
        "action_states": sorted({item["native_action_state"] for item in dispositions}),
        "new_provider_create_permitted": result["new_provider_create_permitted"],
        "snapshot_sha256": receipt["snapshot_sha256"],
        "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
        "publication_valid": True,
        "passes": sorted(passes, key=lambda item: item["pass_number"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case", action="append", nargs=3, metavar=("LABEL", "ROOT", "RESULT_ID"),
        required=True,
    )
    args = parser.parse_args()
    summaries = [summarize(label, Path(root).resolve(), result_id) for label, root, result_id in args.case]
    print(json.dumps({"cases": summaries}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
