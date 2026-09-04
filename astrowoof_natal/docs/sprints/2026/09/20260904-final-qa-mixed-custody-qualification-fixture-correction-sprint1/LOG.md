# Log — final-QA mixed-custody qualification fixture correction

## 2026-09-04 — Slice 0

- Reproduced all three qualification tests failing at
  `build_external_authority_request_v2()` with
  `Lifecycle checkpoint has no external-authority request`.
- Confirmed `_warning_authority()` committed `FINAL_QA_WARN` subject evidence
  before `_ordinary_authority()` attempted to prepare a new polish request.
- Confirmed the `0.4.46` terminal-dominance selector correctly suppresses that
  request.
- Classified the defect as impossible fixture chronology. No runtime relaxation
  is appropriate.
- Confirmed the release gate omitted
  `test_final_qa_mixed_custody_qa` / `astrowoof-final-qa-mixed-custody-qa`.

## 2026-09-04 — Slice 1

- Split coherent ordinary-polish authority construction from later final-QA
  review-evidence injection.
- Pending case now records its scripted provider identity before adding the later
  finalization conclusion; lifecycle remains nonterminal and selects provider
  reconciliation.
- Refusal case now introduces its transient outer-status contradiction only after intent durability and
  still refuses before payload resolution/provider call-entry.
- Added a negative regression proving conclusion-first construction cannot mint
  a new authority request.
- Corrected the nine older mixed-custody characterization cells that shared the
  same invalid finalization-first authority helper; each now introduces review
  evidence at its intended custody/ambiguity/terminal seam.
- Expanded focused matrix: 57 passed, 1 expected optional-schema skip.
- Updated the release playbook to require transitive packaged qualifications in
  an affected focused matrix.

## 2026-09-04 — Voof-paws 1 and Slice 2 start

- API independently reran the two direct source modules: 13 passed.
- API confirmed the closed v1 receipt and exact semantic values remain compatible;
  no API reader/runtime change is required.
- API required the full SBE suite for confidence restoration in addition to the
  focused/package gates.
- Froze the fresh replacement version as `0.4.47` before release-bound testing.

## 2026-09-04 — full-suite reconciliation

- The first full discovery run executed 1,040 tests in 817.495 seconds and
  reported 13 failures, 4 errors, and 52 skips.
- Twelve failures were stale assertions predating already-released terminal
  dominance, provider-custody precedence, and dormant theme-group semantics.
  The corrected 102-test cluster passed.
- Two errors came from five untracked August 31 wheel-battle investigation
  cases under the ordinary test directory. Those historical programs were
  archived with non-test extensions beside their sprint evidence.
- The remaining two errors came from a v1 Waffle/Scone qualification that still
  required the removed `ASSIGN THEME GROUPS.md` artifact. Its current
  qualification was advanced honestly to v2 while the historical v1 schema
  remains packaged.
- The remaining failure came from a smoke test that expected the old
  zero-action terminal-review route. Its current successful route is
  `DELIVERY_COMPLETE`, has no terminal-review result ID, and completes cleanup.
- The canonical rerun executed 1,035 maintained tests in 879.417 seconds:
  all passed with 52 expected environment/optional skips.
