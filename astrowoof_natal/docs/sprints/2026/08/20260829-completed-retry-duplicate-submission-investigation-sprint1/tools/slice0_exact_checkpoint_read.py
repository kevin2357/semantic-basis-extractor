"""Perform one frozen R2 checkpoint HEAD and one validated streaming GET.

This incident-only tool deliberately exposes no list, write, copy, delete, provider,
or SBE runtime operation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import boto3


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(64 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} is missing")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coordinates", type=Path, required=True)
    parser.add_argument("--coordinates-sha256", required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    parser.add_argument("--output-receipt", type=Path, required=True)
    args = parser.parse_args()

    if sha256_file(args.coordinates) != args.coordinates_sha256:
        raise ValueError("Coordinate packet digest mismatch")
    document = json.loads(args.coordinates.read_text(encoding="utf-8"))
    checkpoint = document["active_sbe_checkpoint"]
    key = require_text(checkpoint.get("storage_object_key"), "object key")
    object_uuid = require_text(checkpoint.get("storage_object_uuid"), "object UUID")
    expected_key = "v1/checkpoint/" + object_uuid.replace("-", "").lower()
    if key != expected_key or re.fullmatch(r"v1/checkpoint/[0-9a-f]{32}", key) is None:
        raise ValueError("Frozen checkpoint key is not canonical")

    names = (
        "ASTROWOOF_R2_ENDPOINT_URL",
        "ASTROWOOF_R2_BUCKET",
        "ASTROWOOF_R2_ACCESS_KEY_ID",
        "ASTROWOOF_R2_SECRET_ACCESS_KEY",
    )
    values = {name: require_text(os.environ.get(name), name) for name in names}
    client = boto3.client(
        "s3",
        endpoint_url=values["ASTROWOOF_R2_ENDPOINT_URL"],
        aws_access_key_id=values["ASTROWOOF_R2_ACCESS_KEY_ID"],
        aws_secret_access_key=values["ASTROWOOF_R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    bucket = values["ASTROWOOF_R2_BUCKET"]

    # Authorized remote operation 1/2: one exact HEAD.
    head = client.head_object(Bucket=bucket, Key=key)
    metadata = {str(k).lower(): str(v) for k, v in (head.get("Metadata") or {}).items()}
    expected_metadata = {
        "aw-contract": require_text(checkpoint.get("storage_contract_version"), "contract"),
        "aw-sha256": require_text(checkpoint.get("archive_sha256"), "archive digest"),
        "aw-size": str(checkpoint.get("archive_byte_size")),
        "aw-media-type": require_text(checkpoint.get("media_type"), "media type"),
        "aw-protection": require_text(checkpoint.get("protection_class"), "protection"),
        "aw-created-at": require_text(checkpoint.get("storage_created_at"), "created at"),
    }
    if metadata != expected_metadata:
        raise ValueError("R2 HEAD metadata does not match frozen coordinates")
    if (
        head.get("ContentLength") != checkpoint["archive_byte_size"]
        or head.get("ContentType") != checkpoint["media_type"]
    ):
        raise ValueError("R2 HEAD content identity does not match frozen coordinates")
    observed_version = str(head.get("VersionId") or head.get("ETag") or "").strip('"')
    if observed_version != checkpoint["provider_version_or_etag"]:
        raise ValueError("R2 provider version/ETag does not match frozen coordinates")

    args.output_archive.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    observed_bytes = 0
    # Authorized remote operation 2/2: one exact GET.
    response = client.get_object(Bucket=bucket, Key=key)
    body = response["Body"]
    try:
        with args.output_archive.open("xb") as handle:
            while chunk := body.read(64 * 1024):
                observed_bytes += len(chunk)
                if observed_bytes > checkpoint["archive_byte_size"]:
                    raise ValueError("R2 object exceeded frozen byte size")
                digest.update(chunk)
                handle.write(chunk)
    finally:
        body.close()
    observed_sha256 = digest.hexdigest()
    if (
        observed_bytes != checkpoint["archive_byte_size"]
        or observed_sha256 != checkpoint["archive_sha256"]
    ):
        args.output_archive.unlink(missing_ok=True)
        raise ValueError("Downloaded checkpoint bytes do not match frozen coordinates")

    receipt = {
        "schema_version": "astrowoof.sbe_slice0_read_only_access.v1",
        "coordinate_packet_sha256": args.coordinates_sha256,
        "api_run_id": document["incident"]["api_run_id"],
        "native_run_id": document["incident"]["native_run_id"],
        "checkpoint_id": checkpoint["checkpoint_id"],
        "generation": checkpoint["generation"],
        "object_key": key,
        "archive_sha256": observed_sha256,
        "archive_byte_size": observed_bytes,
        "inventory_sha256": checkpoint["inventory_sha256"],
        "provider_version_or_etag": observed_version,
        "remote_operation_counts": {
            "head": 1,
            "get": 1,
            "list": 0,
            "write": 0,
            "copy": 0,
            "delete": 0,
        },
        "provider_operation_count": 0,
        "workspace_mutation_count": 0,
    }
    args.output_receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
