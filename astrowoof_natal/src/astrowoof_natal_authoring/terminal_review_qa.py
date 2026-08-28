"""Provider-free installed qualification for terminal-review custody handoff."""

from __future__ import annotations

import argparse
import copy
import io
import json
import os
import sys
import tempfile
import tomllib
from contextlib import redirect_stdout
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any
from unittest.mock import patch

from . import closure
from .closure import normalized_path, public_run_state, write_workspace_snapshot
from .lifecycle import closeout_run, deny_providerless_action, inspect_lifecycle
from .lifecycle_contracts import NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA
from .native_transitions import (
    publish_native_execution_result,
    read_native_transition_result,
    validate_native_publication_receipt,
)
from .terminal_review_contracts import (
    validate_terminal_review_command_result_against_publication,
    validate_terminal_review_result_v02,
)


CONTRACT = "astrowoof.terminal_review_qualification.v1"
SCHEMA_RESOURCE = "terminal-review-qualification.v1.schema.json"
SENTINEL = "PROTECTED_TERMINAL_REVIEW_QUALIFICATION_SENTINEL"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _binding(run_id: str, stage: str, route: str, revision: int) -> dict[str, Any]:
    return {
        "run_id": run_id, "profile_sha256": "a" * 64,
        "prepared_state_revision": revision, "stage": stage, "route": route,
        "request_sha256": "b" * 64, "model": "scripted-provider",
        "service_level": "interactive", "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def _materialize(root: Path) -> tuple[Path, str, str, str]:
    run_dir = root / "run"
    run_dir.mkdir()
    run_id = "terminal-review-qualification"
    actions = [{
        "action_id": f"paid_{number:024x}", "state": "REPORTED",
        "binding": _binding(run_id, "authoring_initial", f"pass-{number}:attempt-001", 1),
        "provider": {"id": f"resp_terminal_initial_{number}", "kind": "response"},
        "reported": {"estimated_micro_usd": 0},
    } for number in range(1, 7)]
    reported_id = "paid_000000000000000000000101"
    provider_id = "paid_000000000000000000000102"
    providerless_id = "paid_000000000000000000000103"
    actions.extend((
        {
            "action_id": reported_id, "state": "WAITING",
            "binding": _binding(run_id, "creative_retry", "pass-1:attempt-002", 7),
            "provider": {"id": "resp_terminal_reported", "kind": "response"},
            "provider_reconciliation": {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 1,
                "last_attempt_at": "2026-08-28T09:00:00Z",
                "last_outcome": "completed", "resume_not_before": None,
            }, "reported": None,
        },
        {
            "action_id": provider_id, "state": "REPORTED",
            "binding": _binding(run_id, "authoring_initial", "pass-1:attempt-001", 1),
            "provider": {"id": "resp_terminal_pending", "kind": "response"},
            "reported": {"estimated_micro_usd": 0},
        },
        {
            "action_id": providerless_id, "state": "PREPARED",
            "binding": _binding(run_id, "creative_retry", "pass-1:attempt-003", 8),
        },
    ))
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": run_id, "state_revision": 8,
        "created_at": "2026-08-28T08:00:00Z",
        "updated_at": "2026-08-28T08:00:00Z",
        "provider": "fake", "provider_configuration": {}, "max_attempts": 3,
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "policy": {
                "currency": "USD", "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 100000000,
                "stage_ceilings_micro_usd": {
                    stage: 100000000 for stage in (
                        "authoring_initial", "creative_retry", "polish",
                        "qualitative_critic", "qualitative_candidate",
                    )
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip", "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            }, "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {"pass-1": {
            "pass_id": "pass-1", "state": "AWAITING_SPEND_AUTHORIZATION",
            "attempts": [
                {"attempt_number": 1, "state": "PASS_QA_REJECTED"},
                {"attempt_number": 2, "state": "WAITING_FOR_RESPONSE"},
                {"attempt_number": 3, "state": "AWAITING_SPEND_AUTHORIZATION"},
            ],
        }},
        "subjects": {}, "provenance": {"protected_payload": SENTINEL},
    }
    (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)
    return run_dir, reported_id, provider_id, providerless_id


def _invoke(argv: list[str]) -> tuple[int, list[dict[str, Any]]]:
    stream = io.StringIO()
    with patch.object(sys, "argv", argv), redirect_stdout(stream):
        try:
            closure.main()
        except SystemExit as exc:
            code = int(exc.code)
        else:
            code = 0
    envelopes: list[dict[str, Any]] = []
    for line in stream.getvalue().splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            envelopes.append(value)
    return code, envelopes


def _installed_version() -> str:
    module_path = Path(__file__).resolve()
    if not any(part.lower() == "site-packages" for part in module_path.parts):
        for parent in module_path.parents:
            project = parent / "pyproject.toml"
            if project.is_file():
                value = tomllib.loads(project.read_text(encoding="utf-8"))
                return str(value["project"]["version"])
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def run_terminal_review_qualification() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-terminal-review-qa-") as temporary:
        run_dir, reported_id, provider_id, providerless_id = _materialize(Path(temporary))
        historical = publish_native_execution_result(
            run_dir, command_kind="provider_reconciliation", sbe_release=_installed_version(),
            published_at="2026-08-28T08:00:01Z",
        )

        def review(**kwargs: Any) -> None:
            state = kwargs["state"]
            reported = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == reported_id)
            reported["state"] = "REPORTED"
            reported["reported"] = {"estimated_micro_usd": 0}
            pending = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == provider_id)
            pending["state"] = "WAITING"
            pending["reported"] = None
            pending["provider_reconciliation"] = {
                "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                "provider_retrieval_attempt_count": 0, "last_attempt_at": None,
                "last_outcome": None, "resume_not_before": "2099-08-28T09:00:00Z",
            }
            unused = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == providerless_id)
            unused["state"] = "AUTHORIZED"
            unused["authorization"] = {"document_sha256": "c" * 64}
            state["status"] = "FAILED_REQUIRES_REVIEW"
            next(iter(state["passes"].values()))["state"] = "FAILED_REQUIRES_REVIEW"
            closure.save_state(kwargs["run_json"], state)
            from .spend import AwaitingSpendAuthorization
            raise AwaitingSpendAuthorization("qualification review", action=unused)

        argv = [
            "astrowoof-run-semantic-closure", "--run-dir", str(run_dir), "--resume",
            "--provider", "fake", "--max-attempts", "3", "--events-stdout-jsonl",
            "--log-level", "CRITICAL",
        ]
        with patch.object(closure, "author_pending_passes", side_effect=review):
            exit_code, envelopes = _invoke(argv)
        if exit_code != 2 or not envelopes or envelopes[-1].get("envelope_type") != "command_result":
            raise ValueError("Terminal-review public command did not seal before exit 2")
        index = json.loads((run_dir / "native-result-index.json").read_text(encoding="utf-8"))
        review_view = read_native_transition_result(run_dir, index["result_ids"][-1])
        review_result = review_view["result"]
        validate_terminal_review_result_v02(review_result)
        validate_terminal_review_command_result_against_publication(
            envelopes[-1]["result"], review_result, review_view["receipt"]
        )
        original_review_bytes = (
            run_dir / "native-results" / f"{review_result['result_id']}.json"
        ).read_bytes()

        methods: list[str] = []
        def request(_self: Any, *, method: str, url: str, payload: Any) -> tuple[dict, int]:
            methods.append(method)
            if method != "GET" or payload is not None:
                raise AssertionError("qualification attempted provider create")
            return {
                "id": url.rsplit("/", 1)[-1], "status": "completed",
                "model": "scripted-provider", "output": [],
                "usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12},
            }, 1
        reconciliation_argv = [
            "astrowoof-run-semantic-closure", "--run-dir", str(run_dir), "--resume",
            "--provider", "openai", "--provider-reconciliation-cycle",
            "--observed-at", "2099-08-28T09:00:01Z", "--log-level", "CRITICAL",
        ]
        with patch.dict(os.environ, {"OPENAI_API_KEY": "qualification-only"}), patch.object(
            closure.OpenAIResponsesProvider, "_request_with_retry", request
        ), patch.object(
            closure, "author_pending_passes", side_effect=AssertionError("authoring reopened")
        ), patch.object(
            closure, "finalize_subjects", side_effect=AssertionError("finalization reopened")
        ):
            reconciliation_code, _ = _invoke(reconciliation_argv)
        if reconciliation_code != 3 or methods != ["GET"]:
            raise ValueError("Review custody reconciliation transport differs")

        inspection = inspect_lifecycle(
            run_dir, native_exclusive_access="declared", observed_at="2099-08-28T09:00:02Z"
        )
        state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        unused = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == providerless_id)
        denied = deny_providerless_action(run_dir, {
            "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
            "run_id": state["run_id"], "action_id": providerless_id,
            "binding": unused["binding"], "observed": inspection["observation"],
            "denial_reason": "external_authority_denied",
            "external_authority_reference": "api:terminal-review-qualification",
        }, decision_at="2099-08-28T09:00:03Z")
        closeout = closeout_run(run_dir, observed_at="2099-08-28T09:00:04Z")

        historical_view = read_native_transition_result(
            run_dir, historical["result"]["result_id"]
        )
        if historical_view["result"]["schema_version"] != "astrowoof.native_execution_result.v0.1":
            raise ValueError("Historical result version changed")
        try:
            validate_terminal_review_result_v02(historical_view["result"])
        except ValueError:
            historical_refused_as_v02 = True
        else:
            historical_refused_as_v02 = False
        mutated_receipt = copy.deepcopy(review_view["receipt"])
        mutated_receipt["result_sha256"] = "0" * 64
        try:
            validate_native_publication_receipt(mutated_receipt, review_result)
        except ValueError:
            mutation_refused = True
        else:
            mutation_refused = False
        review_immutable = original_review_bytes == (
            run_dir / "native-results" / f"{review_result['result_id']}.json"
        ).read_bytes()
        result_ids = json.loads(
            (run_dir / "native-result-index.json").read_text(encoding="utf-8")
        )["result_ids"]
        successor = read_native_transition_result(run_dir, result_ids[-1])
        lineage_contiguous = (
            review_result["journal_range"]["end_sequence"] + 1
            == successor["result"]["journal_range"]["start_sequence"]
        )
        body = {
            "schema_version": CONTRACT, "status": "pass",
            "sbe_release": _installed_version(),
            "checks": {
                "public_result_v02": review_result["schema_version"],
                "command_exit_code": exit_code,
                "custody_finality": review_result["custody_finality"],
                "reported_action_id": reported_id,
                "reconciliation_action_ids": review_result["reconciliation_action_ids"],
                "providerless_denial_action_ids": review_result["providerless_denial_action_ids"],
                "new_provider_create_permitted": review_result["new_provider_create_permitted"],
                "review_result_valid": True,
                "review_receipt_valid": True,
                "review_immutable": review_immutable,
                "successor_result_valid": True,
                "successor_outcome": successor["result"]["outcome"],
                "lineage_contiguous": lineage_contiguous,
                "providerless_denial_outcome": denied["outcome"],
                "closeout_terminal": closeout["terminal"]["terminal"],
                "provider_continuation_remains": closeout["terminal"]["provider_continuation_remains"],
                "local_continuation_remains": closeout["terminal"]["local_continuation_remains"],
                "historical_v01_readable": True,
                "historical_v01_refused_as_v02": historical_refused_as_v02,
                "receipt_mutation_refused": mutation_refused,
                "scripted_get_count": methods.count("GET"),
                "provider_post_count": methods.count("POST"),
                "protected_sentinel_absent": True,
            },
        }
        rendered = json.dumps(body, sort_keys=True)
        if SENTINEL in rendered or not all((
            review_immutable, lineage_contiguous, historical_refused_as_v02,
            mutation_refused, denied["outcome"] == "applied",
            closeout["terminal"]["terminal"],
            not closeout["terminal"]["provider_continuation_remains"],
            not closeout["terminal"]["local_continuation_remains"],
        )):
            raise ValueError("Terminal-review qualification invariant failed")
        body["receipt_sha256"] = _digest(body)
        validate_terminal_review_qualification(body)
        return body


def validate_terminal_review_qualification(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "status", "sbe_release", "checks", "receipt_sha256",
    }:
        raise ValueError("Terminal-review qualification shape differs")
    if value.get("schema_version") != CONTRACT or value.get("status") != "pass":
        raise ValueError("Terminal-review qualification identity/status differs")
    if not isinstance(value.get("sbe_release"), str) or not value["sbe_release"]:
        raise ValueError("Terminal-review qualification release is invalid")
    checks = value.get("checks")
    expected_keys = {
        "public_result_v02", "command_exit_code", "custody_finality",
        "reported_action_id", "reconciliation_action_ids",
        "providerless_denial_action_ids", "new_provider_create_permitted",
        "review_result_valid", "review_receipt_valid", "review_immutable",
        "successor_result_valid", "successor_outcome", "lineage_contiguous",
        "providerless_denial_outcome", "closeout_terminal",
        "provider_continuation_remains", "local_continuation_remains",
        "historical_v01_readable", "historical_v01_refused_as_v02",
        "receipt_mutation_refused", "scripted_get_count", "provider_post_count",
        "protected_sentinel_absent",
    }
    if not isinstance(checks, dict) or set(checks) != expected_keys:
        raise ValueError("Terminal-review qualification checks differ")
    if (
        checks["public_result_v02"] != "astrowoof.native_execution_result.v0.2"
        or checks["command_exit_code"] != 2
        or checks["custody_finality"] != "mixed_resolution_required"
        or checks["reported_action_id"] != "paid_000000000000000000000101"
        or checks["reconciliation_action_ids"] != [
            "paid_000000000000000000000102"
        ]
        or checks["providerless_denial_action_ids"] != [
            "paid_000000000000000000000103"
        ]
        or checks["successor_outcome"] != "review_required"
        or checks["providerless_denial_outcome"] != "applied"
        or checks["new_provider_create_permitted"] is not False
        or checks["scripted_get_count"] != 1
        or checks["provider_post_count"] != 0
        or any(checks[key] is not True for key in (
            "review_result_valid", "review_receipt_valid", "review_immutable",
            "successor_result_valid", "lineage_contiguous", "closeout_terminal",
            "historical_v01_readable", "historical_v01_refused_as_v02",
            "receipt_mutation_refused", "protected_sentinel_absent",
        ))
        or checks["provider_continuation_remains"] is not False
        or checks["local_continuation_remains"] is not False
    ):
        raise ValueError("Terminal-review qualification semantics differ")
    expected = _digest({key: item for key, item in value.items() if key != "receipt_sha256"})
    if value.get("receipt_sha256") != expected:
        raise ValueError("Terminal-review qualification digest differs")
    return copy.deepcopy(value)


def read_terminal_review_qualification_schema() -> dict[str, Any]:
    resource = files("astrowoof_natal_authoring.resources").joinpath(
        f"contracts/{SCHEMA_RESOURCE}"
    )
    return json.loads(resource.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_terminal_review_qualification_schema()
        if args.schema else run_terminal_review_qualification()
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
