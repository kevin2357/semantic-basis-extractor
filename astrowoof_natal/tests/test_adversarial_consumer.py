from __future__ import annotations

import copy
import unittest
from importlib.resources import files

from astrowoof_natal_authoring import (
    read_adversarial_consumer_catalog,
    validate_adversarial_consumer_catalog,
)


class AdversarialConsumerCatalogTests(unittest.TestCase):
    def test_catalog_is_closed_and_all_packaged_hashes_validate(self):
        catalog = read_adversarial_consumer_catalog()
        validate_adversarial_consumer_catalog(catalog)
        self.assertEqual(15, len(catalog["cases"]))
        packaged = [
            item for item in catalog["cases"]
            if item["evidence_kind"] == "packaged_fixture"
        ]
        self.assertTrue(packaged)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in packaged))
        root = files("astrowoof_natal_authoring").joinpath(
            "resources", "fixtures"
        )
        for item in packaged:
            with self.subTest(case_id=item["case_id"]):
                fixture = root.joinpath(*item["evidence_ref"].split("/"))
                self.assertNotIn(b"\r\n", fixture.read_bytes())

    def test_joint_inventory_separates_sbe_and_api_owned_cases(self):
        catalog = read_adversarial_consumer_catalog()
        indexed = {item["case_id"]: item for item in catalog["cases"]}
        self.assertEqual("joint", indexed["muffin_review_capacity"]["owner"])
        self.assertEqual("api", indexed["expired_lost_lease"]["owner"])
        self.assertEqual("sbe", indexed["provider_pending_4_plus_2"]["owner"])
        self.assertEqual(
            "api_fixture_required",
            indexed["three_run_starvation"]["evidence_kind"],
        )

    def test_mutation_fails_closed(self):
        catalog = read_adversarial_consumer_catalog()
        changed = copy.deepcopy(catalog)
        changed["cases"][0]["owner"] = "everybody"
        with self.assertRaises(ValueError):
            validate_adversarial_consumer_catalog(changed)


if __name__ == "__main__":
    unittest.main()
