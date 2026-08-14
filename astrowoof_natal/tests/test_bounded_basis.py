from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.bounded_admission import (  # noqa: E402
    BoundedAdmission,
    REQUIRED_CONTEXTS,
)
from astrowoof_natal_authoring.bounded_basis import (  # noqa: E402
    BoundedCandidateError,
    build_bounded_basis,
)


def _basis(classification: str, evidence_ref: str, family: str) -> dict:
    return {
        "classification": classification,
        "evidence_refs": [evidence_ref],
        "evidence_family_groups": [family],
        "proof_scope": "complete_normalized_birth_interval",
    }


def _object(
    context: str,
    number: int,
    correspondence: str,
    source_type: str,
    source_name: str,
    family: str,
    evidence_ref: str,
    *,
    transform: str | None = None,
) -> dict:
    return {
        "id": f"object:{context}:{number}",
        "correspondence_id": correspondence,
        "object_type": (
            "woofmapped_operator"
            if source_type == "bounded_natal_body"
            else "woofmapped_derived_operator"
        ),
        "name": f"operator_{number}",
        "attributes": {
            "source_object_type": source_type,
            "canonical_object_name": source_name,
            "source_owner_object_ref": (
                None if source_type == "bounded_natal_body" else f"owner:{source_name}"
            ),
            "coordinate_transform": transform,
            "term_ref": f"terms:operator_{number}",
            "mode_ref": f"terms:mode_{number}",
        },
        "source_refs": [f"canonical:object:{source_name}:{transform or 'natal'}"],
        "mapping_rule_refs": ["not:a:projected:term"],
        "epistemic_basis": _basis("invariant", evidence_ref, family),
        "projection_relevance_score": None,
    }


def _relationship(
    context: str,
    number: int,
    correspondence: str,
    source_type: str,
    source_number: int,
    target_number: int,
    family: str,
    evidence_ref: str,
    *,
    topology_only: bool = False,
) -> dict:
    return {
        "id": f"relationship:{context}:{number}",
        "correspondence_id": correspondence,
        "relationship_type": "coordinate_transform_of" if topology_only else "channel",
        "source_id": f"object:{context}:{source_number}",
        "target_id": f"object:{context}:{target_number}",
        "attributes": {
            "source_relationship_type": source_type,
            "source_evidence_family_group": family,
            "topology_only": topology_only,
            "relation_ref": "terms:channel",
            "interaction_mode_ref": "terms:interaction",
            "relevance_accounting": {
                "policy": "evidence_family_equal_allocation",
                "raw_record_count_is_weight": False,
            },
        },
        "source_relationship_refs": [f"canonical:relationship:{number}"],
        "epistemic_basis": _basis("invariant", evidence_ref, family),
        "projection_relevance_score": None if topology_only else 0.2,
    }


def admitted_family() -> BoundedAdmission:
    artifacts = {}
    for context in sorted(REQUIRED_CONTEXTS):
        objects = [
            _object(context, 1, "object:sun", "bounded_natal_body", "Sun", "family:sun", "ev:sun"),
            _object(context, 2, "object:mars", "bounded_natal_body", "Mars", "family:mars", "ev:mars"),
            _object(context, 3, "object:sun:h3", "bounded_harmonic_point", "Sun", "family:derived:sun", "ev:sun:h3", transform="harmonic:3"),
            _object(context, 4, "object:sun:h5", "bounded_harmonic_point", "Sun", "family:derived:sun", "ev:sun:h5", transform="harmonic:5"),
        ]
        relationships = [
            _relationship(context, 1, "relationship:direct", "BOUNDED_INVARIANT_ASPECT", 1, 2, "family:direct", "ev:direct"),
            _relationship(context, 2, "relationship:derived:a", "BOUNDED_INVARIANT_DERIVED_ASPECT", 3, 2, "family:derived:a", "ev:derived:a"),
            _relationship(context, 3, "relationship:derived:b", "BOUNDED_INVARIANT_DERIVED_ASPECT", 4, 2, "family:derived:b", "ev:derived:b"),
            _relationship(context, 4, "relationship:topology", "BOUNDED_HAS_HARMONIC_POINT", 1, 3, "family:topology:sun", "ev:sun:h3", topology_only=True),
        ]
        records = {
            "ev:sun": {
                "classification": "invariant",
                "proof_scope": "complete_normalized_birth_interval",
                "prerequisite_refs": ["provider:ephemeris"],
            },
            "ev:mars": {
                "classification": "invariant",
                "proof_scope": "complete_normalized_birth_interval",
                "prerequisite_refs": [],
            },
            "ev:sun:h3": {
                "classification": "invariant",
                "proof_scope": "complete_normalized_birth_interval",
                "prerequisite_refs": ["ev:sun"],
                "evidence_metadata": {
                    "evidence_family_group": "family:derived:sun",
                    "independence_group": "family:derived:sun",
                    "record_independence_group": "record:sun:h3",
                    "source_owner_object_ref": "owner:Sun",
                },
            },
            "ev:sun:h5": {
                "classification": "invariant",
                "proof_scope": "complete_normalized_birth_interval",
                "prerequisite_refs": ["ev:sun"],
                "evidence_metadata": {
                    "evidence_family_group": "family:derived:sun",
                    "independence_group": "family:derived:sun",
                    "record_independence_group": "record:sun:h5",
                    "source_owner_object_ref": "owner:Sun",
                },
            },
            "ev:direct": {"classification": "invariant", "prerequisite_refs": ["ev:sun", "ev:mars"], "proof_scope": "complete_normalized_birth_interval"},
            "ev:derived:a": {"classification": "invariant", "prerequisite_refs": ["ev:sun:h3", "ev:mars"], "proof_scope": "complete_normalized_birth_interval"},
            "ev:derived:b": {"classification": "invariant", "prerequisite_refs": ["ev:sun:h5", "ev:mars"], "proof_scope": "complete_normalized_birth_interval"},
            "ev:variable": {"classification": "variable", "range_evidence": {"minimum": 1.0, "maximum": 2.0}},
        }
        artifacts[context] = {
            "metadata": {"context_id": context},
            "objects": objects,
            "relationships": relationships,
            "source_evidence": {"records": records},
            "source_feature_dispositions": {"aspect_patterns": "unavailable"},
            "audit": {
                "coverage": {
                    "outside_declared_scope_ids": ["source:Spirit"],
                    "outside_declared_scope_relationship_ids": [],
                }
            },
        }
    return BoundedAdmission(artifacts, {"admission_id": "bounded:test"}, {})


class TestBoundedBasis(unittest.TestCase):
    def test_candidate_kinds_preserve_contexts_and_family_units(self) -> None:
        result = build_bounded_basis(admitted_family())
        self.assertEqual(
            len(result.candidates),
            len({candidate["candidate_id"] for candidate in result.candidates}),
        )
        self.assertEqual(
            {
                "derived_family": 3,
                "foundational_object": 2,
                "individualized_relationship": 1,
                "invariant_configuration": 1,
                "topology_dependency": 1,
            },
            result.summary["candidate_kind_counts"],
        )
        for candidate in result.candidates:
            self.assertEqual("invariant", candidate["epistemic_classification"])
            if candidate["candidate_kind"] != "invariant_configuration":
                self.assertEqual(set(REQUIRED_CONTEXTS), set(candidate["context_records"]))
            self.assertFalse(candidate["family_accounting"]["raw_record_count_is_weight"])
        topology = next(c for c in result.candidates if c["candidate_kind"] == "topology_dependency")
        self.assertEqual("dependency_only", topology["candidate_role"])

    def test_evidence_closure_is_opaque_and_excludes_precision_fields(self) -> None:
        result = build_bounded_basis(admitted_family())
        derived = next(
            c
            for c in result.candidates
            if c["candidate_kind"] == "derived_family"
            and "object:sun:h3" in c["correspondence_ids"]
        )
        self.assertIn("ev:sun", derived["evidence_lineage"]["resolved_evidence_refs"])
        self.assertIn("provider:ephemeris", derived["evidence_lineage"]["unresolved_prerequisite_refs"])
        self.assertEqual(1, derived["family_accounting"]["independent_support_unit_count"])
        rendered = json.dumps(result.candidates, sort_keys=True)
        for prohibited in ("range_evidence", "structural_strength", "confidence", "representative_state"):
            self.assertNotIn(prohibited, rendered)
        self.assertTrue(
            all(
                "not:a:projected:term" not in candidate["projected_term_refs"]
                for candidate in result.candidates
            )
        )

    def test_foundational_modes_are_explicit_and_unknown_mode_fails(self) -> None:
        expected = {
            "strong_preference": "preferred",
            "mandatory_when_available": "mandatory",
            "portfolio_neutral": "eligible",
        }
        for policy, status in expected.items():
            result = build_bounded_basis(admitted_family(), foundational_policy=policy)
            foundations = [c for c in result.candidates if c["candidate_kind"] == "foundational_object"]
            self.assertTrue(all(c["foundational_status"] == status for c in foundations))
        with self.assertRaises(BoundedCandidateError) as raised:
            build_bounded_basis(admitted_family(), foundational_policy="guess")
        self.assertEqual("bounded_foundational_policy_unknown", raised.exception.code)

    def test_reorder_is_deterministic_and_non_invariant_rows_fail_closed(self) -> None:
        original = admitted_family()
        copied = deepcopy(original)
        reordered = BoundedAdmission(
            dict(reversed(list(copied.artifacts_by_context.items()))),
            copied.summary,
            copied.event,
        )
        for artifact in reordered.artifacts_by_context.values():
            artifact["objects"].reverse()
            artifact["relationships"].reverse()
        self.assertEqual(
            build_bounded_basis(original).summary,
            build_bounded_basis(reordered).summary,
        )
        for classification in ("conditional", "variable", "unavailable", "inconclusive"):
            with self.subTest(classification=classification):
                invalid = admitted_family()
                first = next(iter(invalid.artifacts_by_context.values()))
                first["objects"][0]["epistemic_basis"]["classification"] = classification
                with self.assertRaises(BoundedCandidateError) as raised:
                    build_bounded_basis(invalid)
                self.assertEqual("bounded_non_invariant_projected_row", raised.exception.code)

    def test_raw_family_multiplicity_does_not_create_support_or_candidate(self) -> None:
        baseline = build_bounded_basis(admitted_family())
        expanded = admitted_family()
        for context, artifact in expanded.artifacts_by_context.items():
            duplicate = deepcopy(artifact["relationships"][1])
            duplicate["id"] = f"relationship:{context}:99"
            duplicate["correspondence_id"] = "relationship:derived:a:duplicate"
            duplicate["source_relationship_refs"] = ["canonical:relationship:99"]
            artifact["relationships"].append(duplicate)
        result = build_bounded_basis(expanded)
        self.assertEqual(len(baseline.candidates), len(result.candidates))
        family = next(
            c
            for c in result.candidates
            if c["candidate_kind"] == "derived_family"
            and "relationship:derived:a" in c["correspondence_ids"]
        )
        self.assertEqual(2, family["family_accounting"]["raw_correspondence_count"])
        self.assertEqual(1, family["family_accounting"]["independent_support_unit_count"])

    def test_disposition_is_complete_for_rows_evidence_and_outside_scope(self) -> None:
        result = build_bounded_basis(admitted_family())
        report = result.disposition_report
        self.assertEqual(8, report["counts"]["projected_row_count"])
        self.assertEqual(8, report["counts"]["evidence_record_count"])
        self.assertEqual(1, report["counts"]["outside_scope_count"])
        variable = next(row for row in report["source_evidence"] if row["evidence_ref"] == "ev:variable")
        self.assertEqual("non_admitted_variable", variable["disposition"])
        self.assertEqual("outside_declared_scope", report["outside_scope"][0]["disposition"])


if __name__ == "__main__":
    unittest.main()
