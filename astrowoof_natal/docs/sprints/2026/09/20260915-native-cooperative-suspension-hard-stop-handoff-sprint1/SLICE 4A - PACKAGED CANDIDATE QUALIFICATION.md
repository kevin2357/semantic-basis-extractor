# Slice 4A — Packaged Candidate Qualification

## Purpose

This slice breaks the release-pair dependency cycle. SBE first supplies one
exact installed candidate and a provider-free public receipt. API can then wire
that candidate into its real subprocess adapter in API Slice 3B. Joined API/SBE
behavior remains Slice 4B.

## Public qualification

`astrowoof-native-suspension-qa` uses a disposable exact-interactive
ordinary-v2 workspace and launches `astrowoof-external-authority-v2` as a real
child process. It validates only the exact output document and immutable public
artifacts; stderr text and mutable status names are not authority.

The closed receipt proves:

- exit 0 with an exact suspension command result;
- checkpointed suspension before provider create;
- exact result/receipt/output joins and inert replay;
- no ambiguous or newly created provider custody;
- unrelated-workspace refusal;
- installed contract-schema and fixture-bundle availability; and
- zero provider create/retrieve, spend, network, live process termination, and
  API resource release.

The package root exports the contract schema/fixture readers, document
validators, and qualification reader/validator for API Slice 3B.

## Source evidence

- Qualification module: 3 passed, 1 expected optional-schema skip.
- Suspension plus neighboring v2/reconciliation matrix: 115 passed, 3 expected
  optional skips.
- `compileall` and `git diff --check` are required before the candidate commit.

## Remaining 4A gate

Build the committed `0.4.65` candidate, install it into a disposable clean
Python 3.11 environment, prove imports resolve from `site-packages`, run
`pip check`, invoke the installed console command, validate its receipt and
schema, and record wheel SHA-256/size/source commit. This is not tag or publish
authorization.
