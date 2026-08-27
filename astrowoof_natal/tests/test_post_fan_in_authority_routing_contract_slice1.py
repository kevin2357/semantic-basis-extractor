from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / (
    "docs/sprints/2026/08/"
    "20260827-post-fan-in-retry-ordinary-resume-authority-routing-sprint1/"
    "fixtures/post-fan-in-authority-routing-matrix.v1.json"
)

ACTIVE = ["AWAITING_SPEND_AUTHORIZATION", "AUTHORIZED", "SUBMITTING"]
HISTORICAL = ["DETACHED", "FAILED"]
TOP_KEYS = {
    "schema_version", "active_initial_wave_states",
    "historical_initial_wave_states", "cases",
}
CASE_KEYS = {
    "case_id", "route_family", "provider_mechanism", "native_fact",
    "selected_command", "authority_contract", "provider_io",
}


def validate_matrix(value: object) -> dict:
    if not isinstance(value, dict) or set(value) != TOP_KEYS:
        raise ValueError("routing matrix must have one closed top-level shape")
    if value["schema_version"] != (
        "astrowoof.post_fan_in_authority_routing_matrix.v1"
    ):
        raise ValueError("unsupported routing matrix")
    if value["active_initial_wave_states"] != ACTIVE:
        raise ValueError("active initial-wave states are not canonical")
    if value["historical_initial_wave_states"] != HISTORICAL:
        raise ValueError("historical initial-wave states are not canonical")
    if set(ACTIVE) & set(HISTORICAL):
        raise ValueError("active and historical wave states overlap")
    cases = value["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("routing matrix requires cases")
    ids: list[str] = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != CASE_KEYS:
            raise ValueError("routing case must have one closed shape")
        ids.append(case["case_id"])
        if case["route_family"] not in {"exact_natal", "bounded_natal"}:
            raise ValueError("route family is not closed")
        if case["provider_mechanism"] not in {"response", "batch"}:
            raise ValueError("provider mechanism is not closed")
        if case["selected_command"] not in {
            "await_external_authority", "provider_reconciliation_cycle",
            "ordinary_resume", "none",
        }:
            raise ValueError("selected command is not closed")
        if case["provider_io"] not in {"none", "retrieve_only"}:
            raise ValueError("provider I/O is not closed")
    if len(ids) != len(set(ids)):
        raise ValueError("routing case IDs must be unique")
    return value


class PostFanInAuthorityRoutingContractSlice1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_matrix_is_closed_and_covers_four_routes(self) -> None:
        value = validate_matrix(self.fixture)
        routes = {
            (item["route_family"], item["provider_mechanism"])
            for item in value["cases"]
        }
        self.assertEqual({
            ("exact_natal", "response"), ("bounded_natal", "response"),
            ("exact_natal", "batch"), ("bounded_natal", "batch"),
        }, routes)

    def test_three_step_retry_authority_separation_is_explicit(self) -> None:
        cases = {item["case_id"]: item for item in validate_matrix(self.fixture)["cases"]}
        fan_in = cases["exact-interactive-retry-retrieved"]
        self.assertEqual("ordinary_resume", fan_in["selected_command"])
        self.assertEqual("none", fan_in["authority_contract"])
        self.assertEqual("none", fan_in["provider_io"])
        prepared = cases["exact-interactive-next-retry-prepared"]
        self.assertEqual("await_external_authority", prepared["selected_command"])
        self.assertEqual("ordinary_action_v2", prepared["authority_contract"])
        initial = cases["exact-interactive-active-initial-awaiting"]
        self.assertEqual("initial_wave_v1_aggregate", initial["authority_contract"])

    def test_batch_retrieval_is_supported_but_ordinary_v2_dispatch_is_deferred(self) -> None:
        cases = {item["case_id"]: item for item in validate_matrix(self.fixture)["cases"]}
        for route in ("exact", "bounded"):
            due = cases[f"{route}-batch-provider-due"]
            self.assertEqual("provider_reconciliation_cycle", due["selected_command"])
            self.assertEqual("retrieve_only", due["provider_io"])
            prepared = cases[f"{route}-batch-ordinary-prepared"]
            self.assertEqual("none", prepared["selected_command"])
            self.assertEqual(
                "ordinary_batch_v2_deferred", prepared["authority_contract"],
            )

    def test_mutations_fail_closed(self) -> None:
        mutations = []
        extra = copy.deepcopy(self.fixture)
        extra["unexpected"] = True
        mutations.append(extra)
        overlap = copy.deepcopy(self.fixture)
        overlap["historical_initial_wave_states"] = ["DETACHED", "SUBMITTING"]
        mutations.append(overlap)
        unknown_route = copy.deepcopy(self.fixture)
        unknown_route["cases"][0]["route_family"] = "whatever"
        mutations.append(unknown_route)
        unknown_command = copy.deepcopy(self.fixture)
        unknown_command["cases"][0]["selected_command"] = "generic_resume"
        mutations.append(unknown_command)
        duplicate = copy.deepcopy(self.fixture)
        duplicate["cases"][1]["case_id"] = duplicate["cases"][0]["case_id"]
        mutations.append(duplicate)
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_matrix(mutation)


if __name__ == "__main__":
    unittest.main()
