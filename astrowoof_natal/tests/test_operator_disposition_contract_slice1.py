from __future__ import annotations

import copy
import json
import unittest

from astrowoof_natal_authoring.operator_disposition import (
    CUSTODY_CLASSES,
    assessment_sha256,
    build_operator_disposition_assessment,
    logical_workspace_root_id,
    read_operator_disposition_assessment_schema,
    validate_operator_disposition_assessment,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64


def _summary(**updates):
    value = {
        "provider_identity_count": 0,
        "completed_unadopted_count": 0,
        "ambiguous_submission_count": 0,
        "local_operation_count": 0,
        "providerless_authority_count": 0,
        "retry_lineage_conflict": False,
        "sealed_result_count": 0,
        "provider_operation_refs": [],
        "provider_operation_refs_overflow": False,
    }
    value.update(updates)
    return value


def _assessment(custody_class: str):
    cases = {
        "provider_free_quiescent": (_summary(), "permitted", [], None, []),
        "provider_pending_known_identity": (
            _summary(
                provider_identity_count=1,
                provider_operation_refs=["resp_fixture_1"],
            ),
            "permitted", ["provider_reconciliation_cycle"], None, [],
        ),
        "completed_unadopted": (
            _summary(
                provider_identity_count=1,
                completed_unadopted_count=1,
                provider_operation_refs=["resp_fixture_1"],
            ),
            "native_prior_action_required", ["ordinary_resume"], None, [],
        ),
        "native_local_work_ready": (
            _summary(local_operation_count=1),
            "native_prior_action_required", ["ordinary_resume"], None, [],
        ),
        "providerless_authority": (
            _summary(providerless_authority_count=1),
            "permitted", ["external_authority_v2"], None, [],
        ),
        "submission_ambiguous": (
            _summary(ambiguous_submission_count=1),
            "permitted", ["operator_review", "fresh_disposition_assessment"],
            None, [],
        ),
        "sealed_terminal": (
            _summary(sealed_result_count=1), "permitted",
            ["terminal_result_ingress"],
            {
                "discovery_mode": "invocation_result",
                "availability_document_sha256": None,
                "result_id": "nres_" + "1" * 24,
                "result_sha256": SHA_C,
                "receipt_id": "nreceipt_" + "2" * 24,
                "receipt_sha256": SHA_D,
                "snapshot_sha256": SHA_A,
                "checkpoint_basis_sha256": SHA_B,
            }, [],
        ),
        "unsupported_or_inconsistent": (
            _summary(retry_lineage_conflict=True), "prohibited", [], None,
            ["retry_lineage_conflict"],
        ),
    }
    summary, posture, actions, terminal, categories = cases[custody_class]
    reasons = {
        "provider_free_quiescent": "provider_free_quiescent",
        "provider_pending_known_identity": "known_provider_operation_pending",
        "completed_unadopted": "completed_provider_evidence_requires_adoption",
        "native_local_work_ready": "native_local_work_ready",
        "providerless_authority": "providerless_authority_requires_named_action",
        "submission_ambiguous": "provider_submission_ambiguous",
        "sealed_terminal": "sealed_terminal_result_available",
        "unsupported_or_inconsistent": "unsupported_or_inconsistent_evidence",
    }
    return build_operator_disposition_assessment(
        native_run_id="run_fixture_1",
        route={"family": "exact_natal", "contract": "astrowoof.semantic_closure_run.v0.9"},
        compatibility={"sbe_release": "fixture", "identity_sha256": SHA_A},
        checkpoint={
            "state_revision": 7,
            "snapshot_sha256": SHA_B,
            "checkpoint_basis_sha256": SHA_C,
            "logical_workspace_root_id": logical_workspace_root_id("fixture/root"),
        },
        lifecycle_evidence={
            "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.8",
            "document_sha256": SHA_D,
        },
        terminal_evidence=terminal,
        native_custody_class=custody_class,
        custody_summary=summary,
        quarantine_posture=posture,
        supported_next_actions=actions,
        reason_code=reasons[custody_class],
        evidence_categories=categories,
        diagnostic_only=True,
        provider_io_performed=False,
        workspace_mutation_performed=False,
    )


class OperatorDispositionContractTests(unittest.TestCase):
    def test_all_eight_positive_class_fixtures_are_strict_and_deterministic(self):
        self.assertEqual(len(CUSTODY_CLASSES), 8)
        for custody_class in sorted(CUSTODY_CLASSES):
            with self.subTest(custody_class=custody_class):
                first = _assessment(custody_class)
                second = _assessment(custody_class)
                self.assertEqual(first, second)
                self.assertEqual(
                    json.dumps(first, sort_keys=True, separators=(",", ":")),
                    json.dumps(second, sort_keys=True, separators=(",", ":")),
                )
                self.assertEqual(first, validate_operator_disposition_assessment(first))

    def test_no_action_is_only_an_explicit_empty_list(self):
        value = _assessment("provider_free_quiescent")
        self.assertEqual(value["supported_next_actions"], [])
        for invalid in (None, ["none"], ["operator_review"]):
            changed = copy.deepcopy(value)
            changed["supported_next_actions"] = invalid
            changed["assessment_sha256"] = assessment_sha256(changed)
            with self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_unknown_cannot_permit_quarantine_or_hide_empty_reason(self):
        value = _assessment("unsupported_or_inconsistent")
        for field, replacement in (
            ("quarantine_posture", "permitted"),
            ("evidence_categories", []),
        ):
            changed = copy.deepcopy(value)
            changed[field] = replacement
            changed["assessment_sha256"] = assessment_sha256(changed)
            with self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_dominant_mixed_custody_cannot_be_flattened(self):
        value = _assessment("provider_pending_known_identity")
        value["custody_summary"]["completed_unadopted_count"] = 1
        value["assessment_sha256"] = assessment_sha256(value)
        with self.assertRaisesRegex(ValueError, "precedence"):
            validate_operator_disposition_assessment(value)

    def test_terminal_requires_exact_reader_bound_evidence(self):
        value = _assessment("sealed_terminal")
        mutations = (
            ("result_id", "nres_" + "9" * 23),
            ("discovery_mode", "availability_recovery"),
        )
        for field, replacement in mutations:
            changed = copy.deepcopy(value)
            changed["terminal_evidence"][field] = replacement
            changed["assessment_sha256"] = assessment_sha256(changed)
            with self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_path_like_logical_root_is_not_public(self):
        value = _assessment("provider_free_quiescent")
        for private in ("C:/tmp/run", "/tmp/run", "s3://bucket/key", "../run"):
            changed = copy.deepcopy(value)
            changed["checkpoint"]["logical_workspace_root_id"] = private
            changed["assessment_sha256"] = assessment_sha256(changed)
            with self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_every_authoritative_identity_is_digest_bound(self):
        value = _assessment("provider_pending_known_identity")
        changed = copy.deepcopy(value)
        changed["checkpoint"]["state_revision"] += 1
        with self.assertRaisesRegex(ValueError, "digest"):
            validate_operator_disposition_assessment(changed)

    def test_closed_shape_and_python_primitive_validation(self):
        base = _assessment("provider_pending_known_identity")
        mutations = []
        changed = copy.deepcopy(base)
        changed["unexpected"] = True
        mutations.append(changed)
        for path, replacement in (
            (("native_run_id",), None),
            (("route", "family"), "whatever"),
            (("compatibility", "identity_sha256"), "A" * 64),
            (("checkpoint", "state_revision"), True),
            (("checkpoint", "snapshot_sha256"), "0" * 63),
            (("checkpoint", "checkpoint_basis_sha256"), "0" * 65),
            (("lifecycle_evidence", "schema_version"), "v0.8"),
            (("lifecycle_evidence", "schema_version"), "astrowoof.authoring_lifecycle_inspection.v0.99"),
            (("custody_summary", "provider_identity_count"), -1),
            (("custody_summary", "provider_operation_refs"), ["resp_z", "resp_a"]),
            (("custody_summary", "provider_operation_refs_overflow"), True),
            (("evidence_categories",), ["z", "a"]),
            (("evidence_categories",), ["made_up_category"]),
            (("diagnostic_only",), False),
            (("provider_io_performed",), True),
            (("workspace_mutation_performed",), True),
        ):
            changed = copy.deepcopy(base)
            target = changed
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            changed["assessment_sha256"] = assessment_sha256(changed)
            mutations.append(changed)
        for index, changed in enumerate(mutations):
            with self.subTest(index=index), self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_terminal_evidence_and_summary_are_exactly_joined(self):
        value = _assessment("sealed_terminal")
        for mutation in ("drop_terminal", "wrong_count", "live_custody"):
            changed = copy.deepcopy(value)
            if mutation == "drop_terminal":
                changed["terminal_evidence"] = None
            elif mutation == "wrong_count":
                changed["custody_summary"]["sealed_result_count"] = 0
            else:
                changed["custody_summary"]["providerless_authority_count"] = 1
            changed["assessment_sha256"] = assessment_sha256(changed)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_operator_disposition_assessment(changed)

    def test_completed_evidence_requires_durable_provider_identity(self):
        value = _assessment("completed_unadopted")
        value["custody_summary"].update({
            "provider_identity_count": 0,
            "provider_operation_refs": [],
        })
        value["assessment_sha256"] = assessment_sha256(value)
        with self.assertRaisesRegex(ValueError, "provider identities"):
            validate_operator_disposition_assessment(value)

    def test_provider_reference_inventory_is_complete_up_to_cap(self):
        value = _assessment("provider_pending_known_identity")
        value["custody_summary"].update({
            "provider_identity_count": 2,
            "provider_operation_refs": ["resp_fixture_1"],
            "provider_operation_refs_overflow": True,
        })
        value["assessment_sha256"] = assessment_sha256(value)
        with self.assertRaisesRegex(ValueError, "reference inventory"):
            validate_operator_disposition_assessment(value)

    def test_json_schema_matches_positive_fixtures_when_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("optional jsonschema dependency unavailable")
        schema = read_operator_disposition_assessment_schema()
        for custody_class in sorted(CUSTODY_CLASSES):
            jsonschema.Draft202012Validator(schema).validate(_assessment(custody_class))


if __name__ == "__main__":
    unittest.main()
