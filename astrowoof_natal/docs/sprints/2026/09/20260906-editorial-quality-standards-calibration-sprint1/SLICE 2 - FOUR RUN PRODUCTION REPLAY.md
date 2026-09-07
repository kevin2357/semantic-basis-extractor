# Slice 2 — four-run production replay

## Result

Slice 2 is complete and provider-free. All four retained workspaces reproduce
their initial assembly and every materialized polish candidate through the
released production operations. The sprint is paused at Voof-paws 2 before any
human/model judgment or policy recommendation.

The repeatable replay tool is `tools/replay_polish_lineage.py`. It:

1. assembles all six accepted pass workspaces with the retained selected packet
   through production `assembly.assemble(..., allow_partial=False)`;
2. applies the production deterministic context-filter sanitizer;
3. reconstructs the exact predecessor for each materialized polish candidate
   from the editable-target map embedded in its retained request;
4. reapplies the retained sparse edits with production `apply_sparse_polish()`;
5. reruns the production structural validator with the historical edit override
   posture; and
6. reruns production editorial lint and extracts finding-local private text.

No provider, R2, API, Better Stack, QA, recovery, reconciliation, or retained-run
operation occurred.

## Reproducibility

Private full receipt:

`.tmp-editorial-calibration-r2/private-lineage/four-run-polish-replay.json`

- canonical receipt SHA-256:
  `3e965d8c682438a3596561827d930454556a5e850b046cae2008929a2c630b56`;
- first file SHA-256:
  `1f6553f20132b4fd1e79e685c04d96812d291f7abc6cf980bf878769e3d19247`;
- second file SHA-256:
  `1f6553f20132b4fd1e79e685c04d96812d291f7abc6cf980bf878769e3d19247`;
- byte equality across two independent executions: `true`.

The private receipt contains authored field text and remains outside the public
repository. This document records only bounded findings and hashes.

## Exact replay matrix

| Case | Six-pass assembly equals pre-polish deck | Materialized candidates | Sparse reapplication | Validation replay | Lint replay |
|---|---:|---:|---:|---:|---:|
| Doughmeat | yes | 2 | 2/2 exact | 2/2 exact | 2/2 exact |
| Macaron | yes | 1 | 1/1 exact | 1/1 exact | 1/1 exact |
| Madeleine | yes | 1 | 1/1 exact | 1/1 exact | 1/1 exact |
| Frisbee | yes | 2 | 2/2 exact | 2/2 exact | 2/2 exact |

Macaron attempt 2 has no materialized candidate by design: production rejected
the sparse response for repeating one field path.

## 2A — Doughmeat

Doughmeat's warning components decreased monotonically:

- baseline: 3 total components;
- polish 1: 2, accepted;
- polish 2: 1, accepted.

The final deck is byte- and semantic-equal to polish candidate 2. Structural
validation passes and whole-deck authoring acceptance says `accept`. The one
remaining lint finding is a six-member `repeated_opening` group in
`no_astro.body.direct_to_dog` using `you do not`.

All six exact fields and their claim identities are preserved in the private
receipt. They are intentionally not copied into this public sprint document.

This repeats the important Frisbee policy tension in a slightly different
shape: the selected final deck passes the whole-deck acceptance rule, but the
run still reaches terminal review because one residual warning remains after
the permitted polish attempts. Unlike Frisbee, Doughmeat's second candidate was
adopted because the raw count decreased from two to one.

## 2B — Macaron

Macaron begins with eight warning components. Polish 1 makes one sparse edit and
reduces the total to seven, so production accepts it. The selected final deck
still has five lint findings and whole-deck acceptance says `reject`:

- one eight-member `you do not` repeated-opening group;
- one 37-member `Lady Macaron may` repeated-opening group; and
- three claim-type-template findings for that same handler opening across
  system-interaction, synthesized-theme, and placement cards.

Polish 2 returns a duplicate edit path and is rejected before candidate
materialization with `Sparse polish repeats field`. This is a useful positive
control: a revised policy must continue to distinguish substantive broad
templating and malformed sparse output from a harmless residual advisory.

## 2C — Madeleine

Madeleine's sole materialized candidate removes both lint findings and passes
whole-deck authoring acceptance, but structural validation rejects one field for
invalid second-person grammar. Exact replay proves the retained error is the
known regex false positive: `you is` spans the grammatical phrase “restores you
is not evidence.”

Production records the candidate as `POLISH_IMPROVED_PARTIAL`, does not adopt it,
and retains the structurally valid predecessor. This is neither provider failure
nor evidence that lint improvement alone should dominate structural integrity;
it is a concrete validator-calibration case.

## 2D — Frisbee control

The prior Frisbee result reproduces under the same four-run tool:

- six-pass assembly exact;
- polish 1 exact and accepted, reducing five warning components to one;
- polish 2 exact and rejected because the total remains one;
- both candidates structurally valid and accepted by whole-deck QA; and
- the selected final deck remains polish 1, with one seven-member repeated
  handler opening.

This verifies that the common replay machinery preserves the established
control rather than relying on its earlier case-specific narrative.

## Causal comparison

The cohort now establishes three distinct calibration problems:

1. **Residual-warning terminalization:** Doughmeat and Frisbee both end with
   structurally valid decks that whole-deck QA accepts, yet one remaining style
   warning drives terminal review after the attempt ceiling.
2. **Count-only candidate selection:** Frisbee's second candidate reduces the
   affected repeated-opening population but not the number of finding objects,
   so the semantic improvement is invisible to the current comparator.
3. **True hard and malformed controls:** Macaron preserves broad templating and
   returns a malformed duplicate-path edit; Madeleine exposes a structural
   regex false positive rather than a reason to let lint override validation.

These are evidence for calibration, not an implemented policy decision.

## Voof-paws 2

Review the exact replay matrix and the private receipt boundary before Slice 3.
No blinded reviewer packet, independent model judgment, threshold change,
prompt change, runtime change, schema freeze, or Better Stack capture is started
under this slice.
