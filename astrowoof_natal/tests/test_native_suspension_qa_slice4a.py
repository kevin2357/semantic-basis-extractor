from __future__ import annotations

import copy
import json
import sys
import unittest

from astrowoof_natal_authoring.native_suspension_qa import (
    read_native_suspension_qualification_schema,
    run_native_suspension_qualification,
    validate_native_suspension_qualification,
)


class NativeSuspensionQualificationSlice4ATests(unittest.TestCase):
    @staticmethod
    def _source_command() -> list[str]:
        return [
            sys.executable, "-c",
            "from astrowoof_natal_authoring.cli.external_authority_v2 import main; "
            "raise SystemExit(main())",
        ]

    def test_public_child_process_qualification_passes_provider_free(self):
        receipt = run_native_suspension_qualification(
            v2_command=self._source_command(),
        )
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["provider_create_count"])
        self.assertEqual(0, receipt["live_process_termination_count"])
        self.assertTrue(all(receipt["checks"].values()))

    def test_rehashed_semantic_mutation_refuses(self):
        receipt = run_native_suspension_qualification(
            v2_command=self._source_command(),
        )
        changed = copy.deepcopy(receipt)
        changed["provider_create_count"] = 1
        body = {key: value for key, value in changed.items() if key != "qualification_sha256"}
        import hashlib
        changed["qualification_sha256"] = hashlib.sha256(json.dumps(
            body, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        with self.assertRaisesRegex(ValueError, "semantics differ"):
            validate_native_suspension_qualification(changed)

    def test_packaged_schema_closes_check_inventory(self):
        schema = read_native_suspension_qualification_schema()
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["properties"]["checks"]["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        receipt = run_native_suspension_qualification(
            v2_command=self._source_command(),
        )
        jsonschema.validate(receipt, schema)


if __name__ == "__main__":
    unittest.main()
