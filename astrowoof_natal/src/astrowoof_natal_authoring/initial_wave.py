"""Transport-neutral six-member initial-authoring wave coordination.

Route adapters own prompts, provider envelopes, semantic validation, and authority
hydration.  This module freezes the shared interactive orchestration shape without
performing provider I/O or native persistence during preparation/preflight.
"""

from __future__ import annotations

import concurrent.futures
import logging
import queue
import time
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from .pass_protocol import canonical_sha256
from .spend import AUTHORIZATION_SCHEMA, PRICE_BOOK_VERSION
from .application_logging import current_logging_context, logging_context
from .response_diagnostics import sanitize_error_message


logger = logging.getLogger(__name__)


WAVE_CONTRACT = "astrowoof.initial_authoring_wave.v1"
WAVE_AUTHORIZATION_CONTRACT = (
    "astrowoof.initial_authoring_wave_authorization.v1"
)
WAVE_RESULT_CONTRACT = "astrowoof.initial_authoring_wave_result.v1"
BINDING_BUNDLE_CONTRACT = (
    "astrowoof.initial_authoring_wave_binding_bundle.v1"
)
INITIAL_WAVE_BINDING_BUNDLE_FILENAME = (
    "initial-authoring-wave-binding-bundle.json"
)
INITIAL_MEMBER_COUNT = 6
MAXIMUM_CONCURRENT_CREATES = 6
PROVIDER_CREATE_TIMEOUT_SECONDS = 15
PROVIDER_IO_WALL_CLOCK_LIMIT_SECONDS = 20
MAXIMUM_DUE_RETRIEVALS_PER_CYCLE = 4
MAXIMUM_PARALLEL_RETRIEVALS = 4
CACHE_POLICY = "no_serial_cache_warmer"
SUPPORTED_ROUTE_FAMILIES = frozenset({"exact_natal", "bounded_natal"})
ACTIVE_INITIAL_WAVE_STATES = frozenset({
    "AWAITING_SPEND_AUTHORIZATION", "AUTHORIZED", "SUBMITTING",
})
HISTORICAL_INITIAL_WAVE_STATES = frozenset({"DETACHED", "FAILED"})
MEMBER_OUTCOMES = frozenset({
    "provider_bound",
    "authorized_unstarted",
    "ambiguous_submission",
    "create_refused",
})
_WAVE_KEYS = frozenset({
    "schema_version", "wave_id", "wave_sha256", "run_id", "route_family",
    "route_contract", "assignment_sha256", "profile_sha256",
    "preparation_basis_revision", "price_book_version", "member_count",
    "ordered_members", "aggregate_maximum_commitment_micro_usd", "timing",
})
_WAVE_MEMBER_KEYS = frozenset({
    "action_id", "binding_sha256", "pass_id", "pass_number", "attempt",
    "stage", "route", "request_sha256", "model", "service_level",
    "maximum_output_tokens", "commitment_micro_usd", "price_book_version",
})
_AUTHORIZATION_KEYS = frozenset({
    "schema_version", "authorization_sha256", "wave_id", "wave_sha256",
    "run_id", "route_family", "profile_sha256", "preparation_basis_revision",
    "price_book_version", "member_count", "ordered_members",
    "aggregate_maximum_commitment_micro_usd", "reservation_set_reference",
    "issuer", "authorized_at",
})
_AUTHORIZATION_MEMBER_KEYS = frozenset({
    "action_id", "binding_sha256", "member_authorization_sha256",
})
_RESULT_KEYS = frozenset({
    "schema_version", "wave_id", "wave_sha256", "outcome", "member_outcomes",
    "local_continuation_required", "provider_custody_action_ids",
    "ambiguous_action_ids", "provider_io_elapsed_seconds",
})
_RESULT_MEMBER_KEYS = frozenset({
    "action_id", "pass_id", "outcome", "provider",
    "provider_create_metadata", "reason",
})
_BUNDLE_KEYS = frozenset({
    "schema_version", "bundle_sha256", "wave_id", "wave_sha256", "run_id",
    "route_family", "profile_sha256", "preparation_basis_revision",
    "price_book_version", "member_count", "ordered_members",
    "aggregate_maximum_commitment_micro_usd",
})
_BUNDLE_MEMBER_KEYS = frozenset({
    "action_id", "pass_id", "pass_number", "binding", "binding_sha256",
})
_BINDING_KEYS = frozenset({
    "run_id", "profile_sha256", "prepared_state_revision", "stage", "route",
    "request_sha256", "model", "service_level", "maximum_output_tokens",
    "commitment_micro_usd", "price_book_version",
})


class InitialWaveError(ValueError):
    """The initial wave or its authority failed closed."""

    def __init__(
        self, reason_code: str, message: str,
        *, evidence_categories: Sequence[str] = (),
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.evidence_categories = tuple(evidence_categories)


class DefinitelyUnattemptedCreate(RuntimeError):
    """Transport proves that no provider request was attempted."""


class ProviderCreateRefused(RuntimeError):
    """Provider definitively refused creation and returned no operation."""


def classify_initial_wave_state(wave: object) -> str:
    """Classify current admission separately from immutable wave lineage."""
    if wave is None:
        return "absent"
    if not isinstance(wave, Mapping):
        raise InitialWaveError(
            "unsupported_contract", "Stored initial-wave evidence is not an object",
        )
    state = wave.get("state")
    if state in ACTIVE_INITIAL_WAVE_STATES:
        return "active"
    if state in HISTORICAL_INITIAL_WAVE_STATES:
        return "historical"
    raise InitialWaveError(
        "unsupported_contract", f"Unsupported stored initial-wave state: {state!r}",
    )


def is_active_initial_wave(wave: object) -> bool:
    """Return true only for the closed positive initial-admission state set."""
    return classify_initial_wave_state(wave) == "active"


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


def _bundle_body(bundle: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in bundle.items() if key != "bundle_sha256"}


def build_initial_wave_binding_bundle(
    wave: Mapping[str, Any], ordered_bindings: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the provider-safe complete binding inventory for one prepared wave."""
    validate_initial_wave(wave)
    if len(ordered_bindings) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Binding bundle requires six bindings"
        )
    members = []
    for wave_member, source_binding in zip(
        wave["ordered_members"], ordered_bindings
    ):
        binding = dict(source_binding)
        binding_sha256 = canonical_sha256(binding)
        members.append({
            "action_id": wave_member["action_id"],
            "pass_id": wave_member["pass_id"],
            "pass_number": wave_member["pass_number"],
            "binding": binding,
            "binding_sha256": binding_sha256,
        })
    bundle = {
        "schema_version": BINDING_BUNDLE_CONTRACT,
        "wave_id": wave["wave_id"],
        "wave_sha256": wave["wave_sha256"],
        "run_id": wave["run_id"],
        "route_family": wave["route_family"],
        "profile_sha256": wave["profile_sha256"],
        "preparation_basis_revision": wave["preparation_basis_revision"],
        "price_book_version": wave["price_book_version"],
        "member_count": INITIAL_MEMBER_COUNT,
        "ordered_members": members,
        "aggregate_maximum_commitment_micro_usd": wave[
            "aggregate_maximum_commitment_micro_usd"
        ],
    }
    bundle["bundle_sha256"] = canonical_sha256(bundle)
    validate_initial_wave_binding_bundle_against_wave(bundle, wave)
    return bundle


def validate_initial_wave_binding_bundle(bundle: Mapping[str, Any]) -> None:
    """Validate one binding bundle without filesystem or provider mutation."""
    if set(bundle) != _BUNDLE_KEYS or bundle.get("schema_version") != BINDING_BUNDLE_CONTRACT:
        raise InitialWaveError("unsupported_contract", "Unsupported binding bundle")
    if bundle.get("bundle_sha256") != canonical_sha256(_bundle_body(bundle)):
        raise InitialWaveError("digest_mismatch", "Binding bundle digest is invalid")
    for key in ("wave_sha256", "profile_sha256"):
        _require_sha256(bundle.get(key), key)
    if not all(isinstance(bundle.get(key), str) and bundle[key]
               for key in ("wave_id", "run_id", "price_book_version")):
        raise InitialWaveError("binding_mismatch", "Bundle identity is incomplete")
    if bundle.get("route_family") not in SUPPORTED_ROUTE_FAMILIES:
        raise InitialWaveError("route_mismatch", "Unsupported bundle route")
    revision = bundle.get("preparation_basis_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise InitialWaveError("binding_mismatch", "Bundle revision is invalid")
    members = bundle.get("ordered_members")
    if bundle.get("member_count") != INITIAL_MEMBER_COUNT \
            or not isinstance(members, list) or len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError("member_inventory_mismatch", "Bundle requires six members")
    if [item.get("pass_number") for item in members] != list(range(1, 7)):
        raise InitialWaveError("member_inventory_mismatch", "Bundle order is invalid")
    if any(not isinstance(item, Mapping) or set(item) != _BUNDLE_MEMBER_KEYS
           for item in members):
        raise InitialWaveError("unsupported_contract", "Bundle member fields are not exact")
    for item in members:
        binding = item.get("binding")
        if not isinstance(binding, Mapping) or set(binding) != _BINDING_KEYS:
            raise InitialWaveError("unsupported_contract", "Binding fields are not exact")
        binding_sha256 = canonical_sha256(binding)
        if item.get("binding_sha256") != binding_sha256:
            raise InitialWaveError("digest_mismatch", "Member binding digest is invalid")
        if item.get("action_id") != "paid_" + binding_sha256[:24]:
            raise InitialWaveError("binding_mismatch", "Action ID does not bind the member")
        if not isinstance(item.get("pass_id"), str) or not item["pass_id"]:
            raise InitialWaveError("binding_mismatch", "Bundle pass ID is invalid")
        expected = {
            "run_id": bundle["run_id"],
            "profile_sha256": bundle["profile_sha256"],
            "prepared_state_revision": revision,
            "stage": "authoring_initial",
            "service_level": "interactive",
            "price_book_version": bundle["price_book_version"],
        }
        if any(binding.get(key) != value for key, value in expected.items()):
            raise InitialWaveError("binding_mismatch", "Binding conflicts with bundle")
        _require_sha256(binding.get("request_sha256"), "request_sha256")
        if not all(isinstance(binding.get(key), str) and binding[key]
                   for key in ("route", "model")):
            raise InitialWaveError("binding_mismatch", "Binding route/model is invalid")
        if any(not isinstance(binding.get(key), int)
               or isinstance(binding[key], bool) or binding[key] <= 0
               for key in ("maximum_output_tokens", "commitment_micro_usd")):
            raise InitialWaveError("binding_mismatch", "Binding limits are invalid")
    if len({item["action_id"] for item in members}) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError("member_inventory_mismatch", "Bundle actions repeat")
    if bundle.get("aggregate_maximum_commitment_micro_usd") != sum(
        item["binding"]["commitment_micro_usd"] for item in members
    ):
        raise InitialWaveError("aggregate_mismatch", "Bundle commitment is invalid")


def validate_initial_wave_binding_bundle_against_wave(
    bundle: Mapping[str, Any], wave: Mapping[str, Any],
) -> None:
    """Validate both public documents and their exact ordered relationship."""
    validate_initial_wave(wave)
    validate_initial_wave_binding_bundle(bundle)
    shared = (
        "wave_id", "wave_sha256", "run_id", "route_family", "profile_sha256",
        "preparation_basis_revision", "price_book_version", "member_count",
        "aggregate_maximum_commitment_micro_usd",
    )
    if any(bundle.get(key) != wave.get(key) for key in shared):
        raise InitialWaveError("wave_mismatch", "Bundle does not bind the prepared wave")
    for bundle_member, wave_member in zip(
        bundle["ordered_members"], wave["ordered_members"]
    ):
        binding = bundle_member["binding"]
        compared = {
            "action_id": bundle_member["action_id"],
            "pass_id": bundle_member["pass_id"],
            "pass_number": bundle_member["pass_number"],
            "binding_sha256": bundle_member["binding_sha256"],
            "route": binding["route"],
            "request_sha256": binding["request_sha256"],
            "model": binding["model"],
            "service_level": binding["service_level"],
            "maximum_output_tokens": binding["maximum_output_tokens"],
            "commitment_micro_usd": binding["commitment_micro_usd"],
            "price_book_version": binding["price_book_version"],
        }
        projected = {key: wave_member[key] for key in compared}
        if compared != projected:
            raise InitialWaveError("binding_mismatch", "Bundle member conflicts with wave")


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
    if set(wave) != _WAVE_KEYS:
        raise InitialWaveError("unsupported_contract", "Wave fields are not exact")
    if wave.get("schema_version") != WAVE_CONTRACT:
        raise InitialWaveError("unsupported_contract", "Unsupported wave contract")
    expected_sha256 = canonical_sha256(_wave_body(wave))
    if wave.get("wave_sha256") != expected_sha256:
        raise InitialWaveError("digest_mismatch", "Wave digest is invalid")
    if wave.get("wave_id") != "wave_" + expected_sha256[:24]:
        raise InitialWaveError("digest_mismatch", "Wave ID is invalid")
    if not isinstance(wave.get("run_id"), str) or not wave["run_id"] \
            or not isinstance(wave.get("route_contract"), str) \
            or not wave["route_contract"]:
        raise InitialWaveError("binding_mismatch", "Wave run/route identity is invalid")
    _require_sha256(wave.get("assignment_sha256"), "assignment_sha256")
    _require_sha256(wave.get("profile_sha256"), "profile_sha256")
    revision = wave.get("preparation_basis_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise InitialWaveError("binding_mismatch", "Wave basis revision is invalid")
    if wave.get("price_book_version") != PRICE_BOOK_VERSION:
        raise InitialWaveError("binding_mismatch", "Wave price book is unsupported")
    members = wave.get("ordered_members")
    if not isinstance(members, list) or len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave member inventory is invalid"
        )
    if [item.get("pass_number") for item in members] != list(range(1, 7)):
        raise InitialWaveError(
            "member_inventory_mismatch", "Wave member order is invalid"
        )
    if any(not isinstance(item, Mapping) or set(item) != _WAVE_MEMBER_KEYS
           for item in members):
        raise InitialWaveError(
            "unsupported_contract", "Wave member fields are not exact"
        )
    for number, item in enumerate(members, 1):
        if not isinstance(item["action_id"], str) \
                or not item["action_id"].startswith("paid_") \
                or len(item["action_id"]) != 29:
            raise InitialWaveError("binding_mismatch", "Wave action ID is invalid")
        _require_sha256(item["binding_sha256"], "binding_sha256")
        _require_sha256(item["request_sha256"], "request_sha256")
        if item["pass_number"] != number or item["attempt"] != 1 \
                or item["stage"] != "authoring_initial" \
                or item["service_level"] != "interactive" \
                or item["price_book_version"] != wave["price_book_version"]:
            raise InitialWaveError("binding_mismatch", "Wave member policy is invalid")
        if not all(isinstance(item[key], str) and item[key]
                   for key in ("pass_id", "route", "model")):
            raise InitialWaveError("binding_mismatch", "Wave member identity is invalid")
        if any(not isinstance(item[key], int) or isinstance(item[key], bool)
               or item[key] <= 0
               for key in ("maximum_output_tokens", "commitment_micro_usd")):
            raise InitialWaveError("binding_mismatch", "Wave member limit is invalid")
    if wave.get("route_family") not in SUPPORTED_ROUTE_FAMILIES:
        raise InitialWaveError("route_mismatch", "Unsupported wave route family")
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


def initial_wave_public_document(stored: Mapping[str, Any]) -> dict[str, Any]:
    """Project and validate the exact public wave from SBE-owned native state."""
    if not isinstance(stored, Mapping) or not _WAVE_KEYS <= set(stored):
        raise InitialWaveError("wave_missing", "No complete prepared wave exists")
    value = {key: deepcopy(stored[key]) for key in _WAVE_KEYS}
    validate_initial_wave(value)
    return value


def validate_wave_authorization_document(
    authorization: Mapping[str, Any],
) -> None:
    """Validate one closed wave-level API authority document without mutation."""
    if set(authorization) != _AUTHORIZATION_KEYS:
        raise InitialWaveError(
            "unsupported_contract", "Wave authorization fields are not exact"
        )
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
    if authorization.get("route_family") not in SUPPORTED_ROUTE_FAMILIES:
        raise InitialWaveError("route_mismatch", "Unsupported authorization route")
    for key in ("wave_sha256", "profile_sha256"):
        _require_sha256(authorization.get(key), key)
    if authorization.get("price_book_version") != PRICE_BOOK_VERSION:
        raise InitialWaveError("binding_mismatch", "Authorization price book is unsupported")
    if not all(isinstance(authorization.get(key), str) and authorization[key]
               for key in ("wave_id", "run_id", "reservation_set_reference", "issuer", "authorized_at")):
        raise InitialWaveError("binding_mismatch", "Authorization identity is incomplete")
    if authorization.get("member_count") != INITIAL_MEMBER_COUNT:
        raise InitialWaveError("member_inventory_mismatch", "Authorization member count is invalid")
    revision = authorization.get("preparation_basis_revision")
    commitment = authorization.get("aggregate_maximum_commitment_micro_usd")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0 \
            or not isinstance(commitment, int) or isinstance(commitment, bool) \
            or commitment <= 0:
        raise InitialWaveError("binding_mismatch", "Authorization limits are invalid")
    members = authorization.get("ordered_members")
    if not isinstance(members, list) or len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Authorization must contain six members"
        )
    if any(not isinstance(item, Mapping) or set(item) != _AUTHORIZATION_MEMBER_KEYS
           for item in members):
        raise InitialWaveError(
            "unsupported_contract", "Authorization member fields are not exact"
        )
    if len({item.get("action_id") for item in members}) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError(
            "member_inventory_mismatch", "Authorization actions are not unique"
        )
    for item in members:
        if not isinstance(item.get("action_id"), str) \
                or not item["action_id"].startswith("paid_") \
                or len(item["action_id"]) != 29:
            raise InitialWaveError("binding_mismatch", "Authorization action ID is invalid")
        _require_sha256(item.get("binding_sha256"), "binding_sha256")
        _require_sha256(
            item.get("member_authorization_sha256"),
            "member_authorization_sha256",
        )


def validate_initial_wave_result(result: Mapping[str, Any]) -> None:
    """Validate the closed aggregate result without treating it as native state."""
    if set(result) != _RESULT_KEYS or result.get("schema_version") != WAVE_RESULT_CONTRACT:
        raise InitialWaveError("unsupported_contract", "Unsupported wave result")
    members = result.get("member_outcomes")
    if not isinstance(members, list) or len(members) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError("member_inventory_mismatch", "Result requires six members")
    if any(not isinstance(item, Mapping) or set(item) != _RESULT_MEMBER_KEYS
           for item in members):
        raise InitialWaveError("unsupported_contract", "Result member fields are not exact")
    action_ids = [item.get("action_id") for item in members]
    if len(set(action_ids)) != INITIAL_MEMBER_COUNT:
        raise InitialWaveError("member_inventory_mismatch", "Result actions are not unique")
    for item in members:
        if not isinstance(item.get("action_id"), str) \
                or not item["action_id"].startswith("paid_") \
                or len(item["action_id"]) != 29 \
                or not isinstance(item.get("pass_id"), str) or not item["pass_id"]:
            raise InitialWaveError("binding_mismatch", "Result member identity is invalid")
        if item.get("outcome") not in MEMBER_OUTCOMES:
            raise InitialWaveError("unsupported_outcome", "Unknown result member outcome")
        if item.get("provider_create_metadata") is not None \
                and not isinstance(item["provider_create_metadata"], Mapping):
            raise InitialWaveError("binding_mismatch", "Result metadata is invalid")
        if item.get("reason") is not None and not isinstance(item["reason"], str):
            raise InitialWaveError("binding_mismatch", "Result reason is invalid")
        provider = item.get("provider")
        if item["outcome"] == "provider_bound":
            if not isinstance(provider, Mapping) or set(provider) != {"kind", "id"} \
                    or provider.get("kind") != "response" or not provider.get("id"):
                raise InitialWaveError("binding_mismatch", "Provider-bound result lacks ID")
        elif provider is not None:
            raise InitialWaveError("binding_mismatch", "Non-bound result contains provider")
    custody = [item["action_id"] for item in members
               if item["outcome"] == "provider_bound"]
    ambiguous = [item["action_id"] for item in members
                 if item["outcome"] == "ambiguous_submission"]
    if result.get("provider_custody_action_ids") != custody \
            or result.get("ambiguous_action_ids") != ambiguous:
        raise InitialWaveError("aggregate_mismatch", "Result aggregate lists conflict")
    expected = (
        "ambiguous_submission" if ambiguous else
        "detached_provider_pending" if custody else
        "awaiting_external_authority"
    )
    if result.get("outcome") != expected:
        raise InitialWaveError("aggregate_mismatch", "Result outcome conflicts with members")
    if not isinstance(result.get("local_continuation_required"), bool):
        raise InitialWaveError("binding_mismatch", "Result continuation flag is invalid")
    expected_local = any(item["outcome"] in {"authorized_unstarted", "create_refused"}
                         for item in members)
    if result["local_continuation_required"] != expected_local:
        raise InitialWaveError("aggregate_mismatch", "Result continuation conflicts with members")
    elapsed = result.get("provider_io_elapsed_seconds")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        raise InitialWaveError("binding_mismatch", "Result elapsed time is invalid")


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
    validate_wave_authorization_document(authorization)
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
    logger.info(
        "initial_wave_start wave_id=%s route_family=%s member_count=%s "
        "maximum_concurrent=%s",
        wave["wave_id"], wave["route_family"], wave["member_count"],
        MAXIMUM_CONCURRENT_CREATES,
    )
    parent_log_context = current_logging_context()

    def create(member: Mapping[str, Any]) -> dict[str, Any]:
        with logging_context(
            host_id=parent_log_context["host_id"],
            run_id=str(wave["run_id"]),
            invocation_id=parent_log_context["invocation_id"],
            current_state="PROVIDER_CREATE",
        ):
            logger.info(
                "initial_member_create_start wave_id=%s action_id=%s pass_id=%s "
                "attempt=%s timeout_s=%s",
                wave["wave_id"], member["action_id"], member["pass_id"],
                member["attempt"], PROVIDER_CREATE_TIMEOUT_SECONDS,
            )
            try:
                result = submit(member, PROVIDER_CREATE_TIMEOUT_SECONDS)
            except DefinitelyUnattemptedCreate as exc:
                logger.warning(
                    "initial_member_create_unattempted action_id=%s pass_id=%s error=%s",
                    member["action_id"], member["pass_id"],
                    sanitize_error_message(exc),
                )
                return {
                    "action_id": member["action_id"], "pass_id": member["pass_id"],
                    "outcome": "authorized_unstarted", "provider": None,
                    "provider_create_metadata": None,
                    "reason": str(exc),
                }
            except ProviderCreateRefused as exc:
                logger.warning(
                    "initial_member_create_refused action_id=%s pass_id=%s error=%s",
                    member["action_id"], member["pass_id"],
                    sanitize_error_message(exc),
                )
                return {
                    "action_id": member["action_id"], "pass_id": member["pass_id"],
                    "outcome": "create_refused", "provider": None,
                    "provider_create_metadata": None,
                    "reason": str(exc),
                }
            except Exception as exc:
                logger.exception(
                    "initial_member_create_ambiguous action_id=%s pass_id=%s "
                    "error_class=%s error=%s",
                    member["action_id"], member["pass_id"], type(exc).__name__,
                    sanitize_error_message(exc),
                )
                return {
                    "action_id": member["action_id"], "pass_id": member["pass_id"],
                    "outcome": "ambiguous_submission", "provider": None,
                    "provider_create_metadata": None,
                    "reason": str(exc),
                }
            if (
                not isinstance(result, ProviderCreateResult)
                or not result.provider_id
                or result.provider_kind != "response"
            ):
                logger.error(
                    "initial_member_create_invalid_identity action_id=%s pass_id=%s",
                    member["action_id"], member["pass_id"],
                )
                return {
                    "action_id": member["action_id"], "pass_id": member["pass_id"],
                    "outcome": "ambiguous_submission", "provider": None,
                    "provider_create_metadata": None,
                    "reason": "Provider create returned no valid Response identity",
                }
            logger.info(
                "initial_member_create_complete action_id=%s pass_id=%s provider_id=%s",
                member["action_id"], member["pass_id"], result.provider_id,
            )
            return {
                "action_id": member["action_id"],
                "pass_id": member["pass_id"],
                "outcome": "provider_bound",
                "provider": {"kind": "response", "id": result.provider_id},
                "provider_create_metadata": dict(result.metadata or {}),
                "reason": None,
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
            logger.info(
                "initial_member_outcome_persisted wave_id=%s action_id=%s "
                "pass_id=%s outcome=%s persisted_count=%s",
                wave["wave_id"], member["action_id"], member["pass_id"],
                outcome["outcome"], len(outcomes) + 1,
            )
            outcomes[member["action_id"]] = outcome
        provider_io_finished = monotonic()
    except InitialWaveError as exc:
        logger.error(
            "initial_wave_failed wave_id=%s error_class=%s error=%s",
            wave["wave_id"], type(exc).__name__, sanitize_error_message(exc),
        )
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
    logger.info(
        "initial_wave_complete wave_id=%s outcome=%s duration_ms=%s "
        "provider_bound=%s ambiguous=%s",
        wave["wave_id"], aggregate_outcome,
        round((provider_io_finished - started) * 1000),
        sum(item["outcome"] == "provider_bound" for item in ordered),
        sum(item["outcome"] == "ambiguous_submission" for item in ordered),
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
