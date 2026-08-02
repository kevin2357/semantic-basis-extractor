# Sprint Plan: Editorial Quality Beyond Mechanical Acceptance

- **Date:** 2026-08-02
- **Sprint:** 1
- **Status:** Phase-0 discovery complete; implementation plan updated from findings
- **Primary subject:** Kevin
- **Supporting subjects:** Ella and future comparison subjects as needed
- **Related backlog:** `docs/post_extraction_authoring/Editorial Quality Research and Improvement Backlog.md`

## Objective

Improve the semantic-closure authoring pipeline in quality dimensions that are
not adequately represented by deterministic validation and linting, while
preserving its reliability, evidence boundaries, resumability, and low cost.

The sprint began with a bounded, human-directed polish experiment. Its findings
now define the responsibility boundary for implementation. Subsequent work will
add pass-6 summary calibration, deterministic diversified claim assignment,
upstream editorial-planning improvements, narrow production-polish hardening,
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

## Phase 0 — Human-directed, context-naive API polish experiment

### Scope

The human/long-context role is diagnosis, prompt design, context selection, and
evaluation. A fresh API response with no conversation history writes every
replacement. Do not manually author replacement prose for the primary
experiment.

The goal is not to force production of a better deck. The goal is to determine
which writing-quality problems can and cannot be repaired after independent
authoring passes have produced a complete deck. A weak or neutral result is
valid and valuable evidence.

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

The diagnosis ledger must not contain proposed replacement prose.

### Experimental isolation

- Use a fresh API response with no previous response ID or conversation state.
- Include only context reproducible by the production pipeline.
- Supply source and whole-dog context already available to the original
  authoring workflow where required for a target.
- Do not include the old manual Kevin deck or any gold examples.
- Do not quote successful old-deck wording in diagnoses or prompt guidance.
- Return only sparse edits to explicitly allowlisted paths.
- Record the exact package, prompt, model, reasoning level, response, usage,
  cost, and latency.

### Pre-submission review gate

After the request package, prompt, schema, and invocation command are ready,
stop before contacting the OpenAI service. Report their exact repository paths
and the exact prompt to the user. Submission requires explicit approval after
that review.

### Iteration policy

Round 1 is not required to produce a superior deck. If its output reveals a
specific, testable weakness in task framing or supplied context, preserve the
round unchanged and consider Round 2 or Round 3. Each round must state its
hypothesis and change only the variables needed to test it. Do not iteratively
prompt merely to chase a preferred result.

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
3. human-directed, context-naive API-polished Kevin.

Where practical, review without revealing which version produced a passage.
Assess memorability, behavioral clarity, grounding, usefulness, voice,
summary-lens separation, and naturalness.

### Discovery checkpoint

Stop after Phase 0. Summarize findings in `LOG.md` and under `results/`. Revise
the remaining sprint plan if the audit shows that a problem belongs at a
different pipeline stage than currently assumed. No production implementation
begins before this checkpoint is recorded.

### Phase-0 discovery conclusion

Phase 0 established a sufficiently stable architectural boundary for the rest
of this sprint:

> Upstream authoring owns conception. Polishing owns evaluation and revision.

A finished deck should remain acceptable if polish makes no changes. The
polish pass is a selective editor and safety net, not the first stage at which
the system decides what a card is about.

Upstream authoring therefore owns:

- the whole-dog portrait and coherent characterization;
- one distinct remembered idea, behavioral doorway, and creative thesis per
  card;
- semantic differentiation among neighboring claims;
- audience purpose and astrology-density conception;
- claim-specific humor premises and initial headline quality;
- complete treatment of compound semantic contributions;
- four genuinely different full-chart summary arguments.

Polish owns or is well suited to:

- preservation-aware `keep` or `replace` evaluation;
- repeated openings and sentence architectures;
- reused comic mechanisms;
- isolated weak headlines and over-explained bodies;
- restoration of supplied compound semantics that prose has flattened;
- false-positive-aware review of deterministic advisories;
- bounded deck-level cleanup that does not reconceive the cards.

Humor, headlines, voice distinction, summary coherence, semantic precision,
and deck diversity remain shared responsibilities: they must begin upstream
and may receive targeted downstream inspection.

Use this routing test when assigning later work:

> Can an editor identify and repair the defect from the finished prose and
> localized evidence without deciding anew what the card fundamentally is?

If yes, the issue is a reasonable polish target. If repair requires a new
thesis, scene, audience posture, joke premise, or whole-chart interpretation,
it belongs upstream.

The full experiment and comparison are preserved in:

`results/PHASE 0 - Targeted Polish Capability Study.md`

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

### Live checkpoint

An isolated Kevin pass-6 API test confirmed that the four-thesis plan produces
distinct identity, daily-life, present-needs, and developmental arguments. The
new summaries recovered the manual reference's richness and materially
improved lens separation over the historical automated baseline.

Because Kevin was also the subject of the complete prose gold, the test exposed
same-subject reference leakage: 30 distinct shared twelve-word sequences and
several transferred organizing frames remained despite explicit anti-copying
instructions. Treat the thesis plan as accepted and the complete prose gold as
experimental. Before making gold always-on, perform a cross-subject pass-6 test
and inspect both quality transfer and structural/phrase leakage.

The live test also exposed a separate pass-6/final-validator contract gap for
theme-group balance. Preserve it as a defect to address without conflating it
with summary calibration.

The subsequent cross-subject Ella test found no exact headline reuse, no
shared eight-word-or-longer sequences, and only one ordinary six-word overlap
with the Kevin gold. This supports same-subject semantic alignment—not general
gold imitation—as the mechanism behind the Kevin leakage. Complete prose gold
may remain a cross-subject experiment but must never use the target subject's
own prose. Its marginal quality benefit remains unproven because the thesis
plan and gold were introduced together and Ella's prior summaries were already
stronger in several literary dimensions.

Summary evaluation must include product fit, not literary quality alone. The
longer optimized Ella summaries and the shorter Phase-1 summaries will be
reviewed in the current desktop and mobile UI. Record screen-level readability,
scroll burden, perceived tractability, skimmability, and whether a user is
likely to finish each card. A richer summary that users avoid reading is not
automatically the better product result; UI review may justify a shorter target
even when the longer version is stronger as standalone prose.

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
- Generated pass manifests and the run manifest expose the exact canonical
  priority IDs, policy, algorithm version, and replay seed.

## Phase 2.5 — Live-run reliability hardening

Address the defects exposed by the Phase-2 live A/B before adding more
editorial complexity:

- treat a durable background response that exceeds the local polling window as
  waiting work, not a failed creative attempt;
- never cancel or resubmit that response automatically; resume the same response
  ID and attempt number;
- preserve accepted-pass state as an invariant when durable acceptance evidence
  and the accepted workspace exist;
- detect missing writable files and fields before invoking opaque editorial QA,
  emit structured `incomplete_delivery` feedback, and retry cleanly;
- enforce pass-6 theme-group count and balance rules at the same boundary as the
  final deck validator;
- cover every path with deterministic regression and resume tests, including
  the Batch reconstruction path.

Cache-TTL tuning and a future `stratified-v2` remain deferred. This phase changes
reliability contracts, not assignment semantics or creative guidance.

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

### Full-chart basis transport review

Review the `FULL CHART BASIS.md` representation supplied to authoring and
summary agents. The current rendering is usable, but it may spend tokens on
low-value structural detail while presenting important chart relationships in
a form that is harder to synthesize than necessary. This is outside the
Phase-0 polish experiment and must not alter its input after submission.

Measure token cost, retained semantic coverage, evidence traceability, and
resulting whole-dog comprehension. Compare the current rendering with at least
one more compact, author-oriented representation before changing the
production handoff.

## Phase 3.5 — Narrow production-polish hardening

Apply only the inexpensive, low-disruption Phase-0 findings that fit the
current polish architecture. This is not the full qualitative critic or
editorial-handbook project described in Phase 4.

Candidate changes, subject to inspection of the current implementation:

- let a polish target resolve to `keep` or no-op when a validator/linter
  advisory is not a substantive writing defect;
- state compactly that preservation of strong prose is editorial success;
- require every replacement to repair the named mechanism while retaining the
  field's strongest image, behavioral insight, or useful guidance;
- provide localized source evidence for semantic-completeness findings,
  especially compound claims, without sending unnecessary whole-chart context;
- distinguish concision from automatic shortening and preserve current length
  when richness is doing useful work;
- keep all existing sparse allowlists, locked-field checks, deterministic QA,
  retry behavior, resumability, and cost accounting;
- place stable compact guidance in a cacheable prompt prefix where practical.

Explicitly out of scope for this stage:

- the full Round-2 editorial handbook;
- mandatory review of every reader-facing field;
- a separate LLM critic call;
- broad summary rewriting;
- a new multi-stage polish architecture.

Tests must prove that accepted no-op decisions do not mutate the deck, actual
replacements remain sparse, false-positive advisories need not trigger prose
damage, compound repairs receive adequate evidence, and ordinary low-cost runs
do not incur a large input-token increase. Record before/after prompt tokens
and estimated polish cost on the next live QA.

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
- **K2:** K1 with Phase-0 human-directed, context-naive API polish only.

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

The sprint is complete when the context-naive polish audit and discovery checkpoint
are preserved; summary calibration and replayable diversified assignment are
implemented and tested; the qualitative critic/polish decision is implemented
or explicitly deferred; the Kevin matrix distinguishes upstream and downstream
effects; all tests pass; documentation and accounting are current; and one
fresh live end-to-end QA succeeds under the chosen configuration.
