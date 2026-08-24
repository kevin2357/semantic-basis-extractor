# Legacy Provider-Pending Bridge Compatibility — Sprint 1 Evidence

Status: Slices 0–1 complete; installed 0.4.16 bridge qualification passed

- External OpenAI/network calls: 0
- Local scripted retrieval GETs: 6 during installed Slice 1 qualification
- POST/create/submit/retry calls: 0
- Provider credentials/network: none
- Spend: USD 0
- Retained QA workspaces touched: 0
- Runtime/source/schema changes: none
- Version/tag/release changes: none
- Current repository branch: `main`
- API request retained as:
  `API Agent Compatibility Qualification Request.md`
- Planning conclusion: existing 0.4.16 behavior appears suitable for focused
  installed-wheel compatibility qualification; no patch is presumed.
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
