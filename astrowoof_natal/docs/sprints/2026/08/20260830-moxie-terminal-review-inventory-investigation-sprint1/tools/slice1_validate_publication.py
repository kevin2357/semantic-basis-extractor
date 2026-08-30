"""Validate retained terminal-review evidence without invoking a native command."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sbe-source", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--result-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.sbe_source.resolve()))

    from astrowoof_natal_authoring.native_transitions import (
        journal_range,
        validate_native_publication_receipt,
    )
    from astrowoof_natal_authoring.terminal_review_contracts import (
        validate_terminal_review_result_v02,
    )

    root = args.workspace.resolve()
    result = json.loads(
        (root / "native-results" / f"{args.result_id}.json").read_text(encoding="utf-8")
    )
    receipt_root = root / "native-publication-receipts"
    receipt = json.loads(
        (receipt_root / f"{args.result_id}.json").read_text(encoding="utf-8")
    )
    validate_terminal_review_result_v02(result)
    validate_native_publication_receipt(receipt, result)
    expected_range = result["journal_range"]
    observed_range = journal_range(
        root, expected_range["start_sequence"], expected_range["end_sequence"]
    )
    for key in ("start_sequence", "end_sequence", "record_count", "range_sha256"):
        if observed_range[key] != expected_range[key]:
            raise ValueError("Journal range does not match terminal result")
    snapshot = receipt_root / f"{args.result_id}.workspace-snapshot.json"
    snapshot_sha = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    if snapshot_sha != receipt["snapshot_sha256"]:
        raise ValueError("Retained snapshot does not match receipt")
    basis = json.loads(
        (receipt_root / f"{args.result_id}.checkpoint-basis.json").read_text(
            encoding="utf-8"
        )
    )
    basis_sha = hashlib.sha256(canonical({
        key: basis[key]
        for key in ("snapshot_schema", "logical_root", "native_state_revision", "members")
    })).hexdigest()
    if (
        basis_sha != basis["checkpoint_basis_sha256"]
        or basis_sha != receipt["checkpoint_basis_sha256"]
        or basis_sha != result["post_checkpoint"]["checkpoint_basis_sha256"]
    ):
        raise ValueError("Checkpoint basis identity does not join result and receipt")
    output = {
        "schema_version": "astrowoof.investigation.retained_publication_validation.v1",
        "result_id": result["result_id"],
        "result_sha256": result["result_sha256"],
        "receipt_id": receipt["receipt_id"],
        "receipt_sha256": receipt["receipt_sha256"],
        "snapshot_sha256": snapshot_sha,
        "checkpoint_basis_sha256": basis_sha,
        "journal_range_sha256": observed_range["range_sha256"],
        "native_state_revision": result["post_checkpoint"]["native_state_revision"],
        "outcome": result["outcome"],
        "cause_code": result["cause_code"],
        "action_count": len(result["action_dispositions"]),
        "action_ids": [item["action_id"] for item in result["action_dispositions"]],
        "reconciliation_action_ids": result["reconciliation_action_ids"],
        "providerless_denial_action_ids": result["providerless_denial_action_ids"],
        "public_result_valid": True,
        "receipt_valid": True,
        "journal_range_valid": True,
        "retained_snapshot_valid": True,
        "checkpoint_basis_valid": True,
        "logical_root_relocation_note": (
            "Receipt retains the original Linux logical root; validation did not "
            "reinterpret the temporary Windows extraction path as native identity."
        ),
        "remote_operation_count": 0,
        "provider_operation_count": 0,
        "native_command_count": 0,
    }
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
