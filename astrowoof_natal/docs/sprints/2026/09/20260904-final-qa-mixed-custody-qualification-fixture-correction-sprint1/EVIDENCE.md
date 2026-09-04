# Evidence — final-QA mixed-custody qualification fixture correction

## Safety boundary

- Provider-free only.
- No QA database, R2, retained workspace, provider, credential, or spend access.
- No production lifecycle, authority, dispatch, or result contract was
  widened. One provider-free qualification receipt advanced from v1 to v2
  because its former success cell depended on the intentionally removed
  theme-group artifact; the historical v1 schema remains packaged.

## Reproduction

Before correction:

```text
python -m unittest astrowoof_natal.tests.test_final_qa_mixed_custody_qa
Ran 3 tests: 3 errors
ValueError: Lifecycle checkpoint has no external-authority request
```

The exception was correct: the fixture had already committed final-QA review
evidence before requesting new polish authority.

## Corrected focused result

```text
python -m unittest astrowoof_natal.tests.test_final_qa_mixed_custody_qa
Ran 4 tests: OK
```

The four direct tests cover the complete provider-free qualification, public CLI/schema
reader, rehashed receipt mutation, and the authority-before-finalization ordering
guard.

Expanded adjacent matrix:

```text
57 tests passed; 1 expected optional-schema skip
```

This includes the older mixed-custody characterization, terminal dominance,
terminal review, provider-pending capacity, and public ordinary-v2 CLI tests.

## Full-suite evidence

The first full discovery run was intentionally retained as evidence rather than
reported as green:

```text
Ran 1040 tests in 817.495s
FAILED (failures=13, errors=4, skipped=52)
```

Classification and correction:

- 12 stale tracked assertions were updated to the already-released runtime
  semantics; their 102-test module matrix then passed.
- 5 untracked historical wheel-battle cases caused 2 errors and were archived
  outside automatic discovery.
- the obsolete theme-dependent Waffle/Scone qualification caused 2 errors and
  was advanced to a closed v2 theme-free success cell;
- the zero-action smoke's old terminal-review expectation caused 1 failure and
  was corrected to assert successful delivery, no terminal result ID, and
  completed cleanup.

Canonical maintained-suite rerun:

```text
Ran 1035 tests in 879.417s
OK (skipped=52)
```

## Release-gate assessment

The `0.4.46` focused gate was incomplete. Because terminal dominance changed a
shared finalization selector, the canonical runbook classifies that release as a
broad/full-gate candidate. Even under a focused exception, this packaged
mixed-custody qualification was a directly affected transitive consumer and
should have been run.

The replacement used the full maintained-suite gate requested by API. Final
release still requires deterministic committed-source wheels, installed public
qualification, and the exact API release-pair rerun against the candidate hash.
