# Phase 3 — Ella Structured Chapters Live Test

## Purpose

Test the UI-derived Phase-3 contract against the real OpenAI service while
isolating the changed authoring surface. The trial regenerated Ella's current
SBE artifacts, reused accepted card passes 1–5, authored only pass 6, retained
the new theme plan during assembly, and ran pass-local and final QA.

## Result

The new chapter contract worked. Pass 6 required one automatic retry, then
produced two independent, balanced, structured registries. Final validation
passed after correcting an unrelated second-person grammar false positive.
The delivery completed with the pre-existing lint/astrology warnings retained
for review and no additional authoring request.

## API attempts

| Attempt | Result | QA signal | Input | Cached input | Output | Estimated cost |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Rejected | `theme_group_balance` | 44,451 | 0 | 8,231 | $0.2345925 |
| 2 | Accepted | none | 44,625 | 26,741 | 8,713 | $0.18209025 |

Total estimated cost was $0.41668275. The retry reused 26,741 cached input
tokens. The runner did not duplicate either in-flight request.

## Authored registries

### Interdogpendence

- 🏅 Fused Drives in Public Life (`Public Drive`) — 4 claims
- 🏠 Private–Public Polarity Work (`Polarity`) — 4 claims
- 🤝 Bond, Boundary, and Action Pressure (`Bond Pressure`) — 6 claims
- 👂 Attunement Turned into Practice (`Attunement`) — 5 claims

### Takeaways

- ⚡ The Shape of Ella's Big Reactions (`Big Reactions`) — 4 claims
- 🫶 What Makes Belonging Work (`Belonging`) — 3 claims
- 📣 Her Social Role in the Pack (`Pack Role`) — 4 claims
- 🔎 Information as a Path to Learning (`Learning Path`) — 3 claims

The two taxonomies perform visibly different editorial jobs. Interdogpendence
describes interacting forces, polarity, pressure, and coordination. Takeaways
describes conclusions about reaction, belonging, social role, and learning.
The long/short title pair also behaves as intended: editorially expressive
headings can coexist with compact navigation labels.

## QA behavior

Attempt 1 reached the service successfully and returned complete material, but
the opaque pass checker rejected its distribution as too lopsided. The runner
automatically retried. Attempt 2 satisfied registry shape, section membership,
coverage, three-to-five chapter count, two-claim minimum, 2:1 balance, and
cross-section title-separation requirements.

Final assembly then exposed an unrelated validator false positive. The phrase
"Virgo in you wants to inspect the route" was flagged as second-person subject
agreement because the detector allowed "of you" as an object of a preposition
but not "in you." The detector now recognizes common prepositional-object
contexts, with regression coverage. Revalidation passed without editing the
authored deck or issuing another API request.

Final validation contains no errors. Three conservative no-astrology warnings
and one deck-lint warning remain, so the artifact is packaged as
`DELIVERY_COMPLETE_WITH_WARNINGS` for later editorial review.

## Conclusion

This is a successful live validation of the new architecture. The LLM can
author two genuinely independent, UI-ready chapter systems from one pass-6
assignment; deterministic QA catches unacceptable distribution; opaque retry
feedback is sufficient to repair it; stable IDs and display metadata survive
assembly; and final validation consumes the resulting deck correctly.

The test also justified keeping redundant QA boundaries. Pass-local checking
caught the chapter defect before assembly, while final QA caught a separate
validator bug against real prose. Both findings improved the pipeline without
requiring manual rewriting or another full-deck run.
