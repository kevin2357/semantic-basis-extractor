from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.theme_group_policy_qa import (  # noqa: E402
    read_theme_group_policy_qualification_schema,
    run_theme_group_policy_qualification,
    validate_theme_group_policy_qualification,
)


class ThemeGroupPolicyQualificationTests(unittest.TestCase):
    def test_provider_free_policy_receipt_is_closed_and_deterministic(self):
        first = run_theme_group_policy_qualification()
        second = run_theme_group_policy_qualification()
        self.assertEqual(first, second)
        validate_theme_group_policy_qualification(first)
        self.assertTrue(all(first["assertions"].values()))

    def test_receipt_mutation_is_refused(self):
        changed = copy.deepcopy(run_theme_group_policy_qualification())
        changed["assertions"]["advisory_only_accepts"] = False
        with self.assertRaises(ValueError):
            validate_theme_group_policy_qualification(changed)

    def test_packaged_schema_identity(self):
        schema = read_theme_group_policy_qualification_schema()
        self.assertEqual(
            "astrowoof.theme_group_policy_qualification.v1",
            schema["properties"]["schema_version"]["const"],
        )


if __name__ == "__main__":
    unittest.main()
