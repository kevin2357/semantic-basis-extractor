# API review — Slice 0 causal reconstruction

## Decision

Approved: the incident has a sufficiently supported causal class to skip a
retained-R2 read for now and proceed to the deterministic concurrency
reproduction. The timestamped trace plus the historical 0.4.35 call path
establishes that whole-workspace validation was invoked from worker-local
`save_state()` while sibling pass-local work was legitimately changing that
workspace. This is the right focus for Slice 2.

## Corrections to carry forward

1. Replace **“It was not a corrupt restored checkpoint”** with a narrower
   statement: the available trace and source evidence identify a live
   validation-boundary race and do not implicate the restored predecessor
   checkpoint. Without inspecting retained bytes, they cannot categorically
   exclude every pre-existing workspace defect.

2. Replace **“pass 3's provider cost became durable, proving local adoption”**
   with “proving execution progressed into local reconciliation/accounting.” A
   reported-cost write may precede native truth adoption or successor
   publication; it must not be used as authority that a completed pass was
   durably adopted.

3. In Slice 2, preserve the actual historical relationship among the
   worker-thread `save_state()` reader, whole-workspace validator, and sibling
   request/response writes. A synthetic generic manifest race is useful only
   if it also demonstrates that real boundary. Compare against current main
   after `96980ab`, but do not label that removal a fix until parity,
   interruption, terminal-review preservation, and typed-exit behavior pass.

4. The correction contract must keep completed-but-unadopted provider evidence
   retrieval-only. A failure after retrieval cannot reopen provider creation;
   nor may a generic subprocess exit become the sole retry classifier.

## API boundary confirmation

The observed top-level `CalledProcessError` explains the API retry loop but is
not sufficient for API to choose an alternative native operation. The eventual
SBE public result/refusal must make safe replay versus review explicit. API will
consume that typed evidence and retain pending-provider custody rather than
infer native adoption from reported cost or traces.

Slice 0's no-R2 decision is approved. No provider, retained-run, deployment,
or release action is authorized by this review.
