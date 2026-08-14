# Slice 7 - Shared Lifecycle, Events, Snapshots, and Failure Recovery

## Result

Bounded-Natal authoring now runs through SBE's released operational authority
rather than a parallel lifecycle. The bounded sequencer owns route order and
bounded artifact semantics, while the existing common implementations remain
authoritative for run/public state, spend, single-writer authorization consumption,
provider identity, workspace integrity, lifecycle inspection, closeout, and event
delivery.

The default exact-Natal CLI and workflow are unchanged.

## Durable route

`astrowoof.bounded_natal.authoring_run.v1` records the distinct
`bounded_natal.v1` route inside the common v0.9 run state. Its authoritative
snapshot includes the private claim deck, provider-minimized packet, disposition
report, raw normalized provider results, validation reports, final cards, critic
result when enabled, delivery record, run/public state, and spend requests.

The runner supports initial authoring, separately classified creative retry,
polish, qualitative critic, qualitative candidate, final QA, and delivery. The
three optional stages are frozen booleans in the generation profile. Existing
spend-policy behavior independently determines whether an enabled optional stage
skips or exhausts at its ceiling.

Final delivery preserves route, input-contract identity and digest, claim deck,
provider packet, disposition, card digest, completed stages, and skipped stages.
Selected-card and whole-dog summary evidence remain distinct inside the underlying
claim and card contracts delivered by reference.

## Paid-action and restart behavior

Paid bounded stages use the existing `SpendController` and ledger. Authorization
therefore binds to the exact request digest, run/profile/state revision, route,
stage, model, service level, maximum output, conservative commitment, and price
book. Consumption uses the same cross-process lock and state-revision comparison.

The provider result is durably written before the action is settled and before
semantic mutations are accepted. If a worker stops after receiving a provider ID,
the next worker reconciles that exact provider operation and does not submit again.
If submission may have happened but no durable provider identity exists, the
existing ambiguous-submission state remains fail-closed. Polling a recorded
operation creates no new commitment.

This is the provider's real atomicity boundary: SBE cannot prove whether a request
without a returned durable ID reached the provider. It does not treat a
deterministic local key as provider idempotency evidence.

## Snapshot and lifecycle truth

Every normal provider-result, semantic mutation, skip, and delivery boundary ends
in the common complete workspace snapshot. Resume validates the exact inventory
before reading or executing work. Missing or changed members fail closed. The
released stable logical absolute-path contract remains in force; restoring at a
different logical path is rejected.

The common inspector recognizes delivery, outstanding actions, local dependencies,
budget exhaustion, ambiguity, and review outcomes from bounded state without route
special cases. Common closeout produces the normal API-consumable decision basis
and cryptographically identified result.

## Events and privacy

The packaged v1 event catalog adds bounded admission, family validation, selection,
disposition, and artifact-commit observations. Payloads contain counts, contract
identities, and hashes only. Provider prompts/responses and protected birth,
interval, coordinate, and location values remain prohibited. Event serialization
or sink failure drops observations and cannot alter native execution.

## Qualification

- Nine focused lifecycle tests cover complete provider-free delivery and closeout,
  separate creative retry, all nine new result/checkpoint failure points, snapshot
  mutation and wrong-path rejection, event sink failure, exact authorization
  consumption, providerless denial/replay, interrupted provider reconciliation
  without resubmission, and profile-driven optional spend skips.
- The failure matrix resumes monotonically from every authoring, retry/polish,
  critic/candidate, and delivery persistence boundary.
- A scripted paid-provider test records one submission and one reconciliation poll
  across worker interruption; no duplicate provider operation is created.
- Packaged event schema/catalog parity and closed-vocabulary tests pass.
- Complete repository suite: 263 tests passed in 169.368 seconds.
- A fresh offline wheel contains the bounded lifecycle module, both updated event
  contracts, and `py.typed`; SHA-256
  `f694f7558b483dec1d5f13d6970a3f6bba0cd3e3d2f56fd31b0fd7f61fb063b5`.
- `git diff --check` passed with only expected Windows line-ending notices.
- No real provider operation or network access was used.

Compact evidence is recorded in `slice7-bounded-lifecycle-summary.json`.

## Gate status

Gate 7 is ready for review. Deterministic scale, adversarial privacy/product QA,
and the full supplied-artifact matrix remain Slice 8 work.
