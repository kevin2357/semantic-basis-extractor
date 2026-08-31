# API review — Slice 3 production-boundary reproduction

## Decision

**Voof-paws 4 is approved.** The public-CLI witness proves the exact producer
contradiction that API observed in QA:

- final QA warning is reduced to a review-terminal-looking outer status;
- the same checkpoint retains a submitting/provider-pending polish action;
- constrained v2 dispatch nevertheless creates one provider operation; and
- no sealed terminal result exists for API to ingest.

This is the right proof standard. It does not rely on QA mutation, provider
network access, private API reconstruction, or a test-only miniature lifecycle.

## Required Slice 4 preservation rules

1. Correct the status-reducer precedence and add the post-intent/pre-call fence
   as one coherent change; changing only one would leave a contradictory
   intermediate state or an unsafe provider-create route.
2. Preserve the no-custody `FINAL_QA_WARN` control as a genuine sealed review
   terminal. The fix must not broadly turn review outcomes into local work.
3. Retain distinct outcomes for providerless authorized work, call-entry
   ambiguity, durable pending identity, completed-not-adopted evidence, and
   terminal closeout. In particular, no branch may silently deny or replace
   work merely because the reducer sees an editorial warning.
4. The new post-intent refusal must prove zero provider POSTs, immutable
   refused-grant history, and fresh-authority-only re-entry. It must not
   masquerade as an external checkpoint-change refusal.
5. The corrected public lifecycle must present active durable provider custody
   as reconciliation-capable/nonterminal, while API continues rejecting any
   contradictory terminal-plus-custody document.

SBE may proceed with the narrow runtime and dispatch-result correction in Slice
4.
