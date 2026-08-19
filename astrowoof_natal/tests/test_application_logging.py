from __future__ import annotations

import io
import logging
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.application_logging import (  # noqa: E402
    configure_logging,
    logging_context,
)


class TestApplicationLogging(unittest.TestCase):
    def tearDown(self) -> None:
        logging.getLogger().handlers.clear()

    def test_default_prefix_and_scoped_context(self) -> None:
        stream = io.StringIO()
        configure_logging(
            level="DEBUG", host_id="host-fixture",
            invocation_id="invoke-fixture", stream=stream, force=True,
        )
        logger = logging.getLogger("fixture")
        with logging_context(run_id="run-fixture", current_state="WAITING"):
            logger.info("retrieving due Responses count=%s", 4)
        rendered = stream.getvalue()
        self.assertRegex(rendered, r"^✨🐶 \d{4}-\d\d-\d\dT.*Z \| INFO \|")
        self.assertIn(
            "| host-fixture | run-fixture | invoke-fixture | "
            "test_default_prefix_and_scoped_context | WAITING : ", rendered,
        )
        self.assertIn("retrieving due Responses count=4", rendered)

    def test_unknown_context_and_level_filter(self) -> None:
        stream = io.StringIO()
        configure_logging(level="WARNING", host_id="host", stream=stream, force=True)
        logger = logging.getLogger("fixture")
        logger.info("hidden")
        logger.warning("visible")
        self.assertNotIn("hidden", stream.getvalue())
        self.assertIn("| - | - |", stream.getvalue())
        self.assertIn("| - : visible", stream.getvalue())

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


if __name__ == "__main__":
    unittest.main()
