from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import astrowoof_natal_authoring as public
from astrowoof_natal_authoring.happy_path_qa import main


class HappyPathQualificationTests(unittest.TestCase):
    def test_public_surface_and_reproducibility(self) -> None:
        names = (
            "read_ordinary_v2_happy_path_bundle_schema",
            "read_ordinary_v2_happy_path_fixture",
            "read_ordinary_v2_happy_path_qualification_schema",
            "run_ordinary_v2_happy_path_bundle",
            "run_ordinary_v2_happy_path_qualification",
            "validate_ordinary_v2_happy_path_bundle",
            "validate_ordinary_v2_happy_path_qualification",
        )
        for name in names:
            self.assertTrue(callable(getattr(public, name)))
        first = public.run_ordinary_v2_happy_path_bundle()
        second = public.run_ordinary_v2_happy_path_bundle()
        self.assertEqual(first, second)
        public.validate_ordinary_v2_happy_path_bundle(first)

    def test_two_real_engine_witnesses_and_aggregate_authority(self) -> None:
        bundle = public.run_ordinary_v2_happy_path_bundle()
        retry_pair, critic = bundle["witnesses"]
        self.assertEqual("two_retries_out_of_order", retry_pair["witness_id"])
        self.assertEqual(2, retry_pair["authority"]["aggregate_action_count"])
        self.assertEqual(
            sorted(retry_pair["authority"]["ordered_action_ids"]),
            retry_pair["authority"]["ordered_action_ids"],
        )
        self.assertEqual(2, len({item["binding_sha256"] for item in retry_pair["authority"]["members"]}))
        self.assertEqual("retry_then_qualitative_critic", critic["witness_id"])
        self.assertEqual("qualitative_critic", critic["authority"]["members"][0]["stage"])
        for witness in bundle["witnesses"]:
            self.assertEqual(
                "post_fan_in_selector_authority_and_replay",
                witness["evidence_scope"],
            )
            self.assertTrue(witness["fixture_installed_precursors"])
            self.assertEqual("exact_replay", witness["replay_outcome"])
            self.assertEqual(0, witness["duplicate_create_count"])
            self.assertEqual(0, witness["duplicate_local_consumption_count"])

    def test_receipt_binding_and_projection_mutations_refuse(self) -> None:
        bundle = public.run_ordinary_v2_happy_path_bundle()
        changed = copy.deepcopy(bundle)
        changed["qualification_receipt_sha256"] = "f" * 64
        body = {key: value for key, value in changed.items() if key != "bundle_sha256"}
        import hashlib
        changed["bundle_sha256"] = hashlib.sha256(json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        ).encode("utf-8")).hexdigest()
        with self.assertRaises(ValueError):
            public.validate_ordinary_v2_happy_path_bundle(changed)

        changed = copy.deepcopy(bundle)
        changed["witnesses"][0]["unexpected"] = True
        with self.assertRaises(ValueError):
            public.validate_ordinary_v2_happy_path_bundle(changed)

        changed = copy.deepcopy(bundle)
        changed["witnesses"][0]["evidence_scope"] = "end_to_end_production"
        body = {key: value for key, value in changed.items() if key != "bundle_sha256"}
        import hashlib
        changed["bundle_sha256"] = hashlib.sha256(json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        ).encode("utf-8")).hexdigest()
        with self.assertRaises(ValueError):
            public.validate_ordinary_v2_happy_path_bundle(changed)

        changed = copy.deepcopy(bundle)
        changed["witnesses"][0]["authority"]["ordered_action_ids"].reverse()
        with self.assertRaises(ValueError):
            public.validate_ordinary_v2_happy_path_bundle(changed)

    def test_public_artifacts_exclude_sensitive_material(self) -> None:
        rendered = json.dumps({
            "fixture": public.read_ordinary_v2_happy_path_fixture(),
            "receipt": public.run_ordinary_v2_happy_path_qualification(),
            "bundle": public.run_ordinary_v2_happy_path_bundle(),
        }, sort_keys=True)
        for prohibited in (
            "workspace-snapshot.json", "provider_payload", "private_selector",
            "resp_fixture_", "sanitized critic qualification", "OPENAI_API_KEY",
        ):
            self.assertNotIn(prohibited, rendered)

    def test_cli_exports_closed_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt = root / "receipt.json"
            bundle = root / "bundle.json"
            fixture = root / "fixture.json"
            self.assertEqual(0, main(["--output", str(receipt)]))
            self.assertEqual(0, main(["--bundle", "--output", str(bundle)]))
            self.assertEqual(0, main(["--fixture", "--output", str(fixture)]))
            public.validate_ordinary_v2_happy_path_qualification(json.loads(receipt.read_text(encoding="utf-8")))
            public.validate_ordinary_v2_happy_path_bundle(json.loads(bundle.read_text(encoding="utf-8")))
            self.assertEqual(public.read_ordinary_v2_happy_path_fixture(), json.loads(fixture.read_text(encoding="utf-8")))

    def test_optional_json_schemas(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema is optional")
        Draft202012Validator.check_schema(public.read_ordinary_v2_happy_path_qualification_schema())
        Draft202012Validator.check_schema(public.read_ordinary_v2_happy_path_bundle_schema())
        Draft202012Validator(public.read_ordinary_v2_happy_path_qualification_schema()).validate(
            public.run_ordinary_v2_happy_path_qualification(),
        )
        Draft202012Validator(public.read_ordinary_v2_happy_path_bundle_schema()).validate(
            public.run_ordinary_v2_happy_path_bundle(),
        )


if __name__ == "__main__":
    unittest.main()
