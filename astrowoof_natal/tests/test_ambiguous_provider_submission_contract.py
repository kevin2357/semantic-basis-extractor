from __future__ import annotations

import copy
import unittest

from astrowoof_natal_authoring import (
    build_external_authority_provider_dispatch_result_v3,
    build_external_authority_v2_command_result_v2,
    read_external_authority_provider_dispatch_result_v3_schema,
    read_external_authority_v2_command_result_v2_schema,
    read_ambiguous_provider_submission_fixture_v1,
    validate_external_authority_provider_dispatch_result_v3,
    validate_external_authority_v2_command_result_v2,
)


ACTION_1 = "paid_000000000000000000000001"
ACTION_2 = "paid_000000000000000000000002"
SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64


def dispatch_case(outcome: str, *, reason_code: str | None = None):
    common = {
        "outcome": outcome,
        "reason_code": reason_code,
        "run_id": "run-fixture",
        "request_sha256": SHA_A,
        "grant_sha256": SHA_B,
        "ordered_action_ids": [ACTION_1, ACTION_2],
        "post_state_revision": 7,
        "post_snapshot_sha256": SHA_C,
    }
    if outcome == "pre_provider_refusal":
        return build_external_authority_provider_dispatch_result_v3(
            **common,
            provider_io_disposition="not_attempted",
            grant_invocation_disposition="refused",
            provider_bound_action_ids=[],
            ambiguous_action_ids=[],
            refused_action_ids=[ACTION_1],
            provider_operation_ids=[],
            prepared_create_records=[{
                "action_id": ACTION_1, "prepared_create_sha256": SHA_D,
            }],
        )
    if outcome == "ambiguous_submission":
        return build_external_authority_provider_dispatch_result_v3(
            **common,
            provider_io_disposition="create_entered_unknown",
            grant_invocation_disposition="create_entered_unknown",
            provider_bound_action_ids=[],
            ambiguous_action_ids=[ACTION_1],
            refused_action_ids=[],
            provider_operation_ids=[],
            prepared_create_records=[{
                "action_id": ACTION_1, "prepared_create_sha256": SHA_D,
            }],
        )
    records = [
        {"action_id": ACTION_1, "prepared_create_sha256": SHA_C},
        {"action_id": ACTION_2, "prepared_create_sha256": SHA_D},
    ]
    return build_external_authority_provider_dispatch_result_v3(
        **common,
        provider_io_disposition="provider_identity_durable",
        grant_invocation_disposition=(
            "provider_pending" if outcome == "detached_provider_pending" else "replayed"
        ),
        provider_bound_action_ids=[ACTION_1, ACTION_2],
        ambiguous_action_ids=[],
        refused_action_ids=[],
        provider_operation_ids=["resp_fixture_1", "resp_fixture_2"],
        prepared_create_records=records,
    )


class AmbiguousProviderSubmissionContractWaypoint1(unittest.TestCase):
    def test_all_closed_outcomes_validate(self):
        cases = (
            ("pre_provider_refusal", "request_payload_unavailable"),
            ("pre_provider_refusal", "request_payload_ambiguous"),
            ("pre_provider_refusal", "request_payload_digest_mismatch"),
            ("pre_provider_refusal", "provider_configuration_invalid"),
            ("ambiguous_submission", "provider_call_interrupted_after_fence"),
            ("ambiguous_submission", "provider_transport_failed_without_identity"),
            ("ambiguous_submission", "provider_returned_invalid_identity"),
            ("ambiguous_submission", "provider_identity_conflict"),
            ("detached_provider_pending", None),
            ("exact_replay", None),
        )
        for outcome, reason in cases:
            with self.subTest(outcome=outcome, reason=reason):
                value = dispatch_case(outcome, reason_code=reason)
                self.assertEqual(
                    value, validate_external_authority_provider_dispatch_result_v3(value)
                )

    def test_semantic_contradictions_fail_even_when_redigested(self):
        cases = (
            ("pre_provider_refusal", "request_payload_unavailable", {"provider_io_disposition": "create_entered_unknown"}),
            ("pre_provider_refusal", "request_payload_unavailable", {"grant_invocation_disposition": "provider_pending"}),
            ("pre_provider_refusal", "request_payload_unavailable", {"refused_action_ids": []}),
            ("ambiguous_submission", "provider_returned_invalid_identity", {"provider_io_disposition": "not_attempted"}),
            ("detached_provider_pending", None, {"provider_operation_ids": []}),
            ("exact_replay", None, {"reason_code": "provider_identity_conflict"}),
        )
        for outcome, reason, mutation in cases:
            with self.subTest(outcome=outcome, mutation=mutation):
                original = dispatch_case(outcome, reason_code=reason)
                fields = {
                    key: copy.deepcopy(value)
                    for key, value in original.items()
                    if key not in {"schema_version", "result_sha256"}
                }
                fields.update(mutation)
                with self.assertRaises(ValueError):
                    build_external_authority_provider_dispatch_result_v3(**fields)

    def test_command_v2_embeds_dispatch_v3_and_joins_outcome(self):
        dispatch = dispatch_case(
            "pre_provider_refusal", reason_code="request_payload_unavailable"
        )
        command = build_external_authority_v2_command_result_v2(
            intent_result=None, dispatch_result=dispatch,
        )
        self.assertEqual(
            "astrowoof.external_authority_v2_command_result.v2",
            command["schema_version"],
        )
        self.assertEqual(command, validate_external_authority_v2_command_result_v2(command))
        changed = copy.deepcopy(command)
        changed["outcome"] = "exact_replay"
        with self.assertRaises(ValueError):
            validate_external_authority_v2_command_result_v2(changed)

    def test_schemas_are_packaged_and_strict(self):
        dispatch_schema = read_external_authority_provider_dispatch_result_v3_schema()
        command_schema = read_external_authority_v2_command_result_v2_schema()
        self.assertEqual(
            "astrowoof.external_authority_provider_dispatch_result.v3",
            dispatch_schema["$id"],
        )
        self.assertEqual(
            "astrowoof.external_authority_v2_command_result.v2",
            command_schema["$id"],
        )
        self.assertFalse(dispatch_schema["additionalProperties"])
        self.assertFalse(command_schema["additionalProperties"])
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(dispatch_schema).validate(
            dispatch_case("pre_provider_refusal", reason_code="request_payload_unavailable")
        )

    def test_packaged_fixture_matrix_is_complete_and_privacy_minimized(self):
        fixture = read_ambiguous_provider_submission_fixture_v1()
        names = {case["name"] for case in fixture["cases"]}
        self.assertEqual({
            "missing_payload", "duplicate_payload", "digest_mismatch",
            "invalid_provider_configuration", "failure_after_call_entry",
            "transport_entered_failure", "malformed_returned_identity",
            "conflicting_returned_identity", "detached_provider_pending",
            "exact_replay", "contradictory_public_evidence",
        }, names)
        import json
        serialized = json.dumps(fixture, sort_keys=True).lower()
        for sentinel in (
            "prompt", "input", "api_key", "authorization: bearer",
            "protected_birth_location_sentinel", "subject_params",
        ):
            self.assertNotIn(sentinel, serialized)


if __name__ == "__main__":
    unittest.main()
