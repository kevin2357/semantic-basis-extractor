# SBE 0.4.15 Known Limitations

- The exact predicate responsible for the historical retained QA rejection is
  unknown because the rejected inspection bytes were not preserved. This release
  does not retroactively claim an empty action inventory.
- No filesystem/provider transaction exists. Provider acceptance before durable
  identity remains an ambiguous submission requiring review.
- Deterministic local keys are not proof of provider-side idempotency.
- A retained workspace must be restored at its stable logical absolute path with
  its complete exact snapshot; arbitrary changed bytes cannot be blessed.
- Qualification receipts are provider-free evidence only. They grant no production
  authority and prove no account-wide reservation or billing policy.
- API-owned reservations, quotas, circuit breakers, entitlements, PostgreSQL/R2
  transactionality, and billing reconciliation remain outside SBE.
- `python -m astrowoof_natal_authoring.external_authority_qa` may emit a harmless
  eager-import warning. The supported console command is clean.
