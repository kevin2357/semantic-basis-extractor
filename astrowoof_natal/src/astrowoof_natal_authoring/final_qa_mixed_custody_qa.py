"""Installed-wheel, provider-free final-QA mixed-custody qualification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
import tempfile
from typing import Any
from unittest.mock import patch

from .cli import external_authority_v2 as authority_cli
from .closure import load_json, persist_state, write_workspace_snapshot
from .external_authority_v2_qa import (
    _ordinary_authority,
    _pending_workspace,
    _reconcile_4_plus_2,
)
from .external_authority_v2_execution import (
    commit_external_authority_v2_dispatch_intent,
    validate_external_authority_v2_command_result_v3,
)
from .lifecycle import inspect_lifecycle
from .temporal_lifecycle import inspect_temporal_lifecycle
from .terminal_review_qa import (
    run_terminal_review_qualification,
    validate_terminal_review_qualification,
)


RECEIPT_SCHEMA = "astrowoof.final_qa_mixed_custody_qualification.v1"
_ASSERTIONS = {
    "provider_custody_outranks_final_qa_review",
    "provider_custody_selects_reconciliation",
    "post_intent_contradiction_refuses_before_provider_io",
    "refused_grant_history_is_immutable",
    "no_custody_review_terminal_remains_valid",
    "terminal_result_receipt_join_is_valid",
}


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


def _warning_authority(root: Path):
    _pending_workspace(root, "exact_natal")
    _reconcile_4_plus_2(root)
    state = load_json(root / "run.json")
    state["subjects"] = {
        "qualification-subject": {
            "subject": "qualification-subject",
            "state": "FINAL_QA_WARN",
            "polish_attempts": [{
                "attempt_number": 1,
                "state": "SUBMITTED",
                "provider_metadata": None,
                "accepted": False,
            }],
            "delivery": None,
        },
    }
    state["status"] = "FINAL_QA_REQUIRES_REVIEW"
    persist_state(root / "run.json", state)
    write_workspace_snapshot(root)
    return _ordinary_authority(root, "exact_natal", "polish")


def _write_inputs(root: Path, inspection: dict[str, Any], request: dict[str, Any], documents: list[dict[str, Any]], grant: dict[str, Any]) -> tuple[list[str], Path]:
    inputs = root.parent / f"{root.name}-inputs"
    inputs.mkdir()
    paths: dict[str, Path] = {}
    for name, value in {"inspection": inspection, "request": request, "grant": grant}.items():
        paths[name] = inputs / f"{name}.json"
        paths[name].write_text(json.dumps(value), encoding="utf-8")
    output = inputs / "result.json"
    argv = ["--run-dir", str(root), "--inspection", str(paths["inspection"]), "--request", str(paths["request"]), "--grant", str(paths["grant"]), "--provider", "openai", "--output", str(output), "--log-level", "CRITICAL"]
    for index, document in enumerate(documents):
        path = inputs / f"authorization-{index}.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        argv.extend(["--authorization", str(path)])
    return argv, output


def _pending_case(root: Path) -> dict[str, Any]:
    inspection, request, documents, grant = _warning_authority(root)
    argv, output = _write_inputs(root, inspection, request, documents, grant)
    creates: list[str] = []
    with patch.dict(os.environ, {"OPENAI_API_KEY": "qualification-only"}), patch.object(authority_cli, "resolve_external_authority_v2_request_payload", return_value={"model": "scripted", "input": []}), patch.object(authority_cli.OpenAIResponsesProvider, "create_response_only", side_effect=lambda *_args, **_kwargs: (creates.append("POST") or ({"id": "resp_final_qa_mixed_custody", "status": "queued"}, 1))):
        exit_code = authority_cli.main(argv)
    command = json.loads(output.read_text(encoding="utf-8"))
    state = load_json(root / "run.json")
    lifecycle = inspect_lifecycle(root, native_exclusive_access="declared")
    temporal = inspect_temporal_lifecycle(root, native_exclusive_access="declared", observed_at="2099-01-01T00:00:00Z")
    return {
        "exit_code": exit_code,
        "command_schema_version": command["schema_version"],
        "outcome": command["outcome"],
        "outer_status": state["status"],
        "terminal": lifecycle["terminal"]["terminal"],
        "provider_continuation_remains": lifecycle["terminal"]["provider_continuation_remains"],
        "selected_command": temporal["temporal_decision"]["selected_command"],
        "scripted_provider_create_count": len(creates),
    }


def _refusal_case(root: Path) -> dict[str, Any]:
    inspection, request, documents, grant = _warning_authority(root)
    argv, output = _write_inputs(root, inspection, request, documents, grant)
    original_commit = commit_external_authority_v2_dispatch_intent

    def commit_then_contradict(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original_commit(*args, **kwargs)
        state = load_json(root / "run.json")
        state["status"] = "FINAL_QA_REQUIRES_REVIEW"
        (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        write_workspace_snapshot(root)
        return result

    creates: list[str] = []
    with patch.dict(os.environ, {"OPENAI_API_KEY": "qualification-only"}), patch.object(authority_cli, "commit_external_authority_v2_dispatch_intent", side_effect=commit_then_contradict), patch.object(authority_cli, "resolve_external_authority_v2_request_payload", side_effect=AssertionError("pre-provider refusal reached payload resolution")), patch.object(authority_cli.OpenAIResponsesProvider, "create_response_only", side_effect=lambda *_args, **_kwargs: creates.append("POST")):
        exit_code = authority_cli.main(argv)
    command = json.loads(output.read_text(encoding="utf-8"))
    validate_external_authority_v2_command_result_v3(command)
    state = load_json(root / "run.json")
    history = state["external_authority_v2_dispatch_history"][-1]
    return {
        "exit_code": exit_code,
        "command_schema_version": command["schema_version"],
        "dispatch_schema_version": command["dispatch_result"]["schema_version"],
        "outcome": command["outcome"],
        "reason_code": command["dispatch_result"]["reason_code"],
        "provider_io_disposition": command["dispatch_result"]["provider_io_disposition"],
        "scripted_provider_create_count": len(creates),
        "history_reason_code": history["reason_code"],
        "fresh_authority_required": state["spend_ledger"]["actions"][-1]["state"] == "PREPARED",
    }


def validate_final_qa_mixed_custody_qualification(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "receipt_sha256", "status", "qualification_only", "provider_free", "external_network_call_count", "real_provider_create_count", "provider_spend_usd", "sbe_version", "pending_case", "refusal_case", "terminal_case", "assertions"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema_version") != RECEIPT_SCHEMA:
        raise ValueError("final-QA mixed-custody qualification fields differ")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("final-QA mixed-custody qualification digest differs")
    if value.get("status") != "pass" or value.get("qualification_only") is not True or value.get("provider_free") is not True or value.get("external_network_call_count") != 0 or value.get("real_provider_create_count") != 0 or value.get("provider_spend_usd") != 0 or not isinstance(value.get("sbe_version"), str) or not value["sbe_version"]:
        raise ValueError("final-QA mixed-custody safety declaration differs")
    if value.get("pending_case") != {"exit_code": 0, "command_schema_version": "astrowoof.external_authority_v2_command_result.v2", "outcome": "detached_provider_pending", "outer_status": "WAITING_FOR_RESPONSE", "terminal": False, "provider_continuation_remains": True, "selected_command": "provider_reconciliation_cycle", "scripted_provider_create_count": 1}:
        raise ValueError("final-QA mixed-custody pending case differs")
    if value.get("refusal_case") != {"exit_code": 3, "command_schema_version": "astrowoof.external_authority_v2_command_result.v3", "dispatch_schema_version": "astrowoof.external_authority_provider_dispatch_result.v4", "outcome": "pre_provider_refusal", "reason_code": "post_intent_lifecycle_contradiction", "provider_io_disposition": "not_attempted", "scripted_provider_create_count": 0, "history_reason_code": "post_intent_lifecycle_contradiction", "fresh_authority_required": True}:
        raise ValueError("final-QA mixed-custody refusal case differs")
    terminal = value.get("terminal_case")
    if not isinstance(terminal, dict) or set(terminal) != {"schema_version", "receipt_sha256", "public_result_v02", "review_receipt_valid", "provider_post_count"} or terminal["schema_version"] != "astrowoof.terminal_review_qualification.v1" or not isinstance(terminal["receipt_sha256"], str) or len(terminal["receipt_sha256"]) != 64 or terminal["public_result_v02"] != "astrowoof.native_execution_result.v0.2" or terminal["review_receipt_valid"] is not True or terminal["provider_post_count"] != 0:
        raise ValueError("final-QA mixed-custody terminal case differs")
    assertions = value.get("assertions")
    if not isinstance(assertions, dict) or set(assertions) != _ASSERTIONS or any(item is not True for item in assertions.values()):
        raise ValueError("final-QA mixed-custody assertions differ")
    return copy.deepcopy(value)


def read_final_qa_mixed_custody_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath("final-qa-mixed-custody-qualification.v1.schema.json")
    return json.loads(path.read_text(encoding="utf-8"))


def run_final_qa_mixed_custody_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-final-qa-mixed-custody-") as temporary:
        root = Path(temporary)
        pending = _pending_case(root / "pending")
        refusal = _refusal_case(root / "refusal")
        terminal_receipt = run_terminal_review_qualification()
        validate_terminal_review_qualification(terminal_receipt)
    terminal = {"schema_version": terminal_receipt["schema_version"], "receipt_sha256": terminal_receipt["receipt_sha256"], "public_result_v02": terminal_receipt["checks"]["public_result_v02"], "review_receipt_valid": terminal_receipt["checks"]["review_receipt_valid"], "provider_post_count": terminal_receipt["checks"]["provider_post_count"]}
    assertions = {
        "provider_custody_outranks_final_qa_review": pending["outer_status"] == "WAITING_FOR_RESPONSE" and pending["terminal"] is False,
        "provider_custody_selects_reconciliation": pending["selected_command"] == "provider_reconciliation_cycle",
        "post_intent_contradiction_refuses_before_provider_io": refusal["provider_io_disposition"] == "not_attempted" and refusal["scripted_provider_create_count"] == 0,
        "refused_grant_history_is_immutable": refusal["history_reason_code"] == "post_intent_lifecycle_contradiction" and refusal["fresh_authority_required"] is True,
        "no_custody_review_terminal_remains_valid": terminal["public_result_v02"] == "astrowoof.native_execution_result.v0.2",
        "terminal_result_receipt_join_is_valid": terminal["review_receipt_valid"] is True and terminal["provider_post_count"] == 0,
    }
    body = {"schema_version": RECEIPT_SCHEMA, "status": "pass" if all(assertions.values()) else "fail", "qualification_only": True, "provider_free": True, "external_network_call_count": 0, "real_provider_create_count": 0, "provider_spend_usd": 0, "sbe_version": _installed_version(), "pending_case": pending, "refusal_case": refusal, "terminal_case": terminal, "assertions": assertions}
    return validate_final_qa_mixed_custody_qualification({**body, "receipt_sha256": _digest(body)})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = read_final_qa_mixed_custody_qualification_schema() if args.schema else run_final_qa_mixed_custody_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
