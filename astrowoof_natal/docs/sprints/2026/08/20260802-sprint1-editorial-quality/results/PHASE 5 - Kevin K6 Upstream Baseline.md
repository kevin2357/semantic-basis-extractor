# Phase 5 — Kevin K6 Upstream Baseline

## Purpose

K6 is the clean current-code upstream baseline for the controlled Kevin matrix.
It measures the authoring pipeline before whole-deck mechanical polish or
qualitative review. It is not silently upgraded into a delivery deck.

The run used fresh SBE extraction, deterministic `stratified-v1` assignment,
`compact-v2` chart context, cost-optimized Batch routing, Luna/medium initial
authoring, Terra/medium creative retry, four-thesis summary planning, no
same-subject prose gold, and no polish or critic.

Run directory: `work/phase-005-controlled-kevin/k6-upstream`

## Authoring outcome

The first Batch contained six Luna requests. Passes 1 and 6 passed immediately.
Passes 2–5 were rejected only for `invalid_context_filter` and entered one
four-request Terra retry Batch. All four retries passed. Seven claims were
affected: one in pass 2, one in pass 3, three in pass 4, and two in pass 5.

No rejection was caused by prose duplication, incomplete delivery, theme-group
structure, or editorial-independence failure.

## Final QA outcome

All six passes ended in `PASS_QA_ACCEPTED`, assembly completed, and structural
validation passed. The unpolished run then correctly stopped at
`FINAL_QA_REQUIRES_REVIEW`.

The linter reported:

1. `Kevin, you are` begins six no-astro direct-to-dog bodies.
2. `Kevin, you can` begins six no-astro direct-to-dog bodies.
3. The fine-print humor mechanism appears four times across three card
   headlines and one summary body.

The validator retained five advisory possible no-astro astrology leaks: cards
13, 43, 48, and 49, plus summary card 3. These are bounded surface findings
suitable for K7 mechanical polish; they do not establish conceptual redundancy.

## Usage and cost

- Input tokens: 425,608
- Cached input tokens reported: 0
- Output tokens: 145,336
- Total tokens: 570,944
- Estimated Batch-discounted cost: $1.12486975

This is not a clean estimate of necessary prose-authoring cost. Four full Terra
retries were triggered by constrained metadata mistakes.

## General architectural findings

### Constrained metadata should not trigger creative regeneration

Context-filter labels come from a fixed vocabulary. Once a pass has otherwise
valid prose, an invalid filter should be handled by deterministic sanitization,
bounded metadata repair, or a metadata-only retry. Escalating the entire pass
discards usable creative work and confounds authoring-cost measurement. This
run records the need; it does not yet implement that recovery route.

### Pass-local acceptance cannot certify deck-level diversity

The repeated openings and comic mechanism crossed independent pass boundaries.
Each pass could be acceptable while the assembled deck converged rhetorically.
Stratified claim order cannot provide global prose memory to isolated authors.
Whole-deck QA is therefore architectural, not redundant.

### Accepted source and delivery-ready artifact are different states

K6 is structurally valid and analytically useful while unsuitable for direct
delivery under the default lint policy. `FINAL_QA_REQUIRES_REVIEW` preserves
that distinction and the best valid baseline.

### Repair layers require preserved lineage

K6 should remain byte-stable. K7 will be a copy with bounded mechanical repair;
K8 will add qualitative diagnosis and a separately reviewable candidate. This
attributes changes to prevention, mechanical repair, or qualitative judgment.

### Retry cost must be classified by cause

Comparative reporting should separate genuine creative escalation from
metadata-driven escalation. Otherwise avoidable control-flow cost can be
mistaken for the model cost of acceptable prose.

## Operational finding

The initial detached submission exposed a transient Windows file lock during
atomic `run.json` replacement. The input file ID was durably saved, so resume
created the Batch without duplicate upload or paid requests. The runner now
retries short-lived `PermissionError` locks while preserving atomic replacement
and still fails on persistent or non-permission errors.

## Next comparison stages

- **K7:** copy K6 and apply only sparse mechanical polish to validator/linter
  findings.
- **K8:** preserve K7, run the qualitative critic, and create a bounded candidate
  only for locally repairable findings.
- Compare K6, K7, and K8 against historical and manual Kevin baselines using
  deterministic reports, cost attribution, and unlabeled editorial review.
