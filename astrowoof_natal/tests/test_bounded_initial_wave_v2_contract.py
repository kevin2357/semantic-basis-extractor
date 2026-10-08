from __future__ import annotations

import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_lifecycle import (
    commit_bounded_initial_wave_v2_dispatch_intent,
    create_bounded_run,
    dispatch_bounded_initial_wave_v2_intent,
    resume_bounded_run,
)
from astrowoof_natal_authoring.bounded_provider import OpenAIBoundedLifecycleProvider
from astrowoof_natal_authoring.spend import PRICE_BOOK_VERSION
from astrowoof_natal_authoring.temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
    validate_external_authority_request_v2_against_inspection,
)
from astrowoof_natal_authoring.lifecycle_contracts import canonical_contract_json
from astrowoof_natal_authoring.external_authority_v2 import (
    build_external_authority_grant_v2,
    build_no_grant_dispatch_result_v2,
    validate_external_authority_grant_v2,
    validate_no_grant_dispatch_result_v2,
)
from astrowoof_natal_authoring.cli.external_authority_v2 import main as authority_v2_main
from astrowoof_natal_authoring import (
    read_bounded_initial_wave_v2_command_result_schema,
    validate_bounded_initial_wave_v2_command_result,
)
from test_bounded_authoring import compiled


class _NoNetworkTransport:
    def request_json(self, **_kwargs):  # pragma: no cover - authority must stop first
        raise AssertionError("provider transport must not run before authority")


class _RecordingInitialWaveProvider:
    """Provider-free create double for the bounded six-member executor."""

    name = "openai"
    calls: list[str]

    def __init__(self) -> None:
        self.calls = []

    def create_interactive_only(self, *, body, idempotency_material, timeout_seconds):
        self.calls.append(idempotency_material)
        return {"id": f"resp_{idempotency_material}", "status": "queued"}, 1


def _policy() -> dict:
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": 5_000_000,
        "stage_ceilings_micro_usd": {
            "authoring_initial": 1_000_000,
            "creative_retry": 1_000_000,
            "polish": 1_000_000,
            "qualitative_critic": 1_000_000,
            "qualitative_candidate": 1_000_000,
        },
        "optional_stage_budget_behavior": {
            "polish": "skip",
            "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


def _bounded_initial_authority(root: Path):
    run_dir = root / "bounded-run"
    provider = OpenAIBoundedLifecycleProvider(
        run_dir=run_dir,
        api_key="qualification-only",
        model="gpt-5.6-luna",
        maximum_output_tokens=1_000,
        transport=_NoNetworkTransport(),
        max_transport_retries=0,
    )
    create_bounded_run(
        run_dir,
        compiled(),
        provider=provider,
        generation_profile={
            "spend_policy": _policy(),
            "optional_stages": {
                "polish": False,
                "qualitative_critic": False,
                "qualitative_candidate": False,
            },
        },
    )
    prepared = resume_bounded_run(run_dir, provider=provider)
    if prepared["initial_authoring_wave"]["state"] != "AWAITING_SPEND_AUTHORIZATION":
        raise AssertionError("bounded fixture did not stop at initial authority")
    inspection = inspect_temporal_lifecycle(
        run_dir,
        native_exclusive_access="declared",
        observed_at="2026-10-08T18:00:00Z",
    )
    request = build_external_authority_request_v2(inspection)
    inventory = {
        action["action_id"]: action
        for action in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action_id,
        "binding": copy.deepcopy(inventory[action_id]["binding"]),
        "authorization_reference": f"qualification:{index}",
    } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
    return run_dir, inspection, request, documents


class BoundedInitialWaveV2ContractSlice1(unittest.TestCase):
    @staticmethod
    def _rehash_inspection(inspection: dict) -> None:
        inspection["checkpoint_basis_sha256"] = hashlib.sha256(
            canonical_contract_json(inspection["checkpoint_basis"]).encode("utf-8")
        ).hexdigest()
        inspection["temporal_decision"]["checkpoint_basis_sha256"] = (
            inspection["checkpoint_basis_sha256"]
        )
        inspection["temporal_decision_sha256"] = hashlib.sha256(
            canonical_contract_json(inspection["temporal_decision"]).encode("utf-8")
        ).hexdigest()

    def test_initial_wave_request_and_grant_bind_the_semantic_six_member_projection(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, request, documents = _bounded_initial_authority(Path(temporary))
            self.assertEqual("initial_wave_admission", request["request_kind"])
            self.assertEqual(6, len(request["ordered_action_ids"]))
            self.assertEqual(6, request["initial_wave"]["member_count"])
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="api-decision-initial-v2",
                issuer="astrowoof-api",
                issued_at="2026-10-08T18:00:01Z",
            )
            self.assertEqual(request["initial_wave"], grant["initial_wave"])
            self.assertEqual(
                grant,
                validate_external_authority_grant_v2(request, inspection, grant, documents),
            )
            no_grant = build_no_grant_dispatch_result_v2(inspection)
            self.assertEqual(request["initial_wave"], no_grant["initial_wave"])
            self.assertEqual(no_grant, validate_no_grant_dispatch_result_v2(no_grant))

    def test_projection_or_binding_tamper_refuses_before_grant_construction(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, request, documents = _bounded_initial_authority(Path(temporary))
            changed = copy.deepcopy(request)
            changed["initial_wave"]["assignment_sha256"] = "0" * 64
            body = {key: value for key, value in changed.items()
                    if key != "external_authority_request_sha256"}
            changed["external_authority_request_sha256"] = hashlib.sha256(
                canonical_contract_json(body).encode("utf-8")
            ).hexdigest()
            with self.assertRaisesRegex(ValueError, "initial_wave"):
                validate_external_authority_request_v2_against_inspection(changed, inspection)
            changed_docs = copy.deepcopy(documents)
            changed_docs[0]["binding"]["request_sha256"] = "1" * 64
            with self.assertRaisesRegex(ValueError, "does not join"):
                build_external_authority_grant_v2(
                    request, inspection, changed_docs,
                    api_decision_id="api-decision-initial-v2",
                    issuer="astrowoof-api",
                    issued_at="2026-10-08T18:00:01Z",
                )

    def test_cross_route_initial_wave_projection_refuses_before_grant_or_no_grant(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, _, documents = _bounded_initial_authority(Path(temporary))
            mismatched = copy.deepcopy(inspection)
            mismatched["checkpoint_basis"]["native_route"]["route_family"] = "exact_natal"
            self._rehash_inspection(mismatched)
            with self.assertRaisesRegex(ValueError, "native route|initial-wave"):
                build_external_authority_request_v2(mismatched)

    def test_initial_wave_binding_descriptor_tamper_refuses_before_authority_export(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _, _, _ = _bounded_initial_authority(Path(temporary))
            descriptor = run_dir / "initial-authoring-wave-binding-bundle.json"
            descriptor.write_bytes(descriptor.read_bytes() + b"\n")
            inspection = inspect_temporal_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-10-08T18:00:01Z",
            )
            self.assertNotEqual(
                "request",
                inspection["checkpoint_basis"]["external_authority_state"]["kind"],
            )
            with self.assertRaisesRegex(ValueError, "no external-authority request"):
                build_external_authority_request_v2(inspection)

    def test_v2_grant_commits_one_semantic_wave_and_replays_without_second_create(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents = _bounded_initial_authority(Path(temporary))
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="api-decision-bounded-v2",
                issuer="astrowoof-api", issued_at="2026-10-08T18:00:01Z",
            )
            intent = commit_bounded_initial_wave_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            self.assertEqual("intent_committed", intent["outcome"])
            self.assertEqual("prepared_wave_semantic_member_order", intent["ordering_semantics"])
            self.assertEqual(request["ordered_action_ids"], intent["ordered_action_ids"])
            replayed_intent = commit_bounded_initial_wave_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=documents,
            )
            self.assertEqual(intent, replayed_intent)
            provider = _RecordingInitialWaveProvider()
            dispatched = dispatch_bounded_initial_wave_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], provider=provider,
            )
            self.assertEqual("detached_provider_pending", dispatched["outcome"])
            self.assertCountEqual(request["ordered_action_ids"], provider.calls)
            replayed_dispatch = dispatch_bounded_initial_wave_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"], provider=provider,
            )
            self.assertEqual(dispatched, replayed_dispatch)
            self.assertEqual(6, len(provider.calls))

    def test_v2_descriptor_tamper_refuses_before_intent_or_provider_io(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents = _bounded_initial_authority(Path(temporary))
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="api-decision-bounded-v2",
                issuer="astrowoof-api", issued_at="2026-10-08T18:00:01Z",
            )
            descriptor = run_dir / "initial-authoring-wave-binding-bundle.json"
            descriptor.write_bytes(descriptor.read_bytes() + b"\n")
            with self.assertRaisesRegex(Exception, "snapshot|lineage|digest"):
                commit_bounded_initial_wave_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents,
                )
            state = __import__("json").loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertNotIn("constrained_submission_intent", state["initial_authoring_wave"])

    def test_v2_pre_intent_failure_and_duplicate_authorization_do_not_mutate(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, request, documents = _bounded_initial_authority(Path(temporary))
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="api-decision-bounded-v2",
                issuer="astrowoof-api", issued_at="2026-10-08T18:00:01Z",
            )
            with self.assertRaisesRegex(RuntimeError, "injected"):
                commit_bounded_initial_wave_v2_dispatch_intent(
                    run_dir, request=request, inspection=inspection, grant=grant,
                    authorization_documents=documents,
                    failure_injector=lambda point: (
                        (_ for _ in ()).throw(RuntimeError("injected"))
                        if point == "before_durable_pre_submit_intent" else None
                    ),
                )
            state = __import__("json").loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                "AWAITING_SPEND_AUTHORIZATION", state["initial_authoring_wave"]["state"],
            )
            with self.assertRaisesRegex(ValueError, "partial|complete"):
                build_external_authority_grant_v2(
                    request, inspection, documents + [copy.deepcopy(documents[0])],
                    api_decision_id="api-decision-bounded-v2",
                    issuer="astrowoof-api", issued_at="2026-10-08T18:00:01Z",
                )

    def test_public_command_emits_typed_success_refusal_and_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, inspection, request, documents = _bounded_initial_authority(root)
            grant = build_external_authority_grant_v2(
                request, inspection, documents,
                api_decision_id="api-decision-bounded-v2",
                issuer="astrowoof-api", issued_at="2026-10-08T18:00:01Z",
            )
            def write(name, value):
                path = root / name
                path.write_text(__import__("json").dumps(value), encoding="utf-8")
                return path
            inspection_path = write("inspection.json", inspection)
            request_path = write("request.json", request)
            grant_path = write("grant.json", grant)
            document_paths = [write(f"authorization-{index}.json", value)
                              for index, value in enumerate(documents)]
            output = root / "result.json"
            arguments = [
                "--run-dir", str(run_dir), "--inspection", str(inspection_path),
                "--request", str(request_path), "--grant", str(grant_path),
                "--provider", "fake", "--output", str(output), "--log-level", "ERROR",
            ]
            for path in document_paths:
                arguments.extend(["--authorization", str(path)])
            self.assertEqual(0, authority_v2_main(arguments))
            success = __import__("json").loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                "astrowoof.bounded_initial_wave_v2_command_result.v1",
                success["schema_version"],
            )
            self.assertEqual("detached_provider_pending", success["outcome"])
            self.assertTrue(success["native_mutation_performed"])
            self.assertTrue(success["provider_io_performed"])
            self.assertTrue(success["checkpoint_published"])
            self.assertEqual(success, validate_bounded_initial_wave_v2_command_result(success))
            self.assertEqual(
                "astrowoof.bounded_initial_wave_v2_command_result.v1",
                read_bounded_initial_wave_v2_command_result_schema()["$id"],
            )
            self.assertEqual(0, authority_v2_main(arguments))
            replay = __import__("json").loads(output.read_text(encoding="utf-8"))
            self.assertEqual("exact_replay", replay["outcome"])
            self.assertFalse(replay["provider_io_performed"])
            self.assertFalse(replay["checkpoint_published"])
            altered = copy.deepcopy(replay)
            altered["provider_io_performed"] = True
            with self.assertRaisesRegex(ValueError, "exact replay"):
                validate_bounded_initial_wave_v2_command_result(altered)

            # A wrong grant is rendered as a closed pre-provider refusal.
            wrong_grant = copy.deepcopy(grant)
            wrong_grant["grant_sha256"] = "0" * 64
            wrong_grant_path = write("wrong-grant.json", wrong_grant)
            wrong_arguments = list(arguments)
            wrong_arguments[wrong_arguments.index(str(grant_path))] = str(wrong_grant_path)
            self.assertEqual(3, authority_v2_main(wrong_arguments))
            refusal = __import__("json").loads(output.read_text(encoding="utf-8"))
            self.assertEqual("pre_provider_refusal", refusal["outcome"])
            self.assertFalse(refusal["native_mutation_performed"])
            self.assertFalse(refusal["provider_io_performed"])


if __name__ == "__main__":
    unittest.main()
