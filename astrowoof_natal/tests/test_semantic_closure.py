from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import unittest
import zipfile
from copy import deepcopy
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
    RoutedOpenAIProvider,
    apply_deck_fields,
    apply_sparse_polish,
    apply_authored_fields,
    authoring_output_schema,
    author_pending_passes,
    author_pending_passes_batch,
    batch_estimated_cost,
    build_prompt_layout_report,
    compare_cost_runs,
    discover_passes,
    editable_deck_fields,
    estimated_cost,
    estimated_text_tokens,
    finalize_subjects,
    fill_fake_workspace,
    initial_run_state,
    load_json,
    normalized_usage,
    polish_subject,
    polish_target_paths,
    provider_configuration,
    prompt_cache_manifest,
    resume_run,
    safe_extract_zip,
    sanitize_context_filters,
    save_state,
    select_cache_warmer,
    sparse_polish_output_schema,
    sparse_polish_transport_metrics,
    update_run_status,
    workspace_file_inventory,
    writable_fields,
    _fake_field_value,
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
from lint_authoring_pass import invalid_context_filter_claim_ids  # noqa: E402


EXAMPLES = ROOT / "examples"


def authored_field_payload(workspace: Path) -> dict:
    result = {}
    ordinal = 0
    for relative_path, fields in writable_fields(workspace).items():
        result[relative_path] = {}
        for field in fields:
            ordinal += 1
            if field == "context_filter_groups.high_level":
                value = "Personality"
            elif field == "context_filter_groups.detail_level":
                value = "Core Personality"
            else:
                value = f"Fresh authored value {ordinal} for {field}."
            result[relative_path][field] = value
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


class ScriptedBatchTransport:
    def __init__(self, *, initially_complete: bool = True) -> None:
        self.initially_complete = initially_complete
        self.lines: list[dict] = []
        self.retrieve_calls = 0

    def upload_jsonl(self, content: bytes, filename: str) -> dict:
        self.lines = [json.loads(line) for line in content.decode().splitlines()]
        return {"id": "file_input"}

    def create_batch(self, payload: dict) -> dict:
        return {
            "id": "batch_test",
            "status": "completed" if self.initially_complete else "in_progress",
            "output_file_id": "file_output" if self.initially_complete else None,
            "error_file_id": None,
        }

    def retrieve_batch(self, batch_id: str) -> dict:
        self.retrieve_calls += 1
        return {
            "id": batch_id,
            "status": "completed",
            "output_file_id": "file_output",
            "error_file_id": None,
            "request_counts": {
                "total": len(self.lines), "completed": len(self.lines), "failed": 0
            },
        }

    def download_file(self, file_id: str) -> str:
        output = []
        for index, line in enumerate(self.lines, 1):
            files_schema = line["body"]["text"]["format"]["schema"]["properties"]["files"]
            authored = {"files": {}}
            ordinal = 0
            for relative_path, file_schema in files_schema["properties"].items():
                authored["files"][relative_path] = {}
                for field in file_schema["properties"]:
                    ordinal += 1
                    authored["files"][relative_path][field] = _fake_field_value(
                        pass_id=line["custom_id"],
                        relative_file=relative_path,
                        field=field,
                        ordinal=ordinal,
                    )
            output.append(json.dumps({
                "custom_id": line["custom_id"],
                "response": {
                    "status_code": 200,
                    "body": completed_response(
                        authored, response_id=f"resp_batch_{index}"
                    ),
                },
                "error": None,
            }))
        return "\n".join(output) + "\n"


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
    def test_summary_gold_and_thesis_plan_are_pass_specific_assignment_inputs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_passes(root)
            card_pass = root / "bre_1"
            summary_pass = root / "bre_6"
            self.assertFalse((card_pass / "SUMMARY GOLD REFERENCE.md").exists())
            self.assertFalse(
                (card_pass / "WRITE SUMMARY THESIS PLAN.md").exists()
            )
            inventory = {
                item["path"]: item
                for item in workspace_file_inventory(summary_pass)
            }
            self.assertEqual(
                "assignment",
                inventory["SUMMARY GOLD REFERENCE.md"]["tier"],
            )
            self.assertEqual(
                "assignment",
                inventory["WRITE SUMMARY THESIS PLAN.md"]["tier"],
            )
            self.assertIn(
                "WRITE SUMMARY THESIS PLAN.md",
                writable_fields(summary_pass),
            )
            cache_manifest = prompt_cache_manifest(
                discover_passes(
                    {
                        "status": "pass",
                        "subject_count": 1,
                        "subjects": [{"subject": "bre", "status": "pass"}],
                    },
                    root / "bundle",
                )
            )
            self.assertIn("bre_6", cache_manifest["passes"])
            self.assertNotEqual(
                cache_manifest["passes"]["bre_1"]["assignment"],
                cache_manifest["passes"]["bre_6"]["assignment"],
            )

    def test_invalid_context_filter_is_caught_inside_authored_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "bre_1"
            build_story_workspace(
                workspace,
                self.packet,
                ROOT,
                1,
                card_start=1,
                pass_number=1,
                pass_count=6,
            )
            fill_fake_workspace(workspace)
            card_path = next(workspace.rglob("WRITE THIS CARD.md"))
            text = card_path.read_text(encoding="utf-8")
            text = text.replace(
                "<!-- BEGIN FIELD: context_filter_groups.high_level -->\nPersonality",
                "<!-- BEGIN FIELD: context_filter_groups.high_level -->\n- Emotions\n- Trust",
            )
            card_path.write_text(text, encoding="utf-8")
            invalid = invalid_context_filter_claim_ids(workspace)
            self.assertEqual(1, len(invalid))
            self.assertEqual(
                card_path.parent.name.split(" -- ", 1)[1], invalid[0]
            )

    def test_context_filter_sanitizer_removes_only_invalid_labels(self) -> None:
        deck = deepcopy(self.packet)
        deck["cards"][0]["context_filter_groups"] = {
            "high_level": ["Emotions", "Trust", "Trust", "Personality"],
            "detail_level": ["Emotions & Inner World", "Bogus Detail"],
        }
        repairs = sanitize_context_filters(deck)
        self.assertEqual(
            ["Trust", "Personality"],
            deck["cards"][0]["context_filter_groups"]["high_level"],
        )
        self.assertEqual(
            ["Emotions & Inner World"],
            deck["cards"][0]["context_filter_groups"]["detail_level"],
        )
        self.assertEqual(2, len(repairs))

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

    def test_sparse_polish_targets_only_reported_opening_fields(self) -> None:
        claim_ids = [card["claim_id"] for card in self.packet["cards"][:6]]
        lint_report = {
            "decks": [{
                "warnings": [{
                    "code": "repeated_opening",
                    "details": {
                        "field": "no_astro.body.direct_to_dog",
                        "opening": "you can see",
                        "claim_ids": claim_ids,
                    },
                }],
            }],
        }
        targets = polish_target_paths(
            self.packet,
            lint_report=lint_report,
            validation_report={"errors": []},
            include_theme_groups=False,
        )
        self.assertEqual(6, len(targets))
        self.assertTrue(all(
            path.endswith(".card.no_astro.body.direct_to_dog")
            for path in targets
        ))
        schema = sparse_polish_output_schema(targets)
        self.assertEqual(
            targets,
            schema["properties"]["edits"]["items"]["properties"]
            ["field_path"]["enum"],
        )
        metrics = sparse_polish_transport_metrics(
            self.packet,
            target_paths=targets,
            include_theme_groups=False,
        )
        self.assertLess(
            metrics["output_estimated_tokens"]["target_ceiling"],
            metrics["output_estimated_tokens"]["full_map"] * 0.2,
        )
        self.assertLess(
            metrics["input_estimated_tokens"]["sparse_transport"],
            metrics["input_estimated_tokens"]["full_map"] * 0.3,
        )

    def test_sparse_polish_rejects_locked_and_duplicate_paths(self) -> None:
        target = "cards.0.card.no_astro.body.handler"
        authored = {
            "edits": [{
                "field_path": target,
                "replacement": "A precise replacement.",
                "reason_codes": ["failure_signature"],
            }],
        }
        result = apply_sparse_polish(
            self.packet,
            authored,
            target_paths=[target],
            include_theme_groups=False,
        )
        self.assertEqual(
            self.packet["cards"][0]["evidence"],
            result["cards"][0]["evidence"],
        )
        locked = deepcopy(authored)
        locked["edits"][0]["field_path"] = "cards.0.evidence"
        with self.assertRaisesRegex(ValueError, "not editable"):
            apply_sparse_polish(
                self.packet,
                locked,
                target_paths=[target],
                include_theme_groups=False,
            )
        duplicate = {"edits": [authored["edits"][0], authored["edits"][0]]}
        with self.assertRaisesRegex(ValueError, "repeats field"):
            apply_sparse_polish(
                self.packet,
                duplicate,
                target_paths=[target],
                include_theme_groups=False,
            )

    def test_second_sparse_attempt_expands_only_affected_cards(self) -> None:
        claim_id = self.packet["cards"][0]["claim_id"]
        lint_report = {
            "decks": [{"warnings": [{
                "code": "repeated_opening",
                "details": {
                    "field": "no_astro.body.handler",
                    "claim_ids": [claim_id],
                },
            }]}],
        }
        narrow = polish_target_paths(
            self.packet,
            lint_report=lint_report,
            validation_report={"errors": []},
            include_theme_groups=False,
        )
        expanded = polish_target_paths(
            self.packet,
            lint_report=lint_report,
            validation_report={"errors": []},
            include_theme_groups=False,
            expand_related=True,
        )
        self.assertEqual(1, len(narrow))
        self.assertGreater(len(expanded), len(narrow))
        self.assertTrue(all(path.startswith("cards.0.") for path in expanded))

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
                json.dumps({
                    "warning_count": 2,
                    "decks": [{"warnings": [{
                        "code": "failure_signature",
                        "details": {
                            "location": "summary:card1",
                            "field": "no_astro.body.handler",
                        },
                    }]}],
                }),
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
            submitted: list[dict] = []
            qa_commands: list[list[str]] = []

            class Provider:
                model = "fake-polish"

                def complete_json(inner_self, **kwargs):
                    submitted.append(kwargs)
                    target_paths = kwargs["schema"]["properties"]["edits"][
                        "items"
                    ]["properties"]["field_path"]["enum"]
                    fields = editable_deck_fields(
                        self.packet, include_theme_groups=True
                    )
                    return {
                        "edits": [
                            {
                                "field_path": path,
                                "replacement": fields[path],
                                "reason_codes": ["theme_group_balance"],
                            }
                            for path in target_paths
                        ]
                    }, {"provider": "fake"}

            def fake_qa(command, report_path, *, accepted_returncodes):
                qa_commands.append(command)
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
            validation_command = next(
                command for command in qa_commands
                if "validate_astrowoof_editorial.py" in command[1]
            )
            self.assertIn("--allow-summary-edits", validation_command)
            self.assertEqual("astrowoof_sparse_polish", submitted[0]["schema_name"])
            transport = record["polish_attempts"][0]["transport"]
            self.assertLess(
                transport["editable_target_count"],
                transport["full_field_count"],
            )
            self.assertTrue(Path(record["delivery"]).is_file())

    def test_polish_preserves_partial_improvement_without_broad_expansion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final_root = root / "final" / "bre"
            final_root.mkdir(parents=True)
            deck_path = final_root / "natal.bre.cards.json"
            deck_path.write_text(json.dumps(self.packet), encoding="utf-8")
            assembly_path = final_root / "assembly.json"
            assembly_path.write_text("{}", encoding="utf-8")
            validation_path = final_root / "validation.json"
            validation_path.write_text(json.dumps({
                "status": "fail",
                "errors": [
                    "Theme groups need rebalancing.",
                    "A second structural problem remains.",
                ],
            }), encoding="utf-8")
            lint_path = final_root / "lint.json"
            lint_path.write_text(json.dumps({
                "status": "warn", "warning_count": 2, "decks": []
            }), encoding="utf-8")
            record = {
                "subject": "bre", "state": "FINAL_QA_FAILED",
                "deck": str(deck_path), "assembly_report": str(assembly_path),
                "validation_report": str(validation_path),
                "lint_report": str(lint_path), "baseline_warning_count": 2,
                "polish_attempts": [], "delivery": None,
            }

            class Provider:
                model = "fake-polish"
                reasoning_effort = "low"

                def complete_json(inner_self, **kwargs):
                    paths = kwargs["schema"]["properties"]["edits"]["items"][
                        "properties"
                    ]["field_path"]["enum"]
                    fields = editable_deck_fields(
                        self.packet, include_theme_groups=True
                    )
                    return {"edits": [{
                        "field_path": path,
                        "replacement": fields[path],
                        "reason_codes": ["theme_group_balance"],
                    } for path in paths]}, {"provider": "fake"}

            validation_calls = 0

            def fake_qa(command, report_path, *, accepted_returncodes):
                nonlocal validation_calls
                if "validate_astrowoof_editorial.py" in command[1]:
                    validation_calls += 1
                    report = (
                        {"status": "fail", "errors": [
                            "Theme groups need rebalancing."
                        ], "warnings": []}
                        if validation_calls == 1
                        else {"status": "pass", "errors": [], "warnings": []}
                    )
                    accepted = report["status"] == "pass"
                else:
                    report = {"status": "warn", "warning_count": 2, "decks": []}
                    accepted = True
                report_path.write_text(json.dumps(report), encoding="utf-8")
                return {
                    "accepted": accepted, "returncode": 0 if accepted else 2,
                    "stdout": "", "stderr": "", "report": report,
                }

            with patch(
                "author_semantic_closure.run_json_command", side_effect=fake_qa
            ):
                polish_subject(
                    record=record, provider=Provider(), run_dir=root,
                    python_executable=Path(sys.executable), max_attempts=2,
                )
            self.assertEqual(
                "POLISH_IMPROVED_PARTIAL",
                record["polish_attempts"][0]["state"],
            )
            self.assertTrue(record["polish_attempts"][0]["improved"])
            self.assertLess(
                record["polish_attempts"][1]["transport"]["editable_target_count"],
                100,
            )

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
            self.assertEqual(
                {"mode": "explicit", "ttl": "30m"},
                request["prompt_cache_options"],
            )
            self.assertTrue(request["prompt_cache_key"].startswith("astrowoof:"))
            user_blocks = request["input"][1]["content"]
            self.assertEqual(3, len(user_blocks))
            self.assertEqual(
                {"mode": "explicit"},
                user_blocks[0]["prompt_cache_breakpoint"],
            )
            self.assertEqual(
                {"mode": "explicit"},
                user_blocks[1]["prompt_cache_breakpoint"],
            )
            self.assertNotIn("prompt_cache_breakpoint", user_blocks[2])
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

    def test_model_router_escalates_only_creative_retries(self) -> None:
        class StubProvider:
            def __init__(inner_self, model, effort):
                inner_self.model = model
                inner_self.reasoning_effort = effort
                inner_self.background = True
                inner_self.base_url = "https://api.openai.com/v1"
                inner_self.max_output_tokens = 100_000
                inner_self.prompt_cache_mode = "explicit"
                inner_self.prompt_cache_ttl = "30m"
                inner_self.calls = []

            def author(inner_self, *args, **kwargs):
                inner_self.calls.append((args, kwargs))
                return ProviderResult(
                    workspace=args[1],
                    metadata={
                        "requested_model": inner_self.model,
                        "usage": {},
                    },
                )

        initial = StubProvider("gpt-5.6-luna", "medium")
        retry = StubProvider("gpt-5.6-terra", "medium")
        router = RoutedOpenAIProvider(initial=initial, retry=retry)
        spec = PassSpec("bre_1", "bre", 1, Path("bre_1.zip"), "hash")
        first = router.author(Path("source"), Path("first"), spec, 1)
        second = router.author(Path("source"), Path("second"), spec, 2)
        self.assertEqual(1, len(initial.calls))
        self.assertEqual(1, len(retry.calls))
        self.assertEqual("initial", first.metadata["routing"]["route"])
        self.assertEqual(
            "creative_retry", second.metadata["routing"]["route"]
        )
        configuration = provider_configuration(router)
        self.assertEqual("cost_optimized", configuration["routing_policy"])
        self.assertEqual(
            "gpt-5.6-luna", configuration["initial"]["model"]
        )
        self.assertEqual(
            "gpt-5.6-terra",
            configuration["creative_retry"]["model"],
        )

    def test_routed_provider_configuration_is_resume_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            router = RoutedOpenAIProvider(
                initial=OpenAIResponsesProvider(
                    api_key="unused", model="gpt-5.6-luna"
                ),
                retry=OpenAIResponsesProvider(
                    api_key="unused", model="gpt-5.6-terra"
                ),
            )
            _, run_json = self.make_state(root, router)
            resumed, resumed_path = resume_run(
                run_dir=run_json.parent,
                provider=router,
                max_attempts=3,
            )
            self.assertEqual(run_json, resumed_path)
            self.assertEqual(
                "cost_optimized",
                resumed["provider_configuration"]["routing_policy"],
            )

    def test_accounting_reports_usage_by_requested_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state, _ = self.make_state(root, FakeAuthoringProvider())
            records = list(state["passes"].values())[:2]
            for record, model in zip(
                records, ("gpt-5.6-luna", "gpt-5.6-terra")
            ):
                record["attempts"] = [{
                    "state": "PASS_QA_ACCEPTED",
                    "provider_metadata": {
                        "requested_model": model,
                        "usage": {
                            "input_tokens": 1000,
                            "cached_input_tokens": 0,
                            "cache_write_tokens": 0,
                            "output_tokens": 100,
                            "reasoning_tokens": 0,
                            "total_tokens": 1100,
                        },
                    },
                }]
            update_run_status(state)
            self.assertEqual(
                {"gpt-5.6-luna", "gpt-5.6-terra"},
                set(state["accounting"]["models"]),
            )
            self.assertLess(
                state["accounting"]["models"]["gpt-5.6-luna"]
                ["estimated_cost_usd"],
                state["accounting"]["models"]["gpt-5.6-terra"]
                ["estimated_cost_usd"],
            )

    def test_cost_accounts_for_explicit_cache_writes(self) -> None:
        usage = {
            "input_tokens": 1000,
            "cached_input_tokens": 200,
            "cache_write_tokens": 300,
            "output_tokens": 100,
            "reasoning_tokens": 0,
            "total_tokens": 1100,
        }
        cost = estimated_cost("gpt-5.6-terra", usage)
        self.assertEqual(
            {
                "uncached_input": 500,
                "cached_input": 200,
                "cache_write": 300,
                "output": 100,
            },
            cost["billable_tokens"],
        )
        self.assertEqual(0.0037375, cost["estimated_amount"])

    def test_prompt_layout_report_is_token_free_and_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = OpenAIResponsesProvider(
                api_key="unused",
                transport=ScriptedTransport([]),
            )
            state, _ = self.make_state(root, provider)
            report = build_prompt_layout_report(
                state=state,
                run_dir=root,
                provider=provider,
            )
            self.assertEqual(6, report["pass_count"])
            self.assertGreater(report["request_estimated_tokens"], 0)
            self.assertGreater(
                report["file_inventory"]["exact_duplicate_estimated_tokens"],
                0,
            )
            self.assertTrue(
                report["segments"]["system_instructions"][
                    "shared_by_all_passes"
                ]
            )
            self.assertTrue(
                report["segments"]["static_prefix"]["shared_by_all_passes"]
            )
            self.assertTrue(
                report["segments"]["subject_prefix"]["shared_by_all_passes"]
            )
            self.assertEqual(
                6,
                report["segments"]["pass_assignment"][
                    "distinct_sha256_count"
                ],
            )
            self.assertEqual(0, len(provider.transport.calls))
            self.assertEqual(1, estimated_text_tokens("a"))

    def test_cache_manifest_verifies_shared_prefixes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, specs, _ = self.make_passes(root)
            manifest = prompt_cache_manifest(specs)
            self.assertEqual("tiered_prefix", manifest["mode"])
            self.assertEqual(1, len(manifest["subject_context_sha256"]))
            self.assertEqual(6, len(manifest["passes"]))

    def test_cache_warmer_is_smallest_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, specs, _ = self.make_passes(root)
            selected = select_cache_warmer(specs)
            self.assertEqual(
                min(item.source_zip.stat().st_size for item in specs),
                selected.source_zip.stat().st_size,
            )

    def test_cost_comparison_reports_stage_and_savings_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = FakeAuthoringProvider()
            (root / "baseline").mkdir()
            (root / "candidate").mkdir()
            baseline, baseline_path = self.make_state(root / "baseline", provider)
            candidate, candidate_path = self.make_state(root / "candidate", provider)
            for state, amount, tokens in (
                (baseline, 4.0, 1000),
                (candidate, 2.0, 600),
            ):
                attempt = state["passes"]["bre_1"]["attempts"] = [{
                    "accepted": True,
                    "provider_metadata": {
                        "response_id": f"response-{amount}",
                        "usage": {
                            "input_tokens": tokens,
                            "cached_input_tokens": 0,
                            "cache_write_tokens": 0,
                            "output_tokens": 0,
                            "reasoning_tokens": 0,
                            "total_tokens": tokens,
                        },
                        "estimated_cost": {
                            "currency": "USD",
                            "estimated_amount": amount,
                        },
                    },
                }]
                save_state(
                    baseline_path if state is baseline else candidate_path,
                    state,
                )
            report = compare_cost_runs(baseline_path, candidate_path)
            self.assertEqual(2.0, report["difference"]["estimated_savings_usd"])
            self.assertEqual(0.5, report["difference"]["estimated_savings_ratio"])
            self.assertEqual(-400, report["difference"]["usage"]["input_tokens"])

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

    def test_batch_service_authors_six_passes_and_records_discount(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = OpenAIResponsesProvider(
                api_key="test-key",
                model="gpt-5.6-terra",
                prompt_cache_mode="disabled",
            )
            state, run_json = self.make_state(root, provider)
            state["service_level"] = "batch"
            save_state(run_json, state)
            transport = ScriptedBatchTransport()
            completed = author_pending_passes_batch(
                state=state,
                provider=provider,
                transport=transport,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                poll_interval_seconds=0,
                sleep=lambda _: None,
            )
            persisted = load_json(run_json)
            self.assertTrue(completed)
            self.assertEqual(6, len(transport.lines))
            self.assertEqual("INGESTED", persisted["batch_service"]["rounds"][0]["state"])
            self.assertEqual(
                {"PASS_QA_ACCEPTED"},
                {record["state"] for record in persisted["passes"].values()},
            )
            metadata = persisted["passes"]["bre_1"]["attempts"][0]["provider_metadata"]
            self.assertEqual("batch", metadata["service_level"])
            self.assertEqual(
                0.5, metadata["estimated_cost"]["discount_ratio"]
            )

    def test_batch_detach_persists_and_resume_ingests_same_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            provider = OpenAIResponsesProvider(
                api_key="test-key", prompt_cache_mode="disabled"
            )
            state, run_json = self.make_state(root, provider)
            state["service_level"] = "batch"
            save_state(run_json, state)
            transport = ScriptedBatchTransport(initially_complete=False)
            self.assertFalse(author_pending_passes_batch(
                state=state,
                provider=provider,
                transport=transport,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                detach=True,
                sleep=lambda _: None,
            ))
            submitted = load_json(run_json)
            self.assertEqual(1, len(submitted["batch_service"]["rounds"]))
            self.assertEqual(1, len(submitted["passes"]["bre_1"]["attempts"]))
            self.assertTrue(author_pending_passes_batch(
                state=submitted,
                provider=provider,
                transport=transport,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                detach=False,
                poll_interval_seconds=0,
                sleep=lambda _: None,
            ))
            resumed = load_json(run_json)
            self.assertEqual(1, len(resumed["batch_service"]["rounds"]))
            self.assertEqual(1, len(resumed["passes"]["bre_1"]["attempts"]))

    def test_batch_cost_is_half_of_interactive_estimate(self) -> None:
        usage = {
            "input_tokens": 1000,
            "cached_input_tokens": 200,
            "cache_write_tokens": 0,
            "output_tokens": 500,
            "reasoning_tokens": 0,
            "total_tokens": 1500,
        }
        interactive = estimated_cost("gpt-5.6-terra", usage)
        batch = batch_estimated_cost("gpt-5.6-terra", usage)
        self.assertAlmostEqual(
            interactive["estimated_amount"] * 0.5,
            batch["estimated_amount"],
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
