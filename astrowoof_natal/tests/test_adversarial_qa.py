from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring import (
    read_adversarial_qualification_schema,
    run_adversarial_qualification,
    validate_adversarial_qualification,
)
from astrowoof_natal_authoring.adversarial_qa import main


class AdversarialQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = run_adversarial_qualification()

    def test_combined_receipt_is_closed_provider_free(self):
        validate_adversarial_qualification(self.receipt)
        self.assertEqual("pass", self.receipt["status"])
        self.assertEqual(22, self.receipt["route_cell_count"])
        self.assertEqual([7, 19, 41], self.receipt["fixed_seeds"])
        self.assertEqual(0, self.receipt["external_network_call_count"])
        self.assertEqual(0, self.receipt["provider_spend_usd"])

    def test_schema_is_packaged_and_structurally_closed(self):
        schema = read_adversarial_qualification_schema()
        self.assertEqual(
            "astrowoof.lifecycle_adversarial_qualification.v1", schema["$id"],
        )
        self.assertFalse(schema["additionalProperties"])

    def test_cli_writes_receipt_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            self.assertEqual(0, main(["--output", str(output)]))
            written = json.loads(output.read_text(encoding="utf-8"))
            validate_adversarial_qualification(written)

    def test_cli_refuses_output_inside_native_workspace_before_qualification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "run.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                main(["--schema", "--output", str(root / "receipt.json")])
            self.assertFalse((root / "receipt.json").exists())

    def test_mutation_fails_closed(self):
        changed = copy.deepcopy(self.receipt)
        changed["fixed_seeds"] = [7]
        with self.assertRaises(ValueError):
            validate_adversarial_qualification(changed)


if __name__ == "__main__":
    unittest.main()
