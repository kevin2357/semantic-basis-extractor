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
