# Log — duration-led provisional test promotion campaign

## 2026-09-06 — campaign initialized

- Created a separate campaign rather than expanding the active runner
  qualification sprint.
- Established duration-led review priority with isolation still requiring
  independent proof.
- Preserved test semantics, protected observability, provider-free execution,
  deterministic receipts, and serial release authority as hard boundaries.
- Planned an evidence-dependent number of small promotion batches rather than
  promising that all provisional modules will become parallel-safe.
- Added a non-blocking architecture slice for evolving the manifest into a
  pipeline-, tier-, resource-, and execution-profile-aware source of truth for
  both conservative local execution and future distributed CI. The runner's
  project-specific isolation semantics remain authoritative; a future CI
  platform supplies capacity and orchestration rather than replacing them.

## 2026-09-07 — baseline refreshed after framework adoption

- Bound the campaign to framework commit `d9129f6` and its final green
  1,118-test default-profile receipt.
- Clarified that the campaign is choosing a larger parallel-safe set and future
  worker profile, not reconsidering the already-adopted runner framework.
- Made the Slice 0 calibration change explicit because the current
  `--measure-weights` mode intentionally measures only `parallel_safe` modules.
- Added Slice 0A to evaluate whether decomposing the unusually large
  serial-only `test_semantic_closure.py` scheduling atom is worth a larger
  test-only refactor. Implementation requires a separate paws-point; all other
  candidates retain the small/easy-refactor boundary.

## 2026-09-07 — Slice 0 provisional inventory

- Extended the existing calibration interface with a closed measurement class
  and named-module selector. Measurement does not modify classification or
  admit provisional/serial modules to parallel execution.
- Added focused coverage for provisional selection, cross-class refusal, and
  duplicate named-module refusal. Focused runner suite: 15 passed.
- Measured all 55 provisional modules independently: all passed, with 520.768
  seconds of summed isolated duration.
- Confirmed a steep Pareto distribution: two modules account for 46.1%, ten
  account for 80.4%, and 20 finish in under one second.
- Repeated the two dominant outliers. `test_bounded_lifecycle.py` measured
  121.750, 122.434, and 144.843 seconds (median 122.434); the Waffle/Scone
  finalization witness measured 117.633, 122.645, and 146.773 seconds (median
  122.645).
- Made no manifest classification or test-behavior change.

## 2026-09-07 — Slice 0A semantic-closure feasibility

- Mapped the serial-only semantic-closure module: 98 discovered test methods
  across seven broad behavioral families, with extensive temporary workspace,
  patching, provider-fake, Batch, snapshot, persistence, and concurrency
  surfaces.
- Three isolated measurements passed at 213.529, 192.970, and 215.110 seconds
  (median 213.529; range 22.141), making this one module approximately 19.0%
  of the frozen supported broad-suite wall time.
- Measured all 36 serial-only modules independently: all passed, totaling
  448.964 seconds. Semantic closure alone represented 47.9% of that measured
  serial-only tail.
- Identified its shared compiled packet fixture and identity-migration burden
  as the principal decomposition risks.
- Recommended a dedicated two-phase test-only refactor: first extract stable
  support and prove serial equivalence, then split cohesive modules while
  retaining global/concurrency cases as serial until independently qualified.
- Explicitly rejected combining decomposition and immediate parallel promotion.
- Paused before any support extraction, file split, test rename, or promotion.

## 2026-09-07 — paws-point review and Slice 1 audit

- Ingested API's paws-point approval and retained its exact fences: support
  stays non-discovered/test-only, production patch targets stay direct, the
  compiled packet remains process-local/immutable, and identity equivalence is
  proven incrementally before any family move.
- Audited the two dominant provisional modules independently.
- Found `test_bounded_lifecycle.py` likely process-isolated already: all writes
  use owned temporary roots, provider surfaces are fake, and its internal
  concurrency is behavior under test. Advanced it to collision qualification
  without proposing a repair.
- Found the Waffle/Scone finalization witness filesystem-isolated but highly
  resource-intensive. Advanced it to collision/contention qualification while
  withholding any promotion decision.
- Defined self-collision, imported-helper-neighbor, semantic-closure-neighbor,
  and resource-heavy-neighbor probes with exact outcome and residue checks.
- Kept both modules provisional and paused before Slice 2.

## 2026-09-07 — Slice 1A support extraction

- Added the explicitly planned Slice 1A implementation phase under API's
  approved serial-equivalence fences.
- Froze all 98 pre-extraction semantic-closure test identities and the empty
  adverse-outcome inventory in a checked-in JSON document.
- Extracted the shared process-local compiled-packet fixture, response builders,
  and scripted transport to non-discovered `_semantic_closure_support.py`.
- Updated all direct consumers to import the support module rather than loading
  the giant discovered test module for fixtures.
- Preserved all 98 semantic-closure test locations and identities; production
  patch targets remain direct.
- Exact post-extraction serial run: 98 passed, with matching identity SHA
  `09e21d...7ed8` and outcome SHA `36f64a...0c97`.
- Strengthened the fixture from a mutable class packet to one process-local
  compiled template plus a fresh deep copy owned by every test, then repeated
  the exact 98-test proof successfully.
- The direct-consumer quiet probe ran 70 tests with one known logging-posture
  failure and no errors; its logging-sensitive module then passed all 11 tests
  in the required unquiet posture.
- Final supported-posture consumer pair: 59 quiet tests passed and 11 unquiet
  tests passed in separate concurrent worker processes.
- Added a permanent runner regression protecting non-discovery and direct
  support imports.
- Final focused runner/support guard: 16 passed; identity inventory JSON
  validated; Python compilation and diff hygiene passed.
- Paused before any family move, test rename, parallel promotion, or Slice 2
  collision work.

## 2026-09-07 — Slice 2 collision and promotion batch

- Incorporated API's Slice 1A approval and preserved its explicit limit: no
  semantic-closure move, rename, or promotion.
- Bounded lifecycle passed three self-collisions, imported-helper neighbors, an
  existing heavy parallel neighbor, and the Waffle/Scone pairing.
- Waffle/Scone passed three self-collisions, the full semantic-closure neighbor,
  and a qualification-heavy provisional neighbor.
- Recorded the owner policy that correctness/isolation controls promotion;
  modest or noisy current-laptop timing regressions do not independently veto
  a safe module. Waffle/Scone showed resource contention but no instability.
- Promoted both candidates, changing manifest counts from 38/55/36 to
  40/53/36.
- Ran two complete promoted two-worker parallel groups concurrently as a
  four-process stress case. Both passed 281 tests with 40 skips and identical
  identity/outcome digests.
- Focused runner/support guard suite passed 16 tests.

## 2026-09-07 — Slice 3 promotion batch 2

- Selected the next three remaining duration leaders: happy-path QA,
  adversarial QA, and legacy local-work upgrade QA.
- Audited their temporary paths, process-local receipt, child CLI, environment,
  provider, repository-write, database, and port surfaces. No repair was needed.
- Ran three six-process collision repetitions comprising two copies of every
  candidate. All 60 aggregate test executions passed with six expected
  optional-schema skips across the three repetitions.
- Promoted all three candidates; manifest counts moved from 40/53/36 to
  43/50/36.
- Two concurrent actual-manifest two-worker runs both passed 301 tests with 42
  skips and exact matching identity/outcome digests.
- Paused before selecting the next composed-runtime/qualification cohort.

## 2026-09-07 — Slice 3 promotion batch 3 audit

- Incorporated API's approval of promotion batch 2.
- Selected the next three duration leaders, representing 56.832 seconds of the
  original provisional tail.
- Audited temporary paths, package-resource reads, provider fakes/fences,
  scoped patches, per-test locks, process-local semantic fixture ownership, and
  discovered-test helper imports.
- Found no ambient environment/cwd, repository write, database, port, real
  provider, or uncontrolled subprocess surface.
- Advanced all three to collision qualification without changing production
  code, test behavior, or manifest classification.
- Paused before collision and promotion as required by the Batch 2 review's
  no-blanket-promotion boundary.

## 2026-09-07 — Slice 3 promotion batch 3 qualification

- Received owner approval to proceed from audit through collision and promotion
  and pause at the combined review point.
- Ran three repetitions containing two independent copies of all three
  candidates. All 18 workers passed with exact expected skip posture.
- Promoted all three modules without test or production changes; manifest moved
  from 43/50/36 to 46/47/36.
- Repeated the promoted actual-manifest stress proof twice concurrently. Both
  runs passed 324 tests with 43 skips and matching identity/outcome digests.
- Four-process critical-path time remained approximately 275.3 seconds despite
  adding 23 tests to the parallel group.
- Paused at the requested combined voof-paws.

## 2026-09-07 — Slice 3 promotion batch 4 audit

- Incorporated API's approval of promotion batch 3.
- Selected and audited the next three duration leaders, totaling 44.448 frozen
  isolated seconds.
- Confirmed temporary-root ownership, local provider callables, unique copied
  workspace paths, byte-level refusal nonmutation, and absence of uncontrolled
  environment/repository/database/port/logger/subprocess state.
- Recorded test-helper inheritance as maintenance debt contained by process
  isolation; no pre-collision refactor is justified.
- Advanced the cohort to collision qualification without changing the manifest.

## 2026-09-07 — Slice 3 promotion batch 4 collision qualification

- Incorporated API's audit approval, which authorized collision testing but
  explicitly withheld promotion.
- Ran three repetitions with two independent copies of all three candidates.
  All 18 workers passed with no skips, failures, or errors.
- Preserved byte-exact unsupported-route nonmutation and exact v2 local
  provider-call inventories.
- Observed modest shared resource contention without correctness, isolation, or
  cleanup instability.
- Left the manifest unchanged at 46/47/36 and paused for the separate promotion
  decision before actual-manifest stress testing.

## 2026-09-07 — Slice 3 promotion batch 4 completion

- Incorporated API and owner promotion approval and corrected the stale
  five-versus-eight cumulative promotion count.
- Promoted the three qualified modules with their frozen isolated weights;
  manifest moved from 46/47/36 to 49/44/36.
- Ran two concurrent actual-manifest two-worker stress groups. Both passed 340
  tests with 43 skips and exact matching identity/outcome digests.
- Recorded the approximately 16.5-second critical-path increase as calibration
  evidence, not a correctness failure or an inflated speedup claim.
- Paused before Batch 5 selection.

## 2026-09-07 — Slice 3 promotion batch 5 state-surface audit

- Selected the next three remaining frozen-duration leaders, totaling 22.887
  isolated seconds and 14 tests.
- Audited owned temporary roots, subprocess environment inheritance,
  process-local tracing, helper imports, local provider callables, and the
  intentional same-workspace native writer-lock contention test.
- Found no uncontrolled shared output, repository mutation, cwd, database,
  port, network, or provider-I/O surface and proposed no pre-collision repair.
- Left the manifest unchanged at 49/44/36 and paused for approval before the
  bounded Batch 5 collision matrix.

## 2026-09-07 — Slice 3 promotion batch 5 collision qualification

- Incorporated API approval for collision testing without treating it as
  promotion authority.
- The laptop restart interrupted the first attempt before any receipt existed.
- Detected and stopped one invalid invocation that selected complete-suite mode
  rather than the named modules; it produced no receipts and is excluded.
- Reran cleanly through the supported secret-scrubbed per-module measurement
  route: three repetitions, two copies of each candidate, 18/18 workers green.
- Exact per-copy inventories remained external-authority 3/1, bounded-product
  7/0, and terminal interruption 4/0 (tests/skips), with no failures/errors.
- Preserved the manifest at 49/44/36 and paused for the separate promotion
  decision before any actual-manifest stress run.

## 2026-09-08 — Slice 3 promotion batch 5 completion

- Incorporated the clean 18-worker collision receipt and API/owner approval to
  promote exactly the three Batch 5 modules.
- Promoted the modules with frozen isolated weights. The campaign-basis
  projection moved from 49/44/36 to 52/41/36; the live shared manifest is
  52/44/36 because three concurrent editorial-contract modules entered
  `provisional`.
- Runner manifest/inventory regression tests passed: 16 tests.
- Ran two complete two-worker `parallel_only` groups concurrently. Both passed
  354 tests with 44 expected skips, empty stderr, and exact matching test,
  outcome, and manifest digests.
- Recorded 424.409- and 420.131-second wall times candidly as contention and
  calibration evidence, without claiming current-host whole-suite speedup.
- Paused before Batch 6 selection.

## 2026-09-08 — Slice 3 promotion batch 6 state-surface audit

- Incorporated API's Batch 5 completion approval and selected the next three
  frozen-duration leaders (16.254 seconds, 36 tests).
- Found the Batch negative-authorization and v2 intent-fence modules suitably
  isolated for bounded collision qualification, including their intentional
  workspace-local contention and provider-call-entry assertions.
- Did not advance the historical duplicate-submission investigation witness:
  it deliberately proves the old two-creates failure and needs an explicit
  retain/archive/replacement decision before the campaign treats its runtime
  cost as an enduring regression.
- Left the live manifest at 52/44/36 and paused before collision testing or any
  test-identity change.

## 2026-09-09 — Slice 3 promotion batch 6 collision qualification

- Preserved the historical duplicate-submission witness as provisional and ran
  collision qualification only for the two clean audit candidates.
- Ran three repetitions with two copies of each module: 12/12 worker receipts
  passed with empty stderr, no failures/errors, and exact 18/0 and 17/0
  test/skip inventories.
- Observed worker ranges of 8.250–9.744 seconds for Batch negative authorization
  and 7.360–10.593 seconds for the v2 intent fence.
- Left the live manifest at 52/44/36 and paused for separate promotion and
  historical-witness disposition decisions.

## 2026-09-09 — Slice 3 promotion batch 6 completion

- Incorporated API/owner approval to promote the two collision-qualified
  modules and archive the obsolete duplicate-submission reproducer.
- Preserved the historical source with provenance beside its incident sprint,
  removed its `test_*.py` discovery surface, and removed it from the manifest.
- Promoted the two qualified modules; the live manifest moved from 52/44/36 to
  54/41/36. Runner manifest/inventory regressions passed: 16 tests.
- Ran two concurrent complete two-worker `parallel_only` groups. Both passed
  389 tests with 44 expected skips, empty stderr, and exact matching test,
  outcome, and manifest digests.
- Recorded 384.030- and 383.823-second wall times without inferring a whole-suite
  speedup.
- Paused before Batch 7 selection.

## 2026-09-09 — Slice 3 promotion batch 7 state-surface audit

- Selected the next three frozen-duration leaders: SBE v0.3, negative
  authorization, and operator retirement (12.942 seconds, 98 tests, two skips).
- Audited class fixtures, read-only examples/resources, temporary output roots,
  child Python invocations, native locks, thread coordination, event sinks, and
  failure injection.
- Kept the single-action stale-seam test as meaningful fail-closed negative
  coverage: it proves no second mutation/provider action while Batch coverage
  proves the current atomic route.
- Found no uncontrolled shared or external state and proposed no pre-collision
  refactor.
- Left the live manifest at 54/41/36 and paused before the Batch 7 collision
  matrix.

## 2026-09-09 — Slice 3 promotion batch 7 collision qualification

- Ran the approved matrix: three repetitions with two copies of all three
  candidates, for 18/18 successful worker receipts.
- Preserved exact inventories of 52/0, 20/0, and 26/2 tests/skips with no
  failures, errors, or stderr.
- Observed narrow worker-duration ranges even under six-process contention:
  4.907–5.787, 4.570–5.973, and 4.408–5.923 seconds respectively.
- Left the live manifest unchanged at 54/41/36 and paused for the separate
  promotion decision before actual-manifest stress testing.

## 2026-09-09 — Slice 3 promotion batch 7 completion

- Incorporated API/owner approval to promote exactly the three Batch 7 modules.
- The first runner inventory check caught concurrently added
  `test_editorial_review_runtime.py`; classified it conservatively as
  provisional, then passed all 16 manifest/inventory regressions.
- Promoted the qualified modules; the live manifest moved from 54/42/36 after
  intake to 57/39/36.
- Ran two concurrent complete two-worker `parallel_only` groups. Both passed
  487 tests with 46 expected skips, empty stderr, and exact matching test,
  outcome, and manifest digests.
- Recorded 339.997- and 340.000-second wall times without inferring a whole-suite
  speedup.
- Paused before Batch 8 selection.

## 2026-09-09 — adaptive batching decision

- Owner approved scaling later Slice 3 cohorts according to duration and state
  risk rather than processing every remaining provisional module three at a
  time.
- Retained small cohorts for expensive/stateful modules, allowed larger cohorts
  for simple sub-second modules, and capped physical collision concurrency at a
  host-appropriate level through controlled waves.
- Required concurrent-sprint test modules to enter provisional immediately and
  deferred their family-level measurement/audit until the owning sprint freezes
  its test set.
- Confirmed that an honest provisional tail is acceptable when qualification
  cost exceeds likely scheduling value.

## 2026-09-09 — Slice 3 promotion batch 8 state-surface audit

- Selected the next four medium-duration frozen leaders under the adaptive
  batching policy: post-fan-in retry runtime, payload recovery,
  operator-disposition packaging, and lifecycle consumer.
- Audited 15 tests representing 12.042 frozen seconds across temporary native
  workspaces, process-global CLI patches, provider-free injected callbacks,
  packaged resources, and nested fresh-process public CLI checks.
- Confirmed child processes inherit the campaign harness's secret-scrubbed
  environment and all mutable paths remain caller-owned temporary roots.
- Found no uncontrolled shared or external state and proposed no pre-collision
  refactor.
- Left the live manifest at 57/39/36 and paused before the Batch 8 collision
  matrix and its separate promotion decision.

## 2026-09-09 — Slice 3 promotion batch 8 collision qualification

- Incorporated API approval for exactly the four audited modules without
  treating collision approval as manifest-promotion authority.
- Ran three repetitions of two independent copies per module in controlled
  waves capped at six workers: all 24 receipts passed.
- Preserved exact per-copy outcomes of 5/0, 2/0, 4/0, and 4/0 tests/skips with
  no failures, errors, expected failures, unexpected successes, or coordinator
  stderr.
- Observed compact collision duration ranges of 3.27–3.53, 2.42–2.53,
  2.61–2.82, and 2.38–2.51 seconds.
- Left the manifest unchanged at 57/39/36 and paused for the separate Batch 8
  promotion decision before actual-manifest stress testing.

## 2026-09-09 — Slice 3 promotion batch 8 completion

- Incorporated API approval to promote exactly the four collision-qualified
  Batch 8 modules.
- Moved only those modules from `provisional` to `parallel_safe`; the live
  manifest moved from 57/39/36 to 61/35/36.
- Passed all 16 runner and exact manifest-inventory regressions.
- Ran two concurrent complete two-worker `parallel_only` groups. Both passed
  502 tests with 46 expected skips and matching test, outcome, and manifest
  digests.
- Recorded 345.942- and 345.803-second wall times without inferring a
  whole-suite speedup.
- Removed temporary stress work roots after extracting the bound receipt facts
  and paused before Batch 9 selection.

## 2026-09-09 — Slice 3 promotion batch 9 state-surface audit

- Selected five compact-duration leaders under the adaptive batching policy:
  review-required pending retries, spend enforcement, external-authority empty
  inventory, lifecycle closeout, and checkpoint repair.
- Audited 53 tests representing 7.924 frozen seconds across owned native
  workspaces, workspace-local locks, injected provider transports, logger/event
  sinks, interruption recovery, and exact backup/apply behavior.
- Confirmed provider cases are transport-doubled or stop before transport and
  that global patches/log capture restore within process-local contexts.
- Found no uncontrolled shared or external state and proposed no pre-collision
  refactor.
- Left the live manifest at 61/35/36 and paused before the Batch 9 collision
  matrix and its separate promotion decision.

## 2026-09-09 — Slice 3 promotion batch 9 collision qualification

- Incorporated API approval for exactly the five audited Batch 9 modules
  without treating collision approval as manifest-promotion authority.
- Ran three repetitions of two independent copies per module in controlled
  waves capped at six workers: all 30 receipts passed.
- Preserved exact per-copy outcomes of 4/0, 18/0, 13/0, 10/0, and 8/0
  tests/skips with no failure, error, or unexpected outcome.
- Observed compact duration ranges of 2.12–2.36, 1.67–1.94, 1.60–1.74,
  1.67–1.72, and 1.42–1.55 seconds.
- Left the manifest unchanged at 61/35/36 and paused for the separate Batch 9
  promotion decision before actual-manifest stress testing.

## 2026-09-09 — Slice 3 promotion batch 9 completion

- Incorporated API approval to promote exactly the five collision-qualified
  Batch 9 modules.
- Moved only those modules from `provisional` to `parallel_safe`; the live
  manifest moved from 61/35/36 to 66/30/36.
- Passed all 16 runner and exact manifest-inventory regressions.
- Ran two concurrent complete two-worker `parallel_only` groups. Both passed
  555 tests with 46 expected skips and matching test, outcome, and manifest
  digests.
- Recorded 337.400- and 337.245-second wall times without inferring a
  whole-suite speedup.
- Removed temporary stress work roots after extracting the bound receipt facts
  and paused before Batch 10 selection.

## 2026-09-09 — Slice 3 promotion batch 10 state-surface audit

- Selected six roughly one-second frozen leaders under the adaptive batching
  policy.
- Advanced five modules totaling 5.549 frozen seconds and 26 tests to the
  collision-review boundary after auditing temporary roots, restoring patches,
  helper imports, injected retrieval, and provider-free qualification.
- Held `test_post_fan_in_retry_matrix_slice0.py`: one test still characterizes
  legacy v0.5 no-progress republication as success, while its fixture helper and
  other compatibility/precedence tests remain useful.
- Requested review of surgical archival/extraction for that single obsolete
  witness instead of treating process isolation as sufficient for promotion.
- Left the live manifest at 66/30/36 and made no production/package or
  semantic-closure change.

## 2026-09-09 — Slice 3 promotion batch 10 witness archival and collision

- Incorporated API direction to archive only the obsolete v0.5 no-progress
  republication method while retaining the active module's helper and three
  live regressions.
- Preserved the exact method and provenance as a non-discoverable `.py.txt`
  artifact beside the original 2026-08-25 incident; the remaining three tests
  passed directly after extraction.
- Ran three two-copy repetitions for each of the five collision-approved
  modules in waves capped at six workers; all 30 receipts passed with exact
  12/0, 1/0, 6/0, 3/0, and 4/1 test/skip inventories.
- Recorded no failure, error, unexpected outcome, coordinator stderr, or
  persisted failure log.
- Left the live manifest at 66/30/36 and paused before the separate Batch 10
  promotion decision.

## 2026-09-09 — Slice 3 promotion batch 10 completion

- Incorporated API approval to promote exactly the five collision-qualified
  Batch 10 modules while retaining the extracted three-test Slice 0 module in
  provisional.
- Moved only those five rows; the live manifest moved from 66/30/36 to
  71/25/36 and all 16 runner/inventory guards passed.
- Ran two concurrent complete two-worker `parallel_only` groups. The existing
  child coordinators continued through a conversation/app interruption without
  restart or duplicate execution.
- Both passed 581 tests with 47 expected skips and matching test, outcome, and
  manifest digests; every shard was clean.
- Recorded 376.533- and 376.562-second wall times without inferring a
  whole-suite speedup.
- Removed generated stress work roots after extracting receipt facts and paused
  before Batch 11 selection.

## 2026-09-09 — Slice 3 promotion batch 11 state-surface audit

- Selected seven compact-duration leaders under the adaptive batching policy,
  totaling 5.034 frozen seconds, 44 tests, and two expected skips.
- Audited temporary-root workspace ownership, restoring argument/log patches,
  immutable package and example reads, fixture-helper imports, workspace-local
  locks, and explicit observation-time inputs.
- Confirmed the provider-reconciliation Slice 0 module's active tests freeze the
  corrected custody-precedence behavior rather than requiring the historical
  defect to survive.
- Found no uncontrolled shared or external state and proposed no pre-collision
  refactor or archival.
- Left the live manifest at 71/25/36 and paused before the Batch 11 collision
  matrix and its separate promotion decision.

## 2026-09-09 — Slice 3 promotion batch 11 collision qualification

- Incorporated API approval for exactly the seven audited Batch 11 modules
  without treating collision approval as manifest-promotion authority.
- Ran three repetitions of two independent copies per module in controlled
  waves capped at six child workers; all 42 receipts passed.
- Preserved exact per-copy outcomes of 5/0, 4/0, 9/1, 5/1, 9/0, 5/0, and 7/0
  tests/skips with no failure, error, or unexpected outcome.
- Every child exited zero, every coordinator stderr file was empty, and no
  persisted failure log or external activity appeared.
- Left the manifest unchanged at 71/25/36 and paused for the separate Batch 11
  promotion decision before actual-manifest stress testing.

## 2026-09-09 — Slice 3 promotion batch 11 completion and sprint split

- Incorporated API and owner approval to promote exactly seven Batch 11
  modules; live manifest moved from 71/25/36 to 78/18/36.
- Passed all 16 runner and exact manifest-inventory regressions.
- Ran two concurrent complete two-worker `parallel_only` coordinators; both
  passed 625 tests with 49 expected skips and matching test, outcome, and
  manifest digests, with empty stderr.
- Recorded 353.781- and 353.749-second wall times without inferring laptop
  speedup.
- Transferred the 18-module provisional tail and all remaining calibration,
  equivalence, architecture, and workflow work to the 20260909 Sprint 2.
- Closed this sprint at Batch 11 without selecting or beginning Batch 12.
