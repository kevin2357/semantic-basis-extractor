from __future__ import annotations

import unittest

from astrowoof_natal_authoring.provider_economics_qa import (
    read_provider_economics_qualification_schema,
    run_provider_economics_qualification,
    validate_provider_economics_qualification,
)


class ProviderEconomicsQualificationTests(unittest.TestCase):
    def test_provider_free_four_route_qualification(self):
        receipt = run_provider_economics_qualification()
        self.assertEqual("passed", receipt["outcome"])
        self.assertEqual(0, receipt["external_provider_io_count"])
        self.assertTrue(all(receipt["checks"].values()))
        validate_provider_economics_qualification(receipt)

    def test_packaged_schema(self):
        schema = read_provider_economics_qualification_schema()
        self.assertEqual(
            "astrowoof.provider_economics_qualification.v1",
            schema["properties"]["schema_version"]["const"],
        )


if __name__ == "__main__":
    unittest.main()
