# API review — Slices 0–1 / Gate A

## Decision

Approved.  The provider-free matrix establishes that the live `type_error`
token is insufficient to choose a correction: at least two materially distinct
public escape routes remain possible, while ordinary delivery/review controls
pass.  No implementation should begin from this evidence alone.

## Findings accepted

- The raw Render-export provenance, authority joins, phase ordering, and
  installed 0.4.61 package/source normalization are sufficient to exclude a
  wrong **passed root string**, package skew, missing observer invocation, and
  Better Stack transport.
- Matching logical-root and call-time-root digests do not claim that every
  persisted member has a valid packet-builder shape.
- The pre-assembly collector escape and the typed-status double-fault are both
  contract-significant possibilities.  A generic exception catch would hide
  their different ownership and fail-closed implications, so it is not an
  acceptable shortcut.
- The passing 11-case normal delivery/review controls correctly prevent treating
  a broad runtime regression as proven.

## Next gate

API will prepare one immutable coordinate packet per witness from the
authoritative checkpoint registry.  That packet will bind the exact API/native
run, result/receipt, SBE-authoring checkpoint generation, storage object/key,
archive and inventory digests, byte size, and original logical root.

The packet alone grants no storage access.  After it is reviewed, the owner may
separately authorize at most one conditional HEAD and one bounded GET for each
named checkpoint, exactly as Slice 2 specifies.

No provider, R2, Better Stack, queue, lifecycle, retained-workspace, package,
or release mutation is approved by this review.
