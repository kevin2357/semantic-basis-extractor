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
from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal.tests.test_initial_wave_binding_bundle_contract_proposal import (  # noqa: E402
    fixture as binding_fixture,
)


class TestInitialWavePublicContract(unittest.TestCase):
    def make_authority_run(self, root: Path, route: str = "exact_natal") -> Path:
        run_dir = root / "run"
        run_dir.mkdir(parents=True)
        wave, bundle = binding_fixture(route)
        state = {
            "schema_version": (
                "astrowoof.bounded_natal.authoring_run.v2"
                if route == "bounded_natal"
                else "astrowoof.semantic_closure_run.v0.9"
            ),
            "run_id": wave["run_id"],
            "state_revision": 12,
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(run_dir),
            },
            "initial_authoring_wave": {
                **wave, "state": "AWAITING_SPEND_AUTHORIZATION", "requests": {},
            },
        }
        (run_dir / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (run_dir / "initial-authoring-wave-binding-bundle.json").write_text(
            json.dumps(bundle, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(run_dir)
        return run_dir

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

    def test_binding_bundle_review_manifest_binds_packaged_resource_bytes(self) -> None:
        manifest_path = (
            ROOT / "docs" / "sprints" / "2026" / "08"
            / "20260818-initial-wave-binding-bundle-patch-sprint4"
            / "fixtures" / "slice2-consumer-review-manifest.json"
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
        bundle_schema = public.read_initial_wave_schema("binding-bundle")
        inputs_schema = public.read_initial_wave_schema("authority-inputs")
        self.assertEqual(
            "astrowoof.initial_authoring_wave_contracts.v1", combined["$id"]
        )
        self.assertEqual(
            "astrowoof.initial_authoring_wave_result.v1", result_schema["$id"]
        )
        self.assertEqual(
            "astrowoof.initial_authoring_wave_binding_bundle.v1",
            bundle_schema["$id"],
        )
        self.assertEqual(
            "astrowoof.initial_authoring_wave_authority_inputs.v1",
            inputs_schema["$id"],
        )
        public.validate_initial_wave(public.read_initial_wave_fixture("prepared"))
        public.validate_wave_authorization_document(
            public.read_initial_wave_fixture("authorization")
        )
        for kind in ("six-id-detach", "partial-ambiguity"):
            public.validate_initial_wave_result(public.read_initial_wave_fixture(kind))
        for kind in ("exact-binding-bundle", "bounded-binding-bundle"):
            public.validate_initial_wave_binding_bundle(
                public.read_initial_wave_fixture(kind)
            )

    def test_root_package_exports_provider_free_consumer_surface(self) -> None:
        expected = {
            "build_wave_authorization", "preflight_wave_authorization",
            "validate_initial_wave", "validate_wave_authorization_document",
            "validate_initial_wave_result", "read_initial_wave_fixture",
            "read_initial_wave_schema", "validate_initial_wave_fixture",
            "build_initial_wave_authority_inputs",
            "build_initial_wave_binding_bundle",
            "read_initial_wave_authority_inputs",
            "validate_initial_wave_authority_inputs",
            "validate_initial_wave_binding_bundle",
            "validate_initial_wave_binding_bundle_against_wave",
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

    def test_snapshot_validating_reader_returns_joined_pair_for_both_routes(self) -> None:
        for route in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as temporary:
                run_dir = self.make_authority_run(Path(temporary), route)
                value = public.read_initial_wave_authority_inputs(run_dir)
                public.validate_initial_wave_authority_inputs(value)
                self.assertEqual(
                    value["prepared_wave"]["wave_sha256"],
                    value["binding_bundle"]["wave_sha256"],
                )
                self.assertEqual(route, value["prepared_wave"]["route_family"])

    def test_joined_reader_fails_closed_on_snapshot_or_join_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_authority_run(Path(temporary))
            bundle_path = run_dir / "initial-authoring-wave-binding-bundle.json"
            original = bundle_path.read_bytes()
            bundle_path.write_bytes(original + b" ")
            with self.assertRaises(public.InitialWaveError) as caught:
                public.read_initial_wave_authority_inputs(run_dir)
            self.assertEqual("snapshot_invalid", caught.exception.reason_code)

    def test_cli_exports_pair_and_rejects_output_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = self.make_authority_run(root)
            target = root / "api" / "authority-inputs.json"
            with (
                patch("sys.argv", [
                    "astrowoof-initial-wave-contract", "--initial-wave-inputs",
                    "--run-dir", str(run_dir), "--output", str(target),
                ]),
                redirect_stdout(io.StringIO()) as stdout,
            ):
                main()
            expected = public.read_initial_wave_authority_inputs(run_dir)
            self.assertEqual(expected, json.loads(target.read_text(encoding="utf-8")))
            self.assertEqual(expected, json.loads(stdout.getvalue()))
            with (
                patch("sys.argv", [
                    "astrowoof-initial-wave-contract", "--initial-wave-inputs",
                    "--run-dir", str(run_dir), "--output",
                    str(run_dir / "unsafe.json"),
                ]),
                self.assertRaises(public.InitialWaveError) as caught,
            ):
                main()
            self.assertEqual("unsafe_output_path", caught.exception.reason_code)


if __name__ == "__main__":
    unittest.main()
