"""Bounded-Natal route over SBE's released lifecycle and spend contracts.

This module owns only bounded route sequencing. Durable persistence, workspace
integrity, paid-action authorization, lifecycle inspection, and closeout are the
same implementations used by exact-Natal authoring.
"""

from __future__ import annotations

import hashlib
import json
import threading
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

from .bounded_authoring import (
    BoundedAuthoringArtifacts,
    assert_provider_minimized,
    fake_author_bounded,
    validate_bounded_final_cards,
)
from .closure import (
    SCHEMA_VERSION,
    SNAPSHOT_SCHEMA,
    SpendController,
    apply_spend_authorizations,
    checkpoint_spend_boundary,
    load_json,
    normalized_path,
    persist_state,
    save_state,
    sha256_file,
    utc_now,
    validate_workspace_snapshot,
    write_json_atomic,
)
from .execution_events import ExecutionEventEmitter
from .spend import (
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
    BudgetExhausted,
    new_ledger,
    validate_policy,
)


BOUNDED_ROUTE = "bounded_natal.v1"
BOUNDED_RUN_CONTRACT = "astrowoof.bounded_natal.authoring_run.v1"
BOUNDED_DELIVERY_CONTRACT = "astrowoof.bounded_natal.delivery.v1"
FINAL_STAGES = ("polish", "qualitative_critic", "qualitative_candidate")


class BoundedLifecycleProvider(Protocol):
    name: str
    model: str
    service_level: str
    maximum_output_tokens: int
    paid: bool

    def execute(
        self,
        *,
        stage: str,
        route: str,
        payload: dict[str, Any],
        before_submit: Callable[[dict[str, Any]], None] | None,
        provider_created: Callable[[str | None, str], None] | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]: ...


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
    }
    for name, value in values.items():
        write_json_atomic(inputs / name, value)
    now = utc_now()
    subject = artifacts.authoring_packet["subject"]
    subject_id = str(subject.get("subject_id") or "bounded-subject")
    run_id = _digest({
        "route": BOUNDED_ROUTE,
        "logical_root": normalized_path(run_dir),
        "claim_deck_sha256": _digest(artifacts.claim_deck),
        "created_at": now,
    })
    pass_id = f"{subject_id}:bounded"
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
        "passes": {pass_id: {
            "pass_id": pass_id, "subject": subject_id, "pass_number": 1,
            "source_zip": normalized_path(inputs / "authoring-packet.json"),
            "source_sha256": sha256_file(inputs / "authoring-packet.json"),
            "state": "GENERATED", "attempts": [],
            "accepted_workspace": None, "accepted_attempt": None,
        }},
        "subjects": {},
        "bounded": {
            "stage": "AUTHORING", "pass_id": pass_id,
            "claim_deck": _artifact(inputs / "claim-deck.json", run_dir),
            "authoring_packet": _artifact(inputs / "authoring-packet.json", run_dir),
            "disposition_report": _artifact(inputs / "disposition-report.json", run_dir),
            "completed_stages": [], "skipped_stages": [],
        },
    }
    if provider.paid:
        state["spend_ledger"] = new_ledger(validate_policy(profile.get("spend_policy")))
    persist_state(run_dir / "run.json", state)
    save_state(run_dir / "run.json", state)
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
    return state


def _payload(state: dict[str, Any], run_dir: Path, stage: str) -> dict[str, Any]:
    packet = load_json(run_dir / state["bounded"]["authoring_packet"]["path"])
    payload: dict[str, Any] = {
        "route": BOUNDED_ROUTE,
        "stage": stage,
        "authoring_packet": packet,
    }
    cards = run_dir / "bounded" / "final" / "cards.json"
    if cards.is_file():
        payload["cards"] = load_json(cards)
    assert_provider_minimized(payload)
    return payload


def _execute_stage(
    state: dict[str, Any], run_dir: Path, provider: BoundedLifecycleProvider,
    stage: str, attempt: int, controller: SpendController | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    route = f"{BOUNDED_ROUTE}:{stage}:{attempt}"
    result_path = run_dir / "bounded" / "provider-results" / f"{stage}-{attempt}.json"
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
            payload=_payload(state, run_dir, stage),
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
            service_level=provider.service_level,
            maximum_output_tokens=provider.maximum_output_tokens,
        )
    try:
        result, metadata = provider.execute(
            stage=stage, route=route, payload=_payload(state, run_dir, stage),
            before_submit=before, provider_created=created,
        )
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission):
        raise
    except Exception as exc:
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


def resume_bounded_run(
    run_dir: Path,
    *,
    provider: BoundedLifecycleProvider | None = None,
    authorizations: list[dict[str, Any]] | None = None,
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
    if authorizations:
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

    try:
        with checkpoint_spend_boundary(run_json, state):
            bounded = state["bounded"]
            pass_record = state["passes"][bounded["pass_id"]]
            final_dir = run_dir / "bounded" / "final"
            final_dir.mkdir(parents=True, exist_ok=True)
            if pass_record["state"] != "PASS_QA_ACCEPTED":
                while len(pass_record["attempts"]) < state["max_attempts"]:
                    attempt = len(pass_record["attempts"]) + 1
                    stage = "authoring_initial" if attempt == 1 else "creative_retry"
                    cards, metadata = _execute_stage(
                        state, run_dir, provider, stage, attempt, controller
                    )
                    if _failure_injector:
                        _failure_injector(
                            "after_authoring_provider_result"
                            if attempt == 1 else "after_creative_retry_provider_result"
                        )
                    report = validate_bounded_final_cards(
                        cards,
                        load_json(run_dir / bounded["claim_deck"]["path"]),
                        load_json(run_dir / bounded["authoring_packet"]["path"]),
                    )
                    write_json_atomic(final_dir / "cards.json", cards)
                    write_json_atomic(final_dir / "validation-report.json", report)
                    accepted = report["status"] == "pass"
                    pass_record["attempts"].append({
                        "attempt": attempt,
                        "state": "PASS_QA_ACCEPTED" if accepted else "PASS_QA_REJECTED",
                        "accepted": accepted,
                        "provider_metadata": metadata,
                        "qa": {"accepted": accepted, "report": report},
                    })
                    if accepted:
                        pass_record["state"] = "PASS_QA_ACCEPTED"
                        pass_record["accepted_attempt"] = attempt
                        pass_record["accepted_workspace"] = normalized_path(final_dir)
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

            optional = state["authoring_profile"]["optional_stages"]
            for stage in FINAL_STAGES:
                if stage in bounded["completed_stages"] or stage in bounded["skipped_stages"]:
                    continue
                if not optional[stage]:
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
                bounded.setdefault("stage_metadata", {})[stage] = metadata
                save_state(run_json, state)
                if _failure_injector:
                    _failure_injector(f"after_{stage}_checkpoint")

            cards_path = final_dir / "cards.json"
            delivery = {
                "schema_version": BOUNDED_DELIVERY_CONTRACT,
                "route": BOUNDED_ROUTE,
                "run_id": state["run_id"],
                "subject_id": next(iter(state["subjects"]), None) or pass_record["subject"],
                "cards": _artifact(cards_path, run_dir),
                "claim_deck": deepcopy(bounded["claim_deck"]),
                "authoring_packet": deepcopy(bounded["authoring_packet"]),
                "disposition_report": deepcopy(bounded["disposition_report"]),
                "input_contract": deepcopy(state["input_contract"]),
                "completed_stages": list(bounded["completed_stages"]),
                "skipped_stages": list(bounded["skipped_stages"]),
            }
            write_json_atomic(final_dir / "delivery.json", delivery)
            subject_id = pass_record["subject"]
            state["subjects"] = {subject_id: {
                "subject": subject_id, "state": "DELIVERY_COMPLETE",
                "deck": normalized_path(cards_path),
                "delivery": normalized_path(final_dir / "delivery.json"),
            }}
            bounded["stage"] = "DELIVERY_COMPLETE"
            save_state(run_json, state)
            if _failure_injector:
                _failure_injector("after_delivery_checkpoint")
            if event_emitter:
                _emit_artifact(event_emitter, "delivery", BOUNDED_DELIVERY_CONTRACT, final_dir / "delivery.json")
                event_emitter.emit("terminal.transitioned", data={
                    "outcome": "delivery_complete", "terminal_reason": "delivery_complete",
                })
            return state
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission):
        if event_emitter:
            event_emitter.emit("run.detached", data={
                "state_revision": state["state_revision"],
                "reason_code": state.get("status", "provider_boundary").lower(),
            })
        raise
    except Exception:
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
