"""Separate bounded-Natal claim, provider-view, and final-card contracts."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .bounded_admission import BoundedAdmission, REQUIRED_CONTEXTS
from .bounded_basis import DISPOSITION_CONTRACT
from .bounded_selection import BoundedSelection, EDITORIAL_TIERS
from .resource_access import read_resource_bytes


CLAIM_DECK_CONTRACT = "astrowoof.bounded_natal.claim_deck.v1"
AUTHORING_PACKET_CONTRACT = "astrowoof.bounded_natal.authoring_packet.v1"
FINAL_CARDS_CONTRACT = "astrowoof.bounded_natal.cards.v1"
PROVIDER_DISCLOSURE_CONTRACT = "astrowoof.bounded_natal.provider_disclosure.v1"
PROVENANCE_CONTRACT = "astrowoof.bounded_natal.delivery_provenance.v1"
BOUNDED_RUN_V2_CONTRACT = "astrowoof.bounded_natal.authoring_run.v2"
BOUNDED_SPLIT_ASSIGNMENT_CONTRACT = "astrowoof.bounded_natal.split_assignment.v1"
BOUNDED_PASS_PACKET_CONTRACT = "astrowoof.bounded_natal.authoring_pass_packet.v1"
BOUNDED_ASSIGNMENT_POLICY = "stratified-v1"
BOUNDED_ASSIGNMENT_ALGORITHM = "bounded-stratified-v1"
BOUNDED_CARD_PASS_COUNT = 5
BOUNDED_TOTAL_PASS_COUNT = 6
PROVIDER_VISIBLE_SUBJECT_FIELDS = (
    "subject_id",
    "display_name",
    "subject_type",
    "gender",
    "pronouns",
    "breed",
)
PROTECTED_SUBJECT_FIELDS = (
    "birth_date",
    "birth_datetime",
    "birth_latitude",
    "birth_longitude",
    "birth_location",
    "birth_date_precision",
    "birth_time_basis",
    "earliest_local",
    "latest_local",
    "coordinates",
    "location_evidence",
)
PROVIDER_OBJECT_ATTRIBUTE_FIELDS = (
    "canonical_object_name",
    "source_object_type",
    "source_sign",
    "projected_mode",
    "coordinate_transform",
    "projection_composition",
    "term_ref",
    "mode_ref",
)
PROVIDER_RELATIONSHIP_ATTRIBUTE_FIELDS = (
    "source_relationship_type",
    "source_aspect",
    "interaction_mode",
    "topology_only",
    "relation_ref",
    "interaction_mode_ref",
)
VOICE_KEYS = ("handler", "direct_to_dog", "hybrid")
DENSITY_KEYS = ("no_astro", "light_astro", "full_astro")


class BoundedAuthoringError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, str]:
        return {"status": "failed", "code": self.code, "message": str(self)}


@dataclass(frozen=True)
class BoundedAuthoringArtifacts:
    claim_deck: dict[str, Any]
    authoring_packet: dict[str, Any]
    disposition_report: dict[str, Any]
    split_assignment: dict[str, Any]
    pass_packets: dict[str, dict[str, Any]]


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def _bounded_resource_set() -> dict[str, Any]:
    paths = (
        "authoring/Bounded Natal Story Workspace Authoring Brief.md",
        "authoring/Bounded Natal Authoring Guiding Lights.md",
    )
    resources = [
        {
            "path": path,
            "sha256": hashlib.sha256(read_resource_bytes(path)).hexdigest(),
        }
        for path in paths
    ]
    return {
        "resource_contract": "astrowoof.bounded_natal.editorial_resources.v1",
        "resources": resources,
        "resource_set_sha256": _canonical_sha256(resources),
    }


def _bounded_assignment_features(claim: Mapping[str, Any]) -> dict[str, Any]:
    authority = claim.get("invariant_authority") or {}
    return {
        "claim_kind": str(claim.get("claim_kind") or "unknown"),
        "editorial_tier": str(claim.get("editorial_tier") or "unknown"),
        "proof_scopes": set(authority.get("proof_scopes") or []),
        "projected_terms": set(claim.get("projected_term_refs") or []),
        "priority_band": (int(claim["priority_id"]) - 1) // 10,
    }


def _bounded_assignment_similarity(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> float:
    score = 3.0 if left["claim_kind"] == right["claim_kind"] else 0.0
    score += 2.0 if left["editorial_tier"] == right["editorial_tier"] else 0.0
    score += len(left["proof_scopes"] & right["proof_scopes"])
    union = left["projected_terms"] | right["projected_terms"]
    if union:
        score += len(left["projected_terms"] & right["projected_terms"]) / len(union)
    return score


def validate_bounded_split_assignment(
    assignment: Mapping[str, Any], authoring_packet: Mapping[str, Any]
) -> None:
    if assignment.get("schema_version") != BOUNDED_SPLIT_ASSIGNMENT_CONTRACT:
        raise BoundedAuthoringError(
            "bounded_assignment_contract", "wrong bounded assignment contract"
        )
    if assignment.get("run_contract") != BOUNDED_RUN_V2_CONTRACT:
        raise BoundedAuthoringError(
            "bounded_assignment_run_contract", "wrong bounded run contract"
        )
    claims = list(authoring_packet.get("claims") or [])
    canonical = [claim.get("claim_id") for claim in claims]
    if len(canonical) != 50 or len(set(canonical)) != 50:
        raise BoundedAuthoringError(
            "bounded_assignment_source", "assignment source must contain fifty claims"
        )
    if assignment.get("canonical_claim_ids") != canonical:
        raise BoundedAuthoringError(
            "bounded_assignment_canonical_order", "canonical claim order changed"
        )
    passes = assignment.get("card_passes")
    if not isinstance(passes, list) or len(passes) != BOUNDED_CARD_PASS_COUNT:
        raise BoundedAuthoringError(
            "bounded_assignment_pass_count", "assignment requires five card passes"
        )
    flattened: list[str] = []
    for expected_number, record in enumerate(passes, 1):
        if record.get("pass_number") != expected_number:
            raise BoundedAuthoringError(
                "bounded_assignment_pass_order", "card pass numbers are not canonical"
            )
        if record.get("purpose") != "card_story":
            raise BoundedAuthoringError(
                "bounded_assignment_pass_purpose", "card pass purpose changed"
            )
        members = record.get("ordered_claim_ids")
        if not isinstance(members, list) or len(members) != 10 or len(set(members)) != 10:
            raise BoundedAuthoringError(
                "bounded_assignment_cardinality", "each card pass requires ten claims"
            )
        flattened.extend(members)
    if len(flattened) != 50 or set(flattened) != set(canonical):
        raise BoundedAuthoringError(
            "bounded_assignment_closure", "assignment must contain every claim once"
        )
    summary = assignment.get("summary_pass") or {}
    if (
        summary.get("pass_number") != BOUNDED_TOTAL_PASS_COUNT
        or summary.get("purpose") != "summary_theme"
        or summary.get("ordered_claim_ids") != []
    ):
        raise BoundedAuthoringError(
            "bounded_assignment_summary", "summary pass identity is invalid"
        )
    basis = deepcopy(dict(assignment))
    digest = basis.pop("assignment_sha256", None)
    if digest != _canonical_sha256(basis):
        raise BoundedAuthoringError(
            "bounded_assignment_digest", "assignment digest does not match content"
        )


def build_bounded_split_assignment(
    authoring_packet: Mapping[str, Any], claim_deck: Mapping[str, Any]
) -> dict[str, Any]:
    """Build the replayable anti-homogeneity five-pass bounded assignment."""
    claims = list(authoring_packet.get("claims") or [])
    if len(claims) != 50:
        raise BoundedAuthoringError(
            "bounded_assignment_source", "assignment requires fifty provider claims"
        )
    subject_id = str((authoring_packet.get("subject") or {}).get("subject_id") or "subject")
    claim_deck_sha256 = _canonical_sha256(claim_deck)
    seed = hashlib.sha256(
        (
            f"astrowoof:{BOUNDED_ASSIGNMENT_POLICY}:{subject_id}:"
            f"{claim_deck_sha256}"
        ).encode("utf-8")
    ).hexdigest()[:16]
    features = {claim["claim_id"]: _bounded_assignment_features(claim) for claim in claims}
    kind_frequency = Counter(item["claim_kind"] for item in features.values())
    tier_frequency = Counter(item["editorial_tier"] for item in features.values())

    def stable_value(*parts: object) -> str:
        material = ":".join(str(part) for part in (seed, *parts))
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    ordered = sorted(
        claims,
        key=lambda claim: (
            kind_frequency[features[claim["claim_id"]]["claim_kind"]],
            tier_frequency[features[claim["claim_id"]]["editorial_tier"]],
            stable_value("allocation", claim["claim_id"]),
        ),
    )
    passes: list[list[dict[str, Any]]] = [
        [] for _ in range(BOUNDED_CARD_PASS_COUNT)
    ]
    for claim in ordered:
        feature = features[claim["claim_id"]]
        minimum_size = min(len(items) for items in passes)
        eligible = [
            index for index, items in enumerate(passes)
            if len(items) == minimum_size and len(items) < 10
        ]

        def allocation_cost(index: int) -> tuple[float, str]:
            assigned = [features[item["claim_id"]] for item in passes[index]]
            score = 6.0 * sum(
                item["claim_kind"] == feature["claim_kind"] for item in assigned
            )
            score += 4.0 * sum(
                item["editorial_tier"] == feature["editorial_tier"] for item in assigned
            )
            score += 2.0 * sum(
                len(item["proof_scopes"] & feature["proof_scopes"])
                for item in assigned
            )
            score += 4.0 * sum(
                item["priority_band"] == feature["priority_band"] for item in assigned
            )
            return score, stable_value("pass", index + 1, claim["claim_id"])

        passes[min(eligible, key=allocation_cost)].append(claim)

    for index, assigned in enumerate(passes):
        remaining = list(assigned)
        first = min(
            remaining,
            key=lambda claim: stable_value("order", index + 1, claim["claim_id"]),
        )
        pass_order = [first]
        remaining.remove(first)
        while remaining:
            previous = features[pass_order[-1]["claim_id"]]
            next_claim = min(
                remaining,
                key=lambda claim: (
                    _bounded_assignment_similarity(
                        previous, features[claim["claim_id"]]
                    ),
                    stable_value("order", index + 1, claim["claim_id"]),
                ),
            )
            pass_order.append(next_claim)
            remaining.remove(next_claim)
        passes[index] = pass_order

    assignment: dict[str, Any] = {
        "schema_version": BOUNDED_SPLIT_ASSIGNMENT_CONTRACT,
        "run_contract": BOUNDED_RUN_V2_CONTRACT,
        "subject_id": subject_id,
        "claim_deck_sha256": claim_deck_sha256,
        "policy": BOUNDED_ASSIGNMENT_POLICY,
        "algorithm_version": BOUNDED_ASSIGNMENT_ALGORITHM,
        "seed": seed,
        "seed_basis": "subject_policy_claim_deck",
        "canonical_claim_ids": [claim["claim_id"] for claim in claims],
        "card_passes": [
            {
                "pass_id": f"{subject_id}_bounded_{index + 1}",
                "pass_number": index + 1,
                "purpose": "card_story",
                "ordered_claim_ids": [claim["claim_id"] for claim in assigned],
            }
            for index, assigned in enumerate(passes)
        ],
        "summary_pass": {
            "pass_id": f"{subject_id}_bounded_6",
            "pass_number": 6,
            "purpose": "summary_theme",
            "ordered_claim_ids": [],
        },
    }
    assignment["assignment_sha256"] = _canonical_sha256(assignment)
    validate_bounded_split_assignment(assignment, authoring_packet)
    return assignment


def _bounded_whole_dog_context(
    authoring_packet: Mapping[str, Any]
) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": claim["claim_id"],
            "claim_kind": claim["claim_kind"],
            "editorial_tier": claim["editorial_tier"],
            "invariant_authority": deepcopy(claim["invariant_authority"]),
            "semantic_seed": claim["semantic_seed"],
            "context_semantics": deepcopy(claim["context_semantics"]),
            "projected_term_refs": list(claim["projected_term_refs"]),
        }
        for claim in authoring_packet["claims"]
    ]


def build_bounded_pass_packets(
    authoring_packet: Mapping[str, Any], assignment: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    """Create six minimized self-contained provider packets from one bounded basis."""
    validate_bounded_split_assignment(assignment, authoring_packet)
    by_id = {claim["claim_id"]: claim for claim in authoring_packet["claims"]}
    whole_dog_context = _bounded_whole_dog_context(authoring_packet)
    resource_set = _bounded_resource_set()
    pass_records = [*assignment["card_passes"], assignment["summary_pass"]]
    result: dict[str, dict[str, Any]] = {}
    for pass_record in pass_records:
        card_pass = pass_record["purpose"] == "card_story"
        packet = {
            "schema_version": BOUNDED_PASS_PACKET_CONTRACT,
            "run_contract": BOUNDED_RUN_V2_CONTRACT,
            "route": "bounded_natal.v2",
            "assignment_sha256": assignment["assignment_sha256"],
            "pass_id": pass_record["pass_id"],
            "pass_number": pass_record["pass_number"],
            "pass_count": BOUNDED_TOTAL_PASS_COUNT,
            "purpose": pass_record["purpose"],
            "subject": deepcopy(authoring_packet["subject"]),
            "authority_notice": deepcopy(authoring_packet["authority_notice"]),
            "provider_disclosure": deepcopy(authoring_packet["provider_disclosure"]),
            "resource_set": deepcopy(resource_set),
            "whole_dog_context": deepcopy(whole_dog_context),
            "claims": [
                deepcopy(by_id[claim_id])
                for claim_id in pass_record["ordered_claim_ids"]
            ],
            "summaries": (
                {} if card_pass else deepcopy(authoring_packet["summaries"])
            ),
            "projected_term_registry": deepcopy(
                authoring_packet["projected_term_registry"]
            ),
        }
        packet["packet_sha256"] = _canonical_sha256(packet)
        validate_bounded_pass_packet(packet, authoring_packet, assignment)
        result[pass_record["pass_id"]] = packet
    return result


def validate_bounded_pass_packet(
    packet: Mapping[str, Any],
    authoring_packet: Mapping[str, Any],
    assignment: Mapping[str, Any],
) -> None:
    validate_bounded_split_assignment(assignment, authoring_packet)
    expected_keys = {
        "schema_version", "run_contract", "route", "assignment_sha256",
        "pass_id", "pass_number", "pass_count", "purpose", "subject",
        "authority_notice", "provider_disclosure", "resource_set",
        "whole_dog_context", "claims", "summaries", "projected_term_registry",
        "packet_sha256",
    }
    if set(packet) != expected_keys:
        raise BoundedAuthoringError(
            "bounded_pass_packet_fields", "pass packet fields are not closed"
        )
    if (
        packet.get("schema_version") != BOUNDED_PASS_PACKET_CONTRACT
        or packet.get("run_contract") != BOUNDED_RUN_V2_CONTRACT
        or packet.get("route") != "bounded_natal.v2"
        or packet.get("assignment_sha256") != assignment["assignment_sha256"]
        or packet.get("pass_count") != BOUNDED_TOTAL_PASS_COUNT
    ):
        raise BoundedAuthoringError(
            "bounded_pass_packet_binding", "pass packet route/assignment binding changed"
        )
    records = {
        item["pass_id"]: item
        for item in [*assignment["card_passes"], assignment["summary_pass"]]
    }
    expected = records.get(packet.get("pass_id"))
    if expected is None or any(
        packet.get(field) != expected[field]
        for field in ("pass_id", "pass_number", "purpose")
    ):
        raise BoundedAuthoringError(
            "bounded_pass_packet_pass", "pass packet identity changed"
        )
    claim_ids = [claim.get("claim_id") for claim in packet.get("claims") or []]
    if claim_ids != expected["ordered_claim_ids"]:
        raise BoundedAuthoringError(
            "bounded_pass_packet_membership", "pass packet membership/order changed"
        )
    expected_summaries = (
        authoring_packet["summaries"] if expected["purpose"] == "summary_theme" else {}
    )
    if packet.get("summaries") != expected_summaries:
        raise BoundedAuthoringError(
            "bounded_pass_packet_summaries", "pass summary assignment changed"
        )
    whole_ids = [
        claim.get("claim_id") for claim in packet.get("whole_dog_context") or []
    ]
    if whole_ids != assignment["canonical_claim_ids"]:
        raise BoundedAuthoringError(
            "bounded_pass_packet_context", "whole-dog context is incomplete or reordered"
        )
    if packet.get("resource_set") != _bounded_resource_set():
        raise BoundedAuthoringError(
            "bounded_pass_packet_resources", "bounded resource identity changed"
        )
    if packet.get("projected_term_registry") != authoring_packet["projected_term_registry"]:
        raise BoundedAuthoringError(
            "bounded_pass_packet_registry", "bounded registry content changed"
        )
    basis = deepcopy(dict(packet))
    digest = basis.pop("packet_sha256", None)
    if digest != _canonical_sha256(basis):
        raise BoundedAuthoringError(
            "bounded_pass_packet_digest", "pass packet digest does not match content"
        )
    assert_provider_minimized(packet)


def assemble_bounded_editorial_passes(
    pass_outputs: Mapping[str, Mapping[str, Any]],
    authoring_packet: Mapping[str, Any],
    assignment: Mapping[str, Any],
) -> dict[str, Any]:
    """Assemble unordered pass-local editorial output in canonical claim order."""
    validate_bounded_split_assignment(assignment, authoring_packet)
    expected_pass_ids = {
        *(item["pass_id"] for item in assignment["card_passes"]),
        assignment["summary_pass"]["pass_id"],
    }
    if set(pass_outputs) != expected_pass_ids:
        raise BoundedAuthoringError(
            "bounded_pass_output_inventory", "pass output inventory is incomplete"
        )
    cards_by_id: dict[str, dict[str, Any]] = {}
    for pass_record in assignment["card_passes"]:
        output = pass_outputs[pass_record["pass_id"]]
        if output.get("pass_id") != pass_record["pass_id"]:
            raise BoundedAuthoringError(
                "bounded_pass_output_binding", "card pass output binding changed"
            )
        cards = output.get("cards")
        if not isinstance(cards, list):
            raise BoundedAuthoringError(
                "bounded_pass_output_cards", "card pass output has no cards"
            )
        supplied = [card.get("claim_id") for card in cards]
        if set(supplied) != set(pass_record["ordered_claim_ids"]) or len(supplied) != 10:
            raise BoundedAuthoringError(
                "bounded_pass_output_membership", "card pass membership changed"
            )
        for card in cards:
            claim_id = card["claim_id"]
            if claim_id in cards_by_id:
                raise BoundedAuthoringError(
                    "bounded_pass_output_duplicate", "claim output is duplicated"
                )
            cards_by_id[claim_id] = deepcopy(card)
    summary_id = assignment["summary_pass"]["pass_id"]
    summary_output = pass_outputs[summary_id]
    if summary_output.get("pass_id") != summary_id:
        raise BoundedAuthoringError(
            "bounded_pass_output_binding", "summary pass output binding changed"
        )
    summaries = summary_output.get("summaries")
    if not isinstance(summaries, list):
        raise BoundedAuthoringError(
            "bounded_pass_output_summaries", "summary pass has no summaries"
        )
    supplied_summary_ids = [item.get("summary_id") for item in summaries]
    if set(supplied_summary_ids) != set(authoring_packet["summaries"]):
        raise BoundedAuthoringError(
            "bounded_pass_output_summary_membership", "summary membership changed"
        )
    summary_by_id = {item["summary_id"]: deepcopy(item) for item in summaries}
    if len(summary_by_id) != len(summaries):
        raise BoundedAuthoringError(
            "bounded_pass_output_summary_duplicate", "summary output is duplicated"
        )
    return {
        "cards": [cards_by_id[claim["claim_id"]] for claim in authoring_packet["claims"]],
        "summaries": [
            summary_by_id[summary_id]
            for summary_id in authoring_packet["summaries"]
        ],
    }


def _term_key(reference: str) -> str:
    return reference.rsplit(":", 1)[-1]


def _provider_subject(subject: Mapping[str, Any] | None) -> dict[str, Any]:
    subject = subject or {}
    return {
        field: deepcopy(subject[field])
        for field in PROVIDER_VISIBLE_SUBJECT_FIELDS
        if field in subject
    }


def _selected_by_id(selection: BoundedSelection) -> dict[str, dict[str, Any]]:
    return {claim["candidate_id"]: claim for claim in selection.selected}


def _expanded_term_refs(
    claim_id: str,
    by_id: Mapping[str, Mapping[str, Any]],
    active: frozenset[str] = frozenset(),
) -> set[str]:
    if claim_id in active:
        raise BoundedAuthoringError(
            "bounded_claim_dependency_cycle", f"claim dependency cycle at {claim_id}"
        )
    claim = by_id[claim_id]
    refs = set(claim.get("projected_term_refs") or [])
    for dependency in claim.get("member_candidate_ids") or []:
        if dependency not in by_id:
            raise BoundedAuthoringError(
                "bounded_claim_dependency_missing", f"missing selected claim {dependency}"
            )
        refs.update(_expanded_term_refs(dependency, by_id, active | {claim_id}))
    return refs


def _safe_context_record(row: Mapping[str, Any]) -> dict[str, Any]:
    attributes = row.get("attributes") or {}
    if "relationship_type" in row:
        allowed_attributes = PROVIDER_RELATIONSHIP_ATTRIBUTE_FIELDS
        value = {
            "semantic_type": "relationship",
            "relationship_type": row.get("relationship_type"),
            "operators": deepcopy(row.get("operators") or []),
            "theme_tags": deepcopy(row.get("theme_tags") or []),
            "attributes": {
                field: deepcopy(attributes[field])
                for field in allowed_attributes
                if field in attributes
            },
        }
    else:
        allowed_attributes = PROVIDER_OBJECT_ATTRIBUTE_FIELDS
        value = {
            "semantic_type": "object",
            "object_type": row.get("object_type"),
            "name": row.get("name"),
            "operators": deepcopy(row.get("operators") or []),
            "attributes": {
                field: deepcopy(attributes[field])
                for field in allowed_attributes
                if field in attributes
            },
        }
    return value


def _semantic_view(
    claim: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    if claim["candidate_kind"] == "invariant_configuration":
        return {
            context: [
                {
                    "semantic_type": "configuration",
                    "member_claim_ids": list(claim["member_candidate_ids"]),
                    "root_owner_count": len(claim.get("root_owner_refs") or []),
                }
            ]
            for context in sorted(REQUIRED_CONTEXTS)
        }
    records = claim.get("context_records") or {}
    return {
        context: [_safe_context_record(row) for row in records[context]]
        for context in sorted(records)
    }


def _semantic_seed(view: Mapping[str, Any], claim_kind: str) -> str:
    first_context = next(iter(sorted(view)))
    rows = view[first_context]
    if claim_kind == "invariant_configuration":
        return "A stable configuration links the listed invariant claim families."
    row = rows[0]
    attributes = row.get("attributes") or {}
    if row["semantic_type"] == "object":
        operator = row.get("name") or "projected subsystem"
        mode = attributes.get("projected_mode")
        source = attributes.get("canonical_object_name")
        transform = attributes.get("coordinate_transform")
        parts = [f"Invariant {source or 'bounded source'} maps to {operator}"]
        if mode:
            parts.append(f"through {mode}")
        if transform:
            parts.append(f"under {transform}")
        return " ".join(parts) + "."
    relation = row.get("relationship_type") or "projected interaction"
    aspect = attributes.get("source_aspect")
    interaction = attributes.get("interaction_mode")
    detail = ", ".join(value for value in (aspect, interaction) if value)
    return f"Invariant relationship: {relation}{f' ({detail})' if detail else ''}."


def _term_subset(
    registry: Mapping[str, Any], references: Iterable[str]
) -> dict[str, Any]:
    terms = registry.get("terms") or {}
    keys = sorted({_term_key(reference) for reference in references})
    missing = sorted(set(keys) - set(terms))
    if missing:
        raise BoundedAuthoringError(
            "bounded_projected_term_missing",
            f"selected claims reference missing projected terms: {missing}",
        )
    return {
        "registry_id": registry.get("registry_id"),
        "registry_version": registry.get("registry_version"),
        "target_ontology": registry.get("target_ontology"),
        "materialization": "selected_terms_subset",
        "terms": {key: deepcopy(terms[key]) for key in keys},
    }


def _blank_editorial_fields() -> dict[str, Any]:
    voices = {voice: "__WRITE__" for voice in VOICE_KEYS}
    return {
        "dos": ["__WRITE__", "__WRITE__", "__WRITE__"],
        "donts": ["__WRITE__", "__WRITE__", "__WRITE__"],
        "funny_dog_quotes": ["__WRITE__"],
        "imperative_dog_quotes": ["__WRITE__"],
        "applicable_canine_jokes": ["__WRITE__"],
        "densities": {
            density: {
                "headline": deepcopy(voices),
                "body": deepcopy(voices),
            }
            for density in DENSITY_KEYS
        },
    }


def compile_bounded_authoring_artifacts(
    admission: BoundedAdmission,
    selection: BoundedSelection,
    *,
    subject: Mapping[str, Any] | None = None,
) -> BoundedAuthoringArtifacts:
    """Compile private and provider-visible bounded artifacts without a provider."""

    if len(selection.selected) != 50:
        raise BoundedAuthoringError(
            "bounded_claim_count", "bounded claim deck requires exactly fifty claims"
        )
    by_id = _selected_by_id(selection)
    selected_ids = [claim["candidate_id"] for claim in selection.selected]
    if len(by_id) != 50:
        raise BoundedAuthoringError("bounded_claim_identity", "claim IDs must be unique")
    if any(
        claim.get("epistemic_classification") != "invariant"
        for claim in selection.selected
    ):
        raise BoundedAuthoringError(
            "bounded_claim_authority", "only invariant claims may be compiled"
        )
    for claim in selection.selected:
        if not set(claim.get("member_candidate_ids") or []) <= set(by_id):
            raise BoundedAuthoringError(
                "bounded_claim_dependency_missing",
                f"{claim['candidate_id']} is not dependency closed",
            )

    baseline = admission.artifacts_by_context[sorted(admission.artifacts_by_context)[0]]
    registry = baseline["projected_term_registry"]
    term_refs = {
        claim_id: sorted(_expanded_term_refs(claim_id, by_id)) for claim_id in selected_ids
    }
    all_term_refs = sorted({ref for refs in term_refs.values() for ref in refs})
    used_registry = _term_subset(registry, all_term_refs)

    private_claims = []
    provider_claims = []
    selected_evidence: dict[str, Any] = {}
    for claim in selection.selected:
        claim_id = claim["candidate_id"]
        view = _semantic_view(claim, by_id)
        evidence_refs = sorted(
            claim.get("evidence_lineage", {}).get("resolved_evidence_refs", [])
        )
        evidence_digest = _canonical_sha256(evidence_refs)
        selected_evidence[claim_id] = {
            "scope": "claim_local_selected_evidence",
            "evidence_refs": evidence_refs,
            "evidence_sha256": evidence_digest,
            "proof_scopes": list(claim.get("proof_scopes") or []),
            "evidence_family_groups": list(
                claim.get("evidence_lineage", {}).get("evidence_family_groups", [])
            ),
        }
        locked = {
            "epistemic_classification": "invariant",
            "claim_kind": claim["candidate_kind"],
            "proof_scopes": list(claim.get("proof_scopes") or []),
            "dependency_claim_ids": list(claim.get("member_candidate_ids") or []),
            "source_refs": list(claim.get("source_refs") or []),
            "correspondence_ids": list(claim.get("correspondence_ids") or []),
            "root_owner_refs": list(claim.get("root_owner_refs") or []),
            "projected_term_refs": term_refs[claim_id],
            "evidence_sha256": evidence_digest,
        }
        private_claims.append(
            {
                "claim_id": claim_id,
                "priority_id": claim["selection_rank"],
                "editorial_tier": claim["editorial_tier"],
                "bounded_editorial_utility": claim["bounded_editorial_utility"],
                "authority": deepcopy(locked),
                "context_records": deepcopy(claim.get("context_records") or {}),
                "evidence_lineage": deepcopy(claim.get("evidence_lineage") or {}),
                "selection_audit": {
                    "components": deepcopy(claim["components"]),
                    "penalties": deepcopy(claim["penalties"]),
                },
            }
        )
        provider_claims.append(
            {
                "claim_id": claim_id,
                "priority_id": claim["selection_rank"],
                "claim_kind": claim["candidate_kind"],
                "editorial_tier": claim["editorial_tier"],
                "editorial_utility": claim["bounded_editorial_utility"],
                "invariant_authority": {
                    "classification": "invariant",
                    "proof_scopes": list(claim.get("proof_scopes") or []),
                    "dependency_claim_ids": list(
                        claim.get("member_candidate_ids") or []
                    ),
                    "evidence_sha256": evidence_digest,
                },
                "semantic_seed": _semantic_seed(view, claim["candidate_kind"]),
                "context_semantics": view,
                "projected_term_refs": term_refs[claim_id],
                "editorial_fields": _blank_editorial_fields(),
            }
        )

    summary_groups = {
        f"summary_{index + 1}": selected_ids[index::4] for index in range(4)
    }
    whole_dog_evidence = {
        summary_id: {
            "scope": "summary_whole_dog_selected_basis",
            "selected_claim_ids": claim_ids,
            "selected_claim_set_sha256": _canonical_sha256(claim_ids),
        }
        for summary_id, claim_ids in summary_groups.items()
    }
    source = {
        "admission_id": admission.summary["admission_id"],
        "source_artifact_sha256": admission.summary["source_artifact_sha256"],
        "input_contract": admission.summary["output_contract"],
        "input_contract_version": admission.summary["contract_version"],
        "spc_version": admission.summary["spc_version"],
        "profile_id": admission.summary["profile_id"],
        "profile_version": admission.summary["profile_version"],
        "projected_term_registry_sha256": admission.summary[
            "projected_term_registry_sha256"
        ],
    }
    provenance = {
        "schema_version": PROVENANCE_CONTRACT,
        "selected_card_evidence": selected_evidence,
        "summary_whole_dog_evidence": whole_dog_evidence,
        "selection_audit_sha256": selection.audit["selected_sha256"],
    }
    claim_deck = {
        "schema_version": CLAIM_DECK_CONTRACT,
        "status": "awaiting_authoring",
        "source": source,
        "authority": {
            "classification": "invariant",
            "proof_domain": "complete_normalized_birth_interval",
            "limitations": deepcopy(baseline.get("limitations") or []),
        },
        "selection": {
            "candidate_policy": selection.audit["candidate_policy"],
            "utility_profile": selection.audit["utility_profile"],
            "foundational_policy": selection.audit["foundational_policy"],
            "selected_count": 50,
            "selected_sha256": selection.audit["selected_sha256"],
        },
        "claims": private_claims,
        "projected_term_registry": used_registry,
        "provenance": provenance,
    }
    disclosure = {
        "schema_version": PROVIDER_DISCLOSURE_CONTRACT,
        "subject_fields_allowed": list(PROVIDER_VISIBLE_SUBJECT_FIELDS),
        "subject_fields_protected": list(PROTECTED_SUBJECT_FIELDS),
        "object_attribute_fields_allowed": list(PROVIDER_OBJECT_ATTRIBUTE_FIELDS),
        "relationship_attribute_fields_allowed": list(
            PROVIDER_RELATIONSHIP_ATTRIBUTE_FIELDS
        ),
        "evidence_disclosure": "classification_proof_scope_and_digest_only",
        "registry_disclosure": "selected_terms_subset_only",
        "disposition_report_disclosed": False,
        "source_graph_disclosed": False,
    }
    authoring_packet = {
        "schema_version": AUTHORING_PACKET_CONTRACT,
        "editorial_status": "awaiting_authoring",
        "subject": _provider_subject(subject),
        "authority_notice": {
            "ordinary_prose_must_be_invariant": True,
            "representative_time_prohibited": True,
            "exact_geometry_reconstruction_prohibited": True,
            "editorial_utility_is_not_confidence": True,
        },
        "provider_disclosure": disclosure,
        "claims": provider_claims,
        "summaries": {
            summary_id: {
                "evidence_scope": "summary_whole_dog_selected_basis",
                "selected_claim_ids": claim_ids,
                "editorial_fields": _blank_editorial_fields(),
            }
            for summary_id, claim_ids in summary_groups.items()
        },
        "projected_term_registry": used_registry,
    }
    assert_provider_minimized(authoring_packet)
    validate_bounded_claim_deck(claim_deck)
    validate_bounded_authoring_packet(authoring_packet, claim_deck)
    disposition = deepcopy(selection.disposition_report)
    if disposition.get("schema_version") != DISPOSITION_CONTRACT:
        raise BoundedAuthoringError(
            "bounded_disposition_contract", "unexpected disposition contract"
        )
    disposition["claim_deck_sha256"] = _canonical_sha256(claim_deck)
    disposition["authoring_packet_sha256"] = _canonical_sha256(authoring_packet)
    split_assignment = build_bounded_split_assignment(authoring_packet, claim_deck)
    pass_packets = build_bounded_pass_packets(authoring_packet, split_assignment)
    return BoundedAuthoringArtifacts(
        claim_deck,
        authoring_packet,
        disposition,
        split_assignment,
        pass_packets,
    )


def assert_provider_minimized(
    packet: Mapping[str, Any], *, protected_values: Iterable[str] = ()
) -> None:
    """Enforce the bounded provider allow-list and seeded-value absence."""

    rendered = json.dumps(packet, sort_keys=True, ensure_ascii=False)
    def keys(value: Any) -> set[str]:
        if isinstance(value, Mapping):
            return {
                *(str(key).lower() for key in value),
                *(item for child in value.values() for item in keys(child)),
            }
        if isinstance(value, list):
            return {item for child in value for item in keys(child)}
        return set()

    disclosed_keys = keys(packet)
    for field in PROTECTED_SUBJECT_FIELDS:
        if field.lower() in disclosed_keys:
            raise BoundedAuthoringError(
                "bounded_provider_protected_field", f"provider packet contains {field}"
            )
    for prohibited in (
        "source_identity",
        "source_artifact_ref",
        "source_evidence",
        "range_evidence",
        "transition_witnesses",
        "counterexamples",
        "structural_strength_score",
        "projection_relevance_score",
        "orb_range",
    ):
        if prohibited in disclosed_keys:
            raise BoundedAuthoringError(
                "bounded_provider_prohibited_field",
                f"provider packet contains prohibited field {prohibited}",
            )
    for value in protected_values:
        if isinstance(value, str) and value and value in rendered:
            raise BoundedAuthoringError(
                "bounded_provider_protected_value",
                "provider packet contains a seeded protected value",
            )


def validate_bounded_claim_deck(deck: Mapping[str, Any]) -> None:
    if deck.get("schema_version") != CLAIM_DECK_CONTRACT:
        raise BoundedAuthoringError("bounded_claim_deck_contract", "wrong claim deck contract")
    claims = deck.get("claims")
    if not isinstance(claims, list) or len(claims) != 50:
        raise BoundedAuthoringError("bounded_claim_count", "claim deck must contain fifty claims")
    ids = [claim.get("claim_id") for claim in claims]
    if len(set(ids)) != 50 or any(not isinstance(value, str) for value in ids):
        raise BoundedAuthoringError("bounded_claim_identity", "claim IDs must be unique strings")
    id_set = set(ids)
    tiers = set(EDITORIAL_TIERS)
    for claim in claims:
        authority = claim.get("authority") or {}
        if authority.get("epistemic_classification") != "invariant":
            raise BoundedAuthoringError("bounded_claim_authority", "claim is not invariant")
        if claim.get("editorial_tier") not in tiers:
            raise BoundedAuthoringError("bounded_editorial_tier", "unknown editorial tier")
        if not set(authority.get("dependency_claim_ids") or []) <= id_set:
            raise BoundedAuthoringError("bounded_claim_dependency_missing", "claim deck is not closed")
    node_variants: dict[str, list[Mapping[str, Any]]] = {
        "Mean_Node": [], "True_Node": [],
    }
    for claim in claims:
        sources = (claim.get("authority") or {}).get("source_refs") or []
        for variant in node_variants:
            if any(str(source).endswith(f":{variant}") for source in sources):
                node_variants[variant].append(claim)
    for mean_claim in node_variants["Mean_Node"]:
        for true_claim in node_variants["True_Node"]:
            if (
                (mean_claim.get("authority") or {}).get("claim_kind")
                == (true_claim.get("authority") or {}).get("claim_kind")
                and (mean_claim.get("authority") or {}).get("projected_term_refs")
                == (true_claim.get("authority") or {}).get("projected_term_refs")
                and {
                    (
                        row.get("name"),
                        tuple(row.get("operators") or []),
                        (row.get("attributes") or {}).get("canonical_object_name"),
                        (row.get("attributes") or {}).get("source_sign"),
                        (row.get("attributes") or {}).get("projected_mode"),
                    )
                    for rows in (mean_claim.get("context_records") or {}).values()
                    for row in rows
                }
                == {
                    (
                        row.get("name"),
                        tuple(row.get("operators") or []),
                        (row.get("attributes") or {}).get("canonical_object_name"),
                        (row.get("attributes") or {}).get("source_sign"),
                        (row.get("attributes") or {}).get("projected_mode"),
                    )
                    for rows in (true_claim.get("context_records") or {}).values()
                    for row in rows
                }
            ):
                raise BoundedAuthoringError(
                    "bounded_equivalent_node_claims",
                    "selected Mean Node and True Node claims have equivalent editorial semantics",
                )
    registry = deck.get("projected_term_registry") or {}
    terms = registry.get("terms") or {}
    referenced = {
        _term_key(ref)
        for claim in claims
        for ref in (claim.get("authority") or {}).get("projected_term_refs") or []
    }
    if not referenced <= set(terms):
        raise BoundedAuthoringError("bounded_projected_term_missing", "claim term closure failed")
    provenance = deck.get("provenance") or {}
    card_evidence = provenance.get("selected_card_evidence") or {}
    summary_evidence = provenance.get("summary_whole_dog_evidence") or {}
    if set(card_evidence) != id_set or set(summary_evidence) != {
        "summary_1", "summary_2", "summary_3", "summary_4"
    }:
        raise BoundedAuthoringError(
            "bounded_evidence_scope", "card and summary evidence scopes are incomplete"
        )
    if any(value.get("scope") != "claim_local_selected_evidence" for value in card_evidence.values()):
        raise BoundedAuthoringError("bounded_evidence_scope", "selected-card scope is invalid")
    if any(value.get("scope") != "summary_whole_dog_selected_basis" for value in summary_evidence.values()):
        raise BoundedAuthoringError("bounded_evidence_scope", "summary scope is invalid")


def validate_bounded_authoring_packet(
    packet: Mapping[str, Any], claim_deck: Mapping[str, Any]
) -> None:
    if packet.get("schema_version") != AUTHORING_PACKET_CONTRACT:
        raise BoundedAuthoringError("bounded_authoring_packet_contract", "wrong packet contract")
    assert_provider_minimized(packet)
    if not set(packet.get("subject") or {}) <= set(PROVIDER_VISIBLE_SUBJECT_FIELDS):
        raise BoundedAuthoringError(
            "bounded_provider_subject_field", "provider subject view is not allow-listed"
        )
    claims = packet.get("claims")
    if not isinstance(claims, list) or len(claims) != 50:
        raise BoundedAuthoringError("bounded_claim_count", "authoring packet must contain fifty claims")
    locked = {claim["claim_id"]: claim for claim in claim_deck["claims"]}
    terms = (packet.get("projected_term_registry") or {}).get("terms") or {}
    for claim in claims:
        source = locked.get(claim.get("claim_id"))
        if source is None:
            raise BoundedAuthoringError("bounded_claim_identity", "packet claim is not selected")
        authority = claim.get("invariant_authority") or {}
        expected = source["authority"]
        if authority != {
            "classification": expected["epistemic_classification"],
            "proof_scopes": expected["proof_scopes"],
            "dependency_claim_ids": expected["dependency_claim_ids"],
            "evidence_sha256": expected["evidence_sha256"],
        }:
            raise BoundedAuthoringError("bounded_locked_authority", "provider authority drifted")
        if set(claim.get("context_semantics") or {}) != set(REQUIRED_CONTEXTS):
            raise BoundedAuthoringError("bounded_context_semantics", "claim lacks four contexts")
        for rows in claim["context_semantics"].values():
            for row in rows:
                attributes = row.get("attributes") or {}
                allowed = (
                    PROVIDER_RELATIONSHIP_ATTRIBUTE_FIELDS
                    if row.get("semantic_type") == "relationship"
                    else PROVIDER_OBJECT_ATTRIBUTE_FIELDS
                )
                if not set(attributes) <= set(allowed):
                    raise BoundedAuthoringError(
                        "bounded_provider_semantic_field",
                        "provider semantic row is not allow-listed",
                    )
        if not {
            _term_key(ref) for ref in claim.get("projected_term_refs") or []
        } <= set(terms):
            raise BoundedAuthoringError(
                "bounded_projected_term_missing", "provider term closure failed"
            )
    if "__WRITE__" not in json.dumps(packet):
        raise BoundedAuthoringError("bounded_editorial_scaffold", "packet lacks writing fields")


def fake_author_bounded(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Produce deterministic provider-free bounded final cards for contract QA."""

    claims = packet.get("claims") or []
    cards = []
    for claim in claims:
        claim_id = claim["claim_id"]
        token = hashlib.sha256(claim_id.encode("utf-8")).hexdigest()[:12]
        seed = claim["semantic_seed"]
        cards.append(
            {
                "claim_id": claim_id,
                "priority_id": claim["priority_id"],
                "claim_kind": claim["claim_kind"],
                "editorial_tier": claim["editorial_tier"],
                "invariant_authority": deepcopy(claim["invariant_authority"]),
                "evidence_provenance": {
                    "scope": "claim_local_selected_evidence",
                    "evidence_sha256": claim["invariant_authority"]["evidence_sha256"],
                },
                "dos": [f"Support invariant practice {token}-{index}." for index in range(1, 4)],
                "donts": [f"Avoid flattening invariant nuance {token}-{index}." for index in range(1, 4)],
                "funny_dog_quotes": [f"My invariant snack forecast is {token}."],
                "imperative_dog_quotes": [f"Observe my stable pattern {token}."],
                "applicable_canine_jokes": [f"The bounded treat theorem {token} holds."],
                "densities": {
                    density: {
                        "headline": {
                            voice: f"Stable Portrait {token} {density} {voice}"
                            for voice in VOICE_KEYS
                        },
                        "body": {
                            voice: (
                                f"Stable behavioral portrait {token} for the {voice} view."
                                if density == "no_astro"
                                else (
                                    f"A bounded projected pattern supports portrait {token} "
                                    f"for the {voice} view."
                                )
                                if density == "light_astro"
                                else f"{seed} Editorial portrait {token} for the {voice} view."
                            )
                            for voice in VOICE_KEYS
                        },
                    }
                    for density in DENSITY_KEYS
                },
            }
        )
    summaries = {}
    for summary_id, summary in sorted((packet.get("summaries") or {}).items()):
        token = hashlib.sha256(summary_id.encode("utf-8")).hexdigest()[:12]
        summaries[summary_id] = {
            "evidence_provenance": {
                "scope": "summary_whole_dog_selected_basis",
                "selected_claim_ids": list(summary["selected_claim_ids"]),
            },
            "headline": {voice: f"Whole Dog Portrait {token} {voice}" for voice in VOICE_KEYS},
            "body": {
                voice: f"Whole-dog synthesis {token} integrates only its selected invariant claims for {voice}."
                for voice in VOICE_KEYS
            },
        }
    return {
        "schema_version": FINAL_CARDS_CONTRACT,
        "editorial_status": "complete",
        "subject": deepcopy(packet.get("subject") or {}),
        "authority_notice": deepcopy(packet["authority_notice"]),
        "cards": cards,
        "summaries": summaries,
        "projected_term_registry": deepcopy(packet["projected_term_registry"]),
    }


def validate_bounded_final_cards(
    final_cards: Mapping[str, Any],
    claim_deck: Mapping[str, Any],
    authoring_packet: Mapping[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if final_cards.get("schema_version") != FINAL_CARDS_CONTRACT:
        errors.append("wrong final-card contract")
    if final_cards.get("subject") != authoring_packet.get("subject"):
        errors.append("provider-visible subject drifted")
    if final_cards.get("authority_notice") != authoring_packet.get("authority_notice"):
        errors.append("authority notice drifted")
    cards = final_cards.get("cards") or []
    if len(cards) != 50:
        errors.append("final deck must contain fifty cards")
    locked = {claim["claim_id"]: claim for claim in authoring_packet["claims"]}
    ids = [card.get("claim_id") for card in cards]
    if len(set(ids)) != 50 or set(ids) != set(locked):
        errors.append("final card IDs do not equal selected claims")
    for card in cards:
        source = locked.get(card.get("claim_id"))
        if source is None:
            continue
        for field in ("priority_id", "claim_kind", "editorial_tier", "invariant_authority"):
            if card.get(field) != source.get(field):
                errors.append(f"{card.get('claim_id')} changed locked {field}")
        evidence = card.get("evidence_provenance") or {}
        if evidence != {
            "scope": "claim_local_selected_evidence",
            "evidence_sha256": source["invariant_authority"]["evidence_sha256"],
        }:
            errors.append(f"{card.get('claim_id')} changed selected-card evidence")
        if any("__WRITE__" in json.dumps(card.get(field)) for field in ("dos", "donts", "densities")):
            errors.append(f"{card.get('claim_id')} retains placeholders")
        for field in ("dos", "donts"):
            values = card.get(field)
            if (
                not isinstance(values, list)
                or len(values) != 3
                or any(not isinstance(value, str) or not value.strip() for value in values)
            ):
                errors.append(f"{card.get('claim_id')} has invalid {field}")
        for field in (
            "funny_dog_quotes",
            "imperative_dog_quotes",
            "applicable_canine_jokes",
        ):
            values = card.get(field)
            if (
                not isinstance(values, list)
                or not values
                or any(not isinstance(value, str) or not value.strip() for value in values)
            ):
                errors.append(f"{card.get('claim_id')} has invalid {field}")
        densities = card.get("densities") or {}
        if set(densities) != set(DENSITY_KEYS):
            errors.append(f"{card.get('claim_id')} has invalid densities")
        else:
            for density in DENSITY_KEYS:
                for field in ("headline", "body"):
                    voices = (densities[density] or {}).get(field) or {}
                    if set(voices) != set(VOICE_KEYS) or any(
                        not isinstance(value, str) or not value.strip()
                        for value in voices.values()
                    ):
                        errors.append(
                            f"{card.get('claim_id')} has invalid {density}.{field}"
                        )
    expected_summaries = authoring_packet["summaries"]
    summaries = final_cards.get("summaries") or {}
    if set(summaries) != set(expected_summaries):
        errors.append("summary set mismatch")
    else:
        for summary_id, source in expected_summaries.items():
            evidence = (summaries[summary_id] or {}).get("evidence_provenance") or {}
            if evidence != {
                "scope": "summary_whole_dog_selected_basis",
                "selected_claim_ids": source["selected_claim_ids"],
            }:
                errors.append(f"{summary_id} changed whole-dog evidence")
            for field in ("headline", "body"):
                voices = (summaries[summary_id] or {}).get(field) or {}
                if set(voices) != set(VOICE_KEYS) or any(
                    not isinstance(value, str) or not value.strip()
                    for value in voices.values()
                ):
                    errors.append(f"{summary_id} has invalid {field}")
    if final_cards.get("projected_term_registry") != claim_deck.get(
        "projected_term_registry"
    ):
        errors.append("projected-term registry drifted")
    normalized_passages: set[str] = set()
    for card in cards:
        for density in DENSITY_KEYS:
            for voice in VOICE_KEYS:
                body = (((card.get("densities") or {}).get(density) or {}).get("body") or {}).get(voice)
                normalized = " ".join(re.findall(r"[a-z0-9]+", (body or "").lower()))
                if normalized in normalized_passages:
                    errors.append("normalized editorial passage is duplicated")
                normalized_passages.add(normalized)
    return {
        "schema_version": "astrowoof.bounded_natal.final_qa.v1",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "claim_count": len(cards),
        "summary_count": len(summaries),
        "selected_card_evidence_scope": "claim_local_selected_evidence",
        "summary_evidence_scope": "summary_whole_dog_selected_basis",
        "provider_operation_count": 0,
    }
