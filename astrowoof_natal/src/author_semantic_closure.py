#!/usr/bin/env python3
"""Orchestrate the deterministic stages of AstroWoof semantic closure.

Phase 1 deliberately ships with a fake authoring provider only.  It exercises
SBE generation, six-pass discovery, durable attempt state, local acceptance
checking, retries, and resumability without making network requests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


SCHEMA_VERSION = "astrowoof.semantic_closure_run.v0.1"
PASS_COUNT = 6
TERMINAL_STATES = {"PASS_QA_ACCEPTED", "FAILED_REQUIRES_REVIEW"}
FIELD_PATTERN = re.compile(
    r"(<!-- BEGIN FIELD: ([a-zA-Z0-9_.]+) -->\s*\n)"
    r"(.*?)"
    r"(\n<!-- END FIELD: \2 -->)",
    re.DOTALL,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
        handle.write(rendered)
        handle.flush()
    temporary.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_path(path: Path) -> str:
    return str(path.resolve())


def safe_extract_zip(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            try:
                target.relative_to(destination_root)
            except ValueError as exc:
                raise ValueError(
                    f"Unsafe ZIP member in {archive_path}: {member.filename}"
                ) from exc
        archive.extractall(destination)


def find_workspace_root(extracted: Path, expected_name: str) -> Path:
    direct = extracted / expected_name
    if (direct / "START HERE.md").is_file():
        return direct
    matches = [
        path.parent
        for path in extracted.rglob("START HERE.md")
        if path.parent.name == expected_name
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one {expected_name!r} workspace in {extracted}; "
            f"found {len(matches)}"
        )
    return matches[0]


@dataclass(frozen=True)
class PassSpec:
    pass_id: str
    subject: str
    pass_number: int
    source_zip: Path
    source_sha256: str


@dataclass(frozen=True)
class ProviderResult:
    workspace: Path
    metadata: dict[str, Any]


class AuthoringProvider(Protocol):
    name: str

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
    ) -> ProviderResult:
        """Author one fresh pass workspace."""


def _fake_field_value(
    *,
    pass_id: str,
    relative_file: str,
    field: str,
    ordinal: int,
) -> str:
    identity = re.sub(
        r"[^a-z0-9]+",
        " ",
        f"{pass_id} {relative_file} {field} {ordinal}".lower(),
    ).strip()
    identity_token = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    if field in {
        "context_filter_groups.high_level",
        "context_filter_groups.detail_level",
    }:
        return f"Personality {ordinal}"
    if field.startswith("theme_group."):
        return f"Chapter {(ordinal % 4) + 1}"
    if field.startswith("plan."):
        return (
            f"Editorial plan {identity} follows a singular behavioral doorway "
            f"and keeps this assignment distinct."
        )
    if ".headline." in field:
        return f"A Singular Portrait {identity.title()}"
    if ".body." in field:
        return (
            f"Insight {identity_token} reveals one memorable behavior through "
            f"an independent cadence."
        )
    if field.startswith("dos."):
        return f"Encourage the specific strength described by {identity}."
    if field.startswith("donts."):
        return f"Do not flatten the distinctive need described by {identity}."
    if "quotes." in field:
        return f"I have reviewed the evidence for {identity}, and request snacks."
    if "jokes." in field:
        return f"The comic premise for {identity} has excellent treat potential."
    return f"Authored value for {identity}."


def fill_fake_workspace(workspace: Path) -> None:
    ordinal = 0
    pass_id = workspace.name
    for path in sorted(workspace.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "__WRITE__" not in text:
            continue
        relative_file = path.relative_to(workspace).as_posix()

        def replace(match: re.Match[str]) -> str:
            nonlocal ordinal
            ordinal += 1
            value = _fake_field_value(
                pass_id=pass_id,
                relative_file=relative_file,
                field=match.group(2),
                ordinal=ordinal,
            )
            return f"{match.group(1)}{value}{match.group(4)}"

        rendered = FIELD_PATTERN.sub(replace, text)
        unfinished_fields = [
            field
            for _, field, value, _ in FIELD_PATTERN.findall(rendered)
            if "__WRITE__" in value
        ]
        if unfinished_fields:
            raise ValueError(
                f"Marked placeholders remain in {path}: "
                f"{', '.join(unfinished_fields)}"
            )
        path.write_text(rendered, encoding="utf-8")


class FakeAuthoringProvider:
    """Deterministic local provider used to prove orchestration behavior."""

    name = "fake"

    def __init__(
        self,
        *,
        reject_attempts: dict[str, int] | None = None,
        error_attempts: dict[str, int] | None = None,
    ) -> None:
        self.reject_attempts = reject_attempts or {}
        self.error_attempts = error_attempts or {}

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
    ) -> ProviderResult:
        if attempt_number <= self.error_attempts.get(spec.pass_id, 0):
            raise RuntimeError(
                f"Injected provider error for {spec.pass_id} attempt "
                f"{attempt_number}"
            )
        shutil.copytree(source_workspace, response_workspace)
        fill_fake_workspace(response_workspace)
        if attempt_number <= self.reject_attempts.get(spec.pass_id, 0):
            writing_files = sorted(
                response_workspace.rglob("WRITE THIS CARD.md")
            )
            if len(writing_files) >= 2:
                duplicate = (
                    "This deliberately duplicated sentence makes the local "
                    "acceptance gate reject the simulated authoring attempt."
                )
                for path in writing_files[:2]:
                    text = path.read_text(encoding="utf-8")
                    body_match = re.search(
                        r"(<!-- BEGIN FIELD: [^.]+\.body\.[^ ]+ -->\s*\n)"
                        r"(.*?)"
                        r"(\n<!-- END FIELD: [^.]+\.body\.[^ ]+ -->)",
                        text,
                        re.DOTALL,
                    )
                    if body_match:
                        text = (
                            text[:body_match.start(2)]
                            + duplicate
                            + text[body_match.end(2):]
                        )
                        path.write_text(text, encoding="utf-8")
        return ProviderResult(
            workspace=response_workspace,
            metadata={
                "provider": self.name,
                "deterministic": True,
                "injected_rejection": (
                    attempt_number
                    <= self.reject_attempts.get(spec.pass_id, 0)
                ),
            },
        )


def parse_attempt_map(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        try:
            pass_id, attempts_text = value.rsplit(":", 1)
            attempts = int(attempts_text)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Expected PASS_ID:COUNT, received {value!r}"
            ) from exc
        if not pass_id or attempts < 0:
            raise argparse.ArgumentTypeError(
                f"Expected PASS_ID:COUNT with COUNT >= 0, received {value!r}"
            )
        result[pass_id] = attempts
    return result


def run_sbe(
    *,
    input_package: Path,
    subject: str | None,
    sbe_script: Path,
    python_executable: Path,
    output_dir: Path,
    bundle_dir: Path,
) -> dict[str, Any]:
    command = [
        str(python_executable),
        str(sbe_script),
        "--input-package",
        str(input_package),
        "--output-dir",
        str(output_dir),
        "--bundle-dir",
        str(bundle_dir),
        "--handoff-profile",
        "authoring-workspace",
        "--workspace-layout",
        "split",
        "--workspace-card-limit",
        "50",
        "--fail-fast",
    ]
    if subject:
        command.extend(["--subject", subject])
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    log = {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    write_json_atomic(output_dir.parent / "sbe-invocation.json", log)
    if completed.returncode != 0:
        raise RuntimeError(
            "SBE generation failed; see "
            f"{output_dir.parent / 'sbe-invocation.json'}"
        )
    manifest_path = output_dir / "run-manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"SBE did not emit {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("status") != "pass":
        raise RuntimeError(f"SBE run manifest did not pass: {manifest_path}")
    return manifest


def discover_passes(
    sbe_manifest: dict[str, Any],
    bundle_dir: Path,
) -> list[PassSpec]:
    specs: list[PassSpec] = []
    for subject_record in sbe_manifest.get("subjects", []):
        if subject_record.get("status") != "pass":
            continue
        subject = subject_record["subject"]
        for pass_number in range(1, PASS_COUNT + 1):
            pass_id = f"{subject}_{pass_number}"
            source_zip = bundle_dir / f"{pass_id}.zip"
            if not source_zip.is_file():
                raise FileNotFoundError(
                    f"Missing SBE authoring pass archive: {source_zip}"
                )
            with zipfile.ZipFile(source_zip) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    raise ValueError(
                        f"Corrupt SBE archive {source_zip}: {bad_member}"
                    )
                expected = f"{pass_id}/START HERE.md"
                if expected not in archive.namelist():
                    raise ValueError(
                        f"{source_zip} does not contain {expected}"
                    )
            specs.append(
                PassSpec(
                    pass_id=pass_id,
                    subject=subject,
                    pass_number=pass_number,
                    source_zip=source_zip,
                    source_sha256=sha256_file(source_zip),
                )
            )
    if not specs:
        raise ValueError("SBE manifest contains no passing subjects")
    return specs


def initial_run_state(
    *,
    input_package: Path,
    run_dir: Path,
    provider: AuthoringProvider,
    max_attempts: int,
    sbe_manifest: dict[str, Any],
    specs: list[PassSpec],
) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUTHORING",
        "created_at": now,
        "updated_at": now,
        "input_package": normalized_path(input_package),
        "run_dir": normalized_path(run_dir),
        "provider": provider.name,
        "max_attempts": max_attempts,
        "sbe": {
            "status": "pass",
            "subject_count": sbe_manifest.get("subject_count"),
            "manifest": normalized_path(
                run_dir / "sbe" / "semantic-basis-output" / "run-manifest.json"
            ),
        },
        "passes": {
            spec.pass_id: {
                "pass_id": spec.pass_id,
                "subject": spec.subject,
                "pass_number": spec.pass_number,
                "source_zip": normalized_path(spec.source_zip),
                "source_sha256": spec.source_sha256,
                "state": "GENERATED",
                "attempts": [],
                "accepted_workspace": None,
                "accepted_attempt": None,
            }
            for spec in specs
        },
    }


def specs_from_state(state: dict[str, Any]) -> list[PassSpec]:
    return [
        PassSpec(
            pass_id=record["pass_id"],
            subject=record["subject"],
            pass_number=record["pass_number"],
            source_zip=Path(record["source_zip"]),
            source_sha256=record["source_sha256"],
        )
        for record in sorted(
            state["passes"].values(),
            key=lambda item: (item["subject"], item["pass_number"]),
        )
    ]


def update_run_status(state: dict[str, Any]) -> None:
    states = {record["state"] for record in state["passes"].values()}
    if states == {"PASS_QA_ACCEPTED"}:
        state["status"] = "AUTHORING_COMPLETE"
    elif "FAILED_REQUIRES_REVIEW" in states:
        state["status"] = "FAILED_REQUIRES_REVIEW"
    else:
        state["status"] = "AUTHORING"
    state["updated_at"] = utc_now()


def save_state(run_json: Path, state: dict[str, Any]) -> None:
    update_run_status(state)
    write_json_atomic(run_json, state)


def prepare_source_workspace(spec: PassSpec, pass_root: Path) -> Path:
    source_root = pass_root / "source"
    if source_root.exists():
        workspace = find_workspace_root(source_root, spec.pass_id)
        return workspace
    safe_extract_zip(spec.source_zip, source_root)
    return find_workspace_root(source_root, spec.pass_id)


def run_pass_acceptance(
    workspace: Path,
    report_path: Path,
    *,
    python_executable: Path,
) -> tuple[bool, dict[str, Any]]:
    checker = workspace / "lint_authoring_pass.py"
    if not checker.is_file():
        raise FileNotFoundError(f"Authored workspace lacks checker: {checker}")
    completed = subprocess.run(
        [
            str(python_executable),
            str(checker),
            str(workspace),
            "--output",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if not report_path.is_file():
        raise RuntimeError(
            f"Acceptance checker emitted no report (exit {completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    report = load_json(report_path)
    accepted = completed.returncode == 0 and report.get("status") == "accept"
    return accepted, {
        "accepted": accepted,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "report": report,
    }


def author_one_pass(
    *,
    spec: PassSpec,
    record: dict[str, Any],
    provider: AuthoringProvider,
    run_dir: Path,
    max_attempts: int,
    python_executable: Path,
    run_json: Path,
    state: dict[str, Any],
) -> None:
    if record["state"] == "PASS_QA_ACCEPTED":
        accepted = Path(record["accepted_workspace"])
        if not accepted.is_dir():
            raise FileNotFoundError(
                f"Accepted workspace is missing for {spec.pass_id}: {accepted}"
            )
        return
    if record["state"] == "FAILED_REQUIRES_REVIEW":
        return
    if sha256_file(spec.source_zip) != spec.source_sha256:
        raise ValueError(
            f"Source pass changed since run creation: {spec.source_zip}"
        )

    pass_root = run_dir / "passes" / spec.pass_id
    source_workspace = prepare_source_workspace(spec, pass_root)
    completed_attempts = len(record["attempts"])
    for attempt_number in range(completed_attempts + 1, max_attempts + 1):
        attempt_root = pass_root / f"attempt-{attempt_number:03d}"
        response_workspace = attempt_root / "response" / spec.pass_id
        attempt = {
            "attempt_number": attempt_number,
            "state": "SUBMITTED",
            "started_at": utc_now(),
            "finished_at": None,
            "response_workspace": normalized_path(response_workspace),
            "provider_metadata": None,
            "qa": None,
            "error": None,
        }
        record["state"] = "SUBMITTED"
        record["attempts"].append(attempt)
        save_state(run_json, state)
        try:
            result = provider.author(
                source_workspace,
                response_workspace,
                spec,
                attempt_number,
            )
            attempt["state"] = "RESPONSE_RECEIVED"
            attempt["provider_metadata"] = result.metadata
            record["state"] = "RESPONSE_RECEIVED"
            save_state(run_json, state)

            report_path = attempt_root / "authoring-pass-acceptance.json"
            accepted, qa = run_pass_acceptance(
                result.workspace,
                report_path,
                python_executable=python_executable,
            )
            attempt["qa"] = qa
            attempt["finished_at"] = utc_now()
            if accepted:
                attempt["state"] = "PASS_QA_ACCEPTED"
                record["state"] = "PASS_QA_ACCEPTED"
                accepted_root = pass_root / "accepted"
                if accepted_root.exists():
                    shutil.rmtree(accepted_root)
                shutil.copytree(result.workspace, accepted_root)
                record["accepted_workspace"] = normalized_path(accepted_root)
                record["accepted_attempt"] = attempt_number
                save_state(run_json, state)
                return
            attempt["state"] = "PASS_QA_REJECTED"
            record["state"] = "PASS_QA_REJECTED"
        except Exception as exc:
            attempt["state"] = "ATTEMPT_ERROR"
            attempt["finished_at"] = utc_now()
            attempt["error"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
            record["state"] = "ATTEMPT_ERROR"
        save_state(run_json, state)

    record["state"] = "FAILED_REQUIRES_REVIEW"
    save_state(run_json, state)


def author_pending_passes(
    *,
    state: dict[str, Any],
    provider: AuthoringProvider,
    run_dir: Path,
    max_attempts: int,
    python_executable: Path,
    run_json: Path,
    stop_after_attempts: int | None = None,
) -> None:
    attempts_before = sum(
        len(record["attempts"]) for record in state["passes"].values()
    )
    for spec in specs_from_state(state):
        record = state["passes"][spec.pass_id]
        author_one_pass(
            spec=spec,
            record=record,
            provider=provider,
            run_dir=run_dir,
            max_attempts=max_attempts,
            python_executable=python_executable,
            run_json=run_json,
            state=state,
        )
        attempts_after = sum(
            len(item["attempts"]) for item in state["passes"].values()
        )
        if (
            stop_after_attempts is not None
            and attempts_after - attempts_before >= stop_after_attempts
        ):
            break
    save_state(run_json, state)


def create_run(
    *,
    input_package: Path,
    run_dir: Path,
    subject: str | None,
    provider: AuthoringProvider,
    max_attempts: int,
    sbe_script: Path,
    python_executable: Path,
) -> tuple[dict[str, Any], Path]:
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(
            f"Run directory is not empty: {run_dir}. Use --resume to continue it."
        )
    run_dir.mkdir(parents=True, exist_ok=True)
    sbe_root = run_dir / "sbe"
    output_dir = sbe_root / "semantic-basis-output"
    bundle_dir = sbe_root / "llm-handoff-bundle"
    sbe_manifest = run_sbe(
        input_package=input_package,
        subject=subject,
        sbe_script=sbe_script,
        python_executable=python_executable,
        output_dir=output_dir,
        bundle_dir=bundle_dir,
    )
    specs = discover_passes(sbe_manifest, bundle_dir)
    state = initial_run_state(
        input_package=input_package,
        run_dir=run_dir,
        provider=provider,
        max_attempts=max_attempts,
        sbe_manifest=sbe_manifest,
        specs=specs,
    )
    run_json = run_dir / "run.json"
    save_state(run_json, state)
    return state, run_json


def resume_run(
    *,
    run_dir: Path,
    provider: AuthoringProvider,
    max_attempts: int,
) -> tuple[dict[str, Any], Path]:
    run_json = run_dir / "run.json"
    if not run_json.is_file():
        raise FileNotFoundError(f"Cannot resume without {run_json}")
    state = load_json(run_json)
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported run schema: {state.get('schema_version')!r}"
        )
    if state.get("provider") != provider.name:
        raise ValueError(
            f"Run provider is {state.get('provider')!r}, not {provider.name!r}"
        )
    if state.get("max_attempts") != max_attempts:
        raise ValueError(
            "Resume must use the original --max-attempts value "
            f"({state.get('max_attempts')})"
        )
    return state, run_json


def default_sbe_script() -> Path:
    return Path(__file__).resolve().with_name(
        "build_projected_semantic_basis.py"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the deterministic Phase-1 AstroWoof semantic-closure workflow."
        )
    )
    parser.add_argument("--input-package", type=Path)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--subject")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--provider", choices=("fake",), default="fake")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument(
        "--sbe-script",
        type=Path,
        default=default_sbe_script(),
    )
    parser.add_argument(
        "--python-executable",
        type=Path,
        default=Path(sys.executable),
    )
    parser.add_argument(
        "--fake-reject",
        action="append",
        default=[],
        metavar="PASS_ID:COUNT",
        help="Make a fake pass fail QA COUNT times before succeeding.",
    )
    parser.add_argument(
        "--fake-error",
        action="append",
        default=[],
        metavar="PASS_ID:COUNT",
        help="Make a fake pass raise COUNT provider errors before succeeding.",
    )
    args = parser.parse_args()
    if args.max_attempts < 1:
        parser.error("--max-attempts must be at least 1")
    if not args.resume and args.input_package is None:
        parser.error("--input-package is required unless --resume is used")

    try:
        reject_attempts = parse_attempt_map(args.fake_reject)
        error_attempts = parse_attempt_map(args.fake_error)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))
    provider = FakeAuthoringProvider(
        reject_attempts=reject_attempts,
        error_attempts=error_attempts,
    )
    if args.resume:
        state, run_json = resume_run(
            run_dir=args.run_dir,
            provider=provider,
            max_attempts=args.max_attempts,
        )
    else:
        state, run_json = create_run(
            input_package=args.input_package,
            run_dir=args.run_dir,
            subject=args.subject,
            provider=provider,
            max_attempts=args.max_attempts,
            sbe_script=args.sbe_script,
            python_executable=args.python_executable,
        )
    author_pending_passes(
        state=state,
        provider=provider,
        run_dir=args.run_dir,
        max_attempts=args.max_attempts,
        python_executable=args.python_executable,
        run_json=run_json,
    )
    print(json.dumps(state, ensure_ascii=False, indent=2))
    if state["status"] == "FAILED_REQUIRES_REVIEW":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
