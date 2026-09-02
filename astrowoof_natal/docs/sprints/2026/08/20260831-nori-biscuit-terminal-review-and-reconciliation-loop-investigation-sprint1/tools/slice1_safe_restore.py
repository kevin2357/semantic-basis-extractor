"""Safely restore and validate one locally downloaded checkpoint archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(64 * 1024):
            value.update(chunk)
    return value.hexdigest()


def canonical_sha(value: object) -> str:
    encoded = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--generation", type=int, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    if args.destination.exists():
        raise ValueError("Destination must not already exist")
    if digest(args.archive) != args.archive_sha256:
        raise ValueError("Archive digest mismatch")
    args.destination.mkdir(parents=True)
    with zipfile.ZipFile(args.archive, "r") as bundle:
        members = bundle.infolist()
        names: set[str] = set()
        for member in members:
            pure = PurePosixPath(member.filename)
            mode = member.external_attr >> 16
            if (
                pure.is_absolute() or ".." in pure.parts or not pure.parts
                or pure.parts[0] not in {"checkpoint-manifest.json", "workspace"}
                or member.filename in names
                or stat.S_ISLNK(mode)
            ):
                raise ValueError(f"Unsafe archive member: {member.filename!r}")
            names.add(member.filename)
        manifest = json.loads(bundle.read("checkpoint-manifest.json"))
        if (
            manifest.get("schema_version") != "astrowoof.checkpoint-archive.v1"
            or manifest.get("checkpoint_contract")
            != "astrowoof.sbe-workspace-checkpoint.v1"
            or manifest.get("generation") != args.generation
            or manifest.get("inventory_sha256") != args.inventory_sha256
            or canonical_sha(manifest.get("members")) != args.inventory_sha256
        ):
            raise ValueError("Checkpoint manifest identity mismatch")
        declared = manifest.get("members")
        if not isinstance(declared, list) or manifest.get("member_count") != len(declared):
            raise ValueError("Checkpoint member inventory is malformed")
        expected_names = {"workspace/" + item["path"] for item in declared}
        file_names = {item.filename for item in members if not item.is_dir()}
        if file_names != expected_names | {"checkpoint-manifest.json"}:
            raise ValueError("Archive members do not exactly match inventory")
        for member in members:
            target = args.destination.joinpath(*PurePosixPath(member.filename).parts)
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(member, "r") as source, target.open("xb") as output:
                while chunk := source.read(64 * 1024):
                    output.write(chunk)
    workspace = args.destination / "workspace"
    for item in declared:
        path = workspace.joinpath(*PurePosixPath(item["path"]).parts)
        if path.stat().st_size != item["byte_size"] or digest(path) != item["sha256"]:
            raise ValueError(f"Restored member mismatch: {item['path']}")
    snapshot = json.loads((workspace / "workspace-snapshot.json").read_text(encoding="utf-8"))
    snapshot_expected = snapshot.get("members")
    snapshot_actual = []
    for path in sorted(item for item in workspace.rglob("*") if item.is_file()):
        relative = path.relative_to(workspace).as_posix()
        if (
            relative == "workspace-snapshot.json"
            or relative.startswith("native-publication-receipts/")
            or relative.endswith(".lock")
        ):
            continue
        snapshot_actual.append({
            "path": relative, "bytes": path.stat().st_size, "sha256": digest(path),
        })
    if (
        not isinstance(snapshot_expected, list)
        or {item["path"]: item for item in snapshot_expected}
        != {item["path"]: item for item in snapshot_actual}
    ):
        raise ValueError("Workspace snapshot member validation failed")
    receipt = {
        "schema_version": "astrowoof.investigation.offline_restore_receipt.v1",
        "archive_sha256": args.archive_sha256,
        "archive_inventory_sha256": args.inventory_sha256,
        "archive_member_count": len(declared),
        "checkpoint_generation": args.generation,
        "workspace_snapshot_schema": snapshot.get("schema_version"),
        "workspace_snapshot_logical_root": snapshot.get("logical_root"),
        "workspace_snapshot_member_count": len(snapshot_actual),
        "archive_safe": True,
        "archive_inventory_valid": True,
        "workspace_snapshot_members_valid": True,
        "provider_operation_count": 0,
        "workspace_mutation_count": 0,
    }
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
