"""Compile four projected natal contexts into a closed AstroWoof authoring packet.

The extractor is deliberately deterministic. It selects existing projected
objects and relationships, generates rule-based syntheses, optimizes a
dependency-closed 50-claim portfolio, and emits an LLM-safe authoring packet.
The LLM is allowed to edit prose fields later; it is not allowed to alter the
selected semantics, evidence, dependencies, IDs, or scores.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import zipfile
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from merge_projected_term_registries import merge as merge_projected_term_registries


CONTEXT_FILES = {
    "general": "natal.{subject}.woof.general.json",
    "direct_to_dog": "natal.{subject}.woof.d2d.json",
    "handler": "natal.{subject}.woof.handler.json",
    "hybrid": "natal.{subject}.woof.hybrid.json",
}

MANDATORY_OBJECTS = {
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto", "ASC", "DSC", "MC", "IC",
    "North Node", "Part of Fortune",
}

WEIGHTS = {
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

OBJECT_LABELS = {
    "Sun": "Pack Identity",
    "Moon": "Comfort and Regulation",
    "Mercury": "Signals and Scent",
    "Venus": "Bonding Preference",
    "Mars": "Action and Play Drive",
    "Jupiter": "Adventure Confidence",
    "Saturn": "Training Rule Structure",
    "Uranus": "Novelty and Surprise Response",
    "Neptune": "Atmosphere and Dream Permeability",
    "Pluto": "Deep Trust Intensity",
    "ASC": "Behavioral Doorway",
    "DSC": "Primary Companion Interface",
    "MC": "Visible Pack Function",
    "IC": "Safe-Den Baseline",
    "North Node": "Training Development Vector",
    "Part of Fortune": "Easy Reward Channel",
    "South Node": "Familiar Instinctive Fallback",
    "Vertex": "Unexpected Encounter Trigger",
}

CATEGORY_BY_OBJECT = {
    "Sun": "big3_core_traits", "Moon": "big3_core_traits", "ASC": "angles",
    "DSC": "angles", "MC": "angles", "IC": "angles",
    "North Node": "development", "Part of Fortune": "development",
}

CONTEXT_FILTER_GROUPS = [
    {"name": "Personality", "level": "high"},
    {"name": "Learning", "level": "high"},
    {"name": "Play", "level": "high"},
    {"name": "Adventure", "level": "high"},
    {"name": "Communication", "level": "high"},
    {"name": "Trust", "level": "high"},
    {"name": "Training", "level": "high"},
    {"name": "Pack", "level": "high"},
    {"name": "Core Personality", "level": "detail"},
    {"name": "Mind & Intelligence", "level": "detail"},
    {"name": "Emotions & Inner World", "level": "detail"},
    {"name": "Energy & Motivation", "level": "detail"},
    {"name": "Strengths & Talents", "level": "detail"},
    {"name": "Growth & Potential", "level": "detail"},
    {"name": "Play & Adventure", "level": "detail"},
    {"name": "Learning & Training", "level": "detail"},
    {"name": "Communication", "level": "detail"},
    {"name": "Social & Pack Life", "level": "detail"},
    {"name": "Trust & Security", "level": "detail"},
    {"name": "Stress & Resilience", "level": "detail"},
]

CONTEXT_SUFFIXES = {
    "general": "general",
    "d2d": "direct_to_dog",
    "handler": "handler",
    "hybrid": "hybrid",
}

CONTEXT_ID_MARKERS = {
    "general": "general",
    "direct_to_dog": "dog_direct",
    "handler": "handler",
    "hybrid": "hybrid",
}

CATEGORY_ORDER = [
    "angles",
    "core_traits",
    "development",
    "synthesized_patterns",
    "system_interactions",
    "big3_core_traits",
]


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


def humanize(value: str | None) -> str:
    if not value:
        return "unspecified pattern"
    value = re.sub(r"^(doghouse_\d+_|woofmapped_)", "", value)
    return value.replace("_", " ").replace("-", " ").strip()


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def semantic_terms(record: dict[str, Any]) -> set[str]:
    attrs = record.get("attributes", {})
    values: list[Any] = [
        record.get("name"), record.get("relationship_type"),
        attrs.get("projected_mode"), attrs.get("projected_domain"),
        attrs.get("interaction_mode"), attrs.get("source_canine_subsystem"),
        attrs.get("target_canine_subsystem"),
    ]
    values.extend(record.get("theme_tags", []))
    values.extend(record.get("operators", []))
    terms: set[str] = set()
    for value in values:
        if isinstance(value, str):
            terms.update(t for t in re.split(r"[_\W]+", value.lower()) if len(t) > 2)
    return terms


@dataclass
class Candidate:
    candidate_id: str
    candidate_type: str
    claim_type: str
    categories: list[str]
    canonical_claim: str
    dependencies: list[str]
    source_refs: list[str]
    evidence: list[dict[str, Any]]
    behavioral_domains: list[str]
    tags: list[str]
    score_components: dict[str, float]
    provenance: dict[str, Any]
    mandatory: bool = False
    semantic_role: list[str] = field(default_factory=list)
    eligible_for_selection: bool = True
    variant_of: str | None = None
    variant_kind: str | None = None
    total_score: float = 0.0
    rejection_reason: str | None = None

    def finish_score(self) -> None:
        self.total_score = round(sum(
            WEIGHTS[name] * self.score_components.get(name, 0.0)
            for name in WEIGHTS
        ), 6)

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate_type": self.candidate_type,
            "claim_type": self.claim_type,
            "categories": self.categories,
            "canonical_claim": self.canonical_claim,
            "mandatory": self.mandatory,
            "semantic_role": self.semantic_role,
            "dependencies": self.dependencies,
            "source_refs": self.source_refs,
            "evidence": self.evidence,
            "behavioral_domains": self.behavioral_domains,
            "tags": self.tags,
            "score_components": self.score_components,
            "total_score": self.total_score,
            "provenance": self.provenance,
            "rejection_reason": self.rejection_reason,
            "eligible_for_selection": self.eligible_for_selection,
            **({"variant_of": self.variant_of} if self.variant_of else {}),
            **({"variant_kind": self.variant_kind} if self.variant_kind else {}),
        }


def discover_subject_packages(
    input_package: Path,
    subject_filter: str | None = None,
) -> dict[str, dict[str, Path]]:
    """Discover one four-context file set per subject.

    A package may contain one subject's files directly or one immediate
    subdirectory per subject. Filenames are used for discovery; graph metadata
    is validated separately and remains authoritative for identity.
    """
    if not input_package.is_dir():
        raise NotADirectoryError(f"Input package is not a directory: {input_package}")

    candidate_dirs = [input_package]
    if not any(input_package.glob("natal.*.woof.*.json")):
        candidate_dirs = sorted(path for path in input_package.iterdir() if path.is_dir())

    discovered: dict[str, dict[str, Path]] = defaultdict(dict)
    pattern = re.compile(
        r"^natal\.(?P<subject>.+?)\.woof\.(?P<context>general|d2d|handler|hybrid)\.json$",
        re.IGNORECASE,
    )
    for directory in candidate_dirs:
        for path in sorted(directory.glob("natal.*.woof.*.json")):
            match = pattern.match(path.name)
            if not match:
                continue
            subject = match.group("subject").lower()
            context = CONTEXT_SUFFIXES[match.group("context").lower()]
            if subject_filter and subject != subject_filter.lower():
                continue
            if context in discovered[subject]:
                raise ValueError(
                    f"Duplicate {context} files for subject {subject}: "
                    f"{discovered[subject][context]} and {path}"
                )
            discovered[subject][context] = path

    if not discovered:
        suffix = f" for subject {subject_filter!r}" if subject_filter else ""
        raise FileNotFoundError(f"No projected natal context files found{suffix}.")

    return dict(sorted(discovered.items()))


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _source_ref_set(records: list[dict[str, Any]], field_name: str) -> set[str]:
    return {
        ref
        for record in records
        for ref in record.get(field_name, [])
    }


def load_and_validate_contexts(
    subject: str,
    paths: dict[str, Path],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    required = set(CONTEXT_FILES)
    missing = sorted(required - set(paths))
    extra = sorted(set(paths) - required)
    if missing or extra:
        raise ValueError(
            f"Subject {subject} must have exactly the four contexts; "
            f"missing={missing}, extra={extra}"
        )
    contexts = {
        context: json.loads(path.read_text(encoding="utf-8"))
        for context, path in sorted(paths.items())
    }
    general = contexts["general"]
    expected_identity = general.get("source_identity")
    expected_graph = general.get("source_graph_ref")
    expected_ontology = general.get("target_ontology")
    expected_objects = _source_ref_set(general.get("objects", []), "source_refs")
    expected_relationships = _source_ref_set(
        general.get("relationships", []), "source_relationship_refs"
    )
    expected_chart_id = f"natal:{subject}"

    errors: list[str] = []
    for context, graph in sorted(contexts.items()):
        identity = graph.get("source_identity")
        chart_ids = set((identity or {}).get("source_chart_ids", []))
        chart_id = (identity or {}).get("source_chart_id")
        if (
            _canonical_json(identity) != _canonical_json(expected_identity)
            or (chart_id and chart_id != expected_chart_id)
            or (chart_ids and expected_chart_id not in chart_ids)
        ):
            errors.append(f"{context}: subject identity does not match {expected_chart_id}")
        if _canonical_json(graph.get("source_graph_ref")) != _canonical_json(expected_graph):
            errors.append(f"{context}: source_graph_ref differs from general")
        if graph.get("target_ontology") != expected_ontology:
            errors.append(f"{context}: target_ontology differs from general")
        context_id = str(
            graph.get("metadata", {}).get("projection_context_id")
            or graph.get("metadata", {}).get("context_id")
            or ""
        ).lower()
        if CONTEXT_ID_MARKERS[context] not in context_id:
            errors.append(
                f"{context}: metadata context ID {context_id!r} does not match"
            )
        if _source_ref_set(graph.get("objects", []), "source_refs") != expected_objects:
            errors.append(f"{context}: canonical object source refs differ from general")
        if (
            _source_ref_set(graph.get("relationships", []), "source_relationship_refs")
            != expected_relationships
        ):
            errors.append(f"{context}: canonical relationship source refs differ from general")

    if errors:
        raise ValueError(
            f"Incompatible projected contexts for subject {subject}: "
            + "; ".join(errors)
        )

    merged_registry, registry_audit = merge_projected_term_registries(
        [paths[context] for context in sorted(paths)]
    )
    input_audit = {
        "subject": subject,
        "input_files": {
            context: str(paths[context].resolve()) for context in sorted(paths)
        },
        "source_identity": expected_identity,
        "source_graph_ref": expected_graph,
        "target_ontology": expected_ontology,
        "object_source_ref_count": len(expected_objects),
        "relationship_source_ref_count": len(expected_relationships),
        "registry_merge": registry_audit,
        "status": "pass",
    }
    return contexts, merged_registry, input_audit


def load_contexts(input_dir: Path, subject: str) -> dict[str, dict[str, Any]]:
    """Backward-compatible single-subject loader used by older callers."""
    packages = discover_subject_packages(input_dir, subject)
    contexts, _, _ = load_and_validate_contexts(subject, packages[subject.lower()])
    return contexts


def index_contexts(contexts: dict[str, dict[str, Any]]) -> tuple[dict, dict]:
    objects: dict[str, dict[str, Any]] = defaultdict(dict)
    relationships: dict[str, dict[str, Any]] = defaultdict(dict)
    for context, graph in contexts.items():
        for record in graph["objects"]:
            key = record["source_refs"][0]
            objects[key][context] = record
        for record in graph["relationships"]:
            key = record["source_relationship_refs"][0]
            relationships[key][context] = record
    return dict(objects), dict(relationships)


def object_name(record: dict[str, Any]) -> str:
    return record.get("attributes", {}).get("canonical_object_name") or record.get("name", "")


def context_evidence(kind: str, records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    general = records.get("general") or next(iter(records.values()))
    return {
        "kind": kind,
        "role": "primary",
        "source_refs": general.get("source_refs", general.get("source_relationship_refs", [])),
        "context_records": {
            context: {
                "id": record["id"],
                "context_refs": record.get("context_refs", []),
                "projection_relevance_score": record.get("projection_relevance_score", 0),
                "structural_strength_score": record.get("structural_strength_score",
                                                        record.get("attributes", {}).get(
                                                            "projection_relevance_components", {}
                                                        ).get("structural_strength", 0)),
                "record": record,
            }
            for context, record in sorted(records.items())
        },
    }


def build_candidates(contexts: dict[str, dict[str, Any]]) -> tuple[list[Candidate], dict[str, Any]]:
    objects, relationships = index_contexts(contexts)
    general = contexts["general"]
    object_by_id = {x["id"]: x for x in general["objects"]}
    # The projected graph may materialize symmetric natal aspects in both
    # directions. Canonicalize them by unordered canonical endpoints, aspect,
    # and orb while retaining every canonical source relationship reference.
    canonical_relationships: dict[str, dict[str, dict[str, Any]]] = {}
    relationship_aliases: dict[str, list[str]] = {}
    for source_ref, records in relationships.items():
        record = records.get("general") or next(iter(records.values()))
        attrs = record.get("attributes", {})
        endpoint_refs = sorted([
            object_by_id[record["source_id"]]["source_refs"][0],
            object_by_id[record["target_id"]]["source_refs"][0],
        ])
        signature = "|".join([
            *endpoint_refs,
            str(attrs.get("canonical_aspect")),
            f"{float(attrs.get('orb') or 0):.6f}",
        ])
        relationship_aliases.setdefault(signature, []).append(source_ref)
        if signature not in canonical_relationships:
            canonical_relationships[signature] = records
        else:
            for context, candidate_record in records.items():
                incumbent = canonical_relationships[signature].get(context)
                if incumbent is None or candidate_record.get(
                    "projection_relevance_score", 0
                ) > incumbent.get("projection_relevance_score", 0):
                    canonical_relationships[signature][context] = candidate_record
    relationships = canonical_relationships
    degrees = Counter()
    for rel in general["relationships"]:
        degrees[rel["source_id"]] += 1
        degrees[rel["target_id"]] += 1
    max_degree = max(degrees.values()) if degrees else 1
    mode_counts = Counter(x.get("attributes", {}).get("projected_mode") for x in general["objects"])
    domain_counts = Counter(x.get("attributes", {}).get("projected_domain") for x in general["objects"])
    interaction_counts = Counter(
        x.get("attributes", {}).get("interaction_mode") for x in general["relationships"]
    )

    candidates: list[Candidate] = []
    object_candidate_by_projected_id: dict[str, str] = {}

    for source_ref, records in sorted(objects.items()):
        record = records.get("general") or next(iter(records.values()))
        attrs = record.get("attributes", {})
        name = object_name(record)
        cid = stable_id("placement", source_ref)
        object_candidate_by_projected_id[record["id"]] = cid
        label = OBJECT_LABELS.get(name, humanize(record.get("name")).title())
        mode = humanize(attrs.get("projected_mode"))
        domain = humanize(attrs.get("projected_domain"))
        claim = f"{label} operates in {mode} through {domain}."
        mandatory = name in MANDATORY_OBJECTS
        centrality = degrees[record["id"]] / max_degree
        rarity = 1 / max(1, mode_counts[attrs.get("projected_mode")])
        components = {
            "core_salience": 1.0 if mandatory else 0.45,
            "structural": clamp(record.get("structural_strength_score", 0) / 0.55),
            "projected_relevance": clamp(record.get("projection_relevance_score", 0) / 0.55),
            "evidence": clamp(len(records) / 4),
            "centrality": clamp(centrality),
            "coverage": clamp(0.55 + 0.45 * rarity),
            "distinctiveness": clamp(rarity),
            "compression": 0.0,
            "narrative_yield": clamp(0.55 + 0.04 * len(record.get("operators", []))),
            "voice_yield": clamp(len(records) / 4),
            "humor_affordance": clamp(0.35 + 0.04 * len(semantic_terms(record))),
            "redundancy_penalty": clamp(1 - rarity),
            "dependency_cost": 0.0,
        }
        candidate = Candidate(
            candidate_id=cid,
            candidate_type="mandatory_basis" if mandatory else "projected_object",
            claim_type=("angle" if name in {"ASC", "DSC", "MC", "IC"}
                        else "orientation" if name in {"North Node", "South Node"}
                        else "placement"),
            categories=(
                ["angles", "big3_core_traits"]
                if name == "ASC"
                else [CATEGORY_BY_OBJECT.get(name, "core_traits")]
            ),
            canonical_claim=claim,
            dependencies=[],
            source_refs=[source_ref],
            evidence=[context_evidence("projected_object", records)],
            behavioral_domains=sorted(set(filter(None, [
                attrs.get("projected_domain"), *attrs.get("canine_domains", [])
            ]))),
            tags=sorted(set(filter(None, [
                record.get("name"), attrs.get("projected_mode"), attrs.get("projected_domain")
            ]))),
            score_components=components,
            provenance={"generation_rule": "projected_object.v1", "canonical_object_name": name},
            mandatory=mandatory,
            semantic_role=["anchor", "primitive"] if mandatory else ["primitive"],
        )
        candidate.finish_score()
        candidates.append(candidate)

    relationship_candidate_by_source_ref: dict[str, str] = {}
    for relationship_signature, records in sorted(relationships.items()):
        record = records.get("general") or next(iter(records.values()))
        attrs = record.get("attributes", {})
        source_obj = object_by_id[record["source_id"]]
        target_obj = object_by_id[record["target_id"]]
        source_name = object_name(source_obj)
        target_name = object_name(target_obj)
        source_label = OBJECT_LABELS.get(source_name, humanize(source_obj.get("name")).title())
        target_label = OBJECT_LABELS.get(target_name, humanize(target_obj.get("name")).title())
        relation = humanize(record.get("relationship_type"))
        interaction = humanize(attrs.get("interaction_mode"))
        aliases = sorted(relationship_aliases[relationship_signature])
        cid = stable_id("relationship", relationship_signature)
        for source_ref in aliases:
            relationship_candidate_by_source_ref[source_ref] = cid
        dependencies = [
            object_candidate_by_projected_id[record["source_id"]],
            object_candidate_by_projected_id[record["target_id"]],
        ]
        centrality = (
            degrees[record["source_id"]] + degrees[record["target_id"]]
        ) / (2 * max_degree)
        exactness = 1 / (1 + max(0, float(attrs.get("orb") or 0)) / 3)
        rarity = 1 / max(1, interaction_counts[attrs.get("interaction_mode")])
        components = {
            "core_salience": clamp(
                0.3 + 0.25 * (source_name in MANDATORY_OBJECTS)
                + 0.25 * (target_name in MANDATORY_OBJECTS)
            ),
            "structural": clamp(
                attrs.get("projection_relevance_components", {}).get("structural_strength", 0) / 0.55
            ),
            "projected_relevance": clamp(record.get("projection_relevance_score", 0) / 0.55),
            "evidence": clamp(0.6 * len(records) / 4 + 0.4 * exactness),
            "centrality": clamp(centrality),
            "coverage": clamp(0.5 + 0.5 * rarity),
            "distinctiveness": clamp(0.45 * rarity + 0.55 * exactness),
            "compression": 0.0,
            "narrative_yield": clamp(
                0.45 + 0.04 * len(record.get("operators", []))
                + 0.05 * len(record.get("theme_tags", []))
            ),
            "voice_yield": clamp(len(records) / 4),
            "humor_affordance": clamp(0.3 + 0.025 * len(semantic_terms(record))),
            "redundancy_penalty": clamp(1 - rarity),
            "dependency_cost": clamp(sum(
                1 for dep in dependencies
                if not next(x for x in candidates if x.candidate_id == dep).mandatory
            ) / 2),
        }
        candidate = Candidate(
            candidate_id=cid,
            candidate_type="projected_relationship",
            claim_type="system_interaction",
            categories=["system_interactions"],
            canonical_claim=(
                f"{source_label} and {target_label} are linked through {relation}, "
                f"creating {interaction}."
            ),
            dependencies=dependencies,
            source_refs=aliases,
            evidence=[context_evidence("projected_relationship", records)],
            behavioral_domains=sorted(set(filter(None, [
                attrs.get("source_doghouse"), attrs.get("target_doghouse"),
                attrs.get("source_canine_subsystem"), attrs.get("target_canine_subsystem"),
            ]))),
            tags=sorted(set(record.get("theme_tags", []) + [
                record.get("relationship_type"), attrs.get("interaction_mode")
            ])),
            score_components=components,
            provenance={
                "generation_rule": "projected_relationship.v1",
                "canonical_aspect": attrs.get("canonical_aspect"),
                "orb": attrs.get("orb"),
                "canonicalized_source_relationship_refs": aliases,
            },
            semantic_role=["bridge", "structural"],
        )
        candidate.finish_score()
        candidates.append(candidate)

    # Rule-based syntheses from repeated object modes/domains and relationship modes/tags.
    general_object_candidates = {
        object_name(record): object_candidate_by_projected_id[record["id"]]
        for record in general["objects"]
    }

    def add_synthesis(
        rule: str,
        key: str,
        claim: str,
        dependencies: list[str],
        domains: list[str],
        tags: list[str],
        evidence_records: list[dict[str, Any]],
        evidence_strength: float,
        *,
        candidate_type: str = "synthesized_motif",
        eligible_for_selection: bool = True,
        variant_of: str | None = None,
        variant_kind: str | None = None,
    ) -> Candidate | None:
        dependencies = sorted(set(dependencies))
        if len(dependencies) < 2:
            return None
        id_prefix = "synthesis_variant" if variant_of else "synthesis"
        cid = stable_id(id_prefix, rule, key, *dependencies)
        dep_count = len(dependencies)
        components = {
            "core_salience": clamp(0.35 + 0.06 * dep_count),
            "structural": clamp(0.35 + 0.08 * dep_count),
            "projected_relevance": clamp(evidence_strength),
            "evidence": clamp(0.45 + 0.1 * dep_count),
            "centrality": clamp(0.35 + 0.08 * dep_count),
            "coverage": clamp(0.45 + 0.09 * len(set(domains))),
            "distinctiveness": clamp(0.65 + 0.04 * dep_count),
            "compression": clamp((dep_count - 1) / dep_count),
            "narrative_yield": clamp(0.65 + 0.06 * dep_count),
            "voice_yield": 0.85,
            "humor_affordance": clamp(0.55 + 0.04 * len(set(tags))),
            "redundancy_penalty": clamp(0.12 * max(0, dep_count - 3)),
            "dependency_cost": clamp(dep_count / 8),
        }
        candidate = Candidate(
            candidate_id=cid,
            candidate_type=candidate_type,
            claim_type="synthesized_theme",
            categories=["synthesized_patterns"],
            canonical_claim=claim,
            dependencies=dependencies,
            source_refs=sorted(set(
                ref for evidence in evidence_records
                for ref in evidence.get("source_refs", evidence.get("source_relationship_refs", []))
            )),
            evidence=[{
                "kind": "synthesis_derivation",
                "role": "derivation",
                "generation_rule": rule,
                "shared_key": key,
                "supporting_candidate_ids": dependencies,
                "source_record_summaries": evidence_records,
            }],
            behavioral_domains=sorted(set(filter(None, domains))),
            tags=sorted(set(filter(None, tags + [key]))),
            score_components=components,
            provenance={"generation_rule": rule, "deterministic": True},
            semantic_role=["compressor", "reinforcement", "abstraction"],
            eligible_for_selection=eligible_for_selection,
            variant_of=variant_of,
            variant_kind=variant_kind,
        )
        candidate.finish_score()
        candidates.append(candidate)
        return candidate

    object_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in general["objects"]:
        attrs = record.get("attributes", {})
        if attrs.get("projected_mode"):
            object_groups[("mode", attrs["projected_mode"])].append(record)
        if attrs.get("projected_domain"):
            object_groups[("domain", attrs["projected_domain"])].append(record)
    for (group_type, key), records in sorted(object_groups.items()):
        if len(records) < 2:
            continue
        deps = [object_candidate_by_projected_id[x["id"]] for x in records]
        labels = [OBJECT_LABELS.get(object_name(x), humanize(x.get("name")).title()) for x in records]
        if group_type == "mode":
            claim = (
                f"{', '.join(labels[:-1])} and {labels[-1]} repeatedly express "
                f"{humanize(key)}, making that style a recurring part of the dog's behavior."
            )
        else:
            claim = (
                f"{', '.join(labels[:-1])} and {labels[-1]} converge in "
                f"{humanize(key)}, concentrating several needs in the same life domain."
            )
        add_synthesis(
            f"object_{group_type}_reinforcement.v1", key, claim, deps,
            [x.get("attributes", {}).get("projected_domain") for x in records],
            [x.get("attributes", {}).get("projected_mode") for x in records],
            [{
                "id": x["id"], "source_refs": x.get("source_refs", []),
                "canonical_object_name": object_name(x),
                "projected_mode": x.get("attributes", {}).get("projected_mode"),
                "projected_domain": x.get("attributes", {}).get("projected_domain"),
            } for x in records],
            sum(x.get("projection_relevance_score", 0) for x in records) / max(1, len(records)) / 0.55,
        )

    relation_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in general["relationships"]:
        interaction = record.get("attributes", {}).get("interaction_mode")
        if interaction:
            relation_groups[("interaction", interaction)].append(record)
        for tag in record.get("theme_tags", []):
            relation_groups[("theme", tag)].append(record)
    for (group_type, key), records in sorted(relation_groups.items()):
        if len(records) < 2:
            continue
        all_ranked = sorted(
            records,
            key=lambda x: (
                -x.get("projection_relevance_score", 0),
                x.get("id", ""),
            ),
        )
        ranked = all_ranked[:4]
        deps = [
            relationship_candidate_by_source_ref[x["source_relationship_refs"][0]]
            for x in ranked
        ]
        source_labels = []
        domains = []
        for record in ranked:
            attrs = record.get("attributes", {})
            source_labels.extend([
                humanize(attrs.get("source_canine_subsystem")),
                humanize(attrs.get("target_canine_subsystem")),
            ])
            domains.extend([attrs.get("source_doghouse"), attrs.get("target_doghouse")])
        claim = (
            f"Several systems repeatedly participate in {humanize(key)}, making "
            f"{humanize(key)} a recurring whole-chart pattern rather than a one-off interaction."
        )
        compact = add_synthesis(
            f"relationship_{group_type}_reinforcement.v1", key, claim, deps,
            domains, [key] + source_labels,
            [{
                "id": x["id"],
                "source_relationship_refs": x.get("source_relationship_refs", []),
                "relationship_type": x.get("relationship_type"),
                "interaction_mode": x.get("attributes", {}).get("interaction_mode"),
                "theme_tags": x.get("theme_tags", []),
            } for x in ranked],
            sum(x.get("projection_relevance_score", 0) for x in ranked) / len(ranked) / 0.55,
        )
        if compact and len(all_ranked) > len(ranked):
            all_dependencies = [
                relationship_candidate_by_source_ref[x["source_relationship_refs"][0]]
                for x in all_ranked
            ]
            all_labels: list[str] = []
            all_domains: list[str] = []
            for record in all_ranked:
                attrs = record.get("attributes", {})
                all_labels.extend([
                    humanize(attrs.get("source_canine_subsystem")),
                    humanize(attrs.get("target_canine_subsystem")),
                ])
                all_domains.extend([
                    attrs.get("source_doghouse"),
                    attrs.get("target_doghouse"),
                ])
            add_synthesis(
                f"relationship_{group_type}_reinforcement.maximal.v1",
                key,
                claim,
                all_dependencies,
                all_domains,
                [key] + all_labels,
                [{
                    "id": x["id"],
                    "source_relationship_refs": x.get("source_relationship_refs", []),
                    "relationship_type": x.get("relationship_type"),
                    "interaction_mode": x.get("attributes", {}).get("interaction_mode"),
                    "theme_tags": x.get("theme_tags", []),
                } for x in all_ranked],
                (
                    sum(x.get("projection_relevance_score", 0) for x in all_ranked)
                    / len(all_ranked)
                    / 0.55
                ),
                candidate_type="synthesized_motif_variant",
                eligible_for_selection=False,
                variant_of=compact.candidate_id,
                variant_kind="maximal_support",
            )

    # Collapse exact duplicate synthesis statements produced by different
    # detectors. Keep the stronger deterministic derivation.
    candidates_before_deduplication = list(candidates)
    deduplicated: dict[tuple[str, str], Candidate] = {}
    for candidate in candidates:
        signature = (candidate.candidate_type, candidate.canonical_claim)
        incumbent = deduplicated.get(signature)
        if incumbent is None or (
            candidate.total_score, candidate.candidate_id
        ) > (
            incumbent.total_score, incumbent.candidate_id
        ):
            deduplicated[signature] = candidate
    candidates = list(deduplicated.values())
    surviving_ids = {candidate.candidate_id for candidate in candidates}
    removed_by_id = {
        candidate.candidate_id: candidate
        for candidate in candidates_before_deduplication
        if candidate.candidate_id not in surviving_ids
    }
    surviving_syntheses_by_claim = {
        candidate.canonical_claim: candidate
        for candidate in candidates
        if candidate.candidate_type == "synthesized_motif"
    }
    for candidate in candidates:
        if candidate.variant_of and candidate.variant_of not in surviving_ids:
            removed_base = removed_by_id.get(candidate.variant_of)
            replacement = (
                surviving_syntheses_by_claim.get(removed_base.canonical_claim)
                if removed_base
                else None
            )
            if replacement is None:
                raise AssertionError(
                    f"Unable to rebase maximal synthesis variant {candidate.candidate_id}"
                )
            candidate.variant_of = replacement.candidate_id
    surviving_by_id = {candidate.candidate_id: candidate for candidate in candidates}
    retained_candidates: list[Candidate] = []
    for candidate in candidates:
        if candidate.variant_of:
            base = surviving_by_id[candidate.variant_of]
            candidate.dependencies = sorted(
                set(candidate.dependencies) | set(base.dependencies)
            )
            if not (set(candidate.dependencies) - set(base.dependencies)):
                continue
            candidate.candidate_id = stable_id(
                "synthesis_variant",
                candidate.provenance.get("generation_rule", ""),
                candidate.variant_of,
                *candidate.dependencies,
            )
        retained_candidates.append(candidate)
    candidates = retained_candidates

    analysis = {
        "subject": general.get("source_identity", {}),
        "object_count": len(objects),
        "relationship_count": len(relationships),
        "raw_relationship_count": len(general["relationships"]),
        "directional_relationship_duplicates_collapsed": (
            len(general["relationships"]) - len(relationships)
        ),
        "candidate_counts": dict(Counter(x.candidate_type for x in candidates)),
        "dominant_projected_modes": mode_counts.most_common(),
        "dominant_projected_domains": domain_counts.most_common(),
        "dominant_interaction_modes": interaction_counts.most_common(),
        "highest_degree_objects": sorted([
            {
                "canonical_object_name": object_name(record),
                "projected_name": record.get("name"),
                "degree": degrees[record["id"]],
            }
            for record in general["objects"]
        ], key=lambda x: (-x["degree"], x["canonical_object_name"])),
        "whole_graph_voice_brief": {
            "status": "deterministic_structural_seed_for_llm_editor",
            "guidance": (
                "Use dominant modes, domains, hubs, and selected tensions to infer a coherent "
                "dog-specific voice. Do not treat this seed as evidence and do not import "
                "discarded graph facts into card prose."
            ),
        },
    }
    return candidates, analysis


def optimize(candidates: list[Candidate], budget: int = 50) -> tuple[list[Candidate], list[Candidate], list[dict]]:
    by_id = {x.candidate_id: x for x in candidates}
    selected_ids = {x.candidate_id for x in candidates if x.mandatory}
    if len(selected_ids) != 16:
        mandatory_names = sorted(
            x.provenance.get("canonical_object_name")
            for x in candidates if x.mandatory
        )
        raise AssertionError(f"Expected 16 mandatory candidates, got {mandatory_names}")

    audit: list[dict[str, Any]] = []

    def closure(candidate_id: str, trail: set[str] | None = None) -> set[str]:
        trail = set() if trail is None else trail
        if candidate_id in trail:
            raise AssertionError(f"Dependency cycle at {candidate_id}")
        trail.add(candidate_id)
        result = {candidate_id}
        for dep in by_id[candidate_id].dependencies:
            if dep not in by_id:
                raise AssertionError(f"Unknown dependency {dep}")
            result.update(closure(dep, trail.copy()))
        return result

    while len(selected_ids) < budget:
        best: tuple[float, float, str, set[str]] | None = None
        for candidate in candidates:
            if candidate.candidate_id in selected_ids or not candidate.eligible_for_selection:
                continue
            bundle = closure(candidate.candidate_id) - selected_ids
            if len(selected_ids) + len(bundle) > budget:
                continue
            # Bundle-aware value: all new premises count, with a small coherence bonus.
            bundle_score = sum(by_id[cid].total_score for cid in bundle)
            coverage_terms = set().union(*(set(by_id[cid].behavioral_domains) for cid in bundle))
            existing_terms = set().union(*(set(by_id[cid].behavioral_domains) for cid in selected_ids))
            novelty = len(coverage_terms - existing_terms) / max(1, len(coverage_terms))
            marginal = bundle_score / len(bundle) + 0.05 * novelty + 0.01 / len(bundle)
            key = (round(marginal, 9), candidate.total_score, candidate.candidate_id, bundle)
            if best is None or key[:3] > best[:3]:
                best = key
        if best is None:
            # Fill a pathological residual slot with the best dependency-free candidate.
            remaining = [
                x for x in candidates
                if x.candidate_id not in selected_ids
                and x.eligible_for_selection
                and not (closure(x.candidate_id) - selected_ids - {x.candidate_id})
            ]
            if not remaining:
                raise AssertionError("Unable to fill selection budget")
            candidate = max(remaining, key=lambda x: (x.total_score, x.candidate_id))
            bundle = {candidate.candidate_id}
            marginal = candidate.total_score
        else:
            marginal, _, candidate_id, bundle = best
            candidate = by_id[candidate_id]
        selected_ids.update(bundle)
        audit.append({
            "decision": len(audit) + 1,
            "winning_candidate_id": candidate.candidate_id,
            "bundle_added": sorted(bundle),
            "bundle_cost": len(bundle),
            "marginal_utility": round(float(marginal), 6),
            "selected_count_after": len(selected_ids),
        })

    selected = [by_id[cid] for cid in selected_ids]
    selected.sort(key=lambda x: (-x.total_score, x.candidate_id))
    rejected = [x for x in candidates if x.candidate_id not in selected_ids]
    selected_domains = Counter(d for x in selected for d in x.behavioral_domains)
    selected_signatures = Counter(
        (x.candidate_type, tuple(sorted(x.tags[:3]))) for x in selected
    )
    for candidate in rejected:
        if not candidate.eligible_for_selection:
            candidate.rejection_reason = (
                "Preserved maximal-support synthesis variant; not eligible for "
                "the closed 50-claim authoring portfolio."
            )
        elif candidate.candidate_type == "synthesized_motif":
            missing = [x for x in candidate.dependencies if x not in selected_ids]
            candidate.rejection_reason = (
                f"Not selected within budget; closure would additionally require "
                f"{len(missing)} unselected premise(s)."
            )
        elif any(selected_signatures[(candidate.candidate_type, tuple(sorted(candidate.tags[:3])))] > 0
                 for _ in [0]):
            candidate.rejection_reason = "Lower marginal utility than a selected candidate with overlapping semantics."
        else:
            candidate.rejection_reason = "Lower marginal portfolio utility at the 50-claim budget."
    return selected, rejected, audit


def blank_voice_map() -> dict[str, str]:
    return {
        "handler": "__LLM_FILL__",
        "direct_to_dog": "__LLM_FILL__",
        "hybrid": "__LLM_FILL__",
    }


def blank_rendering() -> dict[str, Any]:
    return {
        "headline": blank_voice_map(),
        "body": blank_voice_map(),
    }


def blank_card() -> dict[str, Any]:
    return {
        "funny_dog_quotes": ["__LLM_FILL__"],
        "imperative_dog_quotes": ["__LLM_FILL__"],
        "applicable_canine_jokes": ["__LLM_FILL__"],
        "no_astro": blank_rendering(),
        "light_astro": blank_rendering(),
        "full_astro": blank_rendering(),
    }


def blank_summary_card() -> dict[str, Any]:
    return {
        "dos": ["__LLM_FILL__"],
        "donts": ["__LLM_FILL__"],
        **blank_card(),
    }


def unselected_claim_records(
    selected: list[Candidate],
    rejected: list[Candidate],
) -> list[dict[str, Any]]:
    all_candidates = {x.candidate_id: x for x in [*selected, *rejected]}
    selected_ids = {x.candidate_id for x in selected}
    records = []
    for candidate in sorted(rejected, key=lambda x: (-x.total_score, x.candidate_id)):
        record = {
            "claim_id": candidate.candidate_id,
            "claim_type": candidate.claim_type,
            "candidate_type": candidate.candidate_type,
            "categories": candidate.categories,
            **({"variant_of": candidate.variant_of} if candidate.variant_of else {}),
            **({"variant_kind": candidate.variant_kind} if candidate.variant_kind else {}),
            "canonical_claim": candidate.canonical_claim,
            "dependencies": candidate.dependencies,
            "source_refs": candidate.source_refs,
            "behavioral_domains": candidate.behavioral_domains,
            "tags": candidate.tags,
            "evidence": candidate.evidence,
            "score_components": candidate.score_components,
            "total_score": candidate.total_score,
            "provenance": candidate.provenance,
            "selection": {
                "selected": False,
                "eligible_for_selection": candidate.eligible_for_selection,
                "rejection_reason": candidate.rejection_reason,
                "selected_dependency_ids": sorted(
                    dep for dep in candidate.dependencies if dep in selected_ids
                ),
                "unselected_dependency_ids": sorted(
                    dep for dep in candidate.dependencies if dep not in selected_ids
                ),
            },
        }
        if candidate.variant_of:
            base = all_candidates.get(candidate.variant_of)
            base_dependencies = set(base.dependencies if base else [])
            record["additional_supporting_claim_ids"] = sorted(
                set(candidate.dependencies) - base_dependencies
            )
        records.append(record)
    return records


def compile_packet(
    subject: str,
    contexts: dict[str, dict[str, Any]],
    selected: list[Candidate],
    rejected: list[Candidate],
    analysis: dict[str, Any],
    projected_term_registry: dict[str, Any],
    input_audit: dict[str, Any],
) -> dict[str, Any]:
    general = contexts["general"]
    ordered_ids = {candidate.candidate_id: i + 1 for i, candidate in enumerate(selected)}
    max_score = max(x.total_score for x in selected)
    cards = []
    for index, candidate in enumerate(selected, 1):
        dependency_ids = [
            dep for dep in candidate.dependencies if dep in ordered_ids
        ]
        evidence = deepcopy(candidate.evidence)
        if dependency_ids:
            evidence.append({
                "kind": "selected_claim_dependencies",
                "role": "derivation_support",
                "claim_ids": dependency_ids,
                "priority_ids": [ordered_ids[dep] for dep in dependency_ids],
            })
        confidence = clamp(candidate.score_components["evidence"])
        strength = clamp(
            0.55 * candidate.score_components["structural"]
            + 0.45 * candidate.score_components["projected_relevance"]
        )
        cards.append({
            "claim_id": candidate.candidate_id,
            "claim_type": candidate.claim_type,
            "categories": candidate.categories,
            **({
                "theme_group": "__LLM_FILL__",
            } if (
                candidate.candidate_type == "projected_relationship"
                or candidate.claim_type == "synthesized_theme"
            ) else {}),
            "context_filter_groups": {
                "high_level": [],
                "detail_level": [],
            },
            "canonical_claim": candidate.canonical_claim,
            "importance": clamp(candidate.total_score / max_score),
            "confidence": confidence,
            "strength": strength,
            "priority_id": index,
            "selection": {
                "mandatory": candidate.mandatory,
                "semantic_roles": candidate.semantic_role,
                "score_components": candidate.score_components,
                "total_score": candidate.total_score,
                "editing_lock": [
                    "claim_id", "claim_type", "categories", "importance", "confidence",
                    "strength", "priority_id", "selection", "evidence", "relations",
                ],
            },
            "behavioral_domains": candidate.behavioral_domains,
            "tags": candidate.tags,
            "evidence": evidence,
            "relations": {
                "reinforces": dependency_ids if candidate.claim_type == "synthesized_theme" else [],
                "tensions_with": [],
                "related_claims": dependency_ids if candidate.claim_type != "synthesized_theme" else [],
            },
            "dos": ["__LLM_FILL__"],
            "donts": ["__LLM_FILL__"],
            "card": blank_card(),
        })

    domains = sorted(set(d for x in cards for d in x["behavioral_domains"]))
    unselected_claims = unselected_claim_records(selected, rejected)
    discovered_categories = set(
        category
        for claim in [*cards, *unselected_claims]
        for category in claim["categories"]
    )
    categories = [
        category for category in CATEGORY_ORDER if category in discovered_categories
    ] + sorted(discovered_categories - set(CATEGORY_ORDER))
    summary = {
        f"card{index}": blank_summary_card()
        for index in range(1, 5)
    }
    return {
        "schema_version": "astrowoof.projected_natal_cards.authoring_packet.v0.3",
        "generator": {
            "semantic_basis_extractor": "projected-sbe.v0.2",
            "candidate_generator": "projected-candidates.v0.2",
            "optimizer": "closed-marginal-portfolio.v0.1",
            "editorial_status": "awaiting_llm",
        },
        "subject": {
            "subject_id": subject,
            "display_name": subject.title(),
            "subject_type": "dog",
            "gender": "",
            "pronouns": {
                "subject": "", "object": "", "possessive_adjective": "",
                "possessive_pronoun": "", "reflexive": "",
            },
            "breed": "", "birth_datetime": "", "birth_location": "",
        },
        "source": {
            "source_graph_ref": general.get("source_graph_ref"),
            "source_identity": general.get("source_identity"),
            "target_ontology": general.get("target_ontology"),
            "contexts": {
                context: graph.get("metadata", {}).get("projection_context_id")
                or graph.get("metadata", {}).get("context_id")
                or graph.get("target_ontology")
                for context, graph in contexts.items()
            },
            "source_hashes": {
                context: hashlib.sha256(
                    json.dumps(graph, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                for context, graph in contexts.items()
            },
            "input_files": input_audit["input_files"],
            "registry_merge": input_audit["registry_merge"],
        },
        "coverage": {
            "projected_object_count": len(general["objects"]),
            "projected_relationship_count": len(general["relationships"]),
            "selected_claim_count": len(cards),
            "unselected_claim_count": len(unselected_claims),
            "guardrails": general.get("summary", {}).get("guardrails", [
                "playful_experimental_projection",
                "not_veterinary_advice",
                "not_behavioral_diagnosis",
                "not_empirically_validated",
            ]),
        },
        "statistics": {
            "total_claims": len(cards),
            "mandatory_claims": sum(x["selection"]["mandatory"] for x in cards),
            "claim_type_counts": dict(Counter(x["claim_type"] for x in cards)),
            "synthesized_claims": sum(x["claim_type"] == "synthesized_theme" for x in cards),
            "unselected_claims": len(unselected_claims),
            "maximal_support_variants": sum(
                x.get("variant_kind") == "maximal_support" for x in unselected_claims
            ),
            "editorial_placeholders": sum(
                json.dumps(value).count("__LLM_FILL__")
                for value in [cards, summary]
            ),
        },
        "categories": categories,
        "behavioral_domains": domains,
        "context_filter_groups": deepcopy(CONTEXT_FILTER_GROUPS),
        "whole_graph_analysis": analysis,
        "summary": summary,
        "cards": cards,
        "unselected_claims": unselected_claims,
        "projected_term_registry": projected_term_registry,
    }


def qa_report(
    candidates: list[Candidate],
    selected: list[Candidate],
    rejected: list[Candidate],
    packet: dict[str, Any],
) -> dict[str, Any]:
    selected_ids = {x.candidate_id for x in selected}
    errors = []
    if len(selected) != 50:
        errors.append(f"Expected 50 selected claims; found {len(selected)}")
    if sum(x.mandatory for x in selected) != 16:
        errors.append("Mandatory basis is not exactly 16 claims")
    for candidate in selected:
        missing = set(candidate.dependencies) - selected_ids
        if missing:
            errors.append(f"{candidate.candidate_id} has missing dependencies: {sorted(missing)}")
        if not candidate.evidence:
            errors.append(f"{candidate.candidate_id} has no evidence")
    card_ids = [x["claim_id"] for x in packet["cards"]]
    if len(card_ids) != len(set(card_ids)):
        errors.append("Duplicate claim IDs in authoring packet")
    registered_categories = set(packet.get("categories", []))
    for index, (candidate, card) in enumerate(zip(selected, packet["cards"]), 1):
        categories = card.get("categories")
        if (
            not isinstance(categories, list)
            or not categories
            or len(categories) != len(set(categories))
            or not all(isinstance(value, str) and value for value in categories)
        ):
            errors.append(f"Card {index} has invalid categories.")
        elif not set(categories) <= registered_categories:
            errors.append(f"Card {index} uses an unregistered category.")
        if "category" in card:
            errors.append(f"Card {index} retains obsolete category field.")
        needs_theme = (
            candidate.candidate_type == "projected_relationship"
            or candidate.claim_type == "synthesized_theme"
        )
        if needs_theme and card.get("theme_group") != "__LLM_FILL__":
            errors.append(f"Card {index} must contain a theme_group placeholder.")
        if not needs_theme and "theme_group" in card:
            errors.append(f"Card {index} placement unexpectedly contains theme_group.")
        editorial = card.get("card", {})
        for collection in [
            "funny_dog_quotes", "imperative_dog_quotes", "applicable_canine_jokes"
        ]:
            if not editorial.get(collection):
                errors.append(f"Card {index} missing card-level {collection}.")
        for density in ["no_astro", "light_astro", "full_astro"]:
            branch = editorial.get(density, {})
            if any(key in branch for key in [
                "funny_dog_quotes", "imperative_dog_quotes", "applicable_canine_jokes"
            ]):
                errors.append(f"Card {index} retains density-level humor in {density}.")

    expected_big_three = {
        "Sun": ["big3_core_traits"],
        "Moon": ["big3_core_traits"],
        "ASC": ["angles", "big3_core_traits"],
    }
    selected_by_id = {candidate.candidate_id: candidate for candidate in selected}
    packet_by_id = {card["claim_id"]: card for card in packet["cards"]}
    for object_name_key, expected_categories in expected_big_three.items():
        candidate = next(
            (
                item for item in selected
                if item.provenance.get("canonical_object_name") == object_name_key
            ),
            None,
        )
        if candidate is None:
            errors.append(f"Missing mandatory Big Three placement {object_name_key}.")
        elif packet_by_id[candidate.candidate_id]["categories"] != expected_categories:
            errors.append(f"Incorrect categories for {object_name_key}.")

    summary = packet.get("summary", {})
    if list(summary) != ["card1", "card2", "card3", "card4"]:
        errors.append("Summary must contain card1 through card4 in order.")
    for key, value in summary.items():
        if not value.get("dos") or not value.get("donts"):
            errors.append(f"Summary {key} lacks dos or donts placeholders.")
        for density in ["no_astro", "light_astro", "full_astro"]:
            if density not in value:
                errors.append(f"Summary {key} lacks {density}.")

    unselected_records = packet.get("unselected_claims", [])
    unselected_ids = [item.get("claim_id") for item in unselected_records]
    expected_rejected_ids = {candidate.candidate_id for candidate in rejected}
    if set(unselected_ids) != expected_rejected_ids:
        errors.append("unselected_claims does not exactly preserve rejected candidates.")
    if len(unselected_ids) != len(set(unselected_ids)):
        errors.append("Duplicate IDs in unselected_claims.")
    if set(card_ids) & set(unselected_ids):
        errors.append("Selected and unselected claim IDs overlap.")
    all_candidate_ids = set(selected_by_id) | expected_rejected_ids
    for record in unselected_records:
        if (
            not isinstance(record.get("categories"), list)
            or not record["categories"]
            or len(record["categories"]) != len(set(record["categories"]))
            or not set(record["categories"]) <= registered_categories
        ):
            errors.append(
                f"Unselected claim {record.get('claim_id')} has invalid categories."
            )
        if record.get("variant_of") and record["variant_of"] not in all_candidate_ids:
            errors.append(
                f"Unselected variant {record.get('claim_id')} has unknown variant_of."
            )
    registry = packet.get("projected_term_registry")
    if not isinstance(registry, dict) or not isinstance(registry.get("terms"), dict):
        errors.append("Packet lacks a complete projected_term_registry.")
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "checks": {
            "candidate_count": len(candidates),
            "selected_count": len(selected),
            "rejected_count": len(rejected),
            "mandatory_selected": sum(x.mandatory for x in selected),
            "dependency_closure": not any(set(x.dependencies) - selected_ids for x in selected),
            "all_selected_have_evidence": all(x.evidence for x in selected),
            "unique_claim_ids": len(card_ids) == len(set(card_ids)),
            "unselected_claims_preserved": set(unselected_ids) == expected_rejected_ids,
            "projected_term_registry_present": isinstance(
                packet.get("projected_term_registry", {}).get("terms"), dict
            ),
            "summary_template_present": list(packet.get("summary", {})) == [
                "card1", "card2", "card3", "card4"
            ],
            "editorial_placeholders_present": packet["statistics"]["editorial_placeholders"] > 0,
        },
        "selected_type_counts": dict(Counter(x.candidate_type for x in selected)),
        "selected_claim_type_counts": dict(Counter(x.claim_type for x in selected)),
        "score_ranges": {
            "selected_min": min(x.total_score for x in selected),
            "selected_max": max(x.total_score for x in selected),
            "rejected_max": max((x.total_score for x in rejected), default=None),
        },
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_static_assets(bundle: Path, repo_root: Path, manual_zip: Path | None) -> None:
    static = bundle / "static"
    static.mkdir(parents=True, exist_ok=True)
    sources = {
        "Semantic Basis Extractor Pipeline and Scoring Metrics.md": (
            repo_root / "docs" / "extractor"
            / "Semantic Basis Extractor Pipeline and Scoring Metrics.md"
        ),
        "Proposed LLM Handoff Prompt.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "Proposed LLM Handoff Prompt.md"
        ),
        "LLM Editing Permissions and QA Checklist.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "LLM Editing Permissions and QA Checklist.md"
        ),
        "LLM Card-by-Card Authoring Execution Protocol.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "LLM Card-by-Card Authoring Execution Protocol.md"
        ),
        "AstroWoof Projected Natal Card Authoring Manual.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "AstroWoof Projected Natal Card Authoring Manual.md"
        ),
        "AstroWoof Authoring Packet Schema.json": (
            repo_root / "docs" / "extractor" / "AstroWoof Authoring Packet Schema.json"
        ),
        "AstroWoof Bre Editorial Gold Reference.json": (
            repo_root / "docs" / "post_extraction_authoring"
            / "AstroWoof Bre Editorial Gold Reference.json"
        ),
    }
    for name, source in sources.items():
        if source.exists():
            shutil.copy2(source, static / name)
    # An explicit archive may temporarily override the repository-owned manual,
    # but normal builds must not depend on a personal filesystem path.
    if manual_zip and manual_zip.exists():
        with zipfile.ZipFile(manual_zip) as archive:
            member = next(
                x for x in archive.namelist()
                if x.endswith("AstroWoof_Natal_Card_Authoring_Manual.md")
            )
            (static / "AstroWoof Projected Natal Card Authoring Manual.md").write_bytes(
                archive.read(member)
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subject",
        help="Optional subject ID filter within the input package.",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--input-package",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "examples",
        help=(
            "Directory containing one subject's four context files directly, "
            "or one immediate child directory per subject."
        ),
    )
    input_group.add_argument(
        "--input-dir",
        dest="legacy_input_dir",
        type=Path,
        help="Deprecated alias for --input-package.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("semantic-basis-output"))
    parser.add_argument("--bundle-dir", type=Path, default=Path("llm-handoff-bundle"))
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first invalid subject rather than finishing the batch manifest.",
    )
    parser.add_argument(
        "--manual-zip",
        type=Path,
        default=None,
        help=(
            "Optional archive containing a replacement authoring manual. "
            "Normal builds use the versioned repository document."
        ),
    )
    args = parser.parse_args()
    input_package = args.legacy_input_dir or args.input_package
    packages = discover_subject_packages(input_package, args.subject)
    repo_root = Path(__file__).resolve().parent.parent
    args.bundle_dir.mkdir(parents=True, exist_ok=True)
    batch_readme = (
        repo_root / "docs" / "post_extraction_authoring"
        / "Multi-Subject LLM Handoff README.md"
    )
    if batch_readme.exists():
        shutil.copy2(batch_readme, args.bundle_dir / "README.md")
    validator = repo_root / "src" / "validate_astrowoof_editorial.py"
    if validator.exists():
        shutil.copy2(validator, args.bundle_dir / validator.name)
    run_records = []
    failed = False

    for subject, paths in packages.items():
        try:
            contexts, merged_registry, input_audit = load_and_validate_contexts(
                subject, paths
            )
            candidates, analysis = build_candidates(contexts)
            selected, rejected, audit = optimize(candidates)
            packet = compile_packet(
                subject,
                contexts,
                selected,
                rejected,
                analysis,
                merged_registry,
                input_audit,
            )
            qa = qa_report(candidates, selected, rejected, packet)
            if qa["status"] != "pass":
                raise AssertionError(json.dumps(qa, indent=2))

            root = args.output_dir / subject
            write_json(root / f"{subject}.input-audit.json", input_audit)
            write_json(root / f"{subject}.whole-graph-analysis.json", analysis)
            write_json(root / f"{subject}.candidate-pool.json", {
                "schema_version": "semantic_basis.candidate_pool.v0.2",
                "weights": WEIGHTS,
                "candidates": [x.as_dict() for x in sorted(
                    candidates, key=lambda c: (-c.total_score, c.candidate_id)
                )],
            })
            write_json(root / f"{subject}.selection-audit.json", {
                "schema_version": "semantic_basis.selection_audit.v0.2",
                "budget": 50,
                "mandatory_count": 16,
                "optimizer_decisions": audit,
                "selected_ids": [x.candidate_id for x in selected],
                "rejected": [
                    {
                        "candidate_id": x.candidate_id,
                        "score": x.total_score,
                        "reason": x.rejection_reason,
                        **({"variant_of": x.variant_of} if x.variant_of else {}),
                    }
                    for x in sorted(
                        rejected, key=lambda c: (-c.total_score, c.candidate_id)
                    )
                ],
            })
            write_json(root / f"{subject}.selected-authoring-packet.json", packet)
            write_json(root / f"{subject}.selection-qa.json", qa)

            subject_bundle = args.bundle_dir / subject
            request = subject_bundle / "request"
            request.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                root / f"{subject}.selected-authoring-packet.json",
                request / f"{subject}.selected-authoring-packet.json",
            )
            shutil.copy2(
                root / f"{subject}.selection-qa.json",
                request / f"{subject}.selection-qa.json",
            )
            copy_static_assets(subject_bundle, repo_root, args.manual_zip)
            manifest = {
                "bundle_version": "astrowoof.llm_handoff.v0.4",
                "subject": subject,
                "instruction": (
                    "Use the prompt and static guidance to edit only permitted "
                    "editorial fields."
                ),
                "editorial_reference": {
                    "path": "static/AstroWoof Bre Editorial Gold Reference.json",
                    "scope": (
                        "Tone, prose depth, voice differentiation, humor, and "
                        "four-lens summary behavior only; the v0.3 schema and "
                        "current subject packet remain authoritative."
                    ),
                },
                "static_files": sorted(
                    str(x.relative_to(subject_bundle)).replace("\\", "/")
                    for x in (subject_bundle / "static").glob("*")
                ),
                "request_files": sorted(
                    str(x.relative_to(subject_bundle)).replace("\\", "/")
                    for x in request.glob("*")
                ),
                "expected_output": f"natal.{subject}.cards.json",
            }
            write_json(subject_bundle / "manifest.json", manifest)
            run_records.append({
                "subject": subject,
                "status": "pass",
                "input_files": input_audit["input_files"],
                "candidate_count": len(candidates),
                "selected_count": len(selected),
                "unselected_count": len(rejected),
                "synthesized_selected": sum(
                    x.claim_type == "synthesized_theme" for x in selected
                ),
                "registry_unique_term_count": input_audit[
                    "registry_merge"
                ]["unique_term_count"],
                "output": str(root.resolve()),
                "bundle": str(subject_bundle.resolve()),
            })
        except Exception as exc:
            failed = True
            run_records.append({
                "subject": subject,
                "status": "fail",
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
            if args.fail_fast:
                break

    run_manifest = {
        "schema_version": "semantic_basis.batch_run.v0.1",
        "input_package": str(input_package.resolve()),
        "subject_filter": args.subject,
        "subject_count": len(packages),
        "status": "fail" if failed else "pass",
        "subjects": run_records,
    }
    write_json(args.output_dir / "run-manifest.json", run_manifest)
    write_json(
        args.bundle_dir / "manifest.json",
        {
            "bundle_version": "astrowoof.llm_handoff.v0.4",
            "instruction": (
                "Read README.md, then process each passing subject independently "
                "with its mandatory card-by-card execution protocol."
            ),
            "subject_count": len(run_records),
            "subjects": [
                {
                    "subject": record["subject"],
                    "status": record["status"],
                    **(
                        {
                            "manifest": f"{record['subject']}/manifest.json",
                            "expected_output": (
                                f"natal.{record['subject']}.cards.json"
                            ),
                        }
                        if record["status"] == "pass"
                        else {}
                    ),
                }
                for record in run_records
            ],
            "validator": "validate_astrowoof_editorial.py",
        },
    )
    print(json.dumps(run_manifest, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
