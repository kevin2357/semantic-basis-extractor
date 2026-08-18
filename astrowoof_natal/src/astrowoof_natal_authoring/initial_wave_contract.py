"""Supported provider-free readers and validators for initial-wave contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .initial_wave import (
    validate_initial_wave,
    validate_initial_wave_result,
    validate_wave_authorization_document,
)
from .resource_access import read_resource_text


INITIAL_WAVE_FIXTURES = {
    "prepared": "fixtures/initial_wave/prepared-wave.v1.json",
    "authorization": "fixtures/initial_wave/wave-authorization.v1.json",
    "six-id-detach": "fixtures/initial_wave/six-id-detach.v1.json",
    "partial-ambiguity": "fixtures/initial_wave/partial-ambiguity.v1.json",
}
INITIAL_WAVE_SCHEMAS = {
    "wave": "contracts/initial-wave-contracts.v1.schema.json",
    "result": "contracts/initial-wave-result.v1.schema.json",
}


def validate_initial_wave_fixture(kind: str, value: Any) -> dict[str, Any]:
    if kind not in INITIAL_WAVE_FIXTURES or not isinstance(value, dict):
        raise ValueError("Unsupported initial-wave fixture kind")
    if kind == "prepared":
        validate_initial_wave(value)
    elif kind == "authorization":
        validate_wave_authorization_document(value)
    else:
        validate_initial_wave_result(value)
    return value


def read_initial_wave_fixture(kind: str) -> dict[str, Any]:
    """Read and strictly validate one installed consumer fixture."""
    try:
        resource = INITIAL_WAVE_FIXTURES[kind]
    except KeyError as exc:
        raise ValueError("Unsupported initial-wave fixture kind") from exc
    return validate_initial_wave_fixture(
        kind, json.loads(read_resource_text(resource))
    )


def read_initial_wave_schema(kind: str) -> dict[str, Any]:
    """Read one packaged JSON Schema by its closed public kind."""
    try:
        resource = INITIAL_WAVE_SCHEMAS[kind]
    except KeyError as exc:
        raise ValueError("Unsupported initial-wave schema kind") from exc
    value = json.loads(read_resource_text(resource))
    if not isinstance(value, dict) or value.get("$schema") != (
        "https://json-schema.org/draft/2020-12/schema"
    ):
        raise ValueError("Installed initial-wave schema is invalid")
    return value


def main() -> None:
    """Export validated installed wave evidence without provider access."""
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fixture", choices=tuple(INITIAL_WAVE_FIXTURES))
    group.add_argument("--schema", choices=tuple(INITIAL_WAVE_SCHEMAS))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    value = (
        read_initial_wave_fixture(args.fixture)
        if args.fixture else read_initial_wave_schema(args.schema)
    )
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
