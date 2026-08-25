from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    read_external_authority_v2_qualification_schema,
    run_external_authority_v2_qualification,
    validate_external_authority_v2_qualification,
)


class ExternalAuthorityV2QualificationSlice5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = run_external_authority_v2_qualification()

    def test_provider_free_holistic_receipt(self):
        receipt = validate_external_authority_v2_qualification(self.receipt)
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["real_provider_create_count"])
        self.assertEqual(0, receipt["real_provider_retrieval_count"])
        for route in receipt["routes"].values():
            self.assertEqual([4, 2], route["retrieval_cycle_counts"])
            self.assertEqual(4, route["ordinary_create_count"])

    def test_schema_and_mutation_refusal(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(
            read_external_authority_v2_qualification_schema()
        ).validate(self.receipt)
        changed = copy.deepcopy(self.receipt)
        changed["real_provider_create_count"] = 1
        with self.assertRaises(ValueError):
            validate_external_authority_v2_qualification(changed)


if __name__ == "__main__":
    unittest.main()
