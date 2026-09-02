# API review of investigation plan

## Decision

Approved to begin Slice 0 under the stated read-only limits.

The plan has the right shape: it treats Nori and Biscuit as separate observed
manifestations until exact checkpoint joins establish a shared cause, privileges
sealed native/checkpoint evidence over trace interpretation, and makes runtime
work conditional on a demonstrated production-boundary reproduction.

## Confirmed cross-repo guardrails

- The two exact protected checkpoint coordinate packets in `BACKGROUND.md` are
  sufficient for the proposed two `HEAD` + two conditional `GET` accesses.
  No R2 listing, writes, provider access, or retained-run mutation is
  authorized.
- Preserve the distinction between native and API assertions. In particular,
  Nori's trace records a native `terminal_closed` / `sbe.closeout.completed`,
  while API recorded the job disposition `native.terminal.review_required`.
  Those may be causally compatible, but Slice 0/2 must not call either a
  translation of the other until result, receipt, journal, and checkpoint joins
  prove the mapping.
- Biscuit's repeated generation `13` checkpoint accepts are evidence of a
  candidate no-progress loop, not sufficient alone to identify ownership. The
  Slice 2 comparison must establish whether SBE republishes identical semantic
  truth, produces an unapplied successor, or the API rejects/adopts something
  unexpectedly.
- `continue_local_cycle`, `quiescent`, and a deferred API job are observations
  that need their exact due-time/operation joins; they are not intrinsically
  contradictory.

## Small Slice 0 refinement

Record the local path and hash of the 2,000-line trace export in the Slice 0
evidence receipt, in addition to the already recorded SHA-256. That keeps the
diagnostic source reproducible for the current investigators without promoting
it to transition authority.

## Approval boundary

Proceed through Slice 0 and stop at Voof-paws 1 before protected checkpoint
access. At that pause, present the evidence map, the two run-specific hypothesis
matrices, and the exact minimal field list proposed for checkpoint inspection.
