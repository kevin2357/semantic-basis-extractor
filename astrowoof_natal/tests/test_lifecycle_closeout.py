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
from astrowoof_natal_authoring.lifecycle import closeout_run  # noqa: E402
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


if __name__ == "__main__":
    unittest.main()
