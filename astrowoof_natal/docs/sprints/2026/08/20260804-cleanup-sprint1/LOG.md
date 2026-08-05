# 2026-08-04 Cleanup Sprint 1 Log

## Slice 1 — Dynamic-chapter contract closure

Started by promoting the implemented v0.4 registry behavior into a durable
contract and reconciling the earlier UI-review decision inventory. Product-mode
questions such as Quick versus Complete remain explicitly outside this sprint.

Published `AstroWoof Dynamic Chapter Registry Contract.md` and marked the
registry naming, compatibility, and legacy-field questions as implemented in
the original Ella UI decision record. Commit: `6a6bab6`.

## Slice 2 — Subtitle craft guidance

Propagated the live Ella finding into the generated pass-6 assignment, compact
and full workspace briefs, and the handoff prompt. Guidance now asks for direct
reader orientation and natural variation across subtitle sentences without
turning `These cards ...` into a lexical ban or deterministic rejection rule.
A workspace-generation regression test confirms that the instructions are
present in pass 6 and that ordinary card passes do not receive the theme-plan
file.

## Slice 3 — No-astrology advisory audit

Audited all preserved reference decks. The original detector emitted 106 field
warnings across 16 decks; bare `house`, `square`, and `chart` accounted for 93
warnings and mixed ordinary English with astrology leakage. Replaced those
three tokens with contextual forms while leaving all unambiguous vocabulary
unchanged. The corpus now emits 56 advisories across seven decks, removing 50
demonstrated false positives. Every remaining sampled field contains a genuine
chart, aspect, planet, or Doghouse reference. Added regression examples for
ordinary-home/geometric/seating-chart language and explicit astrological usage.

## Slice 4 — Completed-run retention hygiene

Added an explicit `--cleanup-completed-run` operation with token-free dry-run
mode. Cleanup is allowed only after successful delivery and verifies final
artifacts, delivery ZIPs, accepted prose, and source archives before deleting
anything. It removes only expanded SBE copies, extracted attempt sources,
reconstructable response workspaces, and duplicated final accepted-pass trees.
Raw request/response, Batch, cost, retry, QA, accepted-workspace, and delivery
evidence remains intact. Focused tests cover refusal, dry-run, execution,
retention, and idempotence.

The operation was then executed against the disposable completed Ella subtitle
run. It removed nine previously reviewed targets and reclaimed 1,471,698 bytes.
The immediate idempotence check reported zero remaining targets and all retained
artifact preconditions continued to pass.

## Sprint closure

Full regression verification passed: 105 tests in 98.149 seconds. `git diff
--check` reported no whitespace errors. The sprint made no live OpenAI request
and left Quick/Complete products, critic deployment policy, frontend layout,
and aggressive Batch-evidence archival outside its bounded scope.
