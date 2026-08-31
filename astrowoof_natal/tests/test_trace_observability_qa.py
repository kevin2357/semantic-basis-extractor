from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring.trace_observability_qa import (
    read_trace_observability_qualification_schema,
    run_trace_observability_qualification,
    validate_trace_observability_qualification,
)


class TraceObservabilityQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = run_trace_observability_qualification()

    def test_provider_free_exact_and_bounded_receipt(self):
        validated = validate_trace_observability_qualification(self.receipt)
        self.assertEqual(
            [item["route_family"] for item in validated["routes"]],
            ["exact_natal", "bounded_natal"],
        )
        self.assertEqual(validated["external_network_calls"], 0)
        self.assertEqual(validated["provider_create_calls"], 0)
        self.assertEqual(validated["provider_retrieval_calls"], 0)

    def test_receipt_is_reproducible(self):
        repeated = run_trace_observability_qualification()
        self.assertEqual(self.receipt, repeated)

    def test_rehashed_semantic_mutation_is_refused(self):
        mutated = copy.deepcopy(self.receipt)
        mutated["privacy"]["payloads_absent"] = False
        basis = {key: item for key, item in mutated.items() if key != "qualification_sha256"}
        import hashlib, json
        mutated["qualification_sha256"] = hashlib.sha256(json.dumps(
            basis, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        with self.assertRaisesRegex(ValueError, "privacy"):
            validate_trace_observability_qualification(mutated)

    def test_json_schema_when_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        jsonschema.Draft202012Validator(
            read_trace_observability_qualification_schema()
        ).validate(self.receipt)


if __name__ == "__main__":
    unittest.main()
