# Provider-Pending Lifecycle Classification Patch Sprint 3 Plan

Date: 2026-08-19  
Status: API contract approved; awaiting Kevin authorization to implement  
Starting release: SBE 0.4.12  
Expected release: fresh immutable patch version, provisionally 0.4.13

## Purpose

Correct the public lifecycle classification used after an exact-Natal interactive
initial wave has durably recorded six provider Response identities and has no
ordinary local work to execute.

API Sprint 29 demonstrated the current mismatch: ordinary semantic-closure
`--resume` was repeatedly selected, while the supported
`--provider-reconciliation-cycle` command was never invoked. The six provider
operations completed at OpenAI, but their results were never retrieved or fanned
in.

This sprint is limited to native lifecycle classification, branch evidence,
consumer validation/handoff, provider-free qualification, and concise diagnostics.
It does not redesign the API queue, alter capacity ownership, submit paid work, or
change editorial behavior.

## Frozen incident safety

- The paused QA cohort is evidence only during contract and implementation work.
- Do not restore, inspect in a mutating mode, resume, reconcile, authorize,
  retrieve, deny, or resubmit that retained workspace.
- Reproduce exclusively with generated provider-free fixtures and scripted
  transports.
- Any eventual retained-workspace recovery requires the API to deploy the accepted
  consumer contract, restore the complete exact snapshot at its logical path,
  establish exclusive access, ingest a fresh supported lifecycle inspection, and
  invoke reconciliation only. No provider create is permitted.

## Root-cause hypothesis from current code

Two related semantics permit the loop:

1. `_local_dependencies()` emits `provider_result_reconciliation`, and
   `inspect_lifecycle()` currently reduces `bool(local_dependencies)` to
   `terminal.local_continuation_remains = true`. Provider retrieval custody is
   thereby labelled as ordinary local continuation.
2. Once the earliest `resume_not_before` is due, `execution_capacity` becomes
   `continue_local_cycle` with generic `reason_code=local_work_ready`. The public
   inspection has no closed field distinguishing “invoke provider reconciliation”
   from “invoke ordinary semantic closure resume.” If initial-wave submission and
   checkpoint work consume the initial 15-second delay, the first inspection can
   already land in this ambiguous due state and never produce the API predicate’s
   prior `release_until_due` record.

The correction must separate:

```text
ordinary native local continuation
provider reconciliation not yet due
provider reconciliation due now
```

## Contract direction

- Publish lifecycle inspection `astrowoof.authoring_lifecycle_inspection.v0.4`.
- Preserve v0.3 for historical reading only; do not silently change v0.3 meaning
  under the same identity.
- Add one closed top-level `execution_branch` projection that identifies the
  supported next SBE command independently of capacity disposition.
- Treat `provider_result_reconciliation` as a provider dependency, not an ordinary
  local dependency. For a provider-only wait:
  - `terminal.provider_continuation_remains = true`;
  - `terminal.local_continuation_remains = false`;
  - `local_dependencies = []`;
  - provider action identities/timing remain in validated `provider_custody` and
    `action_inventory`.
- Add the closed capacity reason `provider_reconciliation_due`; retain
  `known_provider_work_pending` for the not-due release state.
- Direct due inspection must select reconciliation even if no earlier API-persisted
  release inspection exists. This removes the initial 15-second race.
- Contradictory branch/capacity/custody/local-continuation tuples fail closed in
  both SBE validation and the API consumer.

Exact proposed values are frozen in `LIFECYCLE CLASSIFICATION CONTRACT AND API
HANDOFF.md` and require API review before implementation.

## Slices

### Slice 0 — Reproduction and invariant freeze

- Build an exact-Natal provider-free fixture that prepares and authorizes one
  six-member initial wave, scripts six successful creates, and durably records six
  unique Response IDs.
- Inspect once before the earliest due time and once at/after it.
- Reproduce the v0.3 contradiction and record all public fields without reading
  private state in the consumer assertion.
- Freeze no-submit/no-retrieve counters around lifecycle inspection.

Gate: reproduction proves the mismatch without touching the retained QA cohort.

### Slice 1 — Lifecycle v0.4 contract and API review

- Add the v0.4 schema proposal, strict validator rules, fixture matrix, contract
  catalog entry, and compatibility notes.
- Freeze the exact `execution_branch`, capacity, continuation, custody, and timing
  tuples from the handoff document.
- Provide API fixtures for not-due release, due reconciliation, ordinary local
  continuation, review/ambiguity, and contradictions.
- Pause for API review before runtime implementation.

Gate: API confirms it can select the command using only validated v0.4 evidence.

### Slice 2 — Native classification and branch diagnostics

- Split provider reconciliation dependencies from ordinary local dependencies.
- Project v0.4 `execution_branch` deterministically from validated native state.
- Preserve all snapshot, single-writer, provider identity, spend, consumer
  authority, and route checks.
- Emit concise non-authoritative structured diagnostics for:
  - lifecycle classification;
  - recommended branch and reason;
  - actual CLI branch invoked and whether it matches the lifecycle recommendation.
- Never emit credentials, prompts, outputs, protected subject data, or raw provider
  bodies.

Gate: provider-only pending is never labelled ordinary local continuation.

### Slice 3 — Provider-free transition and safety matrix

- Initial six-member submit -> immediate not-due release tuple.
- Initial submit whose first inspection is already due -> direct reconciliation
  branch, without requiring a historical release record.
- Not-due inspection performs zero creates and zero retrieves.
- Due reconciliation performs retrieval only for due durable IDs, never creates.
- Repeated inspection and fresh-worker replay remain read-only/idempotent.
- Contradictory fields and missing/legacy timing fail closed.
- Ordinary local continuation retains existing `--resume` behavior.

Gate: no duplicate provider submission or retrieval in the scripted counters.

### Slice 4 — All-six reconciliation and fan-in

- Exercise the production reconciliation adapter with six scripted completed
  Responses.
- Respect the existing four-retrieval-per-cycle bound: first cycle retrieves at
  most four; a subsequent due cycle retrieves the remaining members.
- Prove each provider ID is retrieved no more than once, all six results become
  durable, deterministic fan-in runs, and authoring advances beyond the initial
  provider wait.
- Verify fresh-worker restore between cycles and monotonic evidence.

Gate: all six pass results fan in with create count exactly six total and retrieval
count exactly six total.

### Slice 5 — Installed-wheel consumer qualification

- Build and install the candidate wheel in an isolated `site-packages` target.
- Invoke supported public CLI/API surfaces only.
- Run provider-free installed-wheel scenarios for:
  - six-member create/detach and lifecycle release;
  - due reconciliation selection;
  - all-six fan-in;
  - contradictory lifecycle refusal;
  - no duplicate create/retrieval.
- Publish closed compact receipts and hashes for API adoption.

Gate: API reviews the installed-wheel fixtures/receipt before release.

### Slice 6 — Release handoff

- Update lifecycle, provider reconciliation, API worker integration, and release
  compatibility documentation.
- State the exact recovery procedure and limits for the paused retained workspace.
- Run a narrow affected test set, installed-wheel qualification, wheel boundary,
  and checksum checks.
- Recommend a fresh immutable patch release only after API acceptance.

Gate: Kevin and API approval before tag/publication.

## Testing strategy

### Required native tests

- exact interactive six-member initial wave with six durable IDs;
- inspection before due;
- inspection first observed after due;
- ordinary local continuation control;
- contradictory v0.4 tuple matrix;
- snapshot invalid, ambiguous submission, missing timing, and identity conflict;
- repeated inspection produces no native mutation;
- provider-free reconciliation across the existing four-action cycle bound;
- fresh-worker all-six fan-in;
- exact create/retrieve call counters.

### Installed-wheel gate

The installed candidate must execute the public release/qualification CLI from
`site-packages`, with no repository `PYTHONPATH`, provider credentials, network, or
production input. The receipt must report route, six-member cardinality, create
count, retrieval count, lifecycle tuples, fan-in status, and contradiction refusal.

### Explicitly excluded

- live OpenAI calls;
- mutation of the retained QA cohort;
- Batch or bounded-Natal redesign;
- changes to the four-retrieval cycle limit or backoff policy;
- API queue, lease, slot, reservation, or billing implementation;
- new editorial stages or paid operations.

## Acceptance criteria

- Provider-only pending work has `local_continuation_remains=false`.
- Before due, the inspection safely releases capacity until the exact earliest
  `resume_not_before` and recommends provider reconciliation.
- At/after due, the inspection recommends provider reconciliation directly,
  including when no earlier release inspection was persisted.
- Ordinary local work continues to recommend ordinary semantic closure resume.
- The API can validate and select the command using only public v0.4 evidence.
- Contradictory evidence is machine-rejected.
- Six provider operations are created exactly once, retrieved at most once each,
  and deterministically fanned in.
- Logs/events explain classification and branch choice but carry no authority.
- Existing public-state, snapshot, spend, provider-custody, consumer-authority, and
  delivery invariants remain intact.

## Review pauses

1. Now: Kevin/API review of this plan and the field-exact contract.
2. After Slice 0: API confirms the reproduction matches Sprint 29.
3. After Slice 1: API freezes v0.4 ingestion and command selection.
4. After Slice 5: API reviews installed-wheel fixtures.
5. Before release: final Kevin/API acceptance.

API contract review completed at AstroWoof API commit `4455acc`. The API approved
v0.4 and clarified that SBE may expose only its next bounded retrieval subset (up
to four action IDs); the API must neither select members nor reconstruct a command
from those IDs.
