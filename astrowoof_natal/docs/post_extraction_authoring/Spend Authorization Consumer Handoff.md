# Spend Authorization Consumer Handoff

## Consumer workflow

Create a generation-specific policy. These zero values illustrate shape, not
accepted allocations or defaults:

```json
{
  "currency": "USD",
  "price_book_version": "openai-public-2026-08-07.v1",
  "run_ceiling_micro_usd": 0,
  "stage_ceilings_micro_usd": {
    "authoring_initial": 0,
    "creative_retry": 0,
    "polish": 0,
    "qualitative_critic": 0,
    "qualitative_candidate": 0
  },
  "optional_stage_budget_behavior": {
    "polish": "skip",
    "qualitative_critic": "skip",
    "qualitative_candidate": "skip"
  }
}
```

Start a new OpenAI run with `--spend-policy <policy.json>`. SBE performs free
deterministic work, prepares exact paid actions, persists them, and exposes
`AWAITING_SPEND_AUTHORIZATION` without submitting them.

The API reads `spend-authorization-requests.json`, transactionally reserves
cross-run/account budget, and returns one exact envelope per approved action:

```json
{
  "schema_version": "astrowoof.provider_spend_authorization.v0.1",
  "action_id": "paid_...",
  "binding": { "...": "copy the prepared binding exactly" },
  "authorization_reference": "api-owned-reservation-id"
}
```

Resume with one or more `--spend-authorization <authorization.json>` options.
SBE validates and consumes them, executes only matching requests, and then
completes local work, polls existing work, or prepares the next action. Polling
a known provider ID needs no new reservation.

Treat an authorization pause as checkpoint-ready only after the SBE invocation
has exited and its coordinator-written `workspace-snapshot.json` validates
against the complete directory. Internal ledger persistence may precede that
checkpoint while provider or QA work is still settling; it is durable spend
evidence, not permission to snapshot worker scratch mid-invocation. The API
must copy the complete quiescent run directory under its exclusive lease.

## API responsibilities

The API must serialize run mutation under its lease, reserve transactionally,
bind reservations to the complete action binding, define generation-profile
ceilings and optional behavior, enforce cross-run/user/account policy, and
reconcile authoritative billing separately. It must not edit `run.json`, reuse
authorization across actions, or infer publishability from a spend state.

Ambiguous submissions require operator/provider reconciliation. More budget is
not evidence that resubmission is safe.

## Promotion gate

A pinnable consumer must test exact prepare/authorize/execute round trips,
worker replacement while polling, required-stage exhaustion, profile-driven
optional skipping, ambiguous creation, stale authorization/state revision,
single-writer consumption, and API reservation/billing-reference correlation.
