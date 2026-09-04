# API Slice 0 review — terminal-dominance handoff

## Decision

Approved to begin Slice 1.

The source mapping reconciles the two QA traces with one clear native control
flow error: `finalize_subjects()` establishes a native terminal conclusion, but
three coordinator paths continue into qualitative selection and/or emit a
local-progress-shaped result. That is sufficient to explain both:

- Rascal's `DELIVERY_COMPLETE` plus a prepared qualitative-critic request; and
- Madeleine's final-QA-review publication followed by later terminal-lifecycle
  re-entry.

It also confirms that this is not a new provider, custody, retry, optional
adoption, or API-generated semantic failure.

## Required Slice 1 boundary

1. Make the coordinator branch on the **committed finalization/result
   evidence**, including the truthful custody disposition—not merely the
   spelling of a native status. A `review_required` result may retain existing
   provider custody for retrieval/accounting, but it must never select or
   authorize new work.
2. Put that decision before `run_qualitative_review()` and before any
   local-continuation publication in every mapped coordinator. Direct authoring
   must receive the same protection as both reconciliation routes.
3. For a resolved successful delivery, surface the existing delivery handoff;
   for a resolved editorial terminal review, surface its exact terminal result.
   Do not make API reconstruct private native state or infer a successful
   delivery from an unresolved/mixed evidence bundle.
4. The public handoff should preserve the exact sealed result and receipt IDs
   and digests plus terminal outcome/reason and snapshot/checkpoint identity.
   Add one explicit no-new-work/custody disposition assertion so API can fence
   queue re-entry without guessing from prose or status names.
5. Retain typed refusal for malformed, contradictory, or unsupported mixed
   custody. No broad exception suppression is acceptable.

## Requested regression shape

The Slice 2 fixture should prove, at the actual production coordinator level,
that after a terminal conclusion there is no prepared qualitative action, no
external-authority request/grant, and no local-continuation-shaped cycle result.
Keep the retained-provider-review control distinct: it may retain/reconcile
existing provider identity but cannot create a successor action.
