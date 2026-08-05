from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import package_subject_delivery  # noqa: E402
from astrowoof_natal_authoring.contracts import (  # noqa: E402
    AUTHORING_PROFILE_SCHEMA,
    DELIVERY_MANIFEST_SCHEMA,
    INPUT_BUNDLE_SCHEMA,
    PUBLIC_RUN_SCHEMA,
    SUBJECT_PARAMS_SCHEMA,
    authoring_profile,
    discover_projected_input,
    normalize_subject_params,
    public_run_state,
)


def write(path: Path, value: str = "{}\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


class TestReleaseContracts(unittest.TestCase):
    def projected_files(self, root: Path, subject: str = "ella") -> dict[str, Path]:
        suffixes = {
            "general": "general",
            "direct_to_dog": "d2d",
            "handler": "handler",
            "hybrid": "hybrid",
        }
        result = {}
        for context, suffix in suffixes.items():
            path = root / f"natal.{subject}.woof.{suffix}.json"
            write(path)
            result[context] = path
        return result

    def test_legacy_input_normalizes_to_versioned_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.projected_files(root)
            discovered, manifest = discover_projected_input(root)
            self.assertEqual(set(discovered["ella"]), {
                "general", "direct_to_dog", "handler", "hybrid"
            })
            self.assertEqual(INPUT_BUNDLE_SCHEMA, manifest["schema_version"])
            self.assertEqual("legacy-directory-v0", manifest["source_format"])

    def test_explicit_input_manifest_is_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = self.projected_files(root / "ella")
            manifest = {
                "schema_version": INPUT_BUNDLE_SCHEMA,
                "subjects": [{
                    "subject_id": "ella",
                    "contexts": {
                        key: str(path.relative_to(root)).replace("\\", "/")
                        for key, path in paths.items()
                    },
                }],
            }
            write(root / "astrowoof-input-manifest.json", json.dumps(manifest))
            discovered, normalized = discover_projected_input(root)
            self.assertEqual(paths["handler"].resolve(), discovered["ella"]["handler"])
            self.assertEqual("manifest-v0.1", normalized["source_format"])

    def test_explicit_manifest_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = {
                "schema_version": INPUT_BUNDLE_SCHEMA,
                "subjects": [{
                    "subject_id": "ella",
                    "contexts": {name: "../outside.json" for name in (
                        "general", "direct_to_dog", "handler", "hybrid"
                    )},
                }],
            }
            write(root / "astrowoof-input-manifest.json", json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "escapes input package"):
                discover_projected_input(root)

    def test_unversioned_subject_params_normalize(self) -> None:
        normalized = normalize_subject_params(
            {"display_name": "Ella", "birth_latitude": 38.7},
            subject_id="ella",
            source="params.json",
        )
        self.assertEqual(SUBJECT_PARAMS_SCHEMA, normalized["schema_version"])
        self.assertEqual("ella", normalized["subject_id"])

    def test_public_state_excludes_operator_details(self) -> None:
        public = public_run_state({
            "status": "AUTHORING",
            "created_at": "start",
            "updated_at": "now",
            "service_level": "interactive",
            "input_package": "secret-path",
            "provider_configuration": {"model": "secret"},
            "passes": {
                "ella_1": {"state": "PASS_QA_ACCEPTED"},
                "ella_2": {"state": "GENERATED"},
            },
            "subjects": {},
        })
        self.assertEqual(PUBLIC_RUN_SCHEMA, public["schema_version"])
        self.assertEqual(1, public["progress"]["passes_accepted"])
        self.assertNotIn("input_package", public)
        self.assertNotIn("provider_configuration", public)

    def test_delivery_zip_contains_versioned_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "final" / "ella"
            artifacts = {}
            for role in ("deck", "assembly_report", "validation_report", "lint_report"):
                path = final / f"{role}.json"
                write(path)
                artifacts[role] = str(path)
            profile = authoring_profile(extraction={}, authoring={}, qa={})
            self.assertEqual(AUTHORING_PROFILE_SCHEMA, profile["schema_version"])
            write(root / "run.json", json.dumps({
                "schema_version": "astrowoof.semantic_closure_run.v0.7",
                "authoring_profile": profile,
            }))
            record = {"subject": "ella", "state": "DELIVERY_COMPLETE", **artifacts}
            delivery = package_subject_delivery(record, run_dir=root)
            with zipfile.ZipFile(delivery) as archive:
                name = "natal.ella.delivery-manifest.json"
                self.assertIn(name, archive.namelist())
                manifest = json.loads(archive.read(name))
            self.assertEqual(DELIVERY_MANIFEST_SCHEMA, manifest["schema_version"])
            self.assertEqual(profile, manifest["authoring_profile"])


if __name__ == "__main__":
    unittest.main()
