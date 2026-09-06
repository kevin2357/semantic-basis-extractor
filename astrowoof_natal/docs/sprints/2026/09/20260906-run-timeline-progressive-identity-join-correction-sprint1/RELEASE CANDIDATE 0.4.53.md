# Release candidate — SBE 0.4.53

## Scope

Diagnostic-only correction to the run-cohort timeline's progressive wrapper
identity join. No authoring runtime or API consumer contract changes.

## Gate

- Focused regression: 52 passed, four expected optional-dependency skips.
- Broad/full suite: deliberately not run; affected callers are enumerable.
- First committed-source wheel: reproducible at SHA-256
  `78db0fae4f7858b831a0c036cb3bf693a9f9bd38cceafb2b0a729cedc22a5f04`.
- Installed package/resources/CLI/provider-free QA: pass.
- Real three-run Better Stack export: 138 wrapper events accepted, zero
  refused; production cycle and lease spans pair correctly.
- Provider/R2/retained-workspace activity: zero.

## Status

Release-lock provenance rebuild pending. No tag or publication is authorized by
this candidate record alone.

