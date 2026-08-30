"""Installed, provider-free qualification for duplicate-submission fences."""

from __future__ import annotations

import argparse
import hashlib
import json
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any

from .duplicate_submission_fence_fixtures import (
    read_duplicate_submission_fence_fixtures,
    read_duplicate_submission_fence_fixtures_schema,
    validate_duplicate_submission_fence_fixtures,
)


QUALIFICATION_SCHEMA = "astrowoof.duplicate_submission_fence_qualification.v1"


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def read_duplicate_submission_fence_qualification_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "duplicate-submission-fence-qualification.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def run_duplicate_submission_fence_qualification() -> dict[str, Any]:
    fixture = read_duplicate_submission_fence_fixtures()
    validate_duplicate_submission_fence_fixtures(fixture)
    contradiction = fixture["local_work_progress_contradiction"]
    body = {
        "schema_version": QUALIFICATION_SCHEMA,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "package": {
            "name": "astrowoof-natal-authoring",
            "version": _package_version(),
        },
        "fixture_bundle_sha256": fixture["bundle_sha256"],
        "fixture_bundle_schema_sha256": _digest(
            read_duplicate_submission_fence_fixtures_schema()
        ),
        "qualification_schema_sha256": _digest(
            read_duplicate_submission_fence_qualification_schema()
        ),
        "assertions": {
            "generic_refusal_requires_fresh_inspection": (
                fixture["generic_provider_dispatch_refusal"]["next_step"]
                == "fresh_lifecycle_inspection"
            ),
            "generic_refusal_proves_no_provider_attempt": (
                fixture["generic_provider_dispatch_refusal"][
                    "provider_io_disposition"
                ] == "not_attempted"
            ),
            "contradiction_publication_is_sealed": bool(
                contradiction["publication_receipt"]["receipt_id"]
            ),
            "contradiction_exits_review_required": (
                contradiction["command_result"]["exit_code"] == 2
                and contradiction["command_result"]["outcome"]
                == "review_required"
            ),
            "provider_custody_is_retained": bool(
                contradiction["native_result"]["reconciliation_action_ids"]
            ),
            "new_provider_create_is_forbidden": (
                contradiction["native_result"][
                    "new_provider_create_permitted"
                ] is False
            ),
        },
        "external_network_call_count": 0,
        "provider_create_count": 0,
        "provider_retrieval_count": 0,
        "provider_spend_usd": 0,
    }
    return validate_duplicate_submission_fence_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_duplicate_submission_fence_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "fixture_bundle_sha256",
        "fixture_bundle_schema_sha256", "qualification_schema_sha256",
        "assertions", "external_network_call_count",
        "provider_create_count", "provider_retrieval_count",
        "provider_spend_usd",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Duplicate-submission qualification shape is invalid")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    assertions = value.get("assertions")
    package = value.get("package")
    if (
        value.get("schema_version") != QUALIFICATION_SCHEMA
        or value.get("receipt_sha256") != _digest(body)
        or value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or not isinstance(package, dict)
        or set(package) != {"name", "version"}
        or package.get("name") != "astrowoof-natal-authoring"
        or not isinstance(package.get("version"), str)
        or not package["version"]
        or not isinstance(assertions, dict)
        or set(assertions) != {
            "generic_refusal_requires_fresh_inspection",
            "generic_refusal_proves_no_provider_attempt",
            "contradiction_publication_is_sealed",
            "contradiction_exits_review_required",
            "provider_custody_is_retained",
            "new_provider_create_is_forbidden",
        }
        or any(item is not True for item in assertions.values())
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "provider_create_count",
            "provider_retrieval_count", "provider_spend_usd",
        ))
    ):
        raise ValueError("Duplicate-submission qualification semantics are invalid")
    fixture = read_duplicate_submission_fence_fixtures()
    if (
        value.get("fixture_bundle_sha256") != fixture["bundle_sha256"]
        or value.get("fixture_bundle_schema_sha256") != _digest(
            read_duplicate_submission_fence_fixtures_schema()
        )
        or value.get("qualification_schema_sha256") != _digest(
            read_duplicate_submission_fence_qualification_schema()
        )
    ):
        raise ValueError("Duplicate-submission qualification resource identity differs")
    return dict(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run installed provider-free duplicate-submission fence qualification.",
    )
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = (
        read_duplicate_submission_fence_qualification_schema()
        if args.schema else run_duplicate_submission_fence_qualification()
    )
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
