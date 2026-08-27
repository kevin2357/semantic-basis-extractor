from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.initial_wave import (
    ACTIVE_INITIAL_WAVE_STATES,
    HISTORICAL_INITIAL_WAVE_STATES,
    InitialWaveError,
    classify_initial_wave_state,
    is_active_initial_wave,
)
from astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 import (
    PostFanInRetryAuthorityRoutingSlice0Tests,
)
from astrowoof_natal_authoring import closure


class PostFanInRetryRoutingRuntimeSlice2Tests(
    PostFanInRetryAuthorityRoutingSlice0Tests
):
    def test_active_and_historical_state_sets_are_closed_and_disjoint(self) -> None:
        self.assertEqual({
            "AWAITING_SPEND_AUTHORIZATION", "AUTHORIZED", "SUBMITTING",
        }, set(ACTIVE_INITIAL_WAVE_STATES))
        self.assertEqual({"DETACHED", "FAILED"}, set(HISTORICAL_INITIAL_WAVE_STATES))
        self.assertFalse(ACTIVE_INITIAL_WAVE_STATES & HISTORICAL_INITIAL_WAVE_STATES)
        for state in sorted(ACTIVE_INITIAL_WAVE_STATES):
            self.assertEqual("active", classify_initial_wave_state({"state": state}))
            self.assertTrue(is_active_initial_wave({"state": state}))
        for state in sorted(HISTORICAL_INITIAL_WAVE_STATES):
            self.assertEqual("historical", classify_initial_wave_state({"state": state}))
            self.assertFalse(is_active_initial_wave({"state": state}))
        self.assertEqual("absent", classify_initial_wave_state(None))
        self.assertFalse(is_active_initial_wave(None))

    def test_unknown_or_malformed_wave_state_fails_closed(self) -> None:
        for wave in ({}, {"state": "COMPLETED"}, [], "DETACHED"):
            with self.subTest(wave=wave), self.assertRaises(InitialWaveError) as raised:
                classify_initial_wave_state(wave)
            self.assertEqual("unsupported_contract", raised.exception.reason_code)

    def test_unknown_historical_state_refuses_before_public_resume_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _retry_one, _retry_two = self._openai_workspace(Path(temporary))
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["initial_authoring_wave"]["state"] = "COMPLETED"
            closure.save_state(state_path, state)
            run_before = state_path.read_bytes()
            snapshot_before = (run_dir / "workspace-snapshot.json").read_bytes()
            with self.assertRaises(InitialWaveError) as raised:
                self._run_main([
                    "astrowoof-run-semantic-closure", "--run-dir", str(run_dir),
                    "--resume", "--provider", "openai", "--max-attempts", "3",
                    "--model", "gpt-5.6-luna", "--max-output-tokens", "30000",
                    "--prompt-cache-mode", "disabled", "--log-level", "CRITICAL",
                ])
            self.assertEqual("unsupported_contract", raised.exception.reason_code)
            self.assertEqual(run_before, state_path.read_bytes())
            self.assertEqual(
                snapshot_before, (run_dir / "workspace-snapshot.json").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
