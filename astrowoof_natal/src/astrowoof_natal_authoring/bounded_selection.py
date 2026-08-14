"""Editorial utility and deterministic exactly-fifty bounded portfolio selection."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .bounded_basis import BoundedBasis


EDITORIAL_UTILITY_CONTRACT = "astrowoof.bounded_natal.editorial_utility.v1"
SELECTION_AUDIT_CONTRACT = "astrowoof.bounded_natal.selection_audit.v1"
SELECTION_SIZE = 50
UTILITY_WEIGHTS = {
    "foundational_salience": 0.13,
    "ordinary_material_preference": 0.11,
    "family_collapsed_centrality": 0.12,
    "target_relevance": 0.12,
    "distinctiveness": 0.10,
    "topology_configuration_value": 0.10,
    "narrative_yield": 0.09,
    "context_completeness": 0.07,
    "compression": 0.04,
    "incremental_coverage": 0.12,
}
PENALTY_WEIGHTS = {
    "redundancy": 0.15,
    "family_saturation": 0.10,
    "derived_family_saturation": 0.12,
    "dependency_cost": 0.08,
}
EDITORIAL_TIERS = ("foundational", "primary", "supporting", "supplemental")


class BoundedSelectionError(ValueError):
    """Machine-readable bounded portfolio failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, str]:
        return {"status": "failed", "code": self.code, "message": str(self)}


@dataclass(frozen=True)
class BoundedSelection:
    selected: tuple[dict[str, Any], ...]
    rejected: tuple[dict[str, Any], ...]
    audit: dict[str, Any]
    disposition_report: dict[str, Any]


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def _semantic_kind(candidate: Mapping[str, Any]) -> str:
    if candidate["candidate_kind"] == "invariant_configuration":
        return "configuration"
    records = candidate.get("context_records") or {}
    first_context = next(iter(sorted(records)), None)
    rows = records.get(first_context, []) if first_context else []
    if rows and "relationship_type" in rows[0]:
        return "relationship"
    return "object"


def _direct_families(candidate: Mapping[str, Any]) -> tuple[str, ...]:
    if candidate["candidate_kind"] == "invariant_configuration":
        return tuple(
            sorted(candidate.get("evidence_lineage", {}).get("evidence_family_groups", []))
        )
    records = candidate.get("context_records") or {}
    first_context = next(iter(sorted(records)), None)
    rows = records.get(first_context, []) if first_context else []
    return tuple(
        sorted(
            {
                family
                for row in rows
                for family in (row.get("epistemic_basis") or {}).get(
                    "evidence_family_groups", []
                )
            }
        )
    )


def _target_relevance(candidate: Mapping[str, Any]) -> float:
    if _semantic_kind(candidate) != "relationship":
        return 0.0
    records = candidate.get("context_records") or {}
    context = next(iter(sorted(records)), None)
    total = 0.0
    for row in records.get(context, []) if context else []:
        value = row.get("projection_relevance_score")
        if value is None:
            continue
        accounting = (row.get("attributes") or {}).get("relevance_accounting") or {}
        if accounting.get("policy") != "evidence_family_equal_allocation" or (
            accounting.get("raw_record_count_is_weight") is not False
        ):
            raise BoundedSelectionError(
                "bounded_relevance_policy_unsupported",
                "relationship target relevance lacks family-safe allocation",
            )
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
            raise BoundedSelectionError(
                "bounded_relevance_value_invalid",
                f"invalid target relevance on {candidate['candidate_id']}",
            )
        total += float(value)
    return min(1.0, total)


def _closure(
    candidate_id: str,
    by_id: Mapping[str, Mapping[str, Any]],
    *,
    active: frozenset[str] = frozenset(),
) -> set[str]:
    if candidate_id in active:
        raise BoundedSelectionError(
            "bounded_dependency_cycle", f"candidate dependency cycle at {candidate_id}"
        )
    candidate = by_id.get(candidate_id)
    if candidate is None:
        raise BoundedSelectionError(
            "bounded_dependency_missing", f"missing candidate dependency {candidate_id}"
        )
    result = {candidate_id}
    for dependency in candidate.get("member_candidate_ids") or []:
        child = by_id.get(dependency)
        if child is None:
            raise BoundedSelectionError(
                "bounded_dependency_missing", f"missing candidate dependency {dependency}"
            )
        if child.get("candidate_role") == "dependency_only":
            continue
        result.update(_closure(dependency, by_id, active=active | {candidate_id}))
    return result


def _feature_sets(
    by_id: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    roots: dict[str, set[str]] = {}
    terms: dict[str, set[str]] = {}
    features: dict[str, set[str]] = {}
    for candidate_id, candidate in by_id.items():
        roots[candidate_id] = set(candidate.get("root_owner_refs") or [])
        terms[candidate_id] = set(candidate.get("projected_term_refs") or [])
    changed = True
    while changed:
        changed = False
        for candidate_id, candidate in by_id.items():
            before = (len(roots[candidate_id]), len(terms[candidate_id]))
            for dependency in candidate.get("member_candidate_ids") or []:
                roots[candidate_id].update(roots.get(dependency, set()))
                terms[candidate_id].update(terms.get(dependency, set()))
            if before != (len(roots[candidate_id]), len(terms[candidate_id])):
                changed = True
    for candidate_id in by_id:
        features[candidate_id] = {
            *(f"root:{value}" for value in roots[candidate_id]),
            *(f"term:{value}" for value in terms[candidate_id]),
            *(f"family:{value}" for value in _direct_families(by_id[candidate_id])),
        }
    return roots, terms, features


def _base_components(
    candidate: Mapping[str, Any],
    *,
    roots: set[str],
    terms: set[str],
    root_degrees: Mapping[str, int],
    max_root_degree: int,
    term_frequency: Mapping[str, int],
    expected_contexts: set[str],
) -> dict[str, float]:
    kind = candidate["candidate_kind"]
    semantic_kind = _semantic_kind(candidate)
    policy = candidate["foundational_policy"]
    foundational = 0.0
    if kind == "foundational_object" and policy != "portfolio_neutral":
        foundational = 1.0
    ordinary = (
        1.0
        if kind == "individualized_relationship"
        else 0.50
        if kind == "foundational_object"
        else 0.25
        if kind == "invariant_configuration"
        else 0.0
    )
    centrality = (
        sum(root_degrees.get(root, 0) for root in roots)
        / (max(1, len(roots)) * max_root_degree)
        if roots
        else 0.0
    )
    distinctiveness = (
        sum(1.0 / term_frequency[term] for term in terms) / len(terms)
        if terms
        else 0.0
    )
    topology = {
        "configuration": 1.0,
        "relationship": 0.72,
        "object": 0.55 if kind == "foundational_object" else 0.42,
    }[semantic_kind]
    narrative = min(1.0, len(terms) / 4.0)
    records = candidate.get("context_records") or {}
    context_completeness = (
        1.0
        if kind == "invariant_configuration" or set(records) == expected_contexts
        else 0.0
    )
    compression = (
        0.85
        if kind == "invariant_configuration"
        else 0.70
        if kind == "derived_family"
        else 0.50
    )
    return {
        "foundational_salience": foundational,
        "ordinary_material_preference": ordinary,
        "family_collapsed_centrality": min(1.0, centrality),
        "target_relevance": _target_relevance(candidate),
        "distinctiveness": min(1.0, distinctiveness),
        "topology_configuration_value": topology,
        "narrative_yield": narrative,
        "context_completeness": context_completeness,
        "compression": compression,
    }


def _weighted_base(components: Mapping[str, float]) -> float:
    return sum(
        UTILITY_WEIGHTS[key] * value
        for key, value in components.items()
        if key != "incremental_coverage"
    )


def _dynamic_score(
    candidate_id: str,
    *,
    candidates: Mapping[str, Mapping[str, Any]],
    base: Mapping[str, Mapping[str, float]],
    features: Mapping[str, set[str]],
    roots: Mapping[str, set[str]],
    families: Mapping[str, tuple[str, ...]],
    closures: Mapping[str, set[str]],
    selected: set[str],
) -> tuple[float, dict[str, float], dict[str, float]]:
    own_features = features[candidate_id]
    selected_features = set().union(*(features[item] for item in selected)) if selected else set()
    incremental = (
        len(own_features - selected_features) / len(own_features) if own_features else 0.0
    )
    overlap = 0.0
    for selected_id in selected:
        union = own_features | features[selected_id]
        if union:
            overlap = max(overlap, len(own_features & features[selected_id]) / len(union))
    family_counts = Counter(
        family for selected_id in selected for family in families[selected_id]
    )
    candidate_families = families[candidate_id]
    saturation = (
        sum(min(1.0, family_counts[family]) for family in candidate_families)
        / len(candidate_families)
        if candidate_families
        else 0.0
    )
    candidate = candidates[candidate_id]
    derived_root_counts = Counter(
        root
        for selected_id in selected
        if candidates[selected_id]["candidate_kind"] == "derived_family"
        for root in roots[selected_id]
    )
    candidate_roots = roots[candidate_id]
    derived_saturation = 0.0
    if candidate["candidate_kind"] == "derived_family":
        root_saturation = (
            sum(min(1.0, derived_root_counts[root] / 2.0) for root in candidate_roots)
            / len(candidate_roots)
            if candidate_roots
            else 0.0
        )
        derived_saturation = 0.25 + 0.75 * root_saturation
    missing_dependencies = closures[candidate_id] - selected - {candidate_id}
    dependency_cost = min(1.0, len(missing_dependencies) / 8.0)
    components = dict(base[candidate_id])
    components["incremental_coverage"] = incremental
    penalties = {
        "redundancy": overlap,
        "family_saturation": saturation,
        "derived_family_saturation": derived_saturation,
        "dependency_cost": dependency_cost,
    }
    score = sum(UTILITY_WEIGHTS[key] * value for key, value in components.items())
    score -= sum(PENALTY_WEIGHTS[key] * value for key, value in penalties.items())
    return max(0.0, min(1.0, score)), components, penalties


def _tier(candidate: Mapping[str, Any], rank: int) -> str:
    if candidate["candidate_kind"] == "foundational_object":
        return "foundational"
    if rank <= 24:
        return "primary"
    if rank <= 42:
        return "supporting"
    return "supplemental"


def select_bounded_portfolio(
    basis: BoundedBasis, *, selection_size: int = SELECTION_SIZE
) -> BoundedSelection:
    """Select exactly fifty invariant authored candidates with dependency closure."""

    if selection_size != SELECTION_SIZE:
        raise BoundedSelectionError(
            "bounded_selection_size_unsupported",
            f"bounded v1 requires exactly {SELECTION_SIZE} claims",
        )
    all_candidates = list(basis.candidates)
    if len({candidate["candidate_id"] for candidate in all_candidates}) != len(
        all_candidates
    ):
        raise BoundedSelectionError(
            "bounded_candidate_identity_duplicate", "candidate IDs must be unique"
        )
    if any(
        candidate.get("epistemic_classification") != "invariant"
        for candidate in all_candidates
    ):
        raise BoundedSelectionError(
            "bounded_non_invariant_candidate", "only invariant candidates are selectable"
        )
    policy_names = {candidate.get("foundational_policy") for candidate in all_candidates}
    if len(policy_names) != 1:
        raise BoundedSelectionError(
            "bounded_foundational_policy_mixed", "candidate pool mixes foundational policies"
        )
    policy = next(iter(policy_names), None)
    by_id = {candidate["candidate_id"]: candidate for candidate in all_candidates}
    authored = {
        candidate_id: candidate
        for candidate_id, candidate in by_id.items()
        if candidate.get("candidate_role") == "authored"
    }
    if len(authored) < selection_size:
        raise BoundedSelectionError(
            "insufficient_invariant_basis",
            f"only {len(authored)} invariant authored candidates are available; {selection_size} required",
        )
    closures = {candidate_id: _closure(candidate_id, by_id) & set(authored) for candidate_id in authored}
    roots, terms, features = _feature_sets(by_id)
    families = {candidate_id: _direct_families(candidate) for candidate_id, candidate in authored.items()}
    root_degrees = Counter(
        root
        for candidate_id, candidate_roots in roots.items()
        if candidate_id in authored and by_id[candidate_id]["candidate_kind"] != "invariant_configuration"
        for root in candidate_roots
    )
    max_root_degree = max(root_degrees.values(), default=1)
    term_frequency = Counter(
        term for candidate_id, candidate_terms in terms.items() if candidate_id in authored for term in candidate_terms
    )
    expected_contexts = {
        context
        for candidate in authored.values()
        for context in candidate.get("context_records") or {}
    }
    base = {
        candidate_id: _base_components(
            candidate,
            roots=roots[candidate_id],
            terms=terms[candidate_id],
            root_degrees=root_degrees,
            max_root_degree=max_root_degree,
            term_frequency=term_frequency,
            expected_contexts=expected_contexts,
        )
        for candidate_id, candidate in authored.items()
    }

    selected: set[str] = set()
    order: list[str] = []
    decision_scores: dict[str, dict[str, Any]] = {}

    def add_bundle(bundle: set[str]) -> None:
        pending = set(bundle) - selected
        while pending:
            ready = sorted(
                candidate_id
                for candidate_id in pending
                if (closures[candidate_id] - {candidate_id}) <= selected
            )
            if not ready:
                raise BoundedSelectionError(
                    "bounded_dependency_cycle", "candidate bundle cannot be topologically ordered"
                )
            for candidate_id in ready:
                score, components, penalties = _dynamic_score(
                    candidate_id,
                    candidates=authored,
                    base=base,
                    features=features,
                    roots=roots,
                    families=families,
                    closures=closures,
                    selected=selected,
                )
                selected.add(candidate_id)
                order.append(candidate_id)
                decision_scores[candidate_id] = {
                    "bounded_editorial_utility": round(score, 6),
                    "components": {key: round(value, 6) for key, value in components.items()},
                    "penalties": {key: round(value, 6) for key, value in penalties.items()},
                }
                pending.remove(candidate_id)

    if policy == "mandatory_when_available":
        mandatory = {
            candidate_id
            for candidate_id, candidate in authored.items()
            if candidate.get("foundational_status") == "mandatory"
        }
        mandatory_closure = set().union(*(closures[item] for item in mandatory)) if mandatory else set()
        if len(mandatory_closure) > selection_size:
            raise BoundedSelectionError(
                "bounded_mandatory_foundations_exceed_capacity",
                "mandatory foundational closure exceeds fifty-claim capacity",
            )
        add_bundle(mandatory_closure)

    while len(selected) < selection_size:
        options: list[tuple[float, float, str, set[str]]] = []
        for candidate_id in sorted(authored):
            if candidate_id in selected:
                continue
            bundle = closures[candidate_id] - selected
            if not bundle or len(selected) + len(bundle) > selection_size:
                continue
            score, _, _ = _dynamic_score(
                candidate_id,
                candidates=authored,
                base=base,
                features=features,
                roots=roots,
                families=families,
                closures=closures,
                selected=selected,
            )
            dependency_value = sum(
                _weighted_base(base[item]) for item in bundle - {candidate_id}
            )
            # A configuration must earn its complete closure at the average value
            # of the bundle. Large configurations are not rewarded merely for
            # bringing more prerequisite claims with them.
            portfolio_value = (score + dependency_value) / len(bundle)
            options.append((portfolio_value, score, candidate_id, bundle))
        if not options:
            raise BoundedSelectionError(
                "insufficient_invariant_basis",
                f"dependency closure cannot produce exactly {selection_size} invariant claims",
            )
        _, _, _, bundle = max(options, key=lambda item: (item[0], item[1], item[2]))
        add_bundle(bundle)

    if len(selected) != selection_size:
        raise AssertionError("bounded selection did not terminate at exact capacity")
    if any(not closures[item] <= selected for item in selected):
        raise AssertionError("bounded selection is not dependency closed")

    selected_values: list[dict[str, Any]] = []
    for rank, candidate_id in enumerate(order, 1):
        value = deepcopy(authored[candidate_id])
        value.update(decision_scores[candidate_id])
        value["selection_rank"] = rank
        value["editorial_tier"] = _tier(value, rank)
        selected_values.append(value)

    selected_features = set().union(*(features[item] for item in selected))
    selected_families = Counter(
        family for candidate_id in selected for family in families[candidate_id]
    )
    rejected_values: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    for candidate_id in sorted(by_id):
        candidate = by_id[candidate_id]
        if candidate_id in selected:
            decision = "selected"
            reason = "selected_by_editorial_portfolio"
            score_record = decision_scores[candidate_id]
        elif candidate.get("candidate_role") == "dependency_only":
            decision = "retained_dependency"
            reason = "topology_not_authored_as_claim"
            score_record = None
        else:
            score, components, penalties = _dynamic_score(
                candidate_id,
                candidates=authored,
                base=base,
                features=features,
                roots=roots,
                families=families,
                closures=closures,
                selected=selected,
            )
            score_record = {
                "bounded_editorial_utility": round(score, 6),
                "components": {key: round(value, 6) for key, value in components.items()},
                "penalties": {key: round(value, 6) for key, value in penalties.items()},
            }
            if features[candidate_id] and features[candidate_id] <= selected_features:
                reason = "redundant_covered_territory"
            elif families[candidate_id] and all(selected_families[family] for family in families[candidate_id]):
                reason = "derived_family_saturation"
            else:
                reason = "capacity_displaced"
            decision = "rejected"
            value = deepcopy(candidate)
            value.update(score_record)
            value["rejection_reason"] = reason
            rejected_values.append(value)
        row = {
            "candidate_id": candidate_id,
            "decision": decision,
            "reason": reason,
        }
        if score_record is not None:
            row.update(score_record)
        decisions.append(row)

    disposition = deepcopy(basis.disposition_report)
    correspondence_decisions: dict[str, set[str]] = defaultdict(set)
    for candidate_id, candidate in by_id.items():
        if candidate_id in selected:
            value = "selected"
        elif candidate.get("candidate_role") == "dependency_only":
            value = "retained_dependency"
        else:
            value = next(
                row["reason"] for row in decisions if row["candidate_id"] == candidate_id
            )
        for correspondence in candidate.get("correspondence_ids") or []:
            correspondence_decisions[correspondence].add(value)
    for row in disposition["projected_rows"]:
        values = correspondence_decisions.get(row["correspondence_id"], set())
        row["selection_disposition"] = (
            "selected"
            if "selected" in values
            else "retained_dependency"
            if "retained_dependency" in values
            else sorted(values)[0]
            if values
            else "not_candidate"
        )
    selected_evidence = {
        ref
        for candidate_id in selected
        for ref in authored[candidate_id].get("evidence_lineage", {}).get(
            "resolved_evidence_refs", []
        )
    }
    for row in disposition["source_evidence"]:
        row["selection_disposition"] = (
            "selected_lineage"
            if row["evidence_ref"] in selected_evidence
            else "unselected_lineage"
        )
    disposition["selection"] = {
        "utility_profile": EDITORIAL_UTILITY_CONTRACT,
        "selected_count": len(selected),
        "selected_candidate_ids": order,
        "selected_projected_row_count": sum(
            row["selection_disposition"] == "selected"
            for row in disposition["projected_rows"]
        ),
    }

    audit = {
        "schema_version": SELECTION_AUDIT_CONTRACT,
        "utility_profile": EDITORIAL_UTILITY_CONTRACT,
        "candidate_policy": basis.summary["schema_version"],
        "foundational_policy": policy,
        "selection_size": selection_size,
        "status": "passed",
        "epistemic_classification": "invariant",
        "weights": dict(UTILITY_WEIGHTS),
        "penalty_weights": dict(PENALTY_WEIGHTS),
        "selected_candidate_ids": order,
        "selected_sha256": _canonical_sha256(selected_values),
        "rejected_sha256": _canonical_sha256(rejected_values),
        "decisions": decisions,
        "coverage": {
            "root_owner_count": len(
                set().union(*(roots[candidate_id] for candidate_id in selected))
            ),
            "projected_term_count": len(
                set().union(*(terms[candidate_id] for candidate_id in selected))
            ),
            "evidence_family_count": len(selected_families),
            "configuration_count": sum(
                authored[candidate_id]["candidate_kind"] == "invariant_configuration"
                for candidate_id in selected
            ),
        },
        "tier_counts": dict(Counter(value["editorial_tier"] for value in selected_values)),
        "disposition_sha256": _canonical_sha256(disposition),
        "provider_operation_count": 0,
    }
    return BoundedSelection(
        tuple(selected_values), tuple(rejected_values), audit, disposition
    )
