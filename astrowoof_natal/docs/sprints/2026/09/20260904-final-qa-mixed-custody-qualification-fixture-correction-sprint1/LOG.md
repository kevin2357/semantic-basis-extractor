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

## 2026-09-04 — committed-source candidate

- Committed artifact source as `31a09e472bae871a0105d7a5e5719592b9a92407`.
- Exported that exact commit into a clean source root, excluding all untracked
  release and investigation material.
- Built twice with `SOURCE_DATE_EPOCH=1788547986`; both 1,199,948-byte wheels
  were byte-identical at SHA-256
  `4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`.
- The wheel contains 258 members, no absolute member paths, and the expected
  mixed-custody v1 and finalization-boundary v1/v2 schemas.
- Installed the exact candidate with immutable SPC 0.11.1
  (`dc345c…a612`) into an isolated venv; `pip check` passed and both packages
  resolved from that venv's `site-packages`.
- Installed public mixed-custody, terminal-review, finalization-boundary, and
  generic release-smoke commands all passed provider-free.

## 2026-09-04 — release-lock provenance and publication

- API reran its exact Sprint 76 consumer against the candidate and passed every
  closed lifecycle/custody/dispatch receipt with zero provider operations or
  spend.
- Created release-lock commit
  `0d0285297f6c74295939eb24c2a16d29af91a012`.
- Re-exported that exact commit and rebuilt twice with the recorded epoch. Both
  wheels remained byte-identical to the documented 1,199,948-byte
  `4be9db…e875` candidate.
- Repeated the isolated installed mixed-custody, terminal-review,
  finalization-boundary, and release-smoke qualifications against the
  release-lock wheel; all passed.
- Created and pushed annotated tag
  `astrowoof-natal-authoring-v0.4.47`; remote peeled target is the release-lock
  commit.
- Published GitHub Release `RE_kwDOToQdE84W06Ac` with only the exact wheel and
  `SHA256SUMS.txt`.
- Downloaded both assets into a fresh directory. Qualified, GitHub-reported,
  checksum-manifest, and downloaded wheel digests all match.
