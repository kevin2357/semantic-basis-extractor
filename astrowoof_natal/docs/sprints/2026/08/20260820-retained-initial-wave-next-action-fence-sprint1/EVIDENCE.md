# Retained Initial-Wave Next-Action Fence Sprint 1 Evidence

Status: Slice 0 complete; API review pending.

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
