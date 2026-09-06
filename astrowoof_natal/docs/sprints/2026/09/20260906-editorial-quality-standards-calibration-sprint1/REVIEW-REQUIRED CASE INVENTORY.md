# Review-required case inventory

## Cohort boundary

This inventory covers the four runs in the current QA database whose latest
API-persisted native receipt is exactly:

- `outcome = review_required`; and
- `cause_code = final_qa_requires_review`.

It does not infer editorial meaning from API run state. All four API generation
runs currently say `failed`, but that is a separate API disposition and is not
used here as proof that the authored deck was editorially unacceptable.

## Comparative summary

| Subject | API run | Native run | Provider responses | Current evidence-led classification |
| --- | --- | --- | ---: | --- |
| Marauding Madeleine `34c59972` | `98d2819f-4807-4f13-9b73-9bc8e8d2e1f5` | `064c17a411af2df9670372d1e6d1cf71880d2f1c0d5d92b0682e3da751696965` | 7 | Exact editorial defect under-specified; replay required. |
| Doughmeat Dunsinane `de04bf3e` | `cfa8f529-4a70-4e4b-a245-15bc03615671` | `c24a10322bfdd58d70a50e285dcf6d1b0e7013aa42f21e875d3f493235794294` | 8 | Possible severity/disposition mismatch. |
| Lady Macaron MacLean `047e7979` | `218faa53-d773-4e57-9b29-aa8738196078` | `13326ec073ec9b7bf4c214c1db0964f5e59a2b7ba57351fa77645a87b24d4aef` | 8 | Likely justified review; useful positive control. |
| Frisbee Fandango `4a05f776` | `e2d7f0ce-8c2a-4209-b79f-eb2187a58b15` | `cfdd79f1f50bbe940ba40d2c42743bf8b009cc02eef0f44895f0697b0d46be98` | 8 | Confirmed policy disagreement. |

All 31 exact provider Responses are currently available in the private local
archive under:

`C:\Users\kevin\Downloads\AstroWoof First Month AI Responses for Editorial Review\`

## Marauding Madeleine

Recorded provider lineage:

- six initial actions, all `reported`;
- one polish action, `reported`;
- no second polish Response in the authority inventory; and
- sealed native result `review_required / final_qa_requires_review`.

Existing trace evidence says the polish result was adopted, editorial lint
passed, and final structural validation failed. Native terminal publication was
valid; a later terminal-dominance defect was separately corrected and does not
explain the editorial decision itself.

What remains unknown is the exact final validation finding, affected field, and
whether the assembled candidate reasonably deserved review. Provider output alone
cannot answer that because validation ran against the assembled native deck.

## Doughmeat Dunsinane

Recorded provider lineage:

- six initial actions, all `reported`;
- two polish actions, both `reported`; and
- sealed native result `review_required / final_qa_requires_review`.

Prior exact checkpoint inspection established:

| State | Lint findings | Polish disposition |
| --- | ---: | --- |
| Initial assembled deck | 3 | selected for polish |
| Polish attempt 1 | 2 | `POLISH_ACCEPTED` |
| Polish attempt 2 | 1 | `POLISH_ACCEPTED` |

Final structural validation passed. The sole surviving lint finding was
`repeated_opening`: `you do not` began six `no_astro.body.direct_to_dog` fields.
This was historically described as genuine editorial exhaustion, but it now
needs recalibration against the product question: does one six-occurrence opening
warning justify terminal review when the final candidate is structurally valid
and both polish attempts were accepted?

## Lady Macaron MacLean

Recorded provider lineage:

- six initial actions, all `reported`;
- two polish actions, both `reported`; and
- sealed native result `review_required / final_qa_requires_review`.

Prior exact checkpoint inspection established that polish attempt 1 was accepted
but left five lint warnings. Whole-deck deterministic acceptance rejected it for:

- `cross_card_exact_duplicate`: three duplicate groups; and
- `multi_field_opening_template`: two dominant opening groups.

The strongest opening template, `lady macaron may`, appeared in 37
`no_astro.body.handler` fields. Polish attempt 2 reached its stage-specific
consumer but repeated the exact sparse-edit path
`cards.17.card.no_astro.body.handler`, producing `POLISH_ERROR` before a candidate
deck or new lint report existed.

This is the cohort's strongest likely-correct review case. It can test whether a
revised policy continues to reject substantial repetition and malformed polish
without relying on raw warning-count monotonicity.

## Frisbee Fandango

Recorded provider lineage:

- six initial actions, all `reported`;
- two polish actions, both `reported`; and
- sealed native result `review_required / final_qa_requires_review`.

The exact production replay established:

- baseline validation passed;
- baseline lint found four warnings and whole-deck acceptance rejected a
  multi-field opening template;
- polish attempt 1 made 20 edits, reduced the lint finding count to one, passed
  whole-deck acceptance, and was adopted;
- polish attempt 2 made two edits and reduced `frisbee fandango may` from seven
  occurrences to six;
- the attempt-2 candidate passed structural validation and whole-deck
  deterministic acceptance with no rejection reasons; but
- polish attempt 2 was not adopted because the aggregate lint finding count
  remained `1 -> 1`.

This is a confirmed inconsistency between three distinct layers: lint observation,
whole-deck acceptance, and candidate adoption. A warning can remain without being
a deck rejection, yet the count-only polish rule can override the deck-level
acceptance outcome.

## Initial investigation order

1. **Doughmeat:** test whether Frisbee's questionable severity boundary recurs.
2. **Macaron:** preserve a strong positive control for justified review.
3. **Madeleine:** recover the missing validation explanation.
4. **Frisbee:** retain as the exact-replay reference and compare every proposed
   policy against its known lineage.

This ordering is about information value, not priority of remediation.
