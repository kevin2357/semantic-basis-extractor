# AstroWoof Natal Authoring 0.3.0

This release adds the supported authoring lifecycle, provider-less denial,
idempotent closeout, and structured-event consumer surface required by AstroWoof
API orchestration.

## Added

- strict versioned contracts for lifecycle inspection, action inventory, negative
  authorization request/result, closeout, execution events, and command results;
- read-only exact-snapshot inspection with explicit provider identity/evidence,
  typed local dependencies, terminal facts, and quiescence;
- single-writer `DENIED_PROVIDERLESS` disposition for exact `PREPARED` and
  unconsumed `AUTHORIZED` actions, with typed fail-closed race results;
- durable idempotent closeout with semantic-result identity and constrained recovery
  at every multi-file write boundary;
- event-name-specific payload catalog, injected Python event sinks, external JSONL,
  and typed stdout JSONL framing;
- `astrowoof-authoring-lifecycle` installed consumer command;
- `astrowoof-lifecycle-smoke` provider-free installed qualification command; and
- packaged schemas, catalogs, and sanitized lifecycle fixtures.

The supported API sequence is stepwise: typed denial, fresh inspection, then
closeout. Closeout deliberately does not accept a denial request, ensuring expected
provider races remain machine-readable domain results rather than exception prose.

## Qualification

- complete repository suite: 214 passed;
- two independent wheel builds: byte-identical;
- exact wheel SHA-256:
  `377c48ed37d337e42dc9392cc7b5e07a81c3b12c2e0638a50bf33ad1b18cd3b0`;
- Windows CPython 3.12.13: clean install, `pip check`, lifecycle smoke, and complete
  deterministic release smoke passed;
- offline Linux amd64 CPython 3.11.15: clean install, `pip check`, lifecycle smoke,
  and complete deterministic release smoke passed;
- installed resource count/digest: 30 /
  `d989f84404c9ef79fe310f938a8d1588b4714c7e971e85af0b0e7c098f931582`;
- wheel entries/cache entries: 58 / 0; and
- new provider operations and spend: zero / `$0`.

Publication is complete. The immutable annotated tag targets release commit
`d96e2e4e0809f14d574d3241fa2909aa3cdb137c`; authenticated download verification
matched the qualified wheel SHA-256 above. Detailed post-publication coordinates are
recorded in `release-manifest.json`.
