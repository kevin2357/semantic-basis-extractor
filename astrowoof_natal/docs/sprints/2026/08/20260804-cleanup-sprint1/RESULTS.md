# 2026-08-04 Cleanup Sprint 1 Results

## Outcome

The four bounded cleanup slices are complete.

1. Published and reconciled the implemented v0.4 dynamic chapter registry
   contract.
2. Improved pass-6 subtitle craft guidance while avoiding proxy-driven lexical
   rejection rules.
3. Reduced no-astrology advisories from 106 fields across 16 preserved decks to
   56 fields across seven decks by removing 50 demonstrated false positives.
4. Added terminal-state-only completed-run cleanup with dry-run planning,
   retained-artifact verification, a cleanup manifest, and idempotence.

## Verification

- Full suite: 105 tests passed.
- Final Ella reference deck: validation passes; advisories reduced from eight
  to one genuine square-aspect reference.
- Completed Ella subtitle run cleanup: nine targets, 1,471,698 bytes reclaimed,
  zero targets on immediate rerun.
- No OpenAI request was made during this sprint.

## Commits before final slice

- `9acf1c2` — Record subtitle diversity finding.
- `6a6bab6` — Close dynamic chapter contract decisions.
- `76c4aa3` — Diversify dynamic chapter subtitle guidance.
- `d44e186` — Refine no-astrology advisory signal.

## Deferred by design

- Quick versus Complete WoofMap product architecture.
- API/runtime repository ownership and deployment packaging.
- Default qualitative-critic and candidate-promotion policy.
- Card-level gold-reference experiments.
- `stratified-v2` assignment research.
- Aggressive compression or deletion of raw Batch transport evidence.
