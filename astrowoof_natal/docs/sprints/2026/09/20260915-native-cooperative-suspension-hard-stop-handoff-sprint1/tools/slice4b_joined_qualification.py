"""Provider-free joined API/SBE cooperative-suspension qualification."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import tempfile

from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from astrowoof_api.domain.reading_execution import ForceFencedAuthorityError
from astrowoof_api.persistence.base import Base, load_all_models
from astrowoof_api.persistence.models.reading_execution import (
    SbeAuthoringRun,
    SbeCapacityAllocation,
    SbeForceFenceDisposition,
    SbeNativeSupervisionInvocation,
)
from astrowoof_api.services.execution_queue import ExecutionQueueService
from astrowoof_api.services.sbe_force_fence import SbeForceFenceService
from astrowoof_api.services.sbe_native_supervision import SbeNativeSupervisionService
from astrowoof_api.services.sbe_provider_orchestration import (
    HeartbeatingProcessSbeProviderRuntime,
    NativeSuspensionLaunch,
    build_external_authority_v2_command_sha256,
)
from astrowoof_natal_authoring.external_authority_v2_qa import (
    _ordinary_authority,
    _pending_workspace,
    _reconcile_4_plus_2,
)
from astrowoof_natal_authoring.native_suspension_runtime import (
    read_native_suspension_publication,
)
from astrowoof_natal_authoring.native_transitions import checkpoint_basis
from test_sbe_force_fence import _active_target


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*, executable: Path, wheel: Path) -> dict[str, object]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    event.listen(
        engine, "connect", lambda connection, _: connection.execute("PRAGMA foreign_keys=ON")
    )
    load_all_models()
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    provider_operations: list[str] = []
    now = datetime.now(UTC).replace(microsecond=0)

    try:
        with tempfile.TemporaryDirectory(prefix="astrowoof-slice4b-") as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            _pending_workspace(workspace, "exact_natal")
            _reconcile_4_plus_2(workspace)
            native_run_id = json.loads(
                (workspace / "run.json").read_text(encoding="utf-8")
            )["run_id"]
            inspection, request, authorizations, grant = _ordinary_authority(
                workspace, "exact_natal", "polish"
            )
            native_revision = json.loads(
                (workspace / "run.json").read_text(encoding="utf-8")
            )["state_revision"]
            admission_basis = checkpoint_basis(workspace, native_revision)[
                "checkpoint_basis_sha256"
            ]
            documents: dict[str, Path] = {}
            for name, value in (
                ("inspection", inspection),
                ("request", request),
                ("grant", grant),
                ("authorization", authorizations[0]),
            ):
                path = root / f"{name}.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                documents[name] = path
            output = root / "command-result.json"

            with factory() as session:
                run_row, job, attempt, lease = _active_target(session)
                authoring = session.scalar(
                    select(SbeAuthoringRun).where(SbeAuthoringRun.run_id == run_row.id)
                )
                assert authoring is not None
                authoring.native_run_id = native_run_id
                session.flush()
                identity = SbeNativeSupervisionService.new_prelaunch_identity(
                    workspace=workspace
                )
                launch_paths = NativeSuspensionLaunch(
                    identity.envelope_path, identity.control_root
                )
                command_sha = build_external_authority_v2_command_sha256(
                    executable=str(executable),
                    workspace=workspace,
                    inspection=documents["inspection"],
                    request=documents["request"],
                    grant=documents["grant"],
                    authorizations=(documents["authorization"],),
                    output=output,
                    suspension_launch=launch_paths,
                )
                supervision = SbeNativeSupervisionService()
                prepared = supervision.prepare_prelaunch(
                    session,
                    run_id=run_row.id,
                    job_id=job.id,
                    attempt_id=attempt.id,
                    lease_id=lease.id,
                    lease_token_sha256=lease.lease_token_digest,
                    native_run_id=native_run_id,
                    worker_boot_id="slice4b-worker",
                    command_kind="external_authority_v2_dispatch",
                    command_sha256=command_sha,
                    admission_checkpoint_basis_sha256=admission_basis,
                    workspace=workspace,
                    identity=identity,
                    now=now,
                    launch_window=timedelta(seconds=30),
                    grace_window=timedelta(minutes=4),
                )
                session.commit()
                supervision.write_prelaunch_envelope(
                    control_root=prepared.control_root,
                    envelope=prepared.envelope,
                )

                fence_id: list[object] = []
                request_writes: list[str] = []

                def heartbeat() -> None:
                    if not fence_id:
                        receipt = SbeForceFenceService().admit(
                            session,
                            run_id=run_row.id,
                            job_id=job.id,
                            actor="slice4b-operator",
                            reason="joined-provider-free-qualification",
                            environment="qa",
                            grace_seconds=120,
                            now=now + timedelta(seconds=1),
                        )
                        fence_id.append(receipt.disposition_id)
                        session.commit()
                    ExecutionQueueService().require_active_authority(
                        session,
                        job_id=job.id,
                        lease_owner_id="ordinary-worker",
                        lease_token="ordinary-token",
                        now=now + timedelta(seconds=2),
                    )

                def publish_request() -> None:
                    invocation = session.get(
                        SbeNativeSupervisionInvocation,
                        prepared.capability.invocation_id,
                    )
                    fence = session.get(SbeForceFenceDisposition, fence_id[0])
                    assert invocation is not None and fence is not None
                    built = supervision.build_suspension_request(
                        invocation=invocation,
                        fence=fence,
                        now=now + timedelta(seconds=3),
                    )
                    written = supervision.write_suspension_request(
                        control_root=prepared.control_root,
                        request=built.request,
                    )
                    request_writes.append(str(written))

                runtime = HeartbeatingProcessSbeProviderRuntime(
                    heartbeat=heartbeat,
                    heartbeat_seconds=1,
                    frozen_arguments=("--provider", "openai"),
                    events_stdout_jsonl=True,
                )
                import astrowoof_api.services.sbe_provider_orchestration as orchestration

                original_sleep = orchestration.time.sleep
                orchestration.time.sleep = lambda _seconds: None
                old_key = os.environ.get("OPENAI_API_KEY")
                os.environ["OPENAI_API_KEY"] = "provider-free-never-used"
                try:
                    result = runtime.external_authority_v2(
                        executable=str(executable),
                        workspace=workspace,
                        inspection=documents["inspection"],
                        request=documents["request"],
                        grant=documents["grant"],
                        authorizations=(documents["authorization"],),
                        output=output,
                        suspension_launch=launch_paths,
                        on_force_fenced=publish_request,
                    )
                    replay = runtime.external_authority_v2(
                        executable=str(executable),
                        workspace=workspace,
                        inspection=documents["inspection"],
                        request=documents["request"],
                        grant=documents["grant"],
                        authorizations=(documents["authorization"],),
                        output=output,
                        suspension_launch=launch_paths,
                        on_force_fenced=publish_request,
                    )
                finally:
                    orchestration.time.sleep = original_sleep
                    if old_key is None:
                        os.environ.pop("OPENAI_API_KEY", None)
                    else:
                        os.environ["OPENAI_API_KEY"] = old_key

                command = result
                publication = read_native_suspension_publication(
                    workspace,
                    str(command["result_id"]),
                    envelope=prepared.envelope,
                    request=json.loads(
                        (prepared.control_root / "native-suspension-request.v1.json").read_text(
                            encoding="utf-8"
                        )
                    ),
                )
                allocation = session.scalar(
                    select(SbeCapacityAllocation).where(
                        SbeCapacityAllocation.run_id == run_row.id
                    )
                )
                fence = session.get(SbeForceFenceDisposition, fence_id[0])
                checks = {
                    "real_api_parent_returned_suspension_command": command.get(
                        "schema_version"
                    )
                    == "astrowoof.native_suspension_command_result.v1",
                    "real_api_callback_published_one_request_per_launch": len(request_writes)
                    == 2,
                    "child_restart_replays_exact_result": replay == command,
                    "replay_reuses_exact_request_path": len(request_writes) == 2
                    and request_writes[0] == request_writes[1],
                    "exact_sbe_publication_join": publication["command_result"] == command,
                    "provider_boundary_not_entered": publication["result"].get(
                        "provider_boundary"
                    )
                    == "not_entered",
                    "force_fence_remains_immutable_unresolved": fence is not None
                    and fence.state == "ambiguous_fenced",
                    "run_allocation_remains_held": allocation is not None
                    and allocation.state == "active",
                    "no_provider_operations": provider_operations == [],
                }
                return {
                    "schema_version": "astrowoof.native_suspension_joined_qualification.v1",
                    "status": "pass" if all(checks.values()) else "fail",
                    "provider_free": True,
                    "checks": checks,
                    "api_revision": "613c0e01a7d473bf1aa0009e7902c23c98f6e093",
                    "sbe_version": "0.4.66",
                    "sbe_wheel_sha256": _sha(wheel),
                    "command_result_schema": command["schema_version"],
                    "result_id": command["result_id"],
                    "result_sha256": command["result_sha256"],
                    "provider_operation_count": 0,
                    "provider_spend_usd": 0,
                    "r2_access_count": 0,
                    "live_process_termination_count": 0,
                    "api_resource_release_count": 0,
                }
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    receipt = run(executable=args.executable, wheel=args.wheel)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
