# Phase 1 — Kevin Summary Calibration Live Test

## Executive conclusion

Phase 1 produced two different findings that must not be collapsed into one:

1. **The four-thesis planning intervention worked.** The pass-6 author formed
   distinct identity, daily-life, present-needs, and developmental arguments
   before drafting. The resulting summaries are richer, longer, more specific,
   and more clearly separated than the historical automated summaries.
2. **The same-subject full-prose gold contaminated the comparison.** Although
   the handoff explicitly forbade copying Kevin's language and organizing
   devices, the new Kevin summaries reproduce multiple stretches and several
   conceptual frames from the manual Kevin reference. The candidate is useful
   evidence about the attainable quality bar, but it is not clean evidence of
   independent summary conception.

The thesis plan is ready to retain. The complete prose gold should remain
experimental until a cross-subject live test shows whether it transfers craft
without transferring Kevin's structures.

## Experimental design

The test isolated pass 6:

- SBE was rerun on the same Kevin projected-chart inputs under the Phase-1 code.
- Accepted card passes 1–5 from the original automated live run were reused
  byte-for-byte.
- Only `kevin_6` was sent to the OpenAI service.
- The historical automated deck, manually assembled Kevin deck, and a
  same-code assembly control were preserved separately.
- A production candidate restored the newly authored theme-group plan after a
  summary-only isolation candidate had been saved.

This design proves that reader-facing card prose was not changed by the test.
Two old invalid `Emotions` high-level filter tags were removed by current
deterministic post-assembly sanitation; those changes are unrelated to summary
authoring and are identified explicitly in the comparison artifact.

## Service result

- Model: `gpt-5.6-terra`
- Reasoning: `medium`
- Response ID: `resp_09beba8d6c027770006a6f5d4a58b0819a85e2dd67b61044d1`
- Attempts: one
- Pass-gate result: accept
- Wall time: 100 seconds
- Input tokens: 42,961
- Output tokens: 8,277
- Reasoning tokens: 44
- Total tokens: 51,238
- Estimated cost: $0.2315575

No cache hit was expected because this was one isolated request rather than a
six-pass run sharing prefixes.

## The private thesis plan

The model completed the planning fields with genuinely different centers:

- **Identity:** a "socially loyal original" whose unconventional first
  responses invite relationship rather than reject it.
- **Daily life:** a repeated rhythm of exploration, investigation,
  participation, and recognizable decompression.
- **Needs:** a designed environment combining refuge, stable limits, bounded
  agency, and meaningful scent/action/social outlets.
- **Growth:** rehearsed recovery that turns novelty-driven activation into
  choice, cue response, and cooperative reconnection.

It also correctly distinguished the final pair: needs are the conditions Kevin
requires now; growth is the flexibility and recovery repeated practice may
build over time.

That is the intended Phase-1 behavior. The four summaries no longer begin as
four attempts to paraphrase one whole-dog portrait.

## Length and richness

Across the 36 summary bodies:

| Deck | Total words | Mean per body | Range |
|---|---:|---:|---:|
| Historical automated | 2,675 | 74.31 | 53–117 |
| Manual reference | 3,367 | 93.53 | 53–156 |
| Phase-1 candidate | 3,244 | 90.11 | 61–138 |

The candidate recovers nearly all of the manual deck's room for synthesis
without merely inflating every field to the manual maximum. Compared with the
automated baseline, it adds 569 words distributed across the four coordinated
summaries and their nine renderings.

## Four-lens separation

The historical automated headlines were already competent:

- `The Golden Retriever Who Arrives as Himself`
- `Kevin's Day Is a Loop with Paws on It`
- `What Kevin Is Asking For Beneath the Big Feeling`
- `Kevin's Best Growth Is Organized Curiosity`

The candidate's no-astro handler headlines are similarly distinct but more
compactly aligned to their lenses:

- `The Dog With His Own Opening Line`
- `Kevin’s Day Runs in Chapters`
- `The Frame and the Freedom Inside It`
- `Keep the Spark, Teach the Return`

The bodies preserve those distinctions. Identity emphasizes originality
inside relationship. Daily life emphasizes transitions and closure. Needs
emphasizes environmental and handling infrastructure. Growth emphasizes the
skill of returning after surprise. Cross-lens vocabulary overlap remains in
the same range as the manual reference rather than collapsing toward four
versions of one thesis.

The needs/growth distinction is the strongest concrete success. `What He
Needs` recommends a protected rest base, stable rules, bounded choices, and
cooperative outlets. `How He Grows` measures recovery time, cue response at a
workable distance, and the ability to resume after novelty. One describes the
conditions of care; the other describes a developmental trajectory.

## Audience and astrology-density execution

The candidate generally preserves the intended matrix:

- handler prose explains what a person is likely to observe and do;
- direct-to-dog prose reassures or challenges Kevin without becoming a handler
  paragraph with pronouns swapped;
- hybrid prose centers a shared moment, ritual, or adjustment;
- no-astro prose stays behavioral;
- light astrology names a small number of placements and explains their
  relevance;
- full astrology traverses the chart's aspect and house structure.

Several hybrid passages are particularly operational. For growth, the human
creates distance, uses a rehearsed cue, and rewards Kevin's first sincere shift
back. The relationship, rather than dog or handler alone, is the grammatical
and behavioral subject.

## Craft quality

The candidate has no exact headline reuse from either comparison deck. Its
headlines and card-level jokes are readable, specific, and less generic than a
schema-completion output. Phrases such as `The human provides the commas and
period` give the daily-life lens a memorable image, while `freedom with clearly
posted office hours` keeps the needs advice concrete and playful.

The quality floor is high. None of the summaries feels empty, mechanically
short, or unaware of the whole chart. The candidate is materially better than
the historical automated set if evaluated only as reader-facing prose.

## Gold-reference leakage

The prose cannot be treated as an independent result, however. Deterministic
comparison found:

- mean character-level similarity to the manual reference: 0.3692;
- 182 shared distinct six-word sequences;
- 96 shared eight-word sequences;
- 56 shared ten-word sequences;
- 30 shared twelve-word sequences;
- a longest same-field match of 18 consecutive words.

Some full-astro overlap is expected because both decks describe the same chart
and must name the same placements and aspects. The problem is not confined to
technical strings. The no-astro growth address shares this 18-word run after
normalization:

> you do not need to stop noticing everything kevin your noticing is one of
> your gifts the next

Conceptual structures also transfer even when wording changes:

- manual `Kevin's Day Has Acts, Not Just Hours` becomes candidate `Kevin’s Day
  Runs in Chapters`;
- manual `Do Not Train Out the Spark; Train the Landing` becomes candidate
  `Keep the Spark, Teach the Return`;
- the manual anchor/gate/laboratory/stage needs framework becomes a candidate
  four-part system of reliable person, clear edges, legitimate investigation,
  and household role.

These are precisely the organizing devices the gold preface said not to copy.
The safeguard reduced literal headline reuse but did not prevent structural
imitation or local phrase transfer.

## Deterministic QA findings

The pass-6 workspace itself cleared the opaque pass gate on its first attempt.
Final whole-deck validation then found one unrelated error:

```text
Selected aspects and syntheses theme groups are not approximately balanced:
8, 12, 3, 10
```

The historical theme groups also fail the current balance rule (`8, 10, 6,
9`). This is not a summary-calibration failure. It reveals a contract gap:
pass 6 can pass its local gate while returning theme groups that fail the final
validator. That issue should be fixed separately rather than hidden inside the
summary experiment.

The final linter reports two inherited repeated-opening warnings from reused
passes 1–5 (`Kevin you do`, `Kevin you are`). Three inherited no-astro
validator advisories also remain. None was authored in this pass.

## Decision and next test

Retain the four-thesis plan and its explicit needs-versus-growth distinction.
It is inexpensive, auditable, and directly correlated with the desired
summary architecture.

Do not yet declare the complete Kevin prose gold a production default. The
next clean test should author a different dog's pass 6 using Kevin only as the
reference, then measure:

1. four-lens differentiation and prose richness;
2. transfer of Kevin-specific structures such as chapters, spark/return,
   anchor/gate, and office-hours framing;
3. long n-gram overlap with the reference;
4. whether a compact craft abstraction could achieve the same gains with less
   leakage and fewer tokens.

If cross-subject transfer remains clean, the Kevin gold can remain a pass-6
reference with a same-subject exclusion. If structures still migrate, replace
the complete prose gold with a curated multi-subject or principle-level
reference and keep the thesis plan unchanged.

## Preserved artifacts

The experiment directory contains the exact request, response, authored field
map, accepted workspace, reused-pass manifest, same-code control, isolation
deck, production deck, validator and linter reports, token/cost metadata,
comparison JSON, and deterministic quality metrics:

`work/phase-001-live-kevin/`

