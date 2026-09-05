from __future__ import annotations

import io
import json
import logging
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.application_logging import configure_logging
from astrowoof_natal_authoring.closure import _log_durable_evidence_changes
from astrowoof_natal_authoring.trace_observability import (
    bounded_identifiers,
    decision_summary,
    log_cli_exit,
    log_decision_summary,
    log_native_state_summary,
    log_stage_evidence_summary,
    log_publication_evidence_summary,
    log_validation_evidence_summary,
    log_workspace_fingerprint,
    native_state_summary,
    sanitize_exception,
    stage_evidence_summary,
    publication_evidence_summary,
    validation_evidence_summary,
    workspace_fingerprint,
)
from astrowoof_natal_authoring.run_report import parse_trace_text


class _FailingLogger:
    def info(self, *args, **kwargs):
        raise RuntimeError("sink exploded")


class TraceObservabilityTests(unittest.TestCase):
    def _state(self, root: Path, *, protected: str = "") -> dict:
        actions = []
        for index in range(10):
            action_id = f"paid_{index:024x}"
            actions.append({
                "action_id": action_id,
                "state": "WAITING" if index < 2 else "PREPARED",
                "binding": {
                    "stage": "creative_retry" if index < 5 else "polish",
                    "request_sha256": str(index % 10) * 64,
                    "private_prompt": protected,
                },
                "provider": (
                    {"id": f"resp_trace_{index}"} if index < 2 else None
                ),
            })
        return {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "trace-run",
            "status": "WAITING_FOR_RESPONSE",
            "state_revision": 12,
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": str(root),
            },
            "spend_ledger": {"actions": actions},
            "external_authority_v2_dispatch_intent": {
                "state": "PROVIDER_PENDING",
                "request_sha256": "a" * 64,
                "grant_sha256": "b" * 64,
                "ordered_action_ids": [item["action_id"] for item in actions],
                "private_payload": protected,
            },
        }

    def test_workspace_fingerprint_is_identity_only_and_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            protected = "PROTECTED-PROMPT-SENTINEL"
            state = self._state(root, protected=protected)
            snapshot = {
                "schema_version": "astrowoof.semantic_closure_snapshot.v0.1",
                "logical_root": str(root),
                "members": [{"path": "run.json", "bytes": 3, "sha256": "c" * 64}],
            }
            (root / "workspace-snapshot.json").write_text(
                json.dumps(snapshot), encoding="utf-8"
            )
            first = workspace_fingerprint(
                root, state, validation_outcome="valid", sbe_release="0.test",
            )
            second = workspace_fingerprint(
                root, state, validation_outcome="valid", sbe_release="0.test",
            )
            self.assertEqual(first, second)
            rendered = json.dumps(first, sort_keys=True)
            self.assertNotIn(str(root), rendered)
            self.assertNotIn(protected, rendered)
            self.assertEqual(first["snapshot_member_count"], 1)
            self.assertEqual(len(first["fingerprint_sha256"]), 64)

    def test_state_summary_is_bounded_and_excludes_payloads(self):
        with tempfile.TemporaryDirectory() as temp:
            protected = "PROTECTED-BINDING-SENTINEL"
            summary = native_state_summary(
                self._state(Path(temp), protected=protected)
            )
            rendered = json.dumps(summary, sort_keys=True)
            self.assertNotIn(protected, rendered)
            self.assertEqual(summary["action_inventory"]["count"], 10)
            self.assertTrue(summary["action_inventory"]["truncated"])
            self.assertEqual(summary["action_inventory"]["overflow_count"], 2)
            self.assertEqual(summary["provider_custody_count"], 2)

    def test_decision_summary_preserves_branch_without_private_fields(self):
        protected = "PROTECTED-DOCUMENT-SENTINEL"
        document = {
            "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.5",
            "run_id": "trace-run",
            "execution_branch": {
                "command": "provider_reconciliation_cycle",
                "reason_code": "provider_reconciliation_due",
                "eligible_now": True,
                "action_ids": ["paid_0123456789abcdef01234567"],
            },
            "execution_capacity": {
                "disposition": "release_until_due",
                "reason_code": "provider_reconciliation_due",
            },
            "provider_custody": {
                "actions": [{
                    "action_id": "paid_0123456789abcdef01234567",
                    "provider_operation_id": "resp_trace_1",
                    "private_response": protected,
                }],
            },
            "local_dependencies": [],
            "private_prompt": protected,
        }
        summary = decision_summary(document, command="lifecycle", operation="inspect")
        rendered = json.dumps(summary, sort_keys=True)
        self.assertEqual(summary["selected_command"], "provider_reconciliation_cycle")
        self.assertEqual(summary["provider_custody_count"], 1)
        self.assertNotIn(protected, rendered)

    def test_exception_sanitizer_removes_credentials_and_query(self):
        diagnostic = sanitize_exception(
            RuntimeError("Bearer abc.def secret=rainbow sk-secretvalue"),
            endpoint="https://api.example.test/v1/responses/resp_1?token=secret",
        )
        rendered = json.dumps(diagnostic)
        self.assertNotIn("abc.def", rendered)
        self.assertNotIn("rainbow", rendered)
        self.assertNotIn("secretvalue", rendered)
        self.assertNotIn("?token", rendered)
        self.assertEqual(
            diagnostic["endpoint"], "https://api.example.test/v1/responses/resp_1"
        )

    def test_stage_summary_is_bounded_and_excludes_edit_material(self):
        protected = "PROTECTED-EDIT-SENTINEL"
        value = stage_evidence_summary({
            "attempt_number": 2,
            "state": "POLISH_ERROR",
            "paid_action_id": "paid_0123456789abcdef01234567",
            "provider_metadata": {"response_id": "resp_trace_2"},
            "validation_report": None,
            "lint_report": None,
            "editable_target_paths": [protected],
            "error": {
                "type": "ValueError",
                "message": f"Sparse edit repeated field {protected}",
            },
        }, stage="polish", subject_id="dog-trace")
        rendered = json.dumps(value, sort_keys=True)
        self.assertEqual(value["attempt_state"], "POLISH_ERROR")
        self.assertEqual(value["error_class"], "ValueError")
        self.assertFalse(value["validation_report_present"])
        self.assertNotIn(protected, rendered)

    def test_validation_summary_projects_codes_not_prose(self):
        protected = "PROTECTED-FINDING-PROSE"
        value = validation_evidence_summary(
            subject_id="dog-trace",
            validation_report={"status": "pass", "errors": [], "warnings": []},
            lint_report={
                "status": "warn", "warning_count": 2,
                "decks": [{
                    "warnings": [{
                        "code": "repeated_opening", "message": protected,
                        "details": {"excerpt": protected},
                    }],
                    "authoring_pass_acceptance": {
                        "status": "reject",
                        "rejection_reasons": [{
                            "code": "cross_card_exact_duplicate",
                            "message": protected,
                        }],
                    },
                }],
            },
        )
        rendered = json.dumps(value, sort_keys=True)
        self.assertEqual(value["lint_warning_codes"]["counts"], {
            "repeated_opening": 1,
        })
        self.assertEqual(value["rejection_codes"]["counts"], {
            "cross_card_exact_duplicate": 1,
        })
        self.assertNotIn(protected, rendered)

    def test_validation_code_inventory_is_bounded_with_overflow_digest(self):
        codes = [f"safe_code_{index}" for index in range(7)]
        value = validation_evidence_summary(
            subject_id="dog-trace",
            validation_report={"status": "pass", "errors": [], "warnings": []},
            lint_report={
                "status": "warn", "warning_count": 7,
                "decks": [{
                    "warnings": [{"code": code} for code in codes],
                    "authoring_pass_acceptance": {
                        "status": "accept", "rejection_reasons": [],
                    },
                }],
            },
        )
        distribution = value["lint_warning_codes"]
        self.assertEqual(len(distribution["counts"]), 4)
        self.assertEqual(distribution["unique_code_count"], 7)
        self.assertTrue(distribution["truncated"])
        self.assertEqual(distribution["overflow_code_count"], 3)
        self.assertEqual(len(distribution["codes_sha256"]), 64)

    def test_publication_summary_joins_sealed_identities_and_totals(self):
        state = {
            "status": "FINAL_QA_REQUIRES_REVIEW", "state_revision": 69,
            "spend_ledger": {"actions": [{
                "action_id": "paid_0123456789abcdef01234567",
                "state": "REPORTED", "provider": {"id": "resp_trace_1"},
            }]},
            "subjects": {"dog-trace": {
                "state": "FINAL_QA_WARN",
                "polish_attempts": [{"state": "POLISH_ERROR"}],
                "deck": "PROTECTED-DECK-PATH",
            }},
        }
        result = {
            "run_id": "trace-run", "outcome": "review_required",
            "cause_code": "final_qa_requires_review",
            "result_id": "nres_0123456789abcdef01234567",
            "result_sha256": "a" * 64,
            "invocation_id": "ninv_0123456789abcdef01234567",
        }
        receipt = {
            "receipt_id": "nreceipt_0123456789abcdef01234567",
            "receipt_sha256": "b" * 64,
            "checkpoint_basis_sha256": "c" * 64,
            "snapshot_sha256": "d" * 64,
        }
        value = publication_evidence_summary(state, result, receipt)
        rendered = json.dumps(value, sort_keys=True)
        self.assertEqual(value["action_count"], 1)
        self.assertEqual(value["provider_identity_count"], 1)
        self.assertEqual(value["optional_stage_state_counts"], "POLISH_ERROR:1")
        self.assertNotIn("PROTECTED-DECK-PATH", rendered)

    def test_recent_investigation_classes_are_distinguishable_from_trace(self):
        """Replay the operationally distinct classes that once required archives."""
        stream = io.StringIO()
        configure_logging(stream=stream, force=True)
        logger = logging.getLogger("replay-matrix")

        # Doughmeat-shaped: two successful attempts improved but did not clear
        # the final deterministic warning.
        log_stage_evidence_summary(logger, {
            "attempt_number": 1, "state": "POLISH_ACCEPTED",
            "accepted": True, "improved": True, "warning_count": 2,
            "validation_error_count": 0,
        }, stage="polish", subject_id="dog-doughmeat")
        log_stage_evidence_summary(logger, {
            "attempt_number": 2, "state": "POLISH_ACCEPTED",
            "accepted": True, "improved": True, "warning_count": 1,
            "validation_error_count": 0,
        }, stage="polish", subject_id="dog-doughmeat")
        log_validation_evidence_summary(
            logger, subject_id="dog-doughmeat",
            validation_report={"status": "pass", "errors": [], "warnings": [{}]},
            lint_report={
                "status": "warn", "warning_count": 3,
                "decks": [{
                    "warnings": [
                        {"code": "repeated_opening"},
                        {"code": "repeated_opening"},
                        {"code": "repeated_opening"},
                    ],
                    "authoring_pass_acceptance": {
                        "status": "accept", "rejection_reasons": [],
                    },
                }],
            },
        )

        # Macaron-shaped: the second attempt failed structurally and the final
        # report retained two closed rejection classifications.
        log_stage_evidence_summary(logger, {
            "attempt_number": 1, "state": "POLISH_ACCEPTED",
            "accepted": True, "improved": True, "warning_count": 7,
            "validation_error_count": 0,
        }, stage="polish", subject_id="dog-macaron")
        log_stage_evidence_summary(logger, {
            "attempt_number": 2, "state": "POLISH_ERROR",
            "accepted": False,
            "error": {"type": "ValueError", "message": "protected edit detail"},
        }, stage="polish", subject_id="dog-macaron")
        log_validation_evidence_summary(
            logger, subject_id="dog-macaron",
            validation_report={"status": "pass", "errors": [], "warnings": []},
            lint_report={
                "status": "warn", "warning_count": 6,
                "decks": [{
                    "warnings": [{"code": "repeated_opening"}],
                    "authoring_pass_acceptance": {
                        "status": "reject",
                        "rejection_reasons": [
                            {"code": "cross_card_exact_duplicate"},
                            {"code": "multi_field_opening_template"},
                        ],
                    },
                }],
            },
        )

        # The remaining matrix uses already-public decision/result vocabulary:
        # adoption, due/not-due custody, ambiguity, refusal, and publication.
        for outcome, reason in (
            ("progressed_local", "completed_provider_evidence_consumed"),
            ("provider_pending", "provider_reconciliation_due"),
            ("provider_pending", "provider_reconciliation_not_due"),
            ("ambiguous_submission", "provider_call_interrupted_after_fence"),
            ("pre_provider_refusal", "request_payload_unavailable"),
        ):
            log_decision_summary(logger, {
                "schema_version": "trace.replay.v1", "outcome": outcome,
                "reason_code": reason,
            }, command="replay", operation="classify")
        log_publication_evidence_summary(
            logger,
            {
                "status": "FINAL_QA_REQUIRES_REVIEW", "state_revision": 79,
                "spend_ledger": {"actions": [{
                    "action_id": "paid_0123456789abcdef01234567",
                    "state": "WAITING", "provider": {"id": "resp_trace_9"},
                }]},
                "subjects": {},
            },
            {
                "run_id": "trace-run", "outcome": "review_required",
                "cause_code": "final_qa_requires_review",
                "result_id": "nres_0123456789abcdef01234567",
                "result_sha256": "a" * 64,
            },
            {
                "receipt_id": "nreceipt_0123456789abcdef01234567",
                "receipt_sha256": "b" * 64,
            },
        )
        logger.error(
            "finalization_contract_invalid error_class=AssemblyContractError "
            "exception_fingerprint=0123456789abcdef"
        )

        # Render prepends its own envelope timestamp before the SBE marker.
        rendered = "\n".join(
            f"2026-09-04T12:00:00Z {line}"
            for line in stream.getvalue().splitlines()
        )
        trace = parse_trace_text(rendered, source_name="replay.log")
        events = trace["events"]
        stage_events = [
            event for event in events
            if event["event"] == "native_stage_evidence_summary"
        ]
        validation_events = [
            event for event in events
            if event["event"] == "native_validation_evidence_summary"
        ]
        self.assertEqual(len(stage_events), 4)
        self.assertEqual(
            [event["fields"]["state"] for event in stage_events],
            ["POLISH_ACCEPTED", "POLISH_ACCEPTED", "POLISH_ACCEPTED", "POLISH_ERROR"],
        )
        self.assertEqual(stage_events[-1]["fields"]["error_class"], "ValueError")
        self.assertIn(
            ";codes:repeated_opening:3;",
            validation_events[0]["fields"]["lint_warning_codes"],
        )
        self.assertIn(
            ";codes:cross_card_exact_duplicate:1,multi_field_opening_template:1;",
            validation_events[1]["fields"]["rejection_codes"],
        )
        decisions = [
            event["fields"] for event in events
            if event["event"] == "native_decision_summary"
        ]
        self.assertEqual(
            {(item["outcome"], item["reason"]) for item in decisions},
            {
                ("progressed_local", "completed_provider_evidence_consumed"),
                ("provider_pending", "provider_reconciliation_due"),
                ("provider_pending", "provider_reconciliation_not_due"),
                ("ambiguous_submission", "provider_call_interrupted_after_fence"),
                ("pre_provider_refusal", "request_payload_unavailable"),
            },
        )
        publication = next(
            event for event in events
            if event["event"] == "native_publication_evidence_summary"
        )
        self.assertEqual(publication["fields"]["outcome"], "review_required")
        self.assertEqual(publication["fields"]["provider_identity_count"], 1)
        failure = next(
            event for event in events
            if event["event"] == "finalization_contract_invalid"
        )
        self.assertEqual(failure["fields"]["error_class"], "AssemblyContractError")

    def test_durable_change_adapter_emits_only_newly_classified_evidence(self):
        prior = {
            "subjects": {"dog-trace": {
                "polish_attempts": [{"attempt_number": 1, "state": "SUBMITTED"}],
                "validation": None,
                "lint": None,
            }},
        }
        current = {
            "subjects": {"dog-trace": {
                "polish_attempts": [{
                    "attempt_number": 1, "state": "POLISH_ERROR",
                    "error": {"type": "ValueError", "message": "bad edit"},
                }],
                "validation": {
                    "report": {"status": "pass", "errors": [], "warnings": []},
                },
                "lint": {
                    "report": {"status": "warn", "warning_count": 1,
                               "decks": []},
                },
            }},
        }
        with self.assertLogs(
            "astrowoof_natal_authoring.closure", level="INFO",
        ) as captured:
            _log_durable_evidence_changes(prior, current)
        rendered = "\n".join(captured.output)
        self.assertIn("native_stage_evidence_summary", rendered)
        self.assertIn("state=POLISH_ERROR", rendered)
        self.assertIn("native_validation_evidence_summary", rendered)
        self.assertIn("validation_status=pass", rendered)

        with self.assertNoLogs(
            "astrowoof_natal_authoring.closure", level="INFO",
        ):
            _log_durable_evidence_changes(current, current)

    def test_logger_failure_is_isolated(self):
        logger = _FailingLogger()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = self._state(root)
            self.assertIsNone(log_workspace_fingerprint(
                logger, root, state, validation_outcome="valid", sbe_release="0.test",
            ))
            self.assertIsNone(log_native_state_summary(logger, state, phase="entry"))
            self.assertIsNone(log_decision_summary(
                logger, {"schema_version": "x"}, command="test",
            ))
            log_cli_exit(
                logger, command="test", operation=None, exit_code=3,
                outcome="refused", authoritative_transport="output_file",
            )

    def test_human_trace_contains_searchable_boundary_names(self):
        stream = io.StringIO()
        configure_logging(stream=stream, force=True)
        logger = logging.getLogger("trace-test")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = self._state(root)
            (root / "workspace-snapshot.json").write_text(
                json.dumps({"members": []}), encoding="utf-8"
            )
            log_workspace_fingerprint(
                logger, root, state, validation_outcome="valid", sbe_release="0.test",
            )
            log_native_state_summary(logger, state, phase="entry")
            log_decision_summary(
                logger, {
                    "schema_version": "trace.result.v1", "outcome": "pending",
                    "ordered_action_ids": ["paid_0123456789abcdef01234567"],
                }, command="trace_test", operation="inspect",
            )
            attempt = {
                "attempt_number": 1, "state": "POLISH_NO_CHANGE",
                "accepted": False, "improved": False,
            }
            log_stage_evidence_summary(
                logger, attempt, stage="polish", subject_id="dog-trace",
            )
            log_validation_evidence_summary(
                logger,
                validation_report={"status": "pass", "errors": [], "warnings": []},
                lint_report={"status": "pass", "warning_count": 0, "decks": []},
                subject_id="dog-trace",
            )
            log_publication_evidence_summary(
                logger,
                {"run_id": "trace-run", "status": "DONE", "subjects": {}},
                {"run_id": "trace-run", "outcome": "completed",
                 "result_id": "nres_0123456789abcdef01234567",
                 "result_sha256": "a" * 64},
                {"receipt_id": "nreceipt_0123456789abcdef01234567",
                 "receipt_sha256": "b" * 64},
            )
            log_cli_exit(
                logger, command="trace_test", operation="inspect", exit_code=3,
                outcome="pending", authoritative_transport="stdout_json",
            )
        rendered = stream.getvalue()
        self.assertIn("✨🐶", rendered)
        self.assertIn("workspace_fingerprint", rendered)
        self.assertIn("native_state_summary", rendered)
        self.assertIn("native_decision_summary", rendered)
        self.assertIn("native_stage_evidence_summary", rendered)
        self.assertIn("native_validation_evidence_summary", rendered)
        self.assertIn("native_publication_evidence_summary", rendered)
        self.assertIn("command_exit", rendered)


if __name__ == "__main__":
    unittest.main()
