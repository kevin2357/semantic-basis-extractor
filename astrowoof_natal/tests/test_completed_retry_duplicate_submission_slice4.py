from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    read_duplicate_submission_fence_qualification_schema,
    run_duplicate_submission_fence_qualification,
    validate_duplicate_submission_fence_qualification,
)


class CompletedRetryDuplicateSubmissionSlice4Tests(unittest.TestCase):
    def test_provider_free_qualification_reads_packaged_resources(self) -> None:
        receipt = run_duplicate_submission_fence_qualification()
        validate_duplicate_submission_fence_qualification(receipt)
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["provider_create_count"])
        self.assertTrue(all(receipt["assertions"].values()))

    def test_qualification_validator_is_strict(self) -> None:
        receipt = run_duplicate_submission_fence_qualification()
        for field, replacement in (
            ("provider_create_count", 1),
            ("fixture_bundle_schema_sha256", "0" * 64),
            ("qualification_schema_sha256", "0" * 64),
        ):
            mutated = copy.deepcopy(receipt)
            mutated[field] = replacement
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate_duplicate_submission_fence_qualification(mutated)

    def test_qualification_schema_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        jsonschema.Draft202012Validator(
            read_duplicate_submission_fence_qualification_schema()
        ).validate(run_duplicate_submission_fence_qualification())


if __name__ == "__main__":
    unittest.main()
