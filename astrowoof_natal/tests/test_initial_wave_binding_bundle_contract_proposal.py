from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.initial_wave import (  # noqa: E402
    InitialWaveMemberSpec,
    build_initial_wave,
)
from astrowoof_natal_authoring.pass_protocol import canonical_sha256  # noqa: E402
from astrowoof_natal_authoring.spend import PRICE_BOOK_VERSION  # noqa: E402


SCHEMA_PATH = REPOSITORY / (
    "astrowoof_natal/docs/sprints/2026/08/"
    "20260818-initial-wave-binding-bundle-patch-sprint4/contracts/"
    "initial-authoring-wave-binding-bundle.v1.schema.json"
)
FORBIDDEN_KEYS = {
    "input", "instructions", "prompt", "request_body", "response_format",
    "subject", "birth_datetime", "latitude", "longitude", "provenance",
    "provider_id", "authorization_reference", "reservation_set_reference",
}


def fixture(route_family: str) -> tuple[dict, dict]:
    bounded = route_family == "bounded_natal"
    members: list[InitialWaveMemberSpec] = []
    bindings: list[dict] = []
    for number in range(1, 7):
        route = (
            f"bounded_natal:bounded-pass-{number:02d}:attempt-001"
            if bounded else f"kevin_{number}:attempt-001"
        )
        binding = {
            "run_id": "run_initial_wave_fixture",
            "profile_sha256": "a" * 64,
            "prepared_state_revision": 11,
            "stage": "authoring_initial",
            "route": route,
            "request_sha256": f"{number:x}" * 64,
            "model": "gpt-5.6-terra",
            "service_level": "interactive",
            "maximum_output_tokens": 30000,
            "commitment_micro_usd": 700000 + number,
            "price_book_version": PRICE_BOOK_VERSION,
        }
        digest = canonical_sha256(binding)
        bindings.append(binding)
        members.append(InitialWaveMemberSpec(
            action_id="paid_" + digest[:24],
            binding=binding,
            pass_id=(f"bounded-pass-{number:02d}" if bounded else f"kevin_{number}"),
            pass_number=number,
        ))
    wave = build_initial_wave(
        run_id="run_initial_wave_fixture",
        route_family=route_family,
        route_contract=(
            "astrowoof.bounded_natal.authoring_run.v2" if bounded
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        assignment_sha256="b" * 64,
        profile_sha256="a" * 64,
        preparation_basis_revision=11,
        members=members,
    )
    bundle = {
        "schema_version": "astrowoof.initial_authoring_wave_binding_bundle.v1",
        "wave_id": wave["wave_id"],
        "wave_sha256": wave["wave_sha256"],
        "run_id": wave["run_id"],
        "route_family": wave["route_family"],
        "profile_sha256": wave["profile_sha256"],
        "preparation_basis_revision": wave["preparation_basis_revision"],
        "price_book_version": wave["price_book_version"],
        "member_count": 6,
        "ordered_members": [
            {
                "action_id": member.action_id,
                "pass_id": member.pass_id,
                "pass_number": member.pass_number,
                "binding": deepcopy(binding),
                "binding_sha256": canonical_sha256(binding),
            }
            for member, binding in zip(members, bindings)
        ],
        "aggregate_maximum_commitment_micro_usd": sum(
            binding["commitment_micro_usd"] for binding in bindings
        ),
    }
    bundle["bundle_sha256"] = canonical_sha256(bundle)
    return wave, bundle


class TestInitialWaveBindingBundleContractProposal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_exact_and_bounded_representative_fixtures_validate(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional in the source environment")
        expected = {
            "exact_natal": (
                "wave_049d85b3c0deec0e26917e89",
                "c1c4c44afe649f7dcb1eb66c1ac7a3b3d1aea2449f8111b6d7582bc8303f43ad",
            ),
            "bounded_natal": (
                "wave_f830efd2c0245a9fe0626c55",
                "cd497479bd6685c2d1a895994bd42a8285acd1b5016153916f2fa43f56bdf23b",
            ),
        }
        for route, identities in expected.items():
            with self.subTest(route=route):
                wave, bundle = fixture(route)
                jsonschema.validate(bundle, self.schema)
                self.assertEqual(identities, (wave["wave_id"], bundle["bundle_sha256"]))
                self.assertEqual(
                    [member["action_id"] for member in wave["ordered_members"]],
                    [member["action_id"] for member in bundle["ordered_members"]],
                )
                self.assertEqual(
                    [member["binding_sha256"] for member in wave["ordered_members"]],
                    [member["binding_sha256"] for member in bundle["ordered_members"]],
                )

    def test_bundle_disclosure_is_binding_only(self) -> None:
        for route in ("exact_natal", "bounded_natal"):
            _wave, bundle = fixture(route)
            serialized = json.dumps(bundle, sort_keys=True)
            for forbidden in FORBIDDEN_KEYS:
                with self.subTest(route=route, forbidden=forbidden):
                    self.assertNotIn(f'"{forbidden}"', serialized)

    def test_schema_rejects_extra_or_provider_payload_fields(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional in the source environment")
        _wave, bundle = fixture("exact_natal")
        for field, value in (
            ("unexpected", True),
            ("prompt", "private"),
            ("request_body", {"input": "private"}),
        ):
            changed = deepcopy(bundle)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(changed, self.schema)


if __name__ == "__main__":
    unittest.main()
