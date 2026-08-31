from __future__ import annotations

import io
import json
import logging
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.application_logging import configure_logging
from astrowoof_natal_authoring.trace_observability import (
    bounded_identifiers,
    decision_summary,
    log_cli_exit,
    log_decision_summary,
    log_native_state_summary,
    log_workspace_fingerprint,
    native_state_summary,
    sanitize_exception,
    workspace_fingerprint,
)


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
            log_cli_exit(
                logger, command="trace_test", operation="inspect", exit_code=3,
                outcome="pending", authoritative_transport="stdout_json",
            )
        rendered = stream.getvalue()
        self.assertIn("✨🐶", rendered)
        self.assertIn("workspace_fingerprint", rendered)
        self.assertIn("native_state_summary", rendered)
        self.assertIn("native_decision_summary", rendered)
        self.assertIn("command_exit", rendered)


if __name__ == "__main__":
    unittest.main()
