"""Provider-free public qualification for the prepared-polish v2 handoff."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
import tempfile
from typing import Any

from .closure import normalized_path, write_workspace_snapshot
from .lifecycle import inspect_lifecycle
from .temporal_lifecycle import (
    build_external_authority_request_v2,
    inspect_temporal_lifecycle,
)


RECEIPT_SCHEMA = "astrowoof.polish_authority_handoff_qualification.v1"
ACTION_ID = "paid_0123456789abcdef01234567"


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _installed_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def _state(root: Path, *, prepared: bool = True) -> dict[str, Any]:
    action = {
        "action_id": ACTION_ID, "state": "PREPARED",
        "binding": {
            "run_id": "run_polish_handoff_qualification",
            "profile_sha256": "1" * 64, "prepared_state_revision": 53,
            "stage": "polish", "route": "fixture:polish:001",
            "request_sha256": "2" * 64, "model": "gpt-5.6-luna",
            "service_level": "interactive", "maximum_output_tokens": 100000,
            "commitment_micro_usd": 1,
            "price_book_version": "openai-public-2026-08-07.v1",
        },
        "authorization": None, "provider": None, "reported": None,
        "consumption": None,
    }
    return {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "run_polish_handoff_qualification", "state_revision": 53,
        "updated_at": "2026-09-04T23:41:59Z",
        "status": (
            "AWAITING_SPEND_AUTHORIZATION" if prepared
            else "FINAL_QA_REQUIRES_REVIEW"
        ),
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(root),
        },
        "spend_ledger": {"actions": [action] if prepared else []},
        "passes": {},
        "subjects": {"fixture": {
            "subject": "fixture", "state": "FINAL_QA_WARN",
            "polish_attempts": ([{
                "attempt_number": 1, "state": "SUBMITTED",
                "paid_action_id": ACTION_ID,
            }] if prepared else []),
        }},
    }


def _inspect(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    root.mkdir(parents=True)
    (root / "run.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8",
    )
    write_workspace_snapshot(root)
    return inspect_lifecycle(
        root, native_exclusive_access="established",
        observed_at="2026-09-04T23:42:00Z",
    )


def run_polish_authority_handoff_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-polish-handoff-") as temporary:
        base = Path(temporary)
        positive_root = base / "positive"
        positive = _inspect(positive_root, _state(positive_root))
        temporal = inspect_temporal_lifecycle(
            positive_root, native_exclusive_access="established",
            observed_at="2026-09-04T23:42:00Z",
        )
        request_v2 = build_external_authority_request_v2(temporal)

        no_polish_root = base / "no-polish"
        no_polish = _inspect(
            no_polish_root, _state(no_polish_root, prepared=False),
        )

        negative_results: dict[str, bool] = {}
        mutators = {
            "mismatched_subject": lambda state: state["spend_ledger"]["actions"][0][
                "binding"
            ].update(route="other:polish:001"),
            "mismatched_action": lambda state: state["subjects"]["fixture"][
                "polish_attempts"
            ][0].update(paid_action_id="paid_ffffffffffffffffffffffff"),
            "stale_action": lambda state: state["spend_ledger"]["actions"][0].update(
                state="REPORTED", reported={"usage": {}, "estimated_micro_usd": 0},
            ),
            "unrelated_stage": lambda state: state["spend_ledger"]["actions"][0][
                "binding"
            ].update(stage="qualitative_critic"),
            "batch_service": lambda state: state["spend_ledger"]["actions"][0][
                "binding"
            ].update(service_level="batch"),
            "terminalized": lambda state: state.update(
                status="FAILED_REQUIRES_REVIEW",
                terminal_transition={
                    "outcome": "terminalized", "terminal_outcome": "review_required",
                    "resulting_status": "FAILED_REQUIRES_REVIEW",
                },
            ),
        }
        for name, mutate in mutators.items():
            root = base / name
            state = _state(root)
            mutate(state)
            inspected = _inspect(root, state)
            negative_results[name] = bool(
                inspected["execution_branch"]["command"] == "none"
                and inspected["external_authority_request"] is None
            )

    checks = {
        "exact_subject_attempt_action_binding_join": (
            positive["execution_branch"]["command"] == "await_external_authority"
        ),
        "ordinary_v2_request_exact_action": (
            request_v2["schema_version"] == "astrowoof.external_authority_request.v2"
            and request_v2["ordered_action_ids"] == [ACTION_ID]
        ),
        "warning_without_polish_is_non_dispatching": (
            no_polish["execution_branch"]["command"] == "none"
            and no_polish["external_authority_request"] is None
        ),
        "negative_identity_and_terminal_matrix": all(negative_results.values()),
    }
    body = {
        "schema_version": RECEIPT_SCHEMA,
        "status": "pass" if all(checks.values()) else "fail",
        "qualification_only": True, "provider_free": True,
        "external_network_call_count": 0, "provider_create_count": 0,
        "provider_spend_usd": 0, "sbe_version": _installed_version(),
        "positive_action_ids": request_v2["ordered_action_ids"],
        "negative_cases": sorted(negative_results), "checks": checks,
    }
    return validate_polish_authority_handoff_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def validate_polish_authority_handoff_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "receipt_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "provider_create_count",
        "provider_spend_usd", "sbe_version", "positive_action_ids",
        "negative_cases", "checks",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Polish authority qualification fields differ")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("schema_version") != RECEIPT_SCHEMA or value.get(
        "receipt_sha256"
    ) != _digest(body):
        raise ValueError("Polish authority qualification identity differs")
    if (
        value.get("status") != "pass" or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("external_network_call_count") != 0
        or value.get("provider_create_count") != 0
        or value.get("provider_spend_usd") != 0
        or value.get("positive_action_ids") != [ACTION_ID]
        or value.get("negative_cases") != [
            "batch_service", "mismatched_action", "mismatched_subject",
            "stale_action", "terminalized", "unrelated_stage",
        ]
        or not isinstance(value.get("sbe_version"), str) or not value["sbe_version"]
        or set(value.get("checks") or {}) != {
            "exact_subject_attempt_action_binding_join",
            "ordinary_v2_request_exact_action",
            "warning_without_polish_is_non_dispatching",
            "negative_identity_and_terminal_matrix",
        }
        or any(item is not True for item in value["checks"].values())
    ):
        raise ValueError("Polish authority qualification semantics differ")
    return copy.deepcopy(value)


def read_polish_authority_handoff_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "polish-authority-handoff-qualification.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_polish_authority_handoff_qualification_schema()
        if args.schema else run_polish_authority_handoff_qualification()
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
