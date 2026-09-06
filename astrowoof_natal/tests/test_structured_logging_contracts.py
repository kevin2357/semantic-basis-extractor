from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.structured_logging_contracts import (  # noqa: E402
    read_sbe_worker_log_event_catalog,
    read_sbe_worker_log_schema,
    validate_sbe_worker_log,
)


def _record() -> dict:
    return {
        "schema_version": "astrowoof.sbe_worker_log.v1",
        "record_type": "application_log",
        "timestamp": "2026-09-06T12:34:56.789Z",
        "level": "INFO",
        "event_name": "application_message",
        "message": "✨🐶 lifecycle inspection began",
        "logger": "astrowoof_natal_authoring.lifecycle",
        "function": "inspect_lifecycle",
        "current_state": None,
        "correlation": {
            "api_run_id": None,
            "native_run_id": "native-run-fixture",
            "subject_id": None,
            "invocation_id": "invocation-fixture",
            "action_id": None,
            "provider_operation_id": None,
            "checkpoint_object_id": None,
        },
        "payload": {},
        "producer": {
            "service": "sbe-worker",
            "host_id": "host-fixture",
            "runtime_version": "0.4.test",
        },
        "exception": None,
    }


class TestStructuredLoggingContracts(unittest.TestCase):
    def test_closed_record_and_packaged_resources(self) -> None:
        record = _record()
        validate_sbe_worker_log(record)
        self.assertEqual(
            read_sbe_worker_log_schema()["properties"]["record_type"]["const"],
            "application_log",
        )
        self.assertIn("native_decision_summary", read_sbe_worker_log_event_catalog()["events"])
        try:
            import jsonschema
        except ImportError:
            return
        jsonschema.Draft202012Validator(read_sbe_worker_log_schema()).validate(record)

    def test_unknown_event_and_payload_fields_fail_closed(self) -> None:
        record = _record()
        record["event_name"] = "surprise_event"
        with self.assertRaisesRegex(ValueError, "closed vocabulary"):
            validate_sbe_worker_log(record)
        record = _record()
        record["payload"] = {"prompt_text": "protected"}
        with self.assertRaisesRegex(ValueError, "payload shape"):
            validate_sbe_worker_log(record)

    def test_correlation_is_complete_and_nullable(self) -> None:
        record = _record()
        del record["correlation"]["api_run_id"]
        with self.assertRaisesRegex(ValueError, "correlation shape"):
            validate_sbe_worker_log(record)
        validate_sbe_worker_log(_record())

    def test_exception_is_sanitized_bounded_and_single_line(self) -> None:
        record = _record()
        record["exception"] = {
            "exception_class": "RuntimeError",
            "classification_code": "provider_transport_failure",
            "fingerprint": "a" * 16,
            "sanitized_message": "provider transport failed",
        }
        validate_sbe_worker_log(record)
        for bad in ("line one\nline two", "api_key=super-secret-value"):
            mutated = copy.deepcopy(record)
            mutated["exception"]["sanitized_message"] = bad
            with self.assertRaises(ValueError):
                validate_sbe_worker_log(mutated)

    def test_record_serializes_as_exactly_one_json_line(self) -> None:
        rendered = json.dumps(_record(), ensure_ascii=False, separators=(",", ":"))
        self.assertNotIn("\n", rendered)
        self.assertEqual(json.loads(rendered)["message"], "✨🐶 lifecycle inspection began")


if __name__ == "__main__":
    unittest.main()
