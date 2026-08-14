# Slice 1 - Shared Engine Seam and Exact Legacy Policy

## Result

Exact-Natal-specific selection policy now lives behind the explicit
`ExactNatalPolicy` seam. The default resolver selects `legacy_atomic.v1`; unknown
names and versions, and policies for another route, fail closed.

`legacy_atomic.v1` owns:

- the sixteen mandatory exact objects;
- atomic ASC, DSC, MC, and IC treatment;
- object claim types, categories, and semantic roles;
- exact object, relationship, and synthesis scoring formulas and weights;
- the fifty-claim budget and mandatory-count expectation; and
- existing packet, candidate-generator, and optimizer identities.

The shared extractor retains deterministic graph indexing, duplicate relationship
collapse, candidate materialization, dependency closure, marginal portfolio
optimization, provenance/evidence assembly, and output orchestration. This is a
narrow seam: it is sufficient for Slice 2's alternative exact angle policy and does
not pretend the forthcoming bounded route uses exact graph semantics.

## Public behavior

The CLI now accepts:

```text
--exact-natal-policy legacy_atomic.v1
```

Omission remains identical to the released default. The selected packet schema,
candidate IDs, order, scores, dependencies, packet bytes under canonical JSON, QA,
artifact paths, and closure defaults remain unchanged.

The resolved route and policy identity are added to the candidate pool, selection
audit, subject run record, and batch run manifest. They are deliberately not added
to the legacy authoring packet because that would create packet drift for metadata
unrelated to its consumer contract.

## Verification

- Slice 0 Bre candidate, selected, packet, and QA hashes: unchanged.
- Explicit `legacy_atomic.v1` versus omitted policy: complete replay equality.
- Unknown-version and wrong-route resolution: rejected.
- CLI audit identity and default artifact paths: verified.
- Focused policy/baseline tests: 8 passed.
- Full repository suite: 223 passed in 114.923 seconds.
- Python compile check: passed.
- Fresh isolated offline wheel build and install: passed.
- Installed public lifecycle smoke: passed, including replay-stable closeout and a
  valid workspace snapshot.
- Installed complete release smoke: passed through `DELIVERY_COMPLETE` with 50
  cards, four summaries, matching manifest hashes, and the unchanged resource-set
  SHA-256.
- `git diff --check`: passed with only expected Windows line-ending notices.

## Gate status

Gate 1 is ready for review. No Slice 2 behavior is enabled.
