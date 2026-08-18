"""Transport-neutral authoring-pass request/result bindings.

This module deliberately knows nothing about Responses versus Batch transport. Route
adapters retain ownership of prompt construction, schemas, validation, and authority
hydration; the shared seam only freezes the identity of one logical pass attempt.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping


PASS_REQUEST_CONTRACT = "astrowoof.authoring.logical_pass_request.v1"
PASS_RESULT_CONTRACT = "astrowoof.authoring.logical_pass_result.v1"
SUPPORTED_ROUTE_FAMILIES = frozenset({"exact_natal", "bounded_natal"})


class PassProtocolError(ValueError):
    """A logical pass crossed or changed an immutable route binding."""


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class LogicalPassRequest:
    route_family: str
    route_contract: str
    assignment_sha256: str
    pass_id: str
    pass_number: int
    pass_count: int
    attempt_number: int
    stage: str
    resource_sha256: str
    prompt_sha256: str
    output_schema_sha256: str
    maximum_output_tokens: int
    request_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": PASS_REQUEST_CONTRACT, **self.__dict__}


@dataclass(frozen=True)
class LogicalPassResult:
    route_family: str
    pass_id: str
    attempt_number: int
    request_sha256: str
    output_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": PASS_RESULT_CONTRACT, **self.__dict__}


def bind_logical_pass_request(
    *, route_family: str, route_contract: str, assignment_sha256: str,
    pass_id: str, pass_number: int, pass_count: int, attempt_number: int,
    stage: str, resource_identity: Any, prompt: Any, output_schema: Any,
    maximum_output_tokens: int,
) -> LogicalPassRequest:
    if route_family not in SUPPORTED_ROUTE_FAMILIES:
        raise PassProtocolError("Unsupported authoring-pass route family")
    strings = (route_contract, assignment_sha256, pass_id, stage)
    if not all(isinstance(item, str) and item for item in strings):
        raise PassProtocolError("Logical pass string bindings must be non-empty")
    integers = (pass_number, pass_count, attempt_number, maximum_output_tokens)
    if not all(isinstance(item, int) and not isinstance(item, bool) and item > 0 for item in integers):
        raise PassProtocolError("Logical pass numeric bindings must be positive integers")
    if pass_number > pass_count:
        raise PassProtocolError("Logical pass number exceeds pass count")
    basis = {
        "schema_version": PASS_REQUEST_CONTRACT,
        "route_family": route_family,
        "route_contract": route_contract,
        "assignment_sha256": assignment_sha256,
        "pass_id": pass_id,
        "pass_number": pass_number,
        "pass_count": pass_count,
        "attempt_number": attempt_number,
        "stage": stage,
        "resource_sha256": canonical_sha256(resource_identity),
        "prompt_sha256": canonical_sha256(prompt),
        "output_schema_sha256": canonical_sha256(output_schema),
        "maximum_output_tokens": maximum_output_tokens,
    }
    return LogicalPassRequest(
        **{key: value for key, value in basis.items() if key != "schema_version"},
        request_sha256=canonical_sha256(basis),
    )


def bind_logical_pass_result(
    request: LogicalPassRequest, output: Mapping[str, Any]
) -> LogicalPassResult:
    return LogicalPassResult(
        route_family=request.route_family,
        pass_id=request.pass_id,
        attempt_number=request.attempt_number,
        request_sha256=request.request_sha256,
        output_sha256=canonical_sha256(output),
    )


def validate_logical_pass_result(
    result: LogicalPassResult, request: LogicalPassRequest
) -> None:
    if (
        result.route_family != request.route_family
        or result.pass_id != request.pass_id
        or result.attempt_number != request.attempt_number
        or result.request_sha256 != request.request_sha256
    ):
        raise PassProtocolError("Logical pass result does not match its request binding")

