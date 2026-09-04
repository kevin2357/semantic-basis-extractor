"""Validate one downloaded checkpoint and summarize only approved JSON members.

This is an offline-only investigative tool.  It never restores or executes a
workspace, and emits no deck, prompt, generated prose, or protected fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha(value: object) -> str:
    encoded = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    return sha256_bytes(encoded)


def json_member(bundle: zipfile.ZipFile, declared: dict[str, dict[str, Any]], path: str) -> dict[str, Any]:
    item = declared.get(path)
    if not isinstance(item, dict):
        raise ValueError(f"approved member absent from signed inventory: {path}")
    raw = bundle.read(f"workspace/{path}")
    if len(raw) != item.get("byte_size") or sha256_bytes(raw) != item.get("sha256"):
        raise ValueError(f"approved member does not match signed inventory: {path}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f"approved JSON member is not an object: {path}")
    return value


def string_list(value: object) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return []
    return sorted(set(value))


def error_summary(report: dict[str, Any]) -> dict[str, Any]:
    errors = report.get("errors")
    if not isinstance(errors, list):
        errors = []
    encoded = [str(item).encode("utf-8") for item in errors]
    categories = []
    for item in errors:
        message = str(item)
        if re.fullmatch(
            r"Selected aspects and syntheses together must use three or four theme groups; found \d+\.",
            message,
        ):
            categories.append("theme_group_cardinality")
        else:
            categories.append("unclassified_validation_error")
    return {
        "error_categories": sorted(set(categories)),
        "status": report.get("status"),
        "error_count": len(errors),
        "error_sha256": [sha256_bytes(item) for item in encoded],
        "schema_version": report.get("schema_version"),
    }


def lint_summary(report: dict[str, Any]) -> dict[str, Any]:
    warnings = []
    for deck in report.get("decks") if isinstance(report.get("decks"), list) else []:
        if isinstance(deck, dict) and isinstance(deck.get("warnings"), list):
            warnings.extend(deck["warnings"])
    if isinstance(report.get("cross_subject_warnings"), list):
        warnings.extend(report["cross_subject_warnings"])
    codes = sorted({item.get("code") for item in warnings if isinstance(item, dict) and isinstance(item.get("code"), str)})
    return {"status": report.get("status"), "warning_count": len(warnings), "warning_codes": codes, "schema_version": report.get("schema_version")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--generation", type=int, required=True)
    parser.add_argument("--native-run-id", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if sha256_bytes(args.archive.read_bytes()) != args.archive_sha256:
        raise ValueError("archive digest mismatch")
    acceptance = [f"passes/{args.subject}_{number}/attempt-001/authoring-pass-acceptance.json" for number in range(1, 7)]
    approved = [
        "workspace-snapshot.json",
        f"final/{args.subject}/polish/attempt-001/validation-report.json",
        f"final/{args.subject}/polish/attempt-001/lint-report.json",
        *acceptance,
    ]
    with zipfile.ZipFile(args.archive) as bundle:
        entries = bundle.infolist()
        names = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or not path.parts or entry.filename in names:
                raise ValueError("unsafe or duplicate archive member")
            names.add(entry.filename)
        manifest = json.loads(bundle.read("checkpoint-manifest.json"))
        members = manifest.get("members")
        if (
            manifest.get("schema_version") != "astrowoof.checkpoint-archive.v1"
            or manifest.get("checkpoint_contract") != "astrowoof.sbe-workspace-checkpoint.v1"
            or manifest.get("generation") != args.generation
            or manifest.get("inventory_sha256") != args.inventory_sha256
            or canonical_sha(members) != args.inventory_sha256
            or not isinstance(members, list)
        ):
            raise ValueError("checkpoint manifest identity mismatch")
        declared = {item.get("path"): item for item in members if isinstance(item, dict) and isinstance(item.get("path"), str)}
        expected_names = {"workspace/" + path for path in declared} | {"checkpoint-manifest.json"}
        actual_files = {entry.filename for entry in entries if not entry.is_dir()}
        if actual_files != expected_names or len(declared) != len(members):
            raise ValueError("archive member inventory mismatch")
        snapshot = json_member(bundle, declared, "workspace-snapshot.json")
        validation = json_member(bundle, declared, approved[1])
        lint = json_member(bundle, declared, approved[2])
        acceptance_reports = [json_member(bundle, declared, path) for path in acceptance]

    actions = ((snapshot.get("spend_ledger") or {}).get("actions") or [])
    polish_actions = [item for item in actions if isinstance(item, dict) and ((item.get("binding") or {}).get("stage") == "polish")]
    output = {
        "schema_version": "astrowoof.investigation.selective_checkpoint_summary.v1",
        "archive_sha256": args.archive_sha256,
        "inventory_sha256": args.inventory_sha256,
        "checkpoint_generation": args.generation,
        "native_run_id": args.native_run_id,
        "snapshot_join": {
            "logical_root": snapshot.get("logical_root"),
            "member_count": len(snapshot.get("members")) if isinstance(snapshot.get("members"), list) else None,
            "schema_version": snapshot.get("schema_version"),
            "state_fields_present": any(key in snapshot for key in ("run_id", "state_revision", "status", "spend_ledger")),
            "note": "The snapshot is an inventory manifest, not the native run-state document; archive and packet identity bind it to the named run.",
        },
        "post_polish_validation": error_summary(validation),
        "post_polish_lint": lint_summary(lint),
        "authoring_acceptance": [
            {
                "status": report.get("status"),
                "editorial_issue_codes": string_list(report.get("editorial_issue_codes")),
                "advisory_issue_codes": string_list(report.get("advisory_issue_codes")),
                "schema_version": report.get("schema_version"),
            }
            for report in acceptance_reports
        ],
        "provider_operation_count": 0,
        "workspace_execution_count": 0,
        "workspace_mutation_count": 0,
    }
    args.output.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
