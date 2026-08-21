from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.external_authority_qa import (  # noqa: E402
    read_external_authority_qualification_schema,
    run_external_authority_qualification,
    validate_external_authority_qualification_receipt,
)


class TestExternalAuthorityQualification(unittest.TestCase):
    def test_provider_free_receipt_and_public_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            receipt = run_external_authority_qualification(fixture_dir=fixtures)
            validate_external_authority_qualification_receipt(receipt)
            self.assertEqual("pass", receipt["status"])
            self.assertEqual(
                "astrowoof.external_authority_qualification.v2",
                receipt["schema_version"],
            )
            self.assertEqual(6, receipt["provider_create_count"])
            self.assertEqual(4, len(list(fixtures.glob("*.json"))))
            self.assertTrue(receipt["assertions"]["lifecycle_conditionals_enforced"])
            self.assertTrue(receipt["assertions"][
                "typed_refusal_conditionals_enforced"
            ])

    def test_packaged_schema_validates_receipt_when_jsonschema_is_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed in lean host runtime")
        jsonschema.Draft202012Validator(
            read_external_authority_qualification_schema()
        ).validate(run_external_authority_qualification())

    def test_module_cli_is_provider_free_and_closed(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "astrowoof_natal_authoring.external_authority_qa"],
            check=True, capture_output=True, text=True,
            env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "src")},
        )
        receipt = json.loads(completed.stdout)
        validate_external_authority_qualification_receipt(receipt)
        self.assertFalse(receipt["network_required"])


if __name__ == "__main__":
    unittest.main()
