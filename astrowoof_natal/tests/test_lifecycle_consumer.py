from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.lifecycle_smoke import run_lifecycle_smoke  # noqa: E402


class TestLifecycleConsumer(unittest.TestCase):
    def test_provider_free_lifecycle_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = run_lifecycle_smoke(Path(temporary))
            self.assertEqual("pass", report["status"], report["errors"])
            self.assertEqual(
                ["authorization.denied_providerless", "closeout.completed"],
                report["checks"]["event_names"],
            )

    def test_documented_lifecycle_cli_inspects_without_source_internals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            smoke = run_lifecycle_smoke(root)
            self.assertEqual("pass", smoke["status"])
            command = [
                sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
                "--run-dir", str(root / "run"), "inspect",
                "--native-exclusive-access", "declared",
                "--observed-at", "2026-08-13T00:00:03Z",
            ]
            completed = subprocess.run(
                command, text=True, capture_output=True, check=False,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(
                "astrowoof.authoring_lifecycle_inspection.v0.1",
                result["schema_version"],
            )
            self.assertTrue(result["observation"]["inventory_valid"])


if __name__ == "__main__":
    unittest.main()
