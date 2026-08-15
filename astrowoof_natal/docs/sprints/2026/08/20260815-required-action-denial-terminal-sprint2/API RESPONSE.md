# Response to Required-Action Providerless-Denial Handoff

## Resolution

The reported lifecycle gap is fixed. A successful providerless denial of native
required work now commits the action denial and its run-level consequence as one
locked semantic transition. The run cannot remain indefinitely in
`retry_preparation / continuation_required`, and neither normal runner can prepare
or submit replacement provider work after terminalization.

## New denials

For a required action:

- `external_authority_denied` produces `BUDGET_EXHAUSTED`, terminal outcome
  `budget_exhausted`, and reason `external_spend_authority_denied`;
- `reservation_unavailable` produces `BUDGET_EXHAUSTED`, terminal outcome
  `budget_exhausted`, and reason `external_spend_reservation_unavailable`;
- `product_policy_denied` produces `POLICY_STOPPED`, terminal outcome
  `policy_stopped`, and reason `external_product_policy_denied`; and
- `run_cancelled_before_submission` produces `POLICY_STOPPED`, terminal outcome
  `policy_stopped`, and reason `run_cancelled_before_submission`.

Once the API submits an accepted providerless denial, that decision is final. A
temporary inability to reserve capacity must remain API-owned waiting and must not
be sent to SBE as a denial.

Successful new single and batch results use v0.2 and contain required
`run_transition`. In a batch, `denied_action_ids` contains every accepted ordered
member while `required_action_ids` contains only the causal required subset.

## Preserved boundaries

- Optional stages retain their frozen generation-profile `skip` behavior and do
  not terminalize the run merely because they are denied.
- Accepted delivery remains authoritative; cleanup denial does not downgrade or
  reopen delivered editorial work.
- An existing native terminal authority remains first and is not overwritten.
- Provider identity, consumption, reported cost, or ambiguous submission prevents
  providerless denial and continues to fail closed.
- Action authorization history, exact binding, API authority reference, accepted
  editorial evidence, and delivery bytes remain monotonic.
- SBE does not release API reservations or capacity and does not own global quotas,
  circuit breakers, entitlements, leases, billing reconciliation, publication, or
  HTTP status authority.

## Lifecycle result

After a successful required denial, lifecycle inspection and closeout now report:

```text
terminal = true
provider_continuation_remains = false
local_continuation_remains = false
local_dependencies = []
unresolved_action_ids = []
quiescence = quiescent
closeout disposition = closed
delivery_publishable = false (unless accepted delivery already existed)
```

The API can use this native evidence to mark its execution terminal and release
its separately owned capacity. It should consume status plus terminal reason;
`BUDGET_EXHAUSTED` alone does not distinguish external/global refusal from SBE's
own frozen per-run ceiling.

## Retained 0.4.1 workspaces

SBE now recognizes the exact affected legacy shape: durable
`DENIED_PROVIDERLESS` action evidence whose single or atomic-batch artifact lacks
the later run transition. Restore the complete workspace at its stable logical
absolute path and use normal closeout/resume or:

```text
astrowoof-authoring-lifecycle --run-dir RUN reconcile-required-denial
```

The recognizer validates the complete snapshot, exact denial artifact and binding,
provider absence, denial vocabulary, frozen native requiredness, and competing
delivery/review/ambiguity conditions. It then writes one reconciliation artifact,
one state revision, and one snapshot. Exact replay is nonmutating.

Interrupted reconciliation is recoverable at each declared persistence boundary,
but recovery may complete only its exact write set. Changed denial evidence,
provider evidence, optional-only evidence, contradictions, missing members, or
unrelated workspace changes fail closed. Those workspaces must remain retained for
review; consumers must not edit or re-snapshot them manually.

The retained `a5270c02...` workspace itself was not mutated during this sprint.
The API can qualify it through the packaged command after installing the next
pinnable SBE patch.

## Consumer interfaces

The supported installed interfaces are documented in
[`Authoring Lifecycle Consumer Handoff.md`](../../../../post_extraction_authoring/Authoring%20Lifecycle%20Consumer%20Handoff.md).
The packaged catalog identifies v0.2 as the current successful single/batch result
and v0.1 as historical reader compatibility. First reconciliation emits the
existing redacted, non-authoritative `terminal.transitioned` event; replay does not
duplicate it. Events never authorize API mutation.

## Qualification and recommendation

- Focused consumer/lifecycle tests: 79 passed.
- Complete repository suite: 310 passed.
- Failure injection: all four reconciliation boundaries recovered safely.
- Fresh Windows Python 3.11 installed-wheel smoke: passed.
- Fresh Linux Python 3.11 installed-wheel smoke with networking disabled: passed.
- Reproducible candidate builds: byte-identical SHA-256
  `a344dfedf3b71beef52006ed7f19037d5c001cadc583f9d88026c05d4067f296`.
- Provider operations: 0; paid spend: `$0`; API key: not used.

SBE recommends a pinnable `0.4.2` patch release. The recorded candidate is
qualification evidence built from the Slice 4 source state and is not the future
immutable release artifact. Version bump, exact source-commit build, final hashes,
tag, and publication require separate authorization.
