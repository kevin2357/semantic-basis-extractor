from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_authoring import (  # noqa: E402
    BoundedAuthoringError,
    assert_provider_minimized,
)
from astrowoof_natal_authoring.bounded_basis import BoundedBasis  # noqa: E402
from astrowoof_natal_authoring.bounded_lifecycle import (  # noqa: E402
    FakeBoundedLifecycleProvider,
    run_bounded_authoring,
)
from astrowoof_natal_authoring.bounded_qa import (  # noqa: E402
    QUALIFICATION_CONTRACT,
    qualify_bounded_product,
    validate_upstream_interval_evidence,
)
from astrowoof_natal_authoring.bounded_selection import (  # noqa: E402
    BoundedSelectionError,
    select_bounded_portfolio,
)
from astrowoof_natal_authoring.execution_events import (  # noqa: E402
    ExecutionEventEmitter,
)
from test_bounded_authoring import admission  # noqa: E402
from test_bounded_selection import portfolio_basis  # noqa: E402


INTERVAL_EVIDENCE = [
    {"hours": 1, "evaluation_count": 61, "status": "passed"},
    {"hours": 24, "evaluation_count": 1441, "status": "passed"},
    {"hours": 48, "evaluation_count": 2881, "status": "passed"},
]
PROTECTED = (
    "HANDLER-SEED-NAME",
    "1981-10-10",
    "1981-10-10T13:00:00-06:00",
    "1981-10-10T17:00:00-06:00",
    "America/Denver",
    "39.7392",
    "-104.9903",
    "LOCATION-EVIDENCE-SEED",
    "RAW-EVIDENCE-EXCERPT-SEED",
    "C:\\protected\\workspace\\seed",
    "sk-test-api-key-seed",
    "Bearer authorization-seed",
)


class CapturingProvider(FakeBoundedLifecycleProvider):
    def __init__(self, *, reject_initial: bool = False) -> None:
        self.payloads = []
        self.reject_initial = reject_initial
        self.rejected_once = False

    def execute(self, **kwargs):
        self.payloads.append(deepcopy(kwargs["payload"]))
        result, metadata = super().execute(**kwargs)
        if (
            self.reject_initial
            and kwargs["stage"] == "authoring_initial"
            and result["cards"]
            and not self.rejected_once
        ):
            self.rejected_once = True
            result = deepcopy(result)
            result["cards"][0]["priority_id"] = "injected-retry-trigger"
        return result, metadata


class TestBoundedProductQA(unittest.TestCase):
    def test_upstream_interval_matrix_is_context_not_semantic_authority(self) -> None:
        accepted = validate_upstream_interval_evidence(reversed(INTERVAL_EVIDENCE))
        self.assertEqual([1, 24, 48], [item["hours"] for item in accepted])
        for mutation in (
            INTERVAL_EVIDENCE[:-1],
            [{**item, "confidence": 0.9} for item in INTERVAL_EVIDENCE],
            [{**item, "evaluation_count": 1} for item in INTERVAL_EVIDENCE],
        ):
            with self.assertRaises(ValueError):
                validate_upstream_interval_evidence(mutation)

    def test_route_equivalent_interval_labels_produce_same_exact_fifty_product(self) -> None:
        reports = []
        for record in INTERVAL_EVIDENCE:
            admitted = admission()
            admitted.summary["upstream_interval_qa"] = deepcopy(record)
            _, report = qualify_bounded_product(admitted, portfolio_basis())
            reports.append(report)
            self.assertEqual(QUALIFICATION_CONTRACT, report["schema_version"])
            self.assertEqual(50, report["selected_count"])
            self.assertEqual("invariant_only", report["authority"])
        semantic = [
            (item["selected_sha256"], item["claim_deck_sha256"], item["final_cards_sha256"])
            for item in reports
        ]
        self.assertEqual([semantic[0]] * 3, semantic)

    def test_unavailable_and_inconclusive_features_do_not_create_claims(self) -> None:
        baseline = portfolio_basis()
        reduced = BoundedBasis(
            baseline.candidates,
            {
                **deepcopy(baseline.disposition_report),
                "source_feature_dispositions": {
                    "terrestrial_frame": "inconclusive",
                    "optional_external_objects": "unavailable",
                },
            },
            baseline.summary,
        )
        _, first = qualify_bounded_product(admission(), baseline)
        artifacts, second = qualify_bounded_product(admission(), reduced)
        self.assertEqual(first["selected_sha256"], second["selected_sha256"])
        rendered = json.dumps(artifacts.authoring_packet, sort_keys=True)
        self.assertNotIn("terrestrial_frame", rendered)
        self.assertNotIn("optional_external_objects", rendered)

    def test_large_family_cannot_inflate_selection_and_stays_under_guardrail(self) -> None:
        basis = portfolio_basis()
        expanded = deepcopy(list(basis.candidates))
        target = expanded[20]
        for context, rows in target["context_records"].items():
            seed = rows[0]
            target["context_records"][context] = [
                {
                    **deepcopy(seed),
                    "correspondence_id": f"{seed['correspondence_id']}:stress:{index:03d}",
                    "projection_relevance_score": 1.0 / 300,
                }
                for index in range(300)
            ]
        target["correspondence_ids"] = [
            f"correspondence:020:0:stress:{index:03d}" for index in range(300)
        ]
        target["family_accounting"] = {
            "raw_correspondence_count": 300,
            "independent_support_unit_count": 1,
            "raw_record_count_is_weight": False,
        }
        stressed = BoundedBasis(tuple(expanded), basis.disposition_report, basis.summary)
        _, report = qualify_bounded_product(admission(), stressed)
        self.assertEqual(50, report["selected_count"])
        self.assertLess(report["observed_elapsed_seconds"], 10.0)
        self.assertLess(report["observed_peak_traced_bytes"], 256 * 1024 * 1024)
        self.assertFalse(report["performance_guarantee"])

    def test_repeat_and_serialization_order_are_deterministic(self) -> None:
        basis = portfolio_basis()
        reordered = BoundedBasis(
            tuple(reversed(basis.candidates)),
            deepcopy(basis.disposition_report),
            deepcopy(basis.summary),
        )
        _, first = qualify_bounded_product(admission(), basis)
        _, second = qualify_bounded_product(admission(), reordered)
        for key in (
            "selected_sha256", "claim_deck_sha256", "provider_packet_sha256",
            "final_cards_sha256", "candidate_kinds", "editorial_tiers",
        ):
            self.assertEqual(first[key], second[key])

    def test_privacy_corpus_is_absent_across_every_provider_stage_and_events(self) -> None:
        admitted = admission()
        subject = {
            "subject_id": "dog-uuid",
            "display_name": "Juniper",
            "subject_type": "dog",
            "handler_name": PROTECTED[0],
            "birth_date": PROTECTED[1],
            "birth_datetime": PROTECTED[2],
            "earliest_local": PROTECTED[2],
            "latest_local": PROTECTED[3],
            "timezone": PROTECTED[4],
            "birth_latitude": PROTECTED[5],
            "birth_longitude": PROTECTED[6],
            "location_evidence": PROTECTED[7],
            "evidence_excerpt": PROTECTED[8],
            "workspace_path": PROTECTED[9],
            "api_key": PROTECTED[10],
            "authorization": PROTECTED[11],
        }
        artifacts, _ = qualify_bounded_product(
            admitted, portfolio_basis(), subject=subject,
            protected_values=PROTECTED,
        )
        provider = CapturingProvider(reject_initial=True)
        events = []
        emitter = ExecutionEventEmitter(release="qa", sink=events.append)
        with tempfile.TemporaryDirectory() as temporary:
            state = run_bounded_authoring(
                Path(temporary) / "run", artifacts,
                provider=provider, event_emitter=emitter,
            )
        self.assertEqual("DELIVERY_COMPLETE", state["status"])
        self.assertEqual(
            [
                "authoring_initial", "creative_retry",
                "authoring_initial", "authoring_initial", "authoring_initial",
                "authoring_initial", "authoring_initial", "polish",
                "qualitative_critic", "qualitative_candidate",
            ],
            [payload["stage"] for payload in provider.payloads],
        )
        for payload in provider.payloads:
            assert_provider_minimized(payload, protected_values=PROTECTED)
        rendered_events = json.dumps(events, sort_keys=True)
        for value in PROTECTED:
            self.assertNotIn(value, rendered_events)

    def test_mixed_noninvariant_missing_and_unknown_material_fail_closed(self) -> None:
        mutations = []
        non_invariant = portfolio_basis()
        values = deepcopy(list(non_invariant.candidates))
        values[0]["epistemic_classification"] = "variable"
        mutations.append(BoundedBasis(tuple(values), non_invariant.disposition_report, non_invariant.summary))

        missing = portfolio_basis()
        values = deepcopy(list(missing.candidates))
        values[-1]["member_candidate_ids"] = ["candidate:missing"]
        mutations.append(BoundedBasis(tuple(values), missing.disposition_report, missing.summary))

        unknown = portfolio_basis()
        values = deepcopy(list(unknown.candidates))
        values[0]["foundational_policy"] = "unknown"
        mutations.append(BoundedBasis(tuple(values), unknown.disposition_report, unknown.summary))

        for basis in mutations:
            with self.assertRaises(BoundedSelectionError):
                select_bounded_portfolio(basis)


if __name__ == "__main__":
    unittest.main()
