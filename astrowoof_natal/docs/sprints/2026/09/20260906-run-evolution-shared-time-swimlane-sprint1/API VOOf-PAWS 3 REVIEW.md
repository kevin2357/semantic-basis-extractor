# API Voof-paws 3 review — interval reducer

## Decision

The ownership framing and the Slice 2 pairing rules are sound, including the
new evidence-family clock fence and chronological handoff ordering. However,
please correct the following two closed-contract mismatches before proceeding
to the renderer.

## Required implementation corrections

1. **Root shape mismatch:** `build_run_cohort_timeline()` emits
   `adapter_coverage`, but `validate_run_cohort_timeline()` still declares the
   root as an exact closed key set without `adapter_coverage`. Either add it to
   the v1 schema, Python validator, docs, digest fixture, and tests as a fully
   defined diagnostic coverage object, or remove it from the emitted body.
   Do not leave a builder that can only produce a value rejected by its own
   reader.

2. **Interval classification mismatch:** the lease pair is emitted as
   `observed_execution_allocation`, but that value is absent from
   `INTERVAL_CLASSIFICATIONS` and the v1 schema. Slice 0 deliberately calls
   this an *observed execution-allocation/lease window* while keeping it out of
   global slot authority. Please add the exact classification consistently to
   contract/schema/docs/tests, or emit one of the already closed classes with
   the same conservative label. The former seems clearer, provided it remains
   explicitly observed/non-global.

## Required proof

Add a reducer test containing a paired `worker.lease.acquired` /
`worker.lease.released` sequence and nonzero adapter coverage, then validate
the built artifact through the public reader/validator. The current focused
tests appear not to exercise both emitted shapes together.

After those corrections and that end-to-end proof, API approves the reducer and
the sprint can advance to the interactive renderer. No runtime, provider,
workspace, or API mutation is implicated.
