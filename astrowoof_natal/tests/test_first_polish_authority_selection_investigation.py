"""Provider-free reproduction of the Aldus/Ada first-polish selection defect."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (
    normalized_path,
    persist_state,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    inspect_post_fan_in_lifecycle,
)


ACTION_ID = "paid_0123456789abcdef01234567"
RUN_ID = "run_first_polish_selection_001"
SUBJECT_ID = "fixture"


def _state(root: Path) -> dict:
    return {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": RUN_ID,
        "state_revision": 53,
        "updated_at": "2026-09-10T13:00:00Z",
        "status": "AWAITING_SPEND_AUTHORIZATION",
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(root),
        },
        "spend_ledger": {
            "actions": [
                {
                    "action_id": ACTION_ID,
                    "state": "PREPARED",
                    "binding": {
                        "run_id": RUN_ID,
                        "profile_sha256": "1" * 64,
                        "prepared_state_revision": 52,
                        "stage": "polish",
                        "route": f"{SUBJECT_ID}:polish:001",
                        "request_sha256": "2" * 64,
                        "model": "gpt-5.6-luna",
                        "service_level": "interactive",
                        "maximum_output_tokens": 100000,
                        "commitment_micro_usd": 1,
                        "price_book_version": "openai-public-2026-08-07.v1",
                    },
                    "authorization": None,
                    "provider": None,
                    "reported": None,
                }
            ]
        },
        "passes": {},
        "subjects": {
            SUBJECT_ID: {
                "subject": SUBJECT_ID,
                "state": "FINAL_QA_FAILED",
                "polish_attempts": [
                    {
                        "attempt_number": 1,
                        "state": "SUBMITTED",
                        "paid_action_id": ACTION_ID,
                    }
                ],
            }
        },
    }


class FirstPolishAuthoritySelectionInvestigationTests(unittest.TestCase):
    def test_live_first_polish_request_survives_final_qa_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            state = _state(root)
            run_json = root / "run.json"
            persist_state(run_json, state)
            write_workspace_snapshot(root)

            requests = json.loads(
                (root / "spend-authorization-requests.json").read_text(
                    encoding="utf-8"
                )
            )
            result = inspect_post_fan_in_lifecycle(
                root,
                observed_at="2026-09-10T13:00:01Z",
                native_exclusive_access="declared",
            )

        self.assertEqual(1, len(requests["actions"]))
        self.assertEqual(ACTION_ID, requests["actions"][0]["action_id"])
        self.assertEqual(
            state["spend_ledger"]["actions"][0]["binding"],
            requests["actions"][0]["binding"],
        )
        self.assertEqual(
            "await_external_authority",
            result["temporal_decision"]["capacity_disposition"],
        )
        self.assertEqual(
            "await_external_authority",
            result["temporal_decision"]["selected_command"],
        )
        self.assertEqual(
            "spend_authorization_required",
            result["temporal_decision"]["reason_code"],
        )
        self.assertEqual(
            [ACTION_ID],
            result["checkpoint_basis"]["external_authority_state"][
                "ordered_action_ids"
            ],
        )

    def test_missing_stale_or_contradictory_evidence_remains_closed(self) -> None:
        mutations = {
            "missing_request": lambda root, state: (
                root / "spend-authorization-requests.json"
            ).unlink(),
            "stale_request": lambda root, state: (
                root / "spend-authorization-requests.json"
            ).write_text(
                json.dumps({
                    **json.loads((root / "spend-authorization-requests.json").read_text()),
                    "state_revision": state["state_revision"] - 1,
                }) + "\n",
                encoding="utf-8",
            ),
            "mismatched_attempt": lambda root, state: self._mutate_state(
                root,
                lambda value: value["subjects"][SUBJECT_ID]["polish_attempts"][0].update(
                    {"paid_action_id": "paid_ffffffffffffffffffffffff"}
                ),
            ),
            "duplicate_matching_attempt": lambda root, state: self._mutate_state(
                root,
                lambda value: value["subjects"][SUBJECT_ID][
                    "polish_attempts"
                ].append(dict(
                    value["subjects"][SUBJECT_ID]["polish_attempts"][0]
                )),
            ),
            "committed_terminal": lambda root, state: self._mutate_state(
                root,
                lambda value: value.update({
                    "status": "FAILED_REQUIRES_REVIEW",
                    "terminal_transition": {
                        "outcome": "terminalized",
                        "terminal_outcome": "review_required",
                        "resulting_status": "FAILED_REQUIRES_REVIEW",
                    },
                }),
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                state = _state(root)
                persist_state(root / "run.json", state)
                write_workspace_snapshot(root)
                mutate(root, state)
                write_workspace_snapshot(root)
                result = inspect_post_fan_in_lifecycle(
                    root,
                    observed_at="2026-09-10T13:00:01Z",
                    native_exclusive_access="declared",
                )
            self.assertNotEqual(
                "await_external_authority",
                result["temporal_decision"]["selected_command"],
            )
            self.assertNotEqual(
                "request",
                result["checkpoint_basis"]["external_authority_state"]["kind"],
            )

    @staticmethod
    def _mutate_state(root: Path, mutation) -> None:
        run_json = root / "run.json"
        value = json.loads(run_json.read_text(encoding="utf-8"))
        mutation(value)
        run_json.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
