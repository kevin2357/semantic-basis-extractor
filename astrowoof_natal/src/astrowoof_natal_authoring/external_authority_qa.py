"""Installed-wheel, provider-free external-authority runtime qualification."""

from __future__ import annotations

import argparse
from copy import deepcopy
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from typing import Any, Mapping

from .closure import (
    OpenAIResponsesProvider, execute_exact_initial_wave_with_external_authority,
    initial_run_state, load_json, prepare_exact_interactive_initial_wave, save_state,
)
from .deployed_qa import _binding, _exact_workspace_zip, _qualification_spend_policy, _wave
from .external_authority import (
    build_external_authority_refusal, build_external_authority_request,
    read_external_authority_request, validate_external_authority_grant,
    validate_external_authority_refusal, validate_external_authority_request,
)
from .initial_wave import InitialWaveError
from .lifecycle import inspect_lifecycle
from .pass_protocol import canonical_sha256
from .reconciliation import ProviderReconciliationAdapters, reconcile_authoring_provider_cycle
from .resource_access import read_resource_text
from .spend import prepare_action

RECEIPT_CONTRACT = "astrowoof.external_authority_qualification.v1"
SCHEMA_RESOURCE = "contracts/external-authority-qualification.v1.schema.json"
ASSERTIONS = (
    "fresh_initial_admission", "fresh_worker_restore", "retained_exact_replay",
    "conflicting_lineage_refusal", "stale_request_refusal",
    "ordinary_action_authorization", "reconciliation_separated_from_create",
)


def _digest(value: Mapping[str, Any]) -> str:
    return canonical_sha256(value)


def _observation(revision: int = 2) -> dict[str, Any]:
    """Stable synthetic observation used only by published contract fixtures."""
    return {
        "operator_state_revision": revision, "snapshot_sha256": "c" * 64,
        "logical_workspace_root": "/qualification/sbe-run",
        "snapshot_complete": True, "inventory_valid": True,
        "observed_at": "1970-01-01T00:00:00Z",
        "native_exclusive_access": "declared", "writer_race_possible": False,
    }


def _grant(request: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action["action_id"], "binding": deepcopy(action["binding"]),
        "authorization_reference": f"qualification:{index}",
    } for index, action in enumerate(request["ordered_actions"], 1)]
    body = {
        "schema_version": "astrowoof.external_authority_grant.v1",
        "decision": "granted", "api_decision_id": "qualification-only:no-reservation",
        "issuer": "sbe-installed-qualification", "issued_at": "1970-01-01T00:00:00Z",
        "external_authority_request_sha256": request["external_authority_request_sha256"],
        "run_id": request["run_id"],
        "inspected_state_revision": request["observation"]["operator_state_revision"],
        "snapshot_sha256": request["observation"]["snapshot_sha256"],
        "logical_workspace_root": request["observation"]["logical_workspace_root"],
        "request_kind": request["request_kind"], "action_count": request["action_count"],
        "ordered_action_ids": list(request["ordered_action_ids"]),
        "ordered_member_authorizations": [{
            "action_id": action["action_id"], "binding_sha256": action["binding_sha256"],
            "authorization_document_sha256": _digest(document),
            "authorization_reference": document["authorization_reference"],
        } for action, document in zip(request["ordered_actions"], documents, strict=True)],
        "initial_wave": deepcopy(request["initial_wave"]),
    }
    return {**body, "grant_sha256": _digest(body)}, documents


class _ScriptedResponsesTransport:
    """No-network Responses transport with an external durable call counter."""

    def __init__(self, counter_path: Path) -> None:
        self.counter_path = counter_path.resolve()
        self.lock = threading.Lock()

    def _read(self) -> dict[str, Any]:
        return (json.loads(self.counter_path.read_text(encoding="utf-8"))
                if self.counter_path.is_file() else {"creates": [], "retrievals": []})

    def _write(self, value: dict[str, Any]) -> None:
        temporary = self.counter_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
        temporary.replace(self.counter_path)

    def request_json(self, *, method: str, url: str, **_kwargs: Any) -> dict[str, Any]:
        with self.lock:
            counter = self._read()
            if method == "POST" and url.endswith("/responses"):
                response_id = f"resp_qualification_runtime_{len(counter['creates']) + 1}"
                counter["creates"].append(response_id)
                self._write(counter)
                return {"id": response_id, "status": "in_progress"}
            if method == "GET" and "/responses/" in url:
                response_id = url.rsplit("/", 1)[-1]
                counter["retrievals"].append(response_id)
                self._write(counter)
                return {"id": response_id, "status": "in_progress"}
        raise AssertionError(f"Qualification transport rejected {method} {url}")


def _provider(counter_path: Path) -> OpenAIResponsesProvider:
    return OpenAIResponsesProvider(
        api_key="qualification-only-no-network", model="gpt-5.6-luna",
        max_output_tokens=1000, prompt_cache_mode="disabled",
        require_spend_authorization=True,
        transport=_ScriptedResponsesTransport(counter_path), max_transport_retries=0,
        http_timeout_seconds=1,
    )


def _prepare_exact_workspace(run_dir: Path) -> None:
    bundle = run_dir / "qualification-bundle"
    bundle.mkdir(parents=True)
    specs = [_exact_workspace_zip(bundle, number) for number in range(1, 7)]
    provider = _provider(run_dir.parent / "unreachable-counter.json")
    state = initial_run_state(
        input_package=bundle, run_dir=run_dir, provider=provider, max_attempts=1,
        sbe_manifest={"status": "pass", "subject_count": 1}, specs=specs,
        service_level="interactive",
        profile={"spend_policy": _qualification_spend_policy()},
    )
    run_json = run_dir / "run.json"
    save_state(run_json, state)
    prepare_exact_interactive_initial_wave(
        state=state, provider=provider, run_dir=run_dir, run_json=run_json,
    )
    # Preparation persists its state incrementally; seal the complete prepared
    # workspace before exposing it through a public snapshot-validating reader.
    save_state(run_json, state)


def _run_child(*args: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-m", "astrowoof_natal_authoring.external_authority_qa",
         "--internal-step", *args],
        check=True, capture_output=True, text=True, env=dict(os.environ),
    )
    return json.loads(completed.stdout)


def _internal_execute(run_dir: Path, authority_dir: Path, counter_path: Path) -> dict[str, Any]:
    result = execute_exact_initial_wave_with_external_authority(
        run_dir=run_dir,
        request=json.loads((authority_dir / "request.json").read_text(encoding="utf-8")),
        grant=json.loads((authority_dir / "grant.json").read_text(encoding="utf-8")),
        member_authorizations=json.loads(
            (authority_dir / "member-authorizations.json").read_text(encoding="utf-8")
        ), provider=_provider(counter_path),
    )
    state = load_json(run_dir / "run.json")
    return {
        "outcome": result["outcome"],
        "wave_state": state["initial_authoring_wave"]["state"],
        "provider_ids": sorted(
            action["provider"]["id"] for action in state["spend_ledger"]["actions"]
            if (action.get("provider") or {}).get("id")
        ),
    }


def _internal_replay(run_dir: Path, authority_dir: Path, counter_path: Path) -> dict[str, Any]:
    try:
        _internal_execute(run_dir, authority_dir, counter_path)
    except InitialWaveError as exc:
        return {"refused": True, "reason_code": exc.reason_code}
    raise RuntimeError("Retained constrained replay unexpectedly reached provider create")


def _internal_reconcile(run_dir: Path, counter_path: Path) -> dict[str, Any]:
    observed_at = "2099-01-01T00:00:00Z"
    before = inspect_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at,
    )
    result = reconcile_authoring_provider_cycle(
        run_dir, observed_at=observed_at,
        provider_adapters=ProviderReconciliationAdapters(
            exact_interactive_provider=_provider(counter_path), max_attempts=1,
            python_executable=Path(sys.executable),
        ),
    )
    return {
        "selected_command": before["execution_branch"]["command"],
        "selected_action_count": len(before["execution_branch"]["action_ids"]),
        "outcome": result["outcome"],
        "retrieved_action_count": len(result["cycle"]["retrieved_action_ids"]),
    }


def validate_external_authority_qualification_receipt(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "network_required", "production_authority", "sbe_version",
        "assertions", "fixture_hashes", "provider_create_count", "provider_spend_usd",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("External-authority qualification receipt fields are not exact")
    if value.get("schema_version") != RECEIPT_CONTRACT:
        raise ValueError("Unsupported qualification receipt")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Qualification receipt digest mismatch")
    assertions = value.get("assertions")
    if not isinstance(assertions, dict) or set(assertions) != set(ASSERTIONS) \
            or any(item is not True for item in assertions.values()):
        raise ValueError("Qualification assertions are not closed and passing")
    if (value.get("status") != "pass" or value.get("qualification_only") is not True
            or value.get("provider_free") is not True
            or value.get("network_required") is not False
            or value.get("production_authority") is not False
            or value.get("provider_create_count") != 6
            or value.get("provider_spend_usd") != 0):
        raise ValueError("Qualification safety declaration is invalid")
    hashes = value.get("fixture_hashes")
    if not isinstance(hashes, dict) or set(hashes) != {
        "initial_request", "aggregate_grant", "lineage_refusal", "ordinary_request",
    } or any(not isinstance(item, str) or len(item) != 64 for item in hashes.values()):
        raise ValueError("Qualification fixture inventory is invalid")
    return value


def read_external_authority_qualification_schema() -> dict[str, Any]:
    return json.loads(read_resource_text(SCHEMA_RESOURCE))


def _contract_fixtures() -> dict[str, dict[str, Any]]:
    wave, documents = _wave("exact_natal")
    actions = [{
        "action_id": member["action_id"], "binding": deepcopy(document["binding"]),
        "binding_sha256": member["binding_sha256"],
    } for member, document in zip(wave["ordered_members"], documents, strict=True)]
    wave_context = {
        "wave_id": wave["wave_id"], "wave_sha256": wave["wave_sha256"],
        "route_contract": wave["route_contract"],
        "assignment_sha256": wave["assignment_sha256"],
        "profile_sha256": wave["profile_sha256"], "member_count": 6,
        "ordered_member_binding_sha256s": [
            member["binding_sha256"] for member in wave["ordered_members"]
        ],
    }
    request = build_external_authority_request(
        run_id=wave["run_id"], observation=_observation(), actions=actions,
        initial_wave=wave_context,
    )
    grant, member_documents = _grant(request)
    validate_external_authority_request(request)
    validate_external_authority_grant(request, grant, member_documents)
    refusal = build_external_authority_refusal(
        run_id=wave["run_id"], observation=_observation(),
        reason_code="initial_wave_lineage_unjoinable",
        evidence_categories=("prior_initial_action", "native_evidence_conflict"),
    )
    validate_external_authority_refusal(refusal)
    ordinary = build_external_authority_request(
        run_id=wave["run_id"], observation=_observation(3), actions=[actions[0]],
    )
    ordinary_grant, ordinary_documents = _grant(ordinary)
    validate_external_authority_grant(ordinary, ordinary_grant, ordinary_documents)
    return {"initial_request": request, "aggregate_grant": grant,
            "lineage_refusal": refusal, "ordinary_request": ordinary}


def run_external_authority_qualification(*, fixture_dir: Path | None = None) -> dict[str, Any]:
    fixtures = _contract_fixtures()
    with tempfile.TemporaryDirectory(prefix="sbe-external-authority-qa-") as temporary:
        root = Path(temporary).resolve()
        run_dir, authority_dir = root / "run", root / "authority"
        counter_path = root / "provider-counter.json"
        authority_dir.mkdir()
        _prepare_exact_workspace(run_dir)

        inspection = inspect_lifecycle(
            run_dir, native_exclusive_access="declared",
            observed_at="2026-01-01T00:00:00Z",
        )
        request = read_external_authority_request(
            run_dir, observation=inspection["observation"],
        )
        if inspection.get("schema_version") != "astrowoof.authoring_lifecycle_inspection.v0.5":
            raise RuntimeError("Qualification did not use lifecycle inspection v0.5")
        if inspection["external_authority_request"] != request:
            raise RuntimeError("Lifecycle and public authority readers disagree")
        grant, documents = _grant(request)
        validate_external_authority_grant(request, grant, documents)
        for name, value in (("request", request), ("grant", grant),
                            ("member-authorizations", documents)):
            (authority_dir / f"{name}.json").write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        executed = _run_child("execute", str(run_dir), str(authority_dir), str(counter_path))
        replay = _run_child("replay", str(run_dir), str(authority_dir), str(counter_path))
        reconciled = _run_child("reconcile", str(run_dir), str(counter_path))
        counter = json.loads(counter_path.read_text(encoding="utf-8"))

        lineage_dir = root / "unjoinable"
        _prepare_exact_workspace(lineage_dir)
        lineage_state = load_json(lineage_dir / "run.json")
        lineage_state.pop("initial_authoring_wave")
        save_state(lineage_dir / "run.json", lineage_state)
        lineage_inspection = inspect_lifecycle(
            lineage_dir, native_exclusive_access="declared",
            observed_at="2026-01-01T00:00:00Z",
        )
        lineage_refusal = lineage_inspection["external_authority_refusal"]

        ordinary_dir = root / "ordinary"
        ordinary_dir.mkdir()
        ordinary_provider = _provider(root / "ordinary-counter.json")
        ordinary_state = initial_run_state(
            input_package=ordinary_dir, run_dir=ordinary_dir, provider=ordinary_provider,
            max_attempts=1, sbe_manifest={"status": "pass", "subject_count": 0},
            specs=[], service_level="interactive",
            profile={"spend_policy": _qualification_spend_policy()},
        )
        binding = _binding("exact_natal", 1) | {
            "run_id": ordinary_state["run_id"], "stage": "polish",
            "route": "polish:qualification:attempt-001",
        }
        prepare_action(ordinary_state["spend_ledger"], binding)
        save_state(ordinary_dir / "run.json", ordinary_state)
        ordinary_request = read_external_authority_request(ordinary_dir)

        stale_refused = False
        stale = deepcopy(request)
        stale["observation"]["snapshot_sha256"] = "d" * 64
        try:
            validate_external_authority_grant(stale, grant, documents)
        except Exception:
            stale_refused = True

        assertions = {
            "fresh_initial_admission": request["request_kind"] == "initial_wave_admission"
            and request["action_count"] == 6,
            "fresh_worker_restore": executed["wave_state"] == "DETACHED"
            and len(executed["provider_ids"]) == 6,
            "retained_exact_replay": replay["refused"] is True
            and len(counter["creates"]) == 6,
            "conflicting_lineage_refusal":
                lineage_refusal["reason_code"] == "initial_wave_lineage_unjoinable"
                and lineage_inspection["external_authority_request"] is None,
            "stale_request_refusal": stale_refused,
            "ordinary_action_authorization":
                ordinary_request["request_kind"] == "ordinary_action_set"
                and ordinary_request["action_count"] == 1,
            "reconciliation_separated_from_create":
                reconciled["selected_command"] == "provider_reconciliation_cycle"
                and 1 <= reconciled["selected_action_count"] <= 4
                and reconciled["retrieved_action_count"] == reconciled["selected_action_count"]
                and len(counter["retrievals"]) == reconciled["retrieved_action_count"]
                and len(counter["creates"]) == 6,
        }

    if fixture_dir is not None:
        fixture_dir.mkdir(parents=True, exist_ok=True)
        for name, value in fixtures.items():
            (fixture_dir / f"{name.replace('_', '-')}.json").write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    try:
        installed_version = version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        installed_version = "source-tree"
    body = {
        "schema_version": RECEIPT_CONTRACT,
        "status": "pass" if all(assertions.values()) else "fail",
        "qualification_only": True, "provider_free": True,
        "network_required": False, "production_authority": False,
        "sbe_version": installed_version, "assertions": assertions,
        "fixture_hashes": {name: _digest(value) for name, value in fixtures.items()},
        "provider_create_count": 6, "provider_spend_usd": 0,
    }
    receipt = {**body, "receipt_sha256": _digest(body)}
    return validate_external_authority_qualification_receipt(receipt)


def _internal_main(args: list[str]) -> int:
    step, *values = args
    if step == "execute" and len(values) == 3:
        value = _internal_execute(Path(values[0]), Path(values[1]), Path(values[2]))
    elif step == "replay" and len(values) == 3:
        value = _internal_replay(Path(values[0]), Path(values[1]), Path(values[2]))
    elif step == "reconcile" and len(values) == 2:
        value = _internal_reconcile(Path(values[0]), Path(values[1]))
    else:
        raise ValueError("Invalid qualification-only internal step")
    print(json.dumps(value, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw[:1] == ["--internal-step"]:
        return _internal_main(raw[1:])
    parser = argparse.ArgumentParser(
        description="Run provider-free installed-wheel external-authority qualification.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fixtures-dir", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(raw)
    value = (read_external_authority_qualification_schema() if args.schema
             else run_external_authority_qualification(fixture_dir=args.fixtures_dir))
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
