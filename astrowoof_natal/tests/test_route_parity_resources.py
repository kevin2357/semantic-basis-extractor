from __future__ import annotations

import copy
import hashlib
import io
import json
import sys
import unittest
import tempfile
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.route_parity import (  # noqa: E402
    read_bounded_route_parity_traces,
    read_route_parity_oracle,
    validate_bounded_route_traces,
    validate_route_parity_oracle,
)


class TestRouteParityResources(unittest.TestCase):
    def test_consumer_review_manifest_binds_packaged_resources(self) -> None:
        sprint = ROOT / "docs" / "sprints" / "2026" / "08" / "20260818-bounded-authoring-topology-transport-parity-sprint2"
        manifest = json.loads((sprint / "fixtures" / "bounded-route-parity-slice7-consumer-review.json").read_text(encoding="utf-8"))
        package = ROOT / "src" / "astrowoof_natal_authoring" / "resources"
        for item in manifest["resources"]:
            self.assertEqual(
                item["sha256"],
                hashlib.sha256((package / item["installed_path"]).read_bytes()).hexdigest(),
            )

    def test_packaged_oracle_v2_is_strict_and_complete(self) -> None:
        oracle = read_route_parity_oracle()
        names = {item["name"] for item in oracle["scenarios"]}
        self.assertEqual({
            "bounded_batch_awaiting_authorization", "bounded_batch_pending",
            "bounded_batch_not_due", "bounded_batch_reclaimed",
            "bounded_batch_mixed_member_continuation",
            "bounded_batch_retry_pending", "bounded_batch_usage_unavailable",
            "bounded_batch_ambiguous", "bounded_batch_provider_failed",
            "bounded_legacy_topology_unsupported", "bounded_pre_native_failure",
            "bounded_batch_delivery",
        }, names)
        self.assertTrue(all(
            item["native_route"]["route_family"] == "bounded_natal"
            for item in oracle["scenarios"]
        ))
        malformed = copy.deepcopy(oracle)
        malformed["scenarios"][0]["consumer_guess"] = True
        with self.assertRaises(ValueError):
            validate_route_parity_oracle(malformed)
        malformed = copy.deepcopy(oracle)
        malformed["scenarios"][0]["cycle_outcome"] = "new_public_state"
        with self.assertRaises(ValueError):
            validate_route_parity_oracle(malformed)

    def test_route_traces_cover_required_consumer_paths(self) -> None:
        bundle = read_bounded_route_parity_traces()
        names = {trace["name"] for trace in bundle["traces"]}
        self.assertEqual({
            "interactive_multi_pass_and_retry",
            "batch_pending_not_due_reclaim_delivery",
            "batch_partial_member_pass_local_retry",
            "batch_usage_unavailable_after_retrieval",
            "batch_ambiguity_review",
            "batch_terminal_provider_failure",
        }, names)
        not_due = next(
            trace for trace in bundle["traces"]
            if trace["name"] == "batch_pending_not_due_reclaim_delivery"
        )["steps"][1]
        self.assertEqual("not_due", not_due["outcome"])
        self.assertEqual("release_until_due", not_due["capacity_disposition"])
        usage = next(
            trace for trace in bundle["traces"]
            if trace["name"] == "batch_usage_unavailable_after_retrieval"
        )["steps"][0]
        self.assertFalse(usage["retain_provider_custody"])
        self.assertTrue(usage["retain_consumer_authority"])
        malformed = copy.deepcopy(bundle)
        malformed["traces"][0]["steps"][1]["sequence"] = 9
        with self.assertRaises(ValueError):
            validate_bounded_route_traces(malformed)

    def test_public_package_exports_readers(self) -> None:
        import astrowoof_natal_authoring as public

        self.assertIn("read_route_parity_oracle", public.__all__)
        self.assertIn("read_bounded_route_parity_traces", public.__all__)
        self.assertEqual(
            "astrowoof.route_parity_transition_oracle.v2",
            public.read_route_parity_oracle()["schema_version"],
        )

    def test_provider_free_cli_exports_validated_resource(self) -> None:
        from astrowoof_natal_authoring.route_parity import main

        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "nested" / "oracle.json"
            with patch("sys.argv", ["astrowoof-route-parity-evidence", "--kind", "oracle", "--output", str(target)]), redirect_stdout(io.StringIO()):
                    main()
            self.assertEqual(read_route_parity_oracle(), __import__("json").loads(target.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
