from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.run_timeline_qa import (
    main,
    qualification_log,
    read_run_timeline_qualification_schema,
    run_run_timeline_qualification,
    validate_run_timeline_qualification,
)


class RunTimelineQualificationTests(unittest.TestCase):
    def test_public_cli_qualification_is_deterministic_and_closed(self):
        first = run_run_timeline_qualification()
        second = run_run_timeline_qualification()
        self.assertEqual(first, second)
        self.assertEqual({"delivered": 2, "terminal_review": 1}, first["final_postures"])
        self.assertEqual(102, first["witnessed_handoff_duration_ms"])
        self.assertEqual(1, first["open_interval_count"])
        self.assertEqual(1, first["no_progress_candidate_count"])
        self.assertEqual(0, first["provider_call_count"])

    def test_receipt_mutations_fail_closed(self):
        for key, value in (
            ("provider_call_count", 1),
            ("witnessed_handoff_duration_ms", 103),
            ("run_count", 2),
            ("extra", True),
        ):
            changed = copy.deepcopy(run_run_timeline_qualification())
            changed[key] = value
            with self.assertRaises(ValueError):
                validate_run_timeline_qualification(changed)

    def test_schema_is_packaged_and_matches_receipt(self):
        schema = read_run_timeline_qualification_schema()
        self.assertEqual(
            "astrowoof.sbe_run_cohort_timeline_qualification.v1",
            schema["properties"]["schema_version"]["const"],
        )
        self.assertFalse(schema["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(schema).validate(run_run_timeline_qualification())

    def test_cli_writes_valid_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            self.assertEqual(0, main(["--output", str(output)]))
            validate_run_timeline_qualification(json.loads(output.read_text(encoding="utf-8")))

    def test_fixture_is_sanitized(self):
        text = qualification_log()
        for prohibited in (
            "prompt text", "request body", "api_key=", "secret=", "protected-", "https://",
        ):
            self.assertNotIn(prohibited, text.lower())


if __name__ == "__main__":
    unittest.main()
