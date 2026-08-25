# Provider Reconciliation Precedes External Authority — Log

## 2026-08-25 — Planning opened

- Recorded fresh-QA evidence of external-authority deferral while retained
  provider-created dependencies remained.
- Scoped the work as a lifecycle-selection patch, pending SBE-agent assessment.
- No source, workspace, provider, spend, or retained-run state changed.

## 2026-08-25 — SBE pre-implementation assessment

- Located the likely lifecycle precedence seam.
- Current ordering prioritizes due retrieval but checks prepared authority before
  scheduled/not-due custody and completed-provider fan-in.
- Expanded the plan to freeze the complete precedence ladder rather than swapping
  one conditional branch.
- Added explicit v0.5/v0.6, 4+2 fresh-worker, route/stage, failure-injection,
  installed-wheel, privacy, and no-provider-I/O gates.
- Added API review pauses after Slices 0, 1, 5, and 6.
- Implementation remains paused pending owner/API review.

## 2026-08-25 — Compatibility baseline refresh

- Updated the next-release project dependency and bounded runtime admission pin to
  exact SPC 0.11.1.
- Updated bounded admission/authoring fixtures to the same upstream identity.
- Preserved the immutable 0.4.21 release record at SPC 0.11.0 because that is what
  its published wheel actually declares.
- Added exact SPC 0.11.1 alignment to the sprint release gate.

## 2026-08-25 — API plan review

- API approved beginning Slice 0 provider-free.
- Frozen custody-first ordering, causal-local-work scope, preferred in-place
  v0.5/v0.6 hardening, delivery-independent critic behavior, and existing reason
  vocabulary with richer redacted diagnostics.
- Added explicit not-due nonmutation, pre-fan-in authority suppression, stable
  time-only request identity, and new-basis-after-fan-in assertions.
- Frozen cohort recovery remains separate.
- Owner authorization to begin remains pending.
