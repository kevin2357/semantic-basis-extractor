"""Perform one authorized HEAD and one ETag-bound ranged GET per exact manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import boto3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(65536):
            digest.update(chunk)
    return digest.hexdigest()


def require(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} missing")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "astrowoof.investigation.r2_access_manifest.v1":
        raise ValueError("manifest schema unsupported")
    if manifest.get("approved_operations") != {
        "head_count": 1, "get_count": 1, "list_count": 0,
        "write_count": 0, "delete_count": 0,
    }:
        raise ValueError("operation budget not closed")
    key = require(manifest.get("object_key"), "object key")
    object_uuid = require(manifest.get("object_uuid"), "object UUID")
    if key != "v1/checkpoint/" + object_uuid.replace("-", "").lower():
        raise ValueError("object identity mismatch")
    if re.fullmatch(r"v1/checkpoint/[0-9a-f]{32}", key) is None:
        raise ValueError("object key not canonical")

    names = (
        "ASTROWOOF_R2_ENDPOINT_URL", "ASTROWOOF_R2_BUCKET",
        "ASTROWOOF_R2_ACCESS_KEY_ID", "ASTROWOOF_R2_SECRET_ACCESS_KEY",
    )
    values = {name: require(os.environ.get(name), name) for name in names}
    client = boto3.client(
        "s3", endpoint_url=values[names[0]], region_name="auto",
        aws_access_key_id=values[names[2]],
        aws_secret_access_key=values[names[3]],
    )
    head = client.head_object(Bucket=values[names[1]], Key=key)
    etag = require(head.get("ETag"), "HEAD ETag")
    expected = manifest["expected_archive_bytes"]
    if head.get("ContentLength") != expected:
        raise ValueError("HEAD content length mismatch")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    response = client.get_object(
        Bucket=values[names[1]], Key=key, IfMatch=etag,
        Range=f"bytes=0-{expected - 1}",
    )
    body = response["Body"]
    digest = hashlib.sha256()
    count = 0
    try:
        with args.output.open("xb") as output:
            while chunk := body.read(65536):
                count += len(chunk)
                if count > expected:
                    raise ValueError("GET exceeded bound")
                digest.update(chunk)
                output.write(chunk)
    finally:
        body.close()
    observed = digest.hexdigest()
    if count != expected or observed != manifest["expected_archive_sha256"]:
        args.output.unlink(missing_ok=True)
        raise ValueError("GET archive identity mismatch")
    receipt = {
        "schema_version": "astrowoof.investigation.r2_read_only_access_receipt.v1",
        "label": manifest["label"],
        "manifest_sha256": sha256(args.manifest),
        "archive_bytes": count,
        "archive_sha256": observed,
        "inventory_sha256": manifest["expected_inventory_sha256"],
        "etag_sha256": hashlib.sha256(etag.strip('"').encode()).hexdigest(),
        "provider_operation_counts": {
            "head": 1, "get": 1, "list": 0, "write": 0, "delete": 0,
        },
    }
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
