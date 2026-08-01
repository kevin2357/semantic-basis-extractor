from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from author_semantic_closure import (  # noqa: E402
    AuthoringProviderError,
    FIELD_PATTERN,
    FakeAuthoringProvider,
    OpenAIResponsesProvider,
    OpenAIServiceError,
    PassSpec,
    ProviderResult,
    apply_deck_fields,
    apply_authored_fields,
    authoring_output_schema,
    author_pending_passes,
    discover_passes,
    editable_deck_fields,
    estimated_cost,
    finalize_subjects,
    initial_run_state,
    load_json,
    normalized_usage,
    polish_subject,
    resume_run,
    safe_extract_zip,
    save_state,
    update_run_status,
    writable_fields,
)
from build_projected_semantic_basis import (  # noqa: E402
    build_candidates,
    build_story_workspace,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    optimize,
)
from validate_astrowoof_editorial import BAD_SECOND_PERSON  # noqa: E402


EXAMPLES = ROOT / "examples"


def authored_field_payload(workspace: Path) -> dict:
    result = {}
    ordinal = 0
    for relative_path, fields in writable_fields(workspace).items():
        result[relative_path] = {}
        for field in fields:
            ordinal += 1
            result[relative_path][field] = (
                f"Fresh authored value {ordinal} for {field}."
            )
    return {"files": result}


def completed_response(
    authored: dict,
    *,
    response_id: str = "resp_test",
) -> dict:
    return {
        "id": response_id,
        "status": "completed",
        "model": "gpt-5.6-terra",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": json.dumps(authored),
                    }
                ],
            }
        ],
        "usage": {
            "input_tokens": 1000,
            "input_tokens_details": {"cached_tokens": 200},
            "output_tokens": 500,
            "output_tokens_details": {"reasoning_tokens": 100},
            "total_tokens": 1500,
        },
    }


class ScriptedTransport:
    def __init__(self, results: list[dict | Exception]) -> None:
        self.results = list(results)
        self.calls: list[dict] = []

    def request_json(self, **kwargs):
        self.calls.append(kwargs)
        if not self.results:
            raise AssertionError("Unexpected transport call")
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class FeedbackRecordingProvider(FakeAuthoringProvider):
    def __init__(self) -> None:
        super().__init__(reject_attempts={"bre_1": 1})
        self.feedback: list[dict | None] = []

    def author(
        self,
        source_workspace,
        response_workspace,
        spec,
        attempt_number,
        feedback=None,
    ):
        self.feedback.append(feedback)
        return super().author(
            source_workspace,
            response_workspace,
            spec,
            attempt_number,
            feedback,
        )


class ConcurrentTrackingProvider(FakeAuthoringProvider):
    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        self.active = 0
        self.peak = 0

    def author(
        self,
        source_workspace,
        response_workspace,
        spec,
        attempt_number,
        feedback=None,
    ):
        with self._lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
        try:
            time.sleep(0.03)
            return super().author(
                source_workspace,
                response_workspace,
                spec,
                attempt_number,
                feedback,
            )
        finally:
            with self._lock:
                self.active -= 1


class SemanticClosureFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packages = discover_subject_packages(EXAMPLES, "bre")
        contexts, registry, input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )
        candidates, analysis = build_candidates(contexts)
        selected, rejected, _ = optimize(candidates)
        cls.packet = compile_packet(
            "bre",
            contexts,
            selected,
            rejected,
            analysis,
            registry,
            input_audit,
        )

    def make_passes(
        self,
        root: Path,
        *,
        count: int = 6,
        cards_per_pass: int = 2,
    ) -> tuple[dict, list[PassSpec], Path]:
        bundle = root / "bundle"
        bundle.mkdir()
        for number in range(1, count + 1):
            workspace = root / f"bre_{number}"
            if number <= 5:
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    cards_per_pass,
                    card_start=(number - 1) * cards_per_pass + 1,
                    pass_number=number,
                    pass_count=6,
                )
            else:
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    0,
                    card_start=cards_per_pass * 5 + 1,
                    include_summaries=True,
                    include_theme_plan=True,
                    pass_number=6,
                    pass_count=6,
                )
            archive = bundle / f"bre_{number}.zip"
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
                for path in sorted(workspace.rglob("*")):
                    if path.is_file():
                        handle.write(
                            path,
                            (Path(workspace.name) / path.relative_to(workspace)),
                        )
        manifest = {
            "status": "pass",
            "subject_count": 1,
            "subjects": [{"subject": "bre", "status": "pass"}],
        }
        specs = discover_passes(manifest, bundle) if count == 6 else []
        return manifest, specs, bundle

    def make_state(
        self,
        root: Path,
        provider: FakeAuthoringProvider,
        *,
        max_attempts: int = 3,
    ) -> tuple[dict, Path]:
        manifest, specs, _ = self.make_passes(root)
        run_dir = root / "run"
        run_dir.mkdir()
        state = initial_run_state(
            input_package=EXAMPLES,
            run_dir=run_dir,
            provider=provider,
            max_attempts=max_attempts,
            sbe_manifest=manifest,
            specs=specs,
        )
        run_json = run_dir / "run.json"
        save_state(run_json, state)
        return state, run_json


class TestSemanticClosure(SemanticClosureFixture):
    def test_second_person_validator_allows_object_of_preposition(self) -> None:
        self.assertIsNone(BAD_SECOND_PERSON.search("the rest of you has paused"))
        self.assertIsNotNone(BAD_SECOND_PERSON.search("you has paused"))

    def test_polish_transport_can_only_change_reader_facing_fields(self) -> None:
        fields = editable_deck_fields(self.packet)
        authored = {
            "fields": {
                path: f"Polished {index}."
                for index, path in enumerate(fields, start=1)
            }
        }
        polished = apply_deck_fields(self.packet, authored)
        self.assertEqual(
            self.packet["cards"][0]["evidence"],
            polished["cards"][0]["evidence"],
        )
        self.assertNotEqual(
            self.packet["cards"][0]["card"]["no_astro"]["body"]["handler"],
            polished["cards"][0]["card"]["no_astro"]["body"]["handler"],
        )
        incomplete = {"fields": dict(authored["fields"])}
        incomplete["fields"].pop(next(iter(incomplete["fields"])))
        with self.assertRaisesRegex(ValueError, "exactly match"):
            apply_deck_fields(self.packet, incomplete)

    def test_polish_transport_exposes_theme_groups_only_when_requested(
        self,
    ) -> None:
        normal = editable_deck_fields(self.packet)
        rebalancing = editable_deck_fields(
            self.packet,
            include_theme_groups=True,
        )
        self.assertFalse(any(path.endswith(".theme_group") for path in normal))
        self.assertTrue(
            any(path.endswith(".theme_group") for path in rebalancing)
        )

    def test_polish_resumes_from_persisted_final_failure_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final_root = root / "final" / "bre"
            final_root.mkdir(parents=True)
            deck_path = final_root / "natal.bre.cards.json"
            deck_path.write_text(json.dumps(self.packet), encoding="utf-8")
            assembly_path = final_root / "assembly.json"
            assembly_path.write_text("{}", encoding="utf-8")
            validation_path = final_root / "validation.json"
            validation_path.write_text(
                json.dumps({"errors": ["theme groups need rebalancing"]}),
                encoding="utf-8",
            )
            lint_path = final_root / "lint.json"
            lint_path.write_text(
                json.dumps({"warning_count": 2, "warnings": []}),
                encoding="utf-8",
            )
            record = {
                "subject": "bre",
                "state": "FINAL_QA_FAILED",
                "deck": str(deck_path),
                "assembly_report": str(assembly_path),
                "validation_report": str(validation_path),
                "lint_report": str(lint_path),
                "baseline_warning_count": 2,
                "polish_attempts": [],
                "delivery": None,
            }

            class Provider:
                model = "fake-polish"

                def complete_json(inner_self, **kwargs):
                    fields = editable_deck_fields(
                        self.packet,
                        include_theme_groups=True,
                    )
                    return {"fields": fields}, {"provider": "fake"}

            def fake_qa(command, report_path, *, accepted_returncodes):
                if "validate_astrowoof_editorial.py" in command[1]:
                    report = {"status": "pass", "warnings": []}
                else:
                    report = {"status": "pass", "warning_count": 0}
                report_path.write_text(json.dumps(report), encoding="utf-8")
                return {
                    "accepted": True,
                    "returncode": 0,
                    "stdout": "",
                    "stderr": "",
                    "report": report,
                }

            with patch(
                "author_semantic_closure.run_json_command",
                side_effect=fake_qa,
            ):
                polish_subject(
                    record=record,
                    provider=Provider(),
                    run_dir=root,
                    python_executable=Path(sys.executable),
                    max_attempts=1,
                )
            self.assertEqual("DELIVERY_COMPLETE", record["state"])
            self.assertTrue(record["polish_attempts"][0]["accepted"])
            self.assertTrue(Path(record["delivery"]).is_file())

    def test_final_status_requires_every_subject_delivery(self) -> None:
        state = {
            "status": "AUTHORING_COMPLETE",
            "passes": {
                "bre_1": {
                    "state": "PASS_QA_ACCEPTED",
                    "attempts": [],
                }
            },
            "subjects": {
                "bre": {"state": "DELIVERY_COMPLETE", "polish_attempts": []},
                "kevin": {"state": "FINAL_QA_WARN", "polish_attempts": []},
            },
        }
        update_run_status(state)
        self.assertEqual("FINAL_QA_REQUIRES_REVIEW", state["status"])
        state["subjects"]["kevin"]["state"] = "DELIVERY_COMPLETE"
        update_run_status(state)
        self.assertEqual("DELIVERY_COMPLETE", state["status"])

    def test_finalize_packages_clean_subject_and_preserves_warning_review(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            delivery_sources = []
            for number in range(4):
                path = root / f"source-{number}.json"
                path.write_text("{}\n", encoding="utf-8")
                delivery_sources.append(path)
            state = {
                "passes": {
                    f"bre_{number}": {
                        "subject": "bre",
                        "pass_number": number,
                        "state": "PASS_QA_ACCEPTED",
                    }
                    for number in range(1, 7)
                },
                "subjects": {},
            }
            clean = {
                "subject": "bre",
                "state": "FINAL_QA_PASSED",
                "deck": str(delivery_sources[0]),
                "assembly_report": str(delivery_sources[1]),
                "validation_report": str(delivery_sources[2]),
                "lint_report": str(delivery_sources[3]),
                "polish_attempts": [],
            }
            with patch(
                "author_semantic_closure.assemble_subject",
                return_value=clean,
            ):
                finalize_subjects(
                    state=state,
                    run_dir=root,
                    python_executable=Path(sys.executable),
                    allow_lint_warnings=False,
                )
            self.assertEqual(
                "DELIVERY_COMPLETE",
                state["subjects"]["bre"]["state"],
            )
            self.assertTrue(
                Path(state["subjects"]["bre"]["delivery"]).is_file()
            )

    def test_token_free_full_deck_assembles_validates_and_packages(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest, specs, _ = self.make_passes(
                root,
                cards_per_pass=10,
            )
            run_dir = root / "run"
            run_dir.mkdir()
            packet_root = (
                run_dir / "sbe" / "semantic-basis-output" / "bre"
            )
            packet_root.mkdir(parents=True)
            (packet_root / "bre.selected-authoring-packet.json").write_text(
                json.dumps(self.packet),
                encoding="utf-8",
            )
            provider = FakeAuthoringProvider()
            state = initial_run_state(
                input_package=EXAMPLES,
                run_dir=run_dir,
                provider=provider,
                max_attempts=1,
                sbe_manifest=manifest,
                specs=specs,
            )
            run_json = run_dir / "run.json"
            save_state(run_json, state)
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=run_dir,
                max_attempts=1,
                python_executable=Path(sys.executable),
                run_json=run_json,
                max_workers=6,
            )
            finalize_subjects(
                state=state,
                run_dir=run_dir,
                python_executable=Path(sys.executable),
                allow_lint_warnings=True,
            )
            save_state(run_json, state)
            self.assertIn(
                state["status"],
                {"DELIVERY_COMPLETE", "DELIVERY_COMPLETE_WITH_WARNINGS"},
            )
            final = state["subjects"]["bre"]
            self.assertTrue(Path(final["deck"]).is_file())
            self.assertTrue(Path(final["delivery"]).is_file())
            self.assertEqual(
                50,
                len(load_json(Path(final["deck"]))["cards"]),
            )

    def test_openai_provider_reconstructs_structured_fields_and_accounts_usage(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_passes(root)
            source = root / "bre_1"
            authored = authored_field_payload(source)
            transport = ScriptedTransport([completed_response(authored)])
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                background=False,
                transport=transport,
                sleep=lambda _: None,
            )
            response_workspace = (
                root
                / "run"
                / "passes"
                / "bre_1"
                / "attempt-001"
                / "response"
                / "bre_1"
            )
            spec = PassSpec(
                pass_id="bre_1",
                subject="bre",
                pass_number=1,
                source_zip=root / "bundle" / "bre_1.zip",
                source_sha256="source-hash",
            )
            before = (source / "START HERE.md").read_text(encoding="utf-8")
            result = provider.author(
                source,
                response_workspace,
                spec,
                1,
            )
            self.assertEqual(response_workspace, result.workspace)
            self.assertEqual(
                before,
                (response_workspace / "START HERE.md").read_text(
                    encoding="utf-8"
                ),
            )
            for path in response_workspace.rglob("WRITE*.md"):
                marked_values = [
                    match.group(3)
                    for match in FIELD_PATTERN.finditer(
                        path.read_text(encoding="utf-8")
                    )
                ]
                self.assertTrue(
                    all("__WRITE__" not in value for value in marked_values)
                )
            self.assertEqual(
                {
                    "input_tokens": 1000,
                    "cached_input_tokens": 200,
                    "cache_write_tokens": 0,
                    "output_tokens": 500,
                    "reasoning_tokens": 100,
                    "total_tokens": 1500,
                },
                result.metadata["usage"],
            )
            self.assertEqual(
                0.00955,
                result.metadata["estimated_cost"]["estimated_amount"],
            )
            request = transport.calls[0]["payload"]
            self.assertEqual("json_schema", request["text"]["format"]["type"])
            self.assertEqual(
                set(writable_fields(source)),
                set(
                    request["text"]["format"]["schema"]["properties"][
                        "files"
                    ]["properties"]
                ),
            )

    def test_openai_background_polling_retries_transient_transport_errors(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_passes(root)
            source = root / "bre_1"
            authored = authored_field_payload(source)
            sleeps: list[float] = []
            transport = ScriptedTransport(
                [
                    OpenAIServiceError("rate limited", retryable=True),
                    {
                        "id": "resp_background",
                        "status": "in_progress",
                    },
                    {"id": "resp_background", "status": "queued"},
                    completed_response(
                        authored,
                        response_id="resp_background",
                    ),
                ]
            )
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                transport=transport,
                poll_interval_seconds=0.25,
                transport_backoff_seconds=0.5,
                sleep=sleeps.append,
            )
            result = provider.author(
                source,
                (
                    root
                    / "run"
                    / "passes"
                    / "bre_1"
                    / "attempt-001"
                    / "response"
                    / "bre_1"
                ),
                PassSpec(
                    "bre_1",
                    "bre",
                    1,
                    root / "bundle" / "bre_1.zip",
                    "hash",
                ),
                1,
            )
            self.assertEqual("resp_background", result.metadata["response_id"])
            self.assertEqual(2, result.metadata["poll_count"])
            self.assertEqual(
                {"create": 2, "retrieve": 2},
                result.metadata["transport_attempts"],
            )
            self.assertEqual([0.5, 0.25, 0.25], sleeps)
            self.assertEqual(
                ["POST", "POST", "GET", "GET"],
                [call["method"] for call in transport.calls],
            )
            self.assertEqual(
                transport.calls[0]["headers"]["Idempotency-Key"],
                transport.calls[1]["headers"]["Idempotency-Key"],
            )

    def test_completed_malformed_output_preserves_billable_metadata(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_passes(root)
            source = root / "bre_1"
            malformed = completed_response({})
            malformed["output"][0]["content"][0]["text"] = "not json"
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                background=False,
                transport=ScriptedTransport([malformed]),
                sleep=lambda _: None,
            )
            with self.assertRaises(AuthoringProviderError) as raised:
                provider.author(
                    source,
                    (
                        root
                        / "run"
                        / "passes"
                        / "bre_1"
                        / "attempt-001"
                        / "response"
                        / "bre_1"
                    ),
                    PassSpec(
                        "bre_1",
                        "bre",
                        1,
                        root / "bundle" / "bre_1.zip",
                        "hash",
                    ),
                    1,
                )
            self.assertEqual(
                "resp_test",
                raised.exception.metadata["response_id"],
            )
            self.assertEqual(
                1500,
                raised.exception.metadata["usage"]["total_tokens"],
            )

    def test_interrupted_background_attempt_resumes_without_new_post(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider_for_state = FakeAuthoringProvider()
            state, run_json = self.make_state(root, provider_for_state)
            record = state["passes"]["bre_1"]
            attempt_root = (
                root / "run" / "passes" / "bre_1" / "attempt-001"
            )
            attempt_root.mkdir(parents=True)
            (attempt_root / "openai-background-response.json").write_text(
                json.dumps(
                    {"id": "resp_resume", "status": "in_progress"}
                ),
                encoding="utf-8",
            )
            record["state"] = "SUBMITTED"
            record["attempts"] = [
                {
                    "attempt_number": 1,
                    "state": "SUBMITTED",
                    "started_at": "2026-07-31T00:00:00+00:00",
                    "finished_at": None,
                    "response_workspace": str(
                        attempt_root / "response" / "bre_1"
                    ),
                    "provider_metadata": None,
                    "qa": None,
                    "error": None,
                }
            ]
            for pass_id, other in state["passes"].items():
                if pass_id != "bre_1":
                    other["state"] = "PASS_QA_ACCEPTED"
                    other["accepted_workspace"] = str(
                        root / "accepted-placeholder" / pass_id
                    )
                    other["accepted_attempt"] = 1
            save_state(run_json, state)
            source_zip = Path(record["source_zip"])
            with tempfile.TemporaryDirectory() as extracted:
                with zipfile.ZipFile(source_zip) as archive:
                    archive.extractall(extracted)
                authored = authored_field_payload(
                    Path(extracted) / "bre_1"
                )
            transport = ScriptedTransport(
                [
                    completed_response(
                        authored,
                        response_id="resp_resume",
                    )
                ]
            )
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                transport=transport,
                sleep=lambda _: None,
            )
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                max_workers=1,
            )
            persisted = load_json(run_json)
            resumed = persisted["passes"]["bre_1"]
            self.assertEqual("PASS_QA_ACCEPTED", resumed["state"])
            self.assertEqual(1, resumed["accepted_attempt"])
            self.assertEqual(1, len(resumed["attempts"]))
            self.assertEqual(["GET"], [call["method"] for call in transport.calls])
            self.assertEqual(
                0,
                resumed["attempts"][0]["provider_metadata"][
                    "transport_attempts"
                ]["create"],
            )

    def test_fatal_service_configuration_error_does_not_burn_retries(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, run_json = self.make_state(
                root,
                FakeAuthoringProvider(),
            )
            state["passes"] = {"bre_1": state["passes"]["bre_1"]}
            save_state(run_json, state)
            transport = ScriptedTransport(
                [
                    OpenAIServiceError(
                        "invalid request",
                        status_code=400,
                        fatal=True,
                    )
                ]
            )
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                transport=transport,
                sleep=lambda _: None,
            )
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
            )
            record = load_json(run_json)["passes"]["bre_1"]
            self.assertEqual("FAILED_REQUIRES_REVIEW", record["state"])
            self.assertEqual(1, len(record["attempts"]))
            self.assertEqual(
                "OpenAIServiceError",
                record["attempts"][0]["error"]["type"],
            )

    def test_output_schema_and_reconstruction_reject_shape_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_passes(root)
            source = root / "bre_1"
            fields = writable_fields(source)
            schema = authoring_output_schema(fields)
            self.assertFalse(schema["additionalProperties"])
            self.assertEqual(
                list(fields),
                schema["properties"]["files"]["required"],
            )
            authored = authored_field_payload(source)
            authored["files"].pop(next(iter(authored["files"])))
            with self.assertRaisesRegex(ValueError, "file mismatch"):
                apply_authored_fields(
                    source,
                    root / "response" / "bre_1",
                    authored,
                )

    def test_usage_and_cost_normalization_are_deterministic(self) -> None:
        response = completed_response({})
        usage = normalized_usage(response)
        cost = estimated_cost("gpt-5.6-terra", usage)
        self.assertEqual(1500, usage["total_tokens"])
        self.assertEqual(0.00955, cost["estimated_amount"])
        self.assertIsNone(estimated_cost("unknown-model", usage))

    def test_discovers_exactly_six_integral_pass_archives(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, specs, _ = self.make_passes(root)
            self.assertEqual(
                [f"bre_{number}" for number in range(1, 7)],
                [spec.pass_id for spec in specs],
            )
            self.assertTrue(all(len(spec.source_sha256) == 64 for spec in specs))

    def test_rejects_unsafe_zip_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("../escape.txt", "nope")
            with self.assertRaisesRegex(ValueError, "Unsafe ZIP member"):
                safe_extract_zip(archive, root / "extract")

    def test_fake_provider_completes_all_passes_and_persists_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FakeAuthoringProvider()
            state, run_json = self.make_state(root, provider)
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
            )
            persisted = load_json(run_json)
            self.assertEqual("AUTHORING_COMPLETE", persisted["status"])
            for record in persisted["passes"].values():
                self.assertEqual("PASS_QA_ACCEPTED", record["state"])
                self.assertEqual(1, record["accepted_attempt"])
                self.assertTrue(Path(record["accepted_workspace"]).is_dir())
                self.assertEqual(
                    "accept",
                    record["attempts"][0]["qa"]["report"]["status"],
                )

    def test_qa_rejection_retries_fresh_and_then_accepts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FeedbackRecordingProvider()
            state, run_json = self.make_state(root, provider)
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
            )
            record = load_json(run_json)["passes"]["bre_1"]
            self.assertEqual(
                ["PASS_QA_REJECTED", "PASS_QA_ACCEPTED"],
                [attempt["state"] for attempt in record["attempts"]],
            )
            self.assertEqual(2, record["accepted_attempt"])
            self.assertNotEqual(
                record["attempts"][0]["response_workspace"],
                record["attempts"][1]["response_workspace"],
            )
            self.assertIsNone(provider.feedback[0])
            self.assertEqual(
                "editorial_qa_rejection",
                provider.feedback[1]["kind"],
            )
            self.assertIn(
                "cross_card_exact_duplicate",
                provider.feedback[1]["editorial_issue_codes"],
            )

    def test_passes_can_execute_concurrently_without_corrupting_ledger(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = ConcurrentTrackingProvider()
            state, run_json = self.make_state(root, provider)
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                max_workers=6,
            )
            persisted = load_json(run_json)
            self.assertEqual("AUTHORING_COMPLETE", persisted["status"])
            self.assertGreaterEqual(provider.peak, 2)
            self.assertEqual(
                {"PASS_QA_ACCEPTED"},
                {
                    record["state"]
                    for record in persisted["passes"].values()
                },
            )

    def test_resume_skips_accepted_pass_and_continues_remaining(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FakeAuthoringProvider()
            state, run_json = self.make_state(root, provider)
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                stop_after_attempts=1,
            )
            first_record = load_json(run_json)["passes"]["bre_1"]
            accepted_workspace = first_record["accepted_workspace"]
            resumed, resumed_json = resume_run(
                run_dir=root / "run",
                provider=provider,
                max_attempts=3,
            )
            author_pending_passes(
                state=resumed,
                provider=provider,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=resumed_json,
            )
            persisted = load_json(run_json)
            self.assertEqual("AUTHORING_COMPLETE", persisted["status"])
            self.assertEqual(
                accepted_workspace,
                persisted["passes"]["bre_1"]["accepted_workspace"],
            )
            self.assertEqual(1, len(persisted["passes"]["bre_1"]["attempts"]))

    def test_exhausted_attempts_become_terminal_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FakeAuthoringProvider(error_attempts={"bre_1": 5})
            state, run_json = self.make_state(
                root,
                provider,
                max_attempts=2,
            )
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=root / "run",
                max_attempts=2,
                python_executable=Path(sys.executable),
                run_json=run_json,
            )
            persisted = load_json(run_json)
            self.assertEqual("FAILED_REQUIRES_REVIEW", persisted["status"])
            failed = persisted["passes"]["bre_1"]
            self.assertEqual("FAILED_REQUIRES_REVIEW", failed["state"])
            self.assertEqual(2, len(failed["attempts"]))
            self.assertTrue(
                all(
                    attempt["state"] == "ATTEMPT_ERROR"
                    for attempt in failed["attempts"]
                )
            )

    def test_atomic_state_write_survives_interrupted_replace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FakeAuthoringProvider()
            state, run_json = self.make_state(root, provider)
            original = json.loads(run_json.read_text(encoding="utf-8"))
            with patch("pathlib.Path.replace", side_effect=OSError("interrupted")):
                with self.assertRaisesRegex(OSError, "interrupted"):
                    save_state(run_json, state)
            self.assertEqual(
                original,
                json.loads(run_json.read_text(encoding="utf-8")),
            )


if __name__ == "__main__":
    unittest.main()
