from __future__ import annotations

import json
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    load_json,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    deny_providerless_action,
    inspect_lifecycle,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
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
                    "terminal.transitioned",
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
                "astrowoof.authoring_lifecycle_inspection.v0.3",
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
                "astrowoof.provider_negative_authorization_batch_result.v0.2",
                result["schema_version"],
            )
            self.assertEqual("applied", result["outcome"])
            self.assertEqual(2, len(result["actions"]))
            self.assertEqual("terminalized", result["run_transition"]["outcome"])

    def test_documented_reconciliation_cli_returns_terminal_inspection(self) -> None:
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
                observed_at="2026-08-15T23:30:00Z",
            )
            action = inspection["action_inventory"]["actions"][0]
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"], "action_id": action["action_id"],
                "binding": action["binding"], "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:cli-reconcile",
            }
            deny_providerless_action(
                run_dir, request, decision_at="2026-08-15T23:30:01Z"
            )
            state = load_json(run_dir / "run.json")
            state.pop("terminal_transition", None)
            state["status"] = "AUTHORING"
            action = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == request["action_id"]
            )
            denial = action["negative_authorization"]
            denial.pop("run_transition", None)
            artifact = {
                "schema_version": "astrowoof.provider_negative_authorization_record.v0.1",
                "run_id": state["run_id"], "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "disposition": "DENIED_PROVIDERLESS",
                "denial_reason": denial["denial_reason"],
                "authorization_previously_recorded": denial[
                    "authorization_previously_recorded"
                ],
                "external_authority_reference": denial[
                    "external_authority_reference"
                ],
                "request_observation": copy.deepcopy(denial["request_observation"]),
                "decision_basis": copy.deepcopy(denial["decision_basis"]),
            }
            (run_dir / denial["result_artifact"]).write_text(
                json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
            )
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)
            completed = subprocess.run(
                [
                    sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir", str(run_dir), "--stdout-jsonl",
                    "reconcile-required-denial",
                    "--reconciled-at", "2026-08-15T23:30:02Z",
                ],
                text=True, capture_output=True, check=False,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            envelopes = [json.loads(line) for line in completed.stdout.splitlines()]
            self.assertEqual("terminal.transitioned", envelopes[0]["event_name"])
            self.assertEqual("sbe.command_result.v1", envelopes[-1]["schema_version"])
            result = envelopes[-1]["result"]
            self.assertEqual(
                "astrowoof.authoring_lifecycle_inspection.v0.3",
                result["schema_version"],
            )
            self.assertTrue(result["terminal"]["terminal"])
            self.assertEqual("budget_exhausted", result["terminal"]["outcome"])
            self.assertEqual([], result["local_dependencies"])


if __name__ == "__main__":
    unittest.main()
