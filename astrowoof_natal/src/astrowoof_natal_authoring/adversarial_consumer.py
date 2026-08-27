"""Strict public reader for the joint adversarial consumer catalog."""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
from typing import Any, Mapping


CONTRACT = "astrowoof.adversarial_consumer_catalog.v1"
_OWNERS = {"sbe", "api", "joint"}
_KINDS = {"packaged_fixture", "qualification_component", "api_fixture_required"}


def _bytes_digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def _canonical_digest(value: Any) -> str:
    return _bytes_digest(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8"))


def validate_adversarial_consumer_catalog(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != {
        "schema_version", "catalog_sha256", "cases",
    } or value.get("schema_version") != CONTRACT:
        raise ValueError("Adversarial consumer catalog fields are not exact")
    body = {"schema_version": value["schema_version"], "cases": value["cases"]}
    if value.get("catalog_sha256") != _canonical_digest(body):
        raise ValueError("Adversarial consumer catalog digest mismatch")
    cases = value.get("cases")
    if not isinstance(cases, list) or len(cases) != 15:
        raise ValueError("Adversarial consumer case inventory is incomplete")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping) or set(case) != {
            "case_id", "owner", "evidence_kind", "evidence_ref", "sha256", "assertions",
        }:
            raise ValueError("Adversarial consumer case fields are not exact")
        case_id = case.get("case_id")
        kind = case.get("evidence_kind")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError("Adversarial consumer case identity is invalid")
        seen.add(case_id)
        if case.get("owner") not in _OWNERS or kind not in _KINDS or not isinstance(case.get("evidence_ref"), str):
            raise ValueError("Adversarial consumer case classification is invalid")
        digest = case.get("sha256")
        if kind == "packaged_fixture":
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("Packaged consumer fixture digest is missing")
        elif digest is not None:
            raise ValueError("Non-artifact consumer evidence must not invent a digest")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions or len(assertions) != len(set(assertions)) or any(not isinstance(item, str) or not item for item in assertions):
            raise ValueError("Adversarial consumer assertions must be unique strings")
    return deepcopy(dict(value))


def read_adversarial_consumer_catalog() -> dict[str, Any]:
    root = files("astrowoof_natal_authoring").joinpath("resources", "fixtures")
    path = root.joinpath("adversarial-consumer", "catalog.v1.json")
    body = json.loads(path.read_text(encoding="utf-8"))
    for case in body["cases"]:
        if case["evidence_kind"] != "packaged_fixture":
            continue
        artifact = root.joinpath(*case["evidence_ref"].split("/"))
        actual = _bytes_digest(artifact.read_bytes())
        if case["sha256"] is None:
            case["sha256"] = actual
        elif actual != case["sha256"]:
            raise ValueError(f"Consumer fixture digest mismatch: {case['case_id']}")
    result = {**body, "catalog_sha256": _canonical_digest(body)}
    return validate_adversarial_consumer_catalog(result)
