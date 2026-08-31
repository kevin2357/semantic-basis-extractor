# API review — Slice 1 and Oauf-paws 3

## Decision

**Approved to proceed to Slice 2 causal classification and invariant freeze.**
Generation 11 supplies the missing authoritative native/API join. No generation
10 retrieval is needed for the v2 defect. The worker remains suspended and this
approval does not authorize recovery, provider I/O, reconciliation, mutation,
or another remote storage read.

## Confirmed classification

The leading conclusion is now sufficiently supported: this is a **general SBE
sequential-v2-action lifecycle defect**, not API grant inconsistency, polish
request identity drift, or a provider failure.

The exact facts are compatible and jointly decisive:

- API supplied a coherent, exact polish v2 request/grant chain.
- The new native polish action is providerless, unconsumed `PREPARED` work.
- The retained singleton intent instead belongs to completed creative-retry
  action `paid_707…`, yet remains `PROVIDER_PENDING` while that action is
  already `REPORTED` with durable provider identity.
- The current singleton-intent handling mechanically converts that stale
  predecessor into the observed `action_state_or_custody_mismatch` followed by
  `authorization_mismatch`, before any polish provider call.

The append-only local-work error remains an adjacent incident fact with a
generation-11 evidence ceiling. It must remain separately labelled and must not
be made a precondition for repairing the now-proven stale-intent defect.

## Required Slice 2 contract shape

Freeze the invariant as an explicit lifecycle rule, not an accidental field
clearing detail:

1. The singleton dispatch-intent slot represents only one *currently active*
   v2 dispatch authority.
2. An intent may be retired only after exact terminal predecessor evidence is
   joined to its action/request/grant/inventory and provider custody is safely
   resolved.
3. Provider-pending, submitting, ambiguous, mismatched, or otherwise
   unjoinable evidence must retain/refuse/review; it must never be cleared just
   to admit the successor.
4. Once retirement is lawful, a subsequent independent ordinary v2 action may
   establish its own exact intent under the same writer fence.
5. The historical intent, if retained as an archive/journal fact, must not act
   as live dispatch authority. Replays must remain idempotent and cannot create
   a duplicate provider request.

Please state the exact terminal evidence and refusal precedence required for
retirement, then construct the two-sequential-action provider-free proof before
proposing implementation.
