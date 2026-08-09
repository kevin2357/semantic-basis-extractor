# API Worker Integration - AstroWoof Natal Authoring 0.2.1

## Pin and qualify

After publication, install `requirements-api-worker.txt` with `--no-deps
--require-hashes`. Before publication, use the locally reviewed wheel only
after verifying SHA-256
`0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`.

Replace only the SBE 0.2.0 wheel/version/hash in the existing worker lock. AGF
0.6.0, SPC 0.10.0, pyswisseph, and all transitive wheel pins remain unchanged.
Run `astrowoof-release-smoke --require-installed` inside the final Linux image;
promotion requires top-level `status: pass`, `DELIVERY_COMPLETE`, and resource
aggregate
`439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.

Worker reconciliation reads and validates SBE's `public-run.json`, then
persists the mapped API status. HTTP status endpoints read persisted API-owned
state and never execute SBE or depend on a live workspace.

## Contract handoff

All orchestration and ownership instructions remain those reviewed for 0.2.0:

- [0.2.0 API Worker Integration](../0.2.0/API%20WORKER%20INTEGRATION.md);
- [Spend Authorization Consumer Handoff](../../docs/post_extraction_authoring/Spend%20Authorization%20Consumer%20Handoff.md);
- [Provider Spend Enforcement](../../docs/post_extraction_authoring/Provider%20Spend%20Enforcement.md); and
- [packaged contract catalog](../../src/astrowoof_natal_authoring/resources/contracts/contract-catalog.json).

SBE continues to own per-run ceilings, exact action binding, local accounting,
resume safety, disclosure minimization, acceptance, QA, provenance, snapshots,
and delivery construction. The API continues to own cross-run reservations,
quotas, circuit breakers, product entitlements, billing reconciliation, queues,
leases, persisted HTTP status, storage, and promotion policy.
