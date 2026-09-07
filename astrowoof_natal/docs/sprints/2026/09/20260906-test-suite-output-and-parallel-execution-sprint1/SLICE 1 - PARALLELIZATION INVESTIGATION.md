# Slice 1 — parallelization investigation

## Inventory

The current broad discovery contains 129 `test_*.py` modules, including the
runner test added in Slice 3. The corrected conservative classification is:

- 38 parallel-safe candidates: pure contract/schema/fixture computation with
  no detected temp, subprocess, environment, logger, release, or concurrency
  surface;
- 55 provisionally isolated modules: temporary directories, subprocesses, or
  mock-heavy integration surfaces requiring explicit isolation proof; and
- 36 serial-only modules: logging/process-global mutation, release/build,
  concurrency/locking, or historically sensitive runtime integration.

The classification is investigatory, not yet a supported checked-in runner
manifest. Full module membership is recorded in `TEST MODULE CLASSIFICATION.md`.

## Order dependency found

The first direct-module probe failed six imports because some test modules rely
on earlier modules inserting `astrowoof_natal/src` into `sys.path`. Normal
alphabetical discovery hides this dependency. Every shard runner must set one
explicit, identical `PYTHONPATH` before collection. It must not rely on import
side effects from another test module.

After adding the explicit source path, the historical frozen 39-module Slice 1
inventory produced
the same 239 tests and 41 skips at all worker counts:

| Workers | Result | Tests | Skips | Wall time | Relative reduction |
|---:|---|---:|---:|---:|---:|
| 1 | pass | 239 | 41 | 88.253 s | baseline |
| 2 | pass | 239 | 41 | 46.692 s | 47.1% |
| 4 | pass | 239 | 41 | 42.257 s | 52.1% |

Four-way round-robin gained only 4.4 seconds over two workers because two
heavy shards took roughly 37 and 42 seconds while the other two finished in
roughly 1–2 seconds. Module-count balancing is therefore inadequate.

## Recommendation

1. Start the supported prototype at two workers.
2. Use deterministic weighted assignment from checked-in measured module
   weights, with lexical tie-breaking—not dynamic work stealing.
3. Set explicit `PYTHONPATH` and strip provider/R2/Render/database credentials
   in every worker.
4. Give every worker unique temp/cache/output roots.
5. Keep the 35-module serial group and every final artifact gate serial.
6. Promote modules from the provisional group only after direct filesystem,
   environment, subprocess, and repeat-equivalence proof.
7. Compare collected test identities in Slice 4; the Slice 1 probe compared
   frozen module membership plus aggregate test/skip outcomes.

## Gate

The evidence supports implementing quiet logging and a deterministic isolated
runner, but does not yet support changing the default broad-suite command.
