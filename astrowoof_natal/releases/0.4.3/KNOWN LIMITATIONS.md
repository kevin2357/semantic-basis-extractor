# AstroWoof Natal Authoring 0.4.3 Known Limitations

- Provider retrieval and native checkpoint persistence are not one external
  atomic transaction. A durable provider GET may repeat; submission may not.
- Identity-less interrupted submission remains ambiguous and fail-closed.
- Batch and bounded-Natal bounded reconciliation are unsupported and retain local
  capacity/review rather than inheriting exact-interactive semantics.
- The bounded cycle depends on the provider transport honoring its 15-second GET
  timeout; four retrievals run in one parallel wave.
- Consumers must preserve the original frozen provider launch configuration.
- Capacity release does not release API reservation, dollar exposure, lease,
  database, billing, cancellation, or publication authority.
- Events are redacted, failure-isolated, and non-authoritative.
- The API companion must separately prove capacity-slot release and third-reading
  admission in PostgreSQL-backed orchestration.
