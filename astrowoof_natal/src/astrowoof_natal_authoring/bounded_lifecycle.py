"""Bounded-Natal route over SBE's released lifecycle and spend contracts.

This module owns only bounded route sequencing. Durable persistence, workspace
integrity, paid-action authorization, lifecycle inspection, and closeout are the
same implementations used by exact-Natal authoring.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

from .bounded_authoring import (
    BOUNDED_RUN_V2_CONTRACT,
    BoundedAuthoringArtifacts,
    assemble_bounded_editorial_passes,
    assert_provider_minimized,
    fake_author_bounded,
    validate_bounded_final_cards,
)
from .closure import (
    SCHEMA_VERSION,
    SNAPSHOT_SCHEMA,
    SpendController,
    batch_estimated_cost,
    apply_spend_authorizations,
    checkpoint_spend_boundary,
    estimated_text_tokens,
    load_json,
    normalized_path,
    normalized_usage,
    persist_state,
    save_state,
    sha256_file,
    utc_now,
    validate_workspace_snapshot,
    write_workspace_snapshot,
    write_json_atomic,
    response_output_text,
)
from .execution_events import ExecutionEventEmitter
from .application_logging import bind_logging_context, logging_context
from .initial_wave import (
    INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
    InitialWaveError,
    InitialWaveMemberSpec,
    ProviderCreateResult as InitialWaveProviderCreateResult,
    build_initial_wave,
    build_initial_wave_binding_bundle,
    build_wave_authorization,
    execute_initial_wave_creates,
    is_active_initial_wave,
    preflight_wave_authorization,
    validate_initial_wave,
    validate_initial_wave_binding_bundle_against_wave,
)
from .spend import (
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
    BudgetExhausted,
    PRICE_BOOK_VERSION,
    action_binding,
    authorize_action,
    begin_submission,
    conservative_commitment_micros,
    digest as spend_digest,
    mark_ambiguous,
    new_ledger,
    prepare_action,
    profile_digest as spend_profile_digest,
    record_provider_id,
    validate_policy,
)
from .response_diagnostics import sanitize_error_message


logger = logging.getLogger(__name__)
from .reconciliation import initial_timing


BOUNDED_ROUTE = "bounded_natal.v2"
BOUNDED_RUN_CONTRACT = BOUNDED_RUN_V2_CONTRACT
LEGACY_BOUNDED_RUN_CONTRACT = "astrowoof.bounded_natal.authoring_run.v1"
BOUNDED_DELIVERY_CONTRACT = "astrowoof.bounded_natal.delivery.v1"
FINAL_STAGES = ("polish", "qualitative_critic", "qualitative_candidate")


class BoundedLifecycleProvider(Protocol):
    name: str
    model: str
    service_level: str
    maximum_output_tokens: int
    paid: bool
    batch_transport: Any

    def execute(
        self,
        *,
        stage: str,
        route: str,
        payload: dict[str, Any],
        before_submit: Callable[[dict[str, Any]], None] | None,
        provider_created: Callable[[str | None, str], None] | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]: ...


TERMINAL_BATCH_STATES = frozenset({"completed", "failed", "expired", "cancelled"})
BATCH_ROUND_KEYS = frozenset({
    "schema_version", "round_number", "state", "stage", "model", "created_at",
    "input_path", "input_sha256", "member_count", "requests",
    "aggregate_maximum_output_tokens", "aggregate_commitment_micro_usd",
    "input_file_id", "batch_id", "batch_status", "output_file_id",
    "error_file_id", "cost_disposition",
    "request_counts", "finished_at", "integrity_review",
})
BATCH_REQUEST_KEYS = frozenset({
    "custom_id", "pass_id", "attempt_number", "stage", "request_sha256",
    "packet_sha256", "model", "maximum_output_tokens",
})


@dataclass
class FakeBoundedLifecycleProvider:
    """Deterministic provider-free implementation for release qualification."""

    name: str = "fake"
    model: str = "fake-bounded-v1"
    service_level: str = "interactive"
    maximum_output_tokens: int = 0
    paid: bool = False

    def execute(
        self, *, stage: str, route: str, payload: dict[str, Any],
        before_submit: Callable[[dict[str, Any]], None] | None = None,
        provider_created: Callable[[str | None, str], None] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        assert_provider_minimized(payload)
        if stage in {"authoring_initial", "creative_retry"}:
            result = fake_author_bounded(payload["authoring_packet"])
        elif stage in {"polish", "qualitative_candidate"}:
            result = deepcopy(payload["cards"])
        elif stage == "qualitative_critic":
            result = {
                "schema_version": "astrowoof.bounded_natal.critic.v1",
                "outcome": "accept",
                "findings": [],
            }
        else:
            raise ValueError(f"Unsupported bounded provider stage: {stage}")
        return result, {
            "provider": "fake",
            "model": self.model,
            "response_id": "fake_" + _digest({"stage": stage, "route": route, "payload": payload})[:24],
            "duration_ms": 0,
            "usage": {},
            "estimated_cost": {"currency": "USD", "estimated_amount": 0},
        }


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def _artifact(path: Path, run_dir: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(run_dir).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _emit_artifact(
    emitter: ExecutionEventEmitter | None, kind: str, schema: str, path: Path
) -> None:
    if emitter:
        emitter.emit("bounded.artifact.committed", data={
            "artifact_kind": kind,
            "schema_version": schema,
            "sha256": sha256_file(path),
        })


def create_bounded_run(
    run_dir: Path,
    artifacts: BoundedAuthoringArtifacts,
    *,
    provider: BoundedLifecycleProvider | None = None,
    generation_profile: Mapping[str, Any] | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
) -> dict[str, Any]:
    """Create one complete, resumable bounded workspace before provider work."""
    provider = provider or FakeBoundedLifecycleProvider()
    run_dir = run_dir.resolve()
    logger.info(
        "bounded_run_create_start provider=%s service_level=%s run_dir=%s",
        provider.name, getattr(provider, "service_level", "interactive"), run_dir,
    )
    if run_dir.exists() and any(run_dir.iterdir()):
        raise ValueError("Bounded run directory must be absent or empty")
    run_dir.mkdir(parents=True, exist_ok=True)
    profile = deepcopy(dict(generation_profile or {}))
    optional = profile.setdefault("optional_stages", {
        "polish": True,
        "qualitative_critic": True,
        "qualitative_candidate": True,
    })
    if set(optional) != set(FINAL_STAGES) or not all(
        isinstance(value, bool) for value in optional.values()
    ):
        raise ValueError("optional_stages must explicitly boolean-enable all bounded optional stages")

    inputs = run_dir / "bounded" / "inputs"
    inputs.mkdir(parents=True)
    values = {
        "claim-deck.json": artifacts.claim_deck,
        "authoring-packet.json": artifacts.authoring_packet,
        "disposition-report.json": artifacts.disposition_report,
        "split-assignment.json": artifacts.split_assignment,
    }
    for name, value in values.items():
        write_json_atomic(inputs / name, value)
    packets_dir = inputs / "passes"
    packets_dir.mkdir()
    packet_artifacts: dict[str, dict[str, Any]] = {}
    for pass_id, packet in artifacts.pass_packets.items():
        packet_path = packets_dir / f"{pass_id}.json"
        write_json_atomic(packet_path, packet)
        packet_artifacts[pass_id] = _artifact(packet_path, run_dir)
    now = utc_now()
    subject = artifacts.authoring_packet["subject"]
    subject_id = str(subject.get("subject_id") or "bounded-subject")
    run_id = _digest({
        "route": BOUNDED_ROUTE,
        "logical_root": normalized_path(run_dir),
        "claim_deck_sha256": _digest(artifacts.claim_deck),
        "created_at": now,
    })
    pass_records = [
        *artifacts.split_assignment["card_passes"],
        artifacts.split_assignment["summary_pass"],
    ]
    state: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "route_contract": BOUNDED_RUN_CONTRACT,
        "route": BOUNDED_ROUTE,
        "state_revision": 0,
        "run_id": run_id,
        "status": "AUTHORING",
        "created_at": now,
        "updated_at": now,
        "input_package": normalized_path(inputs / "claim-deck.json"),
        "input_contract": {
            "kind": "bounded_natal",
            "schema_version": artifacts.claim_deck["schema_version"],
            "sha256": sha256_file(inputs / "claim-deck.json"),
        },
        "authoring_profile": profile,
        "run_dir": normalized_path(run_dir),
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
            "snapshot_schema": SNAPSHOT_SCHEMA,
            "snapshot_manifest": "workspace-snapshot.json",
        },
        "provider_disclosure": deepcopy(artifacts.authoring_packet["provider_disclosure"]),
        "provider": provider.name,
        "service_level": provider.service_level,
        "provider_configuration": {
            "model": provider.model,
            "maximum_output_tokens": provider.maximum_output_tokens,
        },
        "max_attempts": int(profile.get("max_attempts", 2)),
        "sbe": {"status": "pass", "subject_count": 1, "route": BOUNDED_ROUTE},
        "passes": {
            record["pass_id"]: {
                "pass_id": record["pass_id"],
                "subject": subject_id,
                "pass_number": record["pass_number"],
                "purpose": record["purpose"],
                "ordered_claim_ids": list(record["ordered_claim_ids"]),
                "source_zip": normalized_path(
                    run_dir / packet_artifacts[record["pass_id"]]["path"]
                ),
                "source_sha256": packet_artifacts[record["pass_id"]]["sha256"],
                "state": "GENERATED",
                "attempts": [],
                "accepted_workspace": None,
                "accepted_attempt": None,
            }
            for record in pass_records
        },
        "subjects": {},
        "bounded": {
            "stage": "AUTHORING",
            "assignment_sha256": artifacts.split_assignment["assignment_sha256"],
            "pass_ids": [record["pass_id"] for record in pass_records],
            "claim_deck": _artifact(inputs / "claim-deck.json", run_dir),
            "authoring_packet": _artifact(inputs / "authoring-packet.json", run_dir),
            "disposition_report": _artifact(inputs / "disposition-report.json", run_dir),
            "split_assignment": _artifact(inputs / "split-assignment.json", run_dir),
            "pass_packets": packet_artifacts,
            "completed_stages": [], "skipped_stages": [],
            "completed_pass_ids": [],
        },
    }
    if provider.paid:
        state["spend_ledger"] = new_ledger(validate_policy(profile.get("spend_policy")))
    persist_state(run_dir / "run.json", state)
    save_state(run_dir / "run.json", state)
    bind_logging_context(run_id=state["run_id"], current_state=state["status"])
    logger.info(
        "bounded_run_created state_revision=%s pass_count=%s claim_count=%s",
        state["state_revision"], len(pass_records),
        len(artifacts.claim_deck["claims"]),
    )
    if event_emitter:
        event_emitter.emit("run.started", data={"state_revision": state["state_revision"]})
        event_emitter.emit("bounded.admission.completed", data={
            "admission_id": artifacts.claim_deck["source"]["admission_id"],
            "input_contract": artifacts.claim_deck["source"]["input_contract"],
        })
        event_emitter.emit("bounded.family.validated", data={
            "context_count": 4, "certainty_class": "invariant",
        })
        event_emitter.emit("bounded.selection.completed", data={
            "claim_count": len(artifacts.claim_deck["claims"]),
            "selection_contract": artifacts.claim_deck["selection"]["candidate_policy"],
        })
        event_emitter.emit("bounded.disposition.completed", data={
            "selected_count": len(artifacts.claim_deck["claims"]),
            "suppressed_count": len(artifacts.disposition_report.get("suppressed") or []),
        })
        for name, value in values.items():
            _emit_artifact(event_emitter, name[:-5], value["schema_version"], inputs / name)
        for pass_id, descriptor in packet_artifacts.items():
            _emit_artifact(
                event_emitter,
                f"authoring-pass:{pass_id}",
                artifacts.pass_packets[pass_id]["schema_version"],
                run_dir / descriptor["path"],
            )
    return state


def _payload(
    state: dict[str, Any], run_dir: Path, stage: str, pass_id: str | None = None
) -> dict[str, Any]:
    bounded = state["bounded"]
    packet_descriptor = (
        bounded["pass_packets"][pass_id]
        if pass_id is not None else bounded["authoring_packet"]
    )
    packet = load_json(run_dir / packet_descriptor["path"])
    payload: dict[str, Any] = {
        "route": BOUNDED_ROUTE,
        "stage": stage,
        "authoring_packet": packet,
    }
    if stage == "creative_retry" and pass_id is not None:
        attempts = state["passes"][pass_id]["attempts"]
        if not attempts or attempts[-1]["state"] != "PASS_QA_REJECTED":
            raise ValueError("Bounded creative retry has no rejected pass-local attempt")
        payload["retry_feedback"] = {
            "schema_version": "astrowoof.bounded_natal.pass_retry_feedback.v1",
            "pass_id": pass_id,
            "previous_attempt": attempts[-1]["attempt"],
            "reason_codes": list(attempts[-1]["qa"]["report"]["errors"]),
        }
    cards = run_dir / "bounded" / "final" / "cards.json"
    if cards.is_file():
        payload["cards"] = load_json(cards)
    assert_provider_minimized(payload)
    return payload


def _execute_stage(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
    stage: str, attempt: int, controller: SpendController | None,
    pass_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if pass_id is not None:
        route = f"{BOUNDED_ROUTE}:{pass_id}:attempt-{attempt:03d}"
        result_name = f"{pass_id}-attempt-{attempt:03d}.json"
    else:
        route = f"{BOUNDED_ROUTE}:{stage}:{attempt}"
        result_name = f"{stage}-{attempt}.json"
    result_path = run_dir / "bounded" / "provider-results" / result_name
    if result_path.is_file():
        durable = load_json(result_path)
        if durable.get("route") != route:
            raise ValueError("Durable bounded provider result route mismatch")
        return durable["result"], durable["metadata"]
    resumed = next((
        action for action in ((state.get("spend_ledger") or {}).get("actions") or [])
        if action["binding"]["stage"] == stage
        and action["binding"]["route"] == route
        and (action.get("provider") or {}).get("id")
        and action.get("state") in {"PROVIDER_ID_RECORDED", "WAITING"}
    ), None)
    resume_operation = getattr(provider, "resume", None)
    if resumed is not None:
        if not callable(resume_operation):
            raise AmbiguousProviderSubmission(
                "Bounded provider operation is durable but this provider cannot reconcile it",
                action=resumed,
            )
        if controller:
            controller.local.active_action = resumed["action_id"]
        result, metadata = resume_operation(
            stage=stage,
            route=route,
            provider_operation_id=resumed["provider"]["id"],
            payload=_payload(state, run_dir, stage, pass_id),
        )
        write_json_atomic(result_path, {
            "schema_version": "astrowoof.bounded_natal.provider_result.v1",
            "route": route, "result": result, "metadata": metadata,
        })
        if controller:
            controller.settle_active(metadata)
        return result, metadata
    before = created = None
    if controller:
        before, created = controller.callbacks(
            stage=stage, route=route, model=provider.model,
            service_level=(
                "interactive" if stage in FINAL_STAGES else provider.service_level
            ),
            maximum_output_tokens=provider.maximum_output_tokens,
        )
    try:
        result, metadata = provider.execute(
            stage=stage, route=route,
            payload=_payload(state, run_dir, stage, pass_id),
            before_submit=before, provider_created=created,
        )
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission) as exc:
        logger.warning(
            "bounded_provider_stage_handoff stage=%s route=%s error_class=%s error=%s",
            stage, route, type(exc).__name__, sanitize_error_message(exc),
        )
        raise
    except Exception as exc:
        logger.exception(
            "bounded_provider_stage_failed stage=%s route=%s error_class=%s error=%s",
            stage, route, type(exc).__name__, sanitize_error_message(exc),
        )
        if controller:
            controller.mark_active_ambiguous(str(exc))
        raise
    write_json_atomic(result_path, {
        "schema_version": "astrowoof.bounded_natal.provider_result.v1",
        "route": route, "result": result, "metadata": metadata,
    })
    if controller:
        controller.settle_active(metadata)
    return result, metadata


def _pass_result_report(
    result: Mapping[str, Any], packet: Mapping[str, Any]
) -> dict[str, Any]:
    errors: list[str] = []
    if result.get("subject") != packet.get("subject"):
        errors.append("provider-visible subject drifted")
    if result.get("authority_notice") != packet.get("authority_notice"):
        errors.append("authority notice drifted")
    if result.get("projected_term_registry") != packet.get("projected_term_registry"):
        errors.append("projected term registry drifted")
    expected = {claim["claim_id"]: claim for claim in packet["claims"]}
    cards = result.get("cards") or []
    supplied = [card.get("claim_id") for card in cards]
    if len(supplied) != len(expected) or set(supplied) != set(expected):
        errors.append("pass card membership changed")
    for card in cards:
        source = expected.get(card.get("claim_id"))
        if source is None:
            continue
        for field in (
            "priority_id", "claim_kind", "editorial_tier", "invariant_authority"
        ):
            if card.get(field) != source.get(field):
                errors.append(f"{card.get('claim_id')} changed locked {field}")
    expected_summaries = set(packet.get("summaries") or {})
    supplied_summaries = set((result.get("summaries") or {}).keys())
    if supplied_summaries != expected_summaries:
        errors.append("pass summary membership changed")
    return {
        "schema_version": "astrowoof.bounded_natal.pass_validation.v1",
        "pass_id": packet["pass_id"],
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def _assemble_accepted_passes(
    state: dict[str, Any], run_dir: Path
) -> dict[str, Any]:
    bounded = state["bounded"]
    packet = load_json(run_dir / bounded["authoring_packet"]["path"])
    assignment = load_json(run_dir / bounded["split_assignment"]["path"])
    pass_outputs: dict[str, dict[str, Any]] = {}
    final_by_pass: dict[str, dict[str, Any]] = {}
    for pass_id in bounded["pass_ids"]:
        record = state["passes"][pass_id]
        if record["state"] != "PASS_QA_ACCEPTED":
            raise ValueError("Cannot assemble bounded deck before every pass is accepted")
        accepted = load_json(Path(record["accepted_workspace"]))
        final_by_pass[pass_id] = accepted
        pass_outputs[pass_id] = {
            "pass_id": pass_id,
            "cards": deepcopy(accepted.get("cards") or []),
            "summaries": [
                {"summary_id": summary_id, **deepcopy(summary)}
                for summary_id, summary in (accepted.get("summaries") or {}).items()
            ],
        }
    assembled = assemble_bounded_editorial_passes(pass_outputs, packet, assignment)
    summaries = {
        item["summary_id"]: {
            key: deepcopy(value) for key, value in item.items() if key != "summary_id"
        }
        for item in assembled["summaries"]
    }
    return {
        "schema_version": next(iter(final_by_pass.values()))["schema_version"],
        "editorial_status": "complete",
        "subject": deepcopy(packet["subject"]),
        "authority_notice": deepcopy(packet["authority_notice"]),
        "cards": assembled["cards"],
        "summaries": summaries,
        "projected_term_registry": deepcopy(packet["projected_term_registry"]),
    }


def _batch_jsonl(text: str) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        custom_id = value.get("custom_id")
        if not isinstance(custom_id, str) or not custom_id:
            raise ValueError(f"Bounded Batch line {line_number} has no custom_id")
        if custom_id in records:
            raise ValueError(f"Bounded Batch repeats custom_id {custom_id!r}")
        records[custom_id] = value
    return records


def _batch_response(item: dict[str, Any]) -> dict[str, Any]:
    response = item.get("response") or {}
    body = response.get("body") if isinstance(response, dict) else None
    if not isinstance(body, dict):
        raise ValueError("Bounded Batch member has no Responses body")
    return body


def _validate_batch_round(state: dict[str, Any], value: dict[str, Any]) -> None:
    if set(value) != BATCH_ROUND_KEYS:
        raise ValueError("Bounded Batch round has unsupported or missing fields")
    if value["schema_version"] != "astrowoof.bounded_natal.batch_round.v1":
        raise ValueError("Unsupported bounded Batch round schema")
    requests = value["requests"]
    if not isinstance(requests, list) or not requests or len(requests) > 6:
        raise ValueError("Bounded Batch round member inventory is invalid")
    if value["member_count"] != len(requests):
        raise ValueError("Bounded Batch round member count conflicts with inventory")
    custom_ids: list[str] = []
    maximum = 0
    for request in requests:
        if not isinstance(request, dict) or set(request) != BATCH_REQUEST_KEYS:
            raise ValueError("Bounded Batch request has unsupported or missing fields")
        pass_id = request["pass_id"]
        attempt = request["attempt_number"]
        if pass_id not in state["passes"] or not isinstance(attempt, int) or attempt < 1:
            raise ValueError("Bounded Batch request binding is invalid")
        if request["custom_id"] != f"{pass_id}:attempt-{attempt:03d}":
            raise ValueError("Bounded Batch custom_id conflicts with pass binding")
        if request["stage"] != value["stage"]:
            raise ValueError("Bounded Batch mixes stage authority in one round")
        if request["model"] != value["model"]:
            raise ValueError("Bounded Batch mixes model authority in one round")
        custom_ids.append(request["custom_id"])
        maximum += request["maximum_output_tokens"]
    if len(set(custom_ids)) != len(custom_ids):
        raise ValueError("Bounded Batch round repeats a member identity")
    if value["aggregate_maximum_output_tokens"] != maximum:
        raise ValueError("Bounded Batch aggregate output authority is invalid")


def _pending_batch_candidates(state: dict[str, Any]) -> list[tuple[str, int, str]]:
    candidates: list[tuple[str, int, str]] = []
    for pass_id in state["bounded"]["pass_ids"]:
        record = state["passes"][pass_id]
        if record["state"] == "PASS_QA_ACCEPTED":
            continue
        attempt = len(record["attempts"]) + 1
        if attempt > state["max_attempts"]:
            record["state"] = "FAILED_REQUIRES_REVIEW"
            continue
        stage = "authoring_initial" if attempt == 1 else "creative_retry"
        candidates.append((pass_id, attempt, stage))
    if not candidates:
        return []
    stage = candidates[0][2]
    return [candidate for candidate in candidates if candidate[2] == stage]


def _prepare_bounded_batch_round(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
) -> dict[str, Any] | None:
    candidates = _pending_batch_candidates(state)
    if not candidates:
        return None
    service = state.setdefault("batch_service", {
        "schema_version": "astrowoof.bounded_natal.batch_service.v1",
        "service_level": "batch", "rounds": [],
    })
    round_number = len(service["rounds"]) + 1
    round_root = run_dir / "bounded" / "batches" / f"round-{round_number:03d}"
    round_root.mkdir(parents=True, exist_ok=True)
    requests: list[dict[str, Any]] = []
    lines: list[str] = []
    builder = getattr(provider, "batch_request_body", None)
    if not callable(builder):
        raise ValueError("Bounded Batch provider cannot build pass requests")
    for pass_id, attempt, stage in candidates:
        packet = load_json(
            run_dir / state["bounded"]["pass_packets"][pass_id]["path"]
        )
        payload = _payload(state, run_dir, stage, pass_id)
        body = builder(
            stage=stage, payload=payload, attempt_number=attempt,
        )
        custom_id = f"{pass_id}:attempt-{attempt:03d}"
        lines.append(json.dumps({
            "custom_id": custom_id, "method": "POST",
            "url": "/v1/responses", "body": body,
        }, ensure_ascii=False, sort_keys=True))
        request = {
            "custom_id": custom_id, "pass_id": pass_id,
            "attempt_number": attempt, "stage": stage,
            "request_sha256": _digest(body),
            "packet_sha256": packet["packet_sha256"],
            "model": provider.model,
            "maximum_output_tokens": provider.maximum_output_tokens,
        }
        requests.append(request)
        state["passes"][pass_id]["attempts"].append({
            "attempt": attempt, "state": "BATCH_PREPARED", "accepted": False,
            "provider_metadata": None, "qa": None,
        })
        state["passes"][pass_id]["state"] = "BATCH_PREPARED"
    input_text = "\n".join(lines) + "\n"
    input_path = round_root / "batch-input.jsonl"
    input_path.write_text(input_text, encoding="utf-8")
    round_record = {
        "schema_version": "astrowoof.bounded_natal.batch_round.v1",
        "round_number": round_number, "state": "PREPARED",
        "stage": candidates[0][2], "model": provider.model,
        "created_at": utc_now(), "input_path": normalized_path(input_path),
        "input_sha256": hashlib.sha256(input_text.encode("utf-8")).hexdigest(),
        "member_count": len(requests), "requests": requests,
        "aggregate_maximum_output_tokens": (
            provider.maximum_output_tokens * len(requests)
        ),
        "aggregate_commitment_micro_usd": None,
        "input_file_id": None, "batch_id": None, "batch_status": None,
        "output_file_id": None, "error_file_id": None,
        "request_counts": None, "finished_at": None, "integrity_review": None,
        "cost_disposition": "no_provider_work_consumed",
    }
    service["rounds"].append(round_record)
    _validate_batch_round(state, round_record)
    return round_record


def _bounded_batch_authoring_cycle(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
    controller: SpendController | None,
    failure_injector: Callable[[str], None] | None = None,
) -> bool:
    """Advance at most one bounded Batch round; never poll in a tight loop."""
    service = state.setdefault("batch_service", {
        "schema_version": "astrowoof.bounded_natal.batch_service.v1",
        "service_level": "batch", "rounds": [],
    })
    round_record = next((
        item for item in service["rounds"]
        if item["state"] not in {"INGESTED", "FAILED", "REQUIRES_REVIEW"}
    ), None)
    if round_record is None:
        round_record = _prepare_bounded_batch_round(state, run_dir, provider)
        if round_record is None:
            return all(
                state["passes"][pass_id]["state"] == "PASS_QA_ACCEPTED"
                for pass_id in state["bounded"]["pass_ids"]
            )
        save_state(run_dir / "run.json", state)
    _validate_batch_round(state, round_record)
    transport = getattr(provider, "batch_transport", None)
    if transport is None:
        raise ValueError("Bounded Batch provider has no Batch transport")
    input_path = Path(round_record["input_path"])
    input_bytes = input_path.read_bytes()
    if not round_record["input_file_id"]:
        uploaded = transport.upload_jsonl(input_bytes, input_path.name)
        round_record["input_file_id"] = uploaded["id"]
        round_record["state"] = "UPLOADED"
        save_state(run_dir / "run.json", state)
        if failure_injector:
            failure_injector("after_bounded_batch_input_uploaded")
    batch_payload = {
        "input_file_id": round_record["input_file_id"],
        "endpoint": "/v1/responses", "completion_window": "24h",
        "metadata": {
            "workflow": "astrowoof_bounded_natal",
            "round": str(round_record["round_number"]),
        },
    }
    if not round_record["batch_id"]:
        before = created = None
        if controller:
            action_route = (
                f"{BOUNDED_ROUTE}:batch-round-{round_record['round_number']:03d}"
            )
            before, created = controller.callbacks(
                stage=round_record["stage"],
                route=action_route,
                model=provider.model, service_level="batch",
                maximum_output_tokens=round_record["aggregate_maximum_output_tokens"],
            )
            try:
                before({
                    "batch": batch_payload,
                    "input_sha256": round_record["input_sha256"],
                })
            finally:
                action = next((
                    item for item in controller.ledger["actions"]
                    if item["binding"]["route"] == action_route
                ), None)
                if action is not None:
                    round_record["aggregate_commitment_micro_usd"] = (
                        action["binding"]["commitment_micro_usd"]
                    )
                    save_state(run_dir / "run.json", state)
        try:
            batch = transport.create_batch(batch_payload)
        except Exception as exc:
            if controller:
                controller.mark_active_ambiguous(str(exc))
            raise
        if created:
            created(batch.get("id"), "batch")
        round_record["batch_id"] = batch["id"]
        round_record["batch_status"] = batch.get("status")
        round_record["state"] = "SUBMITTED"
        round_record["cost_disposition"] = (
            "provider_usage_unavailable_billing_reconciliation_pending"
        )
        save_state(run_dir / "run.json", state)
        if failure_injector:
            failure_injector("after_bounded_batch_provider_identity")
    else:
        route = f"{BOUNDED_ROUTE}:batch-round-{round_record['round_number']:03d}"
        action = next((
            item for item in ((state.get("spend_ledger") or {}).get("actions") or [])
            if item["binding"]["route"] == route
            and (item.get("provider") or {}).get("id") == round_record["batch_id"]
        ), None)
        if controller and action:
            controller.local.active_action = action["action_id"]
        batch = transport.retrieve_batch(round_record["batch_id"])
    if batch.get("id") != round_record["batch_id"]:
        round_record["state"] = "REQUIRES_REVIEW"
        save_state(run_dir / "run.json", state)
        raise ValueError("Bounded Batch provider identity conflict")
    status = str(batch.get("status") or "")
    round_record["batch_status"] = status
    round_record["request_counts"] = batch.get("request_counts")
    round_record["output_file_id"] = batch.get("output_file_id")
    round_record["error_file_id"] = batch.get("error_file_id")
    if status not in TERMINAL_BATCH_STATES:
        round_record["state"] = "PENDING"
        if controller:
            controller.mark_active_waiting()
        save_state(run_dir / "run.json", state)
        return False
    round_root = input_path.parent
    round_record["finished_at"] = utc_now()
    write_json_atomic(round_root / "batch-object.json", batch)
    if status != "completed":
        for request in round_record["requests"]:
            record = state["passes"][request["pass_id"]]
            attempt = record["attempts"][request["attempt_number"] - 1]
            report = {
                "schema_version": "astrowoof.bounded_natal.pass_validation.v1",
                "pass_id": request["pass_id"], "status": "fail",
                "errors": [f"provider_batch_{status}"],
            }
            attempt.update({
                "state": "PASS_QA_REJECTED", "accepted": False,
                "qa": {"accepted": False, "report": report},
            })
            record["state"] = "PASS_QA_REJECTED"
        round_record["state"] = "FAILED"
        round_record["cost_disposition"] = (
            "provider_usage_unavailable_billing_reconciliation_pending"
        )
        if controller:
            action = controller.active_action()
            action["reported"] = {
                "usage": None, "estimated_micro_usd": None,
                "cost_disposition": round_record["cost_disposition"],
            }
            action["state"] = "REPORTED"
        save_state(run_dir / "run.json", state)
        return False
    output_text = (
        transport.download_file(batch["output_file_id"])
        if batch.get("output_file_id") else ""
    )
    error_text = (
        transport.download_file(batch["error_file_id"])
        if batch.get("error_file_id") else ""
    )
    (round_root / "batch-output.jsonl").write_text(output_text, encoding="utf-8")
    (round_root / "batch-errors.jsonl").write_text(error_text, encoding="utf-8")
    if failure_injector:
        failure_injector("after_bounded_batch_files_durable")
    outputs = _batch_jsonl(output_text)
    errors = _batch_jsonl(error_text)
    expected = [item["custom_id"] for item in round_record["requests"]]
    if set(outputs) & set(errors) or set(outputs) | set(errors) != set(expected):
        round_record["state"] = "REQUIRES_REVIEW"
        state["status"] = "FINAL_QA_REQUIRES_REVIEW"
        save_state(run_dir / "run.json", state)
        raise ValueError("Bounded Batch member inventory conflict")
    estimated_total = 0.0
    usage_complete = True
    for request in round_record["requests"]:
        pass_id = request["pass_id"]
        record = state["passes"][pass_id]
        attempt = record["attempts"][request["attempt_number"] - 1]
        packet = load_json(
            run_dir / state["bounded"]["pass_packets"][pass_id]["path"]
        )
        item = outputs.get(request["custom_id"])
        if item is None:
            usage_complete = False
            report = {
                "schema_version": "astrowoof.bounded_natal.pass_validation.v1",
                "pass_id": pass_id, "status": "fail",
                "errors": ["provider_batch_member_failed"],
            }
            hydrated = None
            metadata = {"provider": "openai", "service_level": "batch",
                        "batch_id": round_record["batch_id"],
                        "custom_id": request["custom_id"], "usage": {}}
        else:
            response = _batch_response(item)
            usage = normalized_usage(response)
            member_usage_reported = isinstance(response.get("usage"), dict)
            usage_complete = usage_complete and member_usage_reported
            estimate = batch_estimated_cost(request["model"], usage)
            if estimate:
                estimated_total += float(estimate["estimated_amount"])
            metadata = {
                "provider": "openai", "service_level": "batch",
                "batch_id": round_record["batch_id"],
                "custom_id": request["custom_id"], "response_id": response.get("id"),
                "response_status": response.get("status"), "model": response.get("model") or request["model"],
                "usage": usage, "estimated_cost": estimate,
            }
            try:
                editorial = json.loads(response_output_text(response))
                hydrated = provider.hydrate_batch_member(editorial, packet)
                report = _pass_result_report(hydrated, packet)
            except Exception as exc:
                hydrated = None
                report = {
                    "schema_version": "astrowoof.bounded_natal.pass_validation.v1",
                    "pass_id": pass_id, "status": "fail",
                    "errors": [f"output_invalid:{type(exc).__name__}"],
                }
        accepted = report["status"] == "pass"
        result_root = run_dir / "bounded" / "final" / "passes"
        result_root.mkdir(parents=True, exist_ok=True)
        if hydrated is not None:
            write_json_atomic(result_root / f"{pass_id}.json", hydrated)
        write_json_atomic(result_root / f"{pass_id}.validation.json", report)
        attempt.update({
            "state": "PASS_QA_ACCEPTED" if accepted else "PASS_QA_REJECTED",
            "accepted": accepted, "provider_metadata": metadata,
            "qa": {"accepted": accepted, "report": report},
        })
        record["state"] = attempt["state"]
        if accepted:
            record["accepted_attempt"] = request["attempt_number"]
            record["accepted_workspace"] = normalized_path(result_root / f"{pass_id}.json")
            if pass_id not in state["bounded"]["completed_pass_ids"]:
                state["bounded"]["completed_pass_ids"].append(pass_id)
    round_record["state"] = "INGESTED"
    round_record["cost_disposition"] = (
        "provider_usage_reported" if usage_complete
        else "provider_usage_unavailable_billing_reconciliation_pending"
    )
    if controller and usage_complete:
        controller.settle_active({
            "estimated_cost": {"currency": "USD", "estimated_amount": estimated_total}
        })
    elif controller:
        action = controller.active_action()
        action["reported"] = {
            "usage": None, "estimated_micro_usd": None,
            "cost_disposition": round_record["cost_disposition"],
        }
        action["state"] = "REPORTED"
    save_state(run_dir / "run.json", state)
    if failure_injector:
        failure_injector("after_bounded_batch_member_ingestion")
    return all(
        state["passes"][pass_id]["state"] == "PASS_QA_ACCEPTED"
        for pass_id in state["bounded"]["pass_ids"]
    )


def _prepare_bounded_interactive_initial_wave(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
) -> dict[str, Any] | None:
    stored = state.get("initial_authoring_wave")
    if isinstance(stored, dict):
        return stored
    pass_ids = state["bounded"]["pass_ids"]
    if len(pass_ids) != 6 or any(state["passes"][item]["attempts"] for item in pass_ids):
        return None
    builder = getattr(provider, "interactive_request_body", None)
    if not callable(builder):
        raise ValueError("Bounded provider cannot build interactive pass requests")
    ledger = state.get("spend_ledger")
    if not isinstance(ledger, dict):
        raise ValueError("Bounded OpenAI wave requires a spend ledger")
    basis_revision = int(state.get("state_revision") or 0)
    profile_sha256 = spend_profile_digest(state.get("authoring_profile"))
    members: list[InitialWaveMemberSpec] = []
    requests: dict[str, dict[str, Any]] = {}
    for pass_number, pass_id in enumerate(pass_ids, 1):
        payload = _payload(state, run_dir, "authoring_initial", pass_id)
        body = builder(stage="authoring_initial", payload=payload, attempt_number=1)
        request_sha256 = spend_digest(body)
        commitment = conservative_commitment_micros(
            model=provider.model,
            input_tokens=estimated_text_tokens(json.dumps(
                body, ensure_ascii=False, separators=(",", ":"),
            )), maximum_output_tokens=provider.maximum_output_tokens,
            service_level="interactive",
        )
        binding = action_binding(
            run_id=state["run_id"], profile_sha256=profile_sha256,
            prepared_state_revision=basis_revision,
            stage="authoring_initial",
            route=f"{BOUNDED_ROUTE}:{pass_id}:attempt-001",
            request_sha256=request_sha256, model=provider.model,
            service_level="interactive",
            maximum_output_tokens=provider.maximum_output_tokens,
            commitment_micro_usd=commitment,
            price_book_version=PRICE_BOOK_VERSION,
        )
        action = prepare_action(ledger, binding)
        members.append(InitialWaveMemberSpec(
            action_id=action["action_id"], binding=binding,
            pass_id=pass_id, pass_number=pass_number,
        ))
        attempt_root = run_dir / "bounded" / "provider" / (
            f"{BOUNDED_ROUTE}:{pass_id}:attempt-001".replace(":", "_")
        )
        request_path = attempt_root / "openai-request.json"
        write_json_atomic(request_path, body)
        state["passes"][pass_id]["attempts"].append({
            "attempt": 1, "state": "AWAITING_SPEND_AUTHORIZATION",
            "accepted": False, "provider_metadata": None, "qa": None,
            "paid_action_id": action["action_id"],
        })
        state["passes"][pass_id]["state"] = "AWAITING_SPEND_AUTHORIZATION"
        requests[action["action_id"]] = {
            "request_path": normalized_path(request_path),
            "request_sha256": request_sha256, "pass_id": pass_id,
            "attempt_root": normalized_path(attempt_root),
        }
    aggregate = sum(member.binding["commitment_micro_usd"] for member in members)
    policy = ledger["policy"]
    if aggregate > policy["run_ceiling_micro_usd"] or aggregate > policy[
        "stage_ceilings_micro_usd"
    ]["authoring_initial"]:
        for member in members:
            action = next(item for item in ledger["actions"]
                          if item["action_id"] == member.action_id)
            action["state"] = "BUDGET_EXHAUSTED"
            state["passes"][member.pass_id]["state"] = "BUDGET_EXHAUSTED"
            state["passes"][member.pass_id]["attempts"][-1]["state"] = "BUDGET_EXHAUSTED"
        persist_state(run_dir / "run.json", state)
        raise BudgetExhausted(
            "Complete bounded initial wave exceeds frozen spend ceiling",
            action=next(item for item in ledger["actions"]
                        if item["action_id"] == members[0].action_id),
        )
    assignment_sha256 = str(state["bounded"]["assignment_sha256"])
    wave = build_initial_wave(
        run_id=state["run_id"], route_family="bounded_natal",
        route_contract=BOUNDED_RUN_CONTRACT,
        assignment_sha256=assignment_sha256,
        profile_sha256=profile_sha256,
        preparation_basis_revision=basis_revision, members=members,
    )
    state["initial_authoring_wave"] = {
        **wave, "state": "AWAITING_SPEND_AUTHORIZATION", "requests": requests,
    }
    write_json_atomic(
        run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
        build_initial_wave_binding_bundle(
            wave, [member.binding for member in members],
        ),
    )
    save_state(run_dir / "run.json", state)
    return state["initial_authoring_wave"]


def _authorize_bounded_interactive_initial_wave(
    state: dict[str, Any], run_dir: Path, envelope: dict[str, Any],
    documents: list[dict[str, Any]],
) -> None:
    stored = state["initial_authoring_wave"]
    wave = {key: value for key, value in stored.items()
            if key not in {"state", "requests"}}
    preflight_wave_authorization(wave, envelope, documents)
    candidate = deepcopy(state["spend_ledger"])
    for document in documents:
        authorize_action(candidate, document)
    state["spend_ledger"] = candidate
    stored["authorization"] = deepcopy(envelope)
    stored["state"] = "AUTHORIZED"
    save_state(run_dir / "run.json", state)


def _validate_stored_bounded_initial_wave(
    state: dict[str, Any], run_dir: Path,
) -> dict[str, Any]:
    """Prove the stored bounded wave, bundle, requests, ledger, and passes join."""
    stored = state.get("initial_authoring_wave")
    if not isinstance(stored, dict):
        raise InitialWaveError("initial_wave_lineage_unjoinable", "Stored wave is absent")
    try:
        excluded = {
            "state", "requests", "authorization", "result",
            "constrained_submission_intent",
        }
        wave = {key: value for key, value in stored.items() if key not in excluded}
        validate_initial_wave(wave)
        if wave.get("route_family") != "bounded_natal":
            raise InitialWaveError("route_mismatch", "Stored wave is not bounded Natal")
        bundle = load_json(run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME)
        validate_initial_wave_binding_bundle_against_wave(bundle, wave)
        member_ids = [item["action_id"] for item in wave["ordered_members"]]
        requests = stored.get("requests")
        if not isinstance(requests, dict) or set(requests) != set(member_ids):
            raise InitialWaveError("member_inventory_mismatch", "Wave requests do not join")
        ledger = (state.get("spend_ledger") or {}).get("actions", [])
        for member, bundle_member in zip(
            wave["ordered_members"], bundle["ordered_members"], strict=True,
        ):
            matches = [
                item for item in ledger
                if isinstance(item, dict) and item.get("action_id") == member["action_id"]
            ]
            if len(matches) != 1 or matches[0].get("binding") != bundle_member["binding"]:
                raise InitialWaveError("binding_mismatch", "Wave ledger does not join")
            request = requests[member["action_id"]]
            request_path = Path(str(request.get("request_path") or ""))
            if (
                request.get("request_sha256") != member["request_sha256"]
                or not request_path.is_file()
                or spend_digest(load_json(request_path)) != member["request_sha256"]
            ):
                raise InitialWaveError("digest_mismatch", "Wave request bytes do not join")
            pass_record = (state.get("passes") or {}).get(member["pass_id"])
            attempts = pass_record.get("attempts", []) if isinstance(pass_record, dict) else []
            if not any(
                isinstance(attempt, dict)
                and attempt.get("paid_action_id") == member["action_id"]
                for attempt in attempts
            ):
                raise InitialWaveError(
                    "member_inventory_mismatch", "Wave pass attempt is absent",
                )
        return stored
    except (InitialWaveError, KeyError, TypeError, ValueError, FileNotFoundError) as exc:
        raise InitialWaveError(
            "initial_wave_lineage_unjoinable",
            "Stored bounded initial-wave evidence cannot prove one exact wave",
            evidence_categories=("native_evidence_conflict",),
        ) from exc


def _execute_bounded_interactive_initial_wave(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
    event_emitter: ExecutionEventEmitter | None,
    constrained_intent_token: str,
    failure_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    stored = state["initial_authoring_wave"]
    if stored.get("state") != "SUBMITTING":
        raise InitialWaveError(
            "authorization_missing", "Bounded initial wave lacks durable submit intent",
        )
    intent = stored.get("constrained_submission_intent") or {}
    if intent.get("token_sha256") != hashlib.sha256(
        constrained_intent_token.encode("utf-8")
    ).hexdigest():
        raise InitialWaveError(
            "provider_submission_ambiguous", "Submission intent capability is absent",
        )
    wave = {key: value for key, value in stored.items()
            if key not in {
                "state", "requests", "authorization", "result",
                "constrained_submission_intent",
            }}
    documents = [next(
        action["authorization"] for action in state["spend_ledger"]["actions"]
        if action["action_id"] == member["action_id"]
    ) for member in wave["ordered_members"]]
    create = getattr(provider, "create_interactive_only", None)
    if not callable(create):
        raise ValueError("Bounded provider cannot create interactive Responses")
    mutation_lock = threading.Lock()

    def inject(point: str) -> None:
        if failure_injector is not None:
            failure_injector(point)

    pre_post_barrier = threading.Barrier(
        6,
        action=lambda: (
            inject("before_pre_post_snapshot"),
            write_workspace_snapshot(run_dir),
            inject("after_pre_post_snapshot"),
        ),
        timeout=20.0,
    )

    def action_for(action_id: str) -> dict[str, Any]:
        return next(item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == action_id)

    def submit(member: Mapping[str, Any], timeout: int) -> InitialWaveProviderCreateResult:
        request = stored["requests"][member["action_id"]]
        body = load_json(Path(request["request_path"]))
        if spend_digest(body) != member["request_sha256"]:
            raise InitialWaveError("request_digest_mismatch", "Bounded request changed")
        with mutation_lock:
            action = action_for(member["action_id"])
            if (action.get("provider") or {}).get("id"):
                return InitialWaveProviderCreateResult(
                    provider_id=action["provider"]["id"],
                    metadata={"resumed_from_durable_identity": True},
                )
            if action.get("state") != "SUBMITTING":
                raise RuntimeError(
                    f"bounded wave member is not submit-eligible: {action.get('state')}"
                )
        inject(f"after_submitting:{member['action_id']}")
        pre_post_barrier.wait()
        inject(f"before_provider_create:{member['action_id']}")
        response, attempts = create(
            body=body, idempotency_material=member["action_id"],
            timeout_seconds=float(timeout),
        )
        inject(f"after_provider_create_before_identity:{member['action_id']}")
        return InitialWaveProviderCreateResult(
            provider_id=response["id"], metadata={
                "status": response.get("status"),
                "create_transport_attempts": attempts,
            },
        )

    def persist(member: Mapping[str, Any], outcome: Mapping[str, Any]) -> None:
        from .lifecycle import _exclusive_lifecycle_lock
        with _exclusive_lifecycle_lock(run_dir), mutation_lock:
            persisted_revision = int(
                load_json(run_dir / "run.json").get("state_revision") or 0
            )
            if persisted_revision != int(state.get("state_revision") or 0):
                raise AmbiguousProviderSubmission(
                    "Bounded initial-wave state changed before identity persistence",
                    action=action_for(member["action_id"]),
                )
            action = action_for(member["action_id"])
            record = state["passes"][member["pass_id"]]
            attempt = record["attempts"][-1]
            if outcome["outcome"] == "provider_bound":
                provider_id = outcome["provider"]["id"]
                if not action.get("provider"):
                    record_provider_id(action, provider_id=provider_id, kind="response")
                if not isinstance(action.get("provider_reconciliation"), dict):
                    action["provider_reconciliation"] = initial_timing(
                        recorded_at=utc_now().replace("+00:00", "Z"),
                        mechanism="response",
                    )
                action["state"] = "WAITING"
                marker = Path(stored["requests"][member["action_id"]]["attempt_root"])
                write_json_atomic(marker / "openai-background-response.json", {
                    "id": provider_id,
                    "status": (outcome.get("provider_create_metadata") or {}).get("status"),
                })
                attempt["state"] = "WAITING_FOR_RESPONSE"
                attempt["provider_metadata"] = outcome.get("provider_create_metadata")
                record["state"] = "WAITING_FOR_RESPONSE"
                if event_emitter:
                    event_emitter.emit("provider.identity_recorded", data={
                        "action_id": action["action_id"],
                        "provider_operation_id": provider_id,
                    }, correlation={"action_id": action["action_id"]})
                    event_emitter.emit("provider.waiting", data={
                        "action_id": action["action_id"],
                        "provider_operation_id": provider_id,
                    }, correlation={"action_id": action["action_id"]})
            elif outcome["outcome"] == "ambiguous_submission":
                mark_ambiguous(action, reason=outcome.get("reason") or "create ambiguous")
                attempt["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                record["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
            persist_state(run_dir / "run.json", state)
            write_workspace_snapshot(run_dir)
            inject(f"after_identity_checkpoint:{member['action_id']}")

    result = execute_initial_wave_creates(
        wave, authorization=stored["authorization"],
        member_authorizations=documents, submit=submit,
        persist_member_outcome=persist,
    )
    stored["state"] = "DETACHED" if result["outcome"] == "detached_provider_pending" else "FAILED"
    stored["result"] = result
    save_state(run_dir / "run.json", state)
    inject("after_final_wave_snapshot")
    return result


def resume_bounded_run(
    run_dir: Path,
    *,
    provider: BoundedLifecycleProvider | None = None,
    authorizations: list[dict[str, Any]] | None = None,
    initial_wave_authorization: dict[str, Any] | None = None,
    external_authority_request: dict[str, Any] | None = None,
    external_authority_grant: dict[str, Any] | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
    consumer_id: str = "bounded-worker",
    reconciliation_only: bool = False,
    _failure_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Advance a bounded run to its next durable pause or terminal checkpoint."""
    provider = provider or FakeBoundedLifecycleProvider()
    run_dir = run_dir.resolve()
    run_json = run_dir / "run.json"
    state = load_json(run_json)
    bind_logging_context(run_id=state.get("run_id"), current_state=state.get("status"))
    logger.info(
        "bounded_run_resume_start state_revision=%s reconciliation_only=%s "
        "authorization_count=%s",
        state.get("state_revision"), reconciliation_only, len(authorizations or []),
    )
    if state.get("route_contract") == LEGACY_BOUNDED_RUN_CONTRACT:
        raise ValueError("legacy_bounded_topology_unsupported")
    if state.get("route_contract") != BOUNDED_RUN_CONTRACT:
        raise ValueError("Run is not a supported bounded-Natal lifecycle")
    legacy_denial_present = any(
        item.get("state") == "DENIED_PROVIDERLESS"
        and not (item.get("negative_authorization") or {}).get("run_transition")
        for item in (state.get("spend_ledger") or {}).get("actions", [])
    )
    if legacy_denial_present or isinstance(
        state.get("required_denial_reconciliation"), dict
    ):
        from .lifecycle import reconcile_required_providerless_denial
        state = reconcile_required_providerless_denial(run_dir)
    else:
        validate_workspace_snapshot(run_dir, state)
    if (state.get("terminal_transition") or {}).get("outcome") == "terminalized":
        return state
    if state.get("provider") != provider.name:
        raise ValueError("Resume provider does not match the frozen run provider")
    if initial_wave_authorization is not None:
        logger.warning("bounded_external_authority_refused reason=legacy_envelope")
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.refused", data={
                    "reason_code": "aggregate_grant_required",
                    "category": "legacy_envelope", "selected_command": "none",
                    "action_count": len(authorizations or []),
                }, correlation={"native_run_id": str(state.get("run_id") or "")},
                severity="warning",
            )
        raise InitialWaveError(
            "aggregate_grant_required",
            "Legacy bounded initial-wave authority cannot authorize provider create",
        )
    if bool(external_authority_request) != bool(external_authority_grant):
        logger.warning("bounded_external_authority_refused reason=partial_pair")
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.refused", data={
                    "reason_code": "partial_authorization",
                    "category": "partial_request_grant_pair",
                    "selected_command": "none",
                    "action_count": len(authorizations or []),
                }, correlation={"native_run_id": str(state.get("run_id") or "")},
                severity="warning",
            )
        raise InitialWaveError(
            "partial_authorization", "External request and grant are required together",
        )
    if external_authority_request is not None:
        from .external_authority import (
            read_external_authority_request,
            validate_external_authority_grant,
        )
        from .lifecycle import _exclusive_lifecycle_lock

        if len(authorizations or []) != 6:
            raise InitialWaveError(
                "partial_authorization", "Bounded initial wave requires six authorizations",
            )
        token = os.urandom(32).hex()
        logger.info(
            "bounded_external_authority_fence_start request=%s grant=%s actions=%s",
            external_authority_request.get("external_authority_request_sha256"),
            external_authority_grant.get("grant_sha256"), len(authorizations or []),
        )
        with _exclusive_lifecycle_lock(run_dir):
            state = load_json(run_json)
            validate_workspace_snapshot(run_dir, state)
            try:
                current = read_external_authority_request(
                    run_dir,
                    observation=external_authority_request.get("observation"),
                )
            except InitialWaveError as exc:
                if event_emitter is not None:
                    event_emitter.emit(
                        "external_authority.refused", data={
                            "reason_code": exc.reason_code,
                            "category": "request_mismatch",
                            "selected_command": "none",
                            "action_count": len(
                                external_authority_request.get(
                                    "ordered_action_ids"
                                ) or []
                            ),
                        }, correlation={
                            "native_run_id": external_authority_request.get("run_id")
                        }, severity="warning",
                    )
                raise
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.request_selected", data={
                        "request_sha256": current[
                            "external_authority_request_sha256"
                        ], "request_kind": current["request_kind"],
                        "action_count": current["action_count"],
                        "selected_command": "bounded_initial_wave_create",
                    }, correlation={"native_run_id": current["run_id"]},
                )
            if current != external_authority_request:
                if event_emitter is not None:
                    event_emitter.emit(
                        "external_authority.refused", data={
                            "reason_code": "stale_observation",
                            "category": "request_mismatch",
                            "selected_command": "none",
                            "action_count": current["action_count"],
                        }, correlation={"native_run_id": current["run_id"]},
                        severity="warning",
                    )
                raise InitialWaveError(
                    "stale_observation", "External-authority request is not current",
                )
            try:
                validate_external_authority_grant(
                    current, external_authority_grant, authorizations or [],
                )
            except InitialWaveError as exc:
                if event_emitter is not None:
                    event_emitter.emit(
                        "external_authority.refused", data={
                            "reason_code": exc.reason_code,
                            "category": "grant_validation",
                            "selected_command": "none",
                            "action_count": current["action_count"],
                        }, correlation={"native_run_id": current["run_id"]},
                        severity="warning",
                    )
                raise
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.fence_validated", data={
                        "request_sha256": current[
                            "external_authority_request_sha256"
                        ], "grant_sha256": external_authority_grant["grant_sha256"],
                        "action_count": current["action_count"],
                    }, correlation={"native_run_id": current["run_id"]},
                )
            if _failure_injector is not None:
                _failure_injector("after_request_and_grant_validation")
            if (
                current["request_kind"] != "initial_wave_admission"
                or (current.get("initial_wave") or {}).get("route_contract")
                != BOUNDED_RUN_CONTRACT
            ):
                raise InitialWaveError(
                    "unsupported_contract", "Grant is not for a bounded initial wave",
                )
            stored = state.get("initial_authoring_wave")
            if not isinstance(stored, dict) or stored.get("state") != (
                "AWAITING_SPEND_AUTHORIZATION"
            ):
                raise InitialWaveError(
                    "request_unavailable", "Bounded initial wave is no longer admissible",
                )
            wave = {key: value for key, value in stored.items()
                    if key not in {
                        "state", "requests", "authorization", "result",
                        "constrained_submission_intent",
                    }}
            envelope = build_wave_authorization(
                wave, authorizations or [],
                reservation_set_reference=external_authority_grant["api_decision_id"],
                issuer=external_authority_grant["issuer"],
                authorized_at=external_authority_grant["issued_at"],
            )
            preflight_wave_authorization(wave, envelope, authorizations or [])
            candidate = deepcopy(state["spend_ledger"])
            for document in authorizations or []:
                authorize_action(candidate, document)
            for action_id in current["ordered_action_ids"]:
                action = next(
                    item for item in candidate["actions"]
                    if item["action_id"] == action_id
                )
                begin_submission(
                    action,
                    consumer_id=(
                        f"external-grant:{external_authority_grant['api_decision_id']}"
                    ),
                    state_revision=int(state.get("state_revision") or 0),
                )
            state["spend_ledger"] = candidate
            stored["authorization"] = envelope
            stored["state"] = "SUBMITTING"
            stored["constrained_submission_intent"] = {
                "external_authority_request_sha256": current[
                    "external_authority_request_sha256"
                ],
                "grant_sha256": external_authority_grant["grant_sha256"],
                "ordered_action_ids": list(current["ordered_action_ids"]),
                "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
                "created_at": utc_now(),
            }
            if _failure_injector is not None:
                _failure_injector("before_durable_pre_submit_intent")
            save_state(run_json, state)
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.intent_committed", data={
                        "request_sha256": current[
                            "external_authority_request_sha256"
                        ], "grant_sha256": external_authority_grant["grant_sha256"],
                        "action_count": current["action_count"],
                        "state_revision": state["state_revision"],
                    }, correlation={"native_run_id": current["run_id"]},
                )
            logger.info(
                "bounded_external_authority_intent_committed request=%s actions=%s revision=%s",
                current["external_authority_request_sha256"],
                len(current["ordered_action_ids"]), state.get("state_revision"),
            )
        if _failure_injector is not None:
            _failure_injector("after_durable_pre_submit_intent")
        logger.info(
            "bounded_external_authority_provider_io_start request=%s actions=%s",
            current["external_authority_request_sha256"],
            len(current["ordered_action_ids"]),
        )
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.provider_create_permitted", data={
                    "request_sha256": current["external_authority_request_sha256"],
                    "action_count": current["action_count"],
                    "selected_command": "bounded_initial_wave_create",
                }, correlation={"native_run_id": current["run_id"]},
            )
        _execute_bounded_interactive_initial_wave(
            state, run_dir, provider, event_emitter, token, _failure_injector,
        )
        return state
    elif is_active_initial_wave(state.get("initial_authoring_wave")):
        logger.warning(
            "bounded_external_authority_refused reason=aggregate_grant_required wave_state=%s",
            state["initial_authoring_wave"].get("state"),
        )
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.refused", data={
                    "reason_code": "aggregate_grant_required",
                    "category": "generic_resume_forbidden",
                    "selected_command": "none", "action_count": 6,
                }, correlation={"native_run_id": str(state.get("run_id") or "")},
                severity="warning",
            )
        raise InitialWaveError(
            "aggregate_grant_required",
            "Stored bounded initial wave requires its exact request and aggregate grant",
        )
    if authorizations and initial_wave_authorization is None:
        if external_authority_request is None:
            apply_spend_authorizations(state, authorizations)
            save_state(run_json, state)
    if event_emitter:
        event_emitter.emit("run.resumed", data={"state_revision": state["state_revision"]})
    state_lock = threading.Lock()
    controller = SpendController(
        state=state, run_json=run_json, state_lock=state_lock,
        consumer_id=consumer_id, event_emitter=event_emitter,
        reconciliation_only=reconciliation_only,
    ) if provider.paid else None

    prior_local_lifecycle: dict[str, Any] | None = None
    if not reconciliation_only:
        from .post_fan_in_contracts import inspect_post_fan_in_lifecycle

        candidate_local_lifecycle = inspect_post_fan_in_lifecycle(
            run_dir,
            observed_at=datetime.now(timezone.utc).replace(
                microsecond=0
            ).isoformat().replace("+00:00", "Z"),
            native_exclusive_access="declared",
            event_emitter=event_emitter,
        )
        if candidate_local_lifecycle["temporal_decision"]["selected_command"] == (
            "ordinary_resume"
        ):
            prior_local_lifecycle = candidate_local_lifecycle

    def seal_local_progress() -> None:
        nonlocal prior_local_lifecycle, state
        if prior_local_lifecycle is None:
            return
        from .post_fan_in_contracts import commit_local_work_progress

        successor = commit_local_work_progress(
            run_dir, prior=prior_local_lifecycle,
            observed_at=datetime.now(timezone.utc).replace(
                microsecond=0
            ).isoformat().replace("+00:00", "Z"),
            event_emitter=event_emitter,
        )
        prior_local_lifecycle = (
            successor
            if successor["temporal_decision"]["selected_command"]
            == "ordinary_resume"
            else None
        )
        durable = load_json(run_json)
        state.clear()
        state.update(durable)

    try:
        with checkpoint_spend_boundary(
            run_json, state, on_quiescent_checkpoint=seal_local_progress,
        ):
            bounded = state["bounded"]
            final_dir = run_dir / "bounded" / "final"
            final_dir.mkdir(parents=True, exist_ok=True)
            pass_results_dir = final_dir / "passes"
            pass_results_dir.mkdir(exist_ok=True)
            if provider.service_level == "batch":
                while True:
                    complete = _bounded_batch_authoring_cycle(
                        state, run_dir, provider, controller, _failure_injector
                    )
                    if complete:
                        for stage in ("authoring_initial", "creative_retry"):
                            if any(
                                attempt["attempt"] == (1 if stage == "authoring_initial" else 2)
                                for record in state["passes"].values()
                                for attempt in record["attempts"]
                            ) and stage not in bounded["completed_stages"]:
                                bounded["completed_stages"].append(stage)
                        save_state(run_json, state)
                        break
                    latest = state["batch_service"]["rounds"][-1]
                    if latest["state"] in {"PENDING", "REQUIRES_REVIEW"}:
                        return state
                    # A terminal round with rejected members immediately prepares
                    # the next pass-local retry round and reaches its authorization.
            else:
                wave_state = (state.get("initial_authoring_wave") or {}).get("state")
                if (
                    provider.paid
                    and callable(getattr(provider, "interactive_request_body", None))
                    and wave_state is None
                ):
                    wave = _prepare_bounded_interactive_initial_wave(
                        state, run_dir, provider,
                    )
                    if wave is not None:
                        return state
                for pass_id in bounded["pass_ids"]:
                    pass_record = state["passes"][pass_id]
                    if pass_record["state"] == "PASS_QA_ACCEPTED":
                        continue
                    packet = load_json(
                        run_dir / bounded["pass_packets"][pass_id]["path"]
                    )
                    while len(pass_record["attempts"]) < state["max_attempts"] or (
                        pass_record["attempts"]
                        and pass_record["attempts"][-1]["state"]
                        == "WAITING_FOR_RESPONSE"
                    ):
                        interrupted = (
                            pass_record["attempts"][-1]
                            if pass_record["attempts"]
                            and pass_record["attempts"][-1]["state"]
                            == "WAITING_FOR_RESPONSE"
                            else None
                        )
                        attempt = (
                            interrupted["attempt"] if interrupted
                            else len(pass_record["attempts"]) + 1
                        )
                        stage = "authoring_initial" if attempt == 1 else "creative_retry"
                        cards, metadata = _execute_stage(
                            state, run_dir, provider, stage, attempt, controller, pass_id
                        )
                        if _failure_injector:
                            _failure_injector(
                                "after_authoring_provider_result"
                                if attempt == 1 else "after_creative_retry_provider_result"
                            )
                        report = _pass_result_report(cards, packet)
                        result_path = pass_results_dir / f"{pass_id}.json"
                        report_path = pass_results_dir / f"{pass_id}.validation.json"
                        write_json_atomic(result_path, cards)
                        write_json_atomic(report_path, report)
                        accepted = report["status"] == "pass"
                        completed_attempt = {
                            "attempt": attempt,
                            "state": "PASS_QA_ACCEPTED" if accepted else "PASS_QA_REJECTED",
                            "accepted": accepted,
                            "provider_metadata": metadata,
                            "qa": {"accepted": accepted, "report": report},
                        }
                        if interrupted is not None:
                            interrupted.update(completed_attempt)
                        else:
                            pass_record["attempts"].append(completed_attempt)
                        if accepted:
                            pass_record["state"] = "PASS_QA_ACCEPTED"
                            pass_record["accepted_attempt"] = attempt
                            pass_record["accepted_workspace"] = normalized_path(result_path)
                            if pass_id not in bounded["completed_pass_ids"]:
                                bounded["completed_pass_ids"].append(pass_id)
                            if stage not in bounded["completed_stages"]:
                                bounded["completed_stages"].append(stage)
                        elif attempt == state["max_attempts"]:
                            pass_record["state"] = "FAILED_REQUIRES_REVIEW"
                        save_state(run_json, state)
                        if _failure_injector:
                            _failure_injector(
                                "after_authoring_checkpoint"
                                if attempt == 1 else "after_creative_retry_checkpoint"
                            )
                        if accepted:
                            break
                    if pass_record["state"] != "PASS_QA_ACCEPTED":
                        return state

            assembled_cards = _assemble_accepted_passes(state, run_dir)
            assembled_report = validate_bounded_final_cards(
                assembled_cards,
                load_json(run_dir / bounded["claim_deck"]["path"]),
                load_json(run_dir / bounded["authoring_packet"]["path"]),
            )
            write_json_atomic(final_dir / "cards.json", assembled_cards)
            write_json_atomic(final_dir / "validation-report.json", assembled_report)
            if assembled_report["status"] != "pass":
                state["status"] = "FINAL_QA_REQUIRES_REVIEW"
                save_state(run_json, state)
                return state

            optional = state["authoring_profile"]["optional_stages"]
            for stage in FINAL_STAGES:
                if stage in bounded["completed_stages"] or stage in bounded["skipped_stages"]:
                    continue
                if not optional[stage]:
                    logger.info(
                        "bounded_optional_stage_skipped stage=%s reason=profile_disabled",
                        stage,
                    )
                    bounded["skipped_stages"].append(stage)
                    save_state(run_json, state)
                    continue
                try:
                    result, metadata = _execute_stage(
                        state, run_dir, provider, stage, 1, controller
                    )
                except BudgetExhausted as exc:
                    if (
                        exc.action
                        and exc.action.get("state") == "SKIPPED_BUDGET_EXHAUSTED"
                    ):
                        logger.warning(
                            "bounded_optional_stage_skipped stage=%s reason=budget_exhausted",
                            stage,
                        )
                        bounded["skipped_stages"].append(stage)
                        save_state(run_json, state)
                        continue
                    raise
                if _failure_injector:
                    _failure_injector(f"after_{stage}_provider_result")
                if stage == "qualitative_critic":
                    write_json_atomic(final_dir / "critic.json", result)
                else:
                    report = validate_bounded_final_cards(
                        result,
                        load_json(run_dir / bounded["claim_deck"]["path"]),
                        load_json(run_dir / bounded["authoring_packet"]["path"]),
                    )
                    write_json_atomic(final_dir / f"{stage}-validation-report.json", report)
                    if report["status"] == "pass":
                        write_json_atomic(final_dir / "cards.json", result)
                bounded["completed_stages"].append(stage)
                logger.info(
                    "bounded_optional_stage_complete stage=%s provider_id=%s",
                    stage, metadata.get("response_id", metadata.get("id")),
                )
                bounded.setdefault("stage_metadata", {})[stage] = metadata
                save_state(run_json, state)
                if _failure_injector:
                    _failure_injector(f"after_{stage}_checkpoint")

            cards_path = final_dir / "cards.json"
            subject_id = state["passes"][bounded["pass_ids"][0]]["subject"]
            delivery = {
                "schema_version": BOUNDED_DELIVERY_CONTRACT,
                # Delivery v1 remains the stable bounded product contract; v2 is
                # the native authoring topology, not a new reader-facing product.
                "route": "bounded_natal.v1",
                "run_id": state["run_id"],
                "subject_id": next(iter(state["subjects"]), None) or subject_id,
                "cards": _artifact(cards_path, run_dir),
                "claim_deck": deepcopy(bounded["claim_deck"]),
                "authoring_packet": deepcopy(bounded["authoring_packet"]),
                "disposition_report": deepcopy(bounded["disposition_report"]),
                "input_contract": deepcopy(state["input_contract"]),
                "completed_stages": list(bounded["completed_stages"]),
                "skipped_stages": list(bounded["skipped_stages"]),
            }
            write_json_atomic(final_dir / "delivery.json", delivery)
            state["subjects"] = {subject_id: {
                "subject": subject_id, "state": "DELIVERY_COMPLETE",
                "deck": normalized_path(cards_path),
                "delivery": normalized_path(final_dir / "delivery.json"),
            }}
            bounded["stage"] = "DELIVERY_COMPLETE"
            logger.info(
                "bounded_delivery_complete subject_id=%s completed_stages=%s "
                "skipped_stages=%s",
                subject_id, bounded["completed_stages"], bounded["skipped_stages"],
            )
            save_state(run_json, state)
            if _failure_injector:
                _failure_injector("after_delivery_checkpoint")
            if event_emitter:
                _emit_artifact(event_emitter, "delivery", BOUNDED_DELIVERY_CONTRACT, final_dir / "delivery.json")
                event_emitter.emit("terminal.transitioned", data={
                    "outcome": "delivery_complete", "terminal_reason": "delivery_complete",
                })
            return state
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission) as exc:
        logger.warning(
            "bounded_run_detached state_revision=%s status=%s error_class=%s error=%s",
            state.get("state_revision"), state.get("status"), type(exc).__name__,
            sanitize_error_message(exc),
        )
        if event_emitter:
            event_emitter.emit("run.detached", data={
                "state_revision": state["state_revision"],
                "reason_code": state.get("status", "provider_boundary").lower(),
            })
        raise
    except Exception as exc:
        logger.exception(
            "bounded_run_failed state_revision=%s status=%s error_class=%s error=%s",
            state.get("state_revision"), state.get("status"), type(exc).__name__,
            sanitize_error_message(exc),
        )
        # Provider identity and any completed local mutations must share one
        # restorable checkpoint before the worker exits unexpectedly.
        save_state(run_json, state)
        raise


def run_bounded_authoring(
    run_dir: Path, artifacts: BoundedAuthoringArtifacts, **kwargs: Any
) -> dict[str, Any]:
    """Create and advance a bounded run with one provider instance."""
    provider = kwargs.pop("provider", None) or FakeBoundedLifecycleProvider()
    create_bounded_run(run_dir, artifacts, provider=provider, **{
        key: kwargs[key] for key in ("generation_profile", "event_emitter") if key in kwargs
    })
    return resume_bounded_run(run_dir, provider=provider, **{
        key: value for key, value in kwargs.items() if key != "generation_profile"
    })
