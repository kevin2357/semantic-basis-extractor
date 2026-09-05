from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.polish_authority_handoff_qa import (
    _digest,
    main,
    read_polish_authority_handoff_qualification_schema,
    run_polish_authority_handoff_qualification,
    validate_polish_authority_handoff_qualification,
)


class PolishAuthorityHandoffQualificationTests(unittest.TestCase):
    def test_provider_free_public_qualification(self) -> None:
        receipt = run_polish_authority_handoff_qualification()
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["provider_create_count"])
        self.assertTrue(all(receipt["checks"].values()))

    def test_rehashed_semantic_mutation_is_rejected(self) -> None:
        receipt = run_polish_authority_handoff_qualification()
        mutated = copy.deepcopy(receipt)
        mutated["checks"]["negative_identity_and_terminal_matrix"] = False
        body = {
            key: value for key, value in mutated.items()
            if key != "receipt_sha256"
        }
        mutated["receipt_sha256"] = _digest(body)
        with self.assertRaises(ValueError):
            validate_polish_authority_handoff_qualification(mutated)

    def test_public_cli_and_packaged_schema(self) -> None:
        schema = read_polish_authority_handoff_qualification_schema()
        self.assertEqual(
            "astrowoof.polish_authority_handoff_qualification.v1", schema["$id"]
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipt.json"
            self.assertEqual(0, main(["--output", str(output)]))
            validate_polish_authority_handoff_qualification(json.loads(
                output.read_text(encoding="utf-8")
            ))

    def test_packaged_schema_rejects_alternate_check_and_case_names(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        schema = read_polish_authority_handoff_qualification_schema()
        for field, replacement in (
            ("negative_cases", ["alternate"] * 6),
            ("checks", {
                "exact_subject_attempt_action_binding_join": True,
                "negative_identity_and_terminal_matrix": True,
                "ordinary_v2_request_exact_action": True,
                "alternate_check": True,
            }),
        ):
            with self.subTest(field=field):
                mutated = run_polish_authority_handoff_qualification()
                mutated[field] = replacement
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.Draft202012Validator(schema).validate(mutated)


if __name__ == "__main__":
    unittest.main()
