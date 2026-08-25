# Operator Retirement API Consumer Handoff

Status: Slice 4 candidate complete; API review required before release preparation.

## Supported boundary

SBE exposes:

- Python: `build_operator_retirement_request`,
  `assess_operator_retirement`, `execute_operator_retirement`, and strict
  request/assessment/result validators;
- CLI: `astrowoof-operator-retirement schema|build-request|dry-run|execute`;
- qualification: `astrowoof-operator-retirement-qa --require-installed`.

V1 supports only exact Natal. It accepts no provider credentials, request payload,
authorization/grant document, response ID, or provider transport. Bounded and other
routes refuse as `unsupported_contract`.

## API invocation order

1. Restore the complete SBE workspace at its stable logical absolute path.
2. Build the request through SBE's public reader/builder.
3. Run SBE dry-run and validate the returned assessment.
4. Atomically place the API job into API-owned
   `operator-retirement-pending` custody. Block ordinary worker continuation but do
   not release any API resource.
5. Execute the exact request through SBE.
6. Validate the returned operator result, explicit native result, journal range,
   snapshot, and publication receipt through SBE's public readers.
7. In one API transaction, persist that evidence and release only the matching API
   job/lease/capacity/unspent-authority resources.

The API must never hold a database transaction open across SBE execution. If API
finalization is interrupted, call SBE again with the exact request and consume
`exact_replay` of the original seal.

## Release eligibility

Only these outcomes can support API resource release:

- `applied`;
- `exact_replay`; or
- compatible `already_retired`.

For every one, validate:

- native run ID, exact route, and logical root;
- current and original request digests;
- pre/post revision and snapshot digests;
- `POLICY_STOPPED` together with `operator_retired`;
- complete action-ledger closure digest, including denial dispositions;
- native result and publication-receipt identities/digests; and
- all three continuation assertions are false.

Any refusal retains API resources and workspace custody. The API must not infer a
successful retirement from status, process exit, logs, or an empty active-action
list.

## Dry-run semantics

`retirement_quiescent` is native state truth, independent of request validity. A
stale request against an otherwise safe workspace returns
`retirement_quiescent: true`, `outcome: refused`, and `stale_observation`.

Dry-run and refusal publish no snapshot, journal, result, or receipt. The
`provider_io_performed_count` field describes this command's provider I/O and is
always zero; it does not summarize historical provider rows.

## Providerless actions

Every unresolved providerless action must first be disposed through the existing
supported providerless-denial operation. Retirement refuses with
`providerless_action_unresolved`; v1 intentionally has no combined
denial-and-retirement operation.

## Replay and repair

An exact request returns the original seal as `exact_replay`. A later request bound
to the identical pre-retirement native basis may return `already_retired`, with the
later and original request digests distinguished. Neither mutates native bytes.

SBE can narrowly repair interruption after its persisted retirement decision when
only the known run/public/spend files differ from the prior snapshot. Unexpected
workspace changes fail closed. Incomplete native result/receipt publication uses
the existing journal/snapshot-bound repair protocol.

## API-owned facts

SBE does not assert or release API jobs, leases, worker claims, capacity,
reservations, quotas, entitlements, billing state, or product publication state.
The companion API custody fence and final transaction remain API authority.

## Qualification

Run the installed console command:

```text
astrowoof-operator-retirement-qa --require-installed
```

The closed receipt covers public contract loading, eligible dry-run, native
mutation, sealed-reader validation, exact and compatible replay, stale/ambiguity/
unresolved/unsupported refusals, and zero provider I/O. It uses temporary sanitized
workspaces and cannot accept production input.
