# Evidence

## Planning evidence only

- Background: `BACKGROUND.md`
- Supplied log: `C:\Users\kevin\Downloads\sbe logs.txt`
- Log bytes: 1,714,322
- Log lines: 2,000
- Log SHA-256:
  `a0267e1984311ff067027c3897833cd8ce704ed6cee5fc0d3bcb0fa7f8c4fe20`
- Parsed `✨🐶` records: 1,641/1,641
- Parsed native runs: 2
- JSON command/execution envelopes recognized: 265
- Malformed marked records: 0

Diagnostic reporter output is local and ignored:

- `.tmp-nori-biscuit-report/report.json`
- `.tmp-nori-biscuit-report/report.html`
- `.tmp-nori-biscuit-report/report.md`
- `.tmp-nori-biscuit-report/report.mmd`

The reporter identified four candidate semantic-republication windows for
Biscuit and three for Nori. These are navigation evidence only. Its v1 matrix
does not yet reduce API JSON envelopes, so it cannot itself establish Nori's
final API terminal disposition.

## Slice 0 result

- Evidence map: `SLICE 0 - TRACE AND SELECTOR EVIDENCE MAP.md`
- Reporter receipt: `SLICE 0 - RUN REPORTER DIAGNOSTIC RECEIPT.json`
- API review incorporated: `API REVIEW OF INVESTIGATION PLAN.md`
- Nori candidate: a polish semantic operation appears to be tested for
  consumption at the earlier authoring-pass checkpoint.
- Biscuit candidate: completed creative-retry evidence reaches its nominal
  consumer, but the exact adoption join remains ambiguous.
- These are not yet claimed as one implementation cause.
- SBE `terminal_closed` and API `native.terminal.review_required` remain
  unjoined observations pending protected result/checkpoint evidence.

## Current gate

Slices 1–2 complete:

- `SLICE 1 - READ-ONLY ACCESS RECEIPTS.json`
- `SLICE 1 - EXACT CHECKPOINT FINDINGS.md`
- `SLICE 2 - NATIVE CAUSAL MATRIX AND FINDING CLASSIFICATION.md`

Slice 3 complete:

- `SLICE 3 - PROVIDER-FREE PRODUCTION-BOUNDARY REPRODUCTION.md`
- `astrowoof_natal/tests/test_nori_biscuit_reproduction_slice3.py`
- focused public-boundary reproduction and real-consumer matrix: 5 tests passed
- Nori ordering seam reproduced; Biscuit general creative-retry defect not
  reproduced

## Slice 4 correction evidence

- Contract: `SLICE 4 - NARROW POLISH ADOPTION ORDERING CONTRACT.md`
- Runtime: optional-stage local progress is sealed at finalization, not at the
  preceding authoring-pass checkpoint.
- Real-consumer regression uses `finalize_subjects`, `polish_subject`, the
  OpenAI completed-response adoption path, and `SpendController` settlement.
- Provider transport is fail-on-call; create and retrieval count are zero.
- Focused reproduction module: 5 tests passed.

## Slice 5 focused qualification

- Implementation: `SLICE 5 - NARROW NORI RUNTIME CORRECTION.md`
- Nori/Biscuit reproduction + Moxie adoption + final-QA mixed custody:
  22 tests passed.
- Post-fan-in composed/routing/runtime matrices: 21 tests passed.
- Total focused evidence: 43 tests passed.
- Diff hygiene passed; the only message was Git's existing LF/CRLF advisory.
- No provider or R2 operation occurred; no retained checkpoint was executed or
  mutated.

## Release-scope separation

- `pyproject.toml`: no run-reporter console scripts in the Nori diff.
- package `__init__.py`: no run-reporter exports in the Nori diff.
- reporter implementation/resources/tests remain separate untracked work and
  are not authorized for the Nori commit or committed-source wheel.

## Slice 6 release-candidate evidence

- Record: `SLICE 6 - 0.4.38 RELEASE CANDIDATE EVIDENCE.md`
- Candidate: `0.4.38`
- Wheel SHA-256:
  `c50fe0faca9e3f29bfa56a3e9a43cca3733497946223ee240926f8db967e5feb`
- Reproducible builds: byte-identical.
- Reporter members in accepted wheel: none.
- Focused source tests: 43 passed.
- Installed-wheel Nori/Biscuit tests: 5 passed.
- Installed generic smoke and `pip check`: passed.
- SBE/SPC identities: `0.4.38` / `0.11.1`.
- No provider, R2, retained-workspace, or spend activity.

Paused for final API and owner release review.
