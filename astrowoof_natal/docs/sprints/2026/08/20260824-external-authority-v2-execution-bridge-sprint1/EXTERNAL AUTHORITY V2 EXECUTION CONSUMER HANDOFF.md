# External Authority v2 Execution Consumer Handoff

Status: source and provider-free qualification complete; installed-wheel and final
release review pending.

## Supported boundary

Temporal lifecycle v0.6 may expose a stable
`astrowoof.external_authority_request.v2` with
`request_kind: ordinary_action_set`. API admits that exact request through one
closed `astrowoof.external_authority_grant.v2` plus the complete ordered ordinary
authorization documents.

The supported provider-capable command is:

```text
astrowoof-external-authority-v2 \
  --run-dir <stable-restored-workspace> \
  --inspection <validated-v0.6-inspection.json> \
  --request <external-authority-request.v2.json> \
  --grant <external-authority-grant.v2.json> \
  --authorization <ordinary-authorization-1.json> [...] \
  --provider openai \
  --api-key-env OPENAI_API_KEY \
  --output <outside-workspace-result.json>
```

SBE validates the complete workspace, current checkpoint basis, request, grant,
documents, action bindings, inventory, route, mechanism, and provider safety under
its native writer. It publishes a complete intent checkpoint, releases the writer,
then creates from the exact snapshot-bound prepared payload. Provider identities
are checkpointed one at a time before the next member may dispatch.

The command does not poll, retrieve, ingest, or interpret provider results. A
successful create detaches into provider-pending; API later invokes only the
supported SBE-selected reconciliation cycle when the lifecycle says it is due.

## Deliberate Batch deferral — important

> **Ordinary external-authority v2 Batch dispatch is deliberately deferred in this
> release. It is not an adapter-discovery hint and must not be attempted.**

The v2 executor supports only ordinary interactive Response actions for exact and
bounded Natal. A v2 ordinary Batch action returns/refuses with
`unsupported_contract` before authorization consumption, intent publication, or
provider I/O.

This does not remove or alter existing Batch support:

- exact initial-wave Batch continues through the existing exact Batch mechanism;
- bounded initial-wave Batch continues through the existing bounded Batch
  mechanism; and
- provider-bound Batch work remains reconciliation-only through its existing
  adapter.

API must select this v2 command only for a validated request whose complete native
inventory is an applicable ordinary interactive Response set. It must never route
a Batch ordinary action through this executor or convert it to Response transport.

## Passive no-grant behavior

Omit `--grant`, all `--authorization` arguments, and provider selection to obtain
the closed passive `awaiting_compatible_grant` result. This mode:

- returns exit code 3;
- performs no native mutation, checkpoint publication, provider I/O, or authority
  consumption; and
- does not assert API lease, capacity, reservation, admission, or consumer
  authority facts.

Output paths inside the native workspace are refused.

## Result contracts

- `astrowoof.external_authority_dispatch_result.v2`: passive no-grant result;
- `astrowoof.external_authority_intent_result.v2`: newly committed native intent;
- `astrowoof.external_authority_provider_dispatch_result.v2`: provider create and
  replay outcome; and
- `astrowoof.external_authority_v2_command_result.v1`: closed command envelope
  joining intent and dispatch evidence.

Dispatch outcomes map as follows:

| Outcome | API interpretation |
|---|---|
| `detached_provider_pending` | Release execution capacity; retain relevant authority/custody and await SBE reconciliation timing |
| `ambiguous_submission` | Stable blocked/review; never create again |
| `exact_replay` | Idempotent no-op; no provider I/O |

On an exact replay, `intent_result` is null because the prior native intent remains
the authority; `dispatch_result` binds the same request, grant, inventory, current
revision, and snapshot.

## Ownership and invocation sequence

API must atomically persist its admission/reservation decision before invocation,
but must not hold a database transaction across SBE/provider execution. SBE never
claims API-global reservation, capacity, lease, entitlement, quota, billing, or
publication facts.

Recommended sequence:

1. restore and validate the complete native workspace at its stable logical root;
2. read and persist the strict v0.6 inspection and v2 request;
3. atomically admit or decline the complete ordered API authority set;
4. persist the grant and complete authorization documents outside the workspace;
5. invoke the constrained v2 command once;
6. ingest and validate the closed command result;
7. release worker capacity only according to the native dispatch/lifecycle result;
8. retain provider/API authority while provider custody remains; and
9. invoke the SBE reconciliation cycle only when a later lifecycle decision selects
   it.

API must not reconstruct action subsets, payload locations, provider commands, or
native meaning from `run.json`, logs, request IDs, or subprocess exit code.

## Atomicity and recovery

- No valid snapshot can expose a partial aggregate grant/intent unit.
- `CALL_ENTERED` without a durable provider ID is ambiguous, even if the provider
  might not actually have received the request.
- A returned identity is durable before the next selected member can enter create.
- A complete identity inventory replays with zero creates.
- Provider/local deterministic keys are correlation aids, not proof of provider
  idempotency.
- Snapshot-invalid interruption is blocked/operator-review evidence, not permission
  to retry or infer terminal state.

## Qualification command

Run the installed, provider-free qualification with:

```text
astrowoof-external-authority-v2-qa --output <receipt-outside-workspace.json>
```

It accepts no API key, provider endpoint, production input, or retained workspace.
Its closed receipt exercises exact and bounded six-create initial waves, real 4+2
reconciliation, all four ordinary interactive Response stages, durable v2
dispatch/reconciliation selection, and explicit ordinary-Batch refusal. Scripted
create/retrieval counts are reported separately from zero real provider/network
activity and zero spend.

## Compatibility

- Initial-wave v1 authority remains unchanged and is not inferred from v2.
- Temporal lifecycle v0.6 remains the required source for v2 request identity.
- Older lifecycle/request versions fail closed at this execution boundary.
- Retained provider work must not be resumed merely because this command becomes
  available; normal API custody and explicit operational authorization still apply.

