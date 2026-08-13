# Slice 4 Idempotent Terminal Closeout

Status: complete, 2026-08-13

`astrowoof_natal_authoring.lifecycle.closeout_run()` reconciles one exact validated
workspace and persists a native closeout result and complete checkpoint.

The result distinguishes `closed`, `continuation_required`, `review_required`, and
`ambiguous`; preserves the full typed terminal and quiescence summaries; lists local
dependencies and unresolved action IDs; and identifies the durable artifact, result
revision, snapshot SHA-256, and canonical semantic-result SHA-256.

Repeated closeout against the same result revision returns the existing semantic
disposition and artifact without another write. It does not resubmit provider work,
repeat a denial, discard history, or change accepted deck/delivery bytes.

## Stepwise negative authorization

Closeout deliberately does not accept a negative-authorization request. Consumers
call `deny_providerless_action()` first and consume its complete typed result. Only
an applied or exact idempotent denial permits the API to consider its reservation;
a normal race/refusal remains a typed domain result and is never converted to an
exception-only closeout outcome. After mutation, the consumer obtains a fresh
inspection and calls closeout without a denial request.

This stepwise seam is also required for multiple actions: each native mutation
advances revision and snapshot authority, so the next decision requires a fresh
observation rather than a stale batch authorization.

## Provider evidence and correlation

Known active provider identity remains exact in inspection and remains unresolved
through closeout; closeout neither releases nor resubmits it. Reported and reconciled
provider evidence remains preserved but does not falsely count as outstanding
provider continuation.

With a fixed observation time and no intervening mutation, pre-closeout inspection
and closeout `decision_basis` match on run, revision, snapshot SHA-256, logical root,
validation facts, observation time, and race fact. Native exclusivity is the sole
documented strengthening from `declared` to `established`. If state changes, the
closeout basis identifies the new revision/snapshot and therefore cannot correlate
to the stale inventory.

## Interrupted commit recovery

Closeout uses an excluded staged artifact, then persists the native state intent,
promotes the exact artifact, and publishes the complete workspace snapshot. Tests
inject failure after each of these four boundaries.

On restart, SBE may finish the interrupted commit only when:

- state contains the expected closeout intent at its exact result revision;
- the staged or promoted artifact exactly equals the artifact reconstructed from
  that intent;
- the previous snapshot exists; and
- every mismatch is confined to the known closeout write set (`run.json`, public
  and authorization projections, and the closeout artifact).

Missing or changed artifact bytes, unrelated workspace changes, missing snapshots,
or any broader mismatch fail closed. Recovery does not regenerate or bless arbitrary
bytes. The final snapshot is validated before success is returned.

This is a recoverable multi-file protocol, not a claim of filesystem-wide atomicity.
Individual JSON files use atomic replacement; the snapshot and verified intent make
partial commits detectable and narrowly recoverable.
