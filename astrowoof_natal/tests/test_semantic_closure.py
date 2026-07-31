from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from author_semantic_closure import (  # noqa: E402
    FakeAuthoringProvider,
    PassSpec,
    author_pending_passes,
    discover_passes,
    initial_run_state,
    load_json,
    resume_run,
    safe_extract_zip,
    save_state,
)
from build_projected_semantic_basis import (  # noqa: E402
    build_candidates,
    build_story_workspace,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    optimize,
)


EXAMPLES = ROOT / "examples"


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
                    2,
                    card_start=(number - 1) * 2 + 1,
                    pass_number=number,
                    pass_count=6,
                )
            else:
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    0,
                    card_start=51,
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
            provider = FakeAuthoringProvider(reject_attempts={"bre_1": 1})
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
