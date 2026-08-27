# API Slice 7 Review — Joint Consumer Catalog

Date: 2026-08-27  
Reviewer: AstroWoof API agent  
Scope: public-artifact-only candidate review; no provider, retained-QA, deployment,
or production-pin activity.

## Result

**Approved as the SBE-owned public catalog handoff.** The catalog is a useful and
appropriately narrow bridge: it identifies the owner of each scenario, distinguishes
sealed package evidence from runtime qualification components and API-required
fixtures, and does not attempt to fabricate API lease/capacity truth.

This approval does **not** close the plan's joint composed-system gate by itself.
That gate remains open until the API consumes this catalog through its real
translator/persistence/scheduler adapters and emits the corresponding API receipt.
SBE may proceed with Slice 8's provider-free release qualification in parallel, but
tag/adoption should continue to require the eventual joined campaign result.

## Verification performed

- Read `adversarial_consumer.py`, the packaged `catalog.v1.json`, and its focused
  regression tests.
- Ran the candidate source-tree focused test using only a source-path override:
  `3 passed`.
- Built an isolated candidate wheel from the current SBE working tree and installed
  it into an isolated target directory. The installed public package, rather than
  the API's currently pinned SBE 0.4.25 installation, exposed the new reader and
  validator.
- The installed candidate returned the declared contract, 15 cases, 9 packaged
  fixtures, and catalog digest
  `eea70ce9fed3c1ee986454dbac8e71e5e39b266f895628cd8adb2e53e9eab01e`.
- The reader revalidated the literal SHA-256 for every packaged fixture. No source
  tree `run.json`, packet/prompt file, log, provider identifier, workspace, network
  connection, provider invocation, or retained-QA resource was used.

## Fixture-by-fixture consumer mapping

| Catalog cases | Owner | API consumption plan |
| --- | --- | --- |
| `initial_six_member_topology`, `provider_pending_4_plus_2`, `local_retry_transition`, `optional_critic_after_delivery` | SBE | Bind the named qualification components only through their public SBE readers/validators and feed their public outputs to real API worker adapters. |
| `authority_ordinary_action`, `ambiguous_provider_submission`, `providerless_denial_terminalization`, `providerless_batch_denial`, `operator_retirement` | SBE | Validate the sealed fixture with the SBE public validator first; then assert the real API's authority, refusal, custody, and terminal/publication branches. |
| `muffin_review_capacity`, `provider_not_due_wait`, `malformed_contradictory_evidence`, `partial_batch_usage` | Joint | Re-run through real API translation and scheduler/persistence paths. Muffin's narrow review-capacity path is already represented by Slice 2A, but the catalog case will be the stable joined fixture reference. |
| `expired_lost_lease`, `three_run_starvation` | API | Materialize exclusively with API repositories/services and the shared simulation clock. No SBE native assertion or native artifact will be invented for either case. |

## Required API-side guardrails for joined execution

1. Call `validate_adversarial_consumer_catalog()` before using the catalog, and call
   the appropriate public SBE validator before using each sealed fixture or
   qualification component.
2. Treat each catalog assertion as a declared acceptance requirement, not prose.
   The API consumer must maintain a closed case-id-to-real-adapter/assertion mapping;
   an unknown case, evidence kind, or assertion must fail closed. The catalog's
   assertions are intentionally strings, so it is the API joined receipt—not a
   reconstructed SBE interpretation—that must record which concrete API assertion
   discharged each one.
3. Qualification-component references are contract identities rather than static
   fixture bytes. API must consume the associated runtime public receipt through its
   existing/new reader and cannot infer any missing native meaning from a workspace.
4. The catalog is an inventory and integrity fence, not a claim that SBE has executed
   API-owned tests. In particular, lease replacement and three-run fairness remain
   API materialization plus production-service proof.

## Review conclusion

No SBE correction is required for the catalog handoff. The ownership split, sealed
fixture hashes, public-reader boundary, and candidate-wheel behavior all match the
joint plan. API Slice 8 / the remaining composed work can now consume this exact
catalog, with the joined acceptance receipt kept as the final cross-repository gate.
