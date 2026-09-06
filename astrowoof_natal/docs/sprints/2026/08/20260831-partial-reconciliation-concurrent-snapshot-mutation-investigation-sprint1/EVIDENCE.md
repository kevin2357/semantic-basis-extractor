# Evidence

## Slice 0 inputs

- Frozen incident background: `Background.md`
- API plan review: `API REVIEW - INVESTIGATION PLAN.md`
- Full SBE worker export: `C:\tmp\sbe_worker_logs.txt`
- Historical source: tag `astrowoof-natal-authoring-v0.4.35`
- Current source: `main` after SBE 0.4.36

## Trace evidence

- Lifecycle selected four due actions at `2026-08-31T11:54:02.192Z`.
- Four retrievals ran concurrently; passes 3 and 5 entered local adoption with
  `max_workers=2` at `11:54:03.488Z`.
- First invalid snapshot: expected 390, actual 390 at `11:54:04.386Z`.
- Pass-3 cost persisted at `11:54:04.408Z`.
- Second invalid snapshot: expected 390, actual 420 at `11:54:04.611Z`.
- Historical traceback proves the validator was reached through
  `author_one_pass -> save_state -> read_native_transition_result`.
- Public command traceback proves the error escaped through `future.result()`
  without a typed native command result.

## Source evidence

- SBE 0.4.35 `save_state()` inspected `native-result-index.json` and called
  `read_native_transition_result()` before its worker-thread branch.
- `read_native_transition_result()` validates the complete workspace snapshot.
- `author_pending_passes()` runs selected pass continuations in a thread pool.
- `state_lock` serializes state persistence, but OpenAI request and response
  artifacts are written outside that lock.
- Current `main` no longer performs the sealed-result lookup in `save_state()`;
  the removal is visible in commit `96980ab`.

## Provider-free characterization

Command:

```powershell
$env:PYTHONPATH='astrowoof_natal/src'
python -m unittest astrowoof_natal.tests.test_partial_reconciliation_snapshot_mutation_slice0
```

Result:

```text
Ran 2 tests
OK
```

The tests prove:

1. equal member counts can encode an existing-path digest change with no
   additions/removals; and
2. one sibling pass tree can add exactly 30 classified members and invalidate
   the predecessor whole-workspace snapshot.

`git diff --check` passed for the Slice 0 test and plan at the time of the run.

## Safety statement

- Provider calls: 0
- Provider retrievals: 0
- R2 `HEAD`/`GET`/listing/writes: 0
- Retained QA reads or mutations: 0
- Runtime source changes: 0
- Release/deployment activity: 0

## Slice 2 preliminary wheel evidence

- 0.4.35 wheel SHA-256:
  `830a4cd9288628c399a79f9d255edbb49caa5ab608046af6f12cfec8bbe34cfb`
- 0.4.36 wheel SHA-256:
  `a76157d5342cb3b72a88b0b04fe8f3b549b8941b46d92d268182cbf934e8d826`
- Identical module against 0.4.35: 3 passed, expected historical failure
  observed.
- Identical module against 0.4.36: 3 passed, safe worker/coordinator behavior
  observed.
- Serial/concurrent native projection: byte/digest-semantic parity passed with
  actual two-worker overlap.
- Mixed custody: two completed members adopted, two pending members retained,
  zero provider transport calls, valid successor snapshot, immutable predecessor
  replay.
- Provider/R2/retained-QA activity: 0.
- Slice 2 reproduction gate: complete; interruption/result contract pending at
  Paws point 2.

## Final disposition

- Correction selected: SBE 0.4.36 worker/coordinator split.
- Additional runtime/source correction in this sprint: none.
- New release in this sprint: none.
- Broader quarantine/interruption work: explicitly deferred to the following
  sprint.
