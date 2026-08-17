# Slice 3 Exact-Natal Batch Reconciliation

Date: 2026-08-16  
Status: complete; awaiting gate review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

Exact-Natal Batch work with an authoritative Batch ID can now release its worker,
be restored on a fresh worker, and run one bounded retrieval-only reconciliation
cycle. The cycle cannot upload a File, create a Batch, or submit a Response.

## Implemented behavior

- Batch identity persistence now records the Batch-specific durable timing policy.
- Lifecycle inspection admits only a validated exact-Natal Batch round/ID binding.
- One due cycle retrieves at most one known Batch ID through the frozen Batch
  timeout and backoff contract; an early cycle is strictly nonmutating `not_due`.
- Pending and transport-warning outcomes persist one coherent checkpoint and a
  later `resume_not_before` without immediate spin.
- Terminal Batch objects and downloaded output/error JSONL are durable before
  interpretation.
- Completed output is preflighted atomically for exact `custom_id` membership,
  disjoint output/error membership, parseability, and duplicates before any member
  is ingested.
- Member ingestion uses a cache-only transport whose upload/create methods raise;
  newly unblocked deterministic assembly/QA is exhausted before detaching.
- Replay and crash recovery consume durable evidence without a second provider
  retrieval or replacement submission.
- Failed, expired, and cancelled Batch rounds end retrieval custody while retaining
  consumer authority with
  `provider_usage_unavailable_billing_reconciliation_pending`; absent usage is
  never represented as zero spend.
- Terminal output-integrity conflicts likewise end provider polling after bytes are
  durable while retaining consumer authority for review.

## Safety and failure coverage

Coverage includes pending/completed/replay, failed/expired/cancelled, retrieval and
download transport warnings, identity conflict, unknown status, missing/unknown/
duplicate/malformed member evidence, concurrent resume, and injected interruption
after terminal-object persistence, file persistence, member ingestion, local
continuation, and final state persistence.

The local-continuation injection initially exposed an unsafe ordering: final output
mutations could precede the checkpoint used by the injected restart. The ordering
was corrected so the native state and complete workspace snapshot are coherent
before that boundary. Every injected restart now validates the snapshot and resumes
without File upload, Batch creation, or duplicate retrieval after ingestion.

## Tests

The complete repository suite passed all 350 tests in 198.857 seconds.

`git diff --check` is required at the gate. No network transport, API key, provider
endpoint, build, version bump, release, or tag operation was used.

## Gate conclusion

A known exact-Natal Batch operation now has bounded, retrieval-only, replay-safe
worker semantics. Unsafe or financially incomplete evidence remains explicitly
retained under the appropriate provider-custody or consumer-authority projection.
Bounded-Natal interactive parity remains Slice 4 work.
