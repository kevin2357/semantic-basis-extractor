# Temporal Lifecycle API Consumer Handoff

Date: 2026-08-23
Status: implementation and installed-wheel qualification complete; API and owner approved 0.4.16 release

## Supported read boundary

Python:

```python
from astrowoof_natal_authoring import inspect_temporal_lifecycle

inspection = inspect_temporal_lifecycle(
    run_dir,
    observed_at=api_trusted_utc,
    native_exclusive_access="declared",
)
```

CLI:

```text
astrowoof-authoring-lifecycle --run-dir RUN inspect-temporal \
  --native-exclusive-access declared \
  --observed-at 2026-08-23T12:34:56Z
```

The timestamp is required and canonicalized to whole-second UTC. The operation
is provider-free and read-only. Existing `inspect` continues to return lifecycle
v0.5; consumers must not reinterpret it as v0.6.

## API persistence rule

Persist the checkpoint basis once by `checkpoint_basis_sha256`. Persist temporal
decisions that drive a durable route/command decision or explain a refusal or
deferral, under an explicit API retention policy. Choose the current decision by
API-owned monotonic time.

- Same basis and time: exact replay.
- Same basis and later not-due to due: append/advance.
- Changed basis: ingest a new native checkpoint, never update the old basis.
- Clock regression, due regression, digest/binding/identity change: refuse.

`capacity_disposition` is native/local scheduling evidence only. API admission,
leases, slots, reservations, circuit breakers, entitlements, and spend authority
remain API-owned. Repeated due evidence does not authorize duplicate invocation;
leases/custody do that.

The API invokes the supported run-level reconciliation command. It never selects
or reconstructs the due member subset.

## External authority

`astrowoof.external_authority_request.v2` is a stable identity/reference joined
to one validated v0.6 inspection. It binds run ID, checkpoint-basis digest,
request kind, exact ordered action IDs, and—through the strict basis—every
member's complete public binding.

Always call
`validate_external_authority_request_v2_against_inspection()` before persisting
or using that reference. The request alone is insufficient to reconstruct or
authorize an action.

Important compatibility boundary: this sprint qualifies v2 request identity and
joining, but does not silently reinterpret existing constrained v1 grants as v2.
Until the API/SBE constrained-execution seam explicitly adopts v2, existing
external-authority execution continues using its supported v1 artifacts. API
review must decide whether v2 execution adoption belongs in this release pair or
a separately pinned follow-up; no mixed-version inference is allowed.

## Provider facts

Inspection never polls the provider. Provider completion, output, usage, or
failure becomes native fact only after the supported reconciliation operation
retrieves and checkpoints it. That operation produces a new basis digest.

## Route compatibility

- Exact interactive: supported.
- Exact Batch initial/retry: supported.
- Bounded v2 interactive: supported.
- Bounded v2 Batch initial/retry: supported.
- Enabled optional stages: supported through interactive Response transport.
- Optional actions claiming Batch transport: fail closed.
- Legacy bounded v1 Batch and unknown routes: fail closed.

## Release-pair gate

Before paid QA:

1. install the exact fresh SBE wheel;
2. validate both packaged schema identities;
3. run `astrowoof-provider-pending-qa` provider-free;
4. verify six unique creates, six unique 4+2 retrievals, and distinct pre/post
   basis hashes;
5. have API ingest an explicit v0.6 fixture and reject v0.5 at this boundary;
6. prove API trusted-time monotonic persistence and lease-guarded due invocation;
7. freeze the v2 external-authority execution compatibility decision; and
8. only then authorize retained-run read-only inspection or fresh paid QA.

No retained provider operation may be retrieved, recreated, cancelled, or
mutated as part of contract adoption without separate owner authorization.
