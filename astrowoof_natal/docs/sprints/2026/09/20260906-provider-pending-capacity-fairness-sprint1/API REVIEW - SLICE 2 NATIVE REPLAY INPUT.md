# API review — Slice 2 native replay input

## Decision

Approved. The input has the right narrowness and preserves the crucial
semantic distinction: the six-due/four-cap fixture is immediately actionable
native work, not a provider-wait handoff.

The canonical subset and untouched suffix (`1,4,5,6` then `2,3`) are exactly
the kind of concrete, public final evidence API needs to avoid guessing from
counts or trace timing. API will not convert that outcome to
`release_until_due` merely to improve peer latency.

## API counterpart status

API Slice 1 is now complete (`514f6b8` on API `main`). It established:

1. final `release_until_due` already releases capacity and admits a peer;
2. final `continue_local_cycle` retains the one-slot owner and excludes a ready
   peer under current allocation-aware selection;
3. Sprint 58 is a terminal-precedence negative control, not a demonstrated
   healthy provider-pending regression; and
4. `8c389b3` is a retry-ceiling terminal-cleanup positive control only.

The remaining joint decision is therefore an explicit policy/contract question:
whether another existing durable final boundary can authorize a bounded peer
turn, or whether a new versioned cooperative-yield contract is needed. No
runtime policy is approved by this review.

## Minor documentation follow-up

When SBE next updates `PLAN.md`/`EVIDENCE.md`, please replace the now-stale
statement that the API historical replay is pending with the completed API
Slice 1 classification above. The joint Slice 2 policy review is the next gate.
