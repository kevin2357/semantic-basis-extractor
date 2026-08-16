# SBE 0.4.3 API Consumer Handoff

Require lifecycle inspection v0.2 for capacity decisions. Release a short worker
claim only when `execution_capacity.disposition` permits it and
`checkpoint_safe_for_worker_release` is true. Retain API-owned reservation and
financial authority for every exact `provider_custody.actions` member classified
`retain_consumer_authority`.

Schedule one delayed reconciliation per native run no earlier than
`resume_not_before`. Invoke:

```text
astrowoof-semantic-closure --run-dir RUN --resume --provider openai \
  --service-level interactive --bounded-provider-reconciliation
```

Supply the original frozen provider configuration. Consume the typed
`astrowoof.provider_reconciliation_cycle_result.v0.1` result and persist its fresh
inspection/checkpoint into API-owned state. `not_due` is successful and
nonmutating. Events and exit codes are observations, never scheduling authority.

Exact interactive initial/retry/polish/critic/candidate stages are supported.
Batch and bounded Natal fail closed. Publishable reader delivery may coexist with
nonblocking critic/candidate custody, but its reservation remains retained.

The complete mapping, recovery rules, and companion checklist are in:

- `docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`;
- `docs/sprints/2026/08/20260815-provider-pending-capacity-sprint3/FINAL API RESPONSE.md`;
- `docs/sprints/2026/08/20260815-provider-pending-capacity-sprint3/API COMPANION ADOPTION CHECKLIST.md`; and
- the packaged contract catalog and strict lifecycle schema.

SBE owns native state, provider identities, timing, snapshots, and reconciliation.
The API owns leases, queues, capacity allocation, reservations, global spend,
billing reconciliation, PostgreSQL status authority, and publication policy.
