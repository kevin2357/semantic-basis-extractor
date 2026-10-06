from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.bounded_eligibility import (  # noqa: E402
    build_bounded_eligibility_command_result,
    validate_bounded_eligibility_command_result,
)
from astrowoof_natal_authoring.bounded_selection import BoundedSelectionError  # noqa: E402
from astrowoof_natal_authoring.cli.bounded_run import main  # noqa: E402


RUN_ID = "a" * 64
INVOCATION_ID = "ninv_" + "b" * 24
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


class TestBoundedEligibility(unittest.TestCase):
    def test_result_is_strict_and_deterministic(self) -> None:
        first = build_bounded_eligibility_command_result(
            native_run_id=RUN_ID,
            native_invocation_id=INVOCATION_ID,
            source_binding=SOURCE_BINDING,
            processing_profile_binding=PROFILE_BINDING,
        )
        second = build_bounded_eligibility_command_result(
            native_run_id=RUN_ID,
            native_invocation_id=INVOCATION_ID,
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
                "--native-invocation-id", INVOCATION_ID,
                "--canonical-semantic-identity-sha256", SOURCE_BINDING["canonical_semantic_identity_sha256"],
                "--projection-set-evidence-sha256", SOURCE_BINDING["projection_set_evidence_sha256"],
            ]
            output = io.StringIO()
            with (
                patch("sys.argv", argv),
                patch(
                    "astrowoof_natal_authoring.cli.bounded_run._resolve_profile_binding",
                    return_value=(PROFILE_BINDING, {"route": {"family": "bounded_natal"}}),
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
            self.assertFalse(run_dir.exists())


if __name__ == "__main__":
    unittest.main()
