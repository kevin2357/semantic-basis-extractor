# SBE 0.4.27 Compatibility

- Python: 3.11 or newer.
- Semantic Projection Core: exactly 0.11.1.
- Lifecycle v0.5/v0.7, temporal v0.6, ordinary external-authority v2, native
  transition, provider-spend, retirement, and accounting contracts remain intact.
- Exact and bounded interactive Response routes share the corrected custody/local
  precedence rule.
- Existing Batch routes remain reconciliation-compatible; this release does not
  add ordinary-v2 Batch dispatch.
- The new receipt, bundle, schemas, fixture, Python exports, and CLI are additive
  qualification-only surfaces.
