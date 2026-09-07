# Background — duration-led provisional test promotion campaign

## Why this campaign exists

The test-suite output and parallel-execution sprint established a sound,
provider-free runner boundary: deterministic module classification, isolated
worker roots, secret scrubbing, exact outcome inventories, protected
observability tests, and a serial release-authority tail.

Its first conservative manifest intentionally classified only 38 of 129 test
modules as parallel-safe. Those modules complete in roughly 45 seconds with two
workers, while the provisional and protected serial groups account for nearly
all of the broad suite's roughly 21-minute wall time. The runner is therefore
working, but the initial safe set is too small to deliver a material whole-suite
speedup.

The next optimization should not be “add more workers.” It should be an
evidence-led campaign to measure the 55 provisional modules, identify the
largest contributors, prove or create their isolation boundaries, and promote
them in controlled batches.

## Starting evidence

- The checked-in manifest classifies 129 modules:
  - 38 parallel-safe;
  - 55 provisional;
  - 36 serial-only.
- The existing parallel-safe prefix executes 236 tests with 40 skips in about
  44–46 seconds under the custom two-worker runner.
- The conservative serial tail dominates the broad run at approximately 20
  minutes.
- A bounded `pytest-xdist` comparison was slower than the custom coordinator
  and did not remove AstroWoof's project-specific classification, sanitation,
  isolation, receipt, or serial-tail requirements.
- At least two modules that assert `INFO` logging were correctly kept in an
  explicit unquiet protected group. Logging behavior must not be accidentally
  erased during promotion.

Exact authoritative Slice 4 equivalence results remain owned by the preceding
test-suite sprint. This campaign consumes that completed evidence; it does not
rewrite it.

## Campaign hypothesis

A relatively small number of slow provisional modules likely account for most
of the serial tail. Some may already be parallel-safe but were conservatively
unproven. Others may become safely isolated through narrow test-only changes,
such as replacing fixed paths with owned temporary roots, restoring mutated
environment or logger state, or giving subprocesses unique outputs.

Promoting the slowest safe modules first should produce substantially more
wall-clock benefit than uniformly reviewing every provisional module or
increasing worker count against the original 38-module set.

## Safety boundaries

- No behavioral assertion may be weakened, skipped, or deleted to improve
  timing.
- No production behavior, public contract, package resource, or runtime
  logging default changes merely to make a test parallel-safe.
- Test-only isolation repairs must preserve the scenario and failure mode each
  test proves.
- Modules involving shared repository paths, process-global mutation,
  concurrency/locking semantics, build artifacts, installed wheels, release
  receipts, migrations, or live/external systems remain serial unless their
  isolation is separately and convincingly proven.
- Worker environments remain provider-free and scrub secret-bearing
  AstroWoof, OpenAI, database, Render, AWS, and Cloudflare variables.
- Release construction and installed-artifact authority remain serial even if
  their source test modules can execute independently.
- Promotion decisions are checked-in classifications with evidence, not
  transient scheduler guesses.
- A timing improvement is accepted only alongside exact test and outcome
  equivalence.

## Desired outcome

The repository gains a materially faster broad-confidence path whose larger
parallel set remains deterministic, provider-free, reproducible, and easy to
fall back from. Each promoted module has a recorded isolation basis; each
remaining provisional or serial module has a concrete reason and an estimate
of whether further work is worthwhile.

## Out of scope

- replacing the custom runner with xdist without new contrary evidence;
- parallelizing wheel builds, release receipts, or live qualifications;
- changing application semantics for test convenience;
- chasing low-duration modules whose likely savings cannot justify review;
- claiming linear speedup from worker count alone; and
- making the campaign a prerequisite for finishing the current runner sprint.
