# Retained Initial-Wave Next-Action Fence Sprint 1 Log

## 2026-08-20 — Sprint proposed

- Read the API Sprint 33 next-action contract request and surrounding Background,
  Plan, Log, and Evidence documents.
- Confirmed SBE 0.4.13 publishes an empty branch action inventory for
  `await_external_authority` and does not bind generic resume to a public request.
- Confirmed the existing fresh exact-interactive route can infer initial-wave mode
  from empty pass-attempt state without first excluding historical spend/provider
  lineage.
- Proposed lifecycle inspection v0.5, an independently versioned external-authority
  request, a single-writer constrained continuation fence, and strict initial-wave
  anti-reentry policy.
- No implementation, retained-workspace access, provider call, or spend occurred.
- Sprint is paused for Kevin/API plan review.

## 2026-08-20 — API plan review incorporated

- Preserved the API agent's detailed review as a sprint artifact.
- Accepted inline lifecycle v0.5 request publication, a closed aggregate API grant,
  lexical ordinary-action ordering, semantic initial-wave ordering, and the typed
  `initial_wave_lineage_unjoinable` refusal.
- Fixed the intended single-writer boundary through durable pre-submit intent while
  explicitly excluding slow provider I/O from the lock.
- Retained the irreducible post-intent/pre-identity provider gap as fail-closed
  ambiguity rather than overstating aggregate-grant atomicity.
- No runtime implementation, retained-workspace access, provider call, or spend
  occurred. Sprint remains paused for Kevin authorization to begin Slice 0.

## 2026-08-20 — Final planning clarification and approval

- Made `external_authority_refusal` an explicit closed lifecycle v0.5 companion
  object rather than requiring consumers to infer refusal from a null request.
- Added mutual-exclusion and cross-field schema requirements for request, refusal,
  and non-applicable lifecycle states.
- Kevin and the API agent approved the revised sprint direction.
- No implementation, retained-workspace access, provider call, or spend occurred.

## 2026-08-20 — Slice 0 reproduction and mutation map

- Added a provider-free characterization using the production exact-wave
  preparation, authorization, and concurrent create coordinator with a scripted
  transport.
- Added the requested public-path control through the actual `closure.main()`
  resume dispatcher: one generic resume prepares the inferred wave and a second
  generic resume applies the existing v1 authority documents and performs six
  scripted creates without the proposed constrained grant.
- Proved that retained historical initial actions/provider IDs plus empty current
  pass attempts can produce a distinct second six-member inventory in 0.4.13.
- Mapped preparation, authorization, durable all-member intent, provider I/O,
  identity persistence, snapshot, and result-publication boundaries.
- Located the last safe new fence before preparation mutation under the shared
  cross-process writer, with writer release only after durable pre-submit intent.
- Focused controls passed: 3 tests.
- Provider network calls: 0. Retained Aster access: none. Spend: USD 0.
- Paused for API review before Slice 1 schema freeze.

## 2026-08-20 — Canonical nomenclature huddle

- Canonicalized `RIWNAFS` as **ree-WOOF-naffs**.
- Preserved **Native Authority** as the intentional second-layer reading of `NA`,
  while retaining **Next Action** as the formal sprint expansion.
- Recorded complete, compact, and angsty-teen emoji forms.
- Documented the independently verified Norwegian waffle/krumkake and Swedish
  `nafs` linguistic-pastry adjacency.
- Confirmed that the tiny Scandinavian dog-waffle guardian is binding for morale
  and non-authoritative for runtime behavior.

## 2026-08-20 — Slice 1 external-authority contract proposal

- Added the packaged closed-world request/refusal/grant schema and declared
  lifecycle inspection v0.5 without changing the implemented catalog default.
- Froze complete binding disclosure, route-sensitive canonical ordering, canonical
  SHA-256 construction, exact all-or-none grant membership, and initial-wave
  context repetition.
- Froze the lifecycle request/refusal/null branch matrix and separated a native
  inability to publish one exact request from execution-time stale/grant refusals.
- Clarified that requests require a complete valid snapshot while a no-create
  refusal may truthfully report snapshot invalidity or absent exclusivity.
- Kept the six ordinary per-action spend authorization documents as member
  authorities; proposed the new grant as their observation-bound invocation
  envelope on the v0.5 constrained path.
- Documented positive grant versus withheld authority/providerless denial and the
  irreducible post-intent/pre-provider-ID ambiguity boundary.
- Added sanitized initial-wave request/grant/refusal and ordinary-action fixtures
  plus digest, ordering, all-or-none, closed-schema, and observation tests.
- Focused installed-environment result: 9 tests passed with real Draft 2020-12
  schema validation. Provider/network calls: 0. Spend: USD 0.
- Paused for the required API contract review before Slice 2/runtime work.

## 2026-08-20 — Slice 1 API review corrections

- Added full lifecycle-level request and native-refusal fixtures rather than
  relying only on standalone authority objects.
- Added semantic validation for exact outer lifecycle/request/refusal run,
  observation revision, snapshot, logical-root, and execution-branch joins.
- Added mutations for every cross-boundary identity, branch action inventory, and
  invalid request/refusal combinations.
- Strengthened aggregate-grant validation to validate each complete ordinary
  authorization document's closed shape, schema, action ID, exact binding, digest,
  and reference.
- Added digest-consistent wrong-action and wrong-binding attacks to prove that a
  self-consistent grant cannot bless a mismatched member authorization.
- Focused Linux QA result: 16 tests passed. Provider/network calls and spend: zero.
- Slice 1 remains paused for final API contract approval.

## 2026-08-20 — Slice 1 approved and Slice 2 completed

- Committed and pushed the approved Slice 1 contract as `01b8aee`.
- Added a provider-free root-level Python builder, semantic validator,
  snapshot-validating reader, schema reader, and `astrowoof-external-authority` CLI.
- Joined exact and bounded initial waves through the existing public prepared-wave
  and binding-bundle validators; ordinary actions use lexical action-ID order.
- Made unchanged-checkpoint exports deterministic by using the snapshot-bound native
  update time rather than reader wall-clock time.
- Revalidated complete workspace state after request construction and refused a
  simulated coherent writer update during the read.
- Rejected CLI output under the native run directory and kept all reader/validation
  operations free of provider access and state mutation.
- Focused suite: 33 tests passed on the lean host, with four optional JSON Schema
  tests skipped consistently with Slice 1. Offline wheel build and isolated Python
  3.11 install succeeded; the installed CLI read the packaged v1 schema.
- Provider/network calls: 0. Spend: USD 0. Retained Aster access: none.
- Corrected an implementation-shape ambiguity before handoff: action preparation
  revision may precede the later lifecycle observation revision after persistence.
  Tests now use `prepared=N`, `observed=N+1`; only a future action revision fails.

## 2026-08-20 — Slice 2 API fail-closed correction

- Restricted initial-wave request publication to a stored wave whose state is
  exactly `AWAITING_SPEND_AUTHORIZATION`.
- Resolved all six semantic wave members against the durable ledger and required
  exactly one matching `PREPARED`, providerless, unconsumed, binding-identical
  action for every member.
- Added production-shaped ledger fixtures and refusal coverage for authorized
  waves, stale wave labels with provider identity/consumption, changed bindings,
  and duplicate action records.
- Focused host result: 36 tests passed with four optional schema tests skipped;
  Linux QA result: all 36 passed with Draft 2020-12 validation active.

## 2026-08-20 — Slice 3 constrained continuation fence

- Added strict runtime validation of the closed aggregate grant and all six complete
  member authorization documents against the current snapshot-bound request.
- Added the supported exact-interactive constrained execution path and CLI inputs:
  `--external-authority-request`, `--external-authority-grant`, and the six existing
  ordered `--spend-authorization` documents.
- Held native single-writer control through current-request reconstruction, exact
  grant validation, all-or-none ledger authorization, and one durable all-member
  `SUBMITTING` intent checkpoint; released it before slow provider creates.
- Reacquired cross-process single-writer control for every returned identity or
  ambiguity outcome and published a complete workspace snapshot after each.
- Removed the legacy public initial-wave authorization route and rejected loose
  initial-wave member authorizations without the snapshot-bound aggregate grant.
- Proved that interruption after durable intent makes replay fail closed before any
  create, while an injected provider-return/identity-persistence gap becomes six
  durable ambiguous submissions and never creates again.
- Focused results: 33 authority tests passed with four optional schema tests skipped
  on the lean interpreter; 40 existing initial-wave/spend tests passed; two targeted
  semantic-closure compatibility tests passed.
- Provider/network calls were scripted only. Spend: USD 0. Retained Aster access:
  none.

## 2026-08-20 — Slice 3 API review correction

- Added an explicit `aggregate_grant_required` refusal when generic exact
  interactive resume encounters a stored initial wave in
  `AWAITING_SPEND_AUTHORIZATION` without the exact external request/grant pair.
- Placed the refusal before wave preparation, state/snapshot persistence, and native
  result publication; fresh initial preparation remains supported.
- Added a public CLI regression proving byte-identical `run.json` and workspace
  snapshot, no changed/native-result publication artifacts, and zero provider calls.
- Updated focused authority result: 34 passed with four optional schema skips.

## 2026-08-20 — Slice 4 one-wave lineage fence

- Replaced the old “all pass attempts empty” inference with a complete native
  admission check before exact-interactive wave preparation.
- Refused orphaned `authoring_initial` ledger actions, pass attempts, binding/join
  artifacts, provider identities, consumption/reporting, response evidence, and
  ambiguity as typed `initial_wave_lineage_unjoinable` evidence.
- Validated a stored exact wave against its contract, six-member binding bundle,
  unique ledger bindings, complete request inventory and bytes, and matching pass
  attempts before treating it as reusable.
- Added the same orphan-lineage fence before generic interactive dispatch so a
  partially retained run cannot bypass wave preparation and enter ordinary pass
  continuation.
- Prevented the public authority reader from relabeling orphaned prepared initial
  actions as an ordinary action set.
- Preserved a valid stored wave—including six durable provider identities—without
  changing its inventory or creating provider work.
- Converted the Slice 0 unsafe-path characterizations into positive refusal
  regressions with byte-identical state and zero provider creates.
- Full semantic-closure suite: 92 tests passed. Focused lineage/public/execution:
  22 passed; combined lineage/execution/initial-wave/spend compatibility: 52
  passed. Network/provider calls and spend: zero.
