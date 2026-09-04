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

## Committed-source candidate

- Artifact-source commit:
  `31a09e472bae871a0105d7a5e5719592b9a92407`
- Version: `0.4.47`
- `SOURCE_DATE_EPOCH`: `1788547986`
- Wheel: `astrowoof_natal_authoring-0.4.47-py3-none-any.whl`
- Size: `1,199,948` bytes
- SHA-256:
  `4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`
- Independent builds: 2; byte-identical
- Wheel members: 258; absolute paths: 0
- SPC wheel SHA-256:
  `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`
- Installed versions: SBE `0.4.47`, SPC `0.11.1`
- `pip check`: pass

Installed public command results:

- `astrowoof-final-qa-mixed-custody-qa`: pass; receipt digest
  `c99f5631c16cb4150b3188bd58908b391985fbefb82a3a5d0e506e3fabd16850`;
  zero external calls, provider creates, or spend.
- `astrowoof-terminal-review-qa --detailed`: pass; receipt digest
  `190cbe74ee086835bba9a0d7af39a552b36049a9eaa64e88f9ee6c7a438b2de2`.
- `astrowoof-finalization-boundary-qa`: pass; v2 receipt digest
  `e1d32b2a3830fe2a620643dda0aedc8f5d594db3169c222d326fa52e3b5c904a`;
  zero external calls, provider creates, or spend.
- `astrowoof-release-smoke --require-installed`: pass;
  `DELIVERY_COMPLETE`, no terminal-review result ID, cleanup complete.

The exact API Sprint 76 release-pair gate remains required against this wheel
before owner authorization to tag and publish.
