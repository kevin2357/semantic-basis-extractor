from __future__ import annotations

import io
import json
import logging
import queue
import sys
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.application_logging import (  # noqa: E402
    bind_logging_context,
    configure_logging,
    current_logging_context,
    logging_context,
)
from astrowoof_natal_authoring.structured_logging_contracts import (  # noqa: E402
    validate_sbe_worker_log,
)


class TestApplicationLogging(unittest.TestCase):
    def tearDown(self) -> None:
        logging.getLogger().handlers.clear()

    def test_default_json_and_scoped_context(self) -> None:
        stream = io.StringIO()
        configure_logging(
            level="DEBUG", host_id="host-fixture",
            invocation_id="invoke-fixture", stream=stream, force=True,
        )
        logger = logging.getLogger("fixture")
        with logging_context(run_id="run-fixture", current_state="WAITING"):
            logger.info("retrieving due Responses count=%s", 4)
        rendered = json.loads(stream.getvalue())
        validate_sbe_worker_log(rendered)
        self.assertEqual(rendered["record_type"], "application_log")
        self.assertEqual(rendered["message"], "✨🐶 retrieving due Responses count=4")
        self.assertEqual(rendered["producer"]["host_id"], "host-fixture")
        self.assertEqual(rendered["correlation"]["native_run_id"], "run-fixture")
        self.assertEqual(rendered["correlation"]["invocation_id"], "invoke-fixture")
        self.assertIsNone(rendered["correlation"]["api_run_id"])
        self.assertEqual(rendered["current_state"], "WAITING")

    def test_unknown_context_and_level_filter(self) -> None:
        stream = io.StringIO()
        configure_logging(level="WARNING", host_id="host", stream=stream, force=True)
        logger = logging.getLogger("fixture")
        logger.info("hidden")
        logger.warning("visible")
        self.assertNotIn("hidden", stream.getvalue())
        rendered = json.loads(stream.getvalue())
        self.assertEqual(rendered["message"], "✨🐶 visible")
        self.assertIsNone(rendered["correlation"]["native_run_id"])
        self.assertIsNone(rendered["correlation"]["invocation_id"])

    def test_reconfiguration_replaces_only_the_prior_sbe_handler(self) -> None:
        first = io.StringIO()
        second = io.StringIO()
        foreign = logging.NullHandler()
        logging.getLogger().addHandler(foreign)
        configure_logging(level="INFO", stream=first)
        configure_logging(level="INFO", stream=second)
        logging.getLogger("fixture").info("once")
        self.assertEqual(first.getvalue(), "")
        self.assertEqual(second.getvalue().count("once"), 1)
        self.assertIn(foreign, logging.getLogger().handlers)

    def test_default_logging_uses_stderr_and_does_not_pollute_stdout(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            configure_logging(level="INFO", host_id="host", force=True)
            logging.getLogger("fixture").info("command_start command=lifecycle")
        self.assertEqual("", stdout.getvalue())
        self.assertIn("✨🐶", stderr.getvalue())
        rendered = json.loads(stderr.getvalue())
        self.assertEqual(rendered["message"], "✨🐶 command_start command=lifecycle")

    def test_default_application_log_is_not_an_execution_event_envelope(self) -> None:
        stream = io.StringIO()
        configure_logging(level="INFO", host_id="host", stream=stream, force=True)
        logging.getLogger("fixture").info("command_start command=lifecycle")
        rendered = json.loads(stream.getvalue())
        self.assertEqual(rendered["record_type"], "application_log")
        self.assertNotIn("envelope_type", rendered)

    def test_all_correlation_fields_bind_and_restore_without_inference(self) -> None:
        stream = io.StringIO()
        configure_logging(
            level="INFO", host_id="host", api_run_id="api-run", stream=stream,
            force=True,
        )
        with logging_context(
            native_run_id="native-run", subject_id="subject", action_id="paid-action",
            provider_operation_id="resp-operation", checkpoint_object_id="checkpoint",
            current_state="WAITING",
        ):
            logging.getLogger("fixture").info("inside")
        logging.getLogger("fixture").info("outside")
        inside, outside = [json.loads(line) for line in stream.getvalue().splitlines()]
        self.assertEqual(inside["correlation"], {
            "action_id": "paid-action", "api_run_id": "api-run",
            "checkpoint_object_id": "checkpoint", "invocation_id": None,
            "native_run_id": "native-run", "provider_operation_id": "resp-operation",
            "subject_id": "subject",
        })
        self.assertEqual(outside["correlation"]["api_run_id"], "api-run")
        self.assertIsNone(outside["correlation"]["native_run_id"])
        self.assertIsNone(outside["correlation"]["action_id"])

    def test_contextvars_do_not_leak_to_new_thread(self) -> None:
        configure_logging(level="INFO", host_id="host", force=True)
        bind_logging_context(run_id="parent-run", action_id="parent-action")
        observed: queue.Queue[dict[str, str | None]] = queue.Queue()
        thread = threading.Thread(target=lambda: observed.put(current_logging_context()))
        thread.start()
        thread.join()
        child = observed.get_nowait()
        self.assertIsNone(child["native_run_id"])
        self.assertIsNone(child["action_id"])

    def test_exception_is_one_line_sanitized_json(self) -> None:
        stream = io.StringIO()
        configure_logging(level="INFO", host_id="host", stream=stream, force=True)
        try:
            raise RuntimeError("line one\napi_key=do-not-log-this")
        except RuntimeError:
            logging.getLogger("fixture").exception(
                "provider failed password=do-not-log-this",
                extra={"exception_code": "provider_transport_failure"},
            )
        self.assertEqual(len(stream.getvalue().splitlines()), 1)
        rendered = json.loads(stream.getvalue())
        validate_sbe_worker_log(rendered)
        self.assertNotIn("do-not-log-this", stream.getvalue())
        self.assertEqual(
            rendered["exception"]["classification_code"],
            "provider_transport_failure",
        )

    def test_invalid_structured_extra_falls_back_without_recursion(self) -> None:
        stream = io.StringIO()
        configure_logging(level="INFO", host_id="host", stream=stream, force=True)
        logging.getLogger("fixture").info(
            "will not serialize",
            extra={"event_name": "not_in_catalog", "event_payload": {"secret": "x"}},
        )
        self.assertEqual(len(stream.getvalue().splitlines()), 1)
        rendered = json.loads(stream.getvalue())
        validate_sbe_worker_log(rendered)
        self.assertEqual(rendered["message"], "✨🐶 logging serialization failed")
        self.assertEqual(
            rendered["exception"]["classification_code"],
            "logging_serialization_failed",
        )


if __name__ == "__main__":
    unittest.main()
