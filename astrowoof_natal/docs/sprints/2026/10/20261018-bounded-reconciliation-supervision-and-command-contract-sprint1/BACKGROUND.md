# Bounded reconciliation supervision and command contract: background

**Status: not started.** This is the SBE side of the coordinated follow-up to API's bounded QA investigation; API's proposed plan and gates are linked below. SBE should develop its own plan and review the cross-repo contract before implementation.

## What happened

The full-day bounded QA run using released SBE 0.4.72 made it through deterministic processing and its v2 initial wave. Native SBE evidence recorded six provider operations; subsequent cycles selected provider reconciliation but the bounded CLI exited unsuccessfully. API's durable paid-action records were still authorized and their six reservations remained active at the time of investigation. API run `087b55ba-9ee1-42f1-a811-7e61806c4c92`; native run `41d24822311e5e6f85836d19b1d8dc80e7ddd7715aef46e8d6091fc495cb898d`.

The owner prefers a **fresh QA canary** after the fix, not recovery of that particular run. This is not authorization to release or erase its custody, cost exposure or evidence. Existing bound work and its routing need an explicit safe disposition before any deployment or retirement; compatibility for other runs remains a separate operational concern.

## Findings from API's local provider-free investigation

Against the exact retained/released 0.4.72 wheel SHA `298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364`:

- Real SBE bounded reconciliation on a synthetic checkpoint with fake provider retrieved and continued successfully. Its result was `astrowoof.provider_reconciliation_cycle_result.v0.2`, with `bounded_natal` / `astrowoof.bounded_natal.authoring_run.v2`.
- API's real command builder supplied exact-oriented frozen flags, `--events-stdout-jsonl`, and supervision flags not accepted by the 0.4.72 bounded executable. Its stream reader expected a wrapped `sbe.command_result.v1`, while the bounded command writes a plain JSON result. API's lifecycle v0.5 validator expected bounded route v1 and refused the v2 result.
- Bounded interactive reconciliation explicitly rejects a suspension observer. In provider-free exact-route tests, observation before GET, coordinator propagation, and suspension after a response checkpoint passed. The bounded explicit-refusal regression also passed.
- The fake-provider result was not successfully ingested and checkpointed by the actual API path: it was refused at the contract boundary. API's existing mock-based tests passed but did not qualify the real installed CLI join. The earlier economics `sealed_publication_join_mismatch` needs independent investigation.

## Requested joint design and implementation direction

The owner chose coordinated repair, not an unsupervised workaround. Please work with API to freeze a bounded reconciliation CLI/transport contract and safe cooperative supervision, including pre-GET and post-durable-response safe points, force-fence races, child exit, crash/restart, replay, terminal publication, no duplicate provider work, route/profile integrity, and privacy. Preserve exact-route behavior. Decide the command envelope and argument contract jointly rather than relying on informal wrapping or changing a native v2 identity to v1.

Provide fake-provider evidence and a reproducible SHA-pinned candidate for the installed-wheel joint gate. The API side must exercise its real command, ingestion, custody/economics and checkpoint boundaries against those exact bytes; wheel changes require a fresh joint qualification. Final release, QA deployment, and a fresh paid canary are separate owner/process gates. No provider work is authorized by this document.

## Contract ownership and profile direction

SBE will first propose the native executable, result transport and supervision
contract, including exactly what it can and cannot promise for a fence arriving
during a provider GET. API will review that proposal against its lease authority,
direct-child exit, checkpoint publication, custody/accounting, command builder
and result-ingestion boundaries, and specify the API-side handoff. The proposal
is not frozen or approved until both sides review it and resolve material
tradeoffs; implementation and exact-wheel joint qualification follow that gate.

Plan for a new immutable bounded processing profile bound to the successor SBE
release and the appropriate prompt/catalog identities; do not rewrite the
historical `0.4.72` bundle or substitute newer code for work pinned to an older
worker context. Whether this rollout also needs successor exact profiles is a
separate compatibility and operational decision, not an assumption. The new
profile and any rollout require their own evidence and authorization.

## References

- [API sprint background](C:/dev/github/astrowoof-api/docs/sprints/2026/10/20261018-bounded-reconciliation-contract-and-supervision-sprint129/BACKGROUND.md)
- [API sprint plan and cross-repo gates](C:/dev/github/astrowoof-api/docs/sprints/2026/10/20261018-bounded-reconciliation-contract-and-supervision-sprint129/PLAN.md)
- [Previous bounded SBE sprint](../20261005-bounded-birth-time-modern-authoring-integration-sprint4/PLAN.md)
- [Initial-wave v2 sprint](../20261008-bounded-initial-wave-v2-execution-sprint1/PLAN.md)
