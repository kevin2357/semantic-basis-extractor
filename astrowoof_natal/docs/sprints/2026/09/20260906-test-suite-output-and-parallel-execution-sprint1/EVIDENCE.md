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

## Slice 2

- Runner unit tests: 8 passed.
- Protected logging/trace inventory: 89 passed, 4 skipped.
- An initial quiet integration run correctly exposed
  `test_decision_evidence_observability_qa.py` as logging-sensitive; it was
  reclassified from parallel-safe to protected serial without changing an
  assertion.
- Production package logging and installed CLI behavior were not changed.
- Direct subprocess sanitation proves `ASTROWOOF_DATABASE_URL`,
  `ASTROWOOF_OPENAI_API_KEY`, and arbitrary inherited `ASTROWOOF_*` values do
  not reach workers.
- Post-correction weighted rerun under the stricter sanitizer: 236 tests,
  40 skips, pass, 43.614 seconds, unchanged inventory SHA-256
  `b5579d244013a179ed82977cac909fb5ccbe614829dadf80f6d1b3fa36cdf87b`.

## Slice 3

- Measured all 38 approved candidate modules independently and checked their
  durations into the manifest.
- Weighted two-worker coordinator: 236 tests, 40 skips, pass, 46.498 seconds.
- Corrected equal-weight precursor: the same 236 tests, 40 skips, and inventory
  digest passed in 64.378 seconds.
- Shard wall times: 44.400 and 46.478 seconds.
- Inventory SHA-256:
  `b5579d244013a179ed82977cac909fb5ccbe614829dadf80f6d1b3fa36cdf87b`.
- pytest 9.1.1 + pytest-xdist 3.8.0 bounded comparison: same 236 top-level
  outcomes (196 passed, 40 skipped; 198 subtests separately reported), pass,
  57.384 seconds.
- xdist is not recommended for adoption: it was slower, attempted a shared
  pytest cache, and did not replace the required manifest/isolation/receipt
  controls.
- No default command, CI, release playbook, package dependency, or installed
  artifact changed.

## Slice 4 classification feedback

- The first complete coordinated gate ran 1,114 tests with 58 skips.
- Both parallel groups passed; the unquiet observability group passed.
- The quiet serial group had one failure because
  `test_external_authority_execution.py` deliberately asserts an INFO log.
- That already-serial module was moved to the protected logging inventory; no
  test assertion or installed behavior changed.

## Slice 4 final equivalence and isolation gate

- Final two-worker broad run: 1,115 tests, 58 skips, pass, 1,091.085 seconds.
- Final one-worker broad run: 1,115 tests, 58 skips, pass, 964.806 seconds.
- Exact shared test inventory SHA-256:
  `fd9b735381548e2bab7d732aa1a500b87cfe0008873583952f9b7edd8aefd146`.
- Exact shared outcome inventory SHA-256:
  `4f018b127dec7d3c305ec3372a80224d5ab33a3a2707de75a3db6ca247b0f303`.
- Failures, errors, and unexpected successes: none in either mode.
- Deterministic injected failures in both parallel groups failed the aggregate
  and retained exact reproduction commands.
- All group result paths resolved beneath their owned work roots.
- Package/release surfaces remained unmodified; no provider, R2, Render, QA,
  package publication, or release action occurred.
- No Python test processes remained after the runs.
- Focused runner suite: 10 passed.
- Present performance decision: equivalence and safety are proven, but the
  conservative two-worker invocation was 126.279 seconds slower on this
  laptop. Do not claim a current whole-suite speedup.

## Slice 5 adoption

- Supported broad-confidence entry point:
  `python astrowoof_natal/scripts/run_test_suite.py`.
- Supported default worker count: one.
- Two-worker profile: retained for controlled experiments, not the present
  performance default.
- Direct unittest discovery: retained as the universal fallback.
- Manifest controls reject unclassified discovered modules, stale/nonexistent
  entries, and duplicate classifications before execution.
- Focused runner coverage explicitly freezes all three mismatch cases and the
  one-worker default.
- Release builds and installed-artifact authority remain serial and unchanged.

## Slice 6 final supported-command gate

- Command omitted `--workers` and produced `worker_count=1` in its receipt.
- Result: 1,118 tests, 58 skips, pass, 1,122.983334 seconds.
- Test inventory SHA-256:
  `64540bf668560c4fcb3989673fac93fbead58aab9b9d56d46d2a9e53eef53c69`.
- Outcome inventory SHA-256:
  `a400a525811fd41fa58bf97e45957110b0a29a85d0c955f06143c18133e593de`.
- The three additional tests versus Slice 4 are the adopted-default and
  manifest duplicate/stale-entry controls.
- Focused runner suite before the broad gate: 13 passed.
- No installed package/runtime resource changed; no package release required.
