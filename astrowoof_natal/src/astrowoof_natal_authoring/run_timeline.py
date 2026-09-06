"""Closed diagnostic contract for shared-time run cohort projections."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SCHEMA_VERSION = "astrowoof.sbe_run_cohort_timeline.v1"
CANONICAL_TIMEZONE = "UTC"

INTERVAL_CLASSIFICATIONS = frozenset({
    "deterministic_work",
    "initial_provider_wave",
    "provider_reconciliation",
    "external_authority_v2",
    "local_native_work",
    "delivery_validation",
    "observed_execution_allocation",
    "api_deferred_or_queued",
    "provider_wait",
    "terminal_review",
    "delivered",
    "failure_or_refusal",
    "unknown",
})
INTERVAL_STATUSES = frozenset({"complete", "open", "contradictory"})
EVIDENCE_FAMILIES = frozenset({"native_sbe", "api_worker_wrapper"})
CLOCK_RELATIONS = frozenset({
    "exact", "within_tolerance", "disagrees", "outer_unavailable",
})
CANONICAL_TIMESTAMP_FIELDS = frozenset({
    "message.timestamp", "message.observed_at",
})
FINAL_POSTURES = frozenset({
    "delivered", "terminal_review", "failure_or_refusal", "in_progress", "unknown",
})
HANDOFF_KINDS = frozenset({"observed_execution_handoff"})

_SHA256 = __import__("re").compile(r"^[0-9a-f]{64}$")


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError(f"{label} shape is invalid")
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase SHA-256")
    return value


def _text(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be nonempty text")
    return value


def _timestamp(value: Any, label: str, *, nullable: bool = False) -> str | None:
    checked = _text(value, label, nullable=nullable)
    if checked is None:
        return None
    if not checked.endswith("Z"):
        raise ValueError(f"{label} must be canonical UTC with Z suffix")
    try:
        datetime.fromisoformat(checked[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} is not an ISO-8601 timestamp") from error
    return checked


def _instant(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _validate_boundary(value: Any, *, sources: set[str], label: str) -> Mapping[str, Any]:
    boundary = _keys(value, {
        "boundary_id", "canonical_timestamp", "canonical_timestamp_field",
        "outer_timestamp", "clock_relation", "source_sha256", "source_line",
        "raw_line_sha256", "event_name", "evidence_family", "producer",
        "correlation",
    }, label)
    body = {key: item for key, item in boundary.items() if key != "boundary_id"}
    if boundary["boundary_id"] != _digest(body):
        raise ValueError(f"{label} identity is invalid")
    _timestamp(boundary["canonical_timestamp"], f"{label}.canonical_timestamp")
    if boundary["canonical_timestamp_field"] not in CANONICAL_TIMESTAMP_FIELDS:
        raise ValueError(f"{label} canonical timestamp field is unsupported")
    _timestamp(boundary["outer_timestamp"], f"{label}.outer_timestamp", nullable=True)
    if boundary["clock_relation"] not in CLOCK_RELATIONS:
        raise ValueError(f"{label} clock relation is unsupported")
    outer = boundary["outer_timestamp"]
    relation = boundary["clock_relation"]
    if outer is None:
        if relation != "outer_unavailable":
            raise ValueError(f"{label} clock relation contradicts missing outer timestamp")
    else:
        delta_ms = abs(round((_instant(outer) - _instant(boundary["canonical_timestamp"])).total_seconds() * 1000))
        if (
            (relation == "exact" and delta_ms != 0)
            or (relation == "within_tolerance" and not 0 < delta_ms <= 5000)
            or (relation == "disagrees" and delta_ms <= 5000)
            or relation == "outer_unavailable"
        ):
            raise ValueError(f"{label} clock relation is inconsistent")
    source_sha = _sha(boundary["source_sha256"], f"{label}.source_sha256")
    if source_sha not in sources:
        raise ValueError(f"{label} does not join a declared source")
    if not isinstance(boundary["source_line"], int) or boundary["source_line"] < 1:
        raise ValueError(f"{label} source line is invalid")
    _sha(boundary["raw_line_sha256"], f"{label}.raw_line_sha256")
    _text(boundary["event_name"], f"{label}.event_name")
    if boundary["evidence_family"] not in EVIDENCE_FAMILIES:
        raise ValueError(f"{label} evidence family is unsupported")
    required_clock_field = {
        "native_sbe": "message.timestamp",
        "api_worker_wrapper": "message.observed_at",
    }[boundary["evidence_family"]]
    if boundary["canonical_timestamp_field"] != required_clock_field:
        raise ValueError(f"{label} canonical timestamp field contradicts evidence family")
    producer = _keys(
        boundary["producer"], {"service", "component", "instance_id"}, f"{label}.producer",
    )
    _text(producer["service"], f"{label}.producer.service")
    _text(producer["component"], f"{label}.producer.component", nullable=True)
    _text(producer["instance_id"], f"{label}.producer.instance_id", nullable=True)
    correlation = _keys(boundary["correlation"], {
        "api_run_id", "native_run_id", "job_id", "attempt_id", "lease_id",
        "invocation_id", "action_id", "event_id",
    }, f"{label}.correlation")
    for key, item in correlation.items():
        _text(item, f"{label}.correlation.{key}", nullable=True)
    return boundary


def read_run_cohort_timeline_schema() -> dict[str, Any]:
    """Read the packaged structural schema for cohort timeline projections."""
    from importlib.resources import files

    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "sbe-run-cohort-timeline.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def read_run_cohort_timeline(path: Path) -> dict[str, Any]:
    """Read and validate one local diagnostic cohort timeline."""
    return validate_run_cohort_timeline(json.loads(path.read_text(encoding="utf-8")))


def validate_run_cohort_timeline(value: Any) -> dict[str, Any]:
    """Validate the closed shape, joins, ordering, identities, and digest."""
    timeline = _keys(value, {
        "schema_version", "timeline_sha256", "diagnostic_only",
        "canonical_timezone", "source_reports", "log_sources", "adapter_coverage", "runs",
        "observed_handoffs",
    }, "Cohort timeline")
    body = {key: item for key, item in timeline.items() if key != "timeline_sha256"}
    if (
        timeline["schema_version"] != SCHEMA_VERSION
        or timeline["diagnostic_only"] is not True
        or timeline["canonical_timezone"] != CANONICAL_TIMEZONE
        or timeline["timeline_sha256"] != _digest(body)
    ):
        raise ValueError("Cohort timeline semantics are invalid")

    if not isinstance(timeline["log_sources"], list) or not timeline["log_sources"]:
        raise ValueError("Cohort timeline must declare at least one log source")
    source_ids: set[str] = set()
    for index, item in enumerate(timeline["log_sources"]):
        source = _keys(item, {"name", "sha256", "line_count"}, f"Log source {index}")
        _text(source["name"], f"Log source {index}.name")
        source_sha = _sha(source["sha256"], f"Log source {index}.sha256")
        if source_sha in source_ids:
            raise ValueError("Log source identities must be unique")
        source_ids.add(source_sha)
        if not isinstance(source["line_count"], int) or source["line_count"] < 0:
            raise ValueError("Log source line count is invalid")

    if not isinstance(timeline["source_reports"], list) or not timeline["source_reports"]:
        raise ValueError("Cohort timeline must bind at least one validated run report")
    report_ids: set[str] = set()
    for index, item in enumerate(timeline["source_reports"]):
        report = _keys(item, {
            "report_sha256", "source_sha256", "trace_sha256", "parser_version",
        }, f"Source report {index}")
        report_sha = _sha(report["report_sha256"], f"Source report {index}.report_sha256")
        if report_sha in report_ids:
            raise ValueError("Source report identities must be unique")
        report_ids.add(report_sha)
        if _sha(report["source_sha256"], f"Source report {index}.source_sha256") not in source_ids:
            raise ValueError("Source report does not join a declared log source")
        _sha(report["trace_sha256"], f"Source report {index}.trace_sha256")
        _text(report["parser_version"], f"Source report {index}.parser_version")

    coverage = _keys(timeline["adapter_coverage"], {
        "wrapper_candidate_count", "accepted_wrapper_event_count",
        "refused_wrapper_line_numbers", "refused_wrapper_overflow",
        "unsupported_wrapper_events",
    }, "Adapter coverage")
    for key in ("wrapper_candidate_count", "accepted_wrapper_event_count", "refused_wrapper_overflow"):
        if not isinstance(coverage[key], int) or coverage[key] < 0:
            raise ValueError("Adapter coverage count is invalid")
    refused = coverage["refused_wrapper_line_numbers"]
    if (
        not isinstance(refused, list) or refused != sorted(set(refused))
        or any(not isinstance(line, int) or line < 1 for line in refused)
        or coverage["accepted_wrapper_event_count"] > coverage["wrapper_candidate_count"]
    ):
        raise ValueError("Adapter refused-line coverage is invalid")
    unsupported = coverage["unsupported_wrapper_events"]
    if not isinstance(unsupported, list):
        raise ValueError("Unsupported wrapper-event coverage is invalid")
    prior_name: str | None = None
    for index, item in enumerate(unsupported):
        entry = _keys(item, {"event_name", "count"}, f"Unsupported wrapper event {index}")
        name = _text(entry["event_name"], f"Unsupported wrapper event {index}.event_name")
        if prior_name is not None and name <= prior_name:
            raise ValueError("Unsupported wrapper events must be uniquely sorted")
        prior_name = name
        if not isinstance(entry["count"], int) or entry["count"] < 1:
            raise ValueError("Unsupported wrapper event count is invalid")

    if not isinstance(timeline["runs"], list) or not timeline["runs"]:
        raise ValueError("Cohort timeline must contain at least one run")
    prior_run_key: tuple[str, str] | None = None
    interval_ids: set[str] = set()
    interval_bounds: dict[str, tuple[str, str | None]] = {}
    run_ids: set[tuple[str, str]] = set()
    for run_index, item in enumerate(timeline["runs"]):
        run = _keys(item, {
            "api_run_id", "native_run_id", "first_timestamp", "last_timestamp",
            "intervals", "no_progress_candidate_ids", "final_observed_posture",
        }, f"Run {run_index}")
        api_run_id = _text(run["api_run_id"], f"Run {run_index}.api_run_id", nullable=True)
        native_run_id = _text(run["native_run_id"], f"Run {run_index}.native_run_id")
        key = (api_run_id or "", native_run_id or "")
        if key in run_ids or (prior_run_key is not None and key <= prior_run_key):
            raise ValueError("Cohort runs must be uniquely sorted by API/native identity")
        run_ids.add(key)
        prior_run_key = key
        first = _timestamp(run["first_timestamp"], f"Run {run_index}.first_timestamp")
        last = _timestamp(run["last_timestamp"], f"Run {run_index}.last_timestamp")
        if first > last:
            raise ValueError("Run time bounds are reversed")
        if not isinstance(run["no_progress_candidate_ids"], list) or any(
            not isinstance(value, str) or not value for value in run["no_progress_candidate_ids"]
        ) or run["no_progress_candidate_ids"] != sorted(set(run["no_progress_candidate_ids"])):
            raise ValueError("No-progress candidate identities must be unique and sorted")
        posture = _keys(run["final_observed_posture"], {
            "classification", "not_authoritative_current_state", "boundary_ids",
        }, f"Run {run_index}.final_observed_posture")
        if (
            posture["classification"] not in FINAL_POSTURES
            or posture["not_authoritative_current_state"] is not True
            or not isinstance(posture["boundary_ids"], list)
            or posture["boundary_ids"] != sorted(set(posture["boundary_ids"]))
        ):
            raise ValueError("Final observed posture is invalid")

        if not isinstance(run["intervals"], list):
            raise ValueError("Run intervals are invalid")
        prior_interval_key: tuple[str, str] | None = None
        run_boundary_ids: set[str] = set()
        for interval_index, raw_interval in enumerate(run["intervals"]):
            label = f"Run {run_index} interval {interval_index}"
            interval = _keys(raw_interval, {
                "interval_id", "classification", "status", "label", "start",
                "end", "duration_ms", "evidence_families", "constituent_boundary_ids",
                "no_progress_candidate_ids",
            }, label)
            interval_body = {key: value for key, value in interval.items() if key != "interval_id"}
            if interval["interval_id"] != _digest(interval_body):
                raise ValueError(f"{label} identity is invalid")
            if interval["interval_id"] in interval_ids:
                raise ValueError("Interval identities must be globally unique")
            interval_ids.add(interval["interval_id"])
            if interval["classification"] not in INTERVAL_CLASSIFICATIONS:
                raise ValueError(f"{label} classification is unsupported")
            if interval["status"] not in INTERVAL_STATUSES:
                raise ValueError(f"{label} status is unsupported")
            _text(interval["label"], f"{label}.label")
            start = _validate_boundary(interval["start"], sources=source_ids, label=f"{label}.start")
            for key_name, expected in (("api_run_id", api_run_id), ("native_run_id", native_run_id)):
                observed = start["correlation"][key_name]
                if observed is not None and observed != expected:
                    raise ValueError(f"{label} start boundary does not join run identity")
            end_boundary = interval["end"]
            if end_boundary is None:
                if interval["status"] != "open" or interval["duration_ms"] is not None:
                    raise ValueError("Only open intervals may omit end and duration")
                end_timestamp = None
            else:
                end_checked = _validate_boundary(end_boundary, sources=source_ids, label=f"{label}.end")
                for key_name, expected in (("api_run_id", api_run_id), ("native_run_id", native_run_id)):
                    observed = end_checked["correlation"][key_name]
                    if observed is not None and observed != expected:
                        raise ValueError(f"{label} end boundary does not join run identity")
                end_timestamp = end_checked["canonical_timestamp"]
                if interval["status"] == "open":
                    raise ValueError("Open interval cannot contain an end boundary")
                expected_duration = round((
                    _instant(end_timestamp) - _instant(start["canonical_timestamp"])
                ).total_seconds() * 1000)
                if interval["status"] == "contradictory":
                    if expected_duration >= 0 or interval["duration_ms"] != abs(expected_duration):
                        raise ValueError(f"{label} contradictory duration is invalid")
                elif expected_duration < 0 or interval["duration_ms"] != expected_duration:
                    raise ValueError(f"{label} duration is invalid")
            families = interval["evidence_families"]
            if (
                not isinstance(families, list) or not families
                or families != sorted(set(families))
                or any(family not in EVIDENCE_FAMILIES for family in families)
                or start["evidence_family"] not in families
                or (end_boundary is not None and end_boundary["evidence_family"] not in families)
            ):
                raise ValueError(f"{label} evidence families are invalid")
            if interval["classification"] == "terminal_review" and "native_sbe" not in families:
                raise ValueError("API wrapper evidence alone cannot establish terminal review")
            boundary_ids = interval["constituent_boundary_ids"]
            direct_ids = [start["boundary_id"]] + ([] if end_boundary is None else [end_boundary["boundary_id"]])
            if not isinstance(boundary_ids, list) or boundary_ids != sorted(set(direct_ids)):
                raise ValueError(f"{label} constituent boundaries are invalid")
            run_boundary_ids.update(boundary_ids)
            candidate_ids = interval["no_progress_candidate_ids"]
            if (
                not isinstance(candidate_ids, list)
                or candidate_ids != sorted(set(candidate_ids))
                or any(candidate not in run["no_progress_candidate_ids"] for candidate in candidate_ids)
            ):
                raise ValueError(f"{label} no-progress joins are invalid")
            interval_key = (start["canonical_timestamp"], interval["interval_id"])
            if prior_interval_key is not None and interval_key <= prior_interval_key:
                raise ValueError("Run intervals must be sorted by start time and identity")
            prior_interval_key = interval_key
            interval_bounds[interval["interval_id"]] = (start["canonical_timestamp"], end_timestamp)
            if start["canonical_timestamp"] < first or (
                end_timestamp is not None and end_timestamp > last
            ):
                raise ValueError("Interval lies outside declared run bounds")
        if any(boundary_id not in run_boundary_ids for boundary_id in posture["boundary_ids"]):
            raise ValueError(f"Run {run_index} final posture boundary does not join its interval inventory")

    if not isinstance(timeline["observed_handoffs"], list):
        raise ValueError("Observed handoffs are invalid")
    prior_handoff_key: tuple[str, str, str] | None = None
    for index, raw_handoff in enumerate(timeline["observed_handoffs"]):
        handoff = _keys(raw_handoff, {
            "handoff_id", "kind", "from_interval_id", "to_interval_id",
            "duration_ms", "witness_only_not_sla",
        }, f"Observed handoff {index}")
        handoff_body = {key: item for key, item in handoff.items() if key != "handoff_id"}
        if handoff["handoff_id"] != _digest(handoff_body):
            raise ValueError("Observed handoff identity is invalid")
        if (
            handoff["kind"] not in HANDOFF_KINDS
            or handoff["from_interval_id"] not in interval_ids
            or handoff["to_interval_id"] not in interval_ids
            or handoff["from_interval_id"] == handoff["to_interval_id"]
            or not isinstance(handoff["duration_ms"], int)
            or handoff["duration_ms"] < 0
            or handoff["witness_only_not_sla"] is not True
        ):
            raise ValueError("Observed handoff semantics are invalid")
        from_end = interval_bounds[handoff["from_interval_id"]][1]
        to_start = interval_bounds[handoff["to_interval_id"]][0]
        if from_end is None:
            raise ValueError("Observed handoff cannot originate from an open interval")
        expected_handoff = round((_instant(to_start) - _instant(from_end)).total_seconds() * 1000)
        if expected_handoff < 0 or handoff["duration_ms"] != expected_handoff:
            raise ValueError("Observed handoff duration is invalid")
        handoff_key = (from_end, to_start, handoff["handoff_id"])
        if prior_handoff_key is not None and handoff_key <= prior_handoff_key:
            raise ValueError("Observed handoffs must be sorted by witnessed chronology and identity")
        prior_handoff_key = handoff_key
    return deepcopy(dict(timeline))


API_WRAPPER_EVENTS = frozenset({
    "worker.job.claimed", "worker.job.started", "worker.job.completed",
    "worker.job.failed", "worker.job.deferred", "worker.lease.acquired",
    "worker.lease.released", "worker.successor.enqueued", "sbe.cycle.started",
    "sbe.cycle.completed", "sbe.closeout.completed",
    "reading.publication.completed",
})


def _normalize_utc(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip()
    if candidate.endswith("Z"):
        iso = candidate[:-1] + "+00:00"
    else:
        iso = candidate
    try:
        parsed = datetime.fromisoformat(iso)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _clock_relation(canonical: str, outer: str | None) -> str:
    if outer is None:
        return "outer_unavailable"
    difference = abs(round((_instant(outer) - _instant(canonical)).total_seconds() * 1000))
    if difference == 0:
        return "exact"
    return "within_tolerance" if difference <= 5000 else "disagrees"


def _make_boundary(event: Mapping[str, Any], *, source_sha256: str) -> dict[str, Any]:
    family = event["evidence_family"]
    canonical = event["canonical_timestamp"]
    outer = event.get("outer_timestamp")
    body = {
        "canonical_timestamp": canonical,
        "canonical_timestamp_field": (
            "message.timestamp" if family == "native_sbe" else "message.observed_at"
        ),
        "outer_timestamp": outer,
        "clock_relation": _clock_relation(canonical, outer),
        "source_sha256": source_sha256,
        "source_line": event["source_line"],
        "raw_line_sha256": event["raw_line_sha256"],
        "event_name": event["event_name"],
        "evidence_family": family,
        "producer": deepcopy(event["producer"]),
        "correlation": deepcopy(event["correlation"]),
    }
    return {"boundary_id": _digest(body), **body}


def _make_interval(
    classification: str,
    label: str,
    start: Mapping[str, Any],
    end: Mapping[str, Any] | None,
    *,
    status: str = "complete",
    no_progress_candidate_ids: list[str] | None = None,
) -> dict[str, Any]:
    duration = None if end is None else round((
        _instant(end["canonical_timestamp"]) - _instant(start["canonical_timestamp"])
    ).total_seconds() * 1000)
    if duration is not None and duration < 0:
        status = "contradictory"
        duration = abs(duration)
    direct = [start["boundary_id"]] + ([] if end is None else [end["boundary_id"]])
    body = {
        "classification": classification,
        "status": status,
        "label": label,
        "start": deepcopy(dict(start)),
        "end": None if end is None else deepcopy(dict(end)),
        "duration_ms": duration,
        "evidence_families": sorted({
            start["evidence_family"],
            *([] if end is None else [end["evidence_family"]]),
        }),
        "constituent_boundary_ids": sorted(set(direct)),
        "no_progress_candidate_ids": sorted(set(no_progress_candidate_ids or [])),
    }
    return {"interval_id": _digest(body), **body}


def _wrapper_events(text: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    accepted: list[dict[str, Any]] = []
    refused: list[int] = []
    unsupported: dict[str, int] = {}
    candidates = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        start = line.find("{")
        if start < 0:
            continue
        try:
            outer_record = json.loads(line[start:])
        except json.JSONDecodeError:
            continue
        record = outer_record
        outer_value = _normalize_utc(line[:start].strip())
        if (
            isinstance(outer_record, Mapping)
            and isinstance(outer_record.get("message"), Mapping)
            and outer_record["message"].get("schema_version") == "astrowoof.execution_event.v1"
        ):
            record = outer_record["message"]
            outer_value = _normalize_utc(outer_record.get("dt")) or outer_value
        if not isinstance(record, Mapping) or record.get("schema_version") != "astrowoof.execution_event.v1":
            continue
        candidates += 1
        event_name = record.get("event_name")
        if isinstance(event_name, str) and event_name not in API_WRAPPER_EVENTS:
            unsupported[event_name] = unsupported.get(event_name, 0) + 1
            continue
        try:
            if (
                record.get("envelope_type") != "execution_event"
                or not isinstance(event_name, str)
                or not isinstance(record.get("event_id"), str)
                or not isinstance(record.get("observed_at"), str)
                or not isinstance(record.get("payload"), Mapping)
                or not isinstance(record.get("producer"), Mapping)
                or not isinstance(record.get("correlation"), Mapping)
            ):
                raise ValueError("malformed wrapper event")
            canonical = _normalize_utc(record["observed_at"])
            if canonical is None:
                raise ValueError("invalid observed_at")
            correlation = record["correlation"]
            producer = record["producer"]
            api_run_id = correlation.get("run_id")
            native_run_id = correlation.get("native_run_id")
            if not isinstance(api_run_id, str) or not api_run_id:
                raise ValueError("missing run correlation")
            if native_run_id is not None and (
                not isinstance(native_run_id, str) or not native_run_id
            ):
                raise ValueError("invalid native run correlation")
            accepted.append({
                "source_line": line_number,
                "raw_line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                "canonical_timestamp": canonical,
                "outer_timestamp": outer_value,
                "event_name": event_name,
                "evidence_family": "api_worker_wrapper",
                "producer": {
                    "service": str(producer.get("service") or "sbe-worker"),
                    "component": producer.get("component") if isinstance(producer.get("component"), str) else None,
                    "instance_id": producer.get("instance_id") if isinstance(producer.get("instance_id"), str) else None,
                },
                "correlation": {
                    "api_run_id": api_run_id,
                    "native_run_id": native_run_id,
                    "job_id": correlation.get("job_id") if isinstance(correlation.get("job_id"), str) else None,
                    "attempt_id": correlation.get("attempt_id") if isinstance(correlation.get("attempt_id"), str) else None,
                    "lease_id": correlation.get("lease_id") if isinstance(correlation.get("lease_id"), str) else None,
                    "invocation_id": correlation.get("invocation_id") if isinstance(correlation.get("invocation_id"), str) else None,
                    "action_id": correlation.get("action_id") if isinstance(correlation.get("action_id"), str) else None,
                    "event_id": record["event_id"],
                },
                "payload": deepcopy(dict(record["payload"])),
            })
        except (TypeError, ValueError):
            refused.append(line_number)
    # Pair in witnessed source order so an end-before-start clock contradiction
    # cannot be normalized away by sorting on the contradictory clock itself.
    accepted.sort(key=lambda item: item["source_line"])
    return accepted, {
        "wrapper_candidate_count": candidates,
        "accepted_wrapper_event_count": len(accepted),
        "refused_wrapper_line_numbers": sorted(set(refused))[:128],
        "refused_wrapper_overflow": max(0, len(set(refused)) - 128),
        "unsupported_wrapper_events": [
            {"event_name": name, "count": count} for name, count in sorted(unsupported.items())
        ],
    }


def _native_events(text: str, *, source_name: str) -> tuple[list[dict[str, Any]], Mapping[str, Any]]:
    from .run_report import parse_trace_text

    trace = parse_trace_text(text, source_name=source_name)
    events = []
    for item in trace["events"]:
        outer = _normalize_utc(item.get("outer_timestamp"))
        events.append({
            "source_line": item["source_line"],
            "raw_line_sha256": item["raw_sha256"],
            "canonical_timestamp": _normalize_utc(item["timestamp"]),
            "outer_timestamp": outer,
            "event_name": item["event"],
            "evidence_family": "native_sbe",
            "producer": {
                "service": "sbe-worker",
                "component": item.get("function") if item.get("function") != "-" else None,
                "instance_id": item.get("host_id") if item.get("host_id") != "-" else None,
            },
            "correlation": {
                "api_run_id": None,
                "native_run_id": item["run_id"] if item["run_id"] != "-" else None,
                "job_id": None,
                "attempt_id": None,
                "lease_id": None,
                "invocation_id": item["context_id"] if item["context_id"] != "-" else None,
                "action_id": item["fields"].get("action_id") if isinstance(item["fields"].get("action_id"), str) else None,
                "event_id": item["event_id"],
            },
            "payload": deepcopy(item["fields"]),
        })
    return events, trace


def build_run_cohort_timeline(
    report: Mapping[str, Any], text: str, *, source_name: str = "worker.log",
) -> dict[str, Any]:
    """Build a closed cohort timeline from one validated report and its exact log."""
    from .run_report import validate_run_evolution_report

    validated_report = validate_run_evolution_report(report)
    source_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if validated_report["source"]["sha256"] != source_sha:
        raise ValueError("Cohort source bytes do not match the bound run report")
    native_events, trace = _native_events(text, source_name=source_name)
    if trace["trace_sha256"] != validated_report["trace_sha256"]:
        raise ValueError("Cohort normalized trace does not match the bound run report")
    wrapper_events, coverage = _wrapper_events(text)

    api_by_native: dict[str, str] = {}
    native_by_api: dict[str, str] = {}
    for event in wrapper_events:
        correlation = event["correlation"]
        native_run_id = correlation["native_run_id"]
        if native_run_id is None:
            continue
        previous = api_by_native.setdefault(native_run_id, correlation["api_run_id"])
        if previous != correlation["api_run_id"]:
            raise ValueError("Wrapper events contradict API/native run identity")
        previous_native = native_by_api.setdefault(correlation["api_run_id"], native_run_id)
        if previous_native != native_run_id:
            raise ValueError("Wrapper events contradict API/native run identity")

    # API wrapper starts are emitted before the native workspace identity is
    # known, while their matching completion/release events carry both IDs.
    # Enrich only from an explicit, bijective API/native join elsewhere in the
    # accepted export; temporal proximity is never a join rule.
    enriched_wrapper_events: list[dict[str, Any]] = []
    unresolved_lines: list[int] = []
    for event in wrapper_events:
        correlation = event["correlation"]
        if correlation["native_run_id"] is None:
            native_run_id = native_by_api.get(correlation["api_run_id"])
            if native_run_id is None:
                unresolved_lines.append(event["source_line"])
                continue
            event = deepcopy(event)
            event["correlation"]["native_run_id"] = native_run_id
        enriched_wrapper_events.append(event)
    wrapper_events = enriched_wrapper_events
    refused_lines = sorted(set(
        coverage["refused_wrapper_line_numbers"] + unresolved_lines
    ))
    coverage["accepted_wrapper_event_count"] = len(wrapper_events)
    coverage["refused_wrapper_line_numbers"] = refused_lines[:128]
    coverage["refused_wrapper_overflow"] = max(0, len(refused_lines) - 128)

    report_runs = {run["run_id"]: run for run in validated_report["runs"]}
    intervals_by_run: dict[str, list[dict[str, Any]]] = {
        native_run_id: [] for native_run_id in sorted(set(report_runs) | set(api_by_native))
    }
    projected_wrapper_lines: set[int] = set()

    def wrapper_key(event: Mapping[str, Any], fields: tuple[str, ...]) -> tuple[Any, ...]:
        return tuple(event["correlation"].get(name) for name in fields)

    def pair(
        start_name: str,
        end_names: set[str],
        key_fields: tuple[str, ...],
        classification,
        label,
    ) -> list[dict[str, Any]]:
        pending: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
        made: list[dict[str, Any]] = []
        for event in wrapper_events:
            key = wrapper_key(event, key_fields)
            if event["event_name"] == start_name:
                pending.setdefault(key, []).append(event)
            elif event["event_name"] in end_names and pending.get(key):
                start_event = pending[key].pop(0)
                start_boundary = _make_boundary(start_event, source_sha256=source_sha)
                end_boundary = _make_boundary(event, source_sha256=source_sha)
                chosen = classification(event) if callable(classification) else classification
                chosen_label = label(event) if callable(label) else label
                interval = _make_interval(chosen, chosen_label, start_boundary, end_boundary)
                intervals_by_run[event["correlation"]["native_run_id"]].append(interval)
                projected_wrapper_lines.update((start_event["source_line"], event["source_line"]))
                made.append(interval)
        for values in pending.values():
            for event in values:
                boundary = _make_boundary(event, source_sha256=source_sha)
                chosen = classification(event) if callable(classification) else classification
                chosen_label = label(event) if callable(label) else label
                intervals_by_run[event["correlation"]["native_run_id"]].append(
                    _make_interval(chosen, chosen_label + " (open)", boundary, None, status="open")
                )
                projected_wrapper_lines.add(event["source_line"])
        return made

    pair(
        "worker.job.started", {"worker.job.completed", "worker.job.failed"},
        ("api_run_id", "job_id", "attempt_id", "lease_id"),
        "deterministic_work", "Deterministic work",
    )
    cycle_intervals = pair(
        "sbe.cycle.started", {"sbe.cycle.completed"},
        ("api_run_id", "job_id", "attempt_id", "lease_id"),
        lambda event: {
            "initial_wave": "initial_provider_wave",
            "provider_reconciliation": "provider_reconciliation",
            "external_authority_v2": "external_authority_v2",
            "delivery_validation": "delivery_validation",
        }.get(event["payload"].get("execution_branch"), "unknown"),
        lambda event: {
            "initial_wave": "Initial provider wave",
            "provider_reconciliation": "Provider reconciliation",
            "external_authority_v2": "v2 authority / dispatch",
            "delivery_validation": "Delivery validation",
        }.get(event["payload"].get("execution_branch"), "Unknown SBE cycle"),
    )
    pair(
        "worker.lease.acquired", {"worker.lease.released"},
        ("api_run_id", "job_id", "lease_id"),
        "observed_execution_allocation", "Observed execution-allocation / lease window",
    )
    pair(
        "worker.job.deferred", {"worker.job.claimed"},
        ("api_run_id", "job_id"),
        "api_deferred_or_queued", "API deferred / queued observation",
    )

    marker_intervals: dict[str, list[tuple[str, str, str]]] = {}
    for event in native_events:
        native_run_id = event["correlation"]["native_run_id"]
        if native_run_id not in intervals_by_run:
            continue
        values = " ".join(str(event["payload"].get(key, "")) for key in (
            "outcome", "cause", "terminal_outcome", "publication_status", "status",
        )).lower()
        if event["event_name"] in {"native_publication_complete", "native_publication_evidence_summary"} and (
            "review_required" in values or "review" in values
        ):
            boundary = _make_boundary(event, source_sha256=source_sha)
            interval = _make_interval("terminal_review", "Native terminal review", boundary, boundary)
            intervals_by_run[native_run_id].append(interval)
            marker_intervals.setdefault(native_run_id, []).append((
                boundary["canonical_timestamp"], "terminal_review", boundary["boundary_id"],
            ))
    for event in wrapper_events:
        native_run_id = event["correlation"]["native_run_id"]
        boundary = _make_boundary(event, source_sha256=source_sha)
        if event["event_name"] == "reading.publication.completed":
            interval = _make_interval("delivered", "Reading published", boundary, boundary)
            intervals_by_run[native_run_id].append(interval)
            marker_intervals.setdefault(native_run_id, []).append((
                boundary["canonical_timestamp"], "delivered", boundary["boundary_id"],
            ))
            projected_wrapper_lines.add(event["source_line"])
        elif event["event_name"] == "worker.job.failed":
            interval = _make_interval("failure_or_refusal", "API wrapper failure observation", boundary, boundary)
            intervals_by_run[native_run_id].append(interval)
            marker_intervals.setdefault(native_run_id, []).append((
                boundary["canonical_timestamp"], "failure_or_refusal", boundary["boundary_id"],
            ))
            projected_wrapper_lines.add(event["source_line"])

    # Approved wrapper evidence that cannot participate in a closed pair remains
    # visible as an unknown instantaneous boundary. It is never silently dropped
    # or promoted into native truth.
    for event in wrapper_events:
        if event["source_line"] in projected_wrapper_lines:
            continue
        boundary = _make_boundary(event, source_sha256=source_sha)
        intervals_by_run[event["correlation"]["native_run_id"]].append(
            _make_interval("unknown", f"Unpaired API event: {event['event_name']}", boundary, boundary)
        )

    runs = []
    for native_run_id, intervals in intervals_by_run.items():
        if not intervals:
            continue
        intervals.sort(key=lambda item: (item["start"]["canonical_timestamp"], item["interval_id"]))
        report_run = report_runs.get(native_run_id, {})
        candidate_ids = sorted(
            candidate["candidate_sha256"] for candidate in report_run.get("no_progress_candidates", [])
        )
        markers = marker_intervals.get(native_run_id, [])
        if markers:
            _, classification, marker_id = max(markers)
            posture_ids = [marker_id]
        else:
            classification = "in_progress"
            last = intervals[-1]
            posture_ids = [
                (last["end"] or last["start"])["boundary_id"]
            ]
        runs.append({
            "api_run_id": api_by_native.get(native_run_id),
            "native_run_id": native_run_id,
            "first_timestamp": min(
                boundary["canonical_timestamp"]
                for item in intervals
                for boundary in (item["start"], item["end"])
                if boundary is not None
            ),
            "last_timestamp": max(
                boundary["canonical_timestamp"]
                for item in intervals
                for boundary in (item["start"], item["end"])
                if boundary is not None
            ),
            "intervals": intervals,
            "no_progress_candidate_ids": candidate_ids,
            "final_observed_posture": {
                "classification": classification,
                "not_authoritative_current_state": True,
                "boundary_ids": posture_ids,
            },
        })
    runs.sort(key=lambda item: (item["api_run_id"] or "", item["native_run_id"]))

    cycle_intervals.sort(key=lambda item: (
        item["start"]["canonical_timestamp"], item["interval_id"],
    ))
    handoffs = []
    for previous, current in zip(cycle_intervals, cycle_intervals[1:]):
        previous_end = previous["end"]
        if previous_end is None:
            continue
        if previous["start"]["correlation"]["api_run_id"] == current["start"]["correlation"]["api_run_id"]:
            continue
        if previous_end["producer"]["instance_id"] != current["start"]["producer"]["instance_id"]:
            continue
        duration = round((
            _instant(current["start"]["canonical_timestamp"])
            - _instant(previous_end["canonical_timestamp"])
        ).total_seconds() * 1000)
        if duration < 0:
            continue
        handoff_body = {
            "kind": "observed_execution_handoff",
            "from_interval_id": previous["interval_id"],
            "to_interval_id": current["interval_id"],
            "duration_ms": duration,
            "witness_only_not_sla": True,
        }
        handoffs.append({"handoff_id": _digest(handoff_body), **handoff_body})
    handoffs.sort(key=lambda item: (
        next(interval["end"]["canonical_timestamp"] for interval in cycle_intervals if interval["interval_id"] == item["from_interval_id"]),
        next(interval["start"]["canonical_timestamp"] for interval in cycle_intervals if interval["interval_id"] == item["to_interval_id"]),
        item["handoff_id"],
    ))

    body = {
        "schema_version": SCHEMA_VERSION,
        "diagnostic_only": True,
        "canonical_timezone": CANONICAL_TIMEZONE,
        "source_reports": [{
            "report_sha256": validated_report["report_sha256"],
            "source_sha256": source_sha,
            "trace_sha256": validated_report["trace_sha256"],
            "parser_version": validated_report["parser_version"],
        }],
        "log_sources": [{
            "name": validated_report["source"]["name"],
            "sha256": source_sha,
            "line_count": validated_report["source"]["line_count"],
        }],
        "adapter_coverage": coverage,
        "runs": runs,
        "observed_handoffs": handoffs,
    }
    return validate_run_cohort_timeline({"timeline_sha256": _digest(body), **body})


def render_run_cohort_timeline_html(
    timeline: Mapping[str, Any], *, display_timezone: str = "UTC",
) -> str:
    """Render one validated cohort timeline as self-contained interactive HTML."""
    validated = validate_run_cohort_timeline(timeline)
    try:
        ZoneInfo(display_timezone)
    except ZoneInfoNotFoundError as error:
        raise ValueError("Display timezone is unknown") from error
    encoded = json.dumps(validated, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    encoded_timezone = json.dumps(display_timezone)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SBE cohort timeline</title>
<style>
:root{{--bg:#0c111b;--fg:#edf2f7;--muted:#9eacc0;--panel:#151d2b;--line:#304056;--work:#79b8ff;--provider:#b692f6;--wait:#ffd479;--good:#73d99f;--bad:#ff8585;--unknown:#8b98aa}}
@media(prefers-color-scheme:light){{:root{{--bg:#f7f9fc;--fg:#172033;--muted:#58677e;--panel:#fff;--line:#cad3df;--work:#185fa5;--provider:#6f42c1;--wait:#8a5b00;--good:#157347;--bad:#b42318;--unknown:#667085}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif}}main{{padding:16px;max-width:100%}}h1{{font-size:20px;margin:0 0 4px}}.subtitle,.summary,.axis-label{{color:var(--muted)}}.controls{{display:flex;flex-wrap:wrap;gap:12px;align-items:end;margin:14px 0}}label{{display:grid;gap:4px;color:var(--muted)}}select,button{{font:inherit;color:var(--fg);background:var(--panel);border:1px solid var(--line);padding:8px}}button{{cursor:pointer}}.timeline{{border-top:1px solid var(--line);min-width:0}}.axis,.lane{{display:grid;grid-template-columns:minmax(150px,220px) minmax(0,1fr);gap:10px;align-items:center}}.axis{{padding:10px 0 6px}}.axis-track{{position:relative;height:28px;border-bottom:1px solid var(--line)}}.tick{{position:absolute;bottom:-5px;transform:translateX(-50%);color:var(--muted);font-size:11px;white-space:nowrap}}.tick:before{{content:'';display:block;height:6px;border-left:1px solid var(--line);margin:auto}}.lane{{padding:7px 0;border-bottom:1px solid var(--line)}}.lane.dimmed{{opacity:.3}}.lane-name{{min-width:0}}.lane-name strong,.lane-name code{{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.lane-name small{{color:var(--muted)}}.track{{position:relative;height:46px;background:linear-gradient(to right,transparent 24.8%,var(--line) 25%,transparent 25.2%,transparent 49.8%,var(--line) 50%,transparent 50.2%,transparent 74.8%,var(--line) 75%,transparent 75.2%)}}.segment{{position:absolute;top:7px;height:32px;min-width:3px;border:0;border-left:2px solid var(--fg);padding:2px 5px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;text-align:left;color:var(--bg);font-size:12px}}.segment.work{{background:var(--work)}}.segment.provider{{background:var(--provider)}}.segment.wait{{background:var(--wait)}}.segment.good{{background:var(--good)}}.segment.bad{{background:var(--bad)}}.segment.unknown{{background:var(--unknown)}}.segment.open{{border-right:2px dashed var(--fg)}}.segment.contradictory{{outline:2px dashed var(--bad)}}.segment.no-progress{{box-shadow:inset 0 0 0 3px var(--bad)}}.segment.hidden-wait{{display:none}}.detail{{margin-top:12px;padding:10px;border-left:3px solid var(--work);background:var(--panel);min-height:44px;overflow-wrap:anywhere}}.legend{{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0;color:var(--muted)}}.swatch{{display:inline-block;width:12px;height:12px;margin-right:4px;vertical-align:-1px}}@media(max-width:560px){{.axis,.lane{{grid-template-columns:1fr}}.axis .axis-label{{display:none}}.track{{height:54px}}.segment{{top:11px;height:36px}}}}
.segment.no-progress{{box-shadow:none}}.show-progress .segment.no-progress{{box-shadow:inset 0 0 0 3px var(--bad)}}
</style></head><body><main id="cohort-app"><h1>Run cohort timeline</h1><div class="subtitle">Diagnostic observations on one shared clock · not authoritative current state</div>
<div class="controls"><label>Highlight run<select id="run-highlight"><option value="">All runs</option></select></label><button id="wait-toggle" type="button" aria-pressed="true">Hide waits</button><button id="progress-toggle" type="button" aria-pressed="false">Highlight no-progress</button></div>
<div class="summary" id="summary" aria-live="polite"></div><div class="legend"><span><i class="swatch" style="background:var(--work)"></i>local/work</span><span><i class="swatch" style="background:var(--provider)"></i>provider boundary</span><span><i class="swatch" style="background:var(--wait)"></i>wait</span><span><i class="swatch" style="background:var(--good)"></i>delivered</span><span><i class="swatch" style="background:var(--bad)"></i>review/failure</span><span><i class="swatch" style="background:var(--unknown)"></i>unknown</span></div>
<div class="timeline"><div class="axis"><div class="axis-label">Run</div><div class="axis-track" id="axis"></div></div><div id="lanes"></div></div><div class="detail" id="detail" aria-live="polite">Select an interval for exact evidence details.</div>
</main><script>
const timeline={encoded},displayTimezone={encoded_timezone};
const app=document.getElementById('cohort-app'),axis=document.getElementById('axis'),lanes=document.getElementById('lanes'),summary=document.getElementById('summary'),detail=document.getElementById('detail'),runHighlight=document.getElementById('run-highlight'),waitToggle=document.getElementById('wait-toggle'),progressToggle=document.getElementById('progress-toggle');
const starts=timeline.runs.map(r=>Date.parse(r.first_timestamp)),ends=timeline.runs.map(r=>Date.parse(r.last_timestamp)),domainStart=Math.min(...starts),domainEnd=Math.max(...ends),domainSpan=Math.max(1,domainEnd-domainStart);let waitsVisible=true,progressVisible=false;
const waitClasses=new Set(['provider_wait','api_deferred_or_queued']);const providerClasses=new Set(['initial_provider_wave','provider_reconciliation','external_authority_v2']);
function format(ms){{return new Intl.DateTimeFormat('en-US',{{timeZone:displayTimezone,hour:'2-digit',minute:'2-digit',second:'2-digit',fractionalSecondDigits:3,hour12:false}}).format(new Date(ms))}}
function tone(c){{if(waitClasses.has(c))return'wait';if(providerClasses.has(c))return'provider';if(c==='delivered')return'good';if(c==='terminal_review'||c==='failure_or_refusal')return'bad';if(c==='unknown')return'unknown';return'work'}}
function percent(ms){{return ((ms-domainStart)/domainSpan)*100}}
function drawAxis(){{axis.replaceChildren();for(let i=0;i<5;i++){{const ms=domainStart+domainSpan*i/4,t=document.createElement('span');t.className='tick';t.style.left=(i*25)+'%';t.textContent=format(ms);axis.appendChild(t)}}}}
function draw(){{lanes.replaceChildren();const selected=runHighlight.value;for(const run of timeline.runs){{const row=document.createElement('section');row.className='lane'+(selected&&selected!==run.native_run_id?' dimmed':'');const name=document.createElement('div');name.className='lane-name';const strong=document.createElement('strong');strong.textContent=run.api_run_id||'API run unavailable';const code=document.createElement('code');code.textContent=run.native_run_id;const small=document.createElement('small');small.textContent=run.final_observed_posture.classification.replaceAll('_',' ');name.append(strong,code,small);const track=document.createElement('div');track.className='track';for(const interval of run.intervals){{const start=Date.parse(interval.start.canonical_timestamp),end=Date.parse((interval.end||interval.start).canonical_timestamp);const segment=document.createElement('button');segment.type='button';segment.className='segment '+tone(interval.classification)+(interval.status==='open'?' open':'')+(interval.status==='contradictory'?' contradictory':'')+(interval.no_progress_candidate_ids.length?' no-progress':'')+(!waitsVisible&&waitClasses.has(interval.classification)?' hidden-wait':'');segment.style.left=Math.max(0,percent(Math.min(start,end)))+'%';segment.style.width=Math.max(.35,Math.abs(end-start)/domainSpan*100)+'%';segment.textContent=interval.label;const evidence=interval.evidence_families.join(' + ');segment.setAttribute('aria-label',interval.label+', '+format(start)+' to '+format(end)+', '+evidence);segment.onclick=()=>{{detail.textContent=`${{interval.label}} · ${{format(start)}} → ${{format(end)}} · ${{interval.duration_ms??'open'}} ms · ${{interval.status}} · evidence ${{evidence}} · source line(s) ${{interval.start.source_line}}${{interval.end?' / '+interval.end.source_line:''}} · interval ${{interval.interval_id}}`;}};track.appendChild(segment)}}row.append(name,track);lanes.appendChild(row)}}summary.textContent=`${{timeline.runs.length}} runs · ${{format(domainStart)}} → ${{format(domainEnd)}} ${{displayTimezone}} · ${{timeline.observed_handoffs.length}} witnessed handoff(s)`;app.classList.toggle('show-progress',progressVisible)}}
for(const run of timeline.runs){{const option=document.createElement('option');option.value=run.native_run_id;option.textContent=(run.api_run_id||run.native_run_id).slice(0,18);runHighlight.appendChild(option)}}
runHighlight.onchange=draw;waitToggle.onclick=()=>{{waitsVisible=!waitsVisible;waitToggle.setAttribute('aria-pressed',String(waitsVisible));waitToggle.textContent=waitsVisible?'Hide waits':'Show waits';draw()}};progressToggle.onclick=()=>{{progressVisible=!progressVisible;progressToggle.setAttribute('aria-pressed',String(progressVisible));progressToggle.textContent=progressVisible?'Clear no-progress highlight':'Highlight no-progress';app.classList.toggle('show-progress',progressVisible)}};drawAxis();draw();
</script></body></html>"""


__all__ = [
    "API_WRAPPER_EVENTS", "build_run_cohort_timeline",
    "CANONICAL_TIMEZONE", "CLOCK_RELATIONS", "EVIDENCE_FAMILIES",
    "FINAL_POSTURES", "HANDOFF_KINDS", "INTERVAL_CLASSIFICATIONS",
    "INTERVAL_STATUSES", "SCHEMA_VERSION", "read_run_cohort_timeline",
    "read_run_cohort_timeline_schema", "render_run_cohort_timeline_html",
    "validate_run_cohort_timeline",
]
