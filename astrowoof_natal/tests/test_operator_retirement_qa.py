from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.operator_retirement_qa import (  # noqa: E402
    read_operator_retirement_qualification_schema,
    run_operator_retirement_qualification,
    validate_operator_retirement_qualification,
)


class TestOperatorRetirementQualification(unittest.TestCase):
    def test_provider_free_public_qualification(self) -> None:
        receipt = run_operator_retirement_qualification()
        validate_operator_retirement_qualification(receipt)
        self.assertEqual("passed", receipt["outcome"])
        self.assertTrue(all(receipt["checks"].values()))
        self.assertEqual(0, receipt["provider_io_performed_count"])

    def test_schema_is_closed_and_valid_when_jsonschema_available(self) -> None:
        schema = read_operator_retirement_qualification_schema()
        self.assertFalse(schema["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency is unavailable")
        receipt = run_operator_retirement_qualification()
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(receipt, schema)

    def test_receipt_rejects_tampering(self) -> None:
        receipt = run_operator_retirement_qualification()
        changed = json.loads(json.dumps(receipt))
        changed["checks"]["zero_provider_io"] = False
        with self.assertRaises(ValueError):
            validate_operator_retirement_qualification(changed)


if __name__ == "__main__":
    unittest.main()
