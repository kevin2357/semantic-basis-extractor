"""Emit a bounded digest/join comparison for one verified terminal workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from astrowoof_natal_authoring.editorial_review_runtime import (
    _load,
    _logical_path,
    collect_editorial_review_runtime_evidence,
)
from astrowoof_natal_authoring.editorial_review_contracts import editorial_review_sha256
from astrowoof_natal_authoring.native_transitions import read_native_transition_result
from astrowoof_natal_authoring.terminal_review_contracts import _binding, _digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("result_id")
    args = parser.parse_args()

    root = args.root.resolve()
    view = read_native_transition_result(root, args.result_id)
    state = json.loads((root / "run.json").read_text(encoding="utf-8"))
    result = view["result"]
    receipt = view["receipt"]
    actions = (state.get("spend_ledger") or {}).get("actions") or []
    dispositions = result.get("action_dispositions") or []
    disposition_by_id = {row["action_id"]: row for row in dispositions}
    subject = next(iter((state.get("subjects") or {}).values()))
    logical_root = receipt["logical_workspace_root"]
    initial_ref = subject.get("initial_assembled_deck")
    initial_digest = subject.get("initial_assembled_deck_sha256")
    initial_digest_matches = None
    if isinstance(initial_ref, str) and isinstance(initial_digest, str):
        initial_path = _logical_path(root, logical_root, initial_ref)
        initial_digest_matches = (
            initial_path.is_file()
            and editorial_review_sha256(_load(initial_path)) == initial_digest
        )

    comparisons = []
    for action in actions:
        action_id = action["action_id"]
        disposition = disposition_by_id.get(action_id)
        sealed = disposition.get("binding_sha256") if disposition else None
        projected = _digest(_binding(action))
        complete = _digest(action["binding"])
        comparisons.append({
            "action_id": action_id,
            "binding_extra_keys": sorted(set(action["binding"]) - set(_binding(action))),
            "sealed_binding_sha256": sealed,
            "projected_binding_sha256": projected,
            "complete_binding_sha256": complete,
            "sealed_matches_projected": sealed == projected,
            "sealed_matches_complete": sealed == complete,
        })

    branch, capture = collect_editorial_review_runtime_evidence(root, args.result_id)
    post_checkpoint = result.get("post_checkpoint") or {}
    provenance = state.get("provenance") or {}
    output = {
        "native_run_id": state.get("run_id"),
        "result_id": result.get("result_id"),
        "receipt_id": receipt.get("receipt_id"),
        "result_schema": result.get("schema_version"),
        "result_outcome": result.get("outcome"),
        "public_capture_branch": branch,
        "public_capture_reason": capture.get("reason") if branch == "unsupported" else None,
        "top_level_joins": {
            "result_receipt_run": result.get("run_id") == receipt.get("run_id") == state.get("run_id"),
            "state_revision": state.get("state_revision") == post_checkpoint.get("native_state_revision"),
            "checkpoint_basis": post_checkpoint.get("checkpoint_basis_sha256") == receipt.get("checkpoint_basis_sha256"),
            "release": result.get("sbe_release") == (provenance.get("runtime") or {}).get("version"),
        },
        "ledger_action_count": len(actions),
        "disposition_count": len(dispositions),
        "action_ids_exact": {row["action_id"] for row in dispositions} == {row["action_id"] for row in actions},
        "initial_assembled_deck_digest_matches": initial_digest_matches,
        "all_sealed_match_projected": all(row["sealed_matches_projected"] for row in comparisons),
        "all_sealed_match_complete": all(row["sealed_matches_complete"] for row in comparisons),
        "comparisons": comparisons,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
