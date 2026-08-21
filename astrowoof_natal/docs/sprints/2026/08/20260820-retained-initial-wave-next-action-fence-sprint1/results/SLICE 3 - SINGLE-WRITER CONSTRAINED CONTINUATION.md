# Slice 3 — Single-Writer Constrained Continuation

Date: 2026-08-20
Status: complete; awaiting review
Provider/network use: none

## Outcome

The exact-interactive initial wave now has one supported create-capable public
boundary. The caller supplies the snapshot-validated external-authority request,
one positive aggregate API grant, and the six complete ordinary authorization
documents. SBE rebuilds the current request under its native writer and requires
exact equality before it mutates authority or crosses provider I/O.

The previous public `--initial-wave-authorization` route is rejected. Six loose
member authorizations also cannot authorize or strand a stored initial wave; they
require the aggregate grant and exact request.

Generic exact-interactive resume may still prepare a genuinely fresh initial wave.
Once a stored wave is awaiting external authority, however, the same generic resume
returns `aggregate_grant_required` before any state/snapshot write or native-result
publication. It cannot be used as an alternate continuation route.

## Persistence and provider boundary

Under one native single-writer acquisition, SBE:

1. validates the complete workspace snapshot;
2. rebuilds the current public authority request;
3. compares it exactly with the supplied request;
4. validates the aggregate grant and every complete member document;
5. applies all six authorizations to a copied ledger;
6. marks all six exact actions `SUBMITTING`; and
7. publishes one complete snapshot containing a hashed constrained-submission
   intent.

Only then is the writer released and the six independent provider creates allowed
to fan out. The raw capability token is process-local; only its digest is durable.
Each create result reacquires native single-writer control and checkpoints the exact
provider identity or ambiguity before the coordinator proceeds.

This is an atomic local publication protocol, not atomicity with the provider. A
hard interruption after remote acceptance but before local identity durability is
still irreducible ambiguity. Durable intent prevents that gap from becoming
permission to create again.

## Refusal behavior

The runtime uses closed `InitialWaveError.reason_code` values for pre-I/O refusal,
including `stale_observation`, `authorization_mismatch`, `partial_authorization`,
`digest_mismatch`, `aggregate_grant_required`, and `request_unavailable`. These
refusals do not rewrite native state or snapshots and do not call the provider.

Provider reconciliation remains separate. The reconciliation command rejects the
new request/grant inputs and cannot turn them into a create.

## Qualification

- 34 request/grant/public/execution tests passed; four optional JSON Schema checks
  skipped only in the lean host interpreter.
- 40 existing initial-wave and spend tests passed.
- Two targeted legacy/public semantic-closure tests passed.
- Scripted success produced six durable provider IDs.
- Every preflight refusal produced zero provider calls and byte-identical native
  state/snapshot.
- Post-intent interruption replay produced zero provider calls.
- Injected provider-return/identity gap produced durable ambiguity and no replayed
  calls.

Slice 4 will add the stronger pre-preparation lineage fence. This slice deliberately
does not reinterpret retained historical lineage or claim that Aster is recoverable.
