# Evidence

## Current gate

Complete across the joint boundary. Slices 0–2 and the joint Slice 3
classification identified legitimate native actionability plus API
incumbent-policy starvation risk. API subsequently implemented and qualified
the approved `N=1` post-command rotation with exact persisted lifecycle-decision
joins. No SBE runtime change was required.

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
8. SBE's final public documents distinguish not-due release, due retrieval, and
   deterministic local work without treating any of them as a fairness hint.
9. In the six-due/four-cap production fixture, canonical due-time/action ordering
   retrieves responses `1,4,5,6`, leaves actions `2,3` untouched and due, and
   truthfully returns `continue_local_cycle / provider_reconciliation_due`.
10. API's provider-free characterization proves exact `release_until_due`
    already releases the slot, while actionable reconciliation retains the
    owner and excludes a ready peer under one-slot allocation-aware selection.
11. Sprint 58 remains a terminal-precedence negative control, and `8c389b3`
    remains a retry-ceiling cleanup positive control; neither changed healthy
    provider-pending scheduling.
12. API commit `2a7e0d7` proves `continue_local_cycle / local_work_ready` has
    zero provider operations but currently retains A, defers it, and selects it
    again over ready B. Its focused fairness module passes 5 tests.
13. Existing final results and accepted successor checkpoints appear sufficient
    for an API-owned cooperative turn; no new SBE yield meaning is required.
14. A structural one-peer-command bound is supportable. A strict wall-clock
    bound is not yet supportable because native command duration has no proven
    universal deadline.
15. Voof-paws 3 requires the exact checkpoint-bound persisted
    `local_work_ready` or due-reconciliation decision; `ordinary_resume` and
    `provider_reconciliation_cycle` labels alone cannot authorize rotation.
16. Atomic defer/release must be followed by proof that B claims before A's
    ordinary defer matures. Missing/stale/wrong-reason/mismatched decisions fail
    closed.

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
- Ran the SBE provider-pending capacity and observation-idempotency modules:
  66 passed with one expected optional-schema skip.

## Non-actions

- No provider, R2, QA database, deployment, queue, or retained-run mutation.
- No runtime source change.
- No public contract or policy change.
- No API allocation, lease, queue, or claim behavior was simulated by SBE.
