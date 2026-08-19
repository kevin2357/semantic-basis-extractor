from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.deployed_qa import (  # noqa: E402
    read_deployed_qa_schema,
    run_deployed_qa_qualification,
    validate_deployed_qa_receipt,
)


class TestDeployedQa(unittest.TestCase):
    @staticmethod
    def subprocess_environment() -> dict[str, str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return environment

    def test_four_route_receipt(self) -> None:
        receipt = run_deployed_qa_qualification()
        validate_deployed_qa_receipt(receipt)
        self.assertEqual("pass", receipt["status"])
        self.assertTrue(all(receipt["assertions"].values()))
        self.assertEqual(0, receipt["provider_operation_count"])
        self.assertEqual(
            6, receipt["routes"]["exact_interactive"]["create_count"]
        )
        self.assertEqual(
            1, receipt["routes"]["bounded_batch"]["provider_authority_count"]
        )

    def test_closed_digest_validation(self) -> None:
        receipt = run_deployed_qa_qualification()
        changed = copy.deepcopy(receipt)
        changed["provider_operation_count"] = 1
        with self.assertRaises(ValueError):
            validate_deployed_qa_receipt(changed)
        changed = copy.deepcopy(receipt)
        changed["extra"] = True
        with self.assertRaises(ValueError):
            validate_deployed_qa_receipt(changed)

    def test_module_cli_emits_same_contract(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "astrowoof_natal_authoring.cli.deployed_qa"],
            check=True, capture_output=True, text=True,
            env=self.subprocess_environment(),
        )
        receipt = json.loads(completed.stdout)
        validate_deployed_qa_receipt(receipt)

    def test_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            subprocess.run([
                sys.executable, "-m", "astrowoof_natal_authoring.cli.deployed_qa",
                "--output", str(output),
            ], check=True, env=self.subprocess_environment())
            validate_deployed_qa_receipt(json.loads(output.read_text("utf-8")))

    def test_packaged_schema_is_closed(self) -> None:
        schema = read_deployed_qa_schema()
        self.assertEqual(
            "astrowoof.deployed_qa_four_route_qualification.v1", schema["$id"]
        )
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
