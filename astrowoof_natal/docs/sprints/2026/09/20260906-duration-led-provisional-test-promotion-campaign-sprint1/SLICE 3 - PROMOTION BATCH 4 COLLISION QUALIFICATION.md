# Slice 3 — promotion batch 4 collision qualification

## Result

The entire three-module cohort passed its approved collision matrix. This
document proposes promotion but does not change the manifest; promotion and
the resulting actual-manifest stress runs remain behind review.

## Matrix

Three repetitions launched two independent copies of every candidate together,
for six worker processes per repetition and 18 successful workers overall.

| Module | Result per copy | Repetition durations (seconds) |
|---|---|---|
| final-QA mixed custody | 4 tests, 0 skips | 21.61/20.86; 24.15/23.96; 28.81/28.87 |
| post-fan-in routing runtime | 9 tests, 0 skips | 16.71/16.42; 18.75/19.54; 21.28/21.02 |
| external-authority v2 route qualification | 3 tests, 0 skips | 16.04/15.73; 18.68/18.13; 19.69/19.83 |

Across all repetitions:

- no failures, errors, skips, or identity loss occurred;
- unsupported routing retained its byte-level pre/post nonmutation assertion;
- exact/bounded v2 cases retained their local create/retrieve call inventories;
- all artifacts remained below independent temporary roots; and
- no provider, network, database, repository, R2, Render, or QA activity
  occurred.

The modest duration increase across repetitions was shared by all six
processes and produced no correctness or cleanup instability.

## Proposed next step

If approved, move the three modules from `provisional` to `parallel_safe` using
their frozen isolated weights (16.625, 14.857, and 12.966 seconds), then run two
actual two-worker parallel-manifest groups concurrently and require exact
matching identity/outcome digests.

Current manifest remains 46 parallel-safe, 47 provisional, and 36 serial-only.
Semantic closure remains unchanged and serial.
