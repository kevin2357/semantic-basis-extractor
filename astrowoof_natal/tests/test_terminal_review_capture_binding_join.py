from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from astrowoof_natal_authoring.editorial_review_contracts import (
    canonical_editorial_review_json,
    editorial_review_sha256,
)
from astrowoof_natal_authoring.editorial_review_fixtures import (
    validate_editorial_review_packet,
)
from astrowoof_natal_authoring.editorial_review_runtime import (
    build_editorial_review_runtime_capture,
)
from astrowoof_natal_authoring.terminal_review_contracts import (
    build_terminal_action_dispositions,
    terminal_action_binding_sha256,
)


RESULT_ID = "nres_" + "1" * 24
RUN_ID = "run-terminal-review-binding-join"


def _action(ordinal: int, stage: str) -> dict:
    action_id = f"paid_{ordinal:024x}"
    return {
        "action_id": action_id,
        "state": "REPORTED",
        "binding": {
            "action_id": action_id,
            "stage": stage,
            "route": f"subject_1:{stage}:attempt-{ordinal:03d}",
            "request_sha256": f"{ordinal:x}" * 64,
            "profile_sha256": "a" * 64,
            "maximum_output_tokens": 100000,
            "commitment_micro_usd": 100000 + ordinal,
            "price_book_version": "test-price-book.v1",
            "model": "test-model",
            "prepared_state_revision": 1,
            "run_id": RUN_ID,
            "service_level": "interactive",
        },
        "provider": {"id": f"resp_{ordinal}"},
        "consumption": {"consumer_id": f"consumer_{ordinal}"},
        "reported": {"usage": {"total_tokens": ordinal}},
    }


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _fixture(root: Path, polish_count: int) -> tuple[dict, dict, list[dict]]:
    passes = {}
    actions = []
    for number in range(1, 7):
        action = _action(number, "authoring_initial")
        actions.append(action)
        pass_id = f"subject_1_{number}"
        attempt_root = root / "passes" / pass_id / "attempt-001"
        workspace = attempt_root / "response" / pass_id
        _write_json(workspace / "claims.json", {"pass": number})
        _write_json(attempt_root / "openai-authored-fields.json", {"pass": number})
        _write_json(attempt_root / "openai-response.json", {
            "id": action["provider"]["id"], "output": [],
        })
        report = {"status": "accept"}
        _write_json(attempt_root / "authoring-pass-acceptance.json", report)
        passes[pass_id] = {
            "pass_id": pass_id,
            "pass_number": number,
            "source_sha256": f"{number:x}" * 64,
            "attempts": [{
                "attempt_number": 1,
                "state": "PASS_QA_ACCEPTED",
                "response_workspace": str(workspace),
                "paid_action_id": action["action_id"],
                "qa": {"accepted": True, "report": report},
            }],
        }

    initial_deck = {"cards": [{"id": "initial"}]}
    selected_deck = initial_deck
    expected_decks = [initial_deck]
    subject = {
        "deck": str(root / "deck.json"),
        "assembly_report": str(root / "assembly.json"),
        "polish_attempts": [],
    }
    if polish_count:
        initial_path = root / "final" / "subject_1" / "initial-assembled-deck.json"
        _write_json(initial_path, initial_deck)
        subject.update({
            "initial_assembled_deck": str(initial_path),
            "initial_assembled_deck_sha256": editorial_review_sha256(initial_deck),
        })
        for attempt_number in range(1, polish_count + 1):
            action = _action(6 + attempt_number, "polish")
            actions.append(action)
            attempt_root = root / "final" / "subject_1" / "polish" / f"attempt-{attempt_number:03d}"
            candidate = {"cards": [{"id": f"polished-{attempt_number}"}]}
            _write_json(attempt_root / "natal.subject_1.cards.json", candidate)
            _write_json(attempt_root / "openai-response.json", {
                "id": action["provider"]["id"], "output": [],
            })
            validation_path = attempt_root / "validation-report.json"
            lint_path = attempt_root / "lint-report.json"
            _write_json(validation_path, {"status": "pass"})
            _write_json(lint_path, {"decks": []})
            subject["polish_attempts"].append({
                "attempt_number": attempt_number,
                "state": "POLISH_ACCEPTED",
                "validation_report": str(validation_path),
                "lint_report": str(lint_path),
                "accepted": True,
                "improved": True,
                "paid_action_id": action["action_id"],
                "provider_metadata": {"response_id": action["provider"]["id"]},
            })
            selected_deck = candidate
            expected_decks.append(candidate)

    _write_json(root / "deck.json", selected_deck)
    _write_json(root / "assembly.json", {"status": "assembled"})
    state = {
        "run_id": RUN_ID,
        "route": "exact_natal.v1",
        "state_revision": 9,
        "service_level": "interactive",
        "passes": passes,
        "subjects": {"subject_1": subject},
        "spend_ledger": {"actions": actions},
        "authoring_profile": {"profile_id": "profile-1"},
        "provenance": {
            "runtime": {
                "distribution": "astrowoof-natal-authoring", "version": "0.4.test",
            },
            "resources": {"aggregate_sha256": "b" * 64},
        },
    }
    _write_json(root / "run.json", state)
    result = {
        "schema_version": "astrowoof.native_execution_result.v0.2",
        "outcome": "review_required",
        "result_id": RESULT_ID,
        "result_sha256": "1" * 64,
        "run_id": RUN_ID,
        "sbe_release": "0.4.test",
        "route_binding": {
            "route_family": "exact_natal", "provider_mechanism": "response",
        },
        "custody_finality": "final",
        "post_checkpoint": {
            "native_state_revision": 9, "checkpoint_basis_sha256": "c" * 64,
        },
        "action_dispositions": build_terminal_action_dispositions(state),
    }
    receipt = {
        "schema_version": "astrowoof.native_publication_receipt.v0.1",
        "receipt_id": "nreceipt_" + "2" * 24,
        "receipt_sha256": "2" * 64,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "logical_workspace_root": str(root),
        "checkpoint_basis_sha256": "c" * 64,
        "snapshot_sha256": "d" * 64,
    }
    return state, {"result": result, "receipt": receipt, "journal_range": {}}, expected_decks


def _capture(root: Path, view: dict) -> tuple[str, dict]:
    return build_editorial_review_runtime_capture(
        root, RESULT_ID, exact_reader=lambda *_: deepcopy(view),
    )


class TestTerminalReviewCaptureBindingJoin(unittest.TestCase):
    def test_no_polish_and_multi_polish_capture_use_exact_fixture_inventory(self) -> None:
        for polish_count in (0, 2):
            with self.subTest(polish_count=polish_count), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                state, view, expected_decks = _fixture(root, polish_count)
                branch, capture = _capture(root, view)
                self.assertEqual("editorial_review", branch, capture)
                packet = capture["packet"]
                artifacts = capture["artifacts"]
                provider_artifacts = [
                    row for row in artifacts if row["artifact_kind"] == "provider_response"
                ]
                deck_artifacts = [
                    row for row in artifacts if row["artifact_kind"] == "assembled_deck"
                ]
                expected_deck_digests = {editorial_review_sha256(row) for row in expected_decks}
                self.assertEqual(len(state["spend_ledger"]["actions"]), len(provider_artifacts))
                self.assertEqual(
                    expected_deck_digests,
                    {row["object_sha256"] for row in deck_artifacts},
                )
                self.assertEqual(len(provider_artifacts) + len(deck_artifacts), len(artifacts))
                self.assertEqual(
                    "valid",
                    validate_editorial_review_packet(
                        packet, capture["projections"], artifacts,
                    ).outcome,
                )
                actions = {
                    row["action_id"]: row for row in state["spend_ledger"]["actions"]
                }
                for decision in packet["lineage"]["decisions"]:
                    action = actions[decision["action"]["paid_action_id"]]
                    complete_digest = sha256(
                        canonical_editorial_review_json(action["binding"])
                    ).hexdigest()
                    self.assertEqual(complete_digest, decision["action"]["binding_sha256"])
                    self.assertNotEqual(
                        terminal_action_binding_sha256(action), complete_digest,
                    )

    def test_projection_mutations_and_disposition_ambiguity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state, view, _ = _fixture(root, 0)
            replacements = {
                "stage": "creative_retry",
                "route": "subject_1:changed-route",
                "request_sha256": "e" * 64,
                "profile_sha256": "f" * 64,
                "maximum_output_tokens": 99999,
                "commitment_micro_usd": 99999,
                "price_book_version": "changed-price-book.v1",
            }
            for field, replacement in replacements.items():
                changed = deepcopy(state)
                changed["spend_ledger"]["actions"][0]["binding"][field] = replacement
                _write_json(root / "run.json", changed)
                branch, status = _capture(root, view)
                self.assertEqual("unsupported", branch, field)
                self.assertEqual("contradictory_native_evidence", status["reason"], field)

            _write_json(root / "run.json", state)
            variants = []
            missing = deepcopy(view)
            missing["result"]["action_dispositions"].pop()
            variants.append(missing)
            duplicate = deepcopy(view)
            duplicate["result"]["action_dispositions"].append(
                deepcopy(duplicate["result"]["action_dispositions"][0])
            )
            variants.append(duplicate)
            wrong = deepcopy(view)
            wrong["result"]["action_dispositions"][0]["action_id"] = (
                "paid_ffffffffffffffffffffffff"
            )
            variants.append(wrong)
            conflicting = deepcopy(view)
            conflicting["result"]["action_dispositions"][0]["binding_sha256"] = "0" * 64
            variants.append(conflicting)
            for variant in variants:
                branch, status = _capture(root, variant)
                self.assertEqual("unsupported", branch)
                self.assertEqual("contradictory_native_evidence", status["reason"])

            extra = deepcopy(state)
            extra["spend_ledger"]["actions"][0]["binding"]["model"] = "changed-model"
            _write_json(root / "run.json", extra)
            branch, capture = _capture(root, view)
            self.assertEqual("editorial_review", branch, capture)


if __name__ == "__main__":
    unittest.main()
