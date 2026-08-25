from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.bounded_admission import (  # noqa: E402
    BoundedAdmissionError,
    REQUIRED_CONTEXTS,
    REQUIRED_CAPABILITIES,
    REQUIRED_LIMITATIONS,
    SUPPORTED_UPSTREAM_CONTRACTS,
    admit_bounded_family,
)
from astrowoof_natal_authoring.extractor import load_and_validate_contexts  # noqa: E402


def family() -> list[dict]:
    values = []
    for index, (context_id, context_version) in enumerate(
        sorted(REQUIRED_CONTEXTS.items()), 1
    ):
        values.append(
            {
                "metadata": {
                    "output_contract": "projected_bounded_semantic_graph.v1",
                    "contract_version": "1.0.0",
                    "engine_version": "0.11.1",
                    "profile_id": "woofmapped_bounded_astrology.v0",
                    "profile_version": "0.1.0",
                    "context_id": context_id,
                    "context_version": context_version,
                    "projection_id": f"projection:{index}",
                    "runtime_identity": {
                        "distribution": {
                            "name": "semantic-projection-core",
                            "version": "0.11.1",
                        },
                        "route": "bounded_natal_projection",
                        "output_contract": "projected_bounded_semantic_graph.v1",
                    },
                },
                "source_identity": {
                    "source_chart_id": "opaque-dog-id",
                    "source_artifact_sha256": "a" * 64,
                    "protected_birth_location": "must-not-enter-event",
                },
                "source_artifact_ref": {
                    "package_type": "bounded_natal_dataset",
                    "source_artifact_sha256": "a" * 64,
                },
                "target_ontology": "woofmapped_astrology.v0",
                "source_capabilities": deepcopy(REQUIRED_CAPABILITIES),
                "source_feature_dispositions": {
                    "representative_longitudes": "prohibited_precision_laundering",
                    "structural_strength_scores": "unavailable_for_bounded_invariant_subgraph",
                },
                "source_evidence": {"semantic_sha256": "b" * 64, "records": {}},
                "projected_term_registry": {
                    "registry_id": "bounded-terms",
                    "registry_version": "0.1.0",
                    "terms": {"term": {"term_type": "operator"}},
                },
                "objects": [],
                "relationships": [],
                "provenance": {
                    "upstream_contracts": deepcopy(SUPPORTED_UPSTREAM_CONTRACTS),
                    "context_epistemic_policy": "certainty_invariant_across_contexts",
                },
                "limitations": sorted(REQUIRED_LIMITATIONS),
            }
        )
    return values


def passing_validator(artifacts):
    contexts = sorted(value["metadata"]["context_id"] for value in artifacts)
    return {
        "validation_contract": "bounded_parallel_context_validation.v1",
        "status": "passed",
        "profile_id": "woofmapped_bounded_astrology.v0",
        "profile_version": "0.1.0",
        "source_artifact_sha256": "a" * 64,
        "contexts": contexts,
        "context_versions": {
            value["metadata"]["context_id"]: value["metadata"]["context_version"]
            for value in artifacts
        },
        "projection_ids": {
            value["metadata"]["context_id"]: value["metadata"]["projection_id"]
            for value in artifacts
        },
        "object_correspondence_count": 2,
        "relationship_correspondence_count": 1,
        "epistemic_sha256": "c" * 64,
        "structural_semantic_sha256": "d" * 64,
    }


class TestBoundedAdmission(unittest.TestCase):
    def test_valid_family_is_order_independent_and_event_is_minimized(self) -> None:
        forward = admit_bounded_family(family(), validator=passing_validator)
        reverse = admit_bounded_family(
            list(reversed(family())), validator=passing_validator
        )
        self.assertEqual(forward.summary, reverse.summary)
        self.assertEqual("passed", forward.summary["status"])
        self.assertEqual(0, forward.summary["provider_operation_count"])
        rendered_event = json.dumps(forward.event, sort_keys=True)
        self.assertNotIn("opaque-dog-id", rendered_event)
        self.assertNotIn("must-not-enter-event", rendered_event)
        self.assertNotIn("birth", rendered_event.lower())
        self.assertNotIn("path", rendered_event.lower())

    def test_exact_input_is_machine_classified_as_mixed(self) -> None:
        values = family()
        values[0]["source_graph_ref"] = {"graph_type": "exact"}
        with self.assertRaises(BoundedAdmissionError) as raised:
            admit_bounded_family(values, validator=passing_validator)
        self.assertEqual("mixed", raised.exception.status)
        self.assertEqual("mixed_exact_bounded_input", raised.exception.code)

    def test_exact_loader_rejects_bounded_family(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = {}
            names = ("direct_to_dog", "general", "handler", "hybrid")
            for name, artifact in zip(names, family()):
                path = root / f"{name}.json"
                path.write_text(json.dumps(artifact), encoding="utf-8")
                paths[name] = path
            with self.assertRaisesRegex(ValueError, "separate bounded-Natal pipeline"):
                load_and_validate_contexts("dog", paths)

    def test_contract_profile_context_runtime_and_capability_mismatches_fail(self) -> None:
        mutations = {
            "bounded_output_contract": ("metadata", "output_contract", "wrong"),
            "bounded_contract_version": ("metadata", "contract_version", "9.0.0"),
            "bounded_engine_version": ("metadata", "engine_version", "0.12.0"),
            "bounded_profile": ("metadata", "profile_version", "9.0.0"),
            "bounded_context_version": ("metadata", "context_version", "9.0.0"),
            "bounded_runtime_version": (
                "metadata",
                "runtime_identity",
                {"distribution": {"name": "semantic-projection-core", "version": "0.12.0"}, "route": "bounded_natal_projection", "output_contract": "projected_bounded_semantic_graph.v1"},
            ),
            "bounded_capabilities": (
                "source_capabilities",
                "supports_exact_longitudes",
                True,
            ),
        }
        for code, mutation in mutations.items():
            with self.subTest(code=code):
                values = family()
                if len(mutation) == 3 and isinstance(values[0].get(mutation[0]), dict):
                    values[0][mutation[0]][mutation[1]] = mutation[2]
                else:
                    raise AssertionError(mutation)
                with self.assertRaises(BoundedAdmissionError) as raised:
                    admit_bounded_family(values, validator=passing_validator)
                self.assertEqual(code, raised.exception.code)

    def test_missing_context_and_anti_precision_limitations_fail(self) -> None:
        with self.assertRaises(BoundedAdmissionError) as raised:
            admit_bounded_family(family()[:-1], validator=passing_validator)
        self.assertEqual("bounded_context_count", raised.exception.code)

        values = family()
        values[0]["limitations"].remove("no_exact_longitudes_or_orbs")
        with self.assertRaises(BoundedAdmissionError) as raised:
            admit_bounded_family(values, validator=passing_validator)
        self.assertEqual("bounded_limitations", raised.exception.code)

    def test_parallel_validator_failure_is_machine_classified(self) -> None:
        def reject(_artifacts):
            raise ValueError("epistemic material differs")

        with self.assertRaises(BoundedAdmissionError) as raised:
            admit_bounded_family(family(), validator=reject)
        self.assertEqual("spc_validation_failed", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
