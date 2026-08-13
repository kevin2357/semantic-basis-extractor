# API Worker Integration - AstroWoof Natal Authoring 0.3.0

Pin the immutable 0.3.0 wheel only after publication and verify SHA-256
`377c48ed37d337e42dc9392cc7b5e07a81c3b12c2e0638a50bf33ad1b18cd3b0`.
AGF 0.6.0, SPC 0.10.0, pyswisseph, and other worker pins remain unchanged.

Use the installed `astrowoof-authoring-lifecycle` command or documented public
Python functions. Do not import implementation internals or edit native JSON.

Required orchestration:

1. restore the exact workspace under the stable logical path and hold the API lease;
2. inspect and persist the mapped status into API-owned authority;
3. when applicable, submit one exact negative-authorization request and consume its
   typed result;
4. obtain a fresh inspection after every mutation;
5. close out without passing a denial request; and
6. evaluate cleanup using closeout plus API-owned lease/product/storage policy.

Only an applied or exact idempotent native denial supports API reservation-release
evaluation. SBE never releases API funds. Active or ambiguous provider work remains
protected; reported/reconciled work remains evidence without falsely remaining
outstanding.

Worker reconciliation reads and validates SBE public/lifecycle state, then persists
the mapped API status. HTTP status endpoints read persisted API-owned state and never
execute SBE or depend on a live workspace.

Detailed contracts:

- [Authoring Lifecycle Consumer Handoff](../../docs/post_extraction_authoring/Authoring%20Lifecycle%20Consumer%20Handoff.md);
- [Spend Authorization Consumer Handoff](../../docs/post_extraction_authoring/Spend%20Authorization%20Consumer%20Handoff.md);
- [Provider Spend Enforcement](../../docs/post_extraction_authoring/Provider%20Spend%20Enforcement.md);
- [Durable Workspace Contract](../../docs/post_extraction_authoring/Provider%20Disclosure%20and%20Durable%20Workspace%20Contract.md);
- [Qualitative Critic Findings Consumer Contract](../../docs/post_extraction_authoring/Qualitative%20Critic%20Findings%20Consumer%20Contract.md); and
- [packaged contract catalog](../../src/astrowoof_natal_authoring/resources/contracts/contract-catalog.json).

Before promotion, run `astrowoof-lifecycle-smoke --require-installed` against the
exact pinned wheel in the worker image.
