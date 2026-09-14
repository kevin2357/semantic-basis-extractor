from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests.test_relocated_operator_disposition_reader_slice2 import (
    RelocatedOperatorDispositionReaderSlice2Tests,
)
from astrowoof_natal_authoring.closure import (
    load_json,
    snapshot_inventory,
    write_json_atomic,
)
from astrowoof_natal_authoring.relocated_operator_disposition import (
    read_relocated_operator_disposition_assessment,
)


class SnapshotInventoryPortableOrderSlice1Tests(unittest.TestCase):
    def test_inventory_uses_case_sensitive_posix_component_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            members = {
                "bundle/item.txt": b"directory member",
                "bundle.zip": b"archive member",
                "source/DOG DETAILS.md": b"uppercase sibling",
                "source/cards/card.md": b"lowercase directory",
            }
            for relative, content in members.items():
                path = root / Path(relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

            self.assertEqual(
                [
                    "bundle/item.txt",
                    "bundle.zip",
                    "source/DOG DETAILS.md",
                    "source/cards/card.md",
                ],
                [item["path"] for item in snapshot_inventory(
                    root, use_process_cache=False,
                )],
            )

    def test_duplicate_manifest_member_still_fails_closed(self):
        fixture = RelocatedOperatorDispositionReaderSlice2Tests()
        with tempfile.TemporaryDirectory() as temporary:
            _, relocated, authority = fixture._relocated(temporary)
            manifest_path = relocated / "workspace-snapshot.json"
            manifest = load_json(manifest_path)
            manifest["members"].append(dict(manifest["members"][0]))
            write_json_atomic(manifest_path, manifest)

            with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                read_relocated_operator_disposition_assessment(
                    relocated,
                    authority=authority,
                    assessed_at="2026-09-10T19:02:00Z",
                )

    def test_genuine_member_drift_still_fails_closed(self):
        fixture = RelocatedOperatorDispositionReaderSlice2Tests()
        for case in ("missing", "extra", "size", "digest"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                _, relocated, authority = fixture._relocated(temporary)
                manifest = load_json(relocated / "workspace-snapshot.json")
                target = relocated / manifest["members"][0]["path"]
                if case == "missing":
                    target.unlink()
                elif case == "extra":
                    (relocated / "unexpected-member.txt").write_bytes(b"extra")
                elif case == "size":
                    target.write_bytes(target.read_bytes() + b"x")
                else:
                    content = target.read_bytes()
                    replacement = bytes([content[0] ^ 1]) + content[1:]
                    target.write_bytes(replacement)

                with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                    read_relocated_operator_disposition_assessment(
                        relocated,
                        authority=authority,
                        assessed_at="2026-09-10T19:02:00Z",
                    )


if __name__ == "__main__":
    unittest.main()
