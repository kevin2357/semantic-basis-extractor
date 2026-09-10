# Log — editorial-review capture-status native identity correction

## 2026-09-10 — mini-sprint opened

- Reviewed API Sprint 87 Slice 2C's released-consumer discovery against SBE
  `0.4.55` source.
- Confirmed runtime refusal branches call a fixture-oriented helper that emits
  literal fixture correlations and therefore non-real/reused capture identity.
- Identified an additional discrepancy: the helper includes `subject_id` in its
  ID inputs, while semantic contract v5 declares `capture_id` from run ID,
  result ID, reason, and detail code.
- Confirmed the successful exact-delivery handoff is unaffected.
- Recorded `no Alloy impact`: this is concrete identity derivation/population,
  not a change to the modeled editorial relationships.
- Opened a bounded correction plan and paused before implementation at Review
  Gate 0 for Kevin and API/Vafflemutt review.
- No runtime code, schema, fixture, package version, provider, network, API,
  Better Stack, database, workspace, git publication, or release action changed.

## 2026-09-10 — Slice 0 plan approved

- API/Vafflemutt approved the identity-source plan and confirmed SBE ownership
  of the correction.
- Froze the distinction between required payload content and identity domain:
  `subject_id` must be exact and present, while `capture_id` remains derived
  only from native run ID, native result ID, reason, and detail code.
- Added negative requirements for same-result subject mismatch and hypothetical
  subject-only rehashing.
- Authorized provider-free discovery, implementation, and qualification within
  the existing no-I/O/no-mutation fence. External operations and release remain
  separately gated.

## 2026-09-10 — Slice 0 identity-source audit complete

- Enumerated every runtime status/refusal site and the identity available at
  that point.
- Confirmed the native exact reader validates content, receipt, journal,
  checkpoint, snapshot, and workspace bindings but needs a local explicit
  caller/result/receipt result-ID equality check for this consumer contract.
- Froze real correlations as validated result/receipt run identity plus the
  sole validated workspace subject. A run mismatch or zero/multiple subjects
  produces no status.
- Split the conceptual unsupported-service and invalid-subject-count branches:
  only unsupported service with one proven subject can emit an honest
  `ineligible_route` status.
- Preserved capture-status v1 and semantic-contract v5's run/result/reason/detail
  identity domain. Subject remains required content authenticated by the exact
  source join, not by changing the capture-ID formula.
- Paused at Review Gate 0 before runtime, fixture, schema, or test changes.

## 2026-09-10 — Slices 1–2 implementation and source qualification

- Replaced runtime use of the fixture-style status helper with a new public
  explicit-correlation constructor and corrected capture-ID derivation to the
  frozen manifest domain.
- Preserved the existing public fixture-helper signature for consumer
  compatibility and added a public exact-source status validator.
- Added the local caller/result/receipt equality guard plus run and sole-subject
  validation before every emitted runtime status.
- Split unsupported service from invalid subject cardinality and threaded one
  proven correlation context through all later refusal branches.
- Added distinct-input, no-sentinel, result mismatch, run mismatch, subject
  ambiguity, subject-only identity-domain, exact-source validation, public
  export, and supported-service regressions.
- Passed 39 editorial-review tests with one expected skip, 19 release/smoke
  tests with one expected skip, and 38 adjacent terminal/native tests with four
  expected skips. Changed Python files compile and diff hygiene is clean.
- Preserved API's existing synthetic-helper call and passed its five-test intake
  guard unchanged against the SBE source overlay.
- Paused for API/Vafflemutt source-candidate review before versioning or
  installed-wheel qualification.
