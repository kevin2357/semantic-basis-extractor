# Authoring Lifecycle and Structured Logging Sprint 1 Evidence

## Slice 1: contract vocabulary and schemas

Status: implementation complete; consumer review pending.

Artifacts:

- `astrowoof_natal_authoring/lifecycle_contracts.py`
- `resources/contracts/authoring-lifecycle-contracts.schema.json`
- six sanitized fixtures under `resources/fixtures/lifecycle/`
- `tests/test_lifecycle_contracts.py`
- `SLICE 1 CONTRACT.md`

Focused contract and retained release-contract tests:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_release_contracts -v

Ran 21 tests in 0.307s
OK
```

The eight new focused tests cover all fixture shapes, rejection of unsupported
versions and unknown required fields, schema/Python vocabulary agreement,
precondition/result checkpoint separation, stable non-executable presentation
ordering, canonical serialization, recursive protected-field detection, and
rejection of unknown event names and raw lease/protected fields.

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

- Pending AstroWoof API-agent review of the schema, vocabularies, fixtures, and
  read-only inspection shape.
