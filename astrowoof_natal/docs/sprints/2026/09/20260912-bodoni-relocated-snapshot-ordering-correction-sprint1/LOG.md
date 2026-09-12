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

## 2026-09-12 — Slice 1 complete

- Replaced host-`Path` inventory ordering with case-sensitive relative POSIX
  component ordering while preserving historical Linux manifest order.
- Added manifest-registered mixed-case, directory/zip, duplicate, missing,
  extra, size-drift, and digest-drift regression coverage.
- Combined focused qualification passed: `46 passed`.
- Paused before Slice 2 package/release work for API review of Slices 0–1.

## 2026-09-12 — Slice 2 authorized

- API approved Slices 0–1 without requested corrections and authorized package
  qualification against the retained local Bodoni workspace.
- Reviewed the maintainer and native-worker release playbooks.
- Selected fresh unreleased candidate version `0.4.61` before release-bound
  testing.
- Selected the broad/full manifest gate because `snapshot_inventory()` is
  shared persistence infrastructure, despite the correction's narrow code diff.
- Recorded no Alloy-model impact: inventory enumeration order does not change
  lifecycle entities, authority, transitions, cardinality, or temporal rules.
- No R2 read, provider operation, or live QA action is part of Slice 2.

## 2026-09-12 — Source regression gate

- Re-ran the focused matrix after freezing `0.4.61`: `46 passed`.
- Ran the complete checked-in manifest suite with the supported one-worker
  profile: `1,192` tests, `60` expected skips, zero failures in
  `1,600.308523` seconds.
- Test inventory SHA-256:
  `a65a1b0f50cab9902066571817e2db52b2ccf5ed4add76423451d2512f99f2bf`.
- Ready to commit the exact artifact source before reproducible builds.
