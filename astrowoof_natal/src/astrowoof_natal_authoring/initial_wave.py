"""Transport-neutral six-member initial-authoring wave coordination.

Route adapters own prompts, provider envelopes, semantic validation, and authority
hydration.  This module freezes the shared interactive orchestration shape without
performing provider I/O or native persistence during preparation/preflight.
"""

from __future__ import annotations

import concurrent.futures
import queue
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from .pass_protocol import canonical_sha256
from .spend import AUTHORIZATION_SCHEMA, PRICE_BOOK_VERSION


WAVE_CONTRACT = "astrowoof.initial_authoring_wave.v1"
WAVE_AUTHORIZATION_CONTRACT = (
    "astrowoof.initial_authoring_wave_authorization.v1"
)
WAVE_RESULT_CONTRACT = "astrowoof.initial_authoring_wave_result.v1"
INITIAL_MEMBER_COUNT = 6
MAXIMUM_CONCURRENT_CREATES = 6
PROVIDER_CREATE_TIMEOUT_SECONDS = 15
PROVIDER_IO_WALL_CLOCK_LIMIT_SECONDS = 20
MAXIMUM_DUE_RETRIEVALS_PER_CYCLE = 4
MAXIMUM_PARALLEL_RETRIEVALS = 4
CACHE_POLICY = "no_serial_cache_warmer"
SUPPORTED_ROUTE_FAMILIES = frozenset({"exact_natal", "bounded_natal"})
MEMBER_OUTCOMES = frozenset({
    "provider_bound",
    "authorized_unstarted",
    "ambiguous_submission",
    "create_refused",
})


class InitialWaveError(ValueError):
    """The initial wave or its authority failed closed."""

    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code


class DefinitelyUnattemptedCreate(RuntimeError):
    """Transport proves that no provider request was attempted."""


class ProviderCreateRefused(RuntimeError):
    """Provider definitively refused creation and returned no operation."""


@dataclass(frozen=True)
class InitialWaveMemberSpec:
    action_id: str
    binding: Mapping[str, Any]
    pass_id: str
    pass_number: int


@dataclass(frozen=True)
class ProviderCreateResult:
    provider_id: str
    provider_kind: str = "response"
    metadata: Mapping[str, Any] | None = None


def _require_sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise InitialWaveError("binding_mismatch", f"{label} is not SHA-256")
    return value


def _wave_body(wave: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in wave.items()
        if key not in {"wave_id", "wave_sha256"}
    }


def _authorization_body(authorization: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in authorization.items()
        if key != "authorization_sha256"
    }


def build_initial_wave(
    *,
    run_id: str,
    route_family: str,
    route_contract: str,
    assignment_sha256: str,
    profile_sha256: str,
    preparation_basis_revision: int,
    members: Sequence[InitialWaveMemberSpec],
) -> dict[str, Any]:
    """Build one content-addressed wave without provider or filesystem mutation."""
    if route_family not in SUPPORTED_ROUTE_FAMILIES:
        raise InitialWaveError("route_mismatch", "Unsupported wave route family")
    if not all(isinstance(value, str) and value for value in (
        run_id, route_contract,
    )):
        raise InitialWaveError("binding_mismatch", "Run/route bindings are required")
    _require_sha256(assignment_sha256, "assignment_sha256")
    _require_sha256(profile_sha256, "profile_sha256")
    if (
        not isinstance(preparation_basis_revision, int)
        or isinstance(preparation_basis_revision, bool)
        or preparation_basis_revision < 0
    ):
        raise InitialWaveError(
            "binding_mismatch", "Preparation basis revision is invalid"
        )
    if len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Initial wave must contain six members"
        )

    ordered: list[dict[str, Any]] = []
    action_ids: set[str] = set()
    binding_digests: set[str] = set()
    for expected_number, spec in enumerate(members, 1):
        binding = dict(spec.binding)
        if spec.pass_number != expected_number:
            raise InitialWaveError(
                "member_inventory_mismatch", "Wave pass order must be exactly 1..6"
            )
        if not isinstance(spec.pass_id, str) or not spec.pass_id:
            raise InitialWaveError("binding_mismatch", "Wave pass ID is invalid")
        if not isinstance(spec.action_id, str) or not spec.action_id.startswith("paid_"):
            raise InitialWaveError("binding_mismatch", "Wave action ID is invalid")
        if spec.action_id in action_ids:
            raise InitialWaveError(
                "member_inventory_mismatch", "Wave repeats an action ID"
            )
        expected = {
            "run_id": run_id,
            "profile_sha256": profile_sha256,
            "prepared_state_revision": preparation_basis_revision,
            "stage": "authoring_initial",
            "service_level": "interactive",
            "price_book_version": PRICE_BOOK_VERSION,
        }
        if any(binding.get(key) != value for key, value in expected.items()):
            raise InitialWaveError(
                "binding_mismatch", "Wave member binding conflicts with wave authority"
            )
        required_strings = ("route", "request_sha256", "model")
        if not all(isinstance(binding.get(key), str) and binding[key] for key in required_strings):
            raise InitialWaveError("binding_mismatch", "Wave member binding is incomplete")
        _require_sha256(binding["request_sha256"], "request_sha256")
        for key in ("maximum_output_tokens", "commitment_micro_usd"):
            value = binding.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise InitialWaveError(
                    "binding_mismatch", f"Wave member {key} is invalid"
                )
        binding_sha256 = canonical_sha256(binding)
        if binding_sha256 in binding_digests:
            raise InitialWaveError(
                "member_inventory_mismatch", "Wave repeats a binding digest"
            )
        action_ids.add(spec.action_id)
        binding_digests.add(binding_sha256)
        ordered.append({
            "action_id": spec.action_id,
            "binding_sha256": binding_sha256,
            "pass_id": spec.pass_id,
            "pass_number": spec.pass_number,
            "attempt": 1,
            "stage": "authoring_initial",
            "route": binding["route"],
            "request_sha256": binding["request_sha256"],
            "model": binding["model"],
            "service_level": "interactive",
            "maximum_output_tokens": binding["maximum_output_tokens"],
            "commitment_micro_usd": binding["commitment_micro_usd"],
            "price_book_version": PRICE_BOOK_VERSION,
        })

    body: dict[str, Any] = {
        "schema_version": WAVE_CONTRACT,
        "run_id": run_id,
        "route_family": route_family,
        "route_contract": route_contract,
        "assignment_sha256": assignment_sha256,
        "profile_sha256": profile_sha256,
        "preparation_basis_revision": preparation_basis_revision,
        "price_book_version": PRICE_BOOK_VERSION,
        "member_count": INITIAL_MEMBER_COUNT,
        "ordered_members": ordered,
        "aggregate_maximum_commitment_micro_usd": sum(
            item["commitment_micro_usd"] for item in ordered
        ),
        "timing": {
            "maximum_concurrent_creates": MAXIMUM_CONCURRENT_CREATES,
            "provider_create_timeout_seconds": PROVIDER_CREATE_TIMEOUT_SECONDS,
            "provider_io_wall_clock_limit_seconds": (
                PROVIDER_IO_WALL_CLOCK_LIMIT_SECONDS
            ),
            "maximum_due_retrievals_per_cycle": (
                MAXIMUM_DUE_RETRIEVALS_PER_CYCLE
            ),
            "maximum_parallel_retrievals": MAXIMUM_PARALLEL_RETRIEVALS,
            "cache_policy": CACHE_POLICY,
        },
    }
    wave_sha256 = canonical_sha256(body)
    return {
        **body,
        "wave_id": "wave_" + wave_sha256[:24],
        "wave_sha256": wave_sha256,
    }


def validate_initial_wave(wave: Mapping[str, Any]) -> None:
    if wave.get("schema_version") != WAVE_CONTRACT:
        raise InitialWaveError("unsupported_contract", "Unsupported wave contract")
    expected_sha256 = canonical_sha256(_wave_body(wave))
    if wave.get("wave_sha256") != expected_sha256:
        raise InitialWaveError("digest_mismatch", "Wave digest is invalid")
    if wave.get("wave_id") != "wave_" + expected_sha256[:24]:
        raise InitialWaveError("digest_mismatch", "Wave ID is invalid")
    members = wave.get("ordered_members")
    if not isinstance(members, list) or len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave member inventory is invalid"
        )
    if [item.get("pass_number") for item in members] != list(range(1, 7)):
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave member order is invalid"
        )
    if len({item.get("action_id") for item in members}) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave action inventory is not unique"
        )
    if len({item.get("binding_sha256") for item in members}) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave binding inventory is not unique"
        )
    if wave.get("aggregate_maximum_commitment_micro_usd") != sum(
        int(item.get("commitment_micro_usd") or 0) for item in members
    ):
        raise InitialWaveError(
            "aggregate_mismatch", "Wave aggregate commitment is invalid"
        )
    expected_timing = {
        "maximum_concurrent_creates": MAXIMUM_CONCURRENT_CREATES,
        "provider_create_timeout_seconds": PROVIDER_CREATE_TIMEOUT_SECONDS,
        "provider_io_wall_clock_limit_seconds": PROVIDER_IO_WALL_CLOCK_LIMIT_SECONDS,
        "maximum_due_retrievals_per_cycle": MAXIMUM_DUE_RETRIEVALS_PER_CYCLE,
        "maximum_parallel_retrievals": MAXIMUM_PARALLEL_RETRIEVALS,
        "cache_policy": CACHE_POLICY,
    }
    if wave.get("timing") != expected_timing:
        raise InitialWaveError("binding_mismatch", "Wave timing policy changed")


def build_wave_authorization(
    wave: Mapping[str, Any],
    member_authorizations: Sequence[Mapping[str, Any]],
    *,
    reservation_set_reference: str,
    issuer: str,
    authorized_at: str,
) -> dict[str, Any]:
    """Compose an API-facing envelope; production authority remains API-owned."""
    validate_initial_wave(wave)
    if len(member_authorizations) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "partial_authorization", "Wave requires six member authorizations"
        )
    inventory = []
    for member, authorization in zip(wave["ordered_members"], member_authorizations):
        inventory.append({
            "action_id": authorization.get("action_id"),
            "binding_sha256": canonical_sha256(authorization.get("binding")),
            "member_authorization_sha256": canonical_sha256(authorization),
        })
        if (
            authorization.get("schema_version") != AUTHORIZATION_SCHEMA
            or authorization.get("action_id") != member["action_id"]
            or authorization.get("binding") is None
            or not isinstance(authorization.get("authorization_reference"), str)
            or not authorization["authorization_reference"]
            or inventory[-1]["binding_sha256"] != member["binding_sha256"]
        ):
            raise InitialWaveError(
                "binding_mismatch", "Member authorization conflicts with wave"
            )
    if not all(isinstance(value, str) and value for value in (
        reservation_set_reference, issuer, authorized_at,
    )):
        raise InitialWaveError(
            "authorization_mismatch", "Wave authorization metadata is incomplete"
        )
    body = {
        "schema_version": WAVE_AUTHORIZATION_CONTRACT,
        "wave_id": wave["wave_id"],
        "wave_sha256": wave["wave_sha256"],
        "run_id": wave["run_id"],
        "route_family": wave["route_family"],
        "profile_sha256": wave["profile_sha256"],
        "preparation_basis_revision": wave["preparation_basis_revision"],
        "price_book_version": wave["price_book_version"],
        "member_count": INITIAL_MEMBER_COUNT,
        "ordered_members": inventory,
        "aggregate_maximum_commitment_micro_usd": (
            wave["aggregate_maximum_commitment_micro_usd"]
        ),
        "reservation_set_reference": reservation_set_reference,
        "issuer": issuer,
        "authorized_at": authorized_at,
    }
    return {**body, "authorization_sha256": canonical_sha256(body)}


def preflight_wave_authorization(
    wave: Mapping[str, Any],
    authorization: Mapping[str, Any],
    member_authorizations: Sequence[Mapping[str, Any]],
) -> None:
    """Validate the complete wave authority without consuming or mutating it."""
    validate_initial_wave(wave)
    if authorization.get("schema_version") != WAVE_AUTHORIZATION_CONTRACT:
        raise InitialWaveError(
            "unsupported_contract", "Unsupported wave authorization contract"
        )
    if authorization.get("authorization_sha256") != canonical_sha256(
        _authorization_body(authorization)
    ):
        raise InitialWaveError(
            "digest_mismatch", "Wave authorization digest is invalid"
        )
    copied_fields = (
        "wave_id", "wave_sha256", "run_id", "route_family", "profile_sha256",
        "preparation_basis_revision", "price_book_version", "member_count",
        "aggregate_maximum_commitment_micro_usd",
    )
    if any(authorization.get(field) != wave.get(field) for field in copied_fields):
        raise InitialWaveError(
            "authorization_mismatch", "Wave authorization conflicts with prepared wave"
        )
    if not isinstance(authorization.get("reservation_set_reference"), str) or not (
        authorization["reservation_set_reference"]
    ):
        raise InitialWaveError(
            "authorization_mismatch", "Reservation-set reference is missing"
        )
    if len(member_authorizations) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "partial_authorization", "Wave requires all six member authorizations"
        )
    expected_inventory = []
    seen: set[str] = set()
    for member, member_authorization in zip(
        wave["ordered_members"], member_authorizations
    ):
        action_id = member_authorization.get("action_id")
        if action_id in seen:
            raise InitialWaveError(
                "member_inventory_mismatch", "Authorization repeats an action"
            )
        seen.add(str(action_id))
        binding_sha256 = canonical_sha256(member_authorization.get("binding"))
        if (
            member_authorization.get("schema_version") != AUTHORIZATION_SCHEMA
            or action_id != member["action_id"]
            or member_authorization.get("binding") is None
            or not isinstance(
                member_authorization.get("authorization_reference"), str
            )
            or not member_authorization["authorization_reference"]
            or binding_sha256 != member["binding_sha256"]
        ):
            raise InitialWaveError(
                "binding_mismatch", "Member authorization conflicts with wave"
            )
        expected_inventory.append({
            "action_id": action_id,
            "binding_sha256": binding_sha256,
            "member_authorization_sha256": canonical_sha256(member_authorization),
        })
    if authorization.get("ordered_members") != expected_inventory:
        raise InitialWaveError(
            "authorization_mismatch", "Envelope member inventory is not exact"
        )


def execute_initial_wave_creates(
    wave: Mapping[str, Any],
    *,
    authorization: Mapping[str, Any],
    member_authorizations: Sequence[Mapping[str, Any]],
    submit: Callable[[Mapping[str, Any], int], ProviderCreateResult],
    persist_member_outcome: Callable[[Mapping[str, Any], Mapping[str, Any]], None],
    monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Overlap create I/O and serialize outcome persistence in the caller thread.

    Authorization consumption belongs immediately before ``submit`` in the route
    integration layer. This coordinator never claims provider atomicity.
    """
    preflight_wave_authorization(wave, authorization, member_authorizations)
    started = monotonic()

    def create(member: Mapping[str, Any]) -> dict[str, Any]:
        try:
            result = submit(member, PROVIDER_CREATE_TIMEOUT_SECONDS)
            if (
                not isinstance(result, ProviderCreateResult)
                or not result.provider_id
                or result.provider_kind != "response"
            ):
                raise RuntimeError("Provider create returned no valid Response identity")
            return {
                "action_id": member["action_id"],
                "pass_id": member["pass_id"],
                "outcome": "provider_bound",
                "provider": {"kind": "response", "id": result.provider_id},
                "provider_create_metadata": dict(result.metadata or {}),
                "reason": None,
            }
        except DefinitelyUnattemptedCreate as exc:
            return {
                "action_id": member["action_id"], "pass_id": member["pass_id"],
                "outcome": "authorized_unstarted", "provider": None,
                "provider_create_metadata": None,
                "reason": str(exc),
            }
        except ProviderCreateRefused as exc:
            return {
                "action_id": member["action_id"], "pass_id": member["pass_id"],
                "outcome": "create_refused", "provider": None,
                "provider_create_metadata": None,
                "reason": str(exc),
            }
        except Exception as exc:
            return {
                "action_id": member["action_id"], "pass_id": member["pass_id"],
                "outcome": "ambiguous_submission", "provider": None,
                "provider_create_metadata": None,
                "reason": str(exc),
            }

    outcomes: dict[str, dict[str, Any]] = {}
    completions: queue.Queue[tuple[Mapping[str, Any], dict[str, Any]]] = queue.Queue()

    def create_and_enqueue(member: Mapping[str, Any]) -> None:
        completions.put((member, create(member)))

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=MAXIMUM_CONCURRENT_CREATES,
        thread_name_prefix="astrowoof-initial-create",
    )
    futures = [
        executor.submit(create_and_enqueue, member)
        for member in wave["ordered_members"]
    ]
    try:
        while len(outcomes) < INITIAL_MEMBER_COUNT:
            try:
                member, outcome = completions.get_nowait()
            except queue.Empty:
                remaining = (
                    PROVIDER_IO_WALL_CLOCK_LIMIT_SECONDS - (monotonic() - started)
                )
                if remaining <= 0:
                    raise InitialWaveError(
                        "submission_cycle_timeout_with_live_tasks",
                        "Initial create tasks exceeded the provider-I/O wave bound",
                    )
                try:
                    member, outcome = completions.get(timeout=remaining)
                except queue.Empty as exc:
                    raise InitialWaveError(
                        "submission_cycle_timeout_with_live_tasks",
                        "Initial create tasks exceeded the provider-I/O wave bound",
                    ) from exc
            if outcome["outcome"] not in MEMBER_OUTCOMES:
                raise InitialWaveError(
                    "unsupported_outcome", "Create task returned an unknown outcome"
                )
            # This callback is deliberately invoked only by the coordinator thread.
            # Runtime integrations use it for the immediate serialized ledger and
            # journal durability step.
            persist_member_outcome(member, outcome)
            outcomes[member["action_id"]] = outcome
        provider_io_finished = monotonic()
    except InitialWaveError:
        for future in futures:
            future.cancel()
        # Correctness requires all live create tasks to unwind before aggregate
        # publication. The provider transport is required to honor its shorter
        # 15-second timeout; violation retains the worker and fails closed.
        executor.shutdown(wait=True, cancel_futures=True)
        raise
    finally:
        executor.shutdown(wait=True)

    ordered = [outcomes[member["action_id"]] for member in wave["ordered_members"]]
    ambiguous = any(item["outcome"] == "ambiguous_submission" for item in ordered)
    provider_bound = any(item["outcome"] == "provider_bound" for item in ordered)
    aggregate_outcome = (
        "ambiguous_submission"
        if ambiguous
        else "detached_provider_pending"
        if provider_bound
        else "awaiting_external_authority"
    )
    return {
        "schema_version": WAVE_RESULT_CONTRACT,
        "wave_id": wave["wave_id"],
        "wave_sha256": wave["wave_sha256"],
        "outcome": aggregate_outcome,
        "member_outcomes": ordered,
        "local_continuation_required": any(
            item["outcome"] in {"authorized_unstarted", "create_refused"}
            for item in ordered
        ),
        "provider_custody_action_ids": [
            item["action_id"] for item in ordered
            if item["outcome"] == "provider_bound"
        ],
        "ambiguous_action_ids": [
            item["action_id"] for item in ordered
            if item["outcome"] == "ambiguous_submission"
        ],
        "provider_io_elapsed_seconds": max(0.0, provider_io_finished - started),
    }
