# Slice 2: Journal Integrity and Public Reader

Status: complete; awaiting Kevin review.

## Result

The frozen native journal/result contract now has a packaged implementation. This
slice intentionally does not connect it to authoring or provider boundaries; those
integration writes begin in Slice 3.

## Implemented

- `native_transitions.py` provides canonical JSON hashing, SBE invocation/record/
  result identities, append-only journal validation, crash-safe whole-journal
  replacement, exact append replay, bounded range digests, checkpoint-basis
  calculation, immutable result publication, derived index repair, and strict
  result/range/basis/full-snapshot reading.
- The existing cross-process `spend-consumption.lock` is reused as the one-native-
  writer boundary. The package root exposes only read/validate operations, not
  journal/result mutation.
- The packaged contract catalog now identifies journal record v0.1, execution
  result v0.1, and derived result index v0.1.
- The wheel resource set includes a strict Draft 2020-12 schema plus canonical
  hash-valid review-terminal record/result fixtures.

## Publication and integrity behavior

- Record IDs and full record hashes are deterministic; sequence starts at one and
  every later record binds the complete prior hash.
- Exact append replay returns the existing record without adding a duplicate.
- Journal writes replace the complete JSONL file atomically after flushing the
  staged file, avoiding torn appended lines.
- Immutable result identity is content-derived. Exact replay repairs a missing
  derived index; conflicting bytes at the same identity fail closed.
- The public reader requires one explicit result ID and returns only its bounded
  journal range. It validates result hash, chain/range digest, post-state revision,
  checkpoint basis, full snapshot inventory, and stable logical path.
- The checkpoint basis excludes only the publication namespace from basis hashing.
  The ordinary full snapshot still inventories result/index artifacts, so missing,
  additional, changed, truncated, or relocated members fail closed.

## Provider safety

- Submission-started observations cannot contain a fabricated external provider ID.
- Known-ID observations require a real external ID.
- Reported usage requires amount, price book, and evidence reference.
- Pending/unavailable/no-work dispositions cannot carry a fabricated amount.
- Cost dispositions exactly reuse lifecycle/reconciliation v0.2.
- Supersession fields and API acknowledgement do not exist in the schema.

## Tests

- Native journal/result focused tests: 11 passed in 0.870 seconds.
- Final native plus lifecycle/snapshot/consumer compatibility gate: 57 passed in
  3.865 seconds.
- Coverage includes chain/range integrity, exact replay, corruption, gaps, unknown
  kinds, provider/cost rules, immutable result/index repair, full snapshot binding,
  partial publication, relocation, size/range bounds, checkpoint-basis exclusions,
  packaged resources, public surface, and cross-process writer contention.
- One preliminary command named a nonexistent `test_lifecycle_smoke` module after
  46 real tests passed. The authoritative corrected 53-test invocation above is
  clean; the import typo is not product evidence.
- Provider operations: 0. Paid spend: `$0`.
- `git diff --check`: pass.

## Deferred to Slice 3+

- No ordinary authoring/provider callback writes journal observations yet.
- No invocation result is automatically published before command exit yet.
- No CLI result-export mode exists yet.
- No API ingestion or acknowledgement behavior is implemented in SBE.

## Gate assessment

PASS. The journal/result authority is deterministic, append-only, snapshot-bound,
bounded for consumers, single-writer protected, and packaged. Slice 3 may integrate
provider-operation observations after Kevin approves and commits this slice.
