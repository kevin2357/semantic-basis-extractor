"""Provider-free qualification for the legacy v0.5 local-work upgrade seam."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from .closure import save_state
from .lifecycle import inspect_lifecycle
from .lifecycle_contracts import validate_lifecycle_inspection_v05
from .post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
    validate_lifecycle_inspection_v07,
)
from .post_fan_in_retry_qa import _materialize
from .retry_lineage_contracts import (
    inspect_retry_lineage_lifecycle,
    validate_lifecycle_inspection_v08,
)
from .retry_lineage_qa import (
    run_retry_lineage_qualification,
    validate_retry_lineage_qualification,
)


FIXTURE = "legacy-v05-local-work-upgrade-fixture.v1.json"
BUNDLE_SCHEMA = "legacy-v05-local-work-upgrade-bundle.v1.schema.json"
RECEIPT_SCHEMA = "legacy-v05-local-work-upgrade-qualification.v1.schema.json"
BUNDLE_CONTRACT = "astrowoof.legacy_v05_local_work_upgrade_bundle.v1"
RECEIPT_CONTRACT = "astrowoof.legacy_v05_local_work_upgrade_qualification.v1"


def _digest(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _resource(package: str, name: str) -> dict[str, Any]:
    return json.loads(files(package).joinpath(name).read_text(encoding="utf-8"))


def read_legacy_local_work_upgrade_fixture() -> dict[str, Any]:
    value = _resource("astrowoof_natal_authoring.resources.fixtures", FIXTURE)
    keys = {
        "schema_version", "scenario_ids", "expected_outcomes",
        "legacy_upgrade_predicate", "provider_io_permitted", "qualification_only",
    }
    expected_ids = [
        "consistent_not_due", "consistent_due",
        "lineage_conflict_with_custody", "lineage_conflict_after_custody",
    ]
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Legacy-upgrade fixture fields are not exact")
    if value.get("schema_version") != "astrowoof.legacy_v05_local_work_upgrade_fixture.v1":
        raise ValueError("Legacy-upgrade fixture schema is unsupported")
    if value.get("scenario_ids") != expected_ids:
        raise ValueError("Legacy-upgrade fixture scenarios differ")
    if set(value.get("expected_outcomes") or {}) != set(expected_ids):
        raise ValueError("Legacy-upgrade fixture outcomes differ")
    if value.get("legacy_upgrade_predicate") != "local_dependency_count":
        raise ValueError("Legacy-upgrade predicate differs")
    if value.get("provider_io_permitted") is not False or value.get("qualification_only") is not True:
        raise ValueError("Legacy-upgrade fixture safety declaration differs")
    return value


def read_legacy_local_work_upgrade_bundle_schema() -> dict[str, Any]:
    return _resource("astrowoof_natal_authoring.resources.contracts", BUNDLE_SCHEMA)


def read_legacy_local_work_upgrade_qualification_schema() -> dict[str, Any]:
    return _resource("astrowoof_natal_authoring.resources.contracts", RECEIPT_SCHEMA)


def _package_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "source-tree"


def _scenario(root: Path, *, due: bool) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    run_dir, completed_id, pending_id = _materialize(root)
    state_path = run_dir / "run.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    completed = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == completed_id)
    if not due:
        completed["provider_reconciliation"].update({
            "last_outcome": "completed",
            "resume_not_before": "2026-08-27T12:05:00Z",
        })
    pending = next(a for a in state["spend_ledger"]["actions"] if a["action_id"] == pending_id)
    pending["state"] = "WAITING"
    pending["provider"] = {"id": "resp_fixture_retry_2", "kind": "response"}
    pending["provider_reconciliation"] = {
        "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
        "provider_retrieval_attempt_count": 1,
        "last_attempt_at": "2026-08-27T11:59:00Z",
        "last_outcome": "pending",
        "resume_not_before": "2026-08-27T12:00:00Z" if due else "2026-08-27T12:05:00Z",
    }
    save_state(state_path, state)
    observed_at = "2026-08-27T12:01:00Z"
    v05 = inspect_lifecycle(run_dir, observed_at=observed_at, native_exclusive_access="declared")
    v07 = inspect_post_fan_in_lifecycle(run_dir, observed_at=observed_at, native_exclusive_access="declared")
    v08 = inspect_retry_lineage_lifecycle(run_dir, observed_at=observed_at, native_exclusive_access="declared")
    validate_lifecycle_inspection_v05(v05)
    validate_lifecycle_inspection_v07(v07)
    validate_lifecycle_inspection_v08(v08)
    identity = {
        "run_id": v05["run_id"],
        "revision": v05["observation"]["operator_state_revision"],
        "snapshot_sha256": v05["observation"]["snapshot_sha256"],
        "logical_workspace_root": v05["observation"]["logical_workspace_root"],
    }
    joins = []
    for item in (v07, v08):
        observation = item["checkpoint_basis"]["observation"]
        joins.append(identity == {
            "run_id": item["run_id"], "revision": observation["operator_state_revision"],
            "snapshot_sha256": observation["snapshot_sha256"],
            "logical_workspace_root": observation["logical_workspace_root"],
        })
    return {
        "scenario_id": "consistent_due" if due else "consistent_not_due",
        "documents": {"v05": v05, "v07": v07, "v08": v08},
        "stable_identity_join": all(joins),
        "legacy_predicate_failures": (
            ["local_dependency_count"]
            if not due and not v05["local_dependencies"] else []
        ),
        "selected_command": v08["temporal_decision"]["selected_command"],
        "capacity_disposition": v08["temporal_decision"]["capacity_disposition"],
        "eligible_now": v08["temporal_decision"]["eligible_now"],
        "local_source_action_ids": [
            action_id
            for operation in v08["checkpoint_basis"]["local_work_inventory"]["operations"]
            for action_id in operation["source_action_ids"]
        ],
        "custody_action_ids": list(v08["checkpoint_basis"]["provider_custody"]["action_ids"]),
    }


def build_legacy_local_work_upgrade_bundle() -> dict[str, Any]:
    fixture = read_legacy_local_work_upgrade_fixture()
    with tempfile.TemporaryDirectory(prefix="astrowoof-legacy-upgrade-") as temporary:
        root = Path(temporary)
        scenarios = [
            _scenario(root / "not-due", due=False),
            _scenario(root / "due", due=True),
        ]
    conflict = validate_retry_lineage_qualification(run_retry_lineage_qualification())
    body = {
        "schema_version": BUNDLE_CONTRACT,
        "fixture_sha256": _digest(fixture),
        "scenarios": scenarios,
        "conflict_qualification": conflict,
        "provider_io": {"create_count": 0, "retrieve_count": 0, "external_network_count": 0, "spend_usd": 0},
    }
    return validate_legacy_local_work_upgrade_bundle({**body, "bundle_sha256": _digest(body)})


def validate_legacy_local_work_upgrade_bundle(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "bundle_sha256", "fixture_sha256", "scenarios", "conflict_qualification", "provider_io"}
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != BUNDLE_CONTRACT:
        raise ValueError("Legacy-upgrade bundle fields are not exact")
    body = {key: item for key, item in value.items() if key != "bundle_sha256"}
    if value.get("bundle_sha256") != _digest(body):
        raise ValueError("Legacy-upgrade bundle digest mismatch")
    if value.get("fixture_sha256") != _digest(read_legacy_local_work_upgrade_fixture()):
        raise ValueError("Legacy-upgrade fixture digest mismatch")
    scenarios = value.get("scenarios")
    if not isinstance(scenarios, list) or [s.get("scenario_id") for s in scenarios if isinstance(s, Mapping)] != ["consistent_not_due", "consistent_due"]:
        raise ValueError("Legacy-upgrade scenarios differ")
    expected = {"consistent_not_due": "ordinary_resume", "consistent_due": "provider_reconciliation_cycle"}
    for scenario in scenarios:
        required = {"scenario_id", "documents", "stable_identity_join", "legacy_predicate_failures", "selected_command", "capacity_disposition", "eligible_now", "local_source_action_ids", "custody_action_ids"}
        if set(scenario) != required or scenario.get("stable_identity_join") is not True:
            raise ValueError("Legacy-upgrade scenario shape or identity join differs")
        documents = scenario["documents"]
        if not isinstance(documents, Mapping) or set(documents) != {"v05", "v07", "v08"}:
            raise ValueError("Legacy-upgrade documents differ")
        validate_lifecycle_inspection_v05(copy.deepcopy(documents["v05"]))
        validate_lifecycle_inspection_v07(copy.deepcopy(documents["v07"]))
        validate_lifecycle_inspection_v08(copy.deepcopy(documents["v08"]))
        legacy = documents["v05"]
        local = documents["v07"]
        lineage = documents["v08"]
        identity = {
            "run_id": legacy["run_id"],
            "revision": legacy["observation"]["operator_state_revision"],
            "snapshot_sha256": legacy["observation"]["snapshot_sha256"],
            "logical_workspace_root": legacy["observation"]["logical_workspace_root"],
        }
        joined = all(identity == {
            "run_id": item["run_id"],
            "revision": item["checkpoint_basis"]["observation"]["operator_state_revision"],
            "snapshot_sha256": item["checkpoint_basis"]["observation"]["snapshot_sha256"],
            "logical_workspace_root": item["checkpoint_basis"]["observation"]["logical_workspace_root"],
        } for item in (local, lineage))
        if not joined or scenario["stable_identity_join"] is not joined:
            raise ValueError("Legacy-upgrade scenario identity join differs")
        decision = lineage["temporal_decision"]
        derived_sources = [
            action_id
            for operation in lineage["checkpoint_basis"]["local_work_inventory"]["operations"]
            for action_id in operation["source_action_ids"]
        ]
        if (
            scenario["selected_command"] != decision["selected_command"]
            or scenario["capacity_disposition"] != decision["capacity_disposition"]
            or scenario["eligible_now"] is not decision["eligible_now"]
            or scenario["local_source_action_ids"] != derived_sources
            or scenario["custody_action_ids"] != lineage["checkpoint_basis"]["provider_custody"]["action_ids"]
        ):
            raise ValueError("Legacy-upgrade scenario projection differs")
        if scenario["scenario_id"] == "consistent_not_due":
            branch = legacy["execution_branch"]
            capacity = legacy["execution_capacity"]
            completed_evidence = [
                action
                for action in legacy["provider_custody"]["actions"]
                if action["custody_classification"] == "completed_provider_evidence"
            ]
            frozen_ordinary_resume = (
                branch == {
                    "command": "ordinary_resume",
                    "eligible_now": True,
                    "reason_code": "ordinary_local_continuation_ready",
                    "action_ids": [],
                    "not_before": None,
                }
                and capacity["disposition"] == "continue_local_cycle"
                and capacity["local_work_ready_now"] is True
                and capacity["resume_not_before"] is None
                and capacity["reason_code"] == "local_work_ready"
                and legacy["terminal"]["local_continuation_remains"] is True
            )
            if (
                not frozen_ordinary_resume
                or legacy["local_dependencies"] != []
                or not completed_evidence
            ):
                raise ValueError("Legacy-upgrade v0.5 seam evidence differs")
            expected_failures = ["local_dependency_count"]
        else:
            expected_failures = []
        if scenario["legacy_predicate_failures"] != expected_failures or scenario["selected_command"] != expected[scenario["scenario_id"]]:
            raise ValueError("Legacy-upgrade scenario outcome differs")
    validate_retry_lineage_qualification(value.get("conflict_qualification"))
    if value.get("provider_io") != {"create_count": 0, "retrieve_count": 0, "external_network_count": 0, "spend_usd": 0}:
        raise ValueError("Legacy-upgrade provider I/O declaration differs")
    return copy.deepcopy(dict(value))


def run_legacy_local_work_upgrade_qualification() -> dict[str, Any]:
    bundle = build_legacy_local_work_upgrade_bundle()
    fixture = read_legacy_local_work_upgrade_fixture()
    conflict = bundle["conflict_qualification"]
    body = {
        "schema_version": RECEIPT_CONTRACT, "status": "pass",
        "qualification_only": True, "provider_free": True,
        "package": {"name": "astrowoof-natal-authoring", "version": _package_version()},
        "fixture_sha256": _digest(fixture),
        "bundle_schema_sha256": _digest(read_legacy_local_work_upgrade_bundle_schema()),
        "qualification_schema_sha256": _digest(read_legacy_local_work_upgrade_qualification_schema()),
        "scenarios": [
            {"scenario_id": item["scenario_id"], "selected_outcome": item["selected_command"], "stable_identity_join": item["stable_identity_join"]}
            for item in bundle["scenarios"]
        ] + [
            {"scenario_id": "lineage_conflict_with_custody", "selected_outcome": "provider_reconciliation_cycle", "stable_identity_join": True},
            {"scenario_id": "lineage_conflict_after_custody", "selected_outcome": "retain_for_review", "stable_identity_join": conflict["status"] == "pass"},
        ],
        "provider_io": bundle["provider_io"],
        "privacy": {"contains_prompt": False, "contains_provider_payload": False, "contains_raw_run_state": False, "contains_workspace_path": False, "contains_retained_qa_data": False},
    }
    return validate_legacy_local_work_upgrade_qualification({**body, "receipt_sha256": _digest(body)})


def validate_legacy_local_work_upgrade_qualification(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "receipt_sha256", "status", "qualification_only", "provider_free", "package", "fixture_sha256", "bundle_schema_sha256", "qualification_schema_sha256", "scenarios", "provider_io", "privacy"}
    if not isinstance(value, Mapping) or set(value) != keys or value.get("schema_version") != RECEIPT_CONTRACT:
        raise ValueError("Legacy-upgrade receipt fields are not exact")
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _digest(body) or value.get("status") != "pass" or value.get("qualification_only") is not True or value.get("provider_free") is not True:
        raise ValueError("Legacy-upgrade receipt declaration differs")
    if value.get("fixture_sha256") != _digest(read_legacy_local_work_upgrade_fixture()) or value.get("bundle_schema_sha256") != _digest(read_legacy_local_work_upgrade_bundle_schema()) or value.get("qualification_schema_sha256") != _digest(read_legacy_local_work_upgrade_qualification_schema()):
        raise ValueError("Legacy-upgrade receipt resource digest differs")
    fixture = read_legacy_local_work_upgrade_fixture()
    scenarios = value.get("scenarios")
    if not isinstance(scenarios, list) or [item.get("scenario_id") for item in scenarios if isinstance(item, Mapping)] != fixture["scenario_ids"]:
        raise ValueError("Legacy-upgrade receipt scenarios differ")
    for item in scenarios:
        if set(item) != {"scenario_id", "selected_outcome", "stable_identity_join"} or item["selected_outcome"] != fixture["expected_outcomes"][item["scenario_id"]] or item["stable_identity_join"] is not True:
            raise ValueError("Legacy-upgrade receipt scenario outcome differs")
    if value.get("provider_io") != {"create_count": 0, "retrieve_count": 0, "external_network_count": 0, "spend_usd": 0} or any(value.get("privacy", {}).values()):
        raise ValueError("Legacy-upgrade receipt safety declaration differs")
    return copy.deepcopy(dict(value))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fixture", action="store_true")
    group.add_argument("--bundle", action="store_true")
    group.add_argument("--bundle-schema", action="store_true")
    group.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    output = (
        read_legacy_local_work_upgrade_fixture() if args.fixture
        else build_legacy_local_work_upgrade_bundle() if args.bundle
        else read_legacy_local_work_upgrade_bundle_schema() if args.bundle_schema
        else read_legacy_local_work_upgrade_qualification_schema() if args.schema
        else run_legacy_local_work_upgrade_qualification()
    )
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
