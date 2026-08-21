# SBE 0.4.14 Known Limitations

- No filesystem/provider transaction exists. A provider request accepted before its
  identity is durably recorded remains an ambiguous submission requiring review.
- Deterministic local request or idempotency keys are not proof of provider-side
  idempotency.
- Retained historical initial-authoring evidence that cannot prove one exact wave
  fails as `initial_wave_lineage_unjoinable`; SBE does not synthesize lineage.
- A retained workspace must be restored at its stable logical absolute path with
  its complete exact snapshot. Arbitrary changed bytes cannot be blessed.
- The installed qualification is provider-free and qualification-only. It neither
  grants production authority nor proves account-wide reservation/billing policy.
- API-owned cross-run reservations, quotas, circuit breakers, entitlements,
  PostgreSQL/R2 transactionality, and billing reconciliation remain outside SBE.
- `python -m astrowoof_natal_authoring.external_authority_qa` may emit a harmless
  eager-import warning. The supported console command
  `astrowoof-external-authority-qa` is clean.
