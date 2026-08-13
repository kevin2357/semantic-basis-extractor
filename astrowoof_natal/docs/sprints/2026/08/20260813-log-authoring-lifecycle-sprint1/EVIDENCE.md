# Authoring Lifecycle and Structured Logging Sprint 1 Evidence

## Slice 1: contract vocabulary and schemas

Status: implementation complete; consumer review pending.

Artifacts:

- `astrowoof_natal_authoring/lifecycle_contracts.py`
- `resources/contracts/authoring-lifecycle-contracts.schema.json`
- seven sanitized fixtures under `resources/fixtures/lifecycle/`
- `tests/test_lifecycle_contracts.py`
- `SLICE 1 CONTRACT.md`

Focused contract and retained release-contract tests:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_release_contracts -v

Ran 21 tests in 0.307s
OK
```

The original eight focused tests cover all initial fixture shapes, rejection of unsupported
versions and unknown required fields, schema/Python vocabulary agreement,
precondition/result checkpoint separation, stable non-executable presentation
ordering, canonical serialization, recursive protected-field detection, and
rejection of unknown event names and raw lease/protected fields.

API review revisions added three focused tests (11 total) covering explicit action
provider/evidence facts and quiescence, permitted request-observation exclusivity
strengthening with invariant mismatch rejection, and typed refusal without a
mutation checkpoint. The applied result now echoes the immutable action binding;
the seventh fixture demonstrates a raced/provider-identity refusal.

Full repository regression suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 174 tests in 135.557s
OK
```

Package-data qualification:

```text
python -m pip wheel --no-deps --no-build-isolation --wheel-dir <temp> .
Successfully built astrowoof-natal-authoring

required_members=8
missing=[]
```

The eight required members are the lifecycle vocabulary module, combined public
schema, and six sanitized contract fixtures. This was a qualification build only;
it was not promoted or published.

Consumer gate:

- API-agent review completed and approved the boundary subject to four required
  revisions and two small improvements. All requested revisions were implemented;
  event-name-specific payload contracts are recorded as a required Slice 5 gate.

## Slice 2: read-only lifecycle inspection

Status: complete.

Artifacts:

- `astrowoof_natal_authoring/lifecycle.py`
- `tests/test_lifecycle_inspection.py`
- `SLICE 2 INSPECTION.md`

Focused lifecycle qualification:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_lifecycle_inspection -v

Ran 18 tests in 0.340s
OK
```

Coverage includes schema-valid prepared inspection, exact byte-level non-mutation,
snapshot mismatch fail-closed behavior, provider identity/evidence/consumption,
reported-action completion, terminal publishable delivery, review/budget/ambiguity
distinctions, typed local dependencies and quiescence, and deterministic output with
only the documented observation time varied.

Full repository regression suite after Slice 2:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 184 tests in 126.930s
OK
```

## Slice 3: negative authorization and provider-less disposition

Status: complete.

Artifacts:

- `deny_providerless_action()` in `astrowoof_natal_authoring/lifecycle.py`
- `tests/test_negative_authorization.py`
- `SLICE 3 NEGATIVE AUTHORIZATION.md`

Focused mutation qualification:

```text
python -m unittest \
  astrowoof_natal.tests.test_negative_authorization.TestNegativeAuthorization -v

Ran 10 tests in 0.686s
OK
```

Coverage includes provider-free prepared denial, authorized/unconsumed denial with
preserved authorization history, byte-stable idempotent replay, stale observation,
provider identity and consumption races, ambiguous identity-less submission,
immutable-binding mismatch, closed denial-reason rejection, single-writer lock
refusal, and exact multi-action targeting. Refusal comparisons exclude only the
non-authoritative `spend-consumption.lock`; every snapshot-authoritative byte is
unchanged.

Full repository regression suite after Slice 3:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 194 tests in 128.956s
OK
```

An initial discovery run reported 201 passes because the Slice 3 module imported a
Slice 2 `TestCase`, causing seven tests to execute twice. The fixture dependency was
removed and the clean distinct-test count is 194.

## Slice 4: idempotent terminal closeout

Status: complete.

Artifacts:

- `closeout_run()` and constrained interrupted-commit recovery in
  `astrowoof_natal_authoring/lifecycle.py`
- `tests/test_lifecycle_closeout.py`
- `SLICE 4 CLOSEOUT.md`

Focused qualification:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_closeout -v

Ran 9 tests in 1.568s
OK
```

Coverage includes continuation closeout, completed publishable delivery with exact
accepted-byte preservation, ambiguous unresolved provider work, byte-stable replay,
active known provider identity, reported/reconciled evidence without false provider
continuation, inspect-to-closeout decision-basis correlation, injected restart at all
four durable-write boundaries, and fail-closed recovery for unrelated, missing, or
altered bytes.

Full repository regression suite after Slice 4:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 202 tests in 130.352s
OK
```

API-agent review required removal of exception-only refusal behavior. Combined
denial was removed from closeout; consumers use the typed stepwise denial result,
fresh inspection, then closeout. The review also requested and received the known-
provider and decision-basis correlation coverage described above. A new full-suite
run follows these revisions.

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 203 tests in 140.635s
OK
```

## Slice 5: structured execution events

Status: complete.

Artifacts:

- `astrowoof_natal_authoring/execution_events.py`
- `resources/contracts/execution-event-payload-catalog.v1.json`
- event wiring in provider spend control, CLI lifecycle, provider-less denial, and
  closeout
- `tests/test_execution_events.py`
- `SLICE 5 EVENTS.md`

Focused event/lifecycle qualification:

```text
python -m unittest astrowoof_natal.tests.test_execution_events \
  astrowoof_natal.tests.test_negative_authorization \
  astrowoof_natal.tests.test_lifecycle_closeout -v

Ran 27 tests in 2.102s
OK
```

An additional focused provider sequence test passed, proving exact action correlation
across authorization, submission start, provider identity, waiting, and completion.
Coverage also includes packaged catalog agreement, typed payload enforcement,
recursive redaction, deterministic envelopes, JSONL file framing, stdout result
framing, sink failure isolation, denial observation, and closeout truth preserved
when events are lost.

Full repository regression suite after Slice 5:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 212 tests in 130.515s
OK
```

## Slice 6: consumer surface and installed-runtime qualification

Status: complete.

Artifacts:

- `astrowoof-authoring-lifecycle` console entry point
- `astrowoof-lifecycle-smoke` console entry point
- `astrowoof_natal_authoring/cli/lifecycle.py`
- `astrowoof_natal_authoring/lifecycle_smoke.py`
- `tests/test_lifecycle_consumer.py`
- `docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`
- `SLICE 6 CONSUMER.md`

Focused source consumer tests:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_consumer -v

Ran 2 tests in 0.949s
OK
```

Fresh installed-wheel qualification:

```text
pip wheel --no-deps --no-build-isolation --wheel-dir <temp>/dist .
python -m venv <temp>/venv
<temp>/venv/python -m pip install --no-index --no-deps <wheel>
<temp>/venv/python -m astrowoof_natal_authoring.lifecycle_smoke \
  --require-installed --work-dir <temp>/smoke-work

status=pass
runtime_module=<temp>/venv/Lib/site-packages/astrowoof_natal_authoring
```

Qualification wheel:

- filename: `astrowoof_natal_authoring-0.2.2-py3-none-any.whl`
- SHA-256: `29914a16f4c64075575cd5754796bc5bedef7c9573eea4f03db2c4dbd2dcc7fe`
- status: temporary qualification only; not promoted, tagged, published, or accepted
  as the next pinnable artifact

Installed checks passed for packaged resources, prepared eligibility, applied native
denial, post-denial classification, closeout disposition/replay, representative
events, and complete final snapshot.

Both installed console scripts were invoked from the fresh venv outside the source
tree:

- `astrowoof-lifecycle-smoke --require-installed`: pass
- `astrowoof-authoring-lifecycle --run-dir <installed-smoke-run> inspect`: pass,
  returned `astrowoof.authoring_lifecycle_inspection.v0.1` with a valid snapshot

Full repository regression suite after Slice 6:

```text
python -m unittest discover -s astrowoof_natal/tests -p 'test_*.py'

Ran 214 tests in 146.637s
OK
```

## Sprint acceptance

All six slice gates pass. The sprint provides versioned lifecycle contracts,
read-only inspection, native provider-less denial, idempotent recoverable closeout,
typed structured events, dedicated installed consumer commands, packaged schemas and
fixtures, installed smoke, and API handoff. No provider operation was submitted and
qualification cost was `$0`.

Release tagging, artifact promotion, publication, and API pinning are outside this
sprint checkpoint and remain unperformed.
