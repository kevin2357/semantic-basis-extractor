from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.cli.run_report import main as cli_main
from astrowoof_natal_authoring.run_report import (
    build_report_from_text,
    parse_trace_text,
    render_report_html,
    render_report_markdown,
    render_report_mermaid,
    read_run_evolution_report,
    read_run_evolution_report_schema,
    validate_run_evolution_report,
)
from astrowoof_natal_authoring.run_report_qa import (
    read_run_report_qualification_schema,
    run_run_report_qualification,
    validate_run_report_qualification,
)


def _line(ts: str, run: str, function: str, state: str, message: str) -> str:
    return (
        f"{ts}Z ✨🐶 {ts}Z | INFO | host-fixture | {run} | - | "
        f"{function} | {state} : {message}"
    )


def fixture_log() -> str:
    run = "a" * 64
    return "\n".join([
        "2026-08-31T10:00:00Z ordinary render line",
        _line("2026-08-31T10:00:01", run, "workspace", "WAITING_FOR_RESPONSE",
              "workspace_fingerprint revision=4 snapshot_sha256=" + "b" * 64 + " sbe_release=0.4.37"),
        _line("2026-08-31T10:00:02", run, "inspect", "WAITING_FOR_RESPONSE",
              "lifecycle_inspection_complete status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=4 provider_actions=6 local_dependencies=0"),
        _line("2026-08-31T10:00:03", run, "command", "WAITING_FOR_RESPONSE",
              "command_exit command=provider_reconciliation_cycle exit_code=0 outcome=provider_pending"),
        _line("2026-08-31T10:01:02", run, "inspect", "WAITING_FOR_RESPONSE",
              "lifecycle_inspection_complete status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=4 provider_actions=6 local_dependencies=0"),
        _line("2026-08-31T10:01:03", run, "attempt", "WAITING_FOR_RESPONSE",
              "authoring_attempt_accepted pass_id=dog-fixture_1 attempt=1 action_id=paid_" + "1" * 24),
        _line("2026-08-31T10:01:04", run, "checkpoint", "AUTHORING_COMPLETE",
              "checkpoint_committed state_revision=5 snapshot_sha256=" + "c" * 64),
        _line("2026-08-31T10:01:05", run, "provider", "WAITING",
              "provider_identity_recorded action_id=paid_" + "2" * 24 + " provider_id=resp_fixture_2 provider_kind=response"),
        _line("2026-08-31T10:01:06", run, "privacy", "WAITING",
              "native_decision_summary payload=PROTECTED_SENTINEL prompt=PROTECTED_SENTINEL outcome=ok"),
        _line("2026-08-31T10:01:06", run, "acceptance", "AUTHORING",
              "pass_acceptance_advisory codes=theme_group_coverage affected_claim_count=19"),
        "2026-08-31T10:01:07Z {\"envelope_type\":\"command_result\",\"result\":{}}",
    ]) + "\n"


def _structured_line(
    timestamp: str, *, outer: str = "", message: str = "✨🐶 command exited",
) -> str:
    value = {
        "schema_version": "astrowoof.sbe_worker_log.v1",
        "record_type": "application_log",
        "timestamp": timestamp,
        "level": "INFO",
        "event_name": "command_exit",
        "message": message,
        "logger": "astrowoof_natal_authoring.fixture",
        "function": "main",
        "current_state": "WAITING_FOR_RESPONSE",
        "correlation": {
            "api_run_id": "api-run-fixture",
            "native_run_id": "native-run-fixture",
            "subject_id": None,
            "invocation_id": "invocation-fixture",
            "action_id": None,
            "provider_operation_id": None,
            "checkpoint_object_id": "checkpoint-fixture",
        },
        "payload": {
            "command": "provider_reconciliation_cycle",
            "operation": "inspect",
            "exit_code": 0,
            "outcome": "provider_pending",
            "result_id": None,
            "receipt_id": None,
            "authoritative_transport": "output_file",
            "mutation_status": "unchanged",
            "publication_status": "not_published",
            "provider_io_status": "retrieval_only",
        },
        "producer": {
            "service": "sbe-worker", "host_id": "host-fixture",
            "runtime_version": "0.4.test",
        },
        "exception": None,
    }
    rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return f"{outer} {rendered}".lstrip()


class RunReportTests(unittest.TestCase):
    def test_parser_is_deterministic_partitioned_and_privacy_bounded(self):
        text = fixture_log()
        first = parse_trace_text(text, source_name="fixture.log")
        second = parse_trace_text(text, source_name="fixture.log")
        self.assertEqual(first, second)
        self.assertEqual(9, first["coverage"]["trace_marker_line_count"])
        self.assertEqual(9, first["coverage"]["parsed_trace_line_count"])
        self.assertEqual(1, first["coverage"]["json_envelope_count"])
        self.assertNotIn("PROTECTED_SENTINEL", json.dumps(first))

    def test_reducer_builds_lanes_epochs_and_no_progress_candidate(self):
        report = build_report_from_text(fixture_log(), source_name="fixture.log")
        validate_run_evolution_report(report)
        self.assertEqual(1, len(report["runs"]))
        run = report["runs"][0]
        self.assertTrue(any(lane["kind"] == "pass" for lane in run["lanes"]))
        self.assertTrue(any(lane["kind"] == "action" for lane in run["lanes"]))
        self.assertEqual(1, len(run["no_progress_candidates"]))
        self.assertEqual(0, run["no_progress_candidates"][0]["progress_witness_count"])
        self.assertTrue(run["final_observed_posture"]["not_authoritative_current_state"])

    def test_progress_witness_prevents_false_loop(self):
        text = fixture_log().replace(
            "command_exit command=provider_reconciliation_cycle exit_code=0 outcome=provider_pending",
            "reconciliation_completed selected_count=4 outcome=completed",
        )
        report = build_report_from_text(text)
        self.assertEqual([], report["runs"][0]["no_progress_candidates"])

    def test_checkpoint_only_republication_is_still_a_no_progress_candidate(self):
        run = "d" * 64
        text = "\n".join([
            _line("2026-08-31T11:00:00", run, "workspace", "WAITING_FOR_RESPONSE",
                  "workspace_fingerprint revision=4 snapshot_sha256=" + "1" * 64),
            _line("2026-08-31T11:00:01", run, "inspect", "WAITING_FOR_RESPONSE",
                  "lifecycle_inspection_complete status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=4 provider_actions=6 local_dependencies=0"),
            _line("2026-08-31T11:00:02", run, "command", "WAITING_FOR_RESPONSE",
                  "command_exit command=provider_reconciliation_cycle exit_code=0 outcome=provider_pending"),
            _line("2026-08-31T11:00:03", run, "workspace", "WAITING_FOR_RESPONSE",
                  "workspace_fingerprint revision=5 snapshot_sha256=" + "2" * 64),
            _line("2026-08-31T11:00:04", run, "inspect", "WAITING_FOR_RESPONSE",
                  "lifecycle_inspection_complete status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=4 provider_actions=6 local_dependencies=0"),
        ]) + "\n"
        candidates = build_report_from_text(text)["runs"][0]["no_progress_candidates"]
        self.assertEqual(1, len(candidates))
        self.assertEqual("candidate_semantic_republication_cycle", candidates[0]["classification"])
        self.assertTrue(candidates[0]["checkpoint_posture_changed"])

    def test_report_digest_and_closed_shape_refuse_mutation(self):
        report = build_report_from_text(fixture_log())
        changed = copy.deepcopy(report)
        changed["diagnostic_only"] = False
        with self.assertRaises(ValueError):
            validate_run_evolution_report(changed)
        changed = copy.deepcopy(report)
        changed["extra"] = True
        with self.assertRaises(ValueError):
            validate_run_evolution_report(changed)

    def test_renderers_are_deterministic_and_interactive_html_is_self_contained(self):
        report = build_report_from_text(fixture_log())
        markdown = render_report_markdown(report)
        mermaid = render_report_mermaid(report)
        rendered = render_report_html(report)
        self.assertEqual(rendered, render_report_html(report))
        self.assertIn("| Lane |", markdown)
        self.assertTrue(mermaid.startswith("sequenceDiagram\n"))
        self.assertIn("No-progress only", rendered)
        self.assertIn("Lane filter", rendered)
        self.assertNotIn("fetch(", rendered)

    def test_cli_builds_all_four_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "worker.log"
            output = root / "report"
            source.write_text(fixture_log(), encoding="utf-8")
            self.assertEqual(0, cli_main([
                "build", "--input", str(source), "--output-dir", str(output),
            ]))
            self.assertEqual(
                {"report.html", "report.json", "report.md", "report.mmd"},
                {item.name for item in output.iterdir()},
            )
            validate_run_evolution_report(json.loads(
                (output / "report.json").read_text(encoding="utf-8")
            ))

    def test_malformed_trace_is_counted_not_silently_discarded(self):
        trace = parse_trace_text("2026Z ✨🐶 broken\n")
        self.assertEqual([1], trace["coverage"]["malformed_trace_line_numbers"])
        self.assertEqual(0, trace["coverage"]["parsed_trace_line_count"])

    def test_render_dashboard_spaced_outer_timestamp_is_supported(self):
        run = "e" * 64
        text = (
            "2026-09-02 12:30:34  ✨🐶 2026-09-02T12:30:34.620Z | "
            f"INFO | render-host | {run} | - | main | AUTHORING : "
            "command_start command=semantic_closure\n"
            "2026-09-02 12:30:35  {\"envelope_type\":\"command_result\","
            "\"result\":{}}\n"
        )
        trace = parse_trace_text(text, source_name="render-export.log")
        self.assertEqual(1, trace["coverage"]["parsed_trace_line_count"])
        self.assertEqual(1, trace["coverage"]["json_envelope_count"])
        self.assertEqual([], trace["coverage"]["malformed_trace_line_numbers"])

    def test_mixed_pipe_and_structured_json_prefers_native_json_fields(self):
        pipe = _line(
            "2026-09-06T10:00:00", "pipe-run", "main", "WAITING",
            "command_exit command=legacy exit_code=0 outcome=complete",
        )
        structured = _structured_line(
            "2026-09-06T10:00:01.000Z",
            outer="2026-09-06 04:00:01 Render:",
            message="✨🐶 provider_identity_recorded action_id=misleading",
        )
        trace = parse_trace_text(pipe + "\n" + structured + "\n")
        self.assertEqual(2, trace["coverage"]["parsed_trace_line_count"])
        event = trace["events"][1]
        self.assertEqual("command_exit", event["event"])
        self.assertEqual("native-run-fixture", event["run_id"])
        self.assertEqual("provider_pending", event["fields"]["outcome"])
        self.assertNotIn("action_id", event["fields"])

    def test_structured_records_are_chronological_and_exact_duplicates_collapse(self):
        later = _structured_line(
            "2026-09-06T10:00:02.000Z", outer="relay-a",
        )
        earlier = _structured_line(
            "2026-09-06T10:00:01.000Z", outer="relay-b",
        )
        duplicate = _structured_line(
            "2026-09-06T10:00:02.000Z", outer="relay-c",
        )
        trace = parse_trace_text("\n".join([later, earlier, duplicate]) + "\n")
        self.assertEqual(
            [
                "2026-09-06T10:00:01.000Z",
                "2026-09-06T10:00:02.000Z",
                "2026-09-06T10:00:02.000Z",
            ],
            [event["timestamp"] for event in trace["events"]],
        )
        self.assertEqual([3], trace["coverage"]["duplicate_trace_line_numbers"])

    def test_truncated_malformed_and_unknown_json_are_accounted(self):
        truncated = _structured_line("2026-09-06T10:00:01.000Z")[:-5]
        malformed = json.loads(_structured_line("2026-09-06T10:00:02.000Z"))
        del malformed["correlation"]["api_run_id"]
        unknown = {"schema_version": "other.service.v1", "message": "✨🐶 foreign"}
        envelope = {"envelope_type": "command_result", "result": {}}
        text = "\n".join([
            truncated,
            json.dumps(malformed, ensure_ascii=False),
            json.dumps(unknown, ensure_ascii=False),
            json.dumps(envelope),
        ]) + "\n"
        trace = parse_trace_text(text)
        self.assertEqual([1, 2], trace["coverage"]["malformed_trace_line_numbers"])
        self.assertEqual(1, trace["coverage"]["unknown_json_record_count"])
        self.assertEqual(1, trace["coverage"]["json_envelope_count"])

    def test_structured_message_prose_is_not_copied_into_report(self):
        protected = "PROTECTED-REPORTER-SENTINEL"
        text = _structured_line(
            "2026-09-06T10:00:01.000Z", message=f"✨🐶 {protected}",
        ) + "\n"
        trace = parse_trace_text(text)
        report = build_report_from_text(text)
        self.assertNotIn(protected, json.dumps(trace, sort_keys=True))
        self.assertNotIn(protected, json.dumps(report, sort_keys=True))

    def test_provider_free_qualification_is_closed_and_replayable(self):
        first = run_run_report_qualification()
        second = run_run_report_qualification()
        self.assertEqual(first, second)
        validate_run_report_qualification(first)
        changed = copy.deepcopy(first)
        changed["provider_call_count"] = 1
        with self.assertRaises(ValueError):
            validate_run_report_qualification(changed)

    def test_packaged_schema_readers_and_public_report_reader(self):
        self.assertEqual(
            "astrowoof.sbe_run_evolution_report.v1",
            read_run_evolution_report_schema()["properties"]["schema_version"]["const"],
        )
        self.assertEqual(
            "astrowoof.sbe_run_report_qualification.v1",
            read_run_report_qualification_schema()["properties"]["schema_version"]["const"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "report.json"
            report = build_report_from_text(fixture_log())
            path.write_text(json.dumps(report), encoding="utf-8")
            self.assertEqual(report, read_run_evolution_report(path))

    def test_root_package_exports_reporter_surface(self):
        import astrowoof_natal_authoring as public

        for name in (
            "build_report_from_text", "read_run_evolution_report",
            "read_run_evolution_report_schema", "run_run_report_qualification",
            "validate_run_evolution_report",
        ):
            self.assertTrue(callable(getattr(public, name)))


if __name__ == "__main__":
    unittest.main()
