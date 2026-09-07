# Slice 3 — deterministic runner and xdist comparison

## Implemented coordinator

Added `astrowoof_natal/scripts/run_test_suite.py` and a checked-in closed
classification manifest at `astrowoof_natal/tests/test_suite_manifest.json`.

The coordinator:

- validates that every discovered `test_*.py` module is classified exactly
  once;
- uses measured per-module weights and deterministic largest-first assignment
  with lexical tie-breaking;
- sets explicit source and repository import paths;
- removes every inherited `ASTROWOOF_*` value plus generic OpenAI, AWS,
  Cloudflare, Render, and database credential variables from worker
  environments, then supplies only coordinator-owned non-secret test output;
- creates unique temp, cache, coverage, log, workspace/output roots per group;
- runs ordinary `unittest` in isolated subprocesses;
- protects logging-sensitive tests from quieting;
- preserves stdout/stderr only on failure or explicit verbose mode; and
- writes a deterministic-shape JSON receipt with exact test identities, shard
  commands, outcomes, skips, timings, and failure evidence.

The manifest also supports a calibration mode that measures every approved
parallel module independently. Those 38 measurements are checked in as the
initial deterministic weights.

## Weighted two-worker result

Command:

```powershell
python astrowoof_natal/scripts/run_test_suite.py `
  --workers 2 `
  --parallel-only `
  --work-root .tmp-test-suite-weighted `
  --receipt .tmp-test-suite-weighted/receipt.json
```

Result:

| Group | Modules | Tests | Skips | Wall time | Result |
|---|---:|---:|---:|---:|---|
| parallel-1 | 20 | 136 | 22 | 44.400 s | pass |
| parallel-2 | 18 | 100 | 18 | 46.478 s | pass |
| aggregate | 38 | 236 | 40 | 46.498 s | pass |

Test inventory SHA-256:
`b5579d244013a179ed82977cac909fb5ccbe614829dadf80f6d1b3fa36cdf87b`.

The two shards finished within 2.1 seconds of one another. This corrects the
severe imbalance seen in Slice 1's four-worker module-count round robin.
An earlier corrected equal-weight rerun also passed the same 236/40 inventory
with the same identity digest in 64.378 seconds; the measured weighting reduced
that observed wall time by 17.880 seconds without changing membership or
outcomes.

The candidate inventory changed from Slice 1's 239/41 only because the three
tests and one skip in the misclassified decision-evidence observability module
moved into the protected serial inventory.

## Bounded pytest-xdist comparison

For evaluation only, pytest 9.1.1 and pytest-xdist 3.8.0 were installed into an
ignored repository-local temporary directory. They are not project or package
dependencies.

The same 38 files ran with two workers and `--dist=loadfile`, with explicit
source paths, credential removal, quiet bootstrap, and isolated base temp.

Result:

```text
196 passed, 40 skipped, 198 subtests passed in 55.42s
XDIST_EXIT=0 WALL_SECONDS=57.384 MODULES=38
```

Pytest's 196 passed plus 40 skipped are the same 236 top-level unittest tests;
it reports 198 successful unittest subtests separately. No behavioral failure
was found.

The comparison nevertheless does not favor adoption:

- wall time was 57.384 seconds versus 46.498 seconds for the coordinator;
- xdist grouped files but dynamically selected worker ownership, whereas the
  coordinator records stable checked-in weighted membership;
- pytest attempted to use the shared repository `.pytest_cache` and emitted a
  permissions warning, requiring another project-specific isolation control;
- pytest/xdist add runner dependencies and reporting semantics without
  removing the need for the manifest, credential sanitation, unique roots,
  serial tail, or aggregate receipt; and
- direct unittest failure reproduction remains closer to the supported suite.

Decision: record xdist as evaluated but do not adopt it. Retain the thin custom
coordinator for the Slice 4 equivalence and isolation campaign.

## Current gate

Slices 2–3 are complete. The runner is a prototype, not yet the documented
default broad-suite or release command. CI and release-playbook adoption remain
blocked on repeated Slice 4 equivalence, isolation, failure-injection, and
Windows file-lock evidence.
