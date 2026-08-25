from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from astrowoof_natal_authoring.cli.provider_economics import main as cli_main
from astrowoof_natal_authoring.provider_economics_export import (
    read_provider_economics_export,
    validate_provider_economics_export,
)
from astrowoof_natal_authoring.provider_economics_qa import _materialize


class ProviderEconomicsExportTests(unittest.TestCase):
    def test_snapshot_validating_export_and_unchanged_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            _materialize(root, bounded=False, batch=False)
            first = read_provider_economics_export(
                root, observed_at="2026-08-25T12:01:00Z",
            )
            validate_provider_economics_export(first)
            self.assertEqual(1, first["revision_count"])
            replay = read_provider_economics_export(
                root, observed_at="2026-08-25T12:02:00Z",
                previous_revisions=first["revisions"],
            )
            self.assertEqual(0, replay["revision_count"])

    def test_changed_settlement_mints_contiguous_revision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            _materialize(root, bounded=False, batch=False)
            state_path = root / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["state"] = "WAITING"
            state["spend_ledger"]["actions"][0]["reported"] = None
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            from astrowoof_natal_authoring.closure import write_workspace_snapshot
            write_workspace_snapshot(root)
            first = read_provider_economics_export(
                root, observed_at="2026-08-25T12:01:00Z",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["state"] = "REPORTED"
            state["spend_ledger"]["actions"][0]["reported"] = {
                "usage": {"input_tokens": 100, "cached_input_tokens": 40,
                          "output_tokens": 20, "reasoning_tokens": 5},
                "estimated_micro_usd": 1234,
                "price_book_version": "qa-prices.v1",
            }
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(root)
            second = read_provider_economics_export(
                root, observed_at="2026-08-25T12:02:00Z",
                previous_revisions=first["revisions"],
            )
            self.assertEqual(2, second["revisions"][0]["revision_number"])
            with self.assertRaisesRegex(ValueError, "sequence"):
                read_provider_economics_export(
                    root, observed_at="2026-08-25T12:03:00Z",
                    previous_revisions=[second["revisions"][0]],
                )

    def test_incomplete_snapshot_and_noncanonical_time_refuse(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            _materialize(root, bounded=True, batch=False)
            with self.assertRaisesRegex(ValueError, "canonical UTC"):
                read_provider_economics_export(
                    root, observed_at="2026-08-25T12:00:00+00:00",
                )
            (root / "unexpected.txt").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                read_provider_economics_export(
                    root, observed_at="2026-08-25T12:00:00Z",
                )

    def test_cli_writes_only_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "run"
            _materialize(root, bounded=False, batch=True)
            output = base / "export.json"
            self.assertEqual(0, cli_main([
                "--run-dir", str(root), "--observed-at",
                "2026-08-25T12:00:00Z", "--output", str(output),
            ]))
            self.assertEqual(1, json.loads(output.read_text())["revision_count"])
            with self.assertRaisesRegex(ValueError, "outside"):
                cli_main([
                    "--run-dir", str(root), "--observed-at",
                    "2026-08-25T12:00:00Z", "--output", str(root / "bad.json"),
                ])


if __name__ == "__main__":
    unittest.main()
