from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring import (
    build_external_authority_v2_command_result_v2,
    read_ambiguous_provider_submission_fixture_v1,
    validate_external_authority_v2_command_result_v2,
)
from astrowoof_natal_authoring.cli.provider_dispatch_result import main


class ProviderDispatchResultCliWaypoint3(unittest.TestCase):
    def test_exports_and_validates_packaged_fixture_without_provider_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixtures.json"
            self.assertEqual(0, main(["--packaged-fixtures", "--output", str(output)]))
            self.assertEqual(
                read_ambiguous_provider_submission_fixture_v1(),
                json.loads(output.read_text(encoding="utf-8")),
            )

    def test_validates_command_result_and_refuses_unknown_schema(self):
        fixture = read_ambiguous_provider_submission_fixture_v1()
        dispatch = next(
            item["result"] for item in fixture["cases"]
            if item["name"] == "missing_payload"
        )
        command = build_external_authority_v2_command_result_v2(
            intent_result=None, dispatch_result=dispatch,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "command.json"
            output = root / "validated.json"
            source.write_text(json.dumps(command), encoding="utf-8")
            self.assertEqual(0, main([
                "--input", str(source), "--output", str(output),
            ]))
            self.assertEqual(
                command,
                validate_external_authority_v2_command_result_v2(
                    json.loads(output.read_text(encoding="utf-8"))
                ),
            )
            source.write_text(json.dumps({"schema_version": "unknown"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported"):
                main(["--input", str(source)])

    def test_input_fixture_bundle_is_closed_and_writes_nothing_on_failure(self):
        malformed = (
            {
                "schema_version": "astrowoof.ambiguous_provider_submission_fixtures.v1",
                "cases": [],
            },
            {
                **read_ambiguous_provider_submission_fixture_v1(),
                "unexpected": True,
            },
        )
        for index, value in enumerate(malformed):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source = root / "fixture.json"
                output = root / "must-not-exist.json"
                source.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "fixture bundle"):
                    main([
                        "--input", str(source), "--output", str(output),
                    ])
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
