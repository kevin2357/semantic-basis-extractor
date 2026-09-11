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

## 2026-09-10 — Superseding broad gate

- Reran the complete manifest-driven suite from committed candidate identity
  `d7c4014` after the diagnostics isolation correction.
- Result: 1,184 passed, 60 expected skips, 0 failures, in 1,096.672 seconds.
- Test inventory SHA-256:
  `2bd1d2a50c8dc738f5027f24f5989f986d64ac877b7d4bc09748b9d2c6aefb29`.
- The inventory digest exactly matches the first attempt, proving the
  correction changed isolation/classification rather than test scope.
- Receipt:
  `C:\Users\kevin\AppData\Local\Temp\astrowoof-tests-kq8w9xj9\receipt.json`.

## 2026-09-10 — Initial package qualification

- Built two wheels from independent clean archives of candidate source commit
  `a31540d` with `SOURCE_DATE_EPOCH=1789089091`.
- Both wheels are 1,383,825 bytes with 310 members and SHA-256
  `bb514868c972d1444cd5929bf33ee7b8a794f962c5426cb011c71c92f8697155`.
- Package inventory contains the relocated reader and both relocation schemas;
  no cache, bytecode, build, dist, or release-work members were present.
- Installed the exact candidate with clean local SPC `0.11.1`; `pip check`,
  site-packages/version/export checks, release smoke, adversarial lifecycle QA,
  and operator-disposition QA passed.
- Release smoke packaged 195 resources. Adversarial QA covered 22 route cells
  and 32 invariants. All installed qualifications reported zero provider calls,
  zero external network calls, and zero spend.
- These are source-candidate coordinates. The release-lock commit must be
  rebuilt twice at its own recorded epoch before API receives an immutable
  wheel.

## 2026-09-10 — Exact release-lock package gate

- Proposed lock source `964c6c8df66a09437972f301edd1671f3a7e31ef` was
  built twice from clean archives at recorded epoch `1789089592`.
- Both canonical wheels are 1,383,825 bytes with SHA-256
  `618caee2c2f338cf868cfb024f764217c7b4ef4c83aff283b2bf78cd6e67d627`.
- A fresh exact-lock environment passed `pip check`, reported version `0.4.60`
  from `site-packages`, and exported the relocated reader.
- Exact-lock installed release smoke, adversarial lifecycle QA, and operator-
  disposition QA passed with zero provider/network operations and spend.
- Final lock documentation now records these coordinates. One final two-build
  comparison from that documentation commit at the same recorded epoch remains
  before API handoff.
