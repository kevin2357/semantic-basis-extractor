from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _workspace
from astrowoof_natal_authoring.closure import public_run_state, write_workspace_snapshot
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.post_fan_in_contracts import (
    build_lifecycle_inspection_v07,
    build_local_work_inventory,
    read_lifecycle_inspection_v07_schema,
    read_local_work_inventory_schema,
    validate_lifecycle_inspection_v07,
    validate_local_work_inventory,
    validate_local_work_progress,
)


def _inventory(inspection: dict, action_id: str, route: str) -> dict:
    observation = inspection["observation"]
    return build_local_work_inventory(
        run_id=inspection["run_id"],
        state_revision=observation["operator_state_revision"],
        snapshot_sha256=observation["snapshot_sha256"],
        logical_workspace_root=observation["logical_workspace_root"],
        operations=[{
            "kind": "provider_result_fan_in_and_retry_evaluation",
            "route_family": route,
            "stage": "creative_retry",
            "source_action_ids": [action_id],
            "reason_code": "provider_evidence_ingestion_required",
        }],
    )


class PostFanInRetrySlice1ContractTests(unittest.TestCase):
    def test_v07_binds_exact_inventory_and_progresses_to_authority(self) -> None:
        for route in ("exact_natal", "bounded_natal"):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as temporary:
                run_dir, retry_one, retry_two = _workspace(Path(temporary), route)
                prior_v05 = inspect_lifecycle(
                    run_dir, native_exclusive_access="declared",
                    observed_at="2026-08-25T23:43:00Z",
                )
                prior = build_lifecycle_inspection_v07(
                    prior_v05, _inventory(prior_v05, retry_one, route),
                )
                self.assertEqual(
                    "astrowoof.authoring_lifecycle_inspection.v0.7",
                    prior["schema_version"],
                )
                self.assertEqual(
                    "ordinary_resume", prior["temporal_decision"]["selected_command"]
                )

                state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == retry_one
                )
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
                state["state_revision"] += 1
                (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
                write_workspace_snapshot(run_dir)
                successor_v05 = inspect_lifecycle(
                    run_dir, native_exclusive_access="declared",
                    observed_at="2026-08-25T23:44:00Z",
                )
                observation = successor_v05["observation"]
                empty = build_local_work_inventory(
                    run_id=successor_v05["run_id"],
                    state_revision=observation["operator_state_revision"],
                    snapshot_sha256=observation["snapshot_sha256"],
                    logical_workspace_root=observation["logical_workspace_root"],
                    operations=[],
                )
                successor = build_lifecycle_inspection_v07(successor_v05, empty)
                self.assertEqual(
                    "await_external_authority",
                    successor["temporal_decision"]["selected_command"],
                )
                self.assertEqual(
                    [retry_two],
                    successor_v05["execution_branch"]["action_ids"],
                )
                validate_local_work_progress(prior, successor)

    def test_same_basis_or_replayed_operation_fails_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            prior = build_lifecycle_inspection_v07(
                v05, _inventory(v05, retry_one, "exact_natal"),
            )
            with self.assertRaisesRegex(ValueError, "did not advance"):
                validate_local_work_progress(prior, copy.deepcopy(prior))

            replay = copy.deepcopy(prior)
            replay["checkpoint_basis"]["observation"]["operator_state_revision"] += 1
            # A hand-mutated/rehashed document still cannot reuse the old member,
            # because its member basis remains bound to the prior checkpoint.
            with self.assertRaises(ValueError):
                validate_lifecycle_inspection_v07(replay)

    def test_noop_republish_cannot_rename_same_semantic_work(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            prior_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            prior = build_lifecycle_inspection_v07(
                prior_v05, _inventory(prior_v05, retry_one, "exact_natal"),
            )
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            successor_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:01Z",
            )
            successor = build_lifecycle_inspection_v07(
                successor_v05,
                _inventory(successor_v05, retry_one, "exact_natal"),
            )
            prior_member = prior["checkpoint_basis"]["local_work_inventory"]["operations"][0]
            successor_member = successor["checkpoint_basis"]["local_work_inventory"]["operations"][0]
            self.assertNotEqual(prior_member["operation_id"], successor_member["operation_id"])
            self.assertEqual(prior_member["operation_key"], successor_member["operation_key"])
            with self.assertRaisesRegex(ValueError, "semantic local-work"):
                validate_local_work_progress(prior, successor)

    def test_continued_local_work_requires_explicit_consumption_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            prior_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            prior_inventory = _inventory(prior_v05, retry_one, "exact_natal")
            prior = build_lifecycle_inspection_v07(prior_v05, prior_inventory)
            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            successor_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:01Z",
            )
            observation = successor_v05["observation"]
            next_operation = [{
                "kind": "final_assembly_and_qa",
                "route_family": "exact_natal",
                "stage": None,
                "source_action_ids": [retry_one],
                "reason_code": "final_assembly_required",
            }]
            without_consumption = build_lifecycle_inspection_v07(
                successor_v05,
                build_local_work_inventory(
                    run_id=successor_v05["run_id"],
                    state_revision=observation["operator_state_revision"],
                    snapshot_sha256=observation["snapshot_sha256"],
                    logical_workspace_root=observation["logical_workspace_root"],
                    operations=next_operation,
                ),
            )
            with self.assertRaisesRegex(ValueError, "consumption evidence"):
                validate_local_work_progress(prior, without_consumption)
            prior_key = prior_inventory["operations"][0]["operation_key"]
            with_consumption = build_lifecycle_inspection_v07(
                successor_v05,
                build_local_work_inventory(
                    run_id=successor_v05["run_id"],
                    state_revision=observation["operator_state_revision"],
                    snapshot_sha256=observation["snapshot_sha256"],
                    logical_workspace_root=observation["logical_workspace_root"],
                    operations=next_operation,
                    consumed_operation_keys=[prior_key],
                ),
            )
            validate_local_work_progress(prior, with_consumption)

    def test_consumption_history_is_cumulative_and_consumed_work_cannot_return(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            first_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            first_inventory = _inventory(first_v05, retry_one, "exact_natal")
            first = build_lifecycle_inspection_v07(first_v05, first_inventory)
            first_key = first_inventory["operations"][0]["operation_key"]

            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            second_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:01Z",
            )
            observation = second_v05["observation"]
            second_inventory = build_local_work_inventory(
                run_id=second_v05["run_id"],
                state_revision=observation["operator_state_revision"],
                snapshot_sha256=observation["snapshot_sha256"],
                logical_workspace_root=observation["logical_workspace_root"],
                operations=[{
                    "kind": "final_assembly_and_qa",
                    "route_family": "exact_natal",
                    "stage": None,
                    "source_action_ids": [retry_one],
                    "reason_code": "final_assembly_required",
                }],
                consumed_operation_keys=[first_key],
            )
            second = build_lifecycle_inspection_v07(second_v05, second_inventory)
            validate_local_work_progress(first, second)
            second_key = second_inventory["operations"][0]["operation_key"]

            state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            state["state_revision"] += 1
            (run_dir / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            third_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:02Z",
            )
            observation = third_v05["observation"]
            dropped_history = build_local_work_inventory(
                run_id=third_v05["run_id"],
                state_revision=observation["operator_state_revision"],
                snapshot_sha256=observation["snapshot_sha256"],
                logical_workspace_root=observation["logical_workspace_root"],
                operations=[{
                    "kind": "delivery_construction",
                    "route_family": "exact_natal",
                    "stage": None,
                    "source_action_ids": [retry_one],
                    "reason_code": "delivery_not_constructed",
                }],
                consumed_operation_keys=[second_key],
            )
            dropped = build_lifecycle_inspection_v07(third_v05, dropped_history)
            with self.assertRaisesRegex(ValueError, "not append-only"):
                validate_local_work_progress(second, dropped)

            with self.assertRaisesRegex(ValueError, "cannot be advertised again"):
                build_local_work_inventory(
                    run_id=third_v05["run_id"],
                    state_revision=observation["operator_state_revision"],
                    snapshot_sha256=observation["snapshot_sha256"],
                    logical_workspace_root=observation["logical_workspace_root"],
                    operations=[{
                        "kind": "provider_result_fan_in_and_retry_evaluation",
                        "route_family": "exact_natal",
                        "stage": "creative_retry",
                        "source_action_ids": [retry_one],
                        "reason_code": "provider_evidence_ingestion_required",
                    }],
                    consumed_operation_keys=[first_key, second_key],
                )

    def test_nonlocal_branch_refuses_inventory_and_ordinary_refuses_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            ordinary_v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            observation = ordinary_v05["observation"]
            empty = build_local_work_inventory(
                run_id=ordinary_v05["run_id"],
                state_revision=observation["operator_state_revision"],
                snapshot_sha256=observation["snapshot_sha256"],
                logical_workspace_root=observation["logical_workspace_root"],
                operations=[],
            )
            with self.assertRaisesRegex(ValueError, "lacks concrete local work"):
                build_lifecycle_inspection_v07(ordinary_v05, empty)

            pending_state = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            action = next(
                item for item in pending_state["spend_ledger"]["actions"]
                if item["action_id"] == retry_one
            )
            action["provider_reconciliation"]["last_outcome"] = "pending"
            action["provider_reconciliation"]["resume_not_before"] = "2099-01-01T00:00:00Z"
            (run_dir / "run.json").write_text(json.dumps(pending_state, indent=2) + "\n", encoding="utf-8")
            (run_dir / "public-run.json").write_text(json.dumps(public_run_state(pending_state), indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            pending = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            with self.assertRaisesRegex(ValueError, "Non-local"):
                build_lifecycle_inspection_v07(
                    pending, _inventory(pending, retry_one, "exact_natal")
                )

    def test_python_validator_closes_primitive_and_join_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            inventory = _inventory(v05, retry_one, "exact_natal")
            valid = build_lifecycle_inspection_v07(v05, inventory)
            mutations = []
            for mutate in (
                lambda item: item.update(run_id=""),
                lambda item: item.update(snapshot_sha256="x" * 64),
                lambda item: item["operations"][0].update(kind="whatever"),
                lambda item: item["operations"][0].update(source_action_ids=["hello"]),
                lambda item: item["operations"][0].update(basis_state_revision=999),
                lambda item: item["operations"][0].update(operation_key="work_" + "0" * 24),
                lambda item: item.update(consumed_operation_keys=["hello"]),
            ):
                changed = copy.deepcopy(inventory)
                mutate(changed)
                mutations.append(changed)
            for changed in mutations:
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    validate_local_work_inventory(changed)
            changed = copy.deepcopy(valid)
            changed["temporal_decision"]["local_work_inventory_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                validate_lifecycle_inspection_v07(changed)

    def test_json_schemas_are_packaged_and_accept_valid_contracts(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, retry_one, _retry_two = _workspace(Path(temporary), "exact_natal")
            v05 = inspect_lifecycle(
                run_dir, native_exclusive_access="declared",
                observed_at="2026-08-25T23:43:00Z",
            )
            inventory = _inventory(v05, retry_one, "exact_natal")
            v07 = build_lifecycle_inspection_v07(v05, inventory)
            inventory_schema = read_local_work_inventory_schema()
            lifecycle_schema = read_lifecycle_inspection_v07_schema()
            jsonschema.Draft202012Validator(inventory_schema).validate(inventory)
            jsonschema.Draft202012Validator(lifecycle_schema).validate(v07)

    def test_exchanged_inventory_fixture_is_strict_and_digest_valid(self) -> None:
        fixture = Path(__file__).parents[1] / "docs" / "sprints" / "2026" / "08" / (
            "20260825-post-fan-in-retry-matrix-contract-sprint1"
        ) / "fixtures" / "local-work-inventory.ordinary-resume.proposal.json"
        value = json.loads(fixture.read_text(encoding="utf-8"))
        validate_local_work_inventory(value)


if __name__ == "__main__":
    unittest.main()
