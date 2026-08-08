# Provider Spend Enforcement

## Scope

Semantic Closure v0.8 enforces a frozen per-run USD ceiling before every new
paid OpenAI submission. This is distinct from SBE's deterministic fifty-claim
semantic portfolio budget.

SBE owns per-run paid-action identity, authorization consumption, commitment
accounting, provider-operation lineage, reported usage estimates, and
machine-readable pause/failure states. AstroWoof API owns transactional
reservations across runs, owner and account quotas, circuit breakers, product
entitlements, publication policy, and authoritative billing reconciliation.

No dollar allocation is a runtime default. Every new OpenAI run must supply an
explicit generation-profile `spend_policy` pinned to a versioned price book.
Legacy OpenAI runs without a v0.8 ledger fail closed.

## Paid stages

The ledger classifies `authoring_initial`, `creative_retry`, `polish`,
`qualitative_critic`, and `qualitative_candidate` independently. The policy
must ceiling every stage and define `skip` or `exhaust` behavior for each
optional stage. Polling existing work, extraction, acceptance, assembly,
validation, lint, and delivery create no new paid commitment.

## Prepare, authorize, execute

Before submission SBE creates a `PREPARED` action in `run.json` and
`spend-authorization-requests.json`. Its binding includes run ID, frozen
profile digest, prepared state revision, stage, route, request digest, model,
service level, maximum output, micro-USD commitment, and price-book version.

An `astrowoof.provider_spend_authorization.v0.1` document must repeat that
binding exactly and add an external `authorization_reference`. Authorization
is consumed once under an inter-process lock and state-revision compare.

Commitments charge uncached input and authorized maximum output; cache savings
are never assumed. Active or ambiguous work retains its commitment. Reported
usage settles the local estimate. API billing records remain external authority
and may be correlated through append-only reconciliation references.

## Machine states

- `AWAITING_SPEND_AUTHORIZATION`: a prepared action needs authority.
- `BUDGET_EXHAUSTED`: required work cannot fit the frozen ceiling.
- `AMBIGUOUS_PROVIDER_SUBMISSION`: SBE cannot prove whether creation occurred.
- `SKIPPED_BUDGET_EXHAUSTED`: the generation profile skipped an optional stage.

Polling a known provider ID consumes no new authorization.

## Provider atomicity and idempotency boundary

The OpenAI API reference documents creating and retrieving Responses and
Batches by returned IDs. It does not currently document a transaction joining
provider creation to local state, an exactly-once or retention guarantee for
`Idempotency-Key`, or idempotent Batch creation.

SBE still sends deterministic Response idempotency keys as useful request
identity, but does not treat them as proof that resubmission is safe. Failure
after `SUBMITTING` and before durable provider-ID persistence produces
`AMBIGUOUS_PROVIDER_SUBMISSION` and no automatic retry. Batch creation uses the
same conservative boundary. This provider/local-state atomicity gap is
irreducible without a documented provider creation contract.

## Reconciliation

Reported usage and SBE price-book estimates are operational evidence, not
authoritative billing. The API may append immutable references to account
billing or reservation records. SBE retains provider IDs, request digests,
commitments, usage, estimates, and reconciliation reference IDs for audit.

