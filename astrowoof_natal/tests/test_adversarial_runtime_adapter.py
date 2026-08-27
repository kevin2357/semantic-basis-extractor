from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import astrowoof_natal_authoring as public_api
from astrowoof_natal_authoring.adversarial_adapter import (
    build_review_no_action_runtime_trace,
    inspect_review_no_action_workspace,
    materialize_review_no_action_workspace,
)
from astrowoof_natal_authoring.adversarial_trace import validate_adversarial_trace


class AdversarialRuntimeAdapterTests(unittest.TestCase):
    def test_runtime_adapter_is_exported_from_package_root(self):
        self.assertIs(
            public_api.build_review_no_action_runtime_trace,
            build_review_no_action_runtime_trace,
        )
        self.assertIs(
            public_api.inspect_review_no_action_workspace,
            inspect_review_no_action_workspace,
        )

    def test_real_v07_review_result_reproduces_and_corrects_muffin_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = materialize_review_no_action_workspace(Path(temporary))
            lifecycle = inspect_review_no_action_workspace(run_dir)
            decision = lifecycle["temporal_decision"]
            self.assertEqual("none", decision["selected_command"])
            self.assertEqual("retain_for_review", decision["capacity_disposition"])
            self.assertFalse(decision["local_work_ready_now"])
            self.assertEqual(
                [], lifecycle["checkpoint_basis"]["local_work_inventory"]["operations"],
            )

            historical = build_review_no_action_runtime_trace(
                lifecycle, api_translation="historical",
            )
            corrected = build_review_no_action_runtime_trace(
                lifecycle, api_translation="corrected",
            )
            validate_adversarial_trace(historical)
            validate_adversarial_trace(corrected)
            self.assertEqual("stutter", historical["expected"]["classification"])
            self.assertEqual("active", historical["after"]["api_fixture"]["lease_disposition"])
            self.assertEqual("productive", corrected["expected"]["classification"])
            self.assertEqual("released", corrected["after"]["api_fixture"]["lease_disposition"])
            self.assertEqual("released", corrected["after"]["api_fixture"]["capacity_state"])
            self.assertEqual(
                historical["public_evidence"], corrected["public_evidence"],
            )

    def test_adapter_is_provider_free_and_trace_redacts_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = materialize_review_no_action_workspace(Path(temporary))
            lifecycle = inspect_review_no_action_workspace(run_dir)
            trace = build_review_no_action_runtime_trace(
                lifecycle, api_translation="corrected",
            )
            serialized = json.dumps(trace, sort_keys=True)
            self.assertNotIn(str(run_dir), serialized)
            self.assertNotIn("logical_workspace_root", serialized)
            self.assertEqual(0, trace["expected"]["side_effects"]["external_network_calls"])
            self.assertEqual(0, trace["expected"]["side_effects"]["scripted_provider_creates"])
            self.assertEqual(0, trace["expected"]["side_effects"]["scripted_provider_retrievals"])

    def test_unknown_api_translation_refuses(self):
        with tempfile.TemporaryDirectory() as temporary:
            lifecycle = inspect_review_no_action_workspace(
                materialize_review_no_action_workspace(Path(temporary)),
            )
            with self.assertRaisesRegex(ValueError, "unsupported"):
                build_review_no_action_runtime_trace(
                    lifecycle, api_translation="invented",
                )


if __name__ == "__main__":
    unittest.main()
