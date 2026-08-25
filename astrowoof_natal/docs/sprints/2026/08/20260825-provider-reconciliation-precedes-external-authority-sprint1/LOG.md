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

## 2026-08-25 — Slice 0 public selector audit

- Owner authorized execution through the next API review pause.
- Added a provider-free public-path fixture for exact and bounded routes with six
  retained provider identities plus one later prepared action.
- Proved the precise ordering defect: due reconciliation wins, but prepared
  authority masks not-due custody and completed-evidence fan-in.
- Proved the incorrect branch projection also changes temporal v0.6 checkpoint
  basis identity across a time-only not-due → due observation.
- Verified all inspection calls were byte-level nonmutating and performed no
  provider I/O or authorization mutation.
- Runtime and schema behavior remain unchanged; paused at voof-paw 1.

## 2026-08-25 — Slice 0 API approval

- API approved the public reproduction and existing-field compatibility decision.
- Confirmed due/not-due/fan-in precedence and unchanged-basis authority suppression.
- Authorized semantic-contract work only; no provider I/O or frozen-QA access.

## 2026-08-25 — Slice 1 precedence contract

- Tightened lifecycle v0.5 semantic validation in place.
- Added closed failures for retained provider custody and required provider fan-in
  masked by external authority.
- Tightened temporal v0.6 semantic validation against a rehashed basis carrying
  both provider custody and an authority request.
- Corrected authority-digest tests to use a real authority-only workspace rather
  than a synthetic authority-over-custody combination.
- Focused contract suite passed: 28 tests, 1 optional `jsonschema` skip.
- Selector implementation remains unchanged and therefore fails closed at the new
  validator until Slice 2; paused at voof-paw 2.

## 2026-08-25 — Slice 1 API approval

- API approved the in-place v0.5/v0.6 hardening and authorized selector work.
- Reconfirmed SBE-owned subset order/cap, nonmutating not-due behavior, and no
  provider-create or authority-consumption expansion.

## 2026-08-25 — Slice 2 selector correction

- Reordered shared lifecycle classification so due retrieval, completed-evidence
  fan-in, scheduled custody, and causal local work precede prepared authority.
- Preserved the existing four-action due subset and native `not_before` behavior.
- Converted the Slice 0 reproducer into positive exact/bounded regression coverage.
- Proved time-only not-due → due now retains one checkpoint basis with no authority
  inventory in either observation.
- Focused lifecycle/capacity/temporal suite passed: 70 tests, 1 optional schema skip.

## 2026-08-25 — Slice 3 multi-cycle qualification

- Extended the installed provider-pending qualification with one later prepared
  action in the same seven-action ledger.
- Proved not-due and due inspection suppress the prepared action while retaining
  one unchanged temporal basis.
- Proved bounded retrieval remains exactly 4+2 with six unique GET identities and
  no duplicate create/retrieval.
- Proved completed evidence selects deterministic fan-in before authority.
- Proved a new post-fan-in checkpoint exposes exactly the later prepared action.
- Refined causal-local-work classification: authorization-pending bookkeeping is
  not runnable local work and cannot force an ordinary-resume loop.
- Focused qualification/capacity suite passed: 34 tests.
