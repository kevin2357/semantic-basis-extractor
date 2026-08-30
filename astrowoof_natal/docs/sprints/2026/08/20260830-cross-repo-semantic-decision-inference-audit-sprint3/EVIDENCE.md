# Evidence — cross-repository semantic decision inference audit

## Current gate

Slices 0–2 are complete. Joint review is required before Slice 3.

## Slice 0

- Native catalog: `SLICE 0 - SBE PUBLIC FACT CATALOG.md`.
- Registry shape: `SEMANTIC DECISION REGISTRY TEMPLATE.md`.
- Source surfaces inspected: lifecycle contracts/inspection, temporal lifecycle,
  post-fan-in local work, retry lineage, native transition publication and
  availability, external authority v1/v2, reconciliation, terminal review,
  providerless denial, closeout, operator retirement, package exports, fixtures,
  and consumer handoffs.
- Installed compatibility basis: SBE `0.4.32`, SPC `0.11.1`.
- Production source/schema changes, provider activity, retained-QA access,
  deployment, and spend: zero.
- Historical Slice 0 gate: API review before Slice 1; satisfied.

## Slice 1

- Decision inventory: `SLICE 1 - API DECISION SINK INVENTORY.md`.
- API source basis: `main` after Sprint 60 commit `676cb3a`.
- Production areas inspected: SBE worker and runtime, lifecycle consumers,
  native terminal and transition ingestion, provider orchestration, authority
  admission/dispatch, queue/capacity handling, publication/cleanup, and bounded
  operator recovery services.
- Inventory rows: 20 primary worker/runtime sinks, 10 native-result/authority/
  settlement sinks, 10 product/recovery sinks, and 6 subprocess evidence-
  precedence sites.
- Explicit unresolved audit target: lifecycle review versus v0.2 terminal
  review versus bounded review mapping.
- Production source/test/schema changes, provider activity, retained-QA access,
  deployment, and spend: zero.

## Slice 2

- Completed registry: `SLICE 2 - SEMANTIC DECISION REGISTRY.md`.
- Installed API dependency identity:
  - SBE `0.4.32`, SHA-256 `c45cd46…493d6e`;
  - SPC `0.11.1`, SHA-256 `dc345cd3…a7da612`.
- Source traces include exact availability preflight, lifecycle version routing,
  provider reconciliation, local resume, v1/v2 constrained authority,
  invocation-bound terminal review, native transition ingestion, API queue/run/
  reading effects, capacity release, settlement, publication, cleanup, and named
  operator recoveries.
- Registry rows: 28; all 46 Slice 1 sites are covered through explicit ID joins.
- Factual review target: three distinct review-shaped surfaces and their outer
  API terminalization/custody effects.
- Focused API verification: 10 passed. Covered invocation-result precedence,
  explicit preflight identity, conflicting authority refusal, lifecycle review
  upgrade, sealed terminal preflight, and sealed nonterminal routing.
- Production source/test/schema changes, provider activity, retained-QA access,
  deployment, and spend: zero.
