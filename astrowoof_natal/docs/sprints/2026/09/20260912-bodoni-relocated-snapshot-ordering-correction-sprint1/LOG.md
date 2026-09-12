# Log

## 2026-09-12 — Opened

- API supplied the owner-authorized, hash-verified Bodoni checkpoint coordinate
  packet and private local restore locations.
- API classified the relocated-reader failure as snapshot ordering only:
  375 inventory records have identical content identity, but host-path ordering
  differs after Linux-to-Windows relocation.
- SBE worker remains deliberately suspended. No live mutation is authorized.

## 2026-09-12 — Independent native reproduction

- Verified the retained archive SHA-256 and independently compared all 375
  expected and restored inventory records.
- Confirmed identical path sets, byte sizes, and content SHA-256 values with a
  first ordered-list difference at index 16.
- Rejected plain-string and case-folded relative-path sorting because each
  changes historical Linux manifest order.
- Selected case-sensitive `PurePosixPath(relative).parts` ordering: it exactly
  reproduces the retained Linux manifest and removes host-path semantics.
- Expanded the plan with duplicate, mixed-case, same-prefix archive/directory,
  genuine drift, no-rewrite, and retained-Bodoni candidate gates.
- No provider, R2, retained-workspace mutation, or live runner action occurred.

## 2026-09-12 — Slice 0 complete

- Ran the corrected-source reader against the retained Bodoni restore using
  the frozen checkpoint coordinates.
- Obtained `provider_pending_known_identity`, `permitted`, and
  `known_provider_operation_pending`; authority/wrapper pair validation passed.
- Hashed every restored file before and after the read: all 387 were unchanged.
- Slice 0 is complete with no external I/O or live-state action.
