# AstroWoof Natal Authoring 0.4.1 Known Limitations

- Atomicity is semantic and protected by SBE's cross-process single-writer
  protocol; several workspace files are not one filesystem transaction.
- Provider-bound, consumed, reported, or ambiguously submitted actions cannot be
  denied as providerless.
- Deterministic local identities do not establish provider idempotency.
- Recovery accepts only the exact durable batch intent and known write set; it
  cannot bless arbitrary changed workspace bytes.
- The operation does not mutate API reservations, capacity, leases, or databases.
- Batch size is a fixed contract maximum of 32 actions.
- The 0.4.0 bounded-Natal limitation remains: Batch provider authoring is not
  implemented and `service_level=batch` is rejected.
