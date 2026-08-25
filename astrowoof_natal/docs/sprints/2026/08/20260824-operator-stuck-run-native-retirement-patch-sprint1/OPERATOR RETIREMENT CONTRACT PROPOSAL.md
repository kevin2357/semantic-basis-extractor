# Operator Retirement Contract Proposal

Status: Slice 0 candidate for API review; no runtime implementation has begun.

## Purpose

This contract lets an operator deliberately retire one exact-Natal native run that
cannot be delivered and has no provider work to reconcile. It records native truth;
it does not release or describe API leases, capacity, reservations, or jobs.

## The important quiescence distinction

Current SBE lifecycle inspection derives local continuation from status. In
particular, `AWAITING_SPEND_AUTHORIZATION` produces the blocking dependency
`retry_preparation / prepared_action_authorization_pending` even when the spend
ledger contains zero actions. It consequently selects `ordinary_resume` and reports
`local_work_ready`.

That behavior is correct for normal orchestration. It also means that requiring
"no local continuation" before operator retirement would exclude the motivating
historical class by definition.

The proposed predicate is therefore **retirement quiescence**, not ordinary
lifecycle quiescence. Under the native writer it requires:

- a complete unchanged snapshot at the stable logical root;
- a supported exact-Natal run and nonterminal status;
- no active local mutation or provider operation;
- no provider identity awaiting retrieval, provider evidence awaiting ingestion,
  provider ambiguity, or identity conflict;
- no consumed/submitting action without a safe terminal disposition;
- no unresolved providerless action;
- no delivery-complete, deliverable, review-required, or competing terminal state;
  and
- an exact request binding to the current revision, snapshot, basis, route, root,
  and terminal action inventory.

Status-derived future local continuation may exist before retirement. The operator
is explicitly abandoning that continuation. After retirement, the sealed result
must assert no provider-pending, provider-custody, or locally runnable continuation.

## Public request v1

The request is closed and content-addressed. It carries:

- contract identity and version;
- native run ID and `exact_natal` route identity;
- logical workspace root;
- exact observed status from the closed retirement-eligible set (`AUTHORING`,
  `AUTHORING_COMPLETE`, `WAITING_FOR_RESPONSE`, or
  `AWAITING_SPEND_AUTHORIZATION`), plus revision, snapshot SHA-256, and
  checkpoint-basis SHA-256;
- complete terminal action-inventory/closure SHA-256;
- requested terminal status `POLICY_STOPPED`;
- requested terminal cause `operator_retired`;
- durable reason `operator_abandoned_quiescent_run`;
- opaque operator/API audit reference;
- request digest.

Human explanation is audit material and does not create new policy semantics.

## Dry-run and execute

Dry-run validates the exact same eligibility predicate as execute and returns
`eligible` or a closed refusal with deterministically ordered failed predicates. It
does not refresh the snapshot, append a journal record, publish a native result, or
contact a provider.

`retirement_quiescent` describes the current native workspace independently from
the supplied request. A stale or binding-mismatched request against an otherwise
retirement-quiescent workspace therefore returns `outcome: refused` and
`retirement_quiescent: true`. Request admissibility determines the outcome; it does
not rewrite the native-state fact.

`provider_io_performed_count` describes provider I/O performed by this dry-run
operation. It is always zero and does not describe historical provider rows.

Execute reacquires the native single-writer lock, re-reads the workspace, validates
the request and every predicate, then records `POLICY_STOPPED / operator_retired`.
It uses the existing atomic publication protocol: journal range, full validated
snapshot, immutable result, and immutable publication receipt.

## Result v1

Success is one of `applied`, `exact_replay`, or `already_retired` and binds:

- native run ID, exact route, and logical root;
- original request digest;
- pre/post revision and snapshot digest;
- terminal status and terminal cause;
- terminal action-inventory/closure digest;
- native result and publication-receipt IDs/digests; and
- explicit false assertions for provider pending, provider custody, and runnable
  local continuation.

Those three assertions are derived from a fresh post-transition lifecycle
inspection while SBE still owns the native writer. They are never copied from the
request or accepted as caller input. The closure digest commits to the complete
ordered ledger representation, including every providerless denial disposition.

`exact_replay` requires the exact original request digest. A later compatible
request may return `already_retired`; it is not represented as exact replay.
Both outcomes return the original sealed native result and receipt without state,
revision, journal, snapshot, result-index, or receipt mutation. `already_retired`
separately carries the later request digest and the original request digest.

Closed refusals include `stale_observation`, `not_retirement_quiescent`,
`provider_custody_present`, `provider_ambiguity_present`,
`providerless_action_unresolved`, `delivery_or_terminal_conflict`,
`binding_mismatch`, `snapshot_invalid`, and `unsupported_contract`.

## Providerless actions

Retirement never silently disposes an action. Every unresolved providerless action
must first receive its existing supported denial disposition. Until then the
retirement request refuses as `providerless_action_unresolved`. Denial and
retirement are intentionally not one atomic operation in v1.

## API companion fence

Before calling SBE, the API atomically places its job into an API-owned
operator-retirement-pending custody state that prevents ordinary worker claim or
continuation while retaining all API resources. SBE neither validates nor asserts
that external state. API resource release happens only after transactional
ingestion of a validated successful SBE result. Exact replay allows interrupted API
finalization to resume without repeating the native transition.

## Route and safety boundary

V1 supports exact Natal only. Bounded Natal and every other route fail closed as
unsupported. The operation accepts no provider credential, request payload, spend
grant, retrieval, cancellation, retry, or submission input and performs no provider
network operation.

## Slice 0 decision

The API approved `retirement_quiescent` as the precondition for the motivating
`AWAITING_SPEND_AUTHORIZATION` class, while `local continuation = false` remains a
mandatory freshly derived post-transition assertion. Requiring ordinary lifecycle
quiescence before mutation would make that historical class ineligible because its
status itself derives `retry_preparation`, even with an empty action inventory.
