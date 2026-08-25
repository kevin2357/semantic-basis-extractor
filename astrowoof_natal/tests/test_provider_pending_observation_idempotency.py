from __future__ import annotations

import copy
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from astrowoof_natal_authoring.lifecycle import inspect_lifecycle  # noqa: E402
from astrowoof_natal_authoring.reconciliation import (  # noqa: E402
    reconcile_provider_cycle,
)
from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    canonical_contract_json,
)
from astrowoof_natal_authoring.temporal_lifecycle import (  # noqa: E402
    build_external_authority_request_v2,
    build_lifecycle_inspection_v06,
    canonical_utc_instant,
    temporal_transition_errors,
    validate_lifecycle_inspection_v06,
    validate_external_authority_request_v2_against_inspection,
    validate_temporal_transition,
    inspect_temporal_lifecycle,
    read_temporal_external_authority_schema,
    read_temporal_lifecycle_schema,
)
import test_provider_pending_capacity as _fixture  # noqa: E402
from test_external_authority_public import TestExternalAuthorityPublic  # noqa: E402


def changed_paths(left: object, right: object, prefix: str = "") -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        paths: list[str] = []
        for key in sorted(set(left) | set(right)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                paths.append(path)
            else:
                paths.extend(changed_paths(left[key], right[key], path))
        return paths
    if isinstance(left, list) and isinstance(right, list):
        paths = []
        if len(left) != len(right):
            return [prefix]
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            paths.extend(
                changed_paths(left_item, right_item, f"{prefix}[{index}]")
            )
        return paths
    return [] if left == right else [prefix]


class TestProviderPendingObservationIdempotencySlice0(unittest.TestCase):
    def materialize(self, root: Path) -> None:
        # Reuse is deliberately test-only. Installed-wheel qualification must
        # later use packaged/public fixtures rather than importing test helpers.
        _fixture.TestProviderPendingCapacityBaseline().materialize(
            root, action_count=6
        )

    def test_one_checkpoint_legally_projects_not_due_then_due(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = _fixture.hashes(root)

            not_due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            after_not_due = _fixture.hashes(root)
            due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )

            self.assertEqual(before, after_not_due)
            self.assertEqual(before, _fixture.hashes(root))
            self.assertEqual(
                not_due["observation"]["snapshot_sha256"],
                due["observation"]["snapshot_sha256"],
            )
            self.assertEqual(
                not_due["observation"]["operator_state_revision"],
                due["observation"]["operator_state_revision"],
            )
            self.assertEqual(
                "release_until_due",
                not_due["execution_capacity"]["disposition"],
            )
            self.assertEqual(
                "continue_local_cycle",
                due["execution_capacity"]["disposition"],
            )
            self.assertFalse(not_due["execution_branch"]["eligible_now"])
            self.assertTrue(due["execution_branch"]["eligible_now"])
            self.assertEqual(6, len(not_due["execution_branch"]["action_ids"]))
            self.assertEqual(4, len(due["execution_branch"]["action_ids"]))
            self.assertEqual(
                due["provider_custody"]["next_due_action_ids"],
                due["execution_branch"]["action_ids"],
            )

            stable_not_due = copy.deepcopy(not_due)
            stable_due = copy.deepcopy(due)
            stable_not_due["observation"].pop("observed_at")
            stable_due["observation"].pop("observed_at")
            for document in (stable_not_due, stable_due):
                document["action_inventory"]["observation"].pop(
                    "observed_at", None
                )
                document.pop("execution_capacity")
                document.pop("execution_branch")
                document["provider_custody"]["next_due_action_ids"] = []
            self.assertEqual(stable_not_due, stable_due)

    def test_same_checkpoint_and_time_is_exact_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = _fixture.hashes(root)
            first = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            second = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            self.assertEqual(first, second)
            self.assertEqual(before, _fixture.hashes(root))

    def test_changed_paths_are_only_time_relative_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            not_due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:10:00Z",
            )
            due = inspect_lifecycle(
                root,
                native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            self.assertEqual(
                [
                    "action_inventory.observation.observed_at",
                    "execution_branch.action_ids",
                    "execution_branch.eligible_now",
                    "execution_branch.not_before",
                    "execution_branch.reason_code",
                    "execution_capacity.disposition",
                    "execution_capacity.local_work_ready_now",
                    "execution_capacity.reason_code",
                    "execution_capacity.resume_not_before",
                    "observation.observed_at",
                    "provider_custody.next_due_action_ids",
                ],
                changed_paths(not_due, due),
                json.dumps(changed_paths(not_due, due), indent=2),
            )


class TestTemporalLifecycleContractSlice1(unittest.TestCase):
    def materialize(self, root: Path) -> None:
        _fixture.TestProviderPendingCapacityBaseline().materialize(
            root, action_count=6
        )

    def authority_inspection(self, root: Path, observed_at: str) -> dict:
        run_dir = TestExternalAuthorityPublic().make_ordinary_run(root)
        return inspect_temporal_lifecycle(
            run_dir, native_exclusive_access="declared", observed_at=observed_at,
        )

    def inspections(self, root: Path) -> tuple[dict, dict]:
        not_due = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="2026-08-15T20:10:00Z",
        )
        due = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="2026-08-15T20:30:00Z",
        )
        return (
            build_lifecycle_inspection_v06(not_due),
            build_lifecycle_inspection_v06(due),
        )

    @staticmethod
    def rehash_decision(value: dict) -> None:
        value["temporal_decision_sha256"] = hashlib.sha256(
            canonical_contract_json(value["temporal_decision"]).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def rehash_all(value: dict) -> None:
        value["checkpoint_basis_sha256"] = hashlib.sha256(
            canonical_contract_json(value["checkpoint_basis"]).encode("utf-8")
        ).hexdigest()
        value["temporal_decision"]["checkpoint_basis_sha256"] = value[
            "checkpoint_basis_sha256"
        ]
        TestTemporalLifecycleContractSlice1.rehash_decision(value)

    @staticmethod
    def rehash_request(value: dict) -> None:
        body = {
            key: item for key, item in value.items()
            if key != "external_authority_request_sha256"
        }
        value["external_authority_request_sha256"] = hashlib.sha256(
            canonical_contract_json(body).encode("utf-8")
        ).hexdigest()

    def test_basis_is_stable_and_due_subset_is_temporal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            not_due, due = self.inspections(root)
            self.assertEqual(
                not_due["checkpoint_basis_sha256"], due["checkpoint_basis_sha256"]
            )
            self.assertEqual(not_due["checkpoint_basis"], due["checkpoint_basis"])
            self.assertNotIn("observed_at", not_due["checkpoint_basis"]["observation"])
            self.assertNotIn(
                "observation", not_due["checkpoint_basis"]["action_inventory"]
            )
            self.assertNotIn(
                "next_due_action_ids", not_due["checkpoint_basis"]["provider_custody"]
            )
            self.assertEqual([], not_due["temporal_decision"]["due_action_ids"])
            self.assertEqual(4, len(due["temporal_decision"]["due_action_ids"]))
            validate_temporal_transition(not_due, due)

    def test_same_basis_and_time_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            source = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            first = build_lifecycle_inspection_v06(source)
            second = build_lifecycle_inspection_v06(source)
            self.assertEqual(first, second)
            validate_temporal_transition(first, second)

    def test_canonical_utc_normalizes_equivalent_offset(self) -> None:
        self.assertEqual(
            "2026-08-15T20:30:00Z",
            canonical_utc_instant("2026-08-15T14:30:00-06:00"),
        )
        with self.assertRaisesRegex(ValueError, "whole-second"):
            canonical_utc_instant("2026-08-15T20:30:00.1Z")

    def test_validator_refuses_noncanonical_equivalent_spelling(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            _, due = self.inspections(root)
            due["temporal_decision"]["observed_at"] = (
                "2026-08-15T14:30:00-06:00"
            )
            self.rehash_decision(due)
            with self.assertRaisesRegex(ValueError, "not canonical UTC"):
                validate_lifecycle_inspection_v06(due)

    def test_backward_time_and_due_to_not_due_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            not_due, due = self.inspections(root)
            self.assertEqual(
                ["clock_regression", "due_to_not_due", "eligibility_regression"],
                temporal_transition_errors(due, not_due),
            )
            with self.assertRaisesRegex(ValueError, "clock_regression"):
                validate_temporal_transition(due, not_due)

    def test_authority_request_digest_is_stable_across_observation_time(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            not_due = self.authority_inspection(root, "2026-08-20T14:01:00Z")
            due = inspect_temporal_lifecycle(
                root / "ordinary", native_exclusive_access="declared",
                observed_at="2026-08-20T14:02:00Z",
            )
            validate_lifecycle_inspection_v06(not_due)
            validate_lifecycle_inspection_v06(due)
            self.assertEqual(
                build_external_authority_request_v2(not_due),
                build_external_authority_request_v2(due),
            )

    def test_packaged_schema_accepts_v06_document(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            _, due = self.inspections(root)
            schema_path = (
                ROOT / "src" / "astrowoof_natal_authoring" / "resources"
                / "contracts" / "temporal-lifecycle-contracts.v1.schema.json"
            )
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator(schema).validate(due)

    def test_public_import_export_smoke(self) -> None:
        import astrowoof_natal_authoring as public

        self.assertIs(
            build_external_authority_request_v2,
            public.build_external_authority_request_v2,
        )
        self.assertIs(
            validate_external_authority_request_v2_against_inspection,
            public.validate_external_authority_request_v2_against_inspection,
        )

    def test_rehashed_malformed_basis_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            _, due = self.inspections(root)
            mutations = (
                ("route", lambda item: item["checkpoint_basis"]["native_route"].__setitem__("route_family", "synastry")),
                ("provider", lambda item: item["checkpoint_basis"]["provider_custody"]["actions"][0].__setitem__("provider_operation_id", "resp_wrong")),
                ("binding", lambda item: item["checkpoint_basis"]["action_inventory"]["actions"][0]["binding"].__setitem__("stage", "polish")),
                ("authority", lambda item: item["checkpoint_basis"]["consumer_authority"].__setitem__("action_count", 99)),
            )
            for label, mutate in mutations:
                with self.subTest(label=label):
                    changed = copy.deepcopy(due)
                    mutate(changed)
                    self.rehash_all(changed)
                    with self.assertRaises(ValueError):
                        validate_lifecycle_inspection_v06(changed)

    def test_v2_request_must_join_strict_inspection_and_bindings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            due = self.authority_inspection(root, "2026-08-20T14:01:00Z")
            request = build_external_authority_request_v2(due)
            validate_external_authority_request_v2_against_inspection(request, due)

            changed = copy.deepcopy(due)
            changed["checkpoint_basis"]["action_inventory"]["actions"][0][
                "binding"
            ]["model"] = "different-model"
            self.rehash_all(changed)
            validate_lifecycle_inspection_v06(changed)
            with self.assertRaisesRegex(ValueError, "checkpoint_basis_sha256"):
                validate_external_authority_request_v2_against_inspection(
                    request, changed
                )

    def test_python_validators_enforce_schema_primitives_without_jsonschema(self) -> None:
        from astrowoof_natal_authoring.temporal_lifecycle import (
            validate_external_authority_request_v2,
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            due = self.authority_inspection(root, "2026-08-20T14:01:00Z")
            request = build_external_authority_request_v2(due)

            for field, bad_value, message in (
                ("run_id", None, "run_id"),
                ("request_kind", "whatever", "kind"),
                ("ordered_action_ids", ["hello"], "action inventory"),
                ("checkpoint_basis_sha256", "A" * 64, "checkpoint digest"),
            ):
                with self.subTest(request_field=field):
                    changed_request = copy.deepcopy(request)
                    changed_request[field] = bad_value
                    self.rehash_request(changed_request)
                    with self.assertRaisesRegex(ValueError, message):
                        validate_external_authority_request_v2(changed_request)

            changed_run = copy.deepcopy(due)
            changed_run["run_id"] = None
            with self.assertRaisesRegex(ValueError, "run_id"):
                validate_lifecycle_inspection_v06(changed_run)

            changed_authority = copy.deepcopy(due)
            changed_authority["checkpoint_basis"]["external_authority_state"][
                "ordered_action_ids"
            ] = ["hello"]
            self.rehash_all(changed_authority)
            with self.assertRaisesRegex(ValueError, "request is invalid"):
                validate_lifecycle_inspection_v06(changed_authority)

            changed_action = copy.deepcopy(due)
            changed_action["checkpoint_basis"]["action_inventory"]["actions"][0][
                "action_id"
            ] = "hello"
            self.rehash_all(changed_action)
            with self.assertRaisesRegex(ValueError, "action identity"):
                validate_lifecycle_inspection_v06(changed_action)


class TestTemporalLifecycleReconciliationSlice2(unittest.TestCase):
    def materialize(self, root: Path) -> None:
        _fixture.TestProviderPendingCapacityBaseline().materialize(
            root, action_count=3
        )

    def test_real_reconciliation_creates_new_basis_and_never_retrieves_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = build_lifecycle_inspection_v06(inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:00Z",
            ))
            calls: list[str] = []

            def retrieve(provider_id: str, _timeout: float) -> dict:
                calls.append(provider_id)
                return {"id": provider_id, "status": "completed", "output": []}

            reconciled = reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z", retrieve=retrieve,
            )
            self.assertEqual("progressed_local", reconciled["outcome"])
            self.assertEqual(3, len(calls))
            after = build_lifecycle_inspection_v06(inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:01Z",
            ))
            self.assertNotEqual(
                before["checkpoint_basis_sha256"], after["checkpoint_basis_sha256"]
            )
            self.assertEqual(
                ["checkpoint_basis_changed"],
                temporal_transition_errors(before, after),
            )
            self.assertTrue(all(
                item["custody_classification"] == "completed_provider_evidence"
                for item in after["checkpoint_basis"]["provider_custody"]["actions"]
            ))
            self.assertEqual([], after["temporal_decision"]["due_action_ids"])

            second_calls: list[str] = []
            second = reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:02Z",
                retrieve=lambda provider_id, _timeout: second_calls.append(provider_id)
                or {"id": provider_id, "status": "completed", "output": []},
            )
            self.assertEqual([], second_calls)
            self.assertIn(second["outcome"], {"progressed_local", "terminal"})
            self.assertEqual(3, len(calls))

    def test_fresh_process_reconstructs_exact_new_basis(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            reconcile_provider_cycle(
                root, observed_at="2026-08-15T20:18:00Z",
                retrieve=lambda provider_id, _timeout: {
                    "id": provider_id, "status": "completed", "output": []
                },
            )
            local = build_lifecycle_inspection_v06(inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:01Z",
            ))
            code = (
                "import json,sys;from pathlib import Path;"
                "from astrowoof_natal_authoring.lifecycle import inspect_lifecycle;"
                "from astrowoof_natal_authoring.temporal_lifecycle import "
                "build_lifecycle_inspection_v06;"
                "print(json.dumps(build_lifecycle_inspection_v06(inspect_lifecycle("
                "Path(sys.argv[1]),native_exclusive_access='declared',"
                "observed_at='2026-08-15T20:18:01Z')),sort_keys=True))"
            )
            completed = subprocess.run(
                [sys.executable, "-c", code, str(root)],
                text=True, capture_output=True, check=True,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            restored = json.loads(completed.stdout)
            self.assertEqual(local, restored)

    def test_rehashed_reordered_native_due_subset_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            due = build_lifecycle_inspection_v06(inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:18:00Z",
            ))
            due["temporal_decision"]["due_action_ids"].reverse()
            TestTemporalLifecycleContractSlice1.rehash_decision(due)
            with self.assertRaisesRegex(ValueError, "native selection"):
                validate_lifecycle_inspection_v06(due)


class TestTemporalLifecycleCrossRouteSlice3(unittest.TestCase):
    def materialize_route(self, root: Path, route: str) -> None:
        batch = route.endswith("batch")
        _fixture.TestProviderPendingCapacityBaseline().materialize(
            root, action_count=1 if batch else 3
        )
        state = json.loads((root / "run.json").read_text(encoding="utf-8"))
        if route.startswith("bounded"):
            state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v2"
            state["route"] = "bounded_natal.v2"
        if batch:
            action = state["spend_ledger"]["actions"][0]
            action["binding"]["service_level"] = "batch"
            action["provider"]["kind"] = "batch"
            action["provider_reconciliation"]["resume_not_before"] = (
                "2026-08-15T20:15:00Z"
            )
            native_ref = (
                "bounded_natal.v2:batch-round-001"
                if route == "bounded_batch" else "batch-round-001"
            )
            action["binding"]["route"] = native_ref
            state["batch_service"] = {"rounds": [{
                "round_number": 1, "batch_id": action["provider"]["id"],
            }]}
        elif route == "bounded_interactive":
            for index, action in enumerate(state["spend_ledger"]["actions"], 1):
                action["binding"]["route"] = (
                    f"bounded_natal.v2:authoring_initial:{index}"
                )
        (root / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        from astrowoof_natal_authoring.closure import write_workspace_snapshot
        write_workspace_snapshot(root)

    def test_four_supported_routes_share_temporal_contract(self) -> None:
        for route in (
            "exact_interactive", "exact_batch", "bounded_interactive",
            "bounded_batch",
        ):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                self.materialize_route(root, route)
                not_due = build_lifecycle_inspection_v06(inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-15T20:10:00Z",
                ))
                due = build_lifecycle_inspection_v06(inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-15T20:30:00Z",
                ))
                self.assertEqual(
                    not_due["checkpoint_basis_sha256"],
                    due["checkpoint_basis_sha256"],
                )
                self.assertEqual(
                    "bounded_natal" if route.startswith("bounded")
                    else "exact_natal",
                    due["checkpoint_basis"]["native_route"]["route_family"],
                )
                self.assertTrue(due["temporal_decision"]["eligible_now"])
                validate_temporal_transition(not_due, due)

    def test_legacy_bounded_batch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize_route(root, "bounded_batch")
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            state["route_contract"] = "astrowoof.bounded_natal.authoring_run.v1"
            state["route"] = "bounded_natal.v1"
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            from astrowoof_natal_authoring.closure import write_workspace_snapshot
            write_workspace_snapshot(root)
            inspection = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            self.assertEqual(
                "unsupported_retain_capacity",
                inspection["execution_capacity"]["disposition"],
            )

    def test_interactive_optional_stages_project_and_batch_optional_fails_closed(self) -> None:
        optional = ("polish", "qualitative_critic", "qualitative_candidate")
        for route in ("exact_interactive", "bounded_interactive"):
            for stage in optional:
                with self.subTest(route=route, stage=stage), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary).resolve()
                    self.materialize_route(root, route)
                    state = json.loads((root / "run.json").read_text(encoding="utf-8"))
                    profile_key = "optional_stages" if route.startswith("bounded") else "qa"
                    state["authoring_profile"] = {profile_key: {
                        "polish": True, "qualitative_critic": True,
                        "qualitative_candidate": True,
                    }}
                    for action in state["spend_ledger"]["actions"]:
                        action["binding"]["stage"] = stage
                    (root / "run.json").write_text(
                        json.dumps(state, indent=2) + "\n", encoding="utf-8"
                    )
                    from astrowoof_natal_authoring.closure import write_workspace_snapshot
                    write_workspace_snapshot(root)
                    projected = build_lifecycle_inspection_v06(inspect_lifecycle(
                        root, native_exclusive_access="declared",
                        observed_at="2026-08-15T20:10:00Z",
                    ))
                    self.assertEqual(
                        "release_until_due",
                        projected["temporal_decision"]["capacity_disposition"],
                    )
        for route in ("exact_batch", "bounded_batch"):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                self.materialize_route(root, route)
                state = json.loads((root / "run.json").read_text(encoding="utf-8"))
                state["spend_ledger"]["actions"][0]["binding"]["stage"] = "polish"
                (root / "run.json").write_text(
                    json.dumps(state, indent=2) + "\n", encoding="utf-8"
                )
                from astrowoof_natal_authoring.closure import write_workspace_snapshot
                write_workspace_snapshot(root)
                inspection = inspect_lifecycle(
                    root, native_exclusive_access="declared",
                    observed_at="2026-08-15T20:30:00Z",
                )
                self.assertEqual(
                    "unsupported_retain_capacity",
                    inspection["execution_capacity"]["disposition"],
                )


class TestTemporalLifecyclePublicSurfaceSlice4(unittest.TestCase):
    def materialize(self, root: Path) -> None:
        _fixture.TestProviderPendingCapacityBaseline().materialize(
            root, action_count=6
        )

    def test_public_reader_is_explicit_time_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            before = _fixture.hashes(root)
            value = inspect_temporal_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            self.assertEqual(
                "astrowoof.authoring_lifecycle_inspection.v0.6",
                value["schema_version"],
            )
            self.assertEqual(before, _fixture.hashes(root))
            self.assertEqual(4, len(value["temporal_decision"]["due_action_ids"]))

    def test_cli_temporal_inspection_matches_public_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            expected = inspect_temporal_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            completed = subprocess.run(
                [
                    sys.executable, "-m",
                    "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir", str(root), "inspect-temporal",
                    "--native-exclusive-access", "declared",
                    "--observed-at", "2026-08-15T20:30:00Z",
                ],
                text=True, capture_output=True, check=True,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(expected, json.loads(completed.stdout))

    def test_cli_requires_explicit_trusted_time(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.materialize(root)
            completed = subprocess.run(
                [
                    sys.executable, "-m",
                    "astrowoof_natal_authoring.cli.lifecycle",
                    "--run-dir", str(root), "inspect-temporal",
                    "--native-exclusive-access", "declared",
                ],
                text=True, capture_output=True, check=False,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("--observed-at", completed.stderr)

    def test_packaged_schema_readers_are_public_and_closed(self) -> None:
        lifecycle_schema = read_temporal_lifecycle_schema()
        authority_schema = read_temporal_external_authority_schema()
        self.assertEqual(
            "astrowoof.temporal_lifecycle_contracts.v1",
            lifecycle_schema["$id"],
        )
        self.assertFalse(lifecycle_schema["additionalProperties"])
        self.assertEqual(
            "astrowoof.temporal_external_authority_contracts.v2",
            authority_schema["$id"],
        )
        self.assertFalse(authority_schema["additionalProperties"])

    def test_public_reader_definitions_are_singular(self) -> None:
        module_path = (
            ROOT / "src" / "astrowoof_natal_authoring" / "temporal_lifecycle.py"
        )
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        names = [
            node.name for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        for name in (
            "inspect_temporal_lifecycle",
            "read_temporal_lifecycle_schema",
            "read_temporal_external_authority_schema",
        ):
            self.assertEqual(1, names.count(name), name)


if __name__ == "__main__":
    unittest.main()
