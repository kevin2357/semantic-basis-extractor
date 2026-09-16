# Slice 4B — Joined intake blocker

## Exact pair under test

- API source revision: `f5da771`
- SBE source/release-lock revision: `7e4fa13f`
- SBE version: `0.4.66`
- SBE wheel SHA-256:
  `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf`
- SBE fixture bundle schema:
  `astrowoof.native_suspension_fixture_bundle.v1`
- Child command schema:
  `astrowoof.native_suspension_command_result.v1`

## Finding

The API implementation now owns the correct first-route chronology:

1. durably prepare a capability before launch;
2. write its request-isolated envelope;
3. launch the external-authority-v2 child with the exact paths;
4. admit an operator force fence against the running lease;
5. rejoin that fence to the persisted capability and atomically write the
   exact suspension request; and
6. stop ordinary heartbeat activity while awaiting child exit.

The parent does not yet own the corresponding child-result discrimination.
`HeartbeatingProcessSbeProviderRuntime.external_authority_v2()` unconditionally
calls `validate_provider_dispatch_command_result()` after reading the output.
That reader accepts only the released external-authority-v2 dispatch command
families. It correctly rejects SBE's distinct suspension command result, but
the parent has no alternate closed reader through which to accept it.

An exact installed-package probe produced:

```text
sbe 0.4.66
schema astrowoof.native_suspension_command_result.v1
sbe fixture valid astrowoof.native_suspension_fixture_bundle.v1
SbeProviderContractError: SBE provider dispatch result is invalid
```

## Required API correction before joined qualification

The real parent must discriminate on the closed top-level schema and:

- preserve the existing provider-dispatch reader unchanged for its v2-v4
  command families;
- use SBE's packaged public suspension reader/validator for exactly
  `astrowoof.native_suspension_command_result.v1`;
- retain the exact result, receipt, request, capability, and force-fence joins;
- treat child exit plus validated suspension evidence as inputs to a later
  API-owned execution-capacity disposition, never as allocation/provider/
  spend/workspace custody release; and
- fail closed for absent, malformed, unknown-version, stale, mismatched, or
  contradictory evidence.

The callback which publishes the request also remains a caller-owned join. The
joined qualification must use the real durable re-read/builder/writer path,
not a callback that merely writes canned fixture bytes.

## Decision

Slice 4B remains open at a review paws-point. No SBE code or candidate rebuild
is indicated by this finding. Unsupported reconciliation and initial-wave
routes remain deferred exactly as already scoped.
