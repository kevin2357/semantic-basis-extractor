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

## 2026-09-12 — Pre-lock candidate gate

- Committed and pushed exact artifact source
  `edeb38034c239b5b5ea22c4f0e58a89e33aa1632`.
- Built two clean wheels from independent complete source exports with fixed
  epoch `1789242555`; both are 1,383,877 bytes with SHA-256
  `c71ee9717d128107ec09092018f280b3af50b4c569b63869f1b850388773dbcc`.
- Installed the exact candidate and its declared dependencies into a clean
  environment; `pip check`, release smoke, and lifecycle smoke passed.
- The installed public relocated reader accepted the retained Bodoni copy with
  the expected provider-pending disposition, strict pair validation, and all
  387 files unchanged.
- No provider, R2, or live QA operation occurred.
- Ready to freeze the release-lock evidence and repeat the build/install gates
  from the exact lock commit.

## 2026-09-12 — Exact release lock qualified

- Froze and pushed immutable release target
  `477cfa2491f33377f1a873772c5e465c588f0741`.
- Exported that exact commit and rebuilt twice using its epoch `1789243472`.
- Both canonical wheels are byte-identical: 1,383,877 bytes, SHA-256
  `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`.
- Clean installation, dependency check, installed release smoke, installed
  lifecycle smoke, and exact retained-Bodoni reader all passed.
- Retained Bodoni remained byte-identical across all 387 files; no provider,
  R2, or live QA operation occurred.
- Slice 2 is complete. Paused at API consumer review and immutable
  tag/publication authorization. Tag only `477cfa2`, never this later evidence
  commit.
