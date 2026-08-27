"""Provider-free composition of existing production-path qualification receipts."""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256
from typing import Any, Callable, Mapping

from .deployed_qa import run_deployed_qa_qualification, validate_deployed_qa_receipt
from .external_authority_v2_qa import (
    run_external_authority_v2_qualification,
    validate_external_authority_v2_qualification,
)
from .post_fan_in_qa import (
    run_provider_pending_lifecycle_qualification_v2,
    validate_provider_pending_lifecycle_qualification_v2,
)


CONTRACT = "astrowoof.adversarial_route_matrix_qualification.v1"
_ROUTES = ("exact_natal", "bounded_natal")
_ORDINARY_STAGES = (
    "creative_retry", "polish", "qualitative_critic", "qualitative_candidate",
)
_CELL_KEYS = {
    "cell_id", "route_family", "provider_mechanism", "stage", "classification",
    "evidence_contract", "evidence_receipt_sha256", "assertion",
}


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _cell(
    route: str,
    mechanism: str,
    stage: str,
    classification: str,
    receipt: Mapping[str, Any],
    assertion: str,
) -> dict[str, Any]:
    return {
        "cell_id": f"{route}:{mechanism}:{stage}",
        "route_family": route,
        "provider_mechanism": mechanism,
        "stage": stage,
        "classification": classification,
        "evidence_contract": receipt["schema_version"],
        "evidence_receipt_sha256": receipt["receipt_sha256"],
        "assertion": assertion,
    }


def build_adversarial_route_matrix_qualification(
    *,
    deployed_runner: Callable[[], dict[str, Any]] = run_deployed_qa_qualification,
    authority_runner: Callable[[], dict[str, Any]] = run_external_authority_v2_qualification,
    post_fan_in_runner: Callable[[], dict[str, Any]] = run_provider_pending_lifecycle_qualification_v2,
) -> dict[str, Any]:
    """Run and join the real provider-free qualification surfaces.

    Runner injection exists only so the closed join can be tested cheaply. The
    defaults always execute the packaged production-path qualification functions.
    """

    deployed = deployed_runner()
    validate_deployed_qa_receipt(deployed)
    authority = authority_runner()
    validate_external_authority_v2_qualification(authority)
    post_fan_in = post_fan_in_runner()
    validate_provider_pending_lifecycle_qualification_v2(post_fan_in)
    cells: list[dict[str, Any]] = []
    for route in _ROUTES:
        deployed_prefix = "exact" if route == "exact_natal" else "bounded"
        cells.append(_cell(
            route, "response", "authoring_initial", "supported", deployed,
            f"routes.{deployed_prefix}_interactive",
        ))
        cells.append(_cell(
            route, "batch", "authoring_initial", "supported", deployed,
            f"routes.{deployed_prefix}_batch",
        ))
        cells.append(_cell(
            route, "local", "post_fan_in", "supported", post_fan_in,
            f"route_results.{route}",
        ))
        for stage in _ORDINARY_STAGES:
            cells.append(_cell(
                route, "response", stage, "supported", authority,
                f"routes.{route}.stage_outcomes.{stage}",
            ))
            cells.append(_cell(
                route, "batch", stage, "explicitly_refused", authority,
                "assertions.ordinary_batch_explicitly_deferred",
            ))
    body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "external_network_call_count": 0,
        "real_provider_create_count": 0,
        "provider_spend_usd": 0,
        "source_receipts": [
            {
                "schema_version": item["schema_version"],
                "receipt_sha256": item["receipt_sha256"],
            }
            for item in (deployed, authority, post_fan_in)
        ],
        "cells": cells,
    }
    return validate_adversarial_route_matrix_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_adversarial_route_matrix_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "real_provider_create_count",
        "provider_spend_usd", "source_receipts", "cells",
    }
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != CONTRACT:
        raise ValueError("Adversarial route-matrix receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Adversarial route-matrix receipt digest mismatch")
    if (
        value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("real_provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
    ):
        raise ValueError("Adversarial route-matrix safety declaration is invalid")
    sources = value.get("source_receipts")
    if not isinstance(sources, list) or len(sources) != 3:
        raise ValueError("Adversarial route-matrix source receipt inventory is invalid")
    for source in sources:
        if (
            not isinstance(source, Mapping)
            or set(source) != {"schema_version", "receipt_sha256"}
            or not isinstance(source["schema_version"], str)
            or not isinstance(source["receipt_sha256"], str)
            or len(source["receipt_sha256"]) != 64
        ):
            raise ValueError("Adversarial route-matrix source receipt is invalid")
    cells = value.get("cells")
    expected_count = len(_ROUTES) * (3 + 2 * len(_ORDINARY_STAGES))
    if not isinstance(cells, list) or len(cells) != expected_count:
        raise ValueError("Adversarial route-matrix cell inventory is incomplete")
    seen: set[str] = set()
    source_digests = {item["receipt_sha256"] for item in sources}
    expected_classifications: dict[str, str] = {}
    for route in _ROUTES:
        expected_classifications[f"{route}:response:authoring_initial"] = "supported"
        expected_classifications[f"{route}:batch:authoring_initial"] = "supported"
        expected_classifications[f"{route}:local:post_fan_in"] = "supported"
        for stage in _ORDINARY_STAGES:
            expected_classifications[f"{route}:response:{stage}"] = "supported"
            expected_classifications[f"{route}:batch:{stage}"] = "explicitly_refused"
    for cell in cells:
        if not isinstance(cell, Mapping) or set(cell) != _CELL_KEYS:
            raise ValueError("Adversarial route-matrix cell fields are not exact")
        identity = f"{cell['route_family']}:{cell['provider_mechanism']}:{cell['stage']}"
        if (
            cell.get("cell_id") != identity
            or cell.get("route_family") not in _ROUTES
            or cell.get("provider_mechanism") not in {"response", "batch", "local"}
            or cell.get("classification") != expected_classifications.get(identity)
            or not isinstance(cell.get("evidence_contract"), str)
            or cell.get("evidence_receipt_sha256") not in source_digests
            or not isinstance(cell.get("assertion"), str)
            or not cell["assertion"]
            or identity in seen
        ):
            raise ValueError("Adversarial route-matrix cell identity is invalid")
        seen.add(identity)
    if seen != set(expected_classifications):
        raise ValueError("Adversarial route-matrix cell inventory is incomplete")
    return deepcopy(dict(value))
