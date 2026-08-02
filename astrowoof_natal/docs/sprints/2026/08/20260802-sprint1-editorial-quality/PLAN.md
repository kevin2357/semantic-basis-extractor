# Sprint Plan: Editorial Quality Beyond Mechanical Acceptance

- **Date:** 2026-08-02
- **Sprint:** 1
- **Status:** planned; discovery phase begins before implementation
- **Primary subject:** Kevin
- **Supporting subjects:** Ella and future comparison subjects as needed
- **Related backlog:** `docs/post_extraction_authoring/Editorial Quality Research and Improvement Backlog.md`

## Objective

Improve the semantic-closure authoring pipeline in quality dimensions that are
not adequately represented by deterministic validation and linting, while
preserving its reliability, evidence boundaries, resumability, and low cost.

The sprint begins with a bounded manual polish experiment. Its findings may
change the implementation plan before code is modified. Subsequent work will
add pass-6 summary calibration, deterministic diversified claim assignment,
and an optional qualitative review/polish path. Controlled Kevin comparisons
will isolate the contribution of each change.

## Why discovery comes first

The matched Kevin review showed that the automated deck is the stronger
production baseline but the older manual deck retains several higher literary
peaks. A manual sparse polish can reveal whether those qualities are
recoverable after assembly and whether the required edits can be described
precisely enough for automation.

Implementing a qualitative critic before performing that experiment would
force its schema to encode guesses. The manual audit should produce concrete
diagnosis and edit pairs first.

## Protected baseline artifacts

Treat these as immutable inputs:

- Manual assembled Kevin deck:
  `astrowoof_natal/qa/reference_decks/kevin/20260730-six-pass-final/natal.kevin.cards.json`
- Automated Kevin live-run base deck:
  `astrowoof_natal/qa/reference_decks/kevin/20260801-automated-live-base/natal.kevin.cards.json`
- Strongest preserved automated polish candidate:
  `astrowoof_natal/qa/reference_decks/kevin/20260801-automated-live-polish-1/natal.kevin.cards.json`
- Kevin selected authoring packet:
  `astrowoof_natal/qa/reference_decks/kevin/selected-authoring-packet.json`

Copy an input before editing it. Never overwrite a baseline artifact.

## Quality dimensions in scope

1. Peak semantic compression and memorable phrasing.
2. Four-way summary lens separation.
3. Conceptual duplication without textual duplication.
4. Comic-mechanism diversity.
5. Rhetorical-entry and audience-posture diversity.
6. Complete behavioral preservation of compound semantic claims.
7. Clarity without unnecessary explanation.
8. Voice distinction beyond pronoun and grammar correctness.

## Phase 0 — Manual sparse polish experiment

### Scope

Create a new Kevin research candidate while keeping all unrelated fields
value-for-value identical. Target only:

- all four summary cards;
- the six repeated `Kevin, you do...` direct-to-dog openings;
- a bounded sample of jokes sharing the administrative/corporate mechanism;
- a bounded sample of weaker or exchangeable headlines;
- sampled compound claims whose prose drops a major semantic contribution;
- sampled no-astro handler bodies that continue explaining after the useful insight is complete.

### Required audit record

For every changed field, record:

- exact JSON path;
- original and revised text;
- quality dimension, diagnosis, and rewrite objective;
- evidence consulted;
- whether the change required whole-chart context;
- whether the objective appears automatable before authoring, during pass authoring, or during final polish.

### Validation

- Parse the revised JSON.
- Run the standard validator against the Kevin authoring packet.
- Run the whole-deck editorial linter.
- Confirm no locked semantics or evidence changed.
- Produce a value-level diff proving all non-allowlisted fields are unchanged.

### Evaluation

Compare matched passages from:

1. manual assembled Kevin;
2. automated Kevin candidate;
3. manually polished automated Kevin.

Where practical, review without revealing which version produced a passage.
Assess memorability, behavioral clarity, grounding, usefulness, voice,
summary-lens separation, and naturalness.

### Discovery checkpoint

Stop after Phase 0. Summarize findings in `LOG.md` and under `results/`. Revise
the remaining sprint plan if the audit shows that a problem belongs at a
different pipeline stage than currently assumed. No production implementation
begins before this checkpoint is recorded.

## Phase 1 — Pass-6 summary calibration

### Gold reference

Create a pass-6-only gold reference from the four complete manual Kevin summary
cards. Include all audience and astrology-density modes, card-level quotes,
jokes, dos, and don'ts required to demonstrate the finished summary system.

The reference must explain that:

- Kevin is an example subject, not evidence about the current dog;
- wording, metaphors, jokes, and structures must not be copied;
- `anchor/gate/laboratory/stage`, `train the landing`, and other Kevin-specific devices are examples, not templates;
- the transfer target is four-lens differentiation and full-chart synthesis.

Only pass 6 receives this artifact. Passes 1-5 incur no token cost from it.

### Four-thesis planning requirement

Before writing summary prose, require four distinct remembered ideas:

- identity thesis;
- daily-life thesis;
- needs/support thesis;
- growth/development thesis.

The plan must state why `What the Dog Needs` and `How the Dog Grows` are not the
same argument. It must draw from the complete selected and unselected chart
basis while keeping output approachable and non-astrology-centric.

### Tests

- Passes 1-5 do not contain the summary gold artifact.
- Pass 6 contains it and directs the author to it.
- The artifact appears in manifests and cache/accounting inventories.
- Generated workspaces remain deterministic.
- Existing authoring and assembly tests continue to pass.

## Phase 2 — Deterministic diversified claim assignment

### Design

Replace or supplement contiguous priority ranges with a versioned, opt-in
stratified assignment strategy.

The strategy should:

- preserve `priority_id`, claim ID, final assembly order, and selection semantics;
- distribute claim types, categories, semantic motifs, and estimated workload across five ten-card passes;
- maximize semantic distance between adjacent assignments where practical;
- remain deterministic for identical inputs and configuration;
- record algorithm version and seed or subject-derived hash;
- leave pass 6 dedicated to summaries and theme-group planning.

Avoid unseeded shuffling. Random-looking order is acceptable; unreplayable
production behavior is not.

Candidate modes:

- `contiguous`: current behavior and control.
- `stratified-v1`: deterministic diversified assignment.

### Tests

- All selected priority IDs appear exactly once across passes 1-5.
- Each pass contains ten claims.
- Reassembly restores canonical priority order.
- Identical input produces identical assignment.
- The manifest records assignment policy and replay material.
- Stratification improves or preserves type/category balance in fixtures.

## Phase 3 — Semantic-completeness and editorial-planning improvements

Use the Phase-0 audit to select the smallest useful upstream changes.
Candidates include:

- an operator/mode/domain/relationship contribution checklist;
- a claim-specific humor-premise field plus a deck-diversity reminder;
- a rhetorical-purpose selection for each audience rendering;
- a concise-edit question asking what could be removed without losing the remembered idea;
- a sharper distinction between recurring characterization and recurring explanation.

Do not add every candidate automatically. Each addition consumes author
attention and tokens. Implement only changes supported by Phase-0 evidence.

## Phase 4 — Preserve mechanical polish and add qualitative diagnosis

### Mechanical repair polish

Keep the existing deterministic sparse polish as the default first layer. It
must remain bounded to validator and linter findings.

### Structured qualitative critic

Design an optional read-only deck critic returning strict diagnostics. Each
finding should contain:

- quality dimension;
- exact target and comparison paths;
- diagnosis and rewrite objective;
- priority;
- required evidence or whole-chart context;
- whether a summary, card, or deck-level issue is involved.

Initial findings may include overlapping summary theses, repeated comic
mechanisms or rhetorical postures, exchangeable headlines, over-explained
bodies, incomplete compound semantics, and insufficiently distinct voices.
Cap prose targets so review cannot become an implicit whole-deck rewrite.

### Bounded qualitative polish

Optionally send only critic-selected paths, diagnoses, nearby read-only prose,
claim evidence, and necessary whole-chart context to a sparse rewrite call.
Ordinary validation and lint remain mandatory.

Do not accept a rewrite solely because its authoring model declares it better.
During this sprint, preserve candidates for comparison and human review rather
than automatically replacing the production deck.

## Phase 5 — Controlled Kevin comparison matrix

The tests below separate summary calibration, diversified card assignment, and
qualitative polish. Do not compare only an all-changes build against the old
baseline; that would obscure causality.

### Baselines

- **K0:** manual assembled Kevin deck.
- **K1:** original automated Kevin candidate before this sprint.
- **K2:** K1 with Phase-0 manual sparse polish only.

### Summary-isolation tests

Reuse accepted original card passes 1-5 so only pass 6 changes.

- **K3:** rerun Kevin pass 6 with summary gold and four-thesis planning; no qualitative polish.
- **K4:** K3 plus existing mechanical polish only, if deterministic findings require it.
- **K5:** K3 plus the proposed qualitative critic and bounded qualitative polish.

Compare K2 against K3 and K5 directly. This tests whether upstream summary
calibration can equal or outperform manual post hoc improvement and whether
qualitative polish adds value after better summary authoring.

### Claim-ordering tests

Pass-6-only reruns cannot test claim reordering. Use separate full-card runs:

- **K6:** passes 1-5 rerun under `stratified-v1`, paired with the best approved summary-pass configuration, without qualitative polish.
- **K7:** K6 plus mechanical polish as needed.
- **K8:** K6 plus qualitative critic and bounded qualitative polish.

If budget permits, preserve a contemporaneous `contiguous` rerun under the
same model and prompt versions. Otherwise use K1 as the historical control and
state the version confound explicitly.

### Comparison dimensions

Record model, reasoning, service level, prompt version, tokens, cost, latency,
attempts, validator/linter results, body-length distribution, repeated
openings, summary separation, conceptual overlap, comic mechanisms, headline
quality, compound semantic coverage, audience distinction, and label-hidden
human preference notes.

### Interpretation rules

- A cleaner deterministic report is not proof of better writing.
- A preferred passage is not proof of a better full deck.
- Evaluate summaries as a coordinated four-card set.
- Record whether an improvement came from prevention, diagnosis, or repair.
- Track cost per deck and incremental cost per accepted qualitative improvement.

## Phase 6 — Decision and integration

At the end of the comparison matrix:

1. Select the default pass-assignment strategy.
2. Decide whether summary gold is always enabled.
3. Decide whether qualitative critique is default, opt-in, sampled, or deferred.
4. Decide whether qualitative rewrites may be retained automatically.
5. Promote successful examples into versioned gold only when their lesson is clear.
6. Update authoring and runner documentation plus the quality backlog.
7. Run the full test suite and one fresh live subject QA.

## Cost controls

- Restrict complete summary gold to pass 6.
- Keep card gold small and experimental.
- Reuse accepted passes for isolated pass-6 tests.
- Keep qualitative critique read-only and structured.
- Keep qualitative rewriting sparse and capped.
- Prefer Batch for independent authoring reruns.
- Record actual token and cost data for every live variant.
- Do not rerun five card passes to test a summary-only change.

## Exit criteria

The sprint is complete when the manual polish audit and discovery checkpoint
are preserved; summary calibration and replayable diversified assignment are
implemented and tested; the qualitative critic/polish decision is implemented
or explicitly deferred; the Kevin matrix distinguishes upstream and downstream
effects; all tests pass; documentation and accounting are current; and one
fresh live end-to-end QA succeeds under the chosen configuration.
