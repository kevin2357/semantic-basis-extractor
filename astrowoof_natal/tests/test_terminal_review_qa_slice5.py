from __future__ import annotations

import copy
import hashlib
import json
import unittest
from importlib.resources import files

from astrowoof_natal_authoring import (
    read_terminal_review_qualification_schema,
    run_terminal_review_qualification,
    validate_terminal_review_qualification,
)
from astrowoof_natal_authoring.terminal_review_qa import _installed_version


def _with_fixture_release(receipt: dict, fixture_release: str) -> dict:
    normalized = copy.deepcopy(receipt)
    normalized["sbe_release"] = fixture_release
    basis = {
        key: item for key, item in normalized.items()
        if key != "receipt_sha256"
    }
    normalized["receipt_sha256"] = hashlib.sha256(json.dumps(
        basis, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()
    return normalized


class TerminalReviewQualificationTests(unittest.TestCase):
    def test_provider_free_public_qualification_is_reproducible(self) -> None:
        first = run_terminal_review_qualification()
        second = run_terminal_review_qualification()
        self.assertEqual(first, second)
        validate_terminal_review_qualification(first)
        self.assertEqual(_installed_version(), first["sbe_release"])
        self.assertEqual(0, first["checks"]["provider_post_count"])
        self.assertEqual(1, first["checks"]["scripted_get_count"])

    def test_receipt_mutation_is_refused(self) -> None:
        receipt = run_terminal_review_qualification()
        mutated = copy.deepcopy(receipt)
        mutated["checks"]["review_immutable"] = False
        with self.assertRaises(ValueError):
            validate_terminal_review_qualification(mutated)

    def test_rehashed_semantic_mutations_are_refused(self) -> None:
        for field, value in (
            ("reported_action_id", "paid_000000000000000000000199"),
            ("reconciliation_action_ids", ["paid_000000000000000000000199"]),
            ("providerless_denial_action_ids", ["paid_000000000000000000000199"]),
            ("successor_outcome", "provider_pending"),
            ("providerless_denial_outcome", "refused"),
        ):
            with self.subTest(field=field):
                mutated = copy.deepcopy(run_terminal_review_qualification())
                mutated["checks"][field] = value
                basis = {
                    key: item for key, item in mutated.items()
                    if key != "receipt_sha256"
                }
                mutated["receipt_sha256"] = hashlib.sha256(json.dumps(
                    basis, sort_keys=True, separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")).hexdigest()
                with self.assertRaises(ValueError):
                    validate_terminal_review_qualification(mutated)

    def test_packaged_fixture_is_the_release_normalized_receipt(self) -> None:
        resource = files("astrowoof_natal_authoring.resources").joinpath(
            "fixtures/lifecycle/terminal-review-qualification.v1.json"
        )
        fixture = json.loads(resource.read_text(encoding="utf-8"))
        self.assertEqual(
            _with_fixture_release(
                run_terminal_review_qualification(), fixture["sbe_release"]
            ),
            fixture,
        )

    def test_packaged_schema_validates_receipt_when_jsonschema_available(self) -> None:
        schema = read_terminal_review_qualification_schema()
        self.assertEqual(
            "astrowoof.terminal_review_qualification.v1", schema["$id"]
        )
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(schema).validate(
            run_terminal_review_qualification()
        )


if __name__ == "__main__":
    unittest.main()
