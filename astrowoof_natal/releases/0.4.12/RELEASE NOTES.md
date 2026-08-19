# AstroWoof Natal Authoring 0.4.12 Release

Status: published and verified

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
  before publication: pass.
- Provider calls/submissions/spend: 0 / 0 / USD 0.

The qualified wheel is 852,249 bytes with SHA-256
`8a3822a2c76ccf8d436c928a3fc2056388653a046af26292fb2d85dfd9a0492e`.

The immutable tag points to `8c03a1b12970e179b7d70dcf44b4e13b4b9c9329`.
GitHub's published asset size and digest match the qualified wheel. This
post-publication evidence does not move the tag.
