from __future__ import annotations

import hashlib
import json
import unittest
from copy import deepcopy
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, RefResolver, ValidationError
except ImportError:  # Lean source environments may omit SPC's dependency.
    Draft202012Validator = None  # type: ignore[assignment,misc]
    RefResolver = None  # type: ignore[assignment,misc]
    ValidationError = Exception  # type: ignore[assignment,misc]


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "src" / "astrowoof_natal_authoring" / "resources" / "contracts"
FIXTURES = ROOT / "docs" / "sprints" / "2026" / "08" / (
    "20260820-retained-initial-wave-next-action-fence-sprint1"
) / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def without(value: dict, field: str) -> dict:
    return {key: item for key, item in value.items() if key != field}


def member_authorizations(request: dict) -> list[dict]:
    return [{
        "schema_version": "astrowoof.provider_spend_authorization.v0.1",
        "action_id": action["action_id"],
        "binding": action["binding"],
        "authorization_reference": f"reservation-{index}",
    } for index, action in enumerate(request["ordered_actions"], 1)]


def validate_request_semantics(request: dict) -> None:
    actions = request["ordered_actions"]
    action_ids = [action["action_id"] for action in actions]
    if request["action_count"] != len(actions):
        raise ValueError("action_count mismatch")
    if request["ordered_action_ids"] != action_ids:
        raise ValueError("ordered action inventory mismatch")
    if len(action_ids) != len(set(action_ids)):
        raise ValueError("duplicate action ID")
    for action in actions:
        if action["binding"]["run_id"] != request["run_id"]:
            raise ValueError("binding run mismatch")
        prepared_revision = action["binding"]["prepared_state_revision"]
        if prepared_revision > request["observation"]["operator_state_revision"]:
            raise ValueError("binding revision is newer than observation")
        if digest(action["binding"]) != action["binding_sha256"]:
            raise ValueError("binding digest mismatch")
    if request["request_kind"] == "ordinary_action_set":
        if action_ids != sorted(action_ids):
            raise ValueError("ordinary actions are not lexically ordered")
        if request["initial_wave"] is not None:
            raise ValueError("ordinary request contains wave context")
    else:
        wave = request["initial_wave"]
        if wave["member_count"] != 6 or len(actions) != 6:
            raise ValueError("initial wave is not exactly six members")
        if wave["profile_sha256"] != actions[0]["binding"]["profile_sha256"]:
            raise ValueError("wave profile mismatch")
        if wave["ordered_member_binding_sha256s"] != [
            action["binding_sha256"] for action in actions
        ]:
            raise ValueError("wave binding order mismatch")
    if digest(without(request, "external_authority_request_sha256")) != request[
        "external_authority_request_sha256"
    ]:
        raise ValueError("request digest mismatch")


def validate_grant_semantics(
    request: dict, grant: dict, authorizations: list[dict],
) -> None:
    validate_request_semantics(request)
    expected = {
        "external_authority_request_sha256": request[
            "external_authority_request_sha256"
        ],
        "run_id": request["run_id"],
        "inspected_state_revision": request["observation"][
            "operator_state_revision"
        ],
        "snapshot_sha256": request["observation"]["snapshot_sha256"],
        "logical_workspace_root": request["observation"][
            "logical_workspace_root"
        ],
        "request_kind": request["request_kind"],
        "action_count": request["action_count"],
        "ordered_action_ids": request["ordered_action_ids"],
        "initial_wave": request["initial_wave"],
    }
    for field, value in expected.items():
        if grant[field] != value:
            raise ValueError(f"grant field mismatch: {field}")
    if len(authorizations) != request["action_count"]:
        raise ValueError("partial member authorization set")
    members = grant["ordered_member_authorizations"]
    if [member["action_id"] for member in members] != request[
        "ordered_action_ids"
    ]:
        raise ValueError("grant member order mismatch")
    for action, member, document in zip(
        request["ordered_actions"], members, authorizations, strict=True,
    ):
        if set(document) != {
            "schema_version", "action_id", "binding", "authorization_reference",
        }:
            raise ValueError("authorization document shape mismatch")
        if document.get("schema_version") != (
            "astrowoof.provider_spend_authorization.v0.1"
        ):
            raise ValueError("authorization document schema mismatch")
        if document.get("action_id") != action["action_id"]:
            raise ValueError("authorization document action mismatch")
        if document.get("binding") != action["binding"]:
            raise ValueError("authorization document binding mismatch")
        if member["binding_sha256"] != action["binding_sha256"]:
            raise ValueError("grant binding mismatch")
        if member["authorization_reference"] != document[
            "authorization_reference"
        ]:
            raise ValueError("authorization reference mismatch")
        if member["authorization_document_sha256"] != digest(document):
            raise ValueError("authorization document digest mismatch")
    if digest(without(grant, "grant_sha256")) != grant["grant_sha256"]:
        raise ValueError("grant digest mismatch")


def validate_lifecycle_semantics(inspection: dict) -> None:
    request = inspection["external_authority_request"]
    refusal = inspection["external_authority_refusal"]
    if request is not None and refusal is not None:
        raise ValueError("request and refusal are mutually exclusive")
    if request is not None:
        validate_request_semantics(request)
        if inspection["run_id"] != request["run_id"]:
            raise ValueError("outer/request run mismatch")
        if inspection["observation"] != request["observation"]:
            raise ValueError("outer/request observation mismatch")
        branch = inspection["execution_branch"]
        if branch != {
            "command": "await_external_authority",
            "eligible_now": False,
            "reason_code": "spend_authorization_required",
            "action_ids": request["ordered_action_ids"],
            "not_before": None,
        }:
            raise ValueError("request execution branch mismatch")
        return
    if refusal is not None:
        if inspection["run_id"] != refusal["run_id"]:
            raise ValueError("outer/refusal run mismatch")
        if inspection["observation"] != refusal["observation"]:
            raise ValueError("outer/refusal observation mismatch")
        branch = inspection["execution_branch"]
        if branch != {
            "command": "none",
            "eligible_now": False,
            "reason_code": "native_review_or_ambiguity",
            "action_ids": [],
            "not_before": None,
        }:
            raise ValueError("refusal execution branch mismatch")


class TestExternalAuthorityContractProposal(unittest.TestCase):
    def test_packaged_contracts_are_json_and_lifecycle_v05_is_declared(self) -> None:
        contract = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        lifecycle = json.loads((
            CONTRACTS / "authoring-lifecycle-contracts.schema.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual("astrowoof.external_authority_contracts.v1", contract["$id"])
        self.assertIn("lifecycleInspectionV05", lifecycle["$defs"])
        required = lifecycle["$defs"]["lifecycleInspectionV05"]["required"]
        self.assertIn("external_authority_request", required)
        self.assertIn("external_authority_refusal", required)

    @unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
    def test_closed_schema_accepts_canonical_fixtures(self) -> None:
        schema = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
        for name in (
            "initial-wave-external-authority-request.v1.json",
            "initial-wave-external-authority-grant.v1.json",
            "initial-wave-lineage-unjoinable-refusal.v1.json",
            "ordinary-action-set-request.v1.json",
        ):
            with self.subTest(name=name):
                validator.validate(load(name))

    @unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
    def test_lifecycle_v05_schema_accepts_canonical_branch_fixtures(self) -> None:
        lifecycle = json.loads((
            CONTRACTS / "authoring-lifecycle-contracts.schema.json"
        ).read_text(encoding="utf-8"))
        external = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        resolver = RefResolver.from_schema(lifecycle, store={
            "external-authority-contracts.v1.schema.json": external,
            external["$id"]: external,
        })
        validator = Draft202012Validator(lifecycle, resolver=resolver)
        for name in (
            "lifecycle-awaiting-external-authority.v0.5.json",
            "lifecycle-native-review-refusal.v0.5.json",
        ):
            with self.subTest(name=name):
                validator.validate(load(name))

    @unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
    def test_lifecycle_v05_schema_rejects_external_authority_conditionals(
        self,
    ) -> None:
        lifecycle = json.loads((
            CONTRACTS / "authoring-lifecycle-contracts.schema.json"
        ).read_text(encoding="utf-8"))
        external = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        resolver = RefResolver.from_schema(lifecycle, store={
            "external-authority-contracts.v1.schema.json": external,
            external["$id"]: external,
        })
        validator = Draft202012Validator(lifecycle, resolver=resolver)
        request = load("lifecycle-awaiting-external-authority.v0.5.json")
        request_mutations = (
            ("execution_branch", "eligible_now", True),
            ("execution_branch", "reason_code", "terminal_or_no_continuation"),
            ("execution_branch", "action_ids", []),
            ("execution_branch", "not_before", "2026-08-21T12:01:00Z"),
            ("execution_capacity", "disposition", "continue_local_cycle"),
            ("execution_capacity", "reason_code", "local_work_ready"),
            ("execution_capacity", "local_work_ready_now", True),
            ("execution_capacity", "resume_not_before", "2026-08-21T12:01:00Z"),
        )
        refusal = load("lifecycle-native-review-refusal.v0.5.json")
        refusal_mutations = (
            ("execution_branch", "command", "ordinary_resume"),
            ("execution_branch", "eligible_now", True),
            ("execution_branch", "reason_code", "terminal_or_no_continuation"),
            ("execution_branch", "action_ids", ["paid_" + "a" * 24]),
            ("execution_branch", "not_before", "2026-08-21T12:01:00Z"),
            ("execution_capacity", "disposition", "continue_local_cycle"),
            ("execution_capacity", "reason_code", "local_work_ready"),
            ("execution_capacity", "local_work_ready_now", True),
            ("execution_capacity", "resume_not_before", "2026-08-21T12:01:00Z"),
        )
        for canonical, mutations in (
            (request, request_mutations), (refusal, refusal_mutations),
        ):
            for section, field, changed_value in mutations:
                with self.subTest(
                    command=canonical["execution_branch"]["command"], field=field,
                ):
                    changed = deepcopy(canonical)
                    changed[section][field] = changed_value
                    with self.assertRaises(ValidationError):
                        validator.validate(changed)

    @unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
    def test_request_requires_valid_snapshot_but_refusal_can_report_invalidity(
        self,
    ) -> None:
        schema = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)

        request = load("ordinary-action-set-request.v1.json")
        request["observation"]["snapshot_complete"] = False
        with self.assertRaises(ValidationError):
            validator.validate(request)

        refusal = load("initial-wave-lineage-unjoinable-refusal.v1.json")
        refusal["observation"].update({
            "snapshot_complete": False,
            "inventory_valid": False,
            "native_exclusive_access": "not_established",
            "writer_race_possible": True,
        })
        validator.validate(refusal)

    @unittest.skipUnless(Draft202012Validator, "jsonschema is not installed")
    def test_contract_is_closed_and_request_is_always_create_capable(self) -> None:
        schema = json.loads((
            CONTRACTS / "external-authority-contracts.v1.schema.json"
        ).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        request = load("ordinary-action-set-request.v1.json")

        request["unexpected"] = "not allowed"
        with self.assertRaises(ValidationError):
            validator.validate(request)
        request.pop("unexpected")
        request["provider_create_permitted_after_authorization"] = False
        with self.assertRaises(ValidationError):
            validator.validate(request)

    def test_request_digests_bind_complete_public_bindings_and_order(self) -> None:
        validate_request_semantics(load(
            "initial-wave-external-authority-request.v1.json"
        ))
        validate_request_semantics(load("ordinary-action-set-request.v1.json"))

    def test_grant_is_exact_all_or_none_join(self) -> None:
        request = load("initial-wave-external-authority-request.v1.json")
        grant = load("initial-wave-external-authority-grant.v1.json")
        validate_grant_semantics(request, grant, member_authorizations(request))

    def test_grant_rejects_digest_consistent_wrong_authorization_document(self) -> None:
        request = load("initial-wave-external-authority-request.v1.json")
        grant = load("initial-wave-external-authority-grant.v1.json")
        documents = member_authorizations(request)
        documents[0]["action_id"] = request["ordered_action_ids"][1]
        grant["ordered_member_authorizations"][0][
            "authorization_document_sha256"
        ] = digest(documents[0])
        grant["grant_sha256"] = digest(without(grant, "grant_sha256"))
        with self.assertRaisesRegex(ValueError, "document action mismatch"):
            validate_grant_semantics(request, grant, documents)

    def test_grant_rejects_digest_consistent_wrong_authorization_binding(self) -> None:
        request = load("initial-wave-external-authority-request.v1.json")
        grant = load("initial-wave-external-authority-grant.v1.json")
        documents = member_authorizations(request)
        documents[0]["binding"] = deepcopy(request["ordered_actions"][1]["binding"])
        grant["ordered_member_authorizations"][0][
            "authorization_document_sha256"
        ] = digest(documents[0])
        grant["grant_sha256"] = digest(without(grant, "grant_sha256"))
        with self.assertRaisesRegex(ValueError, "document binding mismatch"):
            validate_grant_semantics(request, grant, documents)

    def test_lifecycle_request_and_refusal_branches_are_semantically_joined(self) -> None:
        validate_lifecycle_semantics(load(
            "lifecycle-awaiting-external-authority.v0.5.json"
        ))
        validate_lifecycle_semantics(load(
            "lifecycle-native-review-refusal.v0.5.json"
        ))

    def test_lifecycle_rejects_every_outer_request_identity_mismatch(self) -> None:
        canonical = load("lifecycle-awaiting-external-authority.v0.5.json")
        mutations = []
        changed = deepcopy(canonical)
        changed["run_id"] = "different-run"
        mutations.append(changed)
        changed = deepcopy(canonical)
        changed["observation"]["operator_state_revision"] += 1
        mutations.append(changed)
        changed = deepcopy(canonical)
        changed["observation"]["snapshot_sha256"] = "f" * 64
        mutations.append(changed)
        changed = deepcopy(canonical)
        changed["observation"]["logical_workspace_root"] = "/other/run"
        mutations.append(changed)
        changed = deepcopy(canonical)
        changed["execution_branch"]["action_ids"] = changed[
            "execution_branch"
        ]["action_ids"][:-1]
        mutations.append(changed)

        for inspection in mutations:
            with self.assertRaises(ValueError):
                validate_lifecycle_semantics(inspection)

    def test_lifecycle_rejects_crossed_request_refusal_branches(self) -> None:
        request_branch = load("lifecycle-awaiting-external-authority.v0.5.json")
        request_branch["external_authority_refusal"] = load(
            "initial-wave-lineage-unjoinable-refusal.v1.json"
        )
        with self.assertRaisesRegex(ValueError, "mutually exclusive"):
            validate_lifecycle_semantics(request_branch)

        refusal_branch = load("lifecycle-native-review-refusal.v0.5.json")
        refusal_branch["external_authority_request"] = load(
            "initial-wave-external-authority-request.v1.json"
        )
        with self.assertRaisesRegex(ValueError, "mutually exclusive"):
            validate_lifecycle_semantics(refusal_branch)

    def test_lifecycle_rejects_outer_refusal_identity_mismatch(self) -> None:
        canonical = load("lifecycle-native-review-refusal.v0.5.json")
        mutations = []
        changed = deepcopy(canonical)
        changed["run_id"] = "different-run"
        mutations.append(changed)
        for field, value in (
            ("operator_state_revision", 13),
            ("snapshot_sha256", "f" * 64),
            ("logical_workspace_root", "/other/run"),
        ):
            changed = deepcopy(canonical)
            changed["observation"][field] = value
            mutations.append(changed)

        for inspection in mutations:
            with self.assertRaises(ValueError):
                validate_lifecycle_semantics(inspection)

    def test_refusal_is_content_addressed_and_never_create_capable(self) -> None:
        refusal = load("initial-wave-lineage-unjoinable-refusal.v1.json")
        self.assertEqual("initial_wave_lineage_unjoinable", refusal["reason_code"])
        self.assertTrue(refusal["review_required"])
        self.assertFalse(refusal["provider_create_permitted"])
        self.assertEqual(
            digest(without(refusal, "refusal_sha256")), refusal["refusal_sha256"],
        )

    def test_reordering_partial_grant_and_changed_binding_fail(self) -> None:
        request = load("initial-wave-external-authority-request.v1.json")
        grant = load("initial-wave-external-authority-grant.v1.json")
        documents = member_authorizations(request)
        cases = []

        reordered = deepcopy(grant)
        reordered["ordered_member_authorizations"][0], reordered[
            "ordered_member_authorizations"
        ][1] = (
            reordered["ordered_member_authorizations"][1],
            reordered["ordered_member_authorizations"][0],
        )
        cases.append((request, reordered, documents))
        cases.append((request, grant, documents[:-1]))
        changed_request = deepcopy(request)
        changed_request["ordered_actions"][0]["binding"][
            "maximum_output_tokens"
        ] += 1
        cases.append((changed_request, grant, documents))

        for changed_request, changed_grant, changed_documents in cases:
            with self.assertRaises(ValueError):
                validate_grant_semantics(
                    changed_request, changed_grant, changed_documents,
                )

    def test_request_and_refusal_are_mutually_exclusive_in_v05(self) -> None:
        lifecycle = json.loads((
            CONTRACTS / "authoring-lifecycle-contracts.schema.json"
        ).read_text(encoding="utf-8"))
        v05 = lifecycle["$defs"]["lifecycleInspectionV05"]
        self.assertIn("not", v05["allOf"][0])


if __name__ == "__main__":
    unittest.main()
