# Plan — Bodoni relocated snapshot ordering correction

## Slice 0 — Reproduce and classify

**Status: complete.** Exact retained-workspace reproduction proves identical
member identity and host-dependent ordering only. The compatible canonical key
is `PurePosixPath(relative).parts`; candidate source reads Bodoni successfully
without changing any of 387 files. See
`SLICE 0 - EXACT ORDERING-ONLY REPRODUCTION.md`.

- Use the existing private verified Bodoni archive/local restore only.
- Reproduce the public relocated-reader refusal provider-free.
- Prove whether the difference is ordering-only, not path-set, byte-size, or
  digest drift.
- Compare candidate canonical keys against the retained Linux-authored manifest
  before selecting one. Preserve historical Linux component ordering rather
  than silently defining a new plain-string order.

**Exit:** exact native cause established with no external I/O.

## Slice 1 — Canonical inventory correction

**Status: complete.** Snapshot inventory now uses the portable, historically
compatible POSIX component key. Manifest-registered regressions preserve strict
duplicate and content-identity refusal. Combined focused suites pass: 46.
See `SLICE 1 - PORTABLE SNAPSHOT INVENTORY ORDER.md`.

- Derive each workspace-relative POSIX path before sorting and sort by its
  `PurePosixPath(relative).parts` tuple, not host `Path` ordering or a plain
  relative-path string. Preserve case-sensitive component ordering and the
  historical Linux-authored manifest order.
- Use one canonical ordering helper for snapshot publication and validation;
  compare strict ordered canonical lists rather than unordered maps.
- Preserve existing filtering and strict inventory member identity.
- Add regression coverage for deterministic canonical order and a
  Linux-authored/Windows-restored equivalent fixture.
- Include mixed-case file/directory names, a directory subtree beside a
  same-prefix `.zip`, duplicate manifest paths, and genuine
  missing/extra/size/digest drift.

**Exit:** byte-identical inventory semantics across the supported restore
platforms; genuine missing/extra/changed files still fail closed.

## Slice 2 — Release qualification

**Status: candidate qualified; release lock in progress.** API approved Slices
0–1 and requested the candidate/retained-Bodoni installed-wheel gate. Fresh
candidate version is `0.4.61`. Because snapshot persistence is shared
infrastructure, the full manifest suite followed the focused matrix; no
focused-suite waiver was used.

- Run focused relocation/snapshot tests and relevant package gates.
- Build an immutable wheel candidate twice from the exact artifact source and
  require byte-identical output.
- Before release lock, run the candidate implementation against the retained
  local Bodoni restore and prove the reader performs no snapshot-manifest or
  workspace rewrite.
- Run the public installed reader and pair validation against the retained
  Bodoni copy, checking post-read workspace identity.
- Freeze the release-lock evidence, then rebuild twice from that exact commit
  and repeat the installed qualification before API consumer review.

**Exit:** exact native reader works on the real paused-workspace fixture without
another R2 read or any live run mutation.
