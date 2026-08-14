from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.extractor import (  # noqa: E402
    build_candidates,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    optimize,
    qa_report,
)


BASELINE = (
    ROOT
    / "docs"
    / "sprints"
    / "2026"
    / "08"
    / "20260812-bounded-btime-ingestion-sprint1"
    / "results"
    / "slice0-baseline-contracts.json"
)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class TestBoundedSprintBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_reserved_contract_names_are_versioned_and_distinct(self) -> None:
        names = list(self.baseline["reserved_contract_names"].values())
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(name.endswith(".v1") for name in names))
        self.assertTrue(all("bounded_natal" in name for name in names))

    def test_frozen_exact_bre_replay(self) -> None:
        packages = discover_subject_packages(ROOT / "examples", "bre")
        contexts, registry, input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )
        candidates, analysis = build_candidates(contexts)
        selected, rejected, _ = optimize(candidates)
        packet = compile_packet(
            "bre",
            contexts,
            selected,
            rejected,
            analysis,
            registry,
            input_audit,
        )
        qa = qa_report(candidates, selected, rejected, packet)
        expected = self.baseline["exact_bre_replay"]

        self.assertEqual(expected["candidate_count"], len(candidates))
        self.assertEqual(
            expected["candidate_sha256"],
            canonical_sha256([candidate.as_dict() for candidate in candidates]),
        )
        self.assertEqual(expected["selected_count"], len(selected))
        self.assertEqual(
            expected["selected_sha256"],
            canonical_sha256([candidate.as_dict() for candidate in selected]),
        )
        self.assertEqual(expected["rejected_count"], len(rejected))
        self.assertEqual(expected["packet_sha256"], canonical_sha256(packet))
        self.assertEqual(expected["qa_sha256"], canonical_sha256(qa))
        self.assertEqual(expected["qa_status"], qa["status"])

    def test_bounded_fixture_inventory_is_hash_complete(self) -> None:
        for fixture_name in ("sanitized_bounded_fixture", "full_scale_bounded_fixture"):
            fixture = self.baseline[fixture_name]
            for key, value in fixture.items():
                if key.endswith("sha256") and isinstance(value, str):
                    self.assertRegex(value, r"^[0-9a-f]{64}$")
        projected = self.baseline["sanitized_bounded_fixture"][
            "projected_file_sha256"
        ]
        self.assertEqual(4, len(projected))
        self.assertTrue(all(len(value) == 64 for value in projected.values()))


if __name__ == "__main__":
    unittest.main()
