from __future__ import annotations

import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import astrowoof_natal_authoring as public  # noqa: E402
from astrowoof_natal_authoring.initial_wave_contract import main  # noqa: E402


class TestInitialWavePublicContract(unittest.TestCase):
    def test_consumer_review_manifest_binds_packaged_resource_bytes(self) -> None:
        manifest_path = (
            ROOT / "docs" / "sprints" / "2026" / "08"
            / "20260818-initial-pass-concurrent-fanout-sprint3"
            / "fixtures" / "slice7-consumer-review-manifest.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual("api_approved", manifest["status"])
        package = ROOT / "src" / "astrowoof_natal_authoring" / "resources"
        for item in manifest["resources"]:
            self.assertEqual(
                item["sha256"],
                hashlib.sha256((package / item["installed_path"]).read_bytes()).hexdigest(),
            )

    def test_installed_readers_validate_all_closed_fixtures_and_schemas(self) -> None:
        combined = public.read_initial_wave_schema("wave")
        result_schema = public.read_initial_wave_schema("result")
        self.assertEqual(
            "astrowoof.initial_authoring_wave_contracts.v1", combined["$id"]
        )
        self.assertEqual(
            "astrowoof.initial_authoring_wave_result.v1", result_schema["$id"]
        )
        public.validate_initial_wave(public.read_initial_wave_fixture("prepared"))
        public.validate_wave_authorization_document(
            public.read_initial_wave_fixture("authorization")
        )
        for kind in ("six-id-detach", "partial-ambiguity"):
            public.validate_initial_wave_result(public.read_initial_wave_fixture(kind))

    def test_root_package_exports_provider_free_consumer_surface(self) -> None:
        expected = {
            "build_wave_authorization", "preflight_wave_authorization",
            "validate_initial_wave", "validate_wave_authorization_document",
            "validate_initial_wave_result", "read_initial_wave_fixture",
            "read_initial_wave_schema", "validate_initial_wave_fixture",
        }
        self.assertTrue(expected <= set(public.__all__))
        self.assertEqual(
            "detached_provider_pending",
            public.read_initial_wave_fixture("six-id-detach")["outcome"],
        )

    def test_unsupported_version_extra_field_and_aggregate_conflict_fail_closed(self) -> None:
        prepared = public.read_initial_wave_fixture("prepared")
        changed = copy.deepcopy(prepared)
        changed["schema_version"] = "astrowoof.initial_authoring_wave.v2"
        with self.assertRaises(public.InitialWaveError):
            public.validate_initial_wave(changed)
        changed = copy.deepcopy(prepared)
        changed["consumer_guess"] = True
        with self.assertRaises(public.InitialWaveError):
            public.validate_initial_wave(changed)
        result = public.read_initial_wave_fixture("partial-ambiguity")
        changed = copy.deepcopy(result)
        changed["ambiguous_action_ids"] = []
        with self.assertRaises(public.InitialWaveError):
            public.validate_initial_wave_result(changed)
        with self.assertRaises(ValueError):
            public.read_initial_wave_fixture("future-contract")

    def test_provider_free_cli_exports_exact_validated_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "nested" / "detach.json"
            with (
                patch("sys.argv", [
                    "astrowoof-initial-wave-contract", "--fixture",
                    "six-id-detach", "--output", str(target),
                ]),
                redirect_stdout(io.StringIO()) as stdout,
            ):
                main()
            expected = public.read_initial_wave_fixture("six-id-detach")
            self.assertEqual(expected, json.loads(target.read_text(encoding="utf-8")))
            self.assertEqual(expected, json.loads(stdout.getvalue()))


if __name__ == "__main__":
    unittest.main()
