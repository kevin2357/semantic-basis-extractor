from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import (
    NativeTransitionAvailabilityError,
    read_native_transition_result,
    read_native_transition_result_availability,
    read_native_transition_result_availability_schema,
    validate_native_transition_result_availability,
)
from astrowoof_natal_authoring.cli import native_transition_availability as cli
from astrowoof_natal_authoring.closure import (
    write_json_atomic,
    write_workspace_snapshot,
)
from astrowoof_natal.tests import test_native_transitions as _native_fixtures


class NativeTransitionAvailabilityTests(unittest.TestCase):
    def fixture(self) -> _native_fixtures.TestNativeTransitions:
        return _native_fixtures.TestNativeTransitions(methodName="runTest")

    def test_absent_and_valid_empty_index_are_explicit_none(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.fixture().workspace(Path(temporary))
            absent = read_native_transition_result_availability(run)
            self.assertEqual("none_available", absent["availability"])
            self.assertEqual(0, absent["result_count"])
            self.assertIsNone(absent["latest_result_id"])
            self.assertIsNone(absent["result_index_sha256"])
            validate_native_transition_result_availability(absent)

            write_json_atomic(run / "native-result-index.json", {
                "schema_version": "astrowoof.native_result_index.v0.1",
                "result_ids": [],
            })
            write_workspace_snapshot(run)
            empty = read_native_transition_result_availability(run)
            self.assertEqual("none_available", empty["availability"])
            self.assertIsNotNone(empty["result_index_sha256"])
            self.assertNotEqual(
                absent["workspace_snapshot_sha256"],
                empty["workspace_snapshot_sha256"],
            )

    def test_available_id_is_snapshot_bound_and_joins_exact_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture()
            run = fixture.workspace(Path(temporary))
            result = fixture.publish_review_result(run)
            availability = read_native_transition_result_availability(run)
            self.assertEqual("available", availability["availability"])
            self.assertEqual(1, availability["result_count"])
            self.assertEqual(result["result_id"], availability["latest_result_id"])
            exact = read_native_transition_result(
                run, availability["latest_result_id"]
            )
            self.assertEqual(
                availability["native_run_id"], exact["result"]["run_id"]
            )

            changed = deepcopy(availability)
            changed["workspace_snapshot_sha256"] = "0" * 64
            with self.assertRaises(NativeTransitionAvailabilityError):
                validate_native_transition_result_availability(changed)

    def test_malformed_or_orphaned_evidence_never_becomes_absence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.fixture().workspace(Path(temporary))
            write_json_atomic(run / "native-result-index.json", {
                "schema_version": "astrowoof.native_result_index.v0.1",
                "result_ids": ["hello"],
            })
            write_workspace_snapshot(run)
            with self.assertRaisesRegex(
                NativeTransitionAvailabilityError,
                "availability evidence is invalid",
            ) as raised:
                read_native_transition_result_availability(run)
            self.assertEqual("availability_evidence_invalid", raised.exception.reason_code)

        with tempfile.TemporaryDirectory() as temporary:
            run = self.fixture().workspace(Path(temporary))
            result_dir = run / "native-results"
            result_dir.mkdir()
            (result_dir / "nres_000000000000000000000000.json").write_text(
                "{}\n", encoding="utf-8"
            )
            write_workspace_snapshot(run)
            with self.assertRaises(NativeTransitionAvailabilityError):
                read_native_transition_result_availability(run)

    def test_cli_is_read_only_and_refuses_output_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.fixture().workspace(Path(temporary))
            stdout = io.StringIO()
            with patch.object(sys, "argv", [
                "astrowoof-native-transition-availability",
                "--run-dir", str(run), "--log-level", "CRITICAL",
            ]), redirect_stdout(stdout):
                cli.main()
            value = json.loads(stdout.getvalue())
            self.assertEqual("none_available", value["availability"])

            with patch.object(sys, "argv", [
                "astrowoof-native-transition-availability",
                "--run-dir", str(run), "--output", str(run / "bad.json"),
            ]), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                cli.main()
            self.assertEqual(2, raised.exception.code)
            self.assertFalse((run / "bad.json").exists())

    def test_packaged_schema_and_public_exports(self) -> None:
        schema = read_native_transition_result_availability_schema()
        self.assertEqual(
            "astrowoof.native_transition_result_availability.v1",
            schema["properties"]["schema_version"]["const"],
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator.check_schema(schema)


if __name__ == "__main__":
    unittest.main()
