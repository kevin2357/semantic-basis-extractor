"""Provider-free installed-wheel route and timing qualification driver."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import astrowoof_natal_authoring as installed


ROUTE_TESTS = [
    "astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure."
    "test_exact_interactive_initial_wave_prepares_authorizes_and_detaches",
    "astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure."
    "test_batch_service_authors_six_passes_and_records_discount",
    "astrowoof_natal.tests.test_bounded_lifecycle.TestBoundedLifecycle."
    "test_openai_interactive_prepares_and_creates_one_six_member_wave",
    "astrowoof_natal.tests.test_bounded_lifecycle.TestBoundedLifecycle."
    "test_bounded_batch_authors_six_members_under_one_round",
]


def main() -> None:
    # Import the installed package before source-only test modules alter sys.path.
    if "site-packages" not in installed.__file__.replace("\\", "/"):
        raise SystemExit(f"SBE did not load from site-packages: {installed.__file__}")
    repository = next(
        parent for parent in Path(__file__).resolve().parents
        if (parent / "astrowoof_natal" / "tests").is_dir()
    )
    sys.path.insert(0, str(repository))
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromNames(ROUTE_TESTS)
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
    from astrowoof_natal.tests.test_initial_wave_qualification import (
        measure_serial_and_concurrent,
    )
    print(json.dumps({
        "installed_module": installed.__file__,
        "installed_version": installed.__version__,
        "route_tests": len(ROUTE_TESTS),
        "timing": measure_serial_and_concurrent(),
    }, indent=2))


if __name__ == "__main__":
    main()
