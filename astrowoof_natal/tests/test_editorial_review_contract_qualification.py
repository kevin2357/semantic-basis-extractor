from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess
import unittest
from unittest.mock import patch

from astrowoof_natal_authoring.editorial_review_contracts import (
    digest_without, validate_closed_root,
)
from astrowoof_natal_authoring.editorial_review_fixtures import (
    read_packaged_editorial_review_fixture,
    validate_editorial_review_fixture_bundle,
)
from astrowoof_natal_authoring.editorial_review_qa import (
    run_editorial_review_contract_qualification,
    validate_editorial_review_contract_qualification,
)


class TestEditorialReviewContractQualification(unittest.TestCase):
    def test_receipt_is_deterministic_closed_and_payload_free(self):
        left = run_editorial_review_contract_qualification()
        right = run_editorial_review_contract_qualification()
        self.assertEqual(left, right)
        self.assertTrue(validate_editorial_review_contract_qualification(left))
        self.assertEqual("valid", validate_closed_root(left, "qualification").outcome)
        encoded = json.dumps(left, sort_keys=True)
        for forbidden in ("synthetic accepted", "synthetic closeout", "provider payload", "api_key", "endpoint token"):
            self.assertNotIn(forbidden, encoded.lower())

    def test_all_rehashed_counterexamples_are_typed_and_unique(self):
        receipt = run_editorial_review_contract_qualification()
        cases = receipt["mutation_results"]
        self.assertEqual(39, len(cases))
        self.assertEqual(39, len({item["case"] for item in cases}))
        self.assertEqual(
            {"ineligible_route", "contradictory_evidence", "digest_mismatch", "incomplete_evidence", "invalid_schema"},
            {item["classification"] for item in cases},
        )
        self.assertTrue(all(item["rule_id"] and item["safe_detail_code"] for item in cases))

    def test_receipt_tampering_is_rejected(self):
        receipt = run_editorial_review_contract_qualification()
        receipt["mutation_results"].pop()
        self.assertFalse(validate_editorial_review_contract_qualification(receipt))

    def test_record_limit_fails_before_shallow_projection_noise(self):
        bundle = deepcopy(read_packaged_editorial_review_fixture("accepted_delivery"))
        events = bundle["editorial_request"]["events"]
        while len(events) <= 99:
            events.append(deepcopy(events[-1]))
        bundle["bundle_sha256"] = digest_without(bundle, "bundle_sha256")
        result = validate_editorial_review_fixture_bundle(bundle)
        self.assertEqual(("record_limit_exceeded", "event_limit_exceeded"), (result.classification, result.safe_detail_code))

    def test_qualification_constructs_no_network_or_subprocess(self):
        def forbidden(*args, **kwargs):
            raise AssertionError("external side effect attempted")
        with patch.object(socket, "socket", forbidden), patch.object(subprocess, "Popen", forbidden):
            receipt = run_editorial_review_contract_qualification()
        self.assertEqual({0}, set(receipt["side_effects"].values()))


if __name__ == "__main__":
    unittest.main()
