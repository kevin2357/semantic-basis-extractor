from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    SNAPSHOT_SCHEMA,
    load_json,
    normalized_path,
    snapshot_inventory,
    validate_workspace_snapshot,
    write_json_atomic,
)
from astrowoof_natal_authoring.repair import (  # noqa: E402
    inspect_polish_checkpoint,
    repair_polish_checkpoint,
)
from astrowoof_natal_authoring.spend import (  # noqa: E402
    AUTHORIZATION_SCHEMA,
    digest,
)


class CheckpointRepairTests(unittest.TestCase):
    def refresh_snapshot_member(self, run: Path, relative: str) -> None:
        snapshot_path = run / "workspace-snapshot.json"
        snapshot = load_json(snapshot_path)
        current = {
            item["path"]: item
            for item in snapshot_inventory(run, use_process_cache=False)
        }
        snapshot["members"] = [
            current[relative] if item["path"] == relative else item
            for item in snapshot["members"]
        ]
        write_json_atomic(snapshot_path, snapshot)

    def make_fixture(self, root: Path):
        run = root / "run"
        subject = "juniper"
        final = run / "final" / subject
        attempt1 = final / "polish" / "attempt-001"
        attempt2 = final / "polish" / "attempt-002"
        packet = (
            run / "sbe" / "semantic-basis-output" / subject
            / f"{subject}.selected-authoring-packet.json"
        )
        packet.parent.mkdir(parents=True)
        attempt1.mkdir(parents=True)
        attempt2.mkdir(parents=True)
        write_json_atomic(packet, {"subject": subject})
        write_json_atomic(final / f"natal.{subject}.assembly-report.json", {
            "schema_version": "assembly.v1", "status": "pass", "subject": subject,
        })
        final_paths = {
            "deck": final / f"natal.{subject}.cards.json",
            "lint": final / f"natal.{subject}.lint-report.json",
            "validation": final / f"natal.{subject}.validation-report.json",
        }
        write_json_atomic(final_paths["deck"], {"generation": "baseline"})
        write_json_atomic(final_paths["lint"], {
            "schema_version": "lint.v1", "status": "warn", "warning_count": 2,
            "decks": [], "cross_subject_warnings": [],
        })
        write_json_atomic(final_paths["validation"], {
            "status": "pass", "errors": [], "warnings": ["baseline warning"],
            "checks": {},
        })
        write_json_atomic(attempt1 / f"natal.{subject}.cards.json", {
            "generation": "polish-1",
        })
        write_json_atomic(attempt1 / "lint-report.json", {
            "schema_version": "lint.v1", "status": "warn", "warning_count": 1,
            "decks": [], "cross_subject_warnings": [],
        })
        write_json_atomic(attempt1 / "validation-report.json", {
            "status": "pass", "errors": [], "warnings": [], "checks": {},
        })
        response_id = "resp_polish_1"
        write_json_atomic(attempt1 / "openai-background-response.json", {
            "id": response_id, "status": "completed",
        })
        write_json_atomic(attempt1 / "openai-response.json", {
            "id": response_id,
            "status": "completed",
            "model": "gpt-test",
            "completed_at": "2026-08-09T00:00:00+00:00",
        })
        request2 = {"model": "gpt-test", "input": "exact prepared request"}
        write_json_atomic(attempt2 / "openai-request.json", request2)
        binding1 = {
            "run_id": "run-test", "profile_sha256": "profile", "prepared_state_revision": 5,
            "stage": "polish", "route": f"{subject}:polish:001",
            "request_sha256": "request-1", "model": "gpt-test",
            "service_level": "interactive", "maximum_output_tokens": 100,
            "commitment_micro_usd": 20000, "price_book_version": "prices-test",
        }
        binding2 = {**binding1, "route": f"{subject}:polish:002", "request_sha256": digest(request2)}
        action1 = {
            "action_id": "paid_one", "state": "REPORTED", "binding": binding1,
            "authorization": {"reference": "used"},
            "provider": {"kind": "response", "id": response_id},
            "reported": {
                "usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12},
                "estimated_micro_usd": 1234,
            },
            "reconciliation_reference_ids": [],
            "consumption": {"consumer_id": "worker"},
        }
        action2 = {
            "action_id": "paid_two", "state": "PREPARED", "binding": binding2,
            "authorization": None, "provider": None, "reported": None,
            "reconciliation_reference_ids": [],
        }
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "state_revision": 8,
            "run_id": "run-test",
            "status": "AWAITING_SPEND_AUTHORIZATION",
            "created_at": "2026-08-09T00:00:00+00:00",
            "updated_at": "2026-08-09T00:00:00+00:00",
            "run_dir": normalized_path(run),
            "workspace_contract": {
                "mode": "stable_logical_absolute_path", "logical_root": normalized_path(run),
            },
            "authoring_profile": {
                "schema_version": "astrowoof.authoring_profile.v0.1",
                "qa": {"polish": True, "max_polish_attempts": 2},
            },
            "passes": {"juniper_1": {"state": "PASS_QA_ACCEPTED", "attempts": []}},
            "subjects": {},
            "spend_ledger": {"actions": [action1, action2], "reconciliation_references": []},
        }
        write_json_atomic(run / "run.json", state)
        write_json_atomic(run / "public-run.json", {"status": state["status"]})
        write_json_atomic(run / "spend-authorization-requests.json", {
            "actions": [{"action_id": action2["action_id"], "binding": binding2}],
        })
        write_json_atomic(run / "workspace-snapshot.json", {
            "schema_version": SNAPSHOT_SCHEMA,
            "logical_root": normalized_path(run),
            "members": snapshot_inventory(run, use_process_cache=False),
        })
        shutil.copy2(attempt1 / f"natal.{subject}.cards.json", final_paths["deck"])
        shutil.copy2(attempt1 / "lint-report.json", final_paths["lint"])
        shutil.copy2(attempt1 / "validation-report.json", final_paths["validation"])
        authorization = root / "authorization.json"
        write_json_atomic(authorization, {
            "schema_version": AUTHORIZATION_SCHEMA,
            "action_id": action2["action_id"],
            "binding": binding2,
            "authorization_reference": "api-reservation-test",
        })
        return run, authorization, final_paths, attempt1

    def test_dry_run_and_apply_exact_polish_shape(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, _attempt = self.make_fixture(root)
            plan, repaired = inspect_polish_checkpoint(run, authorization_path=authorization)
            self.assertTrue(plan["eligible"])
            self.assertEqual(3, len(plan["changed_members"]))
            self.assertEqual("paid_two", plan["prepared_action_id"])
            self.assertIn("juniper", repaired["subjects"])
            self.assertEqual({}, load_json(run / "run.json")["subjects"])

            backup = root / "backup"
            shutil.copytree(run, backup)
            applied = repair_polish_checkpoint(
                run, authorization_path=authorization, backup_path=backup,
                owner_reference="api-exclusive-lease-test",
            )
            state = load_json(run / "run.json")
            self.assertEqual("apply", applied["mode"])
            self.assertEqual("AWAITING_SPEND_AUTHORIZATION", state["status"])
            self.assertEqual("PREPARED", state["spend_ledger"]["actions"][1]["state"])
            self.assertIsNone(state["spend_ledger"]["actions"][1]["authorization"])
            self.assertEqual(2, len(state["subjects"]["juniper"]["polish_attempts"]))
            self.assertEqual(
                "POLISH_IMPROVED_PARTIAL",
                state["subjects"]["juniper"]["polish_attempts"][0]["state"],
            )
            self.assertFalse(
                state["subjects"]["juniper"]["polish_attempts"][0]["accepted"]
            )
            self.assertEqual(
                "SUBMITTED",
                state["subjects"]["juniper"]["polish_attempts"][1]["state"],
            )
            validate_workspace_snapshot(run, state)

    def test_refuses_unexplained_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, _attempt = self.make_fixture(root)
            (run / "unexpected.txt").write_text("mutation", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing or additional"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_refuses_changed_retained_attempt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, attempt = self.make_fixture(root)
            write_json_atomic(attempt / "lint-report.json", {"altered": True})
            self.refresh_snapshot_member(
                run, "final/juniper/polish/attempt-001/lint-report.json"
            )
            with self.assertRaisesRegex(ValueError, "retained attempt"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_refuses_mismatched_authorization(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, _attempt = self.make_fixture(root)
            document = load_json(authorization)
            document["binding"]["maximum_output_tokens"] += 1
            write_json_atomic(authorization, document)
            with self.assertRaisesRegex(ValueError, "exactly bound"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_refuses_provider_identity_mismatch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, attempt = self.make_fixture(root)
            response = load_json(attempt / "openai-response.json")
            response["id"] = "resp_conflict"
            write_json_atomic(attempt / "openai-response.json", response)
            self.refresh_snapshot_member(
                run, "final/juniper/polish/attempt-001/openai-response.json"
            )
            with self.assertRaisesRegex(ValueError, "provider identity"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_refuses_missing_native_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, attempt = self.make_fixture(root)
            (attempt / "openai-response.json").unlink()
            with self.assertRaisesRegex(ValueError, "missing or additional"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_refuses_used_next_action(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, _attempt = self.make_fixture(root)
            state = load_json(run / "run.json")
            state["spend_ledger"]["actions"][1]["state"] = "AUTHORIZED"
            state["spend_ledger"]["actions"][1]["authorization"] = {"used": True}
            write_json_atomic(run / "run.json", state)
            self.refresh_snapshot_member(run, "run.json")
            with self.assertRaisesRegex(ValueError, "expected one PREPARED"):
                inspect_polish_checkpoint(run, authorization_path=authorization)

    def test_apply_requires_separate_exact_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, authorization, _final, _attempt = self.make_fixture(root)
            backup = root / "backup"
            shutil.copytree(run, backup)
            (backup / "workspace-snapshot.json").unlink()
            with self.assertRaisesRegex(ValueError, "byte-identical"):
                repair_polish_checkpoint(
                    run, authorization_path=authorization, backup_path=backup,
                    owner_reference="api-exclusive-lease-test",
                )


if __name__ == "__main__":
    unittest.main()
