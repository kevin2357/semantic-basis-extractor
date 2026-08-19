from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SOURCE_PYTHONPATH = os.pathsep.join(
    item for item in (str(ROOT / "src"), os.environ.get("PYTHONPATH", ""))
    if item
)

from astrowoof_natal_authoring import smoke as smoke_module  # noqa: E402
from astrowoof_natal_authoring.closure import (  # noqa: E402
    _fake_field_value,
    save_state,
)
from astrowoof_natal_authoring.editorial_lint import (  # noqa: E402
    authoring_pass_acceptance,
    words,
)


class TestReleaseSmokeRuntime(unittest.TestCase):
    def test_built_wheel_runs_required_installed_smoke(self):
        wheel_value = os.environ.get("ASTROWOOF_TEST_INSTALLED_WHEEL")
        if not wheel_value:
            self.skipTest("set ASTROWOOF_TEST_INSTALLED_WHEEL at the release gate")
        wheel = Path(wheel_value).resolve()
        self.assertTrue(wheel.is_file())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / "site-packages"
            subprocess.run(
                [
                    sys.executable, "-m", "pip", "install", "--no-deps",
                    "--target", str(installed), str(wheel),
                ],
                check=True, capture_output=True, text=True,
            )
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(installed)
            completed = subprocess.run(
                [
                    sys.executable, "-m", "astrowoof_natal_authoring.smoke",
                    "--work-dir", str(root / "smoke"), "--require-installed",
                ],
                cwd=root, env=environment, capture_output=True, text=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual("pass", report["status"])
            self.assertEqual("DELIVERY_COMPLETE", report["checks"]["resume"])

    def test_fake_body_identity_survives_production_normalization(self):
        items = []
        normalized_tokens = set()
        for index in range(1, 501):
            value = _fake_field_value(
                pass_id="bre_1",
                relative_file=(
                    f"cards/Story {index:03d} -- claim_{index}/"
                    "WRITE THIS CARD.md"
                ),
                field="card.no_astro.body.handler",
                occurrence=1,
            )
            token = words(value)[1]
            self.assertRegex(token, r"^[a-p]{16}$")
            normalized_tokens.add(token)
            items.append({
                "location": f"card:{index}",
                "claim_id": f"claim_{index}",
                "claim_type": "placement",
                "density": "no_astro",
                "kind": "body",
                "voice": "handler",
                "field": "no_astro.body.handler",
                "text": value,
            })
        self.assertEqual(500, len(normalized_tokens))
        self.assertEqual("accept", authoring_pass_acceptance(items)["status"])

    def test_fake_value_is_independent_of_root_separator_and_call_order(self):
        identities = [
            ("cards/Story 001 -- first/WRITE THIS CARD.md", "card.no_astro.body.handler"),
            ("cards/Story 002 -- second/WRITE THIS CARD.md", "card.light_astro.body.hybrid"),
        ]

        def render(sequence, separator):
            return {
                relative: _fake_field_value(
                    pass_id="bre_1",
                    relative_file=relative.replace("/", separator),
                    field=field,
                    occurrence=1,
                )
                for relative, field in sequence
            }

        forward = render(identities, "/")
        reverse = render(reversed(identities), "\\")
        self.assertEqual(forward, reverse)

    def test_successful_smoke_still_completes_cleanup(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.dict(os.environ, {"PYTHONPATH": SOURCE_PYTHONPATH}):
                report = smoke_module.run_smoke(Path(temporary))
        self.assertEqual("pass", report["status"])
        self.assertEqual("DELIVERY_COMPLETE", report["checks"]["resume"])
        self.assertEqual("complete", report["checks"]["cleanup_status"])
        self.assertGreater(report["checks"]["cleanup_target_count"], 0)

    def test_non_delivery_smoke_is_structured_and_skips_cleanup(self):
        real_run = subprocess.run
        with tempfile.TemporaryDirectory() as temporary:
            work_dir = Path(temporary)

            def complete_then_require_review(*args, **kwargs):
                result = real_run(*args, **kwargs)
                run_json = work_dir / "run" / "run.json"
                if run_json.is_file():
                    state = json.loads(run_json.read_text(encoding="utf-8"))
                    state["subjects"]["bre"]["state"] = "FINAL_QA_WARN"
                    save_state(run_json, state)
                return result

            with (
                patch.dict(os.environ, {"PYTHONPATH": SOURCE_PYTHONPATH}),
                patch.object(
                    smoke_module.subprocess,
                    "run",
                    side_effect=complete_then_require_review,
                ),
            ):
                report = smoke_module.run_smoke(work_dir)

            self.assertEqual("fail", report["status"])
            self.assertEqual(
                "FINAL_QA_REQUIRES_REVIEW", report["checks"]["resume"]
            )
            self.assertEqual(
                "FINAL_QA_WARN",
                report["checks"]["final_qa"]["subject_state"],
            )
            self.assertIn("run did not complete delivery", report["errors"])
            self.assertEqual("skipped", report["checks"]["cleanup_status"])
            self.assertEqual(
                "run_did_not_complete_delivery",
                report["checks"]["cleanup_skip_reason"],
            )
            self.assertFalse(
                (work_dir / "run" / "cleanup-report.json").exists()
            )


if __name__ == "__main__":
    unittest.main()
