from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring.closure import (
    main as closure_main, normalized_path, write_workspace_snapshot,
)
from astrowoof_natal_authoring.temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
    validate_external_authority_request_v2_against_inspection,
)


def workspace_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.name.endswith(".lock")
    }


def make_ordinary_run(root: Path) -> Path:
    run_dir = root / "ordinary"
    run_dir.mkdir(parents=True)
    actions = []
    for suffix, stage in (("b", "qualitative_critic"), ("a", "polish")):
        actions.append({
            "action_id": f"paid_{'0' * 23}{suffix}", "state": "PREPARED",
            "binding": {
                "run_id": "run_ordinary_fixture", "profile_sha256": "a" * 64,
                "prepared_state_revision": 21, "stage": stage,
                "route": f"{stage}:attempt-001", "request_sha256": suffix * 64,
                "model": "gpt-5.6-luna", "service_level": "interactive",
                "maximum_output_tokens": 30000, "commitment_micro_usd": 200000,
                "price_book_version": "openai-public-2026-08-07.v1",
            },
        })
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "run_ordinary_fixture", "state_revision": 22,
        "status": "AWAITING_SPEND_AUTHORIZATION", "passes": {}, "subjects": {},
        "provider_configuration": {},
        "authoring_profile": {"qa": {
            "polish": True, "qualitative_critic": True,
            "qualitative_candidate": True,
        }},
        "updated_at": "2026-08-20T14:01:00Z",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "schema_version": "astrowoof.provider_spend_ledger.v0.1",
            "policy": {
                "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 100000000,
                "stage_ceilings_micro_usd": {
                    "authoring_initial": 100000000, "creative_retry": 100000000,
                    "polish": 100000000, "qualitative_critic": 100000000,
                    "qualitative_candidate": 100000000,
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip", "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            },
            "actions": actions,
        },
    }
    (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    write_workspace_snapshot(run_dir)
    return run_dir


class ExternalAuthorityV2ExecutionGapSlice0(unittest.TestCase):
    def test_real_inspection_exports_quiescent_ordinary_v2_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = make_ordinary_run(Path(temporary))
            before = workspace_hashes(run_dir)
            inspection = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-20T15:00:00Z",
            )
            request = build_external_authority_request_v2(inspection)
            validate_external_authority_request_v2_against_inspection(
                request, inspection,
            )
            decision = inspection["temporal_decision"]
            self.assertEqual("await_external_authority", decision["selected_command"])
            self.assertEqual("spend_authorization_required", decision["reason_code"])
            self.assertFalse(decision["eligible_now"])
            self.assertFalse(decision["local_work_ready_now"])
            self.assertEqual([], decision["due_action_ids"])
            self.assertIsNone(decision["not_before"])
            self.assertEqual("ordinary_action_set", request["request_kind"])
            self.assertEqual(sorted(request["ordered_action_ids"]), request["ordered_action_ids"])
            self.assertEqual(before, workspace_hashes(run_dir))

    def test_public_resume_has_no_v2_ordinary_execution_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            run_dir = make_ordinary_run(outer)
            inspection = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-20T15:00:00Z",
            )
            request = build_external_authority_request_v2(inspection)
            request_path = outer / "request-v2.json"
            grant_path = outer / "grant-v2-placeholder.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")
            grant_path.write_text("{}", encoding="utf-8")
            auth_paths = []
            for index in range(2):
                path = outer / f"authorization-{index}.json"
                path.write_text("{}", encoding="utf-8")
                auth_paths.append(path)
            before = workspace_hashes(run_dir)
            argv = [
                "astrowoof-run-closure", "--resume", "--run-dir", str(run_dir),
                "--provider", "openai", "--service-level", "interactive",
                "--external-authority-request", str(request_path),
                "--external-authority-grant", str(grant_path),
            ]
            for path in auth_paths:
                argv.extend(["--spend-authorization", str(path)])
            stderr = StringIO()
            with patch.object(sys, "argv", argv), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as caught:
                    closure_main()
            self.assertEqual(2, caught.exception.code)
            self.assertIn("requires exactly six", stderr.getvalue())
            self.assertEqual(before, workspace_hashes(run_dir))


if __name__ == "__main__":
    unittest.main()
