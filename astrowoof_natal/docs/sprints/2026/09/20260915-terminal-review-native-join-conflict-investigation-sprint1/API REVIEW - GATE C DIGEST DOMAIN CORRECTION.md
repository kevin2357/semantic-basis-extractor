# API review — Gate C digest-domain correction

## Decision

Approved for the narrow SBE implementation described in Slice 2.

The evidence establishes one shared, review-only consumer defect rather than
two witness-specific data problems:

- each v0.2 producer disposition agrees with the producer's closed
  terminal-action projection in all 15 retained action joins;
- none agrees with a digest of the complete ledger binding; and
- the successful delivery control bypasses this review-only disposition join.

That is enough to assign ownership to the SBE capture consumer. API has no
lifecycle, custody, terminal-selection, or external contract change to make
for this correction.

## Approved correction boundary

- Centralize the canonical closed terminal action-binding projection/digest and
  use it in both the v0.2 producer and editorial capture consumer.
- Keep the exact action-ID, cardinality, missing/duplicate, and conflicting
  disposition checks.
- Keep full ledger bindings useful as evidence, but do not use their extra
  producer-irrelevant fields to redefine the sealed digest identity.
- Do not accept either digest opportunistically, rewrite historical results,
  add latest-result discovery, or alter result/receipt schemas.

## Qualification expectations

The proposed provider-free regressions are appropriate. Please also ensure the
successful-review artifact assertion is derived from the exact fixture's
action/deck inventory rather than hard-coding the prior delivery control's
eleven rows: a review route may legitimately have a different action count.

The live follow-up should use a fresh ordinary terminal-review witness and
confirm, from the same exact terminal result, that capture produces a canonical
packet, its projections, and the corresponding longitudinal artifact bundle.

No API release or deployment is needed until an SBE implementation is
qualified and released.

