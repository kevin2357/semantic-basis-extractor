# Phase 1 — Ella Cross-Subject Gold Test

## Executive conclusion

The Ella test strongly suggests that the severe Kevin leakage was caused by
the reference and target being the same subject, not by the gold reference
generally turning every dog into Kevin.

Against the complete Kevin summary gold, Ella's new summaries contain:

- no exact reused headlines;
- no shared eight-, ten-, or twelve-word sequences;
- one shared six-word sequence: `cue and a familiar resting place`;
- a maximum cross-field body match of six words.

Several broad devices—chapters, sparks, landings, and returns—appear in the
candidate, but they were already prominent in Ella's old summaries and chart
prose. Their presence cannot reasonably be attributed to the Kevin gold.

The gold therefore appears safe from meaningful literal or Kevin-specific
content transfer across subjects. Its incremental quality value remains less
certain: the new summaries are good and cleanly differentiated, but they are
35% shorter than Ella's already-strong automated baseline and lose some of its
literary richness.

## Experimental design

- Current Phase-1 SBE was run on Ella's original projected inputs.
- Accepted Ella card passes 1–5 from the optimized Batch run were reused.
- Only `ella_6` was sent to the OpenAI service.
- The request used the same Terra/medium interactive configuration as the
  isolated Kevin test.
- The newly authored theme plan was preserved separately.
- Ella's historical accepted theme plan was restored before comparison so
  reader-facing differences were confined to summaries.
- A same-code deck was assembled from all six historical accepted workspaces;
  the Phase-1 candidate differs from it at exactly 108 summary values and no
  non-summary value. All 50 reader-facing card payloads are identical.
- The candidate was compared against Ella's optimized automated deck and the
  manual Kevin gold.

## Service result

- Model: `gpt-5.6-terra`
- Reasoning: `medium`
- Response ID: `resp_0c7df228968c8380006a6f61b996c0819aa9015072264bfba8`
- Attempts: one
- Pass-gate result: accept
- Elapsed time including detached polling: 188.625 seconds
- Input tokens: 43,398
- Output tokens: 7,639
- Reasoning tokens: 53
- Total tokens: 51,037
- Estimated cost: $0.22308

The local command window ended after submission, and the same durable response
was resumed later. No duplicate request was issued. This also exercised the
runner's detachable-response path.

## Four-thesis result

Ella's private thesis plan is clear and internally differentiated:

- **Identity:** a loyal, exacting participant whose investigation, affection,
  and pack role belong to one personality.
- **Daily life:** patrol and play opening outward, followed by a recognizable
  route back to den-like calm.
- **Needs:** protected refuge, consistent companionship, clear permissions,
  and purposeful outlets for attention and scent.
- **Growth:** practice connecting surprise or scrutiny to a cue, choice, and
  renewed cooperation.

It explicitly distinguishes the supportive environment Ella needs now from
the recovery, communication, and flexibility that may develop through
practice. This independently confirms the usefulness of the thesis-plan
intervention.

## Leakage analysis

The full candidate and full Kevin gold summary matrices were compared after
case and punctuation normalization.

| N-gram size | Shared distinct sequences |
|---:|---:|
| 6 words | 1 |
| 8 words | 0 |
| 10 words | 0 |
| 12 words | 0 |

The only six-word overlap is ordinary care language: `cue and a familiar
resting place`. The remaining longest matches are generic fragments of four or
five words such as `you do not have to`.

There is no evidence of Kevin's facts, astrology, exact jokes, headlines,
anchor/gate/laboratory/stage framework, or office-hours metaphor entering
Ella's summaries.

### Structural-device caution

Ella's candidate uses chapter, spark, landing, and return language. Those
devices also occur in the Kevin gold, but they were already present throughout
Ella's pre-Phase-1 artifact:

- `Let the day have chapters.`
- `A Capricorn Landing Pad for Your Aries Spark`
- repeated chart-level launch/landing and return motifs.

Ella's own evidence therefore supplies an independent semantic reason for
those words. Unlike the Kevin-on-Kevin test, the cross-subject n-gram analysis
does not show their surrounding prose being transferred.

## Quality comparison

Across all 36 summary bodies:

| Deck | Total words | Mean per body |
|---|---:|---:|
| Existing optimized Ella | 4,339 | 120.53 |
| Phase-1 Ella candidate | 2,830 | 78.61 |
| Manual Kevin gold | 3,367 | 93.53 |

The new candidate is not comically short. Its bodies generally contain two
substantive paragraphs, a behavioral picture, and actionable guidance. But it
is 1,509 words shorter than the existing Ella set, a 34.8% reduction.

### What improved or remained strong

- The four lenses are unmistakable.
- Needs and growth are more explicitly separated at the planning level.
- Handler prose is concise and operational.
- Direct-to-dog prose is affectionate without becoming handler prose with
  swapped pronouns.
- Hybrid prose usually centers a shared cue, transition, or repair.
- Headlines are compact and specific, including `Ella's Day Needs a Last
  Page`, `Give Ella a Base and a Brief`, and `Teach the Return After the
  Notice`.
- The candidate avoids the reference's exact language and Kevin-specific
  astrology.

### What the existing Ella summaries still do better

The old set has more room for characterization and more memorable literary
peaks. For identity, it develops Ella from household inspection through
affection to a compact three-part character synthesis. The new identity card
gets to a similar conclusion more quickly but offers fewer turns of thought.

For daily life, the old body builds a full outward-and-homeward rhythm, names
what happens when stimulation is too low or high, and ends with `a well-lived
day is not quiet from start to finish; it knows how to come home.` The new
version is cleaner and actionable, but less emotionally resonant.

For needs, the old `home base—and a job worth leaving it for` argument and
`life with good handrails` image are stronger than the candidate's more
functional `base and a brief` treatment. For growth, both versions are good;
the candidate is particularly clear about measuring recovery rather than
demanding the disappearance of interest.

The cross-subject gold did not cause a quality collapse. It also did not
clearly outperform this unusually strong baseline.

## QA findings

The pass-local opaque gate accepted the new Ella pass on its first attempt.
Final whole-deck validation failed because the authored theme plan used five
groups. Restoring the historical Ella theme plan did not resolve current
validation because that historical plan also uses five groups and predates the
current three-or-four-group rule.

The current validator therefore rejects both relevant theme plans for reasons
unrelated to summary prose. The linter's single `fine print` warning is
inherited from reused passes 1–5. Two no-astro advisories are also inherited.

Together with the Kevin test, this confirms a real contract gap: the pass-local
gate can accept a theme plan that the final validator must reject.

## Decision

The evidence now supports these conclusions:

1. **Retain the four-thesis plan.** It worked independently on Kevin and Ella.
2. **The severe Kevin leakage was a same-subject artifact.** Cross-subject
   literal leakage is negligible.
3. **Do not use a subject's own prose as its gold reference.** Add a
   same-subject exclusion if complete prose gold remains available.
4. **The Kevin gold is defensible as a cross-subject craft reference, but its
   marginal benefit is not established.** We have changed both the thesis plan
   and gold together, and Ella's existing baseline was already excellent.
5. **Do not treat summary gold as a license to shorten.** Rich existing
   summaries may be better than a cleaner replacement.
6. **A later no-gold A/B can measure incremental value.** Run the same current
   pass-6 protocol with the thesis plan but omit gold, then compare quality,
   length, and cost. This is useful but not required before Phase 2.
7. **Fix pass-local theme-plan acceptance separately.** That defect should not
   block the summary-quality conclusion.

## Preserved artifacts

Exact request/response files, the accepted pass, detached polling state,
assembled candidate, historical-theme control, QA reports, and deterministic
leakage metrics are under:

`work/phase-001-live-ella/`
