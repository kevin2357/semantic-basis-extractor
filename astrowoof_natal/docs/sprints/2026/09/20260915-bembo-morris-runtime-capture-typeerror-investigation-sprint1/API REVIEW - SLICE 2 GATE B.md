# API review — Slice 2 / Gate B

## Decision

Approved.  The bounded reads and exact-root, network-disabled reproductions are
sufficient to rule out an SBE correction or package release from this evidence.
No SBE broad exception normalization is approved.

## What the reproduction establishes

- Both R2 objects match the API-pinned archive byte sizes and SHA-256 values,
  and their inventories were verified before read-only extraction.
- The exact installed/source-equivalent 0.4.61 public capture callable does not
  reproduce either live `TypeError` against the verified generation-8 roots.
- Bembo correctly returns a delivery packet; Morris correctly returns the typed
  `unsupported / contradictory_native_evidence` status.
- This confirms neither of the provider-free escape constructions is proven to
  be the live cause.

## API-side check

API invokes `_observe_editorial_terminal(...)` before
`_cleanup_completed(...)` on delivery, and the terminal-review path likewise
observes before its non-retained cleanup.  The discrepancy is therefore not
explained by API deleting the workspace before capture.

## Ownership and next diagnostic shape

The remaining issue is an API/runtime observation-window discrepancy: either a
transient workspace member/state visible in the live call but absent from the
generation-8 archive, or an in-process import/interpreter condition not present
in the isolated source-equivalent container.

Any next API diagnostic should be narrowly non-authoritative and avoid paths,
exception prose, native content, prompts, responses, and secrets.  It should
differentiate at minimum:

1. pre-assembly evidence collection;
2. guarded packet assembly; and
3. typed-status construction following an assembly refusal.

Safe function/frame identifiers and source line numbers from a caught failure
are appropriate, as are bounded call-time checkpoint/publication ordering
identities.  This requires an API-side review before implementation; no live
retry, R2 read, workspace mutation, Better Stack replay, provider work, or
SBE package change follows from this approval.
