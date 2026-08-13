from __future__ import annotations

import json
import sys
import unittest
import io
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    EVENT_PAYLOAD_REQUIRED,
    ExecutionEventEmitter,
    JsonlEventSink,
    StdoutJsonlSink,
    command_result_envelope,
    payload_catalog,
)
from astrowoof_natal_authoring.lifecycle_contracts import EVENT_NAMES  # noqa: E402
from astrowoof_natal_authoring.resource_access import read_resource_text  # noqa: E402
from astrowoof_natal_authoring.closure import (  # noqa: E402
    OpenAIResponsesProvider,
    SpendController,
    load_json,
    save_state,
)
from astrowoof_natal_authoring.spend import (  # noqa: E402
    action_binding,
    authorize_action,
    new_ledger,
    prepare_action,
)
import threading


class TestExecutionEvents(unittest.TestCase):
    def emitter(self, sink=None) -> ExecutionEventEmitter:
        return ExecutionEventEmitter(
            release="0.2.2", sink=sink,
            clock=lambda: datetime(2026, 8, 13, 23, 0, tzinfo=timezone.utc),
            id_factory=lambda: "evt_fixed",
            base_correlation={"native_run_id": "run_fixed"},
        )

    def test_packaged_payload_catalog_exactly_matches_code_and_allowlist(self) -> None:
        packaged = json.loads(read_resource_text(
            "contracts/execution-event-payload-catalog.v1.json"
        ))
        self.assertEqual(payload_catalog(), packaged)
        self.assertEqual(set(EVENT_NAMES), set(EVENT_PAYLOAD_REQUIRED))

    def test_typed_event_is_deterministic_and_delivered(self) -> None:
        delivered = []
        emitter = self.emitter(delivered.append)
        event = emitter.emit("run.started", data={"state_revision": 1})
        self.assertEqual([event], delivered)
        self.assertEqual("evt_fixed", event["event_id"])
        self.assertEqual("2026-08-13T23:00:00Z", event["event_time"])
        self.assertEqual(1, emitter.stats.emitted)

    def test_missing_typed_field_and_protected_data_are_dropped_safely(self) -> None:
        emitter = self.emitter()
        self.assertIsNone(emitter.emit("run.started", data={}))
        self.assertIsNone(emitter.emit(
            "run.started",
            data={"state_revision": 1, "nested": {"birth_datetime": "secret"}},
        ))
        self.assertEqual(2, emitter.stats.dropped)
        self.assertEqual(2, emitter.stats.serialization_warnings)

    def test_sink_failure_does_not_escape_or_become_state_authority(self) -> None:
        def fail(_event):
            raise RuntimeError("sink unavailable")

        emitter = self.emitter(fail)
        self.assertIsNone(emitter.emit("run.started", data={"state_revision": 1}))
        self.assertEqual(1, emitter.stats.dropped)
        self.assertEqual(1, emitter.stats.sink_warnings)
        self.assertEqual(0, emitter.stats.emitted)

    def test_jsonl_file_sink_appends_complete_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.jsonl"
            emitter = self.emitter(JsonlEventSink(path))
            emitter.emit("run.started", data={"state_revision": 1})
            emitter.emit("run.resumed", data={"state_revision": 2})
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(lines))
            self.assertEqual(
                ["run.started", "run.resumed"],
                [json.loads(line)["event_name"] for line in lines],
            )

    def test_stdout_transport_contains_only_typed_single_line_envelopes(self) -> None:
        stream = io.StringIO()
        sink = StdoutJsonlSink(stream)
        emitter = self.emitter(sink)
        emitter.emit("run.started", data={"state_revision": 1})
        sink(command_result_envelope({"status": "complete"}))
        documents = [json.loads(line) for line in stream.getvalue().splitlines()]
        self.assertEqual(
            ["execution_event", "command_result"],
            [item["envelope_type"] for item in documents],
        )
        self.assertEqual("sbe.command_result.v1", documents[-1]["schema_version"])

    def test_provider_lifecycle_events_share_exact_action_correlation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary).resolve()
            policy = {
                "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 10_000_000,
                "stage_ceilings_micro_usd": {
                    name: 10_000_000 for name in (
                        "authoring_initial", "creative_retry", "polish",
                        "qualitative_critic", "qualitative_candidate",
                    )
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip", "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            }
            state = {
                "schema_version": "astrowoof.semantic_closure_run.v0.9",
                "run_id": "run-events", "state_revision": 0, "status": "AUTHORING",
                "created_at": "2026-08-13T23:00:00Z", "passes": {}, "subjects": {},
                "authoring_profile": {"spend_policy": policy},
                "spend_ledger": new_ledger(policy), "provenance": {},
            }
            binding = action_binding(
                run_id="run-events", profile_sha256="1" * 64,
                prepared_state_revision=0, stage="polish", route="ella:polish:001",
                request_sha256="2" * 64, model="gpt-5.6-luna",
                service_level="interactive", maximum_output_tokens=1000,
                commitment_micro_usd=1000,
            )
            action = prepare_action(state["spend_ledger"], binding)
            authorize_action(state["spend_ledger"], {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action["action_id"], "binding": binding,
                "authorization_reference": "api-reservation",
            })
            run_json = run_dir / "run.json"
            save_state(run_json, state)
            delivered = []
            emitter = self.emitter(delivered.append)
            controller = SpendController(
                state=state, run_json=run_json, state_lock=threading.Lock(),
                consumer_id="event-worker", event_emitter=emitter,
            )
            before_submit, provider_created = controller.callbacks(
                stage="polish", route="ella:polish:001", model="gpt-5.6-luna",
                service_level="interactive", maximum_output_tokens=1000,
            )
            # Match the prepared binding's exact request digest via direct replacement.
            payload = {"fixture": True}
            from astrowoof_natal_authoring.spend import digest
            action["binding"]["request_sha256"] = digest(payload)
            save_state(run_json, state)
            before_submit(payload)
            provider_created("resp_event_exact", "response")
            controller.mark_active_waiting()
            controller.settle_active({
                "usage": {}, "estimated_cost": {"estimated_amount": 0.01},
                "duration_ms": 42,
            })
            names = [item["event_name"] for item in delivered]
            self.assertEqual([
                "authorization.granted", "provider.submission_started",
                "provider.identity_recorded", "provider.waiting", "provider.completed",
            ], names)
            self.assertTrue(all(
                item["correlation"]["action_id"] == action["action_id"]
                for item in delivered
            ))
            self.assertEqual("REPORTED", load_json(run_json)["spend_ledger"]["actions"][0]["state"])


if __name__ == "__main__":
    unittest.main()
