# Plan — duration-led provisional test promotion campaign

## Status

Slices 0, 0A, 1, 1A, and 2 plus Slice 3 promotion batch 2 are complete. Five
audited provisional modules have moved to `parallel_safe`, producing a 46/47/36
manifest after promotion batch 3. The campaign is paused at the requested
combined review point before another cohort is selected. Semantic closure remains serial: support-only extraction passed exact
equivalence, but no behavioral family moved and no test identity changed.

## Objective

Reduce broad-suite wall time materially by measuring all provisional modules
and promoting the highest-value safely isolated modules into the deterministic
parallel set without changing tested semantics or release authority.

## Governing rules

1. Duration identifies review priority; duration never proves isolation.
2. Promotion requires exact identity/outcome equivalence plus an explicit
   state-surface assessment.
3. Every promoted module owns all writable paths and restores any environment,
   logger, process-global, cache, mock, or subprocess state it changes.
4. A test-only repair may improve isolation, but must preserve the original
   assertion, scenario, and failure sensitivity.
5. Protected observability modules remain explicitly unquiet wherever their
   assertions require production-shaped logs.
6. Provisional modules are promoted in small, reviewable batches with an exact
   rollback consisting of manifest and associated test-isolation changes.
7. Each batch is compared against the frozen serial baseline using exact test
   identities, outcome inventories, failures, errors, skips, and unexpected
   successes—not exit code alone.
8. Provider credentials, storage credentials, database URLs, and other
   secret-bearing external-service variables remain absent from child workers.
9. Release builds and installed-wheel qualifications remain a separate serial
   authority chain.
10. Whole-suite speedup claims use repeated runs from a named source identity
    on the same machine and record worker count and resource pressure.
11. This campaign may change the recommended worker profile, but it does not
    reconsider whether the already-adopted manifest/coordinator exists as the
    supported broad-confidence framework.

## Slice 0 — freeze baseline and enhance timing evidence

- Import the final manifest, source identity, inventory digest, outcome digest,
  wall time, and group timings from the preceding sprint.
- Confirm the provisional set contains exactly the expected 55 modules and
  that no module is unclassified or multiply classified.
- Extend the runner's diagnostic receipt, if necessary, to capture per-module
  elapsed time for serial/provisional execution without changing test outcomes.
- Extend the existing `--measure-weights` calibration path explicitly: it
  currently measures only `parallel_safe` entries and must not classify or run
  provisional modules through the parallel path merely to time them.
- Measure every provisional module in a deterministic one-module-at-a-time
  calibration pass using the same quiet/unquiet and sanitized environment rules
  intended for production test runs.
- Measure `test_semantic_closure.py` separately as a named serial-only
  scheduling atom. Do not reclassify it through the provisional calibration
  path.
- Repeat materially noisy/slow measurements and record median plus range rather
  than trusting one sample.
- Produce a ranked table with cumulative serial-tail contribution and an
  initial Pareto cut (for example, modules accounting for roughly 70–80% of
  provisional time).

Deliverables:

- frozen baseline pointer;
- complete provisional timing inventory;
- ranked promotion-candidate table;
- timing methodology and noise notes; and
- runner timing changes covered by focused tests, if any.

**Campaign paws-point 1:** review the ranked inventory and choose the first
promotion batch before modifying test isolation.

## Slice 0A — semantic-closure module decomposition feasibility

This is the campaign's one explicit exception to the normal “small test-only
repair” preference. It is an investigation only; implementation requires a
separate go/no-go decision.

- Measure `test_semantic_closure.py` independently and determine its share of
  the serial tail. The module is currently `serial_only`, contains 98
  test methods, and is one indivisible scheduling atom despite covering many
  distinct behaviors.
- Map its test classes, shared fixtures/helpers, module/process globals,
  environment and logger mutation, filesystem roots, subprocesses, provider
  fakes, concurrency cases, and ordering assumptions.
- Group its cases into plausible cohesive modules such as initial authority,
  reconciliation/retry, optional qualitative stages, Batch behavior,
  persistence/checkpointing, finalization/cleanup, and provider
  accounting/routing.
- Determine whether common fixtures/helpers can move to a non-test support
  module without altering discovery, patch targets, setup/teardown order, or
  failure sensitivity.
- Compare three options:
  1. retain the module intact and serial;
  2. split it for maintainability but keep every resulting module serial; or
  3. split it and separately qualify appropriate child modules for parallel
     execution while retaining truly global/concurrent cases as serial.
- Estimate implementation size, review burden, likely merge-conflict risk,
  expected scheduling benefit, and rollback complexity.
- Define an exact before/after inventory and outcome equivalence proof that
  accounts for renamed test identities rather than hiding them behind aggregate
  counts.
- Reject decomposition if it would require broad production changes, weaken
  assertions, obscure scenario ownership, or create a fragile shared-fixture
  abstraction merely to improve timing.

Deliverables:

- independent duration and serial-tail contribution;
- state-surface and test-family map;
- proposed file/helper boundaries, if viable;
- benefit/risk/effort comparison of the three options; and
- explicit go/no-go recommendation for a larger test-only refactor.

**Special refactor paws-point:** owner/reviewer approval is required before any
semantic-closure decomposition. All other campaign candidates remain limited
to small, easily attributable isolation repairs.

## Slice 1 — state-surface audit of the highest-value batch

For each selected high-duration module:

- inventory fixed filesystem paths, repository writes, temporary directories,
  caches, environment mutation, logger mutation, process globals, mock scope,
  ports, databases, subprocesses, clocks/randomness, and package/build outputs;
- distinguish true serial semantics from incidental test-harness coupling;
- identify whether the module is already safe, needs a narrow test-only repair,
  or must remain serial;
- define collision probes that run the candidate concurrently with itself and
  with representative existing parallel modules; and
- record the exact reason and expected timing value for its disposition.

No module changes classification in this slice.

## Slice 1A — semantic-closure support extraction and serial equivalence

This is the approved first implementation phase of the Slice 0A feasibility
study. It remains separate from provisional promotion and from any test-family
move.

- Freeze the exact 98-test pre-extraction identity and outcome inventory.
- Create one non-discovered, test-only support module for the shared compiled
  packet fixture, response builders, and scripted transport used across test
  modules.
- Keep fixture material process-local and immutable by convention; do not add a
  persisted or cross-process cache.
- Update consumers to import shared support directly rather than importing the
  giant discovered test module merely to obtain its fixture.
- Keep every test method in its existing file/class with its existing identity.
- Keep production patches pointed at the original production module symbols.
- Run the original semantic-closure module serially and require an exact
  identity/outcome match to the frozen pre-extraction receipt.
- Run all direct consumers of the extracted support to catch import, fixture,
  patch-target, and setup/teardown drift.
- Record the support dependency inventory and prove the new support filename is
  outside `test_*.py` discovery.

**Semantic-closure move paws-point:** pause after support extraction and serial
equivalence. Moving any behavioral family, renaming any test identity, or
attempting parallel promotion requires the next explicit approval.

## Slice 2 — first test-isolation repair and promotion batch

- Apply only the smallest test-only isolation changes approved in Slice 1.
- Prefer owned temporary roots, unique cache/output paths, explicit environment
  restoration, scoped logger configuration, and deterministic subprocess
  cleanup.
- Do not mock away concurrency, persistence, locking, or publication behavior
  that the test exists to prove.
- Add focused regressions for each repaired state surface.
- Run every candidate alone, concurrently with itself where meaningful, and in
  the full parallel group repeatedly.
- Promote only modules whose exact outcomes and isolation probes remain stable.
- Leave rejected candidates provisional/serial with the observed reason.
- Treat correctness/isolation as the promotion gate. Current-machine timing is
  calibration evidence, not a veto for a safely parallelizable module unless
  slowdown is clearly substantial/pathological or exposes resource instability.

**Campaign paws-point 2:** review the first promotion batch and measured gain
before expanding the technique.

## Slice 3 — iterative duration-led promotion batches

- Recompute the serial-tail timing ranking after Batch 1.
- Select the next highest-value cohort rather than mechanically continuing in
  lexical order.
- Repeat state-surface audit, narrow repair, collision qualification, and exact
  outcome comparison.
- Keep each batch small enough that a regression has a narrow attribution and
  rollback.
- Stop promoting when marginal savings no longer justify isolation complexity,
  resource contention erases the gain, or remaining modules express genuinely
  serial semantics.

The number of batches is evidence-dependent. Each batch receives its own short
evidence record and manifest diff.

## Slice 4 — worker-count and scheduling calibration

After the parallel set becomes materially larger:

- compare one, two, three, and four workers where machine capacity permits;
- retain deterministic weighted assignment and lexical tie-breaking;
- measure wall time, CPU utilization, memory pressure, file-lock contention,
  subprocess cleanup, and timing variance;
- verify that additional workers do not starve or slow the serial tail through
  overlap/resource contention;
- consider whether weights should be refreshed periodically and define the
  controlled refresh procedure; and
- select a default worker ceiling based on repeated evidence, not CPU count
  alone.

## Slice 5 — authoritative whole-suite equivalence campaign

- Freeze the final candidate manifest and source identity.
- Run repeated one-worker and chosen multi-worker broad suites.
- Require identical test inventory and outcome inventory digests.
- Compare exact skipped/failure/error/unexpected-success identities.
- Inject a deterministic failure into each worker and retain exact reproduction
  commands.
- Prove all per-worker output roots are disjoint and release paths unchanged.
- Prove no provider, R2, Render, QA, production, or network activity occurred.
- Check for orphan subprocesses and Windows file-lock residue.
- Quantify absolute and percentage improvement against both the original serial
  baseline and the preceding conservative runner.

**Campaign paws-point 3:** approve or reject adopting the expanded
parallel-safe set and any new recommended worker profile. The underlying
manifest/coordinator remains the supported broad-confidence framework either
way.

## Slice 6 — workflow adoption and closeout

- Update the existing runner guide and release playbook with any changed
  parallel-safe set, recommended worker profile, and reproduction flow.
- Document how new modules enter provisional classification and how promotion
  evidence is reviewed.
- Document how timing weights are measured/refreshed without silently changing
  the frozen release gate.
- Update the relevant Control Room issue with timings, exclusions, and
  remaining bottlenecks.
- Run focused runner tests, `git diff --check`, and one final supported broad
  invocation.
- Close without a package release if only repository test/process tooling and
  tests changed. If installed package behavior or resources changed, stop and
  apply the normal release playbook under a fresh version.

## Miscellaneous architecture slice — distributed-growth manifest

This is a non-blocking follow-up slice. It may be completed during the campaign
when the manifest is already changing, or explicitly deferred with its design
recorded. It is not a prerequisite for the first duration-led promotions.

- Evolve the manifest beyond today's three execution classifications so it can
  describe future natal, synastry, transit, and production-path simulation
  suites without creating separate incompatible runners.
- Evaluate closed, validated metadata for:
  - product/pipeline ownership;
  - test tier (`unit`, `contract`, `integration`, `simulation`, `release`);
  - resource class (CPU, memory, disk I/O, subprocess, database, or artifact
    authority);
  - measured/estimated duration and measurement provenance;
  - required isolation capabilities;
  - protected logging/diagnostic posture;
  - serial-authority reason; and
  - eligible local and distributed execution profiles.
- Keep classification and safety semantics in the repository manifest while
  allowing GitHub Actions, Buildkite, or another future CI orchestrator to
  materialize balanced jobs across machines.
- Define at least two profiles driven from the same manifest:
  - a conservative local/laptop profile with a small worker ceiling; and
  - a distributed CI profile capable of producing more weighted shards.
- Preserve exact local reproduction for a remotely failed shard; a CI job ID or
  scheduler-specific partition must not become the only way to identify its
  tests.
- Keep expensive production-path simulations separately selectable for
  scheduled/nightly or pre-release campaigns rather than forcing them into
  every fast pull-request gate.
- Keep deterministic build, release receipt, and installed-artifact authority
  explicitly serial regardless of available CI capacity.
- Prefer a backward-compatible manifest migration with a closed schema and
  validator. Do not prematurely bind the repository contract to one CI vendor.

Deliverables if implemented:

- versioned manifest schema and migration;
- local and distributed execution-profile examples;
- deterministic shard-plan projection suitable for CI consumption;
- tests proving profile selection cannot override isolation or serial-authority
  restrictions; and
- a concise future CI integration handoff.

## Candidate disposition vocabulary

Each provisional module ends the campaign in exactly one class:

- `promoted_parallel_safe`: proven isolated and admitted to deterministic
  parallel execution;
- `retained_provisional`: promising but insufficiently proven or currently too
  expensive to repair;
- `serial_semantic`: serial execution is part of what the module proves;
- `serial_shared_authority`: build/release/database/global artifact authority
  must remain singular; or
- `deferred_low_value`: measured savings do not justify present work.

## Success criteria

- all provisional modules have measured durations and explicit dispositions;
- the highest-duration safe candidates are promoted first;
- promoted tests preserve exact behavior and failure sensitivity;
- repeated serial/parallel inventories and outcomes agree;
- broad wall time improves materially and repeatably;
- failures remain exactly reproducible;
- external systems remain untouched; and
- release authority remains serial and provenance-bound; and
- the manifest has a recorded path to pipeline-, tier-, and resource-aware
  distributed growth, whether implemented or explicitly deferred.
