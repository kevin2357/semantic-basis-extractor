# Slice 2 — quiet test harness

## Result

Implemented a repository-only quiet logging boundary in the new test-suite
coordinator. Production package logging, installed CLIs, event streams, and
application sinks are unchanged.

Ordinary coordinated test groups receive a per-worker `sitecustomize.py` on an
explicit worker-only `PYTHONPATH`. It applies:

```python
logging.disable(logging.INFO)
```

This suppresses routine Sparkle Dog INFO output in that worker and in Python
subprocesses inheriting its explicit environment. Warnings and errors remain
visible. The parent process and normal production invocations are unaffected.

Tests whose subject is logging, structured events, stderr relay, reporting, or
trace observability are listed in the manifest's `logging_sensitive` inventory.
They run in a separate unquiet serial group.

## Classification correction

The first quiet parallel run found two honest failures in
`test_decision_evidence_observability_qa.py`: its qualification consumes INFO
trace units. The module was incorrectly classified as a pure parallel
candidate.

It was moved from parallel-safe to serial/logging-sensitive. No assertion or
runtime behavior was weakened. The frozen classification is now:

- 38 parallel-safe candidates;
- 55 provisional modules, including the new runner-test module; and
- 36 serial-only modules.

## Verification

The runner-focused suite passed:

```text
Ran 8 tests
OK
```

The protected logging inventory passed without quieting:

```text
Ran 89 tests in 8.312s
OK (skipped=4)
```

Dedicated tests prove that the bootstrap suppresses INFO in a child Python
process, preserves WARNING, and does not change the parent logging threshold.
The worker sanitizer removes every inherited `ASTROWOOF_*` value, including
`ASTROWOOF_DATABASE_URL` and `ASTROWOOF_OPENAI_API_KEY`; the coordinator then
sets only its owned non-secret `ASTROWOOF_TEST_OUTPUT_ROOT`. A subprocess
regression proves the named secrets are absent in the child environment.

The stricter sanitizer was also exercised through the complete approved
parallel subset: 236 tests passed with 40 skips and the unchanged inventory
digest in 43.614 seconds.

Slice 4's first broad coordinated run found one further protected surface:
`test_external_authority_execution.py` contains an `assertLogs(INFO)` contract
test. The module was already serial-only and was moved from the quiet serial
subgroup to the unquiet observability subgroup. The underlying test correctly
remained unchanged.

## Boundary

This slice adds no installed-package behavior and does not change the existing
broad-suite command. Quieting exists only when the repository coordinator
constructs an explicitly isolated test environment.
