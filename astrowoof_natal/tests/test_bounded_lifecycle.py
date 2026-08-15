from __future__ import annotations

import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_authoring import (  # noqa: E402
    assert_provider_minimized,
    fake_author_bounded,
)
from astrowoof_natal_authoring.bounded_lifecycle import (  # noqa: E402
    BOUNDED_DELIVERY_CONTRACT,
    FakeBoundedLifecycleProvider,
    create_bounded_run,
    resume_bounded_run,
    run_bounded_authoring,
)
from astrowoof_natal_authoring.closure import (  # noqa: E402
    load_json,
    validate_workspace_snapshot,
)
from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    ExecutionEventEmitter,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    closeout_run,
    deny_providerless_action,
    inspect_lifecycle,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.spend import (  # noqa: E402
    AUTHORIZATION_SCHEMA,
    PRICE_BOOK_VERSION,
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
)
from test_bounded_authoring import compiled  # noqa: E402


def spend_policy() -> dict:
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": 5_000_000,
        "stage_ceilings_micro_usd": {
            "authoring_initial": 1_000_000,
            "creative_retry": 1_000_000,
            "polish": 1_000_000,
            "qualitative_critic": 1_000_000,
            "qualitative_candidate": 1_000_000,
        },
        "optional_stage_budget_behavior": {
            "polish": "skip",
            "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


class PaidScriptedProvider:
    name = "openai"
    model = "gpt-5.6-luna"
    service_level = "interactive"
    maximum_output_tokens = 1_000
    paid = True

    def __init__(self, *, interrupt_after_identity: bool = False) -> None:
        self.submissions = 0
        self.polls = 0
        self.interrupt_after_identity = interrupt_after_identity

    @staticmethod
    def metadata(response_id: str) -> dict:
        return {
            "provider": "openai", "model": "gpt-5.6-luna",
            "response_id": response_id, "duration_ms": 1,
            "usage": {"input_tokens": 10, "output_tokens": 10},
            "estimated_cost": {"currency": "USD", "estimated_amount": 0.001},
        }

    def execute(self, *, stage, route, payload, before_submit, provider_created):
        assert_provider_minimized(payload)
        before_submit(payload)
        self.submissions += 1
        response_id = f"resp-bounded-{self.submissions}"
        provider_created(response_id, "response")
        if self.interrupt_after_identity:
            self.interrupt_after_identity = False
            raise RuntimeError("injected worker interruption")
        return fake_author_bounded(payload["authoring_packet"]), self.metadata(response_id)

    def resume(self, *, stage, route, provider_operation_id, payload):
        self.polls += 1
        return fake_author_bounded(payload["authoring_packet"]), self.metadata(provider_operation_id)


class RetryFakeProvider(FakeBoundedLifecycleProvider):
    def execute(self, **kwargs):
        result, metadata = super().execute(**kwargs)
        if kwargs["stage"] == "authoring_initial":
            result = deepcopy(result)
            result["cards"][0]["priority_id"] = "drifted"
        return result, metadata


class TestBoundedLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = compiled()

    def test_fake_route_completes_shared_lifecycle_and_closeout(self) -> None:
        events = []
        emitter = ExecutionEventEmitter(release="test", sink=events.append)
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            state = run_bounded_authoring(
                run_dir, self.artifacts,
                generation_profile={"optional_stages": {
                    "polish": True, "qualitative_critic": True,
                    "qualitative_candidate": True,
                }},
                event_emitter=emitter,
            )
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            validate_workspace_snapshot(run_dir, state)
            delivery = load_json(run_dir / "bounded/final/delivery.json")
            self.assertEqual(BOUNDED_DELIVERY_CONTRACT, delivery["schema_version"])
            self.assertEqual(50, len(load_json(run_dir / "bounded/final/cards.json")["cards"]))
            inspection = inspect_lifecycle(run_dir, native_exclusive_access="declared")
            self.assertEqual("delivery_complete", inspection["terminal"]["outcome"])
            first_closeout = closeout_run(run_dir)
            second_closeout = closeout_run(run_dir)
            self.assertEqual("closed", first_closeout["disposition"])
            self.assertEqual(
                first_closeout["semantic_result_sha256"],
                second_closeout["semantic_result_sha256"],
            )
            names = {event["event_name"] for event in events}
            self.assertTrue({
                "bounded.admission.completed", "bounded.family.validated",
                "bounded.selection.completed", "bounded.disposition.completed",
                "bounded.artifact.committed", "terminal.transitioned",
            } <= names)

    def test_snapshot_rejects_mutation_and_wrong_restore_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "run"
            state = run_bounded_authoring(run_dir, self.artifacts)
            cards = run_dir / "bounded/final/cards.json"
            cards.write_text(cards.read_text(encoding="utf-8") + " ", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                resume_bounded_run(run_dir)
            with self.assertRaisesRegex(ValueError, "original logical absolute path"):
                validate_workspace_snapshot(root / "different", state)

    def test_event_sink_failure_is_non_authoritative(self) -> None:
        emitter = ExecutionEventEmitter(
            release="test", sink=lambda _: (_ for _ in ()).throw(OSError("sink down"))
        )
        with tempfile.TemporaryDirectory() as temporary:
            state = run_bounded_authoring(
                Path(temporary) / "run", self.artifacts, event_emitter=emitter
            )
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertGreater(emitter.stats.sink_warnings, 0)

    def test_creative_retry_is_separate_and_accepts_only_valid_result(self) -> None:
        provider = RetryFakeProvider()
        with tempfile.TemporaryDirectory() as temporary:
            state = run_bounded_authoring(
                Path(temporary) / "run", self.artifacts, provider=provider,
                generation_profile={
                    "max_attempts": 2,
                    "optional_stages": {
                        "polish": False, "qualitative_critic": False,
                        "qualitative_candidate": False,
                    },
                },
            )
            record = next(iter(state["passes"].values()))
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertEqual(2, record["accepted_attempt"])
            self.assertEqual(
                ["PASS_QA_REJECTED", "PASS_QA_ACCEPTED"],
                [attempt["state"] for attempt in record["attempts"]],
            )
            self.assertIn("creative_retry", state["bounded"]["completed_stages"])

    def test_every_bounded_persistence_boundary_resumes_monotonically(self) -> None:
        points = (
            "after_authoring_provider_result",
            "after_authoring_checkpoint",
            "after_polish_provider_result",
            "after_polish_checkpoint",
            "after_qualitative_critic_provider_result",
            "after_qualitative_critic_checkpoint",
            "after_qualitative_candidate_provider_result",
            "after_qualitative_candidate_checkpoint",
            "after_delivery_checkpoint",
        )
        for point in points:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temporary:
                run_dir = Path(temporary) / "run"
                create_bounded_run(run_dir, self.artifacts)
                fired = False

                def inject(actual: str) -> None:
                    nonlocal fired
                    if actual == point and not fired:
                        fired = True
                        raise RuntimeError(f"injected:{point}")

                with self.assertRaisesRegex(RuntimeError, point):
                    resume_bounded_run(run_dir, _failure_injector=inject)
                interrupted = load_json(run_dir / "run.json")
                revision = interrupted["state_revision"]
                validate_workspace_snapshot(run_dir, interrupted)
                final = resume_bounded_run(run_dir)
                self.assertTrue(fired)
                self.assertEqual("DELIVERY_COMPLETE", final["status"])
                self.assertGreaterEqual(final["state_revision"], revision)
                self.assertEqual(
                    50, len(load_json(run_dir / "bounded/final/cards.json")["cards"])
                )

    def test_paid_authorization_binds_request_and_is_consumed_once(self) -> None:
        provider = PaidScriptedProvider()
        profile = {
            "optional_stages": {stage: False for stage in (
                "polish", "qualitative_critic", "qualitative_candidate"
            )},
            "spend_policy": spend_policy(),
        }
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            create_bounded_run(run_dir, self.artifacts, provider=provider, generation_profile=profile)
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            paused = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, paused)
            action = paused["spend_ledger"]["actions"][0]
            authorization = {
                "schema_version": AUTHORIZATION_SCHEMA,
                "action_id": action["action_id"],
                "binding": deepcopy(action["binding"]),
                "authorization_reference": "api-reservation-bounded-1",
            }
            state = resume_bounded_run(
                run_dir, provider=provider, authorizations=[authorization]
            )
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertEqual(1, provider.submissions)
            self.assertEqual("REPORTED", state["spend_ledger"]["actions"][0]["state"])

    def test_prepared_bounded_action_supports_providerless_denial_and_replay(self) -> None:
        provider = PaidScriptedProvider()
        profile = {
            "optional_stages": {stage: False for stage in (
                "polish", "qualitative_critic", "qualitative_candidate"
            )},
            "spend_policy": spend_policy(),
        }
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile=profile,
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            state = load_json(run_dir / "run.json")
            action = state["spend_ledger"]["actions"][0]
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared"
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"],
                "action_id": action["action_id"],
                "binding": action["binding"],
                "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:bounded-test",
            }
            first = deny_providerless_action(run_dir, request)
            second = deny_providerless_action(run_dir, request)
            self.assertEqual("DENIED_PROVIDERLESS", first["disposition"])
            self.assertEqual("idempotent_replay", second["outcome"])
            self.assertEqual(0, provider.submissions)
            validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))
            after = inspect_lifecycle(
                run_dir, native_exclusive_access="declared"
            )
            self.assertFalse(after["terminal"]["provider_continuation_remains"])
            self.assertFalse(after["terminal"]["local_continuation_remains"])
            self.assertEqual("budget_exhausted", after["terminal"]["outcome"])
            self.assertEqual("closed", closeout_run(run_dir)["disposition"])
            resumed = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("BUDGET_EXHAUSTED", resumed["status"])
            self.assertEqual(0, provider.submissions)

    def test_optional_providerless_denial_skips_and_delivers_without_resubmit(self) -> None:
        provider = PaidScriptedProvider()
        profile = {
            "optional_stages": {
                "polish": True,
                "qualitative_critic": False,
                "qualitative_candidate": False,
            },
            "spend_policy": spend_policy(),
        }
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile=profile,
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            initial = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0]
            authorization = {
                "schema_version": AUTHORIZATION_SCHEMA,
                "action_id": initial["action_id"],
                "binding": initial["binding"],
                "authorization_reference": "api-reservation-initial",
            }
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(
                    run_dir, provider=provider, authorizations=[authorization]
                )
            paused = load_json(run_dir / "run.json")
            polish = next(
                item for item in paused["spend_ledger"]["actions"]
                if item["binding"]["stage"] == "polish"
            )
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared"
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": paused["run_id"],
                "action_id": polish["action_id"],
                "binding": polish["binding"],
                "observed": inspection["observation"],
                "denial_reason": "external_authority_denied",
                "external_authority_reference": "api-global:optional-polish",
            }
            denied = deny_providerless_action(run_dir, request)
            self.assertEqual("optional_stage_skipped", denied["run_transition"]["outcome"])
            self.assertEqual([], denied["run_transition"]["required_action_ids"])
            completed = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", completed["status"])
            self.assertIn("polish", completed["bounded"]["skipped_stages"])
            self.assertEqual(1, provider.submissions)

    def test_interrupted_submission_reconciles_durable_id_without_resubmit(self) -> None:
        provider = PaidScriptedProvider(interrupt_after_identity=True)
        profile = {
            "optional_stages": {stage: False for stage in (
                "polish", "qualitative_critic", "qualitative_candidate"
            )},
            "spend_policy": spend_policy(),
        }
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            create_bounded_run(run_dir, self.artifacts, provider=provider, generation_profile=profile)
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            paused = load_json(run_dir / "run.json")
            action = paused["spend_ledger"]["actions"][0]
            authorization = {
                "schema_version": AUTHORIZATION_SCHEMA, "action_id": action["action_id"],
                "binding": action["binding"], "authorization_reference": "api-reservation-2",
            }
            with self.assertRaisesRegex(RuntimeError, "injected"):
                resume_bounded_run(run_dir, provider=provider, authorizations=[authorization])
            interrupted = load_json(run_dir / "run.json")
            validate_workspace_snapshot(run_dir, interrupted)
            self.assertEqual("PROVIDER_ID_RECORDED", interrupted["spend_ledger"]["actions"][0]["state"])
            final = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(1, provider.submissions)
            self.assertEqual(1, provider.polls)

    def test_optional_paid_stages_skip_under_frozen_profile_ceiling(self) -> None:
        provider = PaidScriptedProvider()
        frozen = spend_policy()
        for stage in ("polish", "qualitative_critic", "qualitative_candidate"):
            frozen["stage_ceilings_micro_usd"][stage] = 0
        profile = {
            "optional_stages": {
                "polish": True, "qualitative_critic": True,
                "qualitative_candidate": True,
            },
            "spend_policy": frozen,
        }
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile=profile,
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            paused = load_json(run_dir / "run.json")
            action = paused["spend_ledger"]["actions"][0]
            authorization = {
                "schema_version": AUTHORIZATION_SCHEMA,
                "action_id": action["action_id"],
                "binding": action["binding"],
                "authorization_reference": "api-reservation-optional-skip",
            }
            final = resume_bounded_run(
                run_dir, provider=provider, authorizations=[authorization]
            )
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(
                ["polish", "qualitative_critic", "qualitative_candidate"],
                final["bounded"]["skipped_stages"],
            )
            self.assertEqual(1, provider.submissions)


if __name__ == "__main__":
    unittest.main()
