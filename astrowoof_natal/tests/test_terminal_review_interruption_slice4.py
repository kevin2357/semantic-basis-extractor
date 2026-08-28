from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

from astrowoof_natal_authoring import closure
from astrowoof_natal_authoring.native_transitions import (
    publish_native_execution_result,
    read_native_transition_result,
    validate_transition_journal,
)
from astrowoof_natal_authoring.execution_events import ExecutionEventEmitter
from astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 import _workspace


CAUSE = "native_lifecycle_review_required"


def _review_workspace(root: Path) -> Path:
    run_dir, _retry_one, _retry_two = _workspace(root, "exact_natal")
    state_path = run_dir / "run.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "FAILED_REQUIRES_REVIEW"
    next(iter(state["passes"].values()))["state"] = "FAILED_REQUIRES_REVIEW"
    state["provenance"]["protected_payload"] = "PROTECTED_SLICE4_SENTINEL"
    closure.save_state(state_path, state)
    closure.write_workspace_snapshot(run_dir)
    return run_dir


def _publish(run_dir: Path, **kwargs):
    return publish_native_execution_result(
        run_dir,
        command_kind="ordinary_authoring",
        sbe_release="0.4.27",
        published_at="2026-08-28T10:00:00Z",
        terminal_review_v02=True,
        terminal_review_cause=CAUSE,
        **kwargs,
    )


class TerminalReviewInterruptionSlice4Tests(unittest.TestCase):
    def test_every_publication_cut_repairs_or_replays_exact_review_result(self) -> None:
        cuts = (
            "after_journal_appended",
            "after_result_written",
            "after_snapshot_written",
            "after_snapshot_validated",
            "after_receipt_published",
        )
        for cut in cuts:
            with self.subTest(cut=cut), tempfile.TemporaryDirectory() as temporary:
                run_dir = _review_workspace(Path(temporary))

                def fail(point: str) -> None:
                    if point == cut:
                        raise OSError(f"injected:{cut}")

                with self.assertRaisesRegex(OSError, cut):
                    _publish(run_dir, _failure_injector=fail)
                repaired = _publish(run_dir)
                index = json.loads(
                    (run_dir / "native-result-index.json").read_text(encoding="utf-8")
                )
                self.assertEqual([repaired["result"]["result_id"]], index["result_ids"])
                exported = read_native_transition_result(
                    run_dir, repaired["result"]["result_id"]
                )
                self.assertEqual("astrowoof.native_execution_result.v0.2", exported["result"]["schema_version"])
                self.assertEqual("review_required", exported["result"]["outcome"])
                self.assertEqual(CAUSE, exported["result"]["cause_code"])
                records = validate_transition_journal(run_dir)
                self.assertEqual(
                    1,
                    sum(
                        item["record_kind"] == "invocation.closed"
                        for item in records
                    ),
                )

    def test_two_finalizers_publish_one_semantic_review_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = _review_workspace(Path(temporary))
            barrier = threading.Barrier(2)
            results: list[dict] = []
            errors: list[BaseException] = []

            def worker() -> None:
                try:
                    barrier.wait()
                    results.append(_publish(run_dir))
                except BaseException as exc:  # pragma: no cover - asserted below
                    errors.append(exc)

            threads = [threading.Thread(target=worker) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(1, len(results))
            self.assertEqual(1, len(errors))
            self.assertIsInstance(errors[0], (OSError, BlockingIOError))
            replay = _publish(run_dir)
            self.assertEqual(
                results[0]["result"]["result_id"], replay["result"]["result_id"]
            )
            index = json.loads(
                (run_dir / "native-result-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(1, len(index["result_ids"]))

    def test_custody_successor_preserves_and_orders_review_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = _review_workspace(Path(temporary))
            review = _publish(run_dir)["result"]
            review_path = run_dir / "native-results" / f"{review['result_id']}.json"
            immutable_review_bytes = review_path.read_bytes()

            state_path = run_dir / "run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["state_revision"] += 1
            first_action = state["spend_ledger"]["actions"][0]
            first_action["state"] = "REPORTED"
            first_action["reported"] = {"usage": None, "estimated_micro_usd": None}
            closure.save_state(state_path, state)
            closure.write_workspace_snapshot(run_dir)
            successor = publish_native_execution_result(
                run_dir,
                command_kind="provider_reconciliation",
                sbe_release="0.4.27",
                published_at="2026-08-28T10:01:00Z",
            )["result"]

            index = json.loads(
                (run_dir / "native-result-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual([review["result_id"], successor["result_id"]], index["result_ids"])
            self.assertEqual(immutable_review_bytes, review_path.read_bytes())
            original = read_native_transition_result(run_dir, review["result_id"])
            later = read_native_transition_result(run_dir, successor["result_id"])
            self.assertEqual("review_required", original["result"]["outcome"])
            self.assertEqual("review_required", later["result"]["outcome"])
            self.assertEqual("provider_reconciliation", later["result"]["command_kind"])
            self.assertEqual(
                original["result"]["journal_range"]["end_sequence"] + 1,
                later["result"]["journal_range"]["start_sequence"],
            )
            public_bytes = json.dumps({
                "review": original, "successor": later,
            }, sort_keys=True)
            self.assertNotIn("PROTECTED_SLICE4_SENTINEL", public_bytes)

    def test_failing_event_sink_cannot_change_publication_or_leak_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = _review_workspace(Path(temporary))

            def failing_sink(_event: dict) -> None:
                raise RuntimeError("injected sink failure")

            emitter = ExecutionEventEmitter(
                release="0.4.27", sink=failing_sink,
                base_correlation={"native_run_id": "slice4"},
            )
            sealed = _publish(run_dir, event_emitter=emitter)
            exported = read_native_transition_result(
                run_dir, sealed["result"]["result_id"]
            )
            self.assertEqual("review_required", exported["result"]["outcome"])
            self.assertNotIn(
                "PROTECTED_SLICE4_SENTINEL",
                json.dumps(exported, sort_keys=True),
            )


if __name__ == "__main__":
    unittest.main()
