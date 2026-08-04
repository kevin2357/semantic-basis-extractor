# Phase 4 — Qualitative Critic Architecture

## Purpose

Phase 0 showed that a context-naive polish call can improve diagnosed prose but
cannot reliably discover every qualitative defect or replace missing upstream
conception. Phase 4 therefore separates three responsibilities:

1. deterministic mechanical QA and sparse repair;
2. read-only qualitative diagnosis;
3. bounded candidate editing for human comparison.

The critic is not another linter and the candidate editor is not authorized to
replace production output during this sprint.

## Placement in semantic closure

Qualitative review runs only after a structurally valid subject delivery exists.
It can be added to an already completed run through resume, so experimental
review never requires paying for authoring again.

Mechanical polish remains unchanged. Validator or linter findings continue to
control its targets and its accepted improvements may update delivery. The
qualitative layer writes only beneath `final/<subject>/qualitative/` and stores
its state in `record.qualitative_review`.

## Critic contract

The critic receives a provenance-light whole-deck view:

- all reader-facing fields and their exact paths;
- subject identity;
- card index, claim ID, type, canonical claim, categories, domains, and
  priority;
- compact semantic evidence sufficient to inspect compound meaning.

It does not receive the full projected-term registry, unselected-claim records,
or raw source graphs.

The response contains an overall strengths/risk assessment plus at most a
configured number of findings. Each finding contains:

- stable finding ID;
- quality dimension;
- summary, card, or deck scope;
- priority and confidence;
- exact target and comparison paths;
- concrete diagnosis and rewrite objective;
- required context;
- `local_repair`, `upstream_reconception`, or `advisory_only` classification.

It contains no proposed prose. Empty findings are explicitly valid.

The first dimensions are summary-thesis overlap, repeated comic mechanism,
repeated rhetorical posture, exchangeable headline, over-explained body,
incomplete compound semantics, insufficient audience distinction, insufficient
astrology-density progression, and a narrow other-editorial-quality escape
hatch.

## Deterministic critic validation and selection

Structured output constrains shape and finding count. Post-response validation
then rejects invented paths, duplicate IDs, and repeated targets.

Selection is intentionally conservative:

- confidence must be at least `0.70`;
- priority must be high or medium;
- repairability must be `local_repair`;
- default total is at most twelve fields;
- default spread is at most six cards or summaries.

Findings are expected in descending priority and confidence. A finding that
would exceed a cap remains in the critic artifact with its exclusion reason.
Upstream and advisory findings likewise remain visible without becoming edit
instructions.

## Candidate editor contract

The optional editor receives only:

- selected editable targets;
- selected diagnoses and objectives;
- critic comparison paths and nearby prose as read-only context;
- compact semantic evidence for affected claims;
- a compact whole-deck behavioral handler view only when requested.

It may omit individual targets or return an empty edit set. A nonempty candidate
must pass polish-mode structural validation and must not worsen the composite
deterministic finding count.

Even then its state is `CANDIDATE_READY_FOR_REVIEW`, not accepted. The production
deck, reports, state, and delivery ZIP remain unchanged. This preserves a clean
human A/B and prevents a critic/editor pair from serving as its own unsupported
quality judge.

## Resume and accounting

Critic and editor Responses use the existing persisted background-response
transport. Their request, response ID, complete response, structured artifact,
usage, cost, routing, and QA reports survive interruption.

Run accounting adds separate `qualitative_critic` and
`qualitative_candidate` stages. This makes the incremental price of diagnosis
and repair visible rather than blending it into authoring or mechanical polish.
A diagnosis-only checkpoint can later resume into candidate editing from its
persisted findings without issuing a second critic request.

Against the preserved polished Ella deck, the critic transport contains 1,458
reader-facing fields and 50 compact semantic descriptors. It renders to an
estimated 87,248 tokens rather than shipping the 1.68 MB deck wholesale; the
strict response schema adds approximately 410 tokens. This is intentionally a
whole-deck diagnostic call, but remains practical on Luna and is optional.

## Initial evaluation policy

The first live checkpoint should answer two questions separately:

1. Did the critic identify specific defects that a careful human review agrees
   are real, while avoiding invented busywork?
2. Did the bounded editor improve those diagnosed fields without weakening
   semantic completeness, voice distinction, memorable imagery, or nearby
   prose?

Deterministic acceptance is necessary but not sufficient. Exact findings,
omitted targets, before/after prose, token use, latency, and cost must be
preserved for review before Phase 5 uses the mechanism in the Kevin matrix.
