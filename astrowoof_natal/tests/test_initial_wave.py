from __future__ import annotations

import threading
import time
import unittest
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.initial_wave import (  # noqa: E402
    CACHE_POLICY,
    DefinitelyUnattemptedCreate,
    InitialWaveError,
    InitialWaveMemberSpec,
    ProviderCreateRefused,
    ProviderCreateResult,
    build_initial_wave,
    build_wave_authorization,
    execute_initial_wave_creates,
    preflight_wave_authorization,
    validate_initial_wave,
)
from astrowoof_natal_authoring.pass_protocol import canonical_sha256  # noqa: E402
from astrowoof_natal_authoring.spend import (  # noqa: E402
    AUTHORIZATION_SCHEMA,
    PRICE_BOOK_VERSION,
)


RUN_ID = "run_initial_wave_fixture"
PROFILE = "a" * 64
ASSIGNMENT = "b" * 64
BASIS = 11


def binding(number: int) -> dict:
    return {
        "run_id": RUN_ID,
        "profile_sha256": PROFILE,
        "prepared_state_revision": BASIS,
        "stage": "authoring_initial",
        "route": f"kevin_{number}:attempt-001",
        "request_sha256": f"{number:x}" * 64,
        "model": "gpt-5.6-terra",
        "service_level": "interactive",
        "maximum_output_tokens": 30000,
        "commitment_micro_usd": 700000 + number,
        "price_book_version": PRICE_BOOK_VERSION,
    }


def members() -> list[InitialWaveMemberSpec]:
    return [
        InitialWaveMemberSpec(
            action_id=f"paid_{number:024x}",
            binding=binding(number),
            pass_id=f"kevin_{number}",
            pass_number=number,
        )
        for number in range(1, 7)
    ]


def wave(route_family: str = "exact_natal") -> dict:
    return build_initial_wave(
        run_id=RUN_ID,
        route_family=route_family,
        route_contract=(
            "astrowoof.semantic_closure_run.v0.9"
            if route_family == "exact_natal"
            else "astrowoof.bounded_natal.authoring_run.v2"
        ),
        assignment_sha256=ASSIGNMENT,
        profile_sha256=PROFILE,
        preparation_basis_revision=BASIS,
        members=members(),
    )


def member_authorizations(value: dict) -> list[dict]:
    specs = members()
    return [
        {
            "schema_version": AUTHORIZATION_SCHEMA,
            "action_id": member["action_id"],
            "binding": dict(spec.binding),
            "authorization_reference": f"api:member:{index}",
        }
        for index, (member, spec) in enumerate(
            zip(value["ordered_members"], specs), 1
        )
    ]


def envelope(value: dict, authorizations: list[dict]) -> dict:
    return build_wave_authorization(
        value,
        authorizations,
        reservation_set_reference="api:reservation-set:wave-001",
        issuer="astrowoof-api",
        authorized_at="2026-08-18T20:00:00Z",
    )


def execute(
    value: dict,
    *,
    submit,
    persist_member_outcome,
) -> dict:
    documents = member_authorizations(value)
    return execute_initial_wave_creates(
        value,
        authorization=envelope(value, documents),
        member_authorizations=documents,
        submit=submit,
        persist_member_outcome=persist_member_outcome,
    )


class TestInitialWave(unittest.TestCase):
    def test_exact_and_bounded_wave_identity_is_deterministic_and_separate(self) -> None:
        exact = wave()
        self.assertEqual(exact, wave())
        bounded = wave("bounded_natal")
        self.assertNotEqual(exact["wave_sha256"], bounded["wave_sha256"])
        self.assertEqual(list(range(1, 7)), [
            item["pass_number"] for item in exact["ordered_members"]
        ])
        self.assertEqual(CACHE_POLICY, exact["timing"]["cache_policy"])
        self.assertEqual(4, exact["timing"]["maximum_parallel_retrievals"])

    def test_wave_validation_rejects_changed_digest_timing_and_order(self) -> None:
        for change in ("digest", "timing", "order"):
            changed = wave()
            if change == "digest":
                changed["wave_sha256"] = "0" * 64
            elif change == "timing":
                changed["timing"]["maximum_concurrent_creates"] = 5
            else:
                changed["ordered_members"].reverse()
            with self.subTest(change=change):
                with self.assertRaises(InitialWaveError):
                    validate_initial_wave(changed)

    def test_preflight_is_complete_exact_and_nonmutating(self) -> None:
        value = wave()
        authorizations = member_authorizations(value)
        authorization = envelope(value, authorizations)
        before = deepcopy((value, authorization, authorizations))
        preflight_wave_authorization(value, authorization, authorizations)
        self.assertEqual(before, (value, authorization, authorizations))

    def test_preflight_rejects_partial_reordered_stale_and_conflicting_authority(self) -> None:
        value = wave()
        documents = member_authorizations(value)
        authorization = envelope(value, documents)
        cases: list[tuple[dict, list[dict]]] = []

        cases.append((authorization, documents[:-1]))

        reordered = deepcopy(documents)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        cases.append((authorization, reordered))

        stale = deepcopy(authorization)
        stale["preparation_basis_revision"] += 1
        stale["authorization_sha256"] = canonical_sha256({
            key: item for key, item in stale.items()
            if key != "authorization_sha256"
        })
        cases.append((stale, documents))

        conflicting = deepcopy(documents)
        conflicting[0]["binding"]["request_sha256"] = "f" * 64
        cases.append((authorization, conflicting))

        for changed_envelope, changed_documents in cases:
            with self.subTest(
                authorization=changed_envelope, documents=changed_documents
            ):
                with self.assertRaises(InitialWaveError):
                    preflight_wave_authorization(
                        value, changed_envelope, changed_documents
                    )

    def test_concurrent_create_io_has_serialized_immediate_persistence(self) -> None:
        value = wave()
        barrier = threading.Barrier(6)
        lock = threading.Lock()
        active = 0
        peak = 0
        submit_threads: set[int] = set()
        persisted: list[tuple[str, str, int]] = []
        persisted_while_active: list[int] = []
        coordinator_thread = threading.get_ident()

        def submit(member: dict, timeout: int) -> ProviderCreateResult:
            nonlocal active, peak
            self.assertEqual(15, timeout)
            submit_threads.add(threading.get_ident())
            with lock:
                active += 1
                peak = max(peak, active)
            barrier.wait(timeout=2)
            time.sleep((7 - member["pass_number"]) * 0.002)
            with lock:
                active -= 1
            return ProviderCreateResult(f"resp_{member['pass_number']}")

        def persist(member: dict, outcome: dict) -> None:
            with lock:
                persisted_while_active.append(active)
            persisted.append((
                member["action_id"], outcome["provider"]["id"],
                threading.get_ident(),
            ))

        result = execute(
            value, submit=submit, persist_member_outcome=persist
        )
        self.assertEqual(6, peak)
        self.assertEqual(6, len(submit_threads))
        self.assertEqual(6, len(persisted))
        self.assertEqual({coordinator_thread}, {item[2] for item in persisted})
        self.assertTrue(any(count > 0 for count in persisted_while_active))
        self.assertEqual("detached_provider_pending", result["outcome"])
        self.assertEqual(
            [f"paid_{number:024x}" for number in range(1, 7)],
            result["provider_custody_action_ids"],
        )

    def test_completion_order_does_not_change_canonical_result_order(self) -> None:
        value = wave()
        persisted: list[str] = []

        def submit(member: dict, _timeout: int) -> ProviderCreateResult:
            time.sleep((7 - member["pass_number"]) * 0.001)
            return ProviderCreateResult(f"resp_{member['pass_number']}")

        result = execute(
            value,
            submit=submit,
            persist_member_outcome=lambda member, _outcome: persisted.append(
                member["action_id"]
            ),
        )
        self.assertNotEqual(
            [item["action_id"] for item in result["member_outcomes"]],
            persisted,
        )
        self.assertEqual(
            [item["action_id"] for item in value["ordered_members"]],
            [item["action_id"] for item in result["member_outcomes"]],
        )

    def test_partial_member_outcomes_are_classified_without_rollback(self) -> None:
        value = wave()
        persisted: list[str] = []

        def submit(member: dict, _timeout: int) -> ProviderCreateResult:
            number = member["pass_number"]
            if number == 2:
                raise DefinitelyUnattemptedCreate("socket was never opened")
            if number == 3:
                raise ProviderCreateRefused("provider rejected before acceptance")
            if number == 4:
                raise TimeoutError("provider acceptance is unknown")
            return ProviderCreateResult(f"resp_{number}")

        result = execute(
            value,
            submit=submit,
            persist_member_outcome=lambda member, _outcome: persisted.append(
                member["action_id"]
            ),
        )
        self.assertEqual(6, len(persisted))
        self.assertEqual("ambiguous_submission", result["outcome"])
        self.assertTrue(result["local_continuation_required"])
        self.assertEqual([f"paid_{4:024x}"], result["ambiguous_action_ids"])
        self.assertEqual(
            ["provider_bound", "authorized_unstarted", "create_refused",
             "ambiguous_submission", "provider_bound", "provider_bound"],
            [item["outcome"] for item in result["member_outcomes"]],
        )

    def test_prepare_and_preflight_never_call_provider_or_persistence(self) -> None:
        calls = {"provider": 0, "persist": 0}
        value = wave()
        documents = member_authorizations(value)
        authorization = envelope(value, documents)
        preflight_wave_authorization(value, authorization, documents)
        self.assertEqual({"provider": 0, "persist": 0}, calls)

    def test_execute_rejects_partial_authority_before_provider_or_persistence(self) -> None:
        calls = {"provider": 0, "persist": 0}
        value = wave()
        documents = member_authorizations(value)
        authorization = envelope(value, documents)

        def submit(_member: dict, _timeout: int) -> ProviderCreateResult:
            calls["provider"] += 1
            return ProviderCreateResult("should_not_exist")

        def persist(_member: dict, _outcome: dict) -> None:
            calls["persist"] += 1

        with self.assertRaises(InitialWaveError):
            execute_initial_wave_creates(
                value,
                authorization=authorization,
                member_authorizations=documents[:-1],
                submit=submit,
                persist_member_outcome=persist,
            )
        self.assertEqual({"provider": 0, "persist": 0}, calls)


if __name__ == "__main__":
    unittest.main()
