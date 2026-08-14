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
    CLAIM_DECK_CONTRACT,
    FINAL_CARDS_CONTRACT,
    BoundedAuthoringError,
    assert_provider_minimized,
    compile_bounded_authoring_artifacts,
    fake_author_bounded,
    validate_bounded_authoring_packet,
    validate_bounded_claim_deck,
    validate_bounded_final_cards,
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
        self.assertIn("representative time", read_resource_text("authoring/Bounded Natal Authoring Brief.md"))
        inventory = read_resource_text("authoring/Bounded Natal Provider Disclosure Inventory.md")
        self.assertIn("initial generation, retries, polish, and critic", inventory)


if __name__ == "__main__":
    unittest.main()
