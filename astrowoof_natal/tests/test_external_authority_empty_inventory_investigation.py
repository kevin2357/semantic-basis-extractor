from __future__ import annotations

import json
import logging
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import write_workspace_snapshot
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter
from astrowoof_natal_authoring.lifecycle_contracts import (
    validate_lifecycle_inspection_v05,
)
from astrowoof_natal_authoring.external_authority import (
    validate_external_authority_request,
)
from astrowoof_natal.tests import test_external_authority_public as fixture_module  # noqa: E402


def api_external_authority_predicates(inspection: dict) -> list[str]:
    """Mirror the five API predicates collapsed into the incident message."""
    branch = inspection["execution_branch"]
    capacity = inspection["execution_capacity"]
    failures = []
    if branch["eligible_now"]:
        failures.append("eligible_now")
    if branch["reason_code"] != "spend_authorization_required":
        failures.append("branch_reason")
    if capacity["disposition"] != "await_external_authority":
        failures.append("capacity_disposition")
    if not branch["action_ids"]:
        failures.append("empty_action_ids")
    if branch["not_before"] is not None:
        failures.append("not_before")
    return failures


class TestExternalAuthorityEmptyInventoryInvestigation(unittest.TestCase):
    """Provider-free Slice 0 evidence; never opens the retained QA workspace."""

    helper = fixture_module.TestExternalAuthorityPublic()

    def test_real_inspection_satisfies_all_api_predicates_for_both_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for route in ("exact_natal", "bounded_natal"):
                with self.subTest(route=route):
                    run_dir = self.helper.make_wave_run(Path(temporary), route)
                    before_run = (run_dir / "run.json").read_bytes()
                    before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()

                    inspection = inspect_lifecycle(
                        run_dir,
                        native_exclusive_access="declared",
                        observed_at="2026-08-21T12:00:00Z",
                    )

                    self.assertEqual([], api_external_authority_predicates(inspection))
                    self.assertEqual(6, len(inspection["execution_branch"]["action_ids"]))
                    self.assertEqual(
                        inspection["external_authority_request"]["ordered_action_ids"],
                        inspection["execution_branch"]["action_ids"],
                    )
                    self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
                    self.assertEqual(
                        before_snapshot,
                        (run_dir / "workspace-snapshot.json").read_bytes(),
                    )

    def test_inadmissible_stored_wave_becomes_typed_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_wave_run(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["state"] = "AUTHORIZED"
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            before_run = run_json.read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()

            inspection = inspect_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )

            self.assertEqual("none", inspection["execution_branch"]["command"])
            self.assertEqual([], inspection["execution_branch"]["action_ids"])
            self.assertIsNone(inspection["external_authority_request"])
            self.assertEqual(
                "native_state_inconsistent",
                inspection["external_authority_refusal"]["reason_code"],
            )
            self.assertEqual(
                "retain_for_review", inspection["execution_capacity"]["disposition"],
            )
            self.assertEqual(before_run, run_json.read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes(),
            )

    def test_each_collapsed_api_predicate_is_distinguishable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            canonical = inspect_lifecycle(
                self.helper.make_wave_run(Path(temporary), "exact_natal"),
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            mutations = {
                "eligible_now": ("execution_branch", "eligible_now", True),
                "branch_reason": (
                    "execution_branch", "reason_code", "terminal_or_no_continuation",
                ),
                "capacity_disposition": (
                    "execution_capacity", "disposition", "continue_local_cycle",
                ),
                "empty_action_ids": ("execution_branch", "action_ids", []),
                "not_before": (
                    "execution_branch", "not_before", "2026-08-21T12:01:00Z",
                ),
            }
            for expected, (section, field, value) in mutations.items():
                with self.subTest(predicate=expected):
                    changed = deepcopy(canonical)
                    changed[section][field] = value
                    self.assertEqual([expected], api_external_authority_predicates(changed))
                    with self.assertRaises(ValueError):
                        validate_lifecycle_inspection_v05(changed)

    def test_all_approved_await_conditionals_are_native_invariants(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            canonical = inspect_lifecycle(
                self.helper.make_wave_run(Path(temporary), "exact_natal"),
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            mutations = (
                ("execution_branch", "eligible_now", True),
                ("execution_branch", "reason_code", "terminal_or_no_continuation"),
                ("execution_branch", "action_ids", []),
                ("execution_branch", "not_before", "2026-08-21T12:01:00Z"),
                ("execution_capacity", "disposition", "continue_local_cycle"),
                ("execution_capacity", "reason_code", "local_work_ready"),
                ("execution_capacity", "local_work_ready_now", True),
                ("execution_capacity", "resume_not_before", "2026-08-21T12:01:00Z"),
                ("document", "external_authority_request", None),
            )
            for section, field, value in mutations:
                with self.subTest(section=section, field=field):
                    changed = deepcopy(canonical)
                    if section == "document":
                        changed[field] = value
                    else:
                        changed[section][field] = value
                    with self.assertRaises(ValueError):
                        validate_lifecycle_inspection_v05(changed)

    def test_typed_refusal_requires_none_empty_and_retain_for_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_wave_run(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["state"] = "AUTHORIZED"
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            canonical = inspect_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            validate_lifecycle_inspection_v05(canonical)
            mutations = (
                ("execution_branch", "command", "ordinary_resume"),
                ("execution_branch", "eligible_now", True),
                ("execution_branch", "reason_code", "terminal_or_no_continuation"),
                ("execution_branch", "action_ids", ["paid_" + "a" * 24]),
                ("execution_branch", "not_before", "2026-08-21T12:01:00Z"),
                ("execution_capacity", "disposition", "continue_local_cycle"),
                ("execution_capacity", "reason_code", "local_work_ready"),
                ("execution_capacity", "local_work_ready_now", True),
                ("execution_capacity", "resume_not_before", "2026-08-21T12:01:00Z"),
            )
            for section, field, value in mutations:
                with self.subTest(section=section, field=field):
                    changed = deepcopy(canonical)
                    changed[section][field] = value
                    with self.assertRaises(ValueError):
                        validate_lifecycle_inspection_v05(changed)

    def test_success_and_refusal_emit_safe_typed_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            success_dir = self.helper.make_wave_run(root, "exact_natal")
            success_events: list[dict] = []
            success_emitter = ExecutionEventEmitter(
                release="test", sink=success_events.append,
            )
            inspect_lifecycle(
                success_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
                event_emitter=success_emitter,
            )
            self.assertEqual(
                ["external_authority.request_selected", "lifecycle.branch_selected"],
                [event["event_name"] for event in success_events],
            )
            self.assertEqual(6, success_events[-1]["data"]["branch_action_count"])
            self.assertEqual(0, success_events[-1]["data"]["failed_predicate_count"])

            refusal_dir = self.helper.make_wave_run(root, "bounded_natal")
            run_json = refusal_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            state["spend_ledger"]["actions"][0]["state"] = "AUTHORIZED"
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(refusal_dir)
            refusal_events: list[dict] = []
            inspect_lifecycle(
                refusal_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
                event_emitter=ExecutionEventEmitter(
                    release="test", sink=refusal_events.append,
                ),
            )
            self.assertEqual(
                ["external_authority.refused", "lifecycle.branch_selected"],
                [event["event_name"] for event in refusal_events],
            )
            self.assertEqual(
                "request_construction", refusal_events[0]["data"]["category"],
            )
            self.assertFalse(refusal_events[-1]["data"]["request_present"])
            self.assertTrue(refusal_events[-1]["data"]["refusal_present"])

    def test_invalid_constructed_branch_emits_sorted_predicate_diagnostic(self) -> None:
        import astrowoof_natal_authoring.lifecycle as lifecycle

        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_wave_run(Path(temporary), "exact_natal")
            before_run = (run_dir / "run.json").read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()
            events: list[dict] = []
            original = lifecycle._execution_branch

            def contradictory(*args: object, **kwargs: object) -> dict:
                branch = original(*args, **kwargs)
                branch["reason_code"] = "terminal_or_no_continuation"
                branch["not_before"] = "2026-08-21T12:01:00Z"
                return branch

            with (
                patch.object(lifecycle, "_execution_branch", side_effect=contradictory),
                self.assertLogs(lifecycle.logger, level=logging.INFO) as captured,
                self.assertRaises(ValueError),
            ):
                inspect_lifecycle(
                    run_dir,
                    native_exclusive_access="declared",
                    observed_at="2026-08-21T12:00:00Z",
                    event_emitter=ExecutionEventEmitter(
                        release="test", sink=events.append,
                    ),
                )
            failed = events[-1]
            self.assertEqual("execution.failed", failed["event_name"])
            self.assertEqual(
                ["branch_not_before", "branch_reason_code"],
                failed["data"]["failed_predicates"],
            )
            self.assertIn(
                "failed_predicates=branch_not_before,branch_reason_code",
                "\n".join(captured.output),
            )
            self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes(),
            )

    def test_diagnostic_sink_failure_and_protected_sentinel_cannot_change_result(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_wave_run(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            sentinel = "PROTECTED-BIRTH-PAYLOAD-SENTINEL-9d6f"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            state["protected_test_sentinel"] = sentinel
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            before_run = run_json.read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()

            def failed_sink(_event: dict) -> None:
                raise RuntimeError("injected diagnostic sink failure")

            emitter = ExecutionEventEmitter(release="test", sink=failed_sink)
            with self.assertLogs(level=logging.INFO) as captured:
                inspection = inspect_lifecycle(
                    run_dir,
                    native_exclusive_access="declared",
                    observed_at="2026-08-21T12:00:00Z",
                    event_emitter=emitter,
                )
            self.assertEqual("await_external_authority", inspection[
                "execution_branch"
            ]["command"])
            self.assertEqual(2, emitter.stats.dropped)
            self.assertNotIn(sentinel, json.dumps(inspection))
            self.assertNotIn(sentinel, "\n".join(captured.output))
            self.assertEqual(before_run, run_json.read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes(),
            )

    def test_ordinary_action_set_is_nonempty_lexical_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_ordinary_run(Path(temporary))
            before_run = (run_dir / "run.json").read_bytes()
            before_snapshot = (run_dir / "workspace-snapshot.json").read_bytes()
            inspection = inspect_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            request = inspection["external_authority_request"]
            self.assertEqual("ordinary_action_set", request["request_kind"])
            self.assertEqual(2, request["action_count"])
            self.assertEqual(
                sorted(request["ordered_action_ids"]), request["ordered_action_ids"],
            )
            self.assertEqual(
                request["ordered_action_ids"], inspection["execution_branch"]["action_ids"],
            )
            self.assertEqual(before_run, (run_dir / "run.json").read_bytes())
            self.assertEqual(
                before_snapshot, (run_dir / "workspace-snapshot.json").read_bytes(),
            )

    def test_no_prepared_actions_never_selects_external_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.helper.make_ordinary_run(Path(temporary))
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            for action in state["spend_ledger"]["actions"]:
                action["state"] = "DENIED_PROVIDERLESS"
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            inspection = inspect_lifecycle(
                run_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            self.assertNotEqual(
                "await_external_authority", inspection["execution_branch"]["command"],
            )
            self.assertIsNone(inspection["external_authority_request"])

    def test_public_request_validator_refuses_inventory_and_binding_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            canonical = inspect_lifecycle(
                self.helper.make_wave_run(Path(temporary), "exact_natal"),
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )["external_authority_request"]
            mutations = []
            empty = deepcopy(canonical)
            empty["ordered_actions"] = []
            empty["ordered_action_ids"] = []
            empty["action_count"] = 0
            mutations.append(empty)
            duplicate = deepcopy(canonical)
            duplicate["ordered_actions"][1] = deepcopy(duplicate["ordered_actions"][0])
            duplicate["ordered_action_ids"][1] = duplicate["ordered_action_ids"][0]
            mutations.append(duplicate)
            unknown = deepcopy(canonical)
            unknown["ordered_action_ids"][0] = "paid_" + "f" * 24
            mutations.append(unknown)
            binding = deepcopy(canonical)
            binding["ordered_actions"][0]["binding"]["maximum_output_tokens"] += 1
            mutations.append(binding)
            for changed in mutations:
                with self.assertRaises(ValueError):
                    validate_external_authority_request(changed)

    def test_outer_request_identity_mutations_fail_native_join(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            canonical = inspect_lifecycle(
                self.helper.make_wave_run(Path(temporary), "exact_natal"),
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            mutations = []
            run_id = deepcopy(canonical)
            run_id["run_id"] = "different-native-run"
            mutations.append(run_id)
            observation = deepcopy(canonical)
            observation["observation"]["operator_state_revision"] += 1
            mutations.append(observation)
            ordered = deepcopy(canonical)
            ordered["execution_branch"]["action_ids"] = list(reversed(
                ordered["execution_branch"]["action_ids"]
            ))
            mutations.append(ordered)
            digest = deepcopy(canonical)
            digest["external_authority_request"][
                "external_authority_request_sha256"
            ] = "f" * 64
            mutations.append(digest)
            for changed in mutations:
                with self.assertRaises(ValueError):
                    validate_lifecycle_inspection_v05(changed)

    def test_incomplete_snapshot_and_writer_race_never_publish_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            incomplete_dir = self.helper.make_wave_run(root, "exact_natal")
            (incomplete_dir / "request-1.json").unlink()
            incomplete = inspect_lifecycle(
                incomplete_dir,
                native_exclusive_access="declared",
                observed_at="2026-08-21T12:00:00Z",
            )
            self.assertEqual("none", incomplete["execution_branch"]["command"])
            self.assertIsNone(incomplete["external_authority_request"])
            self.assertIn("snapshot_incomplete_or_invalid", incomplete["review_reasons"])

            race_dir = self.helper.make_wave_run(root, "bounded_natal")
            raced = inspect_lifecycle(
                race_dir,
                native_exclusive_access="not_established",
                observed_at="2026-08-21T12:00:00Z",
            )
            self.assertEqual("none", raced["execution_branch"]["command"])
            self.assertIsNone(raced["external_authority_request"])
            self.assertIn("writer_race_possible", raced["review_reasons"])


if __name__ == "__main__":
    unittest.main()
