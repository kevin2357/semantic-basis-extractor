# Muffin Local-Resume Quiescent-Loop Investigation — Sprint 1

Date: 2026-08-25
Status: closed before Slice 0; transferred to API after exact wrapper diagnosis
Starting release: SBE 0.4.25
Expected release: none on accepted evidence; fresh patch only if contrary native evidence emerges

## Review disposition

API review located the defect in the API worker wrapper, not in SBE's v0.7
contract or native executor. The wrapper reduced the complete lifecycle result to
`not inspection.release_until_due`, incorrectly classifying typed
`retain_for_review` and `unsupported_retain_capacity` outcomes as local
continuation.

Accordingly:

- none of the implementation slices below is authorized or required;
- SBE 0.4.25 remains the accepted native contract;
- the API sprint owns the typed result translation and starvation regression;
- the API also owns the separate expired-lease reaper/reset-precondition repair;
- Muffin and Biscotti remain frozen until the API's supported recovery/reset gates
  permit action; and
- no SBE release will be produced from this sprint unless new evidence contradicts
  the accepted diagnosis.

The original plan is retained below as a contingency investigation plan and an
audit record of what would have been tested had the boundary remained uncertain.

## Original contingency objective (not executed)

Eliminate the scheduler-visible no-progress loop in which SBE advertises a concrete
post-fan-in `ordinary_resume`, the supported native command returns quiescent
without consuming that work, and the same semantic operation is scheduled again.

The corrected release must prove through real production entry points that every
advertised local operation either advances native truth exactly once or yields a
different closed, non-spinning disposition.

## Scope

In scope:

- exact-Natal and bounded-Natal interactive creative-retry fan-in;
- the join from durable reconciliation response evidence to pass/attempt state;
- lifecycle v0.7 selection, execution, consumption, and successor evidence;
- ordinary-resume no-progress refusal;
- installed-wheel provider-free qualification correction;
- API consumer handoff for scheduling and capacity release; and
- fleet-level companion recommendations based on native evidence.

Out of scope:

- retained Muffin/Biscotti mutation or recovery;
- live provider calls or dashboard-based inference;
- new retry policy, editorial prompts, quality rules, or spend defaults;
- queue/capacity implementation inside SBE;
- Batch or optional-stage expansion unless characterization proves the identical
  production defect in an already supported route; and
- API-owned reservations, leases, billing, entitlements, or publication policy.

## Frozen invariants

1. SBE alone selects and executes native local work.
2. API invokes only a supported run-level command; it never executes inventory members.
3. Provider custody outranks local work; ambiguity remains fail-closed.
4. An operation is consumed only after its underlying native mutation is durable.
5. Cumulative consumed-operation history remains append-only.
6. The same semantic operation cannot be renamed by a checkpoint republish.
7. No-progress ordinary resume is a contradiction/refusal, not schedulable quiescence.
8. API ledger history is not reconstructed into native state.
9. Frozen QA workspaces remain untouched throughout development and qualification.
10. Logs are diagnostic; lifecycle/result/receipt artifacts remain authoritative.

## Slice 0 — Reproduce the real production failure

- Build a sanitized exact-Natal workspace through supported runtime preparation,
  initial authoring, creative-retry preparation, scripted provider creation, and
  real provider reconciliation.
- Persist a completed creative-retry response through the same reconciliation
  adapter/artifact path used in production.
- Invoke public lifecycle v0.7 inspection and record the exact local-work inventory.
- Invoke the actual ordinary semantic-closure resume command without mocking
  `author_pending_passes`, pass ingestion, retry evaluation, or state persistence.
- Reopen in a fresh runtime and compare:
  - run revision and snapshot;
  - pass/attempt state;
  - action state and reported evidence;
  - reconciliation response artifact;
  - advertised/consumed operation keys;
  - selected command and disposition; and
  - provider create/retrieval counts.
- Run the same characterization for bounded interactive if its real continuation
  shares the affected adapter.
- Identify the first production function and exact predicate at which durable
  completed evidence ceases to advance.
- Record why the current v2 qualification and mocked regression did not catch it.

Gate / voof-paws 1: owner and API review the real reproducer, exact missing join,
route applicability, and proposed outcome semantics before code changes.

## Slice 1 — Freeze truthful execution and no-progress contracts

- Decide whether the correction belongs in:
  - reconciliation-to-attempt materialization;
  - ordinary authoring continuation;
  - a route-neutral local-operation executor; or
  - a narrow combination of those boundaries.
- Freeze the preconditions and postconditions for
  `provider_result_fan_in_and_retry_evaluation`.
- Define a closed no-progress outcome/reason. Prefer the smallest compatible
  evolution, but do not widen a closed public schema silently.
- Specify whether lifecycle v0.7 can express the successor safely or whether a
  fresh lifecycle/result version is required.
- Require that successful execution binds prior operation key, prior basis,
  resulting native mutation, cumulative consumption, successor basis, and next
  selected command.
- Require no-progress refusal to bind the attempted operation/basis while exposing
  no create/retrieval authority and no new schedulable ordinary resume.
- Freeze exact/bounded parity and explicitly classify Batch/optional-stage cells.
- Publish sanitized proposed fixtures for:
  - successful retry-result ingestion;
  - accepted retry/no further retry;
  - rejected retry/retry-2 authority;
  - retry exhaustion;
  - malformed/missing response artifact;
  - action/pass/attempt binding mismatch;
  - stale operation inventory;
  - already-consumed operation replay; and
  - genuine native no-progress contradiction.

Gate / voof-paws 2: API approves schemas, result vocabulary, scheduling meaning,
and capacity-release interpretation before runtime mutation.

## Slice 2 — Implement the real production executor

- Correct the proven reconciliation-to-pass join or add the narrow route-aware
  executor selected in Slice 1.
- Resolve response evidence only from exact snapshot-declared, action-bound native
  references; do not recursively discover candidate artifacts.
- Revalidate under the native single writer:
  - run/route identity;
  - action binding and provider identity;
  - response artifact identity/hash;
  - pass/attempt lineage;
  - current local-work inventory/basis; and
  - absence of conflicting provider/ambiguity evidence.
- Apply deterministic ingestion, pass acceptance/rejection, retry evaluation, and
  next-action preparation as one coherent native progression.
- Persist the underlying mutation before appending operation consumption.
- Reinspect the successor under the writer and validate progress-or-disposition.
- Preserve provider I/O at zero during this local phase.
- Refuse malformed, stale, conflicting, or incomplete evidence before mutation.

Gate: focused exact/bounded source tests prove real ingestion and byte-identical
nonmutation for every refusal cell.

## Slice 3 — Enforce no-spin command semantics

- At the supported ordinary-resume command boundary, compare the selected prior
  operation with the post-command lifecycle result.
- If the prior operation was neither consumed nor replaced by a different truthful
  disposition, emit the closed no-progress failure instead of generic quiescence.
- Ensure the failure is machine-readable in native result/lifecycle evidence and
  cannot be mapped back to executable `ordinary_resume` on the same basis.
- Emit bounded, redacted, failure-isolated diagnostics containing only safe IDs,
  operation kind/key, basis digests, selected command, and failed predicate.
- Add interruption tests around:
  - response materialization;
  - pass mutation;
  - retry evaluation;
  - state/snapshot persistence;
  - operation-consumption persistence; and
  - successor inspection/publication.
- Prove exact replay and fresh-worker recovery never duplicate provider I/O or
  consume an operation twice.

Gate / voof-paws 3: API reviews the final native result and confirms its scheduler
cannot requeue the same no-progress operation or retain capacity indefinitely.

## Slice 4 — Replace the misleading qualification cell

- Preserve provider-pending qualification v1 unchanged as historical evidence.
- Correct/supersede v2 only through a fresh schema version if changing its claimed
  semantics would make the published v2 statement historically false.
- Build an installed-wheel, provider-free qualification that uses:
  - real initial authoring/retry preparation;
  - real scripted provider create;
  - real reconciliation artifact persistence;
  - public v0.7 inspection;
  - actual ordinary resume without mocked mutation;
  - fresh-process reopening;
  - exact operation consumption and successor selection; and
  - exact replay/no-seventh-create/no-duplicate-retrieval checks.
- Cover exact and bounded routes where Slice 0 proves applicability.
- Include a deliberate no-progress/fault-injection cell and prove it yields the
  closed refusal rather than schedulable quiescence.
- Publish a strict concise receipt, schema, reader, CLI, fixture hashes, privacy
  sentinel coverage, and malformed/extra-key/version tests.

Gate: isolated installed wheel passes with no credentials, network, provider spend,
retained workspace, or production input.

## Slice 5 — API handoff and starvation-proof release rule

- Document the exact mapping for successful local progression and no-progress
  refusal.
- State explicitly that API must not infer actionability from
  `local_continuation_required=true` alone.
- Require the API to validate the operation inventory and successor progress before
  scheduling another ordinary cycle.
- Recommend a fleet-level defensive rule:
  - same native operation key/basis plus quiescent/no-consumption result is blocked
    for review;
  - release the run's long-lived capacity allocation according to API policy;
  - do not release provider/spend authority unless native evidence supports it;
  - permit other due provider-reconciliation jobs to proceed.
- Keep that API rule a consumer requirement, not an SBE assertion of API capacity.
- Publish a paired trace showing Muffin-like no-progress cannot starve a
  Biscotti-like due reconciliation.

Gate / voof-paws 4: API accepts the consumer handoff and companion defense before
release qualification.

## Slice 6 — Release qualification

- Run focused lifecycle, reconciliation, exact/bounded retry, pass acceptance,
  authority, snapshot, privacy, interruption, and installed-wheel suites.
- Run the broad source release suite.
- Build twice from one committed source identity with fixed `SOURCE_DATE_EPOCH` and
  prove byte-identical wheels.
- Install the candidate into a fresh Python 3.11 environment with exact SPC 0.11.1.
- Run generic installed smoke and the corrected post-fan-in qualification.
- Record source/dependency/resource/wheel/receipt/fixture hashes.
- Confirm provider/network/spend and frozen Muffin/Biscotti access remain zero.
- Pause for final owner/API authorization before tag or publication.

Gate / voof-paws 5: explicit release approval.

## Required failure-injection matrix

| Boundary | Required proof |
| --- | --- |
| Before response-artifact read | refusal; no mutation |
| Missing/extra/wrong response artifact | refusal; no recursive discovery |
| Response/provider identity mismatch | review/refusal; zero provider I/O |
| Wrong run/route/action/pass/attempt binding | refusal; no mutation |
| After deterministic parse, before pass mutation | replay safely recomputes locally |
| After pass mutation, before state checkpoint | no valid partial snapshot |
| After state checkpoint, before consumption append | recovery recognizes native progress and seals consumption exactly once |
| After consumption, before successor publication | replay returns the same truthful successor without re-execution |
| Stale v0.7 inventory | refusal before mutation |
| Already-consumed operation | exact replay/refusal; no new checkpoint |
| Genuine executor no-op | typed no-progress; never generic quiescent defer |
| Event sink failure | native outcome unchanged |
| Protected-data sentinel | absent from logs/events/public fixtures/receipts |

## Test strategy

Use four concentric levels:

1. Unit tests for closed joins, response resolution, progress predicates, and
   no-progress classification.
2. Production-path source tests entering real reconciliation and ordinary command
   surfaces without mocked native mutation.
3. Fresh-process provider-free qualification from the installed wheel.
4. API companion trace proving the consumer releases fleet capacity on the typed
   contradiction without inventing native/provider/spend facts.

Mocks may replace only the external provider transport. They may not replace the
native mutation whose existence the test claims to prove.

## Exit criteria

- The Muffin topology is reproduced without accessing Muffin.
- The first missing production join is proven and corrected.
- Real ordinary resume consumes advertised local work or returns a different closed
  disposition.
- The same semantic operation cannot enter an unbounded defer/reclaim loop.
- Exact/bounded supported routes pass holistic installed-wheel qualification.
- The qualification no longer injects the mutation it claims to test.
- API can prevent one bad run from starving a due reconciliation without
  reconstructing private SBE state.
- No provider work, spend, or retained-run mutation occurs during development.
