# Slice 4 — Timing Semantics Review

Date: 2026-08-25
Status: complete; Slice 5 public export may proceed

## Durable timing boundary

The transaction revision continues to expose only semantically named durable
facts. Missing facts remain `null`; zero is reserved for a known measured zero.

The native projector now recognizes explicit durable timestamps for preparation,
authorization, submission intent, provider-identity durability, provider-terminal
observation, reconciliation completion, and native settlement. It derives only two
wall-clock spans:

- `observed_provider_pending_ms`: provider identity durability to the time SBE
  actually observed terminal provider evidence; and
- `native_action_span_ms`: native preparation to native settlement.

Neither span is provider compute time. SBE does not derive compute time from
provider-pending wall time, queue delay, retry delay, worker restoration, or API
lease history. `provider_reported_duration_ms` remains null unless the provider
actually supplies a durable duration with that meaning.

## Retrieval summary

Each real reconciliation GET now adds one cumulative, durable action-local summary:

- exact attempt count;
- first and last SBE observation timestamps;
- total measured retrieval HTTP duration;
- the first 16 diagnostic attempt IDs in order; and
- explicit overflow count after the reference cap.

This summary is persisted in the same native reconciliation checkpoint as the
diagnostic artifact. It is observation evidence only: it cannot authorize, submit,
settle, release custody, or select another retrieval.

Historical actions that have only the old scheduler attempt count and last-attempt
time do not receive a fabricated first-attempt time or HTTP duration. If their
partial legacy shape cannot satisfy the strict public timing contract, projection
fails closed rather than manufacturing a complete timeline.

## Monotonicity

Later cumulative revisions may add previously unknown timing facts and extend the
retrieval tape. They may not:

- remove or alter an accepted timestamp or fixed duration;
- reduce cumulative observed-pending/native-action spans;
- reduce retrieval count or total HTTP duration;
- reorder or replace retained retrieval references;
- move the last retrieval observation backwards; or
- change already accepted provider settlement, usage, member order, or cohort
  identity.

## Qualification

- Provider-economics contract/projection/timing suite: 22 passed; 1 optional-schema
  skip in the lean interpreter.
- Provider-pending, temporal-observation, and v2 route qualification regression:
  57 passed; 1 optional-schema skip.
- Clock regression and negative-duration projection: refused.
- Eighteen-attempt reference case: 16 retained ordered references plus overflow 2.
- Real provider calls, credentials, spend, API writes, and retained-run access: 0.
