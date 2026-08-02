"""Compile four projected natal contexts into a closed AstroWoof authoring packet.

The extractor is deliberately deterministic. It selects existing projected
objects and relationships, generates rule-based syntheses, optimizes a
dependency-closed 50-claim portfolio, and emits an LLM-safe authoring packet.
The LLM is allowed to edit prose fields later; it is not allowed to alter the
selected semantics, evidence, dependencies, IDs, or scores.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import shutil
import zipfile
import zlib
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


def load_subject_params(
    subject: str,
    paths: dict[str, Path],
) -> tuple[dict[str, Any], str | None]:
    directories = {path.resolve().parent for path in paths.values()}
    if len(directories) != 1:
        raise ValueError(
            f"Subject {subject} context files must share one directory to load params.json"
        )
    params_path = next(iter(directories)) / "params.json"
    if not params_path.exists():
        return {}, None
    value = json.loads(params_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{params_path}: params.json must contain one object")
    allowed = {
        "subject_id",
        "display_name",
        "subject_type",
        "gender",
        "pronouns",
        "breed",
        "birth_date",
        "birth_datetime",
        "birth_latitude",
        "birth_longitude",
        "birth_location",
        "birth_date_precision",
    }
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(f"{params_path}: unsupported fields: {unknown}")
    if value.get("subject_id") not in (None, "", subject):
        raise ValueError(
            f"{params_path}: subject_id {value['subject_id']!r} must match {subject!r}"
        )
    string_fields = allowed - {
        "pronouns",
        "birth_latitude",
        "birth_longitude",
    }
    for field_name in string_fields:
        if field_name in value and not isinstance(value[field_name], str):
            raise ValueError(f"{params_path}: {field_name} must be a string")
    for field_name in ("birth_latitude", "birth_longitude"):
        if field_name in value and not isinstance(value[field_name], (int, float)):
            raise ValueError(f"{params_path}: {field_name} must be numeric")
    if "birth_latitude" in value and not -90 <= value["birth_latitude"] <= 90:
        raise ValueError(f"{params_path}: birth_latitude must be between -90 and 90")
    if "birth_longitude" in value and not -180 <= value["birth_longitude"] <= 180:
        raise ValueError(f"{params_path}: birth_longitude must be between -180 and 180")
    pronoun_fields = {
        "subject",
        "object",
        "possessive_adjective",
        "possessive_pronoun",
        "reflexive",
    }
    pronouns = value.get("pronouns")
    if pronouns is not None:
        if not isinstance(pronouns, dict):
            raise ValueError(f"{params_path}: pronouns must be an object")
        unknown_pronouns = sorted(set(pronouns) - pronoun_fields)
        if unknown_pronouns:
            raise ValueError(
                f"{params_path}: unsupported pronoun fields: {unknown_pronouns}"
            )
        for field_name, field_value in pronouns.items():
            if not isinstance(field_value, str):
                raise ValueError(
                    f"{params_path}: pronouns.{field_name} must be a string"
                )
    return value, str(params_path.resolve())


def subject_record(subject: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    params = params or {}
    pronouns = {
        "subject": "",
        "object": "",
        "possessive_adjective": "",
        "possessive_pronoun": "",
        "reflexive": "",
    }
    pronouns.update(params.get("pronouns") or {})
    return {
        "subject_id": subject,
        "display_name": params.get("display_name") or subject.title(),
        "subject_type": params.get("subject_type") or "dog",
        "gender": params.get("gender", ""),
        "pronouns": pronouns,
        "breed": params.get("breed", ""),
        "birth_date": params.get("birth_date", ""),
        "birth_datetime": params.get("birth_datetime", ""),
        "birth_latitude": params.get("birth_latitude"),
        "birth_longitude": params.get("birth_longitude"),
        "birth_location": params.get("birth_location", ""),
        "birth_date_precision": params.get("birth_date_precision", ""),
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
        "dos": ["__LLM_FILL__", "__LLM_FILL__", "__LLM_FILL__"],
        "donts": ["__LLM_FILL__", "__LLM_FILL__", "__LLM_FILL__"],
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
    params: dict[str, Any] | None = None,
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
            "dos": ["__LLM_FILL__", "__LLM_FILL__", "__LLM_FILL__"],
            "donts": ["__LLM_FILL__", "__LLM_FILL__", "__LLM_FILL__"],
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
        "subject": subject_record(subject, params),
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
        if len(card.get("dos", [])) != 3 or len(card.get("donts", [])) != 3:
            errors.append(
                f"Card {index} must scaffold exactly three dos and three donts."
            )
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
        if len(value.get("dos", [])) != 3 or len(value.get("donts", [])) != 3:
            errors.append(
                f"Summary {key} must scaffold exactly three dos and three donts."
            )
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


def _markdown_scalar(value: Any) -> str:
    if value is None:
        return "not specified"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _markdown_data(value: Any, indent: int = 0) -> list[str]:
    prefix = "  " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            label = str(key).replace("_", " ")
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{prefix}- **{label}:**")
                lines.extend(_markdown_data(item, indent + 1))
            else:
                lines.append(f"{prefix}- **{label}:** {_markdown_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_markdown_data(item, indent + 1))
            else:
                lines.append(f"{prefix}- {_markdown_scalar(item)}")
        return lines
    return [f"{prefix}- {_markdown_scalar(value)}"]


def _collect_registry_terms(value: Any, registry_terms: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in registry_terms:
                found.add(key)
            found.update(_collect_registry_terms(item, registry_terms))
    elif isinstance(value, list):
        for item in value:
            found.update(_collect_registry_terms(item, registry_terms))
    elif isinstance(value, str):
        if value in registry_terms:
            found.add(value)
        for token in re.findall(r"[a-z][a-z0-9_]+", value.lower()):
            if token in registry_terms:
                found.add(token)
    return found


def _field_block(label: str, field_path: str) -> str:
    return (
        f"### {label}\n\n"
        f"<!-- BEGIN FIELD: {field_path} -->\n"
        "__WRITE__\n"
        f"<!-- END FIELD: {field_path} -->"
    )


def render_story_writing_template(
    item: dict[str, Any],
    *,
    summary: bool = False,
    include_theme_group: bool = True,
) -> str:
    title = "Summary" if summary else f"Story {item.get('priority_id')}"
    lines = [
        f"# {title} Writing File",
        "",
        "Replace every `__WRITE__` value. Preserve all field markers exactly.",
        "Write no reader-facing prose outside marked fields.",
        "",
        "Write this evidence-bounded insight about the dog described in "
        "`WRITE WHOLE DOG PROFILE.md`.",
        "",
        "Let the previous page leave your desk. Use the shared guidance to plan "
        "this claim as an independent miniature essay before filling its "
        "renderings.",
        "",
        "## Editorial Plan",
        "",
        _field_block("Center of Gravity", "plan.center_of_gravity"),
        "",
        _field_block(
            "Remembered Idea — What Should Remain an Hour Later?",
            "plan.memorable_takeaway",
        ),
        "",
        _field_block("Recognizable Behavior", "plan.recognizable_behavior"),
        "",
        _field_block("Likely Misunderstanding", "plan.likely_misunderstanding"),
        "",
        _field_block("Grounded Surprise", "plan.grounded_surprise"),
        "",
        _field_block("Distinct From Neighboring Stories", "plan.neighbor_distinction"),
        "",
        _field_block("Chosen Writing Form", "plan.writing_form"),
        "",
        _field_block(
            "Comic Premise — What Is Funny About This Trait?",
            "plan.comic_premise",
        ),
        "",
        _field_block("Chosen Creative Approach", "plan.creative_approach"),
        "",
    ]
    for density, density_label in (
        ("no_astro", "No Astrology"),
        ("light_astro", "Light Astrology"),
        ("full_astro", "Full Astrology"),
    ):
        lines.extend([f"## {density_label}", ""])
        for voice, voice_label in (
            ("handler", "Handler"),
            ("direct_to_dog", "Direct to Dog"),
            ("hybrid", "Hybrid"),
        ):
            lines.extend(
                [
                    _field_block(
                        f"{voice_label} Headline",
                        f"{density}.headline.{voice}",
                    ),
                    "",
                    _field_block(
                        f"{voice_label} Story",
                        f"{density}.body.{voice}",
                    ),
                    "",
                ]
            )
    lines.extend(["## Practical Guidance", ""])
    for index in range(len(item.get("dos", []))):
        lines.extend(
            [_field_block(f"Do {index + 1}", f"dos.{index}"), ""]
        )
    for index in range(len(item.get("donts", []))):
        lines.extend(
            [_field_block(f"Don't {index + 1}", f"donts.{index}"), ""]
        )
    lines.extend(["## Humor", ""])
    for field_name, label in (
        ("funny_dog_quotes", "Funny Dog Quote"),
        ("imperative_dog_quotes", "Imperative Dog Quote"),
        ("applicable_canine_jokes", "Canine Joke"),
    ):
        humor = item.get("card", item).get(field_name, [])
        for index in range(len(humor)):
            lines.extend(
                [
                    _field_block(
                        f"{label} {index + 1}",
                        f"{field_name}.{index}",
                    ),
                    "",
                ]
            )
    if not summary:
        lines.extend(["## Organization", ""])
        lines.extend(
            [
                _field_block(
                    "High-Level Filters — one registered value per line",
                    "context_filter_groups.high_level",
                ),
                "",
                _field_block(
                    "Detail-Level Filters — one registered value per line",
                    "context_filter_groups.detail_level",
                ),
                "",
            ]
        )
        if "theme_group" in item and include_theme_group:
            lines.extend(
                [_field_block("Theme Group", "theme_group"), ""]
            )
    return "\n".join(lines).rstrip() + "\n"


def render_theme_group_assignment(packet: dict[str, Any]) -> str:
    cards_by_id = {item["claim_id"]: item for item in packet["cards"]}
    themed_cards = [
        card for card in packet["cards"] if "theme_group" in card
    ]
    lines = [
        "# Global Theme-Group Assignment",
        "",
        "Organize all aspect and synthesis stories below into three or four "
        "approximately equal chapters. Use one concise chapter name for each "
        "group and reuse that exact name for every story assigned to it. Base "
        "the chapters on meaningful similarities in the stories, not their "
        "priority numbers or claim types.",
        "",
    ]
    for card in themed_cards:
        brief, facts, focus = _story_brief(card, cards_by_id)
        lines.extend(
            [
                f"## Story {card['priority_id']:03d}",
                "",
                brief,
                "",
                *[f"- {fact}" for fact in facts if fact],
                "",
                focus,
                "",
                _field_block(
                    "Chapter Name",
                    f"theme_group.{card['priority_id']}",
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


ASTRO_OBJECT_FUNCTIONS = {
    "Sun": "identity, vitality, and the way the dog most naturally feels like themself",
    "Moon": "emotional regulation, instinctive comfort, and private needs",
    "Mercury": "attention, learning, signaling, and information processing",
    "Venus": "bonding style, pleasure, affection, and social preference",
    "Mars": "action, pursuit, play drive, assertion, and frustration",
    "Jupiter": "confidence, exploration, growth, and appetite for possibility",
    "Saturn": "limits, rules, patience, responsibility, and durable structure",
    "Uranus": "novelty, independence, disruption, and unconventional response",
    "Neptune": "sensitivity, imagination, atmosphere, and porous boundaries",
    "Pluto": "intensity, deep trust, control, and transformative pressure",
    "Ascendant": "the dog's first response to situations and visible way of meeting the world",
    "ASC": "the dog's first response to situations and visible way of meeting the world",
    "Descendant": "one-to-one bonds and what the dog seeks or encounters in a close counterpart",
    "DSC": "one-to-one bonds and what the dog seeks or encounters in a close counterpart",
    "Imum Coeli": "private safety, home base, roots, and innermost comfort",
    "IC": "private safety, home base, roots, and innermost comfort",
    "Midheaven": "visible role, pack contribution, and outward development",
    "MC": "visible role, pack contribution, and outward development",
    "North Node": "a developmental direction that becomes more natural through experience",
    "Part of Fortune": "conditions that tend to feel rewarding, fluent, or naturally enlivening",
}

ASPECT_DYNAMICS = {
    "conjunction": "The two functions are fused and tend to activate together.",
    "opposition": "The two functions pull across a polarity and ask for an active balance rather than a permanent winner.",
    "square": "The two functions create friction that demands adjustment, effort, and usable action.",
    "trine": "The two functions reinforce one another easily and can become a strong natural habit.",
    "sextile": "The two functions offer a cooperative possibility that becomes more useful through practice.",
    "quincunx": "The two functions do not naturally speak the same language and require repeated recalibration.",
    "semisextile": "The two functions create a subtle nudge toward awareness and small adjustments.",
}


def _context_record(evidence: dict[str, Any]) -> dict[str, Any]:
    contexts = evidence.get("context_records", {})
    for context in ("general", "handler", "hybrid", "direct_to_dog"):
        record = contexts.get(context, {}).get("record")
        if isinstance(record, dict):
            return record
    return {}


def _card_primary_record(card: dict[str, Any]) -> dict[str, Any]:
    for evidence in card.get("evidence", []):
        record = _context_record(evidence)
        if record:
            return record
    return {}


def _object_name(record: dict[str, Any]) -> str:
    attributes = record.get("attributes") or {}
    source_names = attributes.get("source_names")
    source_name = source_names[0] if isinstance(source_names, list) and source_names else None
    return str(
        attributes.get("canonical_object_name")
        or attributes.get("source_object")
        or source_name
        or record.get("name")
        or "this chart factor"
    )


def _placement_sentence(record: dict[str, Any]) -> str:
    attributes = record.get("attributes") or {}
    object_name = _object_name(record)
    sign = attributes.get("source_sign")
    house = attributes.get("source_house")
    doghouse = attributes.get("doghouse_number")
    locations = []
    if sign:
        locations.append(str(sign))
    if doghouse not in (None, ""):
        locations.append(f"Doghouse {doghouse}")
    elif house not in (None, ""):
        locations.append(f"house {house}")
    sentence = object_name
    if locations:
        sentence += " in " + ", ".join(locations)
    function = ASTRO_OBJECT_FUNCTIONS.get(object_name)
    if function:
        sentence += f" describes {function}"
    return sentence.rstrip(".") + "."


def _relationship_facts(
    card: dict[str, Any],
    cards_by_id: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    record = _card_primary_record(card)
    attributes = record.get("attributes") or {}
    dependency_ids = [
        claim_id
        for evidence in card.get("evidence", [])
        for claim_id in evidence.get("claim_ids", [])
    ]
    dependency_records = [
        _card_primary_record(cards_by_id[claim_id])
        for claim_id in dependency_ids
        if claim_id in cards_by_id
    ]
    names = [_object_name(item) for item in dependency_records[:2]]
    source_name = names[0] if names else str(
        attributes.get("source_object") or "the first chart factor"
    )
    target_name = names[1] if len(names) > 1 else str(
        attributes.get("target_object") or "the second chart factor"
    )
    aspect = str(
        attributes.get("canonical_aspect")
        or record.get("relationship_type")
        or "aspect"
    ).lower()
    orb = attributes.get("orb")
    endpoint_labels = []
    for name, endpoint_record in zip(
        (source_name, target_name),
        dependency_records[:2],
    ):
        sign = (endpoint_record.get("attributes") or {}).get("source_sign")
        endpoint_labels.append(f"{name} in {sign}" if sign else name)
    while len(endpoint_labels) < 2:
        endpoint_labels.append((source_name, target_name)[len(endpoint_labels)])
    exact = "exact " if orb in (0, 0.0, "0", "0.0") else ""
    article = "an" if (exact or aspect[:1] in "aeiou") else "a"
    fact = (
        f"{endpoint_labels[0]} forms {article} {exact}{aspect} "
        f"to {endpoint_labels[1]}"
    )
    if orb not in (None, ""):
        fact += f" with an orb of {orb}°"
    fact += "."
    functions = []
    for name in (source_name, target_name):
        if name in ASTRO_OBJECT_FUNCTIONS:
            functions.append(f"{name} describes {ASTRO_OBJECT_FUNCTIONS[name]}")
    explanation = ". ".join(functions)
    if explanation:
        explanation += "."
    if aspect in ASPECT_DYNAMICS:
        explanation += f" {ASPECT_DYNAMICS[aspect]}"
    return fact, explanation.strip()


def _story_brief(
    card: dict[str, Any],
    cards_by_id: dict[str, dict[str, Any]],
) -> tuple[str, list[str], str]:
    claim_type = card.get("claim_type", "")
    record = _card_primary_record(card)
    if claim_type in {"relationship", "system_interaction", "aspect"}:
        fact, explanation = _relationship_facts(card, cards_by_id)
        aspect = str(
            (record.get("attributes") or {}).get("canonical_aspect")
            or record.get("relationship_type")
            or "aspect"
        ).lower()
        return (
            f"Explore how the two functions named below interact in this dog. "
            f"Show the recognizable behavioral tension, cooperation, or adjustment "
            f"created by the {aspect}.",
            [fact, explanation],
            "Keep both endpoints present. This story is about their interaction, not a generic description of either endpoint alone.",
        )
    if claim_type == "placement":
        return (
            "Translate this placement into one specific, recognizable pattern in the dog's temperament or daily behavior.",
            [_placement_sentence(record)],
            "Stay centered on this placement's distinctive function rather than borrowing a neighboring story's main lesson.",
        )
    dependency_ids = [
        claim_id
        for evidence in card.get("evidence", [])
        for claim_id in evidence.get("claim_ids", [])
    ]
    support = [
        cards_by_id[claim_id]
        for claim_id in dependency_ids
        if claim_id in cards_by_id
    ]
    facts = [
        _placement_sentence(_card_primary_record(item))
        if item.get("claim_type") == "placement"
        else item.get("canonical_claim", item["claim_id"])
        for item in support
    ] or [card.get("canonical_claim", "Use the supplied evidence records.")]
    return (
        "Develop the repeated or compound pattern supported by the facts below. Explain what becomes visible only when those pieces are considered together.",
        facts,
        "Preserve the synthesis: do not flatten it into a restatement of only one supporting fact.",
    )


def authoring_projection_payload(wrapper: dict[str, Any]) -> dict[str, Any]:
    """Return exactly the projected data rendered for an authoring client."""
    record = wrapper.get("record", {})
    return {
        "projection_relevance_score": wrapper.get(
            "projection_relevance_score"
        ),
        "structural_strength_score": wrapper.get(
            "structural_strength_score"
        ),
        "record": {
            key: record.get(key)
            for key in (
                "object_type",
                "name",
                "relationship_type",
                "operators",
                "theme_tags",
            )
            if record.get(key) not in (None, [], {})
        },
        "attributes": {
            key: value
            for key, value in (record.get("attributes") or {}).items()
            if key not in {"projection_relevance_components", "guardrails"}
            and value not in (None, [], {})
        },
    }


def render_claim_and_evidence(
    card: dict[str, Any],
    packet: dict[str, Any],
) -> str:
    registry_terms = packet["projected_term_registry"].get("terms", {})
    relevant_terms = _collect_registry_terms(card.get("evidence", []), registry_terms)
    relevant_terms.update(_collect_registry_terms(card.get("relations", []), registry_terms))
    cards_by_id = {item["claim_id"]: item for item in packet["cards"]}
    dependency_ids: list[str] = []
    for evidence in card.get("evidence", []):
        dependency_ids.extend(evidence.get("claim_ids", []))
    nearby_ids = list(dict.fromkeys(dependency_ids))
    position = card["priority_id"] - 1
    for neighbor_index in (position - 1, position + 1):
        if 0 <= neighbor_index < len(packet["cards"]):
            nearby_ids.append(packet["cards"][neighbor_index]["claim_id"])
    nearby_ids = [
        claim_id for claim_id in dict.fromkeys(nearby_ids)
        if claim_id != card["claim_id"] and claim_id in cards_by_id
    ]
    brief, astrology_facts, focus = _story_brief(card, cards_by_id)

    lines = [
        f"# Story {card['priority_id']:03d}: {card['claim_id']}",
        "",
        "This file is read-only source material. Write in `WRITE THIS CARD.md`.",
        "",
        "## Story Brief",
        "",
        brief,
        "",
        "## Underlying Astrology",
        "",
    ]
    lines.extend(f"- {fact}" for fact in astrology_facts if fact)
    lines.extend(
        [
            "",
            "## What This Story Is Specifically About",
            "",
            focus,
            "",
            "Use the evidence below to choose the exact behavioral expression, "
            "emotional center, and practical consequence.",
            "",
            "## Supporting Evidence",
            "",
        ]
    )
    for evidence_index, evidence in enumerate(card.get("evidence", []), 1):
        lines.extend(
            [
                f"### Evidence {evidence_index}: "
                f"{evidence.get('kind', 'unknown')} ({evidence.get('role', 'unspecified')})",
                "",
            ]
        )
        if evidence.get("source_refs"):
            lines.append(
                f"- **Astrological source references:** "
                f"{', '.join(evidence['source_refs'])}"
            )
        if evidence.get("claim_ids"):
            lines.append(
                f"- **Required selected dependencies:** "
                f"{', '.join(evidence['claim_ids'])}"
            )
        grouped_contexts: dict[str, dict[str, Any]] = {}
        for context, wrapper in evidence.get("context_records", {}).items():
            fingerprint = json.dumps(
                authoring_projection_payload(wrapper),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            group = grouped_contexts.setdefault(
                fingerprint,
                {"contexts": [], "wrapper": wrapper},
            )
            group["contexts"].append(context)
        for group in grouped_contexts.values():
            wrapper = group["wrapper"]
            record = wrapper.get("record", {})
            context_label = ", ".join(
                context.replace("_", " ") for context in group["contexts"]
            )
            lines.extend(
                [
                    f"- **Projection used by:** {context_label}",
                    f"  - relevance: {wrapper.get('projection_relevance_score')}",
                    f"  - structural strength: {wrapper.get('structural_strength_score')}",
                ]
            )
            for key in ("object_type", "name", "relationship_type", "operators", "theme_tags"):
                if record.get(key) not in (None, [], {}):
                    lines.append(
                        f"  - {key.replace('_', ' ')}: "
                        f"{_markdown_scalar(record[key])}"
                    )
            attributes = record.get("attributes") or {}
            for key, value in attributes.items():
                if key in {"projection_relevance_components", "guardrails"}:
                    continue
                if value not in (None, [], {}):
                    lines.append(
                        f"  - {key.replace('_', ' ')}: {_markdown_scalar(value)}"
                    )
        lines.append("")
    lines.extend(["## Projected-Term Reference", ""])
    if relevant_terms:
        for term in sorted(relevant_terms):
            entry = registry_terms[term]
            lines.extend(
                [
                    f"### {term}",
                    "",
                    f"- **Canonical label:** {entry.get('canonical_label', term)}",
                    f"- **Meaning:** {entry.get('long_description') or entry.get('short_description')}",
                    f"- **Core operators:** {', '.join(entry.get('core_operators', [])) or 'not specified'}",
                    f"- **Semantic facets:** {', '.join(entry.get('semantic_facets', [])) or 'not specified'}",
                    "",
                ]
            )
    else:
        lines.extend(["No registry entries were directly referenced.", ""])
    lines.extend(["## Distinguish It From Nearby Stories", ""])
    if nearby_ids:
        for claim_id in nearby_ids:
            neighbor = cards_by_id[claim_id]
            lines.append(
                f"- **Story {neighbor['priority_id']:03d}:** "
                f"{_story_brief(neighbor, cards_by_id)[0]}"
            )
    else:
        lines.append("- No explicit dependencies; distinguish this story from adjacent priorities.")
    return "\n".join(lines).rstrip() + "\n"


def render_whole_dog_context(packet: dict[str, Any]) -> str:
    analysis = packet["whole_graph_analysis"]
    lines = [
        f"# Whole Dog Context: {packet['subject']}",
        "",
        "Use this file to understand the complete dog. Ordinary story claims remain "
        "bounded by their own evidence files.",
        "",
        "## Whole-graph voice brief",
        "",
        *_markdown_data(analysis.get("whole_graph_voice_brief", {})),
        "",
        "## Dominant projected patterns",
        "",
        *_markdown_data(
            {
                "modes": analysis.get("dominant_projected_modes", []),
                "domains": analysis.get("dominant_projected_domains", []),
                "interactions": analysis.get("dominant_interaction_modes", []),
                "highest degree objects": analysis.get("highest_degree_objects", []),
            }
        ),
        "",
        "## Selected story map",
        "",
    ]
    for card in packet["cards"]:
        lines.append(
            f"- **{card['priority_id']:03d} — {card['claim_id']}:** "
            f"{card['canonical_claim']}"
        )
    lines.extend(["", "## Unselected chart material for whole-dog understanding", ""])
    for claim in packet.get("unselected_claims", []):
        lines.append(
            f"- **{claim.get('claim_id', claim.get('candidate_id', 'unidentified'))}:** "
            f"{claim.get('canonical_claim', claim.get('claim', 'No claim text supplied.'))}"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_dog_details(packet: dict[str, Any]) -> str:
    subject = packet["subject"]
    pronouns = subject.get("pronouns") or {}
    return "\n".join(
        [
            f"# Dog Details: {subject.get('display_name') or subject.get('subject_id')}",
            "",
            f"- **Display name:** {subject.get('display_name', '')}",
            f"- **Subject ID:** {subject.get('subject_id', '')}",
            f"- **Pronouns:** {pronouns.get('subject', '')} / {pronouns.get('object', '')} / {pronouns.get('possessive_adjective', '')}",
            f"- **Gender:** {subject.get('gender', '') or 'not supplied'}",
            f"- **Breed:** {subject.get('breed', '') or 'not supplied'}",
            f"- **Birth date:** {subject.get('birth_date', '') or 'not supplied'}",
            f"- **Birth datetime:** {subject.get('birth_datetime', '') or 'not supplied'}",
            f"- **Birth location:** {subject.get('birth_location', '') or 'not supplied'}",
            f"- **Birth latitude:** {subject.get('birth_latitude') if subject.get('birth_latitude') is not None else 'not supplied'}",
            f"- **Birth longitude:** {subject.get('birth_longitude') if subject.get('birth_longitude') is not None else 'not supplied'}",
            f"- **Birth-date precision:** {subject.get('birth_date_precision', '') or 'not supplied'}",
            "",
        ]
    )


def _full_chart_claim_lines(packet: dict[str, Any]) -> list[str]:
    lines = ["## Selected Chart Material", ""]
    for card in packet["cards"]:
        lines.extend(
            [
                f"### {card['priority_id']:03d}: {card['claim_id']}",
                "",
                f"- **Claim:** {card.get('canonical_claim', '')}",
                f"- **Type:** {card.get('claim_type', 'unspecified')}",
                f"- **Priority weight:** {card.get('pct_total_priority', card.get('importance', 'unspecified'))}",
            ]
        )
        source_refs = sorted({
            source_ref
            for evidence in card.get("evidence", [])
            for source_ref in evidence.get("source_refs", [])
        })
        dependencies = sorted({
            claim_id
            for evidence in card.get("evidence", [])
            for claim_id in evidence.get("claim_ids", [])
        })
        if source_refs:
            lines.append(f"- **Source references:** {', '.join(source_refs)}")
        if dependencies:
            lines.append(f"- **Depends on:** {', '.join(dependencies)}")
        lines.append("")
    lines.extend(["## Additional Chart Material", ""])
    for claim in packet.get("unselected_claims", []):
        lines.extend(
            [
                f"### {claim.get('claim_id', claim.get('candidate_id', 'unidentified'))}",
                "",
                f"- **Claim:** {claim.get('canonical_claim', claim.get('claim', 'No claim text supplied.'))}",
                f"- **Type:** {claim.get('claim_type', 'unspecified')}",
            ]
        )
        source_refs = sorted({
            source_ref
            for evidence in claim.get("evidence", [])
            for source_ref in evidence.get("source_refs", [])
        })
        dependencies = sorted({
            claim_id
            for evidence in claim.get("evidence", [])
            for claim_id in evidence.get("claim_ids", [])
        })
        if source_refs:
            lines.append(f"- **Source references:** {', '.join(source_refs)}")
        if dependencies:
            lines.append(f"- **Depends on:** {', '.join(dependencies)}")
        lines.append("")
    return lines


def _authoring_registry(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _authoring_registry(item)
            for key, item in value.items()
            if "template" not in key.lower()
        }
    if isinstance(value, list):
        return [_authoring_registry(item) for item in value]
    return value


def render_full_chart_basis(packet: dict[str, Any]) -> str:
    display_name = packet["subject"].get("display_name") or packet["subject"]["subject_id"]
    lines = [
        f"# Full Chart Basis: {display_name}",
        "",
        "Read this complete chart basis before writing the whole-dog profile. "
        "It includes the selected insights and additional chart material so the "
        "profile can recognize the dog's complete pattern.",
        "",
        *_full_chart_claim_lines(packet),
        "",
        "## Complete Projected-Term Registry",
        "",
        *_markdown_data(_authoring_registry(packet.get("projected_term_registry", {}))),
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_whole_dog_profile_template(packet: dict[str, Any]) -> str:
    display_name = packet["subject"].get("display_name") or packet["subject"]["subject_id"]
    fields = (
        ("Integrated Portrait", "profile.integrated_portrait"),
        ("Core Temperament", "profile.core_temperament"),
        ("Emotional Life and Regulation", "profile.emotional_regulation"),
        ("Learning and Motivation", "profile.learning_motivation"),
        ("Relationships and Trust", "profile.relationships_trust"),
        ("Play, Adventure, and Daily Rhythm", "profile.play_adventure_rhythm"),
        ("Tensions and Counterweights", "profile.tensions_counterweights"),
        ("Strengths and Growth Edges", "profile.strengths_growth"),
        ("Voice, Warmth, Humor, and Imagery", "profile.voice_humor_imagery"),
        ("Factual Cautions", "profile.factual_cautions"),
    )
    lines = [
        f"# Whole-Dog Authoring Profile: {display_name}",
        "",
        "Complete this profile first, using `DOG DETAILS.md` and the entire "
        "`FULL CHART BASIS.md`. This becomes the shared characterization for "
        "every story in the workspace.",
        "",
    ]
    for label, field_path in fields:
        lines.extend([_field_block(label, field_path), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_summary_thesis_plan(packet: dict[str, Any]) -> str:
    display_name = packet["subject"].get("display_name") or packet["subject"]["subject_id"]
    fields = (
        (
            "Who the Dog Is — Identity Thesis",
            "summary_plan.identity_thesis",
        ),
        (
            "How the Dog Lives — Daily-Life Thesis",
            "summary_plan.daily_life_thesis",
        ),
        (
            "What the Dog Needs — Needs and Support Thesis",
            "summary_plan.needs_support_thesis",
        ),
        (
            "How the Dog Grows — Growth and Development Thesis",
            "summary_plan.growth_development_thesis",
        ),
        (
            "Why Needs and Growth Are Different Arguments",
            "summary_plan.needs_vs_growth_distinction",
        ),
    )
    lines = [
        f"# Four-Summary Thesis Plan: {display_name}",
        "",
        "Complete this private editorial plan after the whole-dog profile and "
        "before writing any summary. Give each lens one distinct idea the "
        "reader should remember an hour later. The four theses must describe "
        "the same dog without becoming four paraphrases of one dominant motif.",
        "",
        "The needs thesis explains present-tense support, regulation, handling, "
        "and enrichment. The growth thesis explains learning, development, "
        "challenges, and potential unfolding over time. State their distinction "
        "explicitly before drafting prose.",
        "",
    ]
    for label, field_path in fields:
        lines.extend([_field_block(label, field_path), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_summary_gold_reference(repo_root: Path) -> str:
    reference_path = (
        repo_root
        / "qa"
        / "reference_decks"
        / "kevin"
        / "20260730-six-pass-final"
        / "natal.kevin.cards.json"
    )
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    lens_names = (
        "Who He Is",
        "How He Lives",
        "What He Needs",
        "How He Grows",
    )
    lines = [
        "# AstroWoof Four-Summary Gold Reference",
        "",
        "## Transfer target",
        "",
        "This is a craft reference for four-lens separation, full-chart "
        "synthesis, prose depth, audience purpose, and astrology-density "
        "control. Kevin is an example subject, not evidence about the current "
        "dog.",
        "",
        "Do not copy Kevin's facts, astrology, wording, metaphors, jokes, "
        "headlines, sentence structures, or organizing devices. Phrases such "
        "as `anchor`, `gate`, `laboratory`, `stage`, and `train the landing` "
        "are examples, not templates. Do not imitate lengths mechanically. "
        "The current dog's full chart basis and whole-dog profile are the only "
        "authority for what the new summaries may claim.",
        "",
        "Study how the four cards form a coordinated set while making "
        "different arguments: identity, lived rhythm, present-tense support, "
        "and development over time. Then close this reference conceptually and "
        "write the current dog from the four-thesis plan.",
        "",
    ]
    labels = {
        "dos": "Do",
        "donts": "Don't",
        "funny_dog_quotes": "Funny Dog Quote",
        "imperative_dog_quotes": "Imperative Dog Quote",
        "applicable_canine_jokes": "Applicable Canine Joke",
    }
    density_labels = {
        "no_astro": "No Astrology",
        "light_astro": "Light Astrology",
        "full_astro": "Full Astrology",
    }
    audience_labels = {
        "handler": "Handler",
        "direct_to_dog": "Direct to Dog",
        "hybrid": "Hybrid",
    }
    for index, lens_name in enumerate(lens_names, 1):
        summary = reference["summary"][f"card{index}"]
        lines.extend([f"## Summary {index}: {lens_name}", ""])
        for key, label in labels.items():
            for item_index, value in enumerate(summary[key], 1):
                suffix = f" {item_index}" if len(summary[key]) > 1 else ""
                lines.extend([f"### {label}{suffix}", "", value, ""])
        for density, density_label in density_labels.items():
            lines.extend([f"### {density_label}", ""])
            for audience, audience_label in audience_labels.items():
                headline = summary[density]["headline"][audience]
                body = summary[density]["body"][audience]
                lines.extend(
                    [
                        f"#### {audience_label} headline",
                        "",
                        headline,
                        "",
                        f"#### {audience_label} body",
                        "",
                        body,
                        "",
                    ]
                )
    return "\n".join(lines).rstrip() + "\n"


def _assignment_features(card: dict[str, Any]) -> dict[str, Any]:
    return {
        "claim_type": str(card.get("claim_type") or "unknown"),
        "categories": frozenset(str(x) for x in card.get("categories", [])),
        "domains": frozenset(str(x) for x in card.get("behavioral_domains", [])),
        "tags": frozenset(str(x) for x in card.get("tags", [])),
        "priority_band": (int(card["priority_id"]) - 1) // 10,
    }


def _assignment_similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    score = 3.0 if left["claim_type"] == right["claim_type"] else 0.0
    score += 2.0 * len(left["categories"] & right["categories"])
    score += 1.0 * len(left["domains"] & right["domains"])
    tag_union = left["tags"] | right["tags"]
    if tag_union:
        score += len(left["tags"] & right["tags"]) / len(tag_union)
    return score


def build_split_assignment_plan(
    packet: dict[str, Any],
    policy: str,
    *,
    pass_count: int = 5,
) -> dict[str, Any]:
    """Assign selected cards to fixed-size authoring passes deterministically."""
    cards = list(packet["cards"])
    if len(cards) % pass_count:
        raise ValueError(
            f"Cannot divide {len(cards)} cards evenly across {pass_count} passes"
        )
    capacity = len(cards) // pass_count
    subject = str(packet["subject"].get("subject_id") or "subject")
    seed = hashlib.sha256(
        f"astrowoof:{policy}:{subject}".encode("utf-8")
    ).hexdigest()[:16]
    if policy == "contiguous":
        passes = [
            cards[index * capacity:(index + 1) * capacity]
            for index in range(pass_count)
        ]
    elif policy == "stratified-v1":
        features = {card["claim_id"]: _assignment_features(card) for card in cards}
        type_frequency = Counter(
            feature["claim_type"] for feature in features.values()
        )
        category_frequency = Counter(
            category
            for feature in features.values()
            for category in feature["categories"]
        )

        def stable_value(*parts: object) -> str:
            value = ":".join(str(part) for part in (seed, *parts))
            return hashlib.sha256(value.encode("utf-8")).hexdigest()

        ordered = sorted(
            cards,
            key=lambda card: (
                type_frequency[features[card["claim_id"]]["claim_type"]],
                sum(
                    category_frequency[item]
                    for item in features[card["claim_id"]]["categories"]
                ),
                stable_value("allocation", card["claim_id"]),
            ),
        )
        passes = [[] for _ in range(pass_count)]
        for card in ordered:
            feature = features[card["claim_id"]]
            minimum_size = min(len(items) for items in passes)
            eligible = [
                index for index, items in enumerate(passes)
                if len(items) == minimum_size and len(items) < capacity
            ]

            def allocation_cost(index: int) -> tuple[float, str]:
                assigned = passes[index]
                assigned_features = [features[item["claim_id"]] for item in assigned]
                score = 6.0 * sum(
                    item["claim_type"] == feature["claim_type"]
                    for item in assigned_features
                )
                score += 2.0 * sum(
                    len(item["categories"] & feature["categories"])
                    for item in assigned_features
                )
                score += 1.0 * sum(
                    len(item["domains"] & feature["domains"])
                    for item in assigned_features
                )
                score += 4.0 * sum(
                    item["priority_band"] == feature["priority_band"]
                    for item in assigned_features
                )
                return score, stable_value("pass", index + 1, card["claim_id"])

            target = min(eligible, key=allocation_cost)
            passes[target].append(card)

        for index, assigned in enumerate(passes):
            remaining = list(assigned)
            first = min(
                remaining,
                key=lambda card: stable_value("order", index + 1, card["claim_id"]),
            )
            ordered_pass = [first]
            remaining.remove(first)
            while remaining:
                previous = features[ordered_pass[-1]["claim_id"]]
                next_card = min(
                    remaining,
                    key=lambda card: (
                        _assignment_similarity(previous, features[card["claim_id"]]),
                        stable_value("order", index + 1, card["claim_id"]),
                    ),
                )
                ordered_pass.append(next_card)
                remaining.remove(next_card)
            passes[index] = ordered_pass
    else:
        raise ValueError(f"Unknown split assignment policy: {policy}")

    assigned_ids = [card["priority_id"] for items in passes for card in items]
    if sorted(assigned_ids) != list(range(1, len(cards) + 1)):
        raise AssertionError("Split assignment did not preserve every priority ID once")
    return {
        "schema_version": "astrowoof.split_assignment.v0.1",
        "policy": policy,
        "algorithm_version": policy,
        "subject": subject,
        "seed": seed,
        "pass_count": pass_count,
        "cards_per_pass": capacity,
        "passes": {
            str(index + 1): [card["priority_id"] for card in assigned]
            for index, assigned in enumerate(passes)
        },
    }


def build_story_workspace(
    subject_bundle: Path,
    packet: dict[str, Any],
    repo_root: Path,
    card_limit: int,
    *,
    card_start: int = 1,
    include_summaries: bool | None = None,
    include_theme_plan: bool = False,
    pass_number: int | None = None,
    pass_count: int | None = None,
    assigned_cards: list[dict[str, Any]] | None = None,
) -> None:
    if card_start < 1 or card_limit < 0:
        raise ValueError("card_start must be positive and card_limit nonnegative")
    card_end = card_start + card_limit - 1
    if assigned_cards is not None and len(assigned_cards) != card_limit:
        raise ValueError(
            f"Expected {card_limit} explicitly assigned cards, got "
            f"{len(assigned_cards)}"
        )
    if assigned_cards is None and card_end > len(packet["cards"]):
        raise ValueError(
            f"Requested stories {card_start}-{card_end}, but the packet has "
            f"{len(packet['cards'])} cards"
        )
    if include_summaries is None:
        include_summaries = (
            card_start == 1 and card_limit == len(packet["cards"])
        )
    subject_bundle.mkdir(parents=True, exist_ok=True)
    brief_source = (
        repo_root / "docs" / "post_extraction_authoring"
        / "AstroWoof Story Workspace Authoring Brief.md"
    )
    shutil.copy2(brief_source, subject_bundle / "AUTHORING BRIEF.md")
    guiding_lights_source = (
        repo_root / "docs" / "post_extraction_authoring"
        / "AstroWoof Authoring Guiding Lights.md"
    )
    shutil.copy2(
        guiding_lights_source,
        subject_bundle / "GUIDING LIGHTS.md",
    )
    write_opaque_authoring_checker(
        subject_bundle / "lint_authoring_pass.py",
        repo_root,
    )
    display_name = (
        packet["subject"].get("display_name")
        or packet["subject"].get("subject_id")
    )
    pass_label = (
        f"Pass {pass_number} of {pass_count}"
        if pass_number is not None and pass_count is not None
        else "Authoring Pass"
    )
    if card_limit:
        assignment = (
            f"This pass contains exactly Stories {card_start:03d} through "
            f"{card_end:03d}. Complete those {card_limit} story directories "
            "in numeric order. The assignment is complete when their writing "
            "files and the whole-dog profile contain no unfinished fields."
        )
        sequence = (
            "Begin by reading `AUTHORING BRIEF.md` and `DOG DETAILS.md`. Read "
            "`FULL CHART BASIS.md` in full and complete "
            "`WRITE WHOLE DOG PROFILE.md`. Then author each supplied story as "
            "a fresh miniature essay while retaining a coherent understanding "
            f"of {display_name}."
        )
    else:
        assignment = (
            "This is the summary pass. Complete the four supplied Summary "
            "directories through their distinct lenses: who the dog is, how "
            "the dog lives, what the dog needs, and how the dog grows. Give "
            "each summary its own central argument, examples, advice, and "
            "language. Also complete `ASSIGN THEME GROUPS.md`, which creates "
            "one coherent chapter plan for every aspect and synthesis story."
        )
        sequence = (
            "Begin by reading `AUTHORING BRIEF.md` and `DOG DETAILS.md`. Read "
            "`FULL CHART BASIS.md` in full and complete "
            "`WRITE WHOLE DOG PROFILE.md`. Study `SUMMARY GOLD REFERENCE.md` "
            "for craft only, then complete `WRITE SUMMARY THESIS PLAN.md`. "
            "Only after the four arguments are distinct should you write all "
            f"four summaries from the complete chart understanding of {display_name}."
        )
    pass_specific_reading = (
        "\n\nFor this summary pass, also read `SUMMARY GOLD REFERENCE.md`. "
        "Transfer its quality principles, never its Kevin-specific content or "
        "language. Complete `WRITE SUMMARY THESIS PLAN.md` before drafting any "
        "summary."
        if include_summaries
        else ""
    )
    (subject_bundle / "START HERE.md").write_text(
        f"# Start Here — {pass_label}\n\n"
        f"## Assignment\n\n{assignment}\n\n"
        "## Read first\n\n"
        "Read `GUIDING LIGHTS.md` as the creative doctrine for this pass. "
        "Its independent-card standard is part of the assignment, not "
        f"optional inspiration.{pass_specific_reading}\n\n"
        f"## Working sequence\n\n{sequence}\n\n"
        "## Mechanical acceptance requirements\n\n"
        "Your completed pass will be checked automatically before it is "
        "accepted.\n\n"
        "- No reader-facing field may be copied exactly between cards.\n"
        "- Reused language, recurring prose frames, metric-gaming artifacts, "
        "and cosmetic word insertion do not satisfy editorial independence.\n\n"
        "These are rejection boundaries, not the creative quality standard. "
        "An `accept` verdict proves that detectable copying was avoided; it "
        "does not prove that the prose is insightful, natural, memorable, or "
        "sufficiently varied. Use `GUIDING LIGHTS.md` as the higher standard.\n\n"
        "## Required pre-delivery check\n\n"
        "After completing every field, run:\n\n"
        "```text\n"
        "python lint_authoring_pass.py . --output "
        "authoring-pass-acceptance.json\n"
        "```\n\n"
        "A report status of `reject` means the pass is not complete. Rewrite "
        "the identified cross-card reuse and run the checker again until its "
        "status is `accept`. Include `authoring-pass-acceptance.json` in the "
        "returned ZIP.\n\n"
        "## If the gate rejects the pass\n\n"
        "Treat a rejection as an editorial signal, not as a puzzle about the "
        "checker. The most reliable response is to return to the affected "
        "cards' plans, recover what makes each insight memorable, and rewrite "
        "the prose in a natural voice with genuinely distinct movement and "
        "character. Surface-level interventions—filler, recurring "
        "catchphrases, bracketed insertions, or cosmetic paraphrase—do not "
        "create editorial independence. Writing that sincerely follows "
        "`GUIDING LIGHTS.md` is the best route to a successful pass.\n\n"
        "Preserve every field marker and replace every unfinished field. "
        "Return this complete pass directory as a ZIP archive.\n",
        encoding="utf-8",
    )
    (subject_bundle / "DOG DETAILS.md").write_text(
        render_dog_details(packet),
        encoding="utf-8",
    )
    (subject_bundle / "FULL CHART BASIS.md").write_text(
        render_full_chart_basis(packet),
        encoding="utf-8",
    )
    (subject_bundle / "WRITE WHOLE DOG PROFILE.md").write_text(
        render_whole_dog_profile_template(packet),
        encoding="utf-8",
    )
    cards_root = subject_bundle / "cards"
    if card_limit:
        cards_root.mkdir(parents=True, exist_ok=True)
    workspace_cards = (
        assigned_cards
        if assigned_cards is not None
        else packet["cards"][card_start - 1:card_end]
    )
    for card in workspace_cards:
        story_root = cards_root / (
            f"Story {card['priority_id']:03d} -- {card['claim_id']}"
        )
        story_root.mkdir(parents=True, exist_ok=True)
        (story_root / "CLAIM AND EVIDENCE.md").write_text(
            render_claim_and_evidence(card, packet),
            encoding="utf-8",
        )
        (story_root / "WRITE THIS CARD.md").write_text(
            render_story_writing_template(
                card,
                include_theme_group=not (
                    pass_number is not None and pass_count == 6
                ),
            ),
            encoding="utf-8",
        )
    if include_theme_plan:
        (subject_bundle / "ASSIGN THEME GROUPS.md").write_text(
            render_theme_group_assignment(packet),
            encoding="utf-8",
        )
    if include_summaries:
        (subject_bundle / "SUMMARY GOLD REFERENCE.md").write_text(
            render_summary_gold_reference(repo_root),
            encoding="utf-8",
        )
        (subject_bundle / "WRITE SUMMARY THESIS PLAN.md").write_text(
            render_summary_thesis_plan(packet),
            encoding="utf-8",
        )
        summaries_root = subject_bundle / "summaries"
        summaries_root.mkdir(parents=True, exist_ok=True)
        summary_names = (
            "Who the Dog Is",
            "How the Dog Lives",
            "What the Dog Needs",
            "How the Dog Grows",
        )
        for index, name in enumerate(summary_names, 1):
            summary = packet["summary"][f"card{index}"]
            summary_root = summaries_root / f"Summary {index:02d} -- {name}"
            summary_root.mkdir(parents=True, exist_ok=True)
            (summary_root / "SUMMARY BASIS.md").write_text(
                "# Summary Basis\n\n"
                "Use `WRITE WHOLE DOG PROFILE.md` and `FULL CHART BASIS.md` for "
                "this full-chart summary.\n",
                encoding="utf-8",
            )
            (summary_root / "WRITE THIS SUMMARY.md").write_text(
                render_story_writing_template(summary, summary=True),
                encoding="utf-8",
            )


def archive_story_workspace(workspace: Path) -> Path:
    """Create an attach-ready ZIP containing the workspace root directory."""
    archive_path = workspace.parent / f"{workspace.name}.zip"
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for path in sorted(workspace.rglob("*")):
            if path.is_file():
                archive.write(
                    path,
                    arcname=(
                        Path(workspace.name)
                        / path.relative_to(workspace)
                    ).as_posix(),
                )
    return archive_path


def write_opaque_authoring_checker(target: Path, repo_root: Path) -> None:
    """Bundle the private checker as a portable opaque source payload."""
    module_names = (
        "assemble_authoring_workspace",
        "lint_astrowoof_editorial",
        "lint_authoring_pass",
    )
    sources = {
        name: (repo_root / "src" / f"{name}.py").read_text(encoding="utf-8")
        for name in module_names
    }
    payload = base64.b85encode(
        zlib.compress(
            json.dumps(sources, ensure_ascii=False).encode("utf-8"),
            level=9,
        )
    ).decode("ascii")
    launcher = (
        "#!/usr/bin/env python3\n"
        '"""AstroWoof bundled authoring gate. Run this file; do not edit it."""\n'
        "import base64, json, os, sys, types, zlib\n\n"
        f"_PAYLOAD = {payload!r}\n"
        "_sources = json.loads(zlib.decompress("
        "base64.b85decode(_PAYLOAD)).decode('utf-8'))\n"
        "for _name in ('assemble_authoring_workspace', "
        "'lint_astrowoof_editorial'):\n"
        "    _module = types.ModuleType(_name)\n"
        "    _module.__file__ = f'<bundled:{_name}>'\n"
        "    sys.modules[_name] = _module\n"
        "    exec(compile(_sources[_name], _module.__file__, 'exec'), "
        "_module.__dict__)\n"
        "os.environ['ASTROWOOF_OPAQUE_ACCEPTANCE'] = '1'\n"
        "_scope = {'__name__': '__main__', "
        "'__file__': '<bundled:lint_authoring_pass>'}\n"
        "exec(compile(_sources['lint_authoring_pass'], "
        "_scope['__file__'], 'exec'), _scope)\n"
    )
    target.write_text(launcher, encoding="utf-8")


def copy_static_assets(
    bundle: Path,
    repo_root: Path,
    manual_zip: Path | None,
    handoff_profile: str = "rigorous",
) -> None:
    static = bundle / "static"
    static.mkdir(parents=True, exist_ok=True)
    rigorous_sources = {
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
        "AstroWoof Independent Card Writing Brief.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "AstroWoof Independent Card Writing Brief.md"
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
    compact_sources = {
        "AstroWoof Compact Single-Subject Authoring Brief.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "AstroWoof Compact Single-Subject Authoring Brief.md"
        ),
        "Compact LLM Handoff Prompt.md": (
            repo_root / "docs" / "post_extraction_authoring"
            / "Compact LLM Handoff Prompt.md"
        ),
        "AstroWoof Authoring Packet Schema.json": (
            repo_root / "docs" / "extractor" / "AstroWoof Authoring Packet Schema.json"
        ),
        "AstroWoof Bre Editorial Gold Reference.json": (
            repo_root / "docs" / "post_extraction_authoring"
            / "AstroWoof Bre Editorial Gold Reference.json"
        ),
    }
    sources = compact_sources if handoff_profile == "compact" else rigorous_sources
    for name, source in sources.items():
        if source.exists():
            shutil.copy2(source, static / name)
    # An explicit archive may temporarily override the repository-owned manual,
    # but normal builds must not depend on a personal filesystem path.
    if handoff_profile == "rigorous" and manual_zip and manual_zip.exists():
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
        "--handoff-profile",
        choices=("rigorous", "compact", "authoring-workspace"),
        default="rigorous",
        help=(
            "Instruction profile for the generated LLM bundle. "
            "'rigorous' preserves the resumable ledger/checkpoint protocol; "
            "'compact' emits a low-ceremony single-subject authoring brief; "
            "'authoring-workspace' emits one Markdown writing directory per card."
        ),
    )
    parser.add_argument(
        "--workspace-card-limit",
        type=int,
        default=50,
        help=(
            "Number of card directories to emit for --handoff-profile "
            "authoring-workspace. Use 10 for the initial story-workspace experiment."
        ),
    )
    parser.add_argument(
        "--workspace-layout",
        choices=("split", "single"),
        default="split",
        help=(
            "Layout for --handoff-profile authoring-workspace. 'split' emits "
            "five independent ten-card passes and one summary pass; 'single' "
            "preserves the legacy one-directory workspace."
        ),
    )
    parser.add_argument(
        "--split-assignment-policy",
        choices=("contiguous", "stratified-v1"),
        default="contiguous",
        help=(
            "Card-to-pass assignment for split authoring workspaces. "
            "'contiguous' preserves canonical priority ranges; "
            "'stratified-v1' deterministically mixes claim types, categories, "
            "behavioral domains, and priority bands."
        ),
    )
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
    if not 1 <= args.workspace_card_limit <= 50:
        parser.error("--workspace-card-limit must be between 1 and 50")
    if (
        args.handoff_profile != "authoring-workspace"
        and (
            args.workspace_card_limit != 50
            or args.workspace_layout != "split"
            or args.split_assignment_policy != "contiguous"
        )
    ):
        parser.error(
            "--workspace-card-limit, --workspace-layout, and "
            "--split-assignment-policy are only valid with "
            "--handoff-profile authoring-workspace"
        )
    input_package = args.legacy_input_dir or args.input_package
    packages = discover_subject_packages(input_package, args.subject)
    repo_root = Path(__file__).resolve().parent.parent
    args.bundle_dir.mkdir(parents=True, exist_ok=True)
    if args.handoff_profile == "authoring-workspace":
        (args.bundle_dir / "README.md").write_text(
            "# AstroWoof Story Workspace Handoff\n\n"
            "Each pass directory is a self-contained Markdown authoring "
            "assignment. In split layout, passes 1–5 each contain ten stories "
            "and pass 6 contains the four full-chart summaries. An attach-ready "
            "ZIP is generated beside every pass directory. Open each ZIP in "
            "its own temporary chat, read that pass's `START HERE.md`, and "
            "return the completed pass directory as a ZIP archive. The six "
            "passes may run simultaneously.\n",
            encoding="utf-8",
        )
    elif args.handoff_profile == "compact":
        (args.bundle_dir / "README.md").write_text(
            "# AstroWoof Compact LLM Handoff\n\n"
            "Each subject directory is an independent authoring job. Read its "
            "`manifest.json`, then follow "
            "`static/Compact LLM Handoff Prompt.md` and "
            "`static/AstroWoof Compact Single-Subject Authoring Brief.md`.\n",
            encoding="utf-8",
        )
    else:
        batch_readme = (
            repo_root / "docs" / "post_extraction_authoring"
            / "Multi-Subject LLM Handoff README.md"
        )
        if batch_readme.exists():
            shutil.copy2(batch_readme, args.bundle_dir / "README.md")
    validator = repo_root / "src" / "validate_astrowoof_editorial.py"
    if validator.exists():
        shutil.copy2(validator, args.bundle_dir / validator.name)
    editorial_linter = repo_root / "src" / "lint_astrowoof_editorial.py"
    if editorial_linter.exists():
        shutil.copy2(editorial_linter, args.bundle_dir / editorial_linter.name)
    assembler = repo_root / "src" / "assemble_authoring_workspace.py"
    if args.handoff_profile == "authoring-workspace" and assembler.exists():
        shutil.copy2(assembler, args.bundle_dir / assembler.name)
    run_records = []
    failed = False

    for subject, paths in packages.items():
        try:
            contexts, merged_registry, input_audit = load_and_validate_contexts(
                subject, paths
            )
            params, params_file = load_subject_params(subject, paths)
            input_audit["params_file"] = params_file
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
                params,
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
            subject_bundles: list[Path] = []
            request_files: list[str] = []
            if args.handoff_profile == "authoring-workspace":
                stale_subject_paths = [
                    subject_bundle,
                    *[
                        args.bundle_dir / f"{subject}_{index}"
                        for index in range(1, 7)
                    ],
                ]
                for stale_path in stale_subject_paths:
                    if stale_path.exists():
                        shutil.rmtree(stale_path)
                for index in range(1, 7):
                    stale_archive = (
                        args.bundle_dir / f"{subject}_{index}.zip"
                    )
                    if stale_archive.exists():
                        stale_archive.unlink()
                if args.workspace_layout == "split":
                    assignment_plan = build_split_assignment_plan(
                        packet, args.split_assignment_policy
                    )
                    assignment_path = root / f"{subject}.split-assignment.json"
                    write_json(assignment_path, assignment_plan)
                    cards_by_priority = {
                        card["priority_id"]: card for card in packet["cards"]
                    }
                    pass_specs = [
                        (index, assignment_plan["passes"][str(index)], False, False)
                        for index in range(1, 6)
                    ] + [(6, [], True, True)]
                    for (
                        pass_number,
                        priority_ids,
                        summaries,
                        theme_plan,
                    ) in pass_specs:
                        assigned_cards = [
                            cards_by_priority[priority_id]
                            for priority_id in priority_ids
                        ]
                        card_count = len(assigned_cards)
                        pass_bundle = (
                            args.bundle_dir / f"{subject}_{pass_number}"
                        )
                        build_story_workspace(
                            pass_bundle,
                            packet,
                            repo_root,
                            card_count,
                            card_start=(priority_ids[0] if priority_ids else 51),
                            include_summaries=summaries,
                            include_theme_plan=theme_plan,
                            pass_number=pass_number,
                            pass_count=6,
                            assigned_cards=assigned_cards,
                        )
                        assignment = (
                            "Stories with canonical priority IDs "
                            + ", ".join(
                                f"{priority_id:03d}" for priority_id in priority_ids
                            )
                            if card_count
                            else "Four full-chart summaries"
                        )
                        pass_specific_files = (
                            "- **Summary craft reference:** "
                            "`SUMMARY GOLD REFERENCE.md`\n"
                            "- **Required private plan:** "
                            "`WRITE SUMMARY THESIS PLAN.md`\n"
                            if summaries
                            else ""
                        )
                        (pass_bundle / "WORKSPACE MANIFEST.md").write_text(
                            "# AstroWoof Authoring Pass\n\n"
                            f"- **Subject:** {subject}\n"
                            f"- **Pass:** {pass_number} of 6\n"
                            f"- **Assignment:** {assignment}\n"
                            f"- **Assignment policy:** {assignment_plan['policy']}\n"
                            f"- **Replay seed:** {assignment_plan['seed']}\n"
                            f"- **Expected return:** "
                            f"`{subject}_{pass_number}-authored.zip`\n"
                            f"- **Start with:** `START HERE.md`\n"
                            f"{pass_specific_files}",
                            encoding="utf-8",
                        )
                        archive_story_workspace(pass_bundle)
                        subject_bundles.append(pass_bundle)
                else:
                    subject_bundle.mkdir(parents=True, exist_ok=True)
                    build_story_workspace(
                        subject_bundle,
                        packet,
                        repo_root,
                        args.workspace_card_limit,
                    )
                    subject_bundles.append(subject_bundle)
            else:
                if subject_bundle.exists():
                    shutil.rmtree(subject_bundle)
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
                request_files = sorted(
                    str(x.relative_to(subject_bundle)).replace("\\", "/")
                    for x in request.glob("*")
                )
                copy_static_assets(
                    subject_bundle,
                    repo_root,
                    args.manual_zip,
                    args.handoff_profile,
                )
            manifest = {
                "bundle_version": "astrowoof.llm_handoff.v0.5.0",
                "handoff_profile": args.handoff_profile,
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
                "static_files": (
                    sorted(
                        str(x.relative_to(subject_bundle)).replace("\\", "/")
                        for x in (subject_bundle / "static").glob("*")
                    )
                    if args.handoff_profile != "authoring-workspace"
                    else []
                ),
                "request_files": request_files,
                "workspace_card_count": (
                    args.workspace_card_limit
                    if args.handoff_profile == "authoring-workspace"
                    else None
                ),
                "expected_output": (
                    f"{subject}-authored-story-workspace.zip"
                    if args.handoff_profile == "authoring-workspace"
                    else f"natal.{subject}.cards.json"
                ),
            }
            if args.handoff_profile == "authoring-workspace":
                if args.workspace_layout == "single":
                    (subject_bundle / "WORKSPACE MANIFEST.md").write_text(
                        f"# AstroWoof Story Workspace\n\n"
                        f"- **Subject:** {subject}\n"
                        f"- **Story directories:** {args.workspace_card_limit}\n"
                        f"- **Expected return:** "
                        f"`{subject}-authored-story-workspace.zip`\n"
                        f"- **Start with:** `START HERE.md`\n",
                        encoding="utf-8",
                    )
            else:
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
                "bundle": (
                    [str(path.resolve()) for path in subject_bundles]
                    if args.handoff_profile == "authoring-workspace"
                    and args.workspace_layout == "split"
                    else str(subject_bundle.resolve())
                ),
                **(
                    {
                        "split_assignment": assignment_plan,
                        "split_assignment_file": str(assignment_path.resolve()),
                    }
                    if args.handoff_profile == "authoring-workspace"
                    and args.workspace_layout == "split"
                    else {}
                ),
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
        "split_assignment_policy": args.split_assignment_policy,
        "subjects": run_records,
    }
    write_json(args.output_dir / "run-manifest.json", run_manifest)
    bundle_manifest = {
            "bundle_version": "astrowoof.llm_handoff.v0.5.0",
            "handoff_profile": args.handoff_profile,
            "split_assignment_policy": args.split_assignment_policy,
            "instruction": (
                "Read README.md, then process each passing subject independently "
                + (
                    "with its compact single-subject authoring brief."
                    if args.handoff_profile == "compact"
                    else (
                        "as a Markdown story workspace."
                        if args.handoff_profile == "authoring-workspace"
                        else "with its mandatory card-by-card execution protocol."
                    )
                )
            ),
            "subject_count": len(run_records),
            "subjects": [
                {
                    "subject": record["subject"],
                    "status": record["status"],
                    **(
                        {
                            "manifest": (
                                f"{record['subject']}/WORKSPACE MANIFEST.md"
                                if args.handoff_profile == "authoring-workspace"
                                else f"{record['subject']}/manifest.json"
                            ),
                            "expected_output": (
                                f"{record['subject']}-authored-story-workspace.zip"
                                if args.handoff_profile == "authoring-workspace"
                                else f"natal.{record['subject']}.cards.json"
                            ),
                        }
                        if record["status"] == "pass"
                        else {}
                    ),
                }
                for record in run_records
            ],
            "validator": "validate_astrowoof_editorial.py",
            "editorial_linter": "lint_astrowoof_editorial.py",
            "workspace_assembler": (
                "assemble_authoring_workspace.py"
                if args.handoff_profile == "authoring-workspace"
                else None
            ),
        }
    if args.handoff_profile == "authoring-workspace":
        lines = [
            "# AstroWoof Authoring Bundle",
            "",
            f"- **Layout:** {args.workspace_layout}",
            f"- **Subjects:** {len(run_records)}",
            "",
            "## Pass directories",
            "",
        ]
        for record in run_records:
            if record["status"] != "pass":
                continue
            if args.workspace_layout == "split":
                plan = record.get("split_assignment", {})
                for index in range(1, 7):
                    assignment = (
                        "Stories with canonical priority IDs "
                        + ", ".join(
                            f"{priority_id:03d}"
                            for priority_id in plan.get("passes", {}).get(
                                str(index), []
                            )
                        )
                        if index <= 5
                        else "Four full-chart summaries"
                    )
                    lines.append(
                        f"- `{record['subject']}_{index}/` — {assignment}"
                    )
            else:
                lines.append(
                    f"- `{record['subject']}/` — supplied story workspace"
                )
        (args.bundle_dir / "BUNDLE MANIFEST.md").write_text(
            "\n".join(lines).rstrip() + "\n",
            encoding="utf-8",
        )
        stale_manifest = args.bundle_dir / "manifest.json"
        if stale_manifest.exists():
            stale_manifest.unlink()
    else:
        write_json(args.bundle_dir / "manifest.json", bundle_manifest)
    print(json.dumps(run_manifest, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
