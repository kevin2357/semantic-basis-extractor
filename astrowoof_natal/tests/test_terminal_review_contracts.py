from __future__ import annotations

import copy
import hashlib
import json
import unittest

from astrowoof_natal_authoring.terminal_review_contracts import (
    build_terminal_delivery_command_result,
    build_terminal_review_command_result,
    build_terminal_review_result_v02,
    build_zero_action_terminal_review_command_result,
    build_zero_action_terminal_review_result_v03,
    read_terminal_delivery_command_result_schema,
    read_terminal_review_command_result_schema,
    read_terminal_review_result_v02_schema,
    read_zero_action_terminal_review_command_result_schema,
    read_zero_action_terminal_review_result_v03_schema,
    validate_terminal_delivery_command_result,
    validate_terminal_delivery_command_result_against_publication,
    validate_terminal_review_command_result,
    validate_terminal_review_command_result_against_publication,
    validate_terminal_review_result_v02,
    validate_terminal_review_result_v02_against_api_actions,
    validate_terminal_review_result_v02_against_receipt,
    validate_zero_action_terminal_review_command_result,
    validate_zero_action_terminal_review_command_result_against_publication,
    validate_zero_action_terminal_review_result_v03,
    validate_zero_action_terminal_review_result_v03_against_receipt,
)
from astrowoof_natal_authoring.native_transitions import (
    validate_native_publication_receipt,
)
from astrowoof_natal_authoring.closure import _ordinary_terminal_output
from astrowoof_natal_authoring.reconciliation import _emit_terminal_command_result


def _binding(stage: str, route: str) -> dict:
    return {
        "stage": stage, "route": route,
        "request_sha256": "1" * 64, "profile_sha256": "2" * 64,
        "maximum_output_tokens": 100, "commitment_micro_usd": 1000,
        "price_book_version": "test.v1", "service_level": "interactive",
    }


class TerminalReviewContractTests(unittest.TestCase):
    def state(self) -> dict:
        return {
            "run_id": "native-run",
            "spend_ledger": {"actions": [
                {"action_id": "paid_000000000000000000000001", "state": "REPORTED", "binding": _binding("authoring_initial", "pass:1"), "provider": {"id": "resp_reported"}, "consumption": {}, "reported": {"usage": {"input_tokens": 1}}},
                {"action_id": "paid_000000000000000000000002", "state": "WAITING", "binding": _binding("creative_retry", "retry:1"), "provider": {"id": "resp_pending"}, "consumption": {}},
                {"action_id": "paid_000000000000000000000003", "state": "AUTHORIZED", "binding": _binding("creative_retry", "retry:2"), "authorization": {}},
            ]},
        }

    def base(self) -> dict:
        return {
            "schema_version": "astrowoof.native_execution_result.v0.1",
            "invocation_id": "ninv_000000000000000000000001",
            "run_id": "native-run", "sbe_release": "0.4.27",
            "published_at": "2026-08-28T00:00:00Z",
            "command_kind": "ordinary_authoring",
            "route_binding": {"route_family": "exact_natal", "provider_mechanism": "response", "native_operation_ref": "semantic_closure"},
            "pre_checkpoint": None,
            "post_checkpoint": {"native_state_revision": 3, "checkpoint_basis_sha256": "3" * 64, "logical_workspace_root": "/work/run"},
            "journal_range": {"start_sequence": 1, "end_sequence": 3, "record_count": 3, "range_sha256": "4" * 64, "closing_record_id": "ntr_000000000000000000000001"},
            "outcome": "review_required", "cause_code": "final_qa_requires_review",
            "action_ids": [], "provider_operations": [], "projection_refs": {},
        }

    def result(self) -> dict:
        return build_terminal_review_result_v02(self.base(), self.state())

    def zero_state(self) -> dict:
        return {"run_id": "native-run", "spend_ledger": {"actions": []}}

    def zero_result(self) -> dict:
        return build_zero_action_terminal_review_result_v03(
            self.base(), self.zero_state(),
        )

    def delivery_result(self) -> dict:
        result = self.base()
        result["outcome"] = "delivery_complete"
        result["cause_code"] = "delivery_complete"
        basis = {
            key: value for key, value in result.items()
            if key not in {"result_id", "result_sha256"}
        }
        result["result_sha256"] = hashlib.sha256(json.dumps(
            basis, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest()
        result["result_id"] = f"nres_{result['result_sha256'][:24]}"
        return result

    def test_reconciliation_emits_exact_review_handoff_from_same_publication(self) -> None:
        result = self.result()
        receipt = self.receipt(result)
        emitted: list[dict] = []

        _emit_terminal_command_result(
            {"result": result, "receipt": receipt}, emitted.append,
        )

        self.assertEqual(
            build_terminal_review_command_result(result, receipt), emitted[0]
        )

    def test_reconciliation_emits_exact_delivery_handoff_from_same_publication(self) -> None:
        result = self.delivery_result()
        receipt = self.receipt(result)
        emitted: list[dict] = []

        _emit_terminal_command_result(
            {"result": result, "receipt": receipt}, emitted.append,
        )

        self.assertEqual(
            build_terminal_delivery_command_result(result, receipt), emitted[0]
        )

    def test_reconciliation_emits_nothing_for_nonterminal_publication(self) -> None:
        result = self.base()
        result["outcome"] = "provider_pending"
        emitted: list[dict] = []

        _emit_terminal_command_result(
            {"result": result, "receipt": {}}, emitted.append,
        )

        self.assertEqual([], emitted)

    def receipt(self, result: dict) -> dict:
        receipt = {
            "schema_version": "astrowoof.native_publication_receipt.v0.1",
            "receipt_id": "", "receipt_sha256": "",
            "run_id": result["run_id"], "invocation_id": result["invocation_id"],
            "result_id": result["result_id"], "result_sha256": result["result_sha256"],
            "snapshot_sha256": "5" * 64,
            "checkpoint_basis_sha256": result["post_checkpoint"]["checkpoint_basis_sha256"],
            "journal_range_sha256": result["journal_range"]["range_sha256"],
            "logical_workspace_root": "/work/run",
        }
        basis = {k: v for k, v in receipt.items() if k not in {"receipt_id", "receipt_sha256"}}
        receipt["receipt_sha256"] = hashlib.sha256(json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        receipt["receipt_id"] = f"nreceipt_{receipt['receipt_sha256'][:24]}"
        return receipt

    def test_mixed_inventory_is_strict_and_ordered(self) -> None:
        result = self.result()
        self.assertEqual("mixed_resolution_required", result["custody_finality"])
        self.assertEqual(["paid_000000000000000000000002"], result["reconciliation_action_ids"])
        self.assertEqual(["paid_000000000000000000000003"], result["providerless_denial_action_ids"])
        self.assertFalse(result["new_provider_create_permitted"])
        validate_terminal_review_result_v02(result)

    def test_mutations_fail_python_validator(self) -> None:
        result = self.result()
        mutations = []
        for path, value in (
            (("run_id",), None),
            (("action_dispositions", 1, "provider_operation_id"), None),
            (("action_dispositions", 2, "custody_disposition"), "terminally_accounted"),
            (("reconciliation_action_ids",), []),
            (("custody_finality",), "final"),
            (("new_provider_create_permitted",), True),
        ):
            changed = copy.deepcopy(result)
            target = changed
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    validate_terminal_review_result_v02(changed)

    def test_rehashed_binding_or_inventory_contradiction_fails(self) -> None:
        result = self.result()
        result["action_dispositions"][1]["native_action_state"] = "REPORTED"
        result["action_inventory_sha256"] = hashlib.sha256(json.dumps(result["action_dispositions"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        basis = {k: v for k, v in result.items() if k not in {"result_id", "result_sha256"}}
        result["result_sha256"] = hashlib.sha256(json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        result["result_id"] = f"nres_{result['result_sha256'][:24]}"
        with self.assertRaisesRegex(ValueError, "custody"):
            validate_terminal_review_result_v02(result)

    def test_receipt_must_join_exact_invocation_and_result(self) -> None:
        result = self.result()
        receipt = self.receipt(result)
        validate_terminal_review_result_v02_against_receipt(result, receipt)
        validate_native_publication_receipt(receipt, result)
        receipt["invocation_id"] = "ninv_ffffffffffffffffffffffff"
        with self.assertRaises(ValueError):
            validate_terminal_review_result_v02_against_receipt(result, receipt)

    def test_api_must_join_complete_immutable_action_bindings(self) -> None:
        result = self.result()
        state_actions = self.state()["spend_ledger"]["actions"]
        api_actions = [
            {
                "native_run_id": result["run_id"],
                "action_id": action["action_id"],
                "binding": action["binding"],
                "route_family": "exact_natal",
                "stage": action["binding"]["stage"],
                "provider_operation_id": (action.get("provider") or {}).get("id"),
            }
            for action in state_actions
        ]
        validate_terminal_review_result_v02_against_api_actions(result, api_actions)
        changed = copy.deepcopy(api_actions)
        changed[1]["binding"]["request_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "immutable API action"):
            validate_terminal_review_result_v02_against_api_actions(result, changed)
        changed = copy.deepcopy(api_actions)
        changed[0]["provider_operation_id"] = "resp_wrong"
        with self.assertRaisesRegex(ValueError, "immutable API action"):
            validate_terminal_review_result_v02_against_api_actions(result, changed)

    def test_canonical_v01_receipt_rejects_mismatched_v02_identity(self) -> None:
        result = self.result()
        receipt = self.receipt(result)
        validate_native_publication_receipt(receipt, result)
        wrong = copy.deepcopy(result)
        wrong["schema_version"] = "astrowoof.native_execution_result.v0.1"
        with self.assertRaises(ValueError):
            validate_native_publication_receipt(receipt, wrong)
        other = self.result()
        other["run_id"] = "different-native-run"
        basis = {k: v for k, v in other.items() if k not in {"result_id", "result_sha256"}}
        other["result_sha256"] = hashlib.sha256(json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        other["result_id"] = f"nres_{other['result_sha256'][:24]}"
        with self.assertRaises(ValueError):
            validate_native_publication_receipt(receipt, other)

    def test_command_result_transports_exact_invocation_result_and_receipt(self) -> None:
        result = self.result()
        receipt = self.receipt(result)
        command = build_terminal_review_command_result(result, receipt)
        validate_terminal_review_command_result(command)
        self.assertEqual(result["invocation_id"], command["native_invocation_id"])
        self.assertEqual(result["result_id"], command["result_id"])
        self.assertEqual(result["result_sha256"], command["result_sha256"])
        self.assertEqual(receipt["receipt_id"], command["receipt_id"])
        self.assertEqual(receipt["receipt_sha256"], command["receipt_sha256"])
        changed = copy.deepcopy(command)
        changed["receipt_sha256"] = "f" * 64
        validate_terminal_review_command_result(changed)
        with self.assertRaisesRegex(ValueError, "exact publication"):
            validate_terminal_review_command_result_against_publication(
                changed, result, receipt
            )
        validate_terminal_review_command_result_against_publication(
            command, result, receipt
        )

    def test_command_result_schema_is_packaged(self) -> None:
        schema = read_terminal_review_command_result_schema()
        self.assertEqual(
            "astrowoof.terminal_review_command_result.v0.1",
            schema["properties"]["schema_version"]["const"],
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        result = self.result()
        jsonschema.Draft202012Validator(schema).validate(
            build_terminal_review_command_result(result, self.receipt(result))
        )

    def test_delivery_command_result_carries_exact_sealed_identity(self) -> None:
        result = self.delivery_result()
        receipt = self.receipt(result)
        command = build_terminal_delivery_command_result(result, receipt)
        validate_terminal_delivery_command_result(command)
        validate_terminal_delivery_command_result_against_publication(
            command, result, receipt,
        )
        self.assertEqual(result["invocation_id"], command["native_invocation_id"])
        self.assertEqual(result["result_id"], command["result_id"])
        self.assertEqual(receipt["receipt_id"], command["receipt_id"])

        changed = copy.deepcopy(command)
        changed["receipt_sha256"] = "f" * 64
        validate_terminal_delivery_command_result(changed)
        with self.assertRaisesRegex(ValueError, "exact publication"):
            validate_terminal_delivery_command_result_against_publication(
                changed, result, receipt,
            )

    def test_delivery_command_result_is_closed_packaged_and_delivery_only(self) -> None:
        schema = read_terminal_delivery_command_result_schema()
        self.assertEqual(
            "astrowoof.terminal_delivery_command_result.v0.1",
            schema["properties"]["schema_version"]["const"],
        )
        result = self.delivery_result()
        command = build_terminal_delivery_command_result(result, self.receipt(result))
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        jsonschema.Draft202012Validator(schema).validate(command)

        non_delivery = copy.deepcopy(result)
        non_delivery["outcome"] = "terminal_failure"
        basis = {
            key: value for key, value in non_delivery.items()
            if key not in {"result_id", "result_sha256"}
        }
        non_delivery["result_sha256"] = hashlib.sha256(json.dumps(
            basis, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest()
        non_delivery["result_id"] = f"nres_{non_delivery['result_sha256'][:24]}"
        with self.assertRaisesRegex(ValueError, "exact delivery result"):
            build_terminal_delivery_command_result(
                non_delivery, self.receipt(non_delivery),
            )

    def test_structured_delivery_emits_handoff_but_plain_cli_retains_state(self) -> None:
        result = self.delivery_result()
        sealed = {"result": result, "receipt": self.receipt(result)}
        state = {"status": "DELIVERY_COMPLETE", "mutable": "legacy-output"}
        self.assertIs(
            state,
            _ordinary_terminal_output(state, sealed, structured=False),
        )
        structured = _ordinary_terminal_output(state, sealed, structured=True)
        self.assertEqual(
            "astrowoof.terminal_delivery_command_result.v0.1",
            structured["schema_version"],
        )
        self.assertEqual(result["result_id"], structured["result_id"])

    def test_schema_is_packaged_and_accepts_candidate(self) -> None:
        schema = read_terminal_review_result_v02_schema()
        self.assertEqual("astrowoof.native_execution_result.v0.2", schema["properties"]["schema_version"]["const"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        jsonschema.Draft202012Validator(schema).validate(self.result())

    def test_zero_action_result_is_explicit_closed_and_receipt_bound(self) -> None:
        result = self.zero_result()
        receipt = self.receipt(result)
        self.assertEqual("astrowoof.native_execution_result.v0.3", result["schema_version"])
        self.assertEqual("explicit_zero_paid_actions", result["action_inventory_kind"])
        self.assertEqual(0, result["paid_action_count"])
        self.assertEqual(0, result["provider_operation_count"])
        validate_zero_action_terminal_review_result_v03(result)
        validate_zero_action_terminal_review_result_v03_against_receipt(result, receipt)
        command = build_zero_action_terminal_review_command_result(result, receipt)
        validate_zero_action_terminal_review_command_result(command)
        validate_zero_action_terminal_review_command_result_against_publication(
            command, result, receipt,
        )

    def test_zero_action_refuses_missing_nonempty_or_attached_evidence(self) -> None:
        for state in (
            {"run_id": "native-run"},
            {"run_id": "native-run", "spend_ledger": None},
            {"run_id": "native-run", "spend_ledger": {"actions": "none"}},
            {"run_id": "native-run", "spend_ledger": {"actions": [self.state()["spend_ledger"]["actions"][0]]}},
        ):
            with self.subTest(state=state):
                with self.assertRaises(ValueError):
                    build_zero_action_terminal_review_result_v03(self.base(), state)
        result = self.zero_result()
        for key, value in (
            ("provider_operations", []),
            ("action_dispositions", []),
            ("paid_action_count", 1),
        ):
            changed = copy.deepcopy(result)
            changed[key] = value
            basis = {k: v for k, v in changed.items() if k not in {"result_id", "result_sha256"}}
            changed["result_sha256"] = hashlib.sha256(json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            changed["result_id"] = f"nres_{changed['result_sha256'][:24]}"
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    validate_zero_action_terminal_review_result_v03(changed)

    def test_paid_and_zero_action_result_versions_fail_closed_on_each_other(self) -> None:
        with self.assertRaises(ValueError):
            validate_zero_action_terminal_review_result_v03(self.result())
        with self.assertRaises(ValueError):
            validate_terminal_review_result_v02(self.zero_result())

    def test_zero_action_schemas_are_packaged(self) -> None:
        result_schema = read_zero_action_terminal_review_result_v03_schema()
        command_schema = read_zero_action_terminal_review_command_result_schema()
        self.assertEqual("astrowoof.native_execution_result.v0.3", result_schema["properties"]["schema_version"]["const"])
        self.assertEqual("astrowoof.terminal_review_command_result.v0.2", command_schema["properties"]["schema_version"]["const"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        result = self.zero_result()
        jsonschema.Draft202012Validator(result_schema).validate(result)
        jsonschema.Draft202012Validator(command_schema).validate(
            build_zero_action_terminal_review_command_result(result, self.receipt(result))
        )


if __name__ == "__main__":
    unittest.main()
