# Plan — Partial reconciliation concurrent snapshot mutation

## Status

Investigation complete. Owner/API review selected the already-released 0.4.36
worker/coordinator correction and no new runtime patch or release. Slice 1 was
skipped because trace, historical source, and immutable-wheel reproduction were
decisive without retained R2 access. Slices 3–6 are superseded here; the broader
quarantine/interruption contract proceeds in the following sprint instead.
No retained-workspace access, provider work, repair, runtime change, release,
or deployment has begun.

## Objective

Explain and reproduce Kardamom Kaboom's partial-reconciliation failure, then
freeze the narrowest correction that preserves all three required properties:

1. restored checkpoints are exact and tamper-evident before execution;
2. approved local work can evolve native output under one serialized
   coordinator checkpoint; and
3. concurrent pass-local computation cannot observe, validate, or publish a
   half-mutated shared workspace.

The investigation must distinguish a true concurrent-writer race from a wrong
snapshot-validation boundary or an inventory leak caused by temporary files.

## Frozen incident facts

- QA cohort and SBE worker remain suspended.
- A validated lifecycle selected four due retrievals from six retained provider
  actions.
- Two retrieved actions completed; two remained in progress.
- SBE then selected ordinary local work for two completed passes and launched
  `author_pending_passes(..., max_workers=2)`.
- Snapshot validation observed equal-but-different 390-member inventory and
  later a 420-member inventory, then the public reconciliation command exited
  nonzero without an adoptable result.
- API retried the same failed command. No provider work or retained-run action
  is authorized during this sprint.
- The affected worker used SBE `0.4.35`; this is the final investigation whose
  historical trace predates the `0.4.36` workspace/state/decision summaries.

## Source findings guiding Slice 0

The exact-interactive reconciliation path currently:

1. retrieves a bounded due subset;
2. derives completed pass IDs;
3. calls `author_pending_passes()` with up to the response reconciliation
   parallelism limit; and
4. allows each pass worker to create/copy/validate pass-local files while
   `save_state()` publishes a snapshot of the entire shared run directory.

`state_lock` serializes state mutation and individual save calls, but it does
not serialize all pass-local filesystem writes against those whole-workspace
snapshot publications. That makes a real race plausible. It is not yet proof:
the exact 30 additional members and the validator call site must be identified.

## Safety and authority boundaries

- Provider mode: provider-free scripted transports only.
- Retained QA: no resume, reconciliation, repair, provider GET/POST, deletion,
  denial, or mutation.
- R2 access, if needed, requires an API-supplied exact checkpoint coordinate
  packet and is limited to one exact `HEAD` and one exact `GET`; no listing.
- Restored retained bytes remain read-only. Reproduction occurs only in a
  separately copied/sanitized fixture workspace.
- Logs are diagnostic evidence, never mutation or custody authority.
- Do not weaken `validate_workspace_snapshot()` globally.
- Do not solve the race by serializing provider retrieval; retrieval fan-out and
  local native mutation have different safety requirements.

## Core invariants to freeze

1. Snapshot validation occurs at stable command-entry/publication boundaries,
   not against a workspace another approved local writer is changing.
2. One coordinator owns mutation/publication of run-wide authoritative state.
3. Pass-local workers may compute concurrently only in disjoint private staging
   roots whose contents are excluded from authoritative state until adoption.
4. Adoption into native pass truth is serialized and produces one complete
   successor checkpoint.
5. A completed provider response is never resubmitted merely because its local
   adoption failed or was interrupted.
6. Pending members retain provider custody while completed members fan in.
7. A command failure before successor publication must be typed and
   non-retryable unless the prior checkpoint still proves a safe supported
   operation; generic `CalledProcessError` retry loops are unacceptable.
8. Single-pass and multi-pass continuations must have identical semantic
   outcomes, differing only in bounded computation latency.

## Investigation matrix

| Retrieved subset | Local continuations | Expected property |
|---|---:|---|
| all pending | 0 | nonmutating detach |
| one completed, remainder pending | 1 | deterministic adoption + retained custody |
| two completed, remainder pending | 1 (forced serial) | two serialized adoptions succeed |
| two completed, remainder pending | 2 concurrent | no shared-workspace race; same successor truth |
| four completed, two pending | up to 4 | bounded computation, serialized adoption/publication |
| all completed | 6 | complete fan-in without new provider creation |
| completed response malformed/identity-conflicting | any | typed refusal/review; no unrelated create |
| interruption before adoption | any | prior checkpoint valid; replay adopts without create |
| interruption during publication | any | no valid partial checkpoint becomes consumable |

The same mechanism must be assessed for initial attempts, creative retries,
polish, critic, and candidate. Batch and bounded routes receive applicability
assessment before any runtime widening.

## Slices

### Slice 0 — trace reconstruction and source-boundary characterization

Correlate `C:\tmp\sbe_worker_logs.txt` with exact source boundaries in SBE
`0.4.35` and current main. Produce a timestamped causal sequence identifying:

- the two completed and two pending retrieved actions;
- selected pass IDs and their attempt/action/provider identities;
- every validation, save, snapshot, staging-copy, QA-report, and accepted-copy
  boundary reached after retrieval;
- whether the first 390-member mismatch reflects changed bytes/metadata with
  stable paths;
- the provenance of the 30 later members; and
- the exception path that escaped without a typed public result.

Add failure-injection hooks or a test-only inventory-diff recorder around the
existing production functions. The recorder must report relative path,
added/removed/changed classification, size, and digest—not file contents.

Deliverables:

- `SLICE 0 - INCIDENT TIMELINE AND MUTATION BOUNDARY MAP.md`
- provider-free characterization demonstrating the current validation failure
- exact inventory delta evidence
- `LOG.md` and `EVIDENCE.md`

**Paws point 1:** confirm the causal class before contract or runtime design.

### Slice 1 — retained checkpoint confirmation, only if still necessary

If Slice 0 cannot identify the writer/path provenance from source and logs,
request one exact active-checkpoint coordinate packet from API and obtain new,
explicit owner authorization for the named object. Only then perform the
packet-authorized `HEAD` and conditional `GET`, validate object/archive/
snapshot identities, and restore to an isolated read-only directory.

Record:

- checkpoint generation/object/version/ETag and expected hashes;
- snapshot member count and state revision;
- six-action custody/reconciliation inventory;
- pass attempt roots and the exact pre-failure snapshot; and
- whether the retained checkpoint predates all conflicting local writes.

Do not make this slice mandatory if the provider-free production reproducer is
already decisive.

### Slice 2 — deterministic concurrency reproduction

Construct a provider-free fixture at the post-retrieval boundary with two
completed and four pending initial-wave actions. Use barriers to control:

- worker A staging creation;
- worker B staging creation;
- state persistence;
- snapshot enumeration/hash; and
- pass QA/adoption.

The reproduction must preserve the historical 0.4.35 relationship rather than
stop at a generic manifest race: worker-thread `save_state()` must reach the
sealed-result reader and whole-workspace validator while a sibling writes its
request/response artifacts. Run the same production-shaped fixture against an
installed 0.4.35 wheel and an installed 0.4.36/current-main artifact. Do not
call the latter fixed unless complete native parity, interruption behavior,
terminal-review preservation, and typed-exit behavior all pass.

Prove the failure deterministically rather than relying on scheduler luck.
Run the same fixture with one selected pass, `max_workers=1`, and
`max_workers=2`. Capture exact inventory deltas and demonstrate whether the
race is:

- snapshot publication versus pass-local file writes;
- one snapshot publication versus another;
- validation versus temporary/native output creation; or
- shared state/file adoption beyond the snapshot layer.

**Paws point 2:** review reproduction and choose correction family.

### Slice 3 — correction contract and interruption model

Freeze one of these correction families based on evidence:

1. **Concurrent private compute, serialized adoption:** workers produce
   disjoint staged outcomes; coordinator validates and adopts each under the
   writer, then publishes one successor checkpoint.
2. **Serialized local continuation:** retain concurrent provider retrieval but
   deliberately execute native fan-in one pass at a time for the first patch.
3. **Explicit mutation epoch:** a more general coordinator-owned transaction
   boundary, only if existing staging/adoption seams cannot express safety.

The contract must name:

- immutable input basis for every worker;
- allowed private output roots;
- coordinator adoption order;
- snapshot publication point;
- interruption outcomes before/during/after adoption;
- replay/no-duplicate-create guarantees; and
- typed public failure when safe progress cannot be proven; and
- the exact distinction between an irrecoverable, non-retryable native
  review/refusal and a prior checkpoint that affirmatively proves one safe
  replay. A child-process exit code is never replay authority.

Completed-but-unadopted provider evidence remains retrieval-only throughout
either outcome. A failed local adoption cannot reopen provider creation.

Default preference: private concurrent compute with serialized adoption, if it
can reuse existing pass-local roots without a large redesign. A short-term
serialized correction is acceptable if it is substantially safer and preserves
semantic behavior.

**Paws point 3:** API reviews the public result/retry implications before code.

### Slice 4 — narrow runtime correction

Implement the approved boundary without weakening entry snapshot validation.
Keep run-wide state mutation and successor publication under one coordinator.
Ensure worker threads cannot invoke whole-workspace snapshot publication while
another worker is producing local files.

Add bounded `✨🐶` diagnostics (now available in `0.4.36`) for:

- immutable input fingerprint;
- local continuation selection and concurrency;
- staging/adoption start and completion;
- inventory delta category on refusal;
- pre/post revision and snapshot digest; and
- typed exit/publication result.

### Slice 5 — route/stage and replay regression matrix

Provider-free coverage must include:

- mixed completed/pending initial wave, 1/2/4 completed members;
- single-worker versus concurrent-worker semantic parity across complete
  native truth, ordered action/attempt inventory, public result, checkpoint,
  and snapshot—not merely successful process exits. Any intentional ordering
  normalization must be stated and tested;
- creative retry fan-in;
- applicable polish/critic/candidate continuation;
- identity mismatch/malformed response;
- interruption and exact replay;
- no seventh create and no re-retrieval of already durable evidence;
- pending custody retained after completed-member adoption;
- snapshot exactness at every published checkpoint; and
- logger/event-sink failure isolation.

Assess bounded interactive and Batch explicitly. Add runtime coverage only when
they share the faulty exact-interactive mechanism; otherwise document why they
are unaffected.

### Slice 6 — installed production-boundary qualification and handoff

Package a provider-free qualification that invokes the real reconciliation
entrypoint from an installed wheel with scripted 2-completed/2-pending
retrieval. It must prove:

- bounded retrieval remains concurrent;
- local processing cannot corrupt snapshot validation;
- completed members become durable native truth;
- pending members remain retrieval-only custody;
- exact replay creates no provider operation;
- returned public result/checkpoint validates in a fresh process; and
- trace evidence explains selection, staging/adoption, publication, and exit.

Produce an API handoff stating whether the prior retryable command failure must
be remapped, or whether the corrected SBE command always returns a sufficient
typed result.

**Paws point 4:** final owner/API release review. No tag/publication without
explicit owner approval.

## Test/release posture

This likely requires a fresh SBE patch release because the correction touches
the production reconciliation/local-adoption boundary. The release gate should
be risk-proportionate but cannot be “logging only”:

- focused deterministic concurrency and replay matrix;
- affected lifecycle/reconciliation/initial-wave tests;
- installed provider-free partial-reconciliation qualification;
- generic installed smoke;
- deterministic committed-source wheel rebuild; and
- broader suite decision made after the correction surface is known.

Freeze the fresh version before any broad release run. Do not rerun a broad
suite merely because the version was bumped afterward.

## API companion expectations

API continues to:

- invoke only SBE-selected run-level commands;
- avoid selecting completed members or reconstructing pass topology;
- ingest exact typed SBE results before scheduling another command;
- retain custody/reservations for pending provider actions; and
- treat contradictory or absent SBE publication evidence as review, not a
  generic retry loop.

SBE does not assert API lease, slot, queue, reservation, or billing facts.

## Open questions for Slice 0

1. Which exact validator call produced each mismatch: command-entry,
   authority/payload resolution, native-result publication, or another reader?
2. Did one worker publish a valid snapshot that immediately became stale when
   the second worker created files, or was the first publication itself built
   from a moving inventory?
3. Are the 30 new members a complete second response/staging tree, QA outputs,
   temporary atomic-write files, or a combination?
4. Does `save_state_locked()` publishing only state (not snapshot) participate,
   or is the race entirely through `save_state()`?
5. Can current pass-local computation be cleanly separated from native
   adoption, or does provider/QA code mutate shared state throughout?
