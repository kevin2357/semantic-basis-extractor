# AstroWoof Natal Authoring 0.4.4 Known Limitations

- Bounded-Natal Batch remains unsupported and fail-closed; no adapter exists.
- Provider retrieval and native checkpoint persistence are not one external
  atomic transaction. A durable provider GET may repeat; submission may not.
- Identity-less interrupted submission remains ambiguous and fail-closed.
- Exact Batch terminal usage can be unavailable. Provider polling may finish while
  API-owned billing reconciliation authority remains retained.
- The bounded cycle depends on provider transports honoring their frozen I/O
  timeout. Deterministic post-I/O continuation can extend total process time.
- Consumers must preserve the original frozen provider launch configuration and
  restore the complete workspace at its stable logical absolute path.
- Capacity release does not release API reservation, dollar exposure, lease,
  database, billing, cancellation, entitlement, or publication authority.
- Events are redacted, failure-isolated, and non-authoritative.
- The API companion must separately qualify queue-slot and reservation behavior in
  its PostgreSQL-backed orchestration.

