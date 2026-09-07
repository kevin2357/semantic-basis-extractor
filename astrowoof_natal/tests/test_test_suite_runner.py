from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "astrowoof_natal" / "scripts" / "run_test_suite.py"
SPEC = importlib.util.spec_from_file_location("astrowoof_test_suite_runner", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TestSuiteRunnerTests(unittest.TestCase):
    def test_supported_default_is_one_worker(self) -> None:
        self.assertEqual(RUNNER.DEFAULT_WORKERS, 1)

    def test_repository_manifest_classifies_every_module_exactly_once(self) -> None:
        manifest = RUNNER.load_manifest(RUNNER.DEFAULT_MANIFEST)
        RUNNER.validate_manifest(manifest)

    def test_weighted_assignment_is_deterministic_and_balances_heavy_modules(self) -> None:
        entries = [
            {"module": "test_heavy.py", "weight_seconds": 10},
            {"module": "test_medium.py", "weight_seconds": 6},
            {"module": "test_light.py", "weight_seconds": 4},
            {"module": "test_tiny.py", "weight_seconds": 1},
        ]
        expected = [["test_heavy.py", "test_tiny.py"], ["test_medium.py", "test_light.py"]]
        self.assertEqual(RUNNER.assign_weighted(entries, 2), expected)
        self.assertEqual(RUNNER.assign_weighted(list(reversed(entries)), 2), expected)

    def test_measurement_selection_does_not_promote_provisional_modules(self) -> None:
        manifest = {
            "parallel_safe": [
                {"module": "test_safe.py", "weight_seconds": 1.0}
            ],
            "provisional": ["test_z.py", "test_a.py"],
            "serial_only": ["test_serial.py"],
        }
        self.assertEqual(
            RUNNER.measurement_modules(manifest, "provisional"),
            ["test_a.py", "test_z.py"],
        )
        self.assertEqual(
            RUNNER.measurement_modules(manifest, "parallel_safe"),
            ["test_safe.py"],
        )
        with self.assertRaisesRegex(ValueError, "unsupported"):
            RUNNER.measurement_modules(manifest, "not-a-class")

    def test_named_measurement_selection_is_closed_to_its_classification(self) -> None:
        manifest = {
            "parallel_safe": [
                {"module": "test_safe.py", "weight_seconds": 1.0}
            ],
            "provisional": ["test_z.py", "test_a.py"],
            "serial_only": ["test_serial.py"],
        }
        self.assertEqual(
            RUNNER.selected_measurement_modules(
                manifest, "provisional", ["test_z.py"]
            ),
            ["test_z.py"],
        )
        with self.assertRaisesRegex(ValueError, "not classified"):
            RUNNER.selected_measurement_modules(
                manifest, "provisional", ["test_serial.py"]
            )
        with self.assertRaisesRegex(ValueError, "duplicate requested"):
            RUNNER.selected_measurement_modules(
                manifest, "provisional", ["test_a.py", "test_a.py"]
            )

    def test_environment_removes_live_credentials(self) -> None:
        cleaned = RUNNER.sanitized_environment(
            {
                "PATH": "safe",
                "OPENAI_API_KEY": "secret",
                "ASTROWOOF_R2_BUCKET": "secret",
                "ASTROWOOF_DATABASE_URL": "secret",
                "ASTROWOOF_OPENAI_API_KEY": "secret",
                "ASTROWOOF_FUTURE_SECRET": "secret",
                "ASTROWOOF_TEST_VERBOSE": "1",
                "RENDER_API_KEY": "secret",
                "DATABASE_URL": "secret",
                "AWS_ACCESS_KEY_ID": "secret",
            }
        )
        self.assertEqual(cleaned, {"PATH": "safe"})

    def test_sanitized_astrowoof_secrets_do_not_reach_subprocess(self) -> None:
        environment = RUNNER.sanitized_environment(
            {
                "PATH": os.environ.get("PATH", ""),
                "ASTROWOOF_DATABASE_URL": "database-secret",
                "ASTROWOOF_OPENAI_API_KEY": "provider-secret",
            }
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import os; print(os.getenv('ASTROWOOF_DATABASE_URL')); "
                    "print(os.getenv('ASTROWOOF_OPENAI_API_KEY'))"
                ),
            ],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.splitlines(), ["None", "None"])

    def test_provisional_modules_remain_in_serial_tail(self) -> None:
        quiet, protected = RUNNER.serial_groups(
            {
                "provisional": ["test_provisional.py"],
                "serial_only": ["test_serial.py", "test_logging.py"],
                "logging_sensitive": ["test_logging.py"],
            }
        )
        self.assertEqual(quiet, ["test_provisional.py", "test_serial.py"])
        self.assertEqual(protected, ["test_logging.py"])

    def test_quiet_bootstrap_suppresses_info_but_not_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            RUNNER._write_quiet_bootstrap(root)
            text = (root / "sitecustomize.py").read_text(encoding="utf-8")
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(root)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import logging; logging.basicConfig(); "
                        "logging.info('hidden'); logging.warning('visible')"
                    ),
                ],
                capture_output=True,
                text=True,
                env=environment,
                check=False,
            )
        self.assertIn("logging.disable(logging.INFO)", text)
        self.assertEqual(completed.returncode, 0)
        self.assertNotIn("hidden", completed.stderr)
        self.assertIn("visible", completed.stderr)

    def test_quiet_bootstrap_does_not_change_parent_logging_threshold(self) -> None:
        import logging

        before = logging.root.manager.disable
        with tempfile.TemporaryDirectory() as temporary:
            RUNNER._write_quiet_bootstrap(Path(temporary))
        self.assertEqual(logging.root.manager.disable, before)

    def test_manifest_rejects_unclassified_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "test_one.py").write_text("", encoding="utf-8")
            manifest = {
                "schema_version": "astrowoof.test-suite-manifest.v1",
                "parallel_safe": [],
                "provisional": [],
                "serial_only": [],
                "logging_sensitive": [],
            }
            with self.assertRaisesRegex(ValueError, "test_one.py"):
                RUNNER.validate_manifest(manifest, root)

    def test_manifest_rejects_duplicate_classification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "test_one.py").write_text("", encoding="utf-8")
            manifest = {
                "schema_version": "astrowoof.test-suite-manifest.v1",
                "parallel_safe": [
                    {"module": "test_one.py", "weight_seconds": 1.0}
                ],
                "provisional": ["test_one.py"],
                "serial_only": [],
                "logging_sensitive": [],
            }
            with self.assertRaisesRegex(ValueError, "duplicate"):
                RUNNER.validate_manifest(manifest, root)

    def test_manifest_rejects_stale_nonexistent_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "test_one.py").write_text("", encoding="utf-8")
            manifest = {
                "schema_version": "astrowoof.test-suite-manifest.v1",
                "parallel_safe": [],
                "provisional": ["test_one.py"],
                "serial_only": ["test_deleted.py"],
                "logging_sensitive": [],
            }
            with self.assertRaisesRegex(ValueError, "test_deleted.py"):
                RUNNER.validate_manifest(manifest, root)

    def test_injected_failure_is_typed_and_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = RUNNER._run_group(
                name="injected",
                modules=["test_terminal_dominance_slice1.py"],
                work_root=Path(temporary),
                quiet=True,
                inject_failure=True,
            )
        self.assertFalse(result["success"])
        self.assertEqual(result["returncode"], 1)
        self.assertEqual(
            result["failures"], ["astrowoof_test_runner.injected_failure"]
        )
        self.assertIn("--inject-failure", result["command"])

    def test_outcome_inventory_is_exact_and_ordered(self) -> None:
        outcomes = RUNNER._outcome_inventory(
            [
                {
                    "test_identities": ["test.z", "test.a"],
                    "skipped": ["test.z"],
                    "expected_failures": [],
                    "unexpected_successes": [],
                    "failures": [],
                    "errors": [],
                }
            ]
        )
        self.assertEqual(outcomes, ["test.a\tpassed", "test.z\tskipped"])


if __name__ == "__main__":
    unittest.main()
