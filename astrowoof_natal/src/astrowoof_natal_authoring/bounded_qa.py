"""Compact product qualification for bounded-Natal semantic artifacts."""

from __future__ import annotations

import hashlib
import json
import time
import tracemalloc
from collections import Counter
from typing import Any, Iterable, Mapping

from .bounded_admission import BoundedAdmission
from .bounded_authoring import (
    BoundedAuthoringArtifacts,
    assert_provider_minimized,
    compile_bounded_authoring_artifacts,
    fake_author_bounded,
    validate_bounded_final_cards,
)
from .bounded_basis import BoundedBasis
from .bounded_selection import select_bounded_portfolio


QUALIFICATION_CONTRACT = "astrowoof.bounded_natal.product_qualification.v1"
UPSTREAM_INTERVAL_CASES = {1: 61, 24: 1441, 48: 2881}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def validate_upstream_interval_evidence(
    records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate upstream route-equivalence evidence without making it SBE authority."""
    values = [dict(record) for record in records]
    observed = {record.get("hours"): record for record in values}
    if set(observed) != set(UPSTREAM_INTERVAL_CASES):
        raise ValueError("Interval evidence must cover 1, 24, and 48 hours exactly")
    for hours, evaluations in UPSTREAM_INTERVAL_CASES.items():
        record = observed[hours]
        if set(record) != {"hours", "evaluation_count", "status"}:
            raise ValueError("Interval evidence has unsupported fields")
        if (
            isinstance(record.get("hours"), bool)
            or isinstance(record.get("evaluation_count"), bool)
            or record.get("hours") != hours
            or not isinstance(record.get("evaluation_count"), int)
            or not isinstance(record.get("hours"), int)
            or record.get("evaluation_count") != evaluations
            or record.get("status") != "passed"
        ):
            raise ValueError(f"Unsupported upstream interval evidence for {hours} hours")
    return [observed[hours] for hours in sorted(observed)]


def qualify_bounded_product(
    admission: BoundedAdmission,
    basis: BoundedBasis,
    *,
    subject: Mapping[str, Any] | None = None,
    protected_values: Iterable[str] = (),
) -> tuple[BoundedAuthoringArtifacts, dict[str, Any]]:
    """Run deterministic provider-free selection through final QA and summarize it."""
    started = time.perf_counter()
    tracemalloc.start()
    try:
        selection = select_bounded_portfolio(basis)
        artifacts = compile_bounded_authoring_artifacts(
            admission, selection, subject=subject
        )
        assert_provider_minimized(
            artifacts.authoring_packet, protected_values=protected_values
        )
        cards = fake_author_bounded(artifacts.authoring_packet)
        qa = validate_bounded_final_cards(
            cards, artifacts.claim_deck, artifacts.authoring_packet
        )
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if qa["status"] != "pass":
        raise ValueError(f"Bounded final QA failed: {qa['errors']}")
    selected = list(selection.selected)
    kinds = Counter(item["candidate_kind"] for item in selected)
    tiers = Counter(item["editorial_tier"] for item in selected)
    families = {
        family
        for item in selected
        for family in item["evidence_lineage"]["evidence_family_groups"]
    }
    roots = {
        root for item in selected for root in item.get("root_owner_refs") or []
    }
    report = {
        "schema_version": QUALIFICATION_CONTRACT,
        "status": "passed",
        "authority": "invariant_only",
        "numeric_interpretation": "editorial_utility_not_confidence_or_strength",
        "admission_id": admission.summary["admission_id"],
        "candidate_count": len(basis.candidates),
        "selected_count": len(selected),
        "selected_sha256": selection.audit["selected_sha256"],
        "claim_deck_sha256": canonical_sha256(artifacts.claim_deck),
        "provider_packet_sha256": canonical_sha256(artifacts.authoring_packet),
        "final_cards_sha256": canonical_sha256(cards),
        "candidate_kinds": dict(sorted(kinds.items())),
        "editorial_tiers": dict(sorted(tiers.items())),
        "selected_root_owner_count": len(roots),
        "selected_evidence_family_count": len(families),
        "selected_projected_term_count": len(
            artifacts.claim_deck["projected_term_registry"]["terms"]
        ),
        "qa": qa,
        "observed_elapsed_seconds": round(time.perf_counter() - started, 6),
        "observed_peak_traced_bytes": peak_bytes,
        "performance_guarantee": False,
        "provider_operation_count": 0,
    }
    return artifacts, report
