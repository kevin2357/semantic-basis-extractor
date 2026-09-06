# Closeout — 0.4.36 correction disposition

## Decision

Close this investigation without another SBE runtime patch or release.

SBE 0.4.36 already contains the narrow correction for Kardamom's demonstrated
failure: `save_state()` no longer performs implicit sealed-result discovery by
calling the strict snapshot-bound native-result reader during ordinary native
mutation. The immutable-wheel comparison proves that 0.4.35 fails and 0.4.36
succeeds at that exact boundary.

The Slice 0 and Slice 2 tests remain valuable regression coverage and should be
committed with the investigation record. They characterize:

- equal-cardinality digest mutation versus added-path mutation;
- the historical worker-save/sibling-response race;
- serial/concurrent local fan-in semantic parity;
- two-completed/two-pending mixed custody;
- zero provider transport during durable-response adoption;
- valid successor snapshot publication; and
- immutable predecessor review-result continuity.

## Public behavior

This closeout does not add or reinterpret lifecycle authority. Logs remain
sanitized diagnostic evidence. Native results, receipts, lifecycle inspection,
and checkpoint/snapshot contracts remain authoritative.

If this class recurs, SBE 0.4.36 trace summaries should expose the workspace
identity, selected command/branch, native mutation/publication state, and CLI
exit without requiring an immediate retained-workspace download.

## Deferred work

The broader quarantine/interruption contract is intentionally not folded into
this sprint. It belongs to the already-following sprint and must not be treated
as a release condition for this investigation closeout.

Likewise, this record does not authorize a deployment, retained-run resume,
provider call, R2 read, tag, or release.
