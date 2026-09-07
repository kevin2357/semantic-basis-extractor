# Slice 0A — semantic-closure decomposition feasibility

## Executive finding

`test_semantic_closure.py` is a plausible decomposition candidate for
maintainability and eventual scheduling flexibility, but it is not a safe
“rename a few files” optimization. It contains 98 discovered `unittest` test
methods (plus a module-level helper whose name begins with `test_`) across
roughly 4,500 lines and 196 KiB. It shares an expensive class-level compiled
packet, imports and patches a broad production surface, and deliberately tests
threading, atomic persistence, snapshots, subprocess behavior, and concurrent
resume.

Recommendation: **approve a separate staged test-only decomposition**, but do
not implement it inside the ordinary provisional-promotion batches. First
extract stable support code and prove identity/outcome equivalence while the
module remains serial; only then evaluate selected child modules for parallel
promotion. The concurrency/persistence tail should remain serial unless its
isolation is independently proven.

## Current scheduling shape

- manifest class: `serial_only`
- scheduler granularity: one module / one indivisible scheduling atom
- discovered methods: 98
- shared class fixture: `SemanticClosureFixture.setUpClass`
- shared fixture work: package discovery, context validation, candidate
  construction, optimization, and packet compilation once per importing
  process
- local workspace posture: 79 `TemporaryDirectory` references
- mutation/concurrency indicators: 27 patch calls, 6 threading references,
  3 subprocess references, 2 explicit sleeps, environment mutation references,
  and module import-time `sys.path` mutation

Three independent measurements passed at 213.529, 192.970, and 215.110 seconds
(median 213.529; range 22.141). The median is 19.0% of the frozen
1,122.983-second supported broad-suite wall time by itself. The complete
serial-only inventory totaled 448.964 seconds in isolated measurements, so the
module represented 47.9% of that measured tail in the complete pass.

## Test-family map

| Family | Approx. methods | Current line region | Main surfaces |
|---|---:|---:|---|
| authority and reconciliation | 10 | 524–1132 | spend authorization, initial wave, resume, exact/bounded reconciliation |
| contracts and context shaping | 8 | 1133–1342 | schemas, compact basis, context repair, validation |
| polish/critic/candidate | 18 | 1343–2364 | qualitative transports, sparse edits, retries, persisted subject state |
| finalization and delivery | 4 | 2365–2514 | terminal outcomes, packaging, token-free deck assembly |
| provider transport/accounting | 23 | 2515–3370 | response reconstruction, polling, usage, cache, routing, costs |
| Batch | 17 | 3371–3978 | archive discovery, submission, detach/resume, reconciliation, cost |
| retry/persistence/concurrency | 18 | 3979–4519 | retries, resume, snapshot integrity, checkpointing, cleanup, atomic writes |

These are review boundaries, not yet proposed filenames. Several tests cross
family boundaries and must be placed according to the authority/invariant they
prove rather than their nearest helper call.

## Shared-state and discovery risks

1. Splitting the module repeats `setUpClass` packet construction once per
   process unless the support design deliberately shares it. A fragile global
   cache could make ordering matter and would be worse than the current file.
2. `unittest` identities will change when methods move. Aggregate count parity
   is insufficient; the refactor needs an explicit old-to-new identity map and
   exact outcome comparison.
3. Patch targets must remain production symbols, not silently migrate to
   support-module aliases that stop testing the intended boundary.
4. Atomic-write, file-lock, snapshot-consistency, and concurrent-resume cases
   express genuinely global behavior and are poor early parallel candidates.
5. Module import currently adjusts `sys.path`. Support extraction should remove
   that incidental coupling through ordinary package imports rather than copy
   it into every child file.
6. Provider fakes and fixture builders are good support-module candidates only
   if they remain deterministic, immutable by default, and return owned state
   per test.

## Viable boundary design

If approved, use a two-step refactor:

1. Create a non-discovered support module for provider fakes, immutable fixture
   builders, and packet construction. Preserve production patch targets and
   return fresh/deep-copied mutable state. Keep all tests in the original module
   until focused and full serial equivalence is green.
2. Move cohesive families into separately classified test modules. Begin with
   contract/context and provider-accounting cases; keep Batch and
   retry/persistence/concurrency serial initially. Measure fixture duplication
   before attempting any parallel promotion.

A process-local lazily built immutable packet may be reasonable because the
runner loads multiple modules into one worker process, but it must not become a
cross-process cache or persisted build artifact. Each process must be able to
construct and validate its own authority-free fixture.

## Option comparison

| Option | Benefit | Risk/effort | Recommendation |
|---|---|---|---|
| Keep intact and serial | zero migration risk | preserves a major indivisible tail and difficult ownership | acceptable fallback, not preferred long term |
| Split, keep children serial | much better ownership, reviewability, failure localization; enables later timing | medium test-only refactor; identity migration and fixture reuse require care | preferred first implementation phase |
| Split and immediately parallelize children | potential wall-time gain | high attribution risk; duplicated setup and hidden shared state may erase benefit | do not combine with initial split |

## Required equivalence proof

- freeze all 98 current discovered test IDs and outcomes;
- publish an explicit old-ID to new-ID mapping for every moved case;
- require a bijection: no dropped, duplicated, or newly unaccounted case;
- run intact-before and split-after serial executions from pinned source states;
- compare pass/skip/failure/error/unexpected-success identities after applying
  the declared mapping;
- prove package/resource/build outputs are unchanged;
- run representative support-fixture cases in isolation and randomized module
  order; and
- only after serial equivalence, run collision probes for any proposed
  parallel child.

## Go/no-go

**GO for a dedicated, staged test-only refactor after reviewer/owner approval.**
The module is too broad to remain a healthy permanent ownership boundary, and a
careful split creates future scheduling options. **NO-GO for implementing the
split during the current ordinary promotion batch or for promising immediate
parallel speedup.** Maintainability is the first justified payoff; parallelism
must earn separate evidence afterward.

This is the special refactor paws-point. No files or test identities should be
moved until it is explicitly approved.
