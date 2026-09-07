# Plan — quiet provider-free tests and safe parallel execution

## Status

Slices 0–6 complete. Quiet runner-bound logging and a deterministic weighted
runner are implemented. Exact one-worker/two-worker test and outcome
equivalence is proven, but the conservative two-worker configuration was
126.279 seconds slower on this laptop because the serial tail dominates. The
runner and manifest are adopted as the supported broad-confidence framework
with a one-worker default; two-worker execution remains experimental pending
duration-led promotion or qualification on stronger hardware. The bounded
xdist comparison was also slower and did not remove the project-specific
isolation layer. Sprint closed without a package release; duration-led
provisional promotion continues in its separate campaign.

## Objective

Shorten SBE's provider-free confidence and release feedback loops without
weakening test coverage, production observability, deterministic artifact
evidence, or the serial authority of installed-wheel qualification.

This sprint implements test-only quiet logging if its benefit and isolation are
proven. It investigates and may prototype deterministic parallel shards, but
parallel execution becomes a supported/default route only after repeated
equivalence and isolation evidence.

## Governing invariants

1. Test outcomes and assertions do not depend on whether routine `INFO` output
   is displayed.
2. Tests whose subject is logging, relay, parsing, or observability explicitly
   enable and verify the records they require.
3. Production logging behavior is byte/field/route compatible and keeps its
   existing default level.
4. Every test belongs to a named classification: parallel-safe,
   provisionally isolated, or serial-only with a reason.
5. Shard membership is deterministic, checked in, and reproducible locally.
6. Each concurrent worker owns unique temp, cache, coverage, log, database (if
   any), workspace, and artifact-output locations.
7. Provider credentials and network/live commands are absent from parallel
   runner environments.
8. Parallel and serial runs must produce equivalent collected-test identities
   and pass/fail/skip outcomes across repeated executions.
9. Wheel builds, deterministic rebuilds, package inventory checks, installed
   qualifications, and release receipts remain serial per candidate identity.
10. A speedup claim records machine, command, test inventory digest, worker
    count, logging posture, and repeated timing samples.

## Slice 0 — baseline output and timing characterization

- Preserve the 0.4.52 broad-gate result as the starting baseline: 1,103 tests,
  1,083.232 seconds, 58 skips.
- Identify how logging is configured in in-process tests and subprocess tests.
- Inventory modules that assert logs, stderr relay, JSONL events, parser input,
  logger failure isolation, or production default levels.
- Measure a representative set under the current logging posture and under an
  experimental test-only `WARNING` posture without committing behavior.
- Separate time spent in actual workloads from time spent formatting,
  transporting, and capturing logs where feasible.
- Confirm whether unittest buffering/capture, subprocess pipe handling, or test
  fixtures are the dominant output costs.
- Record exact tests that must remain explicitly `INFO`-enabled.

Deliverables:

- logging-configuration/source map;
- protected observability-test inventory;
- reproducible baseline commands and timing table; and
- go/no-go decision for test-only quiet defaults.

## Slice 1 — parallelization investigation

Use Control Room issue #16 as the parent requirements record.

- Inventory every broad-suite module and classify its state surfaces:
  temporary directories, fixed paths, environment mutation, logger mutation,
  process globals, mocks, ports, databases, caches, coverage files, package
  resources, build outputs, and subprocesses.
- Identify collection/order dependencies by comparing the current serial order
  with deterministic reordered runs.
- Detect fixed shared paths and tests that read or mutate repository fixtures.
- Establish an explicit serial-only set for concurrency/locking, global logger
  state, migrations, wheel/build/resource checks, installed qualification, and
  release evidence.
- Evaluate fixed named CI/local shards before considering dynamic scheduling.
- Evaluate whether Python `unittest` should be wrapped with deterministic
  module shards or whether adopting a narrowly scoped runner/plugin is safer.
  Do not introduce blanket `pytest-xdist` merely for convenience.
- Prototype two and four isolated workers over the safest pure-test subset.
- Record collection identities, outcomes, wall time, CPU/memory pressure, and
  failure reproduction commands.

Deliverables:

- complete module classification manifest;
- shared-state and order-dependency findings;
- recommended shard mechanism and worker ceiling;
- prototype timing/equivalence evidence; and
- proposed boundary between parallel confidence checks and serial release
  checks.

**Voof-paws 1:** jointly review the evidence before making quiet logging or
parallel sharding the documented default.

Reached. No default behavior has changed.

## Slice 2 — quiet-by-default test harness

Proceed only if Slice 0 shows a worthwhile benefit and a closed implementation
boundary.

- Add one test-runner-specific default that raises ordinary test logging to
  `WARNING` without changing imported package or production defaults.
- Provide an explicit helper/context for tests that require `INFO` structured
  logs, stderr relay, or event streaming.
- Migrate logging-sensitive tests to that explicit posture.
- Restore logger levels, handlers, propagation, environment, and sinks after
  each test so order cannot affect behavior.
- Ensure subprocess fixtures receive the intended test logging posture through
  explicit arguments/environment rather than accidental parent state.
- Keep useful failure diagnostics available, including an opt-in verbose rerun
  command.

Tests:

- production default remains `INFO` where currently specified;
- ordinary tests do not emit routine `INFO` noise;
- each protected logging surface still emits and validates expected records;
- logger/emitter failure-isolation tests remain meaningful;
- serial order permutations cannot leak logging state; and
- pass/fail/skip inventory matches the pre-change baseline.

## Slice 3 — deterministic isolated shard runner

Proceed only for the subset approved at Voof-paws 1.

- Add a checked-in classification/shard manifest with stable module membership
  and explicit serial reasons.
- Add a provider-free local runner that creates unique per-shard temp, cache,
  log, coverage, and output roots.
- Reject provider credentials and shared release/output paths before starting
  workers.
- Emit a small deterministic aggregate receipt containing suite inventory,
  shard commands, outcomes, durations, skips, and failure reproduction commands.
- Preserve individual shard stdout/stderr only on failure or explicit verbose
  mode.
- Run the serial-only group separately and require it alongside all parallel
  shards for a broad-confidence pass.
- After the coordinator works against the frozen candidate inventory, run one
  bounded `pytest-xdist` comparison using two workers and file-level grouping.
  Do not enable unconstrained dynamic scheduling or include provisional/serial
  modules merely to exercise the tool.
- Compare the coordinator and xdist on exact collected identities,
  pass/fail/skip results, environment/path isolation, wall time, dependency and
  collection-semantic changes, and the quality of an exact failure-reproduction
  command.
- Adopt xdist only if it satisfies the same manifest, sanitation, isolation,
  serial-tail, and receipt requirements while materially simplifying the
  supported implementation. Otherwise record it as evaluated and retain the
  coordinator.

## Slice 4 — repeated equivalence, isolation, and failure qualification

- Run the same frozen inventory serially and in parallel repeatedly at the
  approved worker counts.
- Compare exact collected identities and result classifications, not merely
  process exit codes.
- Inject one deterministic failure per shard and prove the aggregate fails with
  an exact local reproduction command.
- Prove no shard writes another shard's directories or the repository's release
  output paths.
- Prove no provider, R2, Render, QA, production, or network activity occurs.
- Run race/order-sensitive and artifact/release tests only in the serial group.
- Check for flaky timing, resource exhaustion, orphan subprocesses, and Windows
  file-lock behavior.
- Require a material repeated wall-clock improvement before adoption.

**Voof-paws 2:** review equivalence and isolation evidence before CI or release
playbook adoption.

Reached. No CI/default/release-playbook adoption has begun.

## Slice 5 — process and CI adoption

- Add CI matrix shards only if the same checked-in manifest drives local runs.
- Require every shard plus the explicit serial group in the aggregate gate.
- Update the Maintainer Release Playbook with:
  - quiet and verbose focused-test commands;
  - parallel broad-confidence command;
  - serial fallback/reproduction command;
  - the immutable serial release-build and installed-qualification boundary;
  - circumstances that force the entire suite back to serial; and
  - how to update and review shard classifications.
- Update contributor/testing documentation and Control Room issue #16 with
  measured results and any remaining exclusions.

Adoption decision: use the checked-in runner and manifest as the supported
broad-confidence framework now, with one worker as the default profile. Retain
direct unittest discovery as the universal fallback. No repository CI workflow
currently exists to wire; future CI must consume the same manifest/coordinator.
Two-worker execution is not the default and no current speedup is claimed.

## Slice 6 — closeout or tooling release decision

- Run focused tests for the test harness/runner itself.
- Run one final serial broad suite and the approved parallel equivalent from the
  same source identity.
- Run `git diff --check` and review repository status.
- If only repository test/process tooling changed, close without manufacturing
  a package release.
- If installed package behavior or packaged resources changed unexpectedly,
  stop and apply the full release playbook under a fresh version.
- Record timing, inventory digests, outcomes, exclusions, and rollback command.

Complete. The supported default command passed 1,118 tests with 58 skips using
its implicit one-worker profile. This repository-only tooling/docs change does
not require an SBE package release.

## Initial test strategy

- Characterization is read-only and provider-free.
- Quiet-logging work starts with dedicated logging/event/reporter suites plus a
  representative ordinary-runtime sample.
- Parallel work starts with pure schema, validator, and fixture modules.
- Provider-free integration modules enter parallel shards only after unique
  workspace/output proof.
- All release artifact work stays serial regardless of shard success.

## Expected result

The common case becomes quieter and faster while the safety case becomes more
explicit:

- developers see failures rather than megabytes of routine `INFO` records;
- observability tests still prove production trace behavior directly;
- broad provider-free confidence can use deterministic isolated shards; and
- the final installed artifact and its release receipt remain one serial,
  provenance-bound authority chain.
