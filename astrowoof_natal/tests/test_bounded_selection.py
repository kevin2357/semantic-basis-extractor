from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.bounded_basis import BoundedBasis  # noqa: E402
from astrowoof_natal_authoring.bounded_selection import (  # noqa: E402
    BoundedSelectionError,
    EDITORIAL_UTILITY_CONTRACT,
    EDITORIAL_TIERS,
    UTILITY_WEIGHTS,
    select_bounded_portfolio,
)


CONTEXTS = (
    "woofmapped.dog_direct.v1",
    "woofmapped.doghouse.general.v0",
    "woofmapped.handler_guidance.v1",
    "woofmapped.hybrid_horoscope.v1",
)


def _candidate(
    number: int,
    kind: str,
    policy: str,
    *,
    dependencies: tuple[str, ...] = (),
    roots: tuple[str, ...] = (),
    family: str | None = None,
    relevance_members: int = 1,
) -> dict:
    candidate_id = f"candidate:{number:03d}"
    family = family or f"family:{number:03d}"
    relationship = kind in {"individualized_relationship", "derived_family"} and number >= 12
    records = {}
    for context in CONTEXTS:
        rows = []
        for member in range(relevance_members):
            row = {
                "correspondence_id": f"correspondence:{number:03d}:{member}",
                "epistemic_basis": {
                    "classification": "invariant",
                    "evidence_family_groups": [family],
                    "proof_scope": "complete_normalized_birth_interval",
                },
            }
            if relationship:
                row.update(
                    {
                        "relationship_type": "channel",
                        "projection_relevance_score": 1.0 / relevance_members,
                        "attributes": {
                            "relevance_accounting": {
                                "policy": "evidence_family_equal_allocation",
                                "raw_record_count_is_weight": False,
                            }
                        },
                    }
                )
            else:
                row["object_type"] = "operator"
            rows.append(row)
        records[context] = rows
    foundational = kind == "foundational_object"
    return {
        "schema_version": "astrowoof.bounded_natal.candidate_policy.v1",
        "candidate_id": candidate_id,
        "candidate_kind": kind,
        "candidate_role": "authored",
        "epistemic_classification": "invariant",
        "correspondence_ids": [f"correspondence:{number:03d}:{member}" for member in range(relevance_members)],
        "context_records": records,
        "source_refs": [f"source:{number:03d}"],
        "root_owner_refs": list(roots or (f"root:{number % 12:02d}",)),
        "proof_scopes": ["complete_normalized_birth_interval"],
        "evidence_lineage": {
            "evidence_family_groups": [family],
            "resolved_evidence_refs": [f"evidence:{number:03d}"],
        },
        "projected_term_refs": [f"term:{number % 20:02d}", f"kind:{kind}"],
        "member_candidate_ids": list(dependencies),
        "foundational_policy": policy,
        "foundational_status": (
            {"strong_preference": "preferred", "mandatory_when_available": "mandatory", "portfolio_neutral": "eligible"}[policy]
            if foundational
            else "not_applicable"
        ),
        "family_accounting": {
            "raw_correspondence_count": relevance_members,
            "independent_support_unit_count": 1,
            "raw_record_count_is_weight": False,
        },
    }


def portfolio_basis(policy: str = "strong_preference") -> BoundedBasis:
    candidates = [
        _candidate(index, "foundational_object", policy, roots=(f"root:{index:02d}",))
        for index in range(12)
    ]
    for index in range(12, 60):
        left = index % 12
        right = (index + 5) % 12
        candidates.append(
            _candidate(
                index,
                "individualized_relationship",
                policy,
                dependencies=(f"candidate:{left:03d}", f"candidate:{right:03d}"),
                roots=(f"root:{left:02d}", f"root:{right:02d}"),
            )
        )
    candidates.append(
        {
            **_candidate(
                60,
                "invariant_configuration",
                policy,
                dependencies=("candidate:012", "candidate:013"),
                roots=("root:00", "root:05"),
            ),
            "context_records": {},
            "correspondence_ids": ["correspondence:012:0", "correspondence:013:0"],
            "evidence_lineage": {
                "evidence_family_groups": ["family:012", "family:013"]
            },
        }
    )
    projected_rows = [
        {
            "row_kind": "object" if index < 12 else "relationship",
            "correspondence_id": f"correspondence:{index:03d}:0",
            "disposition": "admitted",
        }
        for index in range(60)
    ]
    evidence = [
        {
            "evidence_ref": f"evidence:{index:03d}",
            "classification": "invariant",
            "disposition": "admitted_evidence_lineage",
        }
        for index in range(60)
    ]
    disposition = {
        "schema_version": "astrowoof.bounded_natal.disposition_report.v1",
        "projected_rows": projected_rows,
        "source_evidence": evidence,
        "outside_scope": [],
        "source_feature_dispositions": {},
        "counts": {},
    }
    return BoundedBasis(
        tuple(candidates),
        disposition,
        {
            "schema_version": "astrowoof.bounded_natal.candidate_policy.v1",
            "foundational_policy": policy,
        },
    )


class TestBoundedSelection(unittest.TestCase):
    def test_exactly_fifty_invariant_dependency_closed_and_audited(self) -> None:
        basis = portfolio_basis()
        result = select_bounded_portfolio(basis)
        self.assertEqual(50, len(result.selected))
        self.assertEqual(50, len({row["candidate_id"] for row in result.selected}))
        selected_ids = {row["candidate_id"] for row in result.selected}
        for row in result.selected:
            self.assertEqual("invariant", row["epistemic_classification"])
            self.assertTrue(set(row["member_candidate_ids"]) <= selected_ids)
            self.assertIn(row["editorial_tier"], EDITORIAL_TIERS)
            self.assertGreaterEqual(row["bounded_editorial_utility"], 0.0)
            self.assertLessEqual(row["bounded_editorial_utility"], 1.0)
        self.assertEqual(EDITORIAL_UTILITY_CONTRACT, result.audit["utility_profile"])
        self.assertAlmostEqual(1.0, sum(UTILITY_WEIGHTS.values()))
        self.assertEqual(0, result.audit["provider_operation_count"])
        self.assertEqual(50, result.disposition_report["selection"]["selected_count"])

    def test_deterministic_reorder_and_closed_rejection_vocabularies(self) -> None:
        basis = portfolio_basis()
        reversed_basis = BoundedBasis(
            tuple(reversed(basis.candidates)),
            deepcopy(basis.disposition_report),
            deepcopy(basis.summary),
        )
        forward = select_bounded_portfolio(basis)
        reverse = select_bounded_portfolio(reversed_basis)
        self.assertEqual(forward.audit["selected_sha256"], reverse.audit["selected_sha256"])
        self.assertEqual(
            forward.audit["selected_candidate_ids"], reverse.audit["selected_candidate_ids"]
        )
        self.assertTrue(
            {row["rejection_reason"] for row in forward.rejected}
            <= {"redundant_covered_territory", "derived_family_saturation", "capacity_displaced"}
        )

    def test_foundational_policy_modes(self) -> None:
        mandatory = select_bounded_portfolio(portfolio_basis("mandatory_when_available"))
        selected = {row["candidate_id"] for row in mandatory.selected}
        self.assertTrue({f"candidate:{index:03d}" for index in range(12)} <= selected)
        strong = select_bounded_portfolio(portfolio_basis("strong_preference"))
        neutral = select_bounded_portfolio(portfolio_basis("portfolio_neutral"))
        self.assertNotEqual(strong.audit["selected_sha256"], neutral.audit["selected_sha256"])

    def test_relevance_is_conserved_across_raw_family_members(self) -> None:
        basis = portfolio_basis()
        candidates = list(basis.candidates)
        candidates[20] = _candidate(
            20,
            "derived_family",
            "strong_preference",
            dependencies=("candidate:000", "candidate:001"),
            roots=("root:00", "root:01"),
            family="family:conserved",
            relevance_members=10,
        )
        candidates[21] = _candidate(
            21,
            "derived_family",
            "strong_preference",
            dependencies=("candidate:000", "candidate:001"),
            roots=("root:00", "root:01"),
            family="family:single",
            relevance_members=1,
        )
        result = select_bounded_portfolio(
            BoundedBasis(tuple(candidates), deepcopy(basis.disposition_report), basis.summary)
        )
        decisions = {row["candidate_id"]: row for row in result.audit["decisions"]}
        self.assertEqual(1.0, decisions["candidate:020"]["components"]["target_relevance"])
        self.assertEqual(1.0, decisions["candidate:021"]["components"]["target_relevance"])

    def test_insufficient_non_invariant_and_variable_size_fail_closed(self) -> None:
        basis = portfolio_basis()
        sparse = BoundedBasis(
            tuple(basis.candidates[:49]),
            deepcopy(basis.disposition_report),
            basis.summary,
        )
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(sparse)
        self.assertEqual("insufficient_invariant_basis", raised.exception.code)
        self.assertEqual("failed", raised.exception.as_dict()["status"])

        invalid_candidates = list(basis.candidates)
        invalid_candidates[0] = {
            **invalid_candidates[0],
            "epistemic_classification": "variable",
        }
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(
                BoundedBasis(
                    tuple(invalid_candidates), deepcopy(basis.disposition_report), basis.summary
                )
            )
        self.assertEqual("bounded_non_invariant_candidate", raised.exception.code)
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(basis, selection_size=49)
        self.assertEqual("bounded_selection_size_unsupported", raised.exception.code)

    def test_identity_dependency_and_relevance_corruption_fail_closed(self) -> None:
        basis = portfolio_basis()
        duplicate = list(basis.candidates)
        duplicate[1] = {**duplicate[1], "candidate_id": duplicate[0]["candidate_id"]}
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(
                BoundedBasis(tuple(duplicate), deepcopy(basis.disposition_report), basis.summary)
            )
        self.assertEqual("bounded_candidate_identity_duplicate", raised.exception.code)

        missing = list(basis.candidates)
        missing[12] = {**missing[12], "member_candidate_ids": ["candidate:missing"]}
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(
                BoundedBasis(tuple(missing), deepcopy(basis.disposition_report), basis.summary)
            )
        self.assertEqual("bounded_dependency_missing", raised.exception.code)

        cycle = list(basis.candidates)
        cycle[12] = {**cycle[12], "member_candidate_ids": ["candidate:013"]}
        cycle[13] = {**cycle[13], "member_candidate_ids": ["candidate:012"]}
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(
                BoundedBasis(tuple(cycle), deepcopy(basis.disposition_report), basis.summary)
            )
        self.assertEqual("bounded_dependency_cycle", raised.exception.code)

        relevance = deepcopy(list(basis.candidates))
        context = next(iter(relevance[12]["context_records"]))
        relevance[12]["context_records"][context][0]["attributes"][
            "relevance_accounting"
        ]["raw_record_count_is_weight"] = True
        with self.assertRaises(BoundedSelectionError) as raised:
            select_bounded_portfolio(
                BoundedBasis(
                    tuple(relevance), deepcopy(basis.disposition_report), basis.summary
                )
            )
        self.assertEqual("bounded_relevance_policy_unsupported", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
