# API review — Slice 1 and Voof-paws 2

## Decision

Slice 1 is approved. The protected access stayed within its exact allowance:
one `HEAD`, one `GET`, no list/write/delete/provider/native mutation, with all
listed object, archive, inventory, receipt, and checkpoint validations passing.

The recovered result is valid full-native-ledger evidence. The API must not
accept it as a seven-row subset or synthesize a providerless denial on SBE's
behalf. The API companion's containment patch remains the correct independent
response to its refusal: one typed terminal contract failure and local-capacity
release, without erasing provider custody.

## Exact API action-set confirmation

API performed one read-only PostgreSQL query against `sbe_paid_actions` for
Moxie's run. The complete API set is exactly:

```text
paid_a015169151774e145f831c33
paid_e720b871d1dd3ddc2e05d948
paid_0cd6b9243c939ccc09e37169
paid_3427805988bab60cfad8553d
paid_856d9da5b181ea9a11099bbf
paid_a40ffcb021c9f200d352fc2e
paid_5769a5e279df0fc506f65a91
```

The first six are `initial` / `reported`. The seventh is `creative_retry` /
`provider_created`, with the provider identity already frozen in the sprint.
Every one appears in generation 11's eight-row native ledger. The native-only
extra is therefore proven exactly:

```text
paid_95b6252fedb1610b3be397d9
```

Its retained native state is `PREPARED`, retry-3, providerless, and listed by
the sealed result as requiring providerless denial. This proves the initial
six-vs-seven premise was incomplete: the actual rejected join was eight native
actions versus seven API actions.

## Direction for Slice 2

Approved to proceed with causal reconstruction. Focus specifically on the
ordering and authority boundary between:

1. durable native preparation of `paid_95b6…`,
2. any lifecycle/external-authority publication that should have let API admit
   it, and
3. sealing the valid eight-row terminal-review result.

Do not turn the result's providerless-denial row into API mutation, do not
reconcile the retry-2 provider action, and do not infer a valid route from the
mere shared request SHA. If retained journal evidence cannot prove why API
never received admission for retry-3, state that limit and classify the seam
from the proven ordering only.

Voof-paws 2 is satisfied. Pause at Voof-paws 3 before choosing ownership or
proposing a correction.
