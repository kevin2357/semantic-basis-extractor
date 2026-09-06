# Slice 3 — shared-axis interactive renderer

## Outcome

Implemented the reusable horizontal cohort view over the closed
`astrowoof.sbe_run_cohort_timeline.v1` projection.

The renderer establishes one canonical domain from the earliest and latest
validated run boundaries and places every interval against that same domain.
It contains no run-specific names, timing assumptions, scheduler policy, or
authority inference.

## Interaction

- Highlight one run while retaining cohort context.
- Hide or reveal explicitly classified wait intervals.
- Highlight intervals already joined to existing no-progress candidates.
- Select any interval by keyboard or pointer to inspect its exact duration,
  status, evidence ownership, source lines, and interval digest.

The initial rendering is useful without interaction. Color is paired with text
labels, a legend, open-edge styling, and contradiction styling.

## Time semantics

Canonical projection time remains UTC. The optional display timezone changes
only formatted labels in the rendered document. Unknown timezone identifiers
fail before rendering.

Every API and native boundary retains the clock ownership frozen in Slice 1;
the renderer does not choose or replace timestamps.

## Safety and privacy

The HTML is self-contained and offline. It contains the already validated,
privacy-bounded projection and no remote assets, fetches, provider operations,
workspace content, or API mutations. Embedded JSON escapes HTML script-closing
sequences.

## Verification

The focused renderer coverage proves deterministic bytes, shared-domain code,
controls and accessible detail, lack of network references, invalid contract
and timezone refusal, and script-terminator escaping. It runs alongside the
full timeline/reducer and existing run-report focused suites.
