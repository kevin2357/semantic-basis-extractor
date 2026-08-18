"""Provider-free installed-wheel qualification for joined initial-wave inputs."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import astrowoof_natal_authoring as public
from astrowoof_natal_authoring.closure import normalized_path, write_workspace_snapshot
from astrowoof_natal_authoring.initial_wave import InitialWaveMemberSpec, build_initial_wave
from astrowoof_natal_authoring.pass_protocol import canonical_sha256
from astrowoof_natal_authoring.spend import PRICE_BOOK_VERSION


def documents(route_family: str) -> tuple[dict, dict]:
    bounded = route_family == "bounded_natal"
    bindings = []
    members = []
    for number in range(1, 7):
        binding = {
            "run_id": "installed-authority-inputs",
            "profile_sha256": "a" * 64,
            "prepared_state_revision": 4,
            "stage": "authoring_initial",
            "route": (
                f"bounded_natal:bounded-pass-{number:02d}:attempt-001"
                if bounded else f"installed-{number}:attempt-001"
            ),
            "request_sha256": f"{number:x}" * 64,
            "model": "gpt-5.6-terra",
            "service_level": "interactive",
            "maximum_output_tokens": 30000,
            "commitment_micro_usd": 700000 + number,
            "price_book_version": PRICE_BOOK_VERSION,
        }
        digest = canonical_sha256(binding)
        bindings.append(binding)
        members.append(InitialWaveMemberSpec(
            action_id="paid_" + digest[:24], binding=binding,
            pass_id=(f"bounded-pass-{number:02d}" if bounded else f"installed-{number}"),
            pass_number=number,
        ))
    wave = build_initial_wave(
        run_id="installed-authority-inputs", route_family=route_family,
        route_contract=(
            "astrowoof.bounded_natal.authoring_run.v2" if bounded
            else "astrowoof.semantic_closure_run.v0.9"
        ),
        assignment_sha256="b" * 64, profile_sha256="a" * 64,
        preparation_basis_revision=4, members=members,
    )
    return wave, public.build_initial_wave_binding_bundle(wave, bindings)


def main() -> None:
    if "site-packages" not in public.__file__.replace("\\", "/"):
        raise SystemExit(f"package is not installed: {public.__file__}")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for route in ("exact_natal", "bounded_natal"):
            run_dir = root / route
            run_dir.mkdir()
            wave, bundle = documents(route)
            state = {
                "schema_version": (
                    "astrowoof.bounded_natal.authoring_run.v2"
                    if route == "bounded_natal"
                    else "astrowoof.semantic_closure_run.v0.9"
                ),
                "run_id": wave["run_id"], "state_revision": 5,
                "workspace_contract": {
                    "mode": "stable_logical_absolute_path",
                    "logical_root": normalized_path(run_dir),
                },
                "initial_authoring_wave": {
                    **wave, "state": "AWAITING_SPEND_AUTHORIZATION", "requests": {},
                },
            }
            (run_dir / "run.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8"
            )
            (run_dir / "initial-authoring-wave-binding-bundle.json").write_text(
                json.dumps(bundle, indent=2) + "\n", encoding="utf-8"
            )
            write_workspace_snapshot(run_dir)
            value = public.read_initial_wave_authority_inputs(run_dir)
            public.validate_initial_wave_authority_inputs(value)
            output = root / f"{route}.json"
            subprocess.run([
                sys.executable, "-m", "astrowoof_natal_authoring.initial_wave_contract",
                "--initial-wave-inputs", "--run-dir", str(run_dir),
                "--output", str(output),
            ], check=True, capture_output=True, text=True)
            if json.loads(output.read_text(encoding="utf-8")) != value:
                raise SystemExit(f"CLI output mismatch for {route}")
        print(json.dumps({
            "status": "pass", "installed_module": public.__file__,
            "routes": ["exact_natal", "bounded_natal"],
            "reader": "read_initial_wave_authority_inputs",
            "cli": "--initial-wave-inputs",
        }, indent=2))


if __name__ == "__main__":
    main()
