from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_provider import (  # noqa: E402
    OpenAIBoundedLifecycleProvider,
)
from astrowoof_natal_authoring.pass_protocol import (  # noqa: E402
    PassProtocolError,
    bind_logical_pass_request,
    bind_logical_pass_result,
    validate_logical_pass_result,
)
from test_bounded_authoring import compiled  # noqa: E402


class TestLogicalPassProtocol(unittest.TestCase):
    def setUp(self) -> None:
        artifacts = compiled()
        first_pass_id = artifacts.split_assignment["card_passes"][0]["pass_id"]
        self.packet = deepcopy(artifacts.pass_packets[first_pass_id])
        provider = object.__new__(OpenAIBoundedLifecycleProvider)
        provider.maximum_output_tokens = 30_000
        self.provider = provider

    def test_bounded_request_binding_is_deterministic_and_transport_neutral(self) -> None:
        first = self.provider.logical_pass_request(
            stage="authoring_initial", packet=self.packet, attempt_number=1
        )
        second = self.provider.logical_pass_request(
            stage="authoring_initial", packet=deepcopy(self.packet), attempt_number=1
        )
        self.assertEqual(first, second)
        self.assertEqual("bounded_natal", first.route_family)
        self.assertEqual(self.packet["pass_id"], first.pass_id)
        self.assertNotIn("service_level", first.as_dict())
        self.assertNotIn("provider_mechanism", first.as_dict())

    def test_attempt_stage_schema_and_maximum_output_are_bound(self) -> None:
        first = self.provider.logical_pass_request(
            stage="authoring_initial", packet=self.packet, attempt_number=1
        )
        retry = self.provider.logical_pass_request(
            stage="creative_retry", packet=self.packet, attempt_number=2
        )
        self.assertNotEqual(first.request_sha256, retry.request_sha256)
        self.assertEqual(30_000, retry.maximum_output_tokens)
        changed = bind_logical_pass_request(
            route_family="bounded_natal",
            route_contract=self.packet["run_contract"],
            assignment_sha256=self.packet["assignment_sha256"],
            pass_id=self.packet["pass_id"],
            pass_number=self.packet["pass_number"],
            pass_count=self.packet["pass_count"],
            attempt_number=1,
            stage="authoring_initial",
            resource_identity=self.packet["resource_set"],
            prompt={"changed": True},
            output_schema={"type": "object"},
            maximum_output_tokens=30_000,
        )
        self.assertNotEqual(first.request_sha256, changed.request_sha256)

    def test_exact_and_bounded_results_cannot_cross_routes(self) -> None:
        bounded = self.provider.logical_pass_request(
            stage="authoring_initial", packet=self.packet, attempt_number=1
        )
        result = bind_logical_pass_result(bounded, {"cards": []})
        validate_logical_pass_result(result, bounded)
        exact = bind_logical_pass_request(
            route_family="exact_natal", route_contract="exact.v1",
            assignment_sha256="a" * 64, pass_id=bounded.pass_id,
            pass_number=1, pass_count=6, attempt_number=1,
            stage="authoring_initial", resource_identity={"source": "x"},
            prompt={"input": "x"}, output_schema={"type": "object"},
            maximum_output_tokens=30_000,
        )
        with self.assertRaisesRegex(PassProtocolError, "does not match"):
            validate_logical_pass_result(result, exact)

    def test_conflicting_pass_binding_changes_request_identity(self) -> None:
        first = self.provider.logical_pass_request(
            stage="authoring_initial", packet=self.packet, attempt_number=1
        )
        changed = deepcopy(self.packet)
        changed["pass_id"] = "conflicting-pass"
        with self.assertRaises(ValueError):
            self.provider.logical_pass_request(
                stage="authoring_initial", packet=changed, attempt_number=1
            )
        self.assertEqual(self.packet["pass_id"], first.pass_id)

    def test_route_specific_schema_and_hydration_refuse_crossed_exact_output(self) -> None:
        schema = self.provider._schema(
            "authoring_initial", {"authoring_packet": self.packet}
        )
        self.assertEqual(10, schema["properties"]["cards"]["minItems"])
        self.assertEqual(10, schema["properties"]["cards"]["maxItems"])
        self.assertEqual(0, schema["properties"]["summaries"]["maxItems"])
        with self.assertRaisesRegex(ValueError, "missing, duplicate, or unknown"):
            self.provider._hydrate_cards(
                {"cards": [{"relative_file": "WRITE THIS CARD.md"}], "summaries": []},
                self.packet,
            )


if __name__ == "__main__":
    unittest.main()
