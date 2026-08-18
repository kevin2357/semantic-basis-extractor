# SBE 0.4.7 API Consumer Handoff

Status: consumer-approved

The supported initial-wave surface consists of the packaged v1 schemas and
fixtures, root-package builders/validators/readers, and the provider-free
`astrowoof-initial-wave-contract` CLI. These are evidence interfaces; lifecycle
inspection v0.3, reconciliation result v0.2, transition journal, immutable result,
publication receipt, and complete validated snapshot remain native run authority.

## Identity and authority

- `prepared_wave.run_id` binds to `SbeAuthoringRun.native_run_id`, never API
  `GenerationRun.id`.
- Exact and bounded interactive require one complete API-authorized six-action wave
  before any create. Each action remains separately bound and reserved.
- Exact and bounded Batch remain one paid action and one API reservation per Batch
  round; members are audit and settlement evidence only.
- Provider IDs are persisted per member immediately after create. Known identities
  are reconciled and never resubmitted.
- A provider-accepted request whose identity is not durable remains ambiguous and
  fail-closed; deterministic local keys are not provider idempotency proof.
- Local capacity release, provider retrieval custody, native spend state, and API
  consumer authority remain independently represented.

## Adoption order

1. Pin and verify the exact 0.4.7 wheel and SPC 0.11.0 dependency.
2. Validate packaged schemas and fixtures through supported public readers.
3. Atomically reserve or refuse the exact complete interactive wave in API authority.
4. Drive SBE through supported lifecycle operations and ingest terminal evidence
   before subprocess interpretation.
5. Deploy and attest API and every worker independently with matching compatibility
   identities and selected configuration.
6. Register a fresh immutable generation-profile ID and prove a newly created run
   binds that profile.

The API continues to own cross-run reservations, quotas, circuit breakers,
entitlements, rate-pressure policy, account billing reconciliation, worker capacity,
PostgreSQL/R2 state, and publication policy.
