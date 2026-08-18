from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_admission import (  # noqa: E402
    BoundedAdmission,
    REQUIRED_CONTEXTS,
)
from astrowoof_natal_authoring.bounded_authoring import (  # noqa: E402
    AUTHORING_PACKET_CONTRACT,
    BOUNDED_PASS_PACKET_CONTRACT,
    BOUNDED_RUN_V2_CONTRACT,
    BOUNDED_SPLIT_ASSIGNMENT_CONTRACT,
    CLAIM_DECK_CONTRACT,
    FINAL_CARDS_CONTRACT,
    BoundedAuthoringError,
    assemble_bounded_editorial_passes,
    assert_provider_minimized,
    build_bounded_pass_packets,
    build_bounded_split_assignment,
    compile_bounded_authoring_artifacts,
    fake_author_bounded,
    validate_bounded_authoring_packet,
    validate_bounded_claim_deck,
    validate_bounded_final_cards,
    validate_bounded_pass_packet,
    validate_bounded_split_assignment,
)
from astrowoof_natal_authoring.bounded_provider import (  # noqa: E402
    OpenAIBoundedLifecycleProvider,
)
from astrowoof_natal_authoring.bounded_selection import (  # noqa: E402
    select_bounded_portfolio,
)
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from test_bounded_selection import portfolio_basis  # noqa: E402


def admission() -> BoundedAdmission:
    terms = {
        **{
            f"{index:02d}": {
                "term_type": "operator",
                "canonical_label": f"Term {index:02d}",
                "short_description": f"Selected term {index:02d}.",
            }
            for index in range(20)
        },
        **{
            kind: {
                "term_type": "theme",
                "canonical_label": kind.replace("_", " ").title(),
                "short_description": f"Selected {kind} semantics.",
            }
            for kind in (
                "foundational_object",
                "individualized_relationship",
                "derived_family",
                "invariant_configuration",
            )
        },
    }
    artifacts = {
        context: {
            "metadata": {"context_id": context},
            "projected_term_registry": {
                "registry_id": "bounded-test-terms",
                "registry_version": "1.0.0",
                "target_ontology": "woofmapped_astrology.v0",
                "materialization": "used_terms_subset",
                "terms": deepcopy(terms),
            },
            "limitations": [
                "bounded_invariant_subgraph_not_exact_chart",
                "no_representative_or_midpoint_positions",
                "no_exact_longitudes_or_orbs",
            ],
        }
        for context in REQUIRED_CONTEXTS
    }
    return BoundedAdmission(
        artifacts,
        {
            "admission_id": "bounded_admission:test",
            "source_artifact_sha256": "a" * 64,
            "output_contract": "projected_bounded_semantic_graph.v1",
            "contract_version": "1.0.0",
            "spc_version": "0.11.0",
            "profile_id": "woofmapped_bounded_astrology.v0",
            "profile_version": "0.1.0",
            "projected_term_registry_sha256": "b" * 64,
        },
        {},
    )


def compiled():
    selection = select_bounded_portfolio(portfolio_basis())
    return compile_bounded_authoring_artifacts(
        admission(),
        selection,
        subject={
            "subject_id": "dog-uuid",
            "display_name": "Juniper",
            "subject_type": "dog",
            "breed": "Mystery Hound",
            "birth_datetime": "1981-10-10T15:00:00-06:00",
            "birth_latitude": 39.7392,
            "birth_longitude": -104.9903,
            "birth_location": "SEED-PROTECTED-DENVER",
            "earliest_local": "SEED-PROTECTED-START",
            "latest_local": "SEED-PROTECTED-END",
        },
    )


class TestBoundedAuthoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = compiled()

    def test_separate_contracts_compile_exactly_fifty_closed_claims(self) -> None:
        claim_deck = self.artifacts.claim_deck
        packet = self.artifacts.authoring_packet
        self.assertEqual(CLAIM_DECK_CONTRACT, claim_deck["schema_version"])
        self.assertEqual(AUTHORING_PACKET_CONTRACT, packet["schema_version"])
        self.assertEqual(50, len(claim_deck["claims"]))
        self.assertEqual(50, len(packet["claims"]))
        validate_bounded_claim_deck(claim_deck)
        validate_bounded_authoring_packet(packet, claim_deck)
        selected = {claim["claim_id"] for claim in claim_deck["claims"]}
        self.assertTrue(
            all(
                set(claim["authority"]["dependency_claim_ids"]) <= selected
                for claim in claim_deck["claims"]
            )
        )

    def test_provider_view_is_allow_listed_and_protected_values_are_absent(self) -> None:
        packet = self.artifacts.authoring_packet
        rendered = json.dumps(packet, sort_keys=True)
        self.assertIn("Juniper", rendered)
        self.assertIn("Mystery Hound", rendered)
        protected = (
            "1981-10-10T15:00:00-06:00",
            "39.7392",
            "-104.9903",
            "SEED-PROTECTED-DENVER",
            "SEED-PROTECTED-START",
            "SEED-PROTECTED-END",
        )
        assert_provider_minimized(packet, protected_values=protected)
        for value in protected:
            self.assertNotIn(value, rendered)
        for prohibited in (
            "projection_relevance_score",
            "range_evidence",
            "source_identity",
            "source_artifact_ref",
            "structural_strength_score",
        ):
            self.assertNotIn(prohibited, rendered)
        self.assertNotIn("outside_scope", rendered)
        self.assertNotIn("unselected", rendered)

    def test_bounded_split_assignment_is_deterministic_complete_and_mixed(self) -> None:
        first = self.artifacts.split_assignment
        second = build_bounded_split_assignment(
            self.artifacts.authoring_packet, self.artifacts.claim_deck
        )
        self.assertEqual(first, second)
        self.assertEqual(BOUNDED_SPLIT_ASSIGNMENT_CONTRACT, first["schema_version"])
        self.assertEqual(BOUNDED_RUN_V2_CONTRACT, first["run_contract"])
        validate_bounded_split_assignment(first, self.artifacts.authoring_packet)
        memberships = [
            claim_id
            for pass_record in first["card_passes"]
            for claim_id in pass_record["ordered_claim_ids"]
        ]
        self.assertEqual(50, len(memberships))
        self.assertEqual(50, len(set(memberships)))
        self.assertEqual(
            set(first["canonical_claim_ids"]), set(memberships)
        )
        by_id = {
            claim["claim_id"]: claim for claim in self.artifacts.authoring_packet["claims"]
        }
        for pass_record in first["card_passes"]:
            claims = [by_id[claim_id] for claim_id in pass_record["ordered_claim_ids"]]
            self.assertGreaterEqual(len({claim["claim_kind"] for claim in claims}), 2)
            self.assertGreaterEqual(len({claim["editorial_tier"] for claim in claims}), 2)
        self.assertEqual([], first["summary_pass"]["ordered_claim_ids"])

    def test_bounded_pass_packets_are_six_self_contained_minimized_views(self) -> None:
        packets = self.artifacts.pass_packets
        assignment = self.artifacts.split_assignment
        self.assertEqual(6, len(packets))
        protected = (
            "1981-10-10T15:00:00-06:00", "39.7392", "-104.9903",
            "SEED-PROTECTED-DENVER", "SEED-PROTECTED-START",
            "SEED-PROTECTED-END",
        )
        for pass_record in [*assignment["card_passes"], assignment["summary_pass"]]:
            packet = packets[pass_record["pass_id"]]
            self.assertEqual(BOUNDED_PASS_PACKET_CONTRACT, packet["schema_version"])
            self.assertEqual(BOUNDED_RUN_V2_CONTRACT, packet["run_contract"])
            self.assertEqual(assignment["assignment_sha256"], packet["assignment_sha256"])
            self.assertEqual(50, len(packet["whole_dog_context"]))
            self.assertEqual(
                pass_record["ordered_claim_ids"],
                [claim["claim_id"] for claim in packet["claims"]],
            )
            self.assertEqual(
                pass_record["purpose"] == "summary_theme", bool(packet["summaries"])
            )
            self.assertEqual(2, len(packet["resource_set"]["resources"]))
            validate_bounded_pass_packet(
                packet, self.artifacts.authoring_packet, assignment
            )
            assert_provider_minimized(packet, protected_values=protected)
            term_keys = set(packet["projected_term_registry"]["terms"])
            referenced = {
                ref.rsplit(":", 1)[-1]
                for claim in packet["whole_dog_context"]
                for ref in claim["projected_term_refs"]
            }
            self.assertEqual(referenced, term_keys)

    def test_pass_outputs_reassemble_in_canonical_order_and_hydrate_authority(self) -> None:
        packet = self.artifacts.authoring_packet
        assignment = self.artifacts.split_assignment
        final = fake_author_bounded(packet)
        final_by_id = {card["claim_id"]: card for card in final["cards"]}
        editorial_fields = (
            "dos", "donts", "funny_dog_quotes", "imperative_dog_quotes",
            "applicable_canine_jokes", "densities",
        )
        outputs = {}
        for pass_record in reversed(assignment["card_passes"]):
            outputs[pass_record["pass_id"]] = {
                "pass_id": pass_record["pass_id"],
                "cards": [
                    {"claim_id": claim_id} | {
                        field: deepcopy(final_by_id[claim_id][field])
                        for field in editorial_fields
                    }
                    for claim_id in reversed(pass_record["ordered_claim_ids"])
                ],
            }
        outputs[assignment["summary_pass"]["pass_id"]] = {
            "pass_id": assignment["summary_pass"]["pass_id"],
            "summaries": [
                {
                    "summary_id": summary_id,
                    "headline": deepcopy(final["summaries"][summary_id]["headline"]),
                    "body": deepcopy(final["summaries"][summary_id]["body"]),
                }
                for summary_id in reversed(list(packet["summaries"]))
            ],
        }
        assembled = assemble_bounded_editorial_passes(outputs, packet, assignment)
        self.assertEqual(
            [claim["claim_id"] for claim in packet["claims"]],
            [card["claim_id"] for card in assembled["cards"]],
        )
        self.assertEqual(list(packet["summaries"]), [
            summary["summary_id"] for summary in assembled["summaries"]
        ])
        hydrated = OpenAIBoundedLifecycleProvider._hydrate_cards(assembled, packet)
        report = validate_bounded_final_cards(
            hydrated, self.artifacts.claim_deck, packet
        )
        self.assertEqual("pass", report["status"], report["errors"])

    def test_pass_assignment_and_output_mutations_fail_closed(self) -> None:
        assignment = deepcopy(self.artifacts.split_assignment)
        assignment["card_passes"][1]["ordered_claim_ids"][0] = (
            assignment["card_passes"][0]["ordered_claim_ids"][0]
        )
        assignment["assignment_sha256"] = "0" * 64
        with self.assertRaises(BoundedAuthoringError):
            validate_bounded_split_assignment(assignment, self.artifacts.authoring_packet)

        packets = build_bounded_pass_packets(
            self.artifacts.authoring_packet, self.artifacts.split_assignment
        )
        self.assertEqual(self.artifacts.pass_packets, packets)
        changed = deepcopy(next(iter(packets.values())))
        changed["transport_guess"] = "batch"
        with self.assertRaisesRegex(BoundedAuthoringError, "fields"):
            validate_bounded_pass_packet(
                changed,
                self.artifacts.authoring_packet,
                self.artifacts.split_assignment,
            )
        with self.assertRaisesRegex(BoundedAuthoringError, "inventory"):
            assemble_bounded_editorial_passes(
                {}, self.artifacts.authoring_packet, self.artifacts.split_assignment
            )

    def test_registry_is_selected_subset_and_fully_closed(self) -> None:
        claim_deck = self.artifacts.claim_deck
        full_count = len(
            next(iter(admission().artifacts_by_context.values()))[
                "projected_term_registry"
            ]["terms"]
        )
        used = claim_deck["projected_term_registry"]["terms"]
        self.assertLessEqual(len(used), full_count)
        referenced = {
            ref.rsplit(":", 1)[-1]
            for claim in claim_deck["claims"]
            for ref in claim["authority"]["projected_term_refs"]
        }
        self.assertEqual(referenced, set(used))

    def test_card_and_summary_evidence_are_separate_provenance_scopes(self) -> None:
        provenance = self.artifacts.claim_deck["provenance"]
        self.assertEqual(50, len(provenance["selected_card_evidence"]))
        self.assertEqual(4, len(provenance["summary_whole_dog_evidence"]))
        self.assertTrue(
            all(
                value["scope"] == "claim_local_selected_evidence"
                for value in provenance["selected_card_evidence"].values()
            )
        )
        self.assertTrue(
            all(
                value["scope"] == "summary_whole_dog_selected_basis"
                for value in provenance["summary_whole_dog_evidence"].values()
            )
        )

    def test_fake_author_is_deterministic_and_passes_bounded_final_qa(self) -> None:
        first = fake_author_bounded(self.artifacts.authoring_packet)
        second = fake_author_bounded(self.artifacts.authoring_packet)
        self.assertEqual(first, second)
        self.assertEqual(FINAL_CARDS_CONTRACT, first["schema_version"])
        report = validate_bounded_final_cards(
            first, self.artifacts.claim_deck, self.artifacts.authoring_packet
        )
        self.assertEqual("pass", report["status"], report["errors"])
        self.assertEqual(50, report["claim_count"])
        self.assertEqual(4, report["summary_count"])
        self.assertEqual(0, report["provider_operation_count"])
        self.assertTrue(
            all(
                "invariant relationship" not in card["densities"]["no_astro"]["body"]["handler"].lower()
                for card in first["cards"]
            )
        )

    def test_locked_authority_registry_and_summary_mutations_fail_qa(self) -> None:
        final_cards = fake_author_bounded(self.artifacts.authoring_packet)
        cases = []
        authority = deepcopy(final_cards)
        authority["cards"][0]["invariant_authority"]["classification"] = "variable"
        cases.append(authority)
        registry = deepcopy(final_cards)
        registry["projected_term_registry"]["terms"].pop(next(iter(registry["projected_term_registry"]["terms"])))
        cases.append(registry)
        summary = deepcopy(final_cards)
        summary["summaries"]["summary_1"]["evidence_provenance"]["selected_claim_ids"] = []
        cases.append(summary)
        duplicate = deepcopy(final_cards)
        duplicate["cards"][1]["claim_id"] = duplicate["cards"][0]["claim_id"]
        cases.append(duplicate)
        for value in cases:
            with self.subTest(case=len(value.get("cards", []))):
                report = validate_bounded_final_cards(
                    value, self.artifacts.claim_deck, self.artifacts.authoring_packet
                )
                self.assertEqual("fail", report["status"])

    def test_cross_pass_normalized_repetition_fails_whole_deck_qa(self) -> None:
        final_cards = fake_author_bounded(self.artifacts.authoring_packet)
        assignment = self.artifacts.split_assignment["card_passes"]
        first_id = assignment[0]["ordered_claim_ids"][0]
        second_id = assignment[1]["ordered_claim_ids"][0]
        cards = {card["claim_id"]: card for card in final_cards["cards"]}
        repeated = (
            "This deliberately repeated twelve word passage crosses two isolated "
            "authoring contexts today"
        )
        for claim_id in (first_id, second_id):
            cards[claim_id]["densities"]["no_astro"]["body"]["handler"] = repeated
        report = validate_bounded_final_cards(
            final_cards, self.artifacts.claim_deck,
            self.artifacts.authoring_packet,
        )
        self.assertEqual("fail", report["status"])
        self.assertIn("normalized editorial passage is duplicated", report["errors"])

    def test_missing_registry_term_and_provider_field_injection_fail_closed(self) -> None:
        broken_admission = admission()
        for artifact in broken_admission.artifacts_by_context.values():
            artifact["projected_term_registry"]["terms"].pop("00")
        with self.assertRaises(BoundedAuthoringError) as raised:
            compile_bounded_authoring_artifacts(
                broken_admission, select_bounded_portfolio(portfolio_basis())
            )
        self.assertEqual("bounded_projected_term_missing", raised.exception.code)

        packet = deepcopy(self.artifacts.authoring_packet)
        packet["subject"]["birth_location"] = "hidden"
        with self.assertRaises(BoundedAuthoringError) as raised:
            assert_provider_minimized(packet)
        self.assertEqual("bounded_provider_protected_field", raised.exception.code)

    def test_packaged_schemas_catalog_and_authoring_docs_are_discoverable(self) -> None:
        schemas = {
            "schemas/bounded-natal-claim-deck-v1.schema.json": CLAIM_DECK_CONTRACT,
            "schemas/bounded-natal-authoring-packet-v1.schema.json": AUTHORING_PACKET_CONTRACT,
            "schemas/bounded-natal-disposition-report-v1.schema.json": "astrowoof.bounded_natal.disposition_report.v1",
            "schemas/bounded-natal-cards-v1.schema.json": FINAL_CARDS_CONTRACT,
            "schemas/bounded-natal-delivery-v1.schema.json": "astrowoof.bounded_natal.delivery.v1",
            "schemas/bounded-natal-critic-v1.schema.json": "astrowoof.bounded_natal.critic.v1",
            "schemas/bounded-natal-split-assignment-v1.schema.json": BOUNDED_SPLIT_ASSIGNMENT_CONTRACT,
            "schemas/bounded-natal-authoring-pass-packet-v1.schema.json": BOUNDED_PASS_PACKET_CONTRACT,
        }
        for resource, contract in schemas.items():
            schema = json.loads(read_resource_text(resource))
            self.assertEqual(contract, schema["properties"]["schema_version"]["const"])
        catalog = json.loads(read_resource_text("contracts/contract-catalog.json"))
        self.assertEqual(CLAIM_DECK_CONTRACT, catalog["contracts"]["bounded_natal_claim_deck"])
        self.assertEqual(
            "astrowoof.bounded_natal.delivery_provenance.v1",
            catalog["contracts"]["bounded_natal_delivery_provenance"],
        )
        self.assertEqual(
            BOUNDED_RUN_V2_CONTRACT,
            catalog["contracts"]["bounded_natal_authoring_run"],
        )
        self.assertEqual(
            "astrowoof.bounded_natal.delivery.v1",
            catalog["contracts"]["bounded_natal_delivery"],
        )
        self.assertEqual(
            BOUNDED_SPLIT_ASSIGNMENT_CONTRACT,
            catalog["contracts"]["bounded_natal_split_assignment"],
        )
        self.assertEqual(
            BOUNDED_PASS_PACKET_CONTRACT,
            catalog["contracts"]["bounded_natal_authoring_pass_packet"],
        )
        self.assertIn("representative time", read_resource_text("authoring/Bounded Natal Authoring Brief.md"))
        inventory = read_resource_text("authoring/Bounded Natal Provider Disclosure Inventory.md")
        self.assertIn("initial generation, retries, polish, and critic", inventory)


if __name__ == "__main__":
    unittest.main()
