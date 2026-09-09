# API review — promotion batch 4 completion

## Decision

**Approved**: Batch 4 is complete. Its three named modules may remain
`parallel_safe`, and SBE may select and audit a small, duration-led Batch 5.

This is approval to audit the next cohort only. It is not blanket approval to
promote Batch 5, alter semantic-closure classification, change production code,
or relax the campaign's exact-outcome/collision gates.

## Evidence accepted

- The batch retained its narrow boundaries: three already collision-qualified
  modules, frozen isolated weights, no test-identity change, and no production
  semantic change.
- The post-promotion actual-manifest proof is the right final gate. Two
  concurrent two-worker groups both yielded 340 tests, 43 expected skips, and
  identical identity and outcome digests.
- The measured critical-path increase is recorded candidly. Under the agreed
  forward-looking policy, modest current-host contention is calibration input,
  not a retroactive correctness failure when isolation and outcomes are clean.
- The plan correction is now correct: 8 prior promotions plus these 3 yields
  11 total, and the 49/44/36 manifest counts agree with that history.

## Small documentation repair

`EVIDENCE.md` still begins with the stale status “paused at Campaign paws-point
2 before broader promotion.” Please update that status to reflect Batch 4
completion and the current pause before Batch 5 selection. The detailed record
below it is otherwise consistent.

## Next boundary

For Batch 5, retain the same sequence: measured candidate selection,
state-surface audit, bounded collision matrix, then a separate promotion review
before any manifest change and actual-manifest stress proof.
