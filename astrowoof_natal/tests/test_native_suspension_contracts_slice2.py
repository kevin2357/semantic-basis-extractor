from __future__ import annotations

import copy
import hashlib
import json
import unittest

from astrowoof_natal_authoring.native_suspension_contracts import (
    classify_suspension_request_replay,
    read_native_suspension_contract_schema,
    read_native_suspension_fixture_bundle,
    seal_document,
    validate_supervision_invocation,
    validate_suspension_command_result,
    validate_suspension_fixture_bundle,
    validate_suspension_receipt,
    validate_suspension_request,
    validate_suspension_result,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64


def _digest_without(value, *fields):
    return hashlib.sha256(json.dumps(
        {key: item for key, item in value.items() if key not in fields},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode()).hexdigest()


def _docs(*, suffix="one", outcome="suspended_checkpointed"):
    executable = "C:\\qa\\workspace"
    control = f"C:\\qa-control\\{suffix}"
    envelope = seal_document({
        "schema_version": "astrowoof.native_supervision_invocation.v1",
        "supervision_invocation_id": f"supervision-{suffix}",
        "launch_generation": 7,
        "api_run_id": "api-run-one", "job_id": "job-one",
        "attempt_id": "attempt-one", "lease_id": "lease-one",
        "lease_token_sha256": SHA_A, "native_run_id": "native-run-one",
        "worker_boot_id": "boot-one",
        "command_kind": "external_authority_v2_dispatch",
        "command_sha256": SHA_B,
        "executable_workspace_root": executable,
        "executable_workspace_root_sha256": hashlib.sha256(executable.encode()).hexdigest(),
        "control_root": control,
        "control_root_sha256": hashlib.sha256(control.encode()).hexdigest(),
        "created_at": "2026-09-15T12:00:00Z",
        "launch_not_after": "2026-09-15T12:01:00Z",
        "grace_deadline": "2026-09-15T12:05:00Z",
        "supervision_capability_id": "capability-one",
        "supervision_capability_sha256": SHA_D,
        "envelope_sha256": "",
    }, "envelope_sha256")
    request = seal_document({
        "schema_version": "astrowoof.native_suspension_request.v1",
        "operation": "cooperative_suspend", "request_id": f"request-{suffix}",
        "idempotency_key": f"idem-{suffix}",
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "launch_generation": envelope["launch_generation"],
        "envelope_sha256": envelope["envelope_sha256"],
        "supervision_capability_id": envelope["supervision_capability_id"],
        "supervision_capability_sha256": envelope[
            "supervision_capability_sha256"
        ],
        "force_fence_id": "fence-one", "force_fence_sha256": SHA_C,
        "api_run_id": envelope["api_run_id"], "job_id": envelope["job_id"],
        "attempt_id": envelope["attempt_id"], "lease_id": envelope["lease_id"],
        "native_run_id": envelope["native_run_id"],
        "command_kind": envelope["command_kind"],
        "command_sha256": envelope["command_sha256"],
        "executable_workspace_root_sha256": envelope["executable_workspace_root_sha256"],
        "control_root_sha256": envelope["control_root_sha256"],
        "admission_checkpoint_basis_sha256": SHA_A,
        "actor_id": "operator-one", "reason_code": "emergency-stop",
        "environment": "qa", "emergency_containment_confirmed": True,
        "requested_at": "2026-09-15T12:01:30Z",
        "expires_at": "2026-09-15T12:04:00Z",
        "grace_deadline": envelope["grace_deadline"],
        "request_sha256": "",
    }, "request_sha256")
    result = {
        "schema_version": "astrowoof.native_suspension_result.v1",
        "result_id": "", "result_sha256": "",
        "request_id": request["request_id"], "request_sha256": request["request_sha256"],
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "envelope_sha256": envelope["envelope_sha256"],
        "supervision_capability_id": envelope["supervision_capability_id"],
        "supervision_capability_sha256": envelope[
            "supervision_capability_sha256"
        ],
        "force_fence_id": request["force_fence_id"],
        "force_fence_sha256": request["force_fence_sha256"],
        "native_publication_invocation_id": "native-publication-one",
        "native_run_id": envelope["native_run_id"],
        "logical_workspace_root_sha256": SHA_D,
        "command_kind": envelope["command_kind"],
        "safe_point": "dispatch_after_intent_checkpoint",
        "observed_at": "2026-09-15T12:02:00Z",
        "admission_checkpoint_basis_sha256": SHA_A,
        "observed_checkpoint": {
            "state_revision": 8, "snapshot_sha256": SHA_B,
            "checkpoint_basis_sha256": SHA_C,
            "predecessor_checkpoint_basis_sha256": SHA_A,
        },
        "post_publication_checkpoint": {
            "state_revision": 9, "snapshot_sha256": SHA_C,
            "checkpoint_basis_sha256": SHA_D,
            "predecessor_checkpoint_basis_sha256": SHA_C,
        },
        "provider_boundary": "not_entered", "local_work_posture": "durable_pending",
        "actions": [{
            "ordinal": 1, "action_id": "paid_" + "1" * 24,
            "binding_sha256": SHA_B, "native_action_state": "PREPARED",
            "provider_operation_id": None, "custody_class": "providerless_authority",
        }],
        "ordinary_result_preceded_observation": False,
        "outcome": outcome, "reason_code": "cooperative-request-observed",
        "continuation_mode": None, "next_safe_point": None,
        "continuation_deadline": None,
    }
    result["result_sha256"] = _digest_without(result, "result_id", "result_sha256")
    result["result_id"] = "nsusp_" + result["result_sha256"][:24]
    receipt = {
        "schema_version": "astrowoof.native_suspension_receipt.v1",
        "receipt_id": "", "receipt_sha256": "",
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "native_run_id": envelope["native_run_id"],
        "result_id": result["result_id"], "result_sha256": result["result_sha256"],
        "request_id": request["request_id"], "request_sha256": request["request_sha256"],
        "supervision_capability_id": result["supervision_capability_id"],
        "supervision_capability_sha256": result[
            "supervision_capability_sha256"
        ],
        "force_fence_id": result["force_fence_id"],
        "force_fence_sha256": result["force_fence_sha256"],
        "checkpoint_basis_sha256": SHA_D, "snapshot_sha256": SHA_C,
        "published_at": "2026-09-15T12:02:30Z",
    }
    receipt["receipt_sha256"] = _digest_without(receipt, "receipt_id", "receipt_sha256")
    receipt["receipt_id"] = "nsuspr_" + receipt["receipt_sha256"][:24]
    command = seal_document({
        "schema_version": "astrowoof.native_suspension_command_result.v1",
        "command_result_sha256": "", "outcome": result["outcome"], "exit_code": 0,
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "supervision_capability_id": result["supervision_capability_id"],
        "supervision_capability_sha256": result[
            "supervision_capability_sha256"
        ],
        "force_fence_id": result["force_fence_id"],
        "force_fence_sha256": result["force_fence_sha256"],
        "native_publication_invocation_id": result["native_publication_invocation_id"],
        "result_id": result["result_id"], "result_sha256": result["result_sha256"],
        "receipt_id": receipt["receipt_id"], "receipt_sha256": receipt["receipt_sha256"],
        "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
    }, "command_result_sha256")
    return envelope, request, result, receipt, command


def _rebind(result, receipt, command):
    result["result_sha256"] = _digest_without(result, "result_id", "result_sha256")
    result["result_id"] = "nsusp_" + result["result_sha256"][:24]
    receipt["result_id"] = result["result_id"]
    receipt["result_sha256"] = result["result_sha256"]
    receipt["checkpoint_basis_sha256"] = result["post_publication_checkpoint"]["checkpoint_basis_sha256"]
    receipt["snapshot_sha256"] = result["post_publication_checkpoint"]["snapshot_sha256"]
    receipt["receipt_sha256"] = _digest_without(receipt, "receipt_id", "receipt_sha256")
    receipt["receipt_id"] = "nsuspr_" + receipt["receipt_sha256"][:24]
    command.update({
        "outcome": result["outcome"], "result_id": result["result_id"],
        "result_sha256": result["result_sha256"], "receipt_id": receipt["receipt_id"],
        "receipt_sha256": receipt["receipt_sha256"],
        "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
    })
    command["command_result_sha256"] = _digest_without(command, "command_result_sha256")


class NativeSuspensionContractTests(unittest.TestCase):
    def test_exact_documents_and_join_validate(self):
        envelope, request, result, receipt, command = _docs()
        self.assertEqual(envelope, validate_supervision_invocation(envelope))
        self.assertEqual(request, validate_suspension_request(request, envelope=envelope))
        self.assertEqual(result, validate_suspension_result(result, request=request, envelope=envelope))
        self.assertEqual(receipt, validate_suspension_receipt(
            receipt, result=result, request=request, envelope=envelope,
        ))
        self.assertEqual(command, validate_suspension_command_result(
            command, result=result, receipt=receipt, request=request, envelope=envelope,
        ))

    def test_prelaunch_capability_and_later_force_fence_are_distinct(self):
        envelope, request, result, receipt, command = _docs()
        self.assertNotIn("force_fence_id", envelope)
        self.assertNotIn("force_fence_sha256", envelope)
        self.assertEqual(
            envelope["supervision_capability_id"],
            request["supervision_capability_id"],
        )
        self.assertEqual("fence-one", request["force_fence_id"])

        changed = copy.deepcopy(result)
        changed["force_fence_id"] = "fence-other"
        changed["force_fence_sha256"] = SHA_D
        _rebind(changed, receipt, command)
        with self.assertRaisesRegex(ValueError, "identity join"):
            validate_suspension_result(changed, request=request, envelope=envelope)

        changed = copy.deepcopy(request)
        changed["supervision_capability_id"] = "capability-other"
        changed["request_sha256"] = _digest_without(changed, "request_sha256")
        with self.assertRaisesRegex(ValueError, "join"):
            validate_suspension_request(changed, envelope=envelope)

    def test_request_replay_is_exact_or_invocation_wide_conflict(self):
        envelope, request, *_ = _docs()
        self.assertEqual("exact_replay", classify_suspension_request_replay(
            request, copy.deepcopy(request), envelope=envelope,
        ))
        changed = copy.deepcopy(request)
        changed["request_id"] = "request-two"
        changed["idempotency_key"] = "new-key"
        changed["request_sha256"] = _digest_without(changed, "request_sha256")
        self.assertEqual("request_conflict", classify_suspension_request_replay(
            request, changed, envelope=envelope,
        ))

    def test_c1_to_c2_requires_exact_contiguous_successor(self):
        envelope, request, result, *_ = _docs()
        changed = copy.deepcopy(result)
        changed["observed_checkpoint"]["predecessor_checkpoint_basis_sha256"] = SHA_B
        changed["result_sha256"] = _digest_without(changed, "result_id", "result_sha256")
        changed["result_id"] = "nsusp_" + changed["result_sha256"][:24]
        with self.assertRaisesRegex(ValueError, "contiguous"):
            validate_suspension_result(changed, request=request, envelope=envelope)

    def test_prior_ordinary_result_suppresses_suspension_publication(self):
        envelope, request, result, *_ = _docs()
        result["ordinary_result_preceded_observation"] = True
        result["result_sha256"] = _digest_without(result, "result_id", "result_sha256")
        result["result_id"] = "nsusp_" + result["result_sha256"][:24]
        with self.assertRaisesRegex(ValueError, "suppresses"):
            validate_suspension_result(result, request=request, envelope=envelope)

    def test_transport_mutations_fail_even_when_digest_is_recomputed(self):
        envelope, request, result, receipt, command = _docs()
        changed = copy.deepcopy(receipt)
        changed["result_sha256"] = SHA_A
        changed["receipt_sha256"] = _digest_without(changed, "receipt_id", "receipt_sha256")
        changed["receipt_id"] = "nsuspr_" + changed["receipt_sha256"][:24]
        with self.assertRaisesRegex(ValueError, "join"):
            validate_suspension_receipt(
                changed, result=result, request=request, envelope=envelope,
            )
        changed_command = copy.deepcopy(command)
        changed_command["receipt_id"] = "nsuspr_" + "9" * 24
        changed_command["command_result_sha256"] = _digest_without(
            changed_command, "command_result_sha256",
        )
        with self.assertRaisesRegex(ValueError, "join"):
            validate_suspension_command_result(
                changed_command, result=result, receipt=receipt,
                request=request, envelope=envelope,
            )

    def test_all_six_closed_outcomes_have_provider_free_positive_shapes(self):
        for outcome in (
            "suspended_checkpointed", "suspended_quiescent_no_checkpoint_change",
            "suspension_deferred", "suspension_refused",
            "provider_boundary_ambiguous", "checkpoint_publication_ambiguous",
        ):
            envelope, request, result, receipt, command = _docs(outcome=outcome)
            if outcome == "suspended_quiescent_no_checkpoint_change":
                result["post_publication_checkpoint"] = copy.deepcopy(result["observed_checkpoint"])
            elif outcome == "suspension_deferred":
                result["continuation_mode"] = "continue_to_named_safe_point"
                result["next_safe_point"] = "dispatch_before_provider_post"
                result["continuation_deadline"] = "2026-09-15T12:04:30Z"
            elif outcome == "provider_boundary_ambiguous":
                result["provider_boundary"] = "entry_or_result_ambiguous"
            _rebind(result, receipt, command)
            with self.subTest(outcome=outcome):
                validate_suspension_result(result, request=request, envelope=envelope)
                validate_suspension_receipt(
                    receipt, result=result, request=request, envelope=envelope,
                )
                validate_suspension_command_result(
                    command, result=result, receipt=receipt,
                    request=request, envelope=envelope,
                )

    def test_root_identity_and_relocation_fail_closed(self):
        envelope, *_ = _docs()
        for mutation in ("nested", "digest", "relative"):
            changed = copy.deepcopy(envelope)
            if mutation == "nested":
                changed["control_root"] = changed["executable_workspace_root"] + "\\control"
                changed["control_root_sha256"] = hashlib.sha256(changed["control_root"].encode()).hexdigest()
            elif mutation == "digest":
                changed["control_root_sha256"] = SHA_A
            else:
                changed["control_root"] = "relative/control"
                changed["control_root_sha256"] = hashlib.sha256(changed["control_root"].encode()).hexdigest()
            changed["envelope_sha256"] = _digest_without(changed, "envelope_sha256")
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_supervision_invocation(changed)

    def test_stale_and_wrong_identity_requests_fail_closed(self):
        envelope, request, *_ = _docs()
        with self.assertRaisesRegex(ValueError, "expired"):
            validate_suspension_request(
                request, envelope=envelope, observed_at="2026-09-15T12:04:01Z",
            )
        for field, replacement in (
            ("launch_generation", request["launch_generation"] + 1),
            ("native_run_id", "native-run-other"),
            ("job_id", "job-other"), ("lease_id", "lease-other"),
            ("command_sha256", SHA_D), ("control_root_sha256", SHA_D),
            ("supervision_capability_sha256", SHA_C),
        ):
            changed = copy.deepcopy(request)
            changed[field] = replacement
            changed["request_sha256"] = _digest_without(changed, "request_sha256")
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "join"):
                validate_suspension_request(changed, envelope=envelope)
        changed = copy.deepcopy(request)
        changed["request_sha256"] = SHA_D
        with self.assertRaisesRegex(ValueError, "digest"):
            validate_suspension_request(changed, envelope=envelope)

    def test_bundle_enforces_global_transport_uniqueness(self):
        envelope, request, result, receipt, command = _docs()
        case = {"name": "positive-one", "envelope": envelope, "request": request,
                "result": result, "receipt": receipt, "command_result": command}
        bundle = seal_document({
            "schema_version": "astrowoof.native_suspension_fixture_bundle.v1",
            "bundle_sha256": "", "cases": [case],
        }, "bundle_sha256")
        self.assertEqual(bundle, validate_suspension_fixture_bundle(bundle))
        duplicate = copy.deepcopy(bundle)
        duplicate["cases"].append(copy.deepcopy(case))
        duplicate["cases"][1]["name"] = "positive-two"
        duplicate["bundle_sha256"] = _digest_without(duplicate, "bundle_sha256")
        with self.assertRaisesRegex(ValueError, "duplicated"):
            validate_suspension_fixture_bundle(duplicate)

    def test_bundle_rejects_second_resealed_result_for_same_request(self):
        envelope, request, result, receipt, command = _docs()
        first = {"name": "canonical", "envelope": envelope, "request": request,
                 "result": result, "receipt": receipt, "command_result": command}
        second = copy.deepcopy(first)
        second["name"] = "conflicting-second-result"
        second["result"]["reason_code"] = "different-semantic-conclusion"
        _rebind(second["result"], second["receipt"], second["command_result"])
        bundle = seal_document({
            "schema_version": "astrowoof.native_suspension_fixture_bundle.v1",
            "bundle_sha256": "", "cases": [first, second],
        }, "bundle_sha256")

        with self.assertRaisesRegex(ValueError, "request identity is duplicated"):
            validate_suspension_fixture_bundle(bundle)

    def test_packaged_fixture_bundle_contains_full_joined_documents(self):
        bundle = read_native_suspension_fixture_bundle()
        self.assertEqual(["suspended-checkpointed"], [
            case["name"] for case in bundle["cases"]
        ])

    def test_full_schema_resource_is_packaged_and_closed(self):
        schema = read_native_suspension_contract_schema()
        self.assertEqual(
            {"supervision_invocation", "suspension_request", "suspension_result",
             "suspension_receipt", "command_result", "checkpoint", "action",
             "fixture_case", "fixture_bundle", "sha256"},
            set(schema["$defs"]),
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        envelope, request, result, receipt, command = _docs()
        for name, value in (
            ("supervision_invocation", envelope), ("suspension_request", request),
            ("suspension_result", result), ("suspension_receipt", receipt),
            ("command_result", command),
        ):
            with self.subTest(name=name):
                jsonschema.validate(value, {**schema, "$ref": f"#/$defs/{name}"})
        jsonschema.validate(
            read_native_suspension_fixture_bundle(),
            {**schema, "$ref": "#/$defs/fixture_bundle"},
        )


if __name__ == "__main__":
    unittest.main()
