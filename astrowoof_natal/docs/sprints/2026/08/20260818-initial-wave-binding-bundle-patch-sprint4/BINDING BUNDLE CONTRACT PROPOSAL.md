# Initial Authoring Wave Binding Bundle v1 Contract Proposal

Status: frozen proposal; awaiting Kevin/API review

## Finding

SBE 0.4.7 does not expose an adequate strict public source for the six complete
ordinary spend-authorization bindings.

`spend-authorization-requests.json` contains those bindings and remains the
documented ordinary-stage handoff, but it is not wave-bound: it has no packaged
schema/validator, `wave_id`, `wave_sha256`, frozen pass order, or supported
run-specific public reader. Reconstructing bindings from prepared-wave projections
would duplicate SBE canonical composition in the API.

## Frozen artifact

| Property | Decision |
|---|---|
| Contract | `astrowoof.initial_authoring_wave_binding_bundle.v1` |
| Run-relative path | `initial-authoring-wave-binding-bundle.json` |
| Cardinality | exactly six ordered members, pass numbers 1 through 6 |
| Routes | `exact_natal`, `bounded_natal` |
| Transport/stage | `interactive`, `authoring_initial` only |
| Digest | canonical JSON SHA-256 of the complete object excluding `bundle_sha256` |
| Snapshot | authoritative member of the complete workspace snapshot |
| Replay | byte-identical for the same prepared wave and native bindings |

There is deliberately no independently meaningful `bundle_id`: `bundle_sha256` is
the complete content address, while `wave_id` identifies the joined wave. Avoiding
a truncated second identifier removes another value consumers might mistake for
authority.

The proposal schema is
[initial-authoring-wave-binding-bundle.v1.schema.json](contracts/initial-authoring-wave-binding-bundle.v1.schema.json).

Provider-free representative exact and bounded fixtures are constructed and
schema-validated in `test_initial_wave_binding_bundle_contract_proposal.py`. Their
frozen example identities are:

| Route | Wave ID | Bundle SHA-256 |
|---|---|---|
| Exact | `wave_049d85b3c0deec0e26917e89` | `c1c4c44afe649f7dcb1eb66c1ac7a3b3d1aea2449f8111b6d7582bc8303f43ad` |
| Bounded | `wave_f830efd2c0245a9fe0626c55` | `cd497479bd6685c2d1a895994bd42a8285acd1b5016153916f2fa43f56bdf23b` |

## Cross-artifact invariants

The public validator must first validate the prepared wave and bundle independently,
then require:

1. equal `wave_id`, `wave_sha256`, `run_id`, `route_family`, `profile_sha256`,
   `preparation_basis_revision`, `price_book_version`, member count, and aggregate
   commitment;
2. identical ordered `(action_id, pass_id, pass_number, binding_sha256)` inventory;
3. `canonical_sha256(member.binding) == member.binding_sha256` for every member;
4. every binding repeats the bundle's run, profile, revision, price book, initial
   stage, and interactive service level;
5. every binding's route, request digest, model, output maximum, and commitment
   equal the corresponding prepared-wave projection; and
6. action identity is `paid_` plus the first 24 hexadecimal characters of the
   canonical binding SHA-256, preserving the existing spend-ledger identity rule.

A repeated digest string is never accepted as proof without recomputation.

## Supported public interfaces

Proposed root exports:

```python
build_initial_wave_binding_bundle(prepared_wave, ordered_bindings)
validate_initial_wave_binding_bundle(bundle)
validate_initial_wave_binding_bundle_against_wave(bundle, prepared_wave)
read_initial_wave_authority_inputs(run_dir)
```

The pure validators/builders perform no filesystem or provider mutation.
`read_initial_wave_authority_inputs(run_dir)` accepts a run directory only, resolves
the stable logical workspace, validates the complete snapshot, obtains the public
prepared wave through SBE-owned native lookup, reads the fixed bundle filename,
validates each document, and cross-validates them before returning either. It
returns a defensive closed wrapper:

```json
{
  "schema_version": "astrowoof.initial_authoring_wave_authority_inputs.v1",
  "authority_inputs_sha256": "...",
  "prepared_wave": {"schema_version": "astrowoof.initial_authoring_wave.v1"},
  "binding_bundle": {
    "schema_version": "astrowoof.initial_authoring_wave_binding_bundle.v1"
  }
}
```

`authority_inputs_sha256` is canonical JSON SHA-256 of the wrapper excluding that
field. It binds the exact pair the API persists and uses to construct the envelope.
The strict wrapper schema is
[initial-authoring-wave-authority-inputs.v1.schema.json](contracts/initial-authoring-wave-authority-inputs.v1.schema.json).

The CLI extends `astrowoof-initial-wave-contract`:

```text
astrowoof-initial-wave-contract --schema binding-bundle
astrowoof-initial-wave-contract --fixture exact-binding-bundle
astrowoof-initial-wave-contract --fixture bounded-binding-bundle
astrowoof-initial-wave-contract --run-dir <restored-run> --initial-wave-inputs
astrowoof-initial-wave-contract --run-dir <restored-run> --initial-wave-inputs --output <outside-run.json>
```

Stdout is the default. An explicit output path must resolve outside `--run-dir`.
Reading is provider-free and nonmutating. Arbitrary artifact-path inspection is not
the production worker interface; offline fixture/schema export remains available.

## Typed refusal causes

The Python exception and CLI error result use closed reasons:

- `binding_bundle_missing`;
- `unsupported_contract`;
- `snapshot_invalid`;
- `digest_mismatch`;
- `wave_mismatch`;
- `member_inventory_mismatch`;
- `binding_mismatch`;
- `stale_preparation_basis`; and
- `unsafe_output_path`.

No new lifecycle state, reconciliation result, capacity disposition, terminal
outcome, or transition-oracle state is introduced.

## API worker sequence

1. SBE exits at the prepared-wave authorization boundary with a complete validated
   snapshot containing the prepared wave and binding bundle.
2. API calls the supported public run reader/CLI, which returns the validated
   prepared-wave/binding-bundle pair atomically.
3. API verifies both `run_id` values equal `SbeAuthoringRun.native_run_id` and
   persists the exact pair plus its wrapper digest.
4. API atomically reserves the complete six-member set in its own database.
5. API creates six ordinary authorization documents by copying each exact `binding`
   and attaching its API-owned `authorization_reference`.
6. API calls `build_wave_authorization()` with those ordered documents and its
   reservation-set reference, then persists all seven authorization documents.
7. API resumes SBE with the wave authorization and exactly six ordered member
   authorizations. SBE repeats the full preflight before any consumption or create.

The bundle itself grants no authority and contains no API reservation reference.

## Legacy behavior

Fresh 0.4.8 initial waves require the bundle. A retained pre-0.4.8 workspace that
lacks it returns `binding_bundle_missing`. The public reader will not synthesize a
bundle from `run.json` or `spend-authorization-requests.json`; doing so would make
the consumer boundary dependent on private/historical state shape. Ordinary-stage
use of `spend-authorization-requests.json` remains unchanged.

## Provider-disclosure inventory

| Field group | Bundle | Rationale |
|---|---|---|
| Run/profile/revision identity | included | exact authorization binding |
| Stage/route/pass/action identity | included | ordered authority mapping |
| Request SHA-256 | included | binds hidden provider request bytes |
| Model/service/output maximum/commitment/price book | included | spend authority |
| Prompt or request body | excluded | provider-sensitive payload, unnecessary |
| Output JSON schema | excluded | request payload, unnecessary |
| Subject name/view/birth data/location | excluded | protected editorial inputs |
| Claims/cards/evidence/provenance | excluded | semantic/private content |
| Provider ID/status/usage | excluded | not present before authorization/create |
| API reservation/reference | excluded | API-owned authority, added later |

The artifact reveals request digests and commercial limits but no provider-visible
content.
