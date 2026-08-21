from __future__ import annotations

import hashlib
import io
import json
import tempfile
import unittest
import sys
import threading
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (
    OpenAIResponsesProvider,
    execute_exact_initial_wave_with_external_authority,
    load_json,
    prepare_exact_interactive_initial_wave,
    save_state,
    validate_workspace_snapshot,
    main as closure_main,
    write_json_atomic,
)
from astrowoof_natal_authoring.external_authority import (
    read_external_authority_request,
    validate_external_authority_grant,
)
from astrowoof_natal.tests.test_semantic_closure import (
    ScriptedTransport,
    SemanticClosureFixture,
)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def authority(request: dict) -> tuple[dict, list[dict]]:
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action["action_id"], "binding": action["binding"],
        "authorization_reference": f"reservation-{index}",
    } for index, action in enumerate(request["ordered_actions"], 1)]
    body = {
        "schema_version": "astrowoof.external_authority_grant.v1",
        "decision": "granted", "api_decision_id": "decision-slice3-fixture",
        "issuer": "api-slice3-fixture", "issued_at": "2026-08-20T15:00:00Z",
        "external_authority_request_sha256": request[
            "external_authority_request_sha256"
        ],
        "run_id": request["run_id"],
        "inspected_state_revision": request["observation"]["operator_state_revision"],
        "snapshot_sha256": request["observation"]["snapshot_sha256"],
        "logical_workspace_root": request["observation"]["logical_workspace_root"],
        "request_kind": request["request_kind"],
        "action_count": request["action_count"],
        "ordered_action_ids": request["ordered_action_ids"],
        "ordered_member_authorizations": [{
            "action_id": action["action_id"],
            "binding_sha256": action["binding_sha256"],
            "authorization_document_sha256": digest(document),
            "authorization_reference": document["authorization_reference"],
        } for action, document in zip(
            request["ordered_actions"], documents, strict=True,
        )],
        "initial_wave": request["initial_wave"],
    }
    return {**body, "grant_sha256": digest(body)}, documents


class TestExternalAuthorityExecution(SemanticClosureFixture):
    def prepared(self, root: Path) -> tuple[Path, dict, OpenAIResponsesProvider, ScriptedTransport]:
        transport = ScriptedTransport([{
            "id": f"resp_constrained_{number}", "status": "in_progress",
        } for number in range(1, 7)])
        provider = OpenAIResponsesProvider(
            api_key="test-key", model="gpt-5.6-luna", transport=transport,
            max_transport_retries=0, prompt_cache_mode="disabled",
            require_spend_authorization=True, max_output_tokens=30_000,
        )
        state, run_json = self.make_state(root, provider)
        prepare_exact_interactive_initial_wave(
            state=state, provider=provider, run_dir=root / "run", run_json=run_json,
        )
        save_state(run_json, state)
        request = read_external_authority_request(root / "run")
        return root / "run", request, provider, transport

    def test_exact_grant_persists_intent_then_creates_six(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, provider, transport = self.prepared(Path(temporary))
            grant, documents = authority(request)
            validate_external_authority_grant(request, grant, documents)
            result = execute_exact_initial_wave_with_external_authority(
                run_dir=run_dir, request=request, grant=grant,
                member_authorizations=documents, provider=provider,
            )
            self.assertEqual("detached_provider_pending", result["outcome"])
            self.assertEqual(6, len(transport.calls))
            state = load_json(run_dir / "run.json")
            self.assertEqual(
                {"WAITING"}, {
                    action["state"] for action in state["spend_ledger"]["actions"]
                },
            )
            self.assertEqual(
                grant["grant_sha256"],
                state["initial_authoring_wave"]["constrained_submission_intent"][
                    "grant_sha256"
                ],
            )
            validate_workspace_snapshot(run_dir, state)

    def test_crash_after_intent_is_not_create_replay_permission(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, provider, transport = self.prepared(Path(temporary))
            grant, documents = authority(request)

            def crash(point: str) -> None:
                if point == "after_durable_pre_submit_intent":
                    raise RuntimeError("injected after intent")

            with self.assertRaisesRegex(RuntimeError, "injected after intent"):
                execute_exact_initial_wave_with_external_authority(
                    run_dir=run_dir, request=request, grant=grant,
                    member_authorizations=documents, provider=provider,
                    _failure_injector=crash,
                )
            self.assertEqual(0, len(transport.calls))

    def test_provider_return_before_identity_is_durable_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, request, provider, transport = self.prepared(Path(temporary))
            grant, documents = authority(request)

            def crash(point: str) -> None:
                if point.startswith("after_provider_create_before_identity:"):
                    raise RuntimeError("injected identity gap")

            result = execute_exact_initial_wave_with_external_authority(
                run_dir=run_dir, request=request, grant=grant,
                member_authorizations=documents, provider=provider,
                _failure_injector=crash,
            )
            self.assertEqual("ambiguous_submission", result["outcome"])
            self.assertEqual(6, len(transport.calls))
            state = load_json(run_dir / "run.json")
            self.assertEqual(
                {"AMBIGUOUS_PROVIDER_SUBMISSION"}, {
                    action["state"] for action in state["spend_ledger"]["actions"]
                },
            )
            validate_workspace_snapshot(run_dir, state)
            with self.assertRaises(Exception):
                execute_exact_initial_wave_with_external_authority(
                    run_dir=run_dir, request=request, grant=grant,
                    member_authorizations=documents, provider=provider,
                )
            self.assertEqual(6, len(transport.calls))
            state = load_json(run_dir / "run.json")
            self.assertEqual(
                {"AMBIGUOUS_PROVIDER_SUBMISSION"}, {
                    action["state"] for action in state["spend_ledger"]["actions"]
                },
            )
            validate_workspace_snapshot(run_dir, state)

    def test_stale_request_and_partial_grant_mutate_nothing(self) -> None:
        for case in ("stale", "partial"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                run_dir, request, provider, transport = self.prepared(Path(temporary))
                grant, documents = authority(request)
                if case == "stale":
                    request = deepcopy(request)
                    request["observation"]["snapshot_sha256"] = "f" * 64
                else:
                    documents.pop()
                before = (run_dir / "run.json").read_bytes()
                snapshot = (run_dir / "workspace-snapshot.json").read_bytes()
                with self.assertRaises(Exception):
                    execute_exact_initial_wave_with_external_authority(
                        run_dir=run_dir, request=request, grant=grant,
                        member_authorizations=documents, provider=provider,
                    )
                self.assertEqual(before, (run_dir / "run.json").read_bytes())
                self.assertEqual(snapshot, (run_dir / "workspace-snapshot.json").read_bytes())
                self.assertEqual(0, len(transport.calls))

    def test_public_cli_consumes_exact_request_and_grant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, _provider, _transport = self.prepared(root)
            grant, documents = authority(request)
            authority_dir = root / "authority"
            authority_dir.mkdir()
            request_path = authority_dir / "request.json"
            grant_path = authority_dir / "grant.json"
            write_json_atomic(request_path, request)
            write_json_atomic(grant_path, grant)
            document_paths = []
            for index, document in enumerate(documents, 1):
                path = authority_dir / f"member-{index}.json"
                write_json_atomic(path, document)
                document_paths.append(path)
            calls: list[str] = []
            call_lock = threading.Lock()

            def scripted_create(
                _provider: OpenAIResponsesProvider, _payload: dict,
                *, idempotency_key: str, timeout_seconds: float,
            ) -> tuple[dict, int]:
                del idempotency_key, timeout_seconds
                with call_lock:
                    response_id = f"resp_cli_constrained_{len(calls) + 1}"
                    calls.append(response_id)
                return {"id": response_id, "status": "in_progress"}, 1

            argv = [
                "astrowoof-semantic-closure", "--run-dir", str(run_dir),
                "--resume", "--provider", "openai", "--service-level",
                "interactive", "--api-key-env", "SBE_SLICE3_FAKE_KEY",
                "--model", "gpt-5.6-luna", "--max-output-tokens", "30000",
                "--log-level", "CRITICAL",
                "--prompt-cache-mode", "disabled", "--max-transport-retries", "0",
                "--external-authority-request", str(request_path),
                "--external-authority-grant", str(grant_path),
            ]
            for path in document_paths:
                argv.extend(["--spend-authorization", str(path)])
            with (
                patch.dict("os.environ", {"SBE_SLICE3_FAKE_KEY": "test-key"}),
                patch("sys.argv", argv),
                patch.object(
                    OpenAIResponsesProvider, "create_response_only",
                    new=scripted_create,
                ),
                redirect_stdout(io.StringIO()),
            ):
                closure_main()
            self.assertEqual(6, len(calls))
            self.assertEqual(
                {"WAITING"}, {
                    action["state"] for action in load_json(
                        run_dir / "run.json"
                    )["spend_ledger"]["actions"]
                },
            )

    def test_public_cli_rejects_member_authorizations_without_aggregate_grant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, request, _provider, _transport = self.prepared(root)
            _grant, documents = authority(request)
            authority_dir = root / "authority"
            authority_dir.mkdir()
            document_paths = []
            for index, document in enumerate(documents, 1):
                path = authority_dir / f"member-{index}.json"
                write_json_atomic(path, document)
                document_paths.append(path)
            before_run = (run_dir / "run.json").read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()
            argv = [
                "astrowoof-semantic-closure", "--run-dir", str(run_dir),
                "--resume", "--provider", "openai", "--service-level",
                "interactive", "--api-key-env", "SBE_SLICE3_FAKE_KEY",
                "--model", "gpt-5.6-luna", "--max-output-tokens", "30000",
                "--log-level", "CRITICAL", "--prompt-cache-mode", "disabled",
            ]
            for path in document_paths:
                argv.extend(["--spend-authorization", str(path)])
            with (
                patch.dict("os.environ", {"SBE_SLICE3_FAKE_KEY": "test-key"}),
                patch("sys.argv", argv),
                redirect_stdout(io.StringIO()),
                self.assertRaisesRegex(Exception, "aggregate grant"),
            ):
                closure_main()
            self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes()
            )

    def test_generic_resume_of_stored_awaiting_wave_refuses_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _request, _provider, _transport = self.prepared(Path(temporary))
            before_run = (run_dir / "run.json").read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()

            def publication_bytes() -> dict[str, bytes]:
                return {
                    path.relative_to(run_dir).as_posix(): path.read_bytes()
                    for path in run_dir.rglob("*")
                    if path.is_file() and (
                        path.name == "native-result-index.json"
                        or "native-results" in path.parts
                        or "native-publication-receipts" in path.parts
                    )
                }

            before_publication = publication_bytes()
            calls: list[str] = []

            def forbidden_create(*_args: object, **_kwargs: object) -> tuple[dict, int]:
                calls.append("create")
                return {"id": "resp_forbidden", "status": "in_progress"}, 1

            argv = [
                "astrowoof-semantic-closure", "--run-dir", str(run_dir),
                "--resume", "--provider", "openai", "--service-level",
                "interactive", "--api-key-env", "SBE_SLICE3_FAKE_KEY",
                "--model", "gpt-5.6-luna", "--max-output-tokens", "30000",
                "--log-level", "CRITICAL", "--prompt-cache-mode", "disabled",
            ]
            with (
                patch.dict("os.environ", {"SBE_SLICE3_FAKE_KEY": "test-key"}),
                patch("sys.argv", argv),
                patch.object(
                    OpenAIResponsesProvider, "create_response_only",
                    new=forbidden_create,
                ),
                redirect_stdout(io.StringIO()),
                self.assertRaisesRegex(Exception, "aggregate grant"),
            ):
                closure_main()
            self.assertEqual([], calls)
            self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes()
            )
            self.assertEqual(before_publication, publication_bytes())


if __name__ == "__main__":
    unittest.main()
