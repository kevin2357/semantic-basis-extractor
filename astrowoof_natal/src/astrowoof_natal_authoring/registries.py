"""Merge used-term registries from semantic-projection-core artifacts.

Terms are deduplicated by registry key. A duplicate key must have an identical
definition; conflicting definitions under the same registry ID/version are an
error rather than an arbitrary last-write-wins merge.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


METADATA_FIELDS = (
    "registry_id",
    "registry_version",
    "target_ontology",
)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def merge(paths: list[Path]) -> tuple[dict[str, Any], dict[str, Any]]:
    if not paths:
        raise ValueError("At least one projected artifact is required.")

    registries = []
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        registry = document.get("projected_term_registry")
        if not isinstance(registry, dict):
            raise ValueError(f"{path} has no projected_term_registry object.")
        if not isinstance(registry.get("terms"), dict):
            raise ValueError(f"{path} registry has no terms object.")
        registries.append((path, registry))

    first_path, first = registries[0]
    for path, registry in registries[1:]:
        for field in METADATA_FIELDS:
            if registry.get(field) != first.get(field):
                raise ValueError(
                    f"Registry metadata conflict for {field}: "
                    f"{first_path}={first.get(field)!r}, {path}={registry.get(field)!r}"
                )

    merged_terms: dict[str, Any] = {}
    origins: dict[str, list[str]] = {}
    duplicate_count = 0
    for path, registry in registries:
        for term_key, definition in registry["terms"].items():
            origins.setdefault(term_key, []).append(path.name)
            if term_key in merged_terms:
                duplicate_count += 1
                if canonical(merged_terms[term_key]) != canonical(definition):
                    raise ValueError(
                        f"Conflicting definitions for term {term_key!r} in "
                        f"{origins[term_key]}"
                    )
            else:
                merged_terms[term_key] = definition

    output = {
        "registry_id": first["registry_id"],
        "registry_version": first["registry_version"],
        "target_ontology": first["target_ontology"],
        "materialization": "used_terms_subset",
        "terms": {key: merged_terms[key] for key in sorted(merged_terms)},
    }
    audit = {
        "input_files": [str(path) for path, _ in registries],
        "input_term_counts": {
            path.name: len(registry["terms"]) for path, registry in registries
        },
        "unique_term_count": len(merged_terms),
        "duplicate_occurrences_deduplicated": duplicate_count,
        "conflicts": 0,
        "terms_present_in_all_inputs": sum(
            len(files) == len(registries) for files in origins.values()
        ),
    }
    return output, audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("projected_terms_registry.json"),
    )
    args = parser.parse_args()

    registry, audit = merge(args.inputs)
    args.output.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output.resolve()),
        **audit,
    }, indent=2))


if __name__ == "__main__":
    main()
