from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal_authoring import closure
from astrowoof_natal.tests import test_post_fan_in_retry_authority_routing_slice0 as _routing
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture


class CompletedRetryDuplicateSubmissionInvestigationSlice0Tests(
    SemanticClosureFixture
):
    """Characterize replay from a checkpoint containing old fan-in + new authority."""

    def test_restoring_mixed_checkpoint_can_repeat_successor_create_before_progress_refusal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline, predecessor_id, successor_id = (
                _routing.PostFanInRetryAuthorityRoutingSlice0Tests._openai_workspace(
                    self, root,
                )
            )
            frozen = root / "frozen-checkpoint"
            shutil.copytree(baseline, frozen)
            authorization = root / "ordinary-authorization.json"
            authorization.write_text("{}\n", encoding="utf-8")
            provider_creates: list[str] = []

            def authorize(state: dict, _documents: list[dict]) -> list[str]:
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == successor_id
                )
                action["state"] = "AUTHORIZED"
                return [successor_id]

            def create_successor(**kwargs: object) -> None:
                state = kwargs["state"]
                run_json = kwargs["run_json"]
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == successor_id
                )
                self.assertEqual("AUTHORIZED", action["state"])
                provider_creates.append(successor_id)
                action["state"] = "REPORTED"
                action["provider"] = {
                    "id": f"resp_successor_{len(provider_creates)}",
                    "kind": "response",
                }
                action["reported"] = {"estimated_micro_usd": 1}
                for record in state["passes"].values():
                    for attempt in record.get("attempts") or []:
                        if attempt.get("paid_action_id") == successor_id:
                            attempt["state"] = "PASS_QA_ACCEPTED"
                            attempt["finished_at"] = "2026-08-30T04:17:01Z"
                closure.save_state(run_json, state)

            for restore_number in (1, 2):
                if restore_number > 1:
                    shutil.rmtree(baseline)
                    shutil.copytree(frozen, baseline)
                with patch.object(
                    closure, "apply_spend_authorizations", side_effect=authorize,
                ), patch.object(
                    closure, "author_pending_passes", side_effect=create_successor,
                ), self.assertRaises(SystemExit) as raised:
                    _routing.PostFanInRetryAuthorityRoutingSlice0Tests._run_main(
                        self, _routing._resume_arguments(baseline, authorization),
                    )
                self.assertEqual(2, raised.exception.code)

                state = json.loads(
                    (baseline / "run.json").read_text(encoding="utf-8")
                )
                predecessor = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == predecessor_id
                )
                self.assertEqual("completed", predecessor["provider_reconciliation"]["last_outcome"])

            self.assertEqual([successor_id, successor_id], provider_creates)


if __name__ == "__main__":
    unittest.main()
