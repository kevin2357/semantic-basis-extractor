from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from build_blinded_review_page import CHOICES, build


class BlindedReviewPageTests(unittest.TestCase):
    def test_closed_blinded_page_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            packet = {
                "schema_version": "astrowoof.private_blinded_editorial_review.v1",
                "rubric_version": "rubric-v1",
                "packet_id": "editorial-test-packet",
                "candidate_position": 1,
                "transition": [{"path": "cards.0.body", "before": "before </script>", "after": "after & better"}],
                "prior_findings": {"status": "reject", "warning_count": 1, "findings": []},
                "candidate_findings": {"status": "accept", "warning_count": 0, "findings": []},
                "candidate_validation": {"status": "pass", "errors": []},
                "provenance": {"candidate_semantic_sha256": "a" * 64},
            }
            path = root / "packet.json"
            path.write_text(json.dumps(packet), encoding="utf-8")
            html, receipt = build(root)
            self.assertEqual(receipt["packet_count"], 1)
            self.assertEqual(receipt["choice_vocabulary"], list(CHOICES))
            self.assertFalse(receipt["answer_key_embedded"])
            self.assertEqual(receipt["network_dependency_count"], 0)
            self.assertIn("editorial-test-packet", receipt["packet_ids"])
            self.assertNotIn("before </script>", html)
            self.assertNotIn("source_label", html)
            self.assertNotIn("native_run_id", html)
            self.assertNotIn("subject_id", html)
            self.assertIn("complete!==payload.packets.length", html)
            self.assertIn("packet_file_sha256", html)
            self.assertIn("astrowoof.private_editorial_judgments.v1", html)

    def test_rejects_mixed_rubrics(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for index, rubric in enumerate(("a", "b")):
                (root / f"{index}.json").write_text(json.dumps({
                    "schema_version": "astrowoof.private_blinded_editorial_review.v1",
                    "rubric_version": rubric,
                    "packet_id": str(index),
                }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "one rubric"):
                build(root)


if __name__ == "__main__":
    unittest.main()
