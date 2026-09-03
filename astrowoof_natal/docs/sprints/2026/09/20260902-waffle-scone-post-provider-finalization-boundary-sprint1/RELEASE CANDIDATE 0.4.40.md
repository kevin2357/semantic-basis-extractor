# Release Candidate — SBE 0.4.40

Status: owner-approved, tagged, published, and independently verified.

## Scope

- remove obsolete final-assembly hard enforcement of advisory-only theme-group
  distribution findings;
- classify only deterministic `AssemblyContractError` as sealed native v0.2
  `review_required / finalization_contract_invalid` with final custody;
- leave operational failures and non-final custody conservative; and
- package the provider-free `astrowoof-finalization-boundary-qa` command and
  closed qualification schema.

No provider, lifecycle-selection, spend, grant, API-resource, Batch, bounded,
R2, or retained-QA authority changed.

## Candidate evidence

- focused runtime matrix: 7 passed;
- terminal-review/theme-policy suites: 12 passed, 2 optional-schema skips;
- deterministic wheel SHA-256:
  `0a5904150eb2a579724f01d050c035a1c66d5f1882e7b19a78fb22775b54d8ad`;
- installed qualification receipt SHA-256:
  `dcbe5100ebd85a6a6fbbc2a5943a3cdacf7a79ad04030ac44309be7efc948587`;
- installed generic smoke: pass;
- `pip check` with SPC `0.11.1`: pass;
- package command/schema surface: pass; and
- diff hygiene: pass.

The full repository suite was intentionally omitted under the narrow release
gate. The candidate must be rebuilt from the authorized committed source and
retain byte-identical wheel and qualification identities before the immutable
tag is created.

## Published identity

- source commit: `bfc80dbe1ea05fb3b9c1cda4a427ec5137c0f85c`;
- annotated tag: `astrowoof-natal-authoring-v0.4.40`;
- wheel SHA-256:
  `0a5904150eb2a579724f01d050c035a1c66d5f1882e7b19a78fb22775b54d8ad`;
- installed qualification receipt SHA-256:
  `dcbe5100ebd85a6a6fbbc2a5943a3cdacf7a79ad04030ac44309be7efc948587`;
- GitHub release:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.40`.

The published wheel was independently downloaded, hash-checked against its
published checksum, installed, dependency-checked, and requalified. The remote
annotated tag peels to the exact source commit above.
