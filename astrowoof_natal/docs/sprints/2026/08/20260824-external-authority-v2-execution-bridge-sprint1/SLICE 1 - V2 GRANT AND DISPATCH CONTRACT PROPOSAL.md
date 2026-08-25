# Slice 1 — V2 Grant and Dispatch Contract Proposal

Date: 2026-08-24  
Status: implemented as provider-free contract; API schema review requested

## Contract identities

- Request reference: `astrowoof.external_authority_request.v2` (existing)
- API grant: `astrowoof.external_authority_grant.v2` (new)
- Passive no-grant result: `astrowoof.external_authority_dispatch_result.v2` (new)
- Complete member authorization:
  `astrowoof.provider_spend_authorization.v0.1` (existing)

The first and only executable v2 request kind in this sprint is
`ordinary_action_set`. `initial_wave_admission` remains on the existing v1
six-member constrained command and is refused by the v2 grant builder/validator.

## Canonical inventory order

`ordinary_action_set` uses `lexical_action_id_ascending`. This is normative in:

- request semantic validation;
- v2 grant schema and semantic validation;
- grant member order;
- authorization-document order;
- passive result order;
- packaged fixture; and
- the future command/result/receipt join.

Reordering is invalid even when membership and enclosing request identity would
otherwise appear equivalent. JSON Schema documents this semantic constraint;
strict Python validation enforces it in every supported runtime.

## Binding representation

The complete ordinary authorization documents are the only normative binding
carrier. Each grant member contains exactly:

- `action_id`;
- rederived `binding_sha256`;
- `authorization_document_sha256`; and
- `authorization_reference`.

The grant contains no duplicate complete binding. Validation joins, in exact order:

```text
v2 request action ID
  = strict v0.6 inspection inventory action ID
  = grant member action ID
  = authorization document action ID

inspection complete binding
  = authorization document complete binding
  -> rederived binding SHA-256
  = grant member binding SHA-256
```

The authorization document digest and reference must also exactly match the grant
member. The request or grant alone is never enough to reconstruct or authorize an
action. The grant also carries the explicit immutable
`request_schema_version = astrowoof.external_authority_request.v2`, making the
no-v1/v2-inference boundary directly machine-readable and auditable.

## V2 grant shape

The closed grant binds:

- request digest and explicit request schema version;
- native run and checkpoint-basis digest;
- `ordinary_action_set` and canonical ordering rule;
- validated native route family and one homogeneous provider mechanism;
- exact ordered action inventory and count;
- ordered authorization-document/binding digests and references;
- API decision identity, issuer, and canonical issue time; and
- a canonical grant digest.

Mixed Response/Batch action sets refuse. No expiry was added in v2 because the
checkpoint-basis join already makes changed native facts stale and no independent
time-validity policy is currently required.

## Passive no-grant result

The provider-free result is deliberately narrow:

```text
outcome                     = awaiting_compatible_grant
reason_code                 = compatible_grant_required
selected_command            = none
dispatch_permitted          = false
native_mutation_performed   = false
provider_io_performed       = false
checkpoint_published        = false
```

It binds the native run, checkpoint basis, request digest/kind, and canonical ordered
inventory. The strict validator refuses any true side-effect flag. Building the
result is read-only and does not publish a native checkpoint merely because a grant
is absent.

The result makes no API-global assertion about authority, reservations, admission,
leases, attempts, or capacity. API maps it to its own blocked/non-retryable state.

## Public Python surface

- `build_external_authority_grant_v2()`
- `validate_external_authority_grant_v2()`
- `validate_authorization_document_v2()`
- `build_no_grant_dispatch_result_v2()`
- `validate_no_grant_dispatch_result_v2()`
- `read_external_authority_grant_v2_schema()`
- `read_external_authority_dispatch_result_v2_schema()`
- `read_external_authority_v2_fixture()`

The actual mutating constrained executor and CLI command remain Slice 2/3 work.

## Packaged fixture

`resources/fixtures/external-authority-v2/ordinary-action-set.v1.json` contains one
sanitized strict inspection, v2 request, v2 grant, ordered complete authorization
documents, and passive no-grant result. It uses a stable logical fixture root and no
prompt, response text, subject/location data, credential, header, provider payload,
or private authority material.

## Closed refusal semantics for the executor

Slice 2 should expose these machine-readable categories while preserving the Slice
0 precedence:

- `unsupported_contract`
- `request_unavailable`
- `stale_checkpoint_basis`
- `snapshot_invalid`
- `route_or_mechanism_mismatch`
- `member_inventory_mismatch`
- `binding_mismatch`
- `provider_evidence_present`
- `provider_submission_ambiguous`
- `action_state_or_custody_mismatch`
- `partial_authorization`
- `authorization_mismatch`
- `grant_digest_mismatch`
- `compatible_grant_required`
- `reconciliation_only`
- `exact_replay`

The contract module currently raises strict `ValueError` failures; Slice 2 will map
these semantic failures into the closed executor result/refusal contract without
weakening validator behavior.

## Qualification evidence

Focused tests cover:

- valid request/inspection/grant/document join;
- canonical lexical ordering;
- grant omission of complete binding copies;
- partial, reordered, wrong-binding, and cross-version refusal;
- strict passive no-grant behavior and unchanged workspace bytes;
- JSON Schema where installed plus Python validation always;
- packaged fixture loading and validation; and
- protected-data sentinel absence.

No provider constructor, request, retrieval, credential, network, retained workspace,
native mutation, snapshot publication, or spend is used.

## API review questions

1. Approve the exact grant/member fields and homogeneous mechanism rule.
2. Approve no independent expiry in v2; changed native facts stale the basis.
3. Approve the passive result shape and its explicit zero-side-effect assertions.
4. Approve the refusal vocabulary as the Slice 2 executor mapping target.
5. Confirm the packaged fixture is sufficient for initial API validator/admission
   development before the mutating executor exists.
