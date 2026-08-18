"""Create or resume one bounded-Natal authoring run."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .. import __version__
from ..bounded_admission import admit_bounded_family, load_bounded_family
from ..bounded_authoring import compile_bounded_authoring_artifacts
from ..bounded_basis import build_bounded_basis
from ..bounded_lifecycle import (
    FakeBoundedLifecycleProvider,
    create_bounded_run,
    resume_bounded_run,
)
from ..bounded_provider import OpenAIBoundedLifecycleProvider
from ..bounded_selection import select_bounded_portfolio
from ..closure import load_json, public_run_state
from ..execution_events import ExecutionEventEmitter, JsonlEventSink
from ..spend import (
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
    BudgetExhausted,
)


def _json(path: Path | None) -> dict[str, Any] | None:
    return load_json(path) if path else None


def _provider(args: argparse.Namespace):
    if args.provider == "fake":
        return FakeBoundedLifecycleProvider()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required for provider=openai")
    return OpenAIBoundedLifecycleProvider(
        run_dir=args.run_dir,
        api_key=key,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        service_level=args.service_level,
        maximum_output_tokens=args.maximum_output_tokens,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--input-package", type=Path)
    parser.add_argument("--subject", type=Path)
    parser.add_argument("--generation-profile", type=Path)
    parser.add_argument("--provider", choices=("fake", "openai"), default="fake")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--service-level", choices=("interactive", "batch"), default="interactive")
    parser.add_argument("--maximum-output-tokens", type=int, default=100_000)
    parser.add_argument("--spend-authorization", type=Path, action="append", default=[])
    parser.add_argument("--events-jsonl", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--provider-reconciliation-cycle", action="store_true")
    parser.add_argument("--observed-at")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.resume and (args.input_package or args.subject or args.generation_profile):
        parser.error("resume uses the frozen workspace; omit input, subject, and profile")
    if not args.resume and not args.input_package:
        parser.error("new bounded runs require --input-package")
    if args.prepare_only and args.resume:
        parser.error("--prepare-only cannot be combined with --resume")
    if args.provider_reconciliation_cycle and not args.resume:
        parser.error("--provider-reconciliation-cycle requires --resume")
    if args.provider_reconciliation_cycle and args.provider != "openai":
        parser.error("--provider-reconciliation-cycle requires provider=openai")
    if args.provider_reconciliation_cycle and args.service_level != "interactive":
        parser.error("bounded-Natal Batch reconciliation is not supported")
    if args.provider_reconciliation_cycle and args.spend_authorization:
        parser.error("provider reconciliation cannot apply spend authorization")
    if args.provider_reconciliation_cycle and not args.observed_at:
        parser.error("--provider-reconciliation-cycle requires --observed-at")
    provider = _provider(args)
    emitter = ExecutionEventEmitter(
        release=__version__,
        sink=JsonlEventSink(args.events_jsonl) if args.events_jsonl else None,
    )
    try:
        if args.provider_reconciliation_cycle:
            from ..reconciliation import (
                ProviderReconciliationAdapters,
                reconcile_authoring_provider_cycle,
            )
            result = reconcile_authoring_provider_cycle(
                args.run_dir,
                observed_at=args.observed_at,
                provider_adapters=ProviderReconciliationAdapters(
                    bounded_interactive_provider=provider,
                ),
                event_emitter=emitter,
            )
            print(json.dumps(result, sort_keys=True))
            if result["outcome"] != "terminal":
                raise SystemExit(3)
            return
        if not args.resume:
            admission = admit_bounded_family(load_bounded_family(args.input_package))
            basis = build_bounded_basis(admission)
            selection = select_bounded_portfolio(basis)
            artifacts = compile_bounded_authoring_artifacts(
                admission, selection, subject=_json(args.subject)
            )
            state = create_bounded_run(
                args.run_dir, artifacts, provider=provider,
                generation_profile=_json(args.generation_profile),
                event_emitter=emitter,
            )
            if args.prepare_only:
                from ..native_transitions import publish_native_execution_result
                publish_native_execution_result(
                    args.run_dir, command_kind="ordinary_authoring",
                    sbe_release=__version__, published_at=state["updated_at"],
                )
                print(json.dumps(public_run_state(state), sort_keys=True))
                return
        state = resume_bounded_run(
            args.run_dir,
            provider=provider,
            authorizations=[load_json(path) for path in args.spend_authorization],
            event_emitter=emitter,
        )
        from ..native_transitions import publish_native_execution_result
        publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=state["updated_at"],
        )
        print(json.dumps(public_run_state(state), sort_keys=True))
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission):
        state = load_json(args.run_dir / "run.json")
        from ..native_transitions import publish_native_execution_result
        publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=state["updated_at"],
        )
        print(json.dumps(public_run_state(state), sort_keys=True))
        raise SystemExit(3)


if __name__ == "__main__":
    main()
