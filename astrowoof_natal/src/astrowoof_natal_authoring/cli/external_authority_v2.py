"""Supported constrained external-authority v2 command."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from ..closure import OpenAIResponsesProvider
from ..external_authority_v2 import build_no_grant_dispatch_result_v2
from ..external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_v2_command_result,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    resolve_external_authority_v2_request_payload,
)


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
    args = parser.parse_args(argv)
    run_dir = args.run_dir.resolve()
    _outside_workspace(args.output, run_dir)
    inspection = _load(args.inspection)
    request = _load(args.request)

    if args.grant is None:
        if args.authorization or args.provider != "none":
            parser.error("grant-free inspection accepts no authorization or provider")
        _render(build_no_grant_dispatch_result_v2(inspection), args.output)
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
        )
    except ExternalAuthorityV2ExecutionError as exc:
        if exc.reason_code not in {
            "provider_evidence_present", "provider_submission_ambiguous",
            "action_state_or_custody_mismatch",
        }:
            raise
        intent_result = None

    def create(action: dict[str, Any]) -> dict[str, Any]:
        binding = action["binding"]
        payload = resolve_external_authority_v2_request_payload(run_dir, action)
        provider = OpenAIResponsesProvider(
            api_key=api_key, model=binding["model"],
            max_output_tokens=binding["maximum_output_tokens"],
            base_url=args.base_url, http_timeout_seconds=args.http_timeout_seconds,
            max_transport_retries=0, require_spend_authorization=False,
        )
        response, attempts = provider.create_response_only(
            payload,
            idempotency_key=hashlib.sha256(
                f"{request['external_authority_request_sha256']}:{grant['grant_sha256']}:{action['action_id']}".encode()
            ).hexdigest(),
            timeout_seconds=args.http_timeout_seconds,
        )
        return {"id": response["id"], "kind": "response", "transport_attempts": attempts}

    dispatch_result = dispatch_external_authority_v2_intent(
        run_dir, request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"], create=create,
    )
    _render(build_external_authority_v2_command_result(
        intent_result=intent_result, dispatch_result=dispatch_result,
    ), args.output)
    return 0 if dispatch_result["outcome"] in {"detached_provider_pending", "exact_replay"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
