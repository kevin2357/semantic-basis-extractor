"""Provider-free reproduction of the terminal binding digest-domain split."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import unittest

from astrowoof_natal_authoring.editorial_review_contracts import (
    canonical_editorial_review_json,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    _binding,
    _digest,
    build_terminal_action_dispositions,
)


def realistic_action() -> dict:
    return {
        "action_id": "paid_1234567890abcdef12345678",
        "state": "REPORTED",
        "binding": {
            "action_id": "paid_1234567890abcdef12345678",
            "stage": "authoring_initial",
            "route": "subject_1:attempt-001",
            "request_sha256": "1" * 64,
            "profile_sha256": "2" * 64,
            "maximum_output_tokens": 100000,
            "commitment_micro_usd": 123456,
            "price_book_version": "test-price-book.v1",
            "model": "test-model",
            "prepared_state_revision": 1,
            "run_id": "run-live-shape",
            "service_level": "interactive",
        },
        "provider": {"id": "resp_test"},
        "consumption": {"consumer_id": "test"},
        "reported": {"usage": {"total_tokens": 1}},
    }


class TestTerminalBindingDigestDomain(unittest.TestCase):
    def test_realistic_binding_reproduces_current_capture_join_failure(self) -> None:
        action = realistic_action()
        state = {"route": "exact_natal.v1", "spend_ledger": {"actions": [action]}}
        disposition = build_terminal_action_dispositions(state)[0]
        current_capture_digest = sha256(
            canonical_editorial_review_json(action["binding"])
        ).hexdigest()
        self.assertEqual(disposition["binding_sha256"], _digest(_binding(action)))
        self.assertNotEqual(disposition["binding_sha256"], current_capture_digest)

    def test_closed_fields_remain_bound_and_extra_fields_do_not_redefine_contract(self) -> None:
        action = realistic_action()
        original = _digest(_binding(action))
        replacements = {
            "stage": "creative_retry",
            "route": "subject_1:attempt-002",
            "request_sha256": "3" * 64,
            "profile_sha256": "4" * 64,
            "maximum_output_tokens": 99999,
            "commitment_micro_usd": 123457,
            "price_book_version": "test-price-book.v2",
        }
        for field, replacement in replacements.items():
            changed = deepcopy(action)
            changed["binding"][field] = replacement
            self.assertNotEqual(original, _digest(_binding(changed)), field)
        changed_id = deepcopy(action)
        changed_id["action_id"] = "paid_abcdef1234567890abcdef12"
        self.assertNotEqual(original, _digest(_binding(changed_id)), "action_id")
        for field in ("model", "prepared_state_revision", "run_id", "service_level"):
            changed = deepcopy(action)
            changed["binding"][field] = f"changed-{field}"
            self.assertEqual(original, _digest(_binding(changed)), field)


if __name__ == "__main__":
    unittest.main()
