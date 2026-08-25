from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.closure import (
    load_json,
    public_run_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.temporal_lifecycle import inspect_temporal_lifecycle

from test_external_authority_v2_route_qualification import (
    _six_member_pending_workspace,
)


def _workspace_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


def _add_prepared_action(root: Path) -> str:
    state = load_json(root / "run.json")
    action_id = "paid_ffffffffffffffffffffffff"
    state["spend_ledger"]["actions"].append({
        "action_id": action_id,
        "state": "PREPARED",
        "binding": {
            "run_id": state["run_id"],
            "profile_sha256": "f" * 64,
            "prepared_state_revision": state["state_revision"],
            "stage": "polish",
            "route": "polish:attempt-001",
            "request_sha256": "e" * 64,
            "model": "gpt-5.6-terra",
            "service_level": "interactive",
            "maximum_output_tokens": 4000,
            "commitment_micro_usd": 50000,
            "price_book_version": "openai-public-2026-08-07.v1",
        },
    })
    (root / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )
    (root / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(root)
    return action_id


class TestProviderReconciliationPrecedesAuthoritySlice0(unittest.TestCase):
    """Freeze the public 0.4.21 selector defect before changing runtime code."""

    def materialize(self, root: Path, route_family: str) -> str:
        _six_member_pending_workspace(root, route_family)
        state = load_json(root / "run.json")
        state["updated_at"] = "1970-01-01T00:00:00Z"
        # The retained provider work is already past initial-wave admission.  It
        # must not make the later ordinary PREPARED action look like another
        # initial wave.  Bounded v2 natively carries this shape; for exact Natal
        # use six pass-local retry operations so the fixture exercises the same
        # route adapter without manufacturing orphaned initial-wave lineage.
        state.pop("initial_authoring_wave", None)
        if route_family == "exact_natal":
            state["passes"] = {}
            for number, action in enumerate(state["spend_ledger"]["actions"], 1):
                action["binding"]["stage"] = "creative_retry"
                action["binding"]["route"] = (
                    f"creative_retry:qualification-pass-{number:02d}:attempt-002"
                )
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        return _add_prepared_action(root)

    def test_due_provider_custody_already_precedes_prepared_authority(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route_family=route_family), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                prepared_id = self.materialize(root, route_family)
                before = _workspace_hashes(root)

                lifecycle = inspect_lifecycle(
                    root,
                    native_exclusive_access="declared",
                    observed_at="1970-01-01T00:00:15Z",
                )

                self.assertEqual(before, _workspace_hashes(root))
                self.assertEqual(
                    "provider_reconciliation_cycle",
                    lifecycle["execution_branch"]["command"],
                )
                self.assertEqual(
                    "provider_reconciliation_due",
                    lifecycle["execution_branch"]["reason_code"],
                )
                self.assertEqual(4, len(lifecycle["execution_branch"]["action_ids"]))
                self.assertNotIn(prepared_id, lifecycle["execution_branch"]["action_ids"])

    def test_not_due_provider_custody_contradiction_is_now_rejected(self) -> None:
        for route_family in ("exact_natal", "bounded_natal"):
            with self.subTest(route_family=route_family), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                prepared_id = self.materialize(root, route_family)
                before = _workspace_hashes(root)

                with self.assertRaisesRegex(
                    ValueError, "retained_provider_custody_precedes_authority"
                ):
                    inspect_lifecycle(
                        root,
                        native_exclusive_access="declared",
                        observed_at="1970-01-01T00:00:10Z",
                    )
                self.assertEqual(before, _workspace_hashes(root))
                self.assertEqual("paid_ffffffffffffffffffffffff", prepared_id)

    def test_completed_provider_evidence_contradiction_is_now_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            prepared_id = self.materialize(root, "exact_natal")
            state = load_json(root / "run.json")
            for action in state["spend_ledger"]["actions"]:
                if action["action_id"] != prepared_id:
                    action["provider_reconciliation"].update({
                        "last_attempt_at": "1970-01-01T00:00:15Z",
                        "last_outcome": "completed",
                        "resume_not_before": "1970-01-01T00:00:15Z",
                    })
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            (root / "public-run.json").write_text(
                json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            before = _workspace_hashes(root)

            with self.assertRaisesRegex(
                ValueError, "provider_fan_in_precedes_authority"
            ):
                inspect_lifecycle(
                    root,
                    native_exclusive_access="declared",
                    observed_at="1970-01-01T00:00:10Z",
                )
            self.assertEqual(before, _workspace_hashes(root))

    def test_time_only_authority_basis_change_is_rejected_before_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            prepared_id = self.materialize(root, "exact_natal")
            before = _workspace_hashes(root)
            due = inspect_temporal_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="1970-01-01T00:00:15Z",
            )

            self.assertEqual(before, _workspace_hashes(root))
            with self.assertRaisesRegex(
                ValueError, "retained_provider_custody_precedes_authority"
            ):
                inspect_temporal_lifecycle(
                    root,
                    native_exclusive_access="declared",
                    observed_at="1970-01-01T00:00:10Z",
                )
            self.assertEqual(before, _workspace_hashes(root))
            self.assertEqual(
                "none", due["checkpoint_basis"]["external_authority_state"]["kind"]
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                due["temporal_decision"]["selected_command"],
            )
            self.assertEqual(4, len(due["temporal_decision"]["due_action_ids"]))
            self.assertEqual("paid_ffffffffffffffffffffffff", prepared_id)


if __name__ == "__main__":
    unittest.main()
