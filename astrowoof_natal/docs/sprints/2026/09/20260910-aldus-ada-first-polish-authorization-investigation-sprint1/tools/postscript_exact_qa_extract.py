"""Perform one authorized checkpoint read and extract exact pre-polish QA material."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

import boto3


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_line_sha(value: object) -> str:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return sha256(raw)


def required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} is missing")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest_bytes = args.manifest.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema_version") != "astrowoof.investigation.r2_access_manifest.v1":
        raise ValueError("unsupported access manifest")
    if manifest.get("approved_operations") != {
        "head_count": 1, "get_count": 1, "list_count": 0,
        "write_count": 0, "delete_count": 0,
    }:
        raise ValueError("access operation budget is not closed")
    key = required_text(manifest.get("object_key"), "object key")
    object_uuid = required_text(manifest.get("object_uuid"), "object UUID")
    if key != "v1/checkpoint/" + object_uuid.replace("-", "").lower() or re.fullmatch(r"v1/checkpoint/[0-9a-f]{32}", key) is None:
        raise ValueError("object identity is not canonical")

    names = (
        "ASTROWOOF_R2_ENDPOINT_URL", "ASTROWOOF_R2_BUCKET",
        "ASTROWOOF_R2_ACCESS_KEY_ID", "ASTROWOOF_R2_SECRET_ACCESS_KEY",
    )
    values = {name: required_text(os.environ.get(name), name) for name in names}
    if values[names[1]] != "astrowoof-qa-artifacts":
        raise ValueError("unexpected bucket")
    client = boto3.client(
        "s3", endpoint_url=values[names[0]], aws_access_key_id=values[names[2]],
        aws_secret_access_key=values[names[3]], region_name="auto",
    )

    expected_etag = required_text(manifest.get("expected_etag"), "expected ETag")
    head = client.head_object(Bucket=values[names[1]], Key=key, IfMatch=expected_etag)
    observed_etag = str(head.get("ETag") or "").strip('"')
    if observed_etag != expected_etag or head.get("ContentLength") != manifest["expected_archive_bytes"]:
        raise ValueError("HEAD identity mismatch")

    response = client.get_object(Bucket=values[names[1]], Key=key, IfMatch=expected_etag)
    body = response["Body"]
    try:
        archive = body.read(manifest["expected_archive_bytes"] + 1)
    finally:
        body.close()
    if len(archive) != manifest["expected_archive_bytes"] or sha256(archive) != manifest["expected_archive_sha256"]:
        raise ValueError("bounded GET archive identity mismatch")

    args.output_dir.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(Path(args.output_dir, "_download.zip"), mode="w") as temporary:
        pass
    Path(args.output_dir, "_download.zip").unlink()
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(archive)) as bundle:
        entries = bundle.infolist()
        names_seen: set[str] = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or entry.filename in names_seen:
                raise ValueError("unsafe or duplicate archive member")
            names_seen.add(entry.filename)
        archive_manifest = json.loads(bundle.read("checkpoint-manifest.json"))
        members = archive_manifest.get("members")
        if not isinstance(members, list) or archive_manifest.get("generation") != manifest["checkpoint_generation"]:
            raise ValueError("checkpoint manifest mismatch")
        if archive_manifest.get("inventory_sha256") != manifest["expected_inventory_sha256"] or canonical_line_sha(members) != manifest["expected_inventory_sha256"]:
            raise ValueError("checkpoint inventory identity mismatch")
        declared = {item.get("path"): item for item in members if isinstance(item, dict) and isinstance(item.get("path"), str)}
        actual = {entry.filename for entry in entries if not entry.is_dir()}
        if actual != {"workspace/" + path for path in declared} | {"checkpoint-manifest.json"} or len(declared) != len(members):
            raise ValueError("archive inventory mismatch")
        for path, item in declared.items():
            raw = bundle.read("workspace/" + path)
            if len(raw) != item.get("byte_size") or sha256(raw) != item.get("sha256"):
                raise ValueError(f"member identity mismatch: {path}")

        suffixes = (".initial-assembled-deck.json", ".validation-report.json", ".lint-report.json")
        selected = {suffix: [path for path in declared if path.startswith("final/") and path.endswith(suffix)] for suffix in suffixes}
        if any(len(paths) != 1 for paths in selected.values()):
            raise ValueError(f"expected exactly one requested artifact per kind: {selected}")
        output_files = []
        for suffix, paths in selected.items():
            source = paths[0]
            raw = bundle.read("workspace/" + source)
            destination = args.output_dir / source.rsplit("/", 1)[-1]
            destination.write_bytes(raw)
            output_files.append({"kind": suffix[1:-5], "source_path": source, "output_path": str(destination), "bytes": len(raw), "sha256": sha256(raw)})

    receipt = {
        "schema_version": "astrowoof.investigation.qa_material_extract_receipt.v1",
        "label": manifest.get("label"), "api_run_id": manifest["api_run_id"],
        "native_run_id": manifest["native_run_id"], "checkpoint_id": manifest["checkpoint_id"],
        "checkpoint_generation": manifest["checkpoint_generation"], "object_key": key,
        "etag": observed_etag, "archive_bytes": len(archive), "archive_sha256": sha256(archive),
        "inventory_sha256": manifest["expected_inventory_sha256"], "all_member_identities_valid": True,
        "provider_operation_counts": {"head": 1, "get": 1, "list": 0, "write": 0, "delete": 0},
        "workspace_execution_count": 0, "workspace_mutation_count": 0, "files": output_files,
    }
    receipt_path = args.output_dir / "read-and-extract-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
