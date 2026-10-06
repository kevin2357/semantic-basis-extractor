"""Create or resume one bounded-Natal authoring run."""

from __future__ import annotations

import argparse
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
from ..bounded_admission import admit_bounded_family, load_bounded_family
from ..bounded_authoring import compile_bounded_authoring_artifacts
from ..bounded_basis import build_bounded_basis
from ..bounded_lifecycle import (
    FakeBoundedLifecycleProvider,
    create_bounded_run,
    resume_bounded_run,
)
from ..bounded_provider import OpenAIBoundedLifecycleProvider
from ..bounded_authoring import BOUNDED_RUN_V2_CONTRACT
from ..bounded_selection import BoundedSelectionError, select_bounded_portfolio
from ..closure import load_json, public_run_state, resolve_processing_profile_args
from ..execution_events import (
    ExecutionEventEmitter,
    JsonlEventSink,
    StdoutJsonlSink,
    command_result_envelope,
)
from ..bounded_eligibility import build_bounded_eligibility_command_result
from ..processing_profiles import (
    resolve_installed_processing_profile,
    resolve_prompt_release_stage,
    resolve_prompt_release_workspace_assets,
)
from ..spend import (
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
    BudgetExhausted,
)
from ..trace_observability import (
    log_cli_exit,
    log_decision_summary,
    log_native_state_summary,
)


logger = logging.getLogger(__name__)


def _json(path: Path | None) -> dict[str, Any] | None:
    return load_json(path) if path else None


def _provider(
    args: argparse.Namespace, *, processing_profile_id: str | None = None,
):
    if args.provider == "fake":
        return FakeBoundedLifecycleProvider()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required for provider=openai")
    system_prompts_by_stage: dict[str, str] = {}
    prompt_release_provenance_by_stage: dict[str, dict[str, Any]] = {}
    if processing_profile_id is not None:
        stage_map = {
            "authoring_initial": "initial",
            "creative_retry": "retry",
            "polish": "polish",
            "qualitative_critic": "critic",
        }
        for native_stage, release_stage in stage_map.items():
            prompt, provenance = resolve_prompt_release_stage(
                processing_profile_id, stage=release_stage,
            )
            system_prompts_by_stage[native_stage] = prompt
            prompt_release_provenance_by_stage[native_stage] = provenance
    return OpenAIBoundedLifecycleProvider(
        run_dir=args.run_dir,
        api_key=key,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        service_level=args.service_level,
        maximum_output_tokens=args.maximum_output_tokens,
        system_prompts_by_stage=system_prompts_by_stage,
        prompt_release_provenance_by_stage=prompt_release_provenance_by_stage,
    )


def _resolve_profile_binding(args: argparse.Namespace) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Resolve the sealed bounded profile and replace caller-owned knobs."""
    binding = resolve_processing_profile_args(
        args, expected_sbe_contract=BOUNDED_RUN_V2_CONTRACT,
    )
    if binding is None:
        return None, None
    profile = resolve_installed_processing_profile(
        binding["processing_profile_id"]
    )
    if profile["route"]["family"] != "bounded_natal":
        raise ValueError("processing profile is not a bounded-Natal profile")
    sbe = profile["sbe"]
    args.provider = sbe["provider"]
    args.service_level = sbe["provider_service_level"]
    args.model = sbe["model"]
    args.reasoning_effort = sbe["reasoning_effort"]
    args.maximum_output_tokens = sbe["max_output_tokens"]
    return binding, profile


def _profile_generation_settings(
    profile: dict[str, Any] | None, binding: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if profile is None or binding is None:
        return None
    sbe = profile["sbe"]
    return {
        "max_attempts": sbe["max_attempts"],
        "optional_stages": {
            "polish": sbe["polish"],
            "qualitative_critic": sbe["qualitative_critic"],
            "qualitative_candidate": sbe["qualitative_candidate"],
        },
        "processing_profile_binding": binding,
        "selection_policy": profile["selection_policy"],
        "prompt_release": binding["prompt_release"],
    }


def _command_output(state: dict[str, Any], sealed: dict[str, Any]) -> dict[str, Any]:
    """Return the exact same-invocation delivery handoff when available."""
    if sealed["result"].get("outcome") == "delivery_complete":
        from ..terminal_review_contracts import build_terminal_delivery_command_result
        return build_terminal_delivery_command_result(
            sealed["result"], sealed["receipt"],
        )
    return public_run_state(state)


def _bounded_eligibility_handoff(args: argparse.Namespace) -> dict[str, str] | None:
    """Read the atomic API-owned identities needed before a workspace exists."""
    values = {
        "native_run_id": args.native_run_id,
        "native_invocation_id": args.native_invocation_id,
        "canonical_semantic_identity_sha256": args.canonical_semantic_identity_sha256,
        "projection_set_evidence_sha256": args.projection_set_evidence_sha256,
    }
    present = [value is not None for value in values.values()]
    if any(present) and not all(present):
        raise ValueError("bounded eligibility handoff fields are required together")
    if not any(present):
        return None
    return {key: str(value) for key, value in values.items()}


def _bounded_eligibility_profile_binding(
    binding: dict[str, Any] | None,
) -> dict[str, str]:
    """Project the durable installed binding onto the closed public result.

    Workspaces retain the richer nested binding (route, prompt release, and
    package descriptors). The pre-workspace eligibility result instead has the
    deliberately smaller API-frozen projection. Never pass the workspace shape
    through as though it were that public contract.
    """
    if not isinstance(binding, dict):
        raise ValueError("bounded eligibility requires a processing profile binding")
    route = binding.get("route")
    worker = binding.get("worker_compatibility")
    if not isinstance(route, dict) or not isinstance(worker, dict):
        raise ValueError("bounded eligibility processing profile binding is invalid")
    value = {
        "schema_version": binding.get("schema_version"),
        "processing_profile_id": binding.get("processing_profile_id"),
        "processing_profile_sha256": binding.get("processing_profile_sha256"),
        "generation_manifest_sha256": binding.get("generation_manifest_sha256"),
        "route_family": route.get("family"),
        "worker_role": worker.get("worker_role"),
        "worker_compatibility_sha256": worker.get("compatibility_sha256"),
    }
    if (
        value["schema_version"] != "astrowoof.processing_profile_binding.v1"
        or value["route_family"] != "bounded_natal"
        or value["worker_role"] != "sbe_authoring"
        or not all(isinstance(item, str) and item for item in value.values())
    ):
        raise ValueError("bounded eligibility processing profile binding is invalid")
    return {key: str(item) for key, item in value.items()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--input-package", type=Path)
    parser.add_argument("--subject", type=Path)
    parser.add_argument("--generation-profile", type=Path)
    parser.add_argument("--processing-profile-id", dest="processing_profile_id")
    parser.add_argument("--processing-profile-sha256", dest="processing_profile_sha256")
    parser.add_argument("--generation-manifest-sha256", dest="generation_manifest_sha256")
    parser.add_argument(
        "--processing-profile-route-family",
        dest="processing_profile_route_family",
    )
    parser.add_argument("--native-run-id")
    parser.add_argument("--native-invocation-id")
    parser.add_argument("--canonical-semantic-identity-sha256")
    parser.add_argument("--projection-set-evidence-sha256")
    parser.add_argument("--provider", choices=("fake", "openai"), default="fake")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--service-level", choices=("interactive", "batch"), default="interactive")
    parser.add_argument("--maximum-output-tokens", type=int, default=100_000)
    parser.add_argument("--spend-authorization", type=Path, action="append", default=[])
    parser.add_argument("--initial-wave-authorization", type=Path)
    parser.add_argument("--external-authority-request", type=Path)
    parser.add_argument("--external-authority-grant", type=Path)
    parser.add_argument("--events-jsonl", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--provider-reconciliation-cycle", action="store_true")
    parser.add_argument("--observed-at")
    add_logging_arguments(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging_from_args(args)
    if args.resume and (args.run_dir / "run.json").is_file():
        existing = load_json(args.run_dir / "run.json")
        bind_logging_context(
            run_id=existing.get("run_id"), current_state=existing.get("status")
        )
    logger.info(
        "command_start command=bounded_run resume=%s reconciliation=%s "
        "service_level=%s",
        args.resume, args.provider_reconciliation_cycle, args.service_level,
    )
    try:
        processing_profile_binding, processing_profile = _resolve_profile_binding(args)
        bounded_eligibility_handoff = _bounded_eligibility_handoff(args)
    except ValueError as exc:
        parser.error(str(exc))
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
    if args.provider_reconciliation_cycle and (
        args.spend_authorization or args.initial_wave_authorization
        or args.external_authority_request or args.external_authority_grant
    ):
        parser.error("provider reconciliation cannot apply spend authorization")
    if args.provider_reconciliation_cycle and not args.observed_at:
        parser.error("--provider-reconciliation-cycle requires --observed-at")
    if args.initial_wave_authorization and len(args.spend_authorization) != 6:
        parser.error(
            "--initial-wave-authorization requires exactly six ordered "
            "--spend-authorization documents"
        )
    if args.initial_wave_authorization:
        parser.error(
            "legacy --initial-wave-authorization cannot authorize provider create"
        )
    if bool(args.external_authority_request) != bool(args.external_authority_grant):
        parser.error("external authority request and grant are required together")
    if args.external_authority_request and (
        not args.resume or args.provider != "openai"
        or args.service_level != "interactive"
        or len(args.spend_authorization) != 6
    ):
        parser.error(
            "bounded external initial-wave authority requires interactive OpenAI "
            "resume and exactly six member authorizations"
        )
    if args.resume and processing_profile_binding is not None:
        durable = load_json(args.run_dir / "run.json")
        if durable.get("processing_profile_binding") != processing_profile_binding:
            parser.error("resume processing profile binding does not match durable run")
    if args.resume and processing_profile_binding is None and (
        args.run_dir / "run.json"
    ).is_file() and load_json(args.run_dir / "run.json").get("processing_profile_binding") is not None:
        parser.error("profile-bound resume requires the original processing profile handoff")
    if args.resume and bounded_eligibility_handoff is not None:
        parser.error("bounded eligibility handoff is only valid for a new run")
    if not args.resume and processing_profile_binding is not None and bounded_eligibility_handoff is None:
        parser.error(
            "profile-bound bounded run requires the complete bounded eligibility handoff"
        )
    admission = None
    selection = None
    if not args.resume:
        admission = admit_bounded_family(load_bounded_family(args.input_package))
        basis = build_bounded_basis(admission)
        try:
            selection = select_bounded_portfolio(basis)
        except BoundedSelectionError as exc:
            if exc.code != "insufficient_invariant_basis" or bounded_eligibility_handoff is None:
                raise
            result = build_bounded_eligibility_command_result(
                native_run_id=bounded_eligibility_handoff["native_run_id"],
                native_invocation_id=bounded_eligibility_handoff["native_invocation_id"],
                source_binding={
                    "canonical_semantic_identity_sha256": bounded_eligibility_handoff[
                        "canonical_semantic_identity_sha256"
                    ],
                    "projection_set_evidence_sha256": bounded_eligibility_handoff[
                        "projection_set_evidence_sha256"
                    ],
                },
                processing_profile_binding=_bounded_eligibility_profile_binding(
                    processing_profile_binding
                ),
            )
            StdoutJsonlSink()(command_result_envelope(result))
            log_cli_exit(
                logger, command="bounded_run", operation="bounded_eligibility",
                exit_code=0, outcome="ineligible", result_id=result["result_id"],
                authoritative_transport="stdout_jsonl",
            )
            return
    provider = (
        _provider(
            args,
            processing_profile_id=(
                processing_profile_binding["processing_profile_id"]
                if processing_profile_binding is not None else None
            ),
        )
        if (args.resume or args.provider_reconciliation_cycle or not args.prepare_only)
        else FakeBoundedLifecycleProvider()
    )
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
                    bounded_interactive_provider=(
                        provider if args.service_level == "interactive" else None
                    ),
                    bounded_batch_provider=(
                        provider if args.service_level == "batch" else None
                    ),
                    bounded_batch_transport=(
                        provider.batch_transport
                        if args.service_level == "batch" else None
                    ),
                ),
                event_emitter=emitter,
            )
            log_decision_summary(
                logger, result, command="bounded_run",
                operation="provider_reconciliation",
            )
            print(json.dumps(result, sort_keys=True))
            log_cli_exit(
                logger, command="bounded_run", operation="provider_reconciliation",
                exit_code=0 if result["outcome"] == "terminal" else 3,
                outcome=result["outcome"], authoritative_transport="stdout_json",
            )
            if result["outcome"] != "terminal":
                raise SystemExit(3)
            return
        if not args.resume:
            if admission is None or selection is None:
                raise RuntimeError("bounded selection was not prepared")
            artifacts = compile_bounded_authoring_artifacts(
                admission, selection, subject=_json(args.subject)
            )
            prompt_assets = (
                dict(resolve_prompt_release_workspace_assets(
                    processing_profile_binding["processing_profile_id"],
                ) or [])
                if processing_profile_binding is not None else None
            )
            state = create_bounded_run(
                args.run_dir, artifacts, provider=provider,
                generation_profile=(
                    _profile_generation_settings(
                        processing_profile, processing_profile_binding,
                    )
                    if processing_profile_binding is not None
                    else _json(args.generation_profile)
                ),
                processing_profile_binding=processing_profile_binding,
                prompt_workspace_assets=prompt_assets,
                native_run_id=(
                    bounded_eligibility_handoff["native_run_id"]
                    if bounded_eligibility_handoff is not None else None
                ),
                event_emitter=emitter,
            )
            if args.prepare_only:
                from ..native_transitions import publish_native_execution_result
                sealed = publish_native_execution_result(
                    args.run_dir, command_kind="ordinary_authoring",
                    sbe_release=__version__, published_at=state["updated_at"],
                    event_emitter=emitter,
                )
                print(json.dumps(_command_output(state, sealed), sort_keys=True))
                log_native_state_summary(logger, state, phase="prepare_only_complete")
                log_cli_exit(
                    logger, command="bounded_run", operation="prepare_only",
                    exit_code=0, outcome=state.get("status"),
                    authoritative_transport="stdout_json",
                )
                return
        state = resume_bounded_run(
            args.run_dir,
            provider=provider,
            authorizations=[load_json(path) for path in args.spend_authorization],
            initial_wave_authorization=_json(args.initial_wave_authorization),
            external_authority_request=_json(args.external_authority_request),
            external_authority_grant=_json(args.external_authority_grant),
            event_emitter=emitter,
        )
        from ..native_transitions import publish_native_execution_result
        sealed = publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=state["updated_at"],
            event_emitter=emitter,
        )
        log_native_state_summary(logger, state, phase="ordinary_run_complete")
        print(json.dumps(_command_output(state, sealed), sort_keys=True))
        log_cli_exit(
            logger, command="bounded_run",
            operation="resume" if args.resume else "create",
            exit_code=0 if state.get("status") == "DELIVERY_COMPLETE" else 3,
            outcome=state.get("status"), authoritative_transport="stdout_json",
        )
        if state.get("status") != "DELIVERY_COMPLETE":
            raise SystemExit(3)
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission) as exc:
        logger.warning(
            "command_handoff outcome=external_boundary error_class=%s error=%s",
            type(exc).__name__, exc,
        )
        state = load_json(args.run_dir / "run.json")
        from ..native_transitions import publish_native_execution_result
        sealed = publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=state["updated_at"],
            event_emitter=emitter,
        )
        log_native_state_summary(logger, state, phase="external_boundary")
        print(json.dumps(_command_output(state, sealed), sort_keys=True))
        log_cli_exit(
            logger, command="bounded_run", operation="external_boundary",
            exit_code=3, outcome=type(exc).__name__,
            authoritative_transport="stdout_json", exception=exc,
        )
        raise SystemExit(3)


if __name__ == "__main__":
    main()
