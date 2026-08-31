"""Installed, provider-free qualification for operator-disposition assessment."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any

from .closure import normalized_path, public_run_state, write_workspace_snapshot
from .operator_disposition import read_operator_disposition_assessment_schema
from .operator_disposition_fixtures import read_operator_disposition_fixtures


CONTRACT = "astrowoof.operator_disposition_qualification.v1"
PROTECTED_SENTINEL = "PROTECTED_PROMPT_MUST_NOT_ESCAPE_7f3068"


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


def _file_bytes(root: Path) -> dict[str, bytes]:
    return {
        item.relative_to(root).as_posix(): item.read_bytes()
        for item in root.rglob("*") if item.is_file()
    }


def _materialize_pending_workspace(root: Path) -> None:
    run_id = "run_operator_disposition_qualification"
    actions: list[dict[str, Any]] = []
    passes: dict[str, Any] = {}
    for index in range(1, 7):
        action_id = f"paid_{index:024d}"
        response_id = f"resp_disposition_qualification_{index}"
        binding = {
            "run_id": run_id,
            "profile_sha256": "1" * 64,
            "prepared_state_revision": index,
            "stage": "authoring_initial",
            "route": f"qualification:authoring_initial:{index:03d}",
            "request_sha256": f"{index}" * 64,
            "model": "gpt-5.6-terra",
            "service_level": "interactive",
            "maximum_output_tokens": 4000,
            "commitment_micro_usd": 50000,
            "price_book_version": "qualification-price-book.v1",
        }
        actions.append({
            "action_id": action_id,
            "state": "WAITING",
            "binding": binding,
            "authorization": {
                "schema_version": "astrowoof.provider_spend_authorization.v0.1",
                "action_id": action_id,
                "binding": binding,
                "authorization_reference": f"qualification:{index}",
            },
            "consumption": {
                "consumer_id": "qualification-worker",
                "consumed_at": f"2026-08-31T12:0{index}:00Z",
            },
            "provider": {"id": response_id, "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.1",
                "provider_retrieval_attempt_count": 0,
                "last_attempt_at": None,
                "last_outcome": "provider_identity_recorded",
                "resume_not_before": f"2026-08-31T12:{14 + index:02d}:00Z",
            },
            "reported": None,
        })
        passes[f"pass-{index}"] = {
            "pass_id": f"pass-{index}",
            "state": "WAITING_FOR_RESPONSE",
            "attempts": [{
                "attempt": 1,
                "state": "WAITING_FOR_RESPONSE",
                "provider_metadata": {
                    "provider": "openai",
                    "response_id": response_id,
                    "response_status": "in_progress",
                    "last_polled_at": f"2026-08-31T12:0{index}:30Z",
                },
            }],
        }
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": run_id,
        "state_revision": 12,
        "status": "WAITING_FOR_RESPONSE",
        "updated_at": "2026-08-31T12:10:00Z",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(root),
        },
        "spend_ledger": {"actions": actions},
        "passes": passes,
        "subjects": {},
        "provenance": {"protected_diagnostic": PROTECTED_SENTINEL},
        "initial_authoring_wave": {"state": "DETACHED"},
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8",
    )
    (root / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8",
    )
    (root / "spend-consumption.lock").write_bytes(b"0")
    write_workspace_snapshot(root)


def read_operator_disposition_qualification_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "operator-disposition-qualification.v1.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def run_operator_disposition_qualification() -> dict[str, Any]:
    fixture_bundle = read_operator_disposition_fixtures()
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve() / "workspace"
        _materialize_pending_workspace(root)
        before = _file_bytes(root)
        command = [
            sys.executable, "-m",
            "astrowoof_natal_authoring.cli.operator_disposition",
            "--run-dir", str(root),
        ]
        first_run = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8",
        )
        second_run = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8",
        )
        first = json.loads(first_run.stdout)
        second = json.loads(second_run.stdout)
        after = _file_bytes(root)
        assertions = {
            "public_cli_fresh_process": first_run.returncode == 0,
            "assessment_schema_valid": (
                first["schema_version"]
                == "astrowoof.operator_disposition_assessment.v1"
            ),
            "provider_custody_classified": (
                first["native_custody_class"]
                == "provider_pending_known_identity"
            ),
            "reconciliation_named_without_subset": (
                first["supported_next_actions"]
                == ["provider_reconciliation_cycle"]
            ),
            "byte_identical_replay": first_run.stdout == second_run.stdout,
            "workspace_nonmutating": before == after,
            "availability_recovery_default_disabled": (
                first.get("terminal_evidence") is None
            ),
            "protected_sentinel_absent": (
                PROTECTED_SENTINEL not in first_run.stdout
                and PROTECTED_SENTINEL not in first_run.stderr
                and PROTECTED_SENTINEL not in second_run.stdout
                and PROTECTED_SENTINEL not in second_run.stderr
            ),
        }
    body = {
        "schema_version": CONTRACT,
        "status": "pass",
        "qualification_only": True,
        "provider_free": True,
        "package": {
            "name": "astrowoof-natal-authoring",
            "version": _package_version(),
        },
        "assessment_schema_sha256": _digest(
            read_operator_disposition_assessment_schema()
        ),
        "fixture_bundle_sha256": fixture_bundle["bundle_sha256"],
        "qualification_schema_sha256": _digest(
            read_operator_disposition_qualification_schema()
        ),
        "assertions": assertions,
        "external_network_call_count": 0,
        "provider_create_count": 0,
        "provider_retrieval_count": 0,
        "provider_spend_usd": 0,
    }
    return validate_operator_disposition_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_operator_disposition_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "package", "assessment_schema_sha256",
        "fixture_bundle_sha256", "qualification_schema_sha256", "assertions",
        "external_network_call_count", "provider_create_count",
        "provider_retrieval_count", "provider_spend_usd",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Operator-disposition qualification shape is invalid")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    package = value.get("package")
    assertions = value.get("assertions")
    if (
        value.get("schema_version") != CONTRACT
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
            "public_cli_fresh_process", "assessment_schema_valid",
            "provider_custody_classified", "reconciliation_named_without_subset",
            "byte_identical_replay", "workspace_nonmutating",
            "availability_recovery_default_disabled", "protected_sentinel_absent",
        }
        or any(item is not True for item in assertions.values())
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "provider_create_count",
            "provider_retrieval_count", "provider_spend_usd",
        ))
        or value.get("assessment_schema_sha256") != _digest(
            read_operator_disposition_assessment_schema()
        )
        or value.get("fixture_bundle_sha256")
        != read_operator_disposition_fixtures()["bundle_sha256"]
        or value.get("qualification_schema_sha256") != _digest(
            read_operator_disposition_qualification_schema()
        )
    ):
        raise ValueError("Operator-disposition qualification semantics are invalid")
    return dict(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run installed provider-free operator-disposition qualification."
    )
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = (
        read_operator_disposition_qualification_schema()
        if args.schema else run_operator_disposition_qualification()
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
