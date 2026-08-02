"""Create a deterministic value-level audit for Phase 0 round 001."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROUND_ROOT = Path(__file__).resolve().parent
REQUEST_ROOT = ROUND_ROOT / "request"
RESPONSE_ROOT = ROUND_ROOT / "response"
EVALUATION_ROOT = ROUND_ROOT / "evaluation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(value, prefix=""):
    result = {}
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            result.update(flatten(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{prefix}.{index}" if prefix else str(index)
            result.update(flatten(child, path))
    else:
        result[prefix] = value
    return result


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, re.UNICODE))


def main() -> None:
    before = load(REQUEST_ROOT / "natal.kevin.cards.normalized-baseline.json")
    after = load(RESPONSE_ROOT / "natal.kevin.cards.phase0-round001.json")
    targets = load(REQUEST_ROOT / "editable-targets.json")
    diagnoses = {
        item["field_path"]: item
        for item in load(REQUEST_ROOT / "diagnosis-ledger.json")
    }
    basis = load(REQUEST_ROOT / "repair-basis.json")
    card_basis = {item["index"]: item for item in basis["cards"]}
    before_flat = flatten(before)
    after_flat = flatten(after)
    changed = {
        path for path in before_flat
        if before_flat[path] != after_flat.get(path)
    } | {path for path in after_flat if path not in before_flat}
    allowed = set(targets)
    unexpected = sorted(changed - allowed)
    unchanged_targets = sorted(allowed - changed)

    records = []
    for path in sorted(allowed):
        diagnosis = diagnoses[path]
        card_match = re.match(r"cards\.(\d+)\.", path)
        if card_match:
            evidence_consulted = card_basis.get(int(card_match.group(1)), {})
            whole_chart = False
        else:
            evidence_consulted = {
                "source": "FULL CHART BASIS.md",
                "scope": "selected and unselected whole-chart synthesis",
            }
            whole_chart = True
        original = before_flat[path]
        revised = after_flat[path]
        records.append(
            {
                "field_path": path,
                "original": original,
                "revised": revised,
                "original_words": words(original),
                "revised_words": words(revised),
                "word_delta": words(revised) - words(original),
                "reason_codes": diagnosis["reason_codes"],
                "diagnosis": diagnosis["observation"],
                "rewrite_objective": diagnosis["objective"],
                "evidence_consulted": evidence_consulted,
                "whole_chart_context_authorized": whole_chart,
                "candidate_pipeline_stage": (
                    "final_polish" if not whole_chart else "summary_authoring_or_final_polish"
                ),
            }
        )

    by_reason = {}
    for record in records:
        for reason in record["reason_codes"]:
            item = by_reason.setdefault(
                reason,
                {"field_count": 0, "original_words": 0, "revised_words": 0},
            )
            item["field_count"] += 1
            item["original_words"] += record["original_words"]
            item["revised_words"] += record["revised_words"]
    for item in by_reason.values():
        item["word_delta"] = item["revised_words"] - item["original_words"]

    audit = {
        "status": "pass" if not unexpected and not unchanged_targets else "fail",
        "allowed_path_count": len(allowed),
        "changed_path_count": len(changed),
        "unexpected_changed_paths": unexpected,
        "unchanged_target_paths": unchanged_targets,
        "all_non_allowlisted_values_identical": not unexpected,
        "all_allowlisted_values_changed": not unchanged_targets,
        "aggregate_by_reason": by_reason,
        "changes": records,
    }
    EVALUATION_ROOT.mkdir(parents=True, exist_ok=True)
    (EVALUATION_ROOT / "value-level-diff-audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in audit.items() if key != "changes"}, indent=2))


if __name__ == "__main__":
    main()
