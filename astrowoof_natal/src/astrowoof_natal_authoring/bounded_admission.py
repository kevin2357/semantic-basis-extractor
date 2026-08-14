"""Strict admission for one SPC-projected bounded Natal context family."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping


ADMISSION_CONTRACT = "astrowoof.bounded_natal.input_admission.v1"
ADMISSION_EVENT_CONTRACT = "astrowoof.bounded_natal.admission_event.v1"
OUTPUT_CONTRACT = "projected_bounded_semantic_graph.v1"
OUTPUT_CONTRACT_VERSION = "1.0.0"
SUPPORTED_SPC_VERSION = "0.11.0"
SUPPORTED_PROFILE = ("woofmapped_bounded_astrology.v0", "0.1.0")
SUPPORTED_TARGET_ONTOLOGY = "woofmapped_astrology.v0"
REQUIRED_CONTEXTS = {
    "woofmapped.dog_direct.v1": "1.0.0",
    "woofmapped.doghouse.general.v0": "0.1.0",
    "woofmapped.handler_guidance.v1": "1.0.0",
    "woofmapped.hybrid_horoscope.v1": "1.0.0",
}
SUPPORTED_UPSTREAM_CONTRACTS = {
    "package_type": "bounded_natal_dataset",
    "package_schema_version": "1.0.0",
    "canonical_graph_contract": "bounded_canonical_astrology_graph.v1",
    "canonical_graph_version": "1.7.0",
    "evidence_contract": "agf.bounded_uncertainty_evidence.v1.0.0",
    "calculation_profile": "agf.bounded_natal.calculation_profile.v1.12.0",
    "interval_proof_profile": "agf.interval_proof.v1.0.0",
}
REQUIRED_LIMITATIONS = frozenset(
    {
        "bounded_invariant_subgraph_not_exact_chart",
        "no_representative_or_midpoint_positions",
        "no_exact_longitudes_or_orbs",
        "no_structural_strength_or_canonical_claims",
        "no_temporal_activation",
    }
)
REQUIRED_CAPABILITIES = {
    "supports_bounded_categorical_placements": True,
    "supports_exact_longitudes": False,
    "supports_semantic_graph_activation": False,
    "supports_house_transits": False,
    "supports_angle_transits": False,
}
PROHIBITED_TRUE_CAPABILITIES = frozenset(
    {
        "supports_exact_longitudes",
        "supports_structural_strength_scores",
        "supports_canonical_claims",
        "supports_semantic_graph_activation",
        "supports_house_transits",
        "supports_angle_transits",
    }
)


class BoundedAdmissionError(ValueError):
    """Machine-classified bounded intake failure."""

    def __init__(self, code: str, message: str, *, status: str = "invalid") -> None:
        super().__init__(message)
        self.code = code
        self.status = status

    def as_dict(self) -> dict[str, str]:
        return {"status": self.status, "code": self.code, "message": str(self)}


@dataclass(frozen=True)
class BoundedAdmission:
    artifacts_by_context: dict[str, dict[str, Any]]
    summary: dict[str, Any]
    event: dict[str, Any]


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _default_validator(
    artifacts: list[Mapping[str, Any]],
) -> dict[str, Any]:
    try:
        installed_version = importlib.metadata.version("semantic-projection-core")
    except importlib.metadata.PackageNotFoundError as exc:
        raise BoundedAdmissionError(
            "spc_runtime_missing",
            "semantic-projection-core 0.11.0 is required for bounded admission",
            status="unsupported",
        ) from exc
    if installed_version != SUPPORTED_SPC_VERSION:
        raise BoundedAdmissionError(
            "spc_runtime_unsupported",
            f"SPC {SUPPORTED_SPC_VERSION} is required; installed {installed_version}",
            status="unsupported",
        )
    try:
        from semantic_projection import (
            validate_parallel_bounded_contexts,
            validate_projected_bounded_semantic_graph,
        )

        for artifact in artifacts:
            validate_projected_bounded_semantic_graph(dict(artifact))
        return validate_parallel_bounded_contexts(artifacts)
    except BoundedAdmissionError:
        raise
    except Exception as exc:
        raise BoundedAdmissionError(
            "spc_validation_failed", f"SPC rejected bounded family: {exc}"
        ) from exc


def _require_equal(
    observed: Any,
    expected: Any,
    *,
    code: str,
    label: str,
    status: str = "unsupported",
) -> None:
    if observed != expected:
        raise BoundedAdmissionError(
            code,
            f"{label} requires {expected!r}; received {observed!r}",
            status=status,
        )


def _safe_event(summary: Mapping[str, Any]) -> dict[str, Any]:
    safe_keys = (
        "admission_id",
        "source_artifact_sha256",
        "output_contract",
        "contract_version",
        "spc_version",
        "profile_id",
        "profile_version",
        "target_ontology",
        "contexts",
        "object_correspondence_count",
        "relationship_correspondence_count",
        "projected_term_count",
        "epistemic_sha256",
        "structural_semantic_sha256",
    )
    return {
        "schema_version": ADMISSION_EVENT_CONTRACT,
        "event_name": "bounded_input.admitted",
        "status": "passed",
        "data": {key: summary[key] for key in safe_keys},
    }


def admit_bounded_family(
    artifacts: Iterable[Mapping[str, Any]],
    *,
    validator: Callable[[list[Mapping[str, Any]]], dict[str, Any]] | None = None,
) -> BoundedAdmission:
    """Validate and admit exactly one complete projected bounded context family."""

    values = [dict(artifact) for artifact in artifacts]
    if not values:
        raise BoundedAdmissionError("bounded_family_empty", "No bounded artifacts supplied")
    if any("source_graph_ref" in value for value in values):
        raise BoundedAdmissionError(
            "mixed_exact_bounded_input",
            "Exact projected graphs cannot enter bounded admission",
            status="mixed",
        )
    if len(values) != len(REQUIRED_CONTEXTS):
        raise BoundedAdmissionError(
            "bounded_context_count",
            f"Expected four bounded contexts; received {len(values)}",
        )

    by_context: dict[str, dict[str, Any]] = {}
    runtime_resource_identity: dict[str, Any] | None = None
    for value in values:
        metadata = value.get("metadata") or {}
        _require_equal(
            metadata.get("output_contract"),
            OUTPUT_CONTRACT,
            code="bounded_output_contract",
            label="bounded output contract",
        )
        _require_equal(
            metadata.get("contract_version"),
            OUTPUT_CONTRACT_VERSION,
            code="bounded_contract_version",
            label="bounded contract version",
        )
        _require_equal(
            metadata.get("engine_version"),
            SUPPORTED_SPC_VERSION,
            code="bounded_engine_version",
            label="SPC engine version",
        )
        _require_equal(
            (metadata.get("profile_id"), metadata.get("profile_version")),
            SUPPORTED_PROFILE,
            code="bounded_profile",
            label="bounded profile",
        )
        _require_equal(
            value.get("target_ontology"),
            SUPPORTED_TARGET_ONTOLOGY,
            code="bounded_target_ontology",
            label="target ontology",
        )
        context_id = metadata.get("context_id")
        if context_id in by_context:
            raise BoundedAdmissionError(
                "bounded_context_duplicate", f"Duplicate bounded context {context_id!r}"
            )
        if context_id not in REQUIRED_CONTEXTS:
            raise BoundedAdmissionError(
                "bounded_context_unknown",
                f"Unsupported bounded context {context_id!r}",
                status="unsupported",
            )
        _require_equal(
            metadata.get("context_version"),
            REQUIRED_CONTEXTS[context_id],
            code="bounded_context_version",
            label=f"context {context_id}",
        )
        runtime = metadata.get("runtime_identity") or {}
        distribution = runtime.get("distribution") or {}
        _require_equal(
            distribution.get("name"),
            "semantic-projection-core",
            code="bounded_runtime_distribution",
            label="runtime distribution",
        )
        _require_equal(
            distribution.get("version"),
            SUPPORTED_SPC_VERSION,
            code="bounded_runtime_version",
            label="runtime distribution version",
        )
        _require_equal(
            runtime.get("route"),
            "bounded_natal_projection",
            code="bounded_runtime_route",
            label="runtime route",
        )
        _require_equal(
            runtime.get("output_contract"),
            OUTPUT_CONTRACT,
            code="bounded_runtime_contract",
            label="runtime output contract",
        )
        observed_runtime_resources = {
            key: runtime.get(key)
            for key in (
                "identity_contract",
                "distribution",
                "release_compatibility",
                "runtime_package",
                "semantic_resources",
                "schemas",
                "profile",
                "route",
                "output_contract",
            )
        }
        if runtime_resource_identity is None:
            runtime_resource_identity = observed_runtime_resources
        elif observed_runtime_resources != runtime_resource_identity:
            raise BoundedAdmissionError(
                "bounded_runtime_resources",
                "SPC runtime or semantic-resource identity differs across contexts",
                status="unsupported",
            )
        source_identity = value.get("source_identity") or {}
        source_chart_id = source_identity.get("source_chart_id")
        if not isinstance(source_chart_id, str) or not source_chart_id:
            raise BoundedAdmissionError(
                "bounded_source_identity",
                "Bounded source identity requires one opaque source_chart_id",
            )
        source_sha = source_identity.get("source_artifact_sha256")
        if source_sha != (value.get("source_artifact_ref") or {}).get(
            "source_artifact_sha256"
        ):
            raise BoundedAdmissionError(
                "bounded_source_artifact_identity",
                "Source identity and source artifact reference hashes differ",
            )
        capabilities = value.get("source_capabilities") or {}
        if not isinstance(capabilities, dict) or any(
            not isinstance(key, str)
            or not key.startswith("supports_")
            or not isinstance(capability, bool)
            for key, capability in capabilities.items()
        ):
            raise BoundedAdmissionError(
                "bounded_capabilities",
                "Bounded source capabilities must be boolean supports_* fields",
                status="unsupported",
            )
        if any(
            capabilities.get(key) is True for key in PROHIBITED_TRUE_CAPABILITIES
        ) or any(
            capabilities.get(key) is not expected
            for key, expected in REQUIRED_CAPABILITIES.items()
        ):
            raise BoundedAdmissionError(
                "bounded_capabilities",
                "Bounded source capabilities permit unsupported exact or temporal semantics",
                status="unsupported",
            )
        if not REQUIRED_LIMITATIONS <= set(value.get("limitations") or []):
            raise BoundedAdmissionError(
                "bounded_limitations",
                "Bounded artifact omits required anti-precision limitations",
                status="unsupported",
            )
        _require_equal(
            (value.get("provenance") or {}).get("upstream_contracts"),
            SUPPORTED_UPSTREAM_CONTRACTS,
            code="bounded_upstream_contracts",
            label="upstream bounded contracts",
        )
        if (value.get("provenance") or {}).get("context_epistemic_policy") != (
            "certainty_invariant_across_contexts"
        ):
            raise BoundedAdmissionError(
                "bounded_epistemic_policy",
                "Bounded context does not declare certainty invariance",
            )
        by_context[str(context_id)] = value

    observed_contexts = set(by_context)
    if observed_contexts != set(REQUIRED_CONTEXTS):
        raise BoundedAdmissionError(
            "bounded_context_set",
            "Bounded context set mismatch: "
            f"missing={sorted(set(REQUIRED_CONTEXTS) - observed_contexts)}, "
            f"unexpected={sorted(observed_contexts - set(REQUIRED_CONTEXTS))}",
        )

    ordered = [by_context[context] for context in sorted(by_context)]
    try:
        report = (validator or _default_validator)(ordered)
    except BoundedAdmissionError:
        raise
    except Exception as exc:
        raise BoundedAdmissionError(
            "spc_validation_failed", f"SPC rejected bounded family: {exc}"
        ) from exc
    if report.get("status") != "passed":
        raise BoundedAdmissionError(
            "bounded_parallel_validation", "SPC parallel validation did not pass"
        )
    baseline = ordered[0]
    registry = baseline["projected_term_registry"]
    terms = registry.get("terms") or {}
    admission_material = {
        "source_artifact_sha256": report["source_artifact_sha256"],
        "contexts": report["contexts"],
        "epistemic_sha256": report["epistemic_sha256"],
        "structural_semantic_sha256": report["structural_semantic_sha256"],
        "profile_id": report["profile_id"],
        "profile_version": report["profile_version"],
    }
    summary = {
        "schema_version": ADMISSION_CONTRACT,
        "status": "passed",
        "admission_id": "bounded_admission:" + _canonical_sha256(admission_material)[:24],
        "source_artifact_sha256": report["source_artifact_sha256"],
        "source_identity_sha256": _canonical_sha256(baseline["source_identity"]),
        "output_contract": OUTPUT_CONTRACT,
        "contract_version": OUTPUT_CONTRACT_VERSION,
        "spc_version": SUPPORTED_SPC_VERSION,
        "profile_id": report["profile_id"],
        "profile_version": report["profile_version"],
        "target_ontology": baseline["target_ontology"],
        "contexts": report["contexts"],
        "context_versions": report["context_versions"],
        "projection_ids": report["projection_ids"],
        "object_correspondence_count": report["object_correspondence_count"],
        "relationship_correspondence_count": report[
            "relationship_correspondence_count"
        ],
        "projected_term_count": len(terms),
        "projected_term_registry_sha256": _canonical_sha256(registry),
        "source_evidence_sha256": _canonical_sha256(baseline["source_evidence"]),
        "capabilities_sha256": _canonical_sha256(baseline["source_capabilities"]),
        "dispositions_sha256": _canonical_sha256(
            baseline["source_feature_dispositions"]
        ),
        "limitations_sha256": _canonical_sha256(baseline["limitations"]),
        "epistemic_sha256": report["epistemic_sha256"],
        "structural_semantic_sha256": report["structural_semantic_sha256"],
        "validation_contract": report["validation_contract"],
        "provider_operation_count": 0,
    }
    return BoundedAdmission(
        artifacts_by_context=by_context,
        summary=summary,
        event=_safe_event(summary),
    )


def load_bounded_family(input_package: Path) -> list[dict[str, Any]]:
    """Discover one bounded family by contract metadata, independent of filenames."""

    root = input_package.resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Bounded input package is not a directory: {root}")
    bounded: list[dict[str, Any]] = []
    exact_count = 0
    for path in sorted(root.glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            continue
        metadata = value.get("metadata") or {}
        if metadata.get("output_contract") == OUTPUT_CONTRACT:
            bounded.append(value)
        elif "source_graph_ref" in value:
            exact_count += 1
    if bounded and exact_count:
        raise BoundedAdmissionError(
            "mixed_exact_bounded_input",
            "Input package contains exact and bounded projected graphs",
            status="mixed",
        )
    if not bounded:
        raise BoundedAdmissionError(
            "bounded_family_not_found", "No projected bounded artifacts found"
        )
    return bounded
