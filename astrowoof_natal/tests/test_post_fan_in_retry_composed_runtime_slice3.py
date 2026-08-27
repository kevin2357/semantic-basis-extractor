from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import (
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    inspect_temporal_lifecycle,
)
from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.post_fan_in_contracts import inspect_post_fan_in_lifecycle
from astrowoof_natal_authoring.reconciliation import reconcile_provider_cycle
from astrowoof_natal_authoring.spend import AwaitingSpendAuthorization
from astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 import (
    PostFanInRetryAuthorityRoutingSlice0Tests,
    _resume_arguments,
)


class PostFanInRetryComposedRuntimeSlice3Tests(
    PostFanInRetryAuthorityRoutingSlice0Tests
):
    def test_exact_public_path_reconciles_fans_in_and_dispatches_one_v2_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, retry_two = self._openai_workspace(Path(temporary))
            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            first = next(
                action for action in state["spend_ledger"]["actions"]
                if action["action_id"] == retry_one
            )
            first["provider_reconciliation"].update({
                "last_outcome": "pending",
                "resume_not_before": "2026-08-27T12:01:00Z",
            })
            state["status"] = "WAITING_FOR_RESPONSE"
            closure.save_state(state_path, state)

            not_due = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-27T12:00:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                not_due["temporal_decision"]["selected_command"],
            )
            self.assertFalse(not_due["temporal_decision"]["eligible_now"])
            before = state_path.read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()
            retrievals: list[str] = []
            not_due_cycle = reconcile_provider_cycle(
                run_dir, observed_at="2026-08-27T12:00:00Z",
                retrieve=lambda provider_id, _timeout: retrievals.append(provider_id) or {},
            )
            self.assertEqual("not_due", not_due_cycle["outcome"])
            self.assertEqual([], retrievals)
            self.assertEqual(
                before,
                (state_path.read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()),
            )

            def retrieve(provider_id: str, _timeout: float) -> dict:
                retrievals.append(provider_id)
                return {"id": provider_id, "status": "completed", "output": []}

            due_cycle = reconcile_provider_cycle(
                run_dir, observed_at="2026-08-27T12:01:00Z", retrieve=retrieve,
            )
            self.assertEqual("progressed_local", due_cycle["outcome"])
            self.assertEqual(["resp_exact_natal_retry_1"], retrievals)
            self.assertEqual(
                [retry_one], due_cycle["cycle"]["completed_action_ids"],
            )
            local = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-27T12:01:01Z",
                native_exclusive_access="declared",
            )
            self.assertEqual("ordinary_resume", local["temporal_decision"]["selected_command"])
            operation_key = local["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]["operation_key"]

            def fan_in(**kwargs: object) -> None:
                native = kwargs["state"]
                reported = next(
                    action for action in native["spend_ledger"]["actions"]
                    if action["action_id"] == retry_one
                )
                reported["state"] = "REPORTED"
                reported["reported"] = {"estimated_micro_usd": 0}
                closure.save_state(kwargs["run_json"], native)
                raise AwaitingSpendAuthorization(
                    "fresh ordinary retry authority required",
                    action=next(
                        action for action in native["spend_ledger"]["actions"]
                        if action["action_id"] == retry_two
                    ),
                )

            with patch.object(
                closure, "author_pending_passes", side_effect=fan_in,
            ), self.assertRaises(AwaitingSpendAuthorization):
                self._run_main(_resume_arguments(run_dir))

            successor = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-27T12:01:02Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "await_external_authority",
                successor["temporal_decision"]["selected_command"],
            )
            self.assertEqual(
                [operation_key], successor["checkpoint_basis"]["local_work_inventory"][
                    "consumed_operation_keys"
                ],
            )

            inspection = inspect_temporal_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-27T12:01:02Z",
            )
            request = build_external_authority_request_v2(inspection)
            self.assertEqual([retry_two], request["ordered_action_ids"])
            native = json.loads(state_path.read_text(encoding="utf-8"))
            prepared = next(
                action for action in native["spend_ledger"]["actions"]
                if action["action_id"] == retry_two
            )
            document = {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": retry_two,
                "binding": copy.deepcopy(prepared["binding"]),
                "authorization_reference": "slice3:ordinary-v2",
            }
            grant = build_external_authority_grant_v2(
                request, inspection, [document], api_decision_id="slice3:ordinary-v2",
                issuer="astrowoof-api-provider-free",
                issued_at="2026-08-27T12:01:03Z",
            )
            commit_external_authority_v2_dispatch_intent(
                run_dir, request=request, inspection=inspection, grant=grant,
                authorization_documents=[document],
            )
            creates: list[str] = []
            dispatched = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: (
                    creates.append(action["action_id"])
                    or {"id": "resp_slice3_retry_2", "kind": "response"}
                ),
            )
            self.assertEqual("detached_provider_pending", dispatched["outcome"])
            self.assertEqual([retry_two], creates)
            replay = dispatch_external_authority_v2_intent(
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                create=lambda action: creates.append(action["action_id"]) or {},
            )
            self.assertEqual("exact_replay", replay["outcome"])
            self.assertEqual([retry_two], creates)


if __name__ == "__main__":
    unittest.main()
