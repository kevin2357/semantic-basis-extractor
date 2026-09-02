from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.extractor import (  # noqa: E402
    CONTEXT_FILTER_GROUPS,
    archive_story_workspace,
    authoring_projection_payload,
    build_compact_full_chart_basis,
    build_candidates,
    build_split_assignment_plan,
    build_story_workspace,
    compile_packet,
    copy_static_assets,
    discover_subject_packages,
    load_and_validate_contexts,
    load_subject_params,
    optimize,
    qa_report,
    render_full_chart_basis,
    subject_record,
)
from astrowoof_natal_authoring.assembly import assemble  # noqa: E402
from astrowoof_natal_authoring.registries import merge  # noqa: E402
from astrowoof_natal_authoring.editorial_lint import (  # noqa: E402
    authoring_pass_acceptance,
    lint_deck,
    reader_facing_items,
)
from astrowoof_natal_authoring.validation import (  # noqa: E402
    ASTRO_TERMS,
    main as validate_editorial,
)


EXAMPLES = ROOT / "examples"


def minimal_graph(
    subject: str,
    context: str,
    term_description: str = "same",
    source_id: str | None = None,
) -> dict:
    context_ids = {
        "general": "woofmapped.doghouse.general.v0",
        "direct_to_dog": "woofmapped.dog_direct.v1",
        "handler": "woofmapped.handler_guidance.v1",
        "hybrid": "woofmapped.hybrid_horoscope.v1",
    }
    source_id = source_id or f"natal:{subject}"
    return {
        "source_graph_ref": {
            "graph_type": "canonical_astrology_graph",
            "graph_version": "1.3.0",
            "source_graph_hash": f"hash-{subject}",
        },
        "source_identity": {
            "source_chart_id": source_id,
            "source_chart_ids": [source_id],
            "sensor_instance_id": source_id,
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
    registries = {
        "interdogpendence": [
            {"id": "bond_dynamics", "title": "Bond Dynamics", "short_title": "Bonds", "emoji": "🔗", "subtitle": "How trust and closeness shape the relationship.", "order": 1},
            {"id": "shared_rhythms", "title": "Shared Rhythms", "short_title": "Rhythms", "emoji": "🐾", "subtitle": "How dog and handler find a workable pace.", "order": 2},
            {"id": "productive_tensions", "title": "Productive Tensions", "short_title": "Tensions", "emoji": "⚡", "subtitle": "Where friction can become useful information.", "order": 3},
            {"id": "mutual_adjustments", "title": "Mutual Adjustments", "short_title": "Adjustments", "emoji": "🤝", "subtitle": "How both sides adapt while staying connected.", "order": 4},
        ],
        "takeaways": [
            {"id": "essential_character", "title": "Essential Character", "short_title": "Character", "emoji": "✨", "subtitle": "The qualities that make this dog unmistakable.", "order": 1},
            {"id": "daily_wisdom", "title": "Daily Wisdom", "short_title": "Daily Life", "emoji": "🏡", "subtitle": "What everyday life reveals about her style.", "order": 2},
            {"id": "growth_lessons", "title": "Growth Lessons", "short_title": "Growth", "emoji": "🌱", "subtitle": "Where support can help potential unfold.", "order": 3},
            {"id": "lasting_gifts", "title": "Lasting Gifts", "short_title": "Gifts", "emoji": "🎁", "subtitle": "The strengths she brings to her relationships.", "order": 4},
        ],
    }
    edited["theme_group_registry"] = registries
    theme_indexes = {section: 0 for section in registries}
    for claim in edited["cards"]:
        claim["context_filter_groups"] = {
            "high_level": ["Personality"],
            "detail_level": ["Core Personality"],
        }
        claim["dos"] = ["Do one", "Do two", "Do three"]
        claim["donts"] = ["Avoid one", "Avoid two", "Avoid three"]
        if "theme_group_id" in claim:
            section = (
                "interdogpendence"
                if claim["claim_type"] == "system_interaction"
                else "takeaways"
            )
            index = theme_indexes[section]
            claim["theme_group_id"] = registries[section][index % 4]["id"]
            theme_indexes[section] += 1
    for summary in edited["summary"].values():
        summary["dos"] = ["Do one", "Do two", "Do three"]
        summary["donts"] = ["Avoid one", "Avoid two", "Avoid three"]
    return edited


def complete_theme_plan(path: Path, packet: dict) -> None:
    text = path.read_text(encoding="utf-8")
    completed = complete_packet(packet)
    replacements = {
        f"theme_group_registry.{section}": json.dumps(entries, ensure_ascii=False)
        for section, entries in completed["theme_group_registry"].items()
    }
    replacements.update({
        f"theme_group.{section}.{card['priority_id']}": card["theme_group_id"]
        for card in completed["cards"]
        if (section := (
            "interdogpendence"
            if card["claim_type"] == "system_interaction"
            else "takeaways"
            if card["claim_type"] == "synthesized_theme"
            else None
        ))
    })
    for field, value in replacements.items():
        text = re.sub(
            rf"(<!-- BEGIN FIELD: {re.escape(field)} -->\s*)__WRITE__(\s*<!-- END FIELD: {re.escape(field)} -->)",
            lambda match, replacement=value: f"{match.group(1)}{replacement}{match.group(2)}",
            text,
        )
    path.write_text(text, encoding="utf-8")


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
            self.assertEqual(expected, "theme_group_id" in claim)

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
            self.assertEqual(3, len(claim["dos"]))
            self.assertEqual(3, len(claim["donts"]))
        for summary in self.packet["summary"].values():
            self.assertEqual(3, len(summary["dos"]))
            self.assertEqual(3, len(summary["donts"]))

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
        self.assertTrue(all(
            entry["subtitle"].strip()
            for entries in edited["theme_group_registry"].values()
            for entry in entries
        ))

    def test_editorial_validator_allows_optional_registry_subtitles(self) -> None:
        edited = complete_packet(self.packet)
        variants = ("missing", None, "", "   ")
        for variant in variants:
            candidate = deepcopy(edited)
            entry = candidate["theme_group_registry"]["interdogpendence"][0]
            if variant == "missing":
                entry.pop("subtitle")
            else:
                entry["subtitle"] = variant
            report = run_editorial_validator(
                self.packet, candidate, "--phase", "authoring"
            )
            self.assertEqual("pass", report["status"], report["errors"])

    def test_editorial_validator_rejects_nonstring_registry_subtitle(self) -> None:
        edited = complete_packet(self.packet)
        edited["theme_group_registry"]["interdogpendence"][0]["subtitle"] = 42
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("fail", report["status"])
        self.assertTrue(any(
            "invalid subtitle" in error for error in report["errors"]
        ))

    def test_no_astro_advisory_distinguishes_ordinary_and_astrological_usage(self) -> None:
        ordinary = [
            "The house becomes quiet after dinner.",
            "She rests in her favorite square of sunlight.",
            "The sofa has a seating chart.",
        ]
        astrological = [
            "Mars occupies House 7.",
            "This belongs to the seventh house.",
            "Her Doghouse 4 pattern concerns safety.",
            "Several parts of her chart repeat the theme.",
            "The square's friction needs a practiced channel.",
            "A Jupiter-Saturn checkpoint slows the launch.",
        ]
        for text in ordinary:
            self.assertIsNone(ASTRO_TERMS.search(text), text)
        for text in astrological:
            self.assertIsNotNone(ASTRO_TERMS.search(text), text)

    def test_editorial_validator_rejects_too_few_section_chapters(self) -> None:
        edited = complete_packet(self.packet)
        edited["theme_group_registry"]["takeaways"] = (
            edited["theme_group_registry"]["takeaways"][:2]
        )
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("fail", report["status"])
        self.assertTrue(any(
            "takeaways must define three to five" in error
            for error in report["errors"]
        ))

    def test_editorial_validator_defers_lopsided_chapter_policy(self) -> None:
        edited = complete_packet(self.packet)
        ids = [
            entry["id"]
            for entry in edited["theme_group_registry"]["interdogpendence"]
        ]
        cards = [
            card for card in edited["cards"]
            if card["claim_type"] == "system_interaction"
        ]
        for index, card in enumerate(cards):
            card["theme_group_id"] = ids[index // 2] if index < 6 else ids[-1]
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_editorial_validator_defers_cross_section_title_policy(self) -> None:
        edited = complete_packet(self.packet)
        edited["theme_group_registry"]["takeaways"][0]["title"] = (
            edited["theme_group_registry"]["interdogpendence"][0]["title"]
        )
        report = run_editorial_validator(
            self.packet, edited, "--phase", "authoring"
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_editorial_validator_preserves_legacy_theme_group_contract(self) -> None:
        baseline = deepcopy(self.packet)
        edited = complete_packet(self.packet)
        baseline.pop("theme_group_registry", None)
        edited.pop("theme_group_registry", None)
        theme_index = 0
        for before, after in zip(baseline["cards"], edited["cards"]):
            if "theme_group_id" not in before:
                continue
            before.pop("theme_group_id")
            after.pop("theme_group_id")
            before["theme_group"] = "__LLM_FILL__"
            after["theme_group"] = f"Chapter {(theme_index % 4) + 1}"
            theme_index += 1
        report = run_editorial_validator(
            baseline, edited, "--phase", "authoring"
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
        self.assertEqual(
            "reject",
            report["authoring_pass_acceptance"]["status"],
        )

    def test_authoring_pass_acceptance_ignores_overlap_within_one_card(
        self,
    ) -> None:
        edited = complete_packet(self.packet)
        edited["cards"] = edited["cards"][:1]
        edited["summary"] = {}
        repeated = (
            "A deliberately repeated twelve word passage remains inside one "
            "card across all editorial renderings today."
        )
        for density in ("no_astro", "light_astro", "full_astro"):
            for voice in ("handler", "direct_to_dog", "hybrid"):
                edited["cards"][0]["card"][density]["body"][voice] = repeated
        report = authoring_pass_acceptance(reader_facing_items(edited))
        self.assertEqual("accept", report["status"])
        self.assertEqual(0, report["repeated_ngram_group_count"])

    def test_authoring_pass_acceptance_rejects_cross_card_passages(
        self,
    ) -> None:
        edited = complete_packet(self.packet)
        repeated = (
            "This deliberately repeated twelve word passage exposes a reusable "
            "template across otherwise separate cards."
        )
        for card in edited["cards"][:3]:
            card["card"]["no_astro"]["body"]["handler"] = repeated
        report = authoring_pass_acceptance(reader_facing_items(edited))
        self.assertEqual("reject", report["status"])
        codes = {
            reason["code"] for reason in report["rejection_reasons"]
        }
        self.assertIn("cross_card_exact_duplicate", codes)
        self.assertIn("cross_card_repeated_passage", codes)

    def test_authoring_pass_acceptance_rejects_metric_gaming_artifacts(
        self,
    ) -> None:
        edited = complete_packet(self.packet)
        edited["cards"] = edited["cards"][:10]
        edited["summary"] = {}
        for index, card in enumerate(edited["cards"]):
            card["card"]["no_astro"]["body"]["handler"] = (
                f"Distinct observation {index} begins here "
                "[private phrase] and continues [private phrase] through "
                "the evidence [private phrase] before ending [private phrase]."
            )
        report = authoring_pass_acceptance(reader_facing_items(edited))
        codes = {
            reason["code"] for reason in report["rejection_reasons"]
        }
        self.assertEqual("reject", report["status"])
        self.assertIn("editorial_artifact_insertion", codes)

    def test_authoring_pass_acceptance_rejects_multi_field_opening_template(
        self,
    ) -> None:
        edited = complete_packet(self.packet)
        edited["cards"] = edited["cards"][:10]
        edited["summary"] = {}
        for index, card in enumerate(edited["cards"][:8]):
            card["card"]["no_astro"]["body"]["handler"] = (
                f"Ashley notices first, then handler example {index} diverges."
            )
            card["card"]["light_astro"]["body"]["hybrid"] = (
                f"Between Ashley and her person, example {index} diverges."
            )
        report = authoring_pass_acceptance(reader_facing_items(edited))
        codes = {
            reason["code"] for reason in report["rejection_reasons"]
        }
        self.assertEqual("reject", report["status"])
        self.assertIn("multi_field_opening_template", codes)

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


    def test_story_workspace_round_trip_keeps_json_out_of_authoring_surface(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "bre"
            build_story_workspace(workspace, self.packet, ROOT, 2)
            self.assertEqual([], list(workspace.rglob("*.json")))
            self.assertTrue((workspace / "DOG DETAILS.md").exists())
            self.assertTrue((workspace / "FULL CHART BASIS.md").exists())
            self.assertTrue((workspace / "WRITE WHOLE DOG PROFILE.md").exists())
            self.assertTrue((workspace / "GUIDING LIGHTS.md").exists())
            self.assertTrue((workspace / "lint_authoring_pass.py").exists())
            self.assertFalse(
                (workspace / "lint_astrowoof_editorial.py").exists()
            )
            self.assertFalse(
                (workspace / "assemble_authoring_workspace.py").exists()
            )
            self.assertFalse((workspace / "WHOLE DOG CONTEXT.md").exists())
            start_here = (workspace / "START HERE.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Mechanical acceptance requirements", start_here)
            self.assertNotIn("twelve words", start_here)
            self.assertIn("python lint_authoring_pass.py .", start_here)
            self.assertIn(
                "Treat a rejection as an editorial signal",
                start_here,
            )

            self.assertIn(
                "rewrite the prose in a natural voice",
                start_here,
            )
            opaque_checker = (
                workspace / "lint_authoring_pass.py"
            ).read_text(encoding="utf-8")
            self.assertIn("_PAYLOAD =", opaque_checker)
            self.assertNotIn("PASS_NGRAM_MIN_CLAIMS", opaque_checker)
            self.assertNotIn("cross_card_repeated_passage", opaque_checker)
            story_template = next(
                (workspace / "cards").rglob("WRITE THIS CARD.md")
            ).read_text(encoding="utf-8")
            self.assertIn(
                "Let the previous page leave your desk",
                story_template,
            )
            self.assertIn("plan.memorable_takeaway", story_template)
            self.assertIn("plan.semantic_contributions", story_template)
            self.assertIn("plan.writing_form", story_template)
            self.assertIn("plan.comic_premise", story_template)
            self.assertIn("plan.audience_postures", story_template)
            profile = workspace / "WRITE WHOLE DOG PROFILE.md"
            profile.write_text(
                profile.read_text(encoding="utf-8").replace(
                    "__WRITE__",
                    "Whole-dog profile text.",
                ),
                encoding="utf-8",
            )
            claim_brief = next((workspace / "cards").rglob("CLAIM AND EVIDENCE.md"))
            claim_text = claim_brief.read_text(encoding="utf-8")
            self.assertIn("## Story Brief", claim_text)
            self.assertIn("## Underlying Astrology", claim_text)
            self.assertNotIn("## Exact assignment", claim_text)
            expected_projection_groups = sum(
                len({
                    json.dumps(
                        authoring_projection_payload(wrapper),
                        sort_keys=True,
                    )
                    for wrapper in evidence.get("context_records", {}).values()
                })
                for evidence in self.packet["cards"][0].get("evidence", [])
            )
            self.assertEqual(
                expected_projection_groups,
                claim_text.count("**Projection used by:**"),
            )
            self.assertNotIn("## Allowed filter vocabulary", claim_text)
            brief = (workspace / "AUTHORING BRIEF.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("High level: Personality; Learning; Play", brief)
            full_chart = (workspace / "FULL CHART BASIS.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Selected Chart Material", full_chart)
            self.assertIn("## Complete Projected-Term Registry", full_chart)
            self.assertIn("**Source references:**", full_chart)
            for card in self.packet["cards"]:
                self.assertIn(card["claim_id"], full_chart)
            for claim in self.packet.get("unselected_claims", []):
                self.assertIn(
                    claim.get("claim_id", claim.get("candidate_id")),
                    full_chart,
                )
            story_directories = sorted((workspace / "cards").iterdir())
            self.assertEqual(2, len(story_directories))
            for story in story_directories:
                writing = story / "WRITE THIS CARD.md"
                writing.write_text(
                    writing.read_text(encoding="utf-8").replace(
                        "__WRITE__",
                        "Personality",
                    ),
                    encoding="utf-8",
                )
            gate_report = workspace / "gate-report.json"
            gate = subprocess.run(
                [
                    sys.executable,
                    str(workspace / "lint_authoring_pass.py"),
                    str(workspace),
                    "--output",
                    str(gate_report),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(2, gate.returncode, gate.stderr)
            public_report = json.loads(gate_report.read_text(encoding="utf-8"))
            self.assertEqual("reject", public_report["status"])
            self.assertTrue(public_report["editorial_issue_codes"])
            self.assertNotIn("thresholds", public_report)
            self.assertNotIn("repeated_ngrams", public_report)
            deck, report = assemble(
                self.packet,
                workspace,
                allow_partial=True,
            )
            self.assertEqual([1, 2], report["authored_priority_ids"])
            self.assertEqual(3, report["next_unfinished_priority_id"])
            self.assertTrue(report["placeholder_free"])
            self.assertEqual(10, report["whole_dog_profile_field_count"])
            self.assertEqual(
                self.packet["cards"][0]["claim_id"],
                deck["cards"][0]["claim_id"],
            )
            self.assertEqual(
                "Personality",
                deck["cards"][0]["card"]["no_astro"]["body"]["handler"],
            )

    def test_compact_full_chart_basis_preserves_contexts_and_traceability(
        self,
    ) -> None:
        basis = build_compact_full_chart_basis(self.packet)
        self.assertEqual(
            "deterministic_downstream_reconstruction",
            basis["authority"],
        )
        self.assertEqual(50, len(basis["selected_claims"]))
        self.assertEqual(
            len(self.packet.get("unselected_claims", [])),
            len(basis["additional_claims"]),
        )
        self.assertEqual(
            {card["claim_id"] for card in self.packet["cards"]},
            {claim["claim_id"] for claim in basis["selected_claims"]},
        )
        object_contexts = {
            context
            for item in basis["objects"]
            for group in item["context_projections"]
            for context in group["contexts"]
        }
        self.assertEqual(
            {"general", "direct_to_dog", "handler", "hybrid"},
            object_contexts,
        )
        self.assertTrue(all(item["source_ref"] for item in basis["objects"]))
        self.assertTrue(
            all(item["source_ref"] for item in basis["relationships"])
        )
        compact = render_full_chart_basis(self.packet, "compact-v1")
        legacy = render_full_chart_basis(self.packet)
        self.assertIn("## Source and Projected Objects", compact)
        self.assertIn("## Concise Projected-Term Decoder", compact)
        self.assertIn("not a canonical chart export", compact)
        self.assertLess(len(compact), len(legacy))

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "bre"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                2,
                full_chart_basis_format="compact-v1",
            )
            self.assertFalse((workspace / "FULL CHART BASIS.json").exists())
            self.assertIn(
                "## Source and Projected Relationships",
                (workspace / "FULL CHART BASIS.md").read_text(encoding="utf-8"),
            )

    def test_compact_v2_is_an_author_only_chart_map(self) -> None:
        compact_v1 = render_full_chart_basis(self.packet, "compact-v1")
        compact_v2 = render_full_chart_basis(self.packet, "compact-v2")
        self.assertIn("## How to Read This Map", compact_v2)
        self.assertIn("## Placements and Angles", compact_v2)
        self.assertIn("## Aspects and Interactions", compact_v2)
        self.assertIn("## Chart Structure at a Glance", compact_v2)
        self.assertIn("## Projected-Term Decoder", compact_v2)
        self.assertNotIn("Selected Chart Material", compact_v2)
        self.assertNotIn("Additional Chart Material", compact_v2)
        self.assertNotIn("Reconstruction Limits", compact_v2)
        self.assertNotIn(self.packet["cards"][0]["claim_id"], compact_v2)
        self.assertLess(len(compact_v2), len(compact_v1))
        self.assertIn("function(mode) @ domain", compact_v2)
        self.assertIn("relationship(mode): source <> target", compact_v2)

    def test_compact_v2_preserves_genuine_context_variants(self) -> None:
        packet = deepcopy(self.packet)
        evidence = next(
            evidence
            for card in packet["cards"]
            for evidence in card.get("evidence", [])
            if evidence.get("kind") == "projected_object"
        )
        contexts = evidence["context_records"]
        contexts["handler"]["record"]["name"] = "handler_only_function"
        compact_v2 = render_full_chart_basis(packet, "compact-v2")
        self.assertIn("[handler] handler_only_function", compact_v2)
        self.assertIn("[direct-to-dog, general, hybrid]", compact_v2)

    def test_split_story_workspaces_combine_into_one_complete_deck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            specs = [
                (1, 1, 10, False, False),
                (2, 11, 10, False, False),
                (3, 21, 10, False, False),
                (4, 31, 10, False, False),
                (5, 41, 10, False, False),
                (6, 51, 0, True, True),
            ]
            for number, start, count, summaries, theme_plan in specs:
                workspace = root / f"bre_{number}"
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    count,
                    card_start=start,
                    include_summaries=summaries,
                    include_theme_plan=theme_plan,
                    pass_number=number,
                    pass_count=6,
                )
                gold_path = workspace / "SUMMARY GOLD REFERENCE.md"
                thesis_path = workspace / "WRITE SUMMARY THESIS PLAN.md"
                if number == 6:
                    self.assertTrue(gold_path.is_file())
                    self.assertTrue(thesis_path.is_file())
                    self.assertIn(
                        "Kevin is an example subject, not evidence",
                        gold_path.read_text(encoding="utf-8"),
                    )
                    self.assertIn(
                        "The Friendly Original With a Serious Heart",
                        gold_path.read_text(encoding="utf-8"),
                    )
                    thesis_text = thesis_path.read_text(encoding="utf-8")
                    self.assertIn("summary_plan.identity_thesis", thesis_text)
                    self.assertIn(
                        "summary_plan.identity_lens_boundary", thesis_text
                    )
                    self.assertIn(
                        "summary_plan.daily_life_lens_boundary", thesis_text
                    )
                    self.assertIn(
                        "summary_plan.needs_lens_boundary", thesis_text
                    )
                    self.assertIn(
                        "summary_plan.growth_lens_boundary", thesis_text
                    )
                    self.assertIn(
                        "summary_plan.recurring_motif_allocation", thesis_text
                    )
                    self.assertIn(
                        "summary_plan.needs_vs_growth_distinction",
                        thesis_text,
                    )
                    self.assertIn(
                        "same motif may not serve as the remembered conclusion",
                        thesis_text,
                    )
                    start_here = (workspace / "START HERE.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertIn("SUMMARY GOLD REFERENCE.md", start_here)
                    self.assertIn("WRITE SUMMARY THESIS PLAN.md", start_here)
                else:
                    self.assertFalse(gold_path.exists())
                    self.assertFalse(thesis_path.exists())
                for writing in workspace.rglob("WRITE*.md"):
                    writing.write_text(
                        writing.read_text(encoding="utf-8").replace(
                            "__WRITE__",
                            "Personality",
                        ),
                        encoding="utf-8",
                    )
                theme_path = workspace / "ASSIGN THEME GROUPS.md"
                if theme_path.exists():
                    complete_theme_plan(theme_path, self.packet)
            deck, report = assemble(
                self.packet,
                root,
                allow_partial=False,
            )
            self.assertEqual(6, report["workspace_count"])
            self.assertEqual(list(range(1, 51)), report["authored_priority_ids"])
            self.assertEqual([1, 2, 3, 4], report["authored_summary_ids"])
            self.assertTrue(report["authored_theme_group_priority_ids"])
            self.assertTrue(report["placeholder_free"])
            self.assertNotIn("__LLM_FILL__", json.dumps(deck))
            self.assertTrue(all(
                entry["subtitle"].strip()
                for entries in deck["theme_group_registry"].values()
                for entry in entries
            ))

    def test_summary_workspace_excludes_same_subject_gold_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "kevin_6"
            packet = deepcopy(self.packet)
            packet["subject"]["subject_id"] = "kevin"
            packet["subject"]["display_name"] = "Kevin"
            build_story_workspace(
                workspace,
                packet,
                ROOT,
                0,
                card_start=51,
                include_summaries=True,
                include_theme_plan=True,
                pass_number=6,
                pass_count=6,
            )
            self.assertFalse(
                (workspace / "SUMMARY GOLD REFERENCE.md").exists()
            )
            self.assertTrue(
                (workspace / "WRITE SUMMARY THESIS PLAN.md").is_file()
            )
            start_here = (workspace / "START HERE.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("read `SUMMARY GOLD REFERENCE.md`", start_here)
            self.assertIn("No prose reference is supplied", start_here)
            self.assertIn("WRITE SUMMARY THESIS PLAN.md", start_here)

    def test_stratified_split_assignment_is_deterministic_and_complete(self) -> None:
        first = build_split_assignment_plan(self.packet, "stratified-v1")
        second = build_split_assignment_plan(self.packet, "stratified-v1")
        self.assertEqual(first, second)
        assigned = [
            priority_id
            for pass_ids in first["passes"].values()
            for priority_id in pass_ids
        ]
        self.assertEqual(list(range(1, 51)), sorted(assigned))
        self.assertTrue(all(len(pass_ids) == 10 for pass_ids in first["passes"].values()))
        self.assertEqual("stratified-v1", first["algorithm_version"])
        self.assertRegex(first["seed"], r"^[0-9a-f]{16}$")

    def test_stratified_split_improves_type_and_category_balance(self) -> None:
        by_priority = {card["priority_id"]: card for card in self.packet["cards"]}

        def imbalance(policy: str) -> tuple[int, int]:
            plan = build_split_assignment_plan(self.packet, policy)
            passes = [
                [by_priority[priority_id] for priority_id in priority_ids]
                for priority_ids in plan["passes"].values()
            ]
            claim_types = {
                card["claim_type"] for card in self.packet["cards"]
            }
            categories = {
                category
                for card in self.packet["cards"]
                for category in card["categories"]
            }

            def spread(values: set[str], extractor) -> int:
                return sum(
                    max(
                        sum(value in extractor(card) for card in pass_cards)
                        for pass_cards in passes
                    )
                    - min(
                        sum(value in extractor(card) for card in pass_cards)
                        for pass_cards in passes
                    )
                    for value in values
                )

            return (
                spread(claim_types, lambda card: {card["claim_type"]}),
                spread(categories, lambda card: set(card["categories"])),
            )

        contiguous = imbalance("contiguous")
        stratified = imbalance("stratified-v1")
        self.assertLessEqual(stratified[0], contiguous[0])
        self.assertLessEqual(stratified[1], contiguous[1])

    def test_stratified_workspaces_reassemble_in_canonical_order(self) -> None:
        plan = build_split_assignment_plan(self.packet, "stratified-v1")
        by_priority = {card["priority_id"]: card for card in self.packet["cards"]}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for number in range(1, 6):
                assigned = [
                    by_priority[priority_id]
                    for priority_id in plan["passes"][str(number)]
                ]
                workspace = root / f"bre_{number}"
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    len(assigned),
                    card_start=assigned[0]["priority_id"],
                    include_summaries=False,
                    pass_number=number,
                    pass_count=6,
                    assigned_cards=assigned,
                )
                for writing in workspace.rglob("WRITE*.md"):
                    writing.write_text(
                        writing.read_text(encoding="utf-8").replace(
                            "__WRITE__", "Personality"
                        ),
                        encoding="utf-8",
                    )
            summary_workspace = root / "bre_6"
            build_story_workspace(
                summary_workspace,
                self.packet,
                ROOT,
                0,
                card_start=51,
                include_summaries=True,
                include_theme_plan=True,
                pass_number=6,
                pass_count=6,
                assigned_cards=[],
            )
            for writing in summary_workspace.rglob("WRITE*.md"):
                writing.write_text(
                    writing.read_text(encoding="utf-8").replace(
                        "__WRITE__", "Personality"
                    ),
                    encoding="utf-8",
                )
            complete_theme_plan(
                summary_workspace / "ASSIGN THEME GROUPS.md",
                self.packet,
            )
            deck, report = assemble(self.packet, root, allow_partial=False)
            self.assertEqual(list(range(1, 51)), report["authored_priority_ids"])
            self.assertEqual(
                list(range(1, 51)),
                [card["priority_id"] for card in deck["cards"]],
            )

    def test_pass_six_theme_plan_contains_direct_varied_subtitle_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "bre_6"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                0,
                card_start=51,
                include_summaries=True,
                include_theme_plan=True,
                pass_number=6,
                pass_count=6,
                assigned_cards=[],
            )
            theme_plan = (workspace / "ASSIGN THEME GROUPS.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Speak directly about the dog's pattern", theme_plan)
            self.assertIn("Let sentence movement vary naturally", theme_plan)
            self.assertIn("These cards ...", theme_plan)
            first_pass = Path(temporary) / "bre_1"
            build_story_workspace(
                first_pass,
                self.packet,
                ROOT,
                10,
                card_start=1,
                pass_number=1,
                pass_count=6,
            )
            self.assertFalse((first_pass / "ASSIGN THEME GROUPS.md").exists())

    def test_story_workspace_archive_contains_named_root_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "kevin_1"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                10,
                card_start=1,
                pass_number=1,
                pass_count=6,
            )
            (workspace / "WORKSPACE MANIFEST.md").write_text(
                "# Manifest\n",
                encoding="utf-8",
            )
            archive_path = archive_story_workspace(workspace)
            self.assertEqual(root / "kevin_1.zip", archive_path)
            self.assertTrue(archive_path.is_file())
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            self.assertIn("kevin_1/START HERE.md", names)
            self.assertIn("kevin_1/GUIDING LIGHTS.md", names)
            self.assertIn("kevin_1/lint_authoring_pass.py", names)
            self.assertIn("kevin_1/WORKSPACE MANIFEST.md", names)


class TestPackageDiscoveryAndRegistry(unittest.TestCase):
    def test_optional_subject_params_populate_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "kevin")
            params = {
                "display_name": "Kevin",
                "gender": "male",
                "pronouns": {
                    "subject": "he",
                    "object": "him",
                    "possessive_adjective": "his",
                    "possessive_pronoun": "his",
                    "reflexive": "himself",
                },
                "birth_datetime": "2020-01-02T03:04:00-07:00",
                "birth_latitude": 39.7392,
                "birth_longitude": -104.9903,
                "birth_location": "Denver, Colorado",
            }
            (root / "params.json").write_text(
                json.dumps(params),
                encoding="utf-8",
            )
            paths = discover_subject_packages(root)["kevin"]
            loaded, source = load_subject_params("kevin", paths)
            record = subject_record("kevin", loaded)
            self.assertEqual(str((root / "params.json").resolve()), source)
            self.assertEqual("he", record["pronouns"]["subject"])
            self.assertEqual(39.7392, record["birth_latitude"])

    def test_invalid_subject_params_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "kevin")
            (root / "params.json").write_text(
                json.dumps({"subject_id": "someone-else"}),
                encoding="utf-8",
            )
            paths = discover_subject_packages(root)["kevin"]
            with self.assertRaisesRegex(ValueError, "must match"):
                load_subject_params("kevin", paths)

    def test_handoff_static_assets_include_execution_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "subject"
            copy_static_assets(bundle, ROOT, None)
            expected = {
                "AstroWoof Projected Natal Card Authoring Manual.md",
                "AstroWoof Independent Card Writing Brief.md",
                "LLM Card-by-Card Authoring Execution Protocol.md",
                "LLM Editing Permissions and QA Checklist.md",
                "Proposed LLM Handoff Prompt.md",
            }
            self.assertTrue(
                expected.issubset(
                    {path.name for path in (bundle / "static").iterdir()}
                )
            )

    def test_compact_handoff_static_assets_exclude_rigorous_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "subject"
            copy_static_assets(bundle, ROOT, None, "compact")
            names = {path.name for path in (bundle / "static").iterdir()}
            self.assertIn(
                "AstroWoof Compact Single-Subject Authoring Brief.md",
                names,
            )
            self.assertIn("Compact LLM Handoff Prompt.md", names)
            self.assertNotIn(
                "LLM Card-by-Card Authoring Execution Protocol.md",
                names,
            )
            self.assertNotIn("Proposed LLM Handoff Prompt.md", names)

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

    def test_accepts_opaque_canonical_source_identity(self) -> None:
        source_id = "9e0de4ce-58b2-4d0d-8d56-d58ec767b798"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            suffixes = {
                "general": "general",
                "direct_to_dog": "d2d",
                "handler": "handler",
                "hybrid": "hybrid",
            }
            for context, suffix in suffixes.items():
                path = root / f"natal.bre.woof.{suffix}.json"
                path.write_text(
                    json.dumps(minimal_graph("bre", context, source_id=source_id)),
                    encoding="utf-8",
                )
            paths = discover_subject_packages(root)["bre"]
            contexts, _registry, audit = load_and_validate_contexts("bre", paths)
            self.assertEqual(source_id, contexts["general"]["source_identity"]["source_chart_id"])
            self.assertEqual(source_id, audit["source_identity"]["source_chart_id"])

    def test_rejects_mixed_opaque_canonical_source_identities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "bre")
            handler = root / "natal.bre.woof.handler.json"
            graph = json.loads(handler.read_text(encoding="utf-8"))
            source_id = "9e0de4ce-58b2-4d0d-8d56-d58ec767b798"
            graph["source_identity"] = {
                "source_chart_id": source_id,
                "source_chart_ids": [source_id],
                "sensor_instance_id": source_id,
            }
            handler.write_text(json.dumps(graph), encoding="utf-8")
            paths = discover_subject_packages(root)["bre"]
            with self.assertRaisesRegex(
                ValueError, "canonical source identity differs from general"
            ):
                load_and_validate_contexts("bre", paths)

    def test_rejects_missing_canonical_source_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_subject(root, "bre")
            for path in root.glob("natal.bre.woof.*.json"):
                graph = json.loads(path.read_text(encoding="utf-8"))
                graph["source_identity"] = {}
                path.write_text(json.dumps(graph), encoding="utf-8")
            paths = discover_subject_packages(root)["bre"]
            with self.assertRaisesRegex(ValueError, "non-empty source_identity"):
                load_and_validate_contexts("bre", paths)

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
# End of test module.
