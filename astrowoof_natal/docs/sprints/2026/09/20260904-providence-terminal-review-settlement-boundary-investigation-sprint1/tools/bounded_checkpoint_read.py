"""Perform the one authorized HEAD and conditional GET for Providence generation 12."""

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
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    parser.add_argument("--output-receipt", type=Path, required=True)
    args = parser.parse_args()

    if file_sha256(args.manifest) != args.manifest_sha256:
        raise ValueError("Access manifest digest mismatch")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "astrowoof.investigation.r2_access_manifest.v1":
        raise ValueError("Access manifest schema is unsupported")
    key = required_text(manifest.get("object_key"), "object key")
    object_uuid = required_text(manifest.get("object_uuid"), "object UUID")
    if key != "v1/checkpoint/" + object_uuid.replace("-", "").lower():
        raise ValueError("Object key does not join frozen UUID")
    if re.fullmatch(r"v1/checkpoint/[0-9a-f]{32}", key) is None:
        raise ValueError("Object key is not canonical")
    if manifest.get("approved_operations") != {
        "head_count": 1,
        "get_count": 1,
        "list_count": 0,
        "write_count": 0,
        "delete_count": 0,
    }:
        raise ValueError("Access operation budget is not closed")

    names = (
        "ASTROWOOF_R2_ENDPOINT_URL",
        "ASTROWOOF_R2_BUCKET",
        "ASTROWOOF_R2_ACCESS_KEY_ID",
        "ASTROWOOF_R2_SECRET_ACCESS_KEY",
    )
    values = {name: required_text(os.environ.get(name), name) for name in names}
    if values["ASTROWOOF_R2_BUCKET"] != "astrowoof-qa-artifacts":
        raise ValueError("Configured R2 bucket does not match the coordinate packet")
    client = boto3.client(
        "s3",
        endpoint_url=values[names[0]],
        aws_access_key_id=values[names[2]],
        aws_secret_access_key=values[names[3]],
        region_name="auto",
    )
    expected_etag = required_text(manifest.get("expected_etag"), "expected ETag")
    head = client.head_object(Bucket=values[names[1]], Key=key)
    observed_etag = str(head.get("VersionId") or head.get("ETag") or "").strip('"')
    if observed_etag != expected_etag.strip('"'):
        raise ValueError("R2 ETag/version does not match frozen manifest")
    if head.get("ContentLength") != manifest.get("expected_archive_bytes"):
        raise ValueError("R2 content length does not match frozen manifest")

    args.output_archive.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    observed_bytes = 0
    response = client.get_object(
        Bucket=values[names[1]], Key=key, IfMatch=str(head.get("ETag") or "")
    )
    get_etag = str(response.get("VersionId") or response.get("ETag") or "").strip('"')
    if get_etag != observed_etag:
        response["Body"].close()
        raise ValueError("Conditional GET identity changed after HEAD")
    if response.get("ContentLength") != manifest.get("expected_archive_bytes"):
        response["Body"].close()
        raise ValueError("GET content length does not match frozen manifest")
    body = response["Body"]
    try:
        with args.output_archive.open("xb") as handle:
            while chunk := body.read(64 * 1024):
                observed_bytes += len(chunk)
                if observed_bytes > manifest["expected_archive_bytes"]:
                    raise ValueError("R2 object exceeded frozen size")
                digest.update(chunk)
                handle.write(chunk)
    finally:
        body.close()
    observed_sha256 = digest.hexdigest()
    if (
        observed_bytes != manifest["expected_archive_bytes"]
        or observed_sha256 != manifest["expected_archive_sha256"]
    ):
        args.output_archive.unlink(missing_ok=True)
        raise ValueError("Downloaded checkpoint identity mismatch")
    receipt = {
        "schema_version": "astrowoof.investigation.r2_read_only_access_receipt.v1",
        "manifest_sha256": args.manifest_sha256,
        "label": manifest["label"],
        "api_run_id": manifest["api_run_id"],
        "native_run_id": manifest["native_run_id"],
        "checkpoint_id": manifest["checkpoint_id"],
        "checkpoint_generation": manifest["checkpoint_generation"],
        "object_key": key,
        "archive_sha256": observed_sha256,
        "archive_bytes": observed_bytes,
        "inventory_sha256": manifest["expected_inventory_sha256"],
        "provider_operation_counts": {
            "head": 1,
            "get": 1,
            "list": 0,
            "write": 0,
            "delete": 0,
        },
        "workspace_execution_count": 0,
        "workspace_mutation_count": 0,
    }
    args.output_receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
