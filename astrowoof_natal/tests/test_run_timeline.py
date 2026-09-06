from __future__ import annotations

import copy
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.run_timeline import (
    build_run_cohort_timeline,
    read_run_cohort_timeline,
    read_run_cohort_timeline_schema,
    render_run_cohort_timeline_html,
    validate_run_cohort_timeline,
)
from astrowoof_natal_authoring.run_report import build_report_from_text
from astrowoof_natal_authoring.cli.run_report import main as cli_main


def _digest(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


SOURCE_SHA = "1" * 64


def _native_line(timestamp: str, run_id: str, event_name: str, message: str) -> str:
    return (
        f"{timestamp}Z ✨🐶 {timestamp}Z | INFO | host-fixture | {run_id} | "
        f"invocation-fixture | main | WAITING_FOR_RESPONSE : {event_name} {message}"
    )


def _wrapper_line(
    timestamp: str, event_name: str, *, api_run: str,
    native_run: str | None, **payload,
) -> str:
    value = {
        "schema_version": "astrowoof.execution_event.v1",
        "envelope_type": "execution_event",
        "event_id": f"{event_name}-{api_run}-{timestamp}",
        "event_name": event_name,
        "observed_at": timestamp,
        "producer": {
            "service": "api-worker", "component": "queue-worker", "instance_id": "worker-one",
        },
        "correlation": {
            "run_id": api_run,
            "job_id": f"job-{api_run}", "attempt_id": f"attempt-{api_run}",
            "lease_id": f"lease-{api_run}", "invocation_id": None, "action_id": None,
        },
        "payload": payload,
    }
    if native_run is not None:
        value["correlation"]["native_run_id"] = native_run
    return json.dumps(value, sort_keys=True)


def reducer_log() -> str:
    a, b = "native-a", "native-b"
    return "\n".join([
        _wrapper_line("2026-09-06T18:15:00.000Z", "worker.lease.acquired", api_run="api-a", native_run=a),
        _wrapper_line("2026-09-06T18:15:00.010Z", "sbe.cycle.started", api_run="api-a", native_run=a),
        _native_line("2026-09-06T18:15:00.020", a, "reconciliation_cycle_start", "selected_count=1"),
        _wrapper_line("2026-09-06T18:15:41.548Z", "sbe.cycle.completed", api_run="api-a", native_run=a, execution_branch="provider_reconciliation"),
        _wrapper_line("2026-09-06T18:15:41.549Z", "worker.lease.released", api_run="api-a", native_run=a),
        _wrapper_line("2026-09-06T18:15:41.651Z", "worker.lease.acquired", api_run="api-b", native_run=b),
        _wrapper_line("2026-09-06T18:15:41.652Z", "sbe.cycle.started", api_run="api-b", native_run=b),
        _native_line("2026-09-06T18:15:41.660", b, "initial_wave_start", "selected_count=6"),
        _wrapper_line("2026-09-06T18:16:36.024Z", "sbe.cycle.completed", api_run="api-b", native_run=b, execution_branch="initial_wave"),
        _wrapper_line("2026-09-06T18:16:36.025Z", "worker.lease.released", api_run="api-b", native_run=b),
    ]) + "\n"


def _boundary(
    timestamp: str,
    event_name: str,
    *,
    line: int,
    api_run_id: str,
    native_run_id: str,
    attempt_id: str,
    lease_id: str,
    family: str = "api_worker_wrapper",
):
    body = {
        "canonical_timestamp": timestamp,
        "canonical_timestamp_field": (
            "message.observed_at" if family == "api_worker_wrapper" else "message.timestamp"
        ),
        "outer_timestamp": timestamp,
        "clock_relation": "exact",
        "source_sha256": SOURCE_SHA,
        "source_line": line,
        "raw_line_sha256": f"{line:064x}",
        "event_name": event_name,
        "evidence_family": family,
        "producer": {
            "service": "sbe-worker",
            "component": "queue-worker" if family == "api_worker_wrapper" else "native-runtime",
            "instance_id": "worker-fixture",
        },
        "correlation": {
            "api_run_id": api_run_id,
            "native_run_id": native_run_id,
            "job_id": "job-fixture",
            "attempt_id": attempt_id,
            "lease_id": lease_id,
            "invocation_id": None,
            "action_id": None,
            "event_id": f"event-{line}",
        },
    }
    return {"boundary_id": _digest(body), **body}


def _interval(classification, label, start, end):
    body = {
        "classification": classification,
        "status": "complete",
        "label": label,
        "start": start,
        "end": end,
        "duration_ms": round((
            __import__("datetime").datetime.fromisoformat(end["canonical_timestamp"][:-1] + "+00:00")
            - __import__("datetime").datetime.fromisoformat(start["canonical_timestamp"][:-1] + "+00:00")
        ).total_seconds() * 1000),
        "evidence_families": sorted({start["evidence_family"], end["evidence_family"]}),
        "constituent_boundary_ids": sorted([start["boundary_id"], end["boundary_id"]]),
        "no_progress_candidate_ids": [],
    }
    return {"interval_id": _digest(body), **body}


def fixture_timeline():
    run_a = "api-run-a"
    native_a = "native-run-a"
    first_start = _boundary(
        "2026-09-06T18:15:00.000Z", "sbe.cycle.started", line=1,
        api_run_id=run_a, native_run_id=native_a, attempt_id="attempt-a", lease_id="lease-a",
    )
    first_end = _boundary(
        "2026-09-06T18:15:41.548Z", "sbe.cycle.completed", line=2,
        api_run_id=run_a, native_run_id=native_a, attempt_id="attempt-a", lease_id="lease-a",
    )
    first_interval = _interval("provider_reconciliation", "Provider reconciliation", first_start, first_end)

    run_b = "api-run-b"
    native_b = "native-run-b"
    second_start = _boundary(
        "2026-09-06T18:15:41.651Z", "sbe.cycle.started", line=3,
        api_run_id=run_b, native_run_id=native_b, attempt_id="attempt-b", lease_id="lease-b",
    )
    second_end = _boundary(
        "2026-09-06T18:16:36.024Z", "sbe.cycle.completed", line=4,
        api_run_id=run_b, native_run_id=native_b, attempt_id="attempt-b", lease_id="lease-b",
    )
    second_interval = _interval("initial_provider_wave", "Initial provider wave", second_start, second_end)
    runs = [
        {
            "api_run_id": run_a,
            "native_run_id": native_a,
            "first_timestamp": first_start["canonical_timestamp"],
            "last_timestamp": first_end["canonical_timestamp"],
            "intervals": [first_interval],
            "no_progress_candidate_ids": [],
            "final_observed_posture": {
                "classification": "in_progress",
                "not_authoritative_current_state": True,
                "boundary_ids": [first_end["boundary_id"]],
            },
        },
        {
            "api_run_id": run_b,
            "native_run_id": native_b,
            "first_timestamp": second_start["canonical_timestamp"],
            "last_timestamp": second_end["canonical_timestamp"],
            "intervals": [second_interval],
            "no_progress_candidate_ids": [],
            "final_observed_posture": {
                "classification": "in_progress",
                "not_authoritative_current_state": True,
                "boundary_ids": [second_end["boundary_id"]],
            },
        },
    ]
    handoff_body = {
        "kind": "observed_execution_handoff",
        "from_interval_id": first_interval["interval_id"],
        "to_interval_id": second_interval["interval_id"],
        "duration_ms": 103,
        "witness_only_not_sla": True,
    }
    body = {
        "schema_version": "astrowoof.sbe_run_cohort_timeline.v1",
        "diagnostic_only": True,
        "canonical_timezone": "UTC",
        "source_reports": [{
            "report_sha256": "2" * 64,
            "source_sha256": SOURCE_SHA,
            "trace_sha256": "3" * 64,
            "parser_version": "astrowoof.sbe_trace_parser.v1",
        }],
        "log_sources": [{"name": "cohort.log", "sha256": SOURCE_SHA, "line_count": 4}],
        "adapter_coverage": {
            "wrapper_candidate_count": 4,
            "accepted_wrapper_event_count": 4,
            "refused_wrapper_line_numbers": [],
            "refused_wrapper_overflow": 0,
            "unsupported_wrapper_events": [],
        },
        "runs": runs,
        "observed_handoffs": [{"handoff_id": _digest(handoff_body), **handoff_body}],
    }
    return {"timeline_sha256": _digest(body), **body}


class RunCohortTimelineContractTests(unittest.TestCase):
    def test_deployed_start_without_native_identity_pairs_after_exact_join(self):
        text = "\n".join([
            _wrapper_line(
                "2026-09-06T18:15:00.000Z", "worker.lease.acquired",
                api_run="api-a", native_run=None,
            ),
            _wrapper_line(
                "2026-09-06T18:15:00.010Z", "sbe.cycle.started",
                api_run="api-a", native_run=None,
            ),
            _native_line(
                "2026-09-06T18:15:00.020", "native-a",
                "reconciliation_cycle_start", "selected_count=1",
            ),
            _wrapper_line(
                "2026-09-06T18:15:41.548Z", "sbe.cycle.completed",
                api_run="api-a", native_run="native-a",
                execution_branch="provider_reconciliation",
            ),
            _wrapper_line(
                "2026-09-06T18:15:41.549Z", "worker.lease.released",
                api_run="api-a", native_run="native-a",
            ),
        ]) + "\n"
        report = build_report_from_text(text, source_name="deployed.log")
        timeline = build_run_cohort_timeline(report, text, source_name="deployed.log")
        self.assertEqual(4, timeline["adapter_coverage"]["accepted_wrapper_event_count"])
        self.assertEqual([], timeline["adapter_coverage"]["refused_wrapper_line_numbers"])
        run = timeline["runs"][0]
        self.assertEqual("native-a", run["native_run_id"])
        self.assertEqual(
            {"observed_execution_allocation", "provider_reconciliation"},
            {interval["classification"] for interval in run["intervals"]},
        )
        self.assertFalse(any(
            interval["label"].startswith("Unpaired API event")
            for interval in run["intervals"]
        ))

    def test_unresolved_or_contradictory_progressive_run_join_fails_closed(self):
        unresolved = _wrapper_line(
            "2026-09-06T18:15:00.000Z", "sbe.cycle.started",
            api_run="api-a", native_run=None,
        ) + "\n" + _native_line(
            "2026-09-06T18:15:00.020", "native-a", "command_exit", "outcome=done",
        ) + "\n"
        report = build_report_from_text(unresolved, source_name="unresolved.log")
        with self.assertRaisesRegex(ValueError, "at least one run"):
            build_run_cohort_timeline(report, unresolved, source_name="unresolved.log")

        contradictory = "\n".join([
            _wrapper_line(
                "2026-09-06T18:15:00.000Z", "sbe.cycle.completed",
                api_run="api-a", native_run="native-a",
                execution_branch="provider_reconciliation",
            ),
            _wrapper_line(
                "2026-09-06T18:15:01.000Z", "worker.lease.released",
                api_run="api-a", native_run="native-b",
            ),
            _native_line(
                "2026-09-06T18:15:02.000", "native-a", "command_exit", "outcome=done",
            ),
        ]) + "\n"
        report = build_report_from_text(contradictory, source_name="contradictory.log")
        with self.assertRaisesRegex(ValueError, "contradict API/native run identity"):
            build_run_cohort_timeline(report, contradictory, source_name="contradictory.log")

    def test_cli_timeline_and_build_emit_valid_shared_axis_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "cohort.log"
            source.write_text(reducer_log(), encoding="utf-8")
            explicit = root / "explicit"
            self.assertEqual(0, cli_main([
                "timeline", "--input", str(source), "--output-dir", str(explicit),
                "--display-timezone", "America/Denver",
            ]))
            projection = read_run_cohort_timeline(explicit / "report.timeline.json")
            self.assertEqual(2, len(projection["runs"]))
            self.assertIn("America/Denver", (
                explicit / "report.timeline.html"
            ).read_text(encoding="utf-8"))

            combined = root / "combined"
            self.assertEqual(0, cli_main([
                "build", "--input", str(source), "--output-dir", str(combined),
            ]))
            self.assertEqual({
                "report.json", "report.md", "report.html", "report.mmd",
                "report.timeline.json", "report.timeline.html",
            }, {item.name for item in combined.iterdir()})

            rendered = root / "rerendered.html"
            self.assertEqual(0, cli_main([
                "render", "--report", str(combined / "report.timeline.json"),
                "--format", "timeline-html", "--output", str(rendered),
            ]))
            self.assertEqual(
                render_run_cohort_timeline_html(read_run_cohort_timeline(
                    combined / "report.timeline.json",
                )),
                rendered.read_text(encoding="utf-8"),
            )

    def test_cli_rejects_network_input_path(self):
        with contextlib.redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit):
                cli_main([
                    "timeline", "--input", "https://example.invalid/log",
                    "--output-dir", "unused",
                ])
        self.assertIn("network URLs are not supported", stderr.getvalue())

    def test_interactive_renderer_is_deterministic_self_contained_and_shared_axis(self):
        timeline = fixture_timeline()
        rendered = render_run_cohort_timeline_html(
            timeline, display_timezone="America/Denver",
        )
        self.assertEqual(
            rendered,
            render_run_cohort_timeline_html(timeline, display_timezone="America/Denver"),
        )
        for expected in (
            "Run cohort timeline", "Highlight run", "Hide waits",
            "Highlight no-progress", "domainStart", "observed_execution_handoff",
            "America/Denver", "witnessed handoff(s)",
        ):
            self.assertIn(expected, rendered)
        self.assertNotIn("fetch(", rendered)
        self.assertNotIn("http://", rendered)
        self.assertNotIn("https://", rendered)

    def test_renderer_refuses_unknown_timezone_and_invalid_contract(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            render_run_cohort_timeline_html(fixture_timeline(), display_timezone="Mars/Olympus")
        changed = copy.deepcopy(fixture_timeline())
        changed["diagnostic_only"] = False
        with self.assertRaises(ValueError):
            render_run_cohort_timeline_html(changed)

    def test_renderer_escapes_script_terminator_from_diagnostic_label(self):
        changed = copy.deepcopy(fixture_timeline())
        interval = changed["runs"][0]["intervals"][0]
        interval["label"] = "safe </script><script>unsafe()</script>"
        interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
        interval["interval_id"] = _digest(interval_body)
        changed["observed_handoffs"] = []
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        rendered = render_run_cohort_timeline_html(changed)
        self.assertNotIn("</script><script>unsafe()", rendered)
        self.assertIn("<\\/script><script>unsafe()<\\/script>", rendered)

    def test_reducer_builds_shared_axis_from_native_and_wrapper_evidence(self):
        text = reducer_log()
        report = build_report_from_text(text, source_name="cohort.log")
        timeline = build_run_cohort_timeline(report, text, source_name="cohort.log")
        self.assertGreater(timeline["adapter_coverage"]["accepted_wrapper_event_count"], 0)
        self.assertEqual(["api-a", "api-b"], [run["api_run_id"] for run in timeline["runs"]])
        classes = {
            run["api_run_id"]: {interval["classification"] for interval in run["intervals"]}
            for run in timeline["runs"]
        }
        self.assertIn("provider_reconciliation", classes["api-a"])
        self.assertIn("initial_provider_wave", classes["api-b"])
        self.assertEqual(
            {"observed_execution_allocation"},
            classes["api-a"] - {"provider_reconciliation"},
        )
        handoff = timeline["observed_handoffs"][0]
        self.assertEqual(104, handoff["duration_ms"])
        self.assertTrue(handoff["witness_only_not_sla"])
        wrapper_boundaries = [
            boundary
            for run in timeline["runs"]
            for interval in run["intervals"]
            for boundary in (interval["start"], interval["end"])
            if boundary is not None and boundary["evidence_family"] == "api_worker_wrapper"
        ]
        self.assertTrue(wrapper_boundaries)
        self.assertTrue(all(
            boundary["canonical_timestamp_field"] == "message.observed_at"
            for boundary in wrapper_boundaries
        ))
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "cohort.timeline.json"
            artifact.write_text(json.dumps(timeline), encoding="utf-8")
            restored = read_run_cohort_timeline(artifact)
        self.assertEqual(timeline, restored)
        self.assertTrue(any(
            interval["classification"] == "observed_execution_allocation"
            for run in restored["runs"]
            for interval in run["intervals"]
        ))

    def test_reducer_is_deterministic_and_binds_exact_source_bytes(self):
        text = reducer_log()
        report = build_report_from_text(text, source_name="cohort.log")
        first = build_run_cohort_timeline(report, text, source_name="cohort.log")
        second = build_run_cohort_timeline(report, text, source_name="cohort.log")
        self.assertEqual(first, second)
        with self.assertRaisesRegex(ValueError, "source bytes"):
            build_run_cohort_timeline(report, text + "ignored-looking-but-bound\n", source_name="cohort.log")

    def test_reducer_accounts_for_unsupported_and_malformed_wrapper_events(self):
        text = reducer_log()
        unsupported = json.loads(_wrapper_line(
            "2026-09-06T18:17:00.000Z", "worker.lease.acquired",
            api_run="api-a", native_run="native-a",
        ))
        unsupported["event_name"] = "worker.future.event"
        malformed = json.loads(_wrapper_line(
            "2026-09-06T18:17:01.000Z", "worker.lease.acquired",
            api_run="api-a", native_run="native-a",
        ))
        del malformed["observed_at"]
        text += json.dumps(unsupported) + "\n" + json.dumps(malformed) + "\n"
        report = build_report_from_text(text, source_name="cohort.log")
        timeline = build_run_cohort_timeline(report, text, source_name="cohort.log")
        self.assertEqual([12], timeline["adapter_coverage"]["refused_wrapper_line_numbers"])
        self.assertEqual(
            [{"event_name": "worker.future.event", "count": 1}],
            timeline["adapter_coverage"]["unsupported_wrapper_events"],
        )

    def test_reducer_surfaces_orphan_completion_as_unknown(self):
        text = reducer_log() + _wrapper_line(
            "2026-09-06T18:17:00.000Z", "worker.job.completed",
            api_run="api-a", native_run="native-a",
        ) + "\n"
        report = build_report_from_text(text, source_name="cohort.log")
        timeline = build_run_cohort_timeline(report, text, source_name="cohort.log")
        run = next(item for item in timeline["runs"] if item["api_run_id"] == "api-a")
        self.assertTrue(any(
            interval["classification"] == "unknown"
            and interval["start"]["event_name"] == "worker.job.completed"
            for interval in run["intervals"]
        ))

    def test_reversed_pair_is_explicitly_contradictory(self):
        text = "\n".join([
            _wrapper_line("2026-09-06T18:17:02.000Z", "sbe.cycle.started", api_run="api-a", native_run="native-a"),
            _wrapper_line("2026-09-06T18:17:01.000Z", "sbe.cycle.completed", api_run="api-a", native_run="native-a", execution_branch="provider_reconciliation"),
            _native_line("2026-09-06T18:17:03.000", "native-a", "command_exit", "outcome=provider_pending"),
        ]) + "\n"
        report = build_report_from_text(text, source_name="cohort.log")
        timeline = build_run_cohort_timeline(report, text, source_name="cohort.log")
        statuses = [item["status"] for item in timeline["runs"][0]["intervals"]]
        self.assertIn("contradictory", statuses)

    def test_closed_fixture_validates_and_is_defensively_copied(self):
        fixture = fixture_timeline()
        validated = validate_run_cohort_timeline(fixture)
        self.assertEqual(fixture, validated)
        validated["runs"][0]["api_run_id"] = "mutated"
        self.assertEqual("api-run-a", fixture["runs"][0]["api_run_id"])

    def test_schema_is_packaged_and_closed(self):
        schema = read_run_cohort_timeline_schema()
        self.assertEqual("astrowoof.sbe_run_cohort_timeline.v1", schema["properties"]["schema_version"]["const"])
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["interval"]["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(schema).validate(fixture_timeline())

    def test_unknown_version_extra_key_and_evidence_family_are_refused(self):
        for mutate in (
            lambda value: value.__setitem__("schema_version", "astrowoof.sbe_run_cohort_timeline.v2"),
            lambda value: value.__setitem__("extra", True),
            lambda value: value["runs"][0]["intervals"][0].__setitem__(
                "evidence_families", ["unowned"]
            ),
        ):
            changed = copy.deepcopy(fixture_timeline())
            mutate(changed)
            body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
            changed["timeline_sha256"] = _digest(body)
            with self.assertRaises(ValueError):
                validate_run_cohort_timeline(changed)

    def test_clock_disagreement_cannot_be_labeled_exact(self):
        changed = copy.deepcopy(fixture_timeline())
        boundary = changed["runs"][0]["intervals"][0]["start"]
        boundary["outer_timestamp"] = "2026-09-06T18:15:10.000Z"
        boundary_body = {key: value for key, value in boundary.items() if key != "boundary_id"}
        boundary["boundary_id"] = _digest(boundary_body)
        interval = changed["runs"][0]["intervals"][0]
        interval["constituent_boundary_ids"] = sorted([
            interval["start"]["boundary_id"], interval["end"]["boundary_id"],
        ])
        interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
        interval["interval_id"] = _digest(interval_body)
        changed["observed_handoffs"] = []
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "clock relation"):
            validate_run_cohort_timeline(changed)

    def test_evidence_family_cannot_select_the_other_familys_clock(self):
        changed = copy.deepcopy(fixture_timeline())
        boundary = changed["runs"][0]["intervals"][0]["start"]
        boundary["canonical_timestamp_field"] = "message.timestamp"
        boundary_body = {key: value for key, value in boundary.items() if key != "boundary_id"}
        boundary["boundary_id"] = _digest(boundary_body)
        interval = changed["runs"][0]["intervals"][0]
        interval["constituent_boundary_ids"] = sorted([
            interval["start"]["boundary_id"], interval["end"]["boundary_id"],
        ])
        interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
        interval["interval_id"] = _digest(interval_body)
        changed["observed_handoffs"] = []
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "contradicts evidence family"):
            validate_run_cohort_timeline(changed)

    def test_handoffs_are_ordered_by_witnessed_time_not_digest(self):
        changed = copy.deepcopy(fixture_timeline())
        start = _boundary(
            "2026-09-06T18:17:00.000Z", "sbe.cycle.started", line=5,
            api_run_id="api-run-c", native_run_id="native-run-c",
            attempt_id="attempt-c", lease_id="lease-c",
        )
        end = _boundary(
            "2026-09-06T18:18:00.000Z", "sbe.cycle.completed", line=6,
            api_run_id="api-run-c", native_run_id="native-run-c",
            attempt_id="attempt-c", lease_id="lease-c",
        )
        interval = _interval("provider_reconciliation", "Provider reconciliation", start, end)
        changed["runs"].append({
            "api_run_id": "api-run-c",
            "native_run_id": "native-run-c",
            "first_timestamp": start["canonical_timestamp"],
            "last_timestamp": end["canonical_timestamp"],
            "intervals": [interval],
            "no_progress_candidate_ids": [],
            "final_observed_posture": {
                "classification": "in_progress",
                "not_authoritative_current_state": True,
                "boundary_ids": [end["boundary_id"]],
            },
        })
        second_interval = changed["runs"][1]["intervals"][0]
        later_body = {
            "kind": "observed_execution_handoff",
            "from_interval_id": second_interval["interval_id"],
            "to_interval_id": interval["interval_id"],
            "duration_ms": 23976,
            "witness_only_not_sla": True,
        }
        later = {"handoff_id": _digest(later_body), **later_body}
        changed["observed_handoffs"].append(later)
        changed["observed_handoffs"].reverse()
        changed["log_sources"][0]["line_count"] = 6
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "witnessed chronology"):
            validate_run_cohort_timeline(changed)

    def test_reader_validates_digest(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "timeline.json"
            path.write_text(json.dumps(fixture_timeline()), encoding="utf-8")
            self.assertEqual(fixture_timeline(), read_run_cohort_timeline(path))

    def test_mutated_boundary_timestamp_with_rehashed_outer_document_is_refused(self):
        changed = copy.deepcopy(fixture_timeline())
        changed["runs"][0]["intervals"][0]["start"]["canonical_timestamp"] = "2026-09-06T18:15:01.000Z"
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "identity"):
            validate_run_cohort_timeline(changed)

    def test_mismatched_run_join_is_refused_even_when_all_digests_are_recomputed(self):
        changed = copy.deepcopy(fixture_timeline())
        boundary = changed["runs"][0]["intervals"][0]["start"]
        boundary["correlation"]["api_run_id"] = "api-run-b"
        boundary_body = {key: value for key, value in boundary.items() if key != "boundary_id"}
        boundary["boundary_id"] = _digest(boundary_body)
        interval = changed["runs"][0]["intervals"][0]
        interval["constituent_boundary_ids"] = sorted([
            interval["start"]["boundary_id"], interval["end"]["boundary_id"],
        ])
        interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
        interval["interval_id"] = _digest(interval_body)
        changed["observed_handoffs"] = []
        changed["runs"][0]["final_observed_posture"]["boundary_ids"] = [
            interval["end"]["boundary_id"]
        ]
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "does not join run identity"):
            validate_run_cohort_timeline(changed)

    def test_lease_handoff_is_witness_not_sla(self):
        changed = copy.deepcopy(fixture_timeline())
        changed["observed_handoffs"][0]["witness_only_not_sla"] = False
        handoff = changed["observed_handoffs"][0]
        handoff_body = {key: value for key, value in handoff.items() if key != "handoff_id"}
        handoff["handoff_id"] = _digest(handoff_body)
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "handoff semantics"):
            validate_run_cohort_timeline(changed)

    def test_handoff_duration_is_derived_not_declared(self):
        changed = copy.deepcopy(fixture_timeline())
        changed["observed_handoffs"][0]["duration_ms"] = 102
        handoff = changed["observed_handoffs"][0]
        handoff_body = {key: value for key, value in handoff.items() if key != "handoff_id"}
        handoff["handoff_id"] = _digest(handoff_body)
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "handoff duration"):
            validate_run_cohort_timeline(changed)

    def test_wrapper_failure_cannot_be_relabeled_terminal_review(self):
        changed = copy.deepcopy(fixture_timeline())
        interval = changed["runs"][0]["intervals"][0]
        interval["classification"] = "terminal_review"
        interval["label"] = "Review required"
        interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
        interval["interval_id"] = _digest(interval_body)
        changed["runs"][0]["final_observed_posture"] = {
            "classification": "terminal_review",
            "not_authoritative_current_state": True,
            "boundary_ids": [interval["end"]["boundary_id"]],
        }
        changed["observed_handoffs"] = []
        body = {key: value for key, value in changed.items() if key != "timeline_sha256"}
        changed["timeline_sha256"] = _digest(body)
        with self.assertRaisesRegex(ValueError, "terminal review"):
            validate_run_cohort_timeline(changed)


if __name__ == "__main__":
    unittest.main()
