from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring.provider_economics import (
    project_bounded_provider_economics_revision,
    project_exact_provider_economics_revision,
)
from astrowoof_natal.tests.test_provider_economics_exact_projection import (
    ACTION, action, native_state,
)


def bounded_state(item, *, batch=False):
    state = native_state(item, batch=batch)
    state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v2"
    state["route"] = "bounded_natal"
    if batch:
        state["batch_service"] = state.pop("authoring_service")
    return state


class BoundedProjectionTests(unittest.TestCase):
    def test_bounded_interactive_is_one_transaction_per_pass_attempt(self):
        values = []
        for ordinal in range(1, 7):
            item = action()
            item["action_id"] = f"paid_{ordinal:024x}"
            item["binding"]["route"] = f"bounded_natal:pass-{ordinal}:attempt-001"
            state = bounded_state(item)
            state["spend_ledger"]["actions"] = [item]
            state["passes"] = {f"pass-{ordinal}": state["passes"]["pass-1"]}
            values.append(project_bounded_provider_economics_revision(
                state, item, observed_at="2026-08-24T12:00:00Z",
            ))
        self.assertEqual(len({item["transaction_id"] for item in values}), 6)
        self.assertTrue(all(item["transaction_identity"]["route_family"] == "bounded_natal" for item in values))
        self.assertTrue(all(item["transaction_identity"]["cardinality_kind"] == "single_action" for item in values))

    def test_bounded_batch_is_one_round_not_six_transactions(self):
        item = action(service="batch", state="REPORTED", provider_id="batch-1")
        item["binding"]["route"] = "bounded_natal:batch-round-001"
        item["reported"] = {"cost_disposition": "provider_usage_unavailable_billing_reconciliation_pending"}
        state = bounded_state(item, batch=True)
        value = project_bounded_provider_economics_revision(state, item, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(value["transaction_identity"]["cardinality_kind"], "batch_round")
        self.assertEqual(len(value["transaction_identity"]["members"]), 6)
        self.assertEqual(value["authority_and_commitment"]["commitment_micro_usd"], 900000)

    def test_shared_accounting_semantics_but_route_specific_identity(self):
        item = action()
        exact = project_exact_provider_economics_revision(native_state(item), item, observed_at="2026-08-24T12:00:00Z")
        bounded = project_bounded_provider_economics_revision(bounded_state(copy.deepcopy(item)), item, observed_at="2026-08-24T12:00:00Z")
        self.assertEqual(exact["usage_and_cost"], bounded["usage_and_cost"])
        self.assertNotEqual(exact["cohort_identity"]["cohort_identity_sha256"], bounded["cohort_identity"]["cohort_identity_sha256"])

    def test_legacy_bounded_v1_refuses(self):
        item = action()
        state = bounded_state(item)
        state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v1"
        with self.assertRaisesRegex(ValueError, "bounded v2"):
            project_bounded_provider_economics_revision(state, item, observed_at="2026-08-24T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
