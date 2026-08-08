"""Installed-runtime smoke test for the complete deterministic workflow."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .closure import (
    FakeAuthoringProvider,
    cleanup_completed_run,
    create_run,
    load_json,
    sha256_file,
)
from .contracts import authoring_profile
from .provenance import resource_set_provenance
from .resource_access import resource


SMOKE_SCHEMA = "astrowoof.natal_authoring.release_smoke.v0.1"
FIXTURE_FILES = (
    "natal.bre.woof.general.json",
    "natal.bre.woof.d2d.json",
    "natal.bre.woof.handler.json",
    "natal.bre.woof.hybrid.json",
)
SMOKE_SOURCE_ID_ORIGINAL = "natal:bre"
SMOKE_SOURCE_ID = "550e8400-e29b-41d4-a716-446655440000"
QUALIFIED_AGF_WHEEL_SHA256 = (
    "d1b357b1ec0e40faf7070b29e5c25d18e54c9507406518f26587aac46300aa95"
)
QUALIFIED_SPC_WHEEL_SHA256 = (
    "60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150"
)


def materialize_fixture(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in FIXTURE_FILES:
        source = json.loads(
            resource(f"fixtures/bre/{name}").read_text(encoding="utf-8")
        )
        source["source_identity"] = {
            "source_chart_id": SMOKE_SOURCE_ID,
            "source_chart_ids": [SMOKE_SOURCE_ID],
            "sensor_instance_id": SMOKE_SOURCE_ID,
        }
        target.joinpath(name).write_text(
            json.dumps(source, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )


def _check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def run_smoke(work_dir: Path, *, require_installed: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    package_root = Path(__file__).resolve().parent
    if require_installed:
        _check(
            any(part.lower() == "site-packages" for part in package_root.parts),
            f"runtime did not load from site-packages: {package_root}",
            errors,
        )
    input_dir = work_dir / "input"
    run_dir = work_dir / "run"
    materialize_fixture(input_dir)
    fixture_hashes = {
        name: sha256_file(input_dir / name)
        for name in FIXTURE_FILES
    }
    profile = authoring_profile(
        extraction={
            "handoff_profile": "authoring-workspace",
            "workspace_layout": "split",
            "workspace_card_limit": 50,
            "pass_count": 6,
            "split_assignment_policy": "stratified-v1",
            "full_chart_basis_format": "compact-v2",
        },
        authoring={"provider": "fake", "service_level": "interactive"},
        qa={"polish": False, "allow_lint_warnings": False},
    )
    state, run_json = create_run(
        input_package=input_dir,
        run_dir=run_dir,
        subject="bre",
        provider=FakeAuthoringProvider(),
        max_attempts=3,
        sbe_script=None,
        python_executable=Path(sys.executable),
        service_level="interactive",
        split_assignment_policy="stratified-v1",
        full_chart_basis_format="compact-v2",
        profile=profile,
    )
    _check(state.get("status") == "AUTHORING", "create_run did not stop at AUTHORING", errors)
    _check(all(item["state"] == "GENERATED" for item in state["passes"].values()), "passes were not generated", errors)
    packet_path = (
        run_dir / "sbe" / "semantic-basis-output" / "bre"
        / "bre.selected-authoring-packet.json"
    )
    packet = load_json(packet_path)
    _check(
        (packet.get("source", {}).get("source_identity") or {}).get(
            "source_chart_id"
        ) == SMOKE_SOURCE_ID,
        "opaque identity did not reach the authoring packet",
        errors,
    )
    selected_claims = packet.get("cards", [])
    synthesized_claims = [
        item for item in selected_claims
        if item.get("claim_type") == "synthesized_theme"
    ]
    _check(bool(selected_claims), "authoring packet has no selected claims", errors)
    _check(bool(synthesized_claims), "authoring packet has no syntheses", errors)
    _check(
        all(item.get("evidence") for item in selected_claims),
        "selected claims lost evidence under opaque source identity",
        errors,
    )
    _check(
        all(item.get("evidence") for item in synthesized_claims),
        "syntheses lost evidence under opaque source identity",
        errors,
    )

    command = [
        sys.executable,
        "-m",
        "astrowoof_natal_authoring.closure",
        "--resume",
        "--run-dir",
        str(run_dir),
        "--provider",
        "fake",
        "--max-attempts",
        "3",
        "--fake-reject",
        "bre_1:1",
        "--foreground",
        "--poll-interval-seconds",
        "0.01",
    ]
    resumed = subprocess.run(command, capture_output=True, text=True, check=False)
    _check(resumed.returncode == 0, f"resume command failed: {resumed.stderr}", errors)
    state = load_json(run_json)
    _check(state.get("status") == "DELIVERY_COMPLETE", "run did not complete delivery", errors)
    first_pass = state.get("passes", {}).get("bre_1", {})
    _check(len(first_pass.get("attempts", [])) == 2, "forced rejection did not produce two attempts", errors)
    if first_pass.get("attempts"):
        _check(first_pass["attempts"][0].get("state") == "PASS_QA_REJECTED", "first attempt was not rejected", errors)
        _check(first_pass["attempts"][-1].get("state") == "PASS_QA_ACCEPTED", "retry was not accepted", errors)

    public = load_json(run_dir / "public-run.json")
    _check(public.get("progress", {}).get("passes_accepted") == 6, "public progress is not 6/6", errors)
    record = state.get("subjects", {}).get("bre", {})
    deck_path = Path(record.get("deck", ""))
    delivery_path = Path(record.get("delivery") or "")
    _check(deck_path.is_file(), "final deck is missing", errors)
    _check(delivery_path.is_file(), "delivery ZIP is missing", errors)
    if deck_path.is_file():
        deck = load_json(deck_path)
        _check(len(deck.get("cards", [])) == 50, "deck does not contain 50 cards", errors)
        _check(len(deck.get("summary", {})) == 4, "deck does not contain four summaries", errors)
        _check(
            (deck.get("source", {}).get("source_identity") or {}).get(
                "source_chart_id"
            ) == SMOKE_SOURCE_ID,
            "opaque identity did not reach the delivered deck",
            errors,
        )

    delivery_members: list[str] = []
    manifest_hashes_match = False
    if delivery_path.is_file():
        with zipfile.ZipFile(delivery_path) as archive:
            _check(archive.testzip() is None, "delivery ZIP failed integrity test", errors)
            delivery_members = sorted(archive.namelist())
        manifest_path = Path(record["delivery_manifest"])
        manifest = load_json(manifest_path)
        manifest_hashes_match = all(
            sha256_file(manifest_path.parent / item["filename"]) == item["sha256"]
            for item in manifest.get("artifacts", [])
        )
        _check(manifest_hashes_match, "delivery manifest hashes do not match", errors)
        _check(len(delivery_members) == 5, "delivery ZIP does not contain five files", errors)
        manifest_identity = (
            (((manifest.get("provenance") or {}).get("input_subject") or {})
             .get("contexts") or [{}])[0]
            .get("declared", {})
            .get("source_identity", {})
            .get("source_chart_id")
        )
        _check(
            manifest_identity == SMOKE_SOURCE_ID,
            "opaque identity did not reach delivery provenance",
            errors,
        )

    resources = resource_set_provenance()
    _check(resources["resource_count"] >= 19, "packaged resource set is incomplete", errors)
    _check(len(resources["aggregate_sha256"]) == 64, "resource digest is invalid", errors)
    provenance = state.get("provenance", {})
    _check(len((provenance.get("input", {}).get("subjects") or [{}])[0].get("contexts", [])) == 4, "input provenance is incomplete", errors)
    _check(len((provenance.get("execution", {}).get("subjects", {}).get("bre", {}).get("delivery") or {}).get("sha256", "")) == 64, "delivery provenance is incomplete", errors)

    dry_cleanup = cleanup_completed_run(run_dir, dry_run=True)
    _check(dry_cleanup.get("target_count", 0) > 0, "cleanup dry run found no targets", errors)
    cleanup = cleanup_completed_run(run_dir, dry_run=False)
    _check(cleanup.get("status") == "complete", "cleanup did not complete", errors)
    _check(run_json.is_file(), "cleanup removed operator state", errors)
    _check((run_dir / "public-run.json").is_file(), "cleanup removed public state", errors)
    _check(delivery_path.is_file(), "cleanup removed final delivery", errors)

    return {
        "schema_version": SMOKE_SCHEMA,
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "runtime_module": str(package_root),
        "require_installed": require_installed,
        "checks": {
            "fixture_hashes": fixture_hashes,
            "fixture_derivation": {
                "mode": "identity_contract_substitution",
                "original_source_chart_id": SMOKE_SOURCE_ID_ORIGINAL,
                "source_chart_id": SMOKE_SOURCE_ID,
                "agf_0_6_wheel_sha256": QUALIFIED_AGF_WHEEL_SHA256,
                "spc_0_10_wheel_sha256": QUALIFIED_SPC_WHEEL_SHA256,
            },
            "initial_state": "AUTHORING",
            "resume": state.get("status"),
            "forced_retry_attempt_count": len(first_pass.get("attempts", [])),
            "card_count": len(load_json(deck_path).get("cards", [])) if deck_path.is_file() else 0,
            "summary_count": len(load_json(deck_path).get("summary", {})) if deck_path.is_file() else 0,
            "delivery_members": delivery_members,
            "manifest_hashes_match": manifest_hashes_match,
            "resource_count": resources["resource_count"],
            "resource_set_sha256": resources["aggregate_sha256"],
            "cleanup_target_count": cleanup.get("target_count"),
            "cleanup_reclaimed_bytes": cleanup.get("reclaimed_bytes"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-installed", action="store_true")
    args = parser.parse_args()
    if args.work_dir:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        report = run_smoke(args.work_dir, require_installed=args.require_installed)
    else:
        with tempfile.TemporaryDirectory(prefix="astrowoof-release-smoke-") as temporary:
            report = run_smoke(Path(temporary), require_installed=args.require_installed)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if report["status"] != "pass":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
