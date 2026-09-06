# Editorial quality standards calibration

Status: Initial four-run calibration cohort identified. Slice 0 has frozen the
campaign and is paused at the first evidence-access review; implementation
remains gated on the comparative findings.

## Why this sprint exists

AstroWoof's deterministic editorial standards were initially calibrated from a
small number of early runs. Recent QA runs now provide enough real deck lineage
to examine whether those standards still express the product judgment we
actually want.

This is an evidence and calibration sprint expected to lead to a code change,
likely on a short operational horizon. It deliberately does not preselect which
threshold, prompt, lint rule, polish-selection rule, or other implementation
detail should change. The first task is to collect representative cases and
distinguish:

- a useful lint observation;
- a whole-deck rejection condition;
- a polish-candidate adoption rule;
- and the final human or model editorial judgment.

Those are different decisions and must not be treated as interchangeable merely
because they currently share counts or report files.

## Initial concrete case: Frisbee Fandango

The completed OpenAI-response replay audit for Frisbee Fandango reproduced the
production assembly, validation, lint, and sparse-polish lineage exactly from six
initial Responses and two polish Responses.

After polish attempt 2:

- structural validation passed;
- the lint report contained one `repeated_opening` warning because six
  `no_astro.body.handler` fields began with `Frisbee Fandango may`;
- there were no exact duplicate groups, repeated twelve-word passages,
  suspicious artifacts, dominant-opening rejection groups, or rejection
  reasons;
- the lint report's deterministic `authoring_pass_acceptance` decision was
  `accept`;
- nevertheless, the polish candidate was not adopted because its total lint
  finding count remained `1` rather than falling below the prior candidate's
  count of `1`;
- the candidate had reduced the relevant opening count from seven to six, but
  that semantic improvement was invisible to the count-only adoption rule; and
- one of the two proposed edits itself retained the same three-word opening.

This produces an observable policy tension: the final deck-level standard says
the candidate is acceptable, while the polish-comparison rule refuses to adopt
that same candidate because the number of warnings did not decrease.

The case does not by itself prove which rule should change. It establishes that
the layers can disagree and that raw warning-count monotonicity is not equivalent
to either semantic improvement or whole-deck acceptability.

## Initial comparative cohort

The current QA authority inventory contains four runs with a latest sealed native
outcome of `review_required / final_qa_requires_review`. Together they provide a
useful first calibration cohort rather than four interchangeable failures:

- **Frisbee Fandango** is the exact-replay reference case and exposes a clear
  disagreement between whole-deck acceptance and polish-candidate adoption.
- **Doughmeat Dunsinane** ended with structural validation passing and one repeated
  opening warning after both polish candidates were accepted. It is the strongest
  candidate for a second severity/disposition disagreement.
- **Lady Macaron MacLean** retained exact duplicates and broad opening templates,
  then received a malformed second sparse-polish response. It is a useful likely
  positive control where review may have been warranted.
- **Marauding Madeleine** had lint pass but final structural validation fail after
  one polish. The database summary does not retain the exact validation reason, so
  an artifact replay is required before making an editorial judgment.

The detailed inventory and exact run identities are recorded in
`REVIEW-REQUIRED CASE INVENTORY.md`. The complete response-to-run table is
`RESPONSE EDITORIAL INVENTORY.md`.

## Existing evidence

The preceding audit is recorded at:

`astrowoof_natal/docs/sprints/2026/09/20260906-openai-response-editorial-audit-feasibility-sprint1/`

Private working evidence remains outside the repository at:

`C:\tmp\astrowoof-frisbee-openai-audit-20260906\`

That directory contains the exact provider Responses and production replay
outputs. It is evidence for this local investigation, not a public fixture or a
durable product archive.

## Questions for the eventual deep dive

Before proposing any policy or runtime change, investigate a broader sample of
accepted, improved, exhausted, and terminal-review decks. For each lineage, ask:

1. What did the linter observe, including finding identity, location, severity,
   population, and change across attempts?
2. What did whole-deck deterministic acceptance decide, and why?
3. What did polish-candidate adoption decide, and which comparison rule caused
   that decision?
4. Did the candidate make semantic progress even when the aggregate finding
   count stayed flat?
5. Did an adopted candidate remove one problem while introducing a different
   problem of equal count or greater severity?
6. Would a human editor accept the deck, request another polish, retain the prior
   candidate, or send it to review?
7. Would an independent editorial-review model agree, when shown a bounded and
   consistently formatted comparison packet?
8. Which checks are useful diagnostics but unsuitable as hard acceptance or
   adoption gates?
9. Are thresholds stable across dog names, card counts, densities, voices, and
   normal stylistic repetition?
10. Does the current prompt give the polish model enough information to target
    the actual acceptance rule reliably?

## Evidence approach

Prefer exact production replays when retained inputs are available. A useful
sample should include, at minimum:

- cleanly accepted decks;
- decks accepted with warnings;
- successful first- and second-polish improvements;
- exhausted polish attempts;
- flat warning-count cases whose finding contents changed;
- regressions hidden by an unchanged or lower aggregate count; and
- representative examples of every currently hard editorial rejection rule.

Preserve the exact text shown to a human or review model alongside the complete
machine finding—not merely the finding count. Record judgments independently
before reconciling disagreements, so the exercise does not become a post-hoc
defense of the current implementation.

## Guardrails

- Do not change editorial thresholds, prompts, lint rules, adoption rules, or
  terminal disposition until the initial evidence review produces an approved
  plan. A corrective implementation is expected after that gate.
- Do not assume that the whole-deck acceptance decision is automatically correct;
  it is itself part of the calibration target.
- Do not assume that every lint warning should block adoption or delivery.
- Do not collapse `warning`, `reject`, `not adopted`, and `terminal review` into
  one generic failure concept.
- Keep provider content and assembled decks private unless a separately reviewed
  sanitized fixture is deliberately promoted.
- Exact provider retrieval, retained-workspace access, and any live QA operation
  remain separately bounded and authorized activities.
- No provider creation, spend, run recovery, reconciliation, or mutation is in
  scope for this evidence-gathering sprint.

## Planning boundary

An investigation plan now exists because the initial cohort and evidence boundary
are concrete. It deliberately stops before implementation selection. The intended
outcome is a near-term, evidence-backed change; the pause exists to avoid
hard-coding the first plausible correction before we know how the rules behave
across more than one deck.
