from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_semantic_closure import (
    ROOT,
    SemanticClosureFixture,
    build_story_workspace,
    fill_fake_workspace,
)
from astrowoof_natal_authoring import pass_acceptance


class ThemeGroupQaDormantSlice4Tests(SemanticClosureFixture):
    def test_runtime_gate_never_invokes_theme_group_evaluation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "pass-six"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                0,
                card_start=51,
                include_summaries=True,
                include_theme_plan=True,
                pass_number=6,
                pass_count=6,
                assigned_cards=[],
            )
            fill_fake_workspace(workspace)
            output = Path(temporary) / "acceptance.json"
            stdout = io.StringIO()
            with patch.object(
                pass_acceptance,
                "theme_group_plan_issues",
                side_effect=AssertionError("dormant evaluator was invoked"),
            ), patch.object(
                sys, "argv", ["pass-acceptance", str(workspace), "--output", str(output)]
            ), patch.dict(
                "os.environ", {"ASTROWOOF_OPAQUE_ACCEPTANCE": "1"}
            ), patch("sys.stdout", stdout), self.assertRaises(SystemExit) as exited:
                pass_acceptance.main()

            self.assertEqual(0, exited.exception.code)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("accept", report["status"])
            self.assertEqual([], report["editorial_issue_codes"])
            self.assertEqual([], report["advisory_issue_codes"])

    def test_non_theme_hard_gate_remains_active(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "pass-six"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                1,
                card_start=1,
                include_summaries=False,
                include_theme_plan=False,
                pass_number=1,
                pass_count=6,
            )
            fill_fake_workspace(workspace)
            card_path = next(workspace.rglob("WRITE THIS CARD.md"))
            text = card_path.read_text(encoding="utf-8")
            text = text.replace(
                "<!-- BEGIN FIELD: context_filter_groups.high_level -->\nPersonality",
                "<!-- BEGIN FIELD: context_filter_groups.high_level -->\n- Emotions\n- Trust",
            )
            card_path.write_text(text, encoding="utf-8")
            output = Path(temporary) / "acceptance.json"
            with patch.object(
                pass_acceptance,
                "theme_group_plan_issues",
                side_effect=AssertionError("dormant evaluator was invoked"),
            ), patch.object(
                sys, "argv", ["pass-acceptance", str(workspace), "--output", str(output)]
            ), patch.dict(
                "os.environ", {"ASTROWOOF_OPAQUE_ACCEPTANCE": "1"}
            ), patch("sys.stdout", io.StringIO()), self.assertRaises(SystemExit) as exited:
                pass_acceptance.main()

            self.assertEqual(2, exited.exception.code)
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual("reject", report["status"])
        self.assertEqual(
            ["invalid_context_filter"], report["editorial_issue_codes"]
        )


if __name__ == "__main__":
    unittest.main()
