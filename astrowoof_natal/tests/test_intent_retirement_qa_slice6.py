from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    read_intent_retirement_qualification_schema,
    run_intent_retirement_qualification,
    validate_intent_retirement_qualification,
)


class IntentRetirementQualificationSlice6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = run_intent_retirement_qualification()

    def test_closed_provider_free_receipt(self):
        value = validate_intent_retirement_qualification(self.receipt)
        self.assertEqual("pass", value["status"])
        self.assertEqual("exact_replay", value["complete_case"]["replay_outcome"])
        self.assertEqual(1, value["complete_case"]["successor_provider_create_count"])
        self.assertTrue(value["partial_case"]["live_intent_retained"])
        self.assertEqual("native_evidence_invalid", value["conflict_case"]["refusal_reason"])

    def test_schema_and_rehashed_semantic_mutation(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(read_intent_retirement_qualification_schema()).validate(self.receipt)
        changed = copy.deepcopy(self.receipt)
        changed["complete_case"]["successor_provider_create_count"] = 2
        body = {key: item for key, item in changed.items() if key != "receipt_sha256"}
        import hashlib, json
        changed["receipt_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        with self.assertRaises(ValueError):
            validate_intent_retirement_qualification(changed)


if __name__ == "__main__":
    unittest.main()
