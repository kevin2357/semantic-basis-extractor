from __future__ import annotations

import copy
import hashlib
import json
import unittest

from astrowoof_natal_authoring import (
    read_duplicate_submission_fence_fixtures,
    read_duplicate_submission_fence_fixtures_schema,
    validate_duplicate_submission_fence_fixtures,
)


def _digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _reseal_bundle(value: dict) -> None:
    value["bundle_sha256"] = _digest({
        key: item for key, item in value.items() if key != "bundle_sha256"
    })


class CompletedRetryDuplicateSubmissionSlice3Tests(unittest.TestCase):
    def test_packaged_api_shaped_fixture_bundle_is_strict(self) -> None:
        value = read_duplicate_submission_fence_fixtures()
        validate_duplicate_submission_fence_fixtures(value)
        refusal = value["generic_provider_dispatch_refusal"]
        self.assertEqual("fresh_lifecycle_inspection", refusal["next_step"])
        self.assertEqual("not_attempted", refusal["provider_io_disposition"])
        contradiction = value["local_work_progress_contradiction"]
        self.assertEqual(2, contradiction["command_result"]["exit_code"])
        self.assertEqual(
            "local_work_progress_contradiction",
            contradiction["native_result"]["cause_code"],
        )
        self.assertEqual(
            ["paid_000000000000000000000101"],
            contradiction["native_result"]["reconciliation_action_ids"],
        )

    def test_schema_validates_when_jsonschema_is_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        jsonschema.Draft202012Validator(
            read_duplicate_submission_fence_fixtures_schema()
        ).validate(read_duplicate_submission_fence_fixtures())

    def test_recomputed_outer_digest_cannot_hide_nested_mutation(self) -> None:
        fixture = read_duplicate_submission_fence_fixtures()
        mutations = []

        refusal = copy.deepcopy(fixture)
        refusal["generic_provider_dispatch_refusal"]["next_step"] = "ordinary_resume"
        _reseal_bundle(refusal)
        mutations.append(refusal)

        cause = copy.deepcopy(fixture)
        cause["local_work_progress_contradiction"]["native_result"][
            "cause_code"
        ] = "final_qa_requires_review"
        _reseal_bundle(cause)
        mutations.append(cause)

        receipt = copy.deepcopy(fixture)
        receipt["local_work_progress_contradiction"]["publication_receipt"][
            "result_sha256"
        ] = "9" * 64
        _reseal_bundle(receipt)
        mutations.append(receipt)

        provider = copy.deepcopy(fixture)
        provider["local_work_progress_contradiction"]["native_result"][
            "action_dispositions"
        ][0]["provider_operation_id"] = None
        _reseal_bundle(provider)
        mutations.append(provider)

        for mutated in mutations:
            with self.subTest(mutated=mutated):
                with self.assertRaises(ValueError):
                    validate_duplicate_submission_fence_fixtures(mutated)

    def test_fixture_is_privacy_bounded(self) -> None:
        serialized = json.dumps(read_duplicate_submission_fence_fixtures())
        for forbidden in (
            "BEGIN_PROTECTED_PROMPT", "OPENAI_API_KEY", "request_payload",
            "subject_name", "cards.json",
        ):
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
