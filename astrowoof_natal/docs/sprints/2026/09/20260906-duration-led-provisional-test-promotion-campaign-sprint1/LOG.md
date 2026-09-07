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
