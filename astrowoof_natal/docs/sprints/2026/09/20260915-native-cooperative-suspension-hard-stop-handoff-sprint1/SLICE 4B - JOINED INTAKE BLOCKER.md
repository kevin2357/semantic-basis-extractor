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

## First API correction

API revision `e2e9d32` now discriminates on the closed top-level schema and:

- preserves the existing provider-dispatch reader unchanged for its v2-v4
  command families;
- uses SBE's packaged public suspension reader/validator for exactly
  `astrowoof.native_suspension_command_result.v1`;
- retains the exact result, receipt, request, capability, and force-fence joins.

The later API disposition must still:

- treat child exit plus validated suspension evidence as inputs to a later
  API-owned execution-capacity disposition, never as allocation/provider/
  spend/workspace custody release; and
- fail closed for absent, malformed, unknown-version, stale, mismatched, or
  contradictory evidence.

The callback which publishes the request also remains a caller-owned join. The
joined qualification must use the real durable re-read/builder/writer path,
not a callback that merely writes canned fixture bytes.

## Second joined finding at `e2e9d32`

The executable joined harness used API's real capability, fence, request
builder/writer, subprocess parent, new suspension reader, and the exact locked
SBE CLI. It reached SBE's first post-intent safe point without provider I/O,
then refused the API-built request:

```text
ValueError: Suspension request does not join supervision invocation
```

The differing field is `grace_deadline`. The approved contract deliberately
has two bounds:

- `grace_deadline` repeats the immutable pre-launch envelope deadline; and
- `expires_at` is the tighter effective request deadline, including an earlier
  operator-fence deadline.

API's builder currently assigns the minimum effective expiry to both fields.
Its own unit tests check internal construction but do not pass the resulting
request through SBE's public request validator, so they did not expose the
cross-package mismatch.

The narrow correction is to retain the envelope's canonical
`grace_deadline` in the repeated field while continuing to set `expires_at` to
the minimum of envelope grace and force-fence grace. The ordering predicate
`requested_at < expires_at <= grace_deadline` then remains intact.

## Decision

Slice 4B remains open at a second API correction paws-point. No SBE code or candidate rebuild
is indicated by this finding. Unsupported reconciliation and initial-wave
routes remain deferred exactly as already scoped.
