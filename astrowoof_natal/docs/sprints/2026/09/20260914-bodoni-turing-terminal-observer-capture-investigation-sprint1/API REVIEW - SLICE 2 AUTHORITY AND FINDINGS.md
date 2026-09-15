# API review — Slice 2 authority and findings

## Read authority clarification

The owner separately confirmed that the one conditional HEAD and one bounded GET
per coordinate-pinned checkpoint were authorized. The Slice 2 acquisition is
therefore accepted as authorized and its stated R2-read budget is consumed. Do
not perform further R2 reads, listing, extraction, or retained-workspace work for
these witnesses without a new explicit owner grant.

## Technical assessment, separate from the authority defect

The reported exact-root result is highly informative:

- both retained checkpoints return a typed
  `unsupported / contradictory_native_evidence` status rather than an escaping
  local exception;
- the installed 0.4.61 export and relevant source copies are reported equal;
- the live call's `unavailable` cannot therefore be attributed, on this record,
  to ordinary packet construction or to a persistent defect in the retained
  checkpoint contents.

That leaves a live-only/API-boundary difference as the leading hypothesis:
call-time root/result/snapshot state, an earlier reader condition, or another
condition that disappears before the retained checkpoint is observed. It does
not justify changing SBE packet construction yet.

## Confirmed next owner action

API should correct the independently proven telemetry defect before another
live witness:

1. normalize the caught exception class to a lowercase reason token (for
   example `value_error`) before emitting it;
2. add a production-emitter regression that proves the failed capture phase is
   accepted by the event schema and sink; and
3. retain a content-free digest of the call-time root plus the normalized
   exception class and phase, so a future witness can distinguish root
   substitution/early-reader failure without logging a path, deck, prompt, or
   exception prose.

This is API-only observability work and has no Alloy/lifecycle semantic impact.
No SBE runtime correction or release is approved from Slice 2.
