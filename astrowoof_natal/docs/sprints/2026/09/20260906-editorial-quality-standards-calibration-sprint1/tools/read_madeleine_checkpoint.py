"""Perform the single authorized Madeleine HEAD and conditional bounded GET."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import boto3


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} is missing")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    parser.add_argument("--output-receipt", type=Path, required=True)
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
    if key != "v1/checkpoint/" + object_uuid.replace("-", "").lower() or re.fullmatch(
        r"v1/checkpoint/[0-9a-f]{32}", key
    ) is None:
        raise ValueError("object identity is not canonical")

    names = (
        "ASTROWOOF_R2_ENDPOINT_URL", "ASTROWOOF_R2_BUCKET",
        "ASTROWOOF_R2_ACCESS_KEY_ID", "ASTROWOOF_R2_SECRET_ACCESS_KEY",
    )
    values = {name: required_text(os.environ.get(name), name) for name in names}
    client = boto3.client(
        "s3", endpoint_url=values[names[0]],
        aws_access_key_id=values[names[2]],
        aws_secret_access_key=values[names[3]], region_name="auto",
    )

    head = client.head_object(Bucket=values[names[1]], Key=key)
    expected_etag = manifest["expected_etag"]
    observed_etag = str(head.get("VersionId") or head.get("ETag") or "").strip('"')
    metadata = {str(k).lower(): str(v) for k, v in (head.get("Metadata") or {}).items()}
    expected_metadata = {
        "aw-contract": manifest["storage_receipt_contract"],
        "aw-protection": manifest["expected_protection"],
    }
    if (
        observed_etag != expected_etag
        or head.get("ContentLength") != manifest["expected_archive_bytes"]
        or head.get("ContentType") != manifest["expected_media_type"]
        or any(metadata.get(k) != v for k, v in expected_metadata.items())
    ):
        raise ValueError("HEAD identity or protection metadata mismatch")

    args.output_archive.parent.mkdir(parents=True, exist_ok=True)
    response = client.get_object(Bucket=values[names[1]], Key=key, IfMatch=str(head["ETag"]))
    body = response["Body"]
    digest = hashlib.sha256()
    observed_bytes = 0
    try:
        with args.output_archive.open("xb") as handle:
            while chunk := body.read(64 * 1024):
                observed_bytes += len(chunk)
                if observed_bytes > manifest["expected_archive_bytes"]:
                    raise ValueError("GET exceeded bounded byte count")
                digest.update(chunk)
                handle.write(chunk)
    finally:
        body.close()
    observed_sha = digest.hexdigest()
    if observed_bytes != manifest["expected_archive_bytes"] or observed_sha != manifest["expected_archive_sha256"]:
        args.output_archive.unlink(missing_ok=True)
        raise ValueError("downloaded archive identity mismatch")

    receipt = {
        "schema_version": "astrowoof.investigation.r2_read_only_access_receipt.v1",
        "access_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "api_run_id": manifest["api_run_id"],
        "native_run_id": manifest["native_run_id"],
        "checkpoint_id": manifest["checkpoint_id"],
        "checkpoint_generation": manifest["checkpoint_generation"],
        "object_key": key,
        "etag": observed_etag,
        "archive_bytes": observed_bytes,
        "archive_sha256": observed_sha,
        "inventory_sha256": manifest["expected_inventory_sha256"],
        "media_type": head["ContentType"],
        "protection": metadata["aw-protection"],
        "provider_operation_counts": {"head": 1, "get": 1, "list": 0, "write": 0, "delete": 0},
        "workspace_execution_count": 0,
        "workspace_mutation_count": 0,
    }
    args.output_receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
