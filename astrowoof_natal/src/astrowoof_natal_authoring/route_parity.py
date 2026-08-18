"""Strict installed-resource readers for route-parity consumer evidence."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any

from .resource_access import read_resource_text


ROUTE_PARITY_ORACLE_SCHEMA = "astrowoof.route_parity_transition_oracle.v2"
ROUTE_PARITY_TRACES_SCHEMA = "astrowoof.bounded_route_parity_traces.v1"
_ORACLE_RESOURCE = "fixtures/lifecycle/route-parity-transition-oracle.v2.json"
_TRACES_RESOURCE = "fixtures/lifecycle/bounded-route-parity-traces.v1.json"
_ROUTES = {"exact_natal", "bounded_natal"}
_MECHANISMS = {"none", "response", "batch"}
_OUTCOMES = {
    "awaiting_external_authority", "detached_provider_pending", "not_due",
    "progressed_local", "ambiguous_submission", "provider_failed",
    "terminal_failure", "delivery_complete",
}
_CAPACITY = {
    None, "continue_local_cycle", "release_until_due",
    "await_external_authority", "retain_for_review", "terminal",
    "unsupported_retain_capacity",
}
_COST = {
    "provider_usage_reported",
    "provider_usage_unavailable_billing_reconciliation_pending",
    "no_provider_work_consumed", "not_applicable_provider_pending",
}
_AUTHORITY_REASONS = {
    None, "provider_operation_pending", "provider_output_integrity_review",
    "provider_submission_ambiguous", "billing_reconciliation_pending",
}
_SCENARIO_KEYS = {
    "name", "native_route", "cycle_outcome", "capacity_disposition",
    "provider_request_allowed", "mutation_allowed", "retain_provider_custody",
    "retain_consumer_authority", "consumer_authority_reason", "cost_disposition",
    "local_continuation", "reason_code", "observed_run_contract",
    "provider_evidence_present",
}


def _object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly {sorted(keys)}")
    return value


def validate_route_parity_oracle(value: Any) -> dict[str, Any]:
    """Validate and return the strict, closed route-parity oracle v2."""
    root = _object(value, {"schema_version", "public_vocabulary_change", "scenarios"}, "oracle")
    if root["schema_version"] != ROUTE_PARITY_ORACLE_SCHEMA:
        raise ValueError("Unsupported route-parity oracle schema")
    if root["public_vocabulary_change"] is not False:
        raise ValueError("Oracle v2 must reuse the public lifecycle vocabulary")
    scenarios = root["scenarios"]
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("Oracle scenarios must be a non-empty array")
    names: set[str] = set()
    for index, raw in enumerate(scenarios):
        item = _object(raw, _SCENARIO_KEYS, f"scenario[{index}]")
        name = item["name"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("Oracle scenario names must be unique non-empty strings")
        names.add(name)
        route = _object(item["native_route"], {"route_family", "provider_operation_kind"}, f"scenario[{index}].native_route")
        if route["route_family"] not in _ROUTES or route["provider_operation_kind"] not in _MECHANISMS:
            raise ValueError("Oracle native route is outside the closed vocabulary")
        if item["cycle_outcome"] not in _OUTCOMES or item["capacity_disposition"] not in _CAPACITY:
            raise ValueError("Oracle lifecycle value is outside the closed vocabulary")
        if item["cost_disposition"] not in _COST or item["consumer_authority_reason"] not in _AUTHORITY_REASONS:
            raise ValueError("Oracle authority/cost value is outside the closed vocabulary")
        for key in ("provider_request_allowed", "mutation_allowed", "retain_provider_custody", "retain_consumer_authority"):
            if not isinstance(item[key], bool):
                raise ValueError(f"Oracle {key} must be boolean")
        for key in ("local_continuation", "reason_code", "observed_run_contract"):
            if item[key] is not None and not isinstance(item[key], str):
                raise ValueError(f"Oracle {key} must be string or null")
        if item["provider_evidence_present"] is not None and not isinstance(item["provider_evidence_present"], bool):
            raise ValueError("Oracle provider_evidence_present must be boolean or null")
    return root


def validate_bounded_route_traces(value: Any) -> dict[str, Any]:
    """Validate route-specific traces without treating them as native authority."""
    root = _object(value, {"schema_version", "authority", "traces"}, "trace bundle")
    if root["schema_version"] != ROUTE_PARITY_TRACES_SCHEMA or root["authority"] != "consumer_adoption_evidence_only":
        raise ValueError("Unsupported bounded route trace contract")
    traces = root["traces"]
    if not isinstance(traces, list) or not traces:
        raise ValueError("Trace bundle must contain traces")
    names: set[str] = set()
    for index, trace in enumerate(traces):
        trace = _object(trace, {"name", "route_family", "provider_operation_kind", "steps"}, f"trace[{index}]")
        if trace["name"] in names or not isinstance(trace["name"], str):
            raise ValueError("Trace names must be unique strings")
        names.add(trace["name"])
        if trace["route_family"] != "bounded_natal" or trace["provider_operation_kind"] not in {"response", "batch"}:
            raise ValueError("Trace route identity is invalid")
        if not isinstance(trace["steps"], list) or not trace["steps"]:
            raise ValueError("Trace steps must be non-empty")
        for number, step in enumerate(trace["steps"], start=1):
            step = _object(step, {"sequence", "outcome", "capacity_disposition", "retain_provider_custody", "retain_consumer_authority", "cost_disposition", "reason_code"}, f"trace[{index}].step")
            if step["sequence"] != number or step["outcome"] not in _OUTCOMES or step["capacity_disposition"] not in _CAPACITY or step["cost_disposition"] not in _COST:
                raise ValueError("Trace step is not ordered or uses an unknown value")
            if not isinstance(step["retain_provider_custody"], bool) or not isinstance(step["retain_consumer_authority"], bool):
                raise ValueError("Trace custody fields must be boolean")
            if step["reason_code"] is not None and not isinstance(step["reason_code"], str):
                raise ValueError("Trace reason_code must be string or null")
    return root


def read_route_parity_oracle() -> dict[str, Any]:
    return validate_route_parity_oracle(json.loads(read_resource_text(_ORACLE_RESOURCE)))


def read_bounded_route_parity_traces() -> dict[str, Any]:
    return validate_bounded_route_traces(json.loads(read_resource_text(_TRACES_RESOURCE)))


def main() -> None:
    """Export one validated, provider-free installed consumer evidence resource."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("oracle", "bounded-traces"), required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    value = (
        read_route_parity_oracle()
        if args.kind == "oracle"
        else read_bounded_route_parity_traces()
    )
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
