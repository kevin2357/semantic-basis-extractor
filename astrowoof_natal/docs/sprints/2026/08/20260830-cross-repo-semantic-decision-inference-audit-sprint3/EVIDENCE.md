# Evidence — cross-repository semantic decision inference audit

## Current gate

Slices 0–1 are complete. Slice 2 evidence-source tracing is next.

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
