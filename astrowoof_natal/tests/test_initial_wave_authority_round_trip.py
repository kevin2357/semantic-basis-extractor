from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.initial_wave import (  # noqa: E402
    InitialWaveError,
    ProviderCreateResult,
    build_wave_authorization,
    execute_initial_wave_creates,
    preflight_wave_authorization,
)
from astrowoof_natal_authoring.initial_wave_contract import (  # noqa: E402
    build_initial_wave_authority_inputs,
    validate_initial_wave_authority_inputs,
)
from astrowoof_natal.tests.test_initial_wave_binding_bundle_contract_proposal import (  # noqa: E402
    fixture,
)


def documents(inputs: dict) -> list[dict]:
    return [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": member["action_id"],
        "binding": deepcopy(member["binding"]),
        "authorization_reference": f"api:reservation:{index}",
    } for index, member in enumerate(
        inputs["binding_bundle"]["ordered_members"], 1
    )]


def envelope(inputs: dict, authorizations: list[dict]) -> dict:
    return build_wave_authorization(
        inputs["prepared_wave"], authorizations,
        reservation_set_reference="api:reservation-set:initial-wave",
        issuer="astrowoof-api", authorized_at="2026-08-18T22:00:00Z",
    )


class TestInitialWaveAuthorityRoundTrip(unittest.TestCase):
    def inputs(self, route: str = "exact_natal") -> dict:
        wave, bundle = fixture(route)
        return build_initial_wave_authority_inputs(wave, bundle)

    def test_api_shaped_exact_and_bounded_round_trip(self) -> None:
        for route in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route):
                inputs = self.inputs(route)
                validate_initial_wave_authority_inputs(inputs)
                authorizations = documents(inputs)
                authority = envelope(inputs, authorizations)
                preflight_wave_authorization(
                    inputs["prepared_wave"], authority, authorizations
                )
                submitted = []
                persisted = []
                result = execute_initial_wave_creates(
                    inputs["prepared_wave"], authorization=authority,
                    member_authorizations=authorizations,
                    submit=lambda member, _timeout: (
                        submitted.append(member["action_id"])
                        or ProviderCreateResult("resp_" + member["action_id"])
                    ),
                    persist_member_outcome=lambda member, outcome: persisted.append(
                        (member["action_id"], outcome["provider"]["id"])
                    ),
                )
                self.assertEqual("detached_provider_pending", result["outcome"])
                self.assertEqual(6, len(submitted))
                self.assertEqual(6, len(persisted))

    def test_member_authorization_mismatch_matrix_calls_no_submit(self) -> None:
        inputs = self.inputs()
        valid_documents = documents(inputs)
        valid_envelope = envelope(inputs, valid_documents)
        cases = {}
        changed = deepcopy(valid_documents)
        changed.reverse()
        cases["reordered"] = changed
        cases["missing"] = deepcopy(valid_documents[:-1])
        changed = deepcopy(valid_documents)
        changed[-1] = deepcopy(changed[0])
        cases["duplicate"] = changed
        changed = deepcopy(valid_documents)
        changed[-1]["action_id"] = "paid_ffffffffffffffffffffffff"
        cases["unknown"] = changed
        for field, value in (
            ("run_id", "other-run"),
            ("profile_sha256", "f" * 64),
            ("prepared_state_revision", 12),
            ("price_book_version", "future-price-book"),
            ("model", "changed-model"),
        ):
            changed = deepcopy(valid_documents)
            changed[-1]["binding"][field] = value
            cases[field] = changed
        for name, changed in cases.items():
            submitted = []
            with self.subTest(name=name), self.assertRaises(InitialWaveError):
                execute_initial_wave_creates(
                    inputs["prepared_wave"], authorization=valid_envelope,
                    member_authorizations=changed,
                    submit=lambda member, _timeout: submitted.append(member),
                    persist_member_outcome=lambda _member, _outcome: None,
                )
            self.assertEqual([], submitted)

    def test_wrapper_and_wave_mismatch_matrix_fails_before_authority(self) -> None:
        inputs = self.inputs()
        cases = {}
        changed = deepcopy(inputs)
        changed["authority_inputs_sha256"] = "0" * 64
        cases["wrapper_digest"] = changed
        changed = deepcopy(inputs)
        changed["binding_bundle"]["ordered_members"].reverse()
        cases["bundle_order"] = changed
        changed = deepcopy(inputs)
        changed["prepared_wave"]["wave_id"] = "wave_" + "f" * 24
        cases["wave_identity"] = changed
        changed = deepcopy(inputs)
        changed["binding_bundle"]["ordered_members"][0]["binding"][
            "request_sha256"
        ] = "f" * 64
        cases["binding_request"] = changed
        for name, changed in cases.items():
            with self.subTest(name=name), self.assertRaises(InitialWaveError):
                validate_initial_wave_authority_inputs(changed)


if __name__ == "__main__":
    unittest.main()
