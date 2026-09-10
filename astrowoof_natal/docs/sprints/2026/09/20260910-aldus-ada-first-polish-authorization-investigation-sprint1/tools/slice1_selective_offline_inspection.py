"""Validate and summarize the two authorized first-polish checkpoints offline."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha(value: object) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(raw)


def canonical_line_sha(value: object) -> str:
    raw = (
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        + "\n"
    ).encode("utf-8")
    return sha256_bytes(raw)


def read_declared_json(
    bundle: zipfile.ZipFile,
    declared: dict[str, dict[str, Any]],
    path: str,
) -> dict[str, Any]:
    item = declared.get(path)
    if not isinstance(item, dict):
        raise ValueError(f"Required member is absent from inventory: {path}")
    raw = bundle.read("workspace/" + path)
    if len(raw) != item.get("byte_size") or sha256_bytes(raw) != item.get("sha256"):
        raise ValueError(f"Required member identity mismatch: {path}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f"Required member is not a JSON object: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--generation", type=int, required=True)
    parser.add_argument("--native-run-id", required=True)
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--result-id", required=True)
    parser.add_argument("--receipt-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if sha256_bytes(args.archive.read_bytes()) != args.archive_sha256:
        raise ValueError("Archive digest mismatch")

    with zipfile.ZipFile(args.archive) as bundle:
        entries = bundle.infolist()
        names: set[str] = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or entry.filename in names:
                raise ValueError("Unsafe or duplicate archive member")
            names.add(entry.filename)

        manifest = json.loads(bundle.read("checkpoint-manifest.json"))
        members = manifest.get("members")
        if not isinstance(members, list):
            raise ValueError("Checkpoint member inventory is absent")
        if (
            manifest.get("schema_version") != "astrowoof.checkpoint-archive.v1"
            or manifest.get("checkpoint_contract")
            != "astrowoof.sbe-workspace-checkpoint.v1"
            or manifest.get("generation") != args.generation
            or manifest.get("inventory_sha256") != args.inventory_sha256
            or canonical_line_sha(members) != args.inventory_sha256
        ):
            raise ValueError("Checkpoint manifest identity mismatch")

        declared = {
            item.get("path"): item
            for item in members
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        actual = {entry.filename for entry in entries if not entry.is_dir()}
        expected = {"workspace/" + path for path in declared} | {
            "checkpoint-manifest.json"
        }
        if actual != expected or len(declared) != len(members):
            raise ValueError("Archive member inventory mismatch")

        # Verify every archived member before selectively interpreting any of it.
        for path, item in declared.items():
            raw = bundle.read("workspace/" + path)
            if len(raw) != item.get("byte_size") or sha256_bytes(raw) != item.get("sha256"):
                raise ValueError(f"Archived member identity mismatch: {path}")

        run = read_declared_json(bundle, declared, "run.json")
        requests = read_declared_json(
            bundle, declared, "spend-authorization-requests.json"
        )
        result = read_declared_json(
            bundle, declared, f"native-results/{args.result_id}.json"
        )
        receipt = read_declared_json(
            bundle,
            declared,
            f"native-publication-receipts/{args.result_id}.json",
        )

    actions = (run.get("spend_ledger") or {}).get("actions") or []
    action = next(
        (item for item in actions if item.get("action_id") == args.action_id), None
    )
    request = next(
        (
            item
            for item in requests.get("actions") or []
            if item.get("action_id") == args.action_id
        ),
        None,
    )
    disposition = next(
        (
            item
            for item in result.get("action_dispositions") or []
            if item.get("action_id") == args.action_id
        ),
        None,
    )
    if not isinstance(action, dict) or not isinstance(request, dict):
        raise ValueError("Named polish action/request is absent")
    if action.get("binding") != request.get("binding"):
        raise ValueError("Authorization request does not exactly match ledger binding")
    if (
        run.get("run_id") != args.native_run_id
        or requests.get("run_id") != args.native_run_id
        or result.get("run_id") != args.native_run_id
        or receipt.get("run_id") != args.native_run_id
        or result.get("result_id") != args.result_id
        or receipt.get("result_id") != args.result_id
        or receipt.get("receipt_id") != args.receipt_id
        or receipt.get("result_sha256") != result.get("result_sha256")
        or receipt.get("invocation_id") != result.get("invocation_id")
    ):
        raise ValueError("Run/result/receipt/request identity join failed")

    binding = action["binding"]
    terminal_binding = {
        "action_id": args.action_id,
        "stage": binding.get("stage"),
        "route": binding.get("route"),
        "request_sha256": binding.get("request_sha256"),
        "profile_sha256": binding.get("profile_sha256"),
        "maximum_output_tokens": binding.get("maximum_output_tokens"),
        "commitment_micro_usd": binding.get("commitment_micro_usd"),
        "price_book_version": binding.get("price_book_version"),
    }
    summary = {
        "schema_version": "astrowoof.first_polish_authority_inspection.v1",
        "archive_sha256": args.archive_sha256,
        "inventory_sha256": args.inventory_sha256,
        "checkpoint_generation": args.generation,
        "archive_member_count": len(declared),
        "archive_safety_valid": True,
        "all_member_identities_valid": True,
        "native_run_id": args.native_run_id,
        "native_state": {
            "status": run.get("status"),
            "state_revision": run.get("state_revision"),
        },
        "polish_action": {
            "action_id": args.action_id,
            "state": action.get("state"),
            "stage": binding.get("stage"),
            "route": binding.get("route"),
            "subject_id": str(binding.get("route", "")).split(":", 1)[0],
            "request_sha256": binding.get("request_sha256"),
            "request_payload_artifact": action.get("request_payload_artifact"),
            "authorization_present": isinstance(action.get("authorization"), dict),
            "provider_present": isinstance(action.get("provider"), dict),
            "reported_present": isinstance(action.get("reported"), dict),
            "exact_request_sidecar_present": True,
            "request_sidecar_state_revision": requests.get("state_revision"),
            "sidecar_binding_matches_ledger": True,
            "terminal_binding_sha256": canonical_sha(terminal_binding),
        },
        "publication": {
            "schema_version": result.get("schema_version"),
            "command_kind": result.get("command_kind"),
            "outcome": result.get("outcome"),
            "cause_code": result.get("cause_code"),
            "result_id": result.get("result_id"),
            "result_sha256": result.get("result_sha256"),
            "receipt_id": receipt.get("receipt_id"),
            "receipt_sha256": receipt.get("receipt_sha256"),
            "invocation_id": result.get("invocation_id"),
            "polish_action_in_result": args.action_id
            in (result.get("action_ids") or []),
            "polish_disposition": disposition,
            "custody_finality": result.get("custody_finality"),
            "providerless_denial_action_ids": result.get(
                "providerless_denial_action_ids"
            ),
        },
        "provider_operation_count": 0,
        "workspace_execution_count": 0,
        "workspace_mutation_count": 0,
    }
    args.output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
