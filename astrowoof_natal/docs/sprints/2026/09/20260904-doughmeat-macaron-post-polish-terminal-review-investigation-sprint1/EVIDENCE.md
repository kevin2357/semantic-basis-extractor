# Evidence index

| Evidence | Status | Notes |
| --- | --- | --- |
| API custody snapshot | observed | Both runs terminal; 8 reported actions each; capacity released. |
| Per-run SBE trace summaries | observed | Native `FINAL_QA_REQUIRES_REVIEW`; no pending provider custody. |
| Four bounded worker-log exports | preserved | Paths and collection window are in `BACKGROUND.md`. |
| Deterministic per-run timelines | complete | Both runs used two exact polish actions, adopted both completed responses, retired both intents, and sealed review results. |
| Terminal local-dependency source meaning | complete | The one dependency is `native_state_repair_review / final_qa_review_required`; it is review posture, not runnable continuation. |
| API coordinate packet | verified | Pins both generation-11 archives plus exact result, receipt, invocation, checkpoint-basis, and snapshot identities. |
| Bounded R2 access | complete | Exactly two conditional HEADs and two GETs; no listing, writes, deletes, provider access, execution, or mutation. |
| Archive integrity and safety | verified | Both byte sizes, ETags, archive SHA-256 values, and safe member paths matched. |
| Exact terminal joins | verified | Each archive contains the expected result and receipt with the packet's result, receipt, invocation, run, checkpoint-basis, revision, and snapshot identities. |
| Exact surviving editorial findings | complete | Doughmeat retained one repeated-opening warning. Macaron retained real duplicate/opening-template rejection evidence; its second sparse polish was invalid and recorded as `POLISH_ERROR`. |
| API Slice 1 review | approved | Accepts closure without an API or SBE runtime change; no release follows. |

No R2 listing/write/delete, provider activity, run mutation, recovery, or release
has occurred.

## Slice 0 conclusion

No lifecycle, custody, authority, adoption, or publication defect is visible in
the preserved evidence. Doughmeat improved from three findings to one; Macaron
improved from eight findings to seven. Each run then exhausted its configured
two polish attempts and published an immutable `review_required` result with all
eight paid actions reported and no provider custody.

The terminal trace's `local_dependencies=1` is not undispatched local work. The
v0.7/v0.8 lifecycle source intentionally projects terminal final-QA review as a
blocking `native_state_repair_review` dependency with reason
`final_qa_review_required`; branch selection still remains `none` and capacity
remains `retain_for_review`. This describes human review posture rather than an
eligible ordinary-resume operation.

## Slice 1 conclusion

The exact artifacts close the remaining evidence gap:

- Doughmeat's first polish reduced its lint warning count to two and its second
  reduced it to one. The surviving finding is a genuine `repeated_opening`
  warning: `"you do not"` appears at the start of six
  `no_astro.body.direct_to_dog` fields. Validation passed, but the configured
  two-attempt polish allowance was exhausted with one editorial warning left.
- Macaron's first polish was accepted but retained five lint warnings and two
  deterministic acceptance rejection reasons: `cross_card_exact_duplicate`
  (three groups) and `multi_field_opening_template` (two dominant opening
  groups). Its second provider response was retrieved and adopted, but the
  sparse edit itself was invalid because it repeated
  `cards.17.card.no_astro.body.handler`; native state correctly records that
  attempt as `POLISH_ERROR`. The absence of attempt-002 lint/validation files is
  therefore expected, not missing publication evidence.
- Both final decks pass structural validation. Both terminal results are exact,
  sealed `review_required / final_qa_requires_review` publications with all
  eight provider operations and the expected result/receipt/checkpoint/snapshot
  identities.

This is ordinary two-polish exhaustion under current editorial policy, not a
lifecycle, custody, authority, reconciliation, adoption, publication, or API
settlement defect.

## Closeout

Sprint closed. Questions about polish prompting, the two-attempt budget, or
editorial thresholds may be considered later as product-quality work. They do
not authorize recovery of these retained runs and are not lifecycle defects.
