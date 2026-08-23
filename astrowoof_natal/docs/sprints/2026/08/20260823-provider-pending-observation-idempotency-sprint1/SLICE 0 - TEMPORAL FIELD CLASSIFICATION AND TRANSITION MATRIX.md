# Slice 0 — Temporal Field Classification and Transition Matrix

Date: 2026-08-23
Status: candidate findings for SBE/API review

## Reproduction

One provider-free six-action exact-interactive workspace was inspected twice
without changing any workspace byte:

- `t0 = 2026-08-15T20:10:00Z`, before the earliest durable
  `resume_not_before = 2026-08-15T20:15:00Z`; and
- `t1 = 2026-08-15T20:30:00Z`, after all six actions were due.

At `t0`, SBE projected `release_until_due` and a non-eligible
`provider_reconciliation_cycle`. At `t1`, it projected
`continue_local_cycle`, an eligible reconciliation command, and the first four
actions selected by SBE's native bounded-retrieval policy. The snapshot digest,
state revision, route, six provider identities, action order, bindings, custody
schedule, consumer authority, terminal facts, and workspace hashes were
unchanged. No provider transport is reachable from `inspect_lifecycle()`.

## Candidate field classification

### Immutable checkpoint basis

- native run ID, state revision, snapshot digest, logical root, inventory and
  snapshot validity;
- route family, route contract, provider mechanism, native operation identity;
- ordered action inventory, bindings/digests, provider IDs, necessary/release
  evidence, and authority-retention facts;
- complete provider custody action projection, including every action's durable
  `resume_not_before`, and `earliest_resume_not_before`;
- local dependencies, terminal facts, quiescence facts, and review reasons.

Any change above requires a new checkpoint basis or is a contradiction.

### Trusted temporal input

- `observed_at`, supplied in one canonical normalized-UTC representation by the
  API trusted clock.

### Derived temporal scheduling decision

- native/local `capacity_disposition`, `local_work_ready_now`, reason, and
  derived top-level `resume_not_before`;
- supported command, eligibility, reason, and derived `not_before`;
- SBE-selected bounded due-action subset (`next_due_action_ids` and the command
  action IDs when due).

`capacity_disposition` does not represent API admission, worker slots,
reservations, circuit breakers, entitlements, account limits, or spend capacity.

## Observed v0.5 changed paths

The exact changed paths in the reproduction were:

1. `observation.observed_at`
2. `action_inventory.observation.observed_at`
3. `execution_capacity.disposition`
4. `execution_capacity.local_work_ready_now`
5. `execution_capacity.resume_not_before`
6. `execution_capacity.reason_code`
7. `provider_custody.next_due_action_ids`
8. `execution_branch.eligible_now`
9. `execution_branch.reason_code`
10. `execution_branch.action_ids`
11. `execution_branch.not_before`

This list describes incident evidence, not the proposed v0.6 wire shape.

## Candidate transition matrix

| Prior/current relationship | Result |
|---|---|
| Same basis, same canonical `observed_at`, same decision | Exact idempotent replay |
| Same basis, later time, not-due to due | Allowed |
| Same basis, later time, identical due decision | Allowed idempotent evidence; API lease/custody controls invocation |
| Same basis, clock regression | Refuse |
| Same basis, due to not-due | Refuse |
| Same basis, changed custody schedule or `resume_not_before` | Refuse; schedule belongs to basis |
| Same basis, changed route/mechanism/action order/binding/provider ID/authority | Refuse |
| Supported retrieval persists provider status/result/usage | New snapshot and checkpoint basis required |
| Old lifecycle v0.5 presented at the new split boundary | Fail closed; no reinterpretation |

## External-authority conclusion

An external-authority request should bind the immutable checkpoint basis and
exact ordered action inventory. It should not bind incidental `observed_at`.
Repeated inspection of one unchanged prepared basis should reproduce the same
request digest. A time-sensitive authority rule, if ever needed, requires an
explicit validity/expiry field. Exact grants remain fail-closed against a changed
basis, request, or inventory.

## Slice gate

Pause for SBE/API review of this classification, transition matrix, clock
ownership, and authority-request conclusion before designing the v0.6 schema.
