# Slice 2 — provider-free Ganache reproduction

**Status:** superseded before review. Slice 0's exact error is a legacy
theme-group assembly requirement, which is incompatible with the already
approved dormant-feature policy; it must be removed rather than sealed as a
native review outcome.

## Discarded boundary

This document originally proposed making exact reconciliation seal a terminal
review result when it encountered the stale theme-group assembly artifact. That
would have continued to make an unimplemented filtering feature relevant to
deck handling, so the proposal was withdrawn before review or release.

1. completed evidence has already reached native pass/action truth;
2. exact-route local finalization reaches deterministic
   `AssemblyContractError`; and
3. every retained action has `terminally_accounted` custody.

No reconciliation, terminal-result, or API-ingress behavior was changed by the
withdrawn proposal.

## Correct direction

- Treat `ASSIGN THEME GROUPS.md` as a retained, ignored legacy artifact.
- Do not parse, join, validate, report, or emit theme-group assignments during
  final assembly.
- Retain model compatibility for stored theme fields, but omit unused
  theme-group registry/assignment fields from the final assembled deck so old
  placeholders cannot leak into delivery.
- Ganache can then complete normal finalization without a special review route.

## Provider-free evidence

The existing complete six-pass assembly fixture now deliberately creates a
Ganache-shaped retained assignment artifact: its registry remains structurally
valid, while an Interdogpendence assignment names the unregistered
`grounded_companionship` chapter. It then calls the real `assemble()` path. It
proves:

- final assembly still produces all 50 stories and four summaries;
- no theme registry or assignment field survives in the delivered deck;
- the general output placeholder check remains true; and
- `authored_theme_group_priority_ids` is the explicit empty compatibility
  value, not a residual policy signal.

Production split workspace generation also no longer requests the artifact for
pass six. The explicit builder option remains only to make historical-fixture
compatibility testable.
