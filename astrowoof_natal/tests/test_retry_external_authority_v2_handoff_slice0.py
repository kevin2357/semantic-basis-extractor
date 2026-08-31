from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import (
    run_post_fan_in_retry_qualification,
    validate_generic_provider_dispatch_refusal,
    validate_post_fan_in_retry_qualification,
)
from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.lifecycle_contracts import (
    validate_lifecycle_inspection_v05,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from astrowoof_natal_authoring.retry_lineage_contracts import (
    inspect_retry_lineage_lifecycle,
    validate_lifecycle_inspection_v08,
)
from astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 import (
    PostFanInRetryAuthorityRoutingSlice0Tests,
    _resume_arguments,
)


class RetryExternalAuthorityV2HandoffSlice0Tests(
    PostFanInRetryAuthorityRoutingSlice0Tests
):
    """Characterize the released mixed-custody/public-handoff boundary."""

    def _invoke(self, argv: list[str]) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        code = 0
        with patch.object(sys, "argv", argv), patch.dict(
            os.environ, {"OPENAI_API_KEY": "slice-0-no-network"}
        ), patch("sys.stdout", stdout):
            try:
                closure.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, json.loads(stdout.getvalue())

    def test_mixed_custody_is_explicit_in_v07_and_legacy_v05_is_internally_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, provider_bound, providerless = self._openai_workspace(
                Path(temporary)
            )
            legacy = inspect_lifecycle(
                run_dir,
                observed_at="2026-08-30T09:00:00Z",
                native_exclusive_access="declared",
            )
            current = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-08-30T09:00:00Z",
                native_exclusive_access="declared",
            )

            self.assertEqual("ordinary_resume", legacy["execution_branch"]["command"])
            self.assertEqual("local_work_ready", legacy["execution_capacity"]["reason_code"])
            # Completed provider evidence outranks the separately prepared
            # retry even if an older restored outer status still says authority
            # is pending.
            self.assertEqual(
                [
                    {
                        "kind": "local_assembly",
                        "blocking": True,
                        "reason_code": "provider_evidence_ingestion_required",
                    }
                ],
                legacy["local_dependencies"],
            )

            decision = current["temporal_decision"]
            basis = current["checkpoint_basis"]
            self.assertEqual("ordinary_resume", decision["selected_command"])
            self.assertEqual([provider_bound], basis["provider_custody"]["action_ids"])
            operations = basis["local_work_inventory"]["operations"]
            self.assertEqual(1, len(operations))
            self.assertEqual([provider_bound], operations[0]["source_action_ids"])
            # The prepared successor is not yet advertised as authority while
            # predecessor fan-in remains the selected semantic operation.
            self.assertEqual(
                [], basis["external_authority_state"]["ordered_action_ids"]
            )
            action_ids = {
                item["action_id"]: item["state"]
                for item in basis["action_inventory"]["actions"]
            }
            self.assertEqual("PREPARED", action_ids[providerless])

    def test_api_authorization_on_generic_resume_refuses_without_consuming_local_work(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir, provider_bound, providerless = self._openai_workspace(root)
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(
                item
                for item in state["spend_ledger"]["actions"]
                if item["action_id"] == providerless
            )
            authorization = root / "api-authorization.json"
            authorization.write_text(
                json.dumps(
                    {
                        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                        "action_id": providerless,
                        "binding": action["binding"],
                        "authorization_reference": "slice-0:api-admission-only",
                    }
                ),
                encoding="utf-8",
            )
            before = {
                "run": (run_dir / "run.json").read_bytes(),
                "snapshot": (run_dir / "workspace-snapshot.json").read_bytes(),
            }
            creates: list[str] = []
            with patch.object(
                closure.OpenAIResponsesProvider,
                "create_response_only",
                side_effect=lambda *_args, **_kwargs: creates.append("create") or {},
            ):
                code, result = self._invoke(
                    _resume_arguments(run_dir, authorization)
                )

            validate_generic_provider_dispatch_refusal(result)
            self.assertEqual(0, code)
            self.assertEqual("external_authority_v2_dispatch_required", result["reason_code"])
            self.assertEqual([providerless], result["ordered_action_ids"])
            self.assertEqual([], creates)
            self.assertEqual(before["run"], (run_dir / "run.json").read_bytes())
            self.assertEqual(
                before["snapshot"], (run_dir / "workspace-snapshot.json").read_bytes()
            )
            after = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-08-30T09:00:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual("ordinary_resume", after["temporal_decision"]["selected_command"])
            self.assertEqual(
                [provider_bound],
                after["checkpoint_basis"]["local_work_inventory"]["operations"][0][
                    "source_action_ids"
                ],
            )

    def test_completed_retry_beside_pending_retry_has_local_work_but_no_dependency(self) -> None:
        """Characterize the public shape rejected by API's strict v0.5 mapper.

        This is a source-compatible Diffie hypothesis, not a claim that the
        missing live inspection document had these exact bytes.
        """
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, provider_bound, providerless = self._openai_workspace(
                Path(temporary)
            )
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            pending = next(
                action
                for action in state["spend_ledger"]["actions"]
                if action["action_id"] == providerless
            )
            pending["state"] = "WAITING"
            pending["provider"] = {
                "id": "resp_exact_natal_retry_2",
                "kind": "response",
            }
            pending["provider_reconciliation"] = {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-30T08:55:00Z",
                "last_outcome": "pending",
                "resume_not_before": "2026-08-30T09:05:00Z",
            }
            state["status"] = "WAITING_FOR_RESPONSE"
            state["state_revision"] += 1
            closure.save_state(state_path, state)

            legacy = inspect_lifecycle(
                run_dir,
                observed_at="2026-08-30T09:00:00Z",
                native_exclusive_access="declared",
            )
            current = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-08-30T09:00:00Z",
                native_exclusive_access="declared",
            )

            self.assertEqual("ordinary_resume", legacy["execution_branch"]["command"])
            self.assertEqual("local_work_ready", legacy["execution_capacity"]["reason_code"])
            self.assertTrue(legacy["terminal"]["local_continuation_remains"])
            self.assertEqual([], legacy["local_dependencies"])
            operations = current["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ]
            self.assertEqual(1, len(operations))
            self.assertEqual([provider_bound], operations[0]["source_action_ids"])

    def test_legacy_upgrade_witness_joins_v05_v07_v08_on_one_checkpoint(self) -> None:
        """Prove the exact compatibility predicate and public successor joins."""
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, provider_bound, providerless = self._openai_workspace(
                Path(temporary)
            )
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            pending = next(
                action
                for action in state["spend_ledger"]["actions"]
                if action["action_id"] == providerless
            )
            pending["state"] = "WAITING"
            pending["provider"] = {
                "id": "resp_exact_natal_retry_2",
                "kind": "response",
            }
            pending["provider_reconciliation"] = {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-30T08:55:00Z",
                "last_outcome": "pending",
                "resume_not_before": "2026-08-30T09:05:00Z",
            }
            state["status"] = "WAITING_FOR_RESPONSE"
            state["state_revision"] += 1
            closure.save_state(state_path, state)

            observed_at = "2026-08-30T09:00:00Z"
            legacy = inspect_lifecycle(
                run_dir,
                observed_at=observed_at,
                native_exclusive_access="declared",
            )
            local = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at=observed_at,
                native_exclusive_access="declared",
            )
            lineage = inspect_retry_lineage_lifecycle(
                run_dir,
                observed_at=observed_at,
                native_exclusive_access="declared",
            )

            validate_lifecycle_inspection_v05(legacy)
            validate_lifecycle_inspection_v07(local)
            validate_lifecycle_inspection_v08(lineage)

            # Freeze the sole API-only relation which rejects this otherwise
            # coherent native v0.5 document.
            api_predicate_failures = []
            if not legacy["local_dependencies"]:
                api_predicate_failures.append("local_dependency_count")
            self.assertEqual(["local_dependency_count"], api_predicate_failures)
            self.assertEqual("ordinary_resume", legacy["execution_branch"]["command"])
            self.assertTrue(legacy["terminal"]["local_continuation_remains"])
            self.assertTrue(any(
                action["custody_classification"] == "completed_provider_evidence"
                for action in legacy["provider_custody"]["actions"]
            ))

            expected_identity = {
                "run_id": legacy["run_id"],
                "revision": legacy["observation"]["operator_state_revision"],
                "snapshot_sha256": legacy["observation"]["snapshot_sha256"],
                "logical_workspace_root": legacy["observation"][
                    "logical_workspace_root"
                ],
            }
            for successor in (local, lineage):
                observation = successor["checkpoint_basis"]["observation"]
                self.assertEqual(expected_identity, {
                    "run_id": successor["run_id"],
                    "revision": observation["operator_state_revision"],
                    "snapshot_sha256": observation["snapshot_sha256"],
                    "logical_workspace_root": observation["logical_workspace_root"],
                })

            self.assertEqual(
                local["checkpoint_basis"]["local_work_inventory"],
                lineage["checkpoint_basis"]["local_work_inventory"],
            )
            self.assertEqual(
                "ordinary_resume",
                lineage["temporal_decision"]["selected_command"],
            )
            self.assertTrue(lineage["temporal_decision"]["eligible_now"])
            self.assertEqual(
                "continue_local_cycle",
                lineage["temporal_decision"]["capacity_disposition"],
            )
            operations = lineage["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ]
            self.assertEqual(1, len(operations))
            self.assertEqual([provider_bound], operations[0]["source_action_ids"])
            self.assertIn(
                provider_bound,
                lineage["checkpoint_basis"]["provider_custody"]["action_ids"],
            )
            self.assertIn(
                providerless,
                lineage["checkpoint_basis"]["provider_custody"]["action_ids"],
            )

    def test_existing_public_qualification_proves_the_complete_supported_sequence(self) -> None:
        receipt = run_post_fan_in_retry_qualification()
        validate_post_fan_in_retry_qualification(receipt)
        self.assertEqual("detached_provider_pending", receipt["endpoint"])
        self.assertEqual(1, receipt["scripted_retrieval_count"])
        self.assertEqual(1, receipt["scripted_create_count"])
        self.assertEqual(0, receipt["duplicate_create_count"])
        self.assertEqual(0, receipt["external_network_call_count"])
        self.assertEqual(0, receipt["provider_spend_usd"])


if __name__ == "__main__":
    unittest.main()
