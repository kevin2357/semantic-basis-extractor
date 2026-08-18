from __future__ import annotations

import json
import hashlib
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
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
from astrowoof_natal_authoring.bounded_provider import (  # noqa: E402
    OpenAIBoundedLifecycleProvider,
)
from astrowoof_natal_authoring.closure import (  # noqa: E402
    load_json,
    save_state,
    validate_workspace_snapshot,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    ExecutionEventEmitter,
)
from astrowoof_natal_authoring.lifecycle import (  # noqa: E402
    closeout_run,
    deny_providerless_action,
    inspect_lifecycle,
    reconcile_required_providerless_denial,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
)
from astrowoof_natal_authoring.reconciliation import (  # noqa: E402
    ProviderReconciliationAdapters,
    reconcile_authoring_provider_cycle,
    run_bounded_authoring_reconciliation,
)
from astrowoof_natal_authoring.spend import (  # noqa: E402
    AUTHORIZATION_SCHEMA,
    PRICE_BOOK_VERSION,
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
)
from test_bounded_authoring import compiled  # noqa: E402
import test_provider_pending_capacity as provider_pending_fixtures  # noqa: E402


def workspace_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and not path.name.endswith(".lock")
    }


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

    def __init__(
        self, *, interrupt_after_identity: bool = False,
        retrieval_status: str = "completed", retrieval_error: bool = False,
        retrieval_identity_conflict: bool = False,
    ) -> None:
        self.submissions = 0
        self.polls = 0
        self.interrupt_after_identity = interrupt_after_identity
        self.responses = self
        self.base_url = "https://api.openai.invalid/v1"
        self.http_timeout_seconds = 60.0
        self.max_transport_retries = 4
        self.retrievals = 0
        self.retrieval_status = retrieval_status
        self.retrieval_error = retrieval_error
        self.retrieval_identity_conflict = retrieval_identity_conflict

    def _request_with_retry(self, **kwargs):
        self.retrievals += 1
        if self.retrieval_error:
            raise TimeoutError("fixture retrieval timeout")
        response_id = str(kwargs["url"]).rsplit("/", 1)[-1]
        return {
            "id": (
                "resp-conflict" if self.retrieval_identity_conflict else response_id
            ),
            "status": self.retrieval_status,
            "usage": {"input_tokens": 10, "output_tokens": 10},
        }, 1

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
    rejected_once = False

    def execute(self, **kwargs):
        result, metadata = super().execute(**kwargs)
        if (
            kwargs["stage"] == "authoring_initial"
            and result["cards"]
            and not self.rejected_once
        ):
            self.rejected_once = True
            result = deepcopy(result)
            result["cards"][0]["priority_id"] = "drifted"
        return result, metadata


class RecordingFakeProvider(FakeBoundedLifecycleProvider):
    def __init__(self):
        self.pass_ids = []
        self.memberships = []
        self.retry_feedback = []

    def execute(self, **kwargs):
        packet = kwargs["payload"]["authoring_packet"]
        if kwargs["stage"] in {"authoring_initial", "creative_retry"}:
            self.pass_ids.append(packet["pass_id"])
            self.memberships.append([claim["claim_id"] for claim in packet["claims"]])
            if kwargs["stage"] == "creative_retry":
                self.retry_feedback.append(deepcopy(kwargs["payload"]["retry_feedback"]))
        return super().execute(**kwargs)


def _batch_editorial(packet):
    hydrated = fake_author_bounded(packet)
    editorial_fields = (
        "dos", "donts", "funny_dog_quotes", "imperative_dog_quotes",
        "applicable_canine_jokes", "densities",
    )
    return {
        "cards": [
            {"claim_id": card["claim_id"]} |
            {field: card[field] for field in editorial_fields}
            for card in hydrated["cards"]
        ],
        "summaries": [
            {"summary_id": summary_id, "headline": summary["headline"],
             "body": summary["body"]}
            for summary_id, summary in hydrated["summaries"].items()
        ],
    }


class BoundedBatchTransport:
    def __init__(
        self, *, reject_first_member_once=False, pending_once=False,
        error_first_member_once=False, duplicate_first_member=False,
        usage_available=True, terminal_first_status=None,
        missing_usage_member_index=None,
    ):
        self.reject_first_member_once = reject_first_member_once
        self.pending_once = pending_once
        self.error_first_member_once = error_first_member_once
        self.duplicate_first_member = duplicate_first_member
        self.usage_available = usage_available
        self.terminal_first_status = terminal_first_status
        self.missing_usage_member_index = missing_usage_member_index
        self.upload_calls = 0
        self.create_calls = 0
        self.retrieve_calls = 0
        self.rounds = {}
        self.uploaded = None

    def upload_jsonl(self, content, filename):
        self.upload_calls += 1
        self.uploaded = content.decode("utf-8")
        return {"id": f"file-input-{self.upload_calls}"}

    def create_batch(self, payload):
        self.create_calls += 1
        batch_id = f"batch-bounded-{self.create_calls}"
        self.rounds[batch_id] = self.uploaded
        status = (
            self.terminal_first_status
            if self.create_calls == 1 and self.terminal_first_status
            else "in_progress" if self.pending_once else "completed"
        )
        return self._batch(batch_id, status)

    def retrieve_batch(self, batch_id):
        self.retrieve_calls += 1
        self.pending_once = False
        return self._batch(batch_id, "completed")

    def _batch(self, batch_id, status):
        return {
            "id": batch_id, "status": status,
            "output_file_id": f"output-{batch_id}" if status == "completed" else None,
            "error_file_id": (
                f"error-{batch_id}"
                if status == "completed" and self.error_first_member_once
                and self.create_calls == 1 else None
            ),
            "request_counts": {"total": 6, "completed": 6, "failed": 0},
        }

    def download_file(self, file_id):
        is_error = file_id.startswith("error-")
        batch_id = file_id.removeprefix("output-").removeprefix("error-")
        lines = []
        for index, raw in enumerate(self.rounds[batch_id].splitlines()):
            request = json.loads(raw)
            failed_member = (
                self.error_first_member_once and self.create_calls == 1 and index == 0
            )
            if is_error:
                if failed_member:
                    lines.append(json.dumps({
                        "custom_id": request["custom_id"],
                        "error": {"code": "fixture_member_failed"},
                    }))
                continue
            if failed_member:
                continue
            payload = json.loads(request["body"]["input"][1]["content"])
            editorial = _batch_editorial(payload["authoring_packet"])
            if self.reject_first_member_once and self.create_calls == 1 and index == 0:
                editorial["cards"][0]["claim_id"] = "unknown-claim"
            response = {
                "id": f"resp-{request['custom_id']}", "status": "completed",
                "model": request["body"]["model"],
                "output": [{"type": "message", "content": [
                    {"type": "output_text", "text": json.dumps(editorial)}
                ]}],
            }
            if (
                self.usage_available
                and index != self.missing_usage_member_index
            ):
                response["usage"] = {
                    "input_tokens": 100, "output_tokens": 100,
                    "total_tokens": 200,
                }
            lines.append(json.dumps({
                "custom_id": request["custom_id"],
                "response": {"status_code": 200, "body": response},
            }))
        if self.duplicate_first_member and lines and not is_error:
            lines.append(lines[0])
        return "\n".join(lines) + "\n"


class RejectInitialPaidProvider(PaidScriptedProvider):
    rejected_once = False

    def execute(self, **kwargs):
        result, metadata = super().execute(**kwargs)
        if (
            kwargs["stage"] == "authoring_initial"
            and result["cards"]
            and not self.rejected_once
        ):
            self.rejected_once = True
            result = deepcopy(result)
            result["cards"][0]["priority_id"] = "drifted"
        return result, metadata


class TestBoundedLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = compiled()

    def drive_authorized(
        self, run_dir: Path, provider, *, stop_before_stage: str | None = None,
        reference: str = "api-drive",
    ):
        authorizations = None
        while True:
            try:
                return resume_bounded_run(
                    run_dir, provider=provider, authorizations=authorizations
                )
            except AwaitingSpendAuthorization:
                state = load_json(run_dir / "run.json")
                prepared = [
                    item for item in state["spend_ledger"]["actions"]
                    if item["state"] == "PREPARED"
                ]
                self.assertEqual(1, len(prepared))
                action = prepared[0]
                if action["binding"]["stage"] == stop_before_stage:
                    return state, action
                authorizations = [{
                    "schema_version": AUTHORIZATION_SCHEMA,
                    "action_id": action["action_id"],
                    "binding": deepcopy(action["binding"]),
                    "authorization_reference": (
                        f"{reference}:{len(state['spend_ledger']['actions'])}"
                    ),
                }]

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

    def test_bounded_batch_authors_six_members_under_one_round(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.paid = False
            transport = BoundedBatchTransport()
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            state = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            rounds = state["batch_service"]["rounds"]
            self.assertEqual(1, len(rounds))
            self.assertEqual(6, rounds[0]["member_count"])
            self.assertEqual(6000, rounds[0]["aggregate_maximum_output_tokens"])
            self.assertEqual("INGESTED", rounds[0]["state"])
            self.assertEqual("provider_usage_reported", rounds[0]["cost_disposition"])
            self.assertEqual(1, transport.upload_calls)
            self.assertEqual(1, transport.create_calls)

    def test_bounded_batch_retries_only_rejected_member_in_second_round(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.paid = False
            transport = BoundedBatchTransport(reject_first_member_once=True)
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            state = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            rounds = state["batch_service"]["rounds"]
            self.assertEqual([6, 1], [item["member_count"] for item in rounds])
            retried = rounds[1]["requests"][0]
            self.assertEqual(2, retried["attempt_number"])
            self.assertEqual("creative_retry", retried["stage"])
            self.assertEqual(2, transport.create_calls)
            retry_line = json.loads(
                transport.rounds["batch-bounded-2"].splitlines()[0]
            )
            retry_payload = json.loads(
                retry_line["body"]["input"][1]["content"]
            )
            self.assertEqual(
                retried["pass_id"], retry_payload["retry_feedback"]["pass_id"]
            )

    def test_bounded_batch_error_member_retries_only_that_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.paid = False
            transport = BoundedBatchTransport(error_first_member_once=True)
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            state = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertEqual(
                [6, 1],
                [item["member_count"] for item in state["batch_service"]["rounds"]],
            )

    def test_bounded_batch_terminal_provider_failure_retries_the_round(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
            )
            provider.paid = False
            provider.batch_transport = BoundedBatchTransport(
                terminal_first_status="failed"
            )
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            state = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            rounds = state["batch_service"]["rounds"]
            self.assertEqual([6, 6], [item["member_count"] for item in rounds])
            self.assertEqual("FAILED", rounds[0]["state"])
            self.assertEqual("creative_retry", rounds[1]["stage"])

    def test_bounded_batch_duplicate_member_fails_closed_before_ingestion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
            )
            provider.paid = False
            provider.batch_transport = BoundedBatchTransport(
                duplicate_first_member=True
            )
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            with self.assertRaisesRegex(ValueError, "repeats custom_id"):
                resume_bounded_run(run_dir, provider=provider)
            state = load_json(run_dir / "run.json")
            self.assertEqual(
                set(), set(state["bounded"]["completed_pass_ids"])
            )

    def test_bounded_batch_detaches_and_retrieves_same_provider_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.paid = False
            transport = BoundedBatchTransport(pending_once=True)
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            pending = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("PENDING", pending["batch_service"]["rounds"][0]["state"])
            completed = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", completed["status"])
            self.assertEqual(1, transport.upload_calls)
            self.assertEqual(1, transport.create_calls)
            self.assertEqual(1, transport.retrieve_calls)

    def test_bounded_batch_interrupt_after_identity_never_recreates_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
            )
            provider.paid = False
            transport = BoundedBatchTransport(pending_once=True)
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )

            def interrupt(point):
                if point == "after_bounded_batch_provider_identity":
                    raise RuntimeError("injected after durable Batch identity")

            with self.assertRaisesRegex(RuntimeError, "durable Batch identity"):
                resume_bounded_run(
                    run_dir, provider=provider, _failure_injector=interrupt
                )
            persisted = load_json(run_dir / "run.json")
            self.assertEqual(
                "batch-bounded-1",
                persisted["batch_service"]["rounds"][0]["batch_id"],
            )
            completed = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", completed["status"])
            self.assertEqual(1, transport.upload_calls)
            self.assertEqual(1, transport.create_calls)
            self.assertEqual(1, transport.retrieve_calls)

    def test_bounded_batch_round_state_rejects_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
            )
            provider.paid = False
            provider.batch_transport = BoundedBatchTransport(pending_once=True)
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={"optional_stages": {
                    "polish": False, "qualitative_critic": False,
                    "qualitative_candidate": False,
                }},
            )
            resume_bounded_run(run_dir, provider=provider)
            state = load_json(run_dir / "run.json")
            state["batch_service"]["rounds"][0]["consumer_guess"] = True
            save_state(run_dir / "run.json", state)
            with self.assertRaisesRegex(ValueError, "unsupported or missing fields"):
                resume_bounded_run(run_dir, provider=provider)

    def test_bounded_batch_uses_one_paid_action_for_the_round(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            transport = BoundedBatchTransport()
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={
                    "optional_stages": {
                        "polish": False, "qualitative_critic": False,
                        "qualitative_candidate": False,
                    },
                    "spend_policy": spend_policy(),
                },
            )
            state = self.drive_authorized(run_dir, provider)
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            actions = state["spend_ledger"]["actions"]
            self.assertEqual(1, len(actions))
            binding = actions[0]["binding"]
            self.assertEqual("batch", binding["service_level"])
            self.assertEqual(6000, binding["maximum_output_tokens"])
            self.assertEqual(
                "bounded_natal.v2:batch-round-001", binding["route"]
            )
            self.assertEqual(
                binding["commitment_micro_usd"],
                state["batch_service"]["rounds"][0]
                ["aggregate_commitment_micro_usd"],
            )
            self.assertEqual("REPORTED", actions[0]["state"])

    def test_bounded_batch_reconciliation_is_retrieval_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            transport = BoundedBatchTransport(pending_once=True)
            provider.batch_transport = transport
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={
                    "optional_stages": {
                        "polish": False, "qualitative_critic": False,
                        "qualitative_candidate": False,
                    },
                    "spend_policy": spend_policy(),
                },
            )
            pending = self.drive_authorized(run_dir, provider)
            action = pending["spend_ledger"]["actions"][0]
            uploads, creates = transport.upload_calls, transport.create_calls
            result = reconcile_authoring_provider_cycle(
                run_dir,
                observed_at=action["provider_reconciliation"]["resume_not_before"],
                provider_adapters=ProviderReconciliationAdapters(
                    bounded_batch_provider=provider,
                    bounded_batch_transport=transport,
                ),
            )
            self.assertIn(result["outcome"], {"progressed_local", "terminal"})
            self.assertEqual("batch", result["provider_operations"][0]["provider_operation_kind"])
            self.assertEqual(6, result["provider_operations"][0]["member_count"])
            self.assertEqual(uploads, transport.upload_calls)
            self.assertEqual(creates, transport.create_calls)
            self.assertEqual(1, transport.retrieve_calls)
            self.assertEqual(
                "DELIVERY_COMPLETE", load_json(run_dir / "run.json")["status"]
            )

    def test_bounded_batch_missing_usage_retains_consumer_authority_not_custody(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.batch_transport = BoundedBatchTransport(usage_available=False)
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={
                    "optional_stages": {
                        "polish": False, "qualitative_critic": False,
                        "qualitative_candidate": False,
                    },
                    "spend_policy": spend_policy(),
                },
            )
            state = self.drive_authorized(run_dir, provider)
            action = state["spend_ledger"]["actions"][0]
            self.assertEqual("REPORTED", action["state"])
            self.assertEqual(
                "provider_usage_unavailable_billing_reconciliation_pending",
                action["reported"]["cost_disposition"],
            )
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared"
            )
            self.assertEqual(0, inspection["provider_custody"]["provider_action_count"])
            self.assertEqual("retain", inspection["consumer_authority"]["state"])

    def test_bounded_batch_mixed_member_usage_does_not_settle_partial_total(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=run_dir, api_key="test-key", service_level="batch",
                model="gpt-5.6-luna", maximum_output_tokens=1000,
            )
            provider.batch_transport = BoundedBatchTransport(
                missing_usage_member_index=2
            )
            create_bounded_run(
                run_dir, self.artifacts, provider=provider,
                generation_profile={
                    "optional_stages": {
                        "polish": False, "qualitative_critic": False,
                        "qualitative_candidate": False,
                    },
                    "spend_policy": spend_policy(),
                },
            )
            state = self.drive_authorized(run_dir, provider)
            action = state["spend_ledger"]["actions"][0]
            round_record = state["batch_service"]["rounds"][0]
            self.assertEqual("REPORTED", action["state"])
            self.assertIsNone(action["reported"]["usage"])
            self.assertIsNone(action["reported"]["estimated_micro_usd"])
            self.assertEqual(
                "provider_usage_unavailable_billing_reconciliation_pending",
                action["reported"]["cost_disposition"],
            )
            self.assertEqual(
                action["reported"]["cost_disposition"],
                round_record["cost_disposition"],
            )
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared"
            )
            self.assertEqual(0, inspection["provider_custody"]["provider_action_count"])
            self.assertEqual("retain", inspection["consumer_authority"]["state"])

    def test_v2_run_persists_six_passes_and_executes_isolated_membership(self) -> None:
        provider = RecordingFakeProvider()
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            created = create_bounded_run(run_dir, self.artifacts, provider=provider)
            self.assertEqual(
                "astrowoof.bounded_natal.authoring_run.v2",
                created["route_contract"],
            )
            self.assertEqual(6, len(created["passes"]))
            self.assertEqual(6, len(created["bounded"]["pass_packets"]))
            final = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(final["bounded"]["pass_ids"], provider.pass_ids)
            self.assertEqual([10, 10, 10, 10, 10, 0], list(map(len, provider.memberships)))
            flattened = [claim_id for group in provider.memberships for claim_id in group]
            self.assertEqual(50, len(flattened))
            self.assertEqual(50, len(set(flattened)))

    def test_reordered_pass_completion_assembles_canonical_claim_order(self) -> None:
        provider = RecordingFakeProvider()
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            state = create_bounded_run(run_dir, self.artifacts, provider=provider)
            state["bounded"]["pass_ids"].reverse()
            save_state(run_dir / "run.json", state)
            final = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            cards = load_json(run_dir / "bounded/final/cards.json")["cards"]
            claim_deck = load_json(run_dir / "bounded/inputs/claim-deck.json")
            self.assertEqual(
                [claim["claim_id"] for claim in claim_deck["claims"]],
                [card["claim_id"] for card in cards],
            )

    def test_legacy_one_operation_run_fails_closed_with_typed_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            state = create_bounded_run(run_dir, self.artifacts)
            state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v1"
            state["route"] = "bounded_natal.v1"
            save_state(run_dir / "run.json", state)
            with self.assertRaisesRegex(
                ValueError, "legacy_bounded_topology_unsupported"
            ):
                resume_bounded_run(run_dir)

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
            attempts = [len(item["attempts"]) for item in state["passes"].values()]
            self.assertEqual([2, 1, 1, 1, 1, 1], attempts)
            self.assertIn(
                "changed locked priority_id",
                record["attempts"][0]["qa"]["report"]["errors"][0],
            )

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
            state = self.drive_authorized(
                run_dir, provider, reference="api-reservation-bounded"
            )
            self.assertEqual("DELIVERY_COMPLETE", state["status"])
            self.assertEqual(6, provider.submissions)
            self.assertEqual(
                ["REPORTED"] * 6,
                [item["state"] for item in state["spend_ledger"]["actions"]],
            )
            self.assertEqual(
                state["bounded"]["pass_ids"], state["bounded"]["completed_pass_ids"]
            )
            routes = [item["binding"]["route"] for item in state["spend_ledger"]["actions"]]
            self.assertEqual(6, len(set(routes)))
            self.assertTrue(all(route.startswith("bounded_natal.v2:") for route in routes))
            self.assertTrue(all(":attempt-001" in route for route in routes))

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

    def test_bounded_resume_reconciles_retained_required_denial_without_submission(self) -> None:
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
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-15T23:00:00Z",
            )
            request = {
                "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
                "run_id": state["run_id"], "action_id": action["action_id"],
                "binding": action["binding"], "observed": inspection["observation"],
                "denial_reason": "reservation_unavailable",
                "external_authority_reference": "api-fence:retained-bounded",
            }
            deny_providerless_action(
                run_dir, request, decision_at="2026-08-15T23:00:01Z"
            )
            state = load_json(run_dir / "run.json")
            state.pop("terminal_transition", None)
            state["status"] = "AWAITING_SPEND_AUTHORIZATION"
            action = state["spend_ledger"]["actions"][0]
            denial = action["negative_authorization"]
            denial.pop("run_transition", None)
            artifact = {
                "schema_version": "astrowoof.provider_negative_authorization_record.v0.1",
                "run_id": state["run_id"], "action_id": action["action_id"],
                "binding": deepcopy(action["binding"]),
                "disposition": "DENIED_PROVIDERLESS",
                "denial_reason": denial["denial_reason"],
                "authorization_previously_recorded": denial[
                    "authorization_previously_recorded"
                ],
                "external_authority_reference": denial[
                    "external_authority_reference"
                ],
                "request_observation": deepcopy(denial["request_observation"]),
                "decision_basis": deepcopy(denial["decision_basis"]),
            }
            (run_dir / denial["result_artifact"]).write_text(
                json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
            )
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)

            def interrupt(point: str) -> None:
                if point == "after_reconciliation_state_persisted":
                    raise RuntimeError(point)

            with self.assertRaisesRegex(RuntimeError, "state_persisted"):
                reconcile_required_providerless_denial(
                    run_dir, reconciled_at="2026-08-15T23:00:02Z",
                    _failure_injector=interrupt,
                )
            resumed = resume_bounded_run(run_dir, provider=provider)
            self.assertEqual("BUDGET_EXHAUSTED", resumed["status"])
            self.assertEqual(0, provider.submissions)
            self.assertIn("required_denial_reconciliation", resumed)

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
            paused, polish = self.drive_authorized(
                run_dir, provider, stop_before_stage="polish",
                reference="api-reservation-initial",
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
            self.assertEqual(6, provider.submissions)

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
            before = workspace_hashes(run_dir)
            inspection = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at=interrupted["spend_ledger"]["actions"][0]
                ["provider_reconciliation"]["resume_not_before"],
            )
            self.assertEqual(before, workspace_hashes(run_dir))
            self.assertTrue(inspection["observation"]["snapshot_complete"])
            self.assertTrue(inspection["observation"]["inventory_valid"])
            self.assertEqual(
                "continue_local_cycle",
                inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual(
                "known_operations_pending",
                inspection["provider_custody"]["state"],
            )
            self.assertEqual("bounded_natal", inspection["native_route"]["route_family"])
            self.assertEqual(
                "response",
                inspection["provider_custody"]["actions"][0]["provider_operation_kind"],
            )
            self.assertEqual(
                [interrupted["spend_ledger"]["actions"][0]["action_id"]],
                inspection["provider_custody"]["action_ids"],
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(run_dir, provider=provider)
            final = self.drive_authorized(
                run_dir, provider, reference="api-reservation-after-reconcile"
            )
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(6, provider.submissions)
            self.assertEqual(1, provider.polls)

    def test_bounded_reconciliation_retrieves_once_then_exhausts_local_work(self) -> None:
        provider = PaidScriptedProvider(interrupt_after_identity=True)
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
            action = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0]
            authorization = {
                "schema_version": AUTHORIZATION_SCHEMA,
                "action_id": action["action_id"], "binding": action["binding"],
                "authorization_reference": "api-reservation-reconcile-bounded",
            }
            with self.assertRaisesRegex(RuntimeError, "injected"):
                resume_bounded_run(
                    run_dir, provider=provider, authorizations=[authorization]
                )
            interrupted = load_json(run_dir / "run.json")
            due = interrupted["spend_ledger"]["actions"][0][
                "provider_reconciliation"
            ]["resume_not_before"]
            result = reconcile_authoring_provider_cycle(
                run_dir, observed_at=due,
                provider_adapters=ProviderReconciliationAdapters(
                    bounded_interactive_provider=provider,
                    python_executable=Path(sys.executable),
                ),
            )
            self.assertEqual("awaiting_external_authority", result["outcome"])
            self.assertEqual("bounded_natal", result["inspection"]["native_route"]["route_family"])
            self.assertEqual(1, provider.submissions)
            self.assertEqual(1, provider.retrievals)
            self.assertEqual(1, provider.polls)
            self.assertTrue(result["local_continuation"]["exhausted_before_detach"])
            self.assertEqual(
                [interrupted["bounded"]["pass_ids"][0]],
                result["local_continuation"]["pass_ids"],
            )
            self.assertEqual(
                "await_external_authority",
                result["inspection"]["execution_capacity"]["disposition"],
            )
            final = self.drive_authorized(
                run_dir, provider, reference="api-after-retrieval"
            )
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(6, provider.submissions)
            validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))

    def test_bounded_reconciliation_pending_warning_and_conflict_fail_closed(self) -> None:
        cases = (
            ({"retrieval_status": "in_progress"}, "detached_provider_pending"),
            ({"retrieval_error": True}, "detached_provider_pending"),
            ({"retrieval_identity_conflict": True}, "review_required"),
            ({"retrieval_status": "failed"}, "review_required"),
        )
        profile = {
            "optional_stages": {stage: False for stage in (
                "polish", "qualitative_critic", "qualitative_candidate"
            )},
            "spend_policy": spend_policy(),
        }
        for settings, expected in cases:
            with self.subTest(settings=settings), tempfile.TemporaryDirectory() as temporary:
                provider = PaidScriptedProvider(
                    interrupt_after_identity=True, **settings
                )
                run_dir = Path(temporary) / "run"
                create_bounded_run(
                    run_dir, self.artifacts, provider=provider,
                    generation_profile=profile,
                )
                with self.assertRaises(AwaitingSpendAuthorization):
                    resume_bounded_run(run_dir, provider=provider)
                action = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0]
                authorization = {
                    "schema_version": AUTHORIZATION_SCHEMA,
                    "action_id": action["action_id"], "binding": action["binding"],
                    "authorization_reference": "api-reservation-bounded-failure",
                }
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    resume_bounded_run(
                        run_dir, provider=provider, authorizations=[authorization]
                    )
                due = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0][
                    "provider_reconciliation"
                ]["resume_not_before"]
                result = run_bounded_authoring_reconciliation(
                    run_dir, provider=provider, max_attempts=3,
                    python_executable=Path(sys.executable), observed_at=due,
                )
                self.assertEqual(expected, result["outcome"])
                self.assertEqual(1, provider.retrievals)
                self.assertEqual(1, provider.submissions)
                self.assertEqual(0, provider.polls)

    def test_bounded_reconciliation_covers_retry_and_optional_stages(self) -> None:
        cases = (
            ("creative_retry", RejectInitialPaidProvider()),
            ("polish", PaidScriptedProvider()),
            ("qualitative_critic", PaidScriptedProvider()),
            ("qualitative_candidate", PaidScriptedProvider()),
        )
        for target_stage, provider in cases:
            with self.subTest(stage=target_stage), tempfile.TemporaryDirectory() as temporary:
                run_dir = Path(temporary) / "run"
                optional = {
                    stage: stage == target_stage
                    for stage in ("polish", "qualitative_critic", "qualitative_candidate")
                }
                if target_stage == "qualitative_candidate":
                    optional["qualitative_critic"] = False
                profile = {
                    "optional_stages": optional,
                    "spend_policy": spend_policy(),
                }
                create_bounded_run(
                    run_dir, self.artifacts, provider=provider,
                    generation_profile=profile,
                )
                state, target = self.drive_authorized(
                    run_dir, provider, stop_before_stage=target_stage,
                    reference=f"api-initial-{target_stage}",
                )
                provider.interrupt_after_identity = True
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    resume_bounded_run(run_dir, provider=provider, authorizations=[{
                        "schema_version": AUTHORIZATION_SCHEMA,
                        "action_id": target["action_id"], "binding": target["binding"],
                        "authorization_reference": f"api-target-{target_stage}",
                    }])
                state = load_json(run_dir / "run.json")
                due = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == target["action_id"]
                )["provider_reconciliation"]["resume_not_before"]
                result = run_bounded_authoring_reconciliation(
                    run_dir, provider=provider, max_attempts=3,
                    python_executable=Path(sys.executable), observed_at=due,
                )
                expected_outcome = (
                    "awaiting_external_authority"
                    if target_stage == "creative_retry" else "terminal"
                )
                self.assertEqual(expected_outcome, result["outcome"])
                self.assertIn(target_stage, result["local_continuation"]["stages"])
                self.assertEqual(1, provider.retrievals)
                expected_before_finish = 2 if target_stage == "creative_retry" else 7
                self.assertEqual(expected_before_finish, provider.submissions)
                self.assertEqual(1, provider.polls)
                if target_stage == "creative_retry":
                    final = self.drive_authorized(
                        run_dir, provider, reference="api-after-creative-retry"
                    )
                    self.assertEqual("DELIVERY_COMPLETE", final["status"])
                    self.assertEqual(7, provider.submissions)
                validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))

    def test_bounded_reconciliation_crash_checkpoints_resume_without_retrieval(self) -> None:
        profile = {
            "optional_stages": {stage: False for stage in (
                "polish", "qualitative_critic", "qualitative_candidate"
            )},
            "spend_policy": spend_policy(),
        }
        for failure_point in (
            "after_provider_retrieval_checkpoint",
            "after_bounded_local_continuation",
            "after_bounded_result_snapshot",
        ):
            with self.subTest(point=failure_point), tempfile.TemporaryDirectory() as temporary:
                provider = PaidScriptedProvider(interrupt_after_identity=True)
                run_dir = Path(temporary) / "run"
                create_bounded_run(
                    run_dir, self.artifacts, provider=provider,
                    generation_profile=profile,
                )
                with self.assertRaises(AwaitingSpendAuthorization):
                    resume_bounded_run(run_dir, provider=provider)
                action = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0]
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    resume_bounded_run(run_dir, provider=provider, authorizations=[{
                        "schema_version": AUTHORIZATION_SCHEMA,
                        "action_id": action["action_id"], "binding": action["binding"],
                        "authorization_reference": f"api-crash-{failure_point}",
                    }])
                due = load_json(run_dir / "run.json")["spend_ledger"]["actions"][0][
                    "provider_reconciliation"
                ]["resume_not_before"]

                def inject(point: str) -> None:
                    if point == failure_point:
                        raise RuntimeError(f"injected {point}")

                with self.assertRaisesRegex(RuntimeError, failure_point):
                    run_bounded_authoring_reconciliation(
                        run_dir, provider=provider, max_attempts=3,
                        python_executable=Path(sys.executable), observed_at=due,
                        _failure_injector=inject,
                    )
                validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))
                if failure_point == "after_provider_retrieval_checkpoint":
                    recovered = run_bounded_authoring_reconciliation(
                        run_dir, provider=provider, max_attempts=3,
                        python_executable=Path(sys.executable), observed_at=due,
                    )
                    self.assertEqual("awaiting_external_authority", recovered["outcome"])
                else:
                    inspection = inspect_lifecycle(
                        run_dir, native_exclusive_access="declared"
                    )
                    self.assertEqual(
                        "await_external_authority",
                        inspection["execution_capacity"]["disposition"],
                    )
                self.assertEqual(1, provider.retrievals)
                self.assertEqual(1, provider.submissions)
                self.assertLessEqual(provider.polls, 1)
                final = self.drive_authorized(
                    run_dir, provider, reference=f"api-recovered-{failure_point}"
                )
                self.assertEqual("DELIVERY_COMPLETE", final["status"])
                self.assertEqual(6, provider.submissions)
                validate_workspace_snapshot(run_dir, load_json(run_dir / "run.json"))

    def test_mixed_route_pending_cohort_has_independent_capacity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cohort = Path(temporary).resolve()
            exact_root = cohort / "exact-response"
            exact_root.mkdir()
            baseline = provider_pending_fixtures.TestProviderPendingCapacityBaseline()
            baseline.materialize(exact_root)

            batch_root = cohort / "exact-batch"
            batch_root.mkdir()
            batch_state = baseline.materialize(batch_root)
            action = batch_state["spend_ledger"]["actions"][0]
            batch_state["spend_ledger"]["actions"] = [action]
            action["binding"]["service_level"] = "batch"
            action["binding"]["route"] = "batch-round-001"
            action["provider"]["kind"] = "batch"
            action["provider"]["id"] = "batch-cohort-001"
            batch_state["service_level"] = "batch"
            batch_state["batch_service"] = {"rounds": [{
                "round_number": 1, "batch_id": "batch-cohort-001",
                "state": "SUBMITTED", "requests": [],
            }]}
            (batch_root / "run.json").write_text(
                json.dumps(batch_state, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(batch_root)

            bounded_root = cohort / "bounded-response"
            bounded_provider = PaidScriptedProvider(
                interrupt_after_identity=True, retrieval_status="in_progress"
            )
            profile = {
                "optional_stages": {stage: False for stage in (
                    "polish", "qualitative_critic", "qualitative_candidate"
                )},
                "spend_policy": spend_policy(),
            }
            create_bounded_run(
                bounded_root, self.artifacts, provider=bounded_provider,
                generation_profile=profile,
            )
            with self.assertRaises(AwaitingSpendAuthorization):
                resume_bounded_run(bounded_root, provider=bounded_provider)
            bounded_action = load_json(bounded_root / "run.json")["spend_ledger"]["actions"][0]
            with self.assertRaisesRegex(RuntimeError, "injected"):
                resume_bounded_run(bounded_root, provider=bounded_provider, authorizations=[{
                    "schema_version": AUTHORIZATION_SCHEMA,
                    "action_id": bounded_action["action_id"],
                    "binding": bounded_action["binding"],
                    "authorization_reference": "api-cohort-bounded",
                }])
            bounded_due = load_json(bounded_root / "run.json")["spend_ledger"]["actions"][0][
                "provider_reconciliation"
            ]["resume_not_before"]

            class PendingResponses:
                name = "openai"
                base_url = "https://api.openai.invalid/v1"
                http_timeout_seconds = 60.0
                max_transport_retries = 4

                def _request_with_retry(self, **kwargs):
                    operation_id = str(kwargs["url"]).rsplit("/", 1)[-1]
                    return {"id": operation_id, "status": "in_progress"}, 1

            class PendingBatch:
                def retrieve_batch(self, batch_id):
                    return {"id": batch_id, "status": "in_progress"}

            response_provider = PendingResponses()
            adapters = (
                ProviderReconciliationAdapters(
                    exact_interactive_provider=response_provider,
                ),
                ProviderReconciliationAdapters(
                    exact_batch_provider=response_provider,
                    exact_batch_transport=PendingBatch(),
                ),
                ProviderReconciliationAdapters(
                    bounded_interactive_provider=bounded_provider,
                ),
            )
            work = (
                (exact_root, "2026-08-15T20:18:00Z", adapters[0]),
                (batch_root, "2026-08-15T20:18:00Z", adapters[1]),
                (bounded_root, bounded_due, adapters[2]),
            )
            with ThreadPoolExecutor(max_workers=3) as pool:
                results = list(pool.map(
                    lambda item: reconcile_authoring_provider_cycle(
                        item[0], observed_at=item[1], provider_adapters=item[2]
                    ),
                    work,
                ))
            self.assertTrue(all(
                item["outcome"] == "detached_provider_pending"
                and item["inspection"]["execution_capacity"]["disposition"]
                == "release_until_due"
                for item in results
            ), [(item["outcome"], item["inspection"]["execution_capacity"]) for item in results])
            self.assertEqual(
                ["exact_natal", "exact_natal", "bounded_natal"],
                [item["inspection"]["native_route"]["route_family"] for item in results],
            )

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
            final = self.drive_authorized(
                run_dir, provider, reference="api-reservation-optional-skip"
            )
            self.assertEqual("DELIVERY_COMPLETE", final["status"])
            self.assertEqual(
                ["polish", "qualitative_critic", "qualitative_candidate"],
                final["bounded"]["skipped_stages"],
            )
            self.assertEqual(6, provider.submissions)


if __name__ == "__main__":
    unittest.main()
