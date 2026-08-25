"""Installed-wheel, provider-free qualification for v2 payload recovery."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
import threading
import zipfile
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any

from .closure import (
    AwaitingSpendAuthorization,
    OpenAIResponsesProvider,
    PassSpec,
    SpendController,
    initial_run_state,
    load_json,
    prepare_source_workspace,
    save_state,
)
from .external_authority_v2 import build_external_authority_grant_v2
from .external_authority_v2_execution import (
    ExternalAuthorityV2ExecutionError,
    build_external_authority_prepared_create,
    build_external_authority_prepared_create_basis,
    commit_external_authority_v2_dispatch_intent,
    dispatch_external_authority_v2_intent,
    resolve_external_authority_v2_request_payload,
)
from .provenance import resource_set_provenance
from .temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
)


RECEIPT_SCHEMA = "astrowoof.external_authority_v2_payload_recovery_qualification.v1"


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _policy() -> dict[str, Any]:
    ceiling = 100_000_000
    return {
        "currency": "USD",
        "price_book_version": "openai-public-2026-08-07.v1",
        "run_ceiling_micro_usd": ceiling,
        "stage_ceilings_micro_usd": {
            stage: ceiling for stage in (
                "authoring_initial", "creative_retry", "polish",
                "qualitative_critic", "qualitative_candidate",
            )
        },
        "optional_stage_budget_behavior": {
            "polish": "skip",
            "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


def _workspace(root: Path) -> tuple[Path, dict[str, Any]]:
    run_dir = root / "run"
    run_dir.mkdir()
    source = root / "source" / "pass-1"
    source.mkdir(parents=True)
    (source / "AUTHORING BRIEF.md").write_text("Static guidance.\n", encoding="utf-8")
    (source / "DOG DETAILS.md").write_text("Dog: Qualification Pup.\n", encoding="utf-8")
    (source / "START HERE.md").write_text("Complete the supplied card.\n", encoding="utf-8")
    (source / "WRITE THIS CARD.md").write_text(
        "<!-- BEGIN FIELD: body -->\nDraft this card.\n<!-- END FIELD: body -->\n",
        encoding="utf-8",
    )
    retained = run_dir / "retained-inputs" / "pass-1.zip"
    retained.parent.mkdir()
    with zipfile.ZipFile(retained, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, Path("pass-1") / path.relative_to(source))
    source_sha256 = hashlib.sha256(retained.read_bytes()).hexdigest()
    spec = PassSpec("pass-1", "qualification-pup", 1, retained, source_sha256)
    provider = OpenAIResponsesProvider(
        api_key="provider-free", background=False,
        prompt_cache_mode="disabled", require_spend_authorization=True,
    )
    input_root = run_dir / "synthetic-input"
    input_root.mkdir()
    state = initial_run_state(
        input_package=input_root, run_dir=run_dir, provider=provider,
        max_attempts=3,
        sbe_manifest={"status": "pass", "subject_count": 1},
        specs=[spec], profile={"spend_policy": _policy()},
    )
    state["provenance"] = {
        "runtime": {
            "distribution": "astrowoof-natal-authoring", "version": "0.4.23",
        },
        "resources": resource_set_provenance(),
    }
    run_json = run_dir / "run.json"
    source_workspace = prepare_source_workspace(spec, run_dir / "passes" / spec.pass_id)
    attempt_root = run_dir / "passes" / spec.pass_id / "attempt-002"
    attempt = {
        "attempt_number": 2, "state": "SUBMITTED",
        "started_at": "2026-08-25T16:00:00Z", "finished_at": None,
        "response_workspace": str((attempt_root / "response" / spec.pass_id).resolve()),
        "provider_metadata": None, "qa": None, "error": None,
    }
    state["passes"][spec.pass_id]["attempts"].append(attempt)
    state["passes"][spec.pass_id]["state"] = "SUBMITTED"
    save_state(run_json, state)
    controller = SpendController(
        state=state, run_json=run_json, state_lock=threading.Lock(),
        consumer_id="installed-payload-recovery-qualification",
    )
    before_submit, provider_created = controller.callbacks(
        stage="creative_retry", route="pass-1:attempt-002",
        model=provider.model, service_level="interactive",
        maximum_output_tokens=provider.max_output_tokens,
    )
    try:
        provider.author(
            source_workspace, Path(attempt["response_workspace"]), spec, 2, None,
            before_submit, provider_created,
        )
    except AwaitingSpendAuthorization as exc:
        action = exc.action
    else:  # pragma: no cover - contract guard
        raise RuntimeError("qualification action did not await authority")
    if not isinstance(action, dict):
        raise RuntimeError("qualification action was not prepared")
    artifact = action.pop("request_payload_artifact")
    Path(artifact["logical_path"]).unlink()
    attempt["state"] = "AWAITING_SPEND_AUTHORIZATION"
    attempt["paid_action_id"] = action["action_id"]
    state["passes"][spec.pass_id]["state"] = "AWAITING_SPEND_AUTHORIZATION"
    state["initial_authoring_wave"] = {"state": "DETACHED"}
    save_state(run_json, state)
    return run_dir, action


def _authority(run_dir: Path, observed_at: str, label: str) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    inspection = inspect_temporal_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at,
    )
    request = build_external_authority_request_v2(inspection)
    inventory = {
        item["action_id"]: item
        for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action_id,
        "binding": copy.deepcopy(inventory[action_id]["binding"]),
        "authorization_reference": f"qualification:{label}:{index}",
    } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
    grant = build_external_authority_grant_v2(
        request, inspection, documents,
        api_decision_id=f"qualification:{label}",
        issuer="astrowoof-api-qualification", issued_at=observed_at,
    )
    return inspection, request, documents, grant


def _dispatch(run_dir: Path, inspection: dict[str, Any], request: dict[str, Any], documents: list[dict[str, Any]], grant: dict[str, Any], creates: list[str]) -> dict[str, Any]:
    commit_external_authority_v2_dispatch_intent(
        run_dir, request=request, inspection=inspection, grant=grant,
        authorization_documents=documents,
    )

    def prepare(action: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        reason = None
        payload = None
        try:
            payload = resolve_external_authority_v2_request_payload(run_dir, action)
        except ExternalAuthorityV2ExecutionError as exc:
            reason = exc.reason_code
        basis = build_external_authority_prepared_create_basis(
            action, run_id=context["run_id"],
            request_sha256=context["request_sha256"],
            grant_sha256=context["grant_sha256"],
            checkpoint_snapshot_sha256=context["checkpoint_snapshot_sha256"],
            local_request_key_sha256="a" * 64,
            provider_configuration_sha256="b" * 64,
            outcome="refused" if reason else "ready", reason_code=reason,
        )
        return build_external_authority_prepared_create(
            basis=basis,
            transport_context=None if reason else {"payload_sha256": _digest(payload)},
        )

    def create(_prepared: dict[str, Any]) -> dict[str, Any]:
        creates.append("POST")
        return {"id": "resp_payload_recovery_qualification", "kind": "response"}

    return dispatch_external_authority_v2_intent(
        run_dir,
        request_sha256=request["external_authority_request_sha256"],
        grant_sha256=grant["grant_sha256"], prepare=prepare, create=create,
    )


def validate_payload_recovery_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "provider_create_count",
        "provider_spend_usd", "sbe_version", "old_refusal_reason",
        "old_provider_io_disposition", "fresh_request_distinct",
        "fresh_dispatch_outcome", "replay_outcome", "refusal_history_preserved",
    }
    if not isinstance(value, dict) or set(value) != keys or value.get("schema_version") != RECEIPT_SCHEMA:
        raise ValueError("payload-recovery qualification receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("payload-recovery qualification receipt digest mismatch")
    if (
        value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("provider_create_count") != 1
        or value.get("provider_spend_usd") != 0
        or value.get("old_refusal_reason") != "request_payload_digest_mismatch"
        or value.get("old_provider_io_disposition") != "not_attempted"
        or value.get("fresh_request_distinct") is not True
        or value.get("fresh_dispatch_outcome") != "detached_provider_pending"
        or value.get("replay_outcome") != "exact_replay"
        or value.get("refusal_history_preserved") is not True
    ):
        raise ValueError("payload-recovery qualification assertions failed")
    return copy.deepcopy(value)


def read_payload_recovery_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "external-authority-v2-payload-recovery-qualification.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def run_payload_recovery_qualification() -> dict[str, Any]:
    creates: list[str] = []
    with tempfile.TemporaryDirectory(prefix="sbe-payload-recovery-qa-") as temporary:
        run_dir, _action = _workspace(Path(temporary))
        old = _authority(run_dir, "2026-08-25T16:01:00Z", "old")
        old_result = _dispatch(run_dir, *old, creates)
        history = copy.deepcopy(load_json(run_dir / "run.json")["external_authority_v2_dispatch_history"])
        old_replay = dispatch_external_authority_v2_intent(
            run_dir,
            request_sha256=old[1]["external_authority_request_sha256"],
            grant_sha256=old[3]["grant_sha256"],
            prepare=lambda *_args: (_ for _ in ()).throw(RuntimeError("replay prepared")),
            create=lambda *_args: (_ for _ in ()).throw(RuntimeError("replay created")),
        )
        fresh = _authority(run_dir, "2026-08-25T16:02:00Z", "fresh")
        fresh_result = _dispatch(run_dir, *fresh, creates)
        replay = dispatch_external_authority_v2_intent(
            run_dir,
            request_sha256=fresh[1]["external_authority_request_sha256"],
            grant_sha256=fresh[3]["grant_sha256"],
            prepare=lambda *_args: (_ for _ in ()).throw(RuntimeError("replay prepared")),
            create=lambda *_args: (_ for _ in ()).throw(RuntimeError("replay created")),
        )
        preserved = load_json(run_dir / "run.json")["external_authority_v2_dispatch_history"][:len(history)] == history
    try:
        installed = version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        installed = "source-tree"
    body = {
        "schema_version": RECEIPT_SCHEMA,
        "status": "pass", "qualification_only": True, "provider_free": True,
        "external_network_call_count": 0,
        "provider_create_count": len(creates), "provider_spend_usd": 0,
        "sbe_version": installed,
        "old_refusal_reason": old_result["reason_code"],
        "old_provider_io_disposition": old_result["provider_io_disposition"],
        "fresh_request_distinct": old[1]["external_authority_request_sha256"] != fresh[1]["external_authority_request_sha256"],
        "fresh_dispatch_outcome": fresh_result["outcome"],
        "replay_outcome": replay["outcome"],
        "refusal_history_preserved": preserved and old_replay["outcome"] == "pre_provider_refusal",
    }
    return validate_payload_recovery_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run provider-free installed-wheel payload-recovery qualification.",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_payload_recovery_qualification_schema()
        if args.schema else run_payload_recovery_qualification()
    )
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
