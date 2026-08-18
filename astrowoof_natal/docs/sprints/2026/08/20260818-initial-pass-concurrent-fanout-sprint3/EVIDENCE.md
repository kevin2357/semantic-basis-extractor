# Initial Authoring Pass Concurrent Fan-Out Sprint 3 Evidence

Date: 2026-08-18
Status: planning only

No implementation or qualification evidence exists yet.

The retained SBE 0.4.6 bounded interactive live run motivating the observed serial
behavior remains outside Git at:

```text
C:\dev\github\semantic-basis-extractor\.runs\kevin-bounded-live-20260818\run
```

It must remain unmodified diagnostic evidence. Its six initial Responses were
created only after the preceding pass completed; it is not evidence of concurrent
fan-out. Full run and cost details are indexed by the cost-calibration sprint.

## Bounded final-QA defect owned by this sprint

All six pass records reached `PASS_QA_ACCEPTED`. Deterministic assembly then found
nine duplicated normalized body passages. They were the nine density/voice body
variants for two selected foundational claims with equivalent North Node editorial
semantics but distinct upstream source objects:

- `bounded_candidate:foundational_object:4e954709d2409ded004714a1`
  (`True_Node`); and
- `bounded_candidate:foundational_object:3bd9d53c7147e3c17dc64619`
  (`Mean_Node`).

The final validator correctly returned `fail` and the bounded lifecycle assigned
`FINAL_QA_REQUIRES_REVIEW`. Shared `persist_state()` then called generic
pass-derived status recomputation, observed six accepted passes, and overwrote the
state with `AUTHORING_COMPLETE`. The final-QA control flow still returned before
polish, so no optional provider request was made, but native/public status was
misleading.

This sprint owns two SBE-native corrections:

1. final-QA/review state has precedence over pass-derived authoring-complete state
   through every persisted and public projection; and
2. equivalent selected bounded claims are rejected before paid authoring with
   typed diagnostic evidence, without silently merging upstream provenance.

SPC remains authoritative for whether bounded projection emits Mean Node, True
Node, or both. The SBE guard is an editorial admission invariant, not an upstream
projection rewrite.

Each slice will add exact commands, scripted timing records, mutation counts,
provider-operation inventories, failure-injection checkpoints, schema/fixture
hashes, installed-wheel identities, and test results here or in a linked compact
result artifact.

## Slice 0

Full report:
[SLICE 0 - Four-Pipeline Baseline and Seam Inventory.md](results/SLICE%200%20-%20Four-Pipeline%20Baseline%20and%20Seam%20Inventory.md)

- New provider operations: 0.
- Focused tests: 5 passed in 8.738 seconds.
- Full source suite: 423 passed in 321.471 seconds; 10 skipped.
- Exact interactive: cache-warmer-plus-five blocking concurrency when caching is
  enabled; no short create-only detach boundary.
- Bounded interactive: six blocking serial passes.
- Exact Batch: one six-member round.
- Bounded Batch: one six-member round.
- Retained bounded live identity span: 588 seconds across six actions.
- Released interactive reconciliation: four parallel due retrievals per cycle.
- Recommendation: proceed to the versioned wave authorization and create-only
  contract in Slice 1.

API review approved the Slice 0 findings with three Slice 1 emphases:

- explicitly remove full-response cache-warmer latency or prove a nonblocking
  create-only alternative;
- treat complete-wave API reservation/SBE authorization as a real cross-repository
  atomicity boundary; and
- preserve four-at-a-time retrieval independently of six-at-a-time initial create.

The Slice 0 report now also states precisely that per-ID ledger/journal durability
is immediate and serialized; only aggregate wave publication waits for all create
tasks to unwind.

## Slice 1

Full proposal:
[INITIAL WAVE CONTRACT PROPOSAL.md](INITIAL%20WAVE%20CONTRACT%20PROPOSAL.md)

Result:
[SLICE 1 - Initial Wave Contract.md](results/SLICE%201%20-%20Initial%20Wave%20Contract.md)

- Proposal identities: prepared wave v1, authorization envelope v1, result v1.
- Fixed create controls: 6 parallel, 15 seconds each, 20-second provider-I/O wave.
- Fixed retrieval controls: 4 due and 4 parallel per cycle.
- Cache policy: `no_serial_cache_warmer`.
- Exact complete API reservation envelope plus six member authorizations required
  before any create/consumption.
- Per-ID ledger/journal persistence is immediate and serialized.
- Batch remains one round action/reservation with six members.
- Strict proposal tests: 8 passed in 0.026 seconds.
- Related lifecycle/route contract tests: 61 passed in 5.889 seconds.
- Provider operations: 0.

## Slice 2

Result:
[SLICE 2 - Transport-Neutral Wave Coordinator.md](results/SLICE%202%20-%20Transport-Neutral%20Wave%20Coordinator.md)

- Added internal `astrowoof_natal_authoring.initial_wave`; not publicly exported and
  not integrated into exact/bounded routes.
- Deterministic content-addressed exact/bounded wave construction.
- Mandatory complete envelope plus six-member preflight before create callbacks.
- Six concurrent external create tasks with coordinator-thread-only persistence.
- Regression proves at least one returned identity is persisted while other create
  tasks remain active.
- Canonical aggregate ordering is independent of completion order.
- Mixed provider-bound, unstarted, refused, and ambiguous results are typed.
- Focused tests: 9 passed in 0.029 seconds.
- Related strict tests: 66 passed in 6.718 seconds.
- Compile and `git diff --check`: pass.
- Provider operations and spend: 0.

## Slice 3

Result:
[SLICE 3 - Exact Interactive Concurrent Submission.md](results/SLICE%203%20-%20Exact%20Interactive%20Concurrent%20Submission.md)

- Fresh exact interactive now prepares one six-action wave at one revision.
- One API wave envelope plus six exact ordered member authorizations is mandatory;
  failed preflight applies no member authority and creates nothing.
- Six create-only POSTs overlap; no initial thread polls and no full-response cache
  warmer runs.
- Each returned Response ID receives an immediate serialized ledger/journal/marker
  write before aggregate detach publication.
- Durable IDs are replay-safe; identity-less interrupted submissions fail closed as
  ambiguous.
- Existing four-at-a-time fresh-worker retrieval and deterministic fan-in remain the
  reconciliation boundary.
- Focused tests: 12 passed in 3.881 seconds.
- Full exact/coordinator suite: 96 passed in 160.701 seconds, plus the subsequently
  added all-or-none regression in the focused pass.
- Compile and `git diff --check`: pass.
- Provider operations and spend: 0.

## Slice 4

Result:
[SLICE 4 - Bounded Interactive Concurrent Submission.md](results/SLICE%204%20-%20Bounded%20Interactive%20Concurrent%20Submission.md)

- Bounded interactive now prepares and authorizes one exact six-member wave, creates
  six Responses concurrently, durably binds IDs immediately, and detaches.
- Bounded prompts, schemas, provider-minimized packets, immutable hydration, and
  pass-local authority remain route-specific and unchanged.
- Create-only and established interactive request objects are equal for one frozen
  bounded pass; Batch remains a transport-only variation.
- `FINAL_QA_REQUIRES_REVIEW` survives all generic persistence and public/native
  projections and cannot be reopened as authoring-complete.
- Equivalent selected Mean/True Node semantics fail before spend with typed code;
  a truly distinct nearby Node case passes.
- Combined bounded/provider-pending/lifecycle suite: 119 passed in 118.177 seconds.
  Focused expanded assertions: 4 passed in 2.698 seconds.
- Provider operations and spend: 0.

## Slice 5

Result:
[SLICE 5 - Batch Compatibility.md](results/SLICE%205%20-%20Batch%20Compatibility.md)

- Exact Batch: one paid round action/reservation, six initial logical members, no
  interactive-wave state.
- Bounded Batch: one paid round action/reservation, six initial logical members, no
  interactive-wave state.
- Route-local interactive/Batch request parity remains exact after documented
  transport normalization.
- Mixed or missing member usage cannot settle a partial aggregate: billing remains
  pending, the reported amount is null, retrieval custody may end, and consumer
  financial authority remains retained.
- Partial/error members, pass-local retries, terminal failures, conflicts,
  detach/not-due/reclaim, replay, and final assembly remain covered.
- Focused parity: 4 passed in 12.288 seconds. Mixed usage: 2 passed in 9.722 seconds.
  Complete Batch-focused suite: 29 passed in 138.277 seconds.
- Provider operations and spend: 0.

## Slice 6

Result:
[SLICE 6 - Failure Atomicity and Lifecycle.md](results/SLICE%206%20-%20Failure%20Atomicity%20and%20Lifecycle.md)

- One complete pre-POST snapshot covers all six `SUBMITTING` decisions without
  serializing six workspace scans ahead of create I/O.
- Every returned ID receives a serialized ledger/journal/marker mutation followed
  by a complete snapshot refresh.
- Exact and bounded crash injection after the first identity checkpoint validates
  the snapshot, reuses the known ID, classifies five unknown submissions as
  ambiguous, and proves the provider transport remains at exactly six calls.
- Zero-through-six known-ID matrix preserves exact provider custody and never
  converts ambiguity into retry authority.
- Exact and bounded six-ID lifecycle inspections return `release_until_due`, six
  custody actions, and six retained consumer-authority actions.
- Combined wave/bounded/capacity/lifecycle/oracle tests: 99 passed in 104.999
  seconds. Native transition/event tests: 29 passed in 3.339 seconds. Full exact
  semantic-closure tests: 90 passed in 172.225 seconds.
- Final-status precedence regression: all-subject delivery closes a reviewed run;
  absent delivery evidence, final QA remains monotonic through persistence.
- Public lifecycle/oracle vocabulary change: none.
- Provider operations and spend: 0.
