from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.cli.operator_disposition import (
    build_parser, main as assessment_main,
)
from astrowoof_natal_authoring.operator_disposition_qa import (
    _materialize_pending_workspace,
    read_operator_disposition_qualification_schema,
    run_operator_disposition_qualification,
    validate_operator_disposition_qualification,
)
from astrowoof_natal_authoring.operator_disposition_fixtures import (
    read_operator_disposition_fixtures,
    validate_operator_disposition_fixtures,
)


class OperatorDispositionPackagingSlice4Tests(unittest.TestCase):
    def test_public_cli_is_read_only_and_has_no_recovery_or_authority_input(self):
        parser = build_parser()
        option_names = {
            option
            for action in parser._actions
            for option in action.option_strings
        }
        self.assertEqual({"-h", "--help", "--run-dir", "--output"}, option_names)
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            root = base / "workspace"
            output = base / "assessment.json"
            _materialize_pending_workspace(root)
            before = {
                item.relative_to(root).as_posix(): item.read_bytes()
                for item in root.rglob("*") if item.is_file()
            }
            self.assertEqual(
                0, assessment_main([
                    "--run-dir", str(root), "--output", str(output),
                ])
            )
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                "provider_pending_known_identity",
                result["native_custody_class"],
            )
            after = {
                item.relative_to(root).as_posix(): item.read_bytes()
                for item in root.rglob("*") if item.is_file()
            }
            self.assertEqual(before, after)

    def test_cli_refuses_output_inside_native_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "workspace"
            _materialize_pending_workspace(root)
            with self.assertRaises(SystemExit):
                assessment_main([
                    "--run-dir", str(root),
                    "--output", str(root / "assessment.json"),
                ])
            self.assertFalse((root / "assessment.json").exists())

    def test_qualification_is_closed_replayable_and_schema_valid(self):
        first = run_operator_disposition_qualification()
        second = run_operator_disposition_qualification()
        self.assertEqual(first, second)
        validate_operator_disposition_qualification(first)
        schema = read_operator_disposition_qualification_schema()
        self.assertEqual(
            "astrowoof.operator_disposition_qualification.v1",
            schema["properties"]["schema_version"]["const"],
        )
        fixtures = read_operator_disposition_fixtures()
        validate_operator_disposition_fixtures(fixtures)
        self.assertEqual(8, len(fixtures["fixtures"]))

    def test_qualification_mutations_are_refused(self):
        original = run_operator_disposition_qualification()
        for mutate in (
            lambda value: value["assertions"].update(
                {"workspace_nonmutating": False}
            ),
            lambda value: value.update({"provider_retrieval_count": 1}),
            lambda value: value.update({"assessment_schema_sha256": "a" * 64}),
            lambda value: value.update({"extra": True}),
        ):
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(original)
                mutate(changed)
                with self.assertRaises(ValueError):
                    validate_operator_disposition_qualification(changed)


if __name__ == "__main__":
    unittest.main()
