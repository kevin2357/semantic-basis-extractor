from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring.decision_evidence_observability_qa import (
    read_decision_evidence_observability_qualification_schema,
    run_decision_evidence_observability_qualification,
    validate_decision_evidence_observability_qualification,
)


class DecisionEvidenceObservabilityQualificationTests(unittest.TestCase):
    def test_provider_free_qualification(self):
        value = run_decision_evidence_observability_qualification()
        self.assertEqual(value["external_network_calls"], 0)
        self.assertEqual(value["provider_create_calls"], 0)
        self.assertEqual(value["provider_retrieval_calls"], 0)
        self.assertTrue(value["code_distributions_visible"])
        self.assertEqual(
            sum(item["logs_sufficient"] for item in value["case_classifications"]),
            7,
        )

    def test_closed_validator_rejects_rehashed_semantic_mutation(self):
        value = run_decision_evidence_observability_qualification()
        mutated = copy.deepcopy(value)
        mutated["case_classifications"][0]["logs_sufficient"] = False
        from astrowoof_natal_authoring.decision_evidence_observability_qa import _digest
        mutated["qualification_sha256"] = _digest({
            key: item for key, item in mutated.items()
            if key != "qualification_sha256"
        })
        with self.assertRaisesRegex(ValueError, "replay matrix"):
            validate_decision_evidence_observability_qualification(mutated)

    def test_packaged_schema_accepts_receipt_when_jsonschema_is_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.validate(
            run_decision_evidence_observability_qualification(),
            read_decision_evidence_observability_qualification_schema(),
        )


if __name__ == "__main__":
    unittest.main()
