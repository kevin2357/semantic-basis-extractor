SBE completed and adopted its deterministic test-suite coordinator and
checked-in classification manifest as the supported broad-confidence framework.

Current posture:

- Supported command: `python astrowoof_natal/scripts/run_test_suite.py`
- Default profile: one worker
- Two-worker profile: available for controlled experiments, but not currently
  the performance default
- Direct unittest discovery: retained as the universal diagnostic fallback
- Build, wheel, installed qualification, and release-receipt authority: still
  serial

Safety and maintenance evidence:

- Exact one-worker/two-worker equivalence was proven over 1,115 tests and 58
  skips using matching test and outcome inventory digests.
- Every worker owns separate output roots and receives a sanitized environment.
- Logging-sensitive tests run in a protected unquiet group.
- Injected failures retain their exact shard identity and reproduction command.
- Manifest validation fails closed when a test module is unclassified, stale,
  nonexistent, or classified more than once.
- The final supported command, invoked without `--workers`, passed 1,118 tests
  with 58 skips and recorded `worker_count=1` in its receipt.

Performance result:

- One-worker authority run: 964.806 seconds.
- Two-worker authority run: 1,091.085 seconds.
- The current conservative two-worker profile was 126.279 seconds slower on
  the qualifying laptop because the serial/provisional tail dominates.

Decision:

Adopt the framework now so its manifest and safety controls remain continuously
exercised, but do not claim current parallel speedup. A separate
`20260906-duration-led-provisional-test-promotion-campaign-sprint1` will measure
all provisional modules, promote high-duration safe candidates in controlled
batches, and revisit worker count on this and stronger CI hardware. Its
non-blocking architecture slice also plans pipeline-, tier-, resource-, and
execution-profile-aware manifest growth for future natal, synastry, transit,
and production-path simulation suites.

No SBE package release was required; this was repository test/process tooling,
tests, and documentation only.
