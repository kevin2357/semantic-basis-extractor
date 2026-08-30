from __future__ import annotations

import copy
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

from astrowoof_natal_authoring.closure import (
    OpenAIResponsesProvider,
    SpendController,
    author_pending_passes,
    public_run_state,
    save_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import (
    _binding,
    _workspace,
)
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture
from astrowoof_natal_authoring.spend import authorize_action


def _persist(run_dir: Path, state: dict) -> None:
    state["state_revision"] = int(state["state_revision"]) + 1
    (run_dir / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)


def _retained_topology(root: Path, issue_code: str) -> tuple[Path, dict[str, str]]:
    run_dir, pending_attempt_two, prepared_attempt_three = _workspace(
        root, "exact_natal"
    )
    state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    actions = state["spend_ledger"]["actions"]
    pending = next(
        action for action in actions if action["action_id"] == pending_attempt_two
    )
    pending["binding"]["request_sha256"] = "1" * 64
    pending["provider_reconciliation"].update({
        "last_outcome": "pending",
        "resume_not_before": "2026-08-28T06:30:00Z",
    })

    reported_attempt_two = "paid_000000000000000000000201"
    authorized_attempt_three = "paid_000000000000000000000202"
    actions.extend((
        {
            "action_id": reported_attempt_two,
            "state": "REPORTED",
            "binding": {
                **_binding(
                    state["run_id"], "creative_retry",
                    "pass-1:attempt-002", 20,
                ),
                "request_sha256": "2" * 64,
            },
            "provider": {"id": "resp_reported_attempt_two", "kind": "response"},
            "reported": {"estimated_micro_usd": 0},
        },
        {
            "action_id": authorized_attempt_three,
            "state": "AUTHORIZED",
            "binding": {
                **_binding(
                    state["run_id"], "creative_retry",
                    "pass-1:attempt-003", 21,
                ),
                "request_sha256": "3" * 64,
            },
            "authorization": {"document_sha256": "4" * 64},
        },
    ))
    prepared = next(
        action for action in actions
        if action["action_id"] == prepared_attempt_three
    )
    # This is the striking retained join: the current attempt-3 action repeats
    # the reported attempt-2 request rather than the authorized attempt-3 binding.
    prepared["binding"]["request_sha256"] = "2" * 64
    state["passes"]["pass-1"]["attempts"] = [
        {
            "attempt_number": 1,
            "state": "PASS_QA_REJECTED",
            "qa": {"editorial_issue_codes": [issue_code]},
        },
        {
            "attempt_number": 2,
            "state": "PASS_QA_REJECTED",
            "paid_action_id": reported_attempt_two,
            "qa": {"editorial_issue_codes": [issue_code]},
        },
        {
            "attempt_number": 3,
            "state": "AWAITING_SPEND_AUTHORIZATION",
            "paid_action_id": prepared_attempt_three,
        },
    ]
    state["passes"]["pass-1"]["state"] = "AWAITING_SPEND_AUTHORIZATION"
    state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    _persist(run_dir, state)
    return run_dir, {
        "pending_attempt_two": pending_attempt_two,
        "reported_attempt_two": reported_attempt_two,
        "authorized_attempt_three": authorized_attempt_three,
        "prepared_attempt_three": prepared_attempt_three,
    }


class ReviewRequiredPendingRetriesInvestigationSlice2Tests(unittest.TestCase):
    def test_v07_review_projection_masks_retained_provider_custody(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, ids = _retained_topology(
                Path(temporary), "theme_group_coverage"
            )
            legacy = inspect_lifecycle(
                run_dir, observed_at="2026-08-28T06:24:00Z",
                native_exclusive_access="declared",
            )
            self.assertEqual(
                "provider_reconciliation_cycle",
                legacy["execution_branch"]["command"],
            )
            self.assertEqual(
                [ids["pending_attempt_two"]],
                legacy["execution_branch"]["action_ids"],
            )

            projected = inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-28T06:24:00Z",
                native_exclusive_access="declared",
            )
            validate_lifecycle_inspection_v07(projected)
            self.assertEqual("none", projected["temporal_decision"]["selected_command"])
            self.assertEqual(
                "retain_for_review",
                projected["temporal_decision"]["capacity_disposition"],
            )
            self.assertEqual([], projected["temporal_decision"]["due_action_ids"])
            self.assertIn(
                "authorized_providerless_action_requires_constrained_dispatch",
                projected["checkpoint_basis"]["review_reasons"],
            )

    def test_duplicate_route_and_binding_lineages_are_not_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, ids = _retained_topology(Path(temporary), "generic_qa_reject")
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            actions = {
                action["action_id"]: action
                for action in state["spend_ledger"]["actions"]
            }
            self.assertEqual(
                actions[ids["pending_attempt_two"]]["binding"]["route"],
                actions[ids["reported_attempt_two"]]["binding"]["route"],
            )
            self.assertNotEqual(
                actions[ids["pending_attempt_two"]]["binding"]["request_sha256"],
                actions[ids["reported_attempt_two"]]["binding"]["request_sha256"],
            )
            self.assertEqual(
                actions[ids["authorized_attempt_three"]]["binding"]["route"],
                actions[ids["prepared_attempt_three"]]["binding"]["route"],
            )
            self.assertNotEqual(
                actions[ids["authorized_attempt_three"]]["binding"]["request_sha256"],
                actions[ids["prepared_attempt_three"]]["binding"]["request_sha256"],
            )
            self.assertEqual(
                actions[ids["reported_attempt_two"]]["binding"]["request_sha256"],
                actions[ids["prepared_attempt_three"]]["binding"]["request_sha256"],
            )
            # Current public validation accepts this contradictory lineage.
            validate_lifecycle_inspection_v07(inspect_post_fan_in_lifecycle(
                run_dir, observed_at="2026-08-28T06:24:00Z",
                native_exclusive_access="declared",
            ))

    def test_review_projection_is_independent_of_qa_failure_modality(self) -> None:
        projections = []
        for issue_code in ("theme_group_coverage", "generic_qa_reject"):
            with tempfile.TemporaryDirectory() as temporary:
                run_dir, _ids = _retained_topology(Path(temporary), issue_code)
                result = inspect_post_fan_in_lifecycle(
                    run_dir, observed_at="2026-08-28T06:24:00Z",
                    native_exclusive_access="declared",
                )
                projections.append({
                    "selected_command": result["temporal_decision"]["selected_command"],
                    "capacity_disposition": result["temporal_decision"]["capacity_disposition"],
                    "reason_code": result["temporal_decision"]["reason_code"],
                    "review_reasons": result["checkpoint_basis"]["review_reasons"],
                })
        self.assertEqual(projections[0], projections[1])


class ReviewRequiredPendingRetriesRuntimeReproductionTests(SemanticClosureFixture):
    def test_real_retry_preparation_is_idempotent_across_authority_restart(self) -> None:
        """The corrected production loop preserves one attempt/action lineage."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = OpenAIResponsesProvider(
                api_key="provider-free", model="gpt-5.6-terra",
                prompt_cache_mode="disabled", require_spend_authorization=True,
            )
            state, run_json = self.make_state(root, provider)
            records = sorted(
                state["passes"].values(), key=lambda item: item["pass_number"]
            )
            for record in records[:5]:
                record["state"] = "PASS_QA_ACCEPTED"
                record["accepted_attempt"] = 1
            affected = records[5]
            affected["state"] = "PASS_QA_REJECTED"
            affected["attempts"] = [
                {
                    "attempt_number": number,
                    "state": "PASS_QA_REJECTED",
                    "started_at": f"2026-08-28T06:0{number}:00Z",
                    "finished_at": f"2026-08-28T06:0{number}:30Z",
                    "response_workspace": str(
                        root / "run" / "passes" / affected["pass_id"]
                        / f"attempt-{number:03d}" / "response" / affected["pass_id"]
                    ),
                    "provider_metadata": None,
                    "qa": {"report": {
                        "status": "reject",
                        "editorial_issue_codes": ["generic_qa_reject"],
                        "affected_claim_ids": ["fixture-claim"],
                        "guidance": "provider-free retry fixture",
                    }},
                    "error": None,
                }
                for number in (1, 2)
            ]
            save_state(run_json, state)
            controller = SpendController(
                state=state, run_json=run_json, state_lock=threading.Lock(),
                consumer_id="slice-2-provider-free",
            )

            # First entry prepares attempt 3 with the attempt-2 rejection feedback.
            author_pending_passes(
                state=state, provider=provider, run_dir=run_json.parent,
                max_attempts=3, python_executable=Path(sys.executable),
                run_json=run_json, max_workers=1, spend_controller=controller,
                only_pass_ids={affected["pass_id"]},
            )
            first = state["spend_ledger"]["actions"][-1]
            self.assertEqual("PREPARED", first["state"])
            self.assertEqual(
                f"{affected['pass_id']}:attempt-003", first["binding"]["route"]
            )
            evidence = copy.deepcopy(affected["attempts"][-1]["retry_attempt_evidence"])
            self.assertEqual(first["action_id"], evidence["action_id"])

            # A fresh generic entry before authorization rebuilds the exact same
            # request and reuses the existing action; it performs no provider I/O.
            author_pending_passes(
                state=state, provider=provider, run_dir=run_json.parent,
                max_attempts=3, python_executable=Path(sys.executable),
                run_json=run_json, max_workers=1, spend_controller=controller,
                only_pass_ids={affected["pass_id"]},
            )
            same_route = [
                action for action in state["spend_ledger"]["actions"]
                if action["binding"]["route"]
                == f"{affected['pass_id']}:attempt-003"
            ]
            self.assertEqual([first["action_id"]], [item["action_id"] for item in same_route])
            self.assertEqual(evidence, affected["attempts"][-1]["retry_attempt_evidence"])

            authorize_action(state["spend_ledger"], {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": first["action_id"],
                "binding": copy.deepcopy(first["binding"]),
                "authorization_reference": "slice-2-provider-free",
            })
            save_state(run_json, state)

            # Exercise the exact callback boundary with the persisted payload.
            # This consumes the authorized action into SUBMITTING but deliberately
            # stops before any provider transport.
            artifact = first["request_payload_artifact"]
            payload = json.loads(Path(artifact["logical_path"]).read_text(encoding="utf-8"))
            before_submit, _provider_created = controller.callbacks(
                stage="creative_retry",
                route=f"{affected['pass_id']}:attempt-003",
                model=first["binding"]["model"], service_level="interactive",
                maximum_output_tokens=first["binding"]["maximum_output_tokens"],
            )
            before_submit(payload, request_payload_artifact=artifact)
            same_route = [
                action for action in state["spend_ledger"]["actions"]
                if action["binding"]["route"]
                == f"{affected['pass_id']}:attempt-003"
            ]
            self.assertEqual(1, len(same_route))
            self.assertEqual("SUBMITTING", same_route[0]["state"])
            self.assertEqual(evidence, affected["attempts"][-1]["retry_attempt_evidence"])
            self.assertFalse(same_route[0].get("provider"))


if __name__ == "__main__":
    unittest.main()
