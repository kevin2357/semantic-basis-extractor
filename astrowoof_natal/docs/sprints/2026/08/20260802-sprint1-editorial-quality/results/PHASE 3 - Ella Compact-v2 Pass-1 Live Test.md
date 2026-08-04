# Phase 3: Ella Claim-Free Compact-v2 Pass-1 Live Test

## Verdict

The claim-free `compact-v2` transport passed its first live checkpoint. A fresh
Ella pass-1 response authored ten cards, passed opaque QA on attempt 1,
assembled with five preserved accepted passes, and completed final validation.
Removing all 50 selected and 56 additional claims from the shared full-chart
document did not produce a thin or incoherent dog model.

`compact-v2` is the strongest transport candidate so far. It materially lowers
input size while making the chart easier to read. This single pass-1 test does
not by itself establish a production default, particularly because the prior
live controls authored pass 6 rather than pass 1.

## Change under test

The author-facing `FULL CHART BASIS.md` now contains only:

- a five-line reading grammar;
- subject metadata;
- every reconstructed placement and angle;
- every reconstructed aspect, ordered by orb;
- deterministic mode/domain/interaction concentrations;
- connectivity and ASC–DSC/IC–MC attachment summaries;
- a semantic decoder for only the projected terms actually used.

It contains no claim IDs, claim text, selection priorities, dependencies,
source references, unselected claims, or reconstruction-limit commentary.
Those remain available locally in a structured audit excluded from the API
request. Context projections are fingerprinted before collapsing; divergent
contexts are rendered explicitly.

## Experimental design

- **Subject:** Ella.
- **Experimental pass:** `ella_1`, priorities 1–10.
- **Reused passes:** accepted `ella_2` through `ella_6` from the preserved
  compact-v1 experiment.
- **Model:** `gpt-5.6-terra`.
- **Reasoning:** medium.
- **Service:** interactive Responses API, background mode.
- **Attempts allowed:** three.
- **Attempts used:** one.
- **Assignment:** contiguous, matching the preserved Ella controls.
- **Polish:** disabled.

The historical live calls used for cost context authored pass 6. Therefore raw
service totals are reported, but matched no-service pass-1 layouts provide the
valid transport-only comparison.

## Transport measurements

### Chart-map layer

| Format | Characters | Words | Lines |
|---|---:|---:|---:|
| Legacy | 75,215 | 8,754 | 1,720 |
| Compact-v1 | 45,865 | 5,188 | 288 |
| Compact-v2 | 14,029 | 1,250 | 137 |

At the chart-map layer, compact-v2 is 69.4% smaller than compact-v1 and 81.3%
smaller than legacy by characters.

### Matched pass-1 request layouts

| Format | Static prefix | Subject prefix | Assignment | Response schema | Request estimate |
|---|---:|---:|---:|---:|---:|
| Legacy | 4,902 | 19,416 | 27,016 | 14,127 | 65,577 |
| Compact-v1 | 4,902 | 12,106 | 27,016 | 14,127 | 58,267 |
| Compact-v2 | 4,902 | 4,144 | 27,016 | 14,127 | 50,305 |

The subject tier is 65.8% smaller than compact-v1 and 78.7% smaller than
legacy. The complete pass-1 request estimate is 13.7% below compact-v1 and
23.3% below legacy because assignment and response-schema costs are unchanged.

Across six matched no-service requests:

| Format | Aggregate estimated input |
|---|---:|
| Legacy | 381,669 |
| Compact-v1 | 337,809 |
| Compact-v2 | 290,037 |

### Actual historical and treatment usage

| Format | Pass | Input | Output | Estimated cost | Result |
|---|---:|---:|---:|---:|---|
| Pre-compaction legacy | 6 | 43,398 | 7,639 | $0.22308 | accepted attempt 1 |
| Compact-v1 | 6 | 36,841 | 8,089 | $0.21344 | accepted attempt 1 |
| Compact-v2 | 1 | 42,414 | 13,553 | $0.30933 | accepted attempt 1 |

The compact-v2 request used fewer actual input tokens than the legacy pass-6
call despite carrying ten card assignments and their much larger response
schema. Its raw total cost is higher because pass 1 generated 13,553 output
tokens versus roughly eight thousand for four summaries. This is an assignment
cost, not evidence against transport savings.

## Whole-dog comprehension

The 734-word private portrait independently recovered:

- Virgo inspection, practical intelligence, and useful visible role;
- Scorpio doorway intensity and persistent signal-reading;
- Leo visibility, affection, play, and pack participation;
- Capricorn emotional steadiness and practical regulation;
- Pisces home atmosphere and the importance of decompression;
- the exact ASC–DSC negotiation between autonomy and dependable companionship;
- the exact IC–MC negotiation between private restoration and public role;
- Moon–Uranus activation around surprise and recovery;
- Mercury–Saturn structure supporting detailed, durable learning;
- outward mission followed by protected return as a whole-dog rhythm.

This is direct evidence that the author did not need SBE's repeated claim
portfolio to reconstruct the dog's organizing picture. The deterministic chart
and decoder were sufficient.

The preserved baseline portrait is 891 words. It is more behaviorally expanded
and contains excellent formulations such as “Her bond is a return address, not
a permanent tether.” The compact-v2 portrait is more astrologically explicit
and somewhat tighter. Both describe the same dog.

## Ten-card quality

All ten editorial plans define distinct centers of gravity. Representative
headlines include:

- “The Affection in the Empty Inch” for quiet companion proximity;
- “Her Curiosity Wears a Badge” for Sun–Jupiter purposeful exploration;
- “She Needs a Backstage Door” for the IC–MC privacy/visibility axis;
- “Let Her Choose the Weird Little Fortress” for unconventional den safety;
- “Teach One Bridge for Many Moments” for recurring developable coordination;
- “Make New Things Easier to Come Home From” for novelty, comfort, and bond.

The cards begin from different lived doorways rather than translating chart
labels. Audience functions remain distinct: handler prose teaches and advises,
direct-to-dog prose reassures with dignity, and hybrid prose stages reciprocal
moments. Astrology density remains progressive: no-astrology establishes lived
meaning, light astrology names the principal basis, and full astrology exposes
the relevant geometry and projected interaction.

Ordinary-card evidence boundaries held. The full chart informed
characterization, while full-astrology bodies stayed tied to each card's own
claim evidence. Synthesized cards 7 and 10 were authored successfully because
their own assignments supplied their synthesis and dependencies; they did not
need duplication in the whole-chart map.

## Length comparison

| Layer | Preserved baseline | Compact-v2 |
|---|---:|---:|
| Private whole-dog profile | 891 | 734 |
| Ten-card reader-facing prose | 6,588 | 5,219 |
| No-astro handler bodies | 802 | 701 |
| No-astro dog bodies | 630 | 471 |
| No-astro hybrid bodies | 627 | 468 |
| Light handler bodies | 637 | 540 |
| Light dog bodies | 585 | 469 |
| Light hybrid bodies | 558 | 404 |
| Full handler bodies | 781 | 739 |
| Full dog bodies | 667 | 482 |
| Full hybrid bodies | 632 | 450 |

Reader-facing prose is 20.8% shorter overall. Full handler explanations remain
close to baseline length; direct-to-dog and hybrid renderings account for most
of the compression. The resulting prose remains substantial and often benefits
from tighter movement, but this should be evaluated in the UI rather than
treated as an automatic quality improvement.

## QA

- Opaque pass QA accepted attempt 1.
- No exact duplicate groups, repeated long n-grams, suspicious artifacts, or
  dominant opening failures were detected.
- Final validation completed with the inherited advisory-warning profile.
- The one whole-deck “fine-print humor” warning concerns priorities 29 and 41,
  both reused from other passes; it was not introduced by compact-v2 pass 1.

## Decision

Retain all three modes for the moment, but use compact-v2 as the leading
candidate for the next matched subject test. The test supports these claims:

- claim portfolios are unnecessary in the shared whole-chart context;
- context-safe compact grammar is intelligible to a naive author;
- deterministic concentrations help without dictating synthesis;
- the used-term decoder preserves semantic support at low cost;
- whole-dog understanding and evidence-bounded card quality survive aggressive
  transport compaction;
- the remaining prompt cost is dominated by pass assignment and response
  schema, not full-chart context.

Do not attribute output-length variation solely to transport from one stochastic
response. Do not compare the three raw request costs as though pass 1 and pass
6 had equal output obligations.

## Artifacts

- Run state and accounting: `work/phase-003-live-ella-compact-v2/run/run.json`
- Exact API request and response:
  `work/phase-003-live-ella-compact-v2/run/passes/ella_1/attempt-001/`
- Accepted pass:
  `work/phase-003-live-ella-compact-v2/run/passes/ella_1/accepted/`
- Final assembled deck:
  `work/phase-003-live-ella-compact-v2/run/final/ella/natal.ella.cards.json`
- Local traceability audit:
  `work/phase-003-live-ella-compact-v2/run/sbe/semantic-basis-output/ella/ella.compact-v2-full-chart-basis.audit.json`
- Matched prompt layouts:
  `work/phase-003-live-ella-compact-v2/layout-*-report.json`
- Experiment runner:
  `work/phase-003-live-ella-compact-v2/run_compact_v2_pass1.py`
