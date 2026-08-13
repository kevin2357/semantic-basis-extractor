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
