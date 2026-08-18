"""Supported provider-free readers and validators for initial-wave contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .initial_wave import (
    INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
    InitialWaveError,
    initial_wave_public_document,
    validate_initial_wave_binding_bundle,
    validate_initial_wave_binding_bundle_against_wave,
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
    "exact-binding-bundle": "fixtures/initial_wave/exact-binding-bundle.v1.json",
    "bounded-binding-bundle": "fixtures/initial_wave/bounded-binding-bundle.v1.json",
}
INITIAL_WAVE_SCHEMAS = {
    "wave": "contracts/initial-wave-contracts.v1.schema.json",
    "result": "contracts/initial-wave-result.v1.schema.json",
    "binding-bundle": "contracts/initial-authoring-wave-binding-bundle.v1.schema.json",
    "authority-inputs": "contracts/initial-authoring-wave-authority-inputs.v1.schema.json",
}
AUTHORITY_INPUTS_CONTRACT = "astrowoof.initial_authoring_wave_authority_inputs.v1"
_AUTHORITY_INPUTS_KEYS = frozenset({
    "schema_version", "authority_inputs_sha256", "prepared_wave", "binding_bundle",
})


def _canonical_sha256(value: Any) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def build_initial_wave_authority_inputs(
    prepared_wave: dict[str, Any], binding_bundle: dict[str, Any],
) -> dict[str, Any]:
    """Build one content-bound pair after validating both public inputs."""
    validate_initial_wave_binding_bundle_against_wave(
        binding_bundle, prepared_wave
    )
    value = {
        "schema_version": AUTHORITY_INPUTS_CONTRACT,
        "prepared_wave": json.loads(json.dumps(prepared_wave)),
        "binding_bundle": json.loads(json.dumps(binding_bundle)),
    }
    value["authority_inputs_sha256"] = _canonical_sha256(value)
    return value


def validate_initial_wave_authority_inputs(value: Any) -> dict[str, Any]:
    """Strictly validate the closed pair without filesystem access."""
    if not isinstance(value, dict) or set(value) != _AUTHORITY_INPUTS_KEYS:
        raise InitialWaveError("unsupported_contract", "Authority-input fields are not exact")
    if value.get("schema_version") != AUTHORITY_INPUTS_CONTRACT:
        raise InitialWaveError("unsupported_contract", "Unsupported authority-input contract")
    body = {key: item for key, item in value.items()
            if key != "authority_inputs_sha256"}
    if value.get("authority_inputs_sha256") != _canonical_sha256(body):
        raise InitialWaveError("digest_mismatch", "Authority-input digest is invalid")
    prepared = value.get("prepared_wave")
    bundle = value.get("binding_bundle")
    if not isinstance(prepared, dict) or not isinstance(bundle, dict):
        raise InitialWaveError("unsupported_contract", "Authority-input documents are invalid")
    validate_initial_wave_binding_bundle_against_wave(bundle, prepared)
    return value


def read_initial_wave_authority_inputs(run_dir: Path | str) -> dict[str, Any]:
    """Return both public inputs only after complete snapshot and join validation."""
    from .closure import load_json, validate_workspace_snapshot

    root = Path(run_dir).resolve()
    run_json = root / "run.json"
    bundle_path = root / INITIAL_WAVE_BINDING_BUNDLE_FILENAME
    if not run_json.is_file():
        raise InitialWaveError("snapshot_invalid", "Run state is missing")
    state = load_json(run_json)
    try:
        validate_workspace_snapshot(root, state)
    except ValueError as exc:
        raise InitialWaveError("snapshot_invalid", str(exc)) from exc
    if not bundle_path.is_file():
        raise InitialWaveError("binding_bundle_missing", "Binding bundle is missing")
    prepared = initial_wave_public_document(
        state.get("initial_authoring_wave") or {}
    )
    bundle = load_json(bundle_path)
    if not isinstance(bundle, dict):
        raise InitialWaveError("unsupported_contract", "Binding bundle is not an object")
    return build_initial_wave_authority_inputs(prepared, bundle)


def validate_initial_wave_fixture(kind: str, value: Any) -> dict[str, Any]:
    if kind not in INITIAL_WAVE_FIXTURES or not isinstance(value, dict):
        raise ValueError("Unsupported initial-wave fixture kind")
    if kind == "prepared":
        validate_initial_wave(value)
    elif kind == "authorization":
        validate_wave_authorization_document(value)
    elif kind in {"exact-binding-bundle", "bounded-binding-bundle"}:
        validate_initial_wave_binding_bundle(value)
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
    group.add_argument("--initial-wave-inputs", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.initial_wave_inputs:
        if args.run_dir is None:
            parser.error("--initial-wave-inputs requires --run-dir")
        value = read_initial_wave_authority_inputs(args.run_dir)
    else:
        if args.run_dir is not None:
            parser.error("--run-dir is valid only with --initial-wave-inputs")
        value = (
            read_initial_wave_fixture(args.fixture)
            if args.fixture else read_initial_wave_schema(args.schema)
        )
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.run_dir is not None:
            run_root = args.run_dir.resolve()
            output = args.output.resolve()
            if output == run_root or run_root in output.parents:
                raise InitialWaveError(
                    "unsafe_output_path", "Output must be outside the run directory"
                )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
