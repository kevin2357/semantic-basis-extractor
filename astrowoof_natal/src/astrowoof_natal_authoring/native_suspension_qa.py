"""Installed, provider-free qualification for cooperative native suspension."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Sequence

from .closure import load_json, normalized_path
from .external_authority_v2_qa import (
    _ordinary_authority, _pending_workspace, _reconcile_4_plus_2,
)
from .native_suspension_contracts import (
    read_native_suspension_contract_schema, read_native_suspension_fixture_bundle,
    seal_document, validate_suspension_command_result,
)
from .native_suspension_runtime import read_native_suspension_publication
from .native_transitions import checkpoint_basis


QUALIFICATION_SCHEMA = "astrowoof.native_suspension_qualification.v1"
SCHEMA_RESOURCE = "native-suspension-qualification.v1.schema.json"


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _installed_version() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def _default_v2_command() -> list[str]:
    executable = shutil.which("astrowoof-external-authority-v2")
    if executable:
        return [executable]
    return [
        sys.executable, "-c",
        "from astrowoof_natal_authoring.cli.external_authority_v2 import main; "
        "raise SystemExit(main())",
    ]


def _write_control(run_dir: Path, control: Path) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    state = load_json(run_dir / "run.json")
    basis = checkpoint_basis(
        run_dir, int(state["state_revision"])
    )["checkpoint_basis_sha256"]
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = lambda value: value.isoformat().replace("+00:00", "Z")
    control.mkdir()
    envelope_path = control / "supervision-invocation.v1.json"
    envelope = seal_document({
        "schema_version": "astrowoof.native_supervision_invocation.v1",
        "supervision_invocation_id": "qualification-supervision-one",
        "launch_generation": 1, "api_run_id": "qualification-api-run",
        "job_id": "qualification-job", "attempt_id": "qualification-attempt",
        "lease_id": "qualification-lease", "lease_token_sha256": "a" * 64,
        "native_run_id": state["run_id"], "worker_boot_id": "qualification-boot",
        "command_kind": "external_authority_v2_dispatch",
        "command_sha256": "b" * 64,
        "executable_workspace_root": normalized_path(run_dir),
        "executable_workspace_root_sha256": hashlib.sha256(
            normalized_path(run_dir).encode()
        ).hexdigest(),
        "control_root": normalized_path(control),
        "control_root_sha256": hashlib.sha256(
            normalized_path(control).encode()
        ).hexdigest(),
        "created_at": stamp(now - timedelta(minutes=1)),
        "launch_not_after": stamp(now + timedelta(minutes=1)),
        "grace_deadline": stamp(now + timedelta(minutes=4)),
        "supervision_capability_id": "qualification-capability",
        "supervision_capability_sha256": "d" * 64,
        "envelope_sha256": "",
    }, "envelope_sha256")
    request = seal_document({
        "schema_version": "astrowoof.native_suspension_request.v1",
        "operation": "cooperative_suspend", "request_id": "qualification-request",
        "idempotency_key": "qualification-idempotency",
        "supervision_invocation_id": envelope["supervision_invocation_id"],
        "launch_generation": 1, "envelope_sha256": envelope["envelope_sha256"],
        "supervision_capability_id": envelope["supervision_capability_id"],
        "supervision_capability_sha256": envelope[
            "supervision_capability_sha256"
        ],
        "force_fence_id": "qualification-fence", "force_fence_sha256": "c" * 64,
        "api_run_id": envelope["api_run_id"], "job_id": envelope["job_id"],
        "attempt_id": envelope["attempt_id"], "lease_id": envelope["lease_id"],
        "native_run_id": envelope["native_run_id"],
        "command_kind": envelope["command_kind"],
        "command_sha256": envelope["command_sha256"],
        "executable_workspace_root_sha256": envelope[
            "executable_workspace_root_sha256"
        ],
        "control_root_sha256": envelope["control_root_sha256"],
        "admission_checkpoint_basis_sha256": basis,
        "actor_id": "qualification-operator", "reason_code": "qualification-stop",
        "environment": "qa", "emergency_containment_confirmed": True,
        "requested_at": stamp(now), "expires_at": stamp(now + timedelta(minutes=3)),
        "grace_deadline": envelope["grace_deadline"], "request_sha256": "",
    }, "request_sha256")
    envelope_path.write_text(json.dumps(envelope), encoding="utf-8")
    (control / "native-suspension-request.v1.json").write_text(
        json.dumps(request), encoding="utf-8",
    )
    return envelope_path, envelope, request


def _run(command: Sequence[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command), stdin=subprocess.DEVNULL, capture_output=True, text=True,
        timeout=30, check=False, env=env,
    )


def run_native_suspension_qualification(
    *, v2_command: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Exercise the packaged public child-process boundary without provider I/O."""
    with tempfile.TemporaryDirectory(prefix="astrowoof-native-suspension-") as temporary:
        base = Path(temporary)
        run_dir = base / "run"
        _pending_workspace(run_dir, "exact_natal")
        _reconcile_4_plus_2(run_dir)
        inspection, request_v2, documents, grant = _ordinary_authority(
            run_dir, "exact_natal", "polish",
        )
        paths: dict[str, Path] = {}
        for name, value in (
            ("inspection", inspection), ("request", request_v2),
            ("grant", grant), ("authorization", documents[0]),
        ):
            paths[name] = base / f"{name}.json"
            paths[name].write_text(json.dumps(value), encoding="utf-8")
        envelope_path, envelope, suspension_request = _write_control(
            run_dir, base / "control",
        )
        output = base / "command-result.json"
        command = [*(v2_command or _default_v2_command()),
            "--run-dir", str(run_dir), "--inspection", str(paths["inspection"]),
            "--request", str(paths["request"]), "--grant", str(paths["grant"]),
            "--authorization", str(paths["authorization"]), "--provider", "openai",
            "--api-key-env", "OPENAI_API_KEY", "--output", str(output),
            "--log-level", "ERROR", "--supervision-envelope", str(envelope_path),
            "--suspension-control-root", str(base / "control"),
        ]
        env = dict(os.environ)
        env["OPENAI_API_KEY"] = "qualification-only-no-network"
        first = _run(command, env=env)
        if first.returncode != 0 or not output.is_file():
            raise RuntimeError(
                f"Installed suspension command failed: {first.returncode}: {first.stderr}"
            )
        first_command = load_json(output)
        result_id = first_command["result_id"]
        publication = read_native_suspension_publication(
            run_dir, result_id, envelope=envelope, request=suspension_request,
        )
        validate_suspension_command_result(
            first_command, result=publication["result"], receipt=publication["receipt"],
            request=suspension_request, envelope=envelope,
        )
        output.unlink()
        replay = _run(command, env=env)
        replay_command = load_json(output) if output.is_file() else None

        other_run = base / "unrelated-run"
        _pending_workspace(other_run, "exact_natal")
        unrelated_command = deepcopy(command)
        unrelated_command[unrelated_command.index(str(run_dir))] = str(other_run)
        output.unlink()
        unrelated = _run(unrelated_command, env=env)

        suspension_actions = publication["result"]["actions"]
        providerless = [
            item for item in suspension_actions
            if item["custody_class"] == "providerless_authority"
        ]
        checks = {
            "installed_cli_exact_exit_zero": first.returncode == 0,
            "checkpointed_suspension_result": (
                publication["result"]["outcome"] == "suspended_checkpointed"
                and publication["result"]["provider_boundary"] == "not_entered"
            ),
            "exact_output_join": publication["command_result"] == first_command,
            "exact_replay_is_inert": replay.returncode == 0 and replay_command == first_command,
            "no_provider_identity_or_io": bool(providerless) and all(
                item["provider_operation_id"] is None for item in providerless
            ) and not any(
                item["custody_class"] == "provider_ambiguous"
                for item in suspension_actions
            ),
            "unrelated_workspace_refuses": (
                unrelated.returncode != 0
                and not (other_run / "native-suspension-index.v1.json").exists()
            ),
            "packaged_contract_resources_readable": bool(
                read_native_suspension_contract_schema()
                and read_native_suspension_fixture_bundle()
            ),
        }

    body = {
        "schema_version": QUALIFICATION_SCHEMA,
        "status": "pass" if all(checks.values()) else "fail",
        "qualification_only": True, "provider_free": True,
        "external_network_call_count": 0, "provider_create_count": 0,
        "provider_retrieve_count": 0, "provider_spend_usd": 0,
        "live_process_termination_count": 0, "api_resource_release_count": 0,
        "sbe_version": _installed_version(), "checks": checks,
        "result_id": publication["result"]["result_id"],
        "result_sha256": publication["result"]["result_sha256"],
        "receipt_id": publication["receipt"]["receipt_id"],
        "receipt_sha256": publication["receipt"]["receipt_sha256"],
        "command_result_sha256": first_command["command_result_sha256"],
        "contract_schema_sha256": _digest(read_native_suspension_contract_schema()),
        "fixture_bundle_sha256": read_native_suspension_fixture_bundle()[
            "bundle_sha256"
        ],
    }
    return validate_native_suspension_qualification({
        **body, "qualification_sha256": _digest(body),
    })


def validate_native_suspension_qualification(value: Any) -> dict[str, Any]:
    required = {
        "schema_version", "qualification_sha256", "status", "qualification_only",
        "provider_free", "external_network_call_count", "provider_create_count",
        "provider_retrieve_count", "provider_spend_usd",
        "live_process_termination_count", "api_resource_release_count", "sbe_version",
        "checks", "result_id", "result_sha256", "receipt_id", "receipt_sha256",
        "command_result_sha256", "contract_schema_sha256", "fixture_bundle_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Native suspension qualification fields differ")
    body = {key: item for key, item in value.items() if key != "qualification_sha256"}
    expected_checks = {
        "installed_cli_exact_exit_zero", "checkpointed_suspension_result",
        "exact_output_join", "exact_replay_is_inert", "no_provider_identity_or_io",
        "unrelated_workspace_refuses", "packaged_contract_resources_readable",
    }
    if (
        value["schema_version"] != QUALIFICATION_SCHEMA
        or value["qualification_sha256"] != _digest(body)
        or value["status"] != "pass" or value["qualification_only"] is not True
        or value["provider_free"] is not True
        or any(value[field] != 0 for field in (
            "external_network_call_count", "provider_create_count",
            "provider_retrieve_count", "provider_spend_usd",
            "live_process_termination_count", "api_resource_release_count",
        ))
        or set(value["checks"]) != expected_checks
        or any(item is not True for item in value["checks"].values())
        or not all(isinstance(value[field], str) and value[field] for field in (
            "sbe_version", "result_id", "result_sha256", "receipt_id",
            "receipt_sha256", "command_result_sha256", "contract_schema_sha256",
            "fixture_bundle_sha256",
        ))
    ):
        raise ValueError("Native suspension qualification semantics differ")
    return deepcopy(value)


def read_native_suspension_qualification_schema() -> dict[str, Any]:
    path = files("astrowoof_natal_authoring.resources.contracts").joinpath(
        SCHEMA_RESOURCE,
    )
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema", action="store_true")
    args = parser.parse_args(argv)
    value = (
        read_native_suspension_qualification_schema()
        if args.schema else run_native_suspension_qualification()
    )
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
