# Evidence

## Current gate

SBE Slices 0–1 are complete and ready for the first joint review. No runtime
implementation or replay harness has begun.

## Findings

1. A retained post-Sprint-58 pair has a 97-second initial-wave gap.
2. Three retained trace windows prove provider-lifetime overlap on September
   2–3, but with later peer gaps of roughly five to nine minutes.
3. Podium/Laurel prove a terminal-boundary peer wait on September 6.
4. Sprint 58 completed August 30 and did not edit nonterminal capacity release,
   allocation ownership, queue selection, or reconciliation bounds.
5. SBE `0.4.31` added terminal-result availability only.
6. The existing full-pool allocation-owner restriction predates Sprint 58 and
   remains the mechanism capable of excluding a peer while an incumbent retains
   its allocation.
7. The regression is increased peer time-to-first-submit, not a proven binary
   loss of all overlap. Exact causality remains open.

## Commands and source checks

- Enumerated SBE and API sprint files and creation times.
- Inspected API history from `31237f6` through `bc5873f`.
- Inspected production diffs for `d34d3b8` and `56511f6`.
- Inspected current API execution queue, capacity, terminal ingress, runtime,
  worker, and provider-pending release paths.
- Inspected SBE initial-wave timing constants and temporal lifecycle due-subset
  validation.
- Enumerated later scheduling/terminal commits through September 6.
- Confirmed the paced Render export completed without CLI throttling and does
  not contain the immediate cutover cohort.

## Non-actions

- No provider, R2, QA database, deployment, queue, or retained-run mutation.
- No runtime source change.
- No test harness construction before joint review.
