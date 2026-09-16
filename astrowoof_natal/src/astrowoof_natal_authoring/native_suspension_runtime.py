"""Serialized, provider-free observation and publication for cooperative suspension."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from .closure import (
    SNAPSHOT_NAME,
    load_json,
    normalized_path,
    persist_state,
    sha256_file,
    validate_workspace_snapshot,
    write_json_atomic,
    write_workspace_snapshot,
)
from .native_suspension_contracts import (
    COMMAND_RESULT_SCHEMA,
    RECEIPT_SCHEMA,
    RESULT_SCHEMA,
    seal_document,
    validate_supervision_invocation,
    validate_suspension_command_result,
    validate_suspension_receipt,
    validate_suspension_request,
    validate_suspension_result,
)
from .native_transitions import checkpoint_basis, read_native_transition_result


REQUEST_NAME = "native-suspension-request.v1.json"
RESULT_ROOT = "native-suspension-results"
INDEX_NAME = "native-suspension-index.v1.json"


class CooperativeSuspensionPublished(RuntimeError):
    """Internal control-flow signal carrying one exact published handoff."""

    def __init__(self, publication: dict[str, Any]):
        super().__init__("cooperative suspension published")
        self.publication = publication


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _write_bytes_atomic(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _read_control_documents(
    run_dir: Path, envelope_path: Path, control_root: Path, observed_at: str,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    root = run_dir.resolve()
    control = control_root.resolve()
    envelope_file = envelope_path.resolve()
    if envelope_path.is_symlink() or control_root.is_symlink():
        raise ValueError("Suspension control paths cannot be links")
    if envelope_file.parent != control or not envelope_file.is_file():
        raise ValueError("Supervision envelope is not at its canonical control root")
    envelope = validate_supervision_invocation(load_json(envelope_file))
    if normalized_path(root) != envelope["executable_workspace_root"]:
        raise ValueError("Executable workspace root does not join supervision envelope")
    if normalized_path(control) != envelope["control_root"]:
        raise ValueError("Control root does not join supervision envelope")
    members = sorted(item.name for item in control.iterdir())
    allowed = {envelope_file.name, REQUEST_NAME}
    if any(name not in allowed for name in members):
        raise ValueError("Suspension control root contains unexpected members")
    request_path = control / REQUEST_NAME
    if not request_path.exists():
        return None
    if request_path.is_symlink() or not request_path.is_file():
        raise ValueError("Suspension request path is not a regular file")
    before = request_path.stat()
    request = validate_suspension_request(
        load_json(request_path), envelope=envelope, observed_at=observed_at,
    )
    after = request_path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("Suspension request identity changed while reading")
    return envelope, request


def _action_inventory(state: dict[str, Any], run_dir: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for ordinal, action in enumerate(
        (state.get("spend_ledger") or {}).get("actions") or [], 1
    ):
        provider = action.get("provider") or {}
        provider_id = provider.get("id")
        action_id = action.get("action_id")
        binding = action.get("binding") or {}
        response = run_dir / "lifecycle" / "provider-reconciliation" / f"{action_id}.response.json"
        if action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION":
            custody = "provider_ambiguous"
        elif response.is_file() and action.get("state") != "REPORTED":
            custody = "completed_unadopted"
        elif provider_id and action.get("state") != "REPORTED":
            custody = "provider_pending"
        elif action.get("state") == "REPORTED":
            custody = "terminally_accounted"
        elif action.get("state") in {"PREPARED", "SUBMITTING"}:
            custody = "providerless_authority"
        else:
            custody = "none"
        values.append({
            "ordinal": ordinal,
            "action_id": action_id,
            "binding_sha256": binding.get("binding_sha256") or _sha(binding),
            "native_action_state": str(action.get("state") or "UNKNOWN"),
            "provider_operation_id": provider_id,
            "custody_class": custody,
        })
    return values


def _ordinary_result_precedes(run_dir: Path, observed_at: str) -> bool:
    index = run_dir / "native-result-index.json"
    if not index.is_file():
        return False
    for result_id in load_json(index).get("result_ids") or []:
        try:
            result = read_native_transition_result(run_dir, result_id)["result"]
        except (FileNotFoundError, KeyError, TypeError, ValueError):
            continue
        if (
            result.get("outcome") in {"delivery_complete", "review_required"}
            and str(result.get("published_at") or "") <= observed_at
        ):
            return True
    return False


class NativeSuspensionControlObserver:
    """Observe one request at coordinator-owned writer-held safe points."""

    def __init__(
        self, *, envelope_path: Path, control_root: Path, observed_at: str,
        failure_injector: Any = None,
    ):
        self.envelope_path = Path(envelope_path)
        self.control_root = Path(control_root)
        self.observed_at = observed_at
        self.failure_injector = failure_injector

    def __call__(
        self, safe_point: str, run_dir: Path, state: dict[str, Any],
        predecessor_checkpoint_basis_sha256: str | None,
    ) -> None:
        documents = _read_control_documents(
            run_dir, self.envelope_path, self.control_root, self.observed_at,
        )
        if documents is None:
            return
        envelope, request = documents
        if envelope["command_kind"] == "external_authority_v2_dispatch" and not safe_point.startswith("dispatch_"):
            raise ValueError("Suspension request command does not join safe point")
        if envelope["command_kind"] == "provider_reconciliation" and not safe_point.startswith("reconciliation_"):
            raise ValueError("Suspension request command does not join safe point")
        if state.get("run_id") != envelope["native_run_id"]:
            raise ValueError("Suspension native run identity mismatch")
        validate_workspace_snapshot(run_dir, state)
        if _ordinary_result_precedes(run_dir, self.observed_at):
            return

        prior_records = [
            item for item in (state.get("native_suspension_records") or [])
            if item.get("supervision_invocation_id")
            == request["supervision_invocation_id"]
        ]
        matching = [
            item for item in prior_records
            if item.get("request_id") == request["request_id"]
            and item.get("request_sha256") == request["request_sha256"]
        ]
        recovery_record = None
        if matching:
            index = load_json(run_dir / INDEX_NAME) if (run_dir / INDEX_NAME).is_file() else {
                "result_ids": [],
            }
            matches = []
            for result_id in index.get("result_ids") or []:
                candidate_result = load_json(
                    run_dir / RESULT_ROOT / f"{result_id}.json"
                )
                if (
                    candidate_result.get("request_id") == request["request_id"]
                    and candidate_result.get("request_sha256")
                    == request["request_sha256"]
                ):
                    matches.append(result_id)
            if len(matches) > 1:
                raise ValueError("Suspension replay does not have one canonical result")
            if matches:
                raise CooperativeSuspensionPublished(read_native_suspension_publication(
                    run_dir, matches[0], envelope=envelope, request=request,
                ))
            recovery_record = matching[0]
        if prior_records and recovery_record is None:
            raise ValueError("A distinct suspension request conflicts with this invocation")

        anchor = request["admission_checkpoint_basis_sha256"]
        if recovery_record is None:
            observed_basis = checkpoint_basis(
                run_dir, int(state.get("state_revision") or 0)
            )
            if observed_basis["checkpoint_basis_sha256"] != anchor and predecessor_checkpoint_basis_sha256 != anchor:
                raise ValueError("Suspension admission checkpoint is not the observed predecessor")
            observed_checkpoint = {
                "state_revision": int(state.get("state_revision") or 0),
                "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
                "checkpoint_basis_sha256": observed_basis["checkpoint_basis_sha256"],
                "predecessor_checkpoint_basis_sha256": predecessor_checkpoint_basis_sha256,
            }
            publication_id = "nsinv_" + request["request_sha256"][:24]
            candidate = deepcopy(state)
            candidate.setdefault("native_suspension_records", []).append({
                "schema_version": "astrowoof.native_suspension_record.v1",
                "request_id": request["request_id"],
                "request_sha256": request["request_sha256"],
                "supervision_invocation_id": request["supervision_invocation_id"],
                "native_publication_invocation_id": publication_id,
                "safe_point": safe_point,
                "observed_at": self.observed_at,
                "observed_checkpoint": observed_checkpoint,
            })
            persist_state(run_dir / "run.json", candidate)
            write_workspace_snapshot(run_dir)
            validate_workspace_snapshot(run_dir, candidate)
            if self.failure_injector is not None:
                self.failure_injector("after_observation_checkpoint")
        else:
            candidate = deepcopy(state)
            observed_checkpoint = deepcopy(recovery_record["observed_checkpoint"])
            publication_id = recovery_record["native_publication_invocation_id"]
            safe_point = recovery_record["safe_point"]
        publication_observed_at = (
            recovery_record["observed_at"]
            if recovery_record is not None else self.observed_at
        )
        post_basis = checkpoint_basis(run_dir, int(candidate["state_revision"]))
        post_checkpoint = {
            "state_revision": int(candidate["state_revision"]),
            "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
            "checkpoint_basis_sha256": post_basis["checkpoint_basis_sha256"],
            "predecessor_checkpoint_basis_sha256": observed_checkpoint[
                "checkpoint_basis_sha256"
            ],
        }
        actions = _action_inventory(candidate, run_dir)
        custody = {item["custody_class"] for item in actions}
        provider_boundary = (
            "entry_or_result_ambiguous" if "provider_ambiguous" in custody
            else "completed_provider_evidence" if "completed_unadopted" in custody
            else "known_provider_identity" if "provider_pending" in custody
            else "not_entered"
        )
        local_posture = (
            "ambiguous" if "provider_ambiguous" in custody
            else "completed_unadopted" if "completed_unadopted" in custody
            else "durable_pending" if "providerless_authority" in custody
            else "none"
        )
        result = {
            "schema_version": RESULT_SCHEMA, "result_id": "", "result_sha256": "",
            "request_id": request["request_id"], "request_sha256": request["request_sha256"],
            "supervision_invocation_id": envelope["supervision_invocation_id"],
            "envelope_sha256": envelope["envelope_sha256"],
            "supervision_capability_id": envelope["supervision_capability_id"],
            "supervision_capability_sha256": envelope[
                "supervision_capability_sha256"
            ],
            "force_fence_id": request["force_fence_id"],
            "force_fence_sha256": request["force_fence_sha256"],
            "native_publication_invocation_id": publication_id,
            "native_run_id": envelope["native_run_id"],
            "logical_workspace_root_sha256": hashlib.sha256(normalized_path(run_dir).encode()).hexdigest(),
            "command_kind": envelope["command_kind"], "safe_point": safe_point,
            "observed_at": publication_observed_at,
            "admission_checkpoint_basis_sha256": anchor,
            "observed_checkpoint": observed_checkpoint,
            "post_publication_checkpoint": post_checkpoint,
            "provider_boundary": provider_boundary, "local_work_posture": local_posture,
            "actions": actions, "ordinary_result_preceded_observation": False,
            "outcome": (
                "provider_boundary_ambiguous"
                if provider_boundary == "entry_or_result_ambiguous"
                else "suspended_checkpointed"
            ),
            "reason_code": (
                "provider_create_entered_without_durable_identity"
                if provider_boundary == "entry_or_result_ambiguous"
                else "cooperative_request_observed"
            ),
            "continuation_mode": None, "next_safe_point": None,
            "continuation_deadline": None,
        }
        result["result_sha256"] = _sha({
            key: value for key, value in result.items()
            if key not in {"result_id", "result_sha256"}
        })
        result["result_id"] = "nsusp_" + result["result_sha256"][:24]
        validate_suspension_result(result, request=request, envelope=envelope)
        result_dir = run_dir / RESULT_ROOT
        write_json_atomic(result_dir / f"{result['result_id']}.json", result)
        index_path = run_dir / INDEX_NAME
        index = load_json(index_path) if index_path.is_file() else {
            "schema_version": "astrowoof.native_suspension_index.v1", "result_ids": [],
        }
        index["result_ids"].append(result["result_id"])
        write_json_atomic(index_path, index)
        if self.failure_injector is not None:
            self.failure_injector("after_result_indexed")
        write_workspace_snapshot(run_dir)
        validate_workspace_snapshot(run_dir, candidate)
        receipt = {
            "schema_version": RECEIPT_SCHEMA, "receipt_id": "", "receipt_sha256": "",
            "supervision_invocation_id": envelope["supervision_invocation_id"],
            "native_run_id": envelope["native_run_id"],
            "result_id": result["result_id"], "result_sha256": result["result_sha256"],
            "request_id": request["request_id"], "request_sha256": request["request_sha256"],
            "supervision_capability_id": result["supervision_capability_id"],
            "supervision_capability_sha256": result[
                "supervision_capability_sha256"
            ],
            "force_fence_id": result["force_fence_id"],
            "force_fence_sha256": result["force_fence_sha256"],
            "checkpoint_basis_sha256": post_basis["checkpoint_basis_sha256"],
            "snapshot_sha256": sha256_file(run_dir / SNAPSHOT_NAME),
            "published_at": publication_observed_at,
        }
        receipt["receipt_sha256"] = _sha({
            key: value for key, value in receipt.items()
            if key not in {"receipt_id", "receipt_sha256"}
        })
        receipt["receipt_id"] = "nsuspr_" + receipt["receipt_sha256"][:24]
        validate_suspension_receipt(receipt, result=result, request=request, envelope=envelope)
        write_json_atomic(
            run_dir / "native-publication-receipts" / f"{result['result_id']}.json",
            receipt,
        )
        retained = run_dir / "native-publication-receipts"
        _write_bytes_atomic(
            retained / f"{result['result_id']}.workspace-snapshot.json",
            (run_dir / SNAPSHOT_NAME).read_bytes(),
        )
        write_json_atomic(
            retained / f"{result['result_id']}.checkpoint-basis.json",
            post_basis,
        )
        if self.failure_injector is not None:
            self.failure_injector("after_receipt_published")
        # The request observation was already durably checkpointed. The
        # immutable result/index is the canonical request-to-result replay map;
        # do not mutate state again after result identity exists.
        command = seal_document({
            "schema_version": COMMAND_RESULT_SCHEMA, "command_result_sha256": "",
            "outcome": result["outcome"], "exit_code": 0,
            "supervision_invocation_id": envelope["supervision_invocation_id"],
            "supervision_capability_id": result["supervision_capability_id"],
            "supervision_capability_sha256": result[
                "supervision_capability_sha256"
            ],
            "force_fence_id": result["force_fence_id"],
            "force_fence_sha256": result["force_fence_sha256"],
            "native_publication_invocation_id": publication_id,
            "result_id": result["result_id"], "result_sha256": result["result_sha256"],
            "receipt_id": receipt["receipt_id"], "receipt_sha256": receipt["receipt_sha256"],
            "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
        }, "command_result_sha256")
        validate_suspension_command_result(
            command, result=result, receipt=receipt, request=request,
            envelope=envelope,
        )
        raise CooperativeSuspensionPublished({
            "envelope": envelope, "request": request, "result": result,
            "receipt": receipt, "command_result": command,
        })


def read_native_suspension_publication(
    run_dir: Path, result_id: str, *, envelope: dict[str, Any], request: dict[str, Any],
) -> dict[str, Any]:
    result = load_json(Path(run_dir) / RESULT_ROOT / f"{result_id}.json")
    receipt = load_json(
        Path(run_dir) / "native-publication-receipts" / f"{result_id}.json"
    )
    validate_suspension_result(result, request=request, envelope=envelope)
    validate_suspension_receipt(
        receipt, result=result, request=request, envelope=envelope,
    )
    retained = Path(run_dir) / "native-publication-receipts"
    snapshot = retained / f"{result_id}.workspace-snapshot.json"
    basis_path = retained / f"{result_id}.checkpoint-basis.json"
    if (
        not snapshot.is_file() or not basis_path.is_file()
        or hashlib.sha256(snapshot.read_bytes()).hexdigest()
        != receipt["snapshot_sha256"]
        or load_json(basis_path).get("checkpoint_basis_sha256")
        != receipt["checkpoint_basis_sha256"]
    ):
        raise ValueError("Suspension publication retained evidence is invalid")
    command = seal_document({
        "schema_version": COMMAND_RESULT_SCHEMA, "command_result_sha256": "",
        "outcome": result["outcome"], "exit_code": 0,
        "supervision_invocation_id": result["supervision_invocation_id"],
        "supervision_capability_id": result["supervision_capability_id"],
        "supervision_capability_sha256": result["supervision_capability_sha256"],
        "force_fence_id": result["force_fence_id"],
        "force_fence_sha256": result["force_fence_sha256"],
        "native_publication_invocation_id": result["native_publication_invocation_id"],
        "result_id": result["result_id"], "result_sha256": result["result_sha256"],
        "receipt_id": receipt["receipt_id"], "receipt_sha256": receipt["receipt_sha256"],
        "checkpoint_basis_sha256": receipt["checkpoint_basis_sha256"],
    }, "command_result_sha256")
    return {"envelope": envelope, "request": request, "result": result,
            "receipt": receipt, "command_result": command}
