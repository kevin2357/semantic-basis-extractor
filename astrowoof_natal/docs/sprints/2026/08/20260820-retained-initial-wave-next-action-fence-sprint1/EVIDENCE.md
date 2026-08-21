# Retained Initial-Wave Next-Action Fence Sprint 1 Evidence

Status: Slice 2 complete; constrained-continuation implementation has not begun.

## API evidence reviewed

- API Sprint 33 documents one prior immutable initial-wave authority and six prior
  provider-operation records before retained re-entry.
- The retained call created a distinct wave/action inventory and six external
  Responses before API publication validation could reject it.
- API's new provider-free fence refuses this class before native invocation; its
  focused suite reports 155 passing tests.
- API Slice 4 is blocked on a fresh immutable SBE public contract/release.
- API's Slice 1 decision note approves Slices 0-1 and requires the complete request
  inline in lifecycle v0.5, an exact aggregate grant, deterministic route-sensitive
  ordering, typed unjoinable-lineage refusal, and durable intent before unlocked
  provider I/O.
- Review artifact: `API Agent Review and Slice 1 Contract Decisions.md`.
- Final API clarification requires a closed `external_authority_refusal` companion
  object for `initial_wave_lineage_unjoinable`; Kevin and API then approved the
  planning direction.

## SBE source evidence

- Lifecycle v0.4 selects `await_external_authority` with `action_ids=[]`.
- Existing `read_initial_wave_authority_inputs()` is snapshot-validating and
  publicly joins the prepared wave to its binding bundle, but only for an already
  stored initial wave.
- Exact-interactive main routing enters initial-wave mode when a stored wave exists
  or every pass has no attempts.
- `prepare_exact_interactive_initial_wave()` prepares six new actions when no stored
  wave exists and pass attempts are empty; it does not first reject historical
  `authoring_initial` ledger/provider lineage.
- Existing wave authorization preflight strongly validates six exact members once
  a wave exists. The missing controls are public next-action publication and
  pre-preparation/re-entry fencing.

## Safety record

- Retained Aster workspace accessed or mutated: no.

## Slice 3 constrained-execution evidence

- Public runtime validator:
  `validate_external_authority_grant(request, grant, member_authorizations)`.
- Constrained native operation:
  `execute_exact_initial_wave_with_external_authority(...)`.
- Public CLI inputs: exact request, aggregate grant, and six ordered ordinary member
  authorization documents. Legacy `--initial-wave-authorization` is refused.
- Before provider I/O, one single-writer transaction revalidates the complete
  snapshot/current request, validates every binding/reference/digest, applies all
  six authorizations to a candidate ledger, marks all six actions `SUBMITTING`, and
  publishes the durable intent checkpoint.
- During provider I/O, native mutation remains serialized but the cross-process
  writer is not held. Every returned provider identity is individually checkpointed
  under the writer before it is treated as durable.
- Exact refusal cases proved byte-identical `run.json` and snapshot with zero
  provider calls: stale request, partial grant, and loose member authorizations
  without an aggregate grant.
- Interruption after durable intent: zero provider calls; all six actions remain
  `SUBMITTING`; exact replay refused before provider I/O.
- Provider returned before identity durability: six scripted creates; all six
  actions become `AMBIGUOUS_PROVIDER_SUBMISSION`; replay adds zero creates.
- Successful public CLI path: six distinct scripted creates; six durable `WAITING`
  actions and a valid complete workspace snapshot.
- Focused suite: 34 authority tests passed (4 optional schema skips), 40 existing
  initial-wave/spend tests passed, and 2 targeted closure tests passed.
- Generic resume of a stored awaiting-authority wave: typed
  `aggregate_grant_required`; byte-identical run/snapshot, unchanged result artifact
  inventory, and zero provider creates.
- `git diff --check`: passed (only repository line-ending notices).
- External network/provider use: none. Spend: USD 0.
- Retained Aster workspace accessed or mutated: no.
- Detailed implementation handoff:
  `results/SLICE 3 - SINGLE-WRITER CONSTRAINED CONTINUATION.md`.

## Slice 4 initial-wave lineage evidence

- Fresh exact-interactive state with no historical lineage still prepares exactly
  one six-member initial wave.
- A valid stored wave is contract/bundle/ledger/request/pass validated and returned
  exactly; a fixture with six durable provider IDs preserved the same action IDs and
  produced zero new creates.
- Orphaned historical cases refused with
  `initial_wave_lineage_unjoinable` and closed redacted categories:
  provider identity, consumption, reported cost, ambiguity, and prior initial
  action evidence.
- Stored-wave join failures refused before provider I/O: missing binding bundle,
  changed request payload bytes, duplicate ledger action, and missing pass attempt.
- Generic public resume with orphaned attempts refused before ordinary dispatch;
  `run.json` and snapshot remained byte-identical and provider creates remained zero.
- Public request reading cannot reinterpret orphaned `authoring_initial` actions as
  `ordinary_action_set`.
- Updated former Slice 0 reproducer now proves six historical actions remain the
  only inventory, with no second six-member wave and no provider calls.
- Test results:
  - full `test_semantic_closure`: 92 passed;
  - lineage + external public/execution: 22 passed;
  - lineage + constrained execution + existing initial-wave/spend compatibility:
    52 passed.
- `git diff --check`: passed with line-ending notices only.
- External provider/network use: none. Spend: USD 0. Retained Aster access: none.
- Detailed handoff:
  `results/SLICE 4 - INITIAL-WAVE LINEAGE FENCE.md`.

## Slice 2 public-reader evidence

- Public module: `astrowoof_natal_authoring.external_authority`.
- Packaged command: `astrowoof-external-authority`.
- Root exports: builder, validator, snapshot reader, and schema reader.
- Focused test module: `test_external_authority_public.py`.
- Exact and bounded initial-wave snapshot readers: passed.
- Ordinary prepared-action lexical reader: passed.
- Production-shaped revision relationship (`prepared=N`, persisted observation
  `N+1`): passed; future preparation revisions are refused.
- Repeated unchanged-checkpoint determinism: passed.
- Changed member and coherent mid-read checkpoint refusal: passed.
- External output plus in-workspace output refusal: passed.
- Combined request/public/legacy-wave result: 36 tests passed; four schema-only
  proposal tests skipped in the lean interpreter.
- Linux QA result: all 36 tests passed with Draft 2020-12 validation active.
- Offline wheel: `astrowoof_natal_authoring-0.4.13-py3-none-any.whl`.
- Qualification wheel SHA-256:
  `26edc7ec6118bec38ab8374cd34326075cae87db158d2ad660d76b9666839fc5`.
- Isolated Python 3.11 installation: passed.
- Installed `astrowoof-external-authority --schema`: passed and returned
  `astrowoof.external_authority_contracts.v1`.
- Provider creates/retrievals: 0 / 0. Spend: USD 0.
- Retained Aster workspace accessed or mutated: no.
- Detailed handoff: `results/SLICE 2 - PUBLIC REQUEST READER AND CLI.md`.
- Initial-wave request-admission regressions:
  - stored wave not awaiting authority: refused;
  - one provider-recorded/consumed member under a stale wave label: refused;
  - one binding-mismatched ledger member: refused;
  - duplicate ledger resolution for one wave member: refused;
  - exact six `PREPARED`, providerless, unconsumed members: admitted.
- Provider creates/retrievals: 0 / 0.
- Spend: USD 0.
- Repository changes: sprint documentation plus one Slice 0 characterization test.

## Slice 0 generated evidence

- Reproducer:
  `test_characterizes_retained_initial_lineage_reentry_before_fence`.
- Public resume/dispatch reproducer:
  `test_characterizes_public_resume_reentry_before_constrained_grant`.
- Production surfaces exercised: exact initial-wave preparation, binding-bundle
  publication, aggregate wave authorization, concurrent create coordinator,
  durable provider-identity recording, and workspace snapshots.
- Observed unsafe pre-fence result: 12 ledger actions comprising two disjoint
  six-member initial inventories; six scripted creates for the second inventory.
- Fresh-run control:
  `test_exact_interactive_initial_wave_prepares_authorizes_and_detaches`.
- Public-path result: 1 test passed in 7.637 seconds.
- Combined focused result: 3 tests passed.
- Detailed mutation map:
  `results/SLICE 0 - REPRODUCTION AND MUTATION MAP.md`.
- External provider/network calls: 0.
- Retained Aster access or mutation: none.

## Slice 1 contract evidence

- Contract proposal:
  `EXTERNAL AUTHORITY REQUEST AND GRANT CONTRACT PROPOSAL.md`.
- Packaged schema:
  `external-authority-contracts.v1.schema.json`.
- Lifecycle schema proposal declares strict
  `astrowoof.authoring_lifecycle_inspection.v0.5` with required mutually exclusive
  request/refusal fields. The implemented catalog remains v0.4 until runtime work.
- Sanitized fixtures:
  - `initial-wave-external-authority-request.v1.json`;
  - `initial-wave-external-authority-grant.v1.json`;
  - `initial-wave-lineage-unjoinable-refusal.v1.json`;
  - `ordinary-action-set-request.v1.json`;
  - `lifecycle-awaiting-external-authority.v0.5.json`;
  - `lifecycle-native-review-refusal.v0.5.json`.
- Test module: `test_external_authority_contract_proposal.py`.
- Host lean-runtime result: 16 tests passed with 4 schema-dependent tests skipped
  because that development interpreter does not contain `jsonschema`.
- Existing Linux QA-image result: 16 tests passed, including actual Draft 2020-12
  schema and fixture validation.
- Validated properties include canonical digests, complete public bindings,
  ordinary lexical order, wave semantic order, exact six-member grant join,
  rejection of reordering/partial grants/binding mutation/unknown properties,
  valid-snapshot requirement for requests, and diagnostic invalid observations for
  no-create refusals. Lifecycle-level tests additionally prove the exact outer
  run/observation/branch joins and request/refusal exclusivity. Grant tests reject
  digest-consistent authorization documents carrying the wrong action or binding.
- Runtime request builders/readers/commands do not exist yet and are deliberately
  gated on API approval.
- Provider creates/retrievals: 0 / 0. Spend: USD 0.
- Retained Aster workspace accessed or mutated: no.

## Slice 5 cross-route evidence

- Runtime lifecycle contract:
  `astrowoof.authoring_lifecycle_inspection.v0.5`.
- Compatibility validator retained:
  `astrowoof.authoring_lifecycle_inspection.v0.4`.
- Route matrix:
  `results/SLICE 5 - CROSS-ROUTE AUTHORITY AND SAFETY MATRIX.md`.
- Bounded interactive initial-wave grant: exact six-member request/grant/document
  join passed; six scripted creates detached with six durable provider identities.
- Bounded first-identity checkpoint interruption: no duplicate create; remaining
  identity-less submissions became durable ambiguity evidence.
- Exact orphan lineage and retained exact wave regressions: passed.
- Provider-pending installed qualification and 4+2 retrieval behavior: passed.
- Combined lifecycle consumer, installed qualification, bounded lifecycle,
  lineage, and capacity suite: 77 tests passed in 137.205 seconds.
- Provider/network calls: 0. Spend: USD 0. Retained Aster access: none.

### Slice 5 API correction evidence

- Durable bounded pre-submit intent: six ledger actions are `SUBMITTING` in one
  validated snapshot before the scripted transport is reachable.
- Second generic resumer after the intent checkpoint: typed refusal, zero provider
  calls, byte-identical workspace checkpoint.
- Stored `AUTHORIZED` wave with all prepared request files but no provider IDs:
  typed refusal, zero provider calls, byte-identical workspace checkpoint.
- Public reader rejects wave/bundle/ledger/request/pass join mutations before
  publishing an external-authority request.
- Combined focused suite: 113 passed in 182.399 seconds; four optional JSON Schema
  tests skipped on the lean host interpreter.

## Slice 6 failure and diagnostic evidence

- Exact constrained pre-intent failure matrix: byte-identical `run.json` and
  snapshot; zero scripted creates.
- Exact post-intent interruption: durable six-member intent; zero creates.
- Exact provider-return/identity gap: six durable ambiguity outcomes; replay
  refused; no seventh create.
- Exact post-final-snapshot interruption: six durable IDs, detached state, valid
  snapshot, replay refused.
- Bounded post-intent second resumer: zero calls and no checkpoint mutation.
- Bounded identity-checkpoint interruption: existing IDs retained and generic
  create refused.
- Focused execution/bounded result before the combined gate: 11 tests passed in
  28.761 seconds.
- Combined Slice 6 gate: 122 tests passed in 210.972 seconds with four optional
  JSON Schema skips on the lean host interpreter.
- Provider/network calls were scripted only. Spend: USD 0. Retained Aster access:
  none.

## Slice 8 release closeout candidate

- Version: 0.4.14; immutable 0.4.13 remains unchanged.
- Artifact source commit: `7139415d8bf8c0bce1c9a075de6e1fc9df0ada95`.
- Fixed `SOURCE_DATE_EPOCH`: `1787295126`.
- Two independent wheel builds were byte-identical at SHA-256
  `ac660e367a6fd9a49c08fbf7e3f195089342c005117b08090114c864ca5b1d93`.
- Candidate size: 880610 bytes; 132 entries; 77 packaged resources; `py.typed`
  present; zero bytecode/cache entries; contract catalog present.
- Fresh installed Python 3.12 environment:
  - holistic external-authority qualification: pass;
  - provider-pending six-create/4+2-retrieval qualification: pass;
  - `astrowoof-release-smoke --require-installed`: pass;
  - installed version and packaged qualification schema: correct.
- External-authority receipt file SHA-256:
  `1d59ba89c65f494cfda33f0109dbbe59c72b14c4712bff984cead6bb5c3f2be4`.
- External-authority receipt contract SHA-256:
  `5cf177ef0e6cca129a4f07327b56628c5632ef78bce116aeb1a11a8246cddda2`.
- No provider network calls, credentials, or spend. Retained Aster untouched.
- Tag/publication: pending explicit Kevin/API authorization.
- Artifact evidence lock commit:
  `a330760992c7af1e615b19c7c3f6ba78d7fa2e1e`.

### Slice 6 typed-event completion evidence

- Exact and bounded success order:
  `request_selected` → `fence_validated` → `intent_committed` →
  `provider_create_permitted`.
- Stale request: one typed `external_authority.refused` carrying only closed reason
  and category fields; zero provider calls.
- Failing sink: complete detached state, six durable identities, valid snapshot,
  and accumulated sink warnings without escaped failure.
- Protected sentinel scan across captured logs and serialized event envelopes:
  absent.
- Focused catalog/event regression: 3 tests passed in 11.282 seconds.
- Final typed-event/exact/bounded gate: 20 tests passed in 53.456 seconds.
- Lifecycle closed-vocabulary, packaged schema, and payload-catalog gate: 25 tests
  passed.

## Slice 7 installed-wheel evidence

The first candidate evidence below was contract-object qualification only and is
superseded by the 2026-08-21 holistic runtime correction. Fresh wheel and receipt
hashes replace these provisional values before API review.

- Public command: `astrowoof-external-authority-qa`.
- Closed receipt: `astrowoof.external_authority_qualification.v1`.
- Packaged schema:
  `contracts/external-authority-qualification.v1.schema.json`.
- Source suite: 72 passed in 45.321 seconds; five optional schema skips.
- Disposable Python 3.11 installed-wheel console: passed from `C:\tmp`.
- Installed root-level API invocation and receipt validation: passed.
- Installed `--schema` resource read: passed.
- Candidate wheel SHA-256:
  `1e8c405df44ed31ed49c71a765c278100d2e35f8e70cada7fab77aedca26b5ef`.
- Receipt:
  `results/external-authority-qualification-receipt.v1.json`.
- Consumer manifest: `results/slice7-consumer-fixture-manifest.json`.
- Fixture directory: `fixtures/qualification/`.
- Public handoff: `EXTERNAL AUTHORITY CONSUMER HANDOFF.md`.
- Receipt declarations: qualification-only true; provider-free true; network false;
  production authority false; provider creates 6 scripted; spend USD 0.
- Source-tree and installed-wheel receipt bytes matched at SHA-256
  `dee698e4d3663a66b07a0dbcad59f1c11ce43695b5768a4a6260a8d9dd7756a2`.
- Retained Aster workspace accessed or mutated: no.

### Slice 7 holistic runtime correction

- Real runtime workspace preparation: exact interactive, six production-shaped
  pass archives, complete native snapshot, and lifecycle inspection v0.5.
- Authority export: exact embedded request plus aggregate grant and six complete
  member documents persisted outside native workspace.
- Fresh-process constrained continuation: exactly six scripted Responses creates
  and six durable provider IDs.
- Fresh-process retained replay: typed refusal and no seventh create.
- Fresh-process reconciliation: actual route-neutral provider reconciliation entry
  point, SBE-selected due subset of at most four, GET-only scripted retrievals.
- Independent real workspaces: lifecycle-level typed unjoinable-lineage refusal and
  public-reader ordinary-action request.
- Observation join hardening: supplied lifecycle time is accepted only when all
  safety-bearing current snapshot identities match; changed snapshot digest is a
  typed stale refusal.
- Focused public/qualification suite: 15 tests passed, one optional JSON Schema
  test skipped on the lean interpreter.
- Exact constrained execution suite: 11 tests passed.
- Bounded constrained initial-wave regressions: 4 tests passed.
- Combined authority/lineage/lifecycle/event gate: 80 tests passed in 76.954
  seconds with five optional JSON Schema skips.
- Fresh disposable Python 3.11 installed-wheel command and root-level receipt
  validator passed from outside the repository.
- Holistic candidate wheel SHA-256:
  `32f6572ae26af19ebd687548a87dbd8bfc4ac8d1a81ee1408c1377440a52057b`.
- Installed/source receipt bytes remain identical at SHA-256
  `dee698e4d3663a66b07a0dbcad59f1c11ce43695b5768a4a6260a8d9dd7756a2`.
- Provider/network calls were scripted only. Spend: USD 0. Retained Aster access:
  none.
