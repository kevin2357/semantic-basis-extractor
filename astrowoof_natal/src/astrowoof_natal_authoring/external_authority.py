"""Provider-free public readers and validators for external-authority requests."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .initial_wave import InitialWaveError
from .initial_wave_contract import read_initial_wave_authority_inputs
from .resource_access import read_resource_text


REQUEST_SCHEMA = "astrowoof.external_authority_request.v1"
CONTRACT_SCHEMA_RESOURCE = "contracts/external-authority-contracts.v1.schema.json"
SNAPSHOT_FILENAME = "workspace-snapshot.json"
_REQUEST_KEYS = frozenset({
    "schema_version", "external_authority_request_sha256", "run_id",
    "observation", "request_kind", "ordering_semantics", "action_count",
    "ordered_action_ids", "ordered_actions", "initial_wave",
    "provider_create_permitted_after_authorization",
})
_ACTION_KEYS = frozenset({"action_id", "binding", "binding_sha256"})
_BINDING_KEYS = frozenset({
    "run_id", "profile_sha256", "prepared_state_revision", "stage", "route",
    "request_sha256", "model", "service_level", "maximum_output_tokens",
    "commitment_micro_usd", "price_book_version",
})
_OBSERVATION_KEYS = frozenset({
    "operator_state_revision", "snapshot_sha256", "logical_workspace_root",
    "snapshot_complete", "inventory_valid", "observed_at",
    "native_exclusive_access", "writer_race_possible",
})
_WAVE_KEYS = frozenset({
    "wave_id", "wave_sha256", "route_contract", "assignment_sha256",
    "profile_sha256", "member_count", "ordered_member_binding_sha256s",
})


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _require_sha256(value: Any, field: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise InitialWaveError("binding_mismatch", f"{field} is not SHA-256")


def _validate_observation(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != _OBSERVATION_KEYS:
        raise InitialWaveError("unsupported_contract", "Observation fields are not exact")
    try:
        datetime.fromisoformat(str(value["observed_at"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise InitialWaveError(
            "binding_mismatch", "Observation time is invalid"
        ) from exc
    if (
        not isinstance(value["operator_state_revision"], int)
        or isinstance(value["operator_state_revision"], bool)
        or value["operator_state_revision"] < 0
    ):
        raise InitialWaveError("binding_mismatch", "Observation revision is invalid")
    _require_sha256(value["snapshot_sha256"], "snapshot_sha256")
    if not isinstance(value["logical_workspace_root"], str) or not value[
        "logical_workspace_root"
    ]:
        raise InitialWaveError("binding_mismatch", "Logical workspace root is invalid")
    if (
        value["snapshot_complete"] is not True
        or value["inventory_valid"] is not True
        or value["writer_race_possible"] is not False
        or value["native_exclusive_access"] not in {"declared", "established"}
        or not isinstance(value["observed_at"], str)
        or not value["observed_at"]
    ):
        raise InitialWaveError("snapshot_invalid", "Request observation is not validated")


def _validate_action(value: Any, *, run_id: str, revision: int) -> None:
    if not isinstance(value, Mapping) or set(value) != _ACTION_KEYS:
        raise InitialWaveError("unsupported_contract", "Request action fields are not exact")
    action_id = value.get("action_id")
    binding = value.get("binding")
    if not isinstance(action_id, str) or not action_id.startswith("paid_") or len(action_id) != 29:
        raise InitialWaveError("binding_mismatch", "Request action ID is invalid")
    if not isinstance(binding, Mapping) or set(binding) != _BINDING_KEYS:
        raise InitialWaveError("unsupported_contract", "Request binding fields are not exact")
    prepared_revision = binding.get("prepared_state_revision")
    if (
        binding.get("run_id") != run_id
        or not isinstance(prepared_revision, int)
        or isinstance(prepared_revision, bool)
        or prepared_revision < 0
        or prepared_revision > revision
    ):
        raise InitialWaveError("binding_mismatch", "Request binding basis is invalid")
    for field in ("profile_sha256", "request_sha256"):
        _require_sha256(binding.get(field), field)
    if value.get("binding_sha256") != _canonical_sha256(binding):
        raise InitialWaveError("digest_mismatch", "Request binding digest is invalid")


def validate_external_authority_request(value: Any) -> dict[str, Any]:
    """Strictly validate one closed request without filesystem or provider access."""
    if not isinstance(value, dict) or set(value) != _REQUEST_KEYS:
        raise InitialWaveError("unsupported_contract", "Authority-request fields are not exact")
    if value.get("schema_version") != REQUEST_SCHEMA:
        raise InitialWaveError("unsupported_contract", "Unsupported authority request")
    if value.get("provider_create_permitted_after_authorization") is not True:
        raise InitialWaveError("binding_mismatch", "Request is not create-capable")
    run_id = value.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise InitialWaveError("binding_mismatch", "Request run ID is invalid")
    observation = value.get("observation")
    _validate_observation(observation)
    actions = value.get("ordered_actions")
    action_ids = value.get("ordered_action_ids")
    count = value.get("action_count")
    if (
        not isinstance(actions, list) or not 1 <= len(actions) <= 32
        or not isinstance(action_ids, list) or count != len(actions)
        or action_ids != [item.get("action_id") if isinstance(item, Mapping) else None
                          for item in actions]
        or len(action_ids) != len(set(action_ids))
    ):
        raise InitialWaveError("member_inventory_mismatch", "Request inventory is invalid")
    for action in actions:
        _validate_action(
            action, run_id=run_id,
            revision=observation["operator_state_revision"],
        )
    kind = value.get("request_kind")
    wave = value.get("initial_wave")
    if kind == "ordinary_action_set":
        if value.get("ordering_semantics") != "lexical_action_id_canonicalization_only" \
                or action_ids != sorted(action_ids) or wave is not None:
            raise InitialWaveError("member_inventory_mismatch", "Ordinary ordering is invalid")
    elif kind == "initial_wave_admission":
        if (
            value.get("ordering_semantics") != "prepared_wave_semantic_member_order"
            or len(actions) != 6 or not isinstance(wave, Mapping)
            or set(wave) != _WAVE_KEYS or wave.get("member_count") != 6
            or wave.get("ordered_member_binding_sha256s") != [
                action["binding_sha256"] for action in actions
            ]
            or wave.get("profile_sha256") != actions[0]["binding"]["profile_sha256"]
        ):
            raise InitialWaveError("member_inventory_mismatch", "Initial-wave join is invalid")
        for field in ("wave_sha256", "assignment_sha256", "profile_sha256"):
            _require_sha256(wave.get(field), field)
    else:
        raise InitialWaveError("unsupported_contract", "Unsupported request kind")
    body = {key: item for key, item in value.items()
            if key != "external_authority_request_sha256"}
    if value.get("external_authority_request_sha256") != _canonical_sha256(body):
        raise InitialWaveError("digest_mismatch", "Authority-request digest is invalid")
    return value


def build_external_authority_request(
    *, run_id: str, observation: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]], initial_wave: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one deterministic request from complete public bindings."""
    ordered = [{
        "action_id": item["action_id"],
        "binding": deepcopy(item["binding"]),
        "binding_sha256": item.get("binding_sha256")
        or _canonical_sha256(item["binding"]),
    } for item in actions]
    if initial_wave is None:
        ordered.sort(key=lambda item: item["action_id"])
        kind = "ordinary_action_set"
        ordering = "lexical_action_id_canonicalization_only"
        wave_context = None
    else:
        kind = "initial_wave_admission"
        ordering = "prepared_wave_semantic_member_order"
        wave_context = deepcopy(dict(initial_wave))
    value = {
        "schema_version": REQUEST_SCHEMA,
        "run_id": run_id,
        "observation": deepcopy(dict(observation)),
        "request_kind": kind,
        "ordering_semantics": ordering,
        "action_count": len(ordered),
        "ordered_action_ids": [item["action_id"] for item in ordered],
        "ordered_actions": ordered,
        "initial_wave": wave_context,
        "provider_create_permitted_after_authorization": True,
    }
    value["external_authority_request_sha256"] = _canonical_sha256(value)
    return validate_external_authority_request(value)


def _snapshot_observation(root: Path, state: Mapping[str, Any]) -> dict[str, Any]:
    from .closure import normalized_path, sha256_file

    observed_at = state.get("updated_at") or state.get("created_at")
    if not isinstance(observed_at, str) or not observed_at:
        raise InitialWaveError(
            "native_state_inconsistent", "Run lacks a snapshot-bound observation time"
        )
    return {
        "operator_state_revision": state.get("state_revision"),
        "snapshot_sha256": sha256_file(root / SNAPSHOT_FILENAME),
        "logical_workspace_root": normalized_path(root),
        "snapshot_complete": True,
        "inventory_valid": True,
        "observed_at": observed_at,
        "native_exclusive_access": "declared",
        "writer_race_possible": False,
    }


def read_external_authority_request(run_dir: Path | str) -> dict[str, Any]:
    """Read one exact request only after complete snapshot validation."""
    from .closure import load_json, validate_workspace_snapshot

    root = Path(run_dir).resolve()
    run_json = root / "run.json"
    if not run_json.is_file():
        raise InitialWaveError("snapshot_invalid", "Run state is missing")
    state = load_json(run_json)
    try:
        validate_workspace_snapshot(root, state)
    except ValueError as exc:
        raise InitialWaveError("snapshot_invalid", str(exc)) from exc
    observation = _snapshot_observation(root, state)
    stored_wave = state.get("initial_authoring_wave")
    if stored_wave:
        if not isinstance(stored_wave, Mapping) or stored_wave.get("state") != (
            "AWAITING_SPEND_AUTHORIZATION"
        ):
            raise InitialWaveError(
                "request_unavailable",
                "Stored initial wave is not awaiting external authority",
            )
        inputs = read_initial_wave_authority_inputs(root)
        wave = inputs["prepared_wave"]
        bundle = inputs["binding_bundle"]
        ledger_actions = (state.get("spend_ledger") or {}).get("actions")
        if not isinstance(ledger_actions, list):
            raise InitialWaveError(
                "request_unavailable", "Initial wave lacks a durable action ledger"
            )
        wave_ids = [member["action_id"] for member in bundle["ordered_members"]]
        resolved: list[dict[str, Any]] = []
        for member in bundle["ordered_members"]:
            matches = [
                action for action in ledger_actions
                if isinstance(action, dict)
                and action.get("action_id") == member["action_id"]
            ]
            if len(matches) != 1:
                raise InitialWaveError(
                    "request_unavailable",
                    "Initial-wave action inventory is missing or duplicated",
                )
            action = matches[0]
            if (
                action.get("state") != "PREPARED"
                or action.get("provider") is not None
                or action.get("consumption") is not None
                or action.get("binding") != member["binding"]
            ):
                raise InitialWaveError(
                    "request_unavailable",
                    "Initial-wave action is not providerless and admissible",
                )
            resolved.append(action)
        if len(wave_ids) != 6 or len(set(wave_ids)) != 6 or len(resolved) != 6:
            raise InitialWaveError(
                "request_unavailable", "Initial-wave inventory is not exactly six"
            )
        context = {
            "wave_id": wave["wave_id"], "wave_sha256": wave["wave_sha256"],
            "route_contract": wave["route_contract"],
            "assignment_sha256": wave["assignment_sha256"],
            "profile_sha256": wave["profile_sha256"], "member_count": 6,
            "ordered_member_binding_sha256s": [
                member["binding_sha256"] for member in bundle["ordered_members"]
            ],
        }
        request = build_external_authority_request(
            run_id=state["run_id"], observation=observation,
            actions=bundle["ordered_members"], initial_wave=context,
        )
    else:
        actions = [
            item for item in (state.get("spend_ledger") or {}).get("actions", [])
            if item.get("state") == "PREPARED"
            and item.get("provider") is None and item.get("consumption") is None
        ]
        if not actions:
            raise InitialWaveError(
                "request_unavailable", "No exact prepared action set exists"
            )
        request = build_external_authority_request(
            run_id=state["run_id"], observation=observation, actions=actions,
        )
    try:
        final_state = load_json(run_json)
        validate_workspace_snapshot(root, final_state)
    except ValueError as exc:
        raise InitialWaveError("snapshot_invalid", str(exc)) from exc
    if (
        final_state != state
        or _snapshot_observation(root, final_state) != observation
    ):
        raise InitialWaveError(
            "snapshot_invalid", "Run changed while authority request was being read"
        )
    return request


def read_external_authority_schema() -> dict[str, Any]:
    value = json.loads(read_resource_text(CONTRACT_SCHEMA_RESOURCE))
    if not isinstance(value, dict) or value.get("$id") != (
        "astrowoof.external_authority_contracts.v1"
    ):
        raise ValueError("Installed external-authority schema is invalid")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-dir", type=Path)
    group.add_argument("--validate-request", type=Path)
    group.add_argument("--schema", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.run_dir is not None:
        value = read_external_authority_request(args.run_dir)
    elif args.validate_request is not None:
        value = validate_external_authority_request(json.loads(
            args.validate_request.read_text(encoding="utf-8")
        ))
    else:
        value = read_external_authority_schema()
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        output = args.output.resolve()
        if args.run_dir is not None:
            root = args.run_dir.resolve()
            if output == root or root in output.parents:
                raise InitialWaveError(
                    "unsafe_output_path", "Output must be outside the run directory"
                )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
