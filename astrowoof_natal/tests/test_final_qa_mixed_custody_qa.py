from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.final_qa_mixed_custody_qa import (
    main,
    read_final_qa_mixed_custody_qualification_schema,
    run_final_qa_mixed_custody_qualification,
    validate_final_qa_mixed_custody_qualification,
)


class FinalQaMixedCustodyQualificationTests(unittest.TestCase):
    def test_provider_free_qualification(self):
        receipt = run_final_qa_mixed_custody_qualification()
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["real_provider_create_count"])
        self.assertEqual(
            "provider_reconciliation_cycle",
            receipt["pending_case"]["selected_command"],
        )
        self.assertEqual(
            "not_attempted",
            receipt["refusal_case"]["provider_io_disposition"],
        )

    def test_rehashed_semantic_mutation_is_refused(self):
        from astrowoof_natal_authoring.final_qa_mixed_custody_qa import _digest

        receipt = run_final_qa_mixed_custody_qualification()
        mutated = copy.deepcopy(receipt)
        mutated["pending_case"]["selected_command"] = "ordinary_resume"
        body = {
            key: value for key, value in mutated.items()
            if key != "receipt_sha256"
        }
        mutated["receipt_sha256"] = _digest(body)
        with self.assertRaises(ValueError):
            validate_final_qa_mixed_custody_qualification(mutated)

    def test_public_cli_and_schema_reader(self):
        schema = read_final_qa_mixed_custody_qualification_schema()
        self.assertEqual(
            "astrowoof.final_qa_mixed_custody_qualification.v1", schema["$id"]
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            self.assertEqual(0, main(["--output", str(output)]))
            validate_final_qa_mixed_custody_qualification(json.loads(
                output.read_text(encoding="utf-8")
            ))


if __name__ == "__main__":
    unittest.main()
