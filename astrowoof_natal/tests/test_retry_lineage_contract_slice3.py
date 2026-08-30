from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.closure import public_run_state, write_workspace_snapshot
from astrowoof_natal_authoring.post_fan_in_contracts import (
    build_lifecycle_inspection_v07, build_local_work_inventory,
)
from astrowoof_natal_authoring.retry_lineage_contracts import (
    build_lifecycle_inspection_v08, build_retry_lineage_inventory,
    derive_retry_attempt_key, read_retry_lineage_schema,
    validate_lifecycle_inspection_v08, validate_retry_lineage_inventory,
)
from astrowoof_natal.tests.test_provider_pending_observation_idempotency import (
    TestProviderPendingObservationIdempotencySlice0,
)


def _action(number: int, *, binding: str = "a", request: str = "b",
            state: str = "PREPARED", provider_id: str | None = None) -> dict:
    return {
        "native_run_id": "retry-contract-run", "route_family": "exact_natal",
        "stage": "creative_retry", "pass_id": "pass-6", "attempt_number": 3,
        "action_id": f"paid_{number:024x}", "binding_sha256": binding * 64,
        "request_sha256": request * 64, "state": state,
        "provider_mechanism": "response", "provider_operation_id": provider_id,
        "pass_attempt_pointer": "passes/pass-6/attempts/3",
    }


def _rehash(value: dict) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


class RetryLineageSlice3ContractTests(unittest.TestCase):
    def test_attempt_key_excludes_request_and_binding_evidence(self) -> None:
        first, changed = _action(1), _action(2, binding="c", request="d")
        coordinate_names = (
            "native_run_id", "route_family", "stage", "pass_id", "attempt_number",
        )
        self.assertEqual(
            derive_retry_attempt_key(**{key: first[key] for key in coordinate_names}),
            derive_retry_attempt_key(**{key: changed[key] for key in coordinate_names}),
        )
        inventory = build_retry_lineage_inventory(
            run_id="retry-contract-run", actions=[first, changed],
        )
        self.assertEqual("conflict", inventory["status"])
        self.assertFalse(inventory["forward_dispatch_permitted"])
        self.assertIn("request_binding_conflict", inventory["attempts"][0]["reason_codes"])

    def test_python_validator_is_closed_and_recomputes_semantics(self) -> None:
        inventory = build_retry_lineage_inventory(
            run_id="retry-contract-run", actions=[_action(1)],
        )
        for mutation in ("route", "action", "digest", "extra"):
            with self.subTest(mutation=mutation):
                bad = copy.deepcopy(inventory)
                if mutation == "route":
                    bad["attempts"][0]["coordinates"]["route_family"] = "whatever"
                elif mutation == "action":
                    bad["attempts"][0]["actions"][0]["action_id"] = "hello"
                elif mutation == "digest":
                    bad["attempts"][0]["actions"][0]["request_sha256"] = "z" * 64
                else:
                    bad["extra"] = True
                bad["inventory_sha256"] = _rehash({
                    key: value for key, value in bad.items()
                    if key != "inventory_sha256"
                })
                with self.assertRaises(ValueError):
                    validate_retry_lineage_inventory(bad)

    def test_mixed_custody_conflict_requires_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            TestProviderPendingObservationIdempotencySlice0().materialize(root)
            state = json.loads((root / "run.json").read_text(encoding="utf-8"))
            for index, action in enumerate(state["spend_ledger"]["actions"]):
                action["attempt"] = 3
                action["pass_id"] = "pass-6" if index < 2 else f"pass-{index + 1}"
                action["binding"]["stage"] = "creative_retry"
                action["binding"]["route"] = (
                    "pass-6:attempt-003" if index < 2
                    else f"pass-{index + 1}:attempt-003"
                )
                action["binding"]["request_sha256"] = f"{index + 1:x}" * 64
            state["state_revision"] += 1
            (root / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8",
            )
            (root / "public-run.json").write_text(
                json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8",
            )
            write_workspace_snapshot(root)
            v05 = inspect_lifecycle(
                root, native_exclusive_access="declared",
                observed_at="2026-08-15T20:30:00Z",
            )
            observation = v05["observation"]
            empty = build_local_work_inventory(
                run_id=v05["run_id"], state_revision=observation["operator_state_revision"],
                snapshot_sha256=observation["snapshot_sha256"],
                logical_workspace_root=observation["logical_workspace_root"], operations=[],
            )
            v07 = build_lifecycle_inspection_v07(v05, empty)
            lineage_actions = []
            for source in v05["action_inventory"]["actions"]:
                pass_id, attempt = source["route"].rsplit(":attempt-", 1)
                lineage_actions.append({
                    "native_run_id": v05["run_id"], "route_family": "exact_natal",
                    "stage": "creative_retry", "pass_id": pass_id,
                    "attempt_number": int(attempt), "action_id": source["action_id"],
                    "binding_sha256": _rehash(source["binding"]),
                    "request_sha256": source["binding"]["request_sha256"],
                    "state": source["state"], "provider_mechanism": "response",
                    "provider_operation_id": source["provider_operation_id"],
                    "pass_attempt_pointer": f"passes/{pass_id}/attempts/{int(attempt)}",
                })
            lineage = build_retry_lineage_inventory(
                run_id=v05["run_id"], actions=lineage_actions,
            )
            v08 = build_lifecycle_inspection_v08(v07, lineage)
            self.assertEqual("provider_reconciliation_cycle", v08["temporal_decision"]["selected_command"])
            self.assertFalse(lineage["forward_dispatch_permitted"])
            self.assertTrue(lineage["reconciliation_permitted"])

            bad = copy.deepcopy(v08)
            bad["temporal_decision"].update({
                "selected_command": "none", "eligible_now": False,
                "capacity_disposition": "retain_for_review",
                "local_work_ready_now": False, "due_action_ids": [], "not_before": None,
            })
            bad["temporal_decision_sha256"] = _rehash(bad["temporal_decision"])
            with self.assertRaises(ValueError):
                validate_lifecycle_inspection_v08(bad)

            for mutation in ("missing", "fabricated", "provider"):
                with self.subTest(mutation=mutation):
                    malformed_actions = copy.deepcopy(lineage_actions)
                    if mutation == "missing":
                        malformed_actions.pop()
                    elif mutation == "fabricated":
                        malformed_actions[0]["action_id"] = "paid_ffffffffffffffffffffffff"
                    else:
                        malformed_actions[0]["provider_operation_id"] = "resp_wrong"
                    malformed_lineage = build_retry_lineage_inventory(
                        run_id=v05["run_id"], actions=malformed_actions,
                    )
                    with self.assertRaises(ValueError):
                        build_lifecycle_inspection_v08(v07, malformed_lineage)

    def test_schema_and_public_exports_exist(self) -> None:
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", read_retry_lineage_schema()["$schema"])
        import astrowoof_natal_authoring as public
        self.assertIs(public.derive_retry_attempt_key, derive_retry_attempt_key)
        self.assertIs(public.validate_lifecycle_inspection_v08, validate_lifecycle_inspection_v08)
        self.assertEqual(
            "astrowoof.temporal_lifecycle_contracts.v3",
            public.read_lifecycle_inspection_v08_schema()["$id"],
        )
        fixture = public.read_lifecycle_inspection_v08_fixture()
        self.assertEqual("astrowoof.authoring_lifecycle_inspection.v0.8", fixture["schema_version"])
        self.assertEqual(
            "retry_lineage_conflict_requires_review",
            fixture["checkpoint_basis"]["retry_lineage_inventory"]["conflict_classification"],
        )


if __name__ == "__main__":
    unittest.main()
