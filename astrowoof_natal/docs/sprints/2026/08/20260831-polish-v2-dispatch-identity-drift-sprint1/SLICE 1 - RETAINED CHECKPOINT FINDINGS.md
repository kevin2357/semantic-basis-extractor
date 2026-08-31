# Slice 1 — retained checkpoint findings

## Result

Generation 11 establishes a native singleton-intent lifecycle defect. The API's
polish request/grant is coherent and the native polish action is dispatchable in
isolation, but SBE still retains the prior creative-retry dispatch intent after
that retry has completed and been reported.

The mismatch is exact:

| Native fact | Retained value |
|---|---|
| State revision/status | `75` / `AWAITING_SPEND_AUTHORIZATION` |
| New polish action | `paid_c90cf4073c936d22e27e16ae` |
| Polish action posture | `PREPARED`; provider null; consumption absent; authorization null |
| API polish request/grant | `07300bd27a5…` / `bb3aea3813f…` |
| Persisted native intent action | `paid_70700383adb1746594e1204b` |
| Persisted native intent request/grant | `e35ca84d8afa…` / `e09fbc669829…` |
| Persisted intent state | `PROVIDER_PENDING` |
| Creative-retry ledger state | `REPORTED` |
| Creative-retry provider identity | durable `resp_014d…` |

The intent's complete ordered inventory contains only `paid_707…`; it has no
claim over `paid_c90…`. The intent nevertheless occupies the one
`external_authority_v2_dispatch_intent` slot.

## Why the observed refusal pair occurs

`commit_external_authority_v2_dispatch_intent()` first validates the selected
polish action, current inspection, v2 request, grant, and authorization document.
It then checks the singleton intent field. Any existing intent with a different
request/grant produces `action_state_or_custody_mismatch`.

The CLI defers that reason because it may represent a replay/recovery case where
the requested intent was already committed. It calls dispatch using the supplied
polish identities. `dispatch_external_authority_v2_intent()` loads the retained
creative-retry intent, finds that its request/grant is different, and produces
`authorization_mismatch`.

This exactly matches the trace. No provider I/O is possible on this path.

## Lifecycle gap in current source

Current source creates one `external_authority_v2_dispatch_intent` and removes it
only in the pre-provider-refusal path. Normal provider identity durability,
reconciliation completion, usage reporting, and later deterministic fan-in do
not retire or archive the completed intent. The first ordinary v2 dispatch can
therefore succeed, while the next independent ordinary v2 action is permanently
blocked by the predecessor's stale intent.

This is a general sequential-v2-action defect, not polish-specific request drift.
Creative retry followed by polish merely exposed it first.

## Local-work append-only failure

The revision-75 trace failure remains genuine:

`Local-work consumption history is not append-only`

The retained state contains one consumed local-work key, `work_33606e…`, but the
checkpoint does not preserve the transient prior lifecycle document passed to
the failed validator. Generation 11 alone therefore cannot identify which
earlier cumulative key was absent from the successor.

That failure may explain why the ordinary-resume command exited noisily, but it
is **not required** to explain the v2 refusal: the stale creative-retry intent is
independently present, and current source mechanically rejects the new polish
intent because of it. Generation 10 is not requested at this gate.

## Integrity and access evidence

- Exact `HEAD` and `GET` matched all frozen object coordinates.
- Strict API checkpoint restoration validated generation 11, all 964 archive
  members, inventory digest, contract, compatibility identity, and predecessor
  link.
- The inner native snapshot contains 934 exact members with no missing, extra,
  or changed member.
- Remote operations: one `HEAD`, one `GET`, zero list/write/delete.
- Native/provider operations: zero.

## Proposed next classification

The retained evidence supports **SBE runtime lifecycle defect** as the leading
classification: a completed predecessor v2 dispatch intent is not retired before
the next independently authorized ordinary action.

Slice 2 should freeze the retirement/archive invariant and distinguish safe
predecessor completion from provider-pending or ambiguous intent custody. Slice
3 should then reproduce two sequential ordinary v2 actions provider-free through
the real public boundaries before any runtime mutation is proposed.
