# Phase 3: Ella Editorial-Planning Pass-1 Live Test

## Verdict

The remaining Phase-3 upstream planning intervention passed its live
checkpoint. A fresh Ella pass 1 used the new semantic-contribution inventory
and audience-posture plan substantively, passed opaque QA on attempt 1, and
assembled with five byte-preserved control passes. Compound claims retained
their full mechanisms, the three audience modes remained genuinely distinct,
and no evidence-boundary failure appeared.

The test also produced two important cautions. Reader-facing output was 22.6%
shorter than the matched compact-v2 control despite explicit guidance that
shortness is not automatically better. In addition, final whole-deck lint found
a headline collision and a repeated comic mechanism that pass-local QA could
not see across preserved passes. The planning intervention should remain, but
it does not replace whole-deck editorial inspection or settle product length
policy.

## Experimental design

- **Subject:** Ella.
- **Experimental pass:** `ella_1`, priorities 1–10.
- **Control:** Ella's immediately preceding compact-v2 pass 1.
- **Reused passes:** the control's accepted `ella_2` through `ella_6`, copied
  byte-for-byte.
- **Chart transport:** `compact-v2` in both treatment and control.
- **Assignment:** contiguous in both.
- **Model:** `gpt-5.6-terra`, medium reasoning.
- **Service:** interactive Responses API in background mode.
- **Polish:** disabled.
- **Attempts used:** one.

The independent variable was the Phase-3 authoring protocol:

1. a mandatory inventory of semantic contributions that must survive;
2. mandatory claim-specific Handler, Direct-to-Dog, and Hybrid postures;
3. useful-density editing rather than automatic shortening;
4. recurring characterization distinguished from recurring explanation.

## Service and cost

| Metric | Compact-v2 control | Planning treatment | Difference |
|---|---:|---:|---:|
| Actual input tokens | 42,414 | 44,171 | +1,757 (+4.1%) |
| Actual output tokens | 13,553 | 12,371 | -1,182 (-8.7%) |
| Estimated cost | $0.30933 | $0.29599 | -$0.01334 |
| Wall time | not used as a quality control | 175 seconds | — |
| Creative attempts | 1 | 1 | unchanged |

The request-layout estimate rose from 50,305 to 52,671 tokens. The two new
fields increased both assignment and response-schema material, while expanded
stable guidance increased the static prefix. Actual cost nevertheless fell
because output was shorter. That is a stochastic outcome, not a reason to add
instructions merely to suppress output.

## Planning-field quality

All ten semantic inventories were specific to their claims. Examples include:

- priority 3 preserved the polarity between an intense first response and
  loyal one-to-one attachment, explicitly stating that they alternate rather
  than cancel;
- priority 4 preserved private safety, visible pack function, oddball retreat,
  and attention-seeking display;
- priority 7 listed all three developable channels rather than summarizing the
  synthesis as generic trainability;
- priority 10 retained regulation-versus-novelty friction, trainable encounter
  coordination, and the natural affinity between novelty and bonding.

The audience plans also selected real editorial jobs. For priority 4, Handler
plans recovery alongside participation, Direct-to-Dog validates private reset,
and Hybrid casts the household as both backstage crew and audience. For
priority 9, Handler practices group manners, Direct-to-Dog frames social
learning as dignity rather than compliance, and Hybrid stages household
turn-taking.

These are not placeholder paraphrases. The private plan fields appear to have
been understood as decisions made before prose.

## Semantic-completeness results

The strongest evidence comes from compound cards.

### Sun–Jupiter conjunction

The treatment's full Handler rendering preserves identity, optimism,
exploration, Virgo inspection, visible tenth-Doghouse role, conjunction, and
the 0.126° orb. It then synthesizes them: purpose and possibility activate
together, so exploratory work should not force a choice between diligence and
adventure.

### ASC–DSC axis

The full Handler rendering preserves Scorpio investigation, Taurus nap-spot
loyalty, the exact opposition, first response, companion interface, and the
bond-freedom polarity. It does not flatten the card into either caution or
attachment.

### IC–MC axis

The treatment retains private security, visible pack function, unconventional
retreat, public display, exact opposition, and the behavioral rhythm between
them. The no-astrology renderings translate the same mechanism into “backstage
door,” “green room,” and withdrawal after participation.

### Developable-coordination synthesis

The full rendering explicitly carries all three sextiles: Uranus–Vertex,
Mercury–Saturn, and Neptune–Descendant. Each contribution receives a distinct
behavioral role, followed by one integrated practice recommendation.

### Novelty-response synthesis

The full rendering retains Moon–Uranus friction, Uranus–Vertex trainability,
and Uranus–Venus bonding ease. Its synthesis is a complete activation-to-outlet
to-practice to affectionate-recovery sequence.

The intervention therefore succeeds at its primary semantic objective in this
sample. It does not prove that every future compound card will succeed, but it
provides direct evidence that the inventory produces usable pre-draft thought.

## Audience distinction

The treatment did not collapse the three audiences into grammar variants.
Representative priority-4 openings are:

- Handler: `Every Little Star Needs a Backstage Door`;
- Direct-to-Dog: `You Can Shine and Then Disappear`;
- Hybrid: `Applause, Then the Laundry Room`.

They share one insight while teaching, validating, and staging a relationship
moment respectively.

Across the 30 card-density combinations, mean pairwise audience token-set
Jaccard similarity was 0.1344 in the treatment and 0.1354 in the control. This
small difference should not be overinterpreted, but it rules out an obvious
lexical collapse. Qualitative review likewise finds clear audience functions.
Because the control was already strong, this test establishes preservation and
good execution rather than a dramatic measured improvement.

## Length and useful density

| Layer | Compact-v2 control | Planning treatment | Change |
|---|---:|---:|---:|
| Complete ten-card payload | 5,701 words | 4,411 words | -22.6% |
| Nine audience/density bodies | 4,814 words | 3,481 words | -27.7% |
| No-astro Handler bodies | 708 | 476 | -32.8% |
| No-astro Direct-to-Dog bodies | 471 | 329 | -30.1% |
| No-astro Hybrid bodies | 473 | 354 | -25.2% |
| Full-astro Handler bodies | 767 | 591 | -22.9% |
| Full-astro Direct-to-Dog bodies | 491 | 353 | -28.1% |
| Full-astro Hybrid bodies | 470 | 337 | -28.3% |

The shorter treatment remains substantive. `The Nap Spot Has a Person
Attached`, `Applause, Then the Laundry Room`, and `The Zoom Ends at Home Base`
are compact, specific, and memorable. Full-astrology compound renderings still
carry the relevant geometry and projected mechanisms.

The control nevertheless retains more texture in several places. `The
Affection in the Empty Inch` gives more behavioral observation and handler
guidance than the treatment's nap-spot card. `Give Her a Return Address`
develops the autonomy-and-connection rhythm more fully than `First the
Questions, Then the Cuddle`. The control's direct-to-dog and Hybrid prose often
contains one additional conceptual turn.

This result does not show that the useful-density instruction caused
compression. The immediately preceding compact-v2 call was itself 20.8%
shorter than an older preserved baseline, so stochastic and model-level length
variation remains substantial. It does show that saying “shorter is not
automatically better” does not enforce a complete-read length target. If the
product later adopts distinct Quick and Complete WoofMaps, length must become
an explicit product-mode contract rather than an implied craft preference.

## Repetition and whole-deck effects

Pass-local opaque QA accepted with no issues. After assembly, whole-deck lint
found two cross-pass effects:

1. priority 8's new no-astro Hybrid headline, `From Clue to Cue`, exactly
   matched a reused synthesis headline;
2. priority 8 introduced `fine print` language into a deck where that comic
   mechanism already appeared in reused passes, raising the whole-deck count to
   four locations.

Neither defect was visible inside the ten-card treatment workspace. This is an
expected architectural boundary, not evidence that opaque QA malfunctioned.
It supports the Phase-0 conclusion that upstream authoring owns conception
while deck-level polish or review owns cross-pass collisions and reused comic
mechanisms.

Only two of the 210 reader-facing scalar fields matched the control exactly:
`Her Curiosity Wears a Badge` and one full-astrology Handler headline. The
former is independent stochastic convergence on a strong phrase, not source
leakage; the treatment did not receive the control deck.

## QA result

- Opaque pass QA: accept on attempt 1.
- Final validator: pass with five advisory astrology-density warnings.
- Whole-deck linter: one repeated-mechanism warning plus the cross-card exact
  headline collision in its authoring-acceptance view.
- Final run state: `DELIVERY_COMPLETE_WITH_WARNINGS`.
- No polish call was made.

## Decision

Retain the two private planning fields and the supporting guidance. The added
input cost is modest, the fields elicited specific thought, and the treatment
demonstrated excellent compound-mechanism preservation without harming voice
or audience distinction.

Do not interpret the result as proof that the intervention improves every
sentence or controls output length. Preserve the current product discussion
about Quick versus Complete reads, and avoid solving it through vague authoring
adjectives.

Proceed to Phase 3.5. The live result sharpens its responsibility: cheap sparse
polish should be able to keep strong prose, repair a cross-pass exact headline,
and replace one repeated comic mechanism without reconceiving the affected
cards or shortening unrelated text.

## Artifacts

- Experiment runner:
  `work/phase-003-live-ella-planning/run_planning_pass1.py`
- Reuse manifest:
  `work/phase-003-live-ella-planning/reuse-manifest.json`
- Run state and accounting:
  `work/phase-003-live-ella-planning/run/run.json`
- Exact request and response:
  `work/phase-003-live-ella-planning/run/passes/ella_1/attempt-001/`
- Accepted treatment pass:
  `work/phase-003-live-ella-planning/run/passes/ella_1/accepted/`
- Final assembled treatment deck:
  `work/phase-003-live-ella-planning/run/final/ella/natal.ella.cards.json`
- Validation and lint reports:
  `work/phase-003-live-ella-planning/run/final/ella/`
