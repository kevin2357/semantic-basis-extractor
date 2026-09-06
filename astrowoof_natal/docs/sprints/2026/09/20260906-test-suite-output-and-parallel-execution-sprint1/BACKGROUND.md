# Background — quiet provider-free tests and safe parallel execution

## Why this sprint exists

The SBE broad provider-free suite is valuable enough that it should remain a
normal release gate, but its current feedback loop is unnecessarily expensive.
During the 0.4.52 run-timeline release gate, the correctly versioned broad suite
ran 1,103 tests in 1,083.232 seconds and passed with 58 skips. A substantial
portion of its captured output consisted of production-shaped `INFO`-level
`✨🐶` records emitted by subprocess and lifecycle fixtures.

Those records are important in production and in the dedicated logging,
relay, observability, and reporter tests. They are not useful when repeated in
ordinary contract and runtime tests that do not assert logging behavior.
Formatting, transporting, capturing, and retaining hundreds of thousands of
structured records also plausibly contributes measurable wall-clock and memory
overhead. The exact contribution must be measured rather than assumed.

The longer-term opportunity is safe parallel execution. AstroWoof Control Room
[issue #16](https://github.com/kevin2357/astrowoof-api/issues/16) already frames
the cross-repository goal: parallelize isolated provider-free tests while
keeping concurrency/locking tests, migrations, wheel construction, installed
qualification, receipt generation, and live work explicitly serial.

## Problem statement

We want broad confidence without creating pressure to skip the broad suite.
Two changes may reduce its wall time:

1. make routine tests quiet by default while explicitly opting observability
   tests into the production `INFO` trace surface; and
2. run proven-isolated test groups concurrently using one deterministic shard
   manifest shared by local and CI runners.

Neither optimization may change runtime logging defaults, test semantics,
release authority, artifact construction, or provider-free safety.

## Current evidence

- The 0.4.52 broad gate completed successfully: 1,103 tests in 1,083.232
  seconds, `OK (skipped=58)`.
- Its console stream contained very large volumes of structured SBE application
  logs at `INFO`, including workspace fingerprints, native-state summaries,
  lifecycle decisions, state transitions, and checkpoint publication.
- The focused run-timeline/reporter/release-contract matrix completed 69 tests
  in 28.584 seconds with 5 skips.
- Existing logging tests intentionally verify production-shaped records and
  therefore cannot inherit a blanket suppression that makes their assertions
  vacuous.
- Control Room issue #16 requires provider-free operation, isolated temporary
  and output locations, reproducible failing shards, and serial release gates.

## Safety and authority boundaries

- Production and installed-worker logging defaults remain unchanged.
- Test quieting must occur only under an explicit test-runner boundary.
- Logging/relay/reporter tests must explicitly restore the level and sinks they
  exercise, and must fail if expected records disappear.
- Parallel execution is never authorization for provider, R2, Render, QA, or
  production access.
- A parallel shard may not write shared `.runs`, cache, temporary workspace,
  coverage, log, fixture, wheel, or release-receipt paths.
- Locking, process-global environment, logging-global-state, migration,
  deterministic-build, installed-wheel, and release-receipt tests remain
  serial until independently proven safe.
- Final release evidence continues to come from one named serial candidate,
  never from competing shards.
- Serial and parallel executions must agree repeatedly before parallel mode can
  become a documented broad-confidence route.

## Desired outcome

The repository gains a reproducible provider-free test workflow that:

- keeps routine output concise and failure-focused;
- retains full trace assertions where logging itself is under test;
- reports timing evidence for quiet versus current logging behavior;
- classifies every test module as parallel-safe or serial-only with a reason;
- offers deterministic named shards and exact reproduction commands;
- proves repeated serial/parallel result equivalence;
- materially reduces broad-suite wall time; and
- leaves the release playbook's serial build and installed qualification gates
  intact.

## Out of scope

- weakening, deleting, or skipping behavioral tests to improve timing;
- changing production trace level, schema, content, routing, or privacy rules;
- parallel wheel builds or release receipt generation;
- parallel live-provider or retained-workspace qualification;
- treating one green parallel run as sufficient isolation proof; and
- making parallel execution mandatory before the investigation establishes a
  stable benefit.
