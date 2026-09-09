from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import unittest

from astrowoof_natal_authoring.editorial_review_contracts import (
    EditorialReviewValidationResult,
    SCHEMA_RESOURCES,
    VALIDATOR_STAGES,
    canonical_editorial_review_json,
    derive_editorial_review_id,
    editorial_review_resource_sha256,
    editorial_review_sha256,
    native_rule_registry,
    parse_editorial_review_json_strict,
    read_editorial_review_schema,
    read_editorial_review_semantic_contract,
    validate_closed_root,
    validate_rule_registry_coverage,
)
import astrowoof_natal_authoring as public_api


class TestEditorialReviewContractFoundation(unittest.TestCase):
    def test_public_root_exports_contract_foundation(self):
        self.assertIs(public_api.read_editorial_review_schema, read_editorial_review_schema)
        self.assertIs(
            public_api.validate_editorial_review_rule_registry_coverage,
            validate_rule_registry_coverage,
        )

    def test_all_declared_schema_resources_are_packaged_closed_and_digest_bound(self):
        contract = read_editorial_review_semantic_contract()
        declared = {item["resource"]: item["sha256"] for item in contract["schemas"]}
        self.assertEqual(set(declared), set(SCHEMA_RESOURCES.values()))
        for kind, name in SCHEMA_RESOURCES.items():
            raw = files("astrowoof_natal_authoring.resources").joinpath(
                "contracts", name,
            ).read_bytes()
            self.assertEqual(editorial_review_resource_sha256(raw), declared[name])
            schema = read_editorial_review_schema(kind)
            self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
            self.assertFalse(schema["additionalProperties"])

    def test_schema_resource_identity_is_checkout_line_ending_independent(self):
        raw = b'{\r\n  "type": "object"\r\n}\r\n'
        self.assertEqual(
            editorial_review_resource_sha256(raw),
            editorial_review_resource_sha256(raw.replace(b"\r\n", b"\n")),
        )

    def test_optional_jsonschema_accepts_every_schema_document(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional")
        for kind in SCHEMA_RESOURCES:
            jsonschema.Draft202012Validator.check_schema(
                read_editorial_review_schema(kind)
            )

    def test_every_object_schema_is_closed_except_exact_artifact_payloads(self):
        def visit(node, path):
            if isinstance(node, dict):
                if node.get("type") == "object" and path not in {
                    ("artifact", "properties", "assembled_deck"),
                    ("artifact", "properties", "provider_response"),
                }:
                    self.assertFalse(node.get("additionalProperties", True), path)
                for key, item in node.items():
                    visit(item, (*path, key))
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    visit(item, (*path, str(index)))
        for kind in SCHEMA_RESOURCES:
            visit(read_editorial_review_schema(kind), (kind,))

    def test_strict_parser_rejects_duplicate_nonfinite_non_utf8_and_trailing(self):
        failures = (
            b'{"a":1,"a":2}',
            b'{"a":NaN}',
            b'{"a":1} trailing',
            b'\xff',
        )
        for raw in failures:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    parse_editorial_review_json_strict(raw)
        self.assertEqual({"a": [1, True, None]}, parse_editorial_review_json_strict('{"a":[1,true,null]}'))

    def test_canonical_digest_and_id_are_path_time_and_api_independent(self):
        left = {"z": 1, "a": "é"}
        right = {"a": "é", "z": 1}
        self.assertEqual(canonical_editorial_review_json(left), canonical_editorial_review_json(right))
        self.assertEqual(editorial_review_sha256(left), editorial_review_sha256(right))
        self.assertEqual(
            derive_editorial_review_id("era", "artifact", ["packet", "deck", editorial_review_sha256(left)]),
            derive_editorial_review_id("era", "artifact", ["packet", "deck", editorial_review_sha256(right)]),
        )

    def test_closed_root_returns_typed_failures(self):
        schema = read_editorial_review_schema("capture_status")
        required = {
            "schema_version": schema["properties"]["schema_version"]["const"],
            "capture_id": "capture",
            "outcome": "not_captured",
            "reason": "incomplete_native_evidence",
            "native_correlations": {},
            "detail_code": "missing_binding",
        }
        self.assertEqual("valid", validate_closed_root(required, "capture_status").outcome)
        unknown = dict(required, surprise=True)
        result = validate_closed_root(unknown, "capture_status")
        self.assertEqual(
            ("invalid", "invalid_schema", "schema.root.closed.v1"),
            (result.outcome, result.classification, result.rule_id),
        )
        version = dict(required, schema_version="editorial_review_capture_status.v2")
        result = validate_closed_root(version, "capture_status")
        self.assertEqual("unsupported_version", result.classification)

    def test_validation_result_is_closed_and_payload_safe(self):
        self.assertEqual(
            {"schema_version": "editorial_review_validation_result.v1", "outcome": "valid"},
            EditorialReviewValidationResult("valid").as_dict(),
        )
        invalid = EditorialReviewValidationResult(
            "invalid", "contradictory_evidence",
            "deck.transition.output_matches_adoption.v1",
            "packet.lineage.decisions[7].transition.output_deck",
            "adopted_candidate_output_mismatch",
        ).as_dict()
        self.assertNotIn("payload", json.dumps(invalid))
        with self.assertRaises(ValueError):
            EditorialReviewValidationResult("invalid", "invented", "x", "x", "x")


class TestEditorialReviewRuleCoverage(unittest.TestCase):
    def test_manifest_native_rules_and_validator_handlers_are_bidirectional(self):
        validate_rule_registry_coverage()
        registry = native_rule_registry()
        self.assertEqual(set(registry.values()), set(VALIDATOR_STAGES))
        contract = read_editorial_review_semantic_contract()
        rule_ids = [item["rule_id"] for item in contract["rules"]]
        self.assertEqual(len(rule_ids), len(set(rule_ids)))
        self.assertTrue(all(item["owner"] in {"native", "joint_fixture", "api_transport"} for item in contract["rules"]))

    def test_transport_ownership_is_explicit_and_below_external_ceiling(self):
        preflight = read_editorial_review_semantic_contract()["api_transport_preflight_contract"]
        self.assertEqual("api_transport", preflight["owner"])
        self.assertEqual(99, preflight["maximum_editorial_events"])
        self.assertLess(preflight["safe_compressed_byte_threshold"], preflight["verified_external_ceiling_bytes"])
        self.assertEqual((9, 0), (preflight["gzip_compresslevel"], preflight["gzip_mtime"]))

    def test_registered_semantic_stages_fail_closed_until_implemented(self):
        for stage in VALIDATOR_STAGES.values():
            with self.assertRaises(NotImplementedError):
                stage({})


if __name__ == "__main__":
    unittest.main()
