# API Re-review — Slice 1 v0.2 Terminal Review Correction

## Decision

Approved for SBE package qualification.

## Why the added correction is necessary

The new CLI-level regression exposed the actual prerequisite rather than
masking it: a detached `review_required` publication written as native result
v0.1 cannot satisfy the existing closed-custody terminal-review command
contract. Emitting the same-invocation command alone would therefore have
produced a malformed or unauthenticated handoff.

Publishing **only exact detached `review_required` terminal evidence** as
native result v0.2 is the narrow correct response. It reuses the established
terminal-review command contract, leaves delivery and nonterminal result
versions alone, and does not expand any discovery or observation authority.

## Regression evidence accepted

- The real detached terminal-review CLI test preserves exit code `3` while
  producing exactly one valid v0.1 terminal-review command plus the ordinary
  reconciliation cycle result.
- The command is validated against the just-published native result and
  receipt, so it proves the invocation/result/receipt join rather than merely
  line presence.
- The nonterminal detached exit-3 regression proves no terminal command leaks
  into provider-pending behavior.

## Remaining API work

API must still accept the valid terminal-review command on this detached
exit-3 route and use the delivery command to establish authority before first
publication. The later delivery-validation retry remains prohibited from
rediscovery. Those are consumer changes; they do not block SBE package
qualification of this exact producer correction.

