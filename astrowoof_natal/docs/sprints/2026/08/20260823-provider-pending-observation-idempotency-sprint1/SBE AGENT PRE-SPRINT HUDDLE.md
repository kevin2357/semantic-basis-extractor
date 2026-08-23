# SBE Agent Pre-Sprint Huddle

Date: 2026-08-23
Status: review input; no implementation begun

## Finding

The incident is a real contract mismatch, but the native evidence is not itself
contradictory.

SBE lifecycle inspection v0.5 is read-only and provider-free. Its observation
contains both immutable snapshot identity and caller-supplied `observed_at`.
Capacity and branch projection compare that time with durable
`resume_not_before`. Consequently one unchanged valid snapshot can first say
`provider_reconciliation_not_due` and later say
`provider_reconciliation_due`.

The API currently enforces one full byte-identical inspection JSON per snapshot
SHA-256. It therefore rejects the valid later scheduling decision as changed
replay.

## Required conceptual correction

The evolving fact is time-relative scheduling eligibility, not unseen provider
state. Inspection does not poll OpenAI. A provider result, terminal status,
usage value, or failure becomes native evidence only after the supported
reconciliation boundary observes and checkpoints it.

## Recommended contract

Publish a strict versioned split between:

- immutable `checkpoint_basis`, canonically hashed; and
- `temporal_decision`, bound to that basis and one `observed_at`, canonically
  hashed.

The API should persist validated temporal decisions that drive durable routing
or explain a refusal/deferral, select the current one under its trusted monotonic
clock, and define retention rather than storing every harmless poll forever.
SBE should keep inspection nonmutating and may provide pure validators for one
document and for a prior/current pair. SBE should not create a workspace journal
entry merely because a consumer asked whether work is due.

`capacity_disposition` names only SBE's reproducible native/local scheduling
conclusion. It never represents mutable API-global admission, slots,
reservations, circuit breakers, entitlements, or spend capacity.

`observed_at` uses one canonical normalized-UTC form and is supplied by the API
for authoritative sequencing. SBE is deterministic for the exact basis/time
pair; its wall clock is not the API's authority.

## Allowed same-basis evolution

- Same basis and same observation time: exact replay.
- Later observation time: not-due may become due.
- SBE continues to choose the bounded due-action subset.
- Provider identities, bindings, route, action inventory/order, custody schedule,
  and authority remain unchanged.
- Actual provider evidence requires a new checkpoint basis.

Clock regression, due-to-not-due regression, changed native identity, changed
provider identity, changed inventory, or mismatched digests fail closed.

## Adjacent issue

External-authority requests currently bind the complete observation, including
`observed_at`. The preferred correction is to bind the immutable checkpoint
basis and exact action inventory instead. Repeated inspection of one basis then
reproduces one exact request digest. A grant becomes stale because its basis or
request changed, not merely because time advanced. Any genuinely time-sensitive
authority rule should expose an explicit expiry/validity field.

Repeated identical due decisions remain idempotent. API lease/custody controls,
not an assumption of inspection uniqueness, prevent duplicate command execution.
Reconciliation that persists provider evidence creates a new basis.

## Scope assessment

This should fit one focused, moderate-to-meaty sprint. The core change is a
contract split plus validators and API persistence adoption, not a queue redesign
or new provider state machine. Cross-route qualification is important, but routes
that cannot prove parity should fail closed rather than expanding the sprint into
unrelated orchestration work.
