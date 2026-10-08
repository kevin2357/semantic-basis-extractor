"""Supported constrained external-authority v2 command."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from .. import __version__
from ..application_logging import (
    add_logging_arguments,
    bind_logging_context,
    configure_logging_from_args,
)
from ..closure import (
    OpenAIResponsesProvider,
    sha256_file,
    validate_workspace_snapshot,
)
from ..execution_events import ExecutionEventEmitter, JsonlEventSink, StdoutJsonlSink
from ..external_authority_v2 import build_no_grant_dispatch_result_v2
from ..bounded_lifecycle import (
    commit_bounded_initial_wave_v2_dispatch_intent,
    dispatch_bounded_initial_wave_v2_intent,
)
from ..bounded_provider import OpenAIBoundedLifecycleProvider
from ..initial_wave import InitialWaveError
from ..external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_prepared_create,
    build_external_authority_prepared_create_basis,
    build_external_authority_provider_dispatch_result_v5,
    build_external_authority_v2_command_result_v2,
    build_external_authority_v2_command_result_v3,
    build_external_authority_v2_command_result_v4,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    is_completed_external_authority_v2_intent_stale,
    resolve_external_authority_v2_request_payload,
)
from ..trace_observability import (
    log_cli_exit,
    log_decision_summary,
    log_native_state_summary,
)
from ..native_suspension_runtime import (
    CooperativeSuspensionPublished,
    NativeSuspensionControlObserver,
)


logger = logging.getLogger(__name__)


_BOUNDED_COMMAND_SCHEMA = "astrowoof.bounded_initial_wave_v2_command_result.v1"


def _canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _bounded_command_result(
    *, request: dict[str, Any], grant: dict[str, Any] | None,
    intent_result: dict[str, Any] | None, wave_result: dict[str, Any] | None,
    outcome: str, reason_code: str | None, native_mutation_performed: bool,
    provider_io_performed: bool, checkpoint_published: bool,
) -> dict[str, Any]:
    """Closed API-facing envelope for one bounded v2 command invocation."""
    body = {
        "schema_version": _BOUNDED_COMMAND_SCHEMA,
        "outcome": outcome,
        "reason_code": reason_code,
        "native_run_id": request["run_id"],
        "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "request_sha256": request["external_authority_request_sha256"],
        "grant_sha256": None if grant is None else grant["grant_sha256"],
        "api_decision_id": None if grant is None else grant["api_decision_id"],
        "request_kind": "initial_wave_admission",
        "ordering_semantics": "prepared_wave_semantic_member_order",
        "ordered_action_ids": list(request["ordered_action_ids"]),
        "initial_wave": request["initial_wave"],
        "intent_result": intent_result,
        "wave_result": wave_result,
        "native_mutation_performed": native_mutation_performed,
        "provider_io_performed": provider_io_performed,
        "checkpoint_published": checkpoint_published,
    }
    return _validate_bounded_command_result({
        **body, "result_sha256": _canonical_digest(body),
    })


def _validate_bounded_command_result(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "result_sha256", "outcome", "reason_code",
        "native_run_id", "checkpoint_basis_sha256", "request_sha256",
        "grant_sha256", "api_decision_id", "request_kind",
        "ordering_semantics", "ordered_action_ids", "initial_wave",
        "intent_result", "wave_result", "native_mutation_performed",
        "provider_io_performed", "checkpoint_published",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("bounded initial-wave command result fields are not exact")
    if (
        value.get("schema_version") != _BOUNDED_COMMAND_SCHEMA
        or value.get("outcome") not in {
            "pre_provider_refusal", "detached_provider_pending", "exact_replay",
            "ambiguous_custody_refusal",
        }
        or value.get("request_kind") != "initial_wave_admission"
        or value.get("ordering_semantics") != "prepared_wave_semantic_member_order"
        or not isinstance(value.get("native_run_id"), str) or not value["native_run_id"]
        or any(
            not isinstance(value.get(key), str) or len(value[key]) != 64
            for key in ("checkpoint_basis_sha256", "request_sha256", "result_sha256")
        )
        or not isinstance(value.get("ordered_action_ids"), list)
        or len(value["ordered_action_ids"]) != 6
        or len(set(value["ordered_action_ids"])) != 6
        or not isinstance(value.get("initial_wave"), dict)
        or any(not isinstance(value.get(key), bool) for key in (
            "native_mutation_performed", "provider_io_performed", "checkpoint_published",
        ))
    ):
        raise ValueError("bounded initial-wave command result semantics are invalid")
    refusal = value["outcome"] == "pre_provider_refusal"
    if refusal and any(value[key] for key in (
        "native_mutation_performed", "provider_io_performed", "checkpoint_published",
    )):
        raise ValueError("pre-provider refusal must be nonmutating")
    if value["outcome"] == "exact_replay" and value["provider_io_performed"]:
        raise ValueError("bounded exact replay cannot perform provider I/O")
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    if value["result_sha256"] != _canonical_digest(body):
        raise ValueError("bounded initial-wave command result digest mismatch")
    return value


class _FakeBoundedInitialProvider:
    """Provider-free command double; never selected by production API inputs."""

    name = "openai"

    def create_interactive_only(self, *, body, idempotency_material, timeout_seconds):
        del body, timeout_seconds
        return {"id": f"fake-response-{idempotency_material}", "status": "queued"}, 1


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _outside_workspace(path: Path | None, run_dir: Path) -> None:
    if path is None:
        return
    resolved = path.resolve()
    try:
        resolved.relative_to(run_dir.resolve())
    except ValueError:
        return
    raise ValueError("Command output must be outside the native workspace")


def _render(value: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.write_text(rendered, encoding="utf-8")


def _run_bounded_initial_wave_v2(
    *, args: argparse.Namespace, run_dir: Path, request: dict[str, Any],
    inspection: dict[str, Any], event_emitter: ExecutionEventEmitter | None,
) -> int:
    """Consume the bounded v2 pair and dispatch in this exact process only."""
    entry_state = _load(run_dir / "run.json")
    was_detached = (
        (entry_state.get("initial_authoring_wave") or {}).get("state") == "DETACHED"
    )
    if args.grant is None:
        result = _bounded_command_result(
            request=request, grant=None, intent_result=None, wave_result=None,
            outcome="pre_provider_refusal", reason_code="compatible_grant_required",
            native_mutation_performed=False, provider_io_performed=False,
            checkpoint_published=False,
        )
        _render(result, args.output)
        return 3
    grant = _load(args.grant)
    documents = [_load(path) for path in args.authorization]
    if args.provider not in {"openai", "fake"}:
        result = _bounded_command_result(
            request=request, grant=grant, intent_result=None, wave_result=None,
            outcome="pre_provider_refusal", reason_code="provider_required",
            native_mutation_performed=False, provider_io_performed=False,
            checkpoint_published=False,
        )
        _render(result, args.output)
        return 3
    try:
        intent_result = commit_bounded_initial_wave_v2_dispatch_intent(
            run_dir, request=request, inspection=inspection, grant=grant,
            authorization_documents=documents, event_emitter=event_emitter,
        )
    except (InitialWaveError, ValueError) as exc:
        result = _bounded_command_result(
            request=request, grant=grant, intent_result=None, wave_result=None,
            outcome="pre_provider_refusal",
            reason_code=getattr(exc, "reason_code", "authority_validation_failed"),
            native_mutation_performed=False, provider_io_performed=False,
            checkpoint_published=False,
        )
        _render(result, args.output)
        return 3

    if args.provider == "fake":
        provider = _FakeBoundedInitialProvider()
    else:
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            result = _bounded_command_result(
                request=request, grant=grant, intent_result=intent_result,
                wave_result=None, outcome="ambiguous_custody_refusal",
                reason_code="provider_capability_unavailable",
                native_mutation_performed=True, provider_io_performed=False,
                checkpoint_published=True,
            )
            _render(result, args.output)
            return 3
        binding = documents[0].get("binding") if documents else None
        if not isinstance(binding, dict):
            result = _bounded_command_result(
                request=request, grant=grant, intent_result=intent_result,
                wave_result=None, outcome="ambiguous_custody_refusal",
                reason_code="provider_configuration_invalid",
                native_mutation_performed=True, provider_io_performed=False,
                checkpoint_published=True,
            )
            _render(result, args.output)
            return 3
        provider = OpenAIBoundedLifecycleProvider(
            run_dir=run_dir, api_key=api_key, model=binding["model"],
            maximum_output_tokens=binding["maximum_output_tokens"],
            base_url=args.base_url, http_timeout_seconds=args.http_timeout_seconds,
            max_transport_retries=0,
        )
    try:
        wave_result = dispatch_bounded_initial_wave_v2_intent(
            run_dir,
            request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"], provider=provider,
            event_emitter=event_emitter,
        )
    except InitialWaveError as exc:
        result = _bounded_command_result(
            request=request, grant=grant, intent_result=intent_result,
            wave_result=None, outcome="ambiguous_custody_refusal",
            reason_code=exc.reason_code, native_mutation_performed=True,
            provider_io_performed=False, checkpoint_published=True,
        )
        _render(result, args.output)
        return 3
    replay = was_detached and wave_result.get("outcome") == "detached_provider_pending"
    result = _bounded_command_result(
        request=request, grant=grant, intent_result=intent_result,
        wave_result=wave_result,
        outcome="exact_replay" if replay else wave_result["outcome"],
        reason_code=None, native_mutation_performed=not replay,
        provider_io_performed=not replay, checkpoint_published=True,
    )
    _render(result, args.output)
    return 0 if result["outcome"] in {"detached_provider_pending", "exact_replay"} else 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Consume or inspect one exact external-authority v2 request.",
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--inspection", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--grant", type=Path)
    parser.add_argument("--authorization", action="append", type=Path, default=[])
    parser.add_argument("--provider", choices=("none", "openai", "fake"), default="none")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--base-url", default="https://api.openai.com/v1")
    parser.add_argument("--http-timeout-seconds", type=float, default=15.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--events-jsonl", type=Path)
    parser.add_argument("--events-stdout-jsonl", action="store_true")
    parser.add_argument("--supervision-envelope", type=Path)
    parser.add_argument("--suspension-control-root", type=Path)
    add_logging_arguments(parser)
    args = parser.parse_args(argv)
    configure_logging_from_args(args)
    run_dir = args.run_dir.resolve()
    _outside_workspace(args.output, run_dir)
    _outside_workspace(args.events_jsonl, run_dir)
    if args.events_jsonl is not None and args.events_stdout_jsonl:
        parser.error("choose only one event transport")
    if args.events_stdout_jsonl and args.output is None:
        parser.error("--events-stdout-jsonl requires --output")
    native_state = _load(run_dir / "run.json")
    if bool(args.supervision_envelope) != bool(args.suspension_control_root):
        parser.error(
            "--supervision-envelope and --suspension-control-root are an exact pair"
        )
    suspension_observer = None
    if args.supervision_envelope is not None:
        suspension_observer = NativeSuspensionControlObserver(
            envelope_path=args.supervision_envelope,
            control_root=args.suspension_control_root,
            observed_at=datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ).replace("+00:00", "Z"),
        )
    bind_logging_context(
        run_id=str(native_state.get("run_id") or "-"),
        current_state=str(native_state.get("status") or "-"),
    )
    validate_workspace_snapshot(run_dir, native_state)
    log_native_state_summary(logger, native_state, phase="command_entry")
    sink = None
    if args.events_stdout_jsonl:
        sink = StdoutJsonlSink()
    elif args.events_jsonl is not None:
        sink = JsonlEventSink(args.events_jsonl)
    event_emitter = (
        ExecutionEventEmitter(
            release=__version__, sink=sink,
            base_correlation={
                "native_run_id": str(native_state.get("run_id") or ""),
            },
        )
        if sink is not None else None
    )
    logger.info("command_start command=external_authority_v2 provider=%s", args.provider)
    inspection = _load(args.inspection)
    request = _load(args.request)

    if request.get("request_kind") == "initial_wave_admission":
        return _run_bounded_initial_wave_v2(
            args=args, run_dir=run_dir, request=request, inspection=inspection,
            event_emitter=event_emitter,
        )

    if args.grant is None:
        if args.authorization or args.provider != "none":
            parser.error("grant-free inspection accepts no authorization or provider")
        result = build_no_grant_dispatch_result_v2(inspection)
        logger.info(
            "command_complete command=external_authority_v2 outcome=%s provider_io=none",
            result["outcome"],
        )
        log_decision_summary(
            logger, result, command="external_authority_v2", operation="no_grant",
        )
        _render(result, args.output)
        log_cli_exit(
            logger, command="external_authority_v2", operation="no_grant",
            exit_code=3, outcome=result["outcome"],
            authoritative_transport="output_file" if args.output else "stdout_json",
        )
        return 3
    if args.provider != "openai":
        parser.error("provider-capable v2 execution requires --provider openai")
    if not args.authorization:
        parser.error("provider-capable v2 execution requires --authorization")
    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        parser.error(f"environment variable {args.api_key_env!r} is required")
    grant = _load(args.grant)
    documents = [_load(path) for path in args.authorization]
    try:
        intent_result = commit_external_authority_v2_dispatch_intent(
            run_dir, request=request, inspection=inspection, grant=grant,
            authorization_documents=documents,
            event_emitter=event_emitter,
            suspension_observer=suspension_observer,
        )
    except CooperativeSuspensionPublished as exc:
        command_result = exc.publication["command_result"]
        _render(command_result, args.output)
        log_cli_exit(
            logger, command="external_authority_v2",
            operation="cooperative_suspend", exit_code=0,
            outcome=command_result["outcome"],
            result_id=command_result["result_id"],
            receipt_id=command_result["receipt_id"],
            authoritative_transport="output_file" if args.output else "stdout_json",
        )
        return 0
    except ExternalAuthorityV2ExecutionError as exc:
        if (
            exc.reason_code == "action_state_or_custody_mismatch"
            and is_completed_external_authority_v2_intent_stale(
                native_state,
                run_dir,
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
            )
        ):
            # A fresh grant passed its fence, but an old completed intent still
            # owns the native singleton slot. Do not convert that native repair
            # requirement into a dispatch attempt with different identities.
            dispatch_result = build_external_authority_provider_dispatch_result_v5(
                outcome="pre_provider_refusal",
                reason_code="completed_intent_retirement_required",
                provider_io_disposition="not_attempted",
                grant_invocation_disposition="refused",
                run_id=native_state["run_id"],
                request_sha256=request["external_authority_request_sha256"],
                grant_sha256=grant["grant_sha256"],
                ordered_action_ids=request["ordered_action_ids"],
                provider_bound_action_ids=[],
                ambiguous_action_ids=[],
                refused_action_ids=request["ordered_action_ids"],
                provider_operation_ids=[],
                prepared_create_records=[],
                post_state_revision=int(native_state["state_revision"]),
                post_snapshot_sha256=sha256_file(
                    run_dir / "workspace-snapshot.json"
                ),
            )
            command_result = build_external_authority_v2_command_result_v4(
                dispatch_result=dispatch_result,
            )
            if event_emitter is not None:
                event_emitter.emit("external_authority.refused", data={
                    "reason_code": "completed_intent_retirement_required",
                    "category": "pre_provider_refusal",
                    "selected_command": "external_authority_v2_dispatch",
                    "action_count": len(request["ordered_action_ids"]),
                })
            logger.info(
                "provider_dispatch_classified outcome=pre_provider_refusal "
                "reason=completed_intent_retirement_required "
                "provider_io=not_attempted"
            )
            _render(command_result, args.output)
            log_cli_exit(
                logger, command="external_authority_v2",
                operation="constrained_dispatch", exit_code=3,
                outcome=dispatch_result["outcome"],
                authoritative_transport=(
                    "output_file" if args.output else "stdout_json"
                ),
            )
            return 3
        if exc.reason_code not in {
            "provider_evidence_present", "provider_submission_ambiguous",
            "stale_checkpoint_basis",
            "exact_replay",
        }:
            logger.error(
                "command_refused command=external_authority_v2 phase=intent "
                "reason=%s error_class=%s",
                exc.reason_code, type(exc).__name__,
            )
            raise
        logger.info(
            "intent_revalidation_deferred reason=%s",
            exc.reason_code,
        )
        intent_result = None

    def prepare(action: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        binding = action["binding"]
        request_key = hashlib.sha256(
            f"{request['external_authority_request_sha256']}:{grant['grant_sha256']}:{action['action_id']}".encode()
        ).hexdigest()
        provider_config = {
            "provider_kind": "openai_responses",
            "model": binding["model"],
            "maximum_output_tokens": binding["maximum_output_tokens"],
            "base_url": args.base_url.rstrip("/"),
            "http_timeout_seconds": float(args.http_timeout_seconds),
            "max_transport_retries": 0,
        }
        provider_config_sha256 = hashlib.sha256(json.dumps(
            provider_config, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        reason_code = None
        payload = None
        provider = None
        try:
            payload = resolve_external_authority_v2_request_payload(run_dir, action)
            provider = OpenAIResponsesProvider(
                api_key=api_key, model=binding["model"],
                max_output_tokens=binding["maximum_output_tokens"],
                base_url=args.base_url, http_timeout_seconds=args.http_timeout_seconds,
                max_transport_retries=0, require_spend_authorization=False,
            )
        except ExternalAuthorityV2ExecutionError as exc:
            if exc.reason_code not in {
                "request_payload_unavailable", "request_payload_ambiguous",
                "request_payload_digest_mismatch",
            }:
                raise
            reason_code = exc.reason_code
        except ValueError:
            reason_code = "provider_configuration_invalid"
        basis = build_external_authority_prepared_create_basis(
            action,
            run_id=context["run_id"],
            request_sha256=context["request_sha256"],
            grant_sha256=context["grant_sha256"],
            checkpoint_snapshot_sha256=context["checkpoint_snapshot_sha256"],
            local_request_key_sha256=request_key,
            provider_configuration_sha256=provider_config_sha256,
            outcome="refused" if reason_code else "ready",
            reason_code=reason_code,
        )
        return build_external_authority_prepared_create(
            basis=basis,
            transport_context=(None if reason_code else {
                "provider": provider,
                "payload": payload,
                "idempotency_key": request_key,
                "timeout_seconds": args.http_timeout_seconds,
            }),
        )

    def create(prepared: dict[str, Any]) -> dict[str, Any]:
        transport = prepared["transport_context"]
        response, attempts = transport["provider"].create_response_only(
            transport["payload"],
            idempotency_key=transport["idempotency_key"],
            timeout_seconds=transport["timeout_seconds"],
        )
        return {
            "id": response.get("id") if isinstance(response, dict) else None,
            "kind": "response",
            "transport_attempts": attempts,
        }

    try:
        dispatch_result = dispatch_external_authority_v2_intent(
            run_dir, request_sha256=request["external_authority_request_sha256"],
            grant_sha256=grant["grant_sha256"], prepare=prepare, create=create,
            event_emitter=event_emitter,
            suspension_observer=suspension_observer,
        )
    except CooperativeSuspensionPublished as exc:
        command_result = exc.publication["command_result"]
        _render(command_result, args.output)
        log_cli_exit(
            logger, command="external_authority_v2",
            operation="cooperative_suspend", exit_code=0,
            outcome=command_result["outcome"],
            result_id=command_result["result_id"],
            receipt_id=command_result["receipt_id"],
            authoritative_transport="output_file" if args.output else "stdout_json",
        )
        return 0
    except ExternalAuthorityV2ExecutionError as exc:
        logger.error(
            "command_refused command=external_authority_v2 phase=dispatch "
            "reason=%s error_class=%s",
            exc.reason_code, type(exc).__name__,
        )
        raise
    logger.info(
        "command_complete command=external_authority_v2 outcome=%s "
        "provider_bound_count=%s ambiguous_count=%s refused_count=%s",
        dispatch_result["outcome"],
        len(dispatch_result.get("provider_bound_action_ids") or []),
        len(dispatch_result.get("ambiguous_action_ids") or []),
        len(dispatch_result.get("refused_action_ids") or []),
    )
    command_result = (
        build_external_authority_v2_command_result_v3(
            intent_result=intent_result, dispatch_result=dispatch_result,
        )
        if dispatch_result.get("schema_version")
        == "astrowoof.external_authority_provider_dispatch_result.v4"
        else build_external_authority_v2_command_result_v2(
            intent_result=intent_result, dispatch_result=dispatch_result,
        )
    )
    log_decision_summary(
        logger, command_result, command="external_authority_v2",
        operation="constrained_dispatch",
    )
    _render(command_result, args.output)
    exit_code = (
        0 if dispatch_result["outcome"] in {"detached_provider_pending", "exact_replay"}
        else 3
    )
    log_cli_exit(
        logger, command="external_authority_v2", operation="constrained_dispatch",
        exit_code=exit_code, outcome=dispatch_result["outcome"],
        result_id=command_result.get("result_id"),
        receipt_id=command_result.get("receipt_id"),
        authoritative_transport="output_file" if args.output else "stdout_json",
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
