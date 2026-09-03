# Evidence index

- `C:\\tmp\\sbe-worker-last-2-hours-puff-20260903.log` (unfiltered recent QA SBE Render export).
- API authoritative receipt/custody summary recorded in the API companion sprint.
- Pastiche native run:
  `e9a72ba7695dddddc977da162388396a854a0813139c5475ce0b290d038c4ffb`.
- Puff native run:
  `84a24f8facd330a80ad42c19986ccc0f5fde2287e307d30ccbf6e3f85f3c30be`.

- [Slice 0 frozen timelines and source map](SLICE%200%20-%20FROZEN%20TRACE%20TIMELINES%20AND%20SOURCE%20MAP.md).
- [API Slice 0 review and bounded checkpoint authorization](API%20REVIEW%20-%20SLICE%200%20AND%20BOUNDED%20CHECKPOINT%20AUTHORIZATION.md).
- [Slice 1 bounded checkpoint findings](SLICE%201%20-%20BOUNDED%20CHECKPOINT%20FINDINGS.md).
- Closed access manifests and reader under `access-manifests/` and `tools/`.

Current gate: packaging and installed-wheel qualification complete; awaiting
API/owner final release review.
The exact authorized read budget was consumed; no additional retained-workspace
access is authorized or needed.
# Slice 2 provider-free reproduction

- Added `test_optional_stage_completed_evidence_adoption_slice2.py`.
- Real exact-interactive `closure.main()` polish resume reproduces the missing
  completed-evidence adoption with provider transport forbidden.
- The original regression established the safe failure (`WAITING` with no
  provider call); after implementation the same public-resume fixture advances
  to `REPORTED` and consumes its local-work key with provider I/O forbidden.
- Qualitative critic and candidate runtime characterizations both prove their
  persisted in-progress consumers re-enter the stage-specific spend callback
  before completed-evidence adoption.
- Historical pre-fix result: 3 tests, 2 pass, 1 expected failure; no provider
  calls. This is retained as causal evidence, not current qualification.

# Theme-group dormant-feature decision

- Product direction is recorded in
  `PRODUCT DECISION - THEME GROUP QA DORMANT.md`.
- Theme-group fields remain compatibility data; assignment, coverage, and
  balance checks will not execute or emit diagnostics.
- Runtime implementation removes the call from the acceptance path and the
  active theme-group policy tests; a focused non-invocation regression proves
  it. Non-theme acceptance behavior remains separately covered.

# Slices 4–5 implementation evidence

- `test_optional_stage_completed_evidence_adoption_slice2.py`: 6 tests pass,
  including real public resume, mismatch refusal, positive critic/candidate
  adoption, and critic/candidate topology.
- `test_theme_group_qa_dormant_slice4.py`: 2 tests pass; the evaluator is
  patched to fail if invoked and non-theme acceptance remains independent.
- Combined focused result: 8 tests pass, provider/R2/spend activity: zero.

# Slice 6 release qualification — candidate 0.4.41

- Version `0.4.41` was set before release-bound builds or installed checks.
- Focused source qualification: 8 tests passed (`6` optional-stage adoption,
  `2` dormant-theme QA), with provider/R2/spend activity: zero.
- The deterministic final wheel was built twice with
  `SOURCE_DATE_EPOCH=315532800`; both builds are byte-identical:
  `4eb8afada01ae6c4d239d75387b75b32a4ee7756a78d742a48cfad99de848841`.
- The final wheel was installed into a fresh virtual environment with
  `semantic-projection-core 0.11.1`; `pip check` passed.
- The installed package passed the focused eight-test qualification and the
  public `astrowoof-release-smoke --require-installed` command in a fresh
  workspace.
- No external provider request, R2 access, retained-QA access, or spend was
  performed. Supplemental local validation dependencies were used only to run
  the installed artifact's schema-capable test paths.
