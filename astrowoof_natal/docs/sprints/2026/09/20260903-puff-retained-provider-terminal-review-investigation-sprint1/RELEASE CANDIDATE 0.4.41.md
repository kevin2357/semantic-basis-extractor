# Release candidate 0.4.41

## Scope

This candidate has two intentionally independent corrections:

1. Theme-group assignment, coverage, and balance QA is dormant. Theme-group
   fields remain compatibility data, but the evaluators do not run, gate,
   retry, finalize, emit advisories, or log runtime findings.
2. Exact ordinary-v2 interactive optional-stage reconciliation evidence can be
   adopted into its matching stored polish, qualitative-critic, or
   qualitative-candidate attempt before that consumer reaches a provider-create
   boundary. Batch and bounded routes are unchanged.

No public lifecycle, command-result, or API schema changes are introduced.

## Candidate identity

- Version: `0.4.41`
- Deterministic wheel SHA-256:
  `4eb8afada01ae6c4d239d75387b75b32a4ee7756a78d742a48cfad99de848841`
- Deterministic build input: `SOURCE_DATE_EPOCH=315532800`
- Companion dependency: `semantic-projection-core 0.11.1`
- Release source commit: `46c19f7`

## Qualification

- Source focused suite: 8/8 passed.
- Same focused suite with the candidate wheel imported from an isolated target:
  8/8 passed.
- Fresh virtual environment: candidate installed, `pip check` passed, and
  `astrowoof-release-smoke --require-installed` passed.
- Two deterministic wheel builds matched byte-for-byte.
- Provider calls, R2 access, retained-QA access, and spend: zero.

This is release evidence only. Tagging and publication remain subject to the
separate owner/API final gate.
