# Legacy Provider-Pending Bridge Compatibility — Sprint 1 Evidence

Status: Slices 0–4 complete; 0.4.17 installed patch candidate qualified; final
immutable release authorization pending

- External OpenAI/network calls: 0
- Local scripted retrieval GETs: 6 during installed Slice 1 qualification
- POST/create/submit/retry calls: 0
- Provider credentials/network: none
- Spend: USD 0
- Retained QA workspaces touched: 0
- Runtime/source changes: narrow reconciliation binding-integrity preflight
- Schema changes: none
- Candidate version change: `0.4.16` → `0.4.17`
- Tag/publication changes: none
- Current repository branch: `main`
- API request retained as:
  `API Agent Compatibility Qualification Request.md`
- Qualification conclusion: immutable 0.4.16 requires the narrow Slice 4 patch
  before the retained-workspace bridge can be approved.
- Planning gate: owner and API accepted `PLAN.md`; Slice 0 completed below.

## Slice 0 evidence

- Frozen recipe:
  `results/legacy-provider-pending-fixture.v1.json`.
- Recipe SHA-256:
  `e004817f68cc7f5a6572e56f1a019e742dd190ecd11e7a02b553cf540e551b33`.
- Fixture manifest: `results/fixture-manifest.json`.
- Command contract: `SLICE 0 - FROZEN FIXTURE AND COMMAND CONTRACT.md`.
- Test: `test_legacy_provider_pending_bridge_compatibility.py`.
- Focused bridge and provider-capacity result: 32 passed.
- Valid complete snapshot, six provider identities, v0.5 not-due→due projection,
  maximum-four SBE selection, no external-authority projection, and byte-identical
  read-only inspection proved.
- Provider calls/retrievals, credentials/network, spend, and retained workspace
  access: 0.
- Runtime/source/schema changes: none; test and sprint artifacts only.
- Gate: paused for owner/API review before Slice 1.

## Slice 1 evidence

- Exact wheel SHA-256:
  `56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`.
- Qualification test is opt-in through
  `SBE_RUN_INSTALLED_BRIDGE_QUALIFICATION=1` so ordinary source suites do not
  repeatedly construct an installed virtual environment.
- Fresh installed-wheel result: 4 passed.
- Real public command retrieval sequence: four GETs, then two GETs, then zero-GET
  nonmutating `not_due`.
- Total unique GET paths: 6. POST/create/submit/retry count: 0.
- Authorization/grant input variants rejected: 4.
- Installed native result/publication receipt validation: pass.
- External network/provider calls/spend: 0 / 0 / USD 0.
- Retained QA workspace access: 0.
- Runtime/source/schema changes: none; tests and sprint evidence only.
- Finding: no 0.4.16 compatibility patch is indicated by Slice 1.
- Gate: paused before Slice 2.

## Slice 2 evidence

- Matrix document: `SLICE 2 - REPLAY REFUSAL AND TEMPORAL BRIDGE MATRIX.md`.
- Focused result: 9 passed, 1 installed-wheel opt-in test skipped.
- Completed scripted retrieval: four durable response-evidence files; complete
  snapshot validation passed; lifecycle v0.6 validation passed; checkpoint basis
  changed only after the retrieval checkpoint.
- Provider identity conflict: typed native review; original identities preserved.
- Incomplete snapshot: refusal before retrieval.
- Missing timing/provider identity: malformed action excluded from retrieval.
- Binding/run-identity mismatch: affected action was retrieved by immutable 0.4.16;
  this violates the frozen Slice 2 fail-closed requirement and activates the
  conditional patch-design gate.
- External OpenAI/network calls: 0. Provider create/POST/submit/retry: 0.
- Spend: USD 0. Retained QA workspace access: 0.
- Runtime/source/schema changes: none; qualification tests and sprint evidence only.
- Gate: owner/API decision required before runtime correction.

## Slice 4 evidence

- Contract record: `SLICE 4 - WHOLE-CYCLE BINDING INTEGRITY FENCE.md`.
- Whole-inventory preflight occurs before due-member selection or provider I/O.
- Malformed member positions qualified: first due member and fifth deferred member.
- Both outcomes: `review_required`; retrieval count 0; no result checkpoint;
  authoritative workspace hashes unchanged.
- Consistent bridge/lifecycle/capacity result: 46 passed, 1 installed-wheel opt-in
  test skipped.
- Complete repository result: 592 passed, 29 existing environment/opt-in skips.
- External OpenAI/network calls: 0. Provider create/POST/submit/retry: 0.
- Spend: USD 0. Retained Aster access: 0.
- Source change is limited to reconciliation preflight plus focused regression and
  sprint evidence.
- Gate: build a fresh immutable patch candidate, rerun the installed-wheel bridge
  qualification, and obtain API release approval.

## 0.4.17 candidate installed-wheel evidence

- Candidate wheel SHA-256:
  `49ba8ddfb73d8f58786ceabe1d0bdbea49aaab39914a4336dbad73a70b783923`.
- Candidate wheel bytes: 893739.
- Closed receipt: `results/patch-candidate-installed-qualification.v1.json`.
- Fresh installed result: 10 passed.
- Consistent inventory: exact first-four then remaining-two GET identities; sealed
  native reconciliation evidence; subsequent not-due replay nonmutating.
- Malformed first and fifth members: `review_required`, zero GET, exact typed
  diagnostic event, zero native publication, authoritative bytes unchanged.
- External OpenAI/network calls: 0. Provider POST/create/submit/retry: 0.
- Spend: USD 0. Retained Aster access: 0.
- The candidate is not the final immutable artifact: final wheel bytes must be
  rebuilt reproducibly from the committed release-source identity.
