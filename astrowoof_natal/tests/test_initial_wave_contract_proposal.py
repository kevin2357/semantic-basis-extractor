from __future__ import annotations

import json
import hashlib
import unittest
from copy import deepcopy
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:  # Source-only lean environments may omit SPC's dependency.
    Draft202012Validator = None  # type: ignore[assignment,misc]
    ValidationError = Exception  # type: ignore[assignment,misc]


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "sprints" / "2026" / "08" / (
    "20260818-initial-pass-concurrent-fanout-sprint3"
) / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def validate_proposal_pair(wave: dict, authorization: dict) -> None:
    members = wave["ordered_members"]
    if [item["pass_number"] for item in members] != list(range(1, 7)):
        raise ValueError("wave pass order is not exactly 1..6")
    if len({item["action_id"] for item in members}) != 6:
        raise ValueError("wave repeats an action ID")
    if len({item["binding_sha256"] for item in members}) != 6:
        raise ValueError("wave repeats a binding digest")
    if wave["aggregate_maximum_commitment_micro_usd"] != sum(
        item["commitment_micro_usd"] for item in members
    ):
        raise ValueError("wave aggregate commitment is inconsistent")
    for field in (
        "wave_id", "wave_sha256", "run_id", "route_family", "profile_sha256",
        "preparation_basis_revision", "price_book_version", "member_count",
        "aggregate_maximum_commitment_micro_usd",
    ):
        if wave[field] != authorization[field]:
            raise ValueError(f"authorization conflicts with wave field {field}")
    expected = [
        (item["action_id"], item["binding_sha256"]) for item in members
    ]
    observed = [
        (item["action_id"], item["binding_sha256"])
        for item in authorization["ordered_members"]
    ]
    if observed != expected or len({item[0] for item in observed}) != 6:
        raise ValueError("authorization member inventory conflicts with wave")


@unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
class TestInitialWaveContractProposal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load("initial-wave-contract.proposal.schema.json")
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )

    def test_canonical_wave_and_authorization_validate(self) -> None:
        self.validator.validate(load("prepared-initial-wave.proposal.json"))
        self.validator.validate(load("initial-wave-authorization.proposal.json"))

    def test_wave_and_authorization_are_content_addressed(self) -> None:
        wave = load("prepared-initial-wave.proposal.json")
        body = {
            key: value for key, value in wave.items()
            if key not in {"wave_id", "wave_sha256"}
        }
        self.assertEqual(digest(body), wave["wave_sha256"])
        self.assertEqual("wave_" + wave["wave_sha256"][:24], wave["wave_id"])
        authorization = load("initial-wave-authorization.proposal.json")
        authorization_body = {
            key: value for key, value in authorization.items()
            if key != "authorization_sha256"
        }
        self.assertEqual(
            digest(authorization_body), authorization["authorization_sha256"]
        )

    def test_wave_has_exact_ordered_six_member_inventory(self) -> None:
        wave = load("prepared-initial-wave.proposal.json")
        members = wave["ordered_members"]
        self.assertEqual(list(range(1, 7)), [m["pass_number"] for m in members])
        self.assertEqual(6, len({m["action_id"] for m in members}))
        self.assertEqual(6, len({m["binding_sha256"] for m in members}))
        self.assertEqual(
            wave["aggregate_maximum_commitment_micro_usd"],
            sum(m["commitment_micro_usd"] for m in members),
        )
        self.assertEqual(
            {"authoring_initial"}, {m["stage"] for m in members}
        )
        self.assertEqual({"interactive"}, {m["service_level"] for m in members})

    def test_authorization_matches_wave_inventory_exactly(self) -> None:
        wave = load("prepared-initial-wave.proposal.json")
        authorization = load("initial-wave-authorization.proposal.json")
        validate_proposal_pair(wave, authorization)
        for field in (
            "wave_id", "wave_sha256", "run_id", "route_family",
            "profile_sha256", "preparation_basis_revision", "price_book_version",
            "member_count", "aggregate_maximum_commitment_micro_usd",
        ):
            self.assertEqual(wave[field], authorization[field])
        self.assertEqual(
            [(m["action_id"], m["binding_sha256"]) for m in wave["ordered_members"]],
            [(m["action_id"], m["binding_sha256"])
             for m in authorization["ordered_members"]],
        )

    def test_timing_and_cache_policy_are_fixed_not_caller_tuned(self) -> None:
        timing = load("prepared-initial-wave.proposal.json")["timing"]
        self.assertEqual({
            "maximum_concurrent_creates": 6,
            "provider_create_timeout_seconds": 15,
            "provider_io_wall_clock_limit_seconds": 20,
            "maximum_due_retrievals_per_cycle": 4,
            "maximum_parallel_retrievals": 4,
            "cache_policy": "no_serial_cache_warmer",
        }, timing)
        changed = load("prepared-initial-wave.proposal.json")
        changed["timing"]["maximum_parallel_retrievals"] = 6
        with self.assertRaises(ValidationError):
            self.validator.validate(changed)

    def test_partial_duplicate_unknown_and_batch_authority_fail(self) -> None:
        for mutate in (
            lambda value: value["ordered_members"].pop(),
            lambda value: value["ordered_members"].__setitem__(
                5, deepcopy(value["ordered_members"][4])
            ),
            lambda value: value.__setitem__("provider_payload", {}),
            lambda value: value["ordered_members"][0].__setitem__(
                "service_level", "batch"
            ),
        ):
            changed = load("prepared-initial-wave.proposal.json")
            mutate(changed)
            with self.subTest(changed=changed):
                with self.assertRaises(ValidationError):
                    self.validator.validate(changed)

    def test_partial_or_conflicting_authorization_fails(self) -> None:
        partial = load("initial-wave-authorization.proposal.json")
        partial["ordered_members"].pop()
        with self.assertRaises(ValidationError):
            self.validator.validate(partial)

        conflict = load("initial-wave-authorization.proposal.json")
        conflict["ordered_members"][0]["binding_sha256"] = "f" * 63
        with self.assertRaises(ValidationError):
            self.validator.validate(conflict)

        unknown = load("initial-wave-authorization.proposal.json")
        unknown["transaction_claim"] = True
        with self.assertRaises(ValidationError):
            self.validator.validate(unknown)

    def test_cross_document_preflight_rejects_semantic_conflicts(self) -> None:
        wave = load("prepared-initial-wave.proposal.json")
        authorization = load("initial-wave-authorization.proposal.json")
        cases = []

        wrong_order = deepcopy(authorization)
        wrong_order["ordered_members"][0], wrong_order["ordered_members"][1] = (
            wrong_order["ordered_members"][1], wrong_order["ordered_members"][0]
        )
        cases.append((wave, wrong_order))

        repeated_action = deepcopy(wave)
        repeated_action["ordered_members"][5]["action_id"] = (
            repeated_action["ordered_members"][4]["action_id"]
        )
        cases.append((repeated_action, authorization))

        wrong_aggregate = deepcopy(wave)
        wrong_aggregate["aggregate_maximum_commitment_micro_usd"] += 1
        cases.append((wrong_aggregate, authorization))

        stale_basis = deepcopy(authorization)
        stale_basis["preparation_basis_revision"] += 1
        cases.append((wave, stale_basis))

        for changed_wave, changed_authorization in cases:
            with self.subTest(
                wave=changed_wave, authorization=changed_authorization
            ):
                with self.assertRaises(ValueError):
                    validate_proposal_pair(changed_wave, changed_authorization)


if __name__ == "__main__":
    unittest.main()
