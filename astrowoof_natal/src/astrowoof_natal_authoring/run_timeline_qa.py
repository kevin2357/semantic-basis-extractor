"""Provider-free installed qualification for the shared-time cohort reporter."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .cli.run_report import main as report_main
from .run_timeline import read_run_cohort_timeline


SCHEMA_VERSION = "astrowoof.sbe_run_cohort_timeline_qualification.v1"
_SHA256 = __import__("re").compile(r"^[0-9a-f]{64}$")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _line(timestamp: str, run: str, event: str, fields: str) -> str:
    return (
        f"{timestamp}Z ✨🐶 {timestamp}Z | INFO | qa-host | {run} | "
        f"qa-invocation | main | WAITING_FOR_RESPONSE : {event} {fields}"
    )


def _wrapper(timestamp: str, event: str, run: str, native: str, **payload: Any) -> str:
    return json.dumps({
        "schema_version": "astrowoof.execution_event.v1",
        "envelope_type": "execution_event",
        "event_id": f"{event}-{run}-{timestamp}",
        "event_name": event,
        "observed_at": timestamp,
        "producer": {
            "service": "api-worker", "component": "qa-wrapper", "instance_id": "qa-worker-one",
        },
        "correlation": {
            "run_id": run, "native_run_id": native, "job_id": f"job-{run}",
            "attempt_id": f"attempt-{run}", "lease_id": f"lease-{run}",
            "invocation_id": None, "action_id": None,
        },
        "payload": payload,
    }, sort_keys=True)


def qualification_log() -> str:
    """Return a sanitized deterministic three-run cohort log."""
    a, b, c = "native-review", "native-delivered-a", "native-delivered-b"
    return "\n".join([
        _wrapper("2026-09-06T18:15:00.000Z", "worker.lease.acquired", "api-review", a),
        _wrapper("2026-09-06T18:15:00.010Z", "sbe.cycle.started", "api-review", a),
        _line("2026-09-06T18:15:00.020", a, "workspace_fingerprint", "revision=4 snapshot_sha256=" + "1" * 64),
        _line("2026-09-06T18:15:00.030", a, "lifecycle_inspection_complete", "status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=1 provider_actions=1 local_dependencies=0"),
        _line("2026-09-06T18:15:00.040", a, "command_exit", "command=provider_reconciliation_cycle exit_code=0 outcome=provider_pending"),
        _line("2026-09-06T18:15:00.050", a, "workspace_fingerprint", "revision=5 snapshot_sha256=" + "2" * 64),
        _line("2026-09-06T18:15:00.060", a, "lifecycle_inspection_complete", "status=WAITING_FOR_RESPONSE branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=1 provider_actions=1 local_dependencies=0"),
        _wrapper("2026-09-06T18:15:41.548Z", "sbe.cycle.completed", "api-review", a, execution_branch="provider_reconciliation"),
        _wrapper("2026-09-06T18:15:41.549Z", "worker.lease.released", "api-review", a),
        _line("2026-09-06T18:15:41.600", a, "native_publication_complete", "outcome=review_required terminal_outcome=review_required"),
        _wrapper("2026-09-06T18:15:41.650Z", "worker.lease.acquired", "api-delivered-a", b),
        _wrapper("2026-09-06T18:15:41.650Z", "sbe.cycle.started", "api-delivered-a", b),
        _wrapper("2026-09-06T18:16:00.000Z", "sbe.cycle.completed", "api-delivered-a", b, execution_branch="initial_wave"),
        _wrapper("2026-09-06T18:16:00.001Z", "reading.publication.completed", "api-delivered-a", b),
        _wrapper("2026-09-06T18:16:00.002Z", "worker.lease.released", "api-delivered-a", b),
        _wrapper("2026-09-06T18:16:00.100Z", "worker.lease.acquired", "api-delivered-b", c),
        _wrapper("2026-09-06T18:16:00.101Z", "sbe.cycle.started", "api-delivered-b", c),
        _wrapper("2026-09-06T18:16:10.000Z", "sbe.cycle.completed", "api-delivered-b", c, execution_branch="delivery_validation"),
        _wrapper("2026-09-06T18:16:10.001Z", "reading.publication.completed", "api-delivered-b", c),
        _wrapper("2026-09-06T18:16:10.002Z", "worker.lease.released", "api-delivered-b", c),
        # An unmatched start proves partial exports remain explicitly open.
        _wrapper("2026-09-06T18:16:11.000Z", "worker.job.started", "api-delivered-b", c),
    ]) + "\n"


def read_run_timeline_qualification_schema() -> dict[str, Any]:
    from importlib.resources import files

    return json.loads(files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "sbe-run-cohort-timeline-qualification.v1.schema.json"
    ).read_text(encoding="utf-8"))


def validate_run_timeline_qualification(value: Any) -> dict[str, Any]:
    expected = {
        "schema_version", "receipt_sha256", "timeline_sha256", "html_sha256",
        "run_count", "final_postures", "witnessed_handoff_duration_ms",
        "open_interval_count", "no_progress_candidate_count", "provider_call_count",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError("Timeline qualification receipt shape is invalid")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value["schema_version"] != SCHEMA_VERSION or value["receipt_sha256"] != _digest(body):
        raise ValueError("Timeline qualification receipt identity is invalid")
    for key in ("timeline_sha256", "html_sha256"):
        if not isinstance(value[key], str) or _SHA256.fullmatch(value[key]) is None:
            raise ValueError("Timeline qualification digest is invalid")
    if value["run_count"] != 3 or value["final_postures"] != {
        "delivered": 2, "terminal_review": 1,
    }:
        raise ValueError("Timeline qualification cohort outcome is invalid")
    if (
        value["witnessed_handoff_duration_ms"] != 102
        or value["open_interval_count"] < 1
        or value["no_progress_candidate_count"] < 1
        or value["provider_call_count"] != 0
    ):
        raise ValueError("Timeline qualification safety evidence is invalid")
    return dict(value)


def _qualify_in(root: Path) -> dict[str, Any]:
    source = root / "cohort.log"
    output = root / "report"
    root.mkdir(parents=True, exist_ok=True)
    source.write_text(qualification_log(), encoding="utf-8")
    if report_main(["timeline", "--input", str(source), "--output-dir", str(output)]) != 0:
        raise ValueError("Timeline public CLI qualification failed")
    timeline = read_run_cohort_timeline(output / "report.timeline.json")
    html = (output / "report.timeline.html").read_bytes()
    postures: dict[str, int] = {}
    for run in timeline["runs"]:
        name = run["final_observed_posture"]["classification"]
        postures[name] = postures.get(name, 0) + 1
    handoff_durations = [item["duration_ms"] for item in timeline["observed_handoffs"]]
    body = {
        "schema_version": SCHEMA_VERSION,
        "timeline_sha256": timeline["timeline_sha256"],
        "html_sha256": hashlib.sha256(html).hexdigest(),
        "run_count": len(timeline["runs"]),
        "final_postures": postures,
        "witnessed_handoff_duration_ms": handoff_durations[0],
        "open_interval_count": sum(
            item["status"] == "open" for run in timeline["runs"] for item in run["intervals"]
        ),
        "no_progress_candidate_count": sum(
            len(run["no_progress_candidate_ids"]) for run in timeline["runs"]
        ),
        "provider_call_count": 0,
    }
    receipt = validate_run_timeline_qualification({"receipt_sha256": _digest(body), **body})
    (root / "qualification.receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    return receipt


def run_run_timeline_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary:
        return _qualify_in(Path(temporary))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--artifacts-dir", type=Path)
    args = parser.parse_args(argv)
    receipt = (
        _qualify_in(args.artifacts_dir)
        if args.artifacts_dir is not None
        else run_run_timeline_qualification()
    )
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


__all__ = [
    "SCHEMA_VERSION", "qualification_log", "read_run_timeline_qualification_schema",
    "run_run_timeline_qualification", "validate_run_timeline_qualification",
]


if __name__ == "__main__":
    raise SystemExit(main())
