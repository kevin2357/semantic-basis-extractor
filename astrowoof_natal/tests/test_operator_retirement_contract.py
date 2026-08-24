from __future__ import annotations

from copy import deepcopy
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path, write_workspace_snapshot,
)
from astrowoof_natal_authoring.operator_retirement import (  # noqa: E402
    assess_operator_retirement,
    build_operator_retirement_request,
    execute_operator_retirement,
    read_operator_retirement_schema,
    validate_operator_retirement_assessment,
    validate_operator_retirement_request,
    validate_operator_retirement_result,
    _sha256,
)
import astrowoof_natal_authoring as public  # noqa: E402
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    ExecutionEventEmitter,
)
from astrowoof_natal_authoring.native_transitions import (  # noqa: E402
    read_native_transition_result,
)


class TestOperatorRetirementContract(unittest.TestCase):
    def state(self, root: Path) -> dict:
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_retirement_fixture_001",
            "state_revision": 9,
            "status": "AWAITING_SPEND_AUTHORIZATION",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": []},
            "passes": {},
            "subjects": {},
        }

    def materialize(self, root: Path, state: dict | None = None) -> Path:
        root.mkdir(parents=True, exist_ok=True)
        (root / "run.json").write_text(
            json.dumps(state or self.state(root), indent=2) + "\n", encoding="utf-8",
        )
        write_workspace_snapshot(root)
        return root

    def test_build_and_dry_run_are_strict_and_nonmutating(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            before_run = (run / "run.json").read_bytes()
            before_snapshot = (run / "workspace-snapshot.json").read_bytes()
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:001",
                human_reason="Retire retained QA evidence",
            )
            result = assess_operator_retirement(run, request)
            self.assertEqual("eligible", result["outcome"])
            self.assertTrue(result["retirement_quiescent"])
            self.assertEqual([], result["failed_predicates"])
            self.assertFalse(result["mutation_performed"])
            self.assertFalse(result["native_result_published"])
            self.assertEqual(0, result["provider_io_performed_count"])
            self.assertEqual(before_run, (run / "run.json").read_bytes())
            self.assertEqual(before_snapshot, (run / "workspace-snapshot.json").read_bytes())
            validate_operator_retirement_request(request)
            validate_operator_retirement_assessment(result)

    def test_request_mutations_fail_semantic_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:002",
            )
            for field, value in (
                ("run_id", None),
                ("route_family", "bounded_natal"),
                ("reason_code", "whatever"),
                ("expected_snapshot_sha256", "NOPE"),
            ):
                with self.subTest(field=field):
                    changed = deepcopy(request)
                    changed[field] = value
                    with self.assertRaises(ValueError):
                        validate_operator_retirement_request(changed)

    def test_stale_request_refuses_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:003",
            )
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run)
            before = (run / "run.json").read_bytes()
            result = assess_operator_retirement(run, request)
            self.assertEqual("refused", result["outcome"])
            self.assertIn("stale_observation", result["failed_predicates"])
            self.assertTrue(result["retirement_quiescent"])
            self.assertEqual(before, (run / "run.json").read_bytes())

    def test_unresolved_providerless_action_must_be_denied_first(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "run"
            state = self.state(run.resolve())
            state["spend_ledger"]["actions"] = [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "PREPARED",
                "binding": {
                    "run_id": state["run_id"], "profile_sha256": "1" * 64,
                    "prepared_state_revision": 9, "stage": "creative_retry",
                    "route": "retry:1", "request_sha256": "2" * 64,
                    "model": "gpt-5.6", "service_level": "interactive",
                    "maximum_output_tokens": 1000, "commitment_micro_usd": 1000,
                    "price_book_version": "test.v1",
                },
                "authorization": None, "provider": None, "reported": None,
            }]
            self.materialize(run, state)
            with self.assertRaisesRegex(ValueError, "providerless_action_unresolved"):
                build_operator_retirement_request(
                    run, operator_audit_reference="api:retirement:004",
                )

    def test_denial_outcome_changes_closure_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            first = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:005",
            )
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"] = [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "DENIED_PROVIDERLESS",
                "denial": {"reason": "external_authority_denied"},
            }]
            (run / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run)
            second = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:006",
            )
            self.assertNotEqual(
                first["terminal_action_closure_sha256"],
                second["terminal_action_closure_sha256"],
            )

    def test_schema_is_packaged_shape_and_cli_dry_run(self) -> None:
        schema = read_operator_retirement_schema()
        self.assertIn("request", schema["$defs"])
        self.assertIn("assessment", schema["$defs"])
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run = self.materialize(base / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:007",
            )
            request_path = base / "request.json"
            request_path.write_text(json.dumps(request) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "astrowoof_natal_authoring.operator_retirement",
                 "--run-dir", str(run), "dry-run", "--request", str(request_path)],
                check=True, text=True, capture_output=True,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual("eligible", json.loads(completed.stdout)["outcome"])

    def test_public_exports_are_available(self) -> None:
        for name in (
            "assess_operator_retirement", "build_operator_retirement_request",
            "execute_operator_retirement",
            "read_operator_retirement_schema",
            "validate_operator_retirement_assessment",
            "validate_operator_retirement_request",
            "validate_operator_retirement_result",
        ):
            self.assertTrue(callable(getattr(public, name)))

    def test_packaged_public_fixtures_validate(self) -> None:
        request = json.loads(read_resource_text(
            "fixtures/operator-retirement/eligible-request.v1.json"
        ))
        assessment = json.loads(read_resource_text(
            "fixtures/operator-retirement/eligible-assessment.v1.json"
        ))
        validate_operator_retirement_request(request)
        validate_operator_retirement_assessment(assessment)

    def test_schema_validation_when_jsonschema_is_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency is unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:008",
            )
            assessment = assess_operator_retirement(run, request)
            schema = read_operator_retirement_schema()
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.validate(request, schema["$defs"]["request"])
            jsonschema.validate(assessment, schema["$defs"]["assessment"])

    def test_python_assessment_validator_rejects_primitive_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:primitive",
            )
            assessment = assess_operator_retirement(run, request)
            for field, value in (
                ("run_id", None), ("logical_workspace_root", ""),
                ("state_revision", True), ("route_family", "bounded_natal"),
                ("retirement_quiescent", "true"),
                ("mutation_performed", 0), ("native_result_published", None),
                ("provider_io_performed_count", False),
            ):
                with self.subTest(field=field):
                    changed = deepcopy(assessment)
                    changed[field] = value
                    with self.assertRaises(ValueError):
                        validate_operator_retirement_assessment(changed)

    def test_closed_nonterminal_status_set_is_representable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for status in (
                "AUTHORING", "AUTHORING_COMPLETE", "WAITING_FOR_RESPONSE",
                "AWAITING_SPEND_AUTHORIZATION",
            ):
                with self.subTest(status=status):
                    run = Path(temporary) / status.lower()
                    state = self.state(run.resolve())
                    state["status"] = status
                    self.materialize(run, state)
                    request = build_operator_retirement_request(
                        run, operator_audit_reference=f"api:retirement:{status}",
                    )
                    self.assertEqual(status, request["expected_status"])

    def test_snapshot_damage_and_terminal_status_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run = self.materialize(base / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:009",
            )
            (run / "unexpected.json").write_text("{}\n", encoding="utf-8")
            result = assess_operator_retirement(run, request)
            self.assertIn("snapshot_invalid", result["failed_predicates"])

            (run / "unexpected.json").unlink()
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            state["status"] = "POLICY_STOPPED"
            (run / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run)
            result = assess_operator_retirement(run, request)
            self.assertIn("delivery_or_terminal_conflict", result["failed_predicates"])

    def test_consumed_providerless_and_submitting_actions_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for action_state, extra, expected in (
                ("AUTHORIZED", {"consumption": {"consumed_at": "now"}},
                 "provider_ambiguity_present"),
                ("SUBMITTING", {}, "provider_ambiguity_present"),
            ):
                with self.subTest(action_state=action_state):
                    run = Path(temporary) / action_state.lower()
                    state = self.state(run.resolve())
                    action = {
                        "action_id": "paid_0123456789abcdef01234567",
                        "state": action_state,
                        "binding": {
                            "run_id": state["run_id"], "profile_sha256": "1" * 64,
                            "prepared_state_revision": 9, "stage": "creative_retry",
                            "route": "retry:1", "request_sha256": "2" * 64,
                            "model": "gpt-5.6", "service_level": "interactive",
                            "maximum_output_tokens": 1000,
                            "commitment_micro_usd": 1000,
                            "price_book_version": "test.v1",
                        },
                        "authorization": None, "provider": None, "reported": None,
                    }
                    action.update(extra)
                    state["spend_ledger"]["actions"] = [action]
                    self.materialize(run, state)
                    with self.assertRaisesRegex(ValueError, expected):
                        build_operator_retirement_request(
                            run, operator_audit_reference="api:retirement:010",
                        )

    def test_execute_applies_terminal_transition_and_seals_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:execute-001",
            )
            result = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:00:00+00:00",
            )
            validate_operator_retirement_result(result)
            self.assertEqual("applied", result["outcome"])
            self.assertTrue(result["applied"])
            self.assertEqual("POLICY_STOPPED", result["terminal_status"])
            self.assertEqual("operator_retired", result["terminal_cause"])
            self.assertFalse(any(result["continuation_assertions"].values()))
            self.assertEqual(10, result["post_state_revision"])
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            self.assertEqual("POLICY_STOPPED", state["status"])
            self.assertEqual("operator_retired", state["terminal_transition"]["terminal_reason"])
            self.assertEqual(
                request["request_sha256"],
                state["terminal_transition"]["request_sha256"],
            )
            lifecycle = inspect_lifecycle(
                run, native_exclusive_access="declared",
                observed_at="2026-08-24T23:00:01+00:00",
            )
            self.assertTrue(lifecycle["terminal"]["terminal"])
            self.assertEqual("operator_retired", lifecycle["terminal"]["terminal_reason"])
            self.assertFalse(lifecycle["terminal"]["provider_continuation_remains"])
            self.assertFalse(lifecycle["terminal"]["local_continuation_remains"])
            sealed = read_native_transition_result(
                run, result["native_result"]["result_id"],
            )
            self.assertEqual("operator_retirement", sealed["result"]["command_kind"])
            self.assertEqual("operator_retired", sealed["result"]["cause_code"])
            self.assertEqual(
                request["request_sha256"],
                sealed["result"]["projection_refs"]["operator_retirement"]["request_sha256"],
            )

    def test_execute_stale_refusal_is_byte_identical_and_unpublished(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:execute-002",
            )
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run)
            before = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            result = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:05:00+00:00",
            )
            after = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            self.assertEqual("stale_observation", result["outcome"])
            self.assertFalse(result["applied"])
            self.assertEqual(before, after)
            self.assertIsNone(result["native_result"])
            self.assertIsNone(result["publication_receipt"])

    def test_execute_result_matches_schema_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency is unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:schema-result",
            )
            result = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:10:00+00:00",
            )
            jsonschema.validate(
                result, read_operator_retirement_schema()["$defs"]["result"],
            )

    def test_cli_execute_uses_public_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run = self.materialize(base / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:cli-execute",
            )
            request_path = base / "request.json"
            request_path.write_text(json.dumps(request) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "astrowoof_natal_authoring.operator_retirement",
                 "--run-dir", str(run), "execute", "--request", str(request_path),
                 "--committed-at", "2026-08-24T23:15:00+00:00"],
                check=True, text=True, capture_output=True,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            )
            result = json.loads(completed.stdout)
            self.assertEqual("applied", result["outcome"])
            self.assertEqual("POLICY_STOPPED", result["terminal_status"])

    def test_exact_replay_returns_same_seal_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:replay-exact",
            )
            first = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:20:00+00:00",
            )
            before = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            replay = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:21:00+00:00",
            )
            after = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            self.assertEqual("exact_replay", replay["outcome"])
            self.assertFalse(replay["applied"])
            self.assertEqual(request["request_sha256"], replay["original_request_sha256"])
            self.assertEqual(first["native_result"], replay["native_result"])
            self.assertEqual(first["publication_receipt"], replay["publication_receipt"])
            self.assertEqual(before, after)

    def test_compatible_later_request_returns_already_retired(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:original",
            )
            first = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:25:00+00:00",
            )
            later = deepcopy(request)
            later["operator_audit_reference"] = "api:retirement:later-compatible"
            later["human_reason"] = "Equivalent later operator audit reference"
            later["request_sha256"] = _sha256({
                key: value for key, value in later.items() if key != "request_sha256"
            })
            validate_operator_retirement_request(later)
            result = execute_operator_retirement(
                run, later, committed_at="2026-08-24T23:26:00+00:00",
            )
            self.assertEqual("already_retired", result["outcome"])
            self.assertFalse(result["applied"])
            self.assertEqual(request["request_sha256"], result["original_request_sha256"])
            self.assertEqual(later["request_sha256"], result["request_sha256"])
            self.assertEqual(first["native_result"], result["native_result"])

    def test_interruption_after_state_persist_recovers_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:interrupt-state",
            )

            def fail(point: str) -> None:
                if point == "after_state_persisted":
                    raise RuntimeError("injected after state persistence")

            with self.assertRaisesRegex(RuntimeError, "injected"):
                execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:30:00+00:00",
                    _failure_injector=fail,
                )
            recovered = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:31:00+00:00",
            )
            self.assertEqual("exact_replay", recovered["outcome"])
            self.assertEqual("POLICY_STOPPED", recovered["terminal_status"])

    def test_interruption_after_snapshot_or_publication_recovers_without_duplicate(self) -> None:
        for point in ("after_transition_snapshot", "after_native_publication"):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temporary:
                run = self.materialize(Path(temporary) / "run")
                request = build_operator_retirement_request(
                    run, operator_audit_reference=f"api:retirement:{point}",
                )

                def fail(observed: str) -> None:
                    if observed == point:
                        raise RuntimeError(f"injected {point}")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    execute_operator_retirement(
                        run, request, committed_at="2026-08-24T23:35:00+00:00",
                        _failure_injector=fail,
                    )
                recovered = execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:36:00+00:00",
                )
                self.assertEqual("exact_replay", recovered["outcome"])
                index = json.loads(
                    (run / "native-result-index.json").read_text(encoding="utf-8")
                )
                self.assertEqual(1, len(index["result_ids"]))

    def test_interrupted_receipt_publication_uses_native_repair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:interrupt-receipt",
            )
            with patch(
                "astrowoof_natal_authoring.native_transitions._publish_receipt",
                side_effect=RuntimeError("injected receipt failure"),
            ), self.assertRaisesRegex(RuntimeError, "receipt failure"):
                execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:40:00+00:00",
                )
            recovered = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:41:00+00:00",
            )
            self.assertEqual("exact_replay", recovered["outcome"])
            self.assertTrue((
                run / "native-publication-receipts"
                / f"{recovered['native_result']['result_id']}.json"
            ).is_file())

    def test_concurrent_second_writer_cannot_duplicate_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:concurrent",
            )
            entered = threading.Event()
            release = threading.Event()
            outcomes: list[dict] = []
            errors: list[BaseException] = []

            def pause(point: str) -> None:
                if point == "after_state_persisted":
                    entered.set()
                    release.wait(timeout=5)

            def first_writer() -> None:
                try:
                    outcomes.append(execute_operator_retirement(
                        run, request, committed_at="2026-08-24T23:45:00+00:00",
                        _failure_injector=pause,
                    ))
                except BaseException as exc:  # test captures thread failures
                    errors.append(exc)

            thread = threading.Thread(target=first_writer)
            thread.start()
            self.assertTrue(entered.wait(timeout=5))
            try:
                with self.assertRaises(OSError):
                    execute_operator_retirement(
                        run, request, committed_at="2026-08-24T23:45:01+00:00",
                    )
            finally:
                release.set()
                thread.join(timeout=5)
            self.assertFalse(errors)
            self.assertEqual(["applied"], [item["outcome"] for item in outcomes])
            index = json.loads(
                (run / "native-result-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(1, len(index["result_ids"]))

    def test_event_sink_failure_and_protected_sentinel_cannot_change_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            sentinel = "PROTECTED_SENTINEL_BIRTH_LOCATION_999"
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:event-isolation",
                human_reason=sentinel,
            )
            captured: list[dict] = []

            def failing_sink(envelope: dict) -> None:
                captured.append(deepcopy(envelope))
                raise RuntimeError("sink unavailable")

            emitter = ExecutionEventEmitter(release="test", sink=failing_sink)
            with self.assertLogs(level="INFO") as logged:
                result = execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:50:00+00:00",
                    event_emitter=emitter,
                )
            self.assertEqual("applied", result["outcome"])
            rendered = json.dumps(captured, ensure_ascii=False)
            self.assertNotIn(sentinel, rendered)
            self.assertNotIn(sentinel, "\n".join(logged.output))
            self.assertGreaterEqual(emitter.stats.dropped, 1)

    def test_interrupted_state_recovery_refuses_unrelated_workspace_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:unsafe-repair",
            )

            def fail(point: str) -> None:
                if point == "after_state_persisted":
                    raise RuntimeError("injected state boundary")

            with self.assertRaises(RuntimeError):
                execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:55:00+00:00",
                    _failure_injector=fail,
                )
            (run / "unrelated-changed-byte.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cannot be safely recovered"):
                execute_operator_retirement(
                    run, request, committed_at="2026-08-24T23:56:00+00:00",
                )

    def test_execute_recomputes_native_safety_after_pre_writer_race(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.materialize(Path(temporary) / "run")
            request = build_operator_retirement_request(
                run, operator_audit_reference="api:retirement:pre-writer-race",
            )
            state = json.loads((run / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            state["spend_ledger"]["actions"] = [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "SUBMITTING",
                "binding": {
                    "run_id": state["run_id"], "profile_sha256": "1" * 64,
                    "prepared_state_revision": state["state_revision"],
                    "stage": "authoring_initial", "route": "pass-001",
                    "request_sha256": "2" * 64, "model": "gpt-5.6",
                    "service_level": "interactive", "maximum_output_tokens": 1000,
                    "commitment_micro_usd": 1000,
                    "price_book_version": "test.v1",
                },
                "authorization": {"authorization_reference": "api:auth:race"},
                "provider": None, "reported": None, "consumption": None,
            }]
            (run / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            write_workspace_snapshot(run)
            before = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            result = execute_operator_retirement(
                run, request, committed_at="2026-08-24T23:57:00+00:00",
            )
            after = {
                path.relative_to(run).as_posix(): path.read_bytes()
                for path in run.rglob("*") if path.is_file()
                and path.name != "spend-consumption.lock"
            }
            self.assertFalse(result["applied"])
            self.assertIn("provider_ambiguity_present", result["failed_predicates"])
            self.assertIn("not_retirement_quiescent", result["failed_predicates"])
            self.assertIn("stale_observation", result["failed_predicates"])
            self.assertTrue(result["continuation_assertions"]["provider_pending"])
            self.assertTrue(result["continuation_assertions"]["local_continuation"])
            self.assertEqual(before, after)
            self.assertIsNone(result["native_result"])
            self.assertIsNone(result["publication_receipt"])


if __name__ == "__main__":
    unittest.main()
