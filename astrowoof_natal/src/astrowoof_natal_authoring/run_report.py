"""Deterministic, diagnostic-only SBE worker-log run reporting."""

from __future__ import annotations

import hashlib
import html
import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = "astrowoof.sbe_run_evolution_report.v1"
PARSER_VERSION = "astrowoof.sbe_trace_parser.v1"
_TRACE_RE = re.compile(
    r"^(?P<outer>.*?)\s+✨🐶\s+(?P<timestamp>\S+)\s+\|\s+"
    r"(?P<level>[^|]+?)\s+\|\s+(?P<host>[^|]+?)\s+\|\s+"
    r"(?P<run>[^|]+?)\s+\|\s+(?P<context>[^|]+?)\s+\|\s+"
    r"(?P<function>[^|]+?)\s+\|\s+(?P<state>[^:]+?)\s+:\s+"
    r"(?P<message>.*)$"
)
_JSON_RE = re.compile(r"^(?P<outer>.*?)\s+(?P<json>\{.*\})$")
_SAFE_TOKEN = re.compile(r"^[A-Za-z0-9_.:/@+,;\-]+$")
_SAFE_EVENT = re.compile(r"^[a-z][a-z0-9_]{1,79}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

SAFE_FIELDS = frozenset({
    "accepted", "acceptance_states", "cause", "edited_field_count",
    "error_class", "error_fingerprint", "improved", "lint_present",
    "lint_report_present", "lint_sha256", "lint_status",
    "lint_warning_codes", "lint_warnings", "omitted_target_count",
    "optional_stage_states", "receipt_sha256", "rejection_codes", "subject",
    "subject_states", "validation_error_count", "validation_errors",
    "validation_present", "validation_report_present", "validation_sha256",
    "validation_status", "validation_warning_count", "validation_warnings",
    "warning_components", "warning_count",
    "action_count", "action_id", "action_ids", "action_stages", "action_states", "actions",
    "affected_claim_count", "ambiguous_count", "attempt", "attempt_count", "branch_action_count",
    "authority_request_sha256", "branch_reason", "capacity", "capacity_disposition", "checkpoint_basis_sha256",
    "checkpoint_generation", "checkpoint_object_id", "command", "command_kind", "context",
    "codes", "created", "custody_count", "deferred_count", "disposition", "duration_ms",
    "eligible_now", "endpoint", "event_count", "exception_class", "exception_fingerprint",
    "execution_branch", "exit_code", "failed_predicates", "fingerprint_sha256",
    "from_state", "function", "grant_sha256", "kind", "local_dependencies",
    "local_dependency_count", "local_operation_count", "local_work", "logical_root_sha256",
    "max_attempts", "mechanism", "method", "native_schema",
    "new_revision", "new_state", "observed_at", "old_revision", "old_state",
    "operation", "operation_count", "operation_id", "outcome", "pass_count", "pass_id",
    "pass_number", "phase", "prepared_count", "provider_action_count",
    "provider_actions", "provider_bound_count", "provider_count", "provider_custody", "provider_id",
    "provider_identity_count", "provider_kind", "provider_operation_id",
    "provider_status", "providers", "quiescence", "reason", "receipt_id", "refusal_present",
    "refusal_reason", "release", "report", "reported_count", "request", "request_kind",
    "request_present", "request_sha256", "retry_attempt_count", "retry_conflict",
    "retry_lineage_status", "review_reason_count",
    "result_class", "result_id", "result_schema", "retry", "revision", "route", "route_family",
    "run_id", "sbe_release", "schema", "selected_command", "selected_count", "snapshot", "snapshot_members",
    "snapshot_sha256", "spc_release", "stage", "state", "state_revision", "status",
    "subject_count", "summary_sha256", "terminal", "terminal_outcome", "timeout_s", "to_state", "validation",
    "v2_actions", "v2_grant_sha256", "v2_intent_present", "v2_intent_state",
    "v2_request_sha256", "wave_id", "workspace_mutated",
})

BOUNDARY_EVENTS = frozenset({
    "command_start", "command_complete", "command_exit", "subprocess_start",
    "subprocess_complete", "workspace_fingerprint", "native_state_summary",
    "lifecycle_inspection_complete", "run_state_transition", "checkpoint_committed",
    "native_publication_start", "native_publication_complete", "native_decision_summary",
    "native_stage_evidence_summary", "native_validation_evidence_summary",
    "native_publication_evidence_summary",
    "native_invocation_started", "external_authority_request_read_start",
    "external_authority_request_read_complete", "external_authority_intent_retired",
    "external_authority_fence_start", "external_authority_intent_committed",
    "external_authority_provider_io_start",
    "spend_boundary_handoff", "spend_action_prepared", "spend_action_authorized",
    "spend_action_consumed", "spend_action_reported", "provider_identity_recorded",
    "provider_request_start", "provider_request_complete", "provider_retrieval_start",
    "provider_retrieval_returned", "reconciliation_cycle_start",
    "reconciliation_wave_selected", "reconciliation_pending", "reconciliation_completed",
    "reconciliation_cycle_checkpoint", "completed_provider_result_joined_for_adoption",
    "authoring_pass_start", "authoring_attempt_start", "authoring_attempt_accepted", "authoring_attempt_rejected",
    "authoring_attempt_ambiguous", "authoring_attempt_external_authority_handoff",
    "authoring_wave_start", "authoring_wave_complete", "authoring_pass_requires_review",
    "initial_wave_start", "initial_member_create_start", "initial_member_create_complete",
    "initial_member_outcome_persisted", "initial_wave_complete",
    "pass_acceptance_advisory", "subject_assembly_start",
    "subject_assembly_complete", "polish_start", "critic_start", "candidate_start",
    "finalization_start", "finalization_deferred", "local_work_progress_refused",
    "execution_failed", "external_authority_refused", "transport_warning",
})

PROGRESS_EVENTS = frozenset({
    "run_state_transition", "provider_identity_recorded", "spend_action_prepared",
    "spend_action_authorized", "spend_action_consumed", "spend_action_reported",
    "reconciliation_completed", "reconciliation_cycle_checkpoint",
    "completed_provider_result_joined_for_adoption", "authoring_attempt_accepted",
    "authoring_attempt_rejected", "authoring_attempt_ambiguous",
    "external_authority_intent_retired",
    "external_authority_intent_committed", "initial_member_create_complete",
    "initial_member_outcome_persisted", "initial_wave_complete",
    "authoring_pass_requires_review",
    "subject_assembly_complete",
})

FORCE_EPOCH_EVENTS = frozenset({
    "command_start", "command_complete", "command_exit", "subprocess_start",
    "subprocess_complete", "run_state_transition", "checkpoint_committed",
    "native_publication_start", "native_publication_complete",
    "provider_request_start", "provider_request_complete", "provider_retrieval_start",
    "provider_retrieval_returned", "provider_identity_recorded",
    "reconciliation_wave_selected", "reconciliation_completed",
    "authoring_attempt_start", "authoring_attempt_accepted", "authoring_attempt_rejected",
    "authoring_attempt_ambiguous", "external_authority_refused", "execution_failed",
    "initial_wave_start", "initial_member_create_start", "initial_member_create_complete",
    "initial_member_outcome_persisted", "initial_wave_complete",
    "local_work_progress_refused", "transport_warning",
})


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_run_evolution_report_schema() -> dict[str, Any]:
    """Read the packaged closed structural schema for diagnostic reports."""
    from importlib.resources import files

    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "sbe-run-evolution-report.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def read_run_evolution_report(path: Path) -> dict[str, Any]:
    """Read and strictly validate one local diagnostic report artifact."""
    return validate_run_evolution_report(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _tokenize(message: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    quote: str | None = None
    depth = 0
    escaped = False
    for character in message.strip():
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\" and quote:
            current.append(character)
            escaped = True
            continue
        if quote:
            current.append(character)
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
            current.append(character)
        elif character in "([{":
            depth += 1
            current.append(character)
        elif character in ")]}" and depth:
            depth -= 1
            current.append(character)
        elif character.isspace() and depth == 0:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(character)
    if current:
        tokens.append("".join(current))
    return tokens


def _safe_value(raw: str) -> Any:
    value = raw.strip()
    if value in {"True", "true"}:
        return True
    if value in {"False", "false"}:
        return False
    if value in {"None", "null", "unknown", "-"}:
        return None
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    if re.fullmatch(r"-?[0-9]+\.[0-9]+", value):
        return float(value)
    if value.startswith("[") and value.endswith("]"):
        members = re.findall(r"['\"]?([A-Za-z0-9_.:/@+\-]+)['\"]?", value[1:-1])
        return members[:64]
    if len(value) <= 256 and _SAFE_TOKEN.fullmatch(value):
        if value.startswith("https://") or value.startswith("http://"):
            return value.split("?", 1)[0]
        return value
    return "sha256:" + hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def _message(message: str) -> tuple[str, dict[str, Any], list[str]]:
    tokens = _tokenize(message)
    if not tokens or not _SAFE_EVENT.fullmatch(tokens[0]):
        return "unparsed_message", {}, []
    event = tokens[0]
    fields: dict[str, Any] = {}
    unknown: list[str] = []
    for token in tokens[1:]:
        if "=" not in token:
            continue
        key, raw = token.split("=", 1)
        if key in SAFE_FIELDS:
            fields[key] = _safe_value(raw)
        elif re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key):
            unknown.append(key)
    return event, fields, sorted(set(unknown))


def parse_trace_text(text: str, *, source_name: str = "worker.log") -> dict[str, Any]:
    lines = text.splitlines()
    events: list[dict[str, Any]] = []
    envelopes: list[dict[str, Any]] = []
    malformed_trace_lines: list[int] = []
    unknown_events: dict[str, int] = {}
    for line_number, line in enumerate(lines, 1):
        if "✨🐶" in line:
            match = _TRACE_RE.match(line)
            if not match:
                malformed_trace_lines.append(line_number)
                continue
            event_name, fields, unknown_fields = _message(match.group("message"))
            if event_name not in BOUNDARY_EVENTS:
                unknown_events[event_name] = unknown_events.get(event_name, 0) + 1
            events.append({
                "event_id": f"evt_{line_number:06d}_{_sha_bytes(line.encode('utf-8'))[:12]}",
                "source_line": line_number,
                "raw_sha256": _sha_bytes(line.encode("utf-8")),
                "outer_timestamp": match.group("outer"),
                "timestamp": match.group("timestamp"),
                "level": match.group("level").strip(),
                "host_id": match.group("host").strip(),
                "run_id": match.group("run").strip(),
                "context_id": match.group("context").strip(),
                "function": match.group("function").strip(),
                "current_state": match.group("state").strip(),
                "event": event_name,
                "fields": fields,
                "unknown_field_names": unknown_fields,
                "registered": event_name in BOUNDARY_EVENTS,
            })
            continue
        match = _JSON_RE.match(line)
        if match:
            try:
                value = json.loads(match.group("json"))
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and isinstance(value.get("envelope_type"), str):
                envelopes.append({
                    "source_line": line_number,
                    "outer_timestamp": match.group("outer"),
                    "envelope_type": value["envelope_type"],
                    "raw_sha256": _sha_bytes(line.encode("utf-8")),
                })
    body = {
        "schema_version": "astrowoof.sbe_normalized_trace.v1",
        "parser_version": PARSER_VERSION,
        "source": {
            "name": Path(source_name).name,
            "sha256": _sha_bytes(text.encode("utf-8")),
            "line_count": len(lines),
        },
        "coverage": {
            "trace_marker_line_count": sum("✨🐶" in line for line in lines),
            "parsed_trace_line_count": len(events),
            "malformed_trace_line_numbers": malformed_trace_lines[:128],
            "malformed_trace_overflow": max(0, len(malformed_trace_lines) - 128),
            "json_envelope_count": len(envelopes),
            "unknown_events": [
                {"event": key, "count": value}
                for key, value in sorted(unknown_events.items())
            ],
        },
        "events": events,
        "json_envelopes": envelopes,
    }
    return {**body, "trace_sha256": _digest(body)}


def _short(value: Any, length: int = 10) -> str:
    text = str(value or "-")
    return text if len(text) <= length else text[:length] + "…"


def _cell(symbol: str, label: str, event: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "label": label[:96],
        "event_ids": [event["event_id"]],
        "source_lines": [event["source_line"]],
    }


def _lane_for(event: Mapping[str, Any]) -> tuple[str, str, str]:
    name = event["event"]
    fields = event["fields"]
    if name.startswith(("authoring_attempt_", "authoring_pass_")):
        pass_id = fields.get("pass_id") or event.get("context_id")
        return f"pass:{pass_id}", f"Pass {_short(pass_id, 18)}", "pass"
    if fields.get("action_id"):
        action_id = fields["action_id"]
        return f"action:{action_id}", f"Action {_short(action_id, 16)}", "action"
    if "authority" in name or name.startswith("spend_"):
        return "authority", "External authority", "authority"
    if name.startswith("provider_"):
        return "provider", "Provider I/O and custody", "provider"
    if name.startswith("reconciliation_") or name == "completed_provider_result_joined_for_adoption":
        return "reconciliation", "Reconciliation and adoption", "reconciliation"
    if name.startswith(("polish_", "critic_", "candidate_", "finalization_", "subject_assembly_")) or name in {
        "native_stage_evidence_summary", "native_validation_evidence_summary",
    }:
        return "local_work", "QA and local work", "local_work"
    if name.startswith("checkpoint_") or name.startswith("native_publication_"):
        return "checkpoint", "Checkpoint and publication", "checkpoint"
    if name.startswith("lifecycle_") or name == "native_decision_summary":
        return "lifecycle", "Lifecycle selection", "lifecycle"
    if name.startswith("command_") or name.startswith("subprocess_"):
        return "command", "Command and worker handoff", "command"
    if "refused" in name or "warning" in name or "failed" in name:
        return "diagnostic", "Warnings and refusals", "diagnostic"
    return "run", "Run status", "run"


def _event_cell(event: Mapping[str, Any]) -> dict[str, Any]:
    name = event["event"]
    fields = event["fields"]
    symbol = "●"
    if name.endswith(("_complete", "_completed", "_accepted", "_reported", "_committed")):
        symbol = "✓"
    elif name.endswith(("_refused", "_rejected", "_failed")):
        symbol = "×"
    elif "ambiguous" in name or name == "transport_warning":
        symbol = "?"
    elif "pending" in name or name.endswith("_start"):
        symbol = "…"
    details = []
    for key in (
        "new_state", "outcome", "reason", "branch_reason", "provider_status",
        "state_revision", "new_revision", "attempt", "action_count", "selected_count",
    ):
        if fields.get(key) is not None:
            details.append(f"{key}={fields[key]}")
    label = name + (" · " + ", ".join(details) if details else "")
    return _cell(symbol, label, event)


def _posture_signature(
    event: Mapping[str, Any], context: Mapping[str, Any], *, include_checkpoint: bool,
) -> str | None:
    if event["event"] != "lifecycle_inspection_complete":
        return None
    fields = event["fields"]
    value = {
        "status": fields.get("status") or event.get("current_state"),
        "branch_reason": fields.get("branch_reason"),
        "capacity_disposition": fields.get("capacity_disposition"),
        "eligible_now": fields.get("eligible_now"),
        "branch_action_count": fields.get("branch_action_count"),
        "provider_actions": fields.get("provider_actions"),
        "local_dependencies": fields.get("local_dependencies"),
    }
    if include_checkpoint:
        value["revision"] = context.get("revision")
        value["snapshot_sha256"] = context.get("snapshot_sha256")
    return _digest(value)


def _no_progress(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    context: dict[str, Any] = {"revision": None, "snapshot_sha256": None}
    progress_generation = 0
    command_generation = 0
    for event in events:
        fields = event["fields"]
        if event["event"] == "workspace_fingerprint":
            context["revision"] = fields.get("revision")
            context["snapshot_sha256"] = fields.get("snapshot_sha256")
        if event["event"] in PROGRESS_EVENTS:
            progress_generation += 1
        # One semantic command boundary per invocation.  Wrapper subprocess and
        # command-complete records can coexist with command_exit and therefore
        # must not each manufacture another generation.
        if event["event"] == "command_exit":
            command_generation += 1
        exact_signature = _posture_signature(event, context, include_checkpoint=True)
        semantic_signature = _posture_signature(event, context, include_checkpoint=False)
        if exact_signature and semantic_signature:
            observations.append({
                "exact_signature": exact_signature,
                "semantic_signature": semantic_signature,
                "event_id": event["event_id"],
                "source_line": event["source_line"],
                "timestamp": event["timestamp"],
                "progress_generation": progress_generation,
                "command_generation": command_generation,
                "state": event["current_state"],
                "branch_reason": fields.get("branch_reason"),
                "revision": context.get("revision"),
                "snapshot_sha256": context.get("snapshot_sha256"),
            })
    candidates: list[dict[str, Any]] = []
    previous_by_signature: dict[str, dict[str, Any]] = {}
    for observation in observations:
        previous = previous_by_signature.get(observation["semantic_signature"])
        if (
            previous
            and observation["command_generation"] > previous["command_generation"]
            and observation["progress_generation"] == previous["progress_generation"]
        ):
            exact_replay = observation["exact_signature"] == previous["exact_signature"]
            body = {
                "classification": (
                    "candidate_exact_no_progress_cycle"
                    if exact_replay else "candidate_semantic_republication_cycle"
                ),
                "semantic_posture_sha256": observation["semantic_signature"],
                "checkpoint_posture_changed": not exact_replay,
                "first_event_id": previous["event_id"],
                "last_event_id": observation["event_id"],
                "first_source_line": previous["source_line"],
                "last_source_line": observation["source_line"],
                "command_boundaries_crossed": (
                    observation["command_generation"] - previous["command_generation"]
                ),
                "progress_witness_count": 0,
                "state": observation["state"],
                "branch_reason": observation["branch_reason"],
                "first_revision": previous["revision"],
                "last_revision": observation["revision"],
            }
            candidates.append({**body, "candidate_sha256": _digest(body)})
        previous_by_signature[observation["semantic_signature"]] = observation
    return candidates


def _build_run(run_id: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    selected = [event for event in events if event["event"] in BOUNDARY_EVENTS]
    no_progress_candidates = _no_progress(events)
    candidate_lines = {
        candidate["last_source_line"] for candidate in no_progress_candidates
    }
    lanes: dict[str, dict[str, str]] = {
        "run": {"lane_id": "run", "label": "Run status", "kind": "run"},
        "lifecycle": {"lane_id": "lifecycle", "label": "Lifecycle selection", "kind": "lifecycle"},
    }
    epochs: list[dict[str, Any]] = []
    current: dict[str, dict[str, Any]] = {}
    for index, event in enumerate(selected):
        lane_id, label, kind = _lane_for(event)
        lanes.setdefault(lane_id, {"lane_id": lane_id, "label": label, "kind": kind})
        next_cell = _event_cell(event)
        previous_cell = current.get(lane_id)
        changed = previous_cell is None or (
            previous_cell["symbol"], previous_cell["label"]
        ) != (next_cell["symbol"], next_cell["label"])
        current[lane_id] = next_cell
        cell_changes = {lane_id: next_cell}
        if event["event"] == "run_state_transition":
            current["run"] = next_cell
            cell_changes["run"] = next_cell
        elif event.get("current_state") and event["current_state"] != "-":
            current.setdefault("run", _cell("●", str(event["current_state"]), event))
        if not (
            changed
            or event["event"] in FORCE_EPOCH_EVENTS
            or event["source_line"] in candidate_lines
        ):
            continue
        epochs.append({
            "epoch_id": f"epoch_{len(epochs) + 1:04d}",
            "timestamp": event["timestamp"],
            "source_line": event["source_line"],
            "boundary_event": event["event"],
            "boundary_event_id": event["event_id"],
            # Sparse deltas keep long runs compact. Renderers reconstruct the
            # observed posture at each selected epoch deterministically.
            "cell_changes": deepcopy(cell_changes),
        })
    lane_order = ["run", "lifecycle"]
    lane_order.extend(sorted(key for key in lanes if key.startswith("pass:")))
    lane_order.extend(sorted(key for key in lanes if key.startswith("action:")))
    lane_order.extend(key for key in (
        "authority", "provider", "reconciliation", "local_work", "checkpoint",
        "command", "diagnostic",
    ) if key in lanes)
    inventory = {
        "pass_ids": sorted({str(event["fields"].get("pass_id")) for event in events if event["fields"].get("pass_id")}),
        "action_ids": sorted({str(event["fields"].get("action_id")) for event in events if event["fields"].get("action_id")}),
        "provider_ids": sorted({str(event["fields"].get("provider_id") or event["fields"].get("provider_operation_id")) for event in events if event["fields"].get("provider_id") or event["fields"].get("provider_operation_id")}),
        "hosts": sorted({event["host_id"] for event in events}),
    }
    durations: dict[str, list[tuple[int, int]]] = {}
    for event in events:
        duration = event["fields"].get("duration_ms")
        if isinstance(duration, (int, float)) and duration >= 0:
            durations.setdefault(event["event"], []).append((int(duration), event["source_line"]))
    timing = []
    for event_name, observations in sorted(durations.items()):
        values = sorted(item[0] for item in observations)
        middle = len(values) // 2
        median = (
            values[middle] if len(values) % 2
            else (values[middle - 1] + values[middle]) / 2
        )
        timing.append({
            "event": event_name,
            "count": len(values),
            "minimum_ms": values[0],
            "median_ms": median,
            "maximum_ms": values[-1],
            "total_ms": sum(values),
            "source_lines": [item[1] for item in observations[:128]],
            "source_line_overflow": max(0, len(observations) - 128),
        })
    return {
        "run_id": run_id,
        "first_timestamp": events[0]["timestamp"] if events else None,
        "last_timestamp": events[-1]["timestamp"] if events else None,
        "event_count": len(events),
        "inventory": inventory,
        "timing_observations": timing,
        "lanes": [lanes[key] for key in lane_order],
        "epochs": epochs,
        "no_progress_candidates": no_progress_candidates,
        "final_observed_posture": {
            "status": next((event["current_state"] for event in reversed(events) if event["current_state"] != "-"), None),
            "diagnostic_only": True,
            "not_authoritative_current_state": True,
        },
    }


def build_run_evolution_report(trace: Mapping[str, Any]) -> dict[str, Any]:
    if trace.get("schema_version") != "astrowoof.sbe_normalized_trace.v1":
        raise ValueError("Unsupported normalized trace schema")
    grouped: dict[str, list[dict[str, Any]]] = {}
    global_events: list[dict[str, Any]] = []
    for event in trace.get("events", []):
        run_id = event.get("run_id")
        if run_id == "-":
            global_events.append(deepcopy(event))
        elif isinstance(run_id, str) and run_id:
            grouped.setdefault(run_id, []).append(deepcopy(event))
    body = {
        "schema_version": SCHEMA_VERSION,
        "parser_version": trace["parser_version"],
        "source": deepcopy(trace["source"]),
        "trace_sha256": trace["trace_sha256"],
        "coverage": deepcopy(trace["coverage"]),
        "diagnostic_only": True,
        "runs": [_build_run(run_id, grouped[run_id]) for run_id in sorted(grouped)],
        "global_event_count": len(global_events),
    }
    return {**body, "report_sha256": _digest(body)}


def validate_run_evolution_report(value: Any) -> dict[str, Any]:
    required = {
        "schema_version", "report_sha256", "parser_version", "source",
        "trace_sha256", "coverage", "diagnostic_only", "runs", "global_event_count",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Run evolution report shape is invalid")
    body = {key: item for key, item in value.items() if key != "report_sha256"}
    if (
        value.get("schema_version") != SCHEMA_VERSION
        or value.get("parser_version") != PARSER_VERSION
        or value.get("diagnostic_only") is not True
        or value.get("report_sha256") != _digest(body)
        or not isinstance(value.get("runs"), list)
        or not isinstance(value.get("global_event_count"), int)
    ):
        raise ValueError("Run evolution report semantics are invalid")
    for run in value["runs"]:
        if not isinstance(run, dict) or not isinstance(run.get("run_id"), str):
            raise ValueError("Run report entry is invalid")
        if run.get("final_observed_posture", {}).get("not_authoritative_current_state") is not True:
            raise ValueError("Run report overclaims current-state authority")
    return deepcopy(value)


def build_report_from_text(text: str, *, source_name: str = "worker.log") -> dict[str, Any]:
    return validate_run_evolution_report(
        build_run_evolution_report(parse_trace_text(text, source_name=source_name))
    )


def _materialized_epochs(epochs: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    current: dict[str, Any] = {}
    materialized: list[dict[str, Any]] = []
    for epoch in epochs:
        current.update(deepcopy(epoch["cell_changes"]))
        materialized.append({**deepcopy(dict(epoch)), "cells": deepcopy(current)})
    return materialized


def render_report_markdown(report: Mapping[str, Any], *, max_epochs: int = 24) -> str:
    validate_run_evolution_report(report)
    output = ["# SBE run evolution report", "", f"Source: `{report['source']['name']}`", ""]
    for run in report["runs"]:
        epochs = _materialized_epochs(run["epochs"])
        if len(epochs) > max_epochs:
            indices = sorted(set(
                list(range(min(8, len(epochs))))
                + list(range(max(0, len(epochs) - 8), len(epochs)))
                + [round(index * (len(epochs) - 1) / (max_epochs - 1)) for index in range(max_epochs)]
            ))[:max_epochs]
            epochs = [epochs[index] for index in indices]
        output.extend([f"## Run `{run['run_id']}`", ""])
        headers = ["Lane"] + [epoch["epoch_id"] for epoch in epochs]
        output.append("| " + " | ".join(headers) + " |")
        output.append("|" + "|".join(["---"] * len(headers)) + "|")
        for lane in run["lanes"]:
            cells = [lane["label"]]
            for epoch in epochs:
                cell = epoch["cells"].get(lane["lane_id"])
                cells.append("" if cell is None else f"{cell['symbol']} {cell['label']}")
            output.append("| " + " | ".join(item.replace("|", "\\|") for item in cells) + " |")
        output.extend(["", f"No-progress candidates: {len(run['no_progress_candidates'])}", ""])
    return "\n".join(output).rstrip() + "\n"


def render_report_mermaid(report: Mapping[str, Any], *, max_events: int = 80) -> str:
    validate_run_evolution_report(report)
    lines = ["sequenceDiagram", "    participant Worker", "    participant Native", "    participant API", "    participant Provider"]
    for run in report["runs"]:
        lines.append(f"    Note over Worker,Provider: Run {_short(run['run_id'], 16)}")
        epochs = run["epochs"][:max_events]
        for epoch in epochs:
            event = epoch["boundary_event"]
            target = "Native"
            if "authority" in event or event.startswith("spend_"):
                target = "API"
            elif event.startswith("provider_"):
                target = "Provider"
            lines.append(f"    Worker->>{target}: {event}")
        if len(run["epochs"]) > max_events:
            lines.append(f"    Note over Worker,Provider: {len(run['epochs']) - max_events} epochs omitted")
    return "\n".join(lines) + "\n"


def render_report_html(report: Mapping[str, Any]) -> str:
    validate_run_evolution_report(report)
    encoded = json.dumps(report, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>SBE run evolution report</title>
<style>
:root{{--bg:#0c111b;--fg:#edf2f7;--muted:#9eacc0;--panel:#151d2b;--line:#304056;--accent:#79b8ff;--good:#73d99f;--bad:#ff8585;--warn:#ffd479}}
@media (prefers-color-scheme:light){{:root{{--bg:#f7f9fc;--fg:#172033;--muted:#58677e;--panel:#fff;--line:#cad3df;--accent:#185fa5;--good:#157347;--bad:#b42318;--warn:#8a5b00}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif}} main{{padding:16px;max-width:100%}}
h1{{font-size:20px;margin:0 0 12px}} .controls{{display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin-bottom:12px}} label{{display:grid;gap:4px;color:var(--muted)}}
select,input,button{{font:inherit;color:var(--fg);background:var(--panel);border:1px solid var(--line);padding:8px}} button{{cursor:pointer}} .summary{{color:var(--muted);margin:8px 0 12px}}
.matrix{{overflow:auto;border:1px solid var(--line);background:var(--panel);max-height:70vh}} table{{border-collapse:separate;border-spacing:0;min-width:100%}} th,td{{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:6px 8px;min-width:150px;vertical-align:top}}
th{{position:sticky;top:0;background:var(--panel);z-index:2;text-align:left}} th:first-child,td:first-child{{position:sticky;left:0;background:var(--panel);z-index:1;min-width:180px}} th:first-child{{z-index:3}}
td button{{border:0;background:transparent;padding:0;text-align:left;width:100%;color:inherit}} .sym{{font-weight:700}} .good{{color:var(--good)}} .bad{{color:var(--bad)}} .warn{{color:var(--warn)}}
.detail{{margin-top:12px;padding:10px;border-left:3px solid var(--accent);background:var(--panel);min-height:42px}} .hidden{{display:none}} code{{color:var(--accent)}}
</style></head><body><main id=\"app\"><h1>SBE run evolution</h1>
<div class=\"controls\"><label>Run<select id=\"run\"></select></label><label>Lane filter<input id=\"filter\" type=\"search\" placeholder=\"pass, provider, authority…\"></label><label>Epoch density<select id=\"density\"><option value=\"all\">All</option><option value=\"48\">48</option><option value=\"24\" selected>24</option><option value=\"12\">12</option></select></label><button id=\"issues\" type=\"button\">No-progress only</button></div>
<div class=\"summary\" id=\"summary\" aria-live=\"polite\"></div><div class=\"matrix\"><table><thead id=\"head\"></thead><tbody id=\"body\"></tbody></table></div><div class=\"detail\" id=\"detail\" aria-live=\"polite\">Select a cell for source evidence.</div>
</main><script>
const report={encoded}; const runSelect=document.getElementById('run'), filter=document.getElementById('filter'), density=document.getElementById('density'), head=document.getElementById('head'), body=document.getElementById('body'), summary=document.getElementById('summary'), detail=document.getElementById('detail'), issues=document.getElementById('issues'); let issueOnly=false;
for(const run of report.runs){{const o=document.createElement('option');o.value=run.run_id;o.textContent=run.run_id.slice(0,16)+'…';runSelect.appendChild(o)}}
function materialized(items){{const state={{}};return items.map(e=>{{Object.assign(state,e.cell_changes);return Object.assign({{}},e,{{cells:Object.assign({{}},state)}})}})}}
function sampled(items,n){{if(n==='all'||items.length<=Number(n))return items;const count=Number(n),out=[];for(let i=0;i<count;i++)out.push(items[Math.round(i*(items.length-1)/(count-1))]);return [...new Map(out.map(x=>[x.epoch_id,x])).values()]}}
function cls(symbol){{return symbol==='✓'?'good':symbol==='×'?'bad':symbol==='?'||symbol==='↻'?'warn':''}}
function draw(){{const run=report.runs.find(x=>x.run_id===runSelect.value)||report.runs[0];if(!run)return;const candidates=run.no_progress_candidates;let available=materialized(run.epochs);if(issueOnly){{const ranges=candidates.map(x=>[x.first_source_line,x.last_source_line]);available=available.filter(e=>ranges.some(r=>e.source_line>=r[0]&&e.source_line<=r[1]));}}const epochs=sampled(available,density.value),needle=filter.value.toLowerCase();summary.textContent=`${{run.event_count}} events · ${{run.lanes.length}} lanes · ${{run.epochs.length}} semantic epochs · ${{candidates.length}} no-progress candidate(s)`;head.replaceChildren();body.replaceChildren();if(issueOnly&&!candidates.length){{detail.textContent='No no-progress candidates were detected for this run.';}}const hr=document.createElement('tr'),corner=document.createElement('th');corner.textContent='Lane';hr.appendChild(corner);for(const e of epochs){{const th=document.createElement('th');th.textContent=e.epoch_id+' · '+e.boundary_event;th.title=e.timestamp+' · source line '+e.source_line;hr.appendChild(th)}}head.appendChild(hr);for(const lane of run.lanes){{if(needle&&!lane.label.toLowerCase().includes(needle))continue;if(issueOnly&&lane.kind!=='diagnostic'&&lane.kind!=='command'&&lane.kind!=='lifecycle'&&lane.kind!=='run')continue;const tr=document.createElement('tr'),lh=document.createElement('td');lh.textContent=lane.label;tr.appendChild(lh);for(const e of epochs){{const td=document.createElement('td'),cell=e.cells[lane.lane_id];if(cell){{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label',lane.label+', '+cell.label);const s=document.createElement('span');s.className='sym '+cls(cell.symbol);s.textContent=cell.symbol+' ';b.append(s,document.createTextNode(cell.label));b.onclick=()=>{{detail.textContent=`${{lane.label}} · ${{e.timestamp}} · ${{cell.label}} · source line(s) ${{cell.source_lines.join(', ')}} · event ${{cell.event_ids.join(', ')}}`;}};td.appendChild(b)}}tr.appendChild(td)}}body.appendChild(tr)}}}}
runSelect.onchange=draw;filter.oninput=draw;density.onchange=draw;issues.onclick=()=>{{issueOnly=!issueOnly;issues.textContent=issueOnly?'Show all lanes':'No-progress only';draw()}};draw();
</script></body></html>"""


__all__ = [
    "build_report_from_text", "build_run_evolution_report", "parse_trace_text",
    "read_run_evolution_report", "read_run_evolution_report_schema",
    "render_report_html", "render_report_markdown", "render_report_mermaid",
    "validate_run_evolution_report",
]
