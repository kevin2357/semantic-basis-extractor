# Final Response to the AstroWoof API Process-Orchestration Brief

Status: SBE implementation and native qualification complete; API companion
adoption and API capacity-slot qualification remain API-owned.

## Direct answers

### Does the public lifecycle distinguish provider waiting from local work?

Yes. Lifecycle inspection v0.2 adds orthogonal `execution_capacity` and
`provider_custody` projections without redefining the historical terminal,
quiescence, or continuation fields. `release_until_due` means the native process
has unwound, the complete snapshot is valid, no local work is ready now, and only
known provider operations prevent progress. Confidence: high; strict truth-table,
snapshot-failure, installed-wheel, and cohort tests cover this boundary.

### Does SBE publish a recommended next reconciliation time?

Yes. Every supported provider-bound action has durable versioned reconciliation
timing. Run-level `resume_not_before` is the earliest relevant lower bound. The API
may schedule later. An earlier bounded call returns typed `not_due`, performs no
GET, mutates no bytes, emits no checkpoint, and returns no new checkpoint.
Confidence: high; deterministic clock/backoff and mutation-hash tests cover it.

### Can SBE identify whether genuine local continuation prevents release?

Yes. `execution_capacity.disposition`, `local_work_ready_now`,
`checkpoint_safe_for_worker_release`, and `reason_code` provide the closed native
decision. A v0.1 inspection, incomplete snapshot, absent exclusivity, ambiguity,
identity conflict, unsupported route/stage, or timing-free legacy action never
authorizes release. Confidence: high; fail-closed matrices cover each case.

### Can a fresh short-lived worker safely resume the same run?

Yes, after restoring the complete exact workspace at its stable logical absolute
path and establishing one native writer. The bounded operation retrieves at most
one due wave, persists response evidence, exhausts newly unblocked local work,
publishes one complete snapshot/checkpoint, and detaches. Confidence: high for the
native contract; Windows/Linux installed smoke and independent-workspace tests
pass. API lease/restore orchestration still needs the companion qualification.

### Is authoritative lifecycle state held only in a live process?

No supported authority is process-only after the operation returns. Provider IDs,
action state, authorization/consumption/report evidence, timing, completed response
evidence, local continuation, inspection, cycle result, and snapshot identity are
durable. Events remain non-authoritative. Confidence: high within supported exact
interactive routes; Batch and bounded Natal intentionally fail closed.

### Which actions require consumer authority retention after capacity release?

Use `provider_custody.actions`, keyed by exact native action ID. Every member with
`custody_classification: retain_consumer_authority` requires the API to retain its
separately owned reservation/financial authority. SBE does not claim the literal
reservation or dollar exposure. Completed evidence, no-custody, ambiguity, and
unsupported classifications are separately typed. Confidence: high for native
classification; API reservation accounting remains API authority.

## Supported operational sequence

1. Restore the complete native workspace at its stable logical path.
2. Hold the API fenced lease and one native writer.
3. Call lifecycle inspection v0.2 and persist its validated mapping in PostgreSQL.
4. Release local capacity only when the closed disposition and
   `checkpoint_safe_for_worker_release` permit it.
5. Retain API authority for every exact custody action requiring retention.
6. Schedule one delayed reconciliation per run no earlier than
   `resume_not_before`.
7. Invoke the installed bounded operation with the frozen launch configuration.
8. Persist the typed result, new checkpoint when present, and fresh inspection.
9. Repeat, authorize/deny prepared work, enter review, or close out according to
   the closed outcome. Never infer authority from exit code or events alone.

## Supported and deferred routes

Exact interactive Natal supports initial authoring, creative retry, polish,
qualitative critic, and qualitative candidate generation when frozen policy enables
them. Batch and bounded Natal do not inherit this contract and return unsupported
retention advice. A publishable delivery may coexist with nonblocking critic or
candidate custody: reader delivery can proceed while provider authority remains
retained.

## Irreducible boundaries

- A provider GET and native checkpoint write are not one external transaction.
  Repeating GET for a durable provider ID is safe; repeating submission is not.
- Identity-less interrupted submission remains ambiguous and fail-closed.
- SBE cannot prove or mutate API lease, capacity, reservation, queue, billing, or
  PostgreSQL state.
- The API companion test must still prove two waiting API runs release local
  capacity and a third reading is admitted while reservations remain intact.

## Recommendation

The SBE-native work satisfies the approved scope and is suitable for a pinnable
0.4.3 patch candidate after API review and separate release authorization. No tag,
version bump, wheel publication, or immutable release claim is made by this sprint.
