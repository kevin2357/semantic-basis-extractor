from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.payload_recovery_qa import (
    main,
    read_payload_recovery_qualification_schema,
    run_payload_recovery_qualification,
    validate_payload_recovery_qualification,
)


class PayloadRecoveryQualificationTest(unittest.TestCase):
    def test_provider_free_qualification_passes_closed_validator(self) -> None:
        receipt = run_payload_recovery_qualification()
        self.assertEqual(receipt, validate_payload_recovery_qualification(receipt))
        self.assertEqual(1, receipt["provider_create_count"])
        self.assertEqual(0, receipt["external_network_call_count"])

    def test_cli_and_packaged_schema(self) -> None:
        schema = read_payload_recovery_qualification_schema()
        self.assertEqual(
            "astrowoof.external_authority_v2_payload_recovery_qualification.v1",
            schema["$id"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            self.assertEqual(0, main(["--output", str(output)]))
            self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
