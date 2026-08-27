from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.post_fan_in_retry_qa import (
    main,
    read_post_fan_in_retry_fixture,
    read_post_fan_in_retry_qualification_schema,
    run_post_fan_in_retry_qualification,
    validate_post_fan_in_retry_qualification,
)


class PostFanInRetryQualificationTests(unittest.TestCase):
    def test_public_package_exports_are_available(self) -> None:
        import astrowoof_natal_authoring as package

        for name in (
            "read_post_fan_in_retry_fixture",
            "read_post_fan_in_retry_qualification_schema",
            "run_post_fan_in_retry_qualification",
            "validate_post_fan_in_retry_qualification",
        ):
            self.assertTrue(callable(getattr(package, name)))

    def test_provider_free_public_qualification_reaches_pending_endpoint(self) -> None:
        receipt = run_post_fan_in_retry_qualification()
        self.assertEqual("pass", receipt["status"])
        self.assertEqual("detached_provider_pending", receipt["endpoint"])
        self.assertEqual(1, receipt["scripted_retrieval_count"])
        self.assertEqual(1, receipt["scripted_create_count"])
        self.assertEqual(0, receipt["duplicate_create_count"])
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["provider_spend_usd"])

    def test_fixture_and_schema_are_public_and_closed(self) -> None:
        fixture = read_post_fan_in_retry_fixture()
        self.assertEqual("post_fan_in_retry_ordinary_v2", fixture["scenario_id"])
        schema = read_post_fan_in_retry_qualification_schema()
        self.assertFalse(schema["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional in the lean runtime")
        jsonschema.Draft202012Validator(schema).validate(
            run_post_fan_in_retry_qualification(),
        )

    def test_receipt_mutation_fails(self) -> None:
        receipt = run_post_fan_in_retry_qualification()
        changed = copy.deepcopy(receipt)
        changed["duplicate_create_count"] = 1
        with self.assertRaises(ValueError):
            validate_post_fan_in_retry_qualification(changed)

    def test_public_outputs_do_not_contain_private_sentinel_or_paths(self) -> None:
        sentinel = "PRIVATE_POST_FAN_IN_SENTINEL"
        rendered = json.dumps({
            "fixture": read_post_fan_in_retry_fixture(),
            "receipt": run_post_fan_in_retry_qualification(),
        }, sort_keys=True)
        self.assertNotIn(sentinel, rendered)
        self.assertNotIn("run.json", rendered)
        self.assertNotIn("workspace-snapshot.json", rendered)
        self.assertNotIn("resp_fixture", rendered)

    def test_receipt_is_reproducible_across_ephemeral_workspaces(self) -> None:
        first = run_post_fan_in_retry_qualification()
        second = run_post_fan_in_retry_qualification()
        self.assertEqual(first["phases"], second["phases"])
        self.assertEqual(
            first["endpoint_evidence_sha256"],
            second["endpoint_evidence_sha256"],
        )
        self.assertEqual(first["receipt_sha256"], second["receipt_sha256"])
        self.assertEqual(first, second)

    def test_cli_writes_valid_receipt_and_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            receipt_path = Path(temporary) / "receipt.json"
            fixture_path = Path(temporary) / "fixture.json"
            self.assertEqual(0, main(["--output", str(receipt_path)]))
            self.assertEqual(0, main(["--fixture", "--output", str(fixture_path)]))
            validate_post_fan_in_retry_qualification(json.loads(receipt_path.read_text(encoding="utf-8")))
            self.assertEqual(read_post_fan_in_retry_fixture(), json.loads(fixture_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
