# API Consumer Handoff — SBE 0.4.21

The complete contract and ingestion guidance is published in:

- `docs/sprints/2026/08/20260821-silly-owner-wants-accounting-and-performance-visibility-sprint1/SLICE 5 - PUBLIC EXPORT AND API INGESTION HANDOFF.md`;
- the packaged contract catalog and provider-economics schemas;
- `astrowoof-provider-economics-export`; and
- `astrowoof-provider-economics-qa`.

API should retain every accepted immutable revision keyed by
`(transaction_id, revision_number)`, validate exact predecessor continuity, and
may derive an API-owned current projection. API must preserve null/unavailable
distinctly from zero and keep SBE estimates, provider-reported evidence, and
account-authoritative billing separate.

The native transaction authority is `(native_run_id, native_action_id)`.
`transaction_id` is a deterministic convenience alias. One Batch round is one
transaction; members are ordered evidence, not separate global reservations or
inferred proportional costs.
