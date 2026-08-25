"""Provider-free public contract and dry-run for exact-run operator retirement."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import re
import sys
from typing import Any, Mapping

from .closure import (
    SNAPSHOT_NAME, load_json, normalized_path, persist_state,
    snapshot_inventory, validate_workspace_snapshot, write_workspace_snapshot,
)
from .lifecycle import _exclusive_lifecycle_lock, inspect_lifecycle
from .native_transitions import (
    publish_native_execution_result, read_native_transition_result,
)
from .reconciliation import native_provider_route_identity
from .resource_access import read_resource_text


REQUEST_SCHEMA = "astrowoof.operator_retirement_request.v1"
ASSESSMENT_SCHEMA = "astrowoof.operator_retirement_assessment.v1"
RESULT_SCHEMA = "astrowoof.operator_retirement_result.v1"
CONTRACT_RESOURCE = "contracts/operator-retirement-contracts.v1.schema.json"
EXACT_RUN_CONTRACT = "astrowoof.semantic_closure_run.v0.9"
RETIREMENT_ELIGIBLE_STATUSES = frozenset({
    "AUTHORING", "AUTHORING_COMPLETE", "WAITING_FOR_RESPONSE",
    "AWAITING_SPEND_AUTHORIZATION",
})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUEST_KEYS = frozenset({
    "schema_version", "request_sha256", "run_id", "route_family",
    "route_contract", "logical_workspace_root", "expected_status",
    "expected_state_revision", "expected_snapshot_sha256",
    "checkpoint_basis_sha256", "terminal_action_closure_sha256",
    "requested_terminal_status", "requested_terminal_cause", "reason_code",
    "operator_audit_reference", "human_reason",
})
ASSESSMENT_KEYS = frozenset({
    "schema_version", "mode", "outcome", "request_sha256", "run_id",
    "route_family", "logical_workspace_root", "state_revision",
    "snapshot_sha256", "checkpoint_basis_sha256",
    "terminal_action_closure_sha256", "retirement_quiescent",
    "failed_predicates", "mutation_performed", "native_result_published",
    "provider_io_performed_count",
})
RESULT_KEYS = frozenset({
    "schema_version", "outcome", "applied", "request_sha256",
    "original_request_sha256", "run_id",
    "route_family", "logical_workspace_root", "pre_state_revision",
    "post_state_revision", "pre_snapshot_sha256", "post_snapshot_sha256",
    "terminal_status", "terminal_cause", "terminal_action_closure_sha256",
    "continuation_assertions", "native_result", "publication_receipt",
    "failed_predicates", "provider_io_performed_count",
})
FAILURE_VOCABULARY = frozenset({
    "binding_mismatch", "delivery_or_terminal_conflict",
    "not_retirement_quiescent", "provider_ambiguity_present",
    "provider_custody_present", "providerless_action_unresolved",
    "snapshot_invalid", "stale_observation", "unsupported_contract",
})


def _sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _release() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        return "0.4.18.dev0"


def _canonical_utc(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("committed_at is invalid")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("committed_at is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("committed_at must be timezone-aware")
    canonical = parsed.astimezone(timezone.utc).isoformat()
    if canonical != value:
        raise ValueError("committed_at must use canonical UTC representation")
    return canonical


def _closure_sha256(state: Mapping[str, Any]) -> str:
    """Commit to every action byte, including providerless denial outcomes."""
    actions = (state.get("spend_ledger") or {}).get("actions") or []
    return _sha256(actions)


def _basis(
    *, run_id: str, route_contract: str, logical_root: str, status: str,
    revision: int, snapshot_sha256: str, closure_sha256: str,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "route_family": "exact_natal",
        "route_contract": route_contract,
        "logical_workspace_root": logical_root,
        "status": status,
        "state_revision": revision,
        "snapshot_sha256": snapshot_sha256,
        "terminal_action_closure_sha256": closure_sha256,
    }


def validate_operator_retirement_request(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != REQUEST_KEYS:
        raise ValueError("Operator-retirement request fields are not exact")
    if value.get("schema_version") != REQUEST_SCHEMA:
        raise ValueError("Unsupported operator-retirement request")
    for field in (
        "request_sha256", "expected_snapshot_sha256",
        "checkpoint_basis_sha256", "terminal_action_closure_sha256",
    ):
        if not isinstance(value.get(field), str) or not SHA256_RE.fullmatch(value[field]):
            raise ValueError(f"{field} is not a canonical SHA-256")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("run_id is invalid")
    if value.get("route_family") != "exact_natal" or value.get(
        "route_contract"
    ) != EXACT_RUN_CONTRACT:
        raise ValueError("Only the exact-Natal v0.9 route is supported")
    if not isinstance(value.get("logical_workspace_root"), str) or not value[
        "logical_workspace_root"
    ]:
        raise ValueError("logical_workspace_root is invalid")
    revision = value.get("expected_state_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise ValueError("expected_state_revision is invalid")
    if (
        value.get("expected_status") not in RETIREMENT_ELIGIBLE_STATUSES
        or value.get("requested_terminal_status") != "POLICY_STOPPED"
        or value.get("requested_terminal_cause") != "operator_retired"
        or value.get("reason_code") != "operator_abandoned_quiescent_run"
    ):
        raise ValueError("Operator-retirement semantics are invalid")
    reference = value.get("operator_audit_reference")
    human_reason = value.get("human_reason")
    if not isinstance(reference, str) or not 1 <= len(reference) <= 256:
        raise ValueError("operator_audit_reference is invalid")
    if human_reason is not None and (
        not isinstance(human_reason, str) or len(human_reason) > 500
    ):
        raise ValueError("human_reason is invalid")
    basis = _basis(
        run_id=value["run_id"], route_contract=value["route_contract"],
        logical_root=value["logical_workspace_root"],
        status=value["expected_status"], revision=revision,
        snapshot_sha256=value["expected_snapshot_sha256"],
        closure_sha256=value["terminal_action_closure_sha256"],
    )
    if value["checkpoint_basis_sha256"] != _sha256(basis):
        raise ValueError("checkpoint_basis_sha256 is invalid")
    unsigned = {key: deepcopy(item) for key, item in value.items()
                if key != "request_sha256"}
    if value["request_sha256"] != _sha256(unsigned):
        raise ValueError("request_sha256 is invalid")
    return deepcopy(value)


def validate_operator_retirement_assessment(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != ASSESSMENT_KEYS:
        raise ValueError("Operator-retirement assessment fields are not exact")
    if value.get("schema_version") != ASSESSMENT_SCHEMA or value.get("mode") != "dry_run":
        raise ValueError("Unsupported operator-retirement assessment")
    for field in (
        "request_sha256", "snapshot_sha256", "checkpoint_basis_sha256",
        "terminal_action_closure_sha256",
    ):
        if not isinstance(value.get(field), str) or not SHA256_RE.fullmatch(value[field]):
            raise ValueError(f"{field} is not a canonical SHA-256")
    run_id = value.get("run_id")
    root = value.get("logical_workspace_root")
    revision = value.get("state_revision")
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("Assessment run_id is invalid")
    if not isinstance(root, str) or not root:
        raise ValueError("Assessment logical_workspace_root is invalid")
    if (
        not isinstance(revision, int) or isinstance(revision, bool) or revision < 0
        or value.get("route_family") not in {"exact_natal", None}
    ):
        raise ValueError("Assessment native identity is invalid")
    failures = value.get("failed_predicates")
    native_failures = FAILURE_VOCABULARY - {"binding_mismatch", "stale_observation"}
    if (
        not isinstance(failures, list) or failures != sorted(set(failures))
        or any(item not in FAILURE_VOCABULARY for item in failures)
        or value.get("outcome") not in {"eligible", "refused"}
        or (value["outcome"] == "eligible") != (not failures)
        or value["outcome"] == "eligible" and value["route_family"] != "exact_natal"
        or value["route_family"] is None and "unsupported_contract" not in failures
        or not isinstance(value.get("retirement_quiescent"), bool)
        or value["outcome"] == "eligible" and value["retirement_quiescent"] is not True
        or value["retirement_quiescent"] is False
        and not any(item in native_failures for item in failures)
        or value.get("mutation_performed") is not False
        or value.get("native_result_published") is not False
        or not isinstance(value.get("provider_io_performed_count"), int)
        or isinstance(value.get("provider_io_performed_count"), bool)
        or value.get("provider_io_performed_count") != 0
    ):
        raise ValueError("Operator-retirement assessment semantics are invalid")
    return deepcopy(value)


def validate_operator_retirement_result(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != RESULT_KEYS:
        raise ValueError("Operator-retirement result fields are not exact")
    if value.get("schema_version") != RESULT_SCHEMA:
        raise ValueError("Unsupported operator-retirement result")
    for field in (
        "request_sha256", "pre_snapshot_sha256", "post_snapshot_sha256",
        "terminal_action_closure_sha256",
    ):
        if not isinstance(value.get(field), str) or not SHA256_RE.fullmatch(value[field]):
            raise ValueError(f"{field} is not a canonical SHA-256")
    original_request = value.get("original_request_sha256")
    if original_request is not None and (
        not isinstance(original_request, str) or not SHA256_RE.fullmatch(original_request)
    ):
        raise ValueError("original_request_sha256 is invalid")
    if not isinstance(value.get("run_id"), str) or not value["run_id"]:
        raise ValueError("Result run_id is invalid")
    if not isinstance(value.get("logical_workspace_root"), str) or not value[
        "logical_workspace_root"
    ]:
        raise ValueError("Result logical_workspace_root is invalid")
    for field in ("pre_state_revision", "post_state_revision"):
        revision = value.get(field)
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            raise ValueError(f"{field} is invalid")
    failures = value.get("failed_predicates")
    if (
        not isinstance(failures, list) or failures != sorted(set(failures))
        or any(item not in FAILURE_VOCABULARY for item in failures)
        or value.get("outcome") not in {"applied", "exact_replay", "already_retired"}
        | FAILURE_VOCABULARY
        or not isinstance(value.get("applied"), bool)
        or value.get("provider_io_performed_count") != 0
        or isinstance(value.get("provider_io_performed_count"), bool)
    ):
        raise ValueError("Operator-retirement result semantics are invalid")
    assertions = value.get("continuation_assertions")
    if not isinstance(assertions, dict) or set(assertions) != {
        "provider_pending", "provider_custody", "local_continuation",
    } or any(not isinstance(item, bool) for item in assertions.values()):
        raise ValueError("Result continuation assertions are invalid")
    success = value["outcome"] in {"applied", "exact_replay", "already_retired"}
    if success:
        native = value.get("native_result")
        receipt = value.get("publication_receipt")
        if (
            failures or value["route_family"] != "exact_natal"
            or original_request is None
            or value["outcome"] == "applied" and value["applied"] is not True
            or value["terminal_status"] != "POLICY_STOPPED"
            or value["terminal_cause"] != "operator_retired"
            or any(assertions.values()) or not isinstance(native, dict)
            or set(native) != {"result_id", "result_sha256"}
            or not re.fullmatch(r"nres_[0-9a-f]{24}", str(native.get("result_id")))
            or not SHA256_RE.fullmatch(str(native.get("result_sha256")))
            or not isinstance(receipt, dict)
            or set(receipt) != {"receipt_id", "receipt_sha256"}
            or not re.fullmatch(
                r"nreceipt_[0-9a-f]{24}", str(receipt.get("receipt_id"))
            ) or not SHA256_RE.fullmatch(str(receipt.get("receipt_sha256")))
            or value["post_state_revision"] < value["pre_state_revision"]
        ):
            raise ValueError("Successful operator-retirement result is invalid")
        if value["outcome"] in {"exact_replay", "already_retired"} and value[
            "applied"
        ] is not False:
            raise ValueError("Replay result cannot claim a new mutation")
    elif (
        value["applied"] is not False or value["outcome"] not in failures
        or original_request is not None
        or value.get("native_result") is not None
        or value.get("publication_receipt") is not None
        or value.get("terminal_status") is not None
        or value.get("terminal_cause") is not None
    ):
        raise ValueError("Refused operator-retirement result is invalid")
    return deepcopy(value)


def _current(run_dir: Path, state: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    snapshot_path = run_dir / SNAPSHOT_NAME
    try:
        validate_workspace_snapshot(run_dir, state)
        snapshot_sha256 = _file_sha256(snapshot_path)
    except (OSError, ValueError, TypeError, KeyError):
        snapshot_sha256 = "0" * 64
        failures.append("snapshot_invalid")
    identity = native_provider_route_identity(state)
    if not (
        identity.get("valid") and identity.get("route_family") == "exact_natal"
        and identity.get("route_contract") == EXACT_RUN_CONTRACT
    ):
        failures.append("unsupported_contract")
    lifecycle = inspect_lifecycle(
        run_dir, native_exclusive_access="established",
        observed_at="2000-01-01T00:00:00+00:00",
    )
    actions = list((state.get("spend_ledger") or {}).get("actions") or [])
    inventory = lifecycle["action_inventory"]["actions"]
    if any(item.get("state") in {"SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION"}
           or item.get("ambiguity_review_reasons") for item in inventory):
        failures.append("provider_ambiguity_present")
    if any(item.get("necessary") for item in inventory):
        failures.append("provider_custody_present")
    unresolved = []
    for action in actions:
        if (
            action.get("state") in {"PREPARED", "AUTHORIZED"}
            and not action.get("provider") and not action.get("consumption")
            and not action.get("reported")
        ):
            unresolved.append(action)
    if unresolved:
        failures.append("providerless_action_unresolved")
    if any(
        not action.get("provider")
        and action.get("state") != "DENIED_PROVIDERLESS"
        and any(action.get(field) for field in ("authorization", "consumption", "reported"))
        for action in actions
    ):
        failures.append("provider_ambiguity_present")
    terminal = lifecycle["terminal"]
    if (
        terminal.get("terminal") or terminal.get("delivery_publishable")
        or terminal.get("deck_bytes_exist")
        or state.get("status") not in RETIREMENT_ELIGIBLE_STATUSES
    ):
        failures.append("delivery_or_terminal_conflict")
    # Active/ambiguous/action-backed continuation is unsafe. The status-derived
    # retry_preparation dependency with no unresolved action is the future work
    # the operator is deliberately abandoning.
    if any(action.get("state") == "SUBMITTING" for action in actions):
        failures.append("not_retirement_quiescent")
    contract = state.get("workspace_contract") or {}
    logical_root = str(contract.get("logical_root") or normalized_path(run_dir))
    closure_sha256 = _closure_sha256(state)
    basis = _basis(
        run_id=str(state.get("run_id") or ""),
        route_contract=str(identity.get("route_contract") or ""),
        logical_root=logical_root, status=str(state.get("status") or ""),
        revision=int(state.get("state_revision") or 0),
        snapshot_sha256=snapshot_sha256, closure_sha256=closure_sha256,
    )
    return {
        "run_id": basis["run_id"], "route_family": identity.get("route_family"),
        "route_contract": basis["route_contract"],
        "logical_workspace_root": logical_root, "status": basis["status"],
        "state_revision": basis["state_revision"],
        "snapshot_sha256": snapshot_sha256,
        "checkpoint_basis_sha256": _sha256(basis),
        "terminal_action_closure_sha256": closure_sha256,
    }, sorted(set(failures))


def build_operator_retirement_request(
    run_dir: Path, *, operator_audit_reference: str,
    human_reason: str | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        state = load_json(run_dir / "run.json")
        current, native_failures = _current(run_dir, state)
        failures = list(native_failures)
        if failures:
            raise ValueError("Run is not retirement-eligible: " + ", ".join(failures))
        request = {
            "schema_version": REQUEST_SCHEMA,
            "run_id": current["run_id"],
            "route_family": "exact_natal",
            "route_contract": current["route_contract"],
            "logical_workspace_root": current["logical_workspace_root"],
            "expected_status": current["status"],
            "expected_state_revision": current["state_revision"],
            "expected_snapshot_sha256": current["snapshot_sha256"],
            "checkpoint_basis_sha256": current["checkpoint_basis_sha256"],
            "terminal_action_closure_sha256": current[
                "terminal_action_closure_sha256"
            ],
            "requested_terminal_status": "POLICY_STOPPED",
            "requested_terminal_cause": "operator_retired",
            "reason_code": "operator_abandoned_quiescent_run",
            "operator_audit_reference": operator_audit_reference,
            "human_reason": human_reason,
        }
        request["request_sha256"] = _sha256(request)
        return validate_operator_retirement_request(request)


def assess_operator_retirement(run_dir: Path, request: Mapping[str, Any]) -> dict[str, Any]:
    validated = validate_operator_retirement_request(dict(request))
    run_dir = run_dir.resolve()
    with _exclusive_lifecycle_lock(run_dir):
        state = load_json(run_dir / "run.json")
        current, native_failures = _current(run_dir, state)
        failures = list(native_failures)
        joins = {
            "run_id": "binding_mismatch",
            "route_family": "unsupported_contract",
            "route_contract": "unsupported_contract",
            "logical_workspace_root": "binding_mismatch",
            "expected_status": "stale_observation",
            "expected_state_revision": "stale_observation",
            "expected_snapshot_sha256": "stale_observation",
            "checkpoint_basis_sha256": "stale_observation",
            "terminal_action_closure_sha256": "stale_observation",
        }
        current_names = {
            "expected_status": "status", "expected_state_revision": "state_revision",
            "expected_snapshot_sha256": "snapshot_sha256",
        }
        for request_key, reason in joins.items():
            current_key = current_names.get(request_key, request_key)
            if validated[request_key] != current.get(current_key):
                failures.append(reason)
        failures = sorted(set(failures))
        result = {
            "schema_version": ASSESSMENT_SCHEMA,
            "mode": "dry_run",
            "outcome": "eligible" if not failures else "refused",
            "request_sha256": validated["request_sha256"],
            "run_id": current["run_id"],
            "route_family": current["route_family"],
            "logical_workspace_root": current["logical_workspace_root"],
            "state_revision": current["state_revision"],
            "snapshot_sha256": current["snapshot_sha256"],
            "checkpoint_basis_sha256": current["checkpoint_basis_sha256"],
            "terminal_action_closure_sha256": current[
                "terminal_action_closure_sha256"
            ],
            "retirement_quiescent": not native_failures,
            "failed_predicates": failures,
            "mutation_performed": False,
            "native_result_published": False,
            "provider_io_performed_count": 0,
        }
        return validate_operator_retirement_assessment(result)


def _request_failures(
    request: Mapping[str, Any], current: Mapping[str, Any],
    native_failures: list[str],
) -> list[str]:
    failures = list(native_failures)
    joins = {
        "run_id": "binding_mismatch", "route_family": "unsupported_contract",
        "route_contract": "unsupported_contract",
        "logical_workspace_root": "binding_mismatch",
        "expected_status": "stale_observation",
        "expected_state_revision": "stale_observation",
        "expected_snapshot_sha256": "stale_observation",
        "checkpoint_basis_sha256": "stale_observation",
        "terminal_action_closure_sha256": "stale_observation",
    }
    current_names = {
        "expected_status": "status", "expected_state_revision": "state_revision",
        "expected_snapshot_sha256": "snapshot_sha256",
    }
    for request_key, reason in joins.items():
        if request[request_key] != current.get(current_names.get(request_key, request_key)):
            failures.append(reason)
    return sorted(set(failures))


def _retirement_projection(
    request: Mapping[str, Any], *, pre_revision: int,
    assertions: Mapping[str, bool], closure_sha256: str,
) -> dict[str, Any]:
    return {"operator_retirement": {
        "request_sha256": request["request_sha256"],
        "pre_state_revision": pre_revision,
        "pre_snapshot_sha256": request["expected_snapshot_sha256"],
        "checkpoint_basis_sha256": request["checkpoint_basis_sha256"],
        "terminal_action_closure_sha256": closure_sha256,
        "terminal_status": "POLICY_STOPPED", "terminal_cause": "operator_retired",
        "continuation_assertions": deepcopy(dict(assertions)),
    }}


def _recover_retirement_snapshot(run_dir: Path, state: dict[str, Any]) -> None:
    try:
        validate_workspace_snapshot(run_dir, state)
        return
    except (OSError, ValueError, TypeError, KeyError):
        pass
    manifest = load_json(run_dir / SNAPSHOT_NAME)
    expected = {item["path"]: item for item in manifest.get("members", [])}
    actual = {
        item["path"]: item
        for item in snapshot_inventory(run_dir, use_process_cache=False)
    }
    changed = {
        path for path in set(expected) | set(actual)
        if expected.get(path) != actual.get(path)
    }
    allowed = {
        "run.json", "public-run.json", "spend-authorization-requests.json",
    }
    if not changed or not changed <= allowed or "run.json" not in changed:
        raise ValueError("Interrupted retirement snapshot cannot be safely recovered")
    write_workspace_snapshot(run_dir)
    validate_workspace_snapshot(run_dir, state)


def _compatible_retired_request(
    request: Mapping[str, Any], transition: Mapping[str, Any],
) -> bool:
    comparisons = {
        "run_id": "run_id", "route_family": "route_family",
        "route_contract": "route_contract",
        "logical_workspace_root": "logical_workspace_root",
        "expected_status": "prior_status",
        "expected_state_revision": "pre_state_revision",
        "expected_snapshot_sha256": "pre_snapshot_sha256",
        "checkpoint_basis_sha256": "checkpoint_basis_sha256",
        "terminal_action_closure_sha256": "terminal_action_closure_sha256",
    }
    return all(request[left] == transition.get(right) for left, right in comparisons.items())


def _sealed_retirement(
    run_dir: Path, state: dict[str, Any], request: Mapping[str, Any],
    transition: Mapping[str, Any], *, event_emitter: Any,
) -> dict[str, Any]:
    _recover_retirement_snapshot(run_dir, state)
    original_request = dict(request)
    original_request.update({
        "request_sha256": transition["request_sha256"],
        "expected_snapshot_sha256": transition["pre_snapshot_sha256"],
        "checkpoint_basis_sha256": transition["checkpoint_basis_sha256"],
    })
    projection = _retirement_projection(
        original_request, pre_revision=int(transition["pre_state_revision"]),
        assertions={
            "provider_pending": False, "provider_custody": False,
            "local_continuation": False,
        }, closure_sha256=str(transition["terminal_action_closure_sha256"]),
    )
    index_path = run_dir / "native-result-index.json"
    matching = None
    if index_path.is_file():
        for result_id in load_json(index_path).get("result_ids", []):
            candidate = load_json(run_dir / "native-results" / f"{result_id}.json")
            projected = (candidate.get("projection_refs") or {}).get(
                "operator_retirement"
            ) or {}
            if projected.get("request_sha256") == transition["request_sha256"]:
                matching = candidate
    if matching is not None and (
        run_dir / "native-publication-receipts" / f"{matching['result_id']}.json"
    ).is_file():
        return read_native_transition_result(run_dir, matching["result_id"])
    return publish_native_execution_result(
        run_dir, command_kind="operator_retirement", sbe_release=_release(),
        published_at=str(transition["committed_at"]), event_emitter=event_emitter,
        projection_refs=projection, _writer_held=True,
    )


def _replay_result(
    run_dir: Path, state: dict[str, Any], request: Mapping[str, Any], *,
    event_emitter: Any,
) -> dict[str, Any] | None:
    transition = state.get("terminal_transition") or {}
    if not (
        transition.get("schema_version")
        == "astrowoof.operator_retirement_transition.v1"
        and transition.get("outcome") == "terminalized"
        and transition.get("terminal_reason") == "operator_retired"
    ):
        return None
    exact = request["request_sha256"] == transition.get("request_sha256")
    compatible = _compatible_retired_request(request, transition)
    if not exact and not compatible:
        return None
    sealed = _sealed_retirement(
        run_dir, state, request, transition, event_emitter=event_emitter,
    )
    native = sealed["result"]
    receipt = sealed["receipt"]
    assertions = deepcopy(
        ((native.get("projection_refs") or {}).get("operator_retirement") or {}).get(
            "continuation_assertions"
        ) or {}
    )
    result = {
        "schema_version": RESULT_SCHEMA,
        "outcome": "exact_replay" if exact else "already_retired",
        "applied": False, "request_sha256": request["request_sha256"],
        "original_request_sha256": transition["request_sha256"],
        "run_id": state["run_id"], "route_family": "exact_natal",
        "logical_workspace_root": transition["logical_workspace_root"],
        "pre_state_revision": transition["pre_state_revision"],
        "post_state_revision": state["state_revision"],
        "pre_snapshot_sha256": transition["pre_snapshot_sha256"],
        "post_snapshot_sha256": receipt["snapshot_sha256"],
        "terminal_status": "POLICY_STOPPED", "terminal_cause": "operator_retired",
        "terminal_action_closure_sha256": transition[
            "terminal_action_closure_sha256"
        ], "continuation_assertions": assertions,
        "native_result": {"result_id": native["result_id"],
                          "result_sha256": native["result_sha256"]},
        "publication_receipt": {"receipt_id": receipt["receipt_id"],
                                "receipt_sha256": receipt["receipt_sha256"]},
        "failed_predicates": [], "provider_io_performed_count": 0,
    }
    return validate_operator_retirement_result(result)


def execute_operator_retirement(
    run_dir: Path, request: Mapping[str, Any], *, committed_at: str | None = None,
    event_emitter: Any = None, _failure_injector: Any = None,
) -> dict[str, Any]:
    """Apply one exact, provider-free native retirement under the lifecycle writer."""
    validated = validate_operator_retirement_request(dict(request))
    run_dir = run_dir.resolve()
    when = _canonical_utc(committed_at or datetime.now(timezone.utc).isoformat())
    with _exclusive_lifecycle_lock(run_dir):
        state = load_json(run_dir / "run.json")
        replay = _replay_result(
            run_dir, state, validated, event_emitter=event_emitter,
        )
        if replay is not None:
            return replay
        current, native_failures = _current(run_dir, state)
        failures = _request_failures(validated, current, native_failures)
        if failures:
            refused_lifecycle = inspect_lifecycle(
                run_dir, native_exclusive_access="established", observed_at=when,
            )
            result = {
                "schema_version": RESULT_SCHEMA, "outcome": failures[0],
                "applied": False, "request_sha256": validated["request_sha256"],
                "original_request_sha256": None,
                "run_id": current["run_id"],
                "route_family": current["route_family"],
                "logical_workspace_root": current["logical_workspace_root"],
                "pre_state_revision": current["state_revision"],
                "post_state_revision": current["state_revision"],
                "pre_snapshot_sha256": current["snapshot_sha256"],
                "post_snapshot_sha256": current["snapshot_sha256"],
                "terminal_status": None, "terminal_cause": None,
                "terminal_action_closure_sha256": current[
                    "terminal_action_closure_sha256"
                ],
                "continuation_assertions": {
                    "provider_pending": refused_lifecycle["terminal"][
                        "provider_continuation_remains"
                    ],
                    "provider_custody": bool(
                        refused_lifecycle["provider_custody"]["provider_action_count"]
                    ),
                    "local_continuation": refused_lifecycle["terminal"][
                        "local_continuation_remains"
                    ],
                },
                "native_result": None, "publication_receipt": None,
                "failed_predicates": failures, "provider_io_performed_count": 0,
            }
            validated_result = validate_operator_retirement_result(result)
            if event_emitter is not None:
                event_emitter.emit("execution.failed", data={
                    "reason_code": failures[0],
                    "failure_class": "operator_retirement_refused",
                    "failed_predicate_count": len(failures),
                }, correlation={"native_run_id": current["run_id"]})
            return validated_result
        pre_revision = current["state_revision"]
        state["terminal_transition"] = {
            "schema_version": "astrowoof.operator_retirement_transition.v1",
            "outcome": "terminalized", "trigger": "operator_retirement",
            "prior_status": state["status"], "resulting_status": "POLICY_STOPPED",
            "terminal_outcome": "policy_stopped",
            "terminal_reason": "operator_retired",
            "reason_code": "operator_abandoned_quiescent_run",
            "request_sha256": validated["request_sha256"],
            "operator_audit_reference": validated["operator_audit_reference"],
            "terminal_action_closure_sha256": current[
                "terminal_action_closure_sha256"
            ],
            "run_id": validated["run_id"], "route_family": "exact_natal",
            "route_contract": validated["route_contract"],
            "logical_workspace_root": validated["logical_workspace_root"],
            "pre_state_revision": pre_revision,
            "pre_snapshot_sha256": validated["expected_snapshot_sha256"],
            "checkpoint_basis_sha256": validated["checkpoint_basis_sha256"],
            "committed_at": when,
        }
        persist_state(run_dir / "run.json", state)
        if event_emitter is not None:
            event_emitter.emit("terminal.transitioned", data={
                "outcome": "policy_stopped", "terminal_reason": "operator_retired",
                "request_sha256": validated["request_sha256"],
            }, correlation={"native_run_id": validated["run_id"]})
        if _failure_injector is not None:
            _failure_injector("after_state_persisted")
        state = load_json(run_dir / "run.json")
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, state)
        if _failure_injector is not None:
            _failure_injector("after_transition_snapshot")
        post = inspect_lifecycle(
            run_dir, native_exclusive_access="established", observed_at=when,
        )
        assertions = {
            "provider_pending": post["terminal"]["provider_continuation_remains"],
            "provider_custody": bool(post["provider_custody"]["provider_action_count"]),
            "local_continuation": post["terminal"]["local_continuation_remains"],
        }
        if any(assertions.values()):
            raise ValueError("Post-retirement lifecycle is not closed")
        sealed = publish_native_execution_result(
            run_dir, command_kind="operator_retirement", sbe_release=_release(),
            published_at=when, event_emitter=event_emitter, _writer_held=True,
            projection_refs=_retirement_projection(
                validated, pre_revision=pre_revision, assertions=assertions,
                closure_sha256=current["terminal_action_closure_sha256"],
            ),
        )
        if _failure_injector is not None:
            _failure_injector("after_native_publication")
        final_state = load_json(run_dir / "run.json")
        final = inspect_lifecycle(
            run_dir, native_exclusive_access="established", observed_at=when,
        )
        final_assertions = {
            "provider_pending": final["terminal"]["provider_continuation_remains"],
            "provider_custody": bool(final["provider_custody"]["provider_action_count"]),
            "local_continuation": final["terminal"]["local_continuation_remains"],
        }
        if any(final_assertions.values()):
            raise ValueError("Sealed post-retirement lifecycle is not closed")
        native = sealed["result"]
        receipt = sealed["receipt"]
        result = {
            "schema_version": RESULT_SCHEMA, "outcome": "applied", "applied": True,
            "request_sha256": validated["request_sha256"],
            "original_request_sha256": validated["request_sha256"],
            "run_id": final_state["run_id"], "route_family": "exact_natal",
            "logical_workspace_root": current["logical_workspace_root"],
            "pre_state_revision": pre_revision,
            "post_state_revision": final_state["state_revision"],
            "pre_snapshot_sha256": validated["expected_snapshot_sha256"],
            "post_snapshot_sha256": receipt["snapshot_sha256"],
            "terminal_status": "POLICY_STOPPED", "terminal_cause": "operator_retired",
            "terminal_action_closure_sha256": current[
                "terminal_action_closure_sha256"
            ], "continuation_assertions": final_assertions,
            "native_result": {"result_id": native["result_id"],
                              "result_sha256": native["result_sha256"]},
            "publication_receipt": {"receipt_id": receipt["receipt_id"],
                                    "receipt_sha256": receipt["receipt_sha256"]},
            "failed_predicates": [], "provider_io_performed_count": 0,
        }
        return validate_operator_retirement_result(result)


def read_operator_retirement_schema() -> dict[str, Any]:
    return json.loads(read_resource_text(CONTRACT_RESOURCE))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    subparsers.add_parser("schema")
    build = subparsers.add_parser("build-request")
    build.add_argument("--operator-audit-reference", required=True)
    build.add_argument("--human-reason")
    dry = subparsers.add_parser("dry-run")
    dry.add_argument("--request", required=True, type=Path)
    execute = subparsers.add_parser("execute")
    execute.add_argument("--request", required=True, type=Path)
    execute.add_argument("--committed-at")
    args = parser.parse_args()
    if args.operation != "schema" and args.run_dir is None:
        parser.error("--run-dir is required for this operation")
    if args.operation == "schema":
        value = read_operator_retirement_schema()
    elif args.operation == "build-request":
        value = build_operator_retirement_request(
            args.run_dir, operator_audit_reference=args.operator_audit_reference,
            human_reason=args.human_reason,
        )
    elif args.operation == "dry-run":
        value = assess_operator_retirement(
            args.run_dir, json.loads(args.request.read_text(encoding="utf-8")),
        )
    else:
        value = execute_operator_retirement(
            args.run_dir, json.loads(args.request.read_text(encoding="utf-8")),
            committed_at=args.committed_at,
        )
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
