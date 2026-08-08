from __future__ import annotations

import sys
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.spend import (  # noqa: E402
    AUTHORIZATION_SCHEMA,
    PRICE_BOOK_VERSION,
    AmbiguousProviderSubmission,
    BudgetExhausted,
    action_binding,
    append_reconciliation_reference,
    authorize_action,
    begin_submission,
    conservative_commitment_micros,
    mark_ambiguous,
    new_ledger,
    prepare_action,
    record_provider_id,
)
from astrowoof_natal_authoring.closure import (  # noqa: E402
    OpenAIResponsesProvider,
    OpenAIServiceError,
    SpendController,
    load_json,
    save_state,
)


def policy(*, run=10_000_000, initial=10_000_000, optional="skip"):
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": run,
        "stage_ceilings_micro_usd": {
            "authoring_initial": initial,
            "creative_retry": 10_000_000,
            "polish": 10_000_000,
            "qualitative_critic": 10_000_000,
            "qualitative_candidate": 10_000_000,
        },
        "optional_stage_budget_behavior": {
            "polish": optional,
            "qualitative_critic": optional,
            "qualitative_candidate": optional,
        },
    }


def binding(*, stage="authoring_initial", commitment=1000, revision=7):
    return action_binding(
        run_id="run-1",
        profile_sha256="a" * 64,
        prepared_state_revision=revision,
        stage=stage,
        route="bre_1:attempt-001",
        request_sha256="b" * 64,
        model="gpt-5.6-luna",
        service_level="interactive",
        maximum_output_tokens=1000,
        commitment_micro_usd=commitment,
        price_book_version=PRICE_BOOK_VERSION,
    )


def authorization(action):
    return {
        "schema_version": AUTHORIZATION_SCHEMA,
        "action_id": action["action_id"],
        "binding": action["binding"],
        "authorization_reference": "api-reservation-1",
    }


class SpendLedgerTests(unittest.TestCase):
    def test_authorization_is_bound_to_exact_request_and_revision(self):
        ledger = new_ledger(policy())
        action = prepare_action(ledger, binding())
        altered = authorization(action)
        altered["binding"] = {**altered["binding"], "prepared_state_revision": 8}
        with self.assertRaisesRegex(ValueError, "exactly match"):
            authorize_action(ledger, altered)
        self.assertEqual("PREPARED", action["state"])

    def test_hard_exhaustion_and_optional_skip_are_distinct(self):
        hard_ledger = new_ledger(policy(run=100, initial=100))
        hard = prepare_action(hard_ledger, binding(commitment=101))
        with self.assertRaises(BudgetExhausted):
            authorize_action(hard_ledger, authorization(hard))
        self.assertEqual("BUDGET_EXHAUSTED", hard["state"])

        skip_ledger = new_ledger(policy(run=100, optional="skip"))
        skipped = prepare_action(
            skip_ledger, binding(stage="qualitative_critic", commitment=101)
        )
        authorize_action(skip_ledger, authorization(skipped))
        self.assertEqual("SKIPPED_BUDGET_EXHAUSTED", skipped["state"])

    def test_authorization_is_consumed_once(self):
        ledger = new_ledger(policy())
        action = prepare_action(ledger, binding())
        authorize_action(ledger, authorization(action))
        begin_submission(action, consumer_id="worker-1", state_revision=8)
        with self.assertRaisesRegex(Exception, "not authorized"):
            begin_submission(action, consumer_id="worker-2", state_revision=8)

    def test_missing_provider_id_becomes_ambiguous(self):
        ledger = new_ledger(policy())
        action = prepare_action(ledger, binding())
        authorize_action(ledger, authorization(action))
        begin_submission(action, consumer_id="worker-1", state_revision=8)
        with self.assertRaises(AmbiguousProviderSubmission):
            record_provider_id(action, provider_id="", kind="response")
        self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", action["state"])

    def test_reconciliation_references_are_append_only(self):
        ledger = new_ledger(policy())
        action = prepare_action(ledger, binding())
        append_reconciliation_reference(
            ledger,
            action_id=action["action_id"],
            reference_id="billing-line-1",
            authority="astrowoof-api",
            amount_micro_usd=812,
        )
        with self.assertRaisesRegex(ValueError, "already exists"):
            append_reconciliation_reference(
                ledger,
                action_id=action["action_id"],
                reference_id="billing-line-1",
                authority="astrowoof-api",
            )

    def test_commitment_uses_uncached_input_and_maximum_output(self):
        amount = conservative_commitment_micros(
            model="gpt-5.6-luna",
            input_tokens=1000,
            maximum_output_tokens=2000,
            service_level="interactive",
        )
        self.assertEqual(13_000, amount)

    def test_prepare_authorize_execute_persists_each_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_json = Path(temporary) / "run.json"
            state = {
                "schema_version": "astrowoof.semantic_closure_run.v0.8",
                "state_revision": 0,
                "run_id": "run-1",
                "status": "AUTHORING",
                "created_at": "2026-08-07T00:00:00Z",
                "passes": {},
                "subjects": {},
                "authoring_profile": {"spend_policy": policy()},
                "spend_ledger": new_ledger(policy()),
            }
            save_state(run_json, state)
            controller = SpendController(
                state=state,
                run_json=run_json,
                state_lock=threading.Lock(),
                consumer_id="worker-1",
            )
            before, created = controller.callbacks(
                stage="authoring_initial",
                route="bre_1:attempt-001",
                model="gpt-5.6-luna",
                service_level="interactive",
                maximum_output_tokens=1000,
            )
            request = {"model": "gpt-5.6-luna", "input": "exact request"}
            with self.assertRaisesRegex(Exception, "authorization"):
                before(request)
            prepared = state["spend_ledger"]["actions"][0]
            self.assertEqual(
                "PREPARED",
                load_json(run_json)["spend_ledger"]["actions"][0]["state"],
            )
            authorize_action(state["spend_ledger"], authorization(prepared))
            save_state(run_json, state)
            before(request)
            self.assertEqual(
                "SUBMITTING",
                load_json(run_json)["spend_ledger"]["actions"][0]["state"],
            )
            created("resp_123", "response")
            persisted = load_json(run_json)["spend_ledger"]["actions"][0]
            self.assertEqual("PROVIDER_ID_RECORDED", persisted["state"])
            self.assertEqual("resp_123", persisted["provider"]["id"])

    def test_restart_after_submitting_without_provider_id_fails_ambiguous(self):
        ledger = new_ledger(policy())
        action = prepare_action(ledger, binding())
        authorize_action(ledger, authorization(action))
        begin_submission(action, consumer_id="dead-worker", state_revision=8)
        mark_ambiguous(action, reason="process died before provider ID persistence")
        self.assertEqual("AMBIGUOUS_PROVIDER_SUBMISSION", action["state"])

    def test_strict_provider_cannot_create_without_spend_callback(self):
        class NoCalls:
            def request_json(self, **kwargs):
                raise AssertionError("provider must not be contacted")

        provider = OpenAIResponsesProvider(
            api_key="test",
            transport=NoCalls(),
            require_spend_authorization=True,
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "spend authorization"):
                provider.complete_json(
                    system="system",
                    user="user",
                    schema={"type": "object", "additionalProperties": False},
                    schema_name="test",
                    attempt_root=Path(temporary),
                    idempotency_material="test",
                )

    def test_strict_provider_does_not_retry_ambiguous_post(self):
        class FailingTransport:
            calls = 0

            def request_json(self, **kwargs):
                self.calls += 1
                raise OpenAIServiceError(
                    "timeout after submission",
                    status_code=503,
                    retryable=True,
                )

        transport = FailingTransport()
        provider = OpenAIResponsesProvider(
            api_key="test",
            transport=transport,
            require_spend_authorization=True,
            max_transport_retries=4,
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(OpenAIServiceError):
                provider.complete_json(
                    system="system",
                    user="user",
                    schema={"type": "object", "additionalProperties": False},
                    schema_name="test",
                    attempt_root=Path(temporary),
                    idempotency_material="test",
                    before_submit=lambda payload: None,
                )
        self.assertEqual(1, transport.calls)


if __name__ == "__main__":
    unittest.main()
