# API review — Campaign paws-point 1 and semantic-closure refactor paws-point

## Verdict

**Approved** to proceed from the completed measurement work into Slice 1's
state-surface audit for a small, duration-led first promotion batch.

**Approved** to open a separate staged, test-only semantic-closure support
extraction/refactor, subject to the special constraints below. This approval is
for the serial-equivalence/support-extraction phase only. It is not approval to
split-and-promote in one move.

## What is aligned

1. The runner addition is correctly fenced. `--measure-class` selects from the
   existing manifest class without changing it; named-module selection rejects
   cross-class and duplicate requests. Calibration therefore cannot accidentally
   make a provisional module parallel-safe.
2. The empirical prioritization is compelling: the two leading provisional
   modules account for nearly half of provisional isolated duration, while the
   long tail contains many very-low-value candidates. Starting with the ranked
   high-value batch is preferable to lexical churn.
3. The measurement receipt distinguishes class, logging posture, outcome,
   counts, and duration. That is the right evidence for prioritization; it is
   explicitly not treated as isolation proof.
4. Slice 0A’s recommendation is appropriately restrained. The 98-case semantic
   closure atom is an ownership and scheduling problem worth addressing, but its
   shared compiled fixture, patching, persistence, subprocess, and concurrency
   surfaces make immediate parallelization the wrong first objective.
5. The proposed old-to-new identity bijection is essential. Aggregate test
   counts or a green exit status would not prove a safe split.

## Required fences for the semantic-closure support phase

- Keep the new support module non-discovered and test-only. Do not move
  production patch targets through aliases; tests must still patch the actual
  production symbols they are intended to exercise.
- Freeze the exact pre-split discovered identity/outcome inventory before the
  first move. Maintain the mapping incrementally in version control, including
  any intentional one-to-many or many-to-one restructuring explanation; reject
  an unexplained non-bijection.
- Treat the compiled packet as process-local, immutable fixture material only.
  No cross-process cache, persisted packet, or mutable globally shared fixture
  should be introduced in pursuit of faster scheduling.
- Start with the support extraction while the original test module remains
  serial and intact. Perform serial equivalence before moving a behavioral
  family, then repeat it after each cohesive family move. Batch,
  retry/persistence, and concurrency cases remain serial until their own
  collision evidence exists.

## Slice 1 advice

Audit the two dominant provisional modules first, but do not promise either is
promotable. For each, make the state-surface decision independently and retain
the candidate as provisional if its repair would obscure the behavior under
test. The first promotion batch should be deliberately small enough that a
whole-suite regression has an obvious owner and rollback.

No API/SBE lifecycle, provider, R2, Render, QA, release, or package work is
requested or approved by this review.
