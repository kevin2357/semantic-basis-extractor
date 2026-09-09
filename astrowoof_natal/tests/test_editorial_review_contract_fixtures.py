from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from astrowoof_natal_authoring.editorial_review_contracts import (
    canonical_editorial_review_json,
    derive_decision_id,
    validate_closed_root,
)
from astrowoof_natal_authoring.editorial_review_fixtures import (
    FIXTURE_KINDS,
    build_editorial_review_capture_status,
    build_editorial_review_fixture_bundle,
    read_editorial_review_fixture_bundle,
    read_packaged_editorial_review_fixture,
    validate_editorial_review_fixture_bundle,
    validate_editorial_review_request,
)


class TestEditorialReviewPositiveFixtures(unittest.TestCase):
    def test_binding_digest_is_the_only_identity_and_rekeys_decision(self):
        bundle = build_editorial_review_fixture_bundle("accepted_delivery")
        packet = bundle["editorial_request"]["events"][0]["native_content"]
        decision = deepcopy(packet["lineage"]["decisions"][0])
        self.assertNotIn('"binding_id"', canonical_editorial_review_json(bundle).decode("utf-8"))
        original = derive_decision_id(packet["packet_id"], decision)
        decision["action"]["binding_sha256"] = "f" * 64
        self.assertNotEqual(original, derive_decision_id(packet["packet_id"], decision))

    def test_both_production_shaped_worlds_validate_and_are_deterministic(self):
        for kind in sorted(FIXTURE_KINDS):
            with self.subTest(kind=kind):
                left = build_editorial_review_fixture_bundle(kind)
                right = build_editorial_review_fixture_bundle(kind)
                self.assertEqual(left, right)
                self.assertEqual("valid", validate_editorial_review_fixture_bundle(left).outcome)
                self.assertEqual(left, read_editorial_review_fixture_bundle(canonical_editorial_review_json(left)))
                self.assertEqual(left, read_packaged_editorial_review_fixture(kind))

    def test_accepted_world_has_initial_retry_optional_and_delivery_continuity(self):
        bundle = build_editorial_review_fixture_bundle("accepted_delivery")
        packet = bundle["editorial_request"]["events"][0]["native_content"]
        decisions = packet["lineage"]["decisions"]
        self.assertEqual(list(range(1, 7)), [item["initial_pass_index"] for item in decisions[:6]])
        self.assertEqual(["creative_retry", "polish", "polish"], [item["stage"] for item in decisions[6:]])
        self.assertEqual("rejected", decisions[0]["transition"]["acceptance_outcome"])
        self.assertNotIn("accepted_workspace_id", decisions[0]["transition"])
        self.assertEqual("accepted", decisions[6]["transition"]["acceptance_outcome"])
        self.assertEqual(decisions[0]["decision_id"], decisions[6]["transition"]["predecessor_decision_id"])
        self.assertEqual("candidate_adopted", decisions[7]["transition"]["adoption_outcome"])
        self.assertEqual(decisions[7]["transition"]["output_deck"], decisions[8]["transition"]["input_deck"])
        self.assertEqual(packet["terminal_selection"]["selected_deck"], packet["terminal_selection"]["delivered_deck"])

    def test_closeout_world_has_nonmaterialized_and_nonadopted_candidates(self):
        bundle = build_editorial_review_fixture_bundle("editorial_closeout")
        packet = bundle["editorial_request"]["events"][0]["native_content"]
        decisions = packet["lineage"]["decisions"]
        self.assertNotIn("candidate_deck", decisions[7]["transition"])
        self.assertEqual("not_materialized", decisions[7]["transition"]["materialization_outcome"])
        self.assertEqual("candidate_not_adopted", decisions[8]["transition"]["adoption_outcome"])
        self.assertNotIn("delivered_deck", packet["terminal_selection"])
        modes = {item["population"]["mode"] for item in packet["findings"]}
        self.assertEqual({"claim_ids", "count_only", "not_claim_scoped"}, modes)

    def test_editorial_request_is_complete_without_artifact_delivery(self):
        for kind in FIXTURE_KINDS:
            bundle = build_editorial_review_fixture_bundle(kind)
            events = bundle["editorial_request"]["events"]
            before = canonical_editorial_review_json(events)
            self.assertEqual("valid", validate_editorial_review_request(events).outcome)
            stripped = deepcopy(bundle)
            stripped["artifact_batches"] = []
            self.assertEqual(before, canonical_editorial_review_json(stripped["editorial_request"]["events"]))
            self.assertEqual("valid", validate_editorial_review_request(stripped["editorial_request"]["events"]).outcome)

    def test_capture_statuses_are_closed_absence_witnesses(self):
        reasons = {
            "ineligible_route", "unsupported_result_version",
            "incomplete_native_evidence", "contradictory_native_evidence",
            "editorial_request_record_limit_exceeded",
            "editorial_request_byte_limit_exceeded",
        }
        for reason in reasons:
            status = build_editorial_review_capture_status(reason)
            self.assertEqual("valid", validate_closed_root(status, "capture_status").outcome)
            serialized = json.dumps(status, sort_keys=True)
            for forbidden in ("packet_id", "packet_sha256", "projection_id", "projection_sha256"):
                self.assertNotIn(forbidden, serialized)

    def test_duplicate_keys_fail_through_public_fixture_reader(self):
        with self.assertRaises(ValueError):
            read_editorial_review_fixture_bundle(b'{"schema_version":"x","schema_version":"y"}')

    def test_fresh_process_hash_seed_and_workspace_do_not_change_bundle_bytes(self):
        code = (
            "from astrowoof_natal_authoring.editorial_review_contracts import canonical_editorial_review_json;"
            "from astrowoof_natal_authoring.editorial_review_fixtures import build_editorial_review_fixture_bundle;"
            "import hashlib,sys;"
            "sys.stdout.write(hashlib.sha256(canonical_editorial_review_json(build_editorial_review_fixture_bundle(sys.argv[1]))).hexdigest())"
        )
        env = dict(os.environ)
        source = str(Path(__file__).parents[1] / "src")
        env["PYTHONPATH"] = source
        digests = set()
        for seed, kind in (("1", "accepted_delivery"), ("91", "accepted_delivery"), ("2", "editorial_closeout"), ("92", "editorial_closeout")):
            with tempfile.TemporaryDirectory() as directory:
                run_env = dict(env, PYTHONHASHSEED=seed, TZ="Pacific/Kiritimati")
                digest = subprocess.check_output([sys.executable, "-c", code, kind], cwd=directory, env=run_env, text=True)
                digests.add((kind, digest))
        self.assertEqual(2, len(digests))


if __name__ == "__main__":
    unittest.main()
