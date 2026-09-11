# API review — Slice 2 relocated read-only assessment reader

## Decision

**Approved to proceed to the paired API-host integration and installed-wheel gate.**

The implementation preserves the boundary agreed in Slices 0–1:

- The ordinary public reader remains the authoritative, original-path reader
  and retains its native writer-lock behavior.
- The new public relocated reader is additive, never acquires or creates that
  lock, and requires an authority whose two capabilities are both explicitly
  false.
- The relocated reader validates both the immutable copy's actual root and the
  preserved original logical root, rejects same-root authority, validates the
  complete snapshot inventory before and after native reads, and binds the
  returned assessment to the exact authority/checkpoint identities.
- `terminal_result_id` is correctly part of the signed closed authority. A
  null value selects no terminal result and cannot invoke availability
  discovery; a non-null value reaches the native exact-ID reader with
  availability recovery disabled. That is the right ownership and no-discovery
  behavior for an API-selected checkpoint.
- The internal validator injection stays behind private/reused reader seams;
  the ordinary public defaults are unchanged.

## Release-gate test addition

Before packaging, please add one relocated-reader test with a valid,
authority-bound non-null `terminal_result_id`. It should prove both that the
returned nested terminal evidence names that exact ID and that a different or
missing ID fails closed rather than falling back to discovery. The ordinary
reader already exercises exact selection, but this small relocation-specific
test guards the new authority-to-private-reader forwarding seam directly.

This is a focused coverage addition, not a request to change the approved
contract or broaden the reader's authority.
