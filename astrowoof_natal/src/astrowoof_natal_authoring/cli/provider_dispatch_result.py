"""Provider-free validation/export for phase-aware provider dispatch evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from ..external_authority_v2_execution import (
    read_ambiguous_provider_submission_fixture_v1,
    validate_ambiguous_provider_submission_fixture_v1,
    validate_external_authority_provider_dispatch_result_v3,
    validate_external_authority_provider_dispatch_result_v4,
    validate_external_authority_v2_command_result_v2,
    validate_external_authority_v2_command_result_v3,
)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate(value: Any) -> Any:
    if not isinstance(value, dict):
        raise ValueError("provider dispatch evidence must be an object")
    schema = value.get("schema_version")
    if schema == "astrowoof.external_authority_provider_dispatch_result.v3":
        return validate_external_authority_provider_dispatch_result_v3(value)
    if schema == "astrowoof.external_authority_provider_dispatch_result.v4":
        return validate_external_authority_provider_dispatch_result_v4(value)
    if schema == "astrowoof.external_authority_v2_command_result.v2":
        return validate_external_authority_v2_command_result_v2(value)
    if schema == "astrowoof.external_authority_v2_command_result.v3":
        return validate_external_authority_v2_command_result_v3(value)
    if schema == "astrowoof.ambiguous_provider_submission_fixtures.v1":
        return validate_ambiguous_provider_submission_fixture_v1(value)
    raise ValueError("unsupported provider dispatch evidence schema")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate or export provider-dispatch contract evidence without provider I/O.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--packaged-fixtures", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = (
        read_ambiguous_provider_submission_fixture_v1()
        if args.packaged_fixtures else _load(args.input)
    )
    validated = _validate(value)
    rendered = json.dumps(validated, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
