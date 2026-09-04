"""Provider-free qualification for terminal providerless-denial settlement."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
import tomllib
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any

from .closure import normalized_path, public_run_state, write_workspace_snapshot
from .lifecycle import closeout_run, deny_providerless_action, inspect_lifecycle
from .lifecycle_contracts import NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA
from .native_transitions import (
    publish_native_execution_result,
    read_native_transition_result,
)
from .terminal_review_contracts import (
    validate_terminal_review_result_v02,
    validate_terminal_review_result_v02_against_receipt,
)


CONTRACT = "astrowoof.providerless_denial_settlement_qualification.v1"
DETAILED_CONTRACT = "astrowoof.providerless_denial_settlement_qualification.v2"
SCHEMA_RESOURCE = "providerless-denial-settlement-qualification.v1.schema.json"
DETAILED_SCHEMA_RESOURCE = "providerless-denial-settlement-qualification.v2.schema.json"
DENIAL_ACTION_ID = "paid_000000000000000000000108"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _installed_version() -> str:
    module_path = Path(__file__).resolve()
    if not any(part.lower() == "site-packages" for part in module_path.parts):
        for parent in module_path.parents:
            project = parent / "pyproject.toml"
            if project.is_file():
                return str(tomllib.loads(project.read_text(encoding="utf-8"))["project"]["version"])
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def _binding(run_id: str, stage: str, route: str, revision: int) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "profile_sha256": "a" * 64,
        "prepared_state_revision": revision,
        "stage": stage,
        "route": route,
        "request_sha256": "b" * 64,
        "model": "scripted-provider",
        "service_level": "interactive",
        "maximum_output_tokens": 1000,
        "commitment_micro_usd": 1,
        "price_book_version": "openai-public-2026-08-07.v1",
    }


def _materialize(root: Path) -> Path:
    run_dir = root / "run"
    run_dir.mkdir()
    run_id = "providerless-denial-settlement-qualification"
    actions: list[dict[str, Any]] = []
    for number in range(1, 8):
        stage = "authoring_initial" if number <= 6 else "creative_retry"
        route = f"pass-{number}:attempt-001" if number <= 6 else "pass-2:attempt-002"
        actions.append({
            "action_id": f"paid_{number:024x}",
            "state": "REPORTED",
            "binding": _binding(run_id, stage, route, number),
            "provider": {"id": f"resp_providerless_qa_{number}", "kind": "response"},
            "consumption": {"consumer": "providerless-denial-qualification"},
            "reported": {
                "estimated_micro_usd": 0,
                "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
            },
        })
    actions.append({
        "action_id": DENIAL_ACTION_ID,
        "state": "PREPARED",
        "binding": _binding(run_id, "polish", "subject-1:polish:001", 8),
    })
    state = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": run_id,
        "state_revision": 8,
        "created_at": "2026-09-04T20:00:00Z",
        "updated_at": "2026-09-04T20:00:00Z",
        "provider": "fake",
        "provider_configuration": {},
        "max_attempts": 3,
        "status": "FINAL_QA_REQUIRES_REVIEW",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
        },
        "spend_ledger": {
            "policy": {
                "currency": "USD",
                "price_book_version": "openai-public-2026-08-07.v1",
                "run_ceiling_micro_usd": 100000000,
                "stage_ceilings_micro_usd": {
                    stage: 100000000 for stage in (
                        "authoring_initial", "creative_retry", "polish",
                        "qualitative_critic", "qualitative_candidate",
                    )
                },
                "optional_stage_budget_behavior": {
                    "polish": "skip",
                    "qualitative_critic": "skip",
                    "qualitative_candidate": "skip",
                },
            },
            "actions": actions,
        },
        "initial_authoring_wave": {"state": "DETACHED"},
        "passes": {
            f"pass-{number}": {
                "pass_id": f"pass-{number}",
                "subject": "subject-1",
                "pass_number": number,
                "state": "PASS_QA_ACCEPTED",
                "attempts": [{"attempt_number": 1, "state": "PASS_QA_ACCEPTED"}],
            }
            for number in range(1, 7)
        },
        "subjects": {
            "subject-1": {
                "subject_id": "subject-1",
                "state": "FINAL_QA_WARN",
                "polish_attempts": [{"attempt_number": 1, "state": "AWAITING_SPEND_AUTHORIZATION"}],
            }
        },
        "provenance": {},
    }
    (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (run_dir / "public-run.json").write_text(
        json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
    )
    write_workspace_snapshot(run_dir)
    return run_dir


def _request(run_dir: Path, *, observed_at: str) -> dict[str, Any]:
    state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    action = next(item for item in state["spend_ledger"]["actions"] if item["action_id"] == DENIAL_ACTION_ID)
    inspection = inspect_lifecycle(
        run_dir, native_exclusive_access="declared", observed_at=observed_at,
    )
    return {
        "schema_version": NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA,
        "run_id": state["run_id"],
        "action_id": DENIAL_ACTION_ID,
        "binding": copy.deepcopy(action["binding"]),
        "observed": copy.deepcopy(inspection["observation"]),
        "denial_reason": "external_authority_denied",
        "external_authority_reference": "api:providerless-denial-qualification",
    }


def _workspace_identity(run_dir: Path) -> tuple[bytes, bytes]:
    return (
        (run_dir / "run.json").read_bytes(),
        (run_dir / "workspace-snapshot.json").read_bytes(),
    )


def run_providerless_denial_settlement_qualification(
    *, _publication_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="astrowoof-providerless-denial-qa-") as temporary:
        run_dir = _materialize(Path(temporary))
        precursor = publish_native_execution_result(
            run_dir,
            command_kind="ordinary_authoring",
            sbe_release=_installed_version(),
            published_at="2026-09-04T20:00:01Z",
            terminal_review_v02=True,
            terminal_review_cause="native_lifecycle_review_required",
        )
        precursor_result = precursor["result"]
        precursor_receipt = precursor["receipt"]
        validate_terminal_review_result_v02(precursor_result)
        validate_terminal_review_result_v02_against_receipt(precursor_result, precursor_receipt)
        request = _request(run_dir, observed_at="2026-09-04T20:00:02Z")

        refusal_outcomes: dict[str, str] = {}
        wrong_action = copy.deepcopy(request)
        wrong_action["action_id"] = "paid_000000000000000000000199"
        before = _workspace_identity(run_dir)
        refusal_outcomes["wrong_action"] = deny_providerless_action(run_dir, wrong_action)["outcome"]
        if _workspace_identity(run_dir) != before:
            raise ValueError("Wrong-action refusal mutated the workspace")

        wrong_binding = copy.deepcopy(request)
        wrong_binding["binding"]["request_sha256"] = "c" * 64
        refusal_outcomes["wrong_binding"] = deny_providerless_action(run_dir, wrong_binding)["outcome"]
        if _workspace_identity(run_dir) != before:
            raise ValueError("Wrong-binding refusal mutated the workspace")

        stale = copy.deepcopy(request)
        stale["observed"]["operator_state_revision"] -= 1
        refusal_outcomes["stale_observation"] = deny_providerless_action(run_dir, stale)["outcome"]
        if _workspace_identity(run_dir) != before:
            raise ValueError("Stale-observation refusal mutated the workspace")

        denial = deny_providerless_action(
            run_dir, request, decision_at="2026-09-04T20:00:03Z"
        )
        after_denial = _workspace_identity(run_dir)
        replay = deny_providerless_action(
            run_dir, request, decision_at="2026-09-04T20:00:04Z"
        )
        replay_inert = _workspace_identity(run_dir) == after_denial

        changed_replay = copy.deepcopy(request)
        changed_replay["external_authority_reference"] = "api:changed-authority"
        refusal_outcomes["changed_replay"] = deny_providerless_action(
            run_dir, changed_replay, decision_at="2026-09-04T20:00:05Z"
        )["outcome"]
        changed_replay_inert = _workspace_identity(run_dir) == after_denial

        successor = publish_native_execution_result(
            run_dir,
            command_kind="ordinary_authoring",
            sbe_release=_installed_version(),
            published_at="2026-09-04T20:00:06Z",
            terminal_review_v02=True,
            terminal_review_cause="native_lifecycle_review_required",
        )
        successor_result = successor["result"]
        successor_receipt = successor["receipt"]
        validate_terminal_review_result_v02(successor_result)
        validate_terminal_review_result_v02_against_receipt(successor_result, successor_receipt)
        inspection = inspect_lifecycle(
            run_dir, native_exclusive_access="declared", observed_at="2026-09-04T20:00:07Z"
        )
        closeout = closeout_run(run_dir, observed_at="2026-09-04T20:00:08Z")

        precursor_immutable = precursor_result == read_native_transition_result(
            run_dir, precursor_result["result_id"]
        )["result"]
        lineage_contiguous = (
            precursor_result["journal_range"]["end_sequence"] + 1
            == successor_result["journal_range"]["start_sequence"]
        )
        body = {
            "schema_version": CONTRACT,
            "status": "pass",
            "sbe_release": _installed_version(),
            "qualification_only": True,
            "provider_free": True,
            "provider_create_count": 0,
            "provider_retrieval_count": 0,
            "provider_transport_count": 0,
            "fixture": {
                "route_family": "exact_natal",
                "provider_mechanism": "response",
                "paid_action_count": 8,
                "terminally_accounted_action_count": 7,
                "providerless_denial_action_id": DENIAL_ACTION_ID,
                "providerless_denial_stage": "polish",
            },
            "precursor": {
                "schema_version": precursor_result["schema_version"],
                "outcome": precursor_result["outcome"],
                "cause_code": precursor_result["cause_code"],
                "custody_finality": precursor_result["custody_finality"],
                "providerless_denial_action_ids": precursor_result["providerless_denial_action_ids"],
                "reconciliation_action_ids": precursor_result["reconciliation_action_ids"],
                "new_provider_create_permitted": precursor_result["new_provider_create_permitted"],
            },
            "denial": {
                "request_schema_version": request["schema_version"],
                "result_schema_version": denial["schema_version"],
                "outcome": denial["outcome"],
                "action_id": denial["action_id"],
                "disposition": denial["disposition"],
                "exact_replay_outcome": replay["outcome"],
                "refusal_outcomes": refusal_outcomes,
            },
            "successor": {
                "schema_version": successor_result["schema_version"],
                "outcome": successor_result["outcome"],
                "custody_finality": successor_result["custody_finality"],
                "providerless_denial_action_ids": successor_result["providerless_denial_action_ids"],
                "reconciliation_action_ids": successor_result["reconciliation_action_ids"],
                "new_provider_create_permitted": successor_result["new_provider_create_permitted"],
                "inspection_terminal": inspection["terminal"]["terminal"],
                "closeout_terminal": closeout["terminal"]["terminal"],
            },
            "assertions": {
                "precursor_receipt_valid": True,
                "precursor_not_final": precursor_result["custody_finality"] != "final",
                "precursor_immutable": precursor_immutable,
                "denial_applied_once": denial["outcome"] == "applied",
                "exact_replay_inert": replay["outcome"] == "idempotent_replay" and replay_inert,
                "wrong_authority_inert": changed_replay_inert,
                "successor_receipt_valid": True,
                "successor_final": successor_result["custody_finality"] == "final",
                "lineage_contiguous": lineage_contiguous,
                "zero_provider_io": True,
            },
        }
        value = {**body, "receipt_sha256": _digest(body)}
        validate_providerless_denial_settlement_qualification(value)
        if _publication_identity is not None:
            denial_row = next(
                item for item in precursor_result["action_dispositions"]
                if item["action_id"] == DENIAL_ACTION_ID
            )
            _publication_identity.update({
                "denial_request_sha256": _digest(request),
                "denial_action_binding_sha256": denial_row["binding_sha256"],
                "denial_result_artifact_sha256": denial["result_checkpoint"]["result_artifact"]["sha256"],
                "denial_result_snapshot_sha256": denial["result_checkpoint"]["snapshot_sha256"],
                "precursor_result_id": precursor_result["result_id"],
                "precursor_result_sha256": precursor_result["result_sha256"],
                "precursor_action_inventory_sha256": precursor_result["action_inventory_sha256"],
                "precursor_receipt_id": precursor_receipt["receipt_id"],
                "precursor_receipt_sha256": precursor_receipt["receipt_sha256"],
                "precursor_snapshot_sha256": precursor_receipt["snapshot_sha256"],
                "precursor_checkpoint_basis_sha256": precursor_receipt["checkpoint_basis_sha256"],
                "successor_result_id": successor_result["result_id"],
                "successor_result_sha256": successor_result["result_sha256"],
                "successor_action_inventory_sha256": successor_result["action_inventory_sha256"],
                "successor_receipt_id": successor_receipt["receipt_id"],
                "successor_receipt_sha256": successor_receipt["receipt_sha256"],
                "successor_snapshot_sha256": successor_receipt["snapshot_sha256"],
                "successor_checkpoint_basis_sha256": successor_receipt["checkpoint_basis_sha256"],
            })
        return value


def validate_providerless_denial_settlement_qualification(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version", "status", "sbe_release", "qualification_only",
        "provider_free", "provider_create_count", "provider_retrieval_count",
        "provider_transport_count", "fixture", "precursor",
        "denial", "successor", "assertions", "receipt_sha256",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Providerless-denial qualification shape differs")
    fixture = value.get("fixture")
    precursor = value.get("precursor")
    denial = value.get("denial")
    successor = value.get("successor")
    assertions = value.get("assertions")
    if (
        value.get("schema_version") != CONTRACT
        or value.get("status") != "pass"
        or not isinstance(value.get("sbe_release"), str) or not value["sbe_release"]
        or value.get("qualification_only") is not True
        or value.get("provider_free") is not True
        or value.get("provider_create_count") != 0
        or value.get("provider_retrieval_count") != 0
        or value.get("provider_transport_count") != 0
        or not isinstance(fixture, dict)
        or fixture != {
            "route_family": "exact_natal",
            "provider_mechanism": "response",
            "paid_action_count": 8,
            "terminally_accounted_action_count": 7,
            "providerless_denial_action_id": DENIAL_ACTION_ID,
            "providerless_denial_stage": "polish",
        }
        or not isinstance(precursor, dict)
        or precursor != {
            "schema_version": "astrowoof.native_execution_result.v0.2",
            "outcome": "review_required",
            "cause_code": "native_lifecycle_review_required",
            "custody_finality": "providerless_denial_required",
            "providerless_denial_action_ids": [DENIAL_ACTION_ID],
            "reconciliation_action_ids": [],
            "new_provider_create_permitted": False,
        }
        or not isinstance(denial, dict)
        or denial.get("request_schema_version") != NEGATIVE_AUTHORIZATION_REQUEST_SCHEMA
        or denial.get("result_schema_version") != "astrowoof.provider_negative_authorization_result.v0.2"
        or denial.get("outcome") != "applied"
        or denial.get("action_id") != DENIAL_ACTION_ID
        or denial.get("disposition") != "DENIED_PROVIDERLESS"
        or denial.get("exact_replay_outcome") != "idempotent_replay"
        or denial.get("refusal_outcomes") != {
            "wrong_action": "immutable_binding_mismatch",
            "wrong_binding": "immutable_binding_mismatch",
            "stale_observation": "stale_observation",
            "changed_replay": "native_state_inconsistent",
        }
        or not isinstance(successor, dict)
        or successor != {
            "schema_version": "astrowoof.native_execution_result.v0.2",
            "outcome": "review_required",
            "custody_finality": "final",
            "providerless_denial_action_ids": [],
            "reconciliation_action_ids": [],
            "new_provider_create_permitted": False,
            "inspection_terminal": True,
            "closeout_terminal": True,
        }
        or not isinstance(assertions, dict)
        or set(assertions) != {
            "precursor_receipt_valid", "precursor_not_final", "precursor_immutable",
            "denial_applied_once", "exact_replay_inert", "wrong_authority_inert",
            "successor_receipt_valid", "successor_final", "lineage_contiguous",
            "zero_provider_io",
        }
        or any(item is not True for item in assertions.values())
    ):
        raise ValueError("Providerless-denial qualification semantics differ")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Providerless-denial qualification digest differs")
    return copy.deepcopy(value)


def run_providerless_denial_settlement_qualification_v02() -> dict[str, Any]:
    identity: dict[str, Any] = {}
    qualification = run_providerless_denial_settlement_qualification(
        _publication_identity=identity
    )
    body = {
        "schema_version": DETAILED_CONTRACT,
        "status": "pass",
        "qualification": qualification,
        "publication_identity": identity,
    }
    value = {**body, "receipt_sha256": _digest(body)}
    return validate_providerless_denial_settlement_qualification_v02(value)


def validate_providerless_denial_settlement_qualification_v02(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "status", "qualification", "publication_identity", "receipt_sha256",
    }:
        raise ValueError("Detailed providerless-denial qualification shape differs")
    if value.get("schema_version") != DETAILED_CONTRACT or value.get("status") != "pass":
        raise ValueError("Detailed providerless-denial qualification identity differs")
    validate_providerless_denial_settlement_qualification(value.get("qualification"))
    identity = value.get("publication_identity")
    expected = {
        "denial_request_sha256", "denial_action_binding_sha256",
        "denial_result_artifact_sha256", "denial_result_snapshot_sha256",
        "precursor_result_id", "precursor_result_sha256", "precursor_receipt_id",
        "precursor_action_inventory_sha256",
        "precursor_receipt_sha256", "precursor_snapshot_sha256",
        "precursor_checkpoint_basis_sha256", "successor_result_id",
        "successor_result_sha256", "successor_receipt_id", "successor_receipt_sha256",
        "successor_action_inventory_sha256",
        "successor_snapshot_sha256", "successor_checkpoint_basis_sha256",
    }
    if not isinstance(identity, dict) or set(identity) != expected:
        raise ValueError("Detailed providerless-denial publication identity differs")
    for field in (
        "denial_request_sha256", "denial_action_binding_sha256",
        "denial_result_artifact_sha256", "denial_result_snapshot_sha256",
        "precursor_action_inventory_sha256", "successor_action_inventory_sha256",
    ):
        item = identity[field]
        if (
            not isinstance(item, str) or len(item) != 64
            or any(char not in "0123456789abcdef" for char in item)
        ):
            raise ValueError("Detailed providerless-denial action binding differs")
    for prefix in ("precursor", "successor"):
        result_sha = identity[f"{prefix}_result_sha256"]
        receipt_sha = identity[f"{prefix}_receipt_sha256"]
        digests = (
            result_sha, receipt_sha, identity[f"{prefix}_snapshot_sha256"],
            identity[f"{prefix}_checkpoint_basis_sha256"],
        )
        if (
            identity[f"{prefix}_result_id"] != f"nres_{result_sha[:24]}"
            or identity[f"{prefix}_receipt_id"] != f"nreceipt_{receipt_sha[:24]}"
            or any(
                not isinstance(item, str) or len(item) != 64
                or any(char not in "0123456789abcdef" for char in item)
                for item in digests
            )
        ):
            raise ValueError("Detailed providerless-denial publication binding differs")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body):
        raise ValueError("Detailed providerless-denial qualification digest differs")
    return copy.deepcopy(value)


def read_providerless_denial_settlement_qualification_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources").joinpath(
        f"contracts/{SCHEMA_RESOURCE}"
    ).read_text(encoding="utf-8"))


def read_providerless_denial_settlement_fixture() -> dict[str, Any]:
    value = json.loads(files("astrowoof_natal_authoring.resources").joinpath(
        "fixtures/lifecycle/providerless-denial-settlement-qualification.v1.json"
    ).read_text(encoding="utf-8"))
    return validate_providerless_denial_settlement_qualification(value)


def read_providerless_denial_settlement_qualification_v02_schema() -> dict[str, Any]:
    return json.loads(files("astrowoof_natal_authoring.resources").joinpath(
        f"contracts/{DETAILED_SCHEMA_RESOURCE}"
    ).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--detailed", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_providerless_denial_settlement_qualification_v02_schema()
        if args.schema and args.detailed
        else read_providerless_denial_settlement_qualification_schema()
        if args.schema
        else run_providerless_denial_settlement_qualification_v02()
        if args.detailed
        else run_providerless_denial_settlement_qualification()
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
