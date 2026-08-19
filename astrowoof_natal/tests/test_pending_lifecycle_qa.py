from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.pending_lifecycle_qa import (  # noqa: E402
    run_provider_pending_lifecycle_qualification,
)


class TestPendingLifecycleQualification(unittest.TestCase):
    def test_provider_free_receipt_passes(self) -> None:
        receipt = run_provider_pending_lifecycle_qualification()
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(6, receipt["create_count"])
        self.assertEqual(6, receipt["retrieve_count"])
        self.assertTrue(all(receipt["assertions"].values()))


if __name__ == "__main__":
    unittest.main()
