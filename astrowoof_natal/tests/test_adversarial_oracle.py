from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    adversarial_safety_violations,
    assert_adversarial_oracle,
    build_adversarial_trace_fixture,
    build_review_no_action_runtime_trace,
    classify_adversarial_transition,
    finalize_adversarial_trace,
    inspect_review_no_action_workspace,
    materialize_review_no_action_workspace,
    oracle_semantic_fingerprint,
    read_adversarial_trace_fixture,
)
from tempfile import TemporaryDirectory
from pathlib import Path


class AdversarialOracleTests(unittest.TestCase):
    def test_legitimate_wait_and_contradiction_are_derived(self):
        wait = read_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        contradiction = read_adversarial_trace_fixture(
            "contradictory-command-custody.v1.json"
        )
        self.assertEqual(
            "legitimate_wait", assert_adversarial_oracle(wait)["classification"],
        )
        result = assert_adversarial_oracle(contradiction)
        self.assertEqual("contradictory_evidence", result["classification"])
        self.assertEqual(
            ["command_custody_mismatch"], result["contradictions"],
        )

    def test_muffin_historical_translation_is_stutter(self):
        with TemporaryDirectory() as temporary:
            lifecycle = inspect_review_no_action_workspace(
                materialize_review_no_action_workspace(Path(temporary)),
            )
            trace = build_review_no_action_runtime_trace(
                lifecycle, api_translation="historical",
            )
        self.assertEqual("stutter", assert_adversarial_oracle(trace)["classification"])

    def test_snapshot_revision_republish_cannot_masquerade_as_progress(self):
        trace = build_adversarial_trace_fixture(
            "review-no-action-cycle.v1.json"
        )
        # The v1 trace contract treats the stale-binding checkpoint fence as
        # semantic. The oracle deliberately projects past that publication-only
        # churn when deciding whether useful work advanced.
        trace["expected"]["classification"] = "productive"
        trace["expected"]["progress_witness"] = None
        trace["after"]["native"]["state_revision"] += 99
        trace["after"]["native"]["snapshot_sha256"] = "9" * 64
        trace["after"]["native"]["checkpoint_basis_sha256"] = "8" * 64
        checkpoint_fence = next(
            item for item in trace["after"]["native"]["semantic_fences"]
            if item["kind"] == "checkpoint_basis"
        )
        checkpoint_fence["sha256"] = "8" * 64
        trace = finalize_adversarial_trace(trace)
        self.assertNotEqual(
            trace["before"]["semantic_fingerprint_sha256"],
            trace["after"]["semantic_fingerprint_sha256"],
        )
        self.assertEqual(
            oracle_semantic_fingerprint(trace["before"]),
            oracle_semantic_fingerprint(trace["after"]),
        )
        self.assertEqual(
            "stutter", classify_adversarial_transition(trace)["classification"],
        )

    def test_recurrence_is_cycle_and_wrong_expectation_refuses(self):
        trace = build_adversarial_trace_fixture(
            "review-no-action-cycle.v1.json"
        )
        prior = [oracle_semantic_fingerprint(trace["after"])]
        self.assertEqual(
            "cycle",
            assert_adversarial_oracle(
                trace, prior_semantic_fingerprints=prior,
            )["classification"],
        )
        changed = copy.deepcopy(trace)
        changed["expected"]["classification"] = "stutter"
        changed["expected"]["progress_witness"] = None
        changed = finalize_adversarial_trace(changed)
        with self.assertRaisesRegex(ValueError, "oracle mismatch"):
            assert_adversarial_oracle(
                changed, prior_semantic_fingerprints=prior,
            )

    def test_disabled_event_is_refused(self):
        trace = build_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        trace["event"].update({
            "enabled": False,
            "refusal_reason": "event_not_enabled",
        })
        trace["expected"].update({
            "classification": "refused",
            "declared_contradictions": [],
        })
        trace = finalize_adversarial_trace(trace)
        result = classify_adversarial_transition(trace)
        self.assertEqual("refused", result["classification"])
        self.assertEqual("event_not_enabled", result["refusal_reason"])

    def test_provider_identity_is_retrieval_only(self):
        trace = build_adversarial_trace_fixture(
            "provider-not-due-legitimate-wait.v1.json"
        )
        trace["expected"]["side_effects"]["scripted_provider_creates"] = 1
        trace = finalize_adversarial_trace(trace)
        self.assertIn(
            "provider_identity_recreated", adversarial_safety_violations(trace),
        )

    def test_ambiguity_and_unconsumed_local_work_fail_safety_oracle(self):
        ambiguous = build_adversarial_trace_fixture(
            "review-no-action-cycle.v1.json"
        )
        operation = {
            "correlation_id": "simop_" + "a" * 24,
            "state": "entered_identity_unknown",
        }
        ambiguous["before"]["provider_fixture"]["operations"] = [operation]
        ambiguous["after"]["provider_fixture"]["operations"] = [operation]
        ambiguous["before"]["native"]["provider_custody"] = "ambiguous_or_conflicting"
        ambiguous["after"]["native"]["provider_custody"] = "ambiguous_or_conflicting"
        ambiguous["expected"]["side_effects"]["scripted_provider_creates"] = 1
        ambiguous["expected"]["classification"] = "stutter"
        ambiguous["expected"]["progress_witness"] = None
        ambiguous = finalize_adversarial_trace(ambiguous)
        self.assertIn(
            "ambiguous_submission_not_fenced",
            adversarial_safety_violations(ambiguous),
        )

        local = build_adversarial_trace_fixture(
            "review-no-action-cycle.v1.json"
        )
        operation_key = "opkey_" + "b" * 24
        for label in ("before", "after"):
            local[label]["native"].update({
                "selected_command": "ordinary_resume",
                "capacity_disposition": "continue_local_cycle",
                "reason_code": "local_work_ready",
                "local_operation_keys": [operation_key],
                "review_required": False,
            })
        local["event"].update({"kind": "ordinary_resume", "actor": "sbe_command"})
        local["expected"]["classification"] = "stutter"
        local["expected"]["progress_witness"] = None
        local = finalize_adversarial_trace(local)
        self.assertIn(
            "advertised_local_work_not_consumed",
            adversarial_safety_violations(local),
        )


if __name__ == "__main__":
    unittest.main()
