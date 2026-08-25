from __future__ import annotations

import copy
import json
from pathlib import Path

from astrowoof_natal.tests.test_provider_economics_contract import make_revision, revise
from astrowoof_natal_authoring.provider_economics import finalize_provider_economics_revision


ROOT = Path(__file__).resolve().parents[7]
TARGET = ROOT / "astrowoof_natal" / "src" / "astrowoof_natal_authoring" / "resources" / "fixtures" / "provider-economics"


def finalize_changed(value: dict) -> dict:
    value["revision_id"] = "pending"
    return finalize_provider_economics_revision(value)


def write(name: str, value: dict) -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    (TARGET / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


settlement = make_revision()
editorial = revise(settlement, editorial_outcome={"status": "accepted", "retry_reason_category": None})
native = revise(editorial, native_outcome={"status": "delivery_complete", "delivery_publishable": True})
batch = make_revision(batch=True, partial=True)

providerless = copy.deepcopy(settlement)
providerless["provider_operation"].update({"operation_id": None, "status": "not_created"})
providerless["usage_and_cost"].update({
    "settlement_disposition": "no_provider_work_consumed", "usage": None,
    "sbe_estimated_micro_usd": None, "sbe_estimate_price_book_version": None,
})
for key in (
    "provider_identity_durable_at", "provider_terminal_observed_at",
    "reconciliation_completed_at", "native_settled_at", "create_http_duration_ms",
    "observed_provider_pending_ms", "native_action_span_ms",
    "first_retrieval_observed_at", "last_retrieval_observed_at",
    "retrieval_http_duration_total_ms",
):
    providerless["timing"][key] = None
providerless["timing"].update({"retrieval_attempt_count": 0, "retrieval_attempt_refs": [], "retrieval_attempt_ref_overflow_count": 0})
providerless["provenance"]["usage_evidence_ref"] = None
providerless = finalize_changed(providerless)

ambiguous = copy.deepcopy(providerless)
ambiguous["provider_operation"]["status"] = "ambiguous"
ambiguous["usage_and_cost"]["settlement_disposition"] = "submission_ambiguous"
ambiguous = finalize_changed(ambiguous)

legacy = copy.deepcopy(settlement)
legacy["cohort_identity"].update({
    "cohort_completeness": "legacy_unknown", "generation_profile_id": None,
    "profile_manifest_sha256": None, "resource_bundle_sha256": None,
    "request_geometry_sha256": None, "execution_topology_sha256": None,
})
legacy = finalize_changed(legacy)

write("interactive-settlement.v1.json", settlement)
write("interactive-editorial-finalization.v1.json", editorial)
write("interactive-native-finalization.v1.json", native)
write("batch-partial-usage.v1.json", batch)
write("providerless-no-work.v1.json", providerless)
write("ambiguous-submission.v1.json", ambiguous)
write("legacy-unknown.v1.json", legacy)

corpus = {
    "schema_version": "astrowoof.provider_economics_mutation_corpus.v1",
    "mutations": [
        {"id": "unknown_top_level", "fixture": "interactive-settlement.v1.json", "path": "/birth_datetime", "value": "PROTECTED_BIRTH_LOCATION_SENTINEL", "expected_error": "exact keys"},
        {"id": "action_identity", "fixture": "interactive-settlement.v1.json", "path": "/native_action_id", "value": "paid_ffffffffffffffffffffffff", "expected_error": "transaction_id"},
        {"id": "cohort_digest", "fixture": "interactive-settlement.v1.json", "path": "/cohort_identity/execution_topology_version", "value": "serial.v1", "expected_error": "cohort_identity_sha256"},
        {"id": "batch_member_allocation", "fixture": "batch-partial-usage.v1.json", "path": "/transaction_identity/members/4/provider_reported_micro_usd", "value": 1, "expected_error": "allocation is forbidden"},
        {"id": "batch_false_settlement", "fixture": "batch-partial-usage.v1.json", "path": "/usage_and_cost/settlement_disposition", "value": "provider_usage_reported", "expected_error": "requires usage"},
        {"id": "retrieval_overflow", "fixture": "interactive-settlement.v1.json", "path": "/timing/retrieval_attempt_ref_overflow_count", "value": 1, "expected_error": "count must equal"},
        {"id": "noncanonical_observation_time", "fixture": "interactive-settlement.v1.json", "path": "/observed_at", "value": "2026-08-24T12:00:00+00:00", "expected_error": "canonical UTC"}
    ]
}
write("mutation-corpus.v1.json", corpus)
