from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring.provider_economics import (
    project_exact_provider_economics_revision,
    validate_provider_economics_revision_sequence,
)


ACTION = "paid_0123456789abcdef01234567"
H = "a" * 64


def action(*, stage="authoring_initial", service="interactive", state="WAITING", provider_id="resp_1"):
    return {
        "action_id": ACTION,
        "state": state,
        "binding": {
            "run_id": "run-1", "stage": stage,
            "route": "batch-round-001" if service == "batch" else "initial-pass-1",
            "request_sha256": H, "model": "gpt-test", "service_level": service,
            "maximum_output_tokens": 12000, "commitment_micro_usd": 900000,
            "price_book_version": "prices.v1",
        },
        "authorization": {"authorization_reference": "auth-1"},
        "consumption": {"consumer_id": "worker-1"},
        "provider": {"kind": service, "id": provider_id},
        "reported": None,
    }


def native_state(item, *, batch=False):
    provider_id = item.get("provider", {}).get("id") if isinstance(item.get("provider"), dict) else None
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9", "run_id": "run-1",
        "status": "AUTHORING", "updated_at": "2026-08-24T12:00:00Z",
        "authoring_profile": {}, "provider_configuration": {"model": "gpt-test", "reasoning_effort": "medium"},
        "spend_ledger": {"actions": [item]},
        "passes": {"pass-1": {"attempts": [{"state": "WAITING_FOR_RESPONSE", "prompt_sha256": H,
            "provider_metadata": {"response_id": provider_id}}]}},
        "initial_authoring_wave": {"members": [{"action_id": ACTION}]},
    }
    if batch:
        state["authoring_service"] = {"rounds": [{
            "round_number": 1, "round_id": "round-1", "batch_id": item["provider"]["id"],
            "requests": [
                {"custom_id": f"custom-{i}", "pass_id": f"pass-{i}", "attempt_number": 1, "prompt_sha256": f"{i:x}" * 64}
                for i in range(1, 7)
            ],
        }]}
        state["passes"] = {f"pass-{i}": {"attempts": [{"provider_metadata": {
            "custom_id": f"custom-{i}", "response_id": f"resp-{i}", "response_status": "completed",
            "usage": {"input_tokens": 100, "cached_input_tokens": 50, "output_tokens": 20, "reasoning_tokens": 5},
        }}]} for i in range(1, 7)}
    return state


class ExactProjectionTests(unittest.TestCase):
    def test_interactive_pending_settlement_and_unchanged_poll(self):
        item = action()
        state = native_state(item)
        first = project_exact_provider_economics_revision(state, item, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(first["transaction_identity"]["paid_stage"], "authoring_initial")
        self.assertEqual(first["usage_and_cost"]["settlement_disposition"], "provider_pending")
        self.assertIsNone(project_exact_provider_economics_revision(
            state, item, observed_at="2026-08-24T12:01:00Z", previous_revision=first,
        ))

    def test_reported_settlement_mints_monotonic_revision(self):
        item = action()
        state = native_state(item)
        first = project_exact_provider_economics_revision(state, item, observed_at="2026-08-24T12:00:00Z")
        item["state"] = "REPORTED"
        item["reported"] = {"usage": {"input_tokens": 100, "cached_input_tokens": 30, "output_tokens": 20, "reasoning_tokens": 5},
            "estimated_micro_usd": 1234, "price_book_version": "prices.v1"}
        second = project_exact_provider_economics_revision(state, item, observed_at="2026-08-24T12:01:00Z", previous_revision=first)
        self.assertEqual(second["revision_number"], 2)
        self.assertEqual(second["usage_and_cost"]["settlement_disposition"], "provider_usage_reported")
        validate_provider_economics_revision_sequence([first, second])

    def test_all_exact_paid_stages_project(self):
        for stage in ("authoring_initial", "creative_retry", "polish", "qualitative_critic", "qualitative_candidate"):
            with self.subTest(stage=stage):
                item = action(stage=stage)
                value = project_exact_provider_economics_revision(native_state(item), item, observed_at="2026-08-24T12:00:00Z")
                self.assertEqual(value["transaction_identity"]["paid_stage"], stage)

    def test_batch_is_one_round_with_six_audit_members(self):
        item = action(service="batch", state="REPORTED", provider_id="batch-1")
        item["reported"] = {"cost_disposition": "provider_usage_unavailable_billing_reconciliation_pending"}
        value = project_exact_provider_economics_revision(native_state(item, batch=True), item, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(value["transaction_identity"]["cardinality_kind"], "batch_round")
        self.assertEqual(len(value["transaction_identity"]["members"]), 6)
        self.assertEqual(value["usage_and_cost"]["settlement_disposition"], "provider_usage_unavailable_billing_reconciliation_pending")

    def test_no_work_ambiguity_and_binding_refusal(self):
        denied = action(state="DENIED_PROVIDERLESS", provider_id=None)
        denied["provider"] = None
        no_work = project_exact_provider_economics_revision(native_state(denied), denied, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(no_work["usage_and_cost"]["settlement_disposition"], "no_provider_work_consumed")
        ambiguous = action(state="AMBIGUOUS_PROVIDER_SUBMISSION", provider_id=None)
        ambiguous["provider"] = None
        result = project_exact_provider_economics_revision(native_state(ambiguous), ambiguous, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(result["usage_and_cost"]["settlement_disposition"], "submission_ambiguous")
        broken = copy.deepcopy(ambiguous); broken["binding"]["run_id"] = "other"
        with self.assertRaisesRegex(ValueError, "does not join"):
            project_exact_provider_economics_revision(native_state(broken), broken, observed_at="2026-08-24T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
