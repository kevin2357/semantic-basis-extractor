# SBE 0.4.8 Known Limitations

- The public joined reader requires a complete valid workspace snapshot at its
  stable logical absolute path.
- Legacy initial-wave workspaces without the binding bundle cannot use the joined
  reader and fail closed.
- The bundle authorizes nothing by itself; API must still atomically reserve the
  exact six-member wave and issue all required authorization documents.
- Provider acceptance and local provider-identity persistence cannot form one
  atomic transaction. Identity-less interruption remains ambiguous and
  fail-closed.
- Deterministic local request identities are not asserted as provider idempotency.
- Global reservations, quotas, circuit breakers, product policy, and billing
  reconciliation remain API-owned.
