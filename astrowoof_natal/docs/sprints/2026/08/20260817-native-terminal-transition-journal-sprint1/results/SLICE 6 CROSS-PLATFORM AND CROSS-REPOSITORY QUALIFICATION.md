# Slice 6 Cross-Platform and Cross-Repository Qualification

Date: 2026-08-17
Status: SBE-native gate passed; API operational trace pending

## Outcome

The candidate SBE artifact is reproducible and passes source plus installed-runtime
qualification on Windows and Linux. Its packaged native-transition matrix agrees
with the real API Sprint 26 validator without provider access. The remaining joint
gate is the API-owned worker/PostgreSQL/R2 terminal-first trace.

## Source qualification

The first complete run exposed an obsolete checkpoint-repair test fixture that
used short placeholder request/profile digests. Strict journal validation correctly
refused those values. The fixture was corrected to canonical SHA-256 identities;
production validation was not weakened.

- Checkpoint-repair focus: 8 passed in 1.101 seconds.
- Complete suite: 383 passed in 247.272 seconds, with 4 expected skips.
- Provider operations: 0.
- Paid spend: `$0`.

## Reproducible artifact

Two builds used source commit `c25f47e` and
`SOURCE_DATE_EPOCH=1787031309`. They were byte-identical:

```text
astrowoof_natal_authoring-0.4.4-py3-none-any.whl
sha256 1fa992b07cef80725829137c4d6f1871f65d0b01e1f53b69d9bf4eaa78c05b26
```

The wheel has 98 members. It includes `py.typed`, the native-transition schemas,
and `consumer-ingestion-cases.v0.1.json`; it excludes source tests.

## Installed platforms

Both installed gates used the exact published SPC 0.11.0 wheel:

```text
sha256 82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d
```

- Windows CPython 3.11: clean external venv, `pip check`, packaged resources, and
  installed lifecycle smoke passed.
- Linux `python:3.11-slim`: clean container install, `pip check`, packaged
  resources, and installed lifecycle smoke passed.

## API fixture parity

The API Sprint 26 focused ingestion module passed all 6 tests. The packaged SBE
matrix was then supplied directly to the real API validator:

- exact Response delivery: accepted;
- exact Response review: accepted;
- exact Batch provider failure: accepted;
- exact Response pending custody: accepted;
- bounded Response ambiguity: accepted;
- conflicting second operation/review: accepted;
- exact replay: accepted; and
- malformed result: refused for invalid native result identity.

This proves schema and semantic-oracle parity. It does not claim API persistence,
lease, capacity, R2, or public-state behavior.

## Remaining joint gate

The API companion sprint must still run the provider-free Aster-shaped result
through its real worker boundary and prove transactional evidence ingestion,
terminal-first classification, lease/capacity handling, PostgreSQL/R2 behavior,
replay, cleanup, and zero second provider operation. Those are API-owned claims;
Slice 6 remains open only for that trace.
