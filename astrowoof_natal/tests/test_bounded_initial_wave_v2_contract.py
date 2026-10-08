from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_lifecycle import create_bounded_run, resume_bounded_run
from astrowoof_natal_authoring.bounded_provider import OpenAIBoundedLifecycleProvider
from astrowoof_natal_authoring.spend import PRICE_BOOK_VERSION
from astrowoof_natal_authoring.temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
    validate_external_authority_request_v2_against_inspection,
)
from astrowoof_natal_authoring.external_authority_v2 import (
    build_external_authority_grant_v2,
    build_no_grant_dispatch_result_v2,
    validate_external_authority_grant_v2,
    validate_no_grant_dispatch_result_v2,
)
from test_bounded_authoring import compiled


class _NoNetworkTransport:
    def request_json(self, **_kwargs):  # pragma: no cover - authority must stop first
        raise AssertionError("provider transport must not run before authority")


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
            from astrowoof_natal_authoring.lifecycle_contracts import canonical_contract_json
            import hashlib
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


if __name__ == "__main__":
    unittest.main()
