# API review — promotion batch 5 completion

## Decision

**Approved.** Batch 5 is complete. Its three named modules remain
`parallel_safe`; SBE may select and audit a small, duration-led Batch 6.

## Evidence accepted

- The change stays exactly bounded to the three already collision-qualified
  modules. The campaign projection correctly advances from `49/44/36` to
  `52/41/36`; the distinct live `52/44/36` count is honestly explained by
  concurrent editorial-contract modules entering the provisional set.
- Two concurrent actual-manifest two-worker groups both produced 354 tests,
  44 expected skips, empty runner stderr, and identical test, outcome, and
  manifest digests. This proves the promoted set behaves consistently in the
  real manifest rather than only in the hand-built collision matrix.
- The 420–424 second wall times are material host-contention evidence, but do
  not contradict the established isolation proof. Four qualification-heavy
  child processes were deliberately contending on the laptop, while outcomes,
  skip posture, and cleanup remained exact. No speedup claim is warranted yet.

## Next boundary

Re-rank the remaining provisional tail and audit only the next compact cohort.
Keep semantic closure serial, keep newly added editorial-contract modules out
of the campaign until they receive their own timing/audit evidence, and retain
the separate worker-count and authoritative whole-suite calibration gates.
