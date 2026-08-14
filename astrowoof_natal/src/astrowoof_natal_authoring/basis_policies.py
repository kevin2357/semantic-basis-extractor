"""Named semantic-basis policies separated from generic extraction mechanics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


LEGACY_ATOMIC_POLICY_ID = "legacy_atomic.v1"

LEGACY_EXACT_MANDATORY_OBJECTS = frozenset(
    {
        "Sun",
        "Moon",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Pluto",
        "ASC",
        "DSC",
        "MC",
        "IC",
        "North Node",
        "Part of Fortune",
    }
)

LEGACY_EXACT_WEIGHTS = {
    "core_salience": 0.14,
    "structural": 0.12,
    "projected_relevance": 0.12,
    "evidence": 0.09,
    "centrality": 0.10,
    "coverage": 0.10,
    "distinctiveness": 0.08,
    "compression": 0.07,
    "narrative_yield": 0.09,
    "voice_yield": 0.05,
    "humor_affordance": 0.04,
    "redundancy_penalty": -0.08,
    "dependency_cost": -0.07,
}

LEGACY_EXACT_CATEGORY_BY_OBJECT = {
    "Sun": "big3_core_traits",
    "Moon": "big3_core_traits",
    "ASC": "angles",
    "DSC": "angles",
    "MC": "angles",
    "IC": "angles",
    "North Node": "development",
    "Part of Fortune": "development",
}


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


class BasisPolicy(Protocol):
    """Decisions supplied to the policy-agnostic extraction mechanics."""

    policy_id: str
    route: str
    selection_budget: int
    mandatory_count: int
    score_weights: dict[str, float]
    authoring_packet_schema_version: str
    candidate_generator_id: str
    optimizer_id: str

    def object_semantics(self, canonical_name: str) -> dict[str, Any]: ...

    def score_object(
        self,
        *,
        mandatory: bool,
        structural_strength: float,
        projected_relevance: float,
        context_count: int,
        centrality: float,
        rarity: float,
        operator_count: int,
        semantic_term_count: int,
    ) -> dict[str, float]: ...

    def score_relationship(
        self,
        *,
        source_mandatory: bool,
        target_mandatory: bool,
        structural_strength: float,
        projected_relevance: float,
        context_count: int,
        centrality: float,
        exactness: float,
        rarity: float,
        operator_count: int,
        theme_tag_count: int,
        semantic_term_count: int,
        nonmandatory_dependency_count: int,
    ) -> dict[str, float]: ...

    def score_synthesis(
        self,
        *,
        dependency_count: int,
        domain_count: int,
        tag_count: int,
        evidence_strength: float,
    ) -> dict[str, float]: ...


@dataclass(frozen=True)
class ExactNatalPolicy:
    """Released exact-Natal policy with legacy atomic angle behavior."""

    policy_id: str = LEGACY_ATOMIC_POLICY_ID
    route: str = "exact_natal"
    selection_budget: int = 50
    mandatory_count: int = 16
    score_weights: dict[str, float] = field(
        default_factory=lambda: dict(LEGACY_EXACT_WEIGHTS)
    )
    authoring_packet_schema_version: str = (
        "astrowoof.projected_natal_cards.authoring_packet.v0.4"
    )
    candidate_generator_id: str = "projected-candidates.v0.2"
    optimizer_id: str = "closed-marginal-portfolio.v0.1"

    def object_semantics(self, canonical_name: str) -> dict[str, Any]:
        mandatory = canonical_name in LEGACY_EXACT_MANDATORY_OBJECTS
        claim_type = (
            "angle"
            if canonical_name in {"ASC", "DSC", "MC", "IC"}
            else (
                "orientation"
                if canonical_name in {"North Node", "South Node"}
                else "placement"
            )
        )
        categories = (
            ["angles", "big3_core_traits"]
            if canonical_name == "ASC"
            else [LEGACY_EXACT_CATEGORY_BY_OBJECT.get(canonical_name, "core_traits")]
        )
        return {
            "mandatory": mandatory,
            "candidate_type": "mandatory_basis" if mandatory else "projected_object",
            "claim_type": claim_type,
            "categories": categories,
            "semantic_role": ["anchor", "primitive"] if mandatory else ["primitive"],
        }

    def score_object(
        self,
        *,
        mandatory: bool,
        structural_strength: float,
        projected_relevance: float,
        context_count: int,
        centrality: float,
        rarity: float,
        operator_count: int,
        semantic_term_count: int,
    ) -> dict[str, float]:
        return {
            "core_salience": 1.0 if mandatory else 0.45,
            "structural": _clamp(structural_strength / 0.55),
            "projected_relevance": _clamp(projected_relevance / 0.55),
            "evidence": _clamp(context_count / 4),
            "centrality": _clamp(centrality),
            "coverage": _clamp(0.55 + 0.45 * rarity),
            "distinctiveness": _clamp(rarity),
            "compression": 0.0,
            "narrative_yield": _clamp(0.55 + 0.04 * operator_count),
            "voice_yield": _clamp(context_count / 4),
            "humor_affordance": _clamp(0.35 + 0.04 * semantic_term_count),
            "redundancy_penalty": _clamp(1 - rarity),
            "dependency_cost": 0.0,
        }

    def score_relationship(
        self,
        *,
        source_mandatory: bool,
        target_mandatory: bool,
        structural_strength: float,
        projected_relevance: float,
        context_count: int,
        centrality: float,
        exactness: float,
        rarity: float,
        operator_count: int,
        theme_tag_count: int,
        semantic_term_count: int,
        nonmandatory_dependency_count: int,
    ) -> dict[str, float]:
        return {
            "core_salience": _clamp(
                0.3 + 0.25 * source_mandatory + 0.25 * target_mandatory
            ),
            "structural": _clamp(structural_strength / 0.55),
            "projected_relevance": _clamp(projected_relevance / 0.55),
            "evidence": _clamp(0.6 * context_count / 4 + 0.4 * exactness),
            "centrality": _clamp(centrality),
            "coverage": _clamp(0.5 + 0.5 * rarity),
            "distinctiveness": _clamp(0.45 * rarity + 0.55 * exactness),
            "compression": 0.0,
            "narrative_yield": _clamp(
                0.45 + 0.04 * operator_count + 0.05 * theme_tag_count
            ),
            "voice_yield": _clamp(context_count / 4),
            "humor_affordance": _clamp(0.3 + 0.025 * semantic_term_count),
            "redundancy_penalty": _clamp(1 - rarity),
            "dependency_cost": _clamp(nonmandatory_dependency_count / 2),
        }

    def score_synthesis(
        self,
        *,
        dependency_count: int,
        domain_count: int,
        tag_count: int,
        evidence_strength: float,
    ) -> dict[str, float]:
        return {
            "core_salience": _clamp(0.35 + 0.06 * dependency_count),
            "structural": _clamp(0.35 + 0.08 * dependency_count),
            "projected_relevance": _clamp(evidence_strength),
            "evidence": _clamp(0.45 + 0.1 * dependency_count),
            "centrality": _clamp(0.35 + 0.08 * dependency_count),
            "coverage": _clamp(0.45 + 0.09 * domain_count),
            "distinctiveness": _clamp(0.65 + 0.04 * dependency_count),
            "compression": _clamp((dependency_count - 1) / dependency_count),
            "narrative_yield": _clamp(0.65 + 0.06 * dependency_count),
            "voice_yield": 0.85,
            "humor_affordance": _clamp(0.55 + 0.04 * tag_count),
            "redundancy_penalty": _clamp(0.12 * max(0, dependency_count - 3)),
            "dependency_cost": _clamp(dependency_count / 8),
        }


def resolve_exact_natal_policy(policy: str | BasisPolicy | None = None) -> BasisPolicy:
    """Resolve an exact-Natal policy, rejecting unknown identities fail-closed."""

    if policy is None or policy == LEGACY_ATOMIC_POLICY_ID:
        return ExactNatalPolicy()
    if isinstance(policy, str):
        raise ValueError(f"Unsupported exact-Natal policy: {policy}")
    if policy.route != "exact_natal":
        raise ValueError(
            f"Policy {policy.policy_id} is for route {policy.route}, not exact_natal"
        )
    return policy
