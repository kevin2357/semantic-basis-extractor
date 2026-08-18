from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.lifecycle_contracts import (  # noqa: E402
    ACTION_STATE_PRESENTATION_ORDER,
    AMBIGUITY_REVIEW_REASONS,
    BATCH_ACTION_VALIDATION_OUTCOMES,
    BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS,
    BATCH_NEGATIVE_AUTHORIZATION_OUTCOMES,
    BATCH_NEGATIVE_AUTHORIZATION_REVIEW_REASONS,
    DENIAL_REASONS,
    DENIAL_TERMINAL_REASONS,
    EVENT_NAMES,
    LOCAL_DEPENDENCY_KINDS,
    EXECUTION_CAPACITY_DISPOSITIONS,
    CONSUMER_AUTHORITY_RETENTION_REASONS,
    CONSUMER_AUTHORITY_STATES,
    COST_DISPOSITIONS,
    PROVIDER_OPERATION_KINDS,
    PROVIDER_ROUTE_FAMILIES,
    PROVIDER_CUSTODY_CLASSIFICATIONS,
    PROVIDER_CUSTODY_STAGES,
    PROVIDER_CUSTODY_STATES,
    PROVIDER_RECONCILIATION_CYCLE_OUTCOMES,
    PROVIDER_RECONCILIATION_POLICY,
    PROVIDERLESS_ELIGIBILITY_REASONS,
    PROVIDER_ACTION_STATES,
    RUN_TRANSITION_OUTCOMES,
    RUN_TRANSITION_TRIGGERS,
    action_presentation_key,
    batch_negative_authorization_request_sha256,
    canonical_contract_json,
    observation_transition_errors,
    prohibited_event_paths,
)
from astrowoof_natal_authoring.resource_access import (  # noqa: E402
    read_resource_text,
)


FIXTURE_NAMES = (
    "negative-authorization-request.v0.1.json",
    "negative-authorization-result.v0.1.json",
    "negative-authorization-result.v0.2.json",
    "negative-authorization-refused.v0.1.json",
    "batch-negative-authorization-request.v0.1.json",
    "batch-negative-authorization-result.v0.1.json",
    "batch-negative-authorization-result.v0.2.json",
    "batch-negative-authorization-replay.v0.1.json",
    "batch-negative-authorization-refused.v0.1.json",
    "action-inventory.v0.1.json",
    "inspection.v0.1.json",
    "inspection.v0.2.json",
    "inspection.v0.3.json",
    "reconciliation-policy.v0.1.json",
    "reconciliation-policy.v0.2.json",
    "reconciliation-cycle-not-due.v0.1.json",
    "closeout-result.v0.1.json",
    "execution-event.v1.json",
)


def _resolve(schema_root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise AssertionError(f"Test validator only accepts local refs: {reference}")
    value: Any = schema_root
    for component in reference[2:].split("/"):
        value = value[component.replace("~1", "/").replace("~0", "~")]
    return value


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }[expected]


def validate(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> None:
    if "$ref" in schema:
        validate(value, _resolve(root, schema["$ref"]), root, path)
        return
    if "oneOf" in schema:
        matches = 0
        for candidate in schema["oneOf"]:
            try:
                validate(value, candidate, root, path)
                matches += 1
            except AssertionError:
                pass
        if matches != 1:
            raise AssertionError(f"{path}: expected exactly one schema match, got {matches}")
        return
    if "anyOf" in schema:
        for candidate in schema["anyOf"]:
            try:
                validate(value, candidate, root, path)
                return
            except AssertionError:
                pass
        raise AssertionError(f"{path}: expected at least one schema match")
    if "const" in schema and value != schema["const"]:
        raise AssertionError(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise AssertionError(f"{path}: value {value!r} is outside closed vocabulary")
    expected = schema.get("type")
    if expected is not None:
        choices = [expected] if isinstance(expected, str) else expected
        if not any(_type_matches(value, item) for item in choices):
            raise AssertionError(f"{path}: wrong type")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise AssertionError(f"{path}: string too short")
        if len(value) > schema.get("maxLength", len(value)):
            raise AssertionError(f"{path}: string too long")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            raise AssertionError(f"{path}: string does not match pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            raise AssertionError(f"{path}: number below minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise AssertionError(f"{path}: too few items")
        if len(value) > schema.get("maxItems", len(value)):
            raise AssertionError(f"{path}: too many items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            raise AssertionError(f"{path}: duplicate items")
        if "items" in schema:
            for index, item in enumerate(value):
                validate(item, schema["items"], root, f"{path}[{index}]")
    if isinstance(value, dict):
        missing = set(schema.get("required", ())) - set(value)
        if missing:
            raise AssertionError(f"{path}: missing {sorted(missing)}")
        if len(value) > schema.get("maxProperties", len(value)):
            raise AssertionError(f"{path}: too many properties")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = set(value) - set(properties)
            if unknown:
                raise AssertionError(f"{path}: unknown {sorted(unknown)}")
        elif isinstance(schema.get("additionalProperties"), dict):
            for key in set(value) - set(properties):
                validate(
                    value[key], schema["additionalProperties"], root,
                    f"{path}.{key}",
                )
        property_names = schema.get("propertyNames")
        if property_names:
            for key in value:
                validate(key, property_names, root, f"{path}.<key>")
        for key, child_schema in properties.items():
            if key in value:
                validate(value[key], child_schema, root, f"{path}.{key}")


class TestLifecycleContracts(unittest.TestCase):
    def test_public_reconciliation_python_surface_is_typed(self) -> None:
        import astrowoof_natal_authoring as public

        self.assertIn("ProviderReconciliationAdapters", public.__all__)
        self.assertIn("reconcile_authoring_provider_cycle", public.__all__)
        self.assertTrue(public.reconcile_authoring_provider_cycle.__annotations__)
        adapters = public.ProviderReconciliationAdapters()
        self.assertEqual(3, adapters.max_attempts)

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(read_resource_text(
            "contracts/authoring-lifecycle-contracts.schema.json"
        ))
        cls.fixtures = {
            name: json.loads(read_resource_text(f"fixtures/lifecycle/{name}"))
            for name in FIXTURE_NAMES
        }

    def test_all_sanitized_fixtures_validate(self) -> None:
        for name, fixture in self.fixtures.items():
            with self.subTest(name=name):
                validate(fixture, self.schema, self.schema)

    def test_unknown_schema_and_unknown_required_shape_are_rejected(self) -> None:
        fixture = copy.deepcopy(self.fixtures["inspection.v0.1.json"])
        fixture["schema_version"] = "astrowoof.authoring_lifecycle_inspection.v9"
        with self.assertRaises(AssertionError):
            validate(fixture, self.schema, self.schema)
        fixture = copy.deepcopy(self.fixtures["inspection.v0.1.json"])
        fixture["terminal"]["generic_success"] = True
        with self.assertRaises(AssertionError):
            validate(fixture, self.schema, self.schema)

    def test_closed_vocabularies_are_unique_and_match_schema(self) -> None:
        vocabularies = (
            PROVIDER_ACTION_STATES,
            DENIAL_REASONS,
            AMBIGUITY_REVIEW_REASONS,
            LOCAL_DEPENDENCY_KINDS,
            PROVIDERLESS_ELIGIBILITY_REASONS,
            EVENT_NAMES,
            BATCH_NEGATIVE_AUTHORIZATION_OUTCOMES,
            BATCH_ACTION_VALIDATION_OUTCOMES,
            BATCH_NEGATIVE_AUTHORIZATION_REVIEW_REASONS,
            DENIAL_TERMINAL_REASONS,
            RUN_TRANSITION_OUTCOMES,
            RUN_TRANSITION_TRIGGERS,
            EXECUTION_CAPACITY_DISPOSITIONS,
            PROVIDER_CUSTODY_CLASSIFICATIONS,
            PROVIDER_CUSTODY_STAGES,
            PROVIDER_CUSTODY_STATES,
            PROVIDER_RECONCILIATION_CYCLE_OUTCOMES,
            PROVIDER_ROUTE_FAMILIES,
            PROVIDER_OPERATION_KINDS,
            COST_DISPOSITIONS,
            CONSUMER_AUTHORITY_STATES,
            CONSUMER_AUTHORITY_RETENTION_REASONS,
        )
        self.assertTrue(all(len(items) == len(set(items)) for items in vocabularies))
        defs = self.schema["$defs"]
        self.assertEqual(list(PROVIDER_ACTION_STATES), defs["actionState"]["enum"])
        self.assertEqual(list(DENIAL_REASONS), defs["denialReason"]["enum"])
        self.assertEqual(list(EVENT_NAMES), defs["executionEvent"]["properties"]["event_name"]["enum"])
        transition = defs["runTransition"]["properties"]
        self.assertEqual(list(DENIAL_TERMINAL_REASONS), transition["terminal_reason"]["enum"])
        self.assertEqual(list(RUN_TRANSITION_OUTCOMES), transition["outcome"]["enum"])
        self.assertEqual(list(RUN_TRANSITION_TRIGGERS), transition["trigger"]["enum"])

    def test_reconciliation_policy_is_one_bounded_retrieval_wave(self) -> None:
        fixture = self.fixtures["reconciliation-policy.v0.2.json"]
        self.assertEqual(PROVIDER_RECONCILIATION_POLICY, fixture)
        response = fixture["mechanisms"]["response"]
        batch = fixture["mechanisms"]["batch"]
        self.assertEqual(4, response["maximum_due_actions_per_cycle"])
        self.assertEqual(
            response["maximum_due_actions_per_cycle"],
            response["maximum_parallel_requests"],
        )
        self.assertLess(
            response["provider_request_timeout_seconds"],
            response["provider_io_wall_clock_limit_seconds"],
        )
        self.assertEqual([15, 30, 60, 120, 240, 300], response["delays_seconds"])
        self.assertEqual([60, 120, 300, 600, 900, 1800], batch["delays_seconds"])
        self.assertEqual(1, batch["maximum_due_actions_per_cycle"])
        self.assertEqual(40, batch["provider_io_wall_clock_limit_seconds"])

    def test_inspection_v03_binds_native_route_mechanism_and_authority(self) -> None:
        inspection = self.fixtures["inspection.v0.3.json"]
        self.assertEqual("exact_natal", inspection["native_route"]["route_family"])
        action = inspection["provider_custody"]["actions"][0]
        self.assertEqual("response", action["provider_operation_kind"])
        self.assertEqual("interactive", action["service_level"])
        self.assertEqual(
            action["action_id"], inspection["consumer_authority"]["action_ids"][0]
        )
        malformed = copy.deepcopy(inspection)
        malformed["provider_custody"]["actions"][0]["provider_operation_kind"] = "file"
        with self.assertRaises(AssertionError):
            validate(malformed, self.schema, self.schema)
        missing = copy.deepcopy(inspection)
        del missing["native_route"]
        with self.assertRaises(AssertionError):
            validate(missing, self.schema, self.schema)

    def test_cycle_v02_cost_disposition_is_closed_and_explicit(self) -> None:
        inspection = copy.deepcopy(self.fixtures["inspection.v0.3.json"])
        result = {
            "schema_version": "astrowoof.provider_reconciliation_cycle_result.v0.2",
            "run_id": inspection["run_id"], "outcome": "not_due",
            "decision_basis": inspection["observation"],
            "cycle": {
                "started_at": "2026-08-13T18:00:05Z",
                "finished_at": "2026-08-13T18:00:05Z",
                "wall_clock_limit_seconds": 20, "provider_retrieval_count": 0,
                "retrieved_action_ids": [], "completed_action_ids": [],
                "still_pending_action_ids": ["paid_111111111111111111111111"],
                "transport_warning_action_ids": [],
            },
            "inspection": inspection, "provider_operations": [],
        }
        validate(result, self.schema, self.schema)
        operation = {
            "action_id": "paid_111111111111111111111111",
            "route_family": "exact_natal", "provider_operation_kind": "batch",
            "provider_operation_id": "batch_fixture_001",
            "retrieval_outcome": "provider_failed",
            "cost_disposition": "provider_usage_unavailable_billing_reconciliation_pending",
            "member_count": 6, "ingested_member_count": 0,
            "failed_member_count": 6,
        }
        result["provider_operations"] = [operation]
        validate(result, self.schema, self.schema)
        operation["cost_disposition"] = "estimated_zero"
        with self.assertRaises(AssertionError):
            validate(result, self.schema, self.schema)

    def test_inspection_v02_capacity_and_custody_are_strict(self) -> None:
        inspection = self.fixtures["inspection.v0.2.json"]
        custody_action = inspection["provider_custody"]["actions"][0]
        self.assertEqual("release_until_due", inspection["execution_capacity"]["disposition"])
        self.assertTrue(inspection["execution_capacity"]["checkpoint_safe_for_worker_release"])
        self.assertEqual("authoring_initial", custody_action["stage"])
        self.assertEqual(
            "retain_consumer_authority",
            custody_action["custody_classification"],
        )
        malformed = copy.deepcopy(inspection)
        malformed["provider_custody"]["actions"][0]["stage"] = "future_stage"
        with self.assertRaises(AssertionError):
            validate(malformed, self.schema, self.schema)
        historical = copy.deepcopy(self.fixtures["inspection.v0.1.json"])
        historical["execution_capacity"] = inspection["execution_capacity"]
        with self.assertRaises(AssertionError):
            validate(historical, self.schema, self.schema)

    def test_not_due_is_strictly_nonmutating_without_checkpoint(self) -> None:
        result = self.fixtures["reconciliation-cycle-not-due.v0.1.json"]
        self.assertEqual("not_due", result["outcome"])
        self.assertEqual(0, result["cycle"]["provider_retrieval_count"])
        self.assertNotIn("result_checkpoint", result)
        malformed = copy.deepcopy(result)
        malformed["result_checkpoint"] = {
            "operator_state_revision": 13,
            "snapshot_sha256": "4" * 64,
            "result_artifact": {
                "logical_path": "lifecycle/reconciliation-cycle.json",
                "bytes": 128,
                "sha256": "5" * 64,
            },
        }
        with self.assertRaises(AssertionError):
            validate(malformed, self.schema, self.schema)

    def test_progressed_cycle_exposes_strict_local_continuation(self) -> None:
        result = copy.deepcopy(
            self.fixtures["reconciliation-cycle-not-due.v0.1.json"]
        )
        result["outcome"] = "progressed_local"
        result["local_continuation"] = {
            "pass_ids": ["kevin-pass-1"],
            "stages": ["authoring_initial", "polish"],
            "completed_action_ids": ["paid_111111111111111111111111"],
            "exhausted_before_detach": True,
        }
        result["result_checkpoint"] = {
            "operator_state_revision": 13,
            "snapshot_sha256": "4" * 64,
            "result_artifact": {
                "logical_path": "lifecycle/provider-reconciliation/cycle-00000013.json",
                "bytes": 128,
                "sha256": "5" * 64,
            },
        }
        validate(result, self.schema, self.schema)
        result["local_continuation"]["stages"] = ["future_stage"]
        with self.assertRaises(AssertionError):
            validate(result, self.schema, self.schema)

    def test_v02_single_result_requires_exact_run_transition(self) -> None:
        result = self.fixtures["negative-authorization-result.v0.2.json"]
        transition = result["run_transition"]
        self.assertEqual("terminalized", transition["outcome"])
        self.assertEqual("BUDGET_EXHAUSTED", transition["resulting_status"])
        self.assertEqual("budget_exhausted", transition["terminal_outcome"])
        self.assertEqual(
            "external_spend_authority_denied", transition["terminal_reason"]
        )
        self.assertEqual([result["action_id"]], transition["denied_action_ids"])
        self.assertEqual([result["action_id"]], transition["required_action_ids"])
        missing = copy.deepcopy(result)
        del missing["run_transition"]
        with self.assertRaises(AssertionError):
            validate(missing, self.schema, self.schema)

    def test_v02_mixed_batch_separates_denied_and_required_causal_members(self) -> None:
        result = self.fixtures["batch-negative-authorization-result.v0.2.json"]
        transition = result["run_transition"]
        action_ids = [item["action_id"] for item in result["actions"]]
        self.assertEqual(action_ids, transition["denied_action_ids"])
        self.assertEqual(action_ids[:1], transition["required_action_ids"])
        self.assertLess(
            len(transition["required_action_ids"]),
            len(transition["denied_action_ids"]),
        )
        self.assertTrue(
            set(transition["required_action_ids"])
            <= set(transition["denied_action_ids"])
        )
        unknown = copy.deepcopy(result)
        unknown["run_transition"]["policy_detail"] = "secret API policy"
        with self.assertRaises(AssertionError):
            validate(unknown, self.schema, self.schema)

    def test_negative_decision_separates_basis_and_result_checkpoint(self) -> None:
        result = self.fixtures["negative-authorization-result.v0.1.json"]
        request = self.fixtures["negative-authorization-request.v0.1.json"]
        self.assertEqual(request["binding"], result["binding"])
        self.assertEqual(request["observed"], result["request_observation"])
        self.assertTrue(result["applied"])
        self.assertLess(
            result["decision_basis"]["operator_state_revision"],
            result["result_checkpoint"]["operator_state_revision"],
        )
        self.assertNotEqual(
            result["decision_basis"]["snapshot_sha256"],
            result["result_checkpoint"]["snapshot_sha256"],
        )

    def test_observation_may_strengthen_exclusivity_only(self) -> None:
        result = self.fixtures["negative-authorization-result.v0.1.json"]
        self.assertEqual([], observation_transition_errors(
            result["request_observation"], result["decision_basis"]
        ))
        for field in (
            "operator_state_revision", "snapshot_sha256",
            "logical_workspace_root", "inventory_valid",
        ):
            with self.subTest(field=field):
                changed = copy.deepcopy(result["decision_basis"])
                changed[field] = (
                    not changed[field] if isinstance(changed[field], bool)
                    else f"changed-{changed[field]}"
                )
                self.assertIn(field, observation_transition_errors(
                    result["request_observation"], changed
                ))
        raced = copy.deepcopy(result["decision_basis"])
        raced["writer_race_possible"] = True
        self.assertIn("writer_race_possible", observation_transition_errors(
            result["request_observation"], raced
        ))

    def test_refusal_is_typed_and_has_no_mutation_checkpoint(self) -> None:
        refusal = self.fixtures["negative-authorization-refused.v0.1.json"]
        self.assertFalse(refusal["applied"])
        self.assertEqual("provider_identity_appeared", refusal["outcome"])
        self.assertFalse(refusal["release_eligible"])
        self.assertNotIn("result_checkpoint", refusal)
        self.assertNotIn("decision_basis", refusal)

    def test_action_evidence_and_quiescence_are_explicit(self) -> None:
        inventory = self.fixtures["action-inventory.v0.1.json"]
        action = inventory["actions"][0]
        self.assertIsNone(action["provider_operation_id"])
        self.assertFalse(action["provider_identity_present"])
        self.assertFalse(action["provider_evidence_present"])
        self.assertFalse(action["consumption_evidence_present"])
        self.assertEqual([], action["blocking_action_ids"])
        self.assertEqual([], action["ambiguity_review_reasons"])
        inspection = self.fixtures["inspection.v0.1.json"]
        self.assertEqual("not_quiescent", inspection["quiescence"]["state"])

    def test_presentation_order_is_stable_and_not_execution_semantics(self) -> None:
        inventory = self.fixtures["action-inventory.v0.1.json"]
        self.assertEqual(
            "deterministic_presentation_only_not_execution_order",
            inventory["ordering_semantics"],
        )
        actions = [
            {"action_id": "paid_b", "state": "WAITING", "attempt": 1, "binding": {"route": "b"}},
            {"action_id": "paid_a", "state": "PREPARED", "attempt": 2, "binding": {"route": "a"}},
            {"action_id": "paid_c", "state": "AUTHORIZED", "attempt": 1, "binding": {"route": "a"}},
        ]
        ordered = sorted(actions, key=action_presentation_key)
        self.assertEqual(["paid_c", "paid_a", "paid_b"], [item["action_id"] for item in ordered])
        self.assertEqual(set(PROVIDER_ACTION_STATES), set(ACTION_STATE_PRESENTATION_ORDER))

    def test_contract_serialization_is_byte_stable(self) -> None:
        fixture = self.fixtures["closeout-result.v0.1.json"]
        self.assertEqual(
            canonical_contract_json(fixture),
            canonical_contract_json(json.loads(json.dumps(fixture))),
        )

    def test_batch_request_digest_preserves_member_order(self) -> None:
        request = self.fixtures["batch-negative-authorization-request.v0.1.json"]
        result = self.fixtures["batch-negative-authorization-result.v0.1.json"]
        self.assertEqual(
            result["batch_request_sha256"],
            batch_negative_authorization_request_sha256(request),
        )
        same = json.loads(json.dumps(request, indent=4, sort_keys=True))
        self.assertEqual(
            batch_negative_authorization_request_sha256(request),
            batch_negative_authorization_request_sha256(same),
        )
        reordered = copy.deepcopy(request)
        reordered["actions"].reverse()
        self.assertNotEqual(
            batch_negative_authorization_request_sha256(request),
            batch_negative_authorization_request_sha256(reordered),
        )

    def test_batch_contract_is_bounded_and_rejects_duplicates_semantically(self) -> None:
        request = self.fixtures["batch-negative-authorization-request.v0.1.json"]
        self.assertEqual(32, BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS)
        empty = copy.deepcopy(request)
        empty["actions"] = []
        with self.assertRaises(AssertionError):
            validate(empty, self.schema, self.schema)
        oversized = copy.deepcopy(request)
        oversized["actions"] = [copy.deepcopy(request["actions"][0])
                                  for _ in range(BATCH_NEGATIVE_AUTHORIZATION_MAX_ACTIONS + 1)]
        with self.assertRaises(AssertionError):
            validate(oversized, self.schema, self.schema)
        unknown = copy.deepcopy(request)
        unknown["actions"][0]["future_field"] = True
        with self.assertRaises(AssertionError):
            validate(unknown, self.schema, self.schema)
        newline = copy.deepcopy(request)
        newline["actions"][0]["external_authority_reference"] = "unsafe\nreference"
        with self.assertRaises(AssertionError):
            validate(newline, self.schema, self.schema)
        # JSON Schema validates shape; the locked native preflight owns uniqueness.
        duplicate = copy.deepcopy(request)
        duplicate["actions"][1] = copy.deepcopy(duplicate["actions"][0])
        validate(duplicate, self.schema, self.schema)
        self.assertEqual(
            len(duplicate["actions"]),
            len(duplicate["actions"]) - len({item["action_id"] for item in duplicate["actions"]}) + 1,
        )

    def test_batch_results_separate_success_replay_and_all_or_none_refusal(self) -> None:
        applied = self.fixtures["batch-negative-authorization-result.v0.1.json"]
        replay = self.fixtures["batch-negative-authorization-replay.v0.1.json"]
        refusal = self.fixtures["batch-negative-authorization-refused.v0.1.json"]
        self.assertTrue(applied["applied"])
        self.assertEqual("applied", applied["outcome"])
        self.assertFalse(replay["applied"])
        self.assertEqual("idempotent_replay", replay["outcome"])
        self.assertEqual(applied["result_checkpoint"], replay["result_checkpoint"])
        self.assertFalse(refusal["applied"])
        self.assertEqual("provider_identity_appeared", refusal["outcome"])
        self.assertNotIn("result_checkpoint", refusal)
        self.assertTrue(all(not item["release_eligible"] for item in refusal["actions"]))

    def test_event_payload_prohibited_fields_are_detected_recursively(self) -> None:
        fixture = self.fixtures["execution-event.v1.json"]
        self.assertEqual([], prohibited_event_paths(fixture))
        fixture["data"]["nested"] = {"birth_datetime": "protected"}
        self.assertEqual(["$.data.nested.birth_datetime"], prohibited_event_paths(fixture))

    def test_event_unknown_name_and_raw_lease_field_are_rejected(self) -> None:
        fixture = copy.deepcopy(self.fixtures["execution-event.v1.json"])
        fixture["event_name"] = "future.unknown"
        with self.assertRaises(AssertionError):
            validate(fixture, self.schema, self.schema)
        fixture = copy.deepcopy(self.fixtures["execution-event.v1.json"])
        fixture["data"]["lease_token"] = "secret"
        with self.assertRaises(AssertionError):
            validate(fixture, self.schema, self.schema)
        fixture = copy.deepcopy(self.fixtures["execution-event.v1.json"])
        fixture["data"]["nested"] = {"birth_datetime": "protected"}
        with self.assertRaises(AssertionError):
            validate(fixture, self.schema, self.schema)


if __name__ == "__main__":
    unittest.main()
