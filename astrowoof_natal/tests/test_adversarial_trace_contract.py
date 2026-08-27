from __future__ import annotations

import copy
import json
import unittest

import astrowoof_natal_authoring as public_api
from astrowoof_natal_authoring.adversarial_trace import (
    FIXTURE_NAMES,
    SCHEMA_VERSION,
    build_adversarial_trace_fixture,
    canonical_adversarial_trace_bytes,
    finalize_adversarial_trace,
    read_adversarial_trace_fixture,
    read_adversarial_trace_schema,
    validate_adversarial_trace,
)


class AdversarialTraceContractTests(unittest.TestCase):
    def test_packaged_fixtures_are_canonical_and_deterministic(self):
        for name in sorted(FIXTURE_NAMES):
            with self.subTest(name=name):
                fixture = read_adversarial_trace_fixture(name)
                self.assertEqual(fixture, build_adversarial_trace_fixture(name))
                self.assertEqual(
                    canonical_adversarial_trace_bytes(fixture),
                    json.dumps(
                        fixture, sort_keys=True, separators=(",", ":"),
                        ensure_ascii=False,
                    ).encode("utf-8"),
                )
                validate_adversarial_trace(fixture)

    def test_schema_is_packaged_draft_2020_12(self):
        schema = read_adversarial_trace_schema()
        self.assertEqual(
            schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(schema["properties"]["schema_version"]["const"], SCHEMA_VERSION)

    def test_optional_jsonschema_accepts_all_fixtures(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        validator = jsonschema.Draft202012Validator(read_adversarial_trace_schema())
        for name in sorted(FIXTURE_NAMES):
            validator.validate(read_adversarial_trace_fixture(name))

    def test_public_root_exports_reader_builder_and_validator(self):
        self.assertEqual(public_api.ADVERSARIAL_TRACE_SCHEMA_VERSION, SCHEMA_VERSION)
        fixture = public_api.read_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        public_api.validate_adversarial_trace(fixture)
        self.assertEqual(
            fixture,
            public_api.build_adversarial_trace_fixture(
                "provider-not-due-legitimate-wait.v1.json"
            ),
        )

    def test_review_cycle_is_semantic_stutter_with_starvation_witness(self):
        fixture = read_adversarial_trace_fixture("review-no-action-cycle.v1.json")
        self.assertNotEqual(
            fixture["before"]["raw_evidence_sha256"],
            fixture["after"]["raw_evidence_sha256"],
        )
        self.assertEqual(
            fixture["before"]["semantic_fingerprint_sha256"],
            fixture["after"]["semantic_fingerprint_sha256"],
        )
        self.assertEqual(fixture["expected"]["classification"], "cycle")
        self.assertEqual(
            fixture["expected"]["starvation_witness"]["victim_run_ref"],
            "fixture:api-competing-run",
        )
        self.assertEqual(
            fixture["expected"]["progress_witness"]["prior_semantic_fingerprint_sha256"],
            fixture["before"]["semantic_fingerprint_sha256"],
        )
        self.assertLess(
            fixture["expected"]["progress_witness"]["prior_logical_step"],
            fixture["clock"]["logical_step_before"],
        )

    def test_snapshot_and_revision_churn_are_not_semantic_progress(self):
        fixture = read_adversarial_trace_fixture("review-no-action-cycle.v1.json")
        changed = copy.deepcopy(fixture["before"])
        changed["native"]["snapshot_sha256"] = "f" * 64
        changed["native"]["state_revision"] += 1
        changed["raw_evidence_sha256"] = "e" * 64
        self.assertEqual(
            public_api.adversarial_trace_semantic_fingerprint(changed),
            fixture["before"]["semantic_fingerprint_sha256"],
        )
        changed["native"]["semantic_fences"][0]["sha256"] = "d" * 64
        self.assertNotEqual(
            public_api.adversarial_trace_semantic_fingerprint(changed),
            fixture["before"]["semantic_fingerprint_sha256"],
        )

    def test_refusal_classification_is_biconditional_with_event_admissibility(self):
        original = read_adversarial_trace_fixture("review-no-action-cycle.v1.json")
        refused = copy.deepcopy(original)
        refused["expected"]["classification"] = "refused"
        refused["expected"]["progress_witness"] = None
        refused["event"]["enabled"] = False
        refused["event"]["refusal_reason"] = "stale_observation"
        finalized = finalize_adversarial_trace(refused)
        validate_adversarial_trace(finalized)

        for classification, enabled, reason in (
            ("refused", True, None),
            ("stutter", False, "event_not_enabled"),
            ("refused", False, "made_up_reason"),
        ):
            with self.subTest(classification=classification, enabled=enabled, reason=reason):
                bad = copy.deepcopy(original)
                bad["expected"]["classification"] = classification
                bad["expected"]["progress_witness"] = None
                bad["event"]["enabled"] = enabled
                bad["event"]["refusal_reason"] = reason
                with self.assertRaises(ValueError):
                    finalize_adversarial_trace(bad)

    def test_cycle_requires_prior_recurrence_while_one_step_identity_is_stutter(self):
        original = read_adversarial_trace_fixture("review-no-action-cycle.v1.json")
        missing = copy.deepcopy(original)
        missing["expected"]["progress_witness"] = None
        with self.assertRaisesRegex(ValueError, "recurrence witness"):
            finalize_adversarial_trace(missing)

        one_step = copy.deepcopy(original)
        one_step["expected"]["classification"] = "stutter"
        one_step["expected"]["progress_witness"] = None
        validate_adversarial_trace(finalize_adversarial_trace(one_step))

        bad_step = copy.deepcopy(original)
        bad_step["expected"]["progress_witness"]["prior_logical_step"] = 1
        with self.assertRaisesRegex(ValueError, "must precede"):
            finalize_adversarial_trace(bad_step)

    def test_provider_wait_releases_lease_and_capacity(self):
        fixture = read_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        self.assertEqual(fixture["expected"]["classification"], "legitimate_wait")
        self.assertEqual(fixture["after"]["api_fixture"]["lease_disposition"], "released")
        self.assertEqual(fixture["after"]["api_fixture"]["capacity_state"], "released")
        self.assertIsNotNone(fixture["after"]["native"]["resume_not_before"])

    def test_synthetic_contradiction_declares_exact_error(self):
        fixture = read_adversarial_trace_fixture("contradictory-command-custody.v1.json")
        self.assertEqual(
            fixture["expected"]["declared_contradictions"],
            ["command_custody_mismatch"],
        )
        bad = copy.deepcopy(fixture)
        bad["expected"]["declared_contradictions"] = ["wait_schedule_mismatch"]
        with self.assertRaisesRegex(ValueError, "exact contradictions"):
            finalize_adversarial_trace(bad)

    def test_python_validator_is_strict_without_jsonschema(self):
        original = read_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        mutations = [
            (lambda value: value.update({"surprise": True}), "trace keys differ"),
            (lambda value: value["clock"].update({"logical_step_after": 7}), "advance exactly once"),
            (lambda value: value["clock"].update({"simulated_time_before": "2026-08-27T06:00:00-06:00"}), "canonical UTC"),
            (lambda value: value["route_cell"].update({"provider_mechanism": "carrier_pigeon"}), "unsupported"),
            (lambda value: value["before"]["native"].update({"state_revision": True}), "nonnegative integer"),
            (lambda value: value["public_evidence"][0].update({"opaque_ref": "C:\\\\work\\run.json"}), "not opaque"),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message):
                value = copy.deepcopy(original)
                mutate(value)
                value["trace_sha256"] = public_api.derive_adversarial_trace_sha256(value)
                value["trace_id"] = public_api.derive_adversarial_trace_id(value)
                with self.assertRaisesRegex(ValueError, message):
                    validate_adversarial_trace(value)

    def test_privacy_and_provider_free_guards_fail_closed(self):
        original = read_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        for path in ("network_capability", "credential_capability"):
            with self.subTest(path=path):
                value = copy.deepcopy(original)
                value["before"]["provider_fixture"][path] = True
                with self.assertRaisesRegex(ValueError, "provider-free"):
                    finalize_adversarial_trace(value)
        value = copy.deepcopy(original)
        value["privacy"]["contains_prompt"] = True
        with self.assertRaisesRegex(ValueError, "private material"):
            finalize_adversarial_trace(value)
        serialized = canonical_adversarial_trace_bytes(original).decode("utf-8")
        for sentinel in ("OPENAI_API_KEY", "full prompt sentinel", "resp_real_", "C:\\\\work"):
            self.assertNotIn(sentinel, serialized)

    def test_route_matrix_is_closed(self):
        fixture = read_adversarial_trace_fixture("review-no-action-cycle.v1.json")
        bad = copy.deepcopy(fixture)
        bad["route_cell"].update({
            "provider_mechanism": "batch",
            "stage": "polish",
            "support": "supported",
        })
        with self.assertRaisesRegex(ValueError, "frozen v1 matrix"):
            finalize_adversarial_trace(bad)
        good = copy.deepcopy(fixture)
        good["route_cell"].update({
            "route_family": "bounded_natal",
            "provider_mechanism": "batch",
            "stage": "polish",
            "support": "explicitly_refused",
        })
        finalize_adversarial_trace(good)


if __name__ == "__main__":
    unittest.main()
