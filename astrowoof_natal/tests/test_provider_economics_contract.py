from __future__ import annotations

import copy
import json
import unittest

from astrowoof_natal_authoring.provider_economics import (
    MAX_RETRIEVAL_REFERENCES,
    PROVIDER_ECONOMICS_FIXTURE_NAMES,
    SCHEMA_VERSION,
    finalize_provider_economics_revision,
    read_provider_economics_schema,
    read_provider_economics_fixture,
    read_provider_economics_mutation_corpus,
    validate_provider_economics_revision,
    validate_provider_economics_revision_sequence,
)

H = "a" * 64
ACTION = "paid_0123456789abcdef01234567"
USAGE = {"input_tokens": 100, "cached_input_tokens": 40, "output_tokens": 20, "reasoning_tokens": 10}


def make_revision(*, batch=False, partial=False):
    members = []
    if batch:
        for ordinal in range(1, 7):
            reported = not (partial and ordinal == 5)
            members.append({
                "member_id": f"member-{ordinal}", "ordinal": ordinal,
                "pass_id": f"pass-{ordinal}", "attempt_number": 1,
                "paid_stage": "authoring_initial", "request_sha256": f"{ordinal:x}" * 64,
                "provider_member_id": f"custom-{ordinal}", "provider_status": "completed",
                "usage_disposition": "reported" if reported else "unavailable",
                "usage": copy.deepcopy(USAGE) if reported else None,
                "provider_reported_micro_usd": None,
            })
    settlement = "provider_usage_unavailable_billing_reconciliation_pending" if partial else "provider_usage_reported"
    value = {
        "schema_version": SCHEMA_VERSION, "transaction_id": "pending",
        "native_run_id": "native-run-1", "native_action_id": ACTION,
        "revision_number": 1, "previous_revision_id": None, "revision_id": "pending",
        "observed_at": "2026-08-24T12:00:00Z",
        "transaction_identity": {
            "route_family": "bounded_natal" if batch else "exact_natal",
            "paid_stage": "authoring_initial", "provider_mechanism": "batch" if batch else "response",
            "native_operation_ref": "round-1" if batch else "pass-1-attempt-1",
            "pass_id": None if batch else "pass-1", "attempt_number": 1,
            "round_id": "round-1" if batch else None,
            "cardinality_kind": "batch_round" if batch else "single_action", "members": members,
        },
        "cohort_identity": {
            "cohort_completeness": "complete", "sbe_release": "0.4.19",
            "route_contract": "route.v1", "generation_profile_id": "profile-1",
            "profile_manifest_sha256": H, "resource_bundle_sha256": H,
            "request_geometry_version": "geometry.v1", "request_geometry_sha256": H,
            "execution_topology_version": "six-pass-wave.v1", "execution_topology_sha256": H,
            "model": "gpt-test", "reasoning_effort": "medium", "service_level": "default",
            "maximum_output_tokens": 12000, "price_book_version": "prices.v1",
            "cohort_identity_sha256": "pending",
        },
        "authority_and_commitment": {"commitment_micro_usd": 1000000, "authorization_reference": "auth-1", "consumption_reference": "consume-1"},
        "provider_operation": {"provider": "openai", "operation_kind": "batch" if batch else "response", "operation_id": "batch-1" if batch else "resp-1", "status": "completed"},
        "usage_and_cost": {
            "settlement_disposition": settlement, "usage": None if partial else copy.deepcopy(USAGE),
            "sbe_estimated_micro_usd": None if partial else 1234,
            "sbe_estimate_price_book_version": None if partial else "prices.v1",
            "provider_reported_micro_usd": None,
        },
        "timing": {
            "prepared_at": "2026-08-24T11:58:00Z", "authorized_at": "2026-08-24T11:58:01Z",
            "submission_intent_at": "2026-08-24T11:58:02Z", "provider_identity_durable_at": "2026-08-24T11:58:03Z",
            "provider_terminal_observed_at": "2026-08-24T12:00:00Z", "reconciliation_completed_at": "2026-08-24T12:00:01Z",
            "native_settled_at": "2026-08-24T12:00:01Z", "create_http_duration_ms": 500,
            "observed_provider_pending_ms": 117000, "native_action_span_ms": 121000,
            "provider_reported_duration_ms": None, "retrieval_attempt_count": 1,
            "first_retrieval_observed_at": "2026-08-24T12:00:00Z", "last_retrieval_observed_at": "2026-08-24T12:00:00Z",
            "retrieval_http_duration_total_ms": 120, "retrieval_attempt_refs": ["diag/1.json"],
            "retrieval_attempt_ref_overflow_count": 0,
        },
        "editorial_outcome": {"status": "not_yet_evaluated", "retry_reason_category": None},
        "native_outcome": {"status": "in_progress", "delivery_publishable": False},
        "provenance": {
            "action_binding_sha256": H, "request_sha256": H, "native_result_id": None,
            "native_result_sha256": None, "journal_range_sha256": H, "snapshot_sha256": H,
            "publication_receipt_id": None, "publication_receipt_sha256": None,
            "usage_evidence_ref": "ledger:reported-usage", "batch_round_manifest_sha256": H if batch else None,
            "api_reconciliation_join": {"native_run_id": "native-run-1", "native_action_id": ACTION},
        },
    }
    return finalize_provider_economics_revision(value)


def revise(previous, **sections):
    value = copy.deepcopy(previous)
    value["revision_number"] += 1
    value["previous_revision_id"] = previous["revision_id"]
    value["observed_at"] = "2026-08-24T12:00:10Z"
    for section, changes in sections.items():
        value[section].update(changes)
    value["revision_id"] = "pending"
    return finalize_provider_economics_revision(value)


class ProviderEconomicsContractTests(unittest.TestCase):
    def test_packaged_positive_fixtures_and_sequences(self):
        loaded = {name: read_provider_economics_fixture(name) for name in PROVIDER_ECONOMICS_FIXTURE_NAMES}
        self.assertEqual(set(loaded), PROVIDER_ECONOMICS_FIXTURE_NAMES)
        validate_provider_economics_revision_sequence([
            loaded["interactive-settlement.v1.json"],
            loaded["interactive-editorial-finalization.v1.json"],
            loaded["interactive-native-finalization.v1.json"],
        ])
        self.assertEqual(
            loaded["batch-partial-usage.v1.json"]["usage_and_cost"]["settlement_disposition"],
            "provider_usage_unavailable_billing_reconciliation_pending",
        )

    def test_packaged_mutation_corpus_refuses(self):
        corpus = read_provider_economics_mutation_corpus()
        for mutation in corpus["mutations"]:
            with self.subTest(mutation=mutation["id"]):
                value = copy.deepcopy(read_provider_economics_fixture(mutation["fixture"]))
                target = value
                parts = mutation["path"].strip("/").split("/")
                for part in parts[:-1]:
                    target = target[int(part)] if isinstance(target, list) else target[part]
                leaf = parts[-1]
                if isinstance(target, list):
                    target[int(leaf)] = mutation["value"]
                else:
                    target[leaf] = mutation["value"]
                with self.assertRaisesRegex(ValueError, mutation["expected_error"]):
                    validate_provider_economics_revision(value)

    def test_fixture_reader_is_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            read_provider_economics_fixture("../../run.json")

    def test_schema_and_python_validation(self):
        schema = read_provider_economics_schema()
        self.assertFalse(schema["additionalProperties"])
        value = make_revision()
        self.assertEqual(validate_provider_economics_revision(value), value)
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema optional")
        jsonschema.Draft202012Validator(schema).validate(value)

    def test_settlement_editorial_and_native_revisions(self):
        first = make_revision()
        second = revise(first, editorial_outcome={"status": "accepted", "retry_reason_category": None})
        third = revise(second, native_outcome={"status": "delivery_complete", "delivery_publishable": True})
        self.assertEqual(len(validate_provider_economics_revision_sequence([first, second, third])), 3)

    def test_pending_revision_may_gain_settlement_and_cumulative_time(self):
        settled = make_revision()
        pending = copy.deepcopy(settled)
        pending["provider_operation"]["status"] = "pending"
        pending["usage_and_cost"].update({"settlement_disposition": "provider_pending", "usage": None, "sbe_estimated_micro_usd": None, "sbe_estimate_price_book_version": None})
        pending["timing"].update({
            "provider_terminal_observed_at": None, "reconciliation_completed_at": None,
            "native_settled_at": None, "observed_provider_pending_ms": 10000,
            "native_action_span_ms": 12000,
        })
        pending["revision_id"] = "pending"
        pending = finalize_provider_economics_revision(pending)
        settled["revision_number"] = 2
        settled["previous_revision_id"] = pending["revision_id"]
        settled["observed_at"] = "2026-08-24T12:00:10Z"
        settled["revision_id"] = "pending"
        settled = finalize_provider_economics_revision(settled)
        validate_provider_economics_revision_sequence([pending, settled])

    def test_replay_gap_and_contradiction(self):
        first = make_revision()
        self.assertEqual(validate_provider_economics_revision(first), validate_provider_economics_revision(copy.deepcopy(first)))
        later = revise(first, editorial_outcome={"status": "accepted", "retry_reason_category": None})
        gap = copy.deepcopy(later); gap["revision_number"] = 3; gap["revision_id"] = "pending"; gap = finalize_provider_economics_revision(gap)
        with self.assertRaisesRegex(ValueError, "predecessor gap"):
            validate_provider_economics_revision_sequence([first, gap])
        contradiction = copy.deepcopy(later); contradiction["usage_and_cost"]["usage"]["output_tokens"] += 1; contradiction["revision_id"] = "pending"; contradiction = finalize_provider_economics_revision(contradiction)
        with self.assertRaisesRegex(ValueError, "contradicted"):
            validate_provider_economics_revision_sequence([first, contradiction])

    def test_partial_batch_usage_and_no_invented_allocation(self):
        value = make_revision(batch=True, partial=True)
        self.assertIsNone(value["transaction_identity"]["members"][4]["usage"])
        value["transaction_identity"]["members"][4]["provider_reported_micro_usd"] = 1
        value["revision_id"] = "pending"
        with self.assertRaisesRegex(ValueError, "allocation is forbidden"):
            finalize_provider_economics_revision(value)

    def test_partial_batch_cannot_claim_reported_round(self):
        value = make_revision(batch=True, partial=True)
        value["usage_and_cost"] = {"settlement_disposition": "provider_usage_reported", "usage": copy.deepcopy(USAGE), "sbe_estimated_micro_usd": 1, "sbe_estimate_price_book_version": "prices.v1", "provider_reported_micro_usd": None}
        value["revision_id"] = "pending"
        with self.assertRaisesRegex(ValueError, "partial Batch"):
            finalize_provider_economics_revision(value)

    def test_retrieval_overflow_is_explicit(self):
        value = make_revision()
        value["timing"].update({"retrieval_attempt_count": MAX_RETRIEVAL_REFERENCES + 2, "retrieval_attempt_refs": [f"diag/{i}.json" for i in range(MAX_RETRIEVAL_REFERENCES)], "retrieval_attempt_ref_overflow_count": 2})
        value["revision_id"] = "pending"
        finalize_provider_economics_revision(value)
        value["timing"]["retrieval_attempt_ref_overflow_count"] = 1; value["revision_id"] = "pending"
        with self.assertRaisesRegex(ValueError, "count must equal"):
            finalize_provider_economics_revision(value)

    def test_topology_changes_cohort_digest_and_sentinel_absent(self):
        first = make_revision()
        changed = copy.deepcopy(first); changed["cohort_identity"]["execution_topology_version"] = "serial.v1"; changed["revision_id"] = "pending"; changed = finalize_provider_economics_revision(changed)
        self.assertNotEqual(first["cohort_identity"]["cohort_identity_sha256"], changed["cohort_identity"]["cohort_identity_sha256"])
        self.assertNotIn("PROTECTED_BIRTH_LOCATION_SENTINEL", json.dumps(first, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
