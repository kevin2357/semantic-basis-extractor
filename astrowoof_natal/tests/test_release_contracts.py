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
from astrowoof_natal_authoring.provenance import (  # noqa: E402
    PROVENANCE_SCHEMA,
    initial_provenance,
    migrated_run_provenance,
    refresh_execution_provenance,
    resource_set_provenance,
)
from astrowoof_natal_authoring.smoke import (  # noqa: E402
    FIXTURE_FILES,
    SMOKE_SOURCE_ID,
    materialize_fixture,
)
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402


def write(path: Path, value: str = "{}\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


class TestReleaseContracts(unittest.TestCase):
    def test_packaged_gold_reference_omits_protected_birth_values(self) -> None:
        reference = json.loads(
            read_resource_text("references/natal.kevin.summary-gold-source.cards.json")
        )
        subject = reference["subject"]
        self.assertEqual("", subject["birth_date"])
        self.assertEqual("", subject["birth_datetime"])
        self.assertIsNone(subject["birth_latitude"])
        self.assertIsNone(subject["birth_longitude"])
        self.assertEqual("", subject["birth_location"])
        self.assertEqual("", subject["birth_date_precision"])

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
            self.assertEqual(4, len(manifest["artifacts"]))
            scopes = manifest["provenance"]["evidence_scopes"]
            self.assertEqual(
                "claim_local_selected_evidence",
                scopes["selected_cards"]["scope"],
            )
            self.assertEqual(
                "broader_synthesis_evidence",
                scopes["summary_and_whole_dog"]["scope"],
            )
            self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest["artifacts"]))
            self.assertEqual(64, len(record["delivery_artifact"]["sha256"]))

    def test_provenance_captures_declared_upstream_fields_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = self.projected_files(root)
            graph = {
                "metadata": {
                    "engine_version": "0.10.0",
                    "profile_id": "woofmapped_astrology.v0",
                    "context_id": "woofmapped.handler_guidance.v1",
                    "untrusted_extra": "not copied",
                },
                "source_identity": {"source_chart_id": "natal:ella"},
                "source_graph_ref": {
                    "graph_type": "canonical_astrology_graph",
                    "graph_version": "1.3.0",
                    "source_graph_hash": "abc123",
                },
                "target_ontology": "woofmapped_astrology.v0",
                "audit": {"request_hash": "request123"},
            }
            for path in paths.values():
                write(path, json.dumps(graph))
            _discovered, contract = discover_projected_input(root)
            provenance = initial_provenance(
                input_root=root,
                input_contract=contract,
                authoring_profile=authoring_profile(extraction={}, authoring={}, qa={}),
            )
            self.assertEqual(PROVENANCE_SCHEMA, provenance["schema_version"])
            context = provenance["input"]["subjects"][0]["contexts"][0]
            self.assertEqual(64, len(context["artifact"]["sha256"]))
            self.assertEqual("1.3.0", context["declared"]["source_graph_ref"]["graph_version"])
            self.assertNotIn("untrusted_extra", context["declared"]["metadata"])

    def test_resource_set_has_stable_aggregate_digest(self) -> None:
        first = resource_set_provenance()
        second = resource_set_provenance()
        self.assertEqual(first, second)
        self.assertGreater(first["resource_count"], 10)
        self.assertEqual(64, len(first["aggregate_sha256"]))

    def test_packaged_smoke_fixture_is_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            materialize_fixture(target)
            self.assertEqual(set(FIXTURE_FILES), {path.name for path in target.iterdir()})
            self.assertTrue(all((target / name).stat().st_size > 300_000 for name in FIXTURE_FILES))
            identities = {
                json.loads((target / name).read_text(encoding="utf-8"))
                ["source_identity"]["source_chart_id"]
                for name in FIXTURE_FILES
            }
            self.assertEqual({SMOKE_SOURCE_ID}, identities)

    def test_legacy_migration_marks_input_provenance_unavailable(self) -> None:
        provenance = migrated_run_provenance(
            previous_schema="astrowoof.semantic_closure_run.v0.6",
            authoring_profile=None,
        )
        self.assertEqual("unavailable_from_legacy_run", provenance["input"]["status"])
        self.assertEqual(
            "astrowoof.semantic_closure_run.v0.6",
            provenance["migration"]["from_run_schema"],
        )

    def test_execution_provenance_distinguishes_requested_and_actual_models(self) -> None:
        state = {
            "provider": "openai",
            "service_level": "interactive",
            "accounting": {"attempt_count": 1},
            "provenance": {},
            "passes": {"ella_1": {"attempts": [{"provider_metadata": {
                "requested_model": "gpt-requested",
                "model": "gpt-observed",
                "response_id": "resp_123",
            }}]}},
            "subjects": {},
        }
        refresh_execution_provenance(state)
        execution = state["provenance"]["execution"]
        self.assertEqual(["gpt-requested"], execution["requested_models"])
        self.assertEqual(["gpt-observed"], execution["observed_models"])
        self.assertEqual(["resp_123"], execution["response_ids"])

    def test_v010_release_handoff_is_internally_consistent(self) -> None:
        release = ROOT / "releases" / "0.1.0"
        manifest = json.loads(
            (release / "release-manifest.json").read_text(encoding="utf-8")
        )
        artifact = manifest["artifact"]
        digest = artifact["sha256"]
        filename = artifact["filename"]

        self.assertEqual("0.1.0", manifest["version"])
        self.assertEqual(
            "astrowoof-natal-authoring-v0.1.0", manifest["release_tag"]
        )
        self.assertEqual(64, len(digest))
        self.assertTrue(manifest["build"]["byte_reproducible"])

        checksum = (release / "SHA256SUMS.txt").read_text(
            encoding="utf-8"
        ).strip()
        self.assertEqual(f"{digest}  {filename}", checksum)

        requirement = (release / "requirements-api-worker.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn(filename, requirement)
        self.assertIn(f"--hash=sha256:{digest}", requirement)

        smoke = json.loads(
            (
                ROOT
                / "docs"
                / "sprints"
                / "2026"
                / "08"
                / "20260805-release-engineering-sprint1"
                / "results"
                / "slice7-final-installed-smoke.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("pass", smoke["status"])
        self.assertTrue(smoke["require_installed"])
        self.assertEqual(
            manifest["resources"]["aggregate_sha256"],
            smoke["checks"]["resource_set_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
