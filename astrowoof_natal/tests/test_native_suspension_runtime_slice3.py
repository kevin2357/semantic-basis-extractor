from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring.cli.external_authority_v2 import main as v2_main
from astrowoof_natal_authoring.closure import (
    load_json, normalized_path, write_workspace_snapshot,
)
from astrowoof_natal_authoring.external_authority_v2_execution import (
    commit_external_authority_v2_dispatch_intent,
)
from astrowoof_natal_authoring.external_authority_v2_qa import (
    _ordinary_authority,
    _pending_workspace,
    _reconcile_4_plus_2,
)
from astrowoof_natal_authoring.native_suspension_contracts import seal_document
from astrowoof_natal_authoring.native_suspension_runtime import (
    CooperativeSuspensionPublished,
    NativeSuspensionControlObserver,
)
from astrowoof_natal_authoring.native_transitions import checkpoint_basis
from astrowoof_natal_authoring.reconciliation import (
    ProviderReconciliationAdapters,
    reconcile_authoring_provider_cycle,
    reconcile_provider_cycle,
)


SHA = "a" * 64
OBSERVED = "2026-09-15T12:02:00Z"


def _control(run_dir: Path, control: Path, command: str):
    state = load_json(run_dir / "run.json")
    basis = checkpoint_basis(run_dir, state["state_revision"])["checkpoint_basis_sha256"]
    control.mkdir()
    envelope_path = control / "supervision-invocation.v1.json"
    envelope = seal_document({
        "schema_version": "astrowoof.native_supervision_invocation.v1",
        "supervision_invocation_id": "supervision-one", "launch_generation": 1,
        "api_run_id": "api-one", "job_id": "job-one", "attempt_id": "attempt-one",
        "lease_id": "lease-one", "lease_token_sha256": SHA,
        "native_run_id": state["run_id"], "worker_boot_id": "boot-one",
        "command_kind": command, "command_sha256": "b" * 64,
        "executable_workspace_root": normalized_path(run_dir),
        "executable_workspace_root_sha256": hashlib.sha256(normalized_path(run_dir).encode()).hexdigest(),
        "control_root": normalized_path(control),
        "control_root_sha256": hashlib.sha256(normalized_path(control).encode()).hexdigest(),
        "created_at": "2026-09-15T12:00:00Z",
        "launch_not_after": "2026-09-15T12:01:00Z",
        "grace_deadline": "2026-09-15T12:05:00Z",
        "supervision_capability_id": "capability-one",
        "supervision_capability_sha256": "d" * 64,
        "envelope_sha256": "",
    }, "envelope_sha256")
    request = seal_document({
        "schema_version": "astrowoof.native_suspension_request.v1",
        "operation": "cooperative_suspend", "request_id": "request-one",
        "idempotency_key": "idem-one",
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "launch_generation": 1, "envelope_sha256": envelope["envelope_sha256"],
        "supervision_capability_id": envelope["supervision_capability_id"],
        "supervision_capability_sha256": envelope[
            "supervision_capability_sha256"
        ],
        "force_fence_id": "fence-one", "force_fence_sha256": "c" * 64,
        "api_run_id": "api-one", "job_id": "job-one", "attempt_id": "attempt-one",
        "lease_id": "lease-one", "native_run_id": state["run_id"],
        "command_kind": command, "command_sha256": "b" * 64,
        "executable_workspace_root_sha256": envelope["executable_workspace_root_sha256"],
        "control_root_sha256": envelope["control_root_sha256"],
        "admission_checkpoint_basis_sha256": basis,
        "actor_id": "operator-one", "reason_code": "emergency-stop",
        "environment": "qa", "emergency_containment_confirmed": True,
        "requested_at": "2026-09-15T12:01:30Z",
        "expires_at": "2026-09-15T12:04:00Z",
        "grace_deadline": "2026-09-15T12:05:00Z", "request_sha256": "",
    }, "request_sha256")
    envelope_path.write_text(__import__("json").dumps(envelope), encoding="utf-8")
    (control / "native-suspension-request.v1.json").write_text(
        __import__("json").dumps(request), encoding="utf-8"
    )
    return NativeSuspensionControlObserver(
        envelope_path=envelope_path, control_root=control, observed_at=OBSERVED,
    )


class NativeSuspensionRuntimeSlice3Tests(unittest.TestCase):
    def test_public_v2_cli_returns_exact_suspension_command_without_provider_io(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            _reconcile_4_plus_2(run_dir)
            inspection, request, documents, grant = _ordinary_authority(
                run_dir, "exact_natal", "polish"
            )
            observer = _control(run_dir, base / "control", "external_authority_v2_dispatch")
            paths = {}
            for name, value in (
                ("inspection", inspection), ("request", request),
                ("grant", grant), ("authorization", documents[0]),
            ):
                paths[name] = base / f"{name}.json"
                paths[name].write_text(json.dumps(value), encoding="utf-8")
            output = base / "command-result.json"
            provider_calls = []
            with patch.dict("os.environ", {"OPENAI_API_KEY": "provider-free"}), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2."
                "OpenAIResponsesProvider.create_response_only",
                side_effect=lambda *_args, **_kwargs: provider_calls.append("POST"),
            ), patch(
                "astrowoof_natal_authoring.cli.external_authority_v2.datetime"
            ) as clock:
                clock.now.return_value = datetime(
                    2026, 9, 15, 12, 2, tzinfo=timezone.utc
                )
                code = v2_main([
                    "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
                    "--request", str(paths["request"]), "--grant", str(paths["grant"]),
                    "--authorization", str(paths["authorization"]),
                    "--provider", "openai", "--output", str(output),
                    "--log-level", "ERROR",
                    "--supervision-envelope", str(observer.envelope_path),
                    "--suspension-control-root", str(observer.control_root),
                ])
            self.assertEqual(0, code)
            self.assertEqual([], provider_calls)
            self.assertEqual(
                "astrowoof.native_suspension_command_result.v1",
                load_json(output)["schema_version"],
            )

    def test_dispatch_intent_checkpoint_publishes_and_exact_replay_is_inert(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            _reconcile_4_plus_2(run_dir)
            inspection, request, documents, grant = _ordinary_authority(
                run_dir, "exact_natal", "polish"
            )
            observer = _control(run_dir, base / "control", "external_authority_v2_dispatch")
            with self.assertRaises(CooperativeSuspensionPublished) as first:
                commit_external_authority_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents,
                    suspension_observer=observer,
                )
            state = load_json(run_dir / "run.json")
            self.assertEqual("INTENT_COMMITTED", state["external_authority_v2_dispatch_intent"]["state"])
            self.assertFalse(state["external_authority_v2_dispatch_intent"]["provider_io_performed"])
            with self.assertRaises(CooperativeSuspensionPublished) as replay:
                observer("dispatch_before_provider_post", run_dir, state, None)
            self.assertEqual(
                first.exception.publication["command_result"],
                replay.exception.publication["command_result"],
            )

    def test_reconciliation_observes_before_any_provider_get(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            retrievals = []
            with self.assertRaises(CooperativeSuspensionPublished):
                reconcile_provider_cycle(
                    run_dir, observed_at=OBSERVED,
                    retrieve=lambda *_: retrievals.append("GET"),
                    suspension_observer=observer,
                )
            self.assertEqual([], retrievals)

    def test_public_reconciliation_coordinator_propagates_suspension(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            retrievals = []

            class Provider:
                name = "openai"
                responses = None
                http_timeout_seconds = 15.0
                max_transport_retries = 0
                base_url = "https://provider.invalid/v1"
                api_key = "provider-free"

                def _request_with_retry(self, **_kwargs):
                    retrievals.append("GET")
                    raise AssertionError("provider retrieval must not run")

            provider = Provider()
            provider.responses = provider
            with self.assertRaises(CooperativeSuspensionPublished):
                reconcile_authoring_provider_cycle(
                    run_dir, observed_at=OBSERVED,
                    provider_adapters=ProviderReconciliationAdapters(
                        exact_interactive_provider=provider,
                    ),
                    suspension_observer=observer,
                )
            self.assertEqual([], retrievals)

    def test_request_arriving_during_get_suspends_after_response_checkpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            request_path = base / "control" / "native-suspension-request.v1.json"
            request_bytes = request_path.read_bytes()
            request_path.unlink()
            retrievals = []

            def retrieve(provider_id, _timeout):
                retrievals.append(provider_id)
                request_path.write_bytes(request_bytes)
                return {"id": provider_id, "status": "completed", "output": []}

            with self.assertRaises(CooperativeSuspensionPublished) as caught:
                reconcile_provider_cycle(
                    run_dir, observed_at=OBSERVED, retrieve=retrieve,
                    suspension_observer=observer,
                )
            publication = caught.exception.publication
            self.assertEqual(4, len(retrievals))
            self.assertEqual(
                "reconciliation_after_response_checkpoint",
                publication["result"]["safe_point"],
            )
            self.assertEqual(
                "completed_provider_evidence",
                publication["result"]["provider_boundary"],
            )

    def test_prior_ordinary_result_suppresses_suspension_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            result_id = "nres_" + "1" * 24
            (run_dir / "native-results").mkdir(exist_ok=True)
            (run_dir / "native-results" / f"{result_id}.json").write_text(
                json.dumps({
                    "result_id": result_id, "outcome": "delivery_complete",
                    "published_at": "2026-09-15T12:01:59Z",
                }), encoding="utf-8",
            )
            (run_dir / "native-result-index.json").write_text(json.dumps({
                "schema_version": "astrowoof.native_result_index.v0.1",
                "result_ids": [result_id],
            }), encoding="utf-8")
            write_workspace_snapshot(run_dir)
            state = load_json(run_dir / "run.json")
            with patch(
                "astrowoof_natal_authoring.native_suspension_runtime."
                "read_native_transition_result",
                return_value={"result": load_json(
                    run_dir / "native-results" / f"{result_id}.json"
                )},
            ):
                self.assertIsNone(observer(
                    "reconciliation_before_provider_get", run_dir, state, None,
                ))
            self.assertFalse((run_dir / "native-suspension-index.v1.json").exists())

    def test_unvalidated_ordinary_result_cannot_suppress_suspension(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            result_id = "nres_" + "1" * 24
            (run_dir / "native-results").mkdir(exist_ok=True)
            (run_dir / "native-results" / f"{result_id}.json").write_text(
                json.dumps({
                    "result_id": result_id, "outcome": "delivery_complete",
                    "published_at": "2026-09-15T12:01:59Z",
                }), encoding="utf-8",
            )
            (run_dir / "native-result-index.json").write_text(json.dumps({
                "schema_version": "astrowoof.native_result_index.v0.1",
                "result_ids": [result_id],
            }), encoding="utf-8")
            write_workspace_snapshot(run_dir)
            with self.assertRaises(CooperativeSuspensionPublished):
                observer(
                    "reconciliation_before_provider_get", run_dir,
                    load_json(run_dir / "run.json"), None,
                )

    def test_absent_request_is_inert_and_unexpected_member_refuses(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            request = base / "control" / "native-suspension-request.v1.json"
            request.unlink()
            state = load_json(run_dir / "run.json")
            self.assertIsNone(observer(
                "reconciliation_before_provider_get", run_dir, state, None,
            ))
            request.write_text("{}", encoding="utf-8")
            (base / "control" / "unexpected.txt").write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected members"):
                observer("reconciliation_before_provider_get", run_dir, state, None)

    def test_changed_request_after_publication_conflicts_without_second_result(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")
            state = load_json(run_dir / "run.json")
            with self.assertRaises(CooperativeSuspensionPublished):
                observer("reconciliation_before_provider_get", run_dir, state, None)
            request_path = base / "control" / "native-suspension-request.v1.json"
            changed = load_json(request_path)
            changed["request_id"] = "request-two"
            changed["idempotency_key"] = "idem-two"
            changed = seal_document(changed, "request_sha256")
            request_path.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "distinct suspension request"):
                observer(
                    "reconciliation_before_provider_get", run_dir,
                    load_json(run_dir / "run.json"), None,
                )
            self.assertEqual(
                1, len(load_json(run_dir / "native-suspension-index.v1.json")["result_ids"])
            )

    def test_restart_repairs_after_observation_checkpoint_without_second_result(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            run_dir = base / "run"
            _pending_workspace(run_dir, "exact_natal")
            observer = _control(run_dir, base / "control", "provider_reconciliation")

            def interrupt(stage):
                if stage == "after_observation_checkpoint":
                    raise RuntimeError("simulated interruption")

            observer.failure_injector = interrupt
            with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
                observer(
                    "reconciliation_before_provider_get", run_dir,
                    load_json(run_dir / "run.json"), None,
                )
            self.assertFalse((run_dir / "native-suspension-index.v1.json").exists())
            observer.failure_injector = None
            with self.assertRaises(CooperativeSuspensionPublished) as repaired:
                observer(
                    "reconciliation_before_provider_get", run_dir,
                    load_json(run_dir / "run.json"), None,
                )
            self.assertEqual(
                "suspended_checkpointed",
                repaired.exception.publication["result"]["outcome"],
            )
            self.assertEqual(
                1, len(load_json(run_dir / "native-suspension-index.v1.json")["result_ids"])
            )

    def test_bounded_route_remains_explicitly_unsupported(self):
        for route, service_level in (("bounded_natal", "interactive"),):
            with tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                run_dir = base / "run"
                _pending_workspace(run_dir, route)
                state = load_json(run_dir / "run.json")
                state["service_level"] = service_level
                (run_dir / "run.json").write_text(json.dumps(state), encoding="utf-8")
                write_workspace_snapshot(run_dir)
                observer = _control(
                    run_dir, base / "control", "provider_reconciliation"
                )
                with self.assertRaisesRegex(ValueError, "unsupported"):
                    reconcile_authoring_provider_cycle(
                        run_dir, observed_at=OBSERVED,
                        provider_adapters=ProviderReconciliationAdapters(),
                        suspension_observer=observer,
                    )


if __name__ == "__main__":
    unittest.main()
