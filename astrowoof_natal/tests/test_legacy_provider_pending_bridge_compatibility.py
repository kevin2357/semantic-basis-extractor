from __future__ import annotations

import hashlib
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    public_run_state,
    validate_workspace_snapshot,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    validate_lifecycle_inspection_v05,
)
from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    ExecutionEventEmitter,
)
from astrowoof_natal_authoring.reconciliation import (  # noqa: E402
    reconcile_provider_cycle,
)
from astrowoof_natal_authoring.temporal_lifecycle import (  # noqa: E402
    build_lifecycle_inspection_v06,
    validate_lifecycle_inspection_v06,
)


SPRINT = (
    ROOT / "docs" / "sprints" / "2026" / "08"
    / "20260824-legacy-provider-pending-bridge-compatibility-sprint1"
)
RECIPE_PATH = SPRINT / "results" / "legacy-provider-pending-fixture.v1.json"
MANIFEST_PATH = SPRINT / "results" / "fixture-manifest.json"
COMMAND_CONTRACT_PATH = SPRINT / "SLICE 0 - FROZEN FIXTURE AND COMMAND CONTRACT.md"


def workspace_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


def materialize_legacy_fixture(root: Path) -> tuple[dict, dict]:
    recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
    run = recipe["run"]
    defaults = recipe["binding_defaults"]
    policy = recipe["reconciliation"]
    actions = []
    passes = {}
    for ordinal, member in enumerate(recipe["actions"], 1):
        binding = {
            "run_id": run["run_id"],
            "profile_sha256": defaults["profile_sha256"],
            "prepared_state_revision": ordinal,
            "stage": defaults["stage"],
            "route": member["route"],
            "request_sha256": member["request_sha256"],
            "model": defaults["model"],
            "service_level": defaults["service_level"],
            "maximum_output_tokens": defaults["maximum_output_tokens"],
            "commitment_micro_usd": defaults["commitment_micro_usd"],
            "price_book_version": defaults["price_book_version"],
        }
        actions.append({
            "action_id": member["action_id"],
            "state": "WAITING",
            "binding": binding,
            "authorization": {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": member["action_id"],
                "binding": binding,
                "authorization_reference": f"fixture-reservation-{ordinal}",
            },
            "consumption": {
                "consumer_id": f"historical-worker-{ordinal}",
                "consumed_at": f"2026-08-24T14:{ordinal:02d}:00Z",
            },
            "provider": {
                "id": member["provider_response_id"],
                "kind": "response",
            },
            "provider_reconciliation": {
                "policy_version": policy["policy_version"],
                "provider_retrieval_attempt_count": 0,
                "last_attempt_at": None,
                "last_outcome": "provider_identity_recorded",
                "resume_not_before": policy["due_observed_at"],
            },
            "reported": None,
        })
        passes[member["pass_id"]] = {
            "pass_id": member["pass_id"],
            "state": "WAITING_FOR_RESPONSE",
            "attempts": [{
                "attempt": 1,
                "state": "WAITING_FOR_RESPONSE",
                "provider_metadata": {
                    "provider": "openai",
                    "response_id": member["provider_response_id"],
                    "response_status": "in_progress",
                    "last_polled_at": "2026-08-24T14:30:00Z",
                },
            }],
        }
    state = {
        "schema_version": run["run_schema_version"],
        "run_id": run["run_id"],
        "state_revision": run["state_revision"],
        "status": run["status"],
        "service_level": run["service_level"],
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(root),
        },
        "spend_ledger": {"actions": actions},
        "passes": passes,
        "initial_authoring_wave": {"state": run["initial_wave_state"]},
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
    return recipe, state


class TestLegacyProviderPendingBridgeSlice0(unittest.TestCase):
    def test_recipe_is_sanitized_closed_six_member_shape(self) -> None:
        recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            "astrowoof.legacy_provider_pending_fixture.v1",
            recipe["schema_version"],
        )
        self.assertTrue(recipe["qualification_only"])
        self.assertTrue(recipe["sanitized"])
        self.assertEqual("exact_natal", recipe["run"]["route_family"])
        self.assertEqual("response", recipe["run"]["provider_mechanism"])
        self.assertEqual(6, len(recipe["actions"]))
        self.assertEqual(6, len({item["action_id"] for item in recipe["actions"]}))
        self.assertEqual(
            6, len({item["provider_response_id"] for item in recipe["actions"]})
        )
        encoded = RECIPE_PATH.read_text(encoding="utf-8").lower()
        for forbidden in ("ce525bea", "b469adb8", "kevin", "birth", "latitude"):
            self.assertNotIn(forbidden, encoded)

    def test_frozen_manifest_binds_exact_recipe(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            "astrowoof.legacy_provider_pending_fixture_manifest.v1",
            manifest["schema_version"],
        )
        self.assertEqual("api_approved_and_installed_qualified", manifest["status"])
        self.assertEqual(6, manifest["fixture"]["action_count"])
        self.assertEqual(6, manifest["fixture"]["provider_identity_count"])
        self.assertEqual(
            manifest["fixture"]["sha256"],
            hashlib.sha256(RECIPE_PATH.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            manifest["command_contract"]["sha256"],
            hashlib.sha256(COMMAND_CONTRACT_PATH.read_bytes()).hexdigest(),
        )

    def test_materialized_fixture_is_valid_not_due_then_due_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            recipe, state = materialize_legacy_fixture(root)
            validate_workspace_snapshot(root, state)
            before = workspace_hashes(root)
            not_due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at=recipe["reconciliation"]["not_due_observed_at"],
            )
            due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at=recipe["reconciliation"]["due_observed_at"],
            )
            validate_lifecycle_inspection_v05(not_due)
            validate_lifecycle_inspection_v05(due)
            self.assertEqual(before, workspace_hashes(root))
            self.assertEqual("release_until_due", not_due["execution_capacity"]["disposition"])
            self.assertFalse(not_due["execution_branch"]["eligible_now"])
            self.assertEqual("continue_local_cycle", due["execution_capacity"]["disposition"])
            self.assertTrue(due["execution_branch"]["eligible_now"])
            self.assertEqual(4, len(due["execution_branch"]["action_ids"]))
            self.assertEqual(
                due["provider_custody"]["next_due_action_ids"],
                due["execution_branch"]["action_ids"],
            )
            self.assertEqual(
                {item["provider_response_id"] for item in recipe["actions"]},
                {
                    item["provider_operation_id"]
                    for item in due["action_inventory"]["actions"]
                },
            )
            self.assertIsNone(due["external_authority_request"])
            self.assertIsNone(due["external_authority_refusal"])


@unittest.skipUnless(
    os.environ.get("SBE_RUN_INSTALLED_BRIDGE_QUALIFICATION") == "1",
    "installed bridge qualification is opt-in",
)
class TestInstalledLegacyProviderPendingBridgeSlice1(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(
            prefix="sbe-legacy-bridge-installed-"
        )
        cls.root = Path(cls.temporary.name).resolve()
        cls.venv = cls.root / "venv"
        cls.wheel = Path(os.environ.get(
            "SBE_BRIDGE_QUALIFICATION_WHEEL",
            str(
                ROOT / "releases" / "0.4.16"
                / "astrowoof_natal_authoring-0.4.16-py3-none-any.whl"
            ),
        )).resolve()
        cls.expected_version = os.environ.get(
            "SBE_BRIDGE_QUALIFICATION_VERSION", "0.4.16"
        )
        subprocess.run(
            [sys.executable, "-m", "venv", str(cls.venv)],
            check=True,
            text=True,
            capture_output=True,
        )
        cls.python = cls.venv / "Scripts" / "python.exe"
        cls.semantic_closure = cls.venv / "Scripts" / "astrowoof-semantic-closure.exe"
        cls.native_transition = cls.venv / "Scripts" / "astrowoof-native-transition.exe"
        subprocess.run(
            [
                str(cls.python), "-m", "pip", "install", "--no-deps",
                str(cls.wheel),
            ],
            check=True,
            text=True,
            capture_output=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_real_installed_command_is_bounded_get_only_and_sealed(self) -> None:
        run_dir = self.root / "pending-run"
        run_dir.mkdir()
        recipe, _state = materialize_legacy_fixture(run_dir)
        requests: list[tuple[str, str]] = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(handler) -> None:  # noqa: N802
                requests.append(("GET", handler.path))
                response_id = handler.path.rsplit("/", 1)[-1]
                body = json.dumps({
                    "id": response_id,
                    "status": "in_progress",
                }).encode("utf-8")
                handler.send_response(200)
                handler.send_header("Content-Type", "application/json")
                handler.send_header("Content-Length", str(len(body)))
                handler.end_headers()
                handler.wfile.write(body)

            def do_POST(handler) -> None:  # noqa: N802
                requests.append(("POST", handler.path))
                handler.send_error(500, "POST is forbidden in bridge qualification")

            def log_message(self, _format: str, *_args: object) -> None:
                return

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}/v1"
        environment = {**os.environ, "OPENAI_API_KEY": "qualification-only-sentinel"}
        command = [
            str(self.semantic_closure),
            "--run-dir", str(run_dir),
            "--resume",
            "--provider", "openai",
            "--provider-reconciliation-cycle",
            "--observed-at", recipe["reconciliation"]["due_observed_at"],
            "--openai-base-url", base_url,
            "--http-timeout-seconds", "2",
            "--max-transport-retries", "0",
        ]
        try:
            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
                cwd=self.root,
            )
            self.assertEqual(3, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(4, result["cycle"]["provider_retrieval_count"])
            self.assertEqual(4, len(requests))
            self.assertTrue(all(method == "GET" for method, _path in requests))
            self.assertEqual(
                set(result["cycle"]["retrieved_action_ids"]),
                {
                    item["action_id"]
                    for item in recipe["actions"][:4]
                },
            )
            self.assertTrue(all(
                path.startswith("/v1/responses/resp_legacy_bridge_")
                for _method, path in requests
            ))
            first_requested_ids = {
                path.rsplit("/", 1)[-1] for _method, path in requests
            }
            self.assertEqual(
                {
                    item["provider_response_id"]
                    for item in recipe["actions"][:4]
                },
                first_requested_ids,
            )
            checkpoint = result["result_checkpoint"]
            artifact = run_dir / checkpoint["result_artifact"]["logical_path"]
            self.assertTrue(artifact.is_file())
            self.assertEqual(
                checkpoint["result_artifact"]["sha256"],
                hashlib.sha256(artifact.read_bytes()).hexdigest(),
            )
            native = subprocess.run(
                [str(self.native_transition), "--run-dir", str(run_dir), "--latest"],
                text=True,
                capture_output=True,
                check=False,
                cwd=self.root,
            )
            self.assertEqual(0, native.returncode, native.stderr)
            native_view = json.loads(native.stdout)
            native_result = native_view["result"]
            self.assertEqual("provider_reconciliation", native_result["command_kind"])
            self.assertEqual(self.expected_version, native_result["sbe_release"])
            self.assertIsInstance(native_view.get("receipt"), dict)
            self.assertEqual(
                native_result["result_id"], native_view["receipt"]["result_id"]
            )

            after_due = workspace_hashes(run_dir)
            request_count = len(requests)
            second_wave = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
                cwd=self.root,
            )
            self.assertEqual(3, second_wave.returncode, second_wave.stderr)
            second_result = json.loads(second_wave.stdout)
            self.assertEqual("detached_provider_pending", second_result["outcome"])
            self.assertEqual(2, second_result["cycle"]["provider_retrieval_count"])
            self.assertEqual(request_count + 2, len(requests))
            self.assertTrue(all(method == "GET" for method, _path in requests))
            second_requested_ids = {
                path.rsplit("/", 1)[-1]
                for _method, path in requests[request_count:]
            }
            self.assertEqual(
                {
                    item["provider_response_id"]
                    for item in recipe["actions"][4:]
                },
                second_requested_ids,
            )
            self.assertEqual(
                {item["provider_response_id"] for item in recipe["actions"]},
                first_requested_ids | second_requested_ids,
            )
            self.assertNotEqual(after_due, workspace_hashes(run_dir))

            after_second_wave = workspace_hashes(run_dir)
            request_count = len(requests)
            not_due = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
                cwd=self.root,
            )
            self.assertEqual(3, not_due.returncode, not_due.stderr)
            not_due_result = json.loads(not_due.stdout)
            self.assertEqual("not_due", not_due_result["outcome"])
            self.assertEqual(0, not_due_result["cycle"]["provider_retrieval_count"])
            self.assertEqual(request_count, len(requests))
            self.assertEqual(after_second_wave, workspace_hashes(run_dir))

            forbidden_inputs = (
                ["--spend-authorization", str(self.root / "authorization.json")],
                ["--spend-reconciliation", str(self.root / "settlement.json")],
                ["--initial-wave-authorization", str(self.root / "wave.json")],
                [
                    "--external-authority-request", str(self.root / "request.json"),
                    "--external-authority-grant", str(self.root / "grant.json"),
                ],
            )
            for forbidden_flags in forbidden_inputs:
                with self.subTest(forbidden_flags=forbidden_flags):
                    refused = subprocess.run(
                        command + forbidden_flags,
                        text=True,
                        capture_output=True,
                        check=False,
                        env=environment,
                        cwd=self.root,
                    )
                    self.assertEqual(2, refused.returncode)
                    self.assertIn(
                        "provider reconciliation cannot apply spend authorization",
                        refused.stderr,
                    )
                    self.assertEqual(request_count, len(requests))
                    self.assertEqual(after_second_wave, workspace_hashes(run_dir))
            self.assertEqual(6, len({path for _method, path in requests}))
        finally:
            server.shutdown()
            thread.join(timeout=5)
            server.server_close()

    def test_installed_binding_fence_refuses_first_or_deferred_member(self) -> None:
        requests: list[tuple[str, str]] = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(handler) -> None:  # noqa: N802
                requests.append(("GET", handler.path))
                handler.send_error(500, "GET is forbidden for malformed inventory")

            def do_POST(handler) -> None:  # noqa: N802
                requests.append(("POST", handler.path))
                handler.send_error(500, "POST is forbidden in bridge qualification")

            def log_message(self, _format: str, *_args: object) -> None:
                return

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}/v1"
        environment = {**os.environ, "OPENAI_API_KEY": "qualification-only-sentinel"}
        try:
            for malformed_index in (0, 4):
                with self.subTest(malformed_index=malformed_index):
                    run_dir = self.root / f"malformed-{malformed_index}"
                    run_dir.mkdir()
                    recipe, state = materialize_legacy_fixture(run_dir)
                    state["spend_ledger"]["actions"][malformed_index]["binding"][
                        "run_id"
                    ] = "wrong-run"
                    TestLegacyProviderPendingBridgeSlice2.rewrite(run_dir, state)
                    before = workspace_hashes(run_dir)
                    events_path = self.root / f"malformed-{malformed_index}.events.jsonl"
                    completed = subprocess.run(
                        [
                            str(self.semantic_closure),
                            "--run-dir", str(run_dir),
                            "--resume", "--provider", "openai",
                            "--provider-reconciliation-cycle",
                            "--observed-at", recipe["reconciliation"]["due_observed_at"],
                            "--openai-base-url", base_url,
                            "--events-jsonl", str(events_path),
                            "--http-timeout-seconds", "2",
                            "--max-transport-retries", "0",
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                        env=environment,
                        cwd=self.root,
                    )
                    self.assertEqual(3, completed.returncode, completed.stderr)
                    result = json.loads(completed.stdout)
                    self.assertEqual("review_required", result["outcome"])
                    self.assertEqual(0, result["cycle"]["provider_retrieval_count"])
                    self.assertNotIn("result_checkpoint", result)
                    self.assertEqual([], requests)
                    self.assertEqual(before, workspace_hashes(run_dir))
                    events = [
                        json.loads(line) for line in events_path.read_text(
                            encoding="utf-8"
                        ).splitlines()
                    ]
                    failures = [
                        event for event in events
                        if event["event_name"] == "execution.failed"
                    ]
                    self.assertEqual(1, len(failures))
                    self.assertEqual(
                        "provider_binding_integrity_mismatch",
                        failures[0]["data"]["reason_code"],
                    )
        finally:
            server.shutdown()
            thread.join(timeout=5)
            server.server_close()


class TestLegacyProviderPendingBridgeSlice2(unittest.TestCase):
    @staticmethod
    def rewrite(root: Path, state: dict) -> None:
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)

    def test_completed_retrieval_is_durable_and_creates_new_temporal_basis(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            recipe, _state = materialize_legacy_fixture(root)
            before = build_lifecycle_inspection_v06(inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at=recipe["reconciliation"]["due_observed_at"],
            ))
            calls: list[str] = []

            def retrieve(provider_id: str, _timeout: float) -> dict:
                calls.append(provider_id)
                return {
                    "id": provider_id,
                    "status": "completed",
                    "output": [],
                    "usage": {
                        "input_tokens": 10,
                        "output_tokens": 5,
                        "total_tokens": 15,
                    },
                }

            result = reconcile_provider_cycle(
                root,
                observed_at=recipe["reconciliation"]["due_observed_at"],
                retrieve=retrieve,
            )
            self.assertEqual("progressed_local", result["outcome"])
            self.assertEqual(4, len(calls))
            self.assertEqual(4, len(set(calls)))
            self.assertEqual(4, len(result["cycle"]["completed_action_ids"]))
            for action_id in result["cycle"]["completed_action_ids"]:
                evidence = (
                    root / "lifecycle" / "provider-reconciliation"
                    / f"{action_id}.response.json"
                )
                self.assertTrue(evidence.is_file())
            validate_workspace_snapshot(
                root, json.loads((root / "run.json").read_text(encoding="utf-8"))
            )
            after = build_lifecycle_inspection_v06(result["inspection"])
            validate_lifecycle_inspection_v06(after)
            self.assertNotEqual(
                before["checkpoint_basis_sha256"],
                after["checkpoint_basis_sha256"],
            )

    def test_temporal_projection_accepts_resolved_independent_action(self) -> None:
        """A v0.5-valid resolved action remains inspectable under v0.6.

        ``independent`` is the ordinary lifecycle vocabulary for an action
        which no longer blocks the run.  This is the retained-workspace shape
        reached after provider reconciliation, before a distinct external
        authority request is admitted.
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            recipe, _state = materialize_legacy_fixture(root)
            inspection = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at=recipe["reconciliation"]["due_observed_at"],
            )
            action = inspection["action_inventory"]["actions"][0]
            action.update({
                "necessary": False,
                "relationship": "independent",
                "providerless_denial_eligible": False,
                "eligibility_reason": "provider_identity_present",
            })
            validate_lifecycle_inspection_v05(inspection)

            projected = build_lifecycle_inspection_v06(inspection)

            self.assertEqual(
                "independent",
                projected["checkpoint_basis"]["action_inventory"]["actions"][0][
                    "relationship"
                ],
            )
            validate_lifecycle_inspection_v06(projected)

    def test_identity_conflict_is_review_only_and_never_retargets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            recipe, _state = materialize_legacy_fixture(root)
            requested: list[str] = []

            def wrong_identity(provider_id: str, _timeout: float) -> dict:
                requested.append(provider_id)
                return {"id": f"wrong_{provider_id}", "status": "in_progress"}

            result = reconcile_provider_cycle(
                root,
                observed_at=recipe["reconciliation"]["due_observed_at"],
                retrieve=wrong_identity,
            )
            self.assertEqual("review_required", result["outcome"])
            self.assertEqual(4, len(requested))
            persisted = json.loads((root / "run.json").read_text(encoding="utf-8"))
            conflicted = [
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] in result["cycle"]["retrieved_action_ids"]
            ]
            self.assertTrue(all(
                item["state"] == "AMBIGUOUS_PROVIDER_SUBMISSION"
                and item["provider"]["id"] in requested
                for item in conflicted
            ))

    def test_incomplete_snapshot_refuses_before_retrieval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            recipe, _state = materialize_legacy_fixture(root)
            (root / "unexpected-authoritative-byte.txt").write_text(
                "not in snapshot\n", encoding="utf-8"
            )
            calls: list[str] = []
            with self.assertRaisesRegex(ValueError, "snapshot is incomplete or changed"):
                reconcile_provider_cycle(
                    root,
                    observed_at=recipe["reconciliation"]["due_observed_at"],
                    retrieve=lambda provider_id, _timeout: calls.append(provider_id) or {},
                )
            self.assertEqual([], calls)

    def test_missing_timing_or_provider_identity_never_retrieves_that_action(self) -> None:
        cases = {
            "timing": lambda action: action.pop("provider_reconciliation"),
            "provider": lambda action: action.pop("provider"),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                recipe, state = materialize_legacy_fixture(root)
                malformed = state["spend_ledger"]["actions"][0]
                malformed_provider_id = malformed.get("provider", {}).get("id")
                mutate(malformed)
                self.rewrite(root, state)
                calls: list[str] = []
                try:
                    result = reconcile_provider_cycle(
                        root,
                        observed_at=recipe["reconciliation"]["due_observed_at"],
                        retrieve=lambda provider_id, _timeout: calls.append(provider_id) or {},
                    )
                except ValueError:
                    result = None
                self.assertNotIn(malformed_provider_id, calls)
                if result is not None:
                    self.assertLessEqual(len(calls), 4)

    def test_binding_mismatch_anywhere_refuses_whole_cycle_without_mutation(self) -> None:
        for malformed_index in (0, 4):
            with (
                self.subTest(malformed_index=malformed_index),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary).resolve()
                recipe, state = materialize_legacy_fixture(root)
                malformed = state["spend_ledger"]["actions"][malformed_index]
                malformed["binding"]["run_id"] = "wrong-run"
                self.rewrite(root, state)
                before = workspace_hashes(root)
                calls: list[str] = []
                events: list[dict] = []
                emitter = ExecutionEventEmitter(release="test", sink=events.append)

                result = reconcile_provider_cycle(
                    root,
                    observed_at=recipe["reconciliation"]["due_observed_at"],
                    retrieve=lambda provider_id, _timeout: (
                        calls.append(provider_id)
                        or {"id": provider_id, "status": "in_progress"}
                    ),
                    event_emitter=emitter,
                )

                self.assertEqual("review_required", result["outcome"])
                self.assertEqual([], calls)
                self.assertEqual(0, result["cycle"]["provider_retrieval_count"])
                self.assertNotIn("result_checkpoint", result)
                self.assertEqual(before, workspace_hashes(root))
                self.assertEqual(1, len(events))
                self.assertEqual("execution.failed", events[0]["event_name"])
                self.assertEqual(
                    "provider_binding_integrity_mismatch",
                    events[0]["data"]["reason_code"],
                )


if __name__ == "__main__":
    unittest.main()
