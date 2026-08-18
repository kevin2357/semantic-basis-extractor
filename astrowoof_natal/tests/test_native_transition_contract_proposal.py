from __future__ import annotations

import json
import unittest
from copy import deepcopy
from importlib.resources import files
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:  # Source-only lean test environments omit SPC's dependency.
    Draft202012Validator = None  # type: ignore[assignment,misc]
    ValidationError = Exception  # type: ignore[assignment,misc]


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "sprints" / "2026" / "08" / (
    "20260817-native-terminal-transition-journal-sprint1"
) / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
class TestNativeTransitionContractProposal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load("native-transition-contracts.proposal.schema.json")
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_canonical_journal_and_result_examples_validate(self) -> None:
        for name in (
            "native-transition-journal-record.proposal.json",
            "native-execution-result-review.proposal.json",
        ):
            with self.subTest(name=name):
                self.validator.validate(load(name))

    def test_unknown_outcome_and_additional_fields_fail_closed(self) -> None:
        result = load("native-execution-result-review.proposal.json")
        unknown = deepcopy(result)
        unknown["outcome"] = "retry_lol"
        with self.assertRaises(ValidationError):
            self.validator.validate(unknown)
        expanded = deepcopy(result)
        expanded["consumer_guess"] = "retry"
        with self.assertRaises(ValidationError):
            self.validator.validate(expanded)

    def test_provider_id_and_cost_evidence_are_not_fabricated(self) -> None:
        record = load("native-transition-journal-record.proposal.json")
        started = deepcopy(record)
        started["record_kind"] = "provider.submission_started"
        started["provider_observation"]["observation_kind"] = "submission_started"
        with self.assertRaises(ValidationError):
            self.validator.validate(started)

        started["provider_observation"].update({
            "provider_operation_id": None,
            "cost_disposition": "no_provider_work_consumed",
            "price_book_version": None,
            "usage_evidence_ref": None,
            "estimated_micro_usd": None,
        })
        self.validator.validate(started)

        unavailable = deepcopy(record)
        unavailable["record_kind"] = "provider.usage_unavailable"
        unavailable["provider_observation"].update({
            "observation_kind": "usage_unavailable",
            "cost_disposition": (
                "provider_usage_unavailable_billing_reconciliation_pending"
            ),
            "price_book_version": None,
            "usage_evidence_ref": None,
            "estimated_micro_usd": 0,
        })
        with self.assertRaises(ValidationError):
            self.validator.validate(unavailable)
        unavailable["provider_observation"]["estimated_micro_usd"] = None
        self.validator.validate(unavailable)

        pending = deepcopy(unavailable)
        pending["record_kind"] = "provider.pending"
        pending["provider_observation"].update({
            "observation_kind": "pending",
            "status": "in_progress",
            "cost_disposition": "not_applicable_provider_pending",
        })
        self.validator.validate(pending)

    def test_packaged_contract_schema_is_valid(self) -> None:
        packaged = json.loads(
            files("astrowoof_natal_authoring")
            .joinpath("resources/contracts/native-transition-contracts.schema.json")
            .read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(packaged)


if __name__ == "__main__":
    unittest.main()
