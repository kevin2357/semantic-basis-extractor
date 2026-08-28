# Slice 4 — Interruption, Replay, and Immutable Review Lineage

## Crash repair

The terminal-review publication protocol now has deterministic cuts after the
journal close, immutable result, full snapshot, snapshot validation, and immutable
receipt. A retry recognizes only two bounded repair cases:

- the indexed final result exists but lacks its receipt; or
- the journal ends with one exact, fully closed, otherwise-unclaimed invocation
  whose revision, route, review outcome, and cause match current native truth.

Anything partial or contradictory remains invalid. Every supported cut converges
on one v0.2 result, one canonical v0.1 receipt, and one semantic invocation close.

## Exact replay and concurrency

An already sealed v0.2 review publication is an exact replay only when command,
native revision, route, review cause, and complete ordered action-inventory digest
still match. A changed custody fact creates a successor checkpoint instead.

Two simultaneous finalizers do not both mutate native truth. One owns the native
writer; the other refuses at exclusivity. Retrying the refused invocation after
the winner completes returns the exact existing publication.

## Immutable review lineage

Custody-only persistence must not demote `FAILED_REQUIRES_REVIEW` to
provider-pending or authoring. Later reconciliation or denial may change action
custody and financial evidence, but it cannot erase the editorial decision.

The original v0.2 result remains byte-identical and independently receipt-valid.
A successor has its own invocation/result/receipt and a journal range beginning at
the prior result's end sequence plus one. API can therefore retain the original
review authority while transactionally ingesting each exact successor returned by
the command it invoked.

This does not widen v0.2 to every successor outcome and does not make latest-result
discovery authoritative.

## Privacy and diagnostics

A failing typed-event sink cannot alter publication. Protected sentinel material
stored in private native provenance is absent from public results, receipts, and
bounded journal exports. Events remain useful diagnostics, never authority.

## Gate

Focused and adjacent tests: 124 passed. The broad semantic-closure suite added 93
passes with one existing pytest return-value warning. No provider/network calls,
spend, or retained-QA access occurred. Slice 5 remains blocked on API review.
