"""Installed provider-free lifecycle adversarial qualification surface."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from .adversarial_campaign import run_seeded_campaign_qualification
from .adversarial_explorer import run_systematic_explorer_qualification
from .adversarial_route_matrix import build_adversarial_route_matrix_qualification
from .adversarial_trace import FIXTURE_NAMES, canonical_adversarial_trace_bytes, read_adversarial_trace_fixture


CONTRACT = "astrowoof.lifecycle_adversarial_qualification.v1"
SCHEMA_RESOURCE = "lifecycle-adversarial-qualification.v1.schema.json"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def read_adversarial_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        SCHEMA_RESOURCE,
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def run_adversarial_qualification() -> dict[str, Any]:
    matrix = build_adversarial_route_matrix_qualification()
    explorer = run_systematic_explorer_qualification()
    campaign = run_seeded_campaign_qualification()
    corpus = [read_adversarial_trace_fixture(name) for name in sorted(FIXTURE_NAMES)]
    corpus_digest = sha256(b"".join(
        canonical_adversarial_trace_bytes(item) for item in corpus
    )).hexdigest()
    components = [matrix, explorer, campaign]
    body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "package": {
            "name": "astrowoof-natal-authoring",
            "version": _package_version(),
        },
        "schema_sha256": _digest(read_adversarial_qualification_schema()),
        "corpus_sha256": corpus_digest,
        "fixture_count": len(corpus),
        "fixed_seeds": [item["seed"] for item in campaign["walks"]],
        "route_cell_count": len(matrix["cells"]),
        "transition_coverage": campaign["coverage"],
        "invariant_count": (
            len(matrix["cells"])
            + len(explorer["assertions"])
            + len(campaign["assertions"])
        ),
        "counterexample_refs": [
            "fixture:review-no-action-cycle",
            "fixture:noop-checkpoint-republish",
        ],
        "component_contracts": [
            {
                "schema_version": matrix["schema_version"],
                "evidence_sha256": _digest({
                    "cells": [{
                        "cell_id": item["cell_id"],
                        "classification": item["classification"],
                    } for item in matrix["cells"]],
                }),
            },
            {
                "schema_version": explorer["schema_version"],
                "evidence_sha256": _digest({
                    "max_depth": explorer["max_depth"],
                    "assertions": explorer["assertions"],
                }),
            },
            {
                "schema_version": campaign["schema_version"],
                "evidence_sha256": _digest({
                    "fixed_seeds": [item["seed"] for item in campaign["walks"]],
                    "coverage": campaign["coverage"],
                    "assertions": campaign["assertions"],
                }),
            },
        ],
        "external_network_call_count": 0,
        "real_provider_create_count": 0,
        "provider_spend_usd": 0,
    }
    return validate_adversarial_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_adversarial_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "schema_sha256", "corpus_sha256",
        "fixture_count", "fixed_seeds", "route_cell_count", "transition_coverage",
        "invariant_count", "counterexample_refs", "component_contracts",
        "external_network_call_count", "real_provider_create_count",
        "provider_spend_usd",
    }
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != CONTRACT:
        raise ValueError("Adversarial qualification receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Adversarial qualification receipt digest mismatch")
    if (
        value.get("status") != "pass" or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("real_provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
    ):
        raise ValueError("Adversarial qualification safety declaration is invalid")
    package = value.get("package")
    if not isinstance(package, Mapping) or set(package) != {"name", "version"} or package.get("name") != "astrowoof-natal-authoring" or not isinstance(package.get("version"), str):
        raise ValueError("Adversarial qualification package identity is invalid")
    for key in ("schema_sha256", "corpus_sha256"):
        item = value.get(key)
        if not isinstance(item, str) or len(item) != 64 or any(c not in "0123456789abcdef" for c in item):
            raise ValueError("Adversarial qualification digest is invalid")
    if value.get("fixture_count") != 3 or value.get("fixed_seeds") != [7, 19, 41] or value.get("route_cell_count") != 22:
        raise ValueError("Adversarial qualification coverage inventory is invalid")
    if value.get("transition_coverage") != sorted(set(value.get("transition_coverage") or [])) or not {"create", "retrieve"} <= set(value["transition_coverage"]):
        raise ValueError("Adversarial qualification transition coverage is invalid")
    if isinstance(value.get("invariant_count"), bool) or not isinstance(value.get("invariant_count"), int) or value["invariant_count"] < 10:
        raise ValueError("Adversarial qualification invariant count is invalid")
    if value.get("counterexample_refs") != [
        "fixture:review-no-action-cycle", "fixture:noop-checkpoint-republish",
    ]:
        raise ValueError("Adversarial qualification counterexample inventory is invalid")
    components = value.get("component_contracts")
    if not isinstance(components, list) or len(components) != 3:
        raise ValueError("Adversarial qualification component inventory is invalid")
    for component in components:
        if not isinstance(component, Mapping) or set(component) != {"schema_version", "evidence_sha256"} or not isinstance(component.get("schema_version"), str) or not isinstance(component.get("evidence_sha256"), str) or len(component["evidence_sha256"]) != 64:
            raise ValueError("Adversarial qualification component is invalid")
    return dict(value)


def _inside_native_workspace(path: Path) -> bool:
    target = path.resolve()
    for parent in (target.parent, *target.parents):
        if (parent / "run.json").exists() or (parent / "workspace-snapshot.json").exists():
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run installed provider-free lifecycle adversarial qualification.",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    if args.output and _inside_native_workspace(args.output):
        parser.error("--output must not be inside a native SBE workspace")
    value = read_adversarial_qualification_schema() if args.schema else run_adversarial_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
