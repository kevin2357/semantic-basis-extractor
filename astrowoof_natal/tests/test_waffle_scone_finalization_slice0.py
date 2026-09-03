from __future__ import annotations

import io
import hashlib
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture
from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.native_transitions import (
    publish_native_execution_result,
    read_native_transition_result,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    validate_terminal_review_result_v02,
    validate_terminal_review_result_v02_against_api_actions,
)
from astrowoof_natal_authoring import terminal_review_contracts
from astrowoof_natal_authoring.finalization_boundary_qa import (
    read_finalization_boundary_qualification_schema,
    run_finalization_boundary_qualification,
    validate_finalization_boundary_qualification,
)


class WaffleSconeFinalizationSlice0Tests(SemanticClosureFixture):
    def _completed_workspace(self, root: Path) -> tuple[Path, dict, Path]:
        provider = closure.FakeAuthoringProvider()
        state, run_json = self.make_state(
            root, provider, max_attempts=1, cards_per_pass=10,
        )
        closure.author_pending_passes(
            state=state,
            provider=provider,
            run_dir=root / "run",
            max_attempts=1,
            python_executable=Path(sys.executable),
            run_json=run_json,
            max_workers=6,
        )
        self.assertTrue(all(
            record["state"] == "PASS_QA_ACCEPTED"
            for record in state["passes"].values()
        ))
        # Fake authoring deliberately has no paid ledger. Add one fully closed,
        # provider-reported action through the same public identity shape so the
        # v0.7 inspector can advertise Waffle's final-assembly local operation.
        state["spend_ledger"] = {
            "actions": [{
                "action_id": "paid_000000000000000000000001",
                "state": "REPORTED",
                "binding": {
                    "run_id": state["run_id"],
                    "profile_sha256": "1" * 64,
                    "prepared_state_revision": 1,
                    "stage": "authoring_initial",
                    "route": "bre_1:attempt-001",
                    "request_sha256": "2" * 64,
                    "model": "fake-authoring",
                    "service_level": "interactive",
                    "maximum_output_tokens": 100,
                    "commitment_micro_usd": 0,
                    "price_book_version": "openai-public-2026-08-07.v1",
                },
                "authorization": {"authorization_reference": "fixture"},
                "consumption": {"consumer_id": "fixture"},
                "provider": {"kind": "response", "id": "resp_waffle_fixture"},
                "reported": {"usage": None, "estimated_micro_usd": 0},
                "reconciliation_reference_ids": [],
            }],
            "reconciliation_references": [],
        }
        accepted = Path(state["passes"]["bre_6"]["accepted_workspace"])
        return accepted, state, run_json

    @staticmethod
    def _stage_completed_provider_evidence(
        root: Path, state: dict, run_json: Path,
    ) -> None:
        action = state["spend_ledger"]["actions"][0]
        action["state"] = "WAITING"
        action["reported"] = None
        action["consumption"] = None
        action["provider_reconciliation"] = {
            "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
            "provider_retrieval_attempt_count": 1,
            "last_attempt_at": "2026-09-02T21:28:00Z",
            "last_outcome": "completed",
            "resume_not_before": None,
        }
        closure.save_state(run_json, state)
        closure.write_workspace_snapshot(root / "run")

    @staticmethod
    def _adopt_completed_provider_evidence(**kwargs) -> bool:
        current = kwargs["state"]
        completed = current["spend_ledger"]["actions"][0]
        completed["state"] = "REPORTED"
        completed["reported"] = {
            "usage": None, "estimated_micro_usd": 0,
        }
        closure.save_state(kwargs["run_json"], current)
        return True

    def test_deterministic_assembly_contract_failure_seals_review_result(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _accepted, state, run_json = self._completed_workspace(root)
            self._stage_completed_provider_evidence(root, state, run_json)
            argv = [
                "astrowoof-semantic-closure",
                "--run-dir", str(root / "run"),
                "--resume", "--provider", "fake", "--max-attempts", "1",
            ]
            stdout = io.StringIO()
            with self.assertLogs(
                closure.logger, level="INFO",
            ) as captured, patch.object(sys, "argv", argv), patch.object(
                closure,
                "author_pending_passes",
                side_effect=self._adopt_completed_provider_evidence,
            ), patch.object(
                closure,
                "assemble",
                side_effect=closure.AssemblyContractError("protected detail"),
            ), patch("sys.stdout", stdout), self.assertRaises(SystemExit) as raised:
                closure.main()
            self.assertEqual(2, raised.exception.code)
            command_result = json.loads(stdout.getvalue())
            sealed = read_native_transition_result(
                root / "run", command_result["result_id"],
            )
            result = sealed["result"]
            self.assertEqual("review_required", result["outcome"])
            self.assertEqual(
                "finalization_contract_invalid", result["cause_code"],
            )
            self.assertEqual("final", result["custody_finality"])
            self.assertFalse(result["new_provider_create_permitted"])
            self.assertNotIn("protected detail", json.dumps(command_result))
            self.assertNotIn("protected detail", "\n".join(captured.output))
            persisted = json.loads(run_json.read_text(encoding="utf-8"))
            api_actions = []
            for action in persisted["spend_ledger"]["actions"]:
                api_actions.append({
                    "native_run_id": persisted["run_id"],
                    "action_id": action["action_id"],
                    "binding": action["binding"],
                    "route_family": "exact_natal",
                    "stage": action["binding"]["stage"],
                    "provider_operation_id": action["provider"]["id"],
                })
            validate_terminal_review_result_v02_against_api_actions(
                result, api_actions,
            )
            contradictory = deepcopy(result)
            row = contradictory["action_dispositions"][0]
            row["native_action_state"] = "WAITING"
            row["custody_disposition"] = "provider_reconciliation_only"
            row["reported_present"] = False
            row["usage_reported"] = False
            contradictory["reconciliation_action_ids"] = [row["action_id"]]
            contradictory["custody_finality"] = (
                "provider_reconciliation_required"
            )
            contradictory["action_inventory_sha256"] = (
                terminal_review_contracts._digest(
                    contradictory["action_dispositions"]
                )
            )
            basis = {
                key: value for key, value in contradictory.items()
                if key not in {"result_id", "result_sha256"}
            }
            contradictory["result_sha256"] = (
                terminal_review_contracts._digest(basis)
            )
            contradictory["result_id"] = (
                f"nres_{contradictory['result_sha256'][:24]}"
            )
            with self.assertRaisesRegex(
                ValueError, "requires final action custody",
            ):
                validate_terminal_review_result_v02(contradictory)

            replay_stdout = io.StringIO()
            with patch.object(sys, "argv", argv), patch(
                "sys.stdout", replay_stdout,
            ), self.assertRaises(SystemExit) as replay_exit:
                closure.main()
            self.assertEqual(2, replay_exit.exception.code)
            replay = json.loads(replay_stdout.getvalue())
            self.assertEqual(command_result["result_id"], replay["result_id"])

    def test_operational_finalization_failure_does_not_fabricate_review(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _accepted, state, run_json = self._completed_workspace(root)
            self._stage_completed_provider_evidence(root, state, run_json)
            with patch.object(sys, "argv", [
                "astrowoof-semantic-closure",
                "--run-dir", str(root / "run"),
                "--resume", "--provider", "fake", "--max-attempts", "1",
            ]), patch.object(
                closure,
                "author_pending_passes",
                side_effect=self._adopt_completed_provider_evidence,
            ), patch.object(
                closure, "assemble", side_effect=OSError("dependency unavailable"),
            ), self.assertRaisesRegex(OSError, "dependency unavailable"):
                closure.main()
            self.assertFalse(
                (root / "run" / "native-execution-results.json").exists()
            )

    def test_interrupted_finalization_review_publication_repairs_exactly(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _accepted, state, run_json = self._completed_workspace(root)
            state["terminal_transition"] = {
                "schema_version": (
                    "astrowoof.finalization_contract_transition.v0.1"
                ),
                "outcome": "terminalized",
                "trigger": "deterministic_finalization_contract_failure",
                "prior_status": state["status"],
                "resulting_status": "FAILED_REQUIRES_REVIEW",
                "terminal_outcome": "review_required",
                "terminal_reason": "finalization_contract_invalid",
                "committed_at": "2026-09-03T07:00:00Z",
            }
            closure.save_state(
                run_json, state,
                preserve_review_status="FAILED_REQUIRES_REVIEW",
            )

            def fail_after_result(point: str) -> None:
                if point == "after_result_written":
                    raise OSError("injected publication interruption")

            with self.assertRaisesRegex(OSError, "publication interruption"):
                publish_native_execution_result(
                    root / "run",
                    command_kind="ordinary_authoring",
                    sbe_release="0.4.39",
                    published_at="2026-09-03T07:00:01Z",
                    terminal_review_v02=True,
                    terminal_review_cause="finalization_contract_invalid",
                    _failure_injector=fail_after_result,
                )
            repaired = publish_native_execution_result(
                root / "run",
                command_kind="ordinary_authoring",
                sbe_release="0.4.39",
                published_at="2026-09-03T07:00:01Z",
                terminal_review_v02=True,
                terminal_review_cause="finalization_contract_invalid",
            )
            self.assertEqual(
                "finalization_contract_invalid",
                repaired["result"]["cause_code"],
            )
            self.assertEqual("final", repaired["result"]["custody_finality"])

    def test_nonfinal_custody_outranks_assembly_contract_error(self) -> None:
        for action_state in ("WAITING", "SUBMITTING"):
            with self.subTest(state=action_state), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _accepted, state, run_json = self._completed_workspace(root)
                action = state["spend_ledger"]["actions"][0]
                action["state"] = action_state
                action["reported"] = None
                action["consumption"] = None
                if action_state == "WAITING":
                    action["provider_reconciliation"] = {
                        "policy_version": (
                            "astrowoof.provider_reconciliation_policy.v0.2"
                        ),
                        "provider_retrieval_attempt_count": 1,
                        "last_attempt_at": "2026-09-02T21:28:00Z",
                        "last_outcome": "pending",
                        "resume_not_before": "2099-09-02T21:29:00Z",
                    }
                else:
                    action["provider"] = None
                closure.save_state(run_json, state)
                closure.write_workspace_snapshot(root / "run")
                with patch.object(sys, "argv", [
                    "astrowoof-semantic-closure",
                    "--run-dir", str(root / "run"),
                    "--resume", "--provider", "fake", "--max-attempts", "1",
                ]), patch.object(
                    closure, "author_pending_passes", return_value=True,
                ), patch.object(
                    closure,
                    "assemble",
                    side_effect=closure.AssemblyContractError("protected detail"),
                ), self.assertRaises(closure.AssemblyContractError):
                    closure.main()
                self.assertFalse(
                    (root / "run" / "native-execution-results.json").exists()
                )

    def test_packaged_finalization_boundary_qualification(self) -> None:
        receipt = run_finalization_boundary_qualification()
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["real_provider_create_count"])
        self.assertIn("$schema", read_finalization_boundary_qualification_schema())

    def test_qualification_rejects_rehashed_semantic_mutation(self) -> None:
        receipt = run_finalization_boundary_qualification()
        receipt["review_case"]["custody_finality"] = (
            "provider_reconciliation_required"
        )
        body = {
            key: value for key, value in receipt.items()
            if key != "receipt_sha256"
        }
        receipt["receipt_sha256"] = hashlib.sha256(
            json.dumps(
                body, ensure_ascii=False, sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "semantics differ"):
            validate_finalization_boundary_qualification(receipt)


if __name__ == "__main__":
    unittest.main()
