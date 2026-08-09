# API Worker Integration - AstroWoof Natal Authoring 0.2.2

Pin the immutable wheel only after publication and verify SHA-256
`98e8ab142bc4c1dc97fdc53019fb6d2e16d23736f12ca9085119b79fdc842b7e`.
AGF 0.6.0, SPC 0.10.0, pyswisseph, and other worker pins remain unchanged.

Worker reconciliation validates `public-run.json` and persists mapped status
to API-owned state. HTTP status endpoints read PostgreSQL/API authority only;
they never execute SBE or depend on live worker scratch.

For affected 0.2.1 workspaces, follow `RECOVERY ADVISORY.md`. The API owns the
exclusive lease, backup/storage lifecycle, repair-report retention, and any
later authorization. Do not consume action 2 during repair.

For critic ingestion, require
`astrowoof.qualitative_critic_findings.v0.1`, verify artifact hashes, retain the
complete JSON privately, and index only bounded operational fields. Use the
packaged sanitized fixture, not the old Kevin/Ella files.

Detailed authority:

- [Spend Authorization Consumer Handoff](../../docs/post_extraction_authoring/Spend%20Authorization%20Consumer%20Handoff.md);
- [Provider Spend Enforcement](../../docs/post_extraction_authoring/Provider%20Spend%20Enforcement.md);
- [Durable Workspace Contract](../../docs/post_extraction_authoring/Provider%20Disclosure%20and%20Durable%20Workspace%20Contract.md);
- [Qualitative Critic Findings Consumer Contract](../../docs/post_extraction_authoring/Qualitative%20Critic%20Findings%20Consumer%20Contract.md); and
- [packaged contract catalog](../../src/astrowoof_natal_authoring/resources/contracts/contract-catalog.json).

SBE owns per-run integrity and artifacts. The API continues to own cross-run
reservations, quotas, circuit breakers, entitlements, billing reconciliation,
queues, leases, persisted HTTP status, storage, and promotion policy.
