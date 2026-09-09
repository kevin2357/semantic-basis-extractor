from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest

from astrowoof_natal_authoring.editorial_review_runtime import (
    build_editorial_review_runtime_capture,
    collect_editorial_review_runtime_evidence,
    read_eligible_editorial_result,
)
from astrowoof_natal_authoring.editorial_review_fixtures import (
    validate_editorial_review_packet,
)
from astrowoof_natal_authoring.closure import (
    retain_initial_assembled_deck,
    snapshot_inventory,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.assembly import AssemblyContractError


class TestEditorialReviewRuntimeIngress(unittest.TestCase):
    def test_initial_assembled_deck_is_immutable_and_checkpointed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final_root = root / "final" / "subject_1"
            deck = {"cards": [{"id": "original"}]}
            relative, digest = retain_initial_assembled_deck(
                run_dir=root, final_root=final_root, subject="subject_1", deck=deck,
            )
            retained = root / relative
            before = retained.read_bytes()
            same_relative, same_digest = retain_initial_assembled_deck(
                run_dir=root, final_root=final_root, subject="subject_1", deck=deepcopy(deck),
            )
            self.assertEqual((relative, digest), (same_relative, same_digest))
            self.assertEqual(before, retained.read_bytes())
            with self.assertRaises(AssemblyContractError):
                retain_initial_assembled_deck(
                    run_dir=root, final_root=final_root, subject="subject_1",
                    deck={"cards": [{"id": "replacement"}]},
                )
            self.assertEqual(before, retained.read_bytes())
            write_workspace_snapshot(root)
            members = {item["path"]: item for item in snapshot_inventory(root)}
            self.assertIn(relative, members)
            self.assertEqual(
                __import__("hashlib").sha256(before).hexdigest(),
                members[relative]["sha256"],
            )

    def view(self, version: str, outcome: str) -> dict:
        return {
            "result": {
                "schema_version": version,
                "outcome": outcome,
                "result_id": "nres_" + "1" * 24,
                "result_sha256": "1" * 64,
                "route_binding": {
                    "route_family": "exact_natal",
                    "provider_mechanism": "response",
                },
                "custody_finality": "final",
            },
            "receipt": {
                "schema_version": "astrowoof.native_publication_receipt.v0.1",
                "receipt_id": "nreceipt_" + "2" * 24,
                "receipt_sha256": "2" * 64,
            },
            "journal_range": {},
        }

    def classify(self, view: dict):
        calls = []
        def reader(root: Path, result_id: str):
            calls.append((root, result_id))
            return deepcopy(view)
        result = read_eligible_editorial_result(".", "nres_" + "1" * 24, exact_reader=reader)
        self.assertEqual(1, len(calls))
        return result

    def test_v01_delivery_is_eligible(self):
        branch, value = self.classify(self.view(
            "astrowoof.native_execution_result.v0.1", "delivery_complete"
        ))
        self.assertEqual("delivery", branch)
        self.assertIn("result", value)

    def test_v02_final_exact_review_is_eligible(self):
        branch, value = self.classify(self.view(
            "astrowoof.native_execution_result.v0.2", "review_required"
        ))
        self.assertEqual("editorial_review", branch)
        self.assertIn("result", value)

    def test_v03_is_typed_unsupported_without_partial_packet(self):
        branch, value = self.classify(self.view(
            "astrowoof.native_execution_result.v0.3", "review_required"
        ))
        self.assertEqual("unsupported", branch)
        self.assertEqual("unsupported_result_version", value["reason"])
        self.assertNotIn("packet_id", value)

    def test_known_version_wrong_outcome_is_typed_ineligible(self):
        branch, value = self.classify(self.view(
            "astrowoof.native_execution_result.v0.1", "review_required"
        ))
        self.assertEqual("unsupported", branch)
        self.assertEqual("ineligible_route", value["reason"])

    def test_v02_nonfinal_custody_is_ineligible(self):
        view = self.view("astrowoof.native_execution_result.v0.2", "review_required")
        view["result"]["custody_finality"] = "provider_reconciliation_required"
        branch, value = self.classify(view)
        self.assertEqual("unsupported", branch)
        self.assertEqual("ineligible_route", value["reason"])

    def test_runtime_evidence_collects_six_exact_pass_winners_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_id = "run-fixture"
            passes = {}
            actions = []
            for number in range(1, 7):
                pass_id = f"subject_1_{number}"
                attempt_root = root / "passes" / pass_id / "attempt-001"
                workspace = attempt_root / "response" / pass_id
                workspace.mkdir(parents=True)
                (workspace / "claims.json").write_text("{}", encoding="utf-8")
                (attempt_root / "openai-authored-fields.json").write_text("{}", encoding="utf-8")
                (attempt_root / "openai-response.json").write_text(
                    json.dumps({"id": f"resp_{number}", "output": []}), encoding="utf-8"
                )
                report = {"status": "accept"}
                (attempt_root / "authoring-pass-acceptance.json").write_text(
                    json.dumps(report), encoding="utf-8"
                )
                action_id = f"paid_{number}"
                passes[pass_id] = {
                    "pass_id": pass_id, "pass_number": number,
                    "source_sha256": str(number) * 64,
                    "attempts": [{
                        "attempt_number": 1, "state": "PASS_QA_ACCEPTED",
                        "response_workspace": str(workspace),
                        "paid_action_id": action_id,
                        "qa": {"accepted": True, "report": report},
                    }],
                }
                actions.append({
                    "action_id": action_id,
                    "binding": {"request_sha256": format(number, "x") * 64},
                    "provider": {"id": f"resp_{number}"},
                })
            first_attempt = passes["subject_1_1"]["attempts"][0]
            first_attempt["state"] = "PASS_QA_REJECTED"
            first_attempt["qa"] = {"accepted": False, "report": {"status": "reject"}}
            first_root = root / "passes" / "subject_1_1" / "attempt-001"
            (first_root / "authoring-pass-acceptance.json").write_text(
                json.dumps({"status": "reject"}), encoding="utf-8"
            )
            retry_root = root / "passes" / "subject_1_1" / "attempt-002"
            retry_workspace = retry_root / "response" / "subject_1_1"
            retry_workspace.mkdir(parents=True)
            (retry_workspace / "claims.json").write_text(
                json.dumps({"retry": True}), encoding="utf-8"
            )
            (retry_root / "openai-authored-fields.json").write_text(
                json.dumps({"retry": True}), encoding="utf-8"
            )
            (retry_root / "authoring-pass-acceptance.json").write_text(
                json.dumps({"status": "accept"}), encoding="utf-8"
            )
            (retry_root / "openai-response.json").write_text(
                json.dumps({"id": "resp_retry_1", "output": []}), encoding="utf-8"
            )
            passes["subject_1_1"]["attempts"].append({
                "attempt_number": 2, "state": "PASS_QA_ACCEPTED",
                "response_workspace": str(retry_workspace),
                "paid_action_id": "paid_retry_1",
                "qa": {"accepted": True, "report": {"status": "accept"}},
            })
            actions.append({
                "action_id": "paid_retry_1",
                "binding": {"request_sha256": "7" * 64},
                "provider": {"id": "resp_retry_1"},
            })
            state = {
                "run_id": run_id, "state_revision": 9,
                "service_level": "interactive", "passes": passes,
                "authoring_profile": {"profile_id": "profile-1"},
                "provenance": {"runtime": {"distribution": "astrowoof-natal-authoring", "version": "0.4.test"}, "resources": {"aggregate_sha256": "b" * 64}},
                "subjects": {"subject_1": {"deck": str(root / "deck.json"), "assembly_report": str(root / "assembly.json"), "polish_attempts": []}},
                "spend_ledger": {"actions": actions},
            }
            (root / "deck.json").write_text(json.dumps({"cards": []}), encoding="utf-8")
            (root / "assembly.json").write_text(json.dumps({"status": "assembled"}), encoding="utf-8")
            (root / "run.json").write_text(json.dumps(state), encoding="utf-8")
            view = self.view("astrowoof.native_execution_result.v0.1", "delivery_complete")
            view["result"]["run_id"] = run_id
            view["result"].update({"sbe_release": "0.4.test", "post_checkpoint": {"native_state_revision": 9, "checkpoint_basis_sha256": "c" * 64}})
            view["receipt"].update({"logical_workspace_root": str(root), "checkpoint_basis_sha256": "c" * 64, "snapshot_sha256": "d" * 64})
            before = (root / "run.json").read_bytes()
            branch, evidence = collect_editorial_review_runtime_evidence(
                root, "nres_" + "1" * 24, exact_reader=lambda *_: deepcopy(view)
            )
            self.assertEqual("delivery", branch)
            self.assertEqual(7, len(evidence["pass_attempts"]))
            self.assertEqual(
                [1, 1, 2, 3, 4, 5, 6],
                [item["pass_number"] for item in evidence["pass_attempts"]],
            )
            self.assertEqual(before, (root / "run.json").read_bytes())

            capture_branch, capture = build_editorial_review_runtime_capture(
                root, "nres_" + "1" * 24,
                exact_reader=lambda *_: deepcopy(view),
            )
            self.assertEqual("delivery", capture_branch, capture)
            packet = capture["packet"]
            self.assertEqual(7, packet["summary"]["decision_count"])
            self.assertEqual(1, packet["summary"]["creative_retry_count"])
            self.assertEqual(8, len(capture["artifacts"]))
            self.assertEqual(7, len(capture["projections"]))
            self.assertEqual(
                "valid",
                validate_editorial_review_packet(
                    packet, capture["projections"], capture["artifacts"]
                ).outcome,
            )
            self.assertEqual(before, (root / "run.json").read_bytes())

            initial_deck = {"cards": []}
            initial_relative, initial_digest = retain_initial_assembled_deck(
                run_dir=root, final_root=root / "final" / "subject_1",
                subject="subject_1", deck=initial_deck,
            )
            polish_root = root / "final" / "subject_1" / "polish" / "attempt-001"
            polish_root.mkdir(parents=True)
            polished_deck = {"cards": [{"id": "polished"}]}
            (polish_root / "natal.subject_1.cards.json").write_text(
                json.dumps(polished_deck), encoding="utf-8"
            )
            (polish_root / "openai-response.json").write_text(
                json.dumps({"id": "resp_polish", "output": []}), encoding="utf-8"
            )
            validation_path = polish_root / "validation-report.json"
            validation_path.write_text(json.dumps({"status": "pass"}), encoding="utf-8")
            lint_path = polish_root / "lint-report.json"
            lint_path.write_text(json.dumps({"status": "pass"}), encoding="utf-8")
            (root / "deck.json").write_text(json.dumps(polished_deck), encoding="utf-8")
            state["subjects"]["subject_1"].update({
                "initial_assembled_deck": initial_relative,
                "initial_assembled_deck_sha256": initial_digest,
                "polish_attempts": [{
                    "attempt_number": 1, "state": "POLISH_ACCEPTED",
                    "validation_report": str(validation_path),
                    "lint_report": str(lint_path), "accepted": True,
                    "improved": True, "paid_action_id": "paid_polish",
                    "provider_metadata": {"response_id": "resp_polish"},
                }],
            })
            state["spend_ledger"]["actions"].append({
                "action_id": "paid_polish",
                "binding": {"request_sha256": "8" * 64},
                "provider": {"id": "resp_polish"},
            })
            (root / "run.json").write_text(json.dumps(state), encoding="utf-8")
            optional_before = (root / "run.json").read_bytes()
            optional_branch, optional_capture = build_editorial_review_runtime_capture(
                root, "nres_" + "1" * 24,
                exact_reader=lambda *_: deepcopy(view),
            )
            self.assertEqual("delivery", optional_branch, optional_capture)
            optional_packet = optional_capture["packet"]
            self.assertEqual(1, optional_packet["summary"]["optional_stage_count"])
            self.assertEqual(
                initial_digest,
                optional_packet["initial_assembly"]["assembled_deck"]["sha256"],
            )
            self.assertEqual(
                optional_packet["initial_assembly"]["assembled_deck"],
                optional_packet["lineage"]["decisions"][7]["transition"]["input_deck"],
            )
            self.assertEqual(
                "valid",
                validate_editorial_review_packet(
                    optional_packet, optional_capture["projections"],
                    optional_capture["artifacts"],
                ).outcome,
            )
            self.assertEqual(optional_before, (root / "run.json").read_bytes())

            critic_root = root / "final" / "subject_1" / "qualitative" / "critic"
            critic_root.mkdir(parents=True)
            critic_response_path = critic_root / "openai-response.json"
            critic_response_path.write_text(
                json.dumps({"id": "resp_critic", "output": []}), encoding="utf-8"
            )
            critic_artifact_path = critic_root / "critic-findings.json"
            critic_artifact_path.write_text(json.dumps({
                "schema_version": "astrowoof.qualitative_critic_findings.v0.1",
                "critic": {"findings": [{
                    "finding_id": "q1", "quality_dimension": "exchangeable_headline",
                    "scope": "card", "priority": "high", "confidence": 0.9,
                    "repairability": "local_repair", "target_paths": ["cards.0.id"],
                    "comparison_paths": [], "diagnosis": "The identifier is illustrative.",
                    "rewrite_objective": "Make it specific.", "required_context": [],
                    "selected_for_candidate": True, "selection_reason": "eligible",
                }]},
                "provenance": {
                    "raw_provider_response": {
                        "path": critic_response_path.relative_to(root).as_posix(),
                        "sha256": __import__("hashlib").sha256(
                            critic_response_path.read_bytes()
                        ).hexdigest(),
                    },
                    "provider": {"response_id": "resp_critic"},
                },
            }), encoding="utf-8")
            candidate_root = root / "final" / "subject_1" / "qualitative" / "candidate"
            candidate_root.mkdir(parents=True)
            (candidate_root / "openai-response.json").write_text(
                json.dumps({"id": "resp_candidate", "output": []}), encoding="utf-8"
            )
            candidate_path = candidate_root / "natal.subject_1.cards.candidate.json"
            candidate_path.write_text(
                json.dumps({"cards": [{"id": "candidate"}]}), encoding="utf-8"
            )
            state["subjects"]["subject_1"]["qualitative_review"] = {
                "state": "CANDIDATE_READY_FOR_REVIEW",
                "critic": {"artifact": str(critic_artifact_path)},
                "candidate": {
                    "artifact": str(candidate_path),
                    "provider_metadata": {"response_id": "resp_candidate"},
                    "production_deck_replaced": False,
                },
            }
            state["spend_ledger"]["actions"].extend([{
                "action_id": "paid_critic", "binding": {"request_sha256": "9" * 64},
                "provider": {"id": "resp_critic"},
            }, {
                "action_id": "paid_candidate", "binding": {"request_sha256": "a" * 64},
                "provider": {"id": "resp_candidate"},
            }])
            (root / "run.json").write_text(json.dumps(state), encoding="utf-8")
            qualitative_before = (root / "run.json").read_bytes()
            qualitative_branch, qualitative_capture = build_editorial_review_runtime_capture(
                root, "nres_" + "1" * 24,
                exact_reader=lambda *_: deepcopy(view),
            )
            self.assertEqual("delivery", qualitative_branch, qualitative_capture)
            qualitative_packet = qualitative_capture["packet"]
            self.assertEqual(3, qualitative_packet["summary"]["optional_stage_count"])
            self.assertEqual(1, qualitative_packet["summary"]["finding_count"])
            self.assertEqual(
                ["polish", "critic", "candidate"],
                [item["stage"] for item in qualitative_packet["lineage"]["decisions"][-3:]],
            )
            self.assertEqual(
                "valid",
                validate_editorial_review_packet(
                    qualitative_packet, qualitative_capture["projections"],
                    qualitative_capture["artifacts"],
                ).outcome,
            )
            repeat_branch, repeat_capture = build_editorial_review_runtime_capture(
                root, "nres_" + "1" * 24,
                exact_reader=lambda *_: deepcopy(view),
            )
            self.assertEqual(qualitative_branch, repeat_branch)
            self.assertEqual(qualitative_capture, repeat_capture)
            self.assertEqual(qualitative_before, (root / "run.json").read_bytes())

            contradictions = []
            wrong_revision = deepcopy(view)
            wrong_revision["result"]["post_checkpoint"]["native_state_revision"] = 10
            contradictions.append(wrong_revision)
            wrong_basis = deepcopy(view)
            wrong_basis["result"]["post_checkpoint"]["checkpoint_basis_sha256"] = "e" * 64
            contradictions.append(wrong_basis)
            wrong_snapshot = deepcopy(view)
            wrong_snapshot["receipt"]["snapshot_sha256"] = None
            contradictions.append(wrong_snapshot)
            wrong_release = deepcopy(view)
            wrong_release["result"]["sbe_release"] = "0.4.other"
            contradictions.append(wrong_release)
            for contradictory in contradictions:
                with self.subTest(contradictory=contradictory):
                    failed_branch, status = collect_editorial_review_runtime_evidence(
                        root,
                        "nres_" + "1" * 24,
                        exact_reader=lambda *_args, value=contradictory: deepcopy(value),
                    )
                    self.assertEqual("unsupported", failed_branch)
                    self.assertEqual("contradictory_native_evidence", status["reason"])
                    self.assertNotIn("packet_id", status)
                    self.assertEqual(qualitative_before, (root / "run.json").read_bytes())

    def test_review_collection_requires_exact_action_and_binding_disposition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            passes = {}
            actions = []
            dispositions = []
            for number in range(1, 7):
                pass_id = f"subject_1_{number}"
                attempt_root = root / "passes" / pass_id / "attempt-001"
                workspace = attempt_root / "response" / pass_id
                workspace.mkdir(parents=True)
                (workspace / "claims.json").write_text("{}", encoding="utf-8")
                (attempt_root / "openai-authored-fields.json").write_text("{}", encoding="utf-8")
                report = {"status": "accept"}
                (attempt_root / "authoring-pass-acceptance.json").write_text(json.dumps(report), encoding="utf-8")
                action_id = f"paid_{number}"
                binding = {"request_sha256": "a" * 64, "ordinal": number}
                from astrowoof_natal_authoring.editorial_review_contracts import (
                    canonical_editorial_review_json,
                )
                from hashlib import sha256
                digest = sha256(canonical_editorial_review_json(binding)).hexdigest()
                actions.append({"action_id": action_id, "binding": binding, "provider": {"id": f"resp_{number}"}})
                dispositions.append({"action_id": action_id, "binding_sha256": digest})
                passes[pass_id] = {
                    "pass_id": pass_id, "pass_number": number, "source_sha256": str(number) * 64,
                    "attempts": [{"attempt_number": 1, "state": "PASS_QA_ACCEPTED", "response_workspace": str(workspace), "paid_action_id": action_id, "qa": {"accepted": True, "report": report}}],
                }
            state = {"run_id": "run-review", "state_revision": 9, "service_level": "interactive", "passes": passes, "subjects": {"subject_1": {"deck": "deck.json", "assembly_report": "assembly.json"}}, "spend_ledger": {"actions": actions}, "authoring_profile": {"profile_id": "profile-1"}, "provenance": {"runtime": {"distribution": "astrowoof-natal-authoring", "version": "0.4.test"}, "resources": {"aggregate_sha256": "b" * 64}}}
            (root / "run.json").write_text(json.dumps(state), encoding="utf-8")
            view = self.view("astrowoof.native_execution_result.v0.2", "review_required")
            view["result"].update({"run_id": "run-review", "sbe_release": "0.4.test", "post_checkpoint": {"native_state_revision": 9, "checkpoint_basis_sha256": "c" * 64}, "action_dispositions": dispositions})
            view["receipt"].update({"logical_workspace_root": str(root), "checkpoint_basis_sha256": "c" * 64, "snapshot_sha256": "d" * 64})
            branch, _ = collect_editorial_review_runtime_evidence(root, "nres_" + "1" * 24, exact_reader=lambda *_: deepcopy(view))
            self.assertEqual("editorial_review", branch)
            bad = deepcopy(view)
            bad["result"]["action_dispositions"][0]["binding_sha256"] = "f" * 64
            branch, status = collect_editorial_review_runtime_evidence(root, "nres_" + "1" * 24, exact_reader=lambda *_: deepcopy(bad))
            self.assertEqual("unsupported", branch)
            self.assertEqual("contradictory_native_evidence", status["reason"])
            wrong_action = deepcopy(view)
            wrong_action["result"]["action_dispositions"][0]["action_id"] = "paid_other"
            branch, status = collect_editorial_review_runtime_evidence(root, "nres_" + "1" * 24, exact_reader=lambda *_: deepcopy(wrong_action))
            self.assertEqual("unsupported", branch)
            self.assertEqual("contradictory_native_evidence", status["reason"])


if __name__ == "__main__":
    unittest.main()
