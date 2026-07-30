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

from build_projected_semantic_basis import (  # noqa: E402
    CONTEXT_FILTER_GROUPS,
    build_candidates,
    compile_packet,
    copy_static_assets,
    discover_subject_packages,
    load_and_validate_contexts,
    optimize,
    qa_report,
)
from merge_projected_term_registries import merge  # noqa: E402
from lint_astrowoof_editorial import lint_deck  # noqa: E402
from validate_astrowoof_editorial import main as validate_editorial  # noqa: E402


EXAMPLES = ROOT / "examples"


def minimal_graph(subject: str, context: str, term_description: str = "same") -> dict:
    context_ids = {
        "general": "woofmapped.doghouse.general.v0",
        "direct_to_dog": "woofmapped.dog_direct.v1",
        "handler": "woofmapped.handler_guidance.v1",
        "hybrid": "woofmapped.hybrid_horoscope.v1",
    }
    return {
        "source_graph_ref": {
            "graph_type": "canonical_astrology_graph",
            "graph_version": "1.3.0",
            "source_graph_hash": f"hash-{subject}",
        },
        "source_identity": {
            "source_chart_id": f"natal:{subject}",
            "source_chart_ids": [f"natal:{subject}"],
            "sensor_instance_id": f"natal:{subject}",
        },
        "target_ontology": "woofmapped_astrology.v0",
        "metadata": {"context_id": context_ids[context]},
        "objects": [],
        "relationships": [],
        "projected_term_registry": {
            "registry_id": "woofmapped_astrology.projected_terms",
            "registry_version": "0.1.0",
            "target_ontology": "woofmapped_astrology.v0",
            "materialization": "used_terms_subset",
            "terms": {"shared": {"description": term_description}},
        },
    }


def write_subject(directory: Path, subject: str) -> None:
    suffixes = {
        "general": "general",
        "direct_to_dog": "d2d",
        "handler": "handler",
        "hybrid": "hybrid",
    }
    for context, suffix in suffixes.items():
        path = directory / f"natal.{subject}.woof.{suffix}.json"
        path.write_text(
            json.dumps(minimal_graph(subject, context), indent=2),
            encoding="utf-8",
        )


def complete_packet(packet: dict) -> dict:
    def fill(value):
        if isinstance(value, dict):
            return {key: fill(item) for key, item in value.items()}
        if isinstance(value, list):
            return [fill(item) for item in value]
        if value == "__LLM_FILL__":
            return "Completed editorial text"
        return value

    edited = fill(deepcopy(packet))
    edited["generator"]["editorial_status"] = "llm_completed"
    edited["statistics"]["editorial_placeholders"] = 0
    aspect_index = 0
    synthesis_index = 0
    for claim in edited["cards"]:
        claim["context_filter_groups"] = {
            "high_level": ["Personality"],
            "detail_level": ["Core Personality"],
        }
        claim["dos"] = ["Do one", "Do two"]
        claim["donts"] = ["Avoid one", "Avoid two"]
        if "theme_group" in claim:
            if claim["claim_type"] == "synthesized_theme":
                claim["theme_group"] = (
                    f"Synthesis Chapter {(synthesis_index % 4) + 1}"
                )
                synthesis_index += 1
            else:
                claim["theme_group"] = (
                    f"Aspect Chapter {(aspect_index % 4) + 1}"
                )
                aspect_index += 1
    for summary in edited["summary"].values():
        summary["dos"] = ["Do one", "Do two"]
        summary["donts"] = ["Avoid one", "Avoid two"]
    return edited


def run_editorial_validator(
    baseline: dict,
    edited: dict,
    *extra_args: str,
) -> dict:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        baseline_path = root / "baseline.json"
        edited_path = root / "edited.json"
        baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
        edited_path.write_text(json.dumps(edited), encoding="utf-8")
        with patch.object(
            sys,
            "argv",
            [
                "validate_astrowoof_editorial.py",
                str(baseline_path),
                str(edited_path),
                *extra_args,
            ],
        ), redirect_stdout(StringIO()) as output:
            try:
                validate_editorial()
            except SystemExit:
                pass
        return json.loads(output.getvalue())


class TestBrePacket(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packages = discover_subject_packages(EXAMPLES, "bre")
        cls.contexts, cls.registry, cls.input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )
        cls.candidates, cls.analysis = build_candidates(cls.contexts)
        cls.selected, cls.rejected, cls.audit = optimize(cls.candidates)
        cls.packet = compile_packet(
            "bre",
            cls.contexts,
            cls.selected,
            cls.rejected,
            cls.analysis,
            cls.registry,
            cls.input_audit,
        )
        cls.qa = qa_report(
            cls.candidates, cls.selected, cls.rejected, cls.packet
        )

    def test_packet_passes_extractor_qa(self) -> None:
        self.assertEqual("pass", self.qa["status"], self.qa["errors"])
        self.assertEqual(50, len(self.packet["cards"]))

    def test_big_three_categories(self) -> None:
        by_object = {
            candidate.provenance.get("canonical_object_name"): self.packet["cards"][index]
            for index, candidate in enumerate(self.selected)
        }
        self.assertEqual(["big3_core_traits"], by_object["Sun"]["categories"])
        self.assertEqual(["big3_core_traits"], by_object["Moon"]["categories"])
        self.assertEqual(
            ["angles", "big3_core_traits"], by_object["ASC"]["categories"]
        )
        self.assertEqual(
            [
                "angles",
                "core_traits",
                "development",
                "synthesized_patterns",
                "system_interactions",
                "big3_core_traits",
            ],
            self.packet["categories"],
        )

    def test_card_humor_is_hoisted(self) -> None:
        for claim in self.packet["cards"]:
            editorial = claim["card"]
            for field in [
                "funny_dog_quotes",
                "imperative_dog_quotes",
                "applicable_canine_jokes",
            ]:
                self.assertIn(field, editorial)
            for density in ["no_astro", "light_astro", "full_astro"]:
                self.assertEqual({"headline", "body"}, set(editorial[density]))

    def test_theme_group_only_on_aspects_and_syntheses(self) -> None:
        for candidate, claim in zip(self.selected, self.packet["cards"]):
            expected = (
                candidate.candidate_type == "projected_relationship"
                or candidate.claim_type == "synthesized_theme"
            )
            self.assertEqual(expected, "theme_group" in claim)

    def test_context_and_summary_scaffolding(self) -> None:
        self.assertEqual(CONTEXT_FILTER_GROUPS, self.packet["context_filter_groups"])
        self.assertEqual(
            ["card1", "card2", "card3", "card4"], list(self.packet["summary"])
        )
        for claim in self.packet["cards"]:
            self.assertEqual(
                {"high_level": [], "detail_level": []},
                claim["context_filter_groups"],
            )

    def test_every_rejected_candidate_is_preserved(self) -> None:
        expected = {candidate.candidate_id for candidate in self.rejected}
        actual = {
            candidate["claim_id"]
            for candidate in self.packet["unselected_claims"]
        }
        self.assertEqual(expected, actual)
        self.assertFalse(
            actual & {claim["claim_id"] for claim in self.packet["cards"]}
        )

    def test_maximal_synthesis_variants_are_separate(self) -> None:
        variants = [
            claim
            for claim in self.packet["unselected_claims"]
            if claim.get("variant_kind") == "maximal_support"
        ]
        self.assertTrue(variants)
        all_ids = {
            claim["claim_id"] for claim in self.packet["cards"]
        } | {
            claim["claim_id"] for claim in self.packet["unselected_claims"]
        }
        for variant in variants:
            self.assertIn(variant["variant_of"], all_ids)
            self.assertTrue(variant["additional_supporting_claim_ids"])

    def test_registry_is_merged_and_preserved(self) -> None:
        self.assertEqual(self.registry, self.packet["projected_term_registry"])
        self.assertEqual(50, len(self.packet["projected_term_registry"]["terms"]))

    def test_generation_is_deterministic(self) -> None:
        candidates, analysis = build_candidates(self.contexts)
        selected, rejected, _ = optimize(candidates)
        packet = compile_packet(
            "bre",
            self.contexts,
            selected,
            rejected,
            analysis,
            self.registry,
            self.input_audit,
        )
        self.assertEqual(
            json.dumps(self.packet, sort_keys=True),
            json.dumps(packet, sort_keys=True),
        )

    def test_schema_migration_does_not_change_selected_portfolio(self) -> None:
        previous = json.loads(
            (
                ROOT
                / "docs"
                / "post_extraction_authoring"
                / "orig"
                / "semantic-basis-output"
                / "bre"
                / "bre.selected-authoring-packet.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            [claim["claim_id"] for claim in previous["cards"]],
            [claim["claim_id"] for claim in self.packet["cards"]],
        )

    def test_completed_packet_passes_editorial_validator(self) -> None:
        edited = complete_packet(self.packet)
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_authoring_allows_empty_context_filters(self) -> None:
        edited = complete_packet(self.packet)
        edited["cards"][0]["context_filter_groups"] = {
            "high_level": [],
            "detail_level": [],
        }
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_editorial_linter_detects_claim_type_templates(self) -> None:
        edited = complete_packet(self.packet)
        placement_cards = [
            card for card in edited["cards"]
            if card["claim_type"] == "placement"
        ]
        for card in placement_cards:
            card["card"]["no_astro"]["body"]["handler"] = (
                "This repeated placement template introduces the same prose "
                "for every placement card despite different evidence."
            )
        report = lint_deck(Path("templated.json"), edited)
        codes = {item["code"] for item in report["warnings"]}
        self.assertIn("duplicate_body", codes)
        self.assertIn("claim_type_template", codes)

    def test_polish_phase_locks_organizational_fields(self) -> None:
        baseline = complete_packet(self.packet)
        polished = deepcopy(baseline)
        polished["cards"][0]["card"]["no_astro"]["body"]["handler"] = (
            "A polished prose revision."
        )
        passing = run_editorial_validator(
            baseline, polished, "--phase", "polish"
        )
        self.assertEqual("pass", passing["status"], passing["errors"])

        polished["cards"][0]["context_filter_groups"]["high_level"] = ["Play"]
        polished["summary"]["card1"]["no_astro"]["body"]["handler"] = (
            "Changed summary."
        )
        failing = run_editorial_validator(
            baseline, polished, "--phase", "polish"
        )
        self.assertEqual("fail", failing["status"])
        self.assertTrue(
            any("context filters" in error for error in failing["errors"])
        )
        self.assertIn(
            "Polish phase changed locked summary content.",
            failing["errors"],
        )

    def test_polish_phase_allows_explicit_scoped_overrides(self) -> None:
        baseline = complete_packet(self.packet)
        polished = deepcopy(baseline)
        polished["cards"][0]["context_filter_groups"]["high_level"] = ["Play"]
        polished["summary"]["card1"]["no_astro"]["body"]["handler"] = (
            "Changed summary."
        )
        report = run_editorial_validator(
            baseline,
            polished,
            "--phase",
            "polish",
            "--allow-context-filter-edits",
            "--allow-summary-edits",
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_card_shapes_match_current_astrowoof_example(self) -> None:
        reference = json.loads(
            (
                EXAMPLES
                / "natal.bre.cards - almost golden need final manual edits.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(reference["cards"][0]["card"]),
            set(self.packet["cards"][0]["card"]),
        )
        self.assertEqual(
            set(reference["summary"]["card1"]),
            set(self.packet["summary"]["card1"]),
        )


class TestPackageDiscoveryAndRegistry(unittest.TestCase):
    def test_handoff_static_assets_include_execution_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "subject"
            copy_static_assets(bundle, ROOT, None)
            expected = {
                "AstroWoof Projected Natal Card Authoring Manual.md",
                "LLM Card-by-Card Authoring Execution Protocol.md",
                "LLM Editing Permissions and QA Checklist.md",
                "Proposed LLM Handoff Prompt.md",
            }
            self.assertTrue(
                expected.issubset(
                    {path.name for path in (bundle / "static").iterdir()}
                )
            )

    def test_discovers_multiple_subject_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for subject in ["bre", "luna"]:
                directory = root / subject
                directory.mkdir()
                write_subject(directory, subject)
            packages = discover_subject_packages(root)
            self.assertEqual(["bre", "luna"], list(packages))
            for subject, paths in packages.items():
                contexts, registry, audit = load_and_validate_contexts(subject, paths)
                self.assertEqual(4, len(contexts))
                self.assertEqual("pass", audit["status"])
                self.assertIn("shared", registry["terms"])

    def test_discovers_single_subject_direct_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "bre")
            packages = discover_subject_packages(root)
            self.assertEqual(["bre"], list(packages))

    def test_missing_context_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "bre")
            (root / "natal.bre.woof.hybrid.json").unlink()
            packages = discover_subject_packages(root)
            with self.assertRaisesRegex(ValueError, "four contexts"):
                load_and_validate_contexts("bre", packages["bre"])

    def test_registry_conflict_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            one = root / "one.json"
            two = root / "two.json"
            one.write_text(
                json.dumps(minimal_graph("bre", "general", "one")),
                encoding="utf-8",
            )
            two.write_text(
                json.dumps(minimal_graph("bre", "handler", "two")),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Conflicting definitions"):
                merge([one, two])


if __name__ == "__main__":
    unittest.main()
