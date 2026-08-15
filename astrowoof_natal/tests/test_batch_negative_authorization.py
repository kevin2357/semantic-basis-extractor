from __future__ import annotations

import copy
import hashlib
import inspect
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    load_json,
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    _locked_batch_denial_preflight,
    closeout_run,
    deny_providerless_actions,
    deny_providerless_action,
    inspect_lifecycle,
    reconcile_required_providerless_denial,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter  # noqa: E402
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal.tests.test_lifecycle_contracts import validate  # noqa: E402


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


class TestBatchNegativeAuthorizationPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(read_resource_text(
            "contracts/authoring-lifecycle-contracts.schema.json"
        ))

    def binding(self, run_id: str, attempt: int) -> dict:
        return {
            "run_id": run_id,
            "profile_sha256": "1" * 64,
            "prepared_state_revision": 20 + attempt,
            "stage": "creative_retry",
            "route": f"ella:creative_retry:{attempt:03d}",
            "request_sha256": str(attempt) * 64,
            "model": "gpt-5.6",
            "service_level": "interactive",
            "maximum_output_tokens": 4000,
            "commitment_micro_usd": 50000,
            "price_book_version": "openai-public-2026-08-07.v1",
        }

    def materialize(self, root: Path) -> tuple[dict, list[dict]]:
        deck = root / "final" / "ella" / "deck.json"
        deck.parent.mkdir(parents=True)
        deck.write_text('{"accepted":true}\n', encoding="utf-8")
        delivery = root / "final" / "ella" / "delivery.zip"
        delivery.write_bytes(b"accepted-batch-preflight-delivery")
        run_id = "run_batch_preflight_001"
        actions = []
        for attempt, action_id in (
            (1, "paid_111111111111111111111111"),
            (2, "paid_222222222222222222222222"),
        ):
            binding = self.binding(run_id, attempt)
            actions.append({
                "action_id": action_id,
                "state": "AUTHORIZED",
                "binding": binding,
                "authorization": {
                    "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                    "action_id": action_id,
                    "binding": copy.deepcopy(binding),
                    "authorization_reference": f"api-slot-{attempt:03d}",
                },
                "provider": None,
                "reported": None,
            })
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": run_id,
            "state_revision": 23,
            "status": "DELIVERY_COMPLETE",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": actions},
            "passes": {},
            "subjects": {"ella": {
                "state": "DELIVERY_COMPLETE", "deck": str(deck),
                "delivery": str(delivery),
            }},
        }
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        inspection = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="2026-08-15T20:00:00Z",
        )
        members = [{
            "action_id": action["action_id"],
            "binding": copy.deepcopy(action["binding"]),
            "denial_reason": "reservation_unavailable",
            "external_authority_reference": f"api-fence:{index}",
        } for index, action in enumerate(actions, start=1)]
        request = {
            "schema_version": BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
            "run_id": run_id,
            "observed": inspection["observation"],
            "actions": members,
        }
        return request, actions

    def assert_refusal_is_unchanged(
        self, root: Path, request: dict, expected: str,
    ) -> dict:
        before = tree_hashes(root)
        result = _locked_batch_denial_preflight(root, request)
        self.assertEqual(before, tree_hashes(root))
        self.assertFalse(result["applied"])
        self.assertEqual(expected, result["outcome"])
        self.assertNotIn("result_checkpoint", result)
        validate(result, self.schema, self.schema)
        return result

    def test_two_terminal_actions_pass_one_locked_preflight_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            before = tree_hashes(root)
            result = _locked_batch_denial_preflight(
                root, request, decision_at="2026-08-15T20:00:01Z"
            )
            self.assertEqual(before, tree_hashes(root))
            self.assertTrue(result["eligible"])
            self.assertEqual(
                [item["action_id"] for item in request["actions"]],
                result["action_ids"],
            )
            self.assertEqual("established", result["decision_basis"]["native_exclusive_access"])

    def test_required_external_batch_denial_terminalizes_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state = load_json(root / "run.json")
            state["status"] = "AUTHORING"
            state["subjects"] = {}
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            observed = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T22:10:00Z",
            )
            request["observed"] = copy.deepcopy(observed["observation"])
            for member in request["actions"]:
                member["denial_reason"] = "external_authority_denied"

            result = deny_providerless_actions(root, request)
            replay = deny_providerless_actions(root, request)
            after = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T22:10:01Z",
            )
            closeout = closeout_run(root, observed_at="2026-08-15T22:10:02Z")
            persisted = load_json(root / "run.json")

            self.assertEqual("applied", result["outcome"])
            self.assertEqual("idempotent_replay", replay["outcome"])
            self.assertEqual(
                ["DENIED_PROVIDERLESS", "DENIED_PROVIDERLESS"],
                [item["state"] for item in persisted["spend_ledger"]["actions"]],
            )
            self.assertEqual("BUDGET_EXHAUSTED", persisted["status"])
            self.assertEqual(
                [item["action_id"] for item in request["actions"]],
                result["run_transition"]["denied_action_ids"],
            )
            self.assertEqual(
                [item["action_id"] for item in request["actions"]],
                result["run_transition"]["required_action_ids"],
            )
            self.assertFalse(after["terminal"]["provider_continuation_remains"])
            self.assertFalse(after["terminal"]["local_continuation_remains"])
            self.assertEqual("closed", closeout["disposition"])
            self.assertEqual([], closeout["unresolved_action_ids"])

    def test_retained_legacy_batch_denial_reconciles_as_one_causal_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state = load_json(root / "run.json")
            state["status"] = "AUTHORING"
            state["subjects"] = {}
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            request["observed"] = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T22:15:00Z",
            )["observation"]
            deny_providerless_actions(
                root, request, decision_at="2026-08-15T22:15:01Z"
            )

            # Downgrade only the terminal interpretation to its exact 0.4.1
            # representation; retain the original batch request and evidence.
            state = load_json(root / "run.json")
            state.pop("terminal_transition", None)
            state["status"] = "AUTHORING"
            record = next(iter(state["providerless_denial_batches"].values()))
            record.pop("run_transition", None)
            for action in state["spend_ledger"]["actions"]:
                action["negative_authorization"].pop("run_transition", None)
            artifact_path = root / record["result_artifact"]
            artifact = load_json(artifact_path)
            artifact.pop("run_transition", None)
            artifact_path.write_text(
                json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
            )
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)

            reconciled = reconcile_required_providerless_denial(
                root, reconciled_at="2026-08-15T22:15:02Z"
            )
            action_ids = [item["action_id"] for item in request["actions"]]
            self.assertEqual("BUDGET_EXHAUSTED", reconciled["status"])
            self.assertEqual(
                action_ids,
                reconciled["terminal_transition"]["denied_action_ids"],
            )
            self.assertEqual(
                action_ids,
                reconciled["terminal_transition"]["required_action_ids"],
            )
            self.assertEqual(
                1,
                len(reconciled["required_denial_reconciliation"]["action_evidence"]),
            )

    def test_mixed_required_policy_reason_precedes_spend_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state = load_json(root / "run.json")
            state["status"] = "AUTHORING"
            state["subjects"] = {}
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(root)
            request["observed"] = inspect_lifecycle(
                root, native_exclusive_access="declared"
            )["observation"]
            request["actions"][0]["denial_reason"] = "external_authority_denied"
            request["actions"][1]["denial_reason"] = "product_policy_denied"
            result = deny_providerless_actions(root, request)
            self.assertEqual("POLICY_STOPPED", load_json(root / "run.json")["status"])
            self.assertEqual("policy_stopped", result["run_transition"]["terminal_outcome"])
            self.assertEqual(
                "external_product_policy_denied",
                result["run_transition"]["terminal_reason"],
            )

    def test_stale_observation_refuses_all_as_not_evaluated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state = load_json(root / "run.json")
            state["state_revision"] += 1
            (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(root)
            result = self.assert_refusal_is_unchanged(root, request, "stale_observation")
            self.assertEqual({"not_evaluated"}, {item["outcome"] for item in result["actions"]})

    def test_one_ineligible_member_refuses_all_with_zero_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state = load_json(root / "run.json")
            state["spend_ledger"]["actions"][1]["state"] = "BUDGET_EXHAUSTED"
            (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(root)
            request["observed"] = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:00:02Z",
            )["observation"]
            result = self.assert_refusal_is_unchanged(root, request, "action_ineligible")
            self.assertEqual(["eligible", "action_ineligible"], [
                item["outcome"] for item in result["actions"]
            ])

    def test_duplicate_unknown_and_binding_mismatch_are_typed(self) -> None:
        for case, expected in (
            ("duplicate", "duplicate_action"),
            ("unknown", "unknown_action"),
            ("binding", "immutable_binding_mismatch"),
            ("run", "immutable_binding_mismatch"),
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                request, _ = self.materialize(root)
                if case == "duplicate":
                    request["actions"][1] = copy.deepcopy(request["actions"][0])
                elif case == "unknown":
                    request["actions"][1]["action_id"] = "paid_aaaaaaaaaaaaaaaaaaaaaaaa"
                elif case == "binding":
                    request["actions"][1]["binding"]["maximum_output_tokens"] += 1
                else:
                    request["run_id"] = "different-native-run"
                result = self.assert_refusal_is_unchanged(root, request, expected)
                self.assertIn(expected, {item["outcome"] for item in result["actions"]})

    def test_provider_safety_evidence_precedes_shared_staleness(self) -> None:
        cases = (
            ("consumption", "consumption_evidence_appeared"),
            ("identity", "provider_identity_appeared"),
            ("reported", "provider_evidence_appeared"),
            ("ambiguous", "ambiguous_submission_boundary"),
        )
        for case, expected in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                request, _ = self.materialize(root)
                state = load_json(root / "run.json")
                action = state["spend_ledger"]["actions"][1]
                if case == "consumption":
                    action["consumption"] = {"consumer_id": "worker", "state_revision": 24}
                elif case == "identity":
                    action["provider"] = {"kind": "response", "id": "resp_existing"}
                elif case == "reported":
                    action["reported"] = {"usage": {}, "estimated_micro_usd": 10}
                else:
                    action["state"] = "SUBMITTING"
                state["state_revision"] += 1
                (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                write_workspace_snapshot(root)
                result = self.assert_refusal_is_unchanged(root, request, expected)
                self.assertIn(expected, {item["outcome"] for item in result["actions"]})

    def test_invalid_snapshot_and_lock_contention_fail_closed(self) -> None:
        class RefusingLock:
            def __enter__(self):
                raise BlockingIOError("held")

            def __exit__(self, *_args):
                return None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            (root / "unexpected.json").write_text("{}\n", encoding="utf-8")
            invalid = self.assert_refusal_is_unchanged(
                root, request, "native_state_inconsistent"
            )
            self.assertEqual(
                {"not_evaluated"}, {item["outcome"] for item in invalid["actions"]}
            )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            before = tree_hashes(root)
            with mock.patch(
                "astrowoof_natal_authoring.lifecycle._exclusive_lifecycle_lock",
                return_value=RefusingLock(),
            ):
                result = _locked_batch_denial_preflight(root, request)
            self.assertEqual(before, tree_hashes(root))
            self.assertEqual("exclusivity_not_established", result["outcome"])
            validate(result, self.schema, self.schema)

    def test_malformed_request_is_programmer_error_before_workspace_access(self) -> None:
        malformed = {
            "schema_version": BATCH_NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
            "run_id": "run",
            "observed": {},
            "actions": [],
        }
        with self.assertRaisesRegex(ValueError, "observed"):
            _locked_batch_denial_preflight(Path("does-not-exist"), malformed)

    def test_two_actions_apply_in_one_revision_and_preserve_terminal_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            state_before = load_json(root / "run.json")
            deck = root / "final" / "ella" / "deck.json"
            delivery = root / "final" / "ella" / "delivery.zip"
            accepted_before = (hashlib.sha256(deck.read_bytes()).hexdigest(),
                               hashlib.sha256(delivery.read_bytes()).hexdigest())
            result = deny_providerless_actions(
                root, request, decision_at="2026-08-15T20:00:01Z"
            )
            validate(result, self.schema, self.schema)
            self.assertTrue(result["applied"])
            self.assertEqual("applied", result["outcome"])
            self.assertEqual(["applied", "applied"], [
                item["outcome"] for item in result["actions"]
            ])
            self.assertTrue(all(item["release_eligible"] for item in result["actions"]))
            state = load_json(root / "run.json")
            self.assertEqual(state_before["state_revision"] + 1, state["state_revision"])
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertEqual(
                ["DENIED_PROVIDERLESS", "DENIED_PROVIDERLESS"],
                [item["state"] for item in state["spend_ledger"]["actions"]],
            )
            self.assertTrue(all(
                item["authorization"] is not None
                and item["negative_authorization"]["authorization_previously_recorded"]
                for item in state["spend_ledger"]["actions"]
            ))
            digest = result["batch_request_sha256"]
            self.assertIn(digest, state["providerless_denial_batches"])
            self.assertTrue(all(
                item["negative_authorization"]["batch_request_sha256"] == digest
                for item in state["spend_ledger"]["actions"]
            ))
            self.assertEqual(result["result_checkpoint"]["operator_state_revision"],
                             result["post_mutation_observation"]["operator_state_revision"])
            self.assertEqual(result["result_checkpoint"]["snapshot_sha256"],
                             result["post_mutation_observation"]["snapshot_sha256"])
            self.assertEqual(accepted_before, (
                hashlib.sha256(deck.read_bytes()).hexdigest(),
                hashlib.sha256(delivery.read_bytes()).hexdigest(),
            ))

    def test_exact_replay_is_byte_stable_and_preserves_shared_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            first = deny_providerless_actions(root, request)
            before = tree_hashes(root)
            replay = deny_providerless_actions(root, request)
            self.assertEqual(before, tree_hashes(root))
            validate(replay, self.schema, self.schema)
            self.assertFalse(replay["applied"])
            self.assertEqual("idempotent_replay", replay["outcome"])
            self.assertEqual({"idempotent_replay"}, {
                item["outcome"] for item in replay["actions"]
            })
            self.assertEqual(first["batch_request_sha256"], replay["batch_request_sha256"])
            self.assertEqual(first["decision_basis"], replay["decision_basis"])
            self.assertEqual(first["result_checkpoint"], replay["result_checkpoint"])
            self.assertEqual(
                first["post_mutation_observation"], replay["post_mutation_observation"]
            )

    def test_changed_reordered_and_partial_requests_are_not_exact_replay(self) -> None:
        mutations = ("reordered", "reason", "authority", "partial")
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                request, _ = self.materialize(root)
                deny_providerless_actions(root, request)
                changed = copy.deepcopy(request)
                if mutation == "reordered":
                    changed["actions"].reverse()
                elif mutation == "reason":
                    changed["actions"][0]["denial_reason"] = "product_policy_denied"
                elif mutation == "authority":
                    changed["actions"][0]["external_authority_reference"] += ":changed"
                else:
                    changed["actions"] = changed["actions"][:1]
                before = tree_hashes(root)
                result = deny_providerless_actions(root, changed)
                self.assertEqual(before, tree_hashes(root))
                self.assertFalse(result["applied"])
                self.assertNotEqual("idempotent_replay", result["outcome"])
                self.assertEqual("action_ineligible", result["outcome"])
                validate(result, self.schema, self.schema)

    def test_unrelated_action_is_unchanged_and_no_provider_surface_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, actions = self.materialize(root)
            state = load_json(root / "run.json")
            unrelated = copy.deepcopy(actions[0])
            unrelated["action_id"] = "paid_aaaaaaaaaaaaaaaaaaaaaaaa"
            unrelated["binding"]["route"] = "ella:qualitative_critic:001"
            unrelated["binding"]["stage"] = "qualitative_critic"
            unrelated["binding"]["request_sha256"] = "a" * 64
            unrelated["authorization"]["action_id"] = unrelated["action_id"]
            unrelated["authorization"]["binding"] = copy.deepcopy(unrelated["binding"])
            state["spend_ledger"]["actions"].append(unrelated)
            (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(root)
            request["observed"] = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:00:02Z",
            )["observation"]
            result = deny_providerless_actions(root, request)
            self.assertTrue(result["applied"])
            retained = load_json(root / "run.json")["spend_ledger"]["actions"][2]
            self.assertEqual("AUTHORIZED", retained["state"])
            self.assertNotIn("provider", inspect.signature(deny_providerless_actions).parameters)

    def test_crash_restart_recovers_every_batch_write_boundary(self) -> None:
        points = (
            "after_artifact_staged", "after_state_persisted",
            "after_artifact_promoted", "after_snapshot_published",
        )
        for point in points:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                request, _ = self.materialize(root)

                def fail(observed: str) -> None:
                    if observed == point:
                        raise RuntimeError(f"injected:{point}")

                with self.assertRaisesRegex(RuntimeError, f"injected:{point}"):
                    deny_providerless_actions(
                        root, request, decision_at="2026-08-15T20:00:03Z",
                        _failure_injector=fail,
                    )
                recovered = deny_providerless_actions(root, request)
                validate(recovered, self.schema, self.schema)
                self.assertIn(recovered["outcome"], {"applied", "idempotent_replay"})
                self.assertEqual(
                    ["DENIED_PROVIDERLESS", "DENIED_PROVIDERLESS"],
                    [item["state"] for item in load_json(root / "run.json")
                     ["spend_ledger"]["actions"]],
                )
                before_replay = tree_hashes(root)
                replay = deny_providerless_actions(root, request)
                self.assertEqual(before_replay, tree_hashes(root))
                self.assertEqual("idempotent_replay", replay["outcome"])

    def test_recovery_rejects_unrelated_or_changed_protocol_bytes(self) -> None:
        for mutation in (
            "unrelated", "missing_staged", "changed_staged",
            "missing_promoted", "changed_promoted",
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                request, _ = self.materialize(root)

                def fail(point: str) -> None:
                    expected_point = (
                        "after_artifact_promoted"
                        if mutation in {"missing_promoted", "changed_promoted"}
                        else "after_state_persisted"
                    )
                    if point == expected_point:
                        raise RuntimeError("injected")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    deny_providerless_actions(root, request, _failure_injector=fail)
                digest = hashlib.sha256(
                    json.dumps(request, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                staged = (root / "lifecycle" / "negative-authorization-batches" /
                          f".{digest}.json.tmp")
                promoted = staged.with_name(f"{digest}.json")
                if mutation == "unrelated":
                    (root / "unrelated.json").write_text("{}\n", encoding="utf-8")
                elif mutation == "missing_staged":
                    staged.unlink()
                elif mutation == "changed_staged":
                    staged.write_text('{"changed":true}\n', encoding="utf-8")
                elif mutation == "missing_promoted":
                    promoted.unlink()
                else:
                    promoted.write_text('{"changed":true}\n', encoding="utf-8")
                before = tree_hashes(root)
                with self.assertRaisesRegex(ValueError, "snapshot"):
                    deny_providerless_actions(root, request)
                self.assertEqual(before, tree_hashes(root))

    def test_competing_batch_and_single_calls_never_split_application(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            entered = threading.Event()
            release = threading.Event()
            original_persist = __import__(
                "astrowoof_natal_authoring.lifecycle", fromlist=["persist_state"]
            ).persist_state

            def blocking_persist(*args, **kwargs):
                entered.set()
                if not release.wait(timeout=10):
                    raise RuntimeError("test synchronization timeout")
                return original_persist(*args, **kwargs)

            first_result: list[dict] = []
            first_error: list[BaseException] = []

            def run_first() -> None:
                try:
                    first_result.append(deny_providerless_actions(root, request))
                except BaseException as exc:  # pragma: no cover - diagnostic capture
                    first_error.append(exc)

            with mock.patch(
                "astrowoof_natal_authoring.lifecycle.persist_state",
                side_effect=blocking_persist,
            ):
                worker = threading.Thread(target=run_first)
                worker.start()
                self.assertTrue(entered.wait(timeout=10))
                competing_batch = deny_providerless_actions(root, request)
                member = request["actions"][0]
                single_request = {
                    "schema_version": "astrowoof.provider_negative_authorization_request.v0.1",
                    "run_id": request["run_id"],
                    "action_id": member["action_id"],
                    "binding": copy.deepcopy(member["binding"]),
                    "observed": copy.deepcopy(request["observed"]),
                    "denial_reason": member["denial_reason"],
                    "external_authority_reference": member["external_authority_reference"],
                }
                competing_single = deny_providerless_action(root, single_request)
                release.set()
                worker.join(timeout=10)
            self.assertFalse(worker.is_alive())
            self.assertEqual([], first_error)
            self.assertEqual("exclusivity_not_established", competing_batch["outcome"])
            self.assertEqual("exclusivity_not_established", competing_single["outcome"])
            self.assertEqual("applied", first_result[0]["outcome"])
            self.assertEqual(
                ["DENIED_PROVIDERLESS", "DENIED_PROVIDERLESS"],
                [item["state"] for item in load_json(root / "run.json")
                 ["spend_ledger"]["actions"]],
            )
            replay = deny_providerless_actions(root, request)
            self.assertEqual("idempotent_replay", replay["outcome"])

    def test_batch_events_are_ordered_replay_safe_and_failure_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            delivered: list[dict] = []
            emitter = ExecutionEventEmitter(release="test", sink=delivered.append)
            applied = deny_providerless_actions(root, request, event_emitter=emitter)
            self.assertTrue(applied["applied"])
            self.assertEqual([
                "authorization.denied_providerless",
                "authorization.denied_providerless",
                "authorization.denied_providerless_batch",
            ], [item["event_name"] for item in delivered])
            self.assertEqual(
                [item["action_id"] for item in request["actions"]],
                [item["correlation"]["action_id"] for item in delivered[:2]],
            )
            self.assertTrue(all("binding" not in item["data"] for item in delivered))
            before_replay_events = len(delivered)
            replay = deny_providerless_actions(root, request, event_emitter=emitter)
            self.assertEqual("idempotent_replay", replay["outcome"])
            self.assertEqual(before_replay_events + 1, len(delivered))
            self.assertEqual(
                "authorization.denied_providerless_batch", delivered[-1]["event_name"]
            )
            self.assertEqual("idempotent_replay", delivered[-1]["data"]["outcome"])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)
            stale = copy.deepcopy(request)
            stale["observed"]["operator_state_revision"] -= 1
            refused_events: list[dict] = []
            refusal = deny_providerless_actions(
                root, stale,
                event_emitter=ExecutionEventEmitter(
                    release="test", sink=refused_events.append
                ),
            )
            self.assertEqual("stale_observation", refusal["outcome"])
            self.assertEqual(1, len(refused_events))
            self.assertEqual("stale_observation",
                             refused_events[0]["data"]["reason_category"])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            request, _ = self.materialize(root)

            def fail(_event):
                raise RuntimeError("sink unavailable")

            emitter = ExecutionEventEmitter(release="test", sink=fail)
            result = deny_providerless_actions(root, request, event_emitter=emitter)
            self.assertTrue(result["applied"])
            self.assertEqual(3, emitter.stats.dropped)
            self.assertEqual(
                ["DENIED_PROVIDERLESS", "DENIED_PROVIDERLESS"],
                [item["state"] for item in load_json(root / "run.json")
                 ["spend_ledger"]["actions"]],
            )


if __name__ == "__main__":
    unittest.main()
