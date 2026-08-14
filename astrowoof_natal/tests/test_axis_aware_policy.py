from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.basis_policies import (  # noqa: E402
    AXIS_AWARE_POLICY_ID,
    LEGACY_ATOMIC_POLICY_ID,
)
from astrowoof_natal_authoring.extractor import (  # noqa: E402
    build_candidates,
    compare_exact_policy_portfolios,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    main as extract_main,
    object_name,
    optimize,
    qa_report,
)


CLOSED_REASONS = {
    "structurally_inevitable",
    "represented_by_axis_configuration",
}


class TestAxisAwarePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packages = discover_subject_packages(ROOT / "examples", "bre")
        cls.contexts, cls.registry, cls.input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )

    def replay(self, contexts=None):
        contexts = self.contexts if contexts is None else contexts
        candidates, analysis = build_candidates(contexts, AXIS_AWARE_POLICY_ID)
        selected, rejected, audit = optimize(
            candidates, policy=AXIS_AWARE_POLICY_ID
        )
        packet = compile_packet(
            "bre",
            contexts,
            selected,
            rejected,
            analysis,
            self.registry,
            self.input_audit,
            policy=AXIS_AWARE_POLICY_ID,
        )
        qa = qa_report(
            candidates, selected, rejected, packet, AXIS_AWARE_POLICY_ID
        )
        return candidates, selected, rejected, audit, packet, qa

    def test_bre_axis_inventory_is_deterministic_and_closed(self) -> None:
        first = self.replay()
        second = self.replay()
        self.assertEqual(
            json.dumps(first, default=lambda value: value.as_dict(), sort_keys=True),
            json.dumps(second, default=lambda value: value.as_dict(), sort_keys=True),
        )
        candidates, selected, rejected, _audit, _packet, qa = first
        axes = [
            candidate
            for candidate in candidates
            if candidate.candidate_type == "axis_configuration"
        ]
        self.assertEqual(6, len(axes))
        self.assertEqual(6, sum(candidate in selected for candidate in axes))
        self.assertEqual("pass", qa["status"], qa["errors"])
        selected_ids = {candidate.candidate_id for candidate in selected}
        self.assertTrue(
            all(set(candidate.dependencies) <= selected_ids for candidate in selected)
        )
        self.assertFalse(
            [candidate for candidate in selected if not candidate.eligible_for_selection]
        )
        dispositions = [
            candidate.rejection_reason
            for candidate in rejected
            if candidate.rejection_reason in CLOSED_REASONS
        ]
        self.assertEqual(6, dispositions.count("structurally_inevitable"))
        self.assertEqual(
            12, dispositions.count("represented_by_axis_configuration")
        )

    def test_axis_candidate_preserves_both_component_edges_as_evidence(self) -> None:
        candidates, selected, _rejected, _audit, _packet, _qa = self.replay()
        moon_axis = next(
            candidate
            for candidate in selected
            if candidate.candidate_type == "axis_configuration"
            and candidate.provenance["external_object"] == "Moon"
        )
        component_ids = moon_axis.provenance["component_candidate_ids"]
        self.assertEqual(2, len(component_ids))
        evidence = moon_axis.evidence[0]
        self.assertEqual("axis_configuration", evidence["kind"])
        self.assertEqual(2, len(evidence["component_relationships"]))
        preserved_refs = {
            source_ref
            for member in evidence["component_relationships"]
            for source_ref in member["source_refs"]
        }
        self.assertEqual(set(moon_axis.source_refs), preserved_refs)
        by_id = {candidate.candidate_id: candidate for candidate in candidates}
        self.assertTrue(
            all(
                by_id[component_id].rejection_reason
                == "represented_by_axis_configuration"
                for component_id in component_ids
            )
        )

    def test_incomplete_axis_does_not_synthesize(self) -> None:
        contexts = deepcopy(self.contexts)
        for graph in contexts.values():
            objects = {record["id"]: record for record in graph["objects"]}
            graph["relationships"] = [
                relationship
                for relationship in graph["relationships"]
                if {
                    object_name(objects[relationship["source_id"]]),
                    object_name(objects[relationship["target_id"]]),
                }
                != {"Moon", "DSC"}
            ]
        candidates, _analysis = build_candidates(contexts, AXIS_AWARE_POLICY_ID)
        self.assertFalse(
            [
                candidate
                for candidate in candidates
                if candidate.candidate_type == "axis_configuration"
                and candidate.provenance["external_object"] == "Moon"
            ]
        )
        moon_asc = next(
            candidate
            for candidate in candidates
            if candidate.candidate_type == "projected_relationship"
            and "Comfort and Regulation" in candidate.canonical_claim
            and "Behavioral Doorway" in candidate.canonical_claim
        )
        self.assertTrue(moon_asc.eligible_for_selection)
        self.assertIsNone(moon_asc.rejection_reason)

    def test_comparison_report_exposes_drift_topology_coverage_and_closure(self) -> None:
        baseline_candidates, _ = build_candidates(self.contexts)
        baseline_selected, _baseline_rejected, _ = optimize(baseline_candidates)
        _candidates, selected, rejected, _audit, _packet, _qa = self.replay()
        report = compare_exact_policy_portfolios(
            baseline_selected,
            selected,
            rejected,
            candidate_policy_id=AXIS_AWARE_POLICY_ID,
        )
        self.assertEqual(LEGACY_ATOMIC_POLICY_ID, report["baseline_policy_id"])
        self.assertEqual(AXIS_AWARE_POLICY_ID, report["candidate_policy_id"])
        self.assertEqual(6, report["topology"]["baseline"]["pure_angle_frame_relationships"])
        self.assertEqual(0, report["topology"]["candidate"]["pure_angle_frame_relationships"])
        self.assertEqual(6, report["topology"]["candidate"]["axis_configurations"])
        self.assertIn("jaccard", report["portfolio"])
        self.assertIn("lost_source_refs", report["coverage"])
        self.assertIn("candidate_axis_component_count", report["closure"])

    def test_cli_emits_axis_comparison_only_when_opted_in(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            with patch.object(
                sys,
                "argv",
                [
                    "extract",
                    "--input-package",
                    str(ROOT / "examples" / "projected_bre_files"),
                    "--output-dir",
                    str(output),
                    "--bundle-dir",
                    str(root / "bundle"),
                    "--exact-natal-policy",
                    AXIS_AWARE_POLICY_ID,
                ],
            ), redirect_stdout(StringIO()):
                extract_main()
            comparison = output / "bre" / "bre.policy-comparison.json"
            self.assertTrue(comparison.is_file())
            report = json.loads(comparison.read_text("utf-8"))
            self.assertEqual(AXIS_AWARE_POLICY_ID, report["candidate_policy_id"])


if __name__ == "__main__":
    unittest.main()
