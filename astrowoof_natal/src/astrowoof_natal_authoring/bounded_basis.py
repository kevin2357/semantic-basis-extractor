"""Invariant-only candidate construction for admitted bounded Natal families."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .bounded_admission import BoundedAdmission


CANDIDATE_POLICY_CONTRACT = "astrowoof.bounded_natal.candidate_policy.v1"
DISPOSITION_CONTRACT = "astrowoof.bounded_natal.disposition_report.v1"
DEFAULT_FOUNDATIONAL_POLICY = "strong_preference"
FOUNDATIONAL_POLICIES = frozenset(
    {"strong_preference", "mandatory_when_available", "portfolio_neutral"}
)
DIRECT_RELATIONSHIP_TYPES = frozenset(
    {
        "BOUNDED_INVARIANT_ASPECT",
        "BOUNDED_INVARIANT_DECLINATION_PARALLEL",
        "BOUNDED_INVARIANT_DECLINATION_CONTRAPARALLEL",
    }
)
DERIVED_RELATIONSHIP_TYPE = "BOUNDED_INVARIANT_DERIVED_ASPECT"
TOPOLOGY_RELATIONSHIP_TYPES = frozenset(
    {
        "BOUNDED_HAS_ANTISCIA_POINT",
        "BOUNDED_HAS_CONTRA_ANTISCIA_POINT",
        "BOUNDED_HAS_HARMONIC_POINT",
    }
)
PROHIBITED_CANDIDATE_KEYS = frozenset(
    {
        "confidence",
        "structural_strength",
        "structural_strength_score",
        "orb",
        "orb_range",
        "representative_longitude",
        "representative_state",
        "range_evidence",
    }
)


class BoundedCandidateError(ValueError):
    """A machine-classified bounded candidate construction failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class BoundedBasis:
    """Candidate pool and complete private disposition report."""

    candidates: tuple[dict[str, Any], ...]
    disposition_report: dict[str, Any]
    summary: dict[str, Any]


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def _stable_id(kind: str, material: Any) -> str:
    return f"bounded_candidate:{kind}:{_canonical_sha256(material)[:24]}"


def _canonical_owner_ref(value: str) -> str:
    prefix = "canonical:object:"
    return value[len(prefix) :] if value.startswith(prefix) else value


def _evidence_core(record: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = record.get("evidence")
    return nested if isinstance(nested, Mapping) else record


def _evidence_metadata(record: Mapping[str, Any]) -> Mapping[str, Any]:
    value = record.get("evidence_metadata")
    return value if isinstance(value, Mapping) else {}


def _collect_term_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            if (
                key in {"term_ref", "mode_ref", "relation_ref", "interaction_mode_ref"}
                and isinstance(child, str)
            ):
                refs.add(child)
            refs.update(_collect_term_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(_collect_term_refs(child))
    return refs


def _evidence_lineage(
    direct_refs: Iterable[str], records: Mapping[str, Any]
) -> dict[str, Any]:
    direct = sorted(set(direct_refs))
    visited: set[str] = set()
    unresolved: set[str] = set()
    pending = list(reversed(direct))
    proof_scopes: set[str] = set()
    classifications: set[str] = set()
    family_groups: set[str] = set()
    independence_groups: set[str] = set()
    record_independence_groups: set[str] = set()
    owner_refs: set[str] = set()
    while pending:
        ref = pending.pop()
        if ref in visited:
            continue
        record = records.get(ref)
        if not isinstance(record, Mapping):
            unresolved.add(ref)
            continue
        visited.add(ref)
        core = _evidence_core(record)
        metadata = _evidence_metadata(record)
        classification = core.get("classification") or record.get("classification")
        if isinstance(classification, str):
            classifications.add(classification)
        proof_scope = core.get("proof_scope")
        if isinstance(proof_scope, str):
            proof_scopes.add(proof_scope)
        for key, target in (
            ("evidence_family_group", family_groups),
            ("independence_group", independence_groups),
            ("record_independence_group", record_independence_groups),
            ("source_owner_object_ref", owner_refs),
            ("target_owner_object_ref", owner_refs),
        ):
            value = metadata.get(key)
            if isinstance(value, str) and value != "unknown":
                target.add(value)
        values = metadata.get("owner_object_refs")
        if isinstance(values, list):
            owner_refs.update(
                item for item in values if isinstance(item, str) and item != "unknown"
            )
        prerequisites = core.get("prerequisite_refs") or []
        pending.extend(
            reversed([item for item in prerequisites if isinstance(item, str)])
        )
    return {
        "direct_evidence_refs": direct,
        "resolved_evidence_refs": sorted(visited),
        "unresolved_prerequisite_refs": sorted(unresolved),
        "classifications": sorted(classifications),
        "proof_scopes": sorted(proof_scopes),
        "evidence_family_groups": sorted(family_groups),
        "independence_groups": sorted(independence_groups),
        "record_independence_groups": sorted(record_independence_groups),
        "owner_object_refs": sorted(owner_refs),
    }


def _context_rows(
    artifacts: Mapping[str, Mapping[str, Any]], row_key: str
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    rows: dict[str, dict[str, Any]] = defaultdict(dict)
    id_maps: dict[str, dict[str, str]] = {}
    for context_id in sorted(artifacts):
        artifact = artifacts[context_id]
        id_maps[context_id] = {
            row["id"]: row["correspondence_id"] for row in artifact.get("objects", [])
        }
        for row in artifact.get(row_key, []):
            correspondence = row.get("correspondence_id")
            if not isinstance(correspondence, str) or not correspondence:
                raise BoundedCandidateError(
                    "bounded_correspondence_missing",
                    f"{row_key} row lacks correspondence_id in {context_id}",
                )
            if correspondence in rows and context_id in rows[correspondence]:
                raise BoundedCandidateError(
                    "bounded_correspondence_duplicate",
                    f"duplicate {correspondence} in {context_id}",
                )
            rows[correspondence][context_id] = dict(row)
    expected = set(artifacts)
    for correspondence, context_rows in rows.items():
        if set(context_rows) != expected:
            raise BoundedCandidateError(
                "bounded_context_record_incomplete",
                f"{correspondence} does not have all four context records",
            )
        if any(
            (row.get("epistemic_basis") or {}).get("classification") != "invariant"
            for row in context_rows.values()
        ):
            raise BoundedCandidateError(
                "bounded_non_invariant_projected_row",
                f"{correspondence} is not invariant in every context",
            )
    return dict(rows), id_maps


def _base_candidate(
    *,
    kind: str,
    correspondence_ids: Iterable[str],
    context_records: Mapping[str, list[dict[str, Any]]],
    evidence_records: Mapping[str, Any],
    foundational_policy: str,
    member_candidate_ids: Iterable[str] = (),
) -> dict[str, Any]:
    correspondence = sorted(set(correspondence_ids))
    ordered_records = {
        context: sorted(records, key=lambda row: row["correspondence_id"])
        for context, records in sorted(context_records.items())
    }
    flat = [row for records in ordered_records.values() for row in records]
    bases = [row.get("epistemic_basis") or {} for row in flat]
    direct_refs = {
        ref
        for basis in bases
        for ref in basis.get("evidence_refs") or []
        if isinstance(ref, str)
    }
    family_groups = {
        group
        for basis in bases
        for group in basis.get("evidence_family_groups") or []
        if isinstance(group, str)
    }
    proof_scopes = {
        basis.get("proof_scope")
        for basis in bases
        if isinstance(basis.get("proof_scope"), str)
    }
    source_refs = {
        ref
        for row in flat
        for key in ("source_refs", "source_relationship_refs")
        for ref in row.get(key) or []
        if isinstance(ref, str)
    }
    owner_refs = {
        _canonical_owner_ref(value)
        for row in flat
        for value in [(row.get("attributes") or {}).get("source_owner_object_ref")]
        if isinstance(value, str) and value
    }
    for row in flat:
        attributes = row.get("attributes") or {}
        if attributes.get("source_object_type") == "bounded_natal_body":
            owner_refs.update(
                _canonical_owner_ref(ref)
                for ref in row.get("source_refs") or []
                if isinstance(ref, str)
            )
    lineage = _evidence_lineage(direct_refs, evidence_records)
    owner_refs.update(_canonical_owner_ref(ref) for ref in lineage["owner_object_refs"])
    lineage["evidence_family_groups"] = sorted(
        family_groups | set(lineage["evidence_family_groups"])
    )
    candidate_material = {
        "kind": kind,
        "correspondence_ids": correspondence,
        "evidence_family_groups": lineage["evidence_family_groups"],
        "member_candidate_ids": sorted(set(member_candidate_ids)),
    }
    status = "not_applicable"
    if kind == "foundational_object":
        status = {
            "strong_preference": "preferred",
            "mandatory_when_available": "mandatory",
            "portfolio_neutral": "eligible",
        }[foundational_policy]
    candidate = {
        "schema_version": CANDIDATE_POLICY_CONTRACT,
        "candidate_id": _stable_id(kind, candidate_material),
        "candidate_kind": kind,
        "candidate_role": "dependency_only" if kind == "topology_dependency" else "authored",
        "epistemic_classification": "invariant",
        "correspondence_ids": correspondence,
        "context_records": ordered_records,
        "source_refs": sorted(source_refs),
        "root_owner_refs": sorted(owner_refs),
        "proof_scopes": sorted(proof_scopes),
        "evidence_lineage": lineage,
        "projected_term_refs": sorted(_collect_term_refs(flat)),
        "member_candidate_ids": sorted(set(member_candidate_ids)),
        "foundational_policy": foundational_policy,
        "foundational_status": status,
        "family_accounting": {
            "raw_correspondence_count": len(correspondence),
            "independent_support_unit_count": 1,
            "raw_record_count_is_weight": False,
        },
    }
    _assert_candidate_safety(candidate)
    return candidate


def _assert_candidate_safety(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = key.lower()
            if lowered in PROHIBITED_CANDIDATE_KEYS:
                raise BoundedCandidateError(
                    "bounded_prohibited_candidate_field",
                    f"prohibited candidate field {'.'.join(path + (key,))}",
                )
            _assert_candidate_safety(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_candidate_safety(child, path + (str(index),))


def build_bounded_basis(
    admission: BoundedAdmission,
    *,
    foundational_policy: str = DEFAULT_FOUNDATIONAL_POLICY,
) -> BoundedBasis:
    """Build a deterministic, family-collapsed invariant candidate pool."""

    if foundational_policy not in FOUNDATIONAL_POLICIES:
        raise BoundedCandidateError(
            "bounded_foundational_policy_unknown",
            f"unsupported foundational policy {foundational_policy!r}",
        )
    artifacts = admission.artifacts_by_context
    object_rows, id_maps = _context_rows(artifacts, "objects")
    relationship_rows, _ = _context_rows(artifacts, "relationships")
    baseline_context = sorted(artifacts)[0]
    baseline = artifacts[baseline_context]
    evidence_records = (baseline.get("source_evidence") or {}).get("records") or {}
    if not isinstance(evidence_records, Mapping):
        raise BoundedCandidateError(
            "bounded_evidence_records_invalid", "source evidence records must be an object"
        )

    candidates: list[dict[str, Any]] = []
    row_dispositions: list[dict[str, Any]] = []
    object_candidate_by_corr: dict[str, str] = {}
    derived_objects: dict[str, list[str]] = defaultdict(list)

    for correspondence in sorted(object_rows):
        rows = object_rows[correspondence]
        exemplar = rows[baseline_context]
        source_type = (exemplar.get("attributes") or {}).get("source_object_type")
        if source_type == "bounded_natal_body":
            candidate = _base_candidate(
                kind="foundational_object",
                correspondence_ids=[correspondence],
                context_records={context: [row] for context, row in rows.items()},
                evidence_records=evidence_records,
                foundational_policy=foundational_policy,
            )
            candidates.append(candidate)
            object_candidate_by_corr[correspondence] = candidate["candidate_id"]
            disposition = "admitted_foundational_object"
        elif source_type in {
            "bounded_antiscia_point",
            "bounded_contra_antiscia_point",
            "bounded_harmonic_point",
        }:
            groups = (exemplar.get("epistemic_basis") or {}).get(
                "evidence_family_groups"
            ) or []
            if len(groups) != 1:
                raise BoundedCandidateError(
                    "bounded_object_family_identity",
                    f"derived object {correspondence} lacks one evidence family",
                )
            derived_objects[groups[0]].append(correspondence)
            disposition = "admitted_derived_family_member"
        else:
            raise BoundedCandidateError(
                "bounded_object_family_unsupported",
                f"unsupported bounded object type {source_type!r}",
            )
        row_dispositions.append(
            {
                "row_kind": "object",
                "correspondence_id": correspondence,
                "source_type": source_type,
                "disposition": disposition,
            }
        )

    for family_group in sorted(derived_objects):
        correspondences = sorted(derived_objects[family_group])
        records = {
            context: [object_rows[corr][context] for corr in correspondences]
            for context in sorted(artifacts)
        }
        candidate = _base_candidate(
            kind="derived_family",
            correspondence_ids=correspondences,
            context_records=records,
            evidence_records=evidence_records,
            foundational_policy=foundational_policy,
        )
        candidates.append(candidate)
        for corr in correspondences:
            object_candidate_by_corr[corr] = candidate["candidate_id"]

    relationship_families: dict[str, list[str]] = defaultdict(list)
    direct_relationships: list[str] = []
    topology_relationships: list[str] = []
    for correspondence in sorted(relationship_rows):
        rows = relationship_rows[correspondence]
        exemplar = rows[baseline_context]
        source_type = (exemplar.get("attributes") or {}).get(
            "source_relationship_type"
        )
        if source_type in DIRECT_RELATIONSHIP_TYPES:
            direct_relationships.append(correspondence)
            disposition = "admitted_individualized_relationship"
        elif source_type == DERIVED_RELATIONSHIP_TYPE:
            groups = (exemplar.get("epistemic_basis") or {}).get(
                "evidence_family_groups"
            ) or []
            if len(groups) != 1:
                raise BoundedCandidateError(
                    "bounded_relationship_family_identity",
                    f"derived relationship {correspondence} lacks one evidence family",
                )
            relationship_families[groups[0]].append(correspondence)
            disposition = "admitted_derived_family_member"
        elif source_type in TOPOLOGY_RELATIONSHIP_TYPES:
            topology_relationships.append(correspondence)
            disposition = "dependency_only_transform_ownership"
        else:
            raise BoundedCandidateError(
                "bounded_relationship_family_unsupported",
                f"unsupported bounded relationship type {source_type!r}",
            )
        row_dispositions.append(
            {
                "row_kind": "relationship",
                "correspondence_id": correspondence,
                "source_type": source_type,
                "disposition": disposition,
            }
        )

    def endpoint_dependencies(correspondences: Iterable[str]) -> list[str]:
        dependencies: set[str] = set()
        for corr in correspondences:
            for context, row in relationship_rows[corr].items():
                for key in ("source_id", "target_id"):
                    endpoint_corr = id_maps[context].get(row.get(key))
                    if endpoint_corr and endpoint_corr in object_candidate_by_corr:
                        dependencies.add(object_candidate_by_corr[endpoint_corr])
        return sorted(dependencies)

    for correspondence in direct_relationships:
        rows = relationship_rows[correspondence]
        candidates.append(
            _base_candidate(
                kind="individualized_relationship",
                correspondence_ids=[correspondence],
                context_records={context: [row] for context, row in rows.items()},
                evidence_records=evidence_records,
                foundational_policy=foundational_policy,
                member_candidate_ids=endpoint_dependencies([correspondence]),
            )
        )

    topology_families: dict[str, list[str]] = defaultdict(list)
    for correspondence in topology_relationships:
        exemplar = relationship_rows[correspondence][baseline_context]
        groups = (exemplar.get("epistemic_basis") or {}).get(
            "evidence_family_groups"
        ) or []
        if len(groups) != 1:
            raise BoundedCandidateError(
                "bounded_topology_family_identity",
                f"topology relationship {correspondence} lacks one evidence family",
            )
        topology_families[groups[0]].append(correspondence)
    for family_group in sorted(topology_families):
        correspondences = sorted(topology_families[family_group])
        candidates.append(
            _base_candidate(
                kind="topology_dependency",
                correspondence_ids=correspondences,
                context_records={
                    context: [
                        relationship_rows[corr][context] for corr in correspondences
                    ]
                    for context in sorted(artifacts)
                },
                evidence_records=evidence_records,
                foundational_policy=foundational_policy,
                member_candidate_ids=endpoint_dependencies(correspondences),
            )
        )

    family_candidate_ids: dict[str, str] = {}
    for family_group in sorted(relationship_families):
        correspondences = sorted(relationship_families[family_group])
        candidate = _base_candidate(
            kind="derived_family",
            correspondence_ids=correspondences,
            context_records={
                context: [relationship_rows[corr][context] for corr in correspondences]
                for context in sorted(artifacts)
            },
            evidence_records=evidence_records,
            foundational_policy=foundational_policy,
            member_candidate_ids=endpoint_dependencies(correspondences),
        )
        candidates.append(candidate)
        family_candidate_ids[family_group] = candidate["candidate_id"]

    # Multiple invariant relationship families between the same root owners form an
    # inspectable initial configuration. Family candidates, not raw records, are its
    # members, so one prolific derived family still contributes one unit.
    configurations: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for family_group, correspondences in relationship_families.items():
        roots: set[str] = set()
        for corr in correspondences:
            exemplar = relationship_rows[corr][baseline_context]
            for endpoint_key in ("source_id", "target_id"):
                endpoint_corr = id_maps[baseline_context].get(exemplar.get(endpoint_key))
                if endpoint_corr:
                    endpoint = object_rows[endpoint_corr][baseline_context]
                    attrs = endpoint.get("attributes") or {}
                    root = attrs.get("source_owner_object_ref")
                    if not root:
                        refs = endpoint.get("source_refs") or []
                        root = refs[0] if refs else endpoint_corr
                    roots.add(_canonical_owner_ref(root))
        if len(roots) >= 2:
            configurations[tuple(sorted(roots))].add(family_group)
    for roots in sorted(configurations):
        families = sorted(configurations[roots])
        if len(families) < 2:
            continue
        members = [family_candidate_ids[family] for family in families]
        candidate = {
            "schema_version": CANDIDATE_POLICY_CONTRACT,
            "candidate_id": _stable_id(
                "invariant_configuration", {"roots": roots, "members": members}
            ),
            "candidate_kind": "invariant_configuration",
            "candidate_role": "authored",
            "epistemic_classification": "invariant",
            "correspondence_ids": sorted(
                {
                    corr
                    for family in families
                    for corr in relationship_families[family]
                }
            ),
            "context_records": {},
            "source_refs": [],
            "root_owner_refs": list(roots),
            "proof_scopes": sorted(
                {
                    (row.get("epistemic_basis") or {}).get("proof_scope")
                    for family in families
                    for corr in relationship_families[family]
                    for row in relationship_rows[corr].values()
                }
            ),
            "evidence_lineage": {
                "evidence_family_groups": families,
                "independence_groups": families,
                "record_independence_groups": [],
            },
            "projected_term_refs": [],
            "member_candidate_ids": members,
            "foundational_policy": foundational_policy,
            "foundational_status": "not_applicable",
            "family_accounting": {
                "raw_correspondence_count": sum(
                    len(relationship_families[family]) for family in families
                ),
                "independent_support_unit_count": len(families),
                "raw_record_count_is_weight": False,
            },
        }
        _assert_candidate_safety(candidate)
        candidates.append(candidate)

    candidates.sort(key=lambda value: value["candidate_id"])
    baseline_coverage = (baseline.get("audit") or {}).get("coverage") or {}
    outside_scope = []
    for key, row_kind in (
        ("outside_declared_scope_ids", "object"),
        ("outside_declared_scope_relationship_ids", "relationship"),
    ):
        outside_scope.extend(
            {
                "row_kind": row_kind,
                "source_id": source_id,
                "disposition": "outside_declared_scope",
            }
            for source_id in sorted(baseline_coverage.get(key) or [])
        )
    evidence_dispositions = []
    used_evidence = {
        ref
        for candidate in candidates
        for ref in candidate.get("evidence_lineage", {}).get(
            "resolved_evidence_refs", []
        )
    }
    for ref in sorted(evidence_records):
        record = evidence_records[ref]
        core = _evidence_core(record) if isinstance(record, Mapping) else {}
        classification = core.get("classification") or (
            record.get("classification") if isinstance(record, Mapping) else None
        )
        evidence_dispositions.append(
            {
                "evidence_ref": ref,
                "classification": classification or "unknown",
                "disposition": (
                    "admitted_evidence_lineage"
                    if ref in used_evidence
                    else f"non_admitted_{classification or 'unknown'}"
                ),
            }
        )
    disposition = {
        "schema_version": DISPOSITION_CONTRACT,
        "admission_id": admission.summary["admission_id"],
        "foundational_policy": foundational_policy,
        "projected_rows": sorted(
            row_dispositions,
            key=lambda value: (value["row_kind"], value["correspondence_id"]),
        ),
        "source_evidence": evidence_dispositions,
        "outside_scope": outside_scope,
        "source_feature_dispositions": dict(
            sorted((baseline.get("source_feature_dispositions") or {}).items())
        ),
        "counts": {
            "candidate_count": len(candidates),
            "projected_row_count": len(row_dispositions),
            "evidence_record_count": len(evidence_dispositions),
            "outside_scope_count": len(outside_scope),
        },
    }
    summary = {
        "schema_version": CANDIDATE_POLICY_CONTRACT,
        "admission_id": admission.summary["admission_id"],
        "foundational_policy": foundational_policy,
        "candidate_count": len(candidates),
        "candidate_kind_counts": {
            kind: sum(1 for candidate in candidates if candidate["candidate_kind"] == kind)
            for kind in sorted({candidate["candidate_kind"] for candidate in candidates})
        },
        "candidate_sha256": _canonical_sha256(candidates),
        "disposition_sha256": _canonical_sha256(disposition),
        "provider_operation_count": 0,
    }
    return BoundedBasis(tuple(candidates), disposition, summary)
