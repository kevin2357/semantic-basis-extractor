# API to SBE: 0.4.71 bounded initial-wave v2 execution gap

## Status

**New cross-repository corrective handoff.** The first provider-backed QA
bounded run reached SBE's durable spend-authorization boundary without
provider custody, then stopped fail-closed. This is neither a provider outage
nor an API spend-policy rejection. It exposes an incomplete bridge between the
established v1 initial-wave authority and the new bounded v2 lifecycle.

No provider operation was created, submitted, or reconciled. The affected QA
run is terminally failed and must not be resumed or manually reconciled as a
way to test a corrective implementation.

## Observed QA evidence

API run: `bf50cad2-aa78-4543-9e82-dd7c7e654dec`  
Native run: `2aece7cba784409c9d9c1aec11b7abf1465cc50af58a192310af5afd276856a5`  
SBE release: `0.4.71`

The SBE worker's structured BetterStack trace establishes:

1. The bounded deterministic stage completed and SBE created a valid bounded
   native run with `pass_count=6` and `claim_count=50`.
2. SBE prepared six `authoring_initial` actions, moved to
   `AWAITING_SPEND_AUTHORIZATION`, and selected an external-authority request:
   `request_kind=initial_wave_admission`, `action_count=6`.
3. At that point, the trace reports `provider_actions=0`,
   `provider_custody_count=0`, `prepared_count=6`, and no ambiguous custody.
   Therefore no external provider I/O occurred.
4. The worker then failed with `SbeProviderContractError`: `SBE v2 external
   authority request kind is unsupported`.

Authoritative QA PostgreSQL confirms that an API-owned **v1** initial-wave
authority record already exists for this exact authoring/native run, with a
sealed v1 request and v1 grant, both `request_kind=initial_wave_admission`.
All six corresponding paid actions are `authorized`. There is no
`sbe_external_authority_v2_awaiting_grants` row for the run.

Thus, the failure is after the original v1 authorization was persisted but
before any provider submission. It must never result in duplicate paid-action
reservations or a second initial-wave grant.

## Contract mismatch

The released bounded runtime correctly emits a v2 temporal-lifecycle request
for the current state:

```text
schema_version = astrowoof.external_authority_request.v2
request_kind   = initial_wave_admission
action_count   = 6
```

However, the current SBE v2 grant/execution contract is deliberately closed to
`ordinary_action_set`:

- `build_external_authority_grant_v2()` and
  `validate_external_authority_grant_v2()` reject any non-ordinary request.
- The v2 dispatch-result contract likewise models only ordinary lexical action
  ordering.
- The legacy initial-wave executor validates v1 authority documents and
  explicitly refuses bounded constrained execution as deferred.

API's current v2 awaiting-grant/admission route also only accepts
`ordinary_action_set`, so it fails safely at the first incompatible boundary.
Changing that API allowlist alone would be incorrect: it would issue or route
an authorization that SBE's released v2 executor cannot validate or consume.

## Required SBE successor capability

Create a new immutable SBE release/profile context that supports a
**bounded-capable v2 initial-wave execution path**. It must:

1. Accept `initial_wave_admission` under the v2 external-authority request and
   grant contract, including the six-member initial-wave identity and semantic
   member order (not ordinary lexical-only semantics).
2. Preserve the sealed API spend-policy and exact native/checkpoint/profile
   bindings already established by the bounded lifecycle.
3. Produce and consume a compatible v2 grant plus six authorization documents
   without re-creating the initial wave, adding a second reservation, or
   losing the first v1 authority lineage.
4. Make a resumed pre-provider bounded workspace either consume the one
   compatible existing initial authority exactly once, or refuse with a typed
   no-provider outcome. It must never reinterpret an existing v1 grant as an
   arbitrary fresh v2 authorization.
5. Retain zero-provider-I/O behavior for malformed/missing/mismatched grants,
   wrong route/profile/checkpoint identities, and replay changes.
6. Continue to support all later ordinary v2 successor-authority cycles
   without broadening their ordering or identity contract.

The exact migration/interoperability representation—e.g., a sealed v1-to-v2
bridge record versus a new initial-wave-specific v2 grant—should be designed
explicitly. API should not infer that representation from workspace files or
logs.

## Required provider-free qualification

Before a new candidate is offered to API:

1. Start a real eligible four-context bounded run with the API-provided spend
   policy; it must prepare exactly six initial actions and stop before provider
   I/O until authority is supplied.
2. Exercise first authorization and the post-command/resume path that exposed
   this defect. Prove one compatible initial-wave authorization is consumed
   exactly once, with six actions and no duplicate reservation.
3. Prove any wrong/missing/stale/mixed-schema grant refuses before provider
   I/O and without mutating the sealed initial authority.
4. Prove ordinary v2 successor-authority behavior remains unchanged.
5. Provide API with the new wheel identity, profile/prompt/catalog identities,
   exact request/grant/authorization fixtures, and an explicit compatibility
   statement for an already-authorized v1 initial-wave workspace.

## API follow-up once SBE contract is frozen

API will add the corresponding narrowly typed admission and dispatch path,
preserving the existing v1 initial-wave authority instead of authorizing a new
six-action set. We will then run a joined installed-wheel provider-free test
against the exact candidate before rebuilding the bounded SBE worker or
launching another paid QA run.
