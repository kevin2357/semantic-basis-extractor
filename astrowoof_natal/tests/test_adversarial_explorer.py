from __future__ import annotations

import copy
import unittest

import astrowoof_natal_authoring as public_api
from astrowoof_natal_authoring.adversarial_explorer import (
    build_action_binding_projection,
    run_systematic_explorer_qualification,
    validate_action_binding_projection,
    validate_systematic_explorer_qualification,
)


def _member(ordinal: int, *, durable: bool = False) -> dict:
    return {
        "action_ref": f"fixture:action-{ordinal:02d}",
        "binding_sha256": f"{ordinal:x}" * 64,
        "create_state": "provider_identity_durable" if durable else "not_entered",
        "create_count": 1 if durable else 0,
        "provider_identity_sha256": (f"{ordinal + 1:x}" * 64) if durable else None,
        "retrieval_count": 0,
    }


class AdversarialExplorerTests(unittest.TestCase):
    def test_action_projection_is_public_strict_and_create_once(self):
        projection = build_action_binding_projection([
            _member(2), _member(1, durable=True),
        ])
        self.assertIs(
            public_api.validate_action_binding_projection,
            validate_action_binding_projection,
        )
        self.assertEqual(
            ["fixture:action-01", "fixture:action-02"],
            [item["action_ref"] for item in projection["members"]],
        )
        duplicate = copy.deepcopy(projection)
        duplicate["members"][0]["create_count"] = 2
        with self.assertRaisesRegex(ValueError, "Create-at-most-once"):
            validate_action_binding_projection(duplicate)

    def test_distinct_action_members_are_not_global_duplicates(self):
        projection = build_action_binding_projection([
            _member(1, durable=True), _member(2),
        ])
        self.assertEqual(1, projection["members"][0]["create_count"])
        self.assertEqual(0, projection["members"][1]["create_count"])
        validate_action_binding_projection(projection)

    def test_systematic_qualification_finds_minimal_witnesses(self):
        receipt = run_systematic_explorer_qualification(max_depth=2)
        validate_systematic_explorer_qualification(receipt)
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(
            1, len(receipt["wave"]["distinct_member_create_witness"]),
        )
        self.assertEqual(
            1, len(receipt["wave"]["duplicate_create_refusal_witness"]),
        )
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["real_provider_create_count"])
        self.assertGreater(receipt["wave"]["deduplicated_successor_count"], 0)

    def test_receipt_mutation_and_bounds_fail_closed(self):
        receipt = run_systematic_explorer_qualification(max_depth=2)
        changed = copy.deepcopy(receipt)
        changed["provider_spend_usd"] = 1
        with self.assertRaises(ValueError):
            validate_systematic_explorer_qualification(changed)
        for depth in (0, 1, 9, True):
            with self.assertRaises(ValueError):
                run_systematic_explorer_qualification(max_depth=depth)


if __name__ == "__main__":
    unittest.main()
