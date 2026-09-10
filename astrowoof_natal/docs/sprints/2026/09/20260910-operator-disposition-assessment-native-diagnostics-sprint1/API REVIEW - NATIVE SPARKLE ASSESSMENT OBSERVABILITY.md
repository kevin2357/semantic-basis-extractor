# API review — native sparkle assessment observability

Reviewed commit `4873213`.

## Decision

Approved with no release-blocking issue. The implementation adds three closed
structured SBE events for assessment start, safe workspace fingerprinting, and
assessment completion or phase-bounded failure. Reader behavior, authority,
I/O posture, exception propagation, and privacy remain unchanged.

## Pre-package follow-ups

1. Add one failure regression beyond initial snapshot mismatch to prove the
   phase-to-reason mapping at a later native boundary.
2. In the API installed-wheel gate, prove normal `force=False` in-process
   initialization alongside API stdout events. SBE's `force=True` coverage is
   sufficient for formatter correctness but does not establish host coexistence.

The reported diff-check findings are limited to trailing final blank lines in
sprint documents.
