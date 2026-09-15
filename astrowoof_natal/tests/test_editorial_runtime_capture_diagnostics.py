from __future__ import annotations

import json
import logging
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import astrowoof_natal_authoring.editorial_review_runtime as runtime
from astrowoof_natal_authoring.application_logging import (
    configure_logging,
)


class TestEditorialRuntimeCaptureDiagnostics(unittest.TestCase):
    def setUp(self) -> None:
        root = logging.getLogger()
        self.handlers = list(root.handlers)
        self.level = root.level

    def tearDown(self) -> None:
        root = logging.getLogger()
        for handler in list(root.handlers):
            root.removeHandler(handler)
        for handler in self.handlers:
            root.addHandler(handler)
        root.setLevel(self.level)

    @staticmethod
    def _view(version: str, outcome: str, result_id: str, run_id: str) -> dict:
        return {
            "result": {
                "schema_version": version,
                "outcome": outcome,
                "result_id": result_id,
                "result_sha256": "a" * 64,
                "run_id": run_id,
                "route_binding": {
                    "route_family": "exact_natal",
                    "provider_mechanism": "response",
                },
                "custody_finality": "final",
            },
            "receipt": {
                "schema_version": runtime.RECEIPT_VERSION,
                "receipt_id": "nreceipt_" + "b" * 24,
                "receipt_sha256": "b" * 64,
                "result_id": result_id,
                "run_id": run_id,
            },
            "journal_range": {},
        }

    def _records(self, stream: StringIO) -> list[dict]:
        return [json.loads(line) for line in stream.getvalue().splitlines()]

    def test_typed_unsupported_emits_closed_formatter_records_without_path(self) -> None:
        stream = StringIO()
        configure_logging(stream=stream, force=True)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_id = "run-diagnostic"
            result_id = "nres_" + "c" * 24
            (root / "run.json").write_text(json.dumps({
                "run_id": run_id,
                "service_level": "interactive",
                "subjects": {"subject-diagnostic": {}},
            }), encoding="utf-8")
            branch, value = runtime.build_editorial_review_runtime_capture(
                root,
                result_id,
                exact_reader=lambda *_: self._view(
                    "astrowoof.native_execution_result.v0.3",
                    "review_required",
                    result_id,
                    run_id,
                ),
            )
            self.assertEqual("unsupported", branch)
            self.assertEqual("unsupported_result_version", value["reason"])
            records = self._records(stream)
            self.assertEqual("editorial_runtime_capture_started", records[0]["event_name"])
            self.assertEqual("editorial_runtime_capture_completed", records[-1]["event_name"])
            self.assertEqual("typed_status_construction", records[-2]["payload"]["phase"])
            self.assertNotIn(str(root), stream.getvalue())
            self.assertTrue(all(record["exception"] is None for record in records))

    def test_pre_assembly_typeerror_is_logged_and_reraised_unchanged(self) -> None:
        stream = StringIO()
        configure_logging(stream=stream, force=True)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_id = "run-pre-assembly"
            result_id = "nres_" + "d" * 24
            view = self._view(runtime.DELIVERY_RESULT_VERSION, "delivery_complete", result_id, run_id)
            view["result"].update({
                "sbe_release": "0.4.test",
                "post_checkpoint": {
                    "native_state_revision": 7,
                    "checkpoint_basis_sha256": "e" * 64,
                },
            })
            view["receipt"].update({
                "logical_workspace_root": str(root),
                "checkpoint_basis_sha256": "e" * 64,
                "snapshot_sha256": "f" * 64,
            })
            (root / "run.json").write_text(json.dumps({
                "run_id": run_id,
                "state_revision": 7,
                "service_level": "interactive",
                "subjects": {"subject-pre-assembly": {}},
                "provenance": {
                    "runtime": {"distribution": "astrowoof-natal-authoring", "version": "0.4.test"},
                    "resources": {"aggregate_sha256": "1" * 64},
                },
                "authoring_profile": {"profile_id": "profile-diagnostic"},
                "spend_ledger": {"actions": []},
                "passes": {
                    "first": {"pass_number": 1},
                    "second": {"pass_number": "2"},
                },
            }), encoding="utf-8")
            with self.assertRaises(TypeError) as caught:
                runtime.build_editorial_review_runtime_capture(
                    root, result_id, exact_reader=lambda *_: view,
                )
            error = caught.exception
            record = self._records(stream)[-1]
            self.assertEqual("editorial_runtime_capture_failed", record["event_name"])
            self.assertEqual("pre_assembly_evidence_collection", record["payload"]["phase"])
            self.assertEqual(type(error).__name__, record["payload"]["error_class"])
            self.assertEqual("editorial_review_runtime.py", record["payload"]["source_module"])
            self.assertGreater(record["payload"]["source_line"], 0)
            self.assertNotIn(str(root), stream.getvalue())

    def test_typed_status_double_fault_has_distinct_phase_and_same_exception(self) -> None:
        stream = StringIO()
        configure_logging(stream=stream, force=True)
        result_id = "nres_" + "e" * 24
        double_fault = TypeError("must never be logged")

        def evidence(*_args, **kwargs):
            kwargs["diagnostic_trace"].update({
                "branch": "delivery",
                "native_run_id": "run-double-fault",
                "subject_id": "subject-double-fault",
            })
            return "delivery", {
                "result": {"result_id": result_id, "run_id": "run-double-fault"},
                "receipt": {"result_id": result_id, "run_id": "run-double-fault"},
                "subject_id": "subject-double-fault",
            }

        with (
            patch.object(runtime, "_collect_editorial_review_runtime_evidence", side_effect=evidence),
            patch.object(runtime, "_load", side_effect=ValueError("assembly refusal")),
            patch.object(runtime, "_runtime_capture_status", side_effect=double_fault),
            self.assertRaises(TypeError) as caught,
        ):
            runtime.build_editorial_review_runtime_capture(".", result_id)
        self.assertIs(double_fault, caught.exception)
        record = self._records(stream)[-1]
        self.assertEqual("editorial_runtime_capture_failed", record["event_name"])
        self.assertEqual("typed_status_construction", record["payload"]["phase"])
        self.assertNotIn("must never be logged", stream.getvalue())
        self.assertNotIn("assembly refusal", stream.getvalue())

    def test_logging_handler_failure_does_not_change_typed_result(self) -> None:
        class FailingHandler(logging.Handler):
            def emit(self, _record):
                raise RuntimeError("sink failed")

        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
        root_logger.addHandler(FailingHandler())
        root_logger.setLevel(logging.INFO)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_id = "run-handler-failure"
            result_id = "nres_" + "f" * 24
            (root / "run.json").write_text(json.dumps({
                "run_id": run_id,
                "service_level": "interactive",
                "subjects": {"subject-handler-failure": {}},
            }), encoding="utf-8")
            branch, value = runtime.build_editorial_review_runtime_capture(
                root,
                result_id,
                exact_reader=lambda *_: self._view(
                    "astrowoof.native_execution_result.v0.3",
                    "review_required",
                    result_id,
                    run_id,
                ),
            )
        self.assertEqual("unsupported", branch)
        self.assertEqual("unsupported_result_version", value["reason"])


if __name__ == "__main__":
    unittest.main()
