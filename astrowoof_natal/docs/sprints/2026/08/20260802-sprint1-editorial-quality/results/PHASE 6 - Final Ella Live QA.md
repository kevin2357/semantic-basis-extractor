# Phase 6 — Final Ella Live QA

## Purpose

Run one fresh subject from projected chart inputs through current SBE,
six-pass authoring, pass acceptance, deterministic assembly, whole-deck QA,
bounded mechanical polish, and delivery. This verifies the selected production
configuration after the controlled Kevin comparison and tests the two final
upstream integrations in the real service:

1. constrained context-filter recovery before creative retry; and
2. explicit summary-lens boundaries plus recurring-motif allocation.

## Configuration

- Subject: Ella
- Service: OpenAI Batch for authoring, interactive Responses for conditional
  sparse polish
- Initial model: `gpt-5.6-luna`, medium reasoning
- Retry model: `gpt-5.6-terra`, medium reasoning
- Routing: `cost_optimized`
- Assignment: `stratified-v1`
- Chart basis: compact-v2
- Summary reference: cross-subject Kevin only
- Mechanical polish: enabled
- Qualitative critic/candidate: disabled, consistent with sampled/nonblocking
  policy

Initial Batch ID:
`batch_6a724b0bfcb88190a19d077d9dd1a2d1`.

## Execution result

The run reached `DELIVERY_COMPLETE`.

- All six Luna requests completed in one Batch round.
- All six passes passed opaque acceptance on attempt 1.
- No Terra creative-retry round was created.
- Four invalid high-level context labels were removed deterministically:
  two uses of `Emotions` and two uses of `Emotions & Inner World`.
- Every valid label and every authored prose field was preserved.
- Final assembly contained 50 cards, four summaries, 56 unselected claims, and
  all required theme-group assignments.
- Structural validation passed.
- Initial whole-deck lint found one three-location `fine print` mechanism.
- One sparse Luna/low polish call offered three targets, edited one, preserved
  two, and reduced lint warnings from one to zero.

The metadata-recovery result is the most direct integration proof. Under the K6
behavior, passes 3 and 5 would have been rejected despite usable prose and sent
to full Terra retries. Current code repaired four labels and accepted both
original Luna artifacts.

## Accounting

| Stage | Input | Output | Estimated cost |
|---|---:|---:|---:|
| Six-pass Batch authoring | 337,713 | 88,518 | $0.47662236 |
| Sparse mechanical polish | 3,013 | 151 | $0.00391900 |
| **Total** | **340,726** | **88,669** | **$0.48054136** |

Total reported tokens, including reasoning, were 429,395. OpenAI reported no
cached-input tokens. The low total cost therefore came from Luna, Batch pricing,
compact transport, first-attempt acceptance, and sparse polish—not from a
claimed cache hit.

For context, K6 cost $1.12486975 and required four full Terra retries solely
because of invalid context labels. The subjects and exact prompts differ, so
this is not a controlled price A/B, but it demonstrates that those retries are
not an inherent authoring expense.

## Summary-lens review

The accepted thesis plan assigned the recurring motifs before prose:

- investigation to identity as Ella's way of entering relationship;
- sequence and closure to daily life;
- den safety, bounded agency, and purposeful outlets to needs;
- novelty-to-return coordination to growth;
- bond/freedom tension to supporting evidence rather than a fifth thesis.

The resulting handler summaries preserve those boundaries:

1. **Who Ella Is — “The Original Who Always Comes Back With News.”**
   Investigation and visible participation describe identity and belonging.
2. **How Ella Lives — “Ella's Day Has Openings, Middle Acts, and Landings.”**
   The argument is temporal: experiences have phases and need recognizable
   endings.
3. **What Ella Needs — “Give Ella Clear Edges and Interesting Work.”**
   The argument is environmental: calm base, fair rules, bounded choice, and
   useful outlets.
4. **How Ella Grows — “Teach the Return, Not the Disappearance of Curiosity.”**
   The argument is developmental: practice the moment after surprise without
   erasing temperament.

This is meaningful separation. Investigation and return still recur, which
keeps one recognizable dog across the set, but they no longer serve as the
same conclusion in all four cards.

Compared with the prior compact-v2 Ella deck, the no-astro handler summary
bodies changed from 110/109/105/98 words to 108/98/91/92 words. Total length
fell from 422 to 389 words, about 8%, while the lens boundaries became at least
as clear. This is favorable for the current UI without treating compression as
the only quality measure.

## Remaining advisories

The validator retained eight nonblocking warnings for possible astrology words
in no-astro fields. These are heuristic advisories, not proven content errors,
and remain outside the mechanical-polish allowlist. They should be sampled in
future editorial review rather than silently converted into automatic edits.

The summaries validate the stronger planning mechanism on one fresh run. That
does not prove every future summary set will be lens-distinct, so summary-set
review remains an appropriate sampled critic question.

## Decision

The selected configuration passes the sprint's final live QA. Keep:

- `stratified-v1` as default assignment;
- cross-subject-only summary gold;
- deterministic metadata repair before creative retry;
- bounded mechanical polish for blocking whole-deck lint;
- qualitative critique as sampled/diagnostic;
- qualitative candidate prose as non-authoritative until reviewed.

Preserve this deck and its thesis plan as a versioned workflow and summary-
separation reference, not as universal prose to imitate.
