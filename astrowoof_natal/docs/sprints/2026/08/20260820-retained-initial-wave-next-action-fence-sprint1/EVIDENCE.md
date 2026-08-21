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
