"""Build Round 2 model-visible artifacts without making a network request."""

from __future__ import annotations

import json
import hashlib
import re
import statistics
from pathlib import Path


ROUND_ROOT = Path(__file__).resolve().parent
REQUEST_ROOT = ROUND_ROOT / "request"
SPRINT_ROOT = ROUND_ROOT.parents[1]
ROUND1_REQUEST = SPRINT_ROOT / "work" / "round-001" / "request"
REPO_ROOT = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "astrowoof_natal" / "src").is_dir()
)
PACKET_PATH = (
    REPO_ROOT / "astrowoof_natal" / "qa" / "reference_decks" / "kevin"
    / "selected-authoring-packet.json"
)

DOC_ORDER = [
    "START HERE.md",
    "AstroWoof Editorial Polish Handbook.md",
    "DOG DETAILS.md",
    "ASTROWOOF CARD AND FIELD REQUIREMENTS.md",
    "WHOLE DOG ORIENTATION.md",
    "FULL CHART BASIS.md",
    "CURRENT DECK LENGTH PROFILE.md",
    "TARGETED POLISH EXECUTION CONTRACT.md",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, re.UNICODE))


def field_group(path: str) -> str:
    parts = path.split(".")
    scope = "summary" if parts[0] == "summary" else "claim card"
    if "headline" in parts:
        index = parts.index("headline")
        return f"{scope} / {parts[index - 1]} / headline / {parts[index + 1]}"
    if "body" in parts:
        index = parts.index("body")
        return f"{scope} / {parts[index - 1]} / body / {parts[index + 1]}"
    if "dos" in parts:
        return f"{scope} / do"
    if "donts" in parts:
        return f"{scope} / don't"
    if "funny_dog_quotes" in parts:
        return f"{scope} / funny dog quote"
    if "imperative_dog_quotes" in parts:
        return f"{scope} / imperative dog quote"
    return f"{scope} / canine joke"


def length_profile(targets: dict[str, str]) -> str:
    grouped: dict[str, list[int]] = {}
    for path, text in targets.items():
        grouped.setdefault(field_group(path), []).append(words(text))
    rows = []
    for name in sorted(grouped):
        values = grouped[name]
        rows.append(
            f"| {name} | {len(values)} | {min(values)} | "
            f"{statistics.median(values):g} | {max(values)} |"
        )
    return """# Current Deck Length Profile

These measurements describe the existing candidate fields. They are not quotas
or generic style limits. Existing scale and richness are presumptively
intentional.

For a `replace` decision, remain near the current field's own scale unless its
diagnosis specifically identifies over-explanation or additional space is
needed to restore a missing semantic contribution. Never shorten a summary
merely because a briefer paraphrase is possible.

| Field group | Fields | Minimum words | Median words | Maximum words |
|---|---:|---:|---:|---:|
""" + "\n".join(rows) + "\n"


def rich_basis(packet: dict, baseline: dict, target_paths: list[str]) -> dict:
    indexes = sorted({
        int(path.split(".")[1])
        for path in target_paths
        if path.startswith("cards.")
    })
    packet_cards = {
        card.get("claim_id"): card for card in packet.get("cards", [])
    }
    claim_catalog = {}
    for claim in [*packet.get("cards", []), *packet.get("unselected_claims", [])]:
        claim_id = claim.get("claim_id")
        if claim_id:
            claim_catalog[claim_id] = {
                "claim_id": claim_id,
                "claim_type": claim.get("claim_type"),
                "canonical_claim": claim.get("canonical_claim"),
                "categories": claim.get("categories", []),
                "behavioral_domains": claim.get("behavioral_domains", []),
                "tags": claim.get("tags", []),
            }
    results = []
    for index in indexes:
        claim_id = baseline["cards"][index]["claim_id"]
        source = packet_cards.get(claim_id, baseline["cards"][index])
        neighbor_ids = set()
        relations = source.get("relations") or {}
        for value in relations.values():
            if isinstance(value, list):
                neighbor_ids.update(item for item in value if isinstance(item, str))
        for evidence in source.get("evidence", []):
            neighbor_ids.update(
                item for item in evidence.get("claim_ids", [])
                if isinstance(item, str)
            )
        results.append({
            "card_index": index,
            "priority_id": source.get("priority_id"),
            "claim_id": claim_id,
            "claim_type": source.get("claim_type"),
            "canonical_claim": source.get("canonical_claim"),
            "categories": source.get("categories", []),
            "behavioral_domains": source.get("behavioral_domains", []),
            "tags": source.get("tags", []),
            "importance": source.get("importance"),
            "confidence": source.get("confidence"),
            "strength": source.get("strength"),
            "selection": source.get("selection", {}),
            "evidence": source.get("evidence", []),
            "relations": relations,
            "semantic_neighbors": [
                claim_catalog[item]
                for item in sorted(neighbor_ids)
                if item in claim_catalog
            ],
        })
    return {
        "subject": packet.get("subject", {}),
        "ordinary_card_evidence_boundary": (
            "Only the corresponding record below and its projected-term "
            "references may support a claim-card replacement."
        ),
        "cards": results,
    }


def response_schema(paths: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "decisions": {
                "type": "array",
                "minItems": len(paths),
                "maxItems": len(paths),
                "items": {
                    "type": "object",
                    "properties": {
                        "field_path": {"type": "string", "enum": paths},
                        "action": {"type": "string", "enum": ["keep", "replace"]},
                        "replacement": {"type": "string"},
                        "reason_codes": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "editorial_rationale": {"type": "string"},
                    },
                    "required": [
                        "field_path", "action", "replacement",
                        "reason_codes", "editorial_rationale",
                    ],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["decisions"],
        "additionalProperties": False,
    }


def main() -> None:
    baseline = load(ROUND1_REQUEST / "natal.kevin.cards.normalized-baseline.json")
    targets = load(ROUND1_REQUEST / "editable-targets.json")
    diagnoses = load(ROUND1_REQUEST / "diagnosis-ledger.json")
    context = load(ROUND1_REQUEST / "read-only-context.json")
    packet = load(PACKET_PATH)
    paths = sorted(targets)

    # These are identical source artifacts, copied into the independent Round 2
    # request so its exact model-visible input remains self-contained.
    for name in ("DOG DETAILS.md", "FULL CHART BASIS.md"):
        (REQUEST_ROOT / name).write_text(
            (ROUND1_REQUEST / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (REQUEST_ROOT / "CURRENT DECK LENGTH PROFILE.md").write_text(
        length_profile(targets), encoding="utf-8"
    )
    for obsolete_name in (
        "ASTROWOOF PRODUCT AND EDITORIAL GUIDE.md",
        "POLISH DECISION PROTOCOL.md",
    ):
        obsolete = REQUEST_ROOT / obsolete_name
        if obsolete.exists():
            obsolete.unlink()
    basis = rich_basis(packet, baseline, paths)
    write_json(REQUEST_ROOT / "editable-targets.json", targets)
    write_json(REQUEST_ROOT / "diagnosis-ledger.json", diagnoses)
    write_json(REQUEST_ROOT / "read-only-context.json", context)
    write_json(REQUEST_ROOT / "rich-claim-evidence.json", basis)
    schema = response_schema(paths)
    write_json(REQUEST_ROOT / "response-schema.json", schema)

    system = (
        "You are performing a targeted AstroWoof editorial polish pass. "
        "The Editorial Polish Handbook defines enduring editorial judgment; "
        "the Targeted Polish Execution Contract defines this run. Read the "
        "materials in the order specified by START HERE before inspecting "
        "candidate fields. Preserve all locked data and return only strict "
        "JSON matching the response schema."
    )
    user = (
        "Begin with START HERE and read every supplied document in its stated "
        "order. Form the private whole-dog orientation before evaluating any "
        "candidate. Then follow the execution contract and return exactly one "
        "keep-or-replace decision for every allowlisted field. Use whole-chart "
        "evidence only for summaries and corresponding rich claim evidence "
        "for ordinary cards."
    )
    (REQUEST_ROOT / "SYSTEM_PROMPT.txt").write_text(system + "\n", encoding="utf-8")
    (REQUEST_ROOT / "USER_PROMPT.txt").write_text(user + "\n", encoding="utf-8")

    rendered = [user]
    for name in DOC_ORDER:
        rendered.append(
            f"\n\n===== {name} =====\n"
            + (REQUEST_ROOT / name).read_text(encoding="utf-8")
        )
    rendered.extend([
        "\n\n===== EDITABLE CANDIDATE FIELDS =====\n"
        + json.dumps(targets, ensure_ascii=False, indent=2),
        "\n\n===== FIELD DIAGNOSES =====\n"
        + json.dumps(diagnoses, ensure_ascii=False, indent=2),
        "\n\n===== RICH CLAIM EVIDENCE AND SEMANTIC NEIGHBORS =====\n"
        + json.dumps(basis, ensure_ascii=False, indent=2),
        "\n\n===== READ-ONLY DECK CONTEXT =====\n"
        + json.dumps(context, ensure_ascii=False, indent=2),
    ])
    rendered_user = "".join(rendered)
    (REQUEST_ROOT / "OPENAI_USER_MESSAGE.txt").write_text(
        rendered_user, encoding="utf-8"
    )
    handbook_bytes = (
        REQUEST_ROOT / "AstroWoof Editorial Polish Handbook.md"
    ).read_bytes()
    manifest = {
        "experiment": "20260802-sprint1 phase-0 round-002",
        "hypothesis": (
            "Information parity, explicit preservation, length context, and "
            "keep-or-replace decisions improve local repair without sanding "
            "down existing literary peaks."
        ),
        "baseline_identical_to_round_001": True,
        "target_pool_identical_to_round_001": True,
        "target_count": len(paths),
        "gold_examples_supplied": False,
        "prior_manual_kevin_prose_supplied": False,
        "api_submission_performed": False,
        "planned_api": {
            "model": "gpt-5.6-terra",
            "reasoning_effort": "medium",
            "background": True,
            "prompt_cache_mode": "disabled",
        },
        "editorial_handbook": {
            "version": "1.0-round2",
            "sha256": hashlib.sha256(handbook_bytes).hexdigest(),
        },
        "model_visible_documents": DOC_ORDER,
        "system_prompt_chars": len(system),
        "rendered_user_chars": len(rendered_user),
    }
    write_json(REQUEST_ROOT / "request-manifest.json", manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
