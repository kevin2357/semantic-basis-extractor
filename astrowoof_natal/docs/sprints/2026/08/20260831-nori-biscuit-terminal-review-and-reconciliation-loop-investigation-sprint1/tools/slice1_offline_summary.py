"""Print a sanitized, provider-free summary of one restored checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from astrowoof_natal_authoring.lifecycle import _local_dependencies
from astrowoof_natal_authoring.terminal_review_contracts import (
    validate_terminal_review_result_v02,
    validate_terminal_review_result_v02_against_receipt,
)
from astrowoof_natal_authoring.native_transitions import (
    journal_range, validate_native_publication_receipt,
)


def sha(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace.resolve()
    state = json.loads((root / "run.json").read_text(encoding="utf-8"))
    actions = (state.get("spend_ledger") or {}).get("actions") or []
    relevant = []
    for action in actions:
        binding = action.get("binding") or {}
        if action.get("state") == "REPORTED" and binding.get("stage") == "authoring_initial":
            continue
        response_path = root / "lifecycle" / "provider-reconciliation" / f"{action.get('action_id')}.response.json"
        response_identity = None
        if response_path.is_file():
            response = json.loads(response_path.read_text(encoding="utf-8"))
            response_identity = {"id": response.get("id"), "status": response.get("status")}
        relevant.append({
            "action_id": action.get("action_id"),
            "state": action.get("state"),
            "stage": binding.get("stage"),
            "route": binding.get("route"),
            "binding_run_id": binding.get("run_id"),
            "service_level": binding.get("service_level"),
            "binding_sha256": sha(binding),
            "provider_id": (action.get("provider") or {}).get("id"),
            "provider_kind": (action.get("provider") or {}).get("kind"),
            "reconciliation": action.get("provider_reconciliation"),
            "consumption_present": action.get("consumption") is not None,
            "reported_present": action.get("reported") is not None,
            "response_artifact": response_identity,
        })
    passes = []
    for record in (state.get("passes") or {}).values():
        attempts = []
        for attempt in record.get("attempts") or []:
            attempts.append({
                "attempt_number": attempt.get("attempt_number"),
                "state": attempt.get("state"),
                "paid_action_id": attempt.get("paid_action_id"),
                "provider_response_id": (attempt.get("provider_metadata") or {}).get("response_id"),
                "provider_response_status": (attempt.get("provider_metadata") or {}).get("response_status"),
                "qa_present": attempt.get("qa") is not None,
                "finished": attempt.get("finished_at") is not None,
                "error_type": (attempt.get("error") or {}).get("type"),
            })
        if any(item.get("attempt_number", 0) > 1 for item in attempts):
            passes.append({
                "pass_id": record.get("pass_id"), "state": record.get("state"),
                "accepted_attempt": record.get("accepted_attempt"), "attempts": attempts,
            })
    result_index = json.loads((root / "native-result-index.json").read_text(encoding="utf-8"))
    results = []
    for result_id in result_index["result_ids"]:
        result = json.loads((root / "native-results" / f"{result_id}.json").read_text(encoding="utf-8"))
        receipt = json.loads((root / "native-publication-receipts" / f"{result_id}.json").read_text(encoding="utf-8"))
        validate_native_publication_receipt(receipt, result)
        if result.get("schema_version") == "astrowoof.native_execution_result.v0.2":
            validate_terminal_review_result_v02(result)
            validate_terminal_review_result_v02_against_receipt(result, receipt)
        expected_range = result["journal_range"]
        observed_range = journal_range(
            root, expected_range["start_sequence"], expected_range["end_sequence"],
        )
        if any(
            expected_range[key] != observed_range[key]
            for key in ("start_sequence", "end_sequence", "record_count", "range_sha256")
        ):
            raise ValueError("Native result journal range does not join")
        retained_snapshot = root / "native-publication-receipts" / f"{result_id}.workspace-snapshot.json"
        retained_basis = root / "native-publication-receipts" / f"{result_id}.checkpoint-basis.json"
        if (
            hashlib.sha256(retained_snapshot.read_bytes()).hexdigest()
            != receipt["snapshot_sha256"]
            or not retained_basis.is_file()
        ):
            raise ValueError("Native result retained publication evidence does not join")
        results.append({
            "result_id": result_id, "invocation_id": result.get("invocation_id"),
            "schema_version": result.get("schema_version"),
            "command_kind": result.get("command_kind"), "outcome": result.get("outcome"),
            "cause_code": result.get("cause_code"),
            "revision": (result.get("post_checkpoint") or {}).get("native_state_revision"),
            "checkpoint_basis_sha256": (result.get("post_checkpoint") or {}).get("checkpoint_basis_sha256"),
            "custody_finality": result.get("custody_finality"),
            "reconciliation_action_ids": result.get("reconciliation_action_ids"),
            "receipt_id": receipt.get("receipt_id"),
        })
    subjects = []
    for subject, record in (state.get("subjects") or {}).items():
        subjects.append({
            "subject": subject, "state": record.get("state"),
            "polish_attempts": [{
                "attempt_number": item.get("attempt_number"), "state": item.get("state"),
                "paid_action_id": item.get("paid_action_id"),
                "provider_response_id": (item.get("provider_metadata") or {}).get("response_id"),
                "finished": item.get("finished_at") is not None,
            } for item in record.get("polish_attempts") or []],
        })
    output = {
        "run_id": state.get("run_id"), "status": state.get("status"),
        "state_revision": state.get("state_revision"),
        "workspace_logical_root": (state.get("workspace_contract") or {}).get("logical_root"),
        "action_count": len(actions), "relevant_actions": relevant,
        "retry_passes": passes, "subjects": subjects,
        "v2_intent": state.get("external_authority_v2_dispatch_intent"),
        "v2_history_count": len(state.get("external_authority_v2_dispatch_history") or []),
        "local_work_progress": state.get("local_work_progress"),
        "derived_local_dependencies": _local_dependencies(state),
        "results": results,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
