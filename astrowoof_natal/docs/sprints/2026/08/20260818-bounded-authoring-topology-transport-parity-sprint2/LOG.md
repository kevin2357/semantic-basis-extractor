# Bounded Authoring Topology and Transport Parity Sprint 2 Log

## 2026-08-18 — Planning

- Opened the sprint for review; no implementation began.
- Recorded that six-pass fan-out is a writing-quality invariant intended to prevent
  templated bulk generation, not a performance optimization.
- Separated semantic route from provider transport: exact/bounded determine evidence
  and authority; interactive/Batch determine submission and retrieval only.
- Confirmed exact `stratified-v1` assignment is deterministic for a frozen packet,
  subject, and policy identity rather than randomly reshuffled on every run.
- Planned separately versioned bounded editorial resources whose intended shared
  content initially matches exact resources.
- Identified current bounded whole-deck interactive authoring as part of the topology
  correction, not merely a prerequisite for adding bounded Batch.
- Confirmed no new public lifecycle vocabulary is expected. The sprint must still
  version SBE's route-parity oracle because v1 explicitly rejects bounded Batch, and
  must provide bounded live/Batch traces through the API's existing route-neutral
  transition oracle. Discovery of an unrepresentable state pauses for contract
  review.
- API plan review approved the sprint with clarifications now incorporated: the
  post-wave scheduler must re-drive bounded work through its next authorization or
  provider boundary; interactive authority is one action per pass/attempt; Batch
  authority is one action/global reservation per round with member settlement;
  request parity compares bounded live to bounded Batch rather than exact packet
  bytes to bounded packet bytes; and legacy one-operation bounded state fails closed.
- Provider operations: 0. Spend: USD 0.

## 2026-08-18 — Slice 0 baseline and editorial-invariant evidence

- Added a provider-free regression proving exact interactive and Batch builders
  produce identical logical pass requests after removing the documented interactive-
  only `background` transport-envelope field. The test disables explicit cache
  controls because Batch intentionally omits those transport options.
- Reconfirmed `stratified-v1` determinism, complete 50-claim assignment, improved
  claim-type/category balance, and canonical-order reassembly.
- Reconfirmed exact fake interactive and Batch paths each author six isolated passes;
  Batch detach/resume ingests the same durable Batch rather than creating another.
- Reproduced the bounded baseline from the compiled provider fixture: 50 claims and
  four summaries are sent through one bounded pass/whole-deck provider operation.
- Reconfirmed bounded Batch rejects during provider construction before any provider
  submission and the current route-parity oracle labels it `bounded_batch_rejected`.
- Inventoried the reuse seam: Files/Batch transport, JSONL correlation, durable Batch
  identifiers/artifacts, polling, cost disposition, and reconciliation are reusable;
  exact `PassSpec`, Markdown workspace reconstruction, pass acceptance, and assembly
  are route-specific and must sit behind a shared pass protocol rather than be copied.
- Identified the required state migration boundary: current bounded runs persist one
  pass ID and stage/attempt route. New six-pass runs need a new route/run contract;
  legacy one-operation workspaces must fail closed.
- Focused provider-free baseline: 36 tests passed in 23.412 seconds.
- Provider operations: 0. Spend: USD 0.
- Slice 0 is complete and paused for the planned review gate.
