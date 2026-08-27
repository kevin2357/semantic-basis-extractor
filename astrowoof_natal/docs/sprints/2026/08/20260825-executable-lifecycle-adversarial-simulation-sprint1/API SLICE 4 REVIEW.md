# API Slice 4 Review — Systematic Branch Explorer

## Assessment

The action/binding projection corrects the exact issue from the Slice 3 review.
It is closed, redacted, deterministically ordered, and distinguishes a first create
for an unentered member from a second create for the same action/binding. The
two-order partial-wave deduplication and shortest one-event witnesses are also the
right initial systematic cells. The documentation accurately limits the member wave
to an abstract redacted authority model rather than claiming it mutates a real
native workspace.

Two small corrections are needed before the Slice 4 gate is complete.

## Required corrections

1. **Exercise clock equivalence; do not compare precomputed instants.**
   `run_systematic_explorer_qualification()` currently calculates one timestamp by
   adding 300 seconds and compares it to a literal `12:05:00Z`. That proves Python
   arithmetic, not equivalence between the explorer's repeated base-unit transition
   and its accelerated-next-boundary transition. Please add a tiny closed clock
   state/transition helper and a regression that applies 300 actual one-unit events
   on one branch and one actual accelerate-to-boundary event on the other, then
   compares the canonical successor/fingerprint.

2. **Make the receipt validator enforce its own bounds.**
   The runner rejects depths outside 2–8, but
   `validate_systematic_explorer_qualification()` currently accepts a receipt with
   any nonnegative integer depth. A serialized/public receipt must independently
   enforce the same bounded campaign contract.

These are local provider-free corrections. Once present, I approve this Slice 4
foundation; later SBE/API joined adapters can remain separate work rather than
forcing this qualification model to impersonate production scheduling.
