"""Durable per-run spend authorization for paid provider operations.

This module deliberately does not implement account-wide billing policy.  It
binds one external authorization to one exact SBE request and enforces the
frozen per-run and per-stage ceilings recorded in the authoring profile.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from decimal import Decimal, ROUND_CEILING
from typing import Any


LEDGER_SCHEMA = "astrowoof.provider_spend_ledger.v0.1"
AUTHORIZATION_SCHEMA = "astrowoof.provider_spend_authorization.v0.1"
PRICE_BOOK_VERSION = "openai-public-2026-08-07.v1"
PRICE_BOOK_USD_PER_MILLION = {
    "gpt-5.6": {"input": "5.00", "cached_input": "0.50", "output": "30.00"},
    "gpt-5.6-sol": {"input": "5.00", "cached_input": "0.50", "output": "30.00"},
    "gpt-5.6-terra": {"input": "2.50", "cached_input": "0.25", "output": "15.00"},
    "gpt-5.6-luna": {"input": "1.00", "cached_input": "0.10", "output": "6.00"},
}
PAID_STAGES = {
    "authoring_initial",
    "creative_retry",
    "polish",
    "qualitative_critic",
    "qualitative_candidate",
}
OPTIONAL_STAGES = {"polish", "qualitative_critic", "qualitative_candidate"}
OPEN_COMMITMENT_STATES = {
    "AUTHORIZED", "SUBMITTING", "PROVIDER_ID_RECORDED", "WAITING",
    "AMBIGUOUS_PROVIDER_SUBMISSION",
}


class SpendControlError(RuntimeError):
    state = "SPEND_CONTROL_ERROR"

    def __init__(self, message: str, *, action: dict[str, Any] | None = None):
        super().__init__(message)
        self.action = action


class AwaitingSpendAuthorization(SpendControlError):
    state = "AWAITING_SPEND_AUTHORIZATION"


class BudgetExhausted(SpendControlError):
    state = "BUDGET_EXHAUSTED"


class AmbiguousProviderSubmission(SpendControlError):
    state = "AMBIGUOUS_PROVIDER_SUBMISSION"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def usd_to_micros(value: str | int | float | Decimal) -> int:
    amount = Decimal(str(value))
    if amount < 0:
        raise ValueError("USD amount cannot be negative")
    return int((amount * Decimal(1_000_000)).to_integral_value(rounding=ROUND_CEILING))


def conservative_commitment_micros(
    *, model: str, input_tokens: int, maximum_output_tokens: int,
    service_level: str, price_book_version: str = PRICE_BOOK_VERSION,
) -> int:
    if price_book_version != PRICE_BOOK_VERSION:
        raise ValueError(f"Unsupported price book: {price_book_version}")
    rates = PRICE_BOOK_USD_PER_MILLION.get(model)
    if rates is None:
        raise ValueError(f"No spend-enforcement price for model {model!r}")
    multiplier = Decimal("0.5") if service_level == "batch" else Decimal("1")
    amount = multiplier * (
        Decimal(input_tokens) * Decimal(rates["input"])
        + Decimal(maximum_output_tokens) * Decimal(rates["output"])
    )
    return int(amount.to_integral_value(rounding=ROUND_CEILING))


def validate_policy(policy: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(policy, dict):
        raise ValueError("OpenAI runs require an explicit spend_policy object")
    if policy.get("currency") != "USD":
        raise ValueError("spend_policy.currency must be USD")
    if policy.get("price_book_version") != PRICE_BOOK_VERSION:
        raise ValueError("spend_policy must pin the supported price_book_version")
    run_ceiling = policy.get("run_ceiling_micro_usd")
    if not isinstance(run_ceiling, int) or run_ceiling < 0:
        raise ValueError("spend_policy.run_ceiling_micro_usd must be nonnegative integer")
    ceilings = policy.get("stage_ceilings_micro_usd")
    if not isinstance(ceilings, dict) or set(ceilings) != PAID_STAGES:
        raise ValueError("spend_policy must explicitly ceiling every paid stage")
    if any(not isinstance(value, int) or value < 0 for value in ceilings.values()):
        raise ValueError("stage ceilings must be nonnegative integer micro-USD")
    optional = policy.get("optional_stage_budget_behavior")
    if not isinstance(optional, dict) or set(optional) != OPTIONAL_STAGES:
        raise ValueError("spend_policy must define every optional-stage budget behavior")
    if any(value not in {"skip", "exhaust"} for value in optional.values()):
        raise ValueError("optional-stage budget behavior must be skip or exhaust")
    return deepcopy(policy)


def new_ledger(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": LEDGER_SCHEMA,
        "policy": validate_policy(policy),
        "actions": [],
        "reconciliation_references": [],
    }


def profile_digest(profile: dict[str, Any] | None) -> str:
    return digest(profile or {})


def action_binding(
    *, run_id: str, profile_sha256: str, prepared_state_revision: int,
    stage: str, route: str, request_sha256: str, model: str,
    service_level: str, maximum_output_tokens: int,
    commitment_micro_usd: int, price_book_version: str = PRICE_BOOK_VERSION,
) -> dict[str, Any]:
    if stage not in PAID_STAGES:
        raise ValueError(f"Unknown paid stage: {stage}")
    value = {
        "run_id": run_id,
        "profile_sha256": profile_sha256,
        "prepared_state_revision": prepared_state_revision,
        "stage": stage,
        "route": route,
        "request_sha256": request_sha256,
        "model": model,
        "service_level": service_level,
        "maximum_output_tokens": maximum_output_tokens,
        "commitment_micro_usd": commitment_micro_usd,
        "price_book_version": price_book_version,
    }
    return value


def prepare_action(ledger: dict[str, Any], binding: dict[str, Any]) -> dict[str, Any]:
    action_id = "paid_" + digest(binding)[:24]
    existing = next((item for item in ledger["actions"] if item["action_id"] == action_id), None)
    if existing:
        if existing["binding"] != binding:
            raise ValueError(f"Paid action identity collision: {action_id}")
        classify_prepared_budget(ledger, existing)
        return existing
    action = {
        "action_id": action_id,
        "state": "PREPARED",
        "binding": deepcopy(binding),
        "authorization": None,
        "provider": None,
        "reported": None,
        "reconciliation_reference_ids": [],
    }
    ledger["actions"].append(action)
    classify_prepared_budget(ledger, action)
    return action


def _counted_amount(action: dict[str, Any]) -> int:
    if action.get("reported") and action["reported"].get("estimated_micro_usd") is not None:
        return int(action["reported"]["estimated_micro_usd"])
    if action.get("state") in OPEN_COMMITMENT_STATES or action.get("authorization"):
        return int(action["binding"]["commitment_micro_usd"])
    return 0


def classify_prepared_budget(
    ledger: dict[str, Any], action: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed when a prepared action already exceeds its frozen ceiling."""
    if action.get("state") != "PREPARED":
        return action
    binding = action["binding"]
    commitment = int(binding["commitment_micro_usd"])
    policy = ledger["policy"]
    stage = binding["stage"]
    other = [item for item in ledger["actions"] if item is not action]
    run_total = sum(_counted_amount(item) for item in other) + commitment
    stage_total = sum(
        _counted_amount(item) for item in other
        if item["binding"]["stage"] == stage
    ) + commitment
    if (
        run_total > policy["run_ceiling_micro_usd"]
        or stage_total > policy["stage_ceilings_micro_usd"][stage]
    ):
        optional_skip = (
            stage in OPTIONAL_STAGES
            and policy["optional_stage_budget_behavior"][stage] == "skip"
        )
        action["state"] = (
            "SKIPPED_BUDGET_EXHAUSTED" if optional_skip else "BUDGET_EXHAUSTED"
        )
    return action


def authorize_action(
    ledger: dict[str, Any], authorization: dict[str, Any],
) -> dict[str, Any]:
    if authorization.get("schema_version") != AUTHORIZATION_SCHEMA:
        raise ValueError("Unsupported spend authorization schema")
    action_id = authorization.get("action_id")
    action = next((item for item in ledger["actions"] if item["action_id"] == action_id), None)
    if action is None:
        raise ValueError(f"Unknown paid action: {action_id}")
    if authorization.get("binding") != action["binding"]:
        raise ValueError("Authorization binding does not exactly match prepared action")
    if not isinstance(authorization.get("authorization_reference"), str) or not authorization["authorization_reference"]:
        raise ValueError("Authorization requires an external authorization_reference")
    commitment = int(action["binding"]["commitment_micro_usd"])
    policy = ledger["policy"]
    stage = action["binding"]["stage"]
    other = [item for item in ledger["actions"] if item is not action]
    run_total = sum(_counted_amount(item) for item in other) + commitment
    stage_total = sum(
        _counted_amount(item) for item in other
        if item["binding"]["stage"] == stage
    ) + commitment
    if run_total > policy["run_ceiling_micro_usd"] or stage_total > policy["stage_ceilings_micro_usd"][stage]:
        optional_skip = (
            stage in OPTIONAL_STAGES
            and policy["optional_stage_budget_behavior"][stage] == "skip"
        )
        action["state"] = (
            "SKIPPED_BUDGET_EXHAUSTED" if optional_skip else "BUDGET_EXHAUSTED"
        )
        if optional_skip:
            return action
        raise BudgetExhausted("Authorization would exceed frozen spend ceiling", action=action)
    if action["state"] not in {"PREPARED", "AUTHORIZED"}:
        raise ValueError(f"Cannot authorize action in state {action['state']}")
    action["authorization"] = deepcopy(authorization)
    action["state"] = "AUTHORIZED"
    return action


def begin_submission(action: dict[str, Any], *, consumer_id: str, state_revision: int) -> None:
    if action.get("state") != "AUTHORIZED":
        raise AwaitingSpendAuthorization("Paid action is not authorized", action=action)
    action["state"] = "SUBMITTING"
    action["consumption"] = {
        "consumer_id": consumer_id,
        "state_revision": state_revision,
    }


def mark_ambiguous(action: dict[str, Any], *, reason: str) -> None:
    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
    action["ambiguity"] = {"reason": reason}


def record_provider_id(action: dict[str, Any], *, provider_id: str, kind: str) -> None:
    if action.get("state") != "SUBMITTING":
        raise ValueError("Provider identity can only be recorded for a submitting action")
    if not provider_id:
        mark_ambiguous(action, reason="provider returned no durable operation ID")
        raise AmbiguousProviderSubmission("Provider returned no operation ID", action=action)
    action["provider"] = {"kind": kind, "id": provider_id}
    action["state"] = "PROVIDER_ID_RECORDED"


def record_reported_cost(
    action: dict[str, Any], *, usage: dict[str, int], estimated_micro_usd: int,
) -> None:
    action["reported"] = {
        "usage": deepcopy(usage),
        "estimated_micro_usd": estimated_micro_usd,
    }
    action["state"] = "REPORTED"


def append_reconciliation_reference(
    ledger: dict[str, Any], *, action_id: str, reference_id: str,
    authority: str, amount_micro_usd: int | None = None,
) -> dict[str, Any]:
    if any(item["reference_id"] == reference_id for item in ledger["reconciliation_references"]):
        raise ValueError(f"Reconciliation reference already exists: {reference_id}")
    record = {
        "reference_id": reference_id,
        "action_id": action_id,
        "authority": authority,
        "amount_micro_usd": amount_micro_usd,
    }
    ledger["reconciliation_references"].append(record)
    action = next(item for item in ledger["actions"] if item["action_id"] == action_id)
    action["reconciliation_reference_ids"].append(reference_id)
    return record
