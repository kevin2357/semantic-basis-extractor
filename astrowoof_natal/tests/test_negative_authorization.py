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
    closeout_run,
    deny_providerless_action,
    inspect_lifecycle,
    reconcile_required_providerless_denial,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter  # noqa: E402
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

    def downgrade_to_legacy_denial(self, root: Path) -> dict:
        """Rewrite a current denial to the exact retained 0.4.1 evidence shape."""
        state = load_json(root / "run.json")
        action = state["spend_ledger"]["actions"][0]
        denial = action["negative_authorization"]
        denial.pop("run_transition", None)
        state.pop("terminal_transition", None)
        state["status"] = "AUTHORING"
        artifact = {
            "schema_version": "astrowoof.provider_negative_authorization_record.v0.1",
            "run_id": state["run_id"],
            "action_id": action["action_id"],
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
        artifact_path = root / denial["result_artifact"]
        artifact_path.write_text(
            json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
        )
        self.materialize_state(root, state)
        return state

    def materialize_legacy_denial(self, root: Path) -> dict:
        request = self.materialize(root)
        deny_providerless_action(
            root, request, decision_at="2026-08-13T21:00:01Z"
        )
        return self.downgrade_to_legacy_denial(root)

    def test_retained_required_denial_reconciles_and_closeout_is_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            legacy = self.materialize_legacy_denial(root)
            result = reconcile_required_providerless_denial(
                root, reconciled_at="2026-08-15T12:00:00Z"
            )
            self.assertEqual(legacy["state_revision"] + 1, result["state_revision"])
            self.assertEqual("BUDGET_EXHAUSTED", result["status"])
            self.assertEqual(
                "external_spend_reservation_unavailable",
                result["terminal_transition"]["terminal_reason"],
            )
            self.assertEqual(
                ["paid_0123456789abcdef01234567"],
                result["terminal_transition"]["required_action_ids"],
            )
            artifact = root / result["required_denial_reconciliation"]["result_artifact"]
            self.assertTrue(artifact.is_file())
            before = tree_hashes(root)
            replay = reconcile_required_providerless_denial(
                root, reconciled_at="2026-08-15T12:01:00Z"
            )
            self.assertEqual(result, replay)
            self.assertEqual(before, tree_hashes(root))
            closed = closeout_run(
                root, observed_at="2026-08-15T12:02:00Z",
            )
            self.assertEqual("closed", closed["disposition"])
            self.assertTrue(closed["terminal"]["terminal"])
            self.assertEqual([], closed["local_dependencies"])

    def test_closeout_automatically_reconciles_retained_denial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize_legacy_denial(root)
            closed = closeout_run(
                root, observed_at="2026-08-15T12:10:00Z",
            )
            self.assertEqual("closed", closed["disposition"])
            state = load_json(root / "run.json")
            self.assertEqual("BUDGET_EXHAUSTED", state["status"])
            self.assertIn("required_denial_reconciliation", state)

    def test_reconciliation_recovers_each_interrupted_write_boundary(self) -> None:
        points = (
            "after_reconciliation_artifact_staged",
            "after_reconciliation_state_persisted",
            "after_reconciliation_artifact_promoted",
            "after_reconciliation_snapshot_published",
        )
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary).resolve()
            for index, point in enumerate(points):
                root = parent / str(index)
                root.mkdir()
                self.materialize_legacy_denial(root)

                def fail(observed: str, expected: str = point) -> None:
                    if observed == expected:
                        raise RuntimeError(expected)

                with self.assertRaisesRegex(RuntimeError, point):
                    reconcile_required_providerless_denial(
                        root, reconciled_at="2026-08-15T12:20:00Z",
                        _failure_injector=fail,
                    )
                recovered = reconcile_required_providerless_denial(
                    root, reconciled_at="2026-08-15T12:20:00Z"
                )
                self.assertEqual("BUDGET_EXHAUSTED", recovered["status"])
                inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-15T12:21:00Z",
                )

    def test_reconciliation_fails_closed_on_changed_native_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.materialize_legacy_denial(root)
            action = state["spend_ledger"]["actions"][0]
            artifact_path = root / action["negative_authorization"]["result_artifact"]
            artifact = load_json(artifact_path)
            artifact["external_authority_reference"] = "tampered"
            artifact_path.write_text(
                json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            before = tree_hashes(root)
            with self.assertRaisesRegex(ValueError, "evidence is inconsistent"):
                reconcile_required_providerless_denial(root)
            self.assertEqual(before, tree_hashes(root))

    def test_reconciliation_fails_closed_if_provider_evidence_appeared(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.materialize_legacy_denial(root)
            state["spend_ledger"]["actions"][0]["provider"] = {
                "provider": "openai", "response_id": "resp_late_evidence"
            }
            self.materialize_state(root, state)
            before = tree_hashes(root)
            with self.assertRaisesRegex(ValueError, "provider evidence"):
                reconcile_required_providerless_denial(root)
            self.assertEqual(before, tree_hashes(root))

    def test_interrupted_reconciliation_rejects_unrelated_workspace_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize_legacy_denial(root)

            def fail(point: str) -> None:
                if point == "after_reconciliation_state_persisted":
                    raise RuntimeError(point)

            with self.assertRaisesRegex(RuntimeError, "state_persisted"):
                reconcile_required_providerless_denial(
                    root, reconciled_at="2026-08-15T12:30:00Z",
                    _failure_injector=fail,
                )
            (root / "unrelated.txt").write_text("unexpected\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                reconcile_required_providerless_denial(root)

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

    def test_required_external_denial_terminalizes_native_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = self.base_state(root)
            state["status"] = "AUTHORING"
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "AUTHORIZED"
            action["binding"]["stage"] = "creative_retry"
            action["binding"]["route"] = "ella:creative_retry:002"
            action["authorization"] = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "authorization_reference": "api-slot-required-single",
            }
            self.materialize_state(root, state)
            before = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T22:00:00Z",
            )
            self.assertTrue(before["action_inventory"]["actions"][0]["necessary"])
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"],
                "action_id": action["action_id"],
                "binding": copy.deepcopy(action["binding"]),
                "observed": copy.deepcopy(before["observation"]),
                "denial_reason": "external_authority_denied",
                "external_authority_reference": "api-global:required-single",
            }
            result = deny_providerless_action(root, request)
            persisted = load_json(root / "run.json")
            after = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T22:00:01Z",
            )
            closeout = closeout_run(root, observed_at="2026-08-15T22:00:02Z")

            self.assertEqual("applied", result["outcome"])
            self.assertEqual("DENIED_PROVIDERLESS", persisted["spend_ledger"]["actions"][0]["state"])
            self.assertEqual("BUDGET_EXHAUSTED", persisted["status"])
            self.assertEqual(
                "external_spend_authority_denied",
                persisted["terminal_transition"]["terminal_reason"],
            )
            public = load_json(root / "public-run.json")
            self.assertEqual("BUDGET_EXHAUSTED", public["status"])
            self.assertEqual("budget_exhausted", public["terminal"]["outcome"])
            self.assertEqual(
                "external_spend_authority_denied", public["terminal"]["reason"]
            )
            self.assertEqual(
                [action["action_id"]], result["run_transition"]["denied_action_ids"]
            )
            self.assertEqual(
                [action["action_id"]], result["run_transition"]["required_action_ids"]
            )
            self.assertFalse(after["action_inventory"]["actions"][0]["necessary"])
            self.assertEqual("budget_exhausted", after["terminal"]["outcome"])
            self.assertFalse(after["terminal"]["provider_continuation_remains"])
            self.assertFalse(after["terminal"]["local_continuation_remains"])
            self.assertEqual([], after["local_dependencies"])
            self.assertEqual("closed", closeout["disposition"])
            self.assertEqual([], closeout["unresolved_action_ids"])
            self.assertTrue(closeout["terminal"]["terminal"])

    def test_required_product_policy_denial_uses_policy_stopped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root, authorized=True)
            request["denial_reason"] = "product_policy_denied"
            result = deny_providerless_action(root, request)
            state = load_json(root / "run.json")
            self.assertEqual("POLICY_STOPPED", state["status"])
            self.assertEqual("policy_stopped", result["run_transition"]["terminal_outcome"])
            self.assertEqual(
                "external_product_policy_denied",
                result["run_transition"]["terminal_reason"],
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

    def test_terminal_two_action_sequential_denial_reproduces_stale_seam(self) -> None:
        """Freeze the API-reported pre-batch behavior as a regression baseline."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            deck = root / "final" / "ella" / "deck.json"
            deck.parent.mkdir(parents=True)
            deck.write_text('{"accepted":true}\n', encoding="utf-8")
            delivery = root / "final" / "ella" / "delivery.zip"
            delivery.write_bytes(b"accepted-terminal-delivery")

            state = self.base_state(root)
            state["status"] = "DELIVERY_COMPLETE"
            state["subjects"] = {"ella": {
                "state": "DELIVERY_COMPLETE",
                "deck": str(deck),
                "delivery": str(delivery),
            }}
            first = state["spend_ledger"]["actions"][0]
            first["state"] = "AUTHORIZED"
            first["binding"]["stage"] = "creative_retry"
            first["binding"]["route"] = "ella:creative_retry:001"
            first["authorization"] = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": first["action_id"],
                "binding": copy.deepcopy(first["binding"]),
                "authorization_reference": "api-slot-001",
            }
            second = copy.deepcopy(first)
            second["action_id"] = "paid_abcdefabcdefabcdefabcdef"
            second["binding"]["route"] = "ella:creative_retry:002"
            second["binding"]["request_sha256"] = "3" * 64
            second["authorization"]["action_id"] = second["action_id"]
            second["authorization"]["binding"] = copy.deepcopy(second["binding"])
            second["authorization"]["authorization_reference"] = "api-slot-002"
            state["spend_ledger"]["actions"].append(second)
            self.materialize_state(root, state)

            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T18:00:00Z",
            )
            self.assertEqual("delivery_complete", inspection["terminal"]["outcome"])
            self.assertEqual(2, len(inspection["action_inventory"]["actions"]))
            self.assertTrue(all(
                item["providerless_denial_eligible"]
                for item in inspection["action_inventory"]["actions"]
            ))
            accepted_before = (hashlib.sha256(deck.read_bytes()).hexdigest(),
                               hashlib.sha256(delivery.read_bytes()).hexdigest())

            def request_for(action: dict, authority: str) -> dict:
                return {
                    "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                    "run_id": state["run_id"],
                    "action_id": action["action_id"],
                    "binding": copy.deepcopy(action["binding"]),
                    "observed": copy.deepcopy(inspection["observation"]),
                    "denial_reason": "reservation_unavailable",
                    "external_authority_reference": authority,
                }

            first_request = request_for(first, "api-fence:slot-001")
            second_request = request_for(second, "api-fence:slot-002")
            first_result = deny_providerless_action(root, first_request)
            first_replay = deny_providerless_action(root, first_request)
            before_stale = tree_hashes(root)
            second_result = deny_providerless_action(root, second_request)

            self.assertEqual("applied", first_result["outcome"])
            self.assertEqual("idempotent_replay", first_replay["outcome"])
            self.assertEqual("stale_observation", second_result["outcome"])
            self.assertFalse(second_result["applied"])
            self.assertEqual(before_stale, tree_hashes(root))
            actions = load_json(root / "run.json")["spend_ledger"]["actions"]
            self.assertEqual(
                ["DENIED_PROVIDERLESS", "AUTHORIZED"],
                [item["state"] for item in actions],
            )
            self.assertEqual(accepted_before, (
                hashlib.sha256(deck.read_bytes()).hexdigest(),
                hashlib.sha256(delivery.read_bytes()).hexdigest(),
            ))

    def test_applied_denial_emits_bounded_non_authoritative_event(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request = self.materialize(root)
            delivered = []
            emitter = ExecutionEventEmitter(release="test", sink=delivered.append)
            result = deny_providerless_action(root, request, event_emitter=emitter)
            self.assertTrue(result["applied"])
            self.assertEqual([
                "authorization.denied_providerless", "terminal.transitioned",
            ], [item["event_name"] for item in delivered])
            self.assertTrue(all("binding" not in item["data"] for item in delivered))


if __name__ == "__main__":
    unittest.main()
