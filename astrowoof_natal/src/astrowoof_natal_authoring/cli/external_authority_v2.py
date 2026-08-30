"""Supported constrained external-authority v2 command."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any

from .. import __version__
from ..application_logging import (
    add_logging_arguments,
    bind_logging_context,
    configure_logging_from_args,
)
from ..closure import OpenAIResponsesProvider
from ..execution_events import ExecutionEventEmitter, JsonlEventSink, StdoutJsonlSink
from ..external_authority_v2 import build_no_grant_dispatch_result_v2
from ..external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_prepared_create,
    build_external_authority_prepared_create_basis,
    build_external_authority_v2_command_result_v2,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    resolve_external_authority_v2_request_payload,
)


logger = logging.getLogger(__name__)


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Consume or inspect one exact external-authority v2 request.",
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--inspection", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--grant", type=Path)
    parser.add_argument("--authorization", action="append", type=Path, default=[])
    parser.add_argument("--provider", choices=("none", "openai"), default="none")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--base-url", default="https://api.openai.com/v1")
    parser.add_argument("--http-timeout-seconds", type=float, default=15.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--events-jsonl", type=Path)
    parser.add_argument("--events-stdout-jsonl", action="store_true")
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
    bind_logging_context(
        run_id=str(native_state.get("run_id") or "-"),
        current_state=str(native_state.get("status") or "-"),
    )
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

    if args.grant is None:
        if args.authorization or args.provider != "none":
            parser.error("grant-free inspection accepts no authorization or provider")
        result = build_no_grant_dispatch_result_v2(inspection)
        logger.info(
            "command_complete command=external_authority_v2 outcome=%s provider_io=none",
            result["outcome"],
        )
        _render(result, args.output)
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
        )
    except ExternalAuthorityV2ExecutionError as exc:
        if exc.reason_code not in {
            "provider_evidence_present", "provider_submission_ambiguous",
            "action_state_or_custody_mismatch", "stale_checkpoint_basis",
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
        )
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
    _render(build_external_authority_v2_command_result_v2(
        intent_result=intent_result, dispatch_result=dispatch_result,
    ), args.output)
    return 0 if dispatch_result["outcome"] in {"detached_provider_pending", "exact_replay"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
