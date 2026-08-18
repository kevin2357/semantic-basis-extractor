from __future__ import annotations

import json
import sys
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.initial_wave import ProviderCreateResult  # noqa: E402
from astrowoof_natal.tests.test_initial_wave import execute, wave  # noqa: E402


SCRIPTED_MEMBER_SECONDS = 0.075


def measure_serial_and_concurrent() -> dict[str, float]:
    value = wave()

    serial_started = time.perf_counter()
    for _member in value["ordered_members"]:
        time.sleep(SCRIPTED_MEMBER_SECONDS)
    serial = time.perf_counter() - serial_started

    concurrent_started = time.perf_counter()
    result = execute(
        value,
        submit=lambda member, _timeout: (
            time.sleep(SCRIPTED_MEMBER_SECONDS)
            or ProviderCreateResult(f"resp_qualification_{member['pass_number']}")
        ),
        persist_member_outcome=lambda _member, _outcome: None,
    )
    concurrent = time.perf_counter() - concurrent_started
    return {
        "scripted_member_seconds": SCRIPTED_MEMBER_SECONDS,
        "serial_elapsed_seconds": serial,
        "concurrent_elapsed_seconds": concurrent,
        "concurrent_to_serial_ratio": concurrent / serial,
        "provider_io_reported_seconds": result["provider_io_elapsed_seconds"],
    }


class TestInitialWaveQualification(unittest.TestCase):
    def test_concurrent_wave_tracks_slowest_member_not_six_member_sum(self) -> None:
        evidence = measure_serial_and_concurrent()
        self.assertGreaterEqual(evidence["serial_elapsed_seconds"], 0.40)
        self.assertLess(evidence["concurrent_elapsed_seconds"], 0.25)
        self.assertLess(evidence["concurrent_to_serial_ratio"], 0.50)
        self.assertLess(evidence["provider_io_reported_seconds"], 0.25)


if __name__ == "__main__":
    if "--measure" in sys.argv:
        print(json.dumps(measure_serial_and_concurrent(), indent=2))
    else:
        unittest.main()
