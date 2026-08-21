from __future__ import annotations

import tempfile
import unittest
import sys
import io
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (
    OpenAIResponsesProvider,
    load_json,
    prepare_exact_interactive_initial_wave,
    save_state,
    write_json_atomic,
    main as closure_main,
)
from astrowoof_natal_authoring.initial_wave import (
    INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
    InitialWaveError,
)
from astrowoof_natal_authoring.external_authority import (
    read_external_authority_request,
)
from astrowoof_natal_authoring.lifecycle import inspect_lifecycle
from astrowoof_natal_authoring.reconciliation import initial_timing
from astrowoof_natal.tests.test_semantic_closure import SemanticClosureFixture


class TestInitialWaveLineageFence(SemanticClosureFixture):
    def provider(self) -> OpenAIResponsesProvider:
        return OpenAIResponsesProvider(
            api_key="test-key", model="gpt-5.6-luna",
            max_output_tokens=30_000, prompt_cache_mode="disabled",
            require_spend_authorization=True,
        )

    def prepared(self, root: Path) -> tuple[dict, Path, OpenAIResponsesProvider]:
        provider = self.provider()
        state, run_json = self.make_state(root, provider)
        prepare_exact_interactive_initial_wave(
            state=state, provider=provider, run_dir=root / "run", run_json=run_json,
        )
        save_state(run_json, state)
        return state, run_json, provider

    def assert_refused_without_state_mutation(
        self, state: dict, run_json: Path, provider: OpenAIResponsesProvider,
    ) -> InitialWaveError:
        before = run_json.read_bytes()
        with self.assertRaises(InitialWaveError) as raised:
            prepare_exact_interactive_initial_wave(
                state=state, provider=provider, run_dir=run_json.parent,
                run_json=run_json,
            )
        self.assertEqual("initial_wave_lineage_unjoinable", raised.exception.reason_code)
        self.assertEqual(before, run_json.read_bytes())
        return raised.exception

    def test_orphaned_historical_evidence_never_prepares_second_wave(self) -> None:
        for case in ("provider", "consumption", "reported", "ambiguity"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                state, run_json, provider = self.prepared(root)
                state.pop("initial_authoring_wave")
                for record in state["passes"].values():
                    record["attempts"] = []
                    record["state"] = "PENDING"
                action = state["spend_ledger"]["actions"][0]
                if case == "provider":
                    action["provider"] = {"kind": "response", "id": "resp_prior"}
                elif case == "consumption":
                    action["consumption"] = {"consumer_id": "prior", "state_revision": 1}
                elif case == "reported":
                    action["reported"] = {"usage": {}, "estimated_micro_usd": 1}
                else:
                    action["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                    action["ambiguity"] = {"reason": "prior identity gap"}
                save_state(run_json, state)
                error = self.assert_refused_without_state_mutation(
                    state, run_json, provider,
                )
                self.assertIn("prior_initial_action", error.evidence_categories)
                expected = {
                    "provider": "prior_provider_identity",
                    "consumption": "prior_consumption",
                    "reported": "prior_consumption",
                    "ambiguity": "ambiguous_lineage",
                }[case]
                self.assertIn(expected, error.evidence_categories)
                self.assertEqual(6, len(state["spend_ledger"]["actions"]))

    def test_stored_wave_requires_complete_exact_join_evidence(self) -> None:
        for case in ("missing_bundle", "changed_payload", "duplicate_action", "missing_attempt"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                state, run_json, provider = self.prepared(root)
                member = state["initial_authoring_wave"]["ordered_members"][0]
                if case == "missing_bundle":
                    (run_json.parent / INITIAL_WAVE_BINDING_BUNDLE_FILENAME).unlink()
                    save_state(run_json, state)
                elif case == "changed_payload":
                    request = state["initial_authoring_wave"]["requests"][member["action_id"]]
                    payload = load_json(Path(request["request_payload_path"]))
                    payload["model"] = "changed-model"
                    write_json_atomic(Path(request["request_payload_path"]), payload)
                    save_state(run_json, state)
                elif case == "duplicate_action":
                    state["spend_ledger"]["actions"].append(deepcopy(
                        state["spend_ledger"]["actions"][0]
                    ))
                    save_state(run_json, state)
                else:
                    state["passes"][member["pass_id"]]["attempts"] = []
                    save_state(run_json, state)
                error = self.assert_refused_without_state_mutation(
                    state, run_json, provider,
                )
                self.assertIn(
                    "missing_join_artifact" if case == "missing_bundle"
                    else "native_evidence_conflict",
                    error.evidence_categories,
                )

    def test_valid_stored_wave_is_reused_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json, provider = self.prepared(root)
            for index, member in enumerate(
                state["initial_authoring_wave"]["ordered_members"], 1,
            ):
                action = next(
                    item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == member["action_id"]
                )
                action["state"] = "WAITING"
                action["provider"] = {
                    "kind": "response", "id": f"resp_durable_{index}",
                }
                state["passes"][member["pass_id"]]["attempts"][0]["state"] = (
                    "WAITING_FOR_RESPONSE"
                )
            state["initial_authoring_wave"]["state"] = "DETACHED"
            save_state(run_json, state)
            original = deepcopy(state["initial_authoring_wave"])
            returned = prepare_exact_interactive_initial_wave(
                state=state, provider=provider, run_dir=run_json.parent,
                run_json=run_json,
            )
            self.assertEqual(original, returned)
            self.assertEqual(6, len(state["spend_ledger"]["actions"]))

    def test_public_reader_never_relabels_orphaned_initial_actions_as_ordinary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json, _provider = self.prepared(root)
            state.pop("initial_authoring_wave")
            for record in state["passes"].values():
                record["attempts"] = []
                record["state"] = "PENDING"
            save_state(run_json, state)
            with self.assertRaises(InitialWaveError) as raised:
                read_external_authority_request(run_json.parent)
            self.assertEqual(
                "initial_wave_lineage_unjoinable", raised.exception.reason_code,
            )
            self.assertIn("prior_initial_action", raised.exception.evidence_categories)

    def test_generic_resume_with_orphaned_pass_attempts_refuses_before_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json, _provider = self.prepared(root)
            state.pop("initial_authoring_wave")
            save_state(run_json, state)
            before_run = run_json.read_bytes()
            before_snapshot = (run_json.parent / "workspace-snapshot.json").read_bytes()
            calls: list[str] = []

            def forbidden_create(*_args: object, **_kwargs: object) -> tuple[dict, int]:
                calls.append("create")
                return {"id": "resp_forbidden", "status": "in_progress"}, 1

            argv = [
                "astrowoof-semantic-closure", "--run-dir", str(run_json.parent),
                "--resume", "--provider", "openai", "--service-level", "interactive",
                "--api-key-env", "SBE_SLICE4_FAKE_KEY", "--model", "gpt-5.6-luna",
                "--max-output-tokens", "30000", "--log-level", "CRITICAL",
                "--prompt-cache-mode", "disabled",
            ]
            with (
                patch.dict("os.environ", {"SBE_SLICE4_FAKE_KEY": "test-key"}),
                patch("sys.argv", argv),
                patch.object(
                    OpenAIResponsesProvider, "create_response_only", new=forbidden_create,
                ),
                redirect_stdout(io.StringIO()),
                self.assertRaises(InitialWaveError) as raised,
            ):
                closure_main()
            self.assertEqual("initial_wave_lineage_unjoinable", raised.exception.reason_code)
            self.assertIn("native_evidence_conflict", raised.exception.evidence_categories)
            self.assertEqual([], calls)
            self.assertEqual(before_run, run_json.read_bytes())
            self.assertEqual(
                before_snapshot, (run_json.parent / "workspace-snapshot.json").read_bytes(),
            )

    def test_lifecycle_v05_embeds_exact_initial_wave_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json, _provider = self.prepared(root)
            inspection = inspect_lifecycle(
                run_json.parent, native_exclusive_access="declared",
                observed_at="2026-08-20T18:00:00Z",
            )
            request = inspection["external_authority_request"]
            self.assertEqual("astrowoof.authoring_lifecycle_inspection.v0.5", inspection[
                "schema_version"
            ])
            self.assertIsNone(inspection["external_authority_refusal"])
            self.assertEqual(inspection["run_id"], request["run_id"])
            self.assertEqual(inspection["observation"], request["observation"])
            self.assertEqual(
                request["ordered_action_ids"], inspection["execution_branch"]["action_ids"],
            )
            self.assertEqual(
                "await_external_authority", inspection["execution_branch"]["command"],
            )

    def test_lifecycle_v05_embeds_orphaned_provider_lineage_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json, _provider = self.prepared(root)
            state.pop("initial_authoring_wave")
            action = state["spend_ledger"]["actions"][0]
            action["state"] = "WAITING"
            action["provider"] = {"kind": "response", "id": "resp_orphaned"}
            action["provider_reconciliation"] = initial_timing(
                recorded_at="2026-08-20T17:00:00Z", mechanism="response",
            )
            save_state(run_json, state)
            inspection = inspect_lifecycle(
                run_json.parent, native_exclusive_access="declared",
                observed_at="2026-08-20T18:00:00Z",
            )
            refusal = inspection["external_authority_refusal"]
            self.assertIsNone(inspection["external_authority_request"])
            self.assertEqual(
                "initial_wave_lineage_unjoinable", refusal["reason_code"],
            )
            self.assertIn("prior_provider_identity", refusal["evidence_categories"])
            self.assertEqual("none", inspection["execution_branch"]["command"])
            self.assertEqual(
                "retain_for_review", inspection["execution_capacity"]["disposition"],
            )


if __name__ == "__main__":
    unittest.main()
