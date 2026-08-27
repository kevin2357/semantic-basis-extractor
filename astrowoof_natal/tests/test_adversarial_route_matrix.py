from __future__ import annotations

import copy
import unittest

import astrowoof_natal_authoring as public_api
from astrowoof_natal_authoring.adversarial_route_matrix import (
    build_adversarial_route_matrix_qualification,
    validate_adversarial_route_matrix_qualification,
)


class AdversarialRouteMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_adversarial_route_matrix_qualification()

    def test_public_surface_executes_real_qualification_join(self):
        self.assertIs(
            public_api.build_adversarial_route_matrix_qualification,
            build_adversarial_route_matrix_qualification,
        )
        validated = validate_adversarial_route_matrix_qualification(self.receipt)
        self.assertEqual("pass", validated["status"])
        self.assertEqual(22, len(validated["cells"]))
        self.assertEqual(0, validated["external_network_call_count"])
        self.assertEqual(0, validated["real_provider_create_count"])
        self.assertEqual(0, validated["provider_spend_usd"])

    def test_matrix_is_closed_and_classifies_batch_optional_stages(self):
        indexed = {item["cell_id"]: item for item in self.receipt["cells"]}
        for route in ("exact_natal", "bounded_natal"):
            self.assertEqual(
                "supported",
                indexed[f"{route}:response:authoring_initial"]["classification"],
            )
            self.assertEqual(
                "supported",
                indexed[f"{route}:batch:authoring_initial"]["classification"],
            )
            self.assertEqual(
                "supported",
                indexed[f"{route}:local:post_fan_in"]["classification"],
            )
            for stage in (
                "creative_retry", "polish", "qualitative_critic",
                "qualitative_candidate",
            ):
                self.assertEqual(
                    "supported", indexed[f"{route}:response:{stage}"]["classification"],
                )
                self.assertEqual(
                    "explicitly_refused",
                    indexed[f"{route}:batch:{stage}"]["classification"],
                )

    def test_mutation_and_missing_cell_fail_closed(self):
        changed = copy.deepcopy(self.receipt)
        changed["cells"][0]["classification"] = "deferred"
        with self.assertRaises(ValueError):
            validate_adversarial_route_matrix_qualification(changed)

        missing = copy.deepcopy(self.receipt)
        missing["cells"].pop()
        with self.assertRaises(ValueError):
            validate_adversarial_route_matrix_qualification(missing)


if __name__ == "__main__":
    unittest.main()
