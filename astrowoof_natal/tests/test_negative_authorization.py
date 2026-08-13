from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    load_json,
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    deny_providerless_action,
    inspect_lifecycle,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal.tests.test_lifecycle_contracts import validate  # noqa: E402


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


class TestNegativeAuthorization(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(read_resource_text(
            "contracts/authoring-lifecycle-contracts.schema.json"
        ))

    def base_state(self, root: Path) -> dict:
        binding = {
            "run_id": "run_inspection_001", "profile_sha256": "1" * 64,
            "prepared_state_revision": 7, "stage": "polish",
            "route": "ella:polish:002", "request_sha256": "2" * 64,
            "model": "gpt-5.6", "service_level": "batch",
            "maximum_output_tokens": 8000, "commitment_micro_usd": 125000,
            "price_book_version": "openai-public-2026-08-07.v1",
        }
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_inspection_001", "state_revision": 7,
            "status": "AWAITING_SPEND_AUTHORIZATION",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "PREPARED", "binding": binding,
                "authorization": None, "provider": None, "reported": None,
            }]},
            "passes": {}, "subjects": {},
        }

    def materialize_state(self, root: Path, state: dict) -> None:
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)

    def materialize(self, root: Path, *, authorized: bool = False) -> dict:
        state = self.base_state(root)
        action = state["spend_ledger"]["actions"][0]
        if authorized:
            action["state"] = "AUTHORIZED"
            action["authorization"] = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "authorization_reference": "api-reservation-fixture",
            }
        self.materialize_state(root, state)
        inspection = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="2026-08-13T21:00:00Z",
        )
        return {
            "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
            "run_id": state["run_id"],
            "action_id": action["action_id"],
            "binding": copy.deepcopy(action["binding"]),
            "observed": inspection["observation"],
            "denial_reason": "reservation_unavailable",
            "external_authority_reference": "api-fence:negative-fixture",
        }

    def test_prepared_denial_is_durable_schema_valid_and_provider_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            result = deny_providerless_action(
                root, request, decision_at="2026-08-13T21:00:01Z"
            )
            validate(result, self.schema, self.schema)
            self.assertTrue(result["applied"])
            self.assertEqual("DENIED_PROVIDERLESS", result["disposition"])
            self.assertFalse(result["authorization_previously_recorded"])
            state = load_json(root / "run.json")
            action = state["spend_ledger"]["actions"][0]
            self.assertEqual("DENIED_PROVIDERLESS", action["state"])
            artifact = root / result["result_checkpoint"]["result_artifact"]["logical_path"]
            self.assertTrue(artifact.is_file())
            followup = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T21:00:02Z",
            )
            self.assertEqual(
                "already_denied_providerless",
                followup["action_inventory"]["actions"][0]["eligibility_reason"],
            )

    def test_authorized_unconsumed_denial_preserves_authorization_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root, authorized=True)
            result = deny_providerless_action(root, request)
            self.assertTrue(result["applied"])
            self.assertTrue(result["authorization_previously_recorded"])
            action = load_json(root / "run.json")["spend_ledger"]["actions"][0]
            self.assertIsNotNone(action["authorization"])
            self.assertTrue(
                action["negative_authorization"]["authorization_previously_recorded"]
            )

    def test_replay_returns_same_semantic_disposition_without_second_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            first = deny_providerless_action(root, request)
            before = tree_hashes(root)
            second = deny_providerless_action(root, request)
            after = tree_hashes(root)
            self.assertEqual(before, after)
            self.assertEqual("idempotent_replay", second["outcome"])
            self.assertFalse(second["applied"])
            self.assertEqual(first["disposition"], second["disposition"])
            self.assertEqual(
                first["result_checkpoint"]["result_artifact"],
                second["result_checkpoint"]["result_artifact"],
            )
            validate(second, self.schema, self.schema)

    def test_stale_observation_is_typed_and_does_not_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            state = load_json(root / "run.json")
            state["state_revision"] += 1
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            before = tree_hashes(root)
            result = deny_providerless_action(root, request)
            after = tree_hashes(root)
            self.assertEqual(before, after)
            self.assertFalse(result["applied"])
            self.assertEqual("stale_observation", result["outcome"])
            self.assertNotIn("result_checkpoint", result)
            validate(result, self.schema, self.schema)

    def test_provider_identity_refusal_does_not_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.base_state(root)
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "WAITING"
            action["provider"] = {"kind": "response", "id": "resp_never_resubmit"}
            action["consumption"] = {"consumer_id": "worker", "state_revision": 8}
            self.materialize_state(root, state)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T21:00:00Z",
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"],
                "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:provider-fixture",
            }
            before = tree_hashes(root)
            result = deny_providerless_action(root, request)
            self.assertEqual(before, tree_hashes(root))
            self.assertFalse(result["applied"])
            self.assertIn(result["outcome"], {
                "provider_identity_appeared", "consumption_evidence_appeared"
            })
            self.assertEqual("resp_never_resubmit", load_json(root / "run.json")
                             ["spend_ledger"]["actions"][0]["provider"]["id"])

    def test_provider_identity_race_is_more_specific_than_stale_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root, authorized=True)
            state = load_json(root / "run.json")
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "PROVIDER_ID_RECORDED"
            action["consumption"] = {"consumer_id": "racing-worker", "state_revision": 8}
            action["provider"] = {"kind": "response", "id": "resp_race_won"}
            state["state_revision"] += 1
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            before = tree_hashes(root)
            result = deny_providerless_action(root, request)
            self.assertEqual(before, tree_hashes(root))
            self.assertEqual("consumption_evidence_appeared", result["outcome"])
            self.assertNotIn("result_checkpoint", result)

    def test_submitting_without_identity_is_ambiguous_and_never_denied(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.base_state(root)
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "SUBMITTING"
            self.materialize_state(root, state)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T21:00:00Z",
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"], "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:ambiguous",
            }
            result = deny_providerless_action(root, request)
            self.assertEqual("ambiguous_submission_boundary", result["outcome"])
            self.assertFalse(result["release_eligible"])
            self.assertEqual(
                "SUBMITTING",
                load_json(root / "run.json")["spend_ledger"]["actions"][0]["state"],
            )

    def test_binding_mismatch_and_unknown_denial_reason_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            mismatch = copy.deepcopy(request)
            mismatch["binding"]["maximum_output_tokens"] += 1
            before = tree_hashes(root)
            result = deny_providerless_action(root, mismatch)
            self.assertEqual("immutable_binding_mismatch", result["outcome"])
            self.assertEqual(before, tree_hashes(root))
            unsupported = copy.deepcopy(request)
            unsupported["denial_reason"] = "free_form_reason"
            with self.assertRaisesRegex(ValueError, "denial_reason"):
                deny_providerless_action(root, unsupported)

    def test_single_writer_lock_failure_is_typed_and_non_mutating(self) -> None:
        class RefusingLock:
            def __enter__(self):
                raise BlockingIOError("held")

            def __exit__(self, *_args):
                return None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            before = tree_hashes(root)
            with mock.patch(
                "astrowoof_natal_authoring.lifecycle._exclusive_lifecycle_lock",
                return_value=RefusingLock(),
            ):
                result = deny_providerless_action(root, request)
            self.assertEqual(before, tree_hashes(root))
            self.assertEqual("exclusivity_not_established", result["outcome"])
            self.assertFalse(result["applied"])

    def test_denial_targets_only_exact_action_in_multi_action_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.base_state(root)
            first = state["spend_ledger"]["actions"][0]
            second = copy.deepcopy(first)
            second["action_id"] = "paid_abcdefabcdefabcdefabcdef"
            second["binding"]["route"] = "ella:qualitative_critic:001"
            second["binding"]["stage"] = "qualitative_critic"
            second["binding"]["request_sha256"] = "3" * 64
            state["spend_ledger"]["actions"].append(second)
            self.materialize_state(root, state)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-13T21:00:00Z",
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"], "action_id": first["action_id"],
                "binding": copy.deepcopy(first["binding"]),
                "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:multi-action",
            }
            result = deny_providerless_action(root, request)
            self.assertTrue(result["applied"])
            actions = load_json(root / "run.json")["spend_ledger"]["actions"]
            self.assertEqual("DENIED_PROVIDERLESS", actions[0]["state"])
            self.assertEqual("PREPARED", actions[1]["state"])


if __name__ == "__main__":
    unittest.main()
