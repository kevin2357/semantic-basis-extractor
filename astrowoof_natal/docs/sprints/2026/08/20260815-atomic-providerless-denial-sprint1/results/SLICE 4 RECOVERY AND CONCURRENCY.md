# Slice 4 Recovery and Concurrency

Status: complete; pending review and commit

## Recoverable write protocol

The batch operation now exposes internal failure-injection points after:

1. the exact batch artifact is staged;
2. native state and projections are persisted;
3. the staged artifact is promoted; and
4. the new workspace snapshot is published.

Restart behavior is deterministic at each point:

- **After staging:** authoritative state and the prior snapshot are still valid.
  Staged dot-temporary files are deliberately snapshot-excluded. The exact request
  safely reruns preflight and completes the transition.
- **After state persistence:** the old snapshot detects the changed state/projection
  bytes. Recovery accepts only the exact state-recorded request, result revision,
  action-local batch references, staged artifact bytes, and known changed paths;
  it promotes the artifact and republishes the snapshot.
- **After artifact promotion:** the same constrained checks accept the exact final
  artifact and known write set, then republish the snapshot.
- **After snapshot publication:** the workspace is already complete and valid; the
  call returns exact idempotent replay.

Every recovered run ends with both actions denied, one batch result, one coherent
validated snapshot, and stable subsequent replay. No recovery path invokes or
accepts a provider.

## Fail-closed repair boundary

Recovery refuses to bless:

- an unrelated added workspace member;
- a missing or changed staged artifact;
- a missing or changed promoted artifact;
- a changed request or digest;
- a mismatched result state revision;
- absent or inconsistent action-local denial evidence; or
- any changed path outside `run.json`, `public-run.json`,
  `spend-authorization-requests.json`, and the exact batch artifact.

This is constrained completion of a known native protocol, not general snapshot
repair and not permission to bless arbitrary workspace bytes.

## Concurrency result

A deterministic contention test holds the native lock during the batch transition
and attempts both:

- the same batch operation; and
- the legacy single-action denial against one batch member.

Both competitors return their existing typed `exclusivity_not_established` outcome.
The lock holder then applies both actions together. The final state is never split,
and subsequent exact batch replay succeeds without mutation.

Provider evidence injected before locked preflight remains covered by Slice 2 and
refuses the entire batch with the specific safe outcome. Tests deliberately do not
simulate an unsafe provider-side mutation inside SBE's established exclusive
section or claim control over external provider atomicity.

## Atomicity statement

SBE guarantees:

- one single-writer decision/mutation section;
- complete preflight before semantic mutation;
- one native state revision for successful application;
- atomic replacement of each individual JSON file;
- exact durable intent/result evidence;
- snapshot-detected incomplete writes; and
- constrained idempotent recovery across every native write boundary.

The underlying filesystem does not provide one transaction spanning all state,
projection, artifact, and snapshot files. The implementation and documentation do
not claim otherwise.

## Gate evidence

- Focused batch suite: 14 passed, including four interruption boundaries and
  batch/single contention.
- Full repository suite: 292 passed.
- Provider operations: 0.
- Paid spend: $0.
- API key: not used.
