# Slice 3 — Authorization Round Trip and Failure Matrix

Date: 2026-08-18  
Disposition: complete; awaiting Kevin review

## Outcome

The API-shaped authorization path now has provider-free regression coverage from
the public joined authority-inputs document through SBE's existing create seam.
Both exact and bounded fixtures prove that a consumer can:

1. validate the joined prepared wave and binding bundle;
2. copy the six complete public bindings into six ordinary
   `astrowoof.provider_spend_authorization.v0.1` documents;
3. build the wave-level authorization envelope;
4. pass SBE's all-or-none preflight; and
5. reach six independently persisted simulated provider identities.

The two route integration tests now construct their authorization documents from
the public binding bundle rather than reading the private spend ledger. This is
the same authority boundary the API will use.

## Refusal matrix

Before invoking the create callback, SBE rejects:

- reordered, missing, duplicate, or unknown members;
- cross-run identity;
- changed profile, prepared revision, price book, model, or complete binding;
- a changed wrapper digest;
- bundle order or prepared-wave identity conflicts; and
- a binding whose request digest differs by one field.

Every refused case records zero simulated provider creates. Existing integration
coverage continues to prove all-or-none authorization consumption/native state
mutation around the same preflight boundary.

## Qualification

- Focused API-shaped and exact/bounded route integration tests: 5 passed.
- Initial-wave public/contract/bundle/round-trip suite: 36 passed after reconciling
  the consumer-manifest assertion to the API-approved status; 10 optional
  `jsonschema` skips in the base Windows runtime.
- Provider operations: 0.
- Spend: USD 0.

## Contract effect

No production contract, lifecycle state, orchestration, provider transport, or
editorial behavior changed in this slice. The work proves the public boundary
introduced in Slices 1–2 is sufficient and fails closed before provider work.
