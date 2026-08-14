"""Deterministic exact-Natal angular-frame and axis configuration rules."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


ANGLE_NAMES = frozenset({"ASC", "DSC", "MC", "IC"})
AXES = {
    "asc_dsc": ("ASC", "DSC"),
    "mc_ic": ("MC", "IC"),
}
STRUCTURAL_ANGLE_RELATIONSHIPS = {
    (frozenset({"ASC", "DSC"}), "opposition"),
    (frozenset({"MC", "IC"}), "opposition"),
    (frozenset({"ASC", "MC"}), "square"),
    (frozenset({"ASC", "IC"}), "square"),
    (frozenset({"DSC", "MC"}), "square"),
    (frozenset({"DSC", "IC"}), "square"),
}


def structural_angle_reason(
    source_name: str,
    target_name: str,
    canonical_aspect: str | None,
) -> str | None:
    """Return the closed disposition for inevitable angular-frame geometry."""

    signature = (frozenset({source_name, target_name}), canonical_aspect)
    if signature in STRUCTURAL_ANGLE_RELATIONSHIPS:
        return "structurally_inevitable"
    return None


def axis_configuration_specs(
    relationship_rows: list[dict[str, Any]],
    object_candidate_by_name: dict[str, str],
) -> list[dict[str, Any]]:
    """Find external objects represented at both endpoints of one natal axis."""

    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in relationship_rows:
        source_name = row["source_name"]
        target_name = row["target_name"]
        if source_name in ANGLE_NAMES and target_name not in ANGLE_NAMES:
            angle_name, external_name = source_name, target_name
        elif target_name in ANGLE_NAMES and source_name not in ANGLE_NAMES:
            angle_name, external_name = target_name, source_name
        else:
            continue
        for axis_name, endpoints in AXES.items():
            if angle_name in endpoints:
                grouped[(external_name, axis_name)][angle_name] = row
                break

    specs: list[dict[str, Any]] = []
    for (external_name, axis_name), members_by_angle in sorted(grouped.items()):
        endpoints = AXES[axis_name]
        if set(members_by_angle) != set(endpoints):
            continue
        members = [members_by_angle[endpoint] for endpoint in endpoints]
        dependencies = sorted(
            {
                object_candidate_by_name[external_name],
                object_candidate_by_name[endpoints[0]],
                object_candidate_by_name[endpoints[1]],
            }
        )
        specs.append(
            {
                "axis_name": axis_name,
                "axis_endpoints": list(endpoints),
                "external_name": external_name,
                "dependencies": dependencies,
                "component_candidate_ids": sorted(
                    member["candidate"].candidate_id for member in members
                ),
                "source_refs": sorted(
                    {
                        source_ref
                        for member in members
                        for source_ref in member["candidate"].source_refs
                    }
                ),
                "members": [
                    {
                        "angle": endpoint,
                        "canonical_aspect": members_by_angle[endpoint][
                            "canonical_aspect"
                        ],
                        "orb": members_by_angle[endpoint]["orb"],
                        "candidate_id": members_by_angle[endpoint][
                            "candidate"
                        ].candidate_id,
                        "source_refs": members_by_angle[endpoint][
                            "candidate"
                        ].source_refs,
                        "evidence": members_by_angle[endpoint]["candidate"].evidence,
                    }
                    for endpoint in endpoints
                ],
                "component_scores": [
                    member["candidate"].score_components for member in members
                ],
            }
        )
    return specs

