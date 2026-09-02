"""Provider-free installed qualification for theme-group advisory policy."""

from __future__ import annotations

import argparse
import hashlib
import json
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from .pass_acceptance import apply_theme_group_policy


CONTRACT = "astrowoof.theme_group_policy_qualification.v1"


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def _base() -> dict[str, Any]:
    return {
        "status": "accept",
        "rejection_reasons": [],
        "advisory_reasons": [],
    }


def _issue(code: str) -> dict[str, Any]:
    return {
        "code": code,
        "message": f"Sanitized qualification finding: {code}",
        "claim_ids": ["fixture-claim"],
    }


def validate_theme_group_policy_qualification(value: Any) -> dict[str, Any]:
    required = {
        "schema_version", "status", "qualification_only", "package_version",
        "assertions", "external_network_call_count", "provider_call_count",
        "workspace_access_count", "receipt_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Theme-group policy qualification shape is invalid")
    assertions = value.get("assertions")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if (
        value.get("schema_version") != CONTRACT
        or value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or not isinstance(value.get("package_version"), str)
        or not value["package_version"]
        or not isinstance(assertions, dict)
        or set(assertions) != {
            "advisory_only_accepts", "all_advisory_codes_retained",
            "structural_assignment_rejects", "mixed_findings_reject",
            "unknown_code_fails_closed", "advisory_evidence_retained_on_reject",
        }
        or any(item is not True for item in assertions.values())
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "provider_call_count",
            "workspace_access_count",
        ))
        or value.get("receipt_sha256") != _digest(body)
    ):
        raise ValueError("Theme-group policy qualification semantics are invalid")
    return json.loads(json.dumps(value))


def read_theme_group_policy_qualification_schema() -> dict[str, Any]:
    from importlib.resources import files

    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "theme-group-policy-qualification.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def run_theme_group_policy_qualification() -> dict[str, Any]:
    advisory_codes = (
        "theme_group_coverage", "theme_group_balance",
        "cross_section_theme_mirroring",
    )
    advisory = apply_theme_group_policy(
        _base(), [_issue(code) for code in advisory_codes],
    )
    structural = apply_theme_group_policy(
        _base(), [_issue("theme_group_assignment")],
    )
    mixed = apply_theme_group_policy(
        _base(), [_issue("theme_group_coverage"), _issue("theme_group_registry")],
    )
    unknown = apply_theme_group_policy(
        _base(), [_issue("theme_group_future_unknown")],
    )
    assertions = {
        "advisory_only_accepts": advisory["status"] == "accept",
        "all_advisory_codes_retained": [
            item["code"] for item in advisory["advisory_reasons"]
        ] == list(advisory_codes),
        "structural_assignment_rejects": structural["status"] == "reject",
        "mixed_findings_reject": mixed["status"] == "reject",
        "unknown_code_fails_closed": unknown["status"] == "reject",
        "advisory_evidence_retained_on_reject": [
            item["code"] for item in mixed["advisory_reasons"]
        ] == ["theme_group_coverage"],
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
    return validate_theme_group_policy_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = run_theme_group_policy_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
