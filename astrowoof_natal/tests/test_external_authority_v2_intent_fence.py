from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests.test_external_authority_v2_contract import authority_inputs
from astrowoof_natal_authoring import (
    ExternalAuthorityV2ExecutionError,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    read_external_authority_intent_result_v2_schema,
    read_external_authority_provider_dispatch_result_v2_schema,
    validate_external_authority_intent_result_v2,
    validate_external_authority_provider_dispatch_result_v2,
)
from astrowoof_natal_authoring.closure import (
    load_json, validate_workspace_snapshot, write_workspace_snapshot,
)


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.name.endswith(".lock")
    }


class ExternalAuthorityV2IntentFenceSlice2(unittest.TestCase):
    def test_complete_grant_inventory_authorization_and_intent_commit_together(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
            result = commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            state = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, state)
            self.assertEqual("intent_committed", result["outcome"])
            self.assertEqual(
                "astrowoof.external_authority_intent_result.v2",
                result["schema_version"],
            )
            self.assertEqual(result, validate_external_authority_intent_result_v2(result))
            self.assertFalse(result["provider_io_performed"])
            self.assertEqual(request["ordered_action_ids"], result["ordered_action_ids"])
            intent = state["external_authority_v2_dispatch_intent"]
            self.assertEqual(grant["grant_sha256"], intent["grant_sha256"])
            self.assertEqual(request["ordered_action_ids"], intent["ordered_action_ids"])
            self.assertFalse(intent["provider_io_performed"])
            selected = [
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] in request["ordered_action_ids"]
            ]
            self.assertTrue(all(item["state"] == "SUBMITTING" for item in selected))
            self.assertTrue(all(item.get("authorization") for item in selected))
            self.assertTrue(all(item.get("consumption") for item in selected))

    def test_intent_result_schema_and_python_validator_reject_mutation(self):
        self.assertEqual(
            "astrowoof.external_authority_intent_result.v2",
            read_external_authority_intent_result_v2_schema()["$id"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
            result = commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            for key, value in (
                ("run_id", None),
                ("provider_io_performed", True),
                ("ordered_action_ids", list(reversed(result["ordered_action_ids"]))),
                ("result_sha256", "0" * 64),
            ):
                with self.subTest(key=key):
                    mutated = copy.deepcopy(result)
                    mutated[key] = value
                    with self.assertRaises(ValueError):
                        validate_external_authority_intent_result_v2(mutated)

    def test_failure_before_persistence_is_exactly_nonmutating(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
            before = hashes(run_dir)
            def fail(point):
                if point == "before_intent_persistence":
                    raise RuntimeError("injected-before-persist")
            with self.assertRaisesRegex(RuntimeError, "injected-before-persist"):
                commit_external_authority_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents, failure_injector=fail,
                )
            self.assertEqual(before, hashes(run_dir))


class ExternalAuthorityV2ProviderDispatchSlice3(unittest.TestCase):
    def prepared_intent(self, root: Path):
        run_dir, inspection, request, documents, grant = authority_inputs(root)
        commit_external_authority_v2_dispatch_intent(
            run_dir, request=request, inspection=inspection, grant=grant,
            authorization_documents=documents,
        )
        return run_dir, request, grant

    def test_each_identity_is_checkpointed_before_next_create_and_replay_is_exact(self):
        from astrowoof_natal_authoring.lifecycle import _exclusive_lifecycle_lock

        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            calls = []

            def create(action):
                # Slow provider I/O runs outside the native writer.
                with _exclusive_lifecycle_lock(run_dir):
                    pass
                if calls:
                    prior = load_json(run_dir / "run.json")["spend_ledger"]["actions"]
                    prior_action = next(item for item in prior if item["action_id"] == calls[-1])
                    self.assertTrue((prior_action.get("provider") or {}).get("id"))
                    validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))
                calls.append(action["action_id"])
                return {"kind": "response", "id": f"resp_{action['action_id']}"}

            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], create=create,
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(request["ordered_action_ids"], calls)
            self.assertEqual(result, validate_external_authority_provider_dispatch_result_v2(result))
            state = load_json(run_dir / "run.json")
            self.assertTrue(all(item["state"] == "WAITING" for item in state["spend_ledger"]["actions"]))
            self.assertEqual(2, state["external_authority_v2_dispatch_intent"]["next_action_index"])
            from astrowoof_natal_authoring import inspect_temporal_lifecycle
            lifecycle = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="established",
                observed_at="2099-01-01T00:00:00Z",
            )
            self.assertEqual("provider_reconciliation_cycle", lifecycle["temporal_decision"]["selected_command"])
            self.assertTrue(lifecycle["temporal_decision"]["eligible_now"])
            self.assertEqual(request["ordered_action_ids"], lifecycle["temporal_decision"]["due_action_ids"])

            replay = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: self.fail("replay attempted a provider create"),
            )
            self.assertEqual("exact_replay", replay["outcome"])
            self.assertFalse(replay["provider_io_performed"])
            self.assertEqual(request["ordered_action_ids"], calls)

    def test_entered_create_without_identity_is_ambiguous_and_stops_later_members(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            calls = []

            def create(action):
                calls.append(action["action_id"])
                raise TimeoutError("acceptance unknown")

            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], create=create,
            )
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual(request["ordered_action_ids"][:1], calls)
            self.assertEqual(calls, result["ambiguous_action_ids"])
            state = load_json(run_dir / "run.json")
            first = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == calls[0])
            self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", first["state"])
            validate_workspace_snapshot(run_dir, state)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"],
                    create=lambda action: self.fail("ambiguous replay created again"),
                )
            self.assertEqual("provider_submission_ambiguous", caught.exception.reason_code)

    def test_crash_after_first_identity_resumes_only_proven_unentered_member(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            calls = []

            def create(action):
                calls.append(action["action_id"])
                return {"id": f"resp_{action['action_id']}", "kind": "response"}

            def fail(point):
                if point == f"after_identity_checkpoint:{request['ordered_action_ids'][0]}":
                    raise RuntimeError("crash-after-durable-id")

            with self.assertRaisesRegex(RuntimeError, "crash-after-durable-id"):
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"], create=create,
                    failure_injector=fail,
                )
            state = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, state)
            self.assertEqual(1, state["external_authority_v2_dispatch_intent"]["next_action_index"])
            resumed = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], create=create,
            )
            self.assertEqual("detached_provider_pending", resumed["outcome"])
            self.assertEqual(request["ordered_action_ids"], calls)

    def test_crash_after_create_before_identity_becomes_nonreplayable(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            calls = []

            def create(action):
                calls.append(action["action_id"])
                return {"id": "resp_accepted", "kind": "response"}

            def fail(point):
                if point.startswith("after_provider_create_before_identity:"):
                    raise RuntimeError("crash-window")

            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], create=create,
                failure_injector=fail,
            )
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual(1, len(calls))
            with self.assertRaises(ExternalAuthorityV2ExecutionError):
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"], create=create,
                )
            self.assertEqual(1, len(calls))

    def test_process_style_interruption_leaves_durable_entered_fence(self):
        class SimulatedProcessExit(BaseException):
            pass

        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            calls = []

            def create(action):
                calls.append(action["action_id"])
                return {"id": "resp_returned_but_not_checkpointed", "kind": "response"}

            def fail(point):
                if point.startswith("after_provider_create_before_identity:"):
                    raise SimulatedProcessExit()

            with self.assertRaises(SimulatedProcessExit):
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"], create=create,
                    failure_injector=fail,
                )
            state = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, state)
            intent = state["external_authority_v2_dispatch_intent"]
            self.assertEqual(request["ordered_action_ids"][0], intent["active_action_id"])
            self.assertEqual("CALL_ENTERED", intent["active_create_state"])
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"], create=create,
                )
            self.assertEqual("provider_submission_ambiguous", caught.exception.reason_code)
            self.assertEqual(1, len(calls))

    def test_failure_before_create_entry_is_safely_resumable(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))

            def fail(point):
                if point.startswith("before_provider_create:"):
                    raise RuntimeError("before-entry")

            with self.assertRaisesRegex(RuntimeError, "before-entry"):
                dispatch_external_authority_v2_intent(
                    run_dir, request_sha256=request["external_authority_request_sha256"],
                    grant_sha256=grant["grant_sha256"],
                    create=lambda action: self.fail("provider call was entered"),
                    failure_injector=fail,
                )
            state = load_json(run_dir / "run.json")
            self.assertIsNone(state["external_authority_v2_dispatch_intent"]["active_action_id"])
            calls = []
            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: (
                    calls.append(action["action_id"])
                    or {"id": f"resp_{action['action_id']}", "kind": "response"}
                ),
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(request["ordered_action_ids"], calls)

    def test_competing_dispatch_after_create_entry_makes_zero_provider_calls(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            outer_calls = []
            competing_calls = []

            def create(action):
                outer_calls.append(action["action_id"])
                with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                    dispatch_external_authority_v2_intent(
                        run_dir,
                        request_sha256=request["external_authority_request_sha256"],
                        grant_sha256=grant["grant_sha256"],
                        create=lambda nested: competing_calls.append(nested["action_id"]),
                    )
                self.assertEqual("provider_submission_ambiguous", caught.exception.reason_code)
                self.assertEqual([], competing_calls)
                return {"id": f"resp_{action['action_id']}", "kind": "response"}

            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], create=create,
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(request["ordered_action_ids"], outer_calls)
            self.assertEqual([], competing_calls)

    def test_provider_dispatch_result_schema_is_packaged(self):
        self.assertEqual(
            "astrowoof.external_authority_provider_dispatch_result.v2",
            read_external_authority_provider_dispatch_result_v2_schema()["$id"],
        )

    def test_event_sink_failure_cannot_change_dispatch(self):
        from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter

        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            emitter = ExecutionEventEmitter(
                release="slice3",
                sink=lambda event: (_ for _ in ()).throw(RuntimeError("sink-down")),
            )
            calls = []
            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: (
                    calls.append(action["action_id"])
                    or {"id": f"resp_{action['action_id']}", "kind": "response"}
                ),
                event_emitter=emitter,
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(request["ordered_action_ids"], calls)
            self.assertGreater(emitter.stats.sink_warnings, 0)
            validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))

    def test_duplicate_provider_identity_is_durable_ambiguity(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, grant = self.prepared_intent(Path(temporary))
            result = dispatch_external_authority_v2_intent(
                run_dir, request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: {"id": "resp_duplicate", "kind": "response"},
            )
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual(request["ordered_action_ids"][:1], result["provider_bound_action_ids"])
            self.assertEqual(request["ordered_action_ids"][1:], result["ambiguous_action_ids"])
            state = load_json(run_dir / "run.json")
            second = next(
                item for item in state["spend_ledger"]["actions"]
                if item["action_id"] == request["ordered_action_ids"][1]
            )
            self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", second["state"])
            validate_workspace_snapshot(run_dir, state)

    def test_interruption_after_state_before_snapshot_is_invalid_but_not_partial(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
            def fail(point):
                if point == "after_state_before_snapshot":
                    raise RuntimeError("injected-after-state")
            with self.assertRaisesRegex(RuntimeError, "injected-after-state"):
                commit_external_authority_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents, failure_injector=fail,
                )
            state = load_json(run_dir / "run.json")
            with self.assertRaisesRegex(ValueError, "snapshot"):
                validate_workspace_snapshot(run_dir, state)
            self.assertEqual(request["ordered_action_ids"], state["external_authority_v2_dispatch_intent"]["ordered_action_ids"])
            selected = [item for item in state["spend_ledger"]["actions"] if item["action_id"] in request["ordered_action_ids"]]
            self.assertTrue(all(item["state"] == "SUBMITTING" for item in selected))
            self.assertTrue(all(item.get("authorization") and item.get("consumption") for item in selected))

    def test_stale_grant_and_changed_binding_refuse_without_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for mutation in ("grant", "binding"):
                with self.subTest(mutation=mutation):
                    case = root / mutation
                    case.mkdir()
                    run_dir, inspection, request, documents, grant = authority_inputs(case)
                    if mutation == "grant":
                        grant = copy.deepcopy(grant); grant["api_decision_id"] = "changed"
                    else:
                        state = load_json(run_dir / "run.json")
                        state["spend_ledger"]["actions"][0]["binding"]["model"] = "changed"
                        (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                        write_workspace_snapshot(run_dir)
                    before = hashes(run_dir)
                    with self.assertRaises(ExternalAuthorityV2ExecutionError):
                        commit_external_authority_v2_dispatch_intent(
                            run_dir, request=request, inspection=inspection, grant=grant,
                            authorization_documents=documents,
                        )
                    self.assertEqual(before, hashes(run_dir))

    def test_provider_evidence_and_ambiguity_take_precedence_over_staleness(self):
        for mode in ("provider", "ambiguous"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
                state = load_json(run_dir / "run.json")
                action = state["spend_ledger"]["actions"][0]
                if mode == "provider":
                    action["provider"] = {"kind": "response", "id": "resp_existing"}
                else:
                    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                write_workspace_snapshot(run_dir)
                before = hashes(run_dir)
                with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                    commit_external_authority_v2_dispatch_intent(
                        run_dir, request=request, inspection=inspection, grant=grant,
                        authorization_documents=documents,
                    )
                self.assertEqual(
                    "provider_evidence_present" if mode == "provider" else "provider_submission_ambiguous",
                    caught.exception.reason_code,
                )
                self.assertEqual(before, hashes(run_dir))

    def test_same_grant_replay_refuses_without_second_checkpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents, grant = authority_inputs(Path(temporary))
            commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            before = hashes(run_dir)
            with self.assertRaises(ExternalAuthorityV2ExecutionError) as caught:
                commit_external_authority_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents,
                )
            # SUBMITTING is a stronger safety classification than a stale/replay hint.
            self.assertEqual("provider_submission_ambiguous", caught.exception.reason_code)
            self.assertEqual(before, hashes(run_dir))


if __name__ == "__main__":
    unittest.main()
