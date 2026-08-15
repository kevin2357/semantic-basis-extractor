from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import write_workspace_snapshot  # noqa: E402
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.lifecycle_smoke import (  # noqa: E402
    _state,
    run_lifecycle_smoke,
)


class TestLifecycleConsumer(unittest.TestCase):
    def test_provider_free_lifecycle_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = run_lifecycle_smoke(Path(temporary))
            self.assertEqual("pass", report["status"], report["errors"])
            self.assertEqual(
                [
                    "authorization.denied_providerless",
                    "authorization.denied_providerless",
                    "authorization.denied_providerless",
                    "authorization.denied_providerless_batch",
                    "authorization.denied_providerless_batch",
                    "closeout.completed",
                ],
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

    def test_documented_batch_cli_returns_typed_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_dir = root / "run"
            run_dir.mkdir()
            state = _state(run_dir)
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-15T21:00:00Z",
            )
            eligible = [
                item for item in inspection["action_inventory"]["actions"]
                if item["providerless_denial_eligible"]
                and item["binding"]["stage"] == "creative_retry"
            ]
            request = {
                "schema_version": BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"],
                "observed": inspection["observation"],
                "actions": [{
                    "action_id": item["action_id"],
                    "binding": item["binding"],
                    "denial_reason": "reservation_unavailable",
                    "external_authority_reference": f"cli-fixture:{index}",
                } for index, item in enumerate(eligible, start=1)],
            }
            request_path = root / "batch-request.json"
            request_path.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir", str(run_dir), "deny-providerless-batch",
                    "--request", str(request_path),
                    "--decision-at", "2026-08-15T21:00:01Z",
                ],
                text=True, capture_output=True, check=False,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(
                "astrowoof.provider_negative_authorization_batch_result.v0.1",
                result["schema_version"],
            )
            self.assertEqual("applied", result["outcome"])
            self.assertEqual(2, len(result["actions"]))


if __name__ == "__main__":
    unittest.main()
