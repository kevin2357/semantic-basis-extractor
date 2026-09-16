"""Provider-free contracts for exact ordinary-v2 cooperative suspension."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from importlib.resources import files
import json
import re
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Mapping


ENVELOPE_SCHEMA = "astrowoof.native_supervision_invocation.v1"
REQUEST_SCHEMA = "astrowoof.native_suspension_request.v1"
RESULT_SCHEMA = "astrowoof.native_suspension_result.v1"
RECEIPT_SCHEMA = "astrowoof.native_suspension_receipt.v1"
COMMAND_RESULT_SCHEMA = "astrowoof.native_suspension_command_result.v1"
FIXTURE_BUNDLE_SCHEMA = "astrowoof.native_suspension_fixture_bundle.v1"

COMMAND_KINDS = frozenset({
    "external_authority_v2_dispatch", "provider_reconciliation",
})
OUTCOMES = frozenset({
    "suspended_checkpointed", "suspended_quiescent_no_checkpoint_change",
    "suspension_deferred", "suspension_refused",
    "provider_boundary_ambiguous", "checkpoint_publication_ambiguous",
})
PROVIDER_BOUNDARIES = frozenset({
    "not_entered", "known_provider_identity",
    "completed_provider_evidence", "entry_or_result_ambiguous",
})
LOCAL_POSTURES = frozenset({
    "none", "durable_pending", "completed_unadopted",
    "adopted_checkpointed", "ambiguous",
})
CONTINUATION_MODES = frozenset({
    "continue_to_named_safe_point", "exit_after_result_publication",
    "await_separate_api_action",
})
SAFE_POINTS = frozenset({
    "dispatch_after_intent_checkpoint", "dispatch_before_provider_post",
    "dispatch_after_provider_return", "dispatch_after_identity_checkpoint",
    "reconciliation_before_provider_get",
    "reconciliation_after_response_checkpoint",
    "reconciliation_before_local_adoption",
    "reconciliation_after_adoption_checkpoint",
    "reconciliation_before_result_publication",
})
CUSTODY_CLASSES = frozenset({
    "none", "provider_pending", "completed_unadopted", "provider_ambiguous",
    "providerless_authority", "terminally_accounted",
})

_SHA = re.compile(r"^[0-9a-f]{64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_ACTION_ID = re.compile(r"^paid_[0-9a-f]{24}$")
_RESULT_ID = re.compile(r"^nsusp_[0-9a-f]{24}$")
_RECEIPT_ID = re.compile(r"^nsuspr_[0-9a-f]{24}$")

_ENVELOPE_KEYS = frozenset({
    "schema_version", "supervision_invocation_id", "launch_generation",
    "api_run_id", "job_id", "attempt_id", "lease_id",
    "lease_token_sha256", "native_run_id", "worker_boot_id", "command_kind",
    "command_sha256", "executable_workspace_root",
    "executable_workspace_root_sha256", "control_root", "control_root_sha256",
    "created_at", "launch_not_after", "grace_deadline",
    "supervision_capability_id", "supervision_capability_sha256",
    "envelope_sha256",
})
_REQUEST_KEYS = frozenset({
    "schema_version", "operation", "request_id", "idempotency_key",
    "supervision_invocation_id", "launch_generation", "envelope_sha256",
    "supervision_capability_id", "supervision_capability_sha256",
    "force_fence_id", "force_fence_sha256", "api_run_id", "job_id",
    "attempt_id", "lease_id", "native_run_id", "command_kind",
    "command_sha256", "executable_workspace_root_sha256",
    "control_root_sha256", "admission_checkpoint_basis_sha256", "actor_id",
    "reason_code", "environment", "emergency_containment_confirmed",
    "requested_at", "expires_at", "grace_deadline", "request_sha256",
})
_CHECKPOINT_KEYS = frozenset({
    "state_revision", "snapshot_sha256", "checkpoint_basis_sha256",
    "predecessor_checkpoint_basis_sha256",
})
_ACTION_KEYS = frozenset({
    "ordinal", "action_id", "binding_sha256", "native_action_state",
    "provider_operation_id", "custody_class",
})
_RESULT_KEYS = frozenset({
    "schema_version", "result_id", "result_sha256", "request_id",
    "request_sha256", "supervision_invocation_id", "envelope_sha256",
    "supervision_capability_id", "supervision_capability_sha256",
    "force_fence_id", "force_fence_sha256",
    "native_publication_invocation_id", "native_run_id",
    "logical_workspace_root_sha256", "command_kind", "safe_point",
    "observed_at", "admission_checkpoint_basis_sha256",
    "observed_checkpoint", "post_publication_checkpoint", "provider_boundary",
    "local_work_posture", "actions", "ordinary_result_preceded_observation",
    "outcome", "reason_code", "continuation_mode", "next_safe_point",
    "continuation_deadline",
})
_RECEIPT_KEYS = frozenset({
    "schema_version", "receipt_id", "receipt_sha256",
    "supervision_invocation_id", "native_run_id", "result_id",
    "result_sha256", "request_id", "request_sha256",
    "supervision_capability_id", "supervision_capability_sha256",
    "force_fence_id", "force_fence_sha256", "checkpoint_basis_sha256",
    "snapshot_sha256", "published_at",
})
_COMMAND_KEYS = frozenset({
    "schema_version", "command_result_sha256", "outcome", "exit_code",
    "supervision_invocation_id", "supervision_capability_id",
    "supervision_capability_sha256", "force_fence_id", "force_fence_sha256",
    "native_publication_invocation_id",
    "result_id", "result_sha256", "receipt_id", "receipt_sha256",
    "checkpoint_basis_sha256",
})


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    return hashlib.sha256(_canonical({
        key: item for key, item in value.items() if key != field
    })).hexdigest()


def _digest_excluding(value: Mapping[str, Any], fields: set[str]) -> str:
    return hashlib.sha256(_canonical({
        key: item for key, item in value.items() if key not in fields
    })).hexdigest()


def _closed(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} fields are not exact")
    return value


def _sha(value: object, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise ValueError(f"{label} is not a canonical SHA-256")
    return value


def _identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _SAFE_ID.fullmatch(value) is None:
        raise ValueError(f"{label} is invalid")
    return value


def _instant(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} is not a canonical UTC instant")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{label} is not a canonical UTC instant") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValueError(f"{label} is not UTC")
    return parsed


def _absolute_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError(f"{label} is invalid")
    path = PureWindowsPath(value) if re.match(r"^[A-Za-z]:[\\/]", value) else PurePosixPath(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be canonical and absolute")
    return value


def _path_is_within(child: str, parent: str) -> bool:
    windows = bool(re.match(r"^[A-Za-z]:[\\/]", child + parent))
    cls = PureWindowsPath if windows else PurePosixPath
    try:
        cls(child).relative_to(cls(parent))
        return True
    except ValueError:
        return False


def read_native_suspension_contract_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "native-cooperative-suspension-contracts.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def read_native_suspension_fixture_bundle() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.fixtures").joinpath(
        "native-suspension", "native-suspension-fixtures.v1.json"
    )
    return validate_suspension_fixture_bundle(
        json.loads(path.read_text(encoding="utf-8"))
    )


def validate_supervision_invocation(value: object) -> dict[str, Any]:
    doc = _closed(value, _ENVELOPE_KEYS, "Supervision invocation")
    if doc["schema_version"] != ENVELOPE_SCHEMA:
        raise ValueError("Unsupported supervision invocation schema")
    for field in (
        "supervision_invocation_id", "api_run_id", "job_id", "attempt_id",
        "lease_id", "native_run_id", "worker_boot_id",
        "supervision_capability_id",
    ):
        _identifier(doc[field], field)
    if isinstance(doc["launch_generation"], bool) or not isinstance(
        doc["launch_generation"], int
    ) or doc["launch_generation"] < 1:
        raise ValueError("launch_generation is invalid")
    if doc["command_kind"] not in COMMAND_KINDS:
        raise ValueError("Unsupported supervision command kind")
    for field in (
        "lease_token_sha256", "command_sha256",
        "executable_workspace_root_sha256", "control_root_sha256",
        "supervision_capability_sha256",
    ):
        _sha(doc[field], field)
    executable = _absolute_path(doc["executable_workspace_root"], "executable root")
    control = _absolute_path(doc["control_root"], "control root")
    if _path_is_within(control, executable) or _path_is_within(executable, control):
        raise ValueError("Control and executable roots are not disjoint")
    if hashlib.sha256(executable.encode("utf-8")).hexdigest() != doc[
        "executable_workspace_root_sha256"
    ] or hashlib.sha256(control.encode("utf-8")).hexdigest() != doc["control_root_sha256"]:
        raise ValueError("Supervision root identity digest mismatch")
    created = _instant(doc["created_at"], "created_at")
    launch = _instant(doc["launch_not_after"], "launch_not_after")
    grace = _instant(doc["grace_deadline"], "grace_deadline")
    if not created < launch <= grace:
        raise ValueError("Supervision time ordering is invalid")
    if doc["envelope_sha256"] != _digest_without(doc, "envelope_sha256"):
        raise ValueError("Supervision invocation digest mismatch")
    return deepcopy(doc)


def validate_suspension_request(
    value: object, *, envelope: Mapping[str, Any], observed_at: str | None = None,
) -> dict[str, Any]:
    doc = _closed(value, _REQUEST_KEYS, "Suspension request")
    env = validate_supervision_invocation(envelope)
    if doc["schema_version"] != REQUEST_SCHEMA or doc["operation"] != "cooperative_suspend":
        raise ValueError("Unsupported suspension request")
    for field in (
        "request_id", "idempotency_key", "actor_id", "reason_code",
        "environment", "force_fence_id",
    ):
        _identifier(doc[field], field)
    repeated = (
        "supervision_invocation_id", "launch_generation", "envelope_sha256",
        "supervision_capability_id", "supervision_capability_sha256",
        "api_run_id", "job_id",
        "attempt_id", "lease_id", "native_run_id", "command_kind",
        "command_sha256", "executable_workspace_root_sha256",
        "control_root_sha256", "grace_deadline",
    )
    if any(doc[field] != env[field] for field in repeated):
        raise ValueError("Suspension request does not join supervision invocation")
    _sha(doc["force_fence_sha256"], "force fence")
    _sha(doc["admission_checkpoint_basis_sha256"], "admission checkpoint")
    if doc["emergency_containment_confirmed"] is not True:
        raise ValueError("Emergency containment confirmation is required")
    requested = _instant(doc["requested_at"], "requested_at")
    expires = _instant(doc["expires_at"], "expires_at")
    grace = _instant(doc["grace_deadline"], "grace_deadline")
    if not requested < expires <= grace:
        raise ValueError("Suspension request time ordering is invalid")
    if observed_at is not None and _instant(observed_at, "observed_at") > expires:
        raise ValueError("Suspension request is expired")
    if doc["request_sha256"] != _digest_without(doc, "request_sha256"):
        raise ValueError("Suspension request digest mismatch")
    return deepcopy(doc)


def classify_suspension_request_replay(
    first: Mapping[str, Any], later: Mapping[str, Any], *, envelope: Mapping[str, Any],
) -> str:
    first_doc = validate_suspension_request(first, envelope=envelope)
    later_doc = validate_suspension_request(later, envelope=envelope)
    if first_doc == later_doc:
        return "exact_replay"
    if first_doc["supervision_invocation_id"] == later_doc["supervision_invocation_id"]:
        return "request_conflict"
    return "unrelated_invocation"


def _checkpoint(value: object, label: str) -> dict[str, Any]:
    doc = _closed(value, _CHECKPOINT_KEYS, label)
    if isinstance(doc["state_revision"], bool) or not isinstance(
        doc["state_revision"], int
    ) or doc["state_revision"] < 0:
        raise ValueError(f"{label} revision is invalid")
    for field in ("snapshot_sha256", "checkpoint_basis_sha256"):
        _sha(doc[field], f"{label} {field}")
    _sha(doc["predecessor_checkpoint_basis_sha256"], f"{label} predecessor", nullable=True)
    return doc


def _action(value: object, ordinal: int) -> dict[str, Any]:
    doc = _closed(value, _ACTION_KEYS, "Suspension action")
    if doc["ordinal"] != ordinal:
        raise ValueError("Suspension action ordering is invalid")
    if not isinstance(doc["action_id"], str) or _ACTION_ID.fullmatch(doc["action_id"]) is None:
        raise ValueError("Suspension action ID is invalid")
    _sha(doc["binding_sha256"], "Suspension action binding")
    _identifier(doc["native_action_state"], "native_action_state")
    if doc["provider_operation_id"] is not None:
        _identifier(doc["provider_operation_id"], "provider_operation_id")
    if doc["custody_class"] not in CUSTODY_CLASSES:
        raise ValueError("Suspension custody class is invalid")
    if doc["custody_class"] in {"provider_pending", "completed_unadopted"} and doc[
        "provider_operation_id"
    ] is None:
        raise ValueError("Provider custody lacks durable provider identity")
    return doc


def validate_suspension_result(
    value: object, *, request: Mapping[str, Any], envelope: Mapping[str, Any],
) -> dict[str, Any]:
    doc = _closed(value, _RESULT_KEYS, "Suspension result")
    req = validate_suspension_request(request, envelope=envelope, observed_at=doc["observed_at"])
    env = validate_supervision_invocation(envelope)
    if doc["schema_version"] != RESULT_SCHEMA:
        raise ValueError("Unsupported suspension result schema")
    if not isinstance(doc["result_id"], str) or _RESULT_ID.fullmatch(doc["result_id"]) is None:
        raise ValueError("Suspension result ID is invalid")
    for field in (
        "native_publication_invocation_id", "native_run_id", "reason_code",
    ):
        _identifier(doc[field], field)
    for field in ("logical_workspace_root_sha256", "admission_checkpoint_basis_sha256"):
        _sha(doc[field], field)
    joins = {
        "request_id": req["request_id"], "request_sha256": req["request_sha256"],
        "supervision_invocation_id": env["supervision_invocation_id"],
        "envelope_sha256": env["envelope_sha256"],
        "supervision_capability_id": env["supervision_capability_id"],
        "supervision_capability_sha256": env["supervision_capability_sha256"],
        "force_fence_id": req["force_fence_id"],
        "force_fence_sha256": req["force_fence_sha256"],
        "native_run_id": env["native_run_id"], "command_kind": env["command_kind"],
        "admission_checkpoint_basis_sha256": req["admission_checkpoint_basis_sha256"],
    }
    if any(doc[field] != expected for field, expected in joins.items()):
        raise ValueError("Suspension result identity join failed")
    if doc["safe_point"] not in SAFE_POINTS or doc["outcome"] not in OUTCOMES:
        raise ValueError("Suspension result outcome or safe point is invalid")
    observed = _checkpoint(doc["observed_checkpoint"], "Observed checkpoint")
    post = _checkpoint(doc["post_publication_checkpoint"], "Post-publication checkpoint")
    anchor = req["admission_checkpoint_basis_sha256"]
    if observed["checkpoint_basis_sha256"] != anchor and observed[
        "predecessor_checkpoint_basis_sha256"
    ] != anchor:
        raise ValueError("Observed checkpoint is not the admission anchor or contiguous successor")
    if post["state_revision"] < observed["state_revision"]:
        raise ValueError("Post-publication checkpoint regresses")
    if doc["provider_boundary"] not in PROVIDER_BOUNDARIES or doc[
        "local_work_posture"
    ] not in LOCAL_POSTURES:
        raise ValueError("Suspension custody posture is invalid")
    actions = doc["actions"]
    if not isinstance(actions, list) or len(actions) > 128:
        raise ValueError("Suspension action inventory is invalid")
    for index, action in enumerate(actions, 1):
        _action(action, index)
    if len({item["action_id"] for item in actions}) != len(actions):
        raise ValueError("Suspension action IDs are duplicated")
    if doc["ordinary_result_preceded_observation"] is not False:
        raise ValueError("A prior ordinary result suppresses suspension publication")
    if doc["outcome"] == "suspended_checkpointed" and post["state_revision"] <= observed[
        "state_revision"
    ]:
        raise ValueError("Checkpointed suspension did not advance publication state")
    if doc["outcome"] == "suspended_quiescent_no_checkpoint_change" and post != observed:
        raise ValueError("Quiescent suspension changed checkpoint identity")
    if doc["outcome"] == "provider_boundary_ambiguous" and doc[
        "provider_boundary"
    ] != "entry_or_result_ambiguous":
        raise ValueError("Provider ambiguity outcome lacks ambiguous boundary")
    mode = doc["continuation_mode"]
    if doc["outcome"] == "suspension_deferred":
        if mode not in CONTINUATION_MODES:
            raise ValueError("Deferred suspension lacks continuation mode")
        if mode == "continue_to_named_safe_point":
            if doc["next_safe_point"] not in SAFE_POINTS or doc["continuation_deadline"] is None:
                raise ValueError("Deferred continuation safe point is incomplete")
            if _instant(doc["continuation_deadline"], "continuation_deadline") > _instant(
                req["grace_deadline"], "grace_deadline"
            ):
                raise ValueError("Deferred continuation exceeds grace deadline")
        elif doc["next_safe_point"] is not None or doc["continuation_deadline"] is not None:
            raise ValueError("Non-continuing deferred result carries continuation fields")
    elif any(doc[field] is not None for field in (
        "continuation_mode", "next_safe_point", "continuation_deadline",
    )):
        raise ValueError("Non-deferred suspension carries continuation fields")
    if doc["result_sha256"] != _digest_excluding(doc, {"result_id", "result_sha256"}):
        raise ValueError("Suspension result digest mismatch")
    if doc["result_id"] != "nsusp_" + doc["result_sha256"][:24]:
        raise ValueError("Suspension result ID does not bind its digest")
    return deepcopy(doc)


def validate_suspension_receipt(
    value: object, *, result: Mapping[str, Any], request: Mapping[str, Any],
    envelope: Mapping[str, Any],
) -> dict[str, Any]:
    doc = _closed(value, _RECEIPT_KEYS, "Suspension receipt")
    res = validate_suspension_result(result, request=request, envelope=envelope)
    if doc["schema_version"] != RECEIPT_SCHEMA:
        raise ValueError("Unsupported suspension receipt schema")
    joins = {
        "supervision_invocation_id": res["supervision_invocation_id"],
        "native_run_id": res["native_run_id"], "result_id": res["result_id"],
        "result_sha256": res["result_sha256"], "request_id": res["request_id"],
        "request_sha256": res["request_sha256"],
        "supervision_capability_id": res["supervision_capability_id"],
        "supervision_capability_sha256": res["supervision_capability_sha256"],
        "force_fence_id": res["force_fence_id"],
        "force_fence_sha256": res["force_fence_sha256"],
        "checkpoint_basis_sha256": res["post_publication_checkpoint"]["checkpoint_basis_sha256"],
        "snapshot_sha256": res["post_publication_checkpoint"]["snapshot_sha256"],
    }
    if any(doc[field] != expected for field, expected in joins.items()):
        raise ValueError("Suspension receipt does not join result")
    _instant(doc["published_at"], "published_at")
    if doc["receipt_sha256"] != _digest_excluding(doc, {"receipt_id", "receipt_sha256"}):
        raise ValueError("Suspension receipt digest mismatch")
    if doc["receipt_id"] != "nsuspr_" + doc["receipt_sha256"][:24]:
        raise ValueError("Suspension receipt ID does not bind its digest")
    return deepcopy(doc)


def validate_suspension_command_result(
    value: object, *, result: Mapping[str, Any], receipt: Mapping[str, Any],
    request: Mapping[str, Any], envelope: Mapping[str, Any],
) -> dict[str, Any]:
    doc = _closed(value, _COMMAND_KEYS, "Suspension command result")
    res = validate_suspension_result(result, request=request, envelope=envelope)
    rec = validate_suspension_receipt(
        receipt, result=res, request=request, envelope=envelope,
    )
    if doc["schema_version"] != COMMAND_RESULT_SCHEMA:
        raise ValueError("Unsupported suspension command result schema")
    joins = {
        "outcome": res["outcome"], "supervision_invocation_id": res["supervision_invocation_id"],
        "supervision_capability_id": res["supervision_capability_id"],
        "supervision_capability_sha256": res["supervision_capability_sha256"],
        "force_fence_id": res["force_fence_id"],
        "force_fence_sha256": res["force_fence_sha256"],
        "native_publication_invocation_id": res["native_publication_invocation_id"],
        "result_id": res["result_id"], "result_sha256": res["result_sha256"],
        "receipt_id": rec["receipt_id"], "receipt_sha256": rec["receipt_sha256"],
        "checkpoint_basis_sha256": rec["checkpoint_basis_sha256"],
    }
    if any(doc[field] != expected for field, expected in joins.items()):
        raise ValueError("Suspension command result identity join failed")
    if isinstance(doc["exit_code"], bool) or not isinstance(doc["exit_code"], int) or doc[
        "exit_code"
    ] not in {0, 2}:
        raise ValueError("Suspension command exit code is invalid")
    if doc["command_result_sha256"] != _digest_without(doc, "command_result_sha256"):
        raise ValueError("Suspension command result digest mismatch")
    return deepcopy(doc)


def validate_suspension_fixture_bundle(value: object) -> dict[str, Any]:
    keys = frozenset({"schema_version", "bundle_sha256", "cases"})
    doc = _closed(value, keys, "Suspension fixture bundle")
    if doc["schema_version"] != FIXTURE_BUNDLE_SCHEMA or not isinstance(doc["cases"], list):
        raise ValueError("Suspension fixture bundle is invalid")
    seen_requests: set[tuple[str, str]] = set()
    seen_results: set[str] = set()
    seen_receipts: set[str] = set()
    for case in doc["cases"]:
        case = _closed(case, frozenset({
            "name", "envelope", "request", "result", "receipt", "command_result",
        }), "Suspension fixture case")
        _identifier(case["name"], "case name")
        env = validate_supervision_invocation(case["envelope"])
        req = validate_suspension_request(case["request"], envelope=env)
        res = validate_suspension_result(case["result"], request=req, envelope=env)
        rec = validate_suspension_receipt(
            case["receipt"], result=res, request=req, envelope=env,
        )
        validate_suspension_command_result(
            case["command_result"], result=res, receipt=rec,
            request=req, envelope=env,
        )
        request_identity = (req["request_id"], req["request_sha256"])
        if request_identity in seen_requests:
            raise ValueError("Suspension bundle request identity is duplicated")
        if res["result_id"] in seen_results or rec["receipt_id"] in seen_receipts:
            raise ValueError("Suspension bundle transport identity is duplicated")
        seen_requests.add(request_identity)
        seen_results.add(res["result_id"])
        seen_receipts.add(rec["receipt_id"])
    if doc["bundle_sha256"] != _digest_without(doc, "bundle_sha256"):
        raise ValueError("Suspension fixture bundle digest mismatch")
    return deepcopy(doc)


def seal_document(body: Mapping[str, Any], digest_field: str) -> dict[str, Any]:
    """Seal a fully populated provider-free contract body."""
    value = deepcopy(dict(body))
    value[digest_field] = _digest_without(value, digest_field)
    return value
