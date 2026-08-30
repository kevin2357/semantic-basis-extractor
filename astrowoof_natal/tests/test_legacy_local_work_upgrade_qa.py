from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest

from astrowoof_natal_authoring import (
    build_legacy_local_work_upgrade_bundle,
    read_legacy_local_work_upgrade_fixture,
    read_legacy_local_work_upgrade_bundle_schema,
    read_legacy_local_work_upgrade_qualification_schema,
    run_legacy_local_work_upgrade_qualification,
    validate_legacy_local_work_upgrade_bundle,
    validate_legacy_local_work_upgrade_qualification,
)


class LegacyLocalWorkUpgradeQualificationTests(unittest.TestCase):
    @staticmethod
    def _rehash_bundle(bundle: dict) -> None:
        from astrowoof_natal_authoring.legacy_local_work_upgrade_qa import _digest
        body = {key: item for key, item in bundle.items() if key != "bundle_sha256"}
        bundle["bundle_sha256"] = _digest(body)

    def test_packaged_schemas_accept_public_artifacts_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        jsonschema.Draft202012Validator(
            read_legacy_local_work_upgrade_bundle_schema()
        ).validate(build_legacy_local_work_upgrade_bundle())
        jsonschema.Draft202012Validator(
            read_legacy_local_work_upgrade_qualification_schema()
        ).validate(run_legacy_local_work_upgrade_qualification())

    def test_module_cli_emits_closed_receipt(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "astrowoof_natal_authoring.legacy_local_work_upgrade_qa"],
            check=True, capture_output=True, text=True,
        )
        receipt = json.loads(completed.stdout)
        validate_legacy_local_work_upgrade_qualification(receipt)
        serialized = completed.stdout.lower()
        for forbidden in ("sanitized qualification", "resp_fixture", "\\temp\\", "/tmp/"):
            self.assertNotIn(forbidden, serialized)

    def test_bundle_and_receipt_cover_closed_scenarios(self) -> None:
        bundle = build_legacy_local_work_upgrade_bundle()
        validate_legacy_local_work_upgrade_bundle(bundle)
        receipt = run_legacy_local_work_upgrade_qualification()
        validate_legacy_local_work_upgrade_qualification(receipt)
        fixture = read_legacy_local_work_upgrade_fixture()
        self.assertEqual(
            fixture["scenario_ids"],
            [item["scenario_id"] for item in receipt["scenarios"]],
        )
        self.assertEqual(0, receipt["provider_io"]["create_count"])
        self.assertEqual(0, receipt["provider_io"]["retrieve_count"])

    def test_receipt_is_reproducible_across_fresh_workspaces(self) -> None:
        self.assertEqual(
            run_legacy_local_work_upgrade_qualification(),
            run_legacy_local_work_upgrade_qualification(),
        )

    def test_bundle_rejects_rehashed_identity_join_mutation(self) -> None:
        bundle = build_legacy_local_work_upgrade_bundle()
        changed = copy.deepcopy(bundle)
        changed["scenarios"][0]["stable_identity_join"] = False
        self._rehash_bundle(changed)
        with self.assertRaisesRegex(ValueError, "identity join"):
            validate_legacy_local_work_upgrade_bundle(changed)

    def test_bundle_derives_v05_seam_from_embedded_document(self) -> None:
        changed = copy.deepcopy(build_legacy_local_work_upgrade_bundle())
        changed["scenarios"][0]["documents"]["v05"]["local_dependencies"] = [
            {
                "kind": "retry_preparation",
                "blocking": True,
                "reason_code": "prepared_action_authorization_pending",
            }
        ]
        self._rehash_bundle(changed)
        with self.assertRaisesRegex(ValueError, "v0.5 seam evidence"):
            validate_legacy_local_work_upgrade_bundle(changed)

    def test_bundle_rejects_rehashed_projection_mutations(self) -> None:
        for projection in ("local_source_action_ids", "custody_action_ids"):
            with self.subTest(projection=projection):
                changed = copy.deepcopy(build_legacy_local_work_upgrade_bundle())
                changed["scenarios"][0][projection] = []
                self._rehash_bundle(changed)
                with self.assertRaisesRegex(ValueError, "scenario projection"):
                    validate_legacy_local_work_upgrade_bundle(changed)

    def test_bundle_rejects_rehashed_conflict_outcome_mutation(self) -> None:
        from astrowoof_natal_authoring.legacy_local_work_upgrade_qa import _digest
        changed = copy.deepcopy(build_legacy_local_work_upgrade_bundle())
        conflict = changed["conflict_qualification"]
        conflict["routes"][0]["after"]["conflict_classification"] = None
        conflict_body = {
            key: item for key, item in conflict.items() if key != "receipt_sha256"
        }
        conflict["receipt_sha256"] = _digest(conflict_body)
        self._rehash_bundle(changed)
        with self.assertRaisesRegex(ValueError, "projection assertions"):
            validate_legacy_local_work_upgrade_bundle(changed)

    def test_receipt_rejects_rehashed_outcome_and_privacy_mutations(self) -> None:
        from astrowoof_natal_authoring.legacy_local_work_upgrade_qa import _digest
        for mutate in ("outcome", "privacy"):
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(run_legacy_local_work_upgrade_qualification())
                if mutate == "outcome":
                    changed["scenarios"][0]["selected_outcome"] = "none"
                else:
                    changed["privacy"]["contains_prompt"] = True
                body = {key: item for key, item in changed.items() if key != "receipt_sha256"}
                changed["receipt_sha256"] = _digest(body)
                with self.assertRaises(ValueError):
                    validate_legacy_local_work_upgrade_qualification(changed)


if __name__ == "__main__":
    unittest.main()
