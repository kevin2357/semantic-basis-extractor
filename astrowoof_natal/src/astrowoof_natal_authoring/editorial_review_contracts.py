"""Closed native editorial-review contract surface.

This module is deliberately provider-free.  It owns strict JSON parsing,
packaged contract discovery, canonical native digest/ID primitives, typed
validation results, and the staged rule registry.  Runtime packet construction
is a later slice.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from importlib.resources import files
import json
import math
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping


SEMANTIC_CONTRACT_VERSION = "astrowoof.editorial_review_semantic_contract.v5"
VALIDATION_RESULT_VERSION = "editorial_review_validation_result.v1"
CONTRACT_PREFIX = "contracts/"
SEMANTIC_CONTRACT_RESOURCE = "editorial-review-semantic-contract.v5.json"
_SEMANTIC_CONTRACT_KEYS = {
    "schema_version", "compatibility_identity", "canonical_json", "schemas",
    "digest_domains", "id_derivation", "closed_vocabularies",
    "cardinalities", "ordering", "api_transport_preflight_contract",
    "forbidden_content", "rules",
}
_RULE_KEYS = {"rule_id", "owner", "category", "validator_stage", "test_target"}

SCHEMA_RESOURCES = MappingProxyType({
    "artifact": "editorial-review-artifact.v2.schema.json",
    "capture_status": "editorial-review-capture-status.v1.schema.json",
    "fixture_bundle": "editorial-review-contract-fixture-bundle.v1.schema.json",
    "qualification": "editorial-review-contract-qualification.v1.schema.json",
    "decision": "editorial-review-decision.v5.schema.json",
    "finding": "editorial-review-finding.v1.schema.json",
    "packet": "editorial-review-packet.v5.schema.json",
    "projection": "editorial-review-projection.v5.schema.json",
    "transport": "editorial-review-transport.v5.schema.json",
    "validation": "editorial-review-validation.v1.schema.json",
    "validation_result": "editorial-review-validation-result.v1.schema.json",
})

VALID_CLASSIFICATIONS = frozenset({
    "unsupported_version", "ineligible_route", "incomplete_evidence",
    "contradictory_evidence", "invalid_schema", "digest_mismatch",
    "record_limit_exceeded", "byte_limit_exceeded",
})


@dataclass(frozen=True)
class EditorialReviewValidationResult:
    outcome: str
    classification: str | None = None
    rule_id: str | None = None
    location: str | None = None
    safe_detail_code: str | None = None

    def __post_init__(self) -> None:
        if self.outcome == "valid":
            if any(value is not None for value in (
                self.classification, self.rule_id, self.location,
                self.safe_detail_code,
            )):
                raise ValueError("Valid result cannot carry failure fields")
            return
        if self.outcome != "invalid":
            raise ValueError("Validation outcome is closed")
        if self.classification not in VALID_CLASSIFICATIONS:
            raise ValueError("Validation classification is closed")
        if not all(isinstance(value, str) and value for value in (
            self.rule_id, self.location, self.safe_detail_code,
        )):
            raise ValueError("Invalid result requires safe typed failure fields")

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "schema_version": VALIDATION_RESULT_VERSION,
            "outcome": self.outcome,
        }
        if self.outcome == "invalid":
            value.update({
                "classification": self.classification,
                "rule_id": self.rule_id,
                "location": self.location,
                "safe_detail_code": self.safe_detail_code,
            })
        return value


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Editorial review JSON contains duplicate keys")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ValueError(f"Editorial review JSON contains non-finite number: {value}")


def parse_editorial_review_json_strict(source: bytes | bytearray | memoryview | str | Path) -> Any:
    """Read exactly one UTF-8 JSON value with duplicate/nonfinite rejection."""
    if isinstance(source, Path):
        raw = source.read_bytes()
    elif isinstance(source, (bytes, bytearray, memoryview)):
        raw = bytes(source)
    elif isinstance(source, str):
        raw = source.encode("utf-8")
    else:
        raise TypeError("Editorial review JSON source must be bytes, text, or Path")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Editorial review JSON must be UTF-8") from exc
    decoder = json.JSONDecoder(
        object_pairs_hook=_reject_duplicate_pairs,
        parse_constant=_reject_constant,
    )
    try:
        value, end = decoder.raw_decode(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Editorial review JSON is invalid") from exc
    if text[end:].strip():
        raise ValueError("Editorial review JSON has trailing content")
    _assert_finite(value)
    return value


def _assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Editorial review JSON contains non-finite number")
    if isinstance(value, list):
        for item in value:
            _assert_finite(item)
    elif isinstance(value, dict):
        for item in value.values():
            _assert_finite(item)


def canonical_editorial_review_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def editorial_review_sha256(value: Any) -> str:
    return sha256(canonical_editorial_review_json(value)).hexdigest()


def derive_editorial_review_id(prefix: str, domain: str, components: list[Any]) -> str:
    if not prefix or not domain:
        raise ValueError("Editorial review ID prefix and domain are required")
    digest = editorial_review_sha256([domain, *components])
    return f"{prefix}_{digest}"


def digest_without(value: Mapping[str, Any], field: str) -> str:
    copy = dict(value)
    copy.pop(field, None)
    return editorial_review_sha256(copy)


def derive_packet_id(packet: Mapping[str, Any]) -> str:
    eligibility = packet["eligibility"]
    native = packet["native_correlations"]
    terminal = packet["terminal_selection"]
    return derive_editorial_review_id("erp", "packet_id.v1", [
        packet["schema_version"], native["native_run_id"], native["subject_id"],
        eligibility["native_result_id"], eligibility["native_result_sha256"],
        eligibility["canonical_receipt_id"], eligibility["canonical_receipt_sha256"],
        native["native_state_revision"], native["checkpoint_basis_sha256"],
        native["snapshot_sha256"],
        terminal["terminal_selection_id"], terminal["delivery_disposition"],
    ])


def derive_decision_id(packet_id: str, decision: Mapping[str, Any]) -> str:
    action = decision["action"]
    stage_local = decision.get("released_pass_identity", decision["stage"])
    return derive_editorial_review_id("erd", "decision_id.v2", [
        packet_id, decision["decision_ordinal"], decision["stage"], stage_local,
        decision["stage_attempt"], action.get("paid_action_id"),
        action.get("binding_sha256"),
    ])


def derive_finding_id(decision_id: str, finding: Mapping[str, Any], local_ordinal: int) -> str:
    return derive_editorial_review_id("erf", "finding_id.v1", [
        decision_id, finding["finding_kind"], finding["code"],
        finding["evidence_sha256"], local_ordinal,
    ])


def derive_validation_id(owner_id: str, validation: Mapping[str, Any], local_ordinal: int) -> str:
    return derive_editorial_review_id("erv", "validation_id.v1", [
        owner_id, validation["validation_kind"], validation["code"],
        validation["report_id"], validation["report_sha256"], local_ordinal,
    ])


def derive_projection_id(packet_id: str, kind: str, native_id: str) -> str:
    return derive_editorial_review_id(
        "erpj", "projection_id.v1", [packet_id, kind, native_id],
    )


def derive_artifact_id(packet_id: str, kind: str, object_sha256: str) -> str:
    return derive_editorial_review_id("era", "artifact_id.v1", [
        "editorial_review_artifact.v2", packet_id, kind, object_sha256,
    ])


def _resource_bytes(name: str) -> bytes:
    return files("astrowoof_natal_authoring.resources").joinpath(
        CONTRACT_PREFIX, name,
    ).read_bytes()


def editorial_review_resource_sha256(raw: bytes) -> str:
    """Hash packaged text resources independently of checkout line endings."""
    return sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_editorial_review_schema(kind: str) -> dict[str, Any]:
    try:
        name = SCHEMA_RESOURCES[kind]
    except KeyError as exc:
        raise ValueError("Unknown editorial review schema kind") from exc
    value = parse_editorial_review_json_strict(_resource_bytes(name))
    if not isinstance(value, dict):
        raise ValueError("Editorial review schema resource is not an object")
    return value


def read_editorial_review_semantic_contract() -> dict[str, Any]:
    value = parse_editorial_review_json_strict(
        _resource_bytes(SEMANTIC_CONTRACT_RESOURCE)
    )
    if not isinstance(value, dict) or value.get("schema_version") != SEMANTIC_CONTRACT_VERSION:
        raise ValueError("Editorial review semantic contract is unsupported")
    if set(value) != _SEMANTIC_CONTRACT_KEYS:
        raise ValueError("Editorial review semantic contract shape is invalid")
    schemas = value.get("schemas")
    if not isinstance(schemas, list) or not schemas:
        raise ValueError("Editorial review semantic contract schema inventory is invalid")
    seen_resources: set[str] = set()
    for item in schemas:
        if not isinstance(item, dict) or set(item) != {"resource", "sha256"}:
            raise ValueError("Editorial review semantic contract schema entry is invalid")
        name = item["resource"]
        if name in seen_resources or name not in SCHEMA_RESOURCES.values():
            raise ValueError("Editorial review semantic contract schema resource is invalid")
        seen_resources.add(name)
        actual = editorial_review_resource_sha256(_resource_bytes(name))
        if actual != item["sha256"]:
            raise ValueError("Editorial review semantic contract schema digest mismatch")
    rules = value.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("Editorial review semantic contract rule inventory is invalid")
    for item in rules:
        if not isinstance(item, dict) or set(item) != _RULE_KEYS:
            raise ValueError("Editorial review semantic contract rule is invalid")
        if item["owner"] not in {"native", "joint_fixture", "api_transport"}:
            raise ValueError("Editorial review semantic contract rule owner is invalid")
    return value


def validate_closed_root(value: Mapping[str, Any], kind: str) -> EditorialReviewValidationResult:
    """Dependency-free first structural stage; deeper stages follow in 1ε.1/.2."""
    schema = read_editorial_review_schema(kind)
    if not isinstance(value, dict):
        return _invalid("invalid_schema", "schema.root.closed.v1", "$", "root_not_object")
    required = set(schema.get("required", []))
    properties = set(schema.get("properties", {}))
    if missing := sorted(required - set(value)):
        return _invalid("invalid_schema", "schema.root.closed.v1", "$", f"missing_{missing[0]}")
    if extra := sorted(set(value) - properties):
        return _invalid("invalid_schema", "schema.root.closed.v1", "$", f"unknown_{extra[0]}")
    version_key = "transport_schema_version" if kind == "transport" else "schema_version"
    expected = schema["properties"][version_key].get("const")
    if expected is not None and value.get(version_key) != expected:
        return _invalid("unsupported_version", "schema.version.closed.v1", f"$.{version_key}", "unsupported_version")
    return EditorialReviewValidationResult("valid")


def _invalid(classification: str, rule_id: str, location: str, detail: str) -> EditorialReviewValidationResult:
    return EditorialReviewValidationResult(
        "invalid", classification, rule_id, location, detail,
    )


def _stage_placeholder(_: Mapping[str, Any]) -> EditorialReviewValidationResult:
    raise NotImplementedError(
        "Semantic stage is registered but not executable before Slice 1ε.1/.2"
    )


VALIDATOR_STAGES: Mapping[str, Callable[[Mapping[str, Any]], EditorialReviewValidationResult]] = MappingProxyType({
    "validate_schema": _stage_placeholder,
    "validate_digest_domains": _stage_placeholder,
    "validate_provenance_eligibility": _stage_placeholder,
    "validate_chronology": _stage_placeholder,
    "validate_deck_transitions": _stage_placeholder,
    "validate_action_response_joins": _stage_placeholder,
    "validate_ownership": _stage_placeholder,
    "validate_manifest_and_artifacts": _stage_placeholder,
    "validate_projections": _stage_placeholder,
    "validate_summaries_and_request": _stage_placeholder,
})


def native_rule_registry() -> Mapping[str, str]:
    contract = read_editorial_review_semantic_contract()
    return MappingProxyType({
        item["rule_id"]: item["validator_stage"]
        for item in contract["rules"]
        if item["owner"] in {"native", "joint_fixture"}
    })


def validate_rule_registry_coverage() -> None:
    registry = native_rule_registry()
    missing_handlers = sorted(set(registry.values()) - set(VALIDATOR_STAGES))
    if missing_handlers:
        raise ValueError("Editorial review manifest names unknown validator stages")
    if len(registry) != len(set(registry)):
        raise ValueError("Editorial review manifest contains duplicate rule IDs")
    manifest = read_editorial_review_semantic_contract()
    if any(not item.get("test_target") for item in manifest["rules"]):
        raise ValueError("Editorial review manifest rule lacks a test target")


__all__ = [
    "EditorialReviewValidationResult", "SCHEMA_RESOURCES",
    "SEMANTIC_CONTRACT_VERSION", "VALIDATION_RESULT_VERSION",
    "VALIDATOR_STAGES", "canonical_editorial_review_json",
    "derive_editorial_review_id", "editorial_review_sha256",
    "native_rule_registry", "parse_editorial_review_json_strict",
    "read_editorial_review_schema", "read_editorial_review_semantic_contract",
    "validate_closed_root", "validate_rule_registry_coverage",
    "derive_artifact_id", "derive_decision_id", "derive_finding_id",
    "derive_packet_id", "derive_projection_id", "derive_validation_id",
    "digest_without",
]
