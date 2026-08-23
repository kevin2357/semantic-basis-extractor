# Sprint 1 Evidence

Status: complete; SBE 0.4.16 tagged, published, and independently verified

- Provider calls/retrievals: 0
- Spend: USD 0
- Retained QA workspaces touched: 0
- Runtime/source/schema changes: none
- API database/migration changes: none
- Current native evidence inspected:
  - lifecycle inspection v0.5 construction and validation;
  - provider custody timing and maximum-four due selection;
  - execution-capacity and execution-branch projection; and
  - external-authority observation/request joins.
- Current API evidence inspected:
  - one-row-per-snapshot lifecycle-inspection persistence;
  - full canonical inspection replay equality; and
  - `SBE lifecycle inspection replay changed` refusal path.
- Confirmed incident mechanism:
  - native snapshot identity can remain unchanged;
  - caller-supplied observation time advances;
  - scheduling changes from not-due/release to due/reconcile; and
  - API currently rejects the changed full document.
- Important qualification: no provider result availability was observed by
  provider-free inspection. Actual provider facts require supported retrieval
  and a new durable checkpoint.
- Planning artifact: `SBE AGENT PRE-SPRINT HUDDLE.md`.
- Slice 0 start gate: owner/API approved; completed evidence follows below.

## API planning review

- API approved the checkpoint-basis / temporal-decision direction.
- Contract constraints recorded in the plan include trusted canonical UTC time,
  immutable custody schedule, narrow temporal evolution, stable authority
  request identity, bounded decision-history retention, lease-owned invocation
  concurrency, new-basis reconciliation, and fail-closed legacy versions.
- No implementation, provider call, retained-run access, or qualification was
  performed while incorporating this review.

## Slice 0 evidence

- Reproduction and contract finding:
  [SLICE 0 - TEMPORAL FIELD CLASSIFICATION AND TRANSITION MATRIX.md](SLICE%200%20-%20TEMPORAL%20FIELD%20CLASSIFICATION%20AND%20TRANSITION%20MATRIX.md)
- Test:
  `astrowoof_natal/tests/test_provider_pending_observation_idempotency.py`
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_provider_pending_capacity astrowoof_natal.tests.test_provider_pending_observation_idempotency`
- Result: 32 passed in 6.197 seconds.
- Workspace hashes before and after both inspections were identical.
- No credentials, network, provider create/retrieve, retained QA workspace, or
  API authority mutation was used.
- Slice 1 start gate: SBE/API approved; completed evidence follows below.

## Slice 1 evidence

- Contract proposal:
  [SLICE 1 - LIFECYCLE V0.6 CONTRACT PROPOSAL.md](SLICE%201%20-%20LIFECYCLE%20V0.6%20CONTRACT%20PROPOSAL.md)
- Public implementation:
  `astrowoof_natal_authoring.temporal_lifecycle`
- Packaged schemas:
  `temporal-lifecycle-contracts.v1.schema.json` and
  `temporal-external-authority-contracts.v2.schema.json`
- Focused result: 39 passed in 7.571 seconds; one schema-validation case skipped
  because the lean host interpreter lacks `jsonschema`.
- Both JSON Schema resources parsed successfully. Semantic validators and digest
  tests ran on the lean host.
- No credentials, provider I/O, retained-run access, or API mutation occurred.
- Gate: PAUSED before Slice 2 pending joint schema/semantic review.

### Slice 1 review correction evidence

- Exactly one v2 request schema constant, builder, standalone validator, and
  inspection-join validator remain in the source module.
- Root-package import/export smoke passed.
- Rehashed malformed basis tests cover route, provider identity, binding-stage,
  and consumer-authority contradictions.
- The request-against-inspection test proves the complete binding is committed by
  the strict basis and that the original request refuses after binding mutation.
- Updated focused result: 42 passed in 6.716 seconds; one `jsonschema`-dependent
  case skipped on the lean host.

### Primitive-validator parity evidence

- Python validators reject schema-invalid primitive identities without importing
  or calling `jsonschema`.
- Negative cases cover `run_id = null`, `request_kind = "whatever"`,
  `ordered_action_ids = ["hello"]`, malformed checkpoint action IDs, and an
  uppercase/noncanonical checkpoint digest after request rehashing.
- Updated focused result: 43 passed in 7.491 seconds; one optional-schema case
  skipped on the lean host.

## Slice 2 evidence

- Qualification summary:
  [SLICE 2 - RECONCILIATION CHECKPOINT QUALIFICATION.md](SLICE%202%20-%20RECONCILIATION%20CHECKPOINT%20QUALIFICATION.md)
- Installed qualification source now records pre/post v0.6 basis hashes and
  asserts same-basis temporal progress plus new-basis reconciliation.
- Direct regressions cover real reconciliation, fresh-process restore, zero
  repeated retrieval, and reordered-native-subset refusal.
- Focused command exercised provider-pending capacity, temporal idempotency, and
  the provider-pending qualification suites.
- Result: 47 passed in 12.633 seconds; one optional-`jsonschema` case skipped.
- Provider calls/network/spend: 0. Retained QA workspaces touched: 0.

## Slice 3 evidence

- Matrix:
  [SLICE 3 - CROSS-ROUTE COMPATIBILITY MATRIX.md](SLICE%203%20-%20CROSS-ROUTE%20COMPATIBILITY%20MATRIX.md)
- Four-route temporal-contract test and optional-stage classification are in
  `test_provider_pending_observation_idempotency.py`.
- Focused provider-pending/temporal/qualification result: 50 passed in 12.429
  seconds; one optional-`jsonschema` test skipped.
- Existing bounded Batch production-path regressions: 2 passed in 3.273 seconds.
- No credentials, network, paid provider work, or retained QA workspace used.
- Gate: PAUSED before Slice 4 pending API fixture/compatibility review.

## Slice 4 evidence

- Consumer handoff:
  [TEMPORAL LIFECYCLE API CONSUMER HANDOFF.md](TEMPORAL%20LIFECYCLE%20API%20CONSUMER%20HANDOFF.md)
- Installed receipt:
  [installed-wheel-temporal-qualification.json](results/installed-wheel-temporal-qualification.json)
- Public API and CLI require explicit trusted time and are read-only.
- Focused source result: 54 passed in 10.002 seconds; one optional-schema case
  skipped on the lean host.
- Candidate wheel built and isolated-target installed successfully.
- Installed provider-free qualification: pass; six creates, six retrievals,
  distinct pre/post basis hashes, packaged schema identity validated.
- Installed target also exposed both schema readers, temporal inspection and
  request-join APIs, and CLI `inspect-temporal` help.
- The pre-release qualification used version `0.4.15`; publication is authorized
  only as the fresh immutable `0.4.16` patch release.
- Provider network/spend and retained QA access: 0.
- Gate: API and owner approved version bump and immutable release.

### Final reader-surface cleanup evidence

- Source singular-definition regression: passed.
- Focused result: 55 passed in 9.600 seconds; one optional-schema skip.
- Replacement candidate wheel SHA-256:
  `e77b370926ce96df548331e3aa18a14632b80d479d5aafe4ff2eb132d5450fd3`.
- Fresh isolated installation qualification: pass; six creates, six retrievals,
  distinct pre/post checkpoint bases, singular installed public readers.
- Prior candidate wheel/receipt identities are superseded by the replacement
  candidate recorded above.

## Exact 0.4.16 release qualification

- Artifact source commit:
  `9591385fccfcf635d8371b12135a4d25c654166a`.
- Wheel SHA-256:
  `56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`.
- Fixed-epoch rebuild: byte-identical.
- Complete source suite: 583 passed; 28 existing environment-dependent skips.
- Installed release smoke: pass; 50 cards, four summaries, delivery complete.
- Installed provider-pending qualification: pass; six creates, six retrievals,
  bounded 4+2 reconciliation, no duplicates, and distinct post-retrieval basis.
- Wheel inventory: 136 entries, 80 resources, `py.typed` present, no bytecode.
- Provider network calls/spend: 0 / USD 0.

## Publication evidence

- Annotated tag: `astrowoof-natal-authoring-v0.4.16`.
- Tag target: `21705500a3aa6c5f3310a0aaee8aee8a71e4bdac`.
- GitHub release ID: `375150470`; published at `2026-08-23T08:03:34Z`.
- Published wheel asset ID: `525987851`; bytes: 893028.
- GitHub asset digest exactly matches the qualified local wheel SHA-256.
- Post-publication evidence is recorded after the tag and does not move it.
