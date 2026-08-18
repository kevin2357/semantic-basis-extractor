from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_authoring import (  # noqa: E402
    fake_author_bounded,
)
from astrowoof_natal_authoring.bounded_provider import (  # noqa: E402
    OpenAIBoundedLifecycleProvider,
)
from test_bounded_authoring import compiled  # noqa: E402


def completed_response(value, response_id="resp_bounded_test"):
    return {
        "id": response_id,
        "status": "completed",
        "model": "gpt-5.6-luna",
        "output": [{
            "type": "message",
            "content": [{"type": "output_text", "text": json.dumps(value)}],
        }],
        "usage": {
            "input_tokens": 1000,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens": 500,
            "output_tokens_details": {"reasoning_tokens": 100},
            "total_tokens": 1500,
        },
    }


def editorial_response(cards):
    editorial_fields = (
        "dos", "donts", "funny_dog_quotes", "imperative_dog_quotes",
        "applicable_canine_jokes", "densities",
    )
    return {
        "cards": [
            {"claim_id": card["claim_id"]} |
            {field: card[field] for field in editorial_fields}
            for card in cards["cards"]
        ],
        "summaries": [
            {
                "summary_id": summary_id,
                "headline": summary["headline"],
                "body": summary["body"],
            }
            for summary_id, summary in cards["summaries"].items()
        ],
    }


class Transport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def request_json(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class TestBoundedOpenAIProvider(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifacts = compiled()
        cls.cards = fake_author_bounded(cls.artifacts.authoring_packet)

    def test_structured_response_uses_spend_callbacks_and_resumes_get_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            transport = Transport(completed_response(editorial_response(self.cards)))
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=Path(temporary), api_key="test-key",
                model="gpt-5.6-luna", maximum_output_tokens=5000,
                transport=transport,
            )
            submitted = []
            identities = []
            payload = {
                "route": "bounded_natal.v1",
                "stage": "authoring_initial",
                "authoring_packet": self.artifacts.authoring_packet,
            }
            result, metadata = provider.execute(
                stage="authoring_initial",
                route="bounded_natal.v1:authoring_initial:1",
                payload=payload,
                before_submit=submitted.append,
                provider_created=lambda provider_id, kind: identities.append(
                    (provider_id, kind)
                ),
            )
            self.assertEqual(self.cards, result)
            self.assertEqual("resp_bounded_test", metadata["response_id"])
            self.assertEqual(1, len(submitted))
            self.assertEqual([("resp_bounded_test", "response")], identities)
            self.assertEqual("POST", transport.calls[0]["method"])
            rendered = json.dumps(transport.calls[0]["payload"], sort_keys=True)
            self.assertNotIn("1981-10-10T15:00:00-06:00", rendered)
            self.assertNotIn("SEED-PROTECTED-DENVER", rendered)
            self.assertNotIn("source_artifact_ref", rendered)

            resumed, _ = provider.resume(
                stage="authoring_initial",
                route="bounded_natal.v1:authoring_initial:1",
                provider_operation_id="resp_bounded_test",
                payload=payload,
            )
            self.assertEqual(self.cards, resumed)
            self.assertEqual(["POST", "GET"], [call["method"] for call in transport.calls])

    def test_batch_body_matches_interactive_logical_request(self):
        with tempfile.TemporaryDirectory() as temporary:
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=Path(temporary), api_key="test-key",
                service_level="batch", model="gpt-5.6-luna",
                maximum_output_tokens=5000,
            )
            pass_id = self.artifacts.split_assignment["card_passes"][0]["pass_id"]
            packet = self.artifacts.pass_packets[pass_id]
            payload = {
                "route": "bounded_natal.v2", "stage": "authoring_initial",
                "authoring_packet": packet,
            }
            body = provider.batch_request_body(
                stage="authoring_initial", payload=payload, attempt_number=1,
            )
            live_transport = Transport(completed_response(
                editorial_response(fake_author_bounded(packet))
            ))
            live_provider = OpenAIBoundedLifecycleProvider(
                run_dir=Path(temporary) / "live", api_key="test-key",
                service_level="interactive", model="gpt-5.6-luna",
                maximum_output_tokens=5000, transport=live_transport,
            )
            live_provider.execute(
                stage="authoring_initial",
                route=f"bounded_natal.v2:{pass_id}:attempt-001",
                payload=payload, before_submit=lambda _: None,
                provider_created=lambda *_: None,
            )
            live_body = live_transport.calls[0]["payload"]
            self.assertIn("background", live_body)
            live_body.pop("background")
            self.assertEqual(body, live_body)
            self.assertEqual(provider._instructions("authoring_initial"), body["input"][0]["content"])
            self.assertEqual(payload, json.loads(body["input"][1]["content"]))
            self.assertEqual(
                provider._schema("authoring_initial", payload),
                body["text"]["format"]["schema"],
            )
            rendered = json.dumps(body, sort_keys=True)
            self.assertNotIn("1981-10-10T15:00:00-06:00", rendered)
            self.assertNotIn("SEED-PROTECTED-DENVER", rendered)

    def test_interactive_pass_request_is_isolated_and_hydrates_only_its_authority(self):
        pass_id = self.artifacts.split_assignment["card_passes"][0]["pass_id"]
        packet = self.artifacts.pass_packets[pass_id]
        pass_cards = fake_author_bounded(packet)
        with tempfile.TemporaryDirectory() as temporary:
            transport = Transport(completed_response(editorial_response(pass_cards)))
            provider = OpenAIBoundedLifecycleProvider(
                run_dir=Path(temporary), api_key="test-key",
                model="gpt-5.6-luna", maximum_output_tokens=5000,
                transport=transport,
            )
            payload = {
                "route": "bounded_natal.v2",
                "stage": "authoring_initial",
                "authoring_packet": packet,
            }
            result, _ = provider.execute(
                stage="authoring_initial",
                route=f"bounded_natal.v2:{pass_id}:attempt-001",
                payload=payload,
                before_submit=lambda _: None,
                provider_created=lambda *_: None,
            )
            self.assertEqual(10, len(result["cards"]))
            self.assertEqual({}, result["summaries"])
            schema = transport.calls[0]["payload"]["text"]["format"]["schema"]
            self.assertEqual(10, schema["properties"]["cards"]["minItems"])
            self.assertEqual(0, schema["properties"]["summaries"]["maxItems"])
            self.assertEqual(
                {item["claim_id"] for item in packet["claims"]},
                set(schema["properties"]["cards"]["items"]
                    ["properties"]["claim_id"]["enum"]),
            )

    def test_generated_cards_schema_is_strict_and_locks_semantic_fields(self):
        payload = {"authoring_packet": self.artifacts.authoring_packet}
        schema = OpenAIBoundedLifecycleProvider._schema("authoring_initial", payload)

        def assert_closed_objects(node):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertFalse(node.get("additionalProperties", True))
                    self.assertEqual(
                        set(node.get("properties") or {}), set(node.get("required") or [])
                    )
                for child in node.values():
                    assert_closed_objects(child)
            elif isinstance(node, list):
                for child in node:
                    assert_closed_objects(child)

        assert_closed_objects(schema)
        rendered = json.dumps(schema)
        self.assertNotIn("invariant_authority", rendered)
        self.assertNotIn("evidence_provenance", rendered)
        self.assertLess(len(rendered), 20_000)

    def test_hydration_rejects_unknown_claim_and_reattaches_authority(self):
        editorial = editorial_response(self.cards)
        hydrated = OpenAIBoundedLifecycleProvider._hydrate_cards(
            editorial, self.artifacts.authoring_packet
        )
        self.assertEqual(self.cards, hydrated)
        editorial["cards"][0]["claim_id"] = "unknown"
        with self.assertRaisesRegex(ValueError, "missing, duplicate, or unknown claims"):
            OpenAIBoundedLifecycleProvider._hydrate_cards(
                editorial, self.artifacts.authoring_packet
            )


if __name__ == "__main__":
    unittest.main()
