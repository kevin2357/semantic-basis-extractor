# Initial-Wave Binding Bundle Patch Sprint 4 Plan

Date: 2026-08-18
Status: complete; 0.4.8 tagged, published, and independently verified
Starting release: SBE 0.4.7
Target release: SBE 0.4.8

## Purpose

Close the remaining public boundary between a prepared Initial Authoring Wave v1
and the six ordinary `astrowoof.provider_spend_authorization.v0.1` documents the
AstroWoof API must create.

SBE 0.4.7 exposes each prepared member's `binding_sha256` and selected binding
fields. It also writes `spend-authorization-requests.json` with complete bindings,
but that legacy artifact has no packaged closed-world schema/validator, no explicit
`wave_id`/`wave_sha256` binding, and no supported run-specific public reader or CLI.
The API must not reconstruct SBE binding semantics from private `run.json`, packet
files, logs, or undocumented joins.

The patch will publish a provider-safe, versioned, content-addressed bundle that
contains the exact six complete ordered bindings and binds them to the prepared
wave. This is a consumer-contract correction, not a change to orchestration,
editorial semantics, provider transport, spend ownership, or lifecycle states.

## Proposed contract

Contract identity:

`astrowoof.initial_authoring_wave_binding_bundle.v1`

The closed artifact will contain:

- `schema_version`;
- `bundle_sha256`;
- `wave_id` and `wave_sha256`;
- SBE-native `run_id`;
- `route_family`;
- `profile_sha256` and `preparation_basis_revision`;
- `price_book_version`;
- `member_count: 6`;
- six `ordered_members`, each containing `action_id`, the exact complete `binding`,
  and `binding_sha256`; and
- `aggregate_maximum_commitment_micro_usd`.

The complete binding remains the existing spend-authority object:

- `run_id`;
- `profile_sha256`;
- `prepared_state_revision`;
- `stage`;
- `route`;
- `request_sha256`;
- `model`;
- `service_level`;
- `maximum_output_tokens`;
- `commitment_micro_usd`; and
- `price_book_version`.

The bundle must contain no prompt text, request body, output schema, provider
payload, subject details, protected provenance, authorization reference, API
reservation identity, or provider identity.

## Frozen ownership and authority

- SBE owns exact binding construction, action identity, wave membership/order,
  bundle publication, snapshot integrity, and native validation.
- API owns atomic reservation of the complete six-member set, creation and
  persistence of six ordinary authorization documents, the wave-level authority
  envelope, cross-run policy, quotas, circuit breakers, and billing authority.
- `bundle.run_id` and `prepared_wave.run_id` both bind to
  `SbeAuthoringRun.native_run_id`, never API `GenerationRun.id`.
- The bundle is preparation evidence, not authorization, provider custody,
  scheduling authority, or permission to submit.
- Lifecycle inspection/result/receipt and the validated complete snapshot remain
  authoritative for scheduling and native progression.

## Compatibility policy

- Existing `spend-authorization-requests.json` remains supported for ordinary
  single-action stages and historical consumers.
- Fresh v1 six-member initial waves additionally publish the binding bundle.
- API adoption of initial waves uses the new bundle, not reconstruction from the
  prepared-wave projection or private native files.
- Legacy workspaces lacking the bundle fail closed for this public operation; they
  are not silently upgraded or synthesized unless a separately reviewed,
  provenance-bound recovery rule is justified.
- No existing public contract is mutated in place. The new schema/resource is
  additive, and 0.4.7 remains immutable.

## Scope

- Frozen v1 schema, validation rules, digest rules, and artifact filename/path.
- Exact and bounded interactive initial-wave publication from the same prepared
  native facts used to construct the wave.
- Public root-level builder, validator, reader, and prepared-wave cross-validator.
- Provider-free CLI inspection/export/validation behavior.
- Contract catalog, lifecycle smoke, fixtures, handoff, and release documentation.
- Snapshot membership, detach/restore, replay, stale/mixed/tampered evidence, and
  ordinary authorization round-trip tests.
- Windows and Linux Python 3.11+ installed-wheel qualification.
- Fresh immutable 0.4.8 release only after separate final authorization.

## Non-goals

- Changing six-pass topology, prompts, assignment, QA, retries, fan-in, or delivery.
- Changing interactive or Batch authorization cardinality.
- Adding lifecycle states or changing capacity/custody meaning.
- Putting provider request payloads into the public artifact.
- Moving global reservation transactionality into SBE.
- General redesign of `spend-authorization-requests.json` for every stage.
- Live paid provider qualification.

## Slice 0 — Contract freeze and API review

### Work

- Inventory the exact complete binding construction and both exact/bounded wave
  preparation paths.
- Freeze artifact identity, filename, required fields, closed vocabularies,
  canonical digest body, ordering, and cross-artifact invariants.
- Specify the supported worker sequence from lifecycle pause through bundle read,
  API reservation, six authorization documents, wave authorization, and resume.
- Decide whether the public reader accepts an explicit artifact path, run directory,
  or both; any run-directory mode must validate the complete snapshot first.
- Define legacy absence, duplicate/unknown member, stale revision, digest conflict,
  wave mismatch, and unsafe-output-path outcomes.

### Tests/evidence

- Proposed schema and representative exact/bounded fixtures.
- Truth table for bundle/prepared-wave/member-authorization consistency.
- Field-level provider-disclosure inventory.
- Confirm zero lifecycle-state and transition-oracle vocabulary changes.

### Gate

Pause for Kevin and AstroWoof API review before runtime implementation.

## Slice 1 — Native publication and snapshot integrity

### Work

- Build the bundle from the same immutable action bindings used by the prepared
  wave; never reverse-engineer it from display fields.
- Publish it at the completed prepared-wave checkpoint for exact and bounded
  interactive routes.
- Include it in the authoritative workspace snapshot and validate its digest and
  relationship to the prepared wave before advertising the checkpoint.
- Make replay byte-identical and publication safe across interruption boundaries.

### Tests

- Exact and bounded publication with identical binding semantics.
- Byte-stable replay, completion-order neutrality, and snapshot restoration.
- Failure injection before/after artifact write, state write, snapshot write, and
  native result/receipt publication.
- No provider call or authorization consumption during publication/replay.

### Gate

Every fresh prepared initial wave exposes one coherent snapshot-bound bundle, or
fails closed without advertising an ingestible checkpoint.

## Slice 2 — Public Python, schema, CLI, and consumer handoff

### Work

- Package the strict schema and canonical exact/bounded fixtures.
- Export root-level builder/validator/reader and a cross-validator accepting a
  prepared wave plus bundle.
- Make the snapshot-validating production reader return one closed, content-bound
  pair containing both the run-specific prepared wave and binding bundle; neither
  document may be exposed if validation of either or their join fails.
- Extend `astrowoof-initial-wave-contract` with provider-free fixture/schema export
  and supported run-specific `--initial-wave-inputs` pair inspection/validation.
- Reject output paths inside the inspected run workspace.
- Add contract-catalog entries, installed lifecycle smoke coverage, disclosure
  inventory, API request/result examples, and migration guidance.

### Tests

- Closed-world validation and unsupported-version rejection.
- Source and installed-wheel Python/CLI usage without private imports.
- Exact six-member ordering, digest recomputation, aggregate commitment, shared
  identity, and binding field validation.
- Provider-visible/request-payload canaries and safe output-path enforcement.

### Gate

Pause for API review. API must be able to obtain, verify, and persist all six exact
bindings without reading `run.json`, packet files, logs, or undocumented artifacts.

## Slice 3 — Authorization round trip and failure matrix

### Work

- Prove the API-shaped flow: bundle ingestion, six ordinary authorization document
  creations, wave authorization construction, SBE preflight, and zero-provider
  execution seam.
- Preserve all-or-none preflight and exact per-member binding authority.
- Exercise restored-workspace and concurrent/stale observation behavior.

### Tests

- Happy-path exact and bounded round trips.
- Reordered, missing, duplicate, unknown, stale, cross-run, cross-wave,
  cross-profile, changed-revision, changed-price-book, and changed-binding cases.
- Authorization document whose embedded binding differs by one field.
- Bundle hash valid but prepared-wave relationship invalid, and vice versa.
- Proof every refused preflight performs zero creates and zero consumption.

### Gate

The public bundle alone supplies all SBE-owned facts necessary for API reservation
and authorization construction, while every mismatch fails before provider work.

## Slice 4 — Cross-platform qualification and 0.4.8 closeout

### Work

- Run full source and focused contract/lifecycle suites.
- Build twice with a fixed epoch and inspect wheel contents.
- Install the exact candidate with pinned SPC 0.11.0 on Windows and
  network-isolated Linux Python 3.11.
- Run lifecycle/release smokes and provider-free exact/bounded bundle round trips.
- Record artifact/resource hashes, counts, residual limitations, and API review.

### Gate

Pause for final Kevin/API approval. Version lock, annotated tag, GitHub publication,
and authenticated asset verification require explicit authorization.

## Sprint-wide test strategy

1. Treat prepared wave, binding bundle, six ordinary authorizations, and wave
   authorization as four separately validated but cryptographically joined layers.
2. Recompute every canonical digest; never trust repeated hash strings alone.
3. Validate exact key sets and closed vocabularies in both Python and JSON Schema.
4. Use exact and bounded fixtures to prevent route-specific publication drift.
5. Inject failures around artifact/state/snapshot/result publication boundaries.
6. Prove provider payload minimization with explicit forbidden-field canaries.
7. Exercise only supported public imports and CLI behavior in installed wheels.
8. Keep provider operations and spend at zero.

## Exit criteria

The sprint is complete only when:

1. every fresh interactive initial wave publishes one ordered six-binding bundle;
2. the bundle is strictly versioned, content-addressed, snapshot-bound, and joined
   to the exact prepared wave;
3. each complete binding hashes to its prepared member's `binding_sha256`;
4. the bundle contains no provider-sensitive request payload or protected subject
   information;
5. API can build and persist six exact ordinary authorization documents without
   private SBE state;
6. all mismatches fail before provider submission or authorization consumption;
7. exact and bounded routes pass restored-workspace and replay qualification;
8. no lifecycle state, Batch authority, or editorial semantics change;
9. installed Windows/Linux gates pass against the exact artifact; and
10. 0.4.8 release status is explicit and 0.4.7 remains immutable.

## Effort assessment

This is one small patch sprint. The runtime mutation is narrow; most work is strict
contract definition, cross-artifact validation, failure-boundary coverage, and
installed consumer qualification.
