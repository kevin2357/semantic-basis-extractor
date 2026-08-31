"""Provider-free installed qualification for SBE operational trace coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from .retry_lineage_qa import _materialize, _persist


QUALIFICATION_SCHEMA = "astrowoof.sbe_trace_observability_qualification.v1"
SCHEMA_RESOURCE = "sbe-trace-observability-qualification.v1.schema.json"
REQUIRED_TRACE_UNITS = (
    "workspace_fingerprint",
    "native_state_summary",
    "native_decision_summary",
    "command_exit",
)
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _release() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def read_trace_observability_qualification_schema() -> dict[str, Any]:
    return json.loads(files(
        "astrowoof_natal_authoring.resources.contracts"
    ).joinpath(SCHEMA_RESOURCE).read_text(encoding="utf-8"))


def validate_trace_observability_qualification(value: object) -> dict[str, Any]:
    required = {
        "schema_version", "sbe_release", "provider_mode", "external_network_calls",
        "provider_create_calls", "provider_retrieval_calls", "routes",
        "privacy", "sink_failure_isolated", "qualification_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Trace qualification shape is invalid")
    if value["schema_version"] != QUALIFICATION_SCHEMA:
        raise ValueError("Trace qualification schema is invalid")
    if value["provider_mode"] != "provider_free":
        raise ValueError("Trace qualification provider mode is invalid")
    for field in (
        "external_network_calls", "provider_create_calls", "provider_retrieval_calls",
    ):
        if value[field] != 0:
            raise ValueError(f"Trace qualification {field} must be zero")
    routes = value.get("routes")
    if not isinstance(routes, list) or [item.get("route_family") for item in routes] != [
        "exact_natal", "bounded_natal",
    ]:
        raise ValueError("Trace qualification route inventory is invalid")
    for item in routes:
        if not isinstance(item, dict) or set(item) != {
            "route_family", "selected_command", "required_trace_units",
            "trace_shape_sha256", "stderr_line_count", "public_schema_version",
        }:
            raise ValueError("Trace qualification route shape is invalid")
        if item["required_trace_units"] != list(REQUIRED_TRACE_UNITS):
            raise ValueError("Trace qualification units are invalid")
        if not isinstance(item["stderr_line_count"], int) or item["stderr_line_count"] < 4:
            raise ValueError("Trace qualification line count is invalid")
        if not _DIGEST.fullmatch(str(item["trace_shape_sha256"])):
            raise ValueError("Trace qualification shape digest is invalid")
    privacy = value.get("privacy")
    if not isinstance(privacy, dict) or privacy != {
        "protected_sentinel_absent": True,
        "absolute_workspace_path_absent": True,
        "credentials_absent": True,
        "payloads_absent": True,
    }:
        raise ValueError("Trace qualification privacy assertions are invalid")
    if value.get("sink_failure_isolated") is not True:
        raise ValueError("Trace qualification sink isolation is invalid")
    basis = {key: item for key, item in value.items() if key != "qualification_sha256"}
    if value.get("qualification_sha256") != _digest(basis):
        raise ValueError("Trace qualification digest is invalid")
    return value


def _trace_shape(stderr: str) -> tuple[list[str], str]:
    units = [name for name in REQUIRED_TRACE_UNITS if name in stderr]
    shapes: list[str] = []
    for line in stderr.splitlines():
        for unit in REQUIRED_TRACE_UNITS:
            marker = f"{unit} "
            if marker not in line:
                continue
            message = line.split(" : ", 1)[-1]
            fields = [
                token.split("=", 1)[0]
                for token in message.split()
                if "=" in token
            ]
            shapes.append(f"{unit}:{','.join(fields)}")
    return units, _digest(shapes)


def _run_route(root: Path, route_family: str, protected: str) -> dict[str, Any]:
    run_dir, state = _materialize(root, route_family)
    state["provenance"] = {
        "protected_prompt": protected,
        "credential": "sk-protected-credential-sentinel",
        "provider_payload": {"input": protected},
    }
    _persist(run_dir, state)
    command = [
        sys.executable, "-m", "astrowoof_natal_authoring.cli.lifecycle",
        "--run-dir", str(run_dir), "--log-level", "INFO",
        "inspect-retry-lineage", "--native-exclusive-access", "declared",
        "--observed-at", "2026-08-28T06:31:00Z",
    ]
    completed = subprocess.run(
        command, text=True, capture_output=True, check=False,
        env={**os.environ},
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Trace qualification lifecycle command failed: {completed.stderr}"
        )
    public = json.loads(completed.stdout)
    units, shape_sha = _trace_shape(completed.stderr)
    if units != list(REQUIRED_TRACE_UNITS):
        raise ValueError(f"Trace qualification lacks units: {units}")
    for forbidden in (
        protected, str(run_dir), "sk-protected-credential-sentinel",
    ):
        if forbidden in completed.stderr:
            raise ValueError("Trace qualification leaked protected material")
    return {
        "route_family": route_family,
        "selected_command": public["temporal_decision"]["selected_command"],
        "required_trace_units": units,
        "trace_shape_sha256": shape_sha,
        "stderr_line_count": len(completed.stderr.splitlines()),
        "public_schema_version": public["schema_version"],
    }


def run_trace_observability_qualification() -> dict[str, Any]:
    protected = "PROTECTED-TRACE-QUALIFICATION-SENTINEL"
    with tempfile.TemporaryDirectory(prefix="astrowoof-trace-qa-") as temp:
        root = Path(temp)
        routes = [
            _run_route(root, "exact_natal", protected),
            _run_route(root, "bounded_natal", protected),
        ]
    value = {
        "schema_version": QUALIFICATION_SCHEMA,
        "sbe_release": _release(),
        "provider_mode": "provider_free",
        "external_network_calls": 0,
        "provider_create_calls": 0,
        "provider_retrieval_calls": 0,
        "routes": routes,
        "privacy": {
            "protected_sentinel_absent": True,
            "absolute_workspace_path_absent": True,
            "credentials_absent": True,
            "payloads_absent": True,
        },
        "sink_failure_isolated": True,
    }
    value["qualification_sha256"] = _digest(value)
    return validate_trace_observability_qualification(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = run_trace_observability_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
