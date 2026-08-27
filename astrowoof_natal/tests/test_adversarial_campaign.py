from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    replay_seeded_walk,
    run_seeded_campaign_qualification,
    run_seeded_walk,
    shrink_stutter_counterexample,
    validate_seeded_campaign_qualification,
)


class AdversarialCampaignTests(unittest.TestCase):
    def test_seeded_walk_is_exactly_replayable(self):
        walk = run_seeded_walk(seed=7, route_family="exact_natal", steps=12)
        self.assertEqual(walk, replay_seeded_walk(walk))
        changed = copy.deepcopy(walk)
        changed["seed"] = 8
        with self.assertRaisesRegex(ValueError, "replay differs"):
            replay_seeded_walk(changed)

    def test_shrinker_returns_minimal_semantic_witness(self):
        events = [
            "retrieve:fixture:action-01",
            "adversarial:noop_checkpoint_republish",
            "clock:advance_base_unit",
        ]
        self.assertEqual(
            ["adversarial:noop_checkpoint_republish"],
            shrink_stutter_counterexample(events),
        )
        with self.assertRaisesRegex(ValueError, "does not contain"):
            shrink_stutter_counterexample(["clock:advance_base_unit"])

    def test_campaign_receipt_is_closed_provider_free_and_replayable(self):
        receipt = run_seeded_campaign_qualification()
        validate_seeded_campaign_qualification(receipt)
        self.assertEqual("pass", receipt["status"])
        self.assertEqual({"exact_natal", "bounded_natal"}, {
            item["route_family"] for item in receipt["walks"]
        })
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["provider_spend_usd"])

    def test_mutated_receipt_fails_closed(self):
        receipt = run_seeded_campaign_qualification()
        changed = copy.deepcopy(receipt)
        changed["counterexample"]["shrunk_events"] = []
        with self.assertRaises(ValueError):
            validate_seeded_campaign_qualification(changed)


if __name__ == "__main__":
    unittest.main()
