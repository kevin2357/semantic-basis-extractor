# Log — editorial runtime-capture native diagnostics

- Created background and plan from the closed Bembo/Morris Gate B ruling.
- Received API approval for Slice 0 / Gate A with an explicit requirement to
  distinguish pre-assembly collection from typed-status double-fault.
- Froze four catalogued events, nine closed phases, bounded cardinality,
  allowlisted frame projection, and fail-silent behavior.
- Implemented catalog and capture instrumentation without changing public
  signatures, returns, exception conversion, or native/editorial semantics.
- Added `test_editorial_runtime_capture_diagnostics.py` to the suite manifest
  as serial-only and logging-sensitive immediately upon creation.
- Focused qualification passed: 45 tests, targeted Ruff checks, manifest
  enforcement, and `git diff --check`.
- Broader provider-free editorial, logging, trace, release-contract, and
  manifest qualification passed 99 tests with one expected skip.
- Paused before installed-wheel/API-host qualification and any release action.
- Received API approval for Slices 0–2 and authorization to enter the
  installed-wheel/API-host coexistence gate.
- Built the committed implementation twice at fixed epoch `1789467559`; the
  disposable `0.4.61` wheels were byte-identical at 1,386,829 bytes and SHA-256
  `be7c59eb70b3c61adc2dedee13af6dfa62595697615c22e3d2d858f02c6e7f24`.
- Installed the exact wheel outside the checkout and proved the package and
  changed catalog/runtime members resolve from installed package roots and
  match source bytes.
- The real API `force=False` initializer preserved the pre-existing API host
  handler, installed exactly one SBE handler, retained two valid API stdout
  records, and emitted 16 valid SBE records for three capture invocations.
- The host gate distinguished `pre_assembly_evidence_collection` from
  `typed_status_construction`, retained exact exception identity, and exposed
  neither injected exception text nor the workspace root.
- Installed runtime/capture parity passed 15 tests, including ordinary packet,
  typed unsupported, and both exceptional routes. API-host dependency checking
  and wheel inventory also passed; provider operations and workspace mutation
  were zero.
- A first synthetic API event was rejected because the harness used the
  non-catalog environment token `qualification`; it was corrected to the real
  accepted `test` context before capture ran. A separate fresh-venv `pip check`
  lacked `jsonschema` because it inherited the bundled base interpreter rather
  than API's dependency set; the decisive check passed with the candidate
  prepended to the actual API host environment. Neither was a product failure.
- Reached Review Gate B. The wheel is expressly disposable because it still
  carries already-published version `0.4.61`; no version bump, release-bound
  suite, release lock, tag, publication, deployment, live witness, network,
  provider, R2, or Better Stack action occurred.
- Received API Gate B approval and selected fresh, unused candidate version
  `0.4.62`. The release-bound gate includes the full maintained suite,
  reproducible exact-source builds, installed smoke and dependency checks, and
  a rerun of API-host coexistence before returning for pre-tag review.
