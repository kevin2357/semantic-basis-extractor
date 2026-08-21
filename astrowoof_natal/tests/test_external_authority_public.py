from __future__ import annotations

import io
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import astrowoof_natal_authoring as public  # noqa: E402
import astrowoof_natal_authoring.external_authority as external_authority  # noqa: E402
from astrowoof_natal_authoring.closure import (  # noqa: E402
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.external_authority import main  # noqa: E402
from astrowoof_natal_authoring.initial_wave import (  # noqa: E402
    InitialWaveMemberSpec,
    build_initial_wave,
    build_initial_wave_binding_bundle,
    canonical_sha256,
)
from astrowoof_natal.tests.test_initial_wave_binding_bundle_contract_proposal import (  # noqa: E402
    fixture as binding_fixture,
)


class TestExternalAuthorityPublic(unittest.TestCase):
    def make_wave_run(self, root: Path, route: str) -> Path:
        run_dir = root / route
        run_dir.mkdir(parents=True)
        original_wave, original_bundle = binding_fixture(route)
        specs = []
        requests = {}
        passes = {}
        for number, original in enumerate(original_bundle["ordered_members"], 1):
            payload = {"fixture": route, "pass_number": number}
            request_sha256 = canonical_sha256(payload)
            binding = deepcopy(original["binding"])
            binding["request_sha256"] = request_sha256
            action_id = "paid_" + canonical_sha256(binding)[:24]
            pass_id = original["pass_id"]
            request_path = run_dir / f"request-{number}.json"
            request_path.write_text(json.dumps(payload), encoding="utf-8")
            specs.append(InitialWaveMemberSpec(
                action_id=action_id, binding=binding, pass_id=pass_id,
                pass_number=number,
            ))
            requests[action_id] = {
                "request_sha256": request_sha256,
                ("request_path" if route == "bounded_natal" else "request_payload_path"):
                    str(request_path),
            }
            passes[pass_id] = {"attempts": [{"paid_action_id": action_id}]}
        wave = build_initial_wave(
            run_id=original_wave["run_id"], route_family=route,
            route_contract=original_wave["route_contract"],
            assignment_sha256=original_wave["assignment_sha256"],
            profile_sha256=original_wave["profile_sha256"],
            preparation_basis_revision=original_wave["preparation_basis_revision"],
            members=specs,
        )
        bundle = build_initial_wave_binding_bundle(
            wave, [spec.binding for spec in specs],
        )
        state = {
            "schema_version": (
                "astrowoof.bounded_natal.authoring_run.v2"
                if route == "bounded_natal"
                else "astrowoof.semantic_closure_run.v0.9"
            ),
            "run_id": wave["run_id"],
            "route_contract": wave["route_contract"],
            "state_revision": wave["preparation_basis_revision"] + 1,
            "updated_at": "2026-08-20T14:00:00Z",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(run_dir),
            },
            "initial_authoring_wave": {
                **wave, "state": "AWAITING_SPEND_AUTHORIZATION", "requests": requests,
            },
            "passes": passes,
            "spend_ledger": {
                "actions": [{
                    "action_id": member["action_id"], "state": "PREPARED",
                    "binding": deepcopy(member["binding"]),
                } for member in bundle["ordered_members"]],
            },
        }
        (run_dir / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        (run_dir / "initial-authoring-wave-binding-bundle.json").write_text(
            json.dumps(bundle, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(run_dir)
        return run_dir

    def make_ordinary_run(self, root: Path) -> Path:
        run_dir = root / "ordinary"
        run_dir.mkdir(parents=True)
        bindings = []
        for suffix, stage in (("b", "qualitative_critic"), ("a", "polish")):
            binding = {
                "run_id": "run_ordinary_fixture", "profile_sha256": "a" * 64,
                "prepared_state_revision": 21, "stage": stage,
                "route": f"{stage}:attempt-001", "request_sha256": suffix * 64,
                "model": "gpt-5.6-luna", "service_level": "interactive",
                "maximum_output_tokens": 30000, "commitment_micro_usd": 200000,
                "price_book_version": "openai-public-2026-08-07.v1",
            }
            bindings.append({
                "action_id": f"paid_{'0' * 23}{suffix}", "state": "PREPARED",
                "binding": binding,
            })
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": "run_ordinary_fixture", "state_revision": 22,
            "updated_at": "2026-08-20T14:01:00Z",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(run_dir),
            },
            "spend_ledger": {"actions": bindings},
        }
        (run_dir / "run.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(run_dir)
        return run_dir

    def test_snapshot_reader_returns_deterministic_wave_request_for_both_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for route in ("exact_natal", "bounded_natal"):
                with self.subTest(route=route):
                    run_dir = self.make_wave_run(Path(temporary), route)
                    first = public.read_external_authority_request(run_dir)
                    second = public.read_external_authority_request(run_dir)
                    self.assertEqual(first, second)
                    self.assertEqual("initial_wave_admission", first["request_kind"])
                    self.assertEqual(6, first["action_count"])
                    self.assertEqual(
                        [item["action_id"] for item in first["ordered_actions"]],
                        first["ordered_action_ids"],
                    )
                    public.validate_external_authority_request(first)

    def test_ordinary_reader_uses_lexical_order_and_complete_bindings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            value = public.read_external_authority_request(
                self.make_ordinary_run(Path(temporary))
            )
            self.assertEqual("ordinary_action_set", value["request_kind"])
            self.assertEqual(sorted(value["ordered_action_ids"]), value["ordered_action_ids"])
            self.assertIsNone(value["initial_wave"])
            self.assertEqual(2, len(value["ordered_actions"]))

    def test_reader_fails_closed_on_snapshot_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_wave_run(Path(temporary), "exact_natal")
            path = run_dir / "initial-authoring-wave-binding-bundle.json"
            path.write_bytes(path.read_bytes() + b" ")
            with self.assertRaises(public.InitialWaveError) as caught:
                public.read_external_authority_request(run_dir)
            self.assertEqual("snapshot_invalid", caught.exception.reason_code)

    def test_reader_refuses_authorized_stored_wave(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_wave_run(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            state["initial_authoring_wave"]["state"] = "AUTHORIZED"
            for action in state["spend_ledger"]["actions"]:
                action["state"] = "AUTHORIZED"
                action["authorization"] = {"authorization_reference": "fixture"}
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            with self.assertRaises(public.InitialWaveError) as caught:
                public.read_external_authority_request(run_dir)
            self.assertEqual("request_unavailable", caught.exception.reason_code)

    def test_reader_refuses_provider_recorded_member_even_if_wave_label_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_wave_run(Path(temporary), "exact_natal")
            run_json = run_dir / "run.json"
            state = json.loads(run_json.read_text(encoding="utf-8"))
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "PROVIDER_ID_RECORDED"
            action["consumption"] = {"consumer_id": "fixture", "state_revision": 13}
            action["provider"] = {"kind": "response", "id": "resp_fixture"}
            run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            write_workspace_snapshot(run_dir)
            with self.assertRaises(public.InitialWaveError) as caught:
                public.read_external_authority_request(run_dir)
            self.assertEqual("request_unavailable", caught.exception.reason_code)

    def test_reader_refuses_binding_mismatch_and_duplicate_wave_action(self) -> None:
        for mutation in ("binding", "duplicate"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                run_dir = self.make_wave_run(Path(temporary), "exact_natal")
                run_json = run_dir / "run.json"
                state = json.loads(run_json.read_text(encoding="utf-8"))
                if mutation == "binding":
                    state["spend_ledger"]["actions"][0]["binding"][
                        "maximum_output_tokens"
                    ] += 1
                else:
                    state["spend_ledger"]["actions"].append(deepcopy(
                        state["spend_ledger"]["actions"][0]
                    ))
                run_json.write_text(
                    json.dumps(state, indent=2) + "\n", encoding="utf-8"
                )
                write_workspace_snapshot(run_dir)
                with self.assertRaises(public.InitialWaveError) as caught:
                    public.read_external_authority_request(run_dir)
                self.assertEqual(
                    "initial_wave_lineage_unjoinable",
                    caught.exception.reason_code,
                )

    def test_reader_fails_closed_on_coherent_change_during_read(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_wave_run(Path(temporary), "exact_natal")
            original = external_authority.read_initial_wave_authority_inputs

            def change_after_join(path: Path) -> dict:
                value = original(path)
                run_json = run_dir / "run.json"
                state = json.loads(run_json.read_text(encoding="utf-8"))
                state["state_revision"] += 1
                state["updated_at"] = "2026-08-20T14:00:01Z"
                run_json.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                write_workspace_snapshot(run_dir)
                return value

            with (
                patch.object(
                    external_authority, "read_initial_wave_authority_inputs",
                    side_effect=change_after_join,
                ),
                self.assertRaises(public.InitialWaveError) as caught,
            ):
                public.read_external_authority_request(run_dir)
            self.assertEqual("snapshot_invalid", caught.exception.reason_code)

    def test_validator_rejects_changed_binding_and_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            value = public.read_external_authority_request(
                self.make_wave_run(Path(temporary), "exact_natal")
            )
            changed = deepcopy(value)
            changed["ordered_actions"][0]["binding"]["maximum_output_tokens"] += 1
            with self.assertRaises(public.InitialWaveError):
                public.validate_external_authority_request(changed)

    def test_validator_rejects_action_prepared_after_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            value = public.read_external_authority_request(
                self.make_wave_run(Path(temporary), "exact_natal")
            )
            changed = deepcopy(value)
            action = changed["ordered_actions"][0]
            action["binding"]["prepared_state_revision"] = (
                changed["observation"]["operator_state_revision"] + 1
            )
            action["binding_sha256"] = hashlib.sha256(json.dumps(
                action["binding"], ensure_ascii=False, sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
            changed["initial_wave"]["ordered_member_binding_sha256s"][0] = action[
                "binding_sha256"
            ]
            body = {
                key: item for key, item in changed.items()
                if key != "external_authority_request_sha256"
            }
            changed["external_authority_request_sha256"] = hashlib.sha256(json.dumps(
                body, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
            with self.assertRaisesRegex(public.InitialWaveError, "basis is invalid"):
                public.validate_external_authority_request(changed)

    def test_cli_exports_request_and_rejects_workspace_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = self.make_wave_run(root, "exact_natal")
            output = root / "api" / "external-authority-request.json"
            with (
                patch("sys.argv", [
                    "astrowoof-external-authority", "--run-dir", str(run_dir),
                    "--output", str(output),
                ]),
                redirect_stdout(io.StringIO()) as stdout,
            ):
                main()
            expected = public.read_external_authority_request(run_dir)
            self.assertEqual(expected, json.loads(output.read_text(encoding="utf-8")))
            self.assertEqual(expected, json.loads(stdout.getvalue()))
            with (
                patch("sys.argv", [
                    "astrowoof-external-authority", "--run-dir", str(run_dir),
                    "--output", str(run_dir / "unsafe.json"),
                ]),
                self.assertRaises(public.InitialWaveError) as caught,
            ):
                main()
            self.assertEqual("unsafe_output_path", caught.exception.reason_code)

            with (
                patch("sys.argv", [
                    "astrowoof-external-authority", "--validate-request",
                    str(output),
                ]),
                redirect_stdout(io.StringIO()) as validated,
            ):
                main()
            self.assertEqual(expected, json.loads(validated.getvalue()))

    def test_public_surface_and_schema_are_installed_provider_free(self) -> None:
        expected = {
            "build_external_authority_request", "read_external_authority_request",
            "read_external_authority_schema", "validate_external_authority_request",
            "validate_external_authority_grant",
        }
        self.assertTrue(expected <= set(public.__all__))
        schema = public.read_external_authority_schema()
        self.assertEqual("astrowoof.external_authority_contracts.v1", schema["$id"])


if __name__ == "__main__":
    unittest.main()
