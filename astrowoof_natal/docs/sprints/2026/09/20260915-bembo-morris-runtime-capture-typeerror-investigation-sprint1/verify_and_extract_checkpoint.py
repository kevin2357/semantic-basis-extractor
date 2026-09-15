"""Verify one checkpoint archive and safely extract its workspace read-only copy."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")

    with zipfile.ZipFile(args.archive) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)):
            raise ValueError("duplicate archive member")
        for info in infos:
            path = PurePosixPath(info.filename)
            mode = info.external_attr >> 16
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename:
                raise ValueError("unsafe archive member")
            if stat.S_ISLNK(mode):
                raise ValueError("archive link refused")
        manifest = json.loads(archive.read("checkpoint-manifest.json"))
        if manifest["inventory_sha256"] != args.inventory_sha256:
            raise ValueError("manifest inventory digest mismatch")
        members = manifest["members"]
        encoded = (
            json.dumps(members, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()
        if hashlib.sha256(encoded).hexdigest() != args.inventory_sha256:
            raise ValueError("member inventory digest mismatch")
        expected = {"workspace/" + row["path"]: row for row in members}
        actual = {name for name in names if name != "checkpoint-manifest.json"}
        if actual != set(expected):
            raise ValueError("archive member set mismatch")
        for name, row in expected.items():
            payload = archive.read(name)
            if len(payload) != row["byte_size"]:
                raise ValueError("member byte size mismatch")
            if hashlib.sha256(payload).hexdigest() != row["sha256"]:
                raise ValueError("member digest mismatch")
        args.output.mkdir(parents=True)
        for name in sorted(actual):
            target = args.output / PurePosixPath(name).relative_to("workspace")
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as source, target.open("xb") as destination:
                shutil.copyfileobj(source, destination)
    print(json.dumps({
        "archive_members": len(infos),
        "verified_workspace_members": len(members),
        "inventory_sha256": args.inventory_sha256,
        "output": str(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
