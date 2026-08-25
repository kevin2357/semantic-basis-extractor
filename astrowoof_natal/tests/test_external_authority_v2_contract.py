from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests.test_external_authority_v2_execution_gap import make_ordinary_run
from astrowoof_natal_authoring import (
    build_external_authority_grant_v2,
    build_external_authority_request_v2,
    build_no_grant_dispatch_result_v2,
    inspect_temporal_lifecycle,
    read_external_authority_dispatch_result_v2_schema,
    read_external_authority_grant_v2_schema,
    read_external_authority_v2_fixture,
    validate_external_authority_grant_v2,
    validate_external_authority_request_v2,
    validate_no_grant_dispatch_result_v2,
)
from astrowoof_natal_authoring.lifecycle_contracts import canonical_contract_json


def authority_inputs(root: Path):
    run_dir = make_ordinary_run(root)
    inspection = inspect_temporal_lifecycle(
        run_dir, native_exclusive_access="declared",
        observed_at="2026-08-20T15:00:00Z",
    )
    request = build_external_authority_request_v2(inspection)
    inventory = {
        item["action_id"]: item
        for item in inspection["checkpoint_basis"]["action_inventory"]["actions"]
    }
    documents = [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action_id,
        "binding": copy.deepcopy(inventory[action_id]["binding"]),
        "authorization_reference": f"api-auth:{index}",
    } for index, action_id in enumerate(request["ordered_action_ids"], 1)]
    grant = build_external_authority_grant_v2(
        request, inspection, documents, api_decision_id="api-decision-1",
        issuer="astrowoof-api", issued_at="2026-08-20T15:00:01Z",
    )
    return run_dir, inspection, request, documents, grant


class ExternalAuthorityV2ContractSlice1(unittest.TestCase):
    def test_complete_grant_joins_request_inspection_and_documents(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, request, documents, grant = authority_inputs(Path(temporary))
            self.assertEqual(
                request["ordered_action_ids"],
                [item["action_id"] for item in grant["ordered_member_authorizations"]],
            )
            self.assertTrue(all(
                "binding" not in member
                for member in grant["ordered_member_authorizations"]
            ))
            self.assertEqual(
                grant,
                validate_external_authority_grant_v2(request, inspection, grant, documents),
            )

    def test_ordinary_request_order_is_contractually_lexical(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, _, request, _, _ = authority_inputs(Path(temporary))
            changed = copy.deepcopy(request)
            changed["ordered_action_ids"].reverse()
            body = {key: value for key, value in changed.items() if key != "external_authority_request_sha256"}
            changed["external_authority_request_sha256"] = hashlib.sha256(
                canonical_contract_json(body).encode("utf-8")
            ).hexdigest()
            with self.assertRaisesRegex(ValueError, "canonical lexical order"):
                validate_external_authority_request_v2(changed)

    def test_no_grant_result_is_strictly_non_dispatching_and_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, inspection, _, _, _ = authority_inputs(Path(temporary))
            before = (run_dir / "run.json").read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()
            result = build_no_grant_dispatch_result_v2(inspection)
            self.assertFalse(result["dispatch_permitted"])
            self.assertFalse(result["native_mutation_performed"])
            self.assertFalse(result["provider_io_performed"])
            self.assertFalse(result["checkpoint_published"])
            validate_no_grant_dispatch_result_v2(result)
            self.assertEqual(before, ((run_dir / "run.json").read_bytes(), (run_dir / "workspace-snapshot.json").read_bytes()))
            for field in ("dispatch_permitted", "native_mutation_performed", "provider_io_performed", "checkpoint_published"):
                changed = copy.deepcopy(result); changed[field] = True
                with self.assertRaisesRegex(ValueError, "strictly non-dispatching"):
                    validate_no_grant_dispatch_result_v2(changed)

    def test_partial_reordered_wrong_binding_and_cross_version_refuse(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, request, documents, grant = authority_inputs(Path(temporary))
            cases = []
            partial = copy.deepcopy(grant); partial["ordered_member_authorizations"].pop()
            cases.append((partial, documents, "partial"))
            reordered = copy.deepcopy(grant); reordered["ordered_action_ids"].reverse()
            cases.append((reordered, documents, "does not join"))
            wrong_docs = copy.deepcopy(documents); wrong_docs[0]["binding"]["model"] = "other"
            cases.append((grant, wrong_docs, "join failed"))
            v1 = copy.deepcopy(grant); v1["schema_version"] = "astrowoof.external_authority_grant.v1"
            cases.append((v1, documents, "unsupported"))
            wrong_request_schema = copy.deepcopy(grant)
            wrong_request_schema["request_schema_version"] = "astrowoof.external_authority_request.v1"
            cases.append((wrong_request_schema, documents, "does not join"))
            for candidate, docs, message in cases:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(ValueError, message):
                        validate_external_authority_grant_v2(request, inspection, candidate, docs)

    def test_schema_and_public_exports(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, inspection, _, documents, grant = authority_inputs(Path(temporary))
            result = build_no_grant_dispatch_result_v2(inspection)
            grant_schema = read_external_authority_grant_v2_schema()
            result_schema = read_external_authority_dispatch_result_v2_schema()
            self.assertFalse(grant_schema["additionalProperties"])
            self.assertFalse(result_schema["additionalProperties"])
            try:
                import jsonschema
            except ImportError:
                self.skipTest("jsonschema is optional")
            jsonschema.Draft202012Validator(grant_schema).validate(grant)
            jsonschema.Draft202012Validator(result_schema).validate(result)

    def test_packaged_fixture_is_closed_and_privacy_minimized(self):
        value = read_external_authority_v2_fixture()
        self.assertEqual("ordinary_action_set", value["request"]["request_kind"])
        serialized = json.dumps(value, sort_keys=True)
        for sentinel in (
            "protected_birth_location_sentinel", "api_key", "authorization: bearer",
            "prompt", "response_text", "subject_params",
        ):
            self.assertNotIn(sentinel, serialized.lower())


if __name__ == "__main__":
    unittest.main()
