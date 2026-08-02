"""Create a deterministic Round 2 keep/replace and value-level audit."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent / "round-001" / "request"
REQ = ROOT / "request"
RESP = ROOT / "response"
EVAL = ROOT / "evaluation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(value, prefix=""):
    result = {}
    if isinstance(value, dict):
        for key, child in value.items():
            result.update(flatten(child, f"{prefix}.{key}" if prefix else key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            result.update(flatten(child, f"{prefix}.{index}" if prefix else str(index)))
    else:
        result[prefix] = value
    return result


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, re.UNICODE))


def main() -> None:
    before = load(R1 / "natal.kevin.cards.normalized-baseline.json")
    after = load(RESP / "natal.kevin.cards.phase0-round002.json")
    targets = load(REQ / "editable-targets.json")
    authored = load(RESP / "editorial-decisions.json")
    before_flat, after_flat = flatten(before), flatten(after)
    changed = {
        path for path in set(before_flat) | set(after_flat)
        if before_flat.get(path) != after_flat.get(path)
    }
    decisions = {item["field_path"]: item for item in authored["decisions"]}
    records = []
    for path in sorted(targets):
        item = decisions[path]
        original = before_flat[path]
        revised = after_flat[path]
        records.append({
            **item,
            "original": original,
            "final": revised,
            "original_words": words(original),
            "final_words": words(revised),
            "word_delta": words(revised) - words(original),
            "value_changed": original != revised,
        })
    by_action = {}
    by_diagnosis = {}
    for record in records:
        action = record["action"]
        by_action[action] = by_action.get(action, 0) + 1
        for code in record["reason_codes"]:
            if code in {
                "summary_coherence", "administrative_humor_cluster",
                "repeated_opening", "overexplained_body",
                "validator_prose_advisory",
                "generic_or_administrative_headline",
                "compound_semantic_flattening",
            }:
                key = f"{code}:{action}"
                by_diagnosis[key] = by_diagnosis.get(key, 0) + 1
    audit = {
        "status": "pass" if changed <= set(targets) else "fail",
        "target_count": len(targets),
        "decision_count": len(decisions),
        "changed_value_count": len(changed),
        "unexpected_changed_paths": sorted(changed - set(targets)),
        "all_non_allowlisted_values_identical": changed <= set(targets),
        "decision_counts": by_action,
        "diagnosis_action_counts": by_diagnosis,
        "summary_decisions": {
            action: sum(
                1 for record in records
                if record["field_path"].startswith("summary.")
                and record["action"] == action
            )
            for action in ("keep", "replace")
        },
        "changes": records,
    }
    EVAL.mkdir(parents=True, exist_ok=True)
    (EVAL / "value-level-decision-audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in audit.items() if key != "changes"}, indent=2))


if __name__ == "__main__":
    main()
