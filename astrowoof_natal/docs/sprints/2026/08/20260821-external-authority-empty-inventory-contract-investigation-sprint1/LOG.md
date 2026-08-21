# External-Authority Empty-Inventory Contract Investigation — Sprint 1 Log

## 2026-08-21 — Background received

- Received the API-authored incident background for the retained QA recovery.
- Confirmed the retained workspace is evidence only and must not be mutated or
  resubmitted.

## 2026-08-21 — Pre-sprint reconnaissance

- Traced external-authority request validation, public request reading, lifecycle
  classification, inspection projection, and lifecycle v0.5 semantic validation.
- Confirmed SBE 0.4.14 request validation already rejects empty action inventories.
- Confirmed request-building failures are intended to become typed native-review
  refusals.
- Determined the API error collapses five predicates and does not itself prove an
  empty action inventory.
- Identified an explicit nonempty lifecycle-branch invariant as worthwhile defense
  in depth even though request validation currently supplies it transitively.
- Ran 59 focused provider-free tests successfully; 4 JSON Schema tests skipped on
  the lean host environment.
- Created the pre-sprint huddle and draft sliced plan. No source, schema, native
  state, provider, API, database, or release behavior changed.

## 2026-08-21 — Slice 0 failure-shape reconnaissance

- Added a provider-free production-shaped reproducer through real
  `inspect_lifecycle()` for exact and bounded initial-wave workspaces.
- Proved both normal routes publish six exact action IDs and satisfy all five API
  external-authority predicates without mutating run state or snapshot bytes.
- Proved an inadmissible stored-wave member becomes a typed
  `native_state_inconsistent` refusal rather than an empty request.
- Mutated each API predicate independently. Native v0.5 validation rejects wrong
  eligibility, capacity, and empty action IDs, but currently accepts a wrong branch
  reason and non-null `not_before`.
- Recorded the exact retained predicate as unresolved because its raw rejected
  inspection is unavailable; no longer treats empty inventory as proven.
- Provider calls: 0. Spend: USD 0. Retained workspace access: none.
- Slice 0 is complete and paused for API review.

## 2026-08-21 — Slice 0 API review

- API approved the revised evidence boundary and the two proven v0.5 gaps.
- Accepted the requirement that installed-wheel qualification use packaged/public
  fixtures rather than importing source-tree test helpers.
- Accepted conditional branch semantics: empty IDs remain correct for `command=none`
  refusal, but are forbidden for `await_external_authority`.
- No API-side change was requested. Slice 1 may proceed.

## 2026-08-21 — Slice 1 contract and diagnostic proposal

- Proposed correcting lifecycle inspection v0.5 in place because the tightened
  combinations were already invalid by handoff semantics and are refused by API.
- Defined complete conditional invariants for `await_external_authority` and
  `command=none` typed refusal.
- Kept external request, typed refusal, and constructed-document failure distinct.
- Proposed conditional v0.5 JSON Schema constraints plus exact semantic joins.
- Proposed enriching existing typed events rather than expanding the closed event
  name vocabulary.
- Defined a redacted failed-predicate vocabulary and text-log fields.
- Froze no schema/runtime behavior; paused for joint approval.

## 2026-08-21 — Slice 1 API approval

- API approved in-place v0.5 tightening and both conditional command tables.
- API approved event reuse, counts/digests in typed events, the closed predicate
  vocabulary, and raising for constructed contradictions.
- Recorded schema/semantic parity, full timing/readiness conditionals, sink-failure
  isolation, incident uncertainty, and packaged-fixture qualification requirements.
- Slice 2 may proceed.

## 2026-08-21 — Slice 2 native validator and classification hardening

- Tightened lifecycle inspection v0.5 in place in packaged JSON Schema and Python
  semantic validation.
- Enforced the full approved request and refusal command-conditional tables,
  including capacity reason/readiness and both timing fields.
- Preserved v0.4, valid request/refusal byte shape, public states, and provider/API
  ownership boundaries.
- Expanded semantic and schema mutation coverage for every approved predicate.
- Focused evidence: 94 passed, 5 environment-dependent schema tests skipped;
  Python compilation and JSON parsing passed.
- Provider calls: 0. Spend: USD 0. Retained workspace access: none.
- Slice 2 is complete; structured diagnostic enrichment remains Slice 3.

## 2026-08-21 — Slice 3 structured observability

- Added one deterministic closed predicate projection shared by validation, typed
  diagnostics, and text logs.
- Enriched existing request-selected, refusal, branch-selected, and execution-failed
  events without adding an event name/schema version.
- Added safe lifecycle completion/failure logging with action counts, digests,
  presence flags, refusal reasons, and sorted predicate names.
- Proved success/refusal event order, contradiction diagnostics, sink-failure
  isolation, byte-identical state/snapshot, and protected-sentinel absence.
- Focused evidence: 118 passed, 5 environment-dependent schema checks skipped.
- Provider calls: 0. Spend: USD 0. Retained workspace access: none.
- Slice 3 is complete.

## 2026-08-21 — Slice 4 provider-free regression matrix

- Added real public inspection coverage for ordinary action sets, absent prepared
  inventory, exact/bounded initial waves, incomplete snapshots, and writer races.
- Added request inventory/binding and outer lifecycle identity mutation coverage.
- Re-ran lineage, constrained execution, lifecycle consumer/closeout, and typed
  event suites.
- Confirmed source-tree helper reuse remains test-only and will not enter the
  installed-wheel qualification.
- Focused evidence: 105 passed, 5 environment-dependent schema checks skipped.
- Provider calls: 0. Spend: USD 0. Retained workspace access: none.
- Slice 4 gate passed.

## 2026-08-21 — Slice 5 installed-wheel qualification and handoff

- Versioned the qualification receipt forward to v2 while preserving the published
  closed v1 contract.
- Added request/refusal lifecycle-conditional assertions to the holistic public
  runtime qualification.
- Built and isolated-installed the 0.4.14 candidate wheel; its SHA-256 is
  `798381344ea728e851663db3ca2afc5a968205ddce951aea7efce0200398b8e3`.
- Produced a passing v2 receipt plus sanitized request, grant, refusal, and ordinary
  action fixtures from the installed artifact.
- Published exact API selection requirements, compatibility guidance, and retained
  workspace handling in the consumer handoff.
- Combined lifecycle/external-authority verification: 97 tests run, 6 existing
  environment-dependent schema checks skipped, all remaining tests passed.
- Provider calls/spend/retained workspace access: 0 / USD 0 / none.
- Slice 5 is complete and paused for API fixture/consumer review before Slice 6.

## 2026-08-21 — Slice 5 API approval

- API approved the fixtures, installed-wheel qualification, lifecycle contract, and
  consumer handoff conditional on one prose-only correction.
- Corrected both handoff reason-code literals from the descriptive
  `external_authority_required` to the actual validated contract value
  `spend_authorization_required`.
- No source, schema, fixture, qualification, or runtime behavior changed in response
  to review. Slice 5 is approved for commit and release preparation.

## 2026-08-21 — Slice 6 closeout and release decision

- The first complete-suite pass exposed two stale test-integration assumptions in
  cross-file schema resolution and observation-bound digest normalization; neither
  represented a runtime defect.
- Corrected those assumptions and reran all 558 tests successfully with 27 existing
  environment-dependent skips.
- Built and isolated-installed the post-Slice-5 0.4.14 candidate wheel, SHA-256
  `59053ac273d21f6d7b252d34b23a0757bacf1420baa855aee2b7612676d3f12b`.
- Installed release smoke and external-authority qualification both passed through
  advertised console commands outside the source package path.
- Privacy/integrity scans, Python compilation, packaged JSON parsing, and diff
  whitespace checks passed.
- Recommend fresh immutable patch `0.4.15`; no version bump, tag, or publication has
  occurred pending explicit owner authorization.

## 2026-08-21 — 0.4.15 release closeout begins

- Kevin explicitly authorized version bump, tag, and publication after final API
  approval.
- Selected fresh immutable patch `0.4.15`; preserved `0.4.14` unchanged.
- Reconciled the consumer handoff opening status before release finalization.
- Tagging and publication remain pending deterministic artifact qualification and
  release-evidence lock.
- Built 0.4.15 twice at fixed source epoch `1787324603`; wheel bytes matched.
- Installed release smoke, external-authority v2 qualification, provider-pending
  qualification, resource inventory, and package identity checks passed.
- Locked the exact wheel and initial release evidence in commit
  `4ccf3813aa1010500298af9e68e4f3351b5a1ea0`.
- Qualified wheel SHA-256:
  `f557b439fa3096bb1c33f020adc4be40fb3bb749857bc8c3c7a4715cc131a052`.
