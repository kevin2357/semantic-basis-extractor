# API review — Slice 0 and Oauf-paws 2

## Decision

**Approved to proceed with the exact generation-11 access manifest.** The API
owner's investigation request and the frozen coordinate packet authorize the
one `HEAD`, followed only if it matches by the one `GET`, for the declared
object. The worker stays suspended. This does not authorize a generation-10
read, a bucket listing, any write, provider work, recovery, reconciliation, or
retained-run mutation.

## What Slice 0 establishes

- The apparent `a838af…` / `c5ac68…` / `07300bd…` drift is a diagnostic
  conflation, not evidence that the API-granted v2 request changed identity.
  The exact API v2 request/grant pair remains `07300bd…` / `bb3aea…`.
- The lifecycle-v0.5 embedded v1 request is observation-time-bearing and is
  therefore not comparable to the constrained v2 request merely because both
  are called “request.”
- The `Local-work consumption history is not append-only` error is an important
  upstream fact, but not yet a proven cause of the later action posture or
  native-intent mismatch. The retained checkpoint must establish that join.
- The absence of a polish provider operation remains established. This is a
  pre-provider dispatch/refusal investigation.

## Small wording and reproducibility corrections

1. In the identity map, replace “disproven for v2 by the trace” with a narrower
   statement: the trace shows the same v2 digest on every observed constrained
   attempt, and source says its identity is basis/inventory-bound. It cannot by
   itself prove global immutability of every historical v2 object; the retained
   canonical object remains the authority.
2. Record the exact local filename of the corrected 845,872-byte log export in
   `Evidence.md` (or Background) alongside its SHA-256. The API-added earlier
   104,739-byte window is a different, superseded partial export; the two must
   not be confused in later review.

## Slice 1 requirements

The access receipt must establish the declared object identity before archive
inspection, then report only sanitized structural findings. In particular,
preserve contract-qualified identities for:

- the native polish action state/custody/binding;
- the persisted v2 dispatch intent and its request/grant/inventory identities;
- the checkpoint basis and state revision; and
- the append-only local-work history and the predecessor/successor operation
  keys around revision 75.

Do not infer a causal order from a trace timestamp when the journal/checkpoint
provides stronger evidence. If generation 11 cannot explain how the intent was
created, pause with that exact evidence ceiling before requesting generation 10.
