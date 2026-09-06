# Evidence — quiet tests and safe parallel execution

## Baseline

SBE `0.4.52` broad gate: 1,103 tests in 1,083.232 seconds, 58 skips, pass.

## Logging sample

`test_external_authority_v2_cli.py` passed under both configurations:

- INFO: 2.699 seconds, 304,919 captured stderr bytes.
- test-only INFO suppression: 2.471 seconds, 107 captured stderr bytes.

## Parallel-safe candidate probe

Explicit source path and credential-stripped environment were used. Frozen
inventory: 39 modules, 239 tests, 41 skips.

- one worker: pass, 88.253 seconds;
- two workers: pass, 46.692 seconds;
- four workers: pass, 42.257 seconds.

The pre-correction probe is retained as negative evidence: direct module
execution without explicit `PYTHONPATH` produced six import errors because
normal serial discovery had hidden module-order path mutation.

No provider, R2, Render, QA, database, retained workspace, build, wheel, or
release operation occurred.
