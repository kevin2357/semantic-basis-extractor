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
