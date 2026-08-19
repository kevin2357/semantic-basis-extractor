# AstroWoof Natal Authoring 0.4.12 Release

## Summary

SBE 0.4.12 fixes the installed-runtime release smoke failure introduced in 0.4.11.
`closure.author_pending_passes()` now imports the intended
`application_logging.logging_context` API used around per-pass worker execution.

There are no lifecycle, spend, provider, editorial, schema, or consumer-contract
changes.

## Qualification

- Source fake-provider release smoke with six-pass authoring and cleanup: pass.
- Focused logging tests: pass.
- Built-wheel installation plus the exact
  `astrowoof-release-smoke --work-dir ... --require-installed` path: required
  before publication.
- Provider calls/submissions/spend: 0 / 0 / USD 0.
