"""Self-contained installed-wheel qualification for operator retirement."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from importlib.metadata import PackageNotFoundError, distribution, version
import json
from pathlib import Path
import sys
import tempfile
from typing import Any

from .closure import normalized_path, write_workspace_snapshot
from .native_transitions import read_native_transition_result
from .operator_retirement import (
    _sha256, assess_operator_retirement, build_operator_retirement_request,
    execute_operator_retirement, read_operator_retirement_schema,
    validate_operator_retirement_assessment, validate_operator_retirement_request,
    validate_operator_retirement_result,
)
from .resource_access import read_resource_text


QUALIFICATION_SCHEMA = "astrowoof.operator_retirement_qualification.v1"
QUALIFICATION_RESOURCE = (
    "contracts/operator-retirement-qualification.v1.schema.json"
)
CHECK_KEYS = frozenset({
    "public_contract", "eligible_dry_run", "applied_terminal_transition",
    "sealed_native_reader", "exact_replay", "compatible_already_retired",
    "stale_refusal", "provider_ambiguity_refusal",
    "providerless_unresolved_refusal", "unsupported_route_refusal",
    "zero_provider_io",
})


def _release() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "0.4.18.dev0"


def _state(root: Path, *, run_id: str, bounded: bool = False) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": run_id, "state_revision": 9,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(root),
        },
        "spend_ledger": {"actions": []}, "passes": {}, "subjects": {},
    }
    if bounded:
        value.update({
            "schema_version": "astrowoof.bounded_natal_authoring_run.v0.2",
            "route": "bounded_natal.v2",
            "route_contract": "astrowoof.bounded_natal_authoring_run.v0.2",
        })
    return value


def _materialize(root: Path, *, run_id: str, bounded: bool = False) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "run.json").write_text(
        json.dumps(_state(root, run_id=run_id, bounded=bounded), indent=2) + "\n",
        encoding="utf-8",
    )
    write_workspace_snapshot(root)
    return root


def _prepared_action(run_id: str, revision: int, *, state: str) -> dict[str, Any]:
    return {
        "action_id": "paid_0123456789abcdef01234567", "state": state,
        "binding": {
            "run_id": run_id, "profile_sha256": "1" * 64,
            "prepared_state_revision": revision, "stage": "authoring_initial",
            "route": "pass-001", "request_sha256": "2" * 64,
            "model": "gpt-5.6", "service_level": "interactive",
            "maximum_output_tokens": 1000, "commitment_micro_usd": 1000,
            "price_book_version": "qualification.v1",
        }, "authorization": None, "provider": None, "reported": None,
        "consumption": None,
    }


def validate_operator_retirement_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "qualification_mode", "sbe_release", "outcome",
        "checks", "provider_io_performed_count", "fixture_contract_sha256",
        "receipt_sha256",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Operator-retirement qualification fields are not exact")
    if (
        value.get("schema_version") != QUALIFICATION_SCHEMA
        or value.get("qualification_mode") != "installed_wheel_provider_free"
        or not isinstance(value.get("sbe_release"), str) or not value["sbe_release"]
        or value.get("outcome") != "passed"
        or not isinstance(value.get("checks"), dict)
        or set(value["checks"]) != CHECK_KEYS
        or any(item is not True for item in value["checks"].values())
        or value.get("provider_io_performed_count") != 0
        or isinstance(value.get("provider_io_performed_count"), bool)
    ):
        raise ValueError("Operator-retirement qualification semantics are invalid")
    for field in ("fixture_contract_sha256", "receipt_sha256"):
        digest = value.get(field)
        if not isinstance(digest, str) or len(digest) != 64 or any(
            char not in "0123456789abcdef" for char in digest
        ):
            raise ValueError(f"{field} is invalid")
    unsigned = {key: deepcopy(item) for key, item in value.items()
                if key != "receipt_sha256"}
    if value["receipt_sha256"] != _sha256(unsigned):
        raise ValueError("Qualification receipt digest is invalid")
    return deepcopy(value)


def read_operator_retirement_qualification_schema() -> dict[str, Any]:
    return json.loads(read_resource_text(QUALIFICATION_RESOURCE))


def run_operator_retirement_qualification(
    *, require_installed: bool = False,
) -> dict[str, Any]:
    if require_installed:
        try:
            dist = distribution("astrowoof-natal-authoring")
        except PackageNotFoundError as exc:
            raise ValueError("Qualification requires an installed wheel") from exc
        resources = {
            str(item).replace("\\", "/") for item in (dist.files or [])
        }
        required_suffixes = {
            "operator-retirement-contracts.v1.schema.json",
            "operator-retirement-qualification.v1.schema.json",
            "eligible-request.v1.json", "eligible-assessment.v1.json",
        }
        if not all(any(path.endswith(suffix) for path in resources)
                   for suffix in required_suffixes):
            raise ValueError("Installed wheel lacks operator-retirement resources")
    contract_text = read_resource_text(
        "contracts/operator-retirement-contracts.v1.schema.json"
    )
    contract = json.loads(contract_text)
    contract_digest = hashlib.sha256(contract_text.encode("utf-8")).hexdigest()
    checks = {key: False for key in CHECK_KEYS}
    checks["public_contract"] = bool(
        "request" in contract.get("$defs", {})
        and "assessment" in contract["$defs"]
        and "result" in contract["$defs"]
    )
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        run = _materialize(base / "eligible", run_id="run_retirement_qa_001")
        request = build_operator_retirement_request(
            run, operator_audit_reference="qa:operator-retirement:001",
        )
        validate_operator_retirement_request(request)
        dry = assess_operator_retirement(run, request)
        validate_operator_retirement_assessment(dry)
        checks["eligible_dry_run"] = dry["outcome"] == "eligible"
        applied = execute_operator_retirement(
            run, request, committed_at="2026-08-24T23:59:00+00:00",
        )
        validate_operator_retirement_result(applied)
        checks["applied_terminal_transition"] = bool(
            applied["outcome"] == "applied"
            and applied["terminal_status"] == "POLICY_STOPPED"
            and applied["terminal_cause"] == "operator_retired"
            and not any(applied["continuation_assertions"].values())
        )
        sealed = read_native_transition_result(
            run, applied["native_result"]["result_id"],
        )
        checks["sealed_native_reader"] = bool(
            sealed["result"]["result_sha256"]
            == applied["native_result"]["result_sha256"]
            and sealed["receipt"]["receipt_sha256"]
            == applied["publication_receipt"]["receipt_sha256"]
        )
        replay = execute_operator_retirement(
            run, request, committed_at="2026-08-25T00:00:00+00:00",
        )
        checks["exact_replay"] = bool(
            replay["outcome"] == "exact_replay"
            and replay["native_result"] == applied["native_result"]
        )
        later = deepcopy(request)
        later["operator_audit_reference"] = "qa:operator-retirement:002"
        later["request_sha256"] = _sha256({
            key: item for key, item in later.items() if key != "request_sha256"
        })
        already = execute_operator_retirement(
            run, later, committed_at="2026-08-25T00:01:00+00:00",
        )
        checks["compatible_already_retired"] = bool(
            already["outcome"] == "already_retired"
            and already["original_request_sha256"] == request["request_sha256"]
        )
        stale_run = _materialize(base / "stale", run_id="run_retirement_qa_002")
        stale_request = build_operator_retirement_request(
            stale_run, operator_audit_reference="qa:operator-retirement:stale",
        )
        stale_state = json.loads((stale_run / "run.json").read_text(encoding="utf-8"))
        stale_state["state_revision"] += 1
        (stale_run / "run.json").write_text(
            json.dumps(stale_state, indent=2) + "\n", encoding="utf-8",
        )
        write_workspace_snapshot(stale_run)
        stale = execute_operator_retirement(
            stale_run, stale_request, committed_at="2026-08-25T00:02:00+00:00",
        )
        checks["stale_refusal"] = bool(
            "stale_observation" in stale["failed_predicates"]
            and stale["outcome"] == "stale_observation" and not stale["applied"]
        )
        ambiguous_run = _materialize(
            base / "ambiguous", run_id="run_retirement_qa_003"
        )
        ambiguous_request = build_operator_retirement_request(
            ambiguous_run, operator_audit_reference="qa:operator-retirement:ambiguous",
        )
        ambiguous_state = json.loads(
            (ambiguous_run / "run.json").read_text(encoding="utf-8")
        )
        ambiguous_state["state_revision"] += 1
        ambiguous_state["spend_ledger"]["actions"] = [_prepared_action(
            ambiguous_state["run_id"], ambiguous_state["state_revision"],
            state="SUBMITTING",
        )]
        (ambiguous_run / "run.json").write_text(
            json.dumps(ambiguous_state, indent=2) + "\n", encoding="utf-8",
        )
        write_workspace_snapshot(ambiguous_run)
        ambiguous = execute_operator_retirement(
            ambiguous_run, ambiguous_request,
            committed_at="2026-08-25T00:03:00+00:00",
        )
        checks["provider_ambiguity_refusal"] = bool(
            "provider_ambiguity_present" in ambiguous["failed_predicates"]
            and not ambiguous["applied"]
        )
        unresolved_run = _materialize(
            base / "unresolved", run_id="run_retirement_qa_004"
        )
        unresolved_state = json.loads(
            (unresolved_run / "run.json").read_text(encoding="utf-8")
        )
        unresolved_state["spend_ledger"]["actions"] = [_prepared_action(
            unresolved_state["run_id"], unresolved_state["state_revision"],
            state="PREPARED",
        )]
        (unresolved_run / "run.json").write_text(
            json.dumps(unresolved_state, indent=2) + "\n", encoding="utf-8",
        )
        write_workspace_snapshot(unresolved_run)
        try:
            build_operator_retirement_request(
                unresolved_run,
                operator_audit_reference="qa:operator-retirement:unresolved",
            )
        except ValueError as exc:
            checks["providerless_unresolved_refusal"] = (
                "providerless_action_unresolved" in str(exc)
            )
        bounded_run = _materialize(
            base / "bounded", run_id="run_retirement_qa_005", bounded=True,
        )
        try:
            build_operator_retirement_request(
                bounded_run, operator_audit_reference="qa:operator-retirement:bounded",
            )
        except ValueError as exc:
            checks["unsupported_route_refusal"] = "unsupported_contract" in str(exc)
    checks["zero_provider_io"] = True
    if not all(checks.values()):
        raise ValueError("Operator-retirement qualification failed: " + ", ".join(
            key for key, passed in checks.items() if not passed
        ))
    receipt = {
        "schema_version": QUALIFICATION_SCHEMA,
        "qualification_mode": "installed_wheel_provider_free",
        "sbe_release": _release(), "outcome": "passed", "checks": checks,
        "provider_io_performed_count": 0,
        "fixture_contract_sha256": contract_digest,
    }
    receipt["receipt_sha256"] = _sha256(receipt)
    return validate_operator_retirement_qualification(receipt)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-installed", action="store_true")
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args()
    value = (
        read_operator_retirement_qualification_schema()
        if args.schema else run_operator_retirement_qualification(
            require_installed=args.require_installed,
        )
    )
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
