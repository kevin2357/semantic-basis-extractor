# API review — investigation plan

## Decision

Approved to begin **Slice 0 only**. The plan correctly treats this as a native
shared-workspace/concurrent-local-adoption investigation, not as a provider
latency or API scheduling issue. Its staged approach—prove the writer and
inventory delta first, then choose the narrowest correction—is the right one.

The API review is based on the unfiltered QA worker export at
`C:\tmp\sbe_worker_logs.txt` and the frozen Kardamom timeline in
`Background.md`.

## Required clarifications before later slices

1. **No implied retained-R2 authority.** Slice 1 currently says that separate
   owner authorization is already represented by the sprint request. It is
   not. The owner authorized creation of this investigation background and
   preservation of logs; they did not authorize retained workspace/object
   access. Keep Slice 1 conditional on a new, explicit owner authorization and
   an API-supplied exact coordinate packet. The existing background's
   read-only/no-R2 stance controls until then.

2. **Treat the first `390 / 390` failure as a digest/metadata/path issue until
   proven otherwise.** Equal member counts cannot support a claim about added
   or removed members. Slice 0's inventory-diff recorder should report a
   deterministic manifest comparison including relative path, mode/metadata if
   relevant, bytes, and digest classification so the first mismatch is not
   collapsed into the later `390 -> 420` member-count change.

3. **Freeze public failure behavior in the correction contract.** The current
   plan appropriately rejects generic retry loops. Slice 3 should explicitly
   decide whether an irrecoverable concurrent-adoption failure yields a typed
   native review/refusal result, versus whether the prior checkpoint permits a
   known-safe replay. API must never infer retryability from a child exit code
   alone.

4. **Keep semantic-parity assertions strict.** For a serialized interim fix,
   compare final native truth and public result/checkpoint—not merely that both
   paths exit successfully. If output ordering is intentionally canonicalized,
   state that normalization rather than silently accepting ordering drift.

## Cross-repo boundary

The plan correctly keeps API responsible for custody, leasing, slots, queueing,
and spend records. SBE should expose typed native result/refusal evidence only;
API will ingest it rather than reconstruct pass membership, reconcile partial
provider outcomes itself, or reinterpret a nonzero subprocess exit as a
generic transient dependency.

With the four points above carried forward, Slice 0 may proceed without API
code changes, provider activity, retained-run mutation, deployment, or release.
