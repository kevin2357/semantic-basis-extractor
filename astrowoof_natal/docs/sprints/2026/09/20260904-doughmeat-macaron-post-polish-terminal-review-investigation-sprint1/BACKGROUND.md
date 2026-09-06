# Doughmeat / Macaron post-polish terminal-review investigation

## Purpose

Two fresh, live QA qualification runs completed the full initial-authoring and
two-polish path under SBE `0.4.49`, then independently reached native
`FINAL_QA_REQUIRES_REVIEW`. API closed both runs as terminal `failed` and
released capacity. This sprint determines whether those terminal results are
the intended editorial outcome, a remaining final-validation defect, or a
native/API handoff problem. It begins with the retained, read-only evidence;
it does not resume, reconcile, repair, submit provider work, or mutate either
run.

## Frozen cohort and ownership

| Pup | API reading | API generation run | SBE native run |
| --- | --- | --- | --- |
| Doughmeat Dunsinane | `c4667dd7-7f07-4e5d-83f9-45a9f722ca57` | `cfa8f529-4a70-4e4b-a245-15bc03615671` | `c24a10322bfdd58d70a50e285dcf6d1b0e7013aa42f21e875d3f493235794294` |
| Lady Macaron MacLean | `f17abea9-19fb-4c1d-8d07-a256f62bc0bb` | `218faa53-d773-4e57-9b29-aa8738196078` | `13326ec073ec9b7bf4c214c1db0964f5e59a2b7ba57351fa77645a87b24d4aef` |

The runs were created through the documented inside-QA live launcher after the
SBE `0.4.49` fleet rollout. Owner-approved ceilings are USD 50 per run, 100
per cohort, 150 rolling 24-hour, 49 per active stage, and 0 candidate. Those
ceilings authorize the historical actions only; this investigation authorizes
no new spend.

## Observed authoritative and trace outcomes

The last authoritative API read establishes for each run:

- generation run and SBE job are terminal `failed`;
- all six `initial` and both `polish` paid actions are `reported`;
- no paid action remains `provider_created`, `authorized`, or reserved;
- its SBE capacity allocation is `released`.

The corresponding SBE traces independently establish:

- exact lifecycle status `FINAL_QA_REQUIRES_REVIEW`, terminal `true`;
- eight reported actions, classified as six `authoring_initial` plus two
  `polish`, with eight provider identities;
- zero provider custody, zero prepared actions, zero ambiguous actions, and no
  outstanding v2 intent/request/grant;
- final native publication outcome `review_required`.

This rules out an in-flight provider call, retained capacity, and an ordinary
subprocess crash as the explanation. The current trace summaries do not expose
the final editorial issue codes, so they do not yet establish whether the two
review decisions are substantively correct.

## Preserved SBE Render logs

The API agent exported the complete unfiltered QA SBE-worker log window from
`2026-09-05T02:27:26Z` through `2026-09-05T03:27:26Z` in bounded
15-minute JSON chunks. These files are local evidence, not source-controlled
artifacts:

- `C:\tmp\qa-sbe-worker-20260905T022726Z-032726Z-part-01.json`
- `C:\tmp\qa-sbe-worker-20260905T022726Z-032726Z-part-02.json` (zero-byte:
  no records in that interval)
- `C:\tmp\qa-sbe-worker-20260905T022726Z-032726Z-part-03.json`
- `C:\tmp\qa-sbe-worker-20260905T022726Z-032726Z-part-04.json`

The final chunks contain both native-run correlations. Treat API/PostgreSQL
records as custody authority and these SBE logs as complementary diagnostic
evidence.

## Scope and constraints

- Begin provider-free and read-only.
- Do not list R2 or access providers.
- If trace evidence cannot expose the final validation/report details, request
  exact, hash-verified checkpoint and named-artifact coordinates from API
  before any bounded HEAD/GET inspection.
- Do not conflate a `review_required` terminal result with an API/SBE seam
  failure without evidence.
