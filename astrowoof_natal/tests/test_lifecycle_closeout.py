from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import normalized_path, write_workspace_snapshot  # noqa: E402
from astrowoof_natal_authoring.lifecycle import closeout_run, inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal.tests.test_lifecycle_contracts import validate  # noqa: E402


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*") if path.is_file() and not path.name.endswith(".lock")
    }


class TestLifecycleCloseout(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(read_resource_text(
            "contracts/authoring-lifecycle-contracts.schema.json"
        ))

    def state(self, root: Path, *, status: str) -> dict:
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_closeout_001", "state_revision": 9,
            "status": status,
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": []}, "passes": {}, "subjects": {},
        }

    def materialize(self, root: Path, state: dict) -> None:
        (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        write_workspace_snapshot(root)

    def test_continuation_closeout_is_durable_schema_valid_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root, status="AUTHORING_COMPLETE"))
            first = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            validate(first, self.schema, self.schema)
            self.assertEqual("continuation_required", first["disposition"])
            self.assertEqual("local_assembly", first["local_dependencies"][0]["kind"])
            before = hashes(root)
            second = closeout_run(root, observed_at="2026-08-13T22:01:00Z")
            self.assertEqual(before, hashes(root))
            self.assertEqual(first["semantic_result_sha256"], second["semantic_result_sha256"])
            self.assertEqual(first["result_checkpoint"], second["result_checkpoint"])

    def test_completed_delivery_closeout_preserves_delivery_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            deck = root / "final" / "ella" / "deck.json"
            deck.parent.mkdir(parents=True)
            deck.write_text('{"accepted":true}\n', encoding="utf-8")
            delivery = root / "final" / "ella" / "delivery.zip"
            delivery.write_bytes(b"accepted-delivery-fixture")
            state = self.state(root, status="DELIVERY_COMPLETE")
            state["subjects"] = {"ella": {
                "state": "DELIVERY_COMPLETE", "deck": str(deck),
                "delivery": str(delivery),
            }}
            self.materialize(root, state)
            accepted_before = (hashlib.sha256(deck.read_bytes()).hexdigest(),
                               hashlib.sha256(delivery.read_bytes()).hexdigest())
            result = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            self.assertEqual("closed", result["disposition"])
            self.assertEqual("quiescent", result["quiescence"]["state"])
            self.assertEqual(accepted_before, (
                hashlib.sha256(deck.read_bytes()).hexdigest(),
                hashlib.sha256(delivery.read_bytes()).hexdigest(),
            ))

    def test_ambiguous_run_closeout_is_machine_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.state(root, status="AMBIGUOUS_PROVIDER_SUBMISSION")
            binding = {
                "run_id": state["run_id"], "profile_sha256": "1" * 64,
                "prepared_state_revision": 9, "stage": "polish",
                "route": "ella:polish:002", "request_sha256": "2" * 64,
                "model": "gpt-5.6", "service_level": "batch",
                "maximum_output_tokens": 8000, "commitment_micro_usd": 125000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            state["spend_ledger"]["actions"] = [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "AMBIGUOUS_PROVIDER_SUBMISSION", "binding": binding,
                "authorization": {}, "provider": None, "reported": None,
            }]
            self.materialize(root, state)
            result = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            self.assertEqual("ambiguous", result["disposition"])
            self.assertEqual("ambiguous", result["terminal"]["outcome"])
            self.assertEqual(["paid_0123456789abcdef01234567"], result["unresolved_action_ids"])

    def test_crash_restart_recovers_every_closeout_write_boundary(self) -> None:
        points = (
            "after_artifact_staged", "after_state_persisted",
            "after_artifact_promoted", "after_snapshot_published",
        )
        for point in points:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                self.materialize(root, self.state(root, status="AUTHORING_COMPLETE"))

                def fail(observed: str) -> None:
                    if observed == point:
                        raise RuntimeError(f"injected:{point}")

                with self.assertRaisesRegex(RuntimeError, f"injected:{point}"):
                    closeout_run(
                        root, observed_at="2026-08-13T22:00:00Z",
                        _failure_injector=fail,
                    )
                recovered = closeout_run(
                    root, observed_at="2026-08-13T22:00:01Z"
                )
                validate(recovered, self.schema, self.schema)
                self.assertEqual("continuation_required", recovered["disposition"])
                before_replay = hashes(root)
                replay = closeout_run(root)
                self.assertEqual(before_replay, hashes(root))
                self.assertEqual(
                    recovered["semantic_result_sha256"],
                    replay["semantic_result_sha256"],
                )

    def test_recovery_refuses_unrelated_workspace_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root, status="AUTHORING_COMPLETE"))

            def fail(point: str) -> None:
                if point == "after_state_persisted":
                    raise RuntimeError("injected")

            with self.assertRaisesRegex(RuntimeError, "injected"):
                closeout_run(root, _failure_injector=fail)
            (root / "unrelated.json").write_text("{}\n", encoding="utf-8")
            before = hashes(root)
            with self.assertRaisesRegex(ValueError, "snapshot"):
                closeout_run(root)
            self.assertEqual(before, hashes(root))

    def test_missing_or_changed_staged_artifact_cannot_be_recovered(self) -> None:
        for mutation in ("missing", "changed"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                self.materialize(root, self.state(root, status="AUTHORING_COMPLETE"))

                def fail(point: str) -> None:
                    if point == "after_state_persisted":
                        raise RuntimeError("injected")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    closeout_run(root, _failure_injector=fail)
                staged = root / "lifecycle" / ".closeout-result.json.tmp"
                if mutation == "missing":
                    staged.unlink()
                else:
                    staged.write_text('{"changed":true}\n', encoding="utf-8")
                before = hashes(root)
                with self.assertRaisesRegex(ValueError, "snapshot"):
                    closeout_run(root)
                self.assertEqual(before, hashes(root))

    def test_known_active_provider_work_remains_exact_and_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.state(root, status="WAITING_FOR_RESPONSE")
            binding = {
                "run_id": state["run_id"], "profile_sha256": "1" * 64,
                "prepared_state_revision": 9, "stage": "polish",
                "route": "ella:polish:002", "request_sha256": "2" * 64,
                "model": "gpt-5.6", "service_level": "batch",
                "maximum_output_tokens": 8000, "commitment_micro_usd": 125000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            state["spend_ledger"]["actions"] = [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "WAITING", "binding": binding,
                "authorization": {},
                "consumption": {"consumer_id": "worker", "state_revision": 10},
                "provider": {"kind": "response", "id": "resp_exact_active"},
                "reported": None,
            }]
            self.materialize(root, state)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T22:00:00Z",
            )
            action = inspection["action_inventory"]["actions"][0]
            self.assertEqual("resp_exact_active", action["provider_operation_id"])
            result = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            self.assertEqual("continuation_required", result["disposition"])
            self.assertEqual(
                ["paid_0123456789abcdef01234567"], result["unresolved_action_ids"]
            )
            retained = json.loads((root / "run.json").read_text(encoding="utf-8"))[
                "spend_ledger"
            ]["actions"][0]
            self.assertEqual("WAITING", retained["state"])
            self.assertEqual("resp_exact_active", retained["provider"]["id"])

    def test_reported_and_reconciled_provider_evidence_is_not_outstanding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.state(root, status="AUTHORING_COMPLETE")
            binding = {
                "run_id": state["run_id"], "profile_sha256": "1" * 64,
                "prepared_state_revision": 9, "stage": "polish",
                "route": "ella:polish:001", "request_sha256": "2" * 64,
                "model": "gpt-5.6", "service_level": "batch",
                "maximum_output_tokens": 8000, "commitment_micro_usd": 125000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            state["spend_ledger"] = {
                "actions": [{
                    "action_id": "paid_0123456789abcdef01234567",
                    "state": "REPORTED", "binding": binding,
                    "authorization": {},
                    "consumption": {"consumer_id": "worker", "state_revision": 10},
                    "provider": {"kind": "response", "id": "resp_exact_reported"},
                    "reported": {"usage": {}, "estimated_micro_usd": 5000},
                    "reconciliation_reference_ids": ["billing-ref-001"],
                }],
                "reconciliation_references": [{
                    "reference_id": "billing-ref-001",
                    "action_id": "paid_0123456789abcdef01234567",
                    "authority": "astrowoof-api",
                    "amount_micro_usd": 4900,
                }],
            }
            self.materialize(root, state)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T22:00:00Z",
            )
            action = inspection["action_inventory"]["actions"][0]
            self.assertEqual("resp_exact_reported", action["provider_operation_id"])
            self.assertFalse(action["necessary"])
            self.assertFalse(inspection["terminal"]["provider_continuation_remains"])
            result = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            self.assertEqual([], result["unresolved_action_ids"])
            self.assertEqual("continuation_required", result["disposition"])

    def test_inspection_and_closeout_decision_basis_correlate_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root, self.state(root, status="AUTHORING_COMPLETE"))
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T22:00:00Z",
            )
            result = closeout_run(root, observed_at="2026-08-13T22:00:00Z")
            observed = inspection["observation"]
            basis = result["decision_basis"]
            for field in (
                "operator_state_revision", "snapshot_sha256",
                "logical_workspace_root", "snapshot_complete", "inventory_valid",
                "observed_at", "writer_race_possible",
            ):
                self.assertEqual(observed[field], basis[field], field)
            self.assertEqual("declared", observed["native_exclusive_access"])
            self.assertEqual("established", basis["native_exclusive_access"])
            self.assertEqual("run_closeout_001", result["run_id"])


if __name__ == "__main__":
    unittest.main()
