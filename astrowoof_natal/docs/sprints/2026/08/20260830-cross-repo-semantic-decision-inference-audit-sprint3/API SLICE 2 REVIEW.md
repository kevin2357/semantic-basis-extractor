# API Slice 2 review — approved for adversarial classification

## Decision

API approves the completed decision registry and SBE may begin Slice 3.

This is the right level of rigor. The registry separates evidence integrity,
native scheduling, API queue/capacity, provider custody and settlement,
terminal-result ingestion, outer product terminalization, and delivery. It
does not flatten these into a seductive but unsafe total status.

## Confirmed strengths

- R-03 correctly corrects the Sprint 60 error: availability gives only an exact
  result identity to validate and classify; it is not terminal authority.
- R-05/R-07 separate provider retrieval from provider creation and name their
  distinct positive permissions.
- R-11 through R-16 correctly split terminal evidence, outer terminalization,
  nonterminal review, delivery, and workspace cleanup.
- R-25 through R-28 make subprocess precedence an auditable contract rather
  than a convention inferred from return codes.
- The six factual tensions are concrete, reachable, and appropriately left
  unclassified until mutations show whether they are contract-backed behavior
  or a consumer gap.

## One wording correction for the registry

In R-03, replace “normal absence continues inspection” with **“normal absence
continues the ordinary selector.”** A fresh run with no available prior result
may enter initial-wave admission directly; a retained run may select a legacy
bridge or lifecycle inspection. “Inspection” alone would accidentally turn the
same sort of proxy into a universal next-state rule.

## Slice 3 requirements reinforced

1. Test the `read_latest_sealed` fallback separately from the named
   availability-preflight path. It is the one remaining place where generic
   latest-result discovery might bypass invocation identity, so a passing
   preflight test cannot certify that fallback.
2. For tension 2/3, distinguish two questions in each fixture:
   - can the API outer job/run/reading close now; and
   - can action-level provider custody/settlement continue afterward?

   Neither answer follows from the word `review_required`.
3. For R-17, mutate an inspection where the explicit local-continuation value
   is absent but the disposition appears tempting. The expected behavior must
   be a typed refusal/review, not an inferred readiness fallback, unless a
   closed versioned contract explicitly sanctions that fallback.
4. For R-05/R-18, include a due/not-due pair with identical provider custody
   and snapshot identity. The mutation should prove API consumes SBE's temporal
   decision/subset, rather than calculating freshness or expanding action IDs.

No source, provider, retained-QA, deployment, or configuration mutation was
made by this review.
