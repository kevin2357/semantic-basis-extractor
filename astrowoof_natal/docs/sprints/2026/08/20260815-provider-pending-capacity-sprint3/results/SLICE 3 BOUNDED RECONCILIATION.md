# Slice 3: Bounded Interactive Reconciliation

Status: implementation complete; pending Kevin's Slice 3 gate review.

## Cycle behavior

The native reconciliation engine now:

1. validates the complete stable-path snapshot under the paid-action single-writer
   lock;
2. returns an exact, nonmutating `not_due` result before any provider call when the
   native lower bound has not arrived;
3. chooses at most four due actions by `(resume_not_before, action_id)`;
4. issues one parallel wave of GET-only retrievals, each with a 15-second transport
   timeout and no transport retry;
5. verifies every response against its already durable provider ID;
6. persists pending, completed, or transport-warning timing evidence;
7. persists completed response bytes as immutable private native evidence;
8. consumes completed initial/retry response bytes through ordinary local
   reconstruction and QA without another GET or any POST;
9. exhausts that pass-local work until the next provider/spend boundary; and
10. publishes one cycle artifact, complete snapshot, lifecycle inspection v0.2,
    and typed result checkpoint.

The ordinary blocking authoring path remains available and unchanged. The bounded
operation is retrieval-only: even an already authorized subsequent action cannot
be submitted while the reconciliation-only controller is active.

## Outcome and custody semantics

- Pending and transport-warning results retain the exact provider IDs,
  authorizations, consumption evidence, and consumer-authority classification.
- Completed provider evidence has no future retrieval due time and makes local
  continuation immediately runnable until it is consumed.
- A mixed completed/pending wave runs completed local work and then detaches only
  if another provider barrier remains.
- A provider identity mismatch terminalizes into native review; it is never
  treated as an ordinary transport retry.
- More than four due actions remain untouched for a later cycle. Their attempt
  counters do not advance.
- Poll-only work adds no action, commitment, authorization, consumption, or
  reported cost.

## Failure boundaries

Provider retrieval and native checkpoint publication cannot be one atomic external
transaction. SBE therefore relies on the durable pre-existing provider ID: a
retrieval may safely be repeated, but no submission may be repeated. A failure
before a complete new snapshot never advertises capacity release. The retained
workspace fails closed for recovery/review rather than blessing partial bytes.

The transport callable must honor SBE's 15-second timeout. The packaged OpenAI
adapter freezes one zero-retry GET wave; four parallel actions therefore fit under
the reviewed 20-second cycle allowance with checkpoint overhead reserved.

## Gate evidence

Provider-free tests cover early resume, one and several pending responses, a
parallel wave, mixed completion, six-action cycle limiting, transport warning,
identity conflict, snapshot-publication failure, and completed-response local QA.
The local-QA test proves exactly one GET and zero POSTs: the completed response is
consumed from native evidence without a second provider retrieval.

The final complete repository suite passed all 330 tests in 156.238 seconds.
