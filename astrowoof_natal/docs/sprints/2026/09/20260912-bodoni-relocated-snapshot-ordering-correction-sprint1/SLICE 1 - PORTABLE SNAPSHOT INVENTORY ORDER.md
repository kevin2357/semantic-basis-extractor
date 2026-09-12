# Slice 1 — Portable snapshot inventory order

## Implementation

`snapshot_inventory()` now derives each workspace-relative POSIX path before
ordering and sorts candidates by `PurePosixPath(relative).parts`.

This removes Windows host-path comparison from the durable inventory while
preserving the component-wise, case-sensitive ordering of existing
Linux-authored manifests. Filtering, byte-size capture, SHA-256 calculation,
process-cache behavior, and strict ordered-list validation are unchanged.

No existing manifest is rewritten or normalized during validation. Duplicate
manifest entries therefore remain unequal to the one-record-per-file actual
inventory and fail closed.

## Regression coverage

The new manifest-registered module proves:

- a lowercase directory sorts after uppercase sibling files;
- a directory subtree sorts before a same-prefix `.zip`;
- duplicate manifest paths fail closed; and
- missing, extra, size-changed, and same-size digest-changed members fail closed.

Existing relocated reader, authority, capability, checkpoint-repair, and test
suite manifest coverage remains green.

## Qualification

- Combined focused suites: `46 passed`.
- Exact retained Bodoni reader: passed with strict wrapper validation.
- Restored Bodoni files before/after: 387 / 387, byte-identical.
- Provider operations: zero.
- External storage reads: zero during implementation and qualification.

Slice 1 is complete. Slice 2 package/release qualification remains the next
gate; API installed-wheel review is required before release.

