# API Voof-paws 6 review — installed-wheel consumer handoff

## Decision

**Approved for Slice 8 release preparation, subject to a fresh immutable release
version.** API does not yet pin or deploy the candidate.

## Accepted public surface

- Closed v0.8 lifecycle schema/reader/validator and validated mixed-custody
  fixture are packaged and included in the hash-bound consumer fixture manifest.
- The provider-free `astrowoof-retry-lineage-qa` command has no production input
  surface and refuses output beneath a native workspace.
- The qualification receipt binds package and qualification-schema identity,
  retains only bounded/sanitized evidence, and carries the explicit interactive
  route scope plus Batch deferral.
- The handoff keeps the ownership boundary correct: API validates whole native
  evidence, preserves the selected command, and never selects reconciliation
  members or reconstructs actions.

## Required release hygiene

The Slice 7 candidate identifies itself as version `0.4.28`, but SBE `0.4.28`
is already immutable and pinned by API. The candidate bytes must therefore be
published under a fresh version and tag; do not publish different artifacts as
another `0.4.28`.

The release record should provide the new version, source commit, wheel SHA-256,
and installed-wheel receipt. API will then pin that exact artifact and run its
companion intake/mapping/joint qualification before any QA deployment or cohort.

## API work still required

API Sprint 56 must use the installed public v0.8 validator/fixtures to prove:

1. malformed/mixed evidence becomes a typed contract error before worker queue
   failure or capacity release;
2. provider custody plus conflict remains SBE-selected reconciliation;
3. post-custody conflict stays a nonterminal, non-dispatching review posture;
4. authority/request/grant/action/binding joins remain exact; and
5. no consumer test invents action selection or provider work.

No API provider, queue, R2, retained-workspace, configuration, deployment, or
release action occurred during this review.
