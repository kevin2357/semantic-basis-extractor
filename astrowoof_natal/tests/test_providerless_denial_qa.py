from __future__ import annotations

import copy
import hashlib
import json
import unittest
from importlib.resources import files

from astrowoof_natal_authoring import (
    read_providerless_denial_settlement_fixture,
    read_providerless_denial_settlement_qualification_schema,
    read_providerless_denial_settlement_qualification_v02_schema,
    run_providerless_denial_settlement_qualification,
    run_providerless_denial_settlement_qualification_v02,
    validate_providerless_denial_settlement_qualification,
    validate_providerless_denial_settlement_qualification_v02,
)
from astrowoof_natal_authoring.providerless_denial_qa import _installed_version


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _with_fixture_release(receipt: dict, fixture_release: str) -> dict:
    normalized = copy.deepcopy(receipt)
    normalized["sbe_release"] = fixture_release
    normalized["receipt_sha256"] = _digest({
        key: item for key, item in normalized.items() if key != "receipt_sha256"
    })
    return normalized


class ProviderlessDenialQualificationTests(unittest.TestCase):
    def test_semantic_qualification_is_reproducible_and_provider_free(self) -> None:
        first = run_providerless_denial_settlement_qualification()
        second = run_providerless_denial_settlement_qualification()
        self.assertEqual(first, second)
        self.assertEqual(_installed_version(), first["sbe_release"])
        self.assertEqual(0, first["provider_create_count"])
        self.assertEqual(0, first["provider_retrieval_count"])
        self.assertEqual(0, first["provider_transport_count"])
        self.assertTrue(first["assertions"]["successor_final"])
        validate_providerless_denial_settlement_qualification(first)

    def test_detailed_receipt_joins_precursor_and_successor_publications(self) -> None:
        value = run_providerless_denial_settlement_qualification_v02()
        validate_providerless_denial_settlement_qualification_v02(value)
        identity = value["publication_identity"]
        for prefix in ("precursor", "successor"):
            self.assertEqual(
                identity[f"{prefix}_result_id"],
                f"nres_{identity[f'{prefix}_result_sha256'][:24]}",
            )
            self.assertEqual(
                identity[f"{prefix}_receipt_id"],
                f"nreceipt_{identity[f'{prefix}_receipt_sha256'][:24]}",
            )

    def test_rehashed_semantic_mutations_are_refused(self) -> None:
        mutations = (
            ("precursor", "custody_finality", "final"),
            ("precursor", "providerless_denial_action_ids", []),
            ("denial", "exact_replay_outcome", "applied"),
            ("successor", "custody_finality", "providerless_denial_required"),
            ("assertions", "lineage_contiguous", False),
        )
        for section, field, replacement in mutations:
            with self.subTest(section=section, field=field):
                value = run_providerless_denial_settlement_qualification()
                value[section][field] = replacement
                value["receipt_sha256"] = _digest({
                    key: item for key, item in value.items() if key != "receipt_sha256"
                })
                with self.assertRaises(ValueError):
                    validate_providerless_denial_settlement_qualification(value)

    def test_rehashed_publication_identity_mutation_is_refused(self) -> None:
        value = run_providerless_denial_settlement_qualification_v02()
        value["publication_identity"]["successor_result_id"] = "nres_" + "0" * 24
        value["receipt_sha256"] = _digest({
            key: item for key, item in value.items() if key != "receipt_sha256"
        })
        with self.assertRaises(ValueError):
            validate_providerless_denial_settlement_qualification_v02(value)

    def test_packaged_fixture_matches_release_normalized_receipt(self) -> None:
        resource = files("astrowoof_natal_authoring.resources").joinpath(
            "fixtures/lifecycle/providerless-denial-settlement-qualification.v1.json"
        )
        fixture = json.loads(resource.read_text(encoding="utf-8"))
        self.assertEqual(
            _with_fixture_release(
                run_providerless_denial_settlement_qualification(), fixture["sbe_release"]
            ),
            fixture,
        )
        self.assertEqual(fixture, read_providerless_denial_settlement_fixture())

    def test_packaged_schema_validates_when_jsonschema_is_available(self) -> None:
        schema = read_providerless_denial_settlement_qualification_schema()
        self.assertEqual(
            "astrowoof.providerless_denial_settlement_qualification.v1", schema["$id"]
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(schema).validate(
            run_providerless_denial_settlement_qualification()
        )

    def test_detailed_schema_is_packaged(self) -> None:
        schema = read_providerless_denial_settlement_qualification_v02_schema()
        self.assertEqual(
            "astrowoof.providerless_denial_settlement_qualification.v2", schema["$id"]
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(schema).validate(
            run_providerless_denial_settlement_qualification_v02()
        )


if __name__ == "__main__":
    unittest.main()
