# Evidence

## Inputs

| Evidence | SHA-256 / identity |
| --- | --- |
| Bounded Render export | `81de1ad4319b6157a8778053f46850b442feef24584fe084a384b94fe5a4db27` |
| Qualified SBE 0.4.59 wheel | `9211b7a7fd2e1a10a42cfe6bf47cafd749fa2076767b2dd7500621a93d9cbe92` |
| SBE 0.4.59 tag target | `e5127caea466b12340472eee48b2563abfd68650` |
| API source inspected | `d2c95191db186b360449ce02636113eddfe9c068` |
| API reconciliation source SHA-256 | `3b8ad499e152b3e884a4ecc24c91d4a3bf7e8d512effdda84c09762df56dfbd8` |
| API parser-introduction commit | `c1b4c3a05ea6e5d128650a98ed4a3d18b493320b` |

## Trace conclusions

- Three of three runs share the same successful initial-wave shape.
- Three of three restore coherent six-action provider custody.
- Three of three select due provider reconciliation and reduce the due subset.
- Three of three publish `provider_pending` before API rejection.
- Three of three fail with the same outer-envelope error.
- No trace indicates a provider-create replay or initial authority failure.

## Reproduction receipt

```text
installed_version 0.4.59
exit 3
provider_methods ['GET']
1 sbe.execution_event.v1 execution_event provider.reconciliation_observed
2 sbe.execution_event.v1 execution_event run.detached
3 sbe.execution_event.v1 execution_event checkpoint.committed
4 sbe.execution_event.v1 execution_event native.result_published
5 sbe.command_result.v1 command_result astrowoof.provider_reconciliation_cycle_result.v0.2
mixed_stream SbeProviderContractError SBE reconciliation envelope is unsupported
command_only accepted astrowoof.provider_reconciliation_cycle_result.v0.2 detached_provider_pending
```

Existing strict negative/terminal parser coverage was retained and rerun:

```text
5 passed, 37 deselected in 0.74s
```

## Evidence limits

- Render logs are diagnostic rather than lifecycle authority.
- The exact rejected pipe bytes were not persisted as a standalone artifact;
  the public-command reproduction establishes the deterministic equivalent.
- Generation-2 archives predate the failed reconciliation and cannot prove its
  stdout ordering.
- The current API checkout may contain work beyond the deployed incident
  revision; causal attribution is specifically to the blamed `c1b4c3a`
  reconciliation changes and the reproduced production parser behavior.
