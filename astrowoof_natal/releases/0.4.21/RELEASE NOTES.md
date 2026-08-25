# AstroWoof Natal Authoring 0.4.21

Status: authorized release candidate

SBE 0.4.21 adds a privacy-minimized provider-economics transaction tape for
long-term accounting and performance analysis. Exact and bounded interactive
actions and Batch rounds can be projected from validated native snapshots through
a packaged Python reader or read-only CLI.

The contract is append-only and revisioned. Provider settlement may be followed by
later editorial/native finalization without overwriting earlier evidence. One
Batch round remains one paid transaction; ordered members are evidence and missing
member costs are never invented. Unknown and zero remain distinct.

SBE estimates, provider-reported usage/money, and API-authoritative billing
reconciliation remain separate facts. The export changes no provider execution,
lifecycle, spend, custody, settlement, or delivery behavior.

## Qualification

- Artifact source commit: `7fae397da025fb2da8919c2d73072c34ed63c222`.
- Fixed build epoch: `1787638617`.
- Full source suite: 683 passed; 36 expected environment/opt-in skips.
- Two byte-identical candidate wheels; SHA-256
  `44928211effd3ef6593d729ebe70ad74ea5ac0c603e100e815588d3f4d27ade2`.
- Generic installed release smoke: pass with 50 cards and four summaries.
- Installed provider-economics qualification: pass; receipt SHA-256
  `d2cbcdf6eb6dd98b1a124f5e5c21ea58a969f73212c5ccdc74c8c0e60440b8b0`.
- Exact pinned SPC 0.11.0 environment: `pip check` pass.
- External provider/network calls and spend: 0.

API consumer review and product-owner authorization approve immutable 0.4.21
tagging and publication. API worker pinning/deployment remains deferred until the
separate ingestion sprint qualifies fixture, replay, and privacy behavior.
