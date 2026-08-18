from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.initial_wave import (  # noqa: E402
    InitialWaveError,
    build_initial_wave_binding_bundle,
    validate_initial_wave_binding_bundle,
    validate_initial_wave_binding_bundle_against_wave,
)
from astrowoof_natal.tests.test_initial_wave_binding_bundle_contract_proposal import (  # noqa: E402
    fixture,
)


class TestInitialWaveBindingBundle(unittest.TestCase):
    def bundle(self, route: str = "exact_natal") -> tuple[dict, dict]:
        prepared, proposal = fixture(route)
        bundle = build_initial_wave_binding_bundle(
            prepared, [item["binding"] for item in proposal["ordered_members"]]
        )
        return prepared, bundle

    def test_build_is_deterministic_and_provider_safe(self) -> None:
        for route in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route):
                prepared, bundle = self.bundle(route)
                self.assertEqual(bundle, self.bundle(route)[1])
                validate_initial_wave_binding_bundle_against_wave(bundle, prepared)
                self.assertEqual(6, len(bundle["ordered_members"]))
                self.assertNotIn("input", repr(bundle))
                self.assertNotIn("authorization_reference", repr(bundle))

    def test_closed_bundle_and_binding_fields(self) -> None:
        _prepared, bundle = self.bundle()
        for location in ("bundle", "member", "binding"):
            changed = deepcopy(bundle)
            if location == "bundle":
                changed["extra"] = True
            elif location == "member":
                changed["ordered_members"][0]["extra"] = True
            else:
                changed["ordered_members"][0]["binding"]["extra"] = True
            with self.subTest(location=location), self.assertRaises(InitialWaveError):
                validate_initial_wave_binding_bundle(changed)

    def test_tampering_and_cross_wave_mismatch_fail_closed(self) -> None:
        prepared, bundle = self.bundle()
        cases = {}
        changed = deepcopy(bundle)
        changed["bundle_sha256"] = "0" * 64
        cases["bundle_digest"] = changed
        changed = deepcopy(bundle)
        changed["ordered_members"][0]["binding"]["model"] = "changed"
        cases["binding"] = changed
        for name, changed in cases.items():
            with self.subTest(name=name), self.assertRaises(InitialWaveError):
                validate_initial_wave_binding_bundle(changed)
        bounded, _bundle = fixture("bounded_natal")
        with self.assertRaises(InitialWaveError) as caught:
            validate_initial_wave_binding_bundle_against_wave(bundle, bounded)
        self.assertEqual("wave_mismatch", caught.exception.reason_code)


if __name__ == "__main__":
    unittest.main()
