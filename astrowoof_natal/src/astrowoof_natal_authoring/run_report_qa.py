"""Provider-free installed qualification for the deterministic run reporter."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from .cli.run_report import main as report_main
from .run_report import validate_run_evolution_report


CONTRACT = "astrowoof.sbe_run_report_qualification.v1"


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def validate_run_report_qualification(value: Any) -> dict[str, Any]:
    required = {
        "schema_version", "status", "qualification_only", "package_version",
        "assertions", "external_network_call_count", "provider_call_count",
        "workspace_access_count", "receipt_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Run-report qualification receipt shape is invalid")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    assertions = value.get("assertions")
    if (
        value.get("schema_version") != CONTRACT
        or value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or not isinstance(value.get("package_version"), str)
        or not value["package_version"]
        or not isinstance(assertions, dict)
        or not assertions
        or any(type(item) is not bool for item in assertions.values())
        or not all(assertions.values())
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "provider_call_count", "workspace_access_count",
        ))
        or value.get("receipt_sha256") != _digest(body)
    ):
        raise ValueError("Run-report qualification receipt semantics are invalid")
    return json.loads(json.dumps(value))


def read_run_report_qualification_schema() -> dict[str, Any]:
    from importlib.resources import files
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "sbe-run-report-qualification.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def _fixture() -> str:
    run = "f" * 64
    prefix = "2026-08-31T12:00:00Z ✨🐶 2026-08-31T12:00:00Z | INFO | qualification-host"
    return "\n".join([
        f"{prefix} | {run} | - | workspace | WAITING : workspace_fingerprint revision=7 snapshot_sha256={'a' * 64} sbe_release=qualification",
        f"{prefix} | {run} | - | inspect | WAITING : lifecycle_inspection_complete status=WAITING branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=1 provider_actions=1 local_dependencies=0",
        f"{prefix} | {run} | - | command | WAITING : command_exit command=provider_reconciliation_cycle exit_code=0 outcome=provider_pending",
        f"{prefix} | {run} | - | inspect | WAITING : lifecycle_inspection_complete status=WAITING branch_reason=provider_reconciliation_due capacity_disposition=continue_local_cycle eligible_now=True branch_action_count=1 provider_actions=1 local_dependencies=0",
        f"{prefix} | {run} | - | privacy | WAITING : native_decision_summary payload=QUALIFICATION_SECRET prompt=QUALIFICATION_SECRET outcome=ok",
    ]) + "\n"


def run_run_report_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "worker.log"
        first = root / "first"
        second = root / "second"
        source.write_text(_fixture(), encoding="utf-8")
        report_main(["build", "--input", str(source), "--output-dir", str(first)])
        report_main(["build", "--input", str(source), "--output-dir", str(second)])
        first_bytes = {item.name: item.read_bytes() for item in first.iterdir()}
        second_bytes = {item.name: item.read_bytes() for item in second.iterdir()}
        report = validate_run_evolution_report(json.loads(first_bytes["report.json"]))
        rendered = b"".join(first_bytes.values())
        assertions = {
            "all_formats_emitted": set(first_bytes) == {"report.json", "report.md", "report.html", "report.mmd"},
            "byte_identical_replay": first_bytes == second_bytes,
            "no_progress_detected": len(report["runs"][0]["no_progress_candidates"]) == 1,
            "privacy_sentinel_absent": b"QUALIFICATION_SECRET" not in rendered,
            "diagnostic_only": report["diagnostic_only"] is True,
        }
    body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "package_version": _version(),
        "assertions": assertions,
        "external_network_call_count": 0,
        "provider_call_count": 0,
        "workspace_access_count": 0,
    }
    return validate_run_report_qualification({**body, "receipt_sha256": _digest(body)})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = run_run_report_qualification()
    if not all(value["assertions"].values()):
        raise RuntimeError("Run-report qualification failed")
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
