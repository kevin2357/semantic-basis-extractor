# Linux Smoke Patch Sprint Log

## 2026-08-08 - Planning only

- Recorded the API worker's Linux installed-smoke failure and zero-spend stop.
- Scoped a proposed 0.2.1 patch to deterministic fake output, structured smoke
  failure, tests, exact-wheel Windows/Linux smoke, and patch handoff.
- Explicitly excluded paid/live replay and production workflow changes.
- No runtime code, tests, package metadata, tag, or release was changed.

Next action: plan review and explicit approval before Slice 0 begins.

## 2026-08-08 - Slice 0 reproduction and patch boundary

- User approved the plan. Committed the planning-only baseline as `06b9977`
  and began Slice 0 without changing runtime code.
- Confirmed a clean baseline at `06b99773b05f0027d682bc106c1d84babac2c868`.
  Published v0.2.0 annotated tag object remains
  `8e441796d2aa33c5189f718e9e9fc199a7d9b396` and peels to reviewed commit
  `9c3ec9e59da7ad5ec87e0dc43cb9582913d6b7ac`.
- Reduced retained Linux evidence to fake/interactive provider, zero spend
  actions, `FINAL_QA_REQUIRES_REVIEW`, one repeated twelve-word group, and the
  subsequent nonterminal-cleanup exception.
- Reproduced the collision using the production `editorial_lint.words()`
  tokenizer. Three distinct hexadecimal tokens normalize to the identical
  alphabetic sequence `a d e`.
- Compared `PurePosixPath` and `PureWindowsPath` ordering for the 27 Markdown
  files in the retained pass workspace. The orders differ at index 1, proving
  that the tree-global fake ordinal is assigned differently by platform.
- Confirmed the cleanup masking is a direct unconditional call after the smoke
  records failed delivery. No production provider or linter change is needed.

Next action: Slice 0 gate review. Approve the exact fake-provider/smoke patch
surface and proposed v0.2.1 coordinates before implementation.

## 2026-08-08 - Slice 1 deterministic fake and smoke correction

- User approved Slice 0. Committed its evidence as `9c4a5d8` and implemented
  only the frozen fake-provider, smoke, and test surfaces.
- Replaced the tree-global ordinal with stable pass ID, POSIX-relative path,
  field path, and file-local occurrence identity. Theme-plan assignments use
  section-local occurrence order so coverage remains exactly balanced.
- Replaced hexadecimal body tokens with a 16-letter `a`-through-`p` encoding
  of digest nibbles. The production tokenizer preserves each token as one word.
- Added a 500-body normalization regression, separator/call-order invariance,
  complete smoke/cleanup coverage, and injected review-state structured
  failure coverage.
- Gated delivery artifacts, delivery provenance, and cleanup on actual
  `DELIVERY_COMPLETE`. Failed smoke reports now preserve run status, subject
  state, validation/lint/authoring-acceptance status, and rejection reasons;
  cleanup is explicitly reported as skipped.
- Focused release-smoke tests passed (4); the existing semantic-closure suite
  passed (67); the complete deterministic suite passed (148) in 68.404 seconds;
  `git diff --check` passed.
- No version, package metadata, production provider path, linter, release tag,
  or published artifact changed. No provider request was made.

Next action: Slice 1 gate review before commit or exact patch artifact work.

## 2026-08-08 - Slice 2 exact patch artifact qualification

- User approved Slice 1. Committed the correction as `7379ea4` and changed
  only the project version coordinate from 0.2.0 to 0.2.1 for qualification.
- Built the wheel twice with `SOURCE_DATE_EPOCH=1786240889`. Both 624,157-byte
  files are byte-identical with SHA-256
  `0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`.
- Audited all 40 wheel members; no disallowed package content was found.
- Clean-installed the exact wheel outside the checkout on Windows. Installed
  smoke passed through delivery and completed cleanup.
- Copied, rather than edited, the API agent's retained acceptance context.
  Replaced only the copied SBE wheel/hash and built offline with Docker.
- The Linux/amd64 installed smoke passed as the non-root worker user. Windows
  and Linux produced the same 19-resource aggregate digest
  `439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.
- Linux `pip check`, AGF 0.6.0 doctors, and SPC 0.10.0 installed smoke passed.
  Candidate image digest is
  `sha256:b3420fe8c4ff3183e5ebbdced1a678a2e0c278f3791189586488e7792a264dc0`.
- No provider request or networked build operation occurred; spend was USD 0.

Next action: Slice 2 gate review. No commit, release handoff, tag, push, or
publication until explicit approval.

## 2026-08-08 - Slice 3 patch handoff and publication preparation

- User approved Slice 2. Committed its version and evidence as `465cf41`.
- Prepared the 0.2.1 candidate manifest, release notes, compatibility delta,
  SHA-256 file, hash-pinned worker requirement, and API-worker handoff.
- All records identify the qualified 624,157-byte wheel with SHA-256
  `0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`.
- Documented unchanged 0.2.0 production contracts/ownership and direct links
  to spend authorization, spend enforcement, and the packaged catalog.
- No tag, push, GitHub release, asset upload, or provider request occurred.

Next action: Slice 3 publication gate review. Commit the prepared records and
publish only after explicit authorization.

## 2026-08-08 - 0.2.1 publication and verification

- User approved the publication gate. Committed the reviewed release bundle as
  `9e9db5f`, created the annotated release tag, and pushed main plus the tag.
- Published GitHub release 367357028 with the qualified wheel and checksum.
- Verified annotated tag object `7998c299824b13240215b9a501a1a3aeb309464f`
  peels locally and remotely to release commit
  `9e9db5f7378d459db1e5418f1607edc7f4c060bf`.
- Authenticated-download retrieved both assets into a fresh directory. The
  wheel was 624,157 bytes with the qualified SHA-256, and the downloaded
  checksum validated it independently.
- Updated release records with immutable post-publication IDs and evidence.
  The release tag was not moved.

Sprint complete. The API worker may pin 0.2.1 and resume Linux image promotion.
