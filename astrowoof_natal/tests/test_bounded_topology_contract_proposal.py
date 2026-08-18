from __future__ import annotations

import hashlib
import json
import unittest
from copy import deepcopy
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:  # Source-only lean environments may omit SPC's dependency.
    Draft202012Validator = None  # type: ignore[assignment,misc]
    ValidationError = Exception  # type: ignore[assignment,misc]


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "sprints" / "2026" / "08" / (
    "20260818-bounded-authoring-topology-transport-parity-sprint2"
) / "fixtures"
PACKAGED_ORACLE = ROOT / "src" / "astrowoof_natal_authoring" / "resources" / (
    "fixtures/lifecycle/route-parity-transition-oracle.v1.json"
)


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
class TestBoundedTopologyContractProposal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load("bounded-authoring-topology.proposal.schema.json")
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_canonical_assignment_and_aggregation_validate(self) -> None:
        self.validator.validate(load("bounded-split-assignment.proposal.json"))
        self.validator.validate(load("bounded-authority-aggregation.proposal.json"))

    def test_assignment_is_exact_complete_and_ordered(self) -> None:
        assignment = load("bounded-split-assignment.proposal.json")
        members = [
            claim_id
            for pass_record in assignment["card_passes"]
            for claim_id in pass_record["ordered_claim_ids"]
        ]
        self.assertEqual(50, len(members))
        self.assertEqual(set(assignment["canonical_claim_ids"]), set(members))
        self.assertEqual(50, len(set(members)))
        self.assertEqual(list(range(1, 6)), [
            item["pass_number"] for item in assignment["card_passes"]
        ])
        self.assertEqual(6, assignment["summary_pass"]["pass_number"])

    def test_unknown_fields_duplicate_claims_and_wrong_cardinality_fail(self) -> None:
        assignment = load("bounded-split-assignment.proposal.json")
        expanded = deepcopy(assignment)
        expanded["transport_guess"] = "batch"
        with self.assertRaises(ValidationError):
            self.validator.validate(expanded)

        duplicate = deepcopy(assignment)
        duplicate["card_passes"][0]["ordered_claim_ids"][0] = (
            duplicate["card_passes"][0]["ordered_claim_ids"][1]
        )
        with self.assertRaises(ValidationError):
            self.validator.validate(duplicate)

        short = deepcopy(assignment)
        short["card_passes"][0]["ordered_claim_ids"].pop()
        with self.assertRaises(ValidationError):
            self.validator.validate(short)

    def test_authority_units_are_closed_and_distinct(self) -> None:
        aggregation = load("bounded-authority-aggregation.proposal.json")
        self.assertEqual("pass_attempt", aggregation["interactive"]["paid_action_unit"])
        self.assertEqual("batch_round", aggregation["batch"]["paid_action_unit"])
        self.assertEqual("batch_round", aggregation["batch"]["api_reservation_unit"])
        self.assertEqual(
            "audit_and_ingestion_only", aggregation["batch"]["member_authority"]
        )
        self.assertEqual([
            "aggregate_maximum_commitment_micro_usd", "member_count",
            "ordered_member_inventory", "settlement_basis",
        ], aggregation["batch"]["round_artifact_fields"])
        changed = deepcopy(aggregation)
        changed["batch"]["api_reservation_unit"] = "batch_member"
        with self.assertRaises(ValidationError):
            self.validator.validate(changed)

    def test_bounded_resource_copies_are_frozen_to_exact_entry_bytes(self) -> None:
        manifest = load("bounded-editorial-resource-parity.proposal.json")
        resources = ROOT / "src" / "astrowoof_natal_authoring" / "resources"
        self.assertEqual("frozen_not_runtime_admitted", manifest["status"])
        for item in manifest["resources"]:
            with self.subTest(role=item["role"]):
                actual = hashlib.sha256(
                    (resources / item["exact_path"]).read_bytes()
                ).hexdigest()
                self.assertEqual(item["exact_sha256"], actual)
                self.assertEqual(
                    item["exact_sha256"], item["bounded_initial_required_sha256"]
                )
                bounded = hashlib.sha256(
                    (resources / item["bounded_admission_path"]).read_bytes()
                ).hexdigest()
                self.assertEqual(item["bounded_initial_required_sha256"], bounded)

    def test_oracle_v1_refusal_is_preserved_and_v2_reuses_vocabulary(self) -> None:
        v1 = json.loads(PACKAGED_ORACLE.read_text(encoding="utf-8"))
        rejected = next(
            item for item in v1["scenarios"] if item["name"] == "bounded_batch_rejected"
        )
        self.assertEqual("unsupported", rejected["cycle_outcome"])
        self.assertFalse(rejected["provider_request_allowed"])

        v2 = load("route-parity-transition-oracle.v2.proposal.json")
        self.assertFalse(v2["public_vocabulary_change"])
        names = {item["name"] for item in v2["scenarios"]}
        self.assertEqual({
            "bounded_batch_awaiting_authorization",
            "bounded_batch_pending",
            "bounded_batch_not_due",
            "bounded_batch_reclaimed",
            "bounded_batch_mixed_member_continuation",
            "bounded_batch_retry_pending",
            "bounded_batch_usage_unavailable",
            "bounded_batch_ambiguous",
            "bounded_batch_provider_failed",
            "bounded_legacy_topology_unsupported",
            "bounded_pre_native_failure",
            "bounded_batch_delivery",
        }, names)
        allowed = {
            "awaiting_external_authority", "detached_provider_pending", "not_due",
            "progressed_local", "ambiguous_submission", "provider_failed",
            "terminal_failure", "delivery_complete",
        }
        self.assertLessEqual(
            {item["cycle_outcome"] for item in v2["scenarios"]}, allowed
        )
        legacy = next(
            item for item in v2["scenarios"]
            if item["name"] == "bounded_legacy_topology_unsupported"
        )
        self.assertEqual("legacy_bounded_topology_unsupported", legacy["reason_code"])
        self.assertEqual(
            "astrowoof.bounded_natal.authoring_run.v1",
            legacy["observed_run_contract"],
        )
        self.assertFalse(legacy["provider_evidence_present"])
        pre_native = next(
            item for item in v2["scenarios"]
            if item["name"] == "bounded_pre_native_failure"
        )
        self.assertEqual("pre_native_failure", pre_native["reason_code"])
        self.assertFalse(pre_native["provider_evidence_present"])


if __name__ == "__main__":
    unittest.main()
