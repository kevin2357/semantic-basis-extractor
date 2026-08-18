# Final Response to the AstroWoof API Route-Parity Brief

Status: SBE implementation, native qualification, and API consumer review
complete. API queue-slot and financial-reservation qualification remain API-owned.

## Route support matrix

| Native route | Provider mechanism | Reconciliation status | Notes |
|---|---|---|---|
| Exact Natal | Responses | Supported | Initial authoring, creative retry, polish, critic, and candidate stages |
| Exact Natal | Batch | Supported | One paid action per Batch round; member rows are audit evidence, not separate spend actions |
| Bounded Natal | Responses | Supported | Initial authoring and all profile-enabled retry/optional stages |
| Bounded Natal | Batch | Rejected | No bounded Batch adapter exists; construction, inspection, and dispatch fail closed |

Inspection v0.3 supplies validated native `route_family`, `provider_mechanism`,
and operation binding. Consumers must not infer those identities from their own job
record.

## Consumer adoption contract

1. Restore the complete workspace at its stable logical absolute path and acquire
   one native writer under the API's fenced lease.
2. Inspect lifecycle v0.3 and strictly validate its schema and native route,
   mechanism, action, checkpoint, and scheduling identities.
3. Release a worker slot only when SBE reports the closed capacity disposition and
   `checkpoint_safe_for_worker_release: true`.
4. Retain API-owned authority for the exact action IDs projected with
   `retain_consumer_authority`. SBE describes custody; it does not own or release
   reservations, quotas, or dollar exposure.
5. Do not invoke reconciliation before the durable `resume_not_before` lower
   bound. An early call returns typed `not_due`, performs no provider retrieval,
   mutates no bytes, and returns no new checkpoint.
6. Invoke `reconcile_authoring_provider_cycle()` or the neutral
   `--provider-reconciliation-cycle --observed-at` CLI on a short-lived worker.
   Native inspection selects the adapter; caller intent does not.
7. Persist the typed cycle result, per-action custody/financial dispositions, and
   shared post-cycle checkpoint. Reinspect before making the next API decision.
8. Continue local work, detach until due, authorize or deny newly prepared work,
   retain for review, or close out according to the closed result vocabulary.

The deprecated exact-only `--bounded-provider-reconciliation` spelling retains its
historical behavior for compatibility. It does not mean bounded Natal and should
not be adopted by new consumers.

## Batch cost and custody boundary

A terminal Batch ends provider retrieval custody after its terminal object and
files are durably retrieved. That does not necessarily settle financial authority.
The closed cost disposition distinguishes provider-reported usage, usage
unavailable/billing reconciliation pending, and no provider work consumed. Missing
usage must never be interpreted as reported `$0.00`.

An identity or output/member integrity conflict can therefore end provider polling
while retaining consumer authority for review. The API must not keep a worker
polling merely because financial or integrity authority remains retained.

## Safety and replay guarantees

- Reconciliation is retrieval-only for durable provider identities; submission
  methods are unavailable through the public dispatcher and CLI mode.
- Identity-less interrupted submission remains ambiguous and fail-closed.
- Exact Batch performs atomic terminal-object/file checkpointing and member
  preflight before ingestion; mixed or malformed output cannot partially apply.
- Completed provider evidence can re-enter deterministic local continuation after
  a fresh-worker restore without another provider retrieval.
- Snapshot validation, single-writer exclusion, stale-checkpoint rejection, and
  provider-evidence precedence remain mandatory.
- Events are redacted, failure-isolated operational observations and are never
  authority.

## Qualification and confidence

Confidence is **high** for the SBE-native contract. Evidence includes:

- `356` passing repository tests;
- a concurrent exact-Responses, exact-Batch, and bounded-Responses cohort;
- deterministic clocks, concurrency, stale-state, replay, and failure injection;
- byte-identical fixed-epoch candidate wheels;
- clean Linux Python 3.11 and Windows installed-runtime smokes;
- packaged schema, typing marker, public interface, transition fixture, and CLI
  verification; and
- zero provider operations and `$0` paid spend.

Candidate wheel evidence from source commit `b489ef8`:

```text
astrowoof_natal_authoring-0.4.3-py3-none-any.whl
sha256 1a305a15eb9b01860de79bfd6c525b312189b5a46809e894a867ba39a99d69ef
```

The filename reflects the current source baseline and is not a publication claim.
A new pinnable patch should use the next release version after explicit approval.

## API-owned companion gate

The API must separately prove that mixed provider-pending jobs release and reclaim
its worker slots correctly while PostgreSQL authority, reservations, capacity
records, and billing policy remain intact. SBE's packaged route-parity transition
oracle is sanitized input for that adoption test. SBE makes no assertion about the
result until the API reports it.

## Recommendation

All SBE-native exit criteria pass and the API agent accepted the handoff. Kevin
separately authorized a pinnable `0.4.4` release. This document records the
pre-publication contract; immutable publication evidence is recorded in the release
directory after publication.
