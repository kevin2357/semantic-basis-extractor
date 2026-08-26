from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.post_fan_in_qa import (
    read_provider_pending_lifecycle_qualification_v2_schema,
    run_provider_pending_lifecycle_qualification_v2,
    validate_provider_pending_lifecycle_qualification_v2,
)


class PostFanInQualificationSlice4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = run_provider_pending_lifecycle_qualification_v2()

    def test_provider_free_v2_receipt_passes(self) -> None:
        self.assertEqual("pass", self.receipt["status"])
        self.assertTrue(all(self.receipt["assertions"].values()))
        self.assertEqual(["exact_natal", "bounded_natal"], [
            item["route_family"] for item in self.receipt["route_results"]
        ])

    def test_reader_is_packaged(self) -> None:
        self.assertEqual(
            "astrowoof.provider_pending_lifecycle_qualification.v2",
            read_provider_pending_lifecycle_qualification_v2_schema()["$id"],
        )

    def test_closed_validator_rejects_extra_and_mutation(self) -> None:
        extra = copy.deepcopy(self.receipt)
        extra["protected_prompt"] = "DO-NOT-LEAK"
        with self.assertRaises(ValueError):
            validate_provider_pending_lifecycle_qualification_v2(extra)
        mutated = copy.deepcopy(self.receipt)
        mutated["route_results"][0]["provider_create_count"] = 1
        with self.assertRaises(ValueError):
            validate_provider_pending_lifecycle_qualification_v2(mutated)

    def test_privacy_sentinel_absent(self) -> None:
        self.assertNotIn("DO-NOT-LEAK", str(self.receipt))


if __name__ == "__main__":
    unittest.main()
