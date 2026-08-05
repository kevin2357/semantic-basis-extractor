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
