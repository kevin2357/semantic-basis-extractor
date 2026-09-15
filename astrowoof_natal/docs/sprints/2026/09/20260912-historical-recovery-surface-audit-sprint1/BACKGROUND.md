# Historical Recovery Surface Audit — SBE Background

## Control Room source

This companion sprint supports [AstroWoof API Control Room issue #5: Audit and simplify historical recovery surfaces](https://github.com/kevin2357/astrowoof-api/issues/5).

Early QA recovery work accumulated native workspace, journal, authority, and retained-artifact compatibility bridges. The purpose is to distinguish durable native operator support and deliberate versioned migrations from logic that existed only to rescue one historical run shape.

## Objective

Build the native half of a cross-repo inventory. Preserve useful generic operator behavior and explicit supported migrations; identify candidates that can become clean, typed, fail-closed unsupported-history outcomes instead of permanent production rescue branches.

## Guardrails

- Audit and contract mapping only; no runtime implementation, release, provider work, workspace mutation, or retained-run action is authorized by this scaffold.
- Do not infer a removal merely from age. Record exact version/artifact applicability, current API callers, evidence authority, and test coverage.
- Keep operator capabilities generic and run-ID independent.
- Preserve historical proof in docs and fixtures rather than leaving bespoke production paths alive.

## API companion

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260912-historical-recovery-surface-audit-sprint95`
