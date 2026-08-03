#!/usr/bin/env python3
"""Measure current FULL CHART BASIS and prototype a compact chart map."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[8]
SRC = REPO / "astrowoof_natal" / "src"
sys.path.insert(0, str(SRC))

from build_projected_semantic_basis import render_full_chart_basis  # noqa: E402

HERE = Path(__file__).resolve().parent
PACKETS = {
    subject: REPO / "astrowoof_natal" / "qa" / "reference_decks" / subject
    / "selected-authoring-packet.json"
    for subject in ("ashley", "brandi", "bre", "ella", "kevin")
}


def estimate_tokens(text: str) -> int:
    return (len(text.encode("utf-8")) + 3) // 4


def section_metrics(text: str) -> dict[str, dict[str, int]]:
    headings = [
        "## Selected Chart Material",
        "## Additional Chart Material",
        "## Complete Projected-Term Registry",
    ]
    positions = [(heading, text.index(heading)) for heading in headings]
    result: dict[str, dict[str, int]] = {}
    for index, (heading, start) in enumerate(positions):
        end = positions[index + 1][1] if index + 1 < len(positions) else len(text)
        value = text[start:end]
        result[heading.removeprefix("## ")] = {
            "characters": len(value),
            "utf8_bytes": len(value.encode("utf-8")),
            "estimated_tokens": estimate_tokens(value),
            "lines": len(value.splitlines()),
        }
    return result


def claims(packet: dict[str, Any]) -> list[dict[str, Any]]:
    return [*packet.get("cards", []), *packet.get("unselected_claims", [])]


def first_context_record(evidence: dict[str, Any]) -> dict[str, Any] | None:
    records = evidence.get("context_records") or {}
    if not records:
        return None
    return records[sorted(records)[0]].get("record")


def extract_chart_map(packet: dict[str, Any]) -> dict[str, Any]:
    objects: dict[str, dict[str, Any]] = {}
    relationships: dict[str, dict[str, Any]] = {}
    projected_ids: dict[str, dict[str, dict[str, str | None]]] = {}
    all_claims = claims(packet)

    for claim in all_claims:
        for evidence in claim.get("evidence", []):
            if evidence.get("kind") != "projected_object":
                continue
            for context, wrapper in (evidence.get("context_records") or {}).items():
                record = wrapper.get("record") or {}
                attributes = record.get("attributes") or {}
                projected_ids.setdefault(context, {})[record.get("id", "")] = {
                    "projected_name": record.get("name", "unknown"),
                    "canonical_name": attributes.get("canonical_object_name"),
                }
                refs = evidence.get("source_refs") or record.get("source_refs") or []
                if not refs:
                    continue
                key = refs[0]
                objects.setdefault(key, {
                    "source_ref": key,
                    "canonical_name": attributes.get("canonical_object_name"),
                    "source_sign": attributes.get("source_sign"),
                    "source_house": attributes.get("source_house"),
                    "projected_name": record.get("name"),
                    "projected_mode": attributes.get("projected_mode"),
                    "doghouse_number": attributes.get("doghouse_number"),
                    "projected_domain": attributes.get("projected_domain"),
                })

    for claim in all_claims:
        for evidence in claim.get("evidence", []):
            if evidence.get("kind") != "projected_relationship":
                continue
            contexts = evidence.get("context_records") or {}
            if not contexts:
                continue
            context = sorted(contexts)[0]
            record = contexts[context].get("record") or {}
            attributes = record.get("attributes") or {}
            refs = evidence.get("source_refs") or record.get("source_relationship_refs") or []
            if not refs:
                continue
            key = refs[0]
            source_object = projected_ids.get(context, {}).get(record.get("source_id", ""), {})
            target_object = projected_ids.get(context, {}).get(record.get("target_id", ""), {})
            relationships.setdefault(key, {
                "source_ref": key,
                "source_canonical_name": source_object.get("canonical_name"),
                "target_canonical_name": target_object.get("canonical_name"),
                "source_projected_name": source_object.get("projected_name")
                or attributes.get("source_canine_subsystem"),
                "target_projected_name": target_object.get("projected_name")
                or attributes.get("target_canine_subsystem"),
                "canonical_aspect": attributes.get("canonical_aspect"),
                "orb": attributes.get("orb"),
                "projected_relationship": record.get("relationship_type"),
                "interaction_mode": attributes.get("interaction_mode"),
            })

    referenced_terms: set[str] = set()
    for item in [*objects.values(), *relationships.values()]:
        for value in item.values():
            if isinstance(value, str):
                referenced_terms.add(value)
    registry = packet.get("projected_term_registry", {}).get("terms", {})
    glossary = {
        term: {
            "label": entry.get("canonical_label", term),
            "meaning": entry.get("long_description") or entry.get("short_description"),
        }
        for term, entry in registry.items()
        if term in referenced_terms
    }
    return {
        "objects": sorted(objects.values(), key=lambda item: item["source_ref"]),
        "relationships": sorted(
            relationships.values(), key=lambda item: item["source_ref"]
        ),
        "selected_claims": [
            {"id": item["claim_id"], "type": item["claim_type"], "claim": item["canonical_claim"]}
            for item in packet.get("cards", [])
        ],
        "additional_claims": [
            {
                "id": item.get("claim_id", item.get("candidate_id")),
                "type": item.get("claim_type"),
                "claim": item.get("canonical_claim", item.get("claim")),
            }
            for item in packet.get("unselected_claims", [])
        ],
        "projected_glossary": glossary,
        "reconstruction_limits": [
            "Projected object records preserve canonical name, sign, and house/doghouse mapping but not canonical longitude or degree in this packet.",
            "Projected relationship records preserve aspect geometry and orb, but canonical endpoint identity must be inferred through projected object IDs or dependency claims.",
            "Only material retained in projected artifacts and the SBE candidate pool can be reconstructed; absence cannot be distinguished from upstream omission.",
        ],
    }


def compact_markdown(packet: dict[str, Any], chart_map: dict[str, Any]) -> str:
    name = packet["subject"].get("display_name") or packet["subject"]["subject_id"]
    lines = [
        f"# Authoring Chart Map: {name}", "",
        "This is a deterministic downstream reconstruction from projected evidence. It is not a canonical chart export.", "",
        "## Recovered Objects", "",
    ]
    for item in chart_map["objects"]:
        canonical = item.get("canonical_name") or item["source_ref"].rsplit(":", 1)[-1]
        source = " / ".join(str(value) for value in (
            item.get("source_sign"),
            f"house {item['source_house']}" if item.get("source_house") else None,
        ) if value)
        projected = " / ".join(str(value) for value in (
            item.get("projected_name"), item.get("projected_mode"),
            f"Doghouse {item['doghouse_number']}" if item.get("doghouse_number") else item.get("projected_domain"),
        ) if value)
        lines.append(f"- **{canonical}:** {source or 'source details incomplete'} → {projected}")
    lines.extend(["", "## Recovered Interactions", ""])
    for item in chart_map["relationships"]:
        orb = f", orb {item['orb']:.3f}°" if isinstance(item.get("orb"), (int, float)) else ""
        canonical_pair = " — ".join(
            value for value in (
                item.get("source_canonical_name"), item.get("target_canonical_name")
            ) if value
        )
        canonical_pair = f" ({canonical_pair})" if canonical_pair else ""
        lines.append(
            f"- **{item.get('source_projected_name')} {item.get('canonical_aspect') or 'interaction'} "
            f"{item.get('target_projected_name')}**{canonical_pair}{orb} → {item.get('projected_relationship')} / "
            f"{item.get('interaction_mode')}"
        )
    lines.extend(["", "## Selected Semantic Basis", ""])
    lines.extend(f"- **{item['id']}:** {item['claim']}" for item in chart_map["selected_claims"])
    lines.extend(["", "## Additional Semantic Basis", ""])
    lines.extend(f"- **{item['id']}:** {item['claim']}" for item in chart_map["additional_claims"])
    lines.extend(["", "## Projected Decoder", ""])
    for term, entry in chart_map["projected_glossary"].items():
        lines.append(f"- **{term}:** {entry['meaning']}")
    lines.extend(["", "## Reconstruction Limits", ""])
    lines.extend(f"- {item}" for item in chart_map["reconstruction_limits"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    report: dict[str, Any] = {"schema_version": "astrowoof.full_chart_basis_audit.v0.1", "subjects": {}}
    for subject, path in PACKETS.items():
        packet = json.loads(path.read_text(encoding="utf-8"))
        current = render_full_chart_basis(packet)
        chart_map = extract_chart_map(packet)
        compact = compact_markdown(packet, chart_map)
        (HERE / f"{subject}.current-full-chart-basis.md").write_text(current, encoding="utf-8")
        (HERE / f"{subject}.prototype-authoring-chart-map.md").write_text(compact, encoding="utf-8")
        (HERE / f"{subject}.reconstructed-chart-map.json").write_text(
            json.dumps(chart_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        types = Counter(item.get("claim_type") for item in claims(packet))
        report["subjects"][subject] = {
            "packet": str(path),
            "selected_claim_count": len(packet.get("cards", [])),
            "additional_claim_count": len(packet.get("unselected_claims", [])),
            "claim_types": dict(types),
            "registry_term_count": len(packet.get("projected_term_registry", {}).get("terms", {})),
            "reconstructed_object_count": len(chart_map["objects"]),
            "reconstructed_relationship_count": len(chart_map["relationships"]),
            "referenced_glossary_term_count": len(chart_map["projected_glossary"]),
            "current": {
                "characters": len(current), "utf8_bytes": len(current.encode("utf-8")),
                "estimated_tokens": estimate_tokens(current), "lines": len(current.splitlines()),
                "sections": section_metrics(current),
            },
            "prototype": {
                "characters": len(compact), "utf8_bytes": len(compact.encode("utf-8")),
                "estimated_tokens": estimate_tokens(compact), "lines": len(compact.splitlines()),
            },
        }
    (HERE / "audit-metrics.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
