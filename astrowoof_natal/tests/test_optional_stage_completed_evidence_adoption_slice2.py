from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from astrowoof_natal.tests import test_nori_biscuit_reproduction_slice3 as _nori
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture
from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.spend import AmbiguousProviderSubmission
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
)


class OptionalStageCompletedEvidenceAdoptionSlice2Tests(SemanticClosureFixture):
    """Freeze Puff's completed-polish adoption gap before runtime repair."""

    _invoke = _nori.NoriBiscuitProductionBoundarySlice3Tests._invoke
    _nori_polish_workspace = (
        _nori.NoriBiscuitProductionBoundarySlice3Tests._nori_polish_workspace
    )
    _materialize_real_polish_record = (
        _nori.NoriBiscuitProductionBoundarySlice3Tests._materialize_real_polish_record
    )

    def _install_exact_completed_v2_authority(
        self, run_dir: Path, action_id: str,
    ) -> None:
        """Add the v2 joins intentionally omitted by the older Nori fixture."""
        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        action = next(
            item for item in state["spend_ledger"]["actions"]
            if item["action_id"] == action_id
        )
        payload_path = (
            run_dir / "lifecycle" / "prepared-payloads" / f"{action_id}.json"
        )
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"fixture": "exact-v2-payload", "action_id": action_id}
        closure.write_json_atomic(payload_path, payload)
        request_sha256 = closure.spend_digest(payload)
        action["binding"]["request_sha256"] = request_sha256
        action["request_payload_artifact"] = {
            "schema_version": "astrowoof.provider_request_payload_artifact.v1",
            "logical_path": closure.normalized_path(payload_path),
            "file_sha256": closure.sha256_file(payload_path),
            "canonical_request_sha256": request_sha256,
            "representation": "canonical_json_object",
        }
        authorization = {
            "schema_version": "astrowoof.provider_spend_authorization.v0.1",
            "action_id": action_id,
            "binding": action["binding"],
            "authorization_reference": "api-auth:optional-adoption",
        }
        action["authorization"] = authorization
        action["consumption"] = {
            "consumer_id": "external-grant-v2:api-decision-optional-adoption",
            "state_revision": 1,
        }
        response_id = action["provider"]["id"]
        state["external_authority_v2_dispatch_intent"] = {
            "schema_version": "astrowoof.external_authority_dispatch_intent.v2",
            "request_schema_version": "astrowoof.external_authority_request.v2",
            "request_sha256": "1" * 64,
            "checkpoint_basis_sha256": "2" * 64,
            "grant_schema_version": "astrowoof.external_authority_grant.v2",
            "grant_sha256": "3" * 64,
            "state": "PROVIDER_PENDING",
            "api_decision_id": "api-decision-optional-adoption",
            "ordering_semantics": "lexical_action_id_ascending",
            "ordered_action_ids": [action_id],
            "provider_bound_action_ids": [action_id],
            "provider_operation_ids": [response_id],
            "ordered_authorization_document_sha256s": [
                closure.spend_digest(authorization)
            ],
            "next_action_index": 1,
            "prepared_create_records": [{
                "action_id": action_id,
                "prepared_create_sha256": "4" * 64,
            }],
            "active_action_id": None,
            "active_create_state": None,
            "provider_io_performed": True,
        }
        closure.save_state(state_path, state)

    class _CompletedActionController:
        def __init__(self, *, action_id: str, stage: str, route: str) -> None:
            # An empty ledger deliberately makes the adoption helper a no-op;
            # the characterization then proves the old consumer would re-enter
            # SpendController without matching completed evidence.
            self.state: dict = {}
            self.action = {
                "action_id": action_id,
                "state": "WAITING",
                "binding": {"stage": stage, "route": route},
                "provider": {"kind": "response", "id": f"resp_{stage}"},
                "provider_reconciliation": {"last_outcome": "completed"},
            }
            self.calls: list[tuple[str, str]] = []

        def callbacks(self, *, stage: str, route: str, **_kwargs):
            self.calls.append((stage, route))
            raise AmbiguousProviderSubmission(
                "completed provider-bound action re-entered submission",
                action=self.action,
            )

    def _qualitative_record(self, root: Path) -> dict:
        final_root = root / "final" / "bre"
        final_root.mkdir(parents=True, exist_ok=True)
        deck_path = final_root / "natal.bre.cards.json"
        closure.write_json_atomic(deck_path, self.packet)
        lint_path = final_root / "lint.json"
        closure.write_json_atomic(lint_path, {"status": "pass", "warning_count": 0})
        return {
            "subject": "bre",
            "state": "DELIVERY_COMPLETE",
            "deck": closure.normalized_path(deck_path),
            "lint_report": closure.normalized_path(lint_path),
        }

    def _completed_optional_v2_fixture(
        self, root: Path, *, stage: str, response_body: dict,
    ) -> tuple[Path, str, dict, closure.SpendController]:
        """Build one exact optional v2 action with completed native evidence."""
        run_dir, action_id = self._nori_polish_workspace(root)
        self._materialize_real_polish_record(run_dir, action_id)
        state_path = run_dir / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        action = next(
            item for item in state["spend_ledger"]["actions"]
            if item["action_id"] == action_id
        )
        route = f"bre:{stage.replace('_', '-')}"
        action["binding"].update({"stage": stage, "route": route})
        closure.save_state(state_path, state)
        self._install_exact_completed_v2_authority(run_dir, action_id)
        response_path = (
            run_dir / "lifecycle" / "provider-reconciliation"
            / f"{action_id}.response.json"
        )
        closure.write_json_atomic(
            response_path,
            _nori.completed_response(
                response_body, response_id=action["provider"]["id"],
            ),
        )
        current = json.loads(state_path.read_text(encoding="utf-8"))
        current.setdefault("provenance", {}).update({
            "runtime": {"fixture": "optional-stage-adoption"},
            "resources": {"fixture": "provider-free"},
        })
        closure.save_state(state_path, current)
        closure.write_workspace_snapshot(run_dir)
        record = self._qualitative_record(run_dir)
        controller = closure.SpendController(
            state=current,
            run_json=state_path,
            state_lock=threading.Lock(),
            consumer_id="optional-stage-adoption-fixture",
        )
        return run_dir, action_id, record, controller

    def test_real_resume_adopts_reconciled_polish_without_private_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, action_id = self._nori_polish_workspace(Path(temporary))
            self._materialize_real_polish_record(run_dir, action_id)
            self._install_exact_completed_v2_authority(run_dir, action_id)

            # The older Nori qualification supplied this private bridge itself.
            # Puff's real reconciliation checkpoint had the public/durable
            # response artifact but no attempt-local background marker.
            marker = (
                run_dir / "final" / "bre" / "polish" / "attempt-001"
                / "openai-background-response.json"
            )
            marker.unlink()
            closure.write_workspace_snapshot(run_dir)

            before = inspect_post_fan_in_lifecycle(
                run_dir,
                observed_at="2026-09-03T13:52:01Z",
                native_exclusive_access="declared",
            )
            operation = before["checkpoint_basis"]["local_work_inventory"][
                "operations"
            ][0]
            self.assertEqual("polish", operation["stage"])
            self.assertEqual([action_id], operation["source_action_ids"])

            with patch.object(
                closure.OpenAIResponsesProvider,
                "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                code, command = self._invoke(run_dir, polish=True)

            # Desired invariant: completed evidence is adopted before the
            # consumer can re-enter SpendController/provider submission.
            self.assertEqual(2, code, command)
            persisted = json.loads(
                (run_dir / "run.json").read_text(encoding="utf-8")
            )
            action = next(
                item for item in persisted["spend_ledger"]["actions"]
                if item["action_id"] == action_id
            )
            attempt = persisted["subjects"]["bre"]["polish_attempts"][0]
            self.assertEqual("REPORTED", action["state"])
            self.assertEqual("POLISH_NO_CHANGE", attempt["state"])
            self.assertEqual(
                action["provider"]["id"],
                attempt["provider_metadata"]["response_id"],
            )
            self.assertIn(
                operation["operation_key"],
                persisted["local_work_progress"]["consumed_operation_keys"],
            )

    def test_qualitative_critic_reenters_spend_before_completed_adoption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record = self._qualitative_record(root)
            record["qualitative_review"] = {
                "state": "CRITIC_SUBMITTED",
                "started_at": "2026-09-03T14:00:00Z",
                "finished_at": None,
            }
            controller = self._CompletedActionController(
                action_id="paid_0000000000000000000000c1",
                stage="qualitative_critic",
                route="bre:qualitative-critic",
            )
            provider = closure.OpenAIResponsesProvider(
                api_key="provider-free", model="gpt-5.6-luna",
                max_output_tokens=30_000, prompt_cache_mode="disabled",
                require_spend_authorization=True,
            )

            with self.assertRaises(AmbiguousProviderSubmission):
                closure.run_qualitative_review(
                    record=record,
                    critic_provider=provider,
                    editor_provider=None,
                    run_dir=root,
                    python_executable=Path("python"),
                    max_findings=8,
                    max_target_fields=12,
                    max_target_cards=6,
                    spend_controller=controller,
                )

            self.assertEqual(
                [("qualitative_critic", "bre:qualitative-critic")],
                controller.calls,
            )
            self.assertEqual("CRITIC_SUBMITTED", record["qualitative_review"]["state"])

    def test_qualitative_critic_adopts_completed_evidence_without_io(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, action_id, record, controller = (
                self._completed_optional_v2_fixture(
                    Path(temporary), stage="qualitative_critic",
                    response_body={"findings": []},
                )
            )
            record["qualitative_review"] = {
                "state": "CRITIC_SUBMITTED",
                "started_at": "2026-09-03T14:00:00Z",
                "finished_at": None,
            }
            candidate_marker = (
                run_dir / "final" / "bre" / "qualitative" / "candidate"
                / "openai-background-response.json"
            )
            closure.write_json_atomic(candidate_marker, {"id": "resp_other"})
            provider = closure.OpenAIResponsesProvider(
                api_key="provider-free", model="gpt-5.6-luna",
                max_output_tokens=30_000, prompt_cache_mode="disabled",
                require_spend_authorization=True,
            )

            with patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                closure.run_qualitative_review(
                    record=record, critic_provider=provider, editor_provider=None,
                    run_dir=run_dir, python_executable=Path("python"),
                    max_findings=8, max_target_fields=12, max_target_cards=6,
                    spend_controller=controller, run_state=controller.state,
                )

            marker = (
                run_dir / "final" / "bre" / "qualitative" / "critic"
                / "openai-background-response.json"
            )
            self.assertEqual("resp_nori_slice_3", json.loads(
                marker.read_text(encoding="utf-8")
            )["id"])
            self.assertEqual({"id": "resp_other"}, json.loads(
                candidate_marker.read_text(encoding="utf-8")
            ))
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(item for item in state["spend_ledger"]["actions"]
                          if item["action_id"] == action_id)
            self.assertEqual("REPORTED", action["state"])
            self.assertEqual(
                "NO_ELIGIBLE_FINDINGS", record["qualitative_review"]["state"],
                record["qualitative_review"].get("error"),
            )

    def test_mismatched_completed_identity_refuses_before_marker_or_io(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, action_id = self._nori_polish_workspace(Path(temporary))
            self._materialize_real_polish_record(run_dir, action_id)
            self._install_exact_completed_v2_authority(run_dir, action_id)
            response_path = (
                run_dir / "lifecycle" / "provider-reconciliation"
                / f"{action_id}.response.json"
            )
            response = json.loads(response_path.read_text(encoding="utf-8"))
            response["id"] = "resp_conflicting_optional_evidence"
            closure.write_json_atomic(response_path, response)
            marker = (
                run_dir / "final" / "bre" / "polish" / "attempt-001"
                / "openai-background-response.json"
            )
            marker.unlink()
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))

            with self.assertRaisesRegex(ValueError, "identity is invalid"):
                closure.prepare_completed_optional_stage_for_adoption(
                    state=state,
                    run_dir=run_dir,
                    attempt_root=marker.parent,
                    stage="polish",
                    route="bre:polish:001",
                    model="gpt-5.6-luna",
                )

            self.assertFalse(marker.exists())

    def test_qualitative_candidate_reenters_spend_before_completed_adoption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record = self._qualitative_record(root)
            artifact = root / "critic-findings.json"
            closure.write_json_atomic(artifact, {"fixture": "validated below"})
            record["qualitative_review"] = {
                "state": "DIAGNOSIS_COMPLETE",
                "started_at": "2026-09-03T14:00:00Z",
                "finished_at": "2026-09-03T14:00:01Z",
                "critic": {"artifact": closure.normalized_path(artifact)},
            }
            controller = self._CompletedActionController(
                action_id="paid_0000000000000000000000c2",
                stage="qualitative_candidate",
                route="bre:qualitative-candidate",
            )
            provider = closure.OpenAIResponsesProvider(
                api_key="provider-free", model="gpt-5.6-luna",
                max_output_tokens=30_000, prompt_cache_mode="disabled",
                require_spend_authorization=True,
            )
            selection = {
                "selected_target_paths": [
                    "cards.0.card.no_astro.headline.handler"
                ],
                "eligible_findings": [{
                    "comparison_paths": [], "required_context": [],
                }],
            }

            with patch.object(
                closure, "validate_critic_findings_artifact",
                return_value=selection,
            ), self.assertRaises(AmbiguousProviderSubmission):
                closure.run_qualitative_review(
                    record=record,
                    critic_provider=provider,
                    editor_provider=provider,
                    run_dir=root,
                    python_executable=Path("python"),
                    max_findings=8,
                    max_target_fields=12,
                    max_target_cards=6,
                    spend_controller=controller,
                )

            self.assertEqual(
                [("qualitative_candidate", "bre:qualitative-candidate")],
                controller.calls,
            )
            self.assertEqual(
                "CANDIDATE_SUBMITTED", record["qualitative_review"]["state"]
            )

    def test_qualitative_candidate_adopts_completed_evidence_without_io(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, action_id, record, controller = (
                self._completed_optional_v2_fixture(
                    Path(temporary), stage="qualitative_candidate",
                    response_body={"edits": []},
                )
            )
            critic_artifact = (
                run_dir / "final" / "bre" / "qualitative" / "critic"
                / "critic-findings.json"
            )
            closure.write_json_atomic(critic_artifact, {"fixture": "preserve"})
            record["qualitative_review"] = {
                "state": "DIAGNOSIS_COMPLETE",
                "started_at": "2026-09-03T14:00:00Z",
                "finished_at": "2026-09-03T14:00:01Z",
                "critic": {"artifact": closure.normalized_path(critic_artifact)},
            }
            critic_marker = (
                run_dir / "final" / "bre" / "qualitative" / "critic"
                / "openai-background-response.json"
            )
            closure.write_json_atomic(critic_marker, {"id": "resp_critic_predecessor"})
            provider = closure.OpenAIResponsesProvider(
                api_key="provider-free", model="gpt-5.6-luna",
                max_output_tokens=30_000, prompt_cache_mode="disabled",
                require_spend_authorization=True,
            )
            selection = {
                "selected_target_paths": ["cards.0.card.no_astro.headline.handler"],
                "eligible_findings": [{"comparison_paths": [], "required_context": []}],
            }

            with patch.object(
                closure, "validate_critic_findings_artifact", return_value=selection,
            ), patch.object(
                closure.OpenAIResponsesProvider, "_request_with_retry",
                side_effect=AssertionError("provider I/O forbidden"),
            ):
                closure.run_qualitative_review(
                    record=record, critic_provider=provider, editor_provider=provider,
                    run_dir=run_dir, python_executable=Path("python"),
                    max_findings=8, max_target_fields=12, max_target_cards=6,
                    spend_controller=controller,
                )

            marker = (
                run_dir / "final" / "bre" / "qualitative" / "candidate"
                / "openai-background-response.json"
            )
            self.assertEqual("resp_nori_slice_3", json.loads(
                marker.read_text(encoding="utf-8")
            )["id"])
            self.assertEqual({"id": "resp_critic_predecessor"}, json.loads(
                critic_marker.read_text(encoding="utf-8")
            ))
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(item for item in state["spend_ledger"]["actions"]
                          if item["action_id"] == action_id)
            self.assertEqual(
                "REPORTED", action["state"], record["qualitative_review"].get("error"),
            )
            self.assertEqual("CANDIDATE_NO_CHANGE", record["qualitative_review"]["state"])


if __name__ == "__main__":
    unittest.main()
