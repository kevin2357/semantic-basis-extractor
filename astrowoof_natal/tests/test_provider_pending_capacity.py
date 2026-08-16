from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    public_run_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    closeout_run,
    inspect_lifecycle,
)


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


class TestProviderPendingCapacityBaseline(unittest.TestCase):
    """Freeze the 0.4.2 projection before adding capacity-release authority."""

    def materialize(self, root: Path) -> dict:
        run_id = "run_provider_pending_capacity_001"
        actions = []
        passes = {}
        for index in range(1, 4):
            action_id = f"paid_{index:024d}"
            response_id = f"resp_provider_pending_{index}"
            route = f"kevin:authoring_initial:{index:03d}"
            binding = {
                "run_id": run_id,
                "profile_sha256": "1" * 64,
                "prepared_state_revision": index,
                "stage": "authoring_initial",
                "route": route,
                "request_sha256": str(index) * 64,
                "model": "gpt-5.6-terra",
                "service_level": "interactive",
                "maximum_output_tokens": 4000,
                "commitment_micro_usd": 50000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            actions.append({
                "action_id": action_id,
                "state": "WAITING",
                "binding": binding,
                "authorization": {
                    "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                    "action_id": action_id,
                    "binding": binding,
                    "authorization_reference": f"api-reservation-{index}",
                },
                "consumption": {
                    "consumer_id": f"worker-{index}",
                    "consumed_at": f"2026-08-15T20:0{index}:00Z",
                },
                "provider": {"id": response_id, "kind": "response"},
                "reported": None,
            })
            passes[f"pass-{index}"] = {
                "pass_id": f"pass-{index}",
                "state": "WAITING_FOR_RESPONSE",
                "attempts": [{
                    "attempt": 1,
                    "state": "WAITING_FOR_RESPONSE",
                    "provider_metadata": {
                        "provider": "openai",
                        "response_id": response_id,
                        "response_status": "in_progress",
                        "last_polled_at": f"2026-08-15T20:0{index}:30Z",
                    },
                }],
            }
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": run_id,
            "state_revision": 12,
            "status": "WAITING_FOR_RESPONSE",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": actions},
            "passes": passes,
            "subjects": {},
            "provenance": {},
        }
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        return state

    def test_known_provider_wait_is_snapshot_safe_but_not_capacity_releasable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.materialize(root)
            before = hashes(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            self.assertEqual(before, hashes(root))
            self.assertTrue(inspection["observation"]["inventory_valid"])
            self.assertFalse(inspection["terminal"]["terminal"])
            self.assertTrue(
                inspection["terminal"]["provider_continuation_remains"]
            )
            self.assertTrue(inspection["terminal"]["local_continuation_remains"])
            self.assertEqual(
                ["provider_continuation_remains", "local_continuation_remains"],
                inspection["quiescence"]["reasons"],
            )
            self.assertEqual("not_quiescent", inspection["quiescence"]["state"])
            self.assertEqual(
                [{
                    "kind": "provider_result_reconciliation",
                    "blocking": True,
                    "reason_code": "provider_result_pending",
                }],
                inspection["local_dependencies"],
            )
            self.assertNotIn("execution_capacity", inspection)
            self.assertNotIn("provider_custody", inspection)
            self.assertNotIn("resume_not_before", inspection)
            action_ids = inspection["action_inventory"]["actions"]
            self.assertEqual(3, len(action_ids))
            self.assertTrue(all(item["necessary"] for item in action_ids))
            self.assertEqual(
                sorted(item["provider"]["id"] for item in state["spend_ledger"]["actions"]),
                sorted(item["provider_operation_id"] for item in action_ids),
            )

    def test_fresh_process_reads_same_pending_authority_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = hashes(root)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir",
                    str(root),
                    "inspect",
                    "--native-exclusive-access",
                    "declared",
                    "--observed-at",
                    "2026-08-15T20:11:00Z",
                ],
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            inspection = json.loads(completed.stdout)
            self.assertEqual(before, hashes(root))
            self.assertTrue(inspection["observation"]["inventory_valid"])
            self.assertEqual("not_quiescent", inspection["quiescence"]["state"])
            self.assertEqual(
                3,
                sum(
                    item["provider_identity_present"]
                    for item in inspection["action_inventory"]["actions"]
                ),
            )

    def test_closeout_preserves_provider_custody_but_requires_continuation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            result = closeout_run(root, observed_at="2026-08-15T20:12:00Z")
            self.assertEqual("continuation_required", result["disposition"])
            self.assertFalse(result["terminal"]["terminal"])
            self.assertTrue(result["terminal"]["provider_continuation_remains"])
            self.assertTrue(result["terminal"]["local_continuation_remains"])
            self.assertEqual(
                [
                    "paid_000000000000000000000001",
                    "paid_000000000000000000000002",
                    "paid_000000000000000000000003",
                ],
                result["unresolved_action_ids"],
            )
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                [
                    "resp_provider_pending_1",
                    "resp_provider_pending_2",
                    "resp_provider_pending_3",
                ],
                [item["provider"]["id"] for item in persisted["spend_ledger"]["actions"]],
            )


if __name__ == "__main__":
    unittest.main()
