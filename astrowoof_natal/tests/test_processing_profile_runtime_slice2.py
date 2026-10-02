from __future__ import annotations

import argparse
import unittest
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.processing_profiles import read_processing_profile


PROFILE_ID = "astrowoof.exact_natal.live.compat.v1"
AXIS_AWARE_PROFILE_ID = "astrowoof.exact_natal.live.axisawaresbe.v1"


class ProcessingProfileRuntimeSlice2Tests(unittest.TestCase):
    def _args(self) -> argparse.Namespace:
        return argparse.Namespace(
            processing_profile_id=PROFILE_ID,
            processing_profile_sha256="a" * 64,
            generation_manifest_sha256="b" * 64,
            processing_profile_route_family="exact_natal",
            provider="fake", service_level="batch", routing_policy="fixed",
            model="wrong", reasoning_effort="low", retry_model="wrong",
            retry_reasoning_effort="low", split_assignment_policy="contiguous",
            full_chart_basis_format="legacy", max_workers=1, max_attempts=1,
            max_output_tokens=1, foreground=True, poll_interval_seconds=1.0,
            response_timeout_seconds=1.0, http_timeout_seconds=1.0,
            max_transport_retries=0, transport_backoff_seconds=1.0,
            prompt_cache_mode="disabled", prompt_cache_ttl="30m", polish=False,
            max_polish_attempts=1, polish_model="wrong",
            polish_reasoning_effort="low", qualitative_critic=False,
            critic_model="wrong", critic_reasoning_effort="low",
            qualitative_candidate=False, qualitative_editor_model="wrong",
            qualitative_editor_reasoning_effort="low", exact_natal_policy="axis_aware.v1",
        )

    def test_profile_owned_cli_values_are_replaced_after_exact_resolution(self) -> None:
        profile = read_processing_profile(PROFILE_ID)
        binding = {
            "schema_version": "astrowoof.processing_profile_binding.v1",
            "processing_profile_id": PROFILE_ID,
            "processing_profile_sha256": profile["profile_sha256"],
            "generation_manifest_sha256": "b" * 64,
            "route": profile["route"],
            "selection_policy": profile["selection_policy"],
            "prompt_release": {"release_id": "astrowoof.authoring.compat.v1"},
            "worker_compatibility": {"worker_role": "sbe_authoring"},
        }
        args = self._args()
        with patch.object(closure, "resolve_sbe_authoring_binding", return_value=binding):
            resolved = closure.resolve_processing_profile_args(args, environment="qa")
        self.assertEqual(binding, resolved)
        self.assertEqual("openai", args.provider)
        self.assertEqual("interactive", args.service_level)
        self.assertEqual("cost_optimized", args.routing_policy)
        self.assertEqual("legacy_atomic.v1", args.exact_natal_policy)
        self.assertEqual(6, args.max_workers)
        self.assertTrue(args.polish)
        self.assertTrue(args.qualitative_critic)
        self.assertFalse(args.qualitative_candidate)
        self.assertFalse(args.foreground)

    def test_axis_aware_profile_replaces_the_cli_policy_at_the_command_boundary(self) -> None:
        profile = read_processing_profile(AXIS_AWARE_PROFILE_ID)
        binding = {
            "schema_version": "astrowoof.processing_profile_binding.v1",
            "processing_profile_id": AXIS_AWARE_PROFILE_ID,
            "processing_profile_sha256": profile["profile_sha256"],
            "generation_manifest_sha256": "b" * 64,
            "route": profile["route"],
            "selection_policy": profile["selection_policy"],
            "prompt_release": {"release_id": "astrowoof.authoring.compat.v1"},
            "worker_compatibility": {"worker_role": "sbe_authoring"},
        }
        args = self._args()
        args.exact_natal_policy = "legacy_atomic.v1"
        with patch.object(closure, "resolve_sbe_authoring_binding", return_value=binding):
            resolved = closure.resolve_processing_profile_args(args, environment="qa")
        self.assertEqual(binding, resolved)
        self.assertEqual("axis_aware.v1", args.exact_natal_policy)

    def test_partial_handoff_is_refused_before_any_profile_lookup(self) -> None:
        args = self._args()
        args.processing_profile_sha256 = None
        with self.assertRaisesRegex(ValueError, "exact set"):
            closure.resolve_processing_profile_args(args, environment="qa")

    def test_provider_keeps_profile_prompt_provenance_per_initial_and_retry_stage(self) -> None:
        provider = closure.OpenAIResponsesProvider(
            api_key="provider-free", system_prompts_by_stage={
                "initial": "initial-system", "retry": "retry-system",
            }, prompt_release_provenance_by_stage={
                "initial": {"release_id": "release", "stage": "initial"},
                "retry": {"release_id": "release", "stage": "retry"},
            },
        )
        self.assertEqual("initial-system", provider.system_prompts_by_stage["initial"])
        self.assertEqual("retry-system", provider.system_prompts_by_stage["retry"])
        self.assertEqual(
            "retry", provider.prompt_release_provenance_by_stage["retry"]["stage"],
        )


if __name__ == "__main__":
    unittest.main()
