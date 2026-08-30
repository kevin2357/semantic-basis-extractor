from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from astrowoof_natal_authoring.retry_lineage_qa import (
    run_retry_lineage_qualification,
    read_retry_lineage_qualification_schema,
    validate_retry_lineage_qualification,
)


class RetryLineageQualificationSlice6Tests(unittest.TestCase):
    def test_provider_free_exact_and_bounded_runtime_story(self) -> None:
        first = run_retry_lineage_qualification()
        second = run_retry_lineage_qualification()
        self.assertEqual(first, second)
        self.assertEqual("pass", first["status"])
        self.assertEqual(0, first["provider_create_count"])
        self.assertEqual(
            ["provider_reconciliation_cycle", "provider_reconciliation_cycle"],
            [item["before"]["selected_command"] for item in first["routes"]],
        )
        self.assertEqual(
            ["retain_for_review", "retain_for_review"],
            [item["after"]["capacity_disposition"] for item in first["routes"]],
        )

    def test_receipt_mutation_and_privacy_sentinel_fail_closed(self) -> None:
        receipt = run_retry_lineage_qualification()
        mutated = copy.deepcopy(receipt)
        mutated["routes"][0]["after"]["capacity_disposition"] = "continue_local_cycle"
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_retry_lineage_qualification(mutated)
        rendered = json.dumps(receipt, sort_keys=True)
        self.assertNotIn("PROTECTED_RETRY_PROMPT_SENTINEL", rendered)

    def test_schema_and_public_cli_surface(self) -> None:
        schema = read_retry_lineage_qualification_schema()
        self.assertEqual(
            "astrowoof.retry_lineage_qualification.v1", schema["$id"],
        )
        try:
            import jsonschema
        except ImportError:
            jsonschema = None
        if jsonschema is not None:
            jsonschema.Draft202012Validator(schema).validate(
                run_retry_lineage_qualification()
            )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            environment = dict(os.environ)
            source = str(Path(__file__).resolve().parents[1] / "src")
            environment["PYTHONPATH"] = source + os.pathsep + environment.get("PYTHONPATH", "")
            subprocess.run([
                sys.executable, "-m", "astrowoof_natal_authoring.retry_lineage_qa",
                "--output", str(output),
            ], check=True, capture_output=True, text=True, env=environment)
            validate_retry_lineage_qualification(json.loads(
                output.read_text(encoding="utf-8")
            ))

    def test_cli_refuses_output_inside_native_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "run.json").write_text("{}\n", encoding="utf-8")
            environment = dict(os.environ)
            source = str(Path(__file__).resolve().parents[1] / "src")
            environment["PYTHONPATH"] = source + os.pathsep + environment.get("PYTHONPATH", "")
            completed = subprocess.run([
                sys.executable, "-m", "astrowoof_natal_authoring.retry_lineage_qa",
                "--output", str(root / "receipt.json"),
            ], capture_output=True, text=True, env=environment)
            self.assertNotEqual(0, completed.returncode)
            self.assertFalse((root / "receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
