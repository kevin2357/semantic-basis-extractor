# Slice 5 implementation review request

## Decision requested

Approve or amend the narrowly scoped ordinary-v2 optional-stage recovery
implementation before installed-wheel packaging.

## Implemented behavior

- Theme-group assignment, coverage, balance, registry, and mirroring evaluation
  no longer run in pass acceptance. The persisted fields remain compatibility
  data; no theme-group issue/advisory/retry/finalization signal is emitted.
- `prepare_completed_optional_stage_for_adoption()` runs immediately before a
  resumed exact-interactive optional consumer reaches `SpendController`:
  polish, qualitative critic, and qualitative candidate.
- It requires one exact stage/route/model action; a completed interactive
  response identity; the same live v2 intent inventory and authorization;
  a consumed authorization; a workspace-contained binding-owned request payload
  artifact; and a matching reconciliation response artifact.
- Only after that join does it write the existing attempt-local completed marker.
  It performs no provider I/O, grant, action settlement, or state transition.
- Missing v2 intent is an explicit no-op so legacy/non-v2 marker behavior stays
  unchanged. A malformed or mismatched v2 join raises before marker creation.
- Batch and bounded routes are not enabled or modified.

## Evidence

- The Puff-shaped public `closure.main()` resume removes the private marker,
  performs zero provider I/O, adopts the durable completed response, reports
  the action, reaches `POLISH_NO_CHANGE`, and consumes the local-work key.
- A mismatched reconciliation response identity is refused before marker
  creation.
- Critic and candidate each positively adopt their completed stage-local
  response through their normal deterministic consumer result, while an
  untouched sibling marker proves no cross-stage mutation.
- Real pass acceptance rejects an invalid non-theme context filter while its
  theme evaluator is patched to fail if invoked.
- Focused result: 8 tests passed; Python compilation and `git diff --check`
  passed. No provider, R2, or spend activity occurred.

## Requested review focus

Confirm the exact authority join, the legacy no-intent non-broadening rule, and
the dormant-theme policy boundary. No public schema or API code change is
proposed.
