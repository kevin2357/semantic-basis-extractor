# API Slice 0 review — approved with one registry clarification

## Decision

API approves Slice 0 and SBE may begin Slice 1 decision-sink enumeration.

The public-fact catalog correctly adopts the most important boundary rule:
availability is discovery only; an exact invocation-returned result identity
outranks exit code and availability discovery; and a discovered result remains
non-authoritative until its exact public result/receipt joins validate. The
catalog, join map, vocabulary table, and registry template are sufficiently
specific to audit API without asking API to reproduce native state.

## Particular strengths

- The version family is treated as differentiated evidence surfaces, not a
  blind fallback ladder.
- The registry requires a **positive permission**, not merely a state that
  looks compatible with the desired action.
- It separately records native facts, API-owned facts, identity joins,
  evidence precedence, and absent/contradictory/unsupported outcomes.
- The explicit distinction between native terminal-result acceptance and API
  job/run terminalization is essential. It prevents a correct native conclusion
  from silently implying settlement, reservation release, or publication.
- Slice 3's mutations include the two highest-value recovery checks: exact
  invocation result versus conflicting discovery, and named recovery discovery
  only where no invocation result ID was returned.

## Required clarification during Slice 1/2 (not a blocker to enumeration)

The catalog says that `review_required` is “not inherently terminal,” while the
current API terminal-ingress/worker path includes `review_required` in its
closed terminal-result set and currently maps that native result to an API job
terminal-close branch. This may be an intentional difference between:

1. a terminal native *editorial* outcome that still retains provider custody
   for reconciliation, and
2. an API job/run terminalization decision that still has custody, settlement,
   and delivery obligations.

Or it may expose a real consumer mismatch. Do not resolve it from the word
`review` alone. The registry must cite the exact SBE v0.2 result fields,
custody finality, continuation assertions, and command-result binding that
authorize (or forbid) each API action. If the current API terminal-close mapper
uses only `outcome == review_required`, classify it rather than presuming the
catalog wording and mapper are already aligned.

## Additional audit guardrails

- In every recovery row, state whether the result ID is invocation-returned or
  availability-discovered. A later “latest” sealed result may never silently
  replace the returned identity.
- Keep `execution_capacity` and checkpoint-safe release as native worker facts;
  their rows must name the additional API lease/slot/reservation transactions
  rather than project an SBE capacity word into an API release.
- Treat the assertion “sealed validated result wins over a log/exit code” as
  conditional on all exact run/invocation/result/receipt/journal/snapshot joins
  having succeeded. A merely present result or a log line still has no such
  precedence.

No API source, SBE source, retained-QA state, provider work, or deployment was
changed by this review.
