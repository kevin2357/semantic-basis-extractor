"""Provider-free qualification for the post-provider finalization boundary."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any
from unittest.mock import patch

from . import closure
from .contracts import authoring_profile
from .native_transitions import read_native_transition_result
from .smoke import materialize_fixture
from .terminal_review_contracts import (
    validate_terminal_review_result_v02_against_api_actions,
)


RECEIPT_SCHEMA = "astrowoof.finalization_boundary_qualification.v2"


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _installed_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def _completed_run(root: Path) -> tuple[dict[str, Any], Path]:
    input_dir = root / "input"
    run_dir = root / "run"
    materialize_fixture(input_dir)
    profile = authoring_profile(
        extraction={
            "handoff_profile": "authoring-workspace",
            "workspace_layout": "split",
            "workspace_card_limit": 50,
            "pass_count": 6,
            "split_assignment_policy": "stratified-v1",
            "full_chart_basis_format": "compact-v2",
        },
        authoring={"provider": "fake", "service_level": "interactive"},
        qa={"polish": False, "allow_lint_warnings": False},
    )
    provider = closure.FakeAuthoringProvider()
    state, run_json = closure.create_run(
        input_package=input_dir,
        run_dir=run_dir,
        subject="bre",
        provider=provider,
        max_attempts=1,
        sbe_script=None,
        python_executable=Path(sys.executable),
        service_level="interactive",
        split_assignment_policy="stratified-v1",
        full_chart_basis_format="compact-v2",
        profile=profile,
    )
    closure.author_pending_passes(
        state=state,
        provider=provider,
        run_dir=run_dir,
        max_attempts=1,
        python_executable=Path(sys.executable),
        run_json=run_json,
        max_workers=6,
    )
    state["spend_ledger"] = {
        "actions": [{
            "action_id": "paid_000000000000000000000001",
            "state": "REPORTED",
            "binding": {
                "run_id": state["run_id"],
                "profile_sha256": "1" * 64,
                "prepared_state_revision": 1,
                "stage": "authoring_initial",
                "route": "bre_1:attempt-001",
                "request_sha256": "2" * 64,
                "model": "fake-authoring",
                "service_level": "interactive",
                "maximum_output_tokens": 100,
                "commitment_micro_usd": 0,
                "price_book_version": "openai-public-2026-08-07.v1",
            },
            "authorization": {"authorization_reference": "qualification"},
            "consumption": {"consumer_id": "qualification"},
            "provider": {"kind": "response", "id": "resp_qualification"},
            "reported": {"usage": None, "estimated_micro_usd": 0},
            "reconciliation_reference_ids": [],
        }],
        "reconciliation_references": [],
    }
    closure.save_state(run_json, state)
    closure.write_workspace_snapshot(run_dir)
    return state, run_json


def _stage_completed_provider_evidence(state: dict[str, Any], run_json: Path) -> None:
    action = state["spend_ledger"]["actions"][0]
    action["state"] = "WAITING"
    action["reported"] = None
    action["consumption"] = None
    action["provider_reconciliation"] = {
        "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
        "provider_retrieval_attempt_count": 1,
        "last_attempt_at": "2026-09-02T21:28:00Z",
        "last_outcome": "completed",
        "resume_not_before": None,
    }
    closure.save_state(run_json, state)
    closure.write_workspace_snapshot(run_json.parent)


def _adopt_completed_provider_evidence(**kwargs: Any) -> bool:
    action = kwargs["state"]["spend_ledger"]["actions"][0]
    action["state"] = "REPORTED"
    action["reported"] = {"usage": None, "estimated_micro_usd": 0}
    closure.save_state(kwargs["run_json"], kwargs["state"])
    return True


def _invoke(run_dir: Path) -> tuple[int, dict[str, Any] | None]:
    output = io.StringIO()
    argv = [
        "astrowoof-semantic-closure", "--run-dir", str(run_dir), "--resume",
        "--provider", "fake", "--max-attempts", "1",
    ]
    try:
        with patch.object(sys, "argv", argv), patch(
            "sys.stdout", output,
        ), patch.object(
            closure,
            "author_pending_passes",
            side_effect=_adopt_completed_provider_evidence,
        ):
            closure.main()
    except SystemExit as exc:
        code = int(exc.code or 0)
    else:
        code = 0
    rendered = output.getvalue().strip()
    return code, json.loads(rendered) if rendered else None


def validate_finalization_boundary_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "status", "qualification_only", "provider_free",
        "package_version", "external_network_call_count",
        "real_provider_create_count", "provider_spend_usd", "success_case",
        "review_case", "operational_case", "assertions", "receipt_sha256",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("finalization-boundary qualification shape differs")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if (
        value.get("schema_version") != RECEIPT_SCHEMA
        or value.get("status") != "pass"
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or any(value.get(key) != 0 for key in (
            "external_network_call_count", "real_provider_create_count",
            "provider_spend_usd",
        ))
        or not isinstance(value.get("package_version"), str)
        or not value["package_version"]
        or value.get("success_case") != {
            "exit_code": 0, "native_status": "DELIVERY_COMPLETE",
            "theme_group_artifact_present": False,
        }
        or value.get("review_case") != {
            "exit_code": 2,
            "command_schema_version": "astrowoof.terminal_review_command_result.v0.1",
            "outcome": "review_required",
            "cause_code": "finalization_contract_invalid",
            "custody_finality": "final",
            "new_provider_create_permitted": False,
            "api_action_join_valid": True,
            "exact_replay": True,
        }
        or value.get("operational_case") != {
            "exception_class": "OSError", "native_result_published": False,
        }
        or not isinstance(value.get("assertions"), dict)
        or set(value["assertions"]) != {
            "dormant_theme_feature_absent_reaches_delivery",
            "deterministic_contradiction_seals_review",
            "invocation_identity_selects_exact_result",
            "api_action_binding_join_is_valid",
            "exact_replay_is_inert",
            "operational_failure_stays_untyped",
        }
        or any(item is not True for item in value["assertions"].values())
        or value.get("receipt_sha256") != _digest(body)
    ):
        raise ValueError("finalization-boundary qualification semantics differ")
    return json.loads(json.dumps(value))


def read_finalization_boundary_qualification_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "finalization-boundary-qualification.v2.schema.json"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def run_finalization_boundary_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-finalization-boundary-") as temporary:
        root = Path(temporary)

        success_state, success_json = _completed_run(root / "success")
        theme_group_artifact = (
            Path(success_state["passes"]["bre_6"]["accepted_workspace"])
            / "ASSIGN THEME GROUPS.md"
        )
        _stage_completed_provider_evidence(success_state, success_json)
        success_exit, _ = _invoke(success_json.parent)
        success_case = {
            "exit_code": success_exit,
            "native_status": closure.load_json(success_json)["status"],
            "theme_group_artifact_present": theme_group_artifact.exists(),
        }

        review_state, review_json = _completed_run(root / "review")
        _stage_completed_provider_evidence(review_state, review_json)
        protected = "PROTECTED-QUALIFICATION-SENTINEL"
        with patch.object(
            closure, "assemble", side_effect=closure.AssemblyContractError(protected),
        ):
            review_exit, command = _invoke(review_json.parent)
        if command is None:
            raise ValueError("finalization review command result was not emitted")
        sealed = read_native_transition_result(review_json.parent, command["result_id"])
        result = sealed["result"]
        api_actions = [{
            "native_run_id": review_state["run_id"],
            "action_id": action["action_id"],
            "binding": action["binding"],
            "route_family": "exact_natal",
            "stage": action["binding"]["stage"],
            "provider_operation_id": action["provider"]["id"],
        } for action in review_state["spend_ledger"]["actions"]]
        validate_terminal_review_result_v02_against_api_actions(result, api_actions)
        replay_exit, replay = _invoke(review_json.parent)
        exact_replay = replay_exit == 2 and replay == command
        if protected in json.dumps(command):
            raise ValueError("protected finalization detail escaped public output")
        review_case = {
            "exit_code": review_exit,
            "command_schema_version": command["schema_version"],
            "outcome": result["outcome"],
            "cause_code": result["cause_code"],
            "custody_finality": result["custody_finality"],
            "new_provider_create_permitted": result["new_provider_create_permitted"],
            "api_action_join_valid": True,
            "exact_replay": exact_replay,
        }

        _state, operational_json = _completed_run(root / "operational")
        _stage_completed_provider_evidence(_state, operational_json)
        try:
            with patch.object(closure, "assemble", side_effect=OSError("dependency unavailable")):
                _invoke(operational_json.parent)
        except OSError as exc:
            operational_class = type(exc).__name__
        else:
            operational_class = "none"
        operational_case = {
            "exception_class": operational_class,
            "native_result_published": (
                operational_json.parent / "native-execution-results.json"
            ).exists(),
        }

    assertions = {
        "dormant_theme_feature_absent_reaches_delivery": (
            success_case == {
                "exit_code": 0,
                "native_status": "DELIVERY_COMPLETE",
                "theme_group_artifact_present": False,
            }
        ),
        "deterministic_contradiction_seals_review": review_case["cause_code"] == "finalization_contract_invalid",
        "invocation_identity_selects_exact_result": command["result_id"] == result["result_id"],
        "api_action_binding_join_is_valid": review_case["api_action_join_valid"],
        "exact_replay_is_inert": exact_replay,
        "operational_failure_stays_untyped": operational_case == {"exception_class": "OSError", "native_result_published": False},
    }
    body = {
        "schema_version": RECEIPT_SCHEMA,
        "status": "pass" if all(assertions.values()) else "fail",
        "qualification_only": True,
        "provider_free": True,
        "package_version": _installed_version(),
        "external_network_call_count": 0,
        "real_provider_create_count": 0,
        "provider_spend_usd": 0,
        "success_case": success_case,
        "review_case": review_case,
        "operational_case": operational_case,
        "assertions": assertions,
    }
    return validate_finalization_boundary_qualification({
        **body, "receipt_sha256": _digest(body),
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_finalization_boundary_qualification_schema()
        if args.schema else run_finalization_boundary_qualification()
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
