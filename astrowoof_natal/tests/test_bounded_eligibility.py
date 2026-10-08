from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.bounded_eligibility import (  # noqa: E402
    build_bounded_eligibility_command_result,
    validate_bounded_eligibility_command_result,
)
from astrowoof_natal_authoring.bounded_selection import BoundedSelectionError  # noqa: E402
from astrowoof_natal_authoring.cli.bounded_run import main  # noqa: E402
from astrowoof_natal_authoring.closure import load_json  # noqa: E402
from astrowoof_natal_authoring.processing_profiles import (  # noqa: E402
    read_processing_profile,
    read_prompt_release,
)
from astrowoof_natal_authoring.spend import PRICE_BOOK_VERSION  # noqa: E402
from test_bounded_authoring import compiled  # noqa: E402


RUN_ID = "a" * 64
COMMAND_ATTEMPT_ID = "bca_" + "b" * 24
SOURCE_BINDING = {
    "canonical_semantic_identity_sha256": "c" * 64,
    "projection_set_evidence_sha256": "d" * 64,
}
PROFILE_BINDING = {
    "schema_version": "astrowoof.processing_profile_binding.v1",
    "processing_profile_id": "astrowoof.bounded_natal.live.stable_facts.v1",
    "processing_profile_sha256": "e" * 64,
    "generation_manifest_sha256": "f" * 64,
    "route_family": "bounded_natal",
    "worker_role": "sbe_authoring",
    "worker_compatibility_sha256": "1" * 64,
}

DURABLE_PROFILE_BINDING = {
    "schema_version": "astrowoof.processing_profile_binding.v1",
    "processing_profile_id": PROFILE_BINDING["processing_profile_id"],
    "processing_profile_sha256": PROFILE_BINDING["processing_profile_sha256"],
    "generation_manifest_sha256": PROFILE_BINDING["generation_manifest_sha256"],
    "route": {
        "family": "bounded_natal",
        "execution_mode": "live",
        "sbe_contract": "astrowoof.bounded_natal.authoring_run.v2",
    },
    "selection_policy": "stable_facts_only.v1",
    "prompt_release": {"release_id": "bounded", "release_version": "1.0.0", "release_sha256": "2" * 64, "workspace_components": []},
    "worker_compatibility": {
        "worker_role": "sbe_authoring",
        "compatibility_sha256": PROFILE_BINDING["worker_compatibility_sha256"],
        "required_distributions": [],
    },
}


def spend_policy() -> dict:
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": 20_000_000,
        "stage_ceilings_micro_usd": {
            "authoring_initial": 10_000_000,
            "creative_retry": 1_000_000,
            "polish": 1_000_000,
            "qualitative_critic": 1_000_000,
            "qualitative_candidate": 1_000_000,
        },
        "optional_stage_budget_behavior": {
            "polish": "skip",
            "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


def installed_bounded_binding() -> tuple[dict, dict]:
    profile = read_processing_profile("astrowoof.bounded_natal.live.stable_facts.v2")
    release = read_prompt_release(profile["prompt_release"]["release_id"])
    descriptor = profile["worker_compatibility"]["sbe_authoring"]
    return {
        "schema_version": "astrowoof.processing_profile_binding.v1",
        "processing_profile_id": profile["profile_id"],
        "processing_profile_sha256": profile["profile_sha256"],
        "generation_manifest_sha256": "f" * 64,
        "route": profile["route"],
        "selection_policy": profile["selection_policy"],
        "prompt_release": {
            "release_id": release["release_id"],
            "release_version": release["release_version"],
            "release_sha256": release["release_sha256"],
            "workspace_components": [
                {"logical_name": component["destination"], "sha256": component["sha256"]}
                for component in release["workspace_components"]
            ],
        },
        "worker_compatibility": {
            "worker_role": descriptor["worker_role"],
            "compatibility_sha256": descriptor["compatibility_sha256"],
            "required_distributions": descriptor["required_distributions"],
        },
    }, profile


class TestBoundedEligibility(unittest.TestCase):
    def test_result_is_strict_and_deterministic(self) -> None:
        first = build_bounded_eligibility_command_result(
            native_run_id=RUN_ID,
            command_attempt_id=COMMAND_ATTEMPT_ID,
            source_binding=SOURCE_BINDING,
            processing_profile_binding=PROFILE_BINDING,
        )
        second = build_bounded_eligibility_command_result(
            native_run_id=RUN_ID,
            command_attempt_id=COMMAND_ATTEMPT_ID,
            source_binding=SOURCE_BINDING,
            processing_profile_binding=PROFILE_BINDING,
        )
        self.assertEqual(first, second)
        self.assertEqual("ineligible", first["outcome"])
        self.assertEqual("not_attempted", first["provider_activity"])
        validate_bounded_eligibility_command_result(first)
        tampered = dict(first)
        tampered["provider_activity"] = "attempted"
        with self.assertRaises(ValueError):
            validate_bounded_eligibility_command_result(tampered)

    def test_cli_under_floor_emits_one_envelope_without_workspace_or_provider(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "run"
            argv = [
                "astrowoof-run-bounded-natal",
                "--run-dir", str(run_dir),
                "--input-package", str(root / "input"),
                "--processing-profile-id", PROFILE_BINDING["processing_profile_id"],
                "--processing-profile-sha256", PROFILE_BINDING["processing_profile_sha256"],
                "--generation-manifest-sha256", PROFILE_BINDING["generation_manifest_sha256"],
                "--processing-profile-route-family", "bounded_natal",
                "--native-run-id", RUN_ID,
                "--command-attempt-id", COMMAND_ATTEMPT_ID,
                "--canonical-semantic-identity-sha256", SOURCE_BINDING["canonical_semantic_identity_sha256"],
                "--projection-set-evidence-sha256", SOURCE_BINDING["projection_set_evidence_sha256"],
            ]
            output = io.StringIO()
            with (
                patch("sys.argv", argv),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run._resolve_profile_binding",
                    return_value=(DURABLE_PROFILE_BINDING, {"route": {"family": "bounded_natal"}}),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.admit_bounded_family",
                    return_value=object(),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.load_bounded_family",
                    return_value=[],
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.build_bounded_basis",
                    return_value=object(),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.select_bounded_portfolio",
                    side_effect=BoundedSelectionError("insufficient_invariant_basis", "under floor"),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run._provider",
                    side_effect=AssertionError("provider must not be constructed"),
                ),
                contextlib.redirect_stdout(output),
            ):
                main()
            lines = output.getvalue().splitlines()
            self.assertEqual(1, len(lines))
            envelope = json.loads(lines[0])
            self.assertEqual("sbe.command_result.v1", envelope["schema_version"])
            self.assertEqual("command_result", envelope["envelope_type"])
            validate_bounded_eligibility_command_result(envelope["result"])
            self.assertEqual(PROFILE_BINDING, envelope["result"]["processing_profile_binding"])
            self.assertFalse(run_dir.exists())

    def test_cli_openai_initialization_seals_api_policy_then_awaits_six_authorizations(self) -> None:
        """The real paid CLI stops before any provider submission or network I/O."""
        binding, profile = installed_bounded_binding()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "run"
            policy_path = root / "spend-policy.json"
            policy = spend_policy()
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            argv = [
                "astrowoof-run-bounded-natal",
                "--run-dir", str(run_dir),
                "--input-package", str(root / "input"),
                "--processing-profile-id", binding["processing_profile_id"],
                "--processing-profile-sha256", binding["processing_profile_sha256"],
                "--generation-manifest-sha256", binding["generation_manifest_sha256"],
                "--processing-profile-route-family", "bounded_natal",
                "--native-run-id", RUN_ID,
                "--command-attempt-id", COMMAND_ATTEMPT_ID,
                "--canonical-semantic-identity-sha256", SOURCE_BINDING["canonical_semantic_identity_sha256"],
                "--projection-set-evidence-sha256", SOURCE_BINDING["projection_set_evidence_sha256"],
                "--provider", "openai",
                "--spend-policy", str(policy_path),
            ]
            with (
                patch("sys.argv", argv),
                patch.dict(os.environ, {"OPENAI_API_KEY": "provider-free-test"}),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run._resolve_profile_binding",
                    return_value=(binding, profile),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.load_bounded_family",
                    return_value=[],
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.admit_bounded_family",
                    return_value=object(),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.build_bounded_basis",
                    return_value=object(),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.select_bounded_portfolio",
                    return_value=object(),
                ),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run.compile_bounded_authoring_artifacts",
                    return_value=compiled(),
                ),
                patch(
                    "astrowoof_natal_authoring.bounded_provider.OpenAIBoundedLifecycleProvider.execute",
                    side_effect=AssertionError("provider submission must await authority"),
                ),
                patch(
                    "socket.create_connection",
                    side_effect=AssertionError("network must remain disabled"),
                ),
            ):
                with self.assertRaises(SystemExit) as exited:
                    main()
            self.assertEqual(3, exited.exception.code)
            state = load_json(run_dir / "run.json")
            self.assertEqual(policy, state["spend_ledger"]["policy"])
            self.assertEqual(
                "AWAITING_SPEND_AUTHORIZATION",
                state["initial_authoring_wave"]["state"],
            )
            self.assertEqual(6, len(state["initial_authoring_wave"]["requests"]))
            self.assertEqual(6, len(state["spend_ledger"]["actions"]))
            self.assertTrue(all(
                action["state"] == "PREPARED"
                for action in state["spend_ledger"]["actions"]
            ))
            self.assertFalse(any(
                action.get("provider")
                for action in state["spend_ledger"]["actions"]
            ))

    def test_cli_openai_initialization_requires_valid_policy_before_workspace(self) -> None:
        binding, profile = installed_bounded_binding()
        for policy in (None, {"currency": "USD"}):
            with self.subTest(policy=policy), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                run_dir = root / "run"
                argv = [
                    "astrowoof-run-bounded-natal",
                    "--run-dir", str(run_dir),
                    "--input-package", str(root / "input"),
                    "--processing-profile-id", binding["processing_profile_id"],
                    "--processing-profile-sha256", binding["processing_profile_sha256"],
                    "--generation-manifest-sha256", binding["generation_manifest_sha256"],
                    "--processing-profile-route-family", "bounded_natal",
                    "--native-run-id", RUN_ID,
                    "--command-attempt-id", COMMAND_ATTEMPT_ID,
                    "--canonical-semantic-identity-sha256", SOURCE_BINDING["canonical_semantic_identity_sha256"],
                    "--projection-set-evidence-sha256", SOURCE_BINDING["projection_set_evidence_sha256"],
                    "--provider", "openai",
                ]
                if policy is not None:
                    policy_path = root / "spend-policy.json"
                    policy_path.write_text(json.dumps(policy), encoding="utf-8")
                    argv.extend(["--spend-policy", str(policy_path)])
                with (
                    patch("sys.argv", argv),
                    patch(
                        "astrowoof_natal_authoring.cli.bounded_run._resolve_profile_binding",
                        return_value=(binding, profile),
                    ),
                    patch(
                        "astrowoof_natal_authoring.cli.bounded_run.select_bounded_portfolio",
                        side_effect=AssertionError("selection must not start"),
                    ),
                ):
                    with self.assertRaises(SystemExit) as exited:
                        main()
                self.assertEqual(2, exited.exception.code)
                self.assertFalse(run_dir.exists())

    def test_cli_refuses_policy_replacement_on_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            policy_path = root / "spend-policy.json"
            policy_path.write_text(json.dumps(spend_policy()), encoding="utf-8")
            argv = [
                "astrowoof-run-bounded-natal", "--run-dir", str(root / "run"),
                "--resume", "--spend-policy", str(policy_path),
            ]
            with patch("sys.argv", argv):
                with self.assertRaises(SystemExit) as exited:
                    main()
            self.assertEqual(2, exited.exception.code)


if __name__ == "__main__":
    unittest.main()
