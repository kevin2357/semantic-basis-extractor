# Post-Slice 1 thoughts — runner and tooling direction

## Decision summary

Slice 1 supports a deliberately small custom orchestration layer around the
existing `unittest` suite. It does not support replacing the test framework or
turning on unconstrained dynamic parallelism.

The recommended first supported prototype is:

- two deterministic, duration-weighted workers for the approved parallel-safe
  subset;
- one explicit serial tail for tests whose state or release authority must not
  overlap;
- a checked-in classification manifest shared by local and CI commands; and
- ordinary `python -m unittest` subprocesses beneath the coordinator.

`pytest-xdist` remains worth a short, bounded comparison in Slice 3. It should
be adopted only if file-level distribution preserves the same frozen inventory,
outcomes, isolation rules, and exact reproduction quality while materially
reducing custom code.

## Measured Slice 1 evidence

The current broad discovery contains 128 `test_*.py` modules. The conservative
static classification found:

| Classification | Modules | Current meaning |
|---|---:|---|
| Parallel-safe candidate | 39 | Pure contract/schema/fixture computation without a detected shared-state surface |
| Provisionally isolated | 54 | Uses temporary directories, subprocesses, or mock-heavy integration and requires direct isolation proof |
| Serial-only | 35 | Uses logging/process globals, build or release outputs, concurrency/locking, or historically sensitive runtime integration |

The first direct-module run exposed a real hidden order dependency: some modules
only imported successfully because earlier alphabetically discovered modules
had inserted `astrowoof_natal/src` into `sys.path`. An isolated runner therefore
must set the same explicit `PYTHONPATH` for every worker. Collection order must
never be used as environment setup.

With explicit `PYTHONPATH` and the 39-module inventory frozen, every worker
count produced the same aggregate inventory and result:

| Workers | Result | Tests | Skips | Wall time | Reduction from one worker |
|---:|---|---:|---:|---:|---:|
| 1 | pass | 239 | 41 | 88.253 s | baseline |
| 2 | pass | 239 | 41 | 46.692 s | 47.1% |
| 4 | pass | 239 | 41 | 42.257 s | 52.1% |

The four-worker round-robin saved only another 4.435 seconds. Its shards were
badly imbalanced: two completed in roughly 1–2 seconds while the heavy shards
took roughly 37 and 42 seconds. Counting modules is not a useful load-balancing
rule for this suite.

The evidence therefore favors two workers initially. Deterministic
largest-duration-first assignment using checked-in module weights and lexical
tie-breaking should capture most of the available speedup while keeping shard
membership explainable and reproducible.

Slice 0's representative logging measurement also matters to runner design:

| Posture | Wall time | Captured stderr |
|---|---:|---:|
| Existing INFO logging | 2.699 s | 304,919 bytes |
| Test-only `logging.disable(INFO)` probe | 2.471 s | 107 bytes |

Quieting routine Sparkle Dog output is therefore primarily a diagnostic-volume
and developer-usability improvement, with a modest timing benefit in the sample.
It should remain independent from the parallelization mechanism.

## What generic tools do and do not solve

Control Room issue #16 names four approaches: CI matrix sharding, a local shard
runner, narrowly scoped `pytest-xdist`, and an explicit serial group. These are
complementary rather than mutually exclusive.

### CI matrix sharding

This is the desirable eventual CI execution model, but not the source of truth
for membership. CI should ask the same checked-in manifest/coordinator used
locally for each named shard. Otherwise local reproduction and CI may silently
exercise different partitions.

### Local deterministic coordinator

This is the best fit for the first implementation. It should be a thin command
orchestrator, not a new test framework. Its responsibilities are:

1. require every discovered test module to be classified exactly once;
2. validate the approved parallel, provisional, and serial inventories;
3. set explicit `PYTHONPATH` for every subprocess;
4. remove provider, R2, Render, database, QA, and production credentials;
5. create unique worker temp, cache, coverage, log, workspace, and output roots;
6. deterministically assign approved modules using checked-in duration weights;
7. invoke ordinary `unittest` subprocesses;
8. run the serial group only after all parallel workers finish;
9. preserve shard output on failure or explicit verbose mode; and
10. emit a small JSON receipt with inventory, commands, durations, skips,
    outcomes, and exact failure-reproduction commands.

The custom portion should remain small—roughly a manifest validator, deterministic
bin packer, environment builder, subprocess launcher, and result aggregator.

### `pytest-xdist`

Pytest can collect unittest-style tests, and xdist can distribute them. The most
plausible comparison is two workers with file-level grouping (`--dist=loadfile`),
restricted to the exact approved parallel-safe module list.

It does not remove the need for AstroWoof-specific controls: the classification
manifest, serial exclusions, credential removal, isolated paths, release-boundary
sequencing, and deterministic result receipt still belong to us. Dynamic load or
work-stealing modes are not the starting recommendation because they make exact
worker membership and reproduction less stable.

Slice 3 should run a short comparison rather than presume adoption. Promote
xdist only if it:

- collects the identical frozen test identities;
- preserves pass/fail/skip results;
- respects module-level grouping and all serial exclusions;
- operates with the same sanitized and isolated worker environments;
- provides an exact, useful failure-reproduction path;
- does not introduce material collection/plugin semantic drift; and
- is simpler enough to justify adding pytest/xdist as runner dependencies.

### Other parallel runners

Tools such as `unittest-parallel` can launch unittest work concurrently, but
they do not materially reduce the project-specific safety and orchestration
work. Test-level dynamic scheduling is also a poorer first fit for modules with
module-local setup or uncertain shared state. No additional runner should be
added without beating both the deterministic coordinator and the bounded xdist
comparison on clarity, equivalence, and maintenance cost.

## Initial supported boundary

The first prototype should use only the 39 candidate modules and two workers.
The 54 provisional modules should enter only after direct filesystem,
environment, subprocess, and repeated-equivalence evidence. The 35 serial-only
modules stay serial unless a later focused investigation proves a narrower
classification.

Wheel construction, deterministic rebuilds, package/resource checks,
installed-wheel qualifications, release receipts, and all live/provider work
remain serial regardless of runner choice.

## Slice 3 recommendation

Implement the deterministic two-worker coordinator first. Then run the same
frozen subset through a narrowly configured `pytest-xdist` experiment. Record
dependency changes, collection identity, outcomes, wall time, shard behavior,
failure reproduction, and isolation observations side by side. Select the
simpler safe mechanism from evidence; do not retain two supported paths unless
they serve genuinely different purposes.
