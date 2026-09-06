# Evidence

## Slice 0 sources

- Existing implementation:
  `astrowoof_natal/src/astrowoof_natal_authoring/run_report.py`
- Existing focused tests:
  `astrowoof_natal/tests/test_run_report.py`
- Existing operator guide:
  `astrowoof_natal/docs/post_extraction_authoring/Run Evolution Reporter.md`
- Original reporter sprint:
  `astrowoof_natal/docs/sprints/2026/08/20260831-run-evolution-matrix-reporter-mini-sprint1`
- Better Stack source ID `2740198`, complete observed window from
  `2026-09-06T18:03:00Z` through final publication at
  `2026-09-06T18:30:40.234Z`.
- Hand-built proof-of-concept exported locally as
  `C:\tmp\astrowoof-current-three-run-timeline.html`; this is illustrative
  evidence, not a committed contract fixture.

## Frozen run identities

| API run | Native run |
|---|---|
| `70423106-000c-4bc1-a790-fdbf6a2dfb4d` | `aa60af4c2e6c65f613fb276d61ce0a8c246d42b401c244de4b086eff7c23e966` |
| `67a369ac-1953-447c-b3ae-bb19fd7cd994` | `3c59bd1668a29b0735375528630d13c66c2b80a108be3b5c802868dd121199fb` |
| `665cd3d2-332a-4ba7-9c0b-bb3fb4e1a177` | `468479aa4a8d818392b2705919817c2ebca44cab78e3868657f8746b5e50f50e` |

## Gate result

Slices 0–2 are complete. The projection contract, execution-event adapter, and
deterministic interval reducer are implemented; interactive rendering remains
the next slice.

The principal evidence correction is that a shared cohort clock is not purely
an SBE-log rendering concern: the directly observed claim, defer, lease, and
outer-cycle boundaries are API worker-wrapper evidence. The new artifact must
preserve that ownership rather than flatten all rows into native SBE truth.

## Slice 1 contract evidence

- `astrowoof_natal/src/astrowoof_natal_authoring/run_timeline.py`
- `astrowoof_natal/src/astrowoof_natal_authoring/resources/contracts/sbe-run-cohort-timeline.v1.schema.json`
- `astrowoof_natal/tests/test_run_timeline.py`
- Package-root reader and validator exports in
  `astrowoof_natal/src/astrowoof_natal_authoring/__init__.py`

Focused verification:

```text
python -m unittest astrowoof_natal.tests.test_run_timeline astrowoof_natal.tests.test_run_report
```

The contract suite covers the closed schema, defensive reader, canonical
digest, boundary identities, exact run joins, canonical/outer clock relation,
evidence-family closure, terminal-review provenance, calculated handoff, and
the witnessed-not-SLA guardrail. The existing reporter suite remains in the
same focused gate to prove v1 compatibility.

## Slice 2 reducer evidence

- Reducer implementation and adapter:
  `astrowoof_natal/src/astrowoof_natal_authoring/run_timeline.py`
- Mixed native/API and adversarial tests:
  `astrowoof_natal/tests/test_run_timeline.py`
- Public package-root builder export:
  `build_run_cohort_timeline`

Focused verification after the Voof-paws 2 corrections and reducer:

```text
Ran 33 tests in 0.188s
OK (skipped=1)
```

The optional skip is the JSON Schema library check in the minimal runtime; the
strict Python validator and packaged-schema reader both ran. `git diff --check`
was clean apart from Git's informational LF-to-CRLF working-copy warning.

Voof-paws 3 requested an explicit end-to-end proof of the two newly emitted
shapes. The reducer fixture now contains nonzero `adapter_coverage`, paired
`worker.lease.acquired` / `worker.lease.released` evidence classified as
`observed_execution_allocation`, and a JSON artifact round-trip through the
public reader/validator. Both fields were already present in the closed schema
and Python validator when reviewed; the new test makes their joint executable
coverage unmistakable.

## Slice 3 renderer evidence

- Renderer: `render_run_cohort_timeline_html()` in
  `astrowoof_natal/src/astrowoof_natal_authoring/run_timeline.py`
- Public export:
  `astrowoof_natal/src/astrowoof_natal_authoring/__init__.py`
- Renderer contract/adversarial coverage:
  `astrowoof_natal/tests/test_run_timeline.py`

The renderer validates before rendering, embeds only the closed diagnostic
artifact, performs no fetch/network operation, and escapes script terminators.
Its controls are presentation-only: none mutate, reinterpret, or feed back into
the timeline projection.

## Slice 4 CLI evidence

The existing `astrowoof-run-report` entry point now exercises the projection,
public reader, and renderer. Focused tests prove:

- explicit timeline build from mixed evidence;
- combined build produces the original four files plus two timeline files;
- native-only input still produces exactly the original four files;
- timeline HTML re-rendering reads the public closed JSON artifact;
- display timezone is presentation metadata only; and
- HTTP(S) input is refused before file access.

## Slice 5 qualification evidence

- Qualification implementation:
  `astrowoof_natal/src/astrowoof_natal_authoring/run_timeline_qa.py`
- Closed packaged receipt schema:
  `astrowoof_natal/src/astrowoof_natal_authoring/resources/contracts/sbe-run-cohort-timeline-qualification.v1.schema.json`
- Qualification tests:
  `astrowoof_natal/tests/test_run_timeline_qa.py`
- Installed entry point: `astrowoof-run-timeline-qa`

Current deterministic source receipt:

```text
timeline_sha256 = 2956a38644893c83428d884b6cec7500b12391eb5fc0f443d548d14b9f441d0a
html_sha256     = 46a9f92b9cbefa002f44687958c007f2e52feb7a1cdbbe4a3005a833489b8909
receipt_sha256  = 2d65be16c87eb1a6f104868957bc3b1b16980f6ca556aaa9a8aab98cad4d31f0
```

Focused source verification:

```text
Ran 43 tests in 0.723s
OK (skipped=2)
```

The skips are optional `jsonschema` checks in the minimal test runtime. Both
strict Python validators and both packaged schema readers executed. No provider,
network, R2, retained-run, or API mutation occurred.

## Slice 6 source regression gate

The version and version-derived fixture were updated to `0.4.52` before the
expensive gate. The broad provider-free suite then completed once, without a
version-correction rerun:

```text
Ran 1103 tests in 1083.232s
OK (skipped=58)
```

The expanded focused reporter, qualification, release-contract, and smoke
matrix also passed:

```text
Ran 69 tests in 28.584s
OK (skipped=5)
```

The large broad-suite stream was routine structured `INFO` diagnostic output;
it contained no test failures. Reducing that test-only output and investigating
safe deterministic sharding are deliberately separated into the adjacent
`20260906-test-suite-output-and-parallel-execution-sprint1` tooling sprint.
