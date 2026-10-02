# SBE Orbit Economics — Slice 0 Findings

## Scope and conclusion

This finding is based on the existing public SBE export implementation and the
recorded Orbit symptom: API authoritative custody saw a completed set of
reported provider actions, while the final economics receipt was unavailable.
No provider call, retained-workspace read, R2 access, API state change, or
runtime export was made for this slice.

The export itself is a sound read-only projection boundary, but it is not a
self-publishing runtime mechanism. In source, the normal entry points are the
public `read_provider_economics_export()` function and the explicit
`provider_economics` CLI. The repository search found this reader used by its
CLI and provider-free QA/tests, not a hook that automatically invokes it after
every ordinary SBE lifecycle/action transition. That makes a missing successor
export plausible, but not yet proven: API-side handoff timing, predecessor
selection, or a snapshot/read failure could produce the same external
`sbe_export_unavailable` observation.

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

## Leading hypotheses, kept distinct

The evidence supports three non-exclusive explanations:

| Hypothesis | What Slice 0 establishes | What remains unproven |
| --- | --- | --- |
| no normal-cycle invocation | Source exposes an explicit reader/CLI and no automatic lifecycle hook was found | Whether the deployed API already calls it on every relevant cycle. |
| invocation before final durability | Reader refuses incomplete/malformed snapshots and only projects durable state | Orbit’s exact snapshot and action state at the failed read. |
| predecessor/handoff mismatch | Successor projection requires caller-provided, validated predecessors | Whether API supplied the correct accepted predecessor revision(s) and consumed the returned result. |

Accordingly, do not label this a producer omission yet, and do not “fix” it by
inventing latest-revision discovery in SBE. That would violate the exact
handoff/custody lessons from the editorial work.

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

The next slice should trace Orbit’s exact normal-cycle call chain and classify
the missing final receipt into one row of the table above. It should not change
the exporter, add an automatic publisher, or use retained-workspace access
until that call-chain evidence says which boundary actually failed.
