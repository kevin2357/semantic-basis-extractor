# Phase 3.5 — Ella Sparse Polish Live Test

## Purpose

Test the hardened production sparse-polish route against the preserved Ella
Phase-3 planning deck. This deck supplied a deliberately useful checkpoint:
structural validation passed, while whole-deck QA still found one repeated
metaphor family (`fine print`) and one exact cross-card headline collision
(`From Clue to Cue`).

The experiment allowed one OpenAI request and no broad-rewrite fallback. It
therefore measured whether narrow repair could resolve the known findings
without turning polish into a second authoring pass.

## Controls

- Model: `gpt-5.6-luna`
- Reasoning effort: `low`
- Maximum attempts: 1
- Baseline composite findings: 2
- Editable targets: 6 of 1,458 reader-facing fields
- Read-only neighboring fields: 36
- Theme groups: locked
- Summary fields: locked
- Structural, evidentiary, identity, selection, and classification data: locked

The six targets comprised four fields participating in the `fine print`
mechanism and both fields participating in the exact headline collision.

## Result

The sole attempt was accepted.

| Measure | Before | After |
|---|---:|---:|
| Structural validation | pass | pass |
| Ordinary lint warnings | 1 | 0 |
| Nested authoring rejections | 1 | 0 |
| Composite findings | 2 | 0 |
| Editable fields | 6 | 6 |
| Fields changed | — | 5 |
| Fields deliberately preserved | — | 1 |

The response correctly used the new keep-or-replace contract. It changed one
side of the duplicate `From Clue to Cue` pair and omitted the other, preserving
the phrase where it could remain distinctive. This is materially better than
rewriting both sides simply because both were nominated as possible repair
locations.

For the repeated metaphor, it made four local substitutions:

- `Your Pluto Can Read the Fine Print Before Mars Plays Again` became
  `Your Pluto Reads the Hidden Detail Before Mars Plays Again`.
- `Pluto Makes Mars Stop for the Fine Print` became
  `Pluto Makes Mars Pause for the Hidden Detail`.
- `Your Mercury notices the fine print: scent, tone, footsteps, sequence.`
  became `Your Mercury notices the small signals: scent, tone, footsteps,
  sequence.`
- `you pick up the fine print of a room` became `you pick up the hidden details
  of a room`.

For the exact duplicate, the hybrid headline on the scent-and-training card
became `From Scent to Shared Cue`; the neighboring card retained `From Clue to
Cue`.

## Editorial assessment

The accepted edits are genuinely improvements, not merely validator-shaped
evasions.

The strongest result is the duplicate repair. `From Scent to Shared Cue` is
more specific to its own claim than the generic original, while the omitted
target demonstrates that preservation worked as an active editorial choice.

The repeated-metaphor repairs also preserve each field's underlying work.
`small signals` is especially apt beside scent, tone, footsteps, and sequence.
`hidden details` retains the perception-of-subtle-information idea. The Pluto
headlines preserve the pause-before-action mechanism while shedding the shared
signature. Two variants of `hidden detail` remain within one card's audience
matrix, which is coherent rather than cross-card templating.

No unrelated prose, summary content, theme assignment, or locked semantic data
changed. The resulting deck remains recognizably the authored Ella deck rather
than a flattened polish rewrite.

## Cost and transport

- Actual input: 5,498 tokens
- Actual output: 605 tokens
- Reasoning: 267 of the output tokens
- Total: 6,103 tokens
- Estimated cost: **$0.009128**
- Wall-clock time: approximately 21 seconds
- API create attempts: 1
- Poll requests: 7

The sparse transport estimated 4,021 prompt tokens versus 70,234 for the full
editable-field map, with a 288-token replacement ceiling. Actual usage includes
the complete system prompt, reports, schema, semantic repair basis, targets,
and nearby read-only context. Even without a cache hit, the call cost remained
below one cent.

## Conclusion

This test validates the intended Phase-3.5 boundary. Sparse polish can repair
deterministically identifiable whole-deck collisions cheaply and selectively,
including nested authoring-acceptance findings that were previously invisible
to polish scoring. It can also decline an unnecessary target within a finding
group rather than treating every nominated field as mandatory.

This does not alter the Phase-0 conclusion that polish is not the sole remedy
for qualitative conception problems. It does show that the production polish
route is now well suited to its narrower job: precise cleanup of an otherwise
sound authored deck.

