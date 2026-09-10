# API Review — Slice 0

## Decision

Approved. The three-path framing is precise, supported by the frozen worker
trace, and does not need retained-checkpoint inspection to advance.

## Findings accepted

1. **Gutenberg is a detached terminal-review command-handoff gap**, not an
   unsealed-native-evidence or Better Stack transport failure. The invocation,
   result, and receipt are exact in the native trace, while the detached
   exit-3 path reached API without the closed terminal-review command result.
2. **Hypatia is an authority ordering and identity-preservation gap.** The
   first publication was attempted before same-invocation accepted-delivery
   authority was available, then the delivery-validation retry correctly
   avoided invented/latest-result discovery. That recovery is acceptable, but
   the initial retry is not a clean expected steady-state outcome.
3. A later delivery-validation pass is never an identity source. It may carry
   only an exact identity durably preserved from the original invocation.
4. No evidence presently points to the packet builder or Better Stack sink.
   Neither was reached with lawful identity.

## Slice 1 contract fence

- SBE may make the original invocation emit its closed terminal-review or
  terminal-delivery command handoff even when the ordinary detached exit-code
  convention remains in force. It must not change ordinary nonterminal
  detached exit-3 behavior.
- The handoff must bind the exact invocation, result, receipt, native run, and
  outcome. No latest-result discovery, filename inference, synthetic identity,
  or API-side reconstruction is permitted.
- API will consume that exact handoff to establish accepted-delivery authority
  before it calls publication, and preserve the same identity only for a
  subsequent delivery-validation retry if the first publication attempt cannot
  complete.
- The observer remains strictly post-authoritative-publication and best effort:
  a packet/capture failure cannot alter delivery, terminal review, custody,
  allocation, workspace cleanup, or spend.
- Provider-free regressions should cover both the corrected positive paths and
  genuinely missing/contradictory identity refusal. The latter must stay
  fail-closed with no capture attempt.

No R2 read, provider action, recovery, or retained-run mutation is approved or
needed for Slice 1.

