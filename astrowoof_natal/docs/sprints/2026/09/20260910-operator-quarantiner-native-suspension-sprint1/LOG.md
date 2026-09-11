# Log

## 2026-09-10 — 0.4.60 candidate freeze

- Merged the approved relocated-assessment and operator-assessment diagnostics
  work into `main` at `cf15048`.
- Confirmed all remaining local and remote topic branches are ancestors of
  `main`; no additional sprint implementation remains unmerged.
- Reviewed the maintainer release playbook before qualification.
- Selected fresh candidate identity `0.4.60`; local tags show `0.4.59` as the
  latest component-scoped release.
- Selected the broad/full gate because the release changes shared lifecycle and
  retry-lineage validation seams, operator authority contracts, and native
  result publication ordering. The focused matrix must pass first.
- No tag, wheel publication, GitHub Release, live provider call, retained-QA
  read, or API/Render mutation has been authorized or performed.

## 2026-09-10 — Focused release gate

- Ran the expanded focused matrix across operator-disposition contracts,
  ordinary and relocated readers, cross-route and packaging coverage, the
  relocation capability fence, native publication, retirement, retry lineage,
  lifecycle inspection, release contracts, and suite-manifest enforcement.
- Result: 139 passed, 3 expected skips, 0 failures, in 18.885 seconds.
- Provider/network operations: zero.
- The Slice 3 capability-fence module remains registered in the maintained test
  suite manifest.

## 2026-09-10 — Broad gate finding

- The first manifest-driven broad run completed 1,184 tests with 60 skips and
  was not green: one error and one failure occurred in the operator-disposition
  diagnostics module.
- Exact cause: the module deliberately configures and removes the root SBE
  logging handler but had been classified as ordinary parallel-safe work. In
  full-suite order, prior logging mutation could leave its formatter capture
  empty or partial.
- This is a suite-manifest isolation defect, not an operator-assessment runtime
  or relocation-contract failure. Its weighted parallel-safe entry was removed,
  and the module is now classified in both `serial_only` and
  `logging_sensitive` so it runs in the protected observability group.
- The affected diagnostics and manifest guards then passed: 25 tests.
- Because the correction changes test-harness classification, the affected
  focused tests and the complete broad gate must both be rerun.
