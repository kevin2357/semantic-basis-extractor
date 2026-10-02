# SBE Orbit Economics — Slice 0 Findings

## Scope and conclusion

This finding is based on the existing public SBE export implementation and the
recorded Orbit symptom: API authoritative custody saw a completed set of
reported provider actions, while the final economics receipt was unavailable.
No provider call, retained-workspace read, R2 access, API state change, or
runtime export was made for this slice.

The export itself is a sound read-only projection boundary. Slice 0 corrects
the initial “perhaps it is never invoked” hypothesis: SBE exposes the public
`read_provider_economics_export()` function and explicit CLI, while API calls
that public reader at its own sealed-transition boundaries. The reader is not
a remote publisher, which remains the right custody division.

## What the reader guarantees

`read_provider_economics_export(run_dir, observed_at, previous_revisions=())`
performs a deliberately strict projection:

1. resolves the workspace root and validates the complete workspace snapshot;
2. accepts only exact-Natal v0.9 or bounded-Natal v2 route state;
3. canonicalizes an explicit whole-second UTC observation timestamp;
4. validates all supplied predecessor revisions and groups them by transaction;
5. scans the durable spend ledger in canonical action-ID order;
6. projects each action against its exact latest predecessor; and
7. returns only newly durable revisions plus a canonical export SHA-256.

It exports `native_run_id`, route family, snapshot digest, observation time,
and a list of revisions under `astrowoof.provider_economics_export.v1`. The
revision layer is intentionally capable of successor construction: a later
projection receives the preceding accepted transaction revision rather than
inventing a replacement history. This is the correct general shape for the
Orbit result as actions move from prepared/pending to reported/settled.

The boundary also carries an important limitation: it receives
`previous_revisions` from its caller. It does not discover the API catalog,
choose a latest remote record, or persist/publish an export itself. That is
good custody discipline, but it means the integration must explicitly supply
the predecessor set and deliver the returned canonical export each time.

## Completed normal-cycle trace

Source inspection establishes this non-mutating call chain:

1. SBE seals a native transition and complete workspace snapshot.
2. API reads/validates that exact publication and persists its native receipt.
3. API calls `ProviderEconomicsExportIngestionService.observe()` with that
   workspace, API run ID, and validated publication.
4. `observe()` loads accepted tape predecessors, calls the public SBE reader
   with the exact workspace and canonical UTC time, verifies native run and
   snapshot equality, and sends returned revisions through immutable ingress.
5. Initial-wave authority, later external-authority admission, ordinary
   dispatch/reconciliation, and terminal ingress all invoke this observer.

Orbit therefore reached the reader path after its transition was sealed. The
event `sbe_export_unavailable` means that `observe()` caught an
`SbeProviderContractError` while deliberately allowing lifecycle custody to
continue. It does not reveal which internal phase or exception caused it.

## Leading hypotheses, kept distinct

The evidence supports three non-exclusive explanations:

| Hypothesis | What Slice 0 establishes | What remains unproven |
| --- | --- | --- |
| reader/projection failure | The reader can reject snapshot/state/action facts with `OSError`, `TypeError`, or `ValueError`, which API wraps | Which local reader/projection predicate rejected Orbit. |
| sealed-publication join failure | API requires returned native run ID and snapshot digest to equal the exact sealed transition | Whether a returned export disagreed with the publication identity. |
| predecessor/tape failure | API supplies persisted revisions and validates/persists each returned successor | Whether stale/foreign/malformed predecessor or successor evidence failed. |

Accordingly, do not label this a missing normal-cycle invocation or “fix” it
by inventing latest-revision discovery in SBE. The present gap is phase/error
classification inside API's intentionally non-fatal observation wrapper.

## Recommended integration contract

On an ordinary SBE cycle, after the state write and complete snapshot are
durable, the caller should invoke the public reader with:

- the exact workspace used by that invocation;
- a canonical observed-at value; and
- only the exact, API-persisted accepted predecessor revisions for that native
  run/transaction set.

The returned export should be treated as a same-call candidate, validated by
both sides, and persisted/transported with its `export_sha256` and
`snapshot_sha256`. An empty revision list is a valid statement that the
snapshot added no newly durable economics information; it should not be
converted into an error or an invented successor.

The API owns its remote/catalog persistence and can decide when to ask again.
SBE owns strict local snapshot reading and deterministic projection. Neither
side should discover a “latest” value across that boundary.

## Provider-free Gate A

Before implementation, run a deterministic exact and bounded fixture through
three local states: initial pending/prepared, reported, and a later settled or
otherwise changed durable state. For each route prove:

- snapshot validation happens before projection;
- initial export is canonical and valid;
- passing the exact initial revision as predecessor yields the expected,
  monotonic successor (or an explicitly empty export when nothing changed);
- duplicate, foreign-run, malformed, or non-latest predecessors fail closed;
- export output is byte-stable for the same snapshot, timestamp, and
  predecessor inputs; and
- no provider operation, workspace mutation, or catalog discovery occurs.

Then run one installed-wheel/API consumer cell using the real public reader and
a frozen complete workspace. That cell must separately demonstrate that the
API consumes a real returned successor; it cannot be replaced by a synthetic
catalog record.

## Slice 0 decision

Gate A should approve a provider-free diagnostic/reproduction plan that
distinguishes reader snapshot/state failure, export validation failure,
sealed-publication join failure, and immutable-ingress/predecessor failure.
It should not change the exporter, add an automatic publisher, reconstruct
receipts from API custody, or use retained-workspace access.
