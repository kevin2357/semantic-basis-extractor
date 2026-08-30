# API review — Slice 2 and Voof-paws 3

## Decision

Approved. The retained evidence now proves the relevant authority mismatch:

- API's seven rows exactly match native rows 1–7;
- native row 8, `paid_95b6252fedb1610b3be397d9`, is a distinct providerless,
  prepared retry-3 action absent from API; and
- the valid eight-row terminal-review result was the first public evidence API
  received for that action.

API's strict eight-versus-seven refusal was therefore correct. It had no
external-authority request, admission, grant, provider identity, or lawful
providerless-denial authority for retry 3. The separate API worker containment
fix remains correct, but it cannot make the eight-row terminal result ingestible.

## Ownership assessment for the next slice

The leading corrective ownership is native fan-in/adoption ordering, with a
possible supporting public-publication rule:

1. retry-2 completed in the ledger but remained ambiguous in the pass record;
2. ordinary local work consequently prepared retry-3; and
3. terminal review sealed before API could observe an external-authority
   request for that newly durable action.

This is **not** a reason for API to manufacture an action from the terminal
result, accept a subset, or deny retry 3 retrospectively. It is also not yet
proof that the progress fence itself is faulty; it correctly identified the
inconsistent pass/ledger truth it received.

## Slice 3 requirements

Approved to build the provider-free production-boundary reproduction. Include
both:

1. the retained bad ordering: retry-2 completed in ledger, pass metadata still
   ambiguous, retry-3 prepared, then a truthful eight-row terminal review; and
2. the corrected candidate ordering(s):
   - adopt the completed result into pass/attempt truth before a successor is
     selected, so no erroneous retry-3 is prepared; or
   - if retry-3 is legitimately prepared, publish a validated external-authority
     request and stop at that boundary before any terminal result can require an
     API action join.

Assert that neither path creates a provider action. The bad path must preserve
the strict API refusal; the candidate path must preserve full-ledger terminal
review, retry-2 reconciliation custody, and immutable result history.

Voof-paws 3 is satisfied. Pause at Voof-paws 4 before selecting one correction
or starting implementation.
