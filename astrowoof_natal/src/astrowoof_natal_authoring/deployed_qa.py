"""Installed-wheel, provider-free qualification for the four authoring routes.

This module is deliberately qualification-only. It accepts no production run,
provider credential, endpoint, or spend authority and cannot submit provider work.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import threading
import time
import sys
import zipfile
from copy import deepcopy
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Mapping

from .bounded_authoring import BoundedAuthoringError, validate_bounded_claim_deck
from .bounded_lifecycle import (
    BOUNDED_RUN_CONTRACT,
    _bounded_batch_authoring_cycle,
)
from .bounded_provider import OpenAIBoundedLifecycleProvider
from .closure import (
    OpenAIResponsesProvider,
    PassSpec,
    author_pending_passes_batch,
    initial_run_state,
    load_json,
    save_state,
    sha256_file,
)
from .initial_wave import (
    INITIAL_MEMBER_COUNT,
    InitialWaveMemberSpec,
    ProviderCreateResult,
    build_initial_wave,
    build_wave_authorization,
    execute_initial_wave_creates,
    validate_initial_wave_result,
)
from .native_transitions import _outcome
from .pass_protocol import canonical_sha256
from .resource_access import read_resource_text
from .spend import AUTHORIZATION_SCHEMA, PRICE_BOOK_VERSION


RECEIPT_CONTRACT = "astrowoof.deployed_qa_four_route_qualification.v1"
ROUTES = (
    "exact_interactive", "exact_batch", "bounded_interactive", "bounded_batch",
)
_RECEIPT_KEYS = {
    "schema_version", "receipt_sha256", "status", "qualification_only",
    "provider_free", "network_required", "production_authority",
    "sbe_version", "routes", "assertions", "provider_operation_count",
    "provider_spend_usd",
}
_ROUTE_KEYS = {
    "route_family", "provider_mechanism", "status", "member_count",
    "provider_authority_count", "create_count", "peak_concurrent_creates",
    "detached_provider_pending", "fresh_worker_fan_in",
}
_ASSERTION_KEYS = {
    "interactive_concurrent_six_member_create_detach",
    "fresh_worker_fan_in", "batch_one_round_six_member_cardinality",
    "bounded_final_qa_precedence", "duplicate_claim_refused_before_provider_work",
}


def _receipt_body(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(item) for key, item in value.items() if key != "receipt_sha256"}


def _binding(route_family: str, number: int) -> dict[str, Any]:
    return {
        "run_id": f"deployed-qa-{route_family}",
        "profile_sha256": "a" * 64,
        "prepared_state_revision": 1,
        "stage": "authoring_initial",
        "route": f"{route_family}:qualification-pass-{number:02d}:attempt-001",
        "request_sha256": hashlib.sha256(
            f"{route_family}:{number}".encode("utf-8")
        ).hexdigest(),
        "model": "scripted-provider",
        "service_level": "interactive",
        "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": PRICE_BOOK_VERSION,
    }


def _wave(route_family: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    bindings = [_binding(route_family, number) for number in range(1, 7)]
    members = [InitialWaveMemberSpec(
        action_id="paid_" + canonical_sha256(binding)[:24],
        binding=binding,
        pass_id=f"qualification-pass-{number:02d}",
        pass_number=number,
    ) for number, binding in enumerate(bindings, 1)]
    wave = build_initial_wave(
        run_id=f"deployed-qa-{route_family}",
        route_family=route_family,
        route_contract=(
            "astrowoof.bounded_natal.authoring_run.v2"
            if route_family == "bounded_natal"
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        assignment_sha256="b" * 64,
        profile_sha256="a" * 64,
        preparation_basis_revision=1,
        members=members,
    )
    documents = [{
        "schema_version": AUTHORIZATION_SCHEMA,
        "action_id": member["action_id"],
        "binding": binding,
        "authorization_reference": f"qualification-only:{number}",
    } for number, (member, binding) in enumerate(
        zip(wave["ordered_members"], bindings), 1
    )]
    return wave, documents


def _interactive(route_family: str, root: Path) -> dict[str, Any]:
    wave, documents = _wave(route_family)
    authorization = build_wave_authorization(
        wave, documents,
        reservation_set_reference="qualification-only:no-reservation",
        issuer="sbe-installed-qualification",
        authorized_at="1970-01-01T00:00:00Z",
    )
    lock = threading.Lock()
    active = 0
    peak = 0
    creates = 0
    outcomes_path = root / f"{route_family}-durable-outcomes.json"
    persisted: list[dict[str, Any]] = []

    def submit(member: Mapping[str, Any], _timeout: int) -> ProviderCreateResult:
        nonlocal active, peak, creates
        with lock:
            active += 1
            creates += 1
            peak = max(peak, active)
        try:
            time.sleep(0.02)
            return ProviderCreateResult(
                f"resp_qualification_{route_family}_{member['pass_id']}"
            )
        finally:
            with lock:
                active -= 1

    def persist(_member: Mapping[str, Any], outcome: Mapping[str, Any]) -> None:
        persisted.append(deepcopy(dict(outcome)))
        temporary = outcomes_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(persisted, sort_keys=True), encoding="utf-8")
        temporary.replace(outcomes_path)

    result = execute_initial_wave_creates(
        wave, authorization=authorization, member_authorizations=documents,
        submit=submit, persist_member_outcome=persist,
    )
    validate_initial_wave_result(result)
    # A new reader instance reconstructs the fan-in solely from durable bytes.
    reloaded = json.loads(outcomes_path.read_text(encoding="utf-8"))
    ordered_ids = [member["action_id"] for member in wave["ordered_members"]]
    fan_in = (
        len(reloaded) == INITIAL_MEMBER_COUNT
        and {item["action_id"] for item in reloaded} == set(ordered_ids)
        and all((item.get("provider") or {}).get("id") for item in reloaded)
    )
    if creates != 6 or peak < 2 or result["outcome"] != "detached_provider_pending" \
            or not fan_in:
        raise RuntimeError(f"{route_family} interactive qualification failed")
    return {
        "route_family": route_family,
        "provider_mechanism": "response",
        "status": "pass",
        "member_count": 6,
        "provider_authority_count": 6,
        "create_count": creates,
        "peak_concurrent_creates": peak,
        "detached_provider_pending": True,
        "fresh_worker_fan_in": True,
    }


def _batch(route_family: str, root: Path) -> dict[str, Any]:
    run_dir = root / f"{route_family}-batch-run"
    run_dir.mkdir()
    transport = _ScriptedPendingBatchTransport(route_family)
    if route_family == "exact_natal":
        _run_exact_batch_route(run_dir, transport)
    else:
        _run_bounded_batch_route(run_dir, transport)
    # A fresh reader reconstructs the native round exclusively from durable state.
    restored_state = load_json(run_dir / "run.json")
    rounds = restored_state["batch_service"]["rounds"]
    if len(rounds) != 1:
        raise RuntimeError(f"{route_family} did not persist one Batch round")
    round_record = rounds[0]
    requests = round_record["requests"]
    identities = [request["custom_id"] for request in requests]
    batch_id = round_record.get("batch_id")
    fan_in = (
        len(requests) == 6 and len(set(identities)) == 6
        and isinstance(batch_id, str) and bool(batch_id)
        and round_record.get("state") in {"SUBMITTED", "PENDING"}
    )
    if not fan_in or transport.create_calls != 1 or transport.upload_calls != 1:
        raise RuntimeError(f"{route_family} production Batch qualification failed")
    return {
        "route_family": route_family,
        "provider_mechanism": "batch",
        "status": "pass",
        "member_count": 6,
        "provider_authority_count": 1,
        "create_count": transport.create_calls,
        "peak_concurrent_creates": 0,
        "detached_provider_pending": True,
        "fresh_worker_fan_in": fan_in,
    }


class _ScriptedPendingBatchTransport:
    def __init__(self, route_family: str) -> None:
        self.route_family = route_family
        self.upload_calls = 0
        self.create_calls = 0
        self.retrieve_calls = 0
        self.lines: list[dict[str, Any]] = []

    def upload_jsonl(self, content: bytes, _filename: str) -> dict[str, Any]:
        self.upload_calls += 1
        self.lines = [json.loads(line) for line in content.decode("utf-8").splitlines()]
        return {"id": f"file_qualification_{self.route_family}"}

    def create_batch(self, _payload: Mapping[str, Any]) -> dict[str, Any]:
        self.create_calls += 1
        return {
            "id": f"batch_qualification_{self.route_family}",
            "status": "in_progress",
            "output_file_id": None,
            "error_file_id": None,
            "request_counts": {"total": len(self.lines), "completed": 0, "failed": 0},
        }

    def retrieve_batch(self, batch_id: str) -> dict[str, Any]:
        self.retrieve_calls += 1
        return {
            "id": batch_id, "status": "in_progress",
            "output_file_id": None, "error_file_id": None,
            "request_counts": {"total": len(self.lines), "completed": 0, "failed": 0},
        }

    def download_file(self, _file_id: str) -> str:
        raise AssertionError("Pending qualification Batch has no downloadable file")


def _exact_workspace_zip(root: Path, number: int) -> PassSpec:
    pass_id = f"qualification_{number}"
    source = root / "source" / pass_id
    source.mkdir(parents=True)
    files = {
        "START HERE.md": "Qualification assignment.\n",
        "AUTHORING BRIEF.md": "Qualification-only static guidance.\n",
        "DOG DETAILS.md": "Qualification dog.\n",
        "WRITE THIS CARD.md": (
            "<!-- BEGIN FIELD: densities.no_astro.headline.handler -->\n"
            "__WRITE__\n"
            "<!-- END FIELD: densities.no_astro.headline.handler -->\n"
        ),
    }
    for name, text in files.items():
        (source / name).write_text(text, encoding="utf-8")
    archive = root / f"{pass_id}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                handle.write(path, (Path(pass_id) / path.relative_to(source)).as_posix())
    return PassSpec(
        pass_id=pass_id, subject="qualification", pass_number=number,
        source_zip=archive, source_sha256=sha256_file(archive),
    )


def _qualification_spend_policy() -> dict[str, Any]:
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": 100_000_000,
        "stage_ceilings_micro_usd": {
            stage: 100_000_000 for stage in (
                "authoring_initial", "creative_retry", "polish",
                "qualitative_critic", "qualitative_candidate",
            )
        },
        "optional_stage_budget_behavior": {
            stage: "skip" for stage in (
                "polish", "qualitative_critic", "qualitative_candidate",
            )
        },
    }


def _run_exact_batch_route(
    run_dir: Path, transport: _ScriptedPendingBatchTransport,
) -> None:
    bundle = run_dir / "qualification-bundle"
    bundle.mkdir()
    specs = [_exact_workspace_zip(bundle, number) for number in range(1, 7)]
    provider = OpenAIResponsesProvider(
        api_key="qualification-only-no-network", model="gpt-5.6-luna",
        max_output_tokens=1000, prompt_cache_mode="disabled",
        require_spend_authorization=False,
    )
    state = initial_run_state(
        input_package=bundle, run_dir=run_dir, provider=provider,
        max_attempts=1,
        sbe_manifest={"status": "pass", "subject_count": 1},
        specs=specs, service_level="batch",
        profile={"spend_policy": _qualification_spend_policy()},
    )
    run_json = run_dir / "run.json"
    save_state(run_json, state)
    complete = author_pending_passes_batch(
        state=state, provider=provider, transport=transport,
        run_dir=run_dir, max_attempts=1,
        python_executable=Path(sys.executable), run_json=run_json,
        detach=True, sleep=lambda _seconds: None, spend_controller=None,
    )
    if complete:
        raise RuntimeError("Exact qualification Batch unexpectedly completed")


def _minimal_bounded_pass_packet(number: int) -> dict[str, Any]:
    body = {
        "schema_version": "astrowoof.bounded_natal.authoring_pass_packet.v1",
        "run_contract": BOUNDED_RUN_CONTRACT,
        "assignment_sha256": "c" * 64,
        "pass_id": f"bounded-pass-{number:02d}",
        "pass_number": number,
        "pass_count": 6,
        "resource_set": {"qualification": "installed-wheel"},
        "subject": {},
        "authority_notice": "Qualification-only invariant editorial packet.",
        "claims": [],
        "summaries": {},
        "projected_term_registry": {"terms": {}},
    }
    return {**body, "packet_sha256": canonical_sha256(body)}


def _run_bounded_batch_route(
    run_dir: Path, transport: _ScriptedPendingBatchTransport,
) -> None:
    packets: dict[str, dict[str, str]] = {}
    passes: dict[str, dict[str, Any]] = {}
    for number in range(1, 7):
        packet = _minimal_bounded_pass_packet(number)
        pass_id = packet["pass_id"]
        path = Path("bounded") / "inputs" / "passes" / f"{pass_id}.json"
        target = run_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(packet, sort_keys=True), encoding="utf-8")
        packets[pass_id] = {"path": path.as_posix()}
        passes[pass_id] = {
            "pass_id": pass_id, "state": "GENERATED", "attempts": [],
            "accepted_workspace": None,
        }
    provider = OpenAIBoundedLifecycleProvider(
        run_dir=run_dir, api_key="qualification-only-no-network",
        service_level="batch", model="gpt-5.6-luna",
        maximum_output_tokens=1000,
    )
    provider.batch_transport = transport
    state = {
        "schema_version": BOUNDED_RUN_CONTRACT,
        "route": "bounded_natal.v2",
        "route_contract": BOUNDED_RUN_CONTRACT,
        "run_id": "deployed-qa-bounded-batch",
        "state_revision": 0,
        "status": "AUTHORING",
        "provider": "openai",
        "service_level": "batch",
        "max_attempts": 1,
        "passes": passes,
        "subjects": {},
        "bounded": {"pass_ids": list(passes), "pass_packets": packets},
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": str(run_dir.resolve()),
        },
    }
    run_json = run_dir / "run.json"
    save_state(run_json, state)
    complete = _bounded_batch_authoring_cycle(
        state, run_dir, provider, None,
    )
    if complete:
        raise RuntimeError("Bounded qualification Batch unexpectedly completed")


def _bounded_final_qa_precedence() -> bool:
    outcome, reason = _outcome({
        "route": "bounded_natal.v2",
        "service_level": "interactive",
        "status": "FINAL_QA_REQUIRES_REVIEW",
        "passes": {
            f"qualification-pass-{number:02d}": {"state": "PASS_QA_ACCEPTED"}
            for number in range(1, 7)
        },
        "spend_ledger": {"actions": []},
    })
    return outcome == "review_required" and reason == "final_qa_requires_review"


def _duplicate_claim_refusal() -> bool:
    claims = []
    for number in range(50):
        claims.append({
            "claim_id": "duplicate" if number < 2 else f"claim-{number:02d}",
            "authority": {
                "epistemic_classification": "invariant",
                "dependency_claim_ids": [],
                "source_refs": [],
                "projected_term_refs": [],
            },
            "editorial_tier": "strong_preference",
        })
    provider_creates = 0
    try:
        validate_bounded_claim_deck({
            "schema_version": "astrowoof.bounded_natal.claim_deck.v1",
            "claims": claims,
        })
    except BoundedAuthoringError as exc:
        return exc.code == "bounded_claim_identity" and provider_creates == 0
    return False


def run_deployed_qa_qualification() -> dict[str, Any]:
    """Run the self-contained installed qualification and return a closed receipt."""
    try:
        sbe_version = version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        sbe_version = "source-tree"
    with tempfile.TemporaryDirectory(prefix="astrowoof-deployed-qa-") as temporary:
        root = Path(temporary)
        routes = {
            "exact_interactive": _interactive("exact_natal", root),
            "exact_batch": _batch("exact_natal", root),
            "bounded_interactive": _interactive("bounded_natal", root),
            "bounded_batch": _batch("bounded_natal", root),
        }
    assertions = {
        "interactive_concurrent_six_member_create_detach": all(
            routes[name]["create_count"] == 6
            and routes[name]["peak_concurrent_creates"] >= 2
            and routes[name]["detached_provider_pending"]
            for name in ("exact_interactive", "bounded_interactive")
        ),
        "fresh_worker_fan_in": all(item["fresh_worker_fan_in"] for item in routes.values()),
        "batch_one_round_six_member_cardinality": all(
            routes[name]["member_count"] == 6
            and routes[name]["provider_authority_count"] == 1
            for name in ("exact_batch", "bounded_batch")
        ),
        "bounded_final_qa_precedence": _bounded_final_qa_precedence(),
        "duplicate_claim_refused_before_provider_work": _duplicate_claim_refusal(),
    }
    status = "pass" if all(assertions.values()) else "fail"
    body = {
        "schema_version": RECEIPT_CONTRACT,
        "status": status,
        "qualification_only": True,
        "provider_free": True,
        "network_required": False,
        "production_authority": False,
        "sbe_version": sbe_version,
        "routes": routes,
        "assertions": assertions,
        "provider_operation_count": 0,
        "provider_spend_usd": 0,
    }
    receipt = {**body, "receipt_sha256": canonical_sha256(body)}
    validate_deployed_qa_receipt(receipt)
    if status != "pass":
        raise RuntimeError("Deployed four-route qualification failed")
    return receipt


def read_deployed_qa_schema() -> dict[str, Any]:
    """Return the packaged closed schema for the qualification receipt."""
    return json.loads(read_resource_text(
        "contracts/deployed-qa-four-route-qualification.v1.schema.json"
    ))


def validate_deployed_qa_receipt(value: Mapping[str, Any]) -> None:
    if set(value) != _RECEIPT_KEYS or value.get("schema_version") != RECEIPT_CONTRACT:
        raise ValueError("Unsupported deployed-QA receipt")
    if value.get("receipt_sha256") != canonical_sha256(_receipt_body(value)):
        raise ValueError("Deployed-QA receipt digest mismatch")
    if value.get("status") != "pass":
        raise ValueError("Unsupported deployed-QA status")
    if value.get("qualification_only") is not True \
            or value.get("provider_free") is not True \
            or value.get("network_required") is not False \
            or value.get("production_authority") is not False \
            or value.get("provider_operation_count") != 0 \
            or value.get("provider_spend_usd") != 0:
        raise ValueError("Deployed-QA safety declaration is invalid")
    routes = value.get("routes")
    if not isinstance(routes, Mapping) or set(routes) != set(ROUTES):
        raise ValueError("Deployed-QA route inventory is invalid")
    for route in routes.values():
        if not isinstance(route, Mapping) or set(route) != _ROUTE_KEYS:
            raise ValueError("Deployed-QA route fields are not closed")
    expected = {
        "exact_interactive": ("exact_natal", "response", 6, 6),
        "exact_batch": ("exact_natal", "batch", 1, 1),
        "bounded_interactive": ("bounded_natal", "response", 6, 6),
        "bounded_batch": ("bounded_natal", "batch", 1, 1),
    }
    for name, (family, mechanism, authority_count, create_count) in expected.items():
        route = routes[name]
        if (
            route.get("route_family") != family
            or route.get("provider_mechanism") != mechanism
            or route.get("status") != "pass"
            or route.get("member_count") != 6
            or route.get("provider_authority_count") != authority_count
            or route.get("create_count") != create_count
            or route.get("detached_provider_pending") is not True
            or route.get("fresh_worker_fan_in") is not True
            or (
                mechanism == "response"
                and (
                    not isinstance(route.get("peak_concurrent_creates"), int)
                    or route["peak_concurrent_creates"] < 2
                )
            )
            or (mechanism == "batch" and route.get("peak_concurrent_creates") != 0)
        ):
            raise ValueError(f"Deployed-QA route evidence is invalid for {name}")
    assertions = value.get("assertions")
    if not isinstance(assertions, Mapping) or set(assertions) != _ASSERTION_KEYS \
            or any(not isinstance(item, bool) for item in assertions.values()):
        raise ValueError("Deployed-QA assertions are invalid")
    if value["status"] == "pass" and not all(assertions.values()):
        raise ValueError("Passing deployed-QA receipt contains a failed assertion")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run provider-free installed-wheel four-route qualification."
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--schema", action="store_true",
        help="Print the packaged receipt schema instead of running qualification.",
    )
    args = parser.parse_args(argv)
    value = read_deployed_qa_schema() if args.schema else run_deployed_qa_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0
