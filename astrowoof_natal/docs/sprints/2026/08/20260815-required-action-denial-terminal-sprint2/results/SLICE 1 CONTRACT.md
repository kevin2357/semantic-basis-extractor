# Slice 1 Contract: Required Providerless Denial Terminalization

Status: API-approved and schema-complete; pending Kevin's Slice 1 gate approval.

The API accepted the state machine below. Packaged strict v0.2 success-result
schemas and sanitized single/mixed-batch fixtures now encode it. Denial mutation
code remains unchanged until Slice 2.

## Core rule

An accepted providerless denial is final native evidence, not a temporary wait.
If the denied action is required to produce a delivery, SBE must persist the action
denial and one run-level terminal transition in the same locked semantic mutation.

The API must not call a denial operation for a reservation delay it intends to
retry. It should retain the prepared/authorized action and retry API authority
later. Once `reservation_unavailable` is submitted to and accepted by SBE as a
providerless denial, that action is irreversibly denied.

## Status and cause model

The leading contract uses existing terminal outcomes while adding an exact cause:

| Final denial reason | Native status | Lifecycle outcome | Terminal reason/cause |
| --- | --- | --- | --- |
| `external_authority_denied` | `BUDGET_EXHAUSTED` | `budget_exhausted` | `external_spend_authority_denied` |
| `reservation_unavailable` | `BUDGET_EXHAUSTED` | `budget_exhausted` | `external_spend_reservation_unavailable` |
| `product_policy_denied` | `POLICY_STOPPED` | `policy_stopped` | `external_product_policy_denied` |
| `run_cancelled_before_submission` | `POLICY_STOPPED` | `policy_stopped` | `run_cancelled_before_submission` |

`BUDGET_EXHAUSTED` is intentionally shared with SBE per-run spend exhaustion, but
the closed terminal cause is not. Consumers must persist status plus cause and must
not infer which authority stopped the run from status alone.

`POLICY_STOPPED` is proposed as a new private/public native status because a
deliberate product stop or cancellation is neither budget exhaustion nor review.
If the API prefers one status for every final external refusal, it should say so at
this gate; the exact action denial reason still remains durable.

## Requiredness and precedence matrix

The decision basis is the locked native state immediately before mutation. The API
does not supply requiredness.

| Situation | Action result | Run result |
| --- | --- | --- |
| `authoring_initial`, pre-delivery | `DENIED_PROVIDERLESS` | terminalize from denial-reason table |
| `creative_retry` needed because no attempt was accepted | `DENIED_PROVIDERLESS` | terminalize from denial-reason table |
| optional `polish`, critic, or qualitative candidate with frozen `skip` behavior | `DENIED_PROVIDERLESS`; stage durably skipped | continue deterministic pipeline; do not terminalize |
| optional stage without a supported skip policy | refuse or review; never guess | unchanged |
| accepted `DELIVERY_COMPLETE`/warnings plus unused providerless action | `DENIED_PROVIDERLESS` | preserve accepted delivery terminal status |
| already `BUDGET_EXHAUSTED` or `POLICY_STOPPED` with compatible cause | exact replay/no weakening | preserve first terminal authority |
| ambiguous/review/failure state | provider-safety/review precedence | refuse denial or preserve stronger state |
| provider identity, consumption, report, or ambiguity exists | refuse providerless denial | unchanged |
| stale observation or binding mismatch | typed refusal | unchanged |

Requiredness must use the frozen run/profile and actual editorial progress, not
stage name alone. In particular, an already accepted attempt makes a historical
creative retry non-required, and accepted delivery always wins over cleanup of
unused actions.

## Batch semantics

- Preflight remains all-or-none under one lock.
- Requiredness and resulting run consequence are calculated for every member at
  the shared decision basis.
- A successful batch containing any still-required denied action terminalizes the
  run once. All requested action denials and the one run transition share the same
  revision and checkpoint.
- If required members contain different final-denial classes, deterministic
  precedence is `POLICY_STOPPED` over `BUDGET_EXHAUSTED`, while every action keeps
  its exact reason. The API is asked to confirm this uncommon mixed batch rule.
- Optional members in the same successful batch are still denied/skipped; they do
  not weaken the required-member terminal result.
- Any refused member means zero action and zero run mutation.
- Exact replay returns the original transition and checkpoint without a second
  revision or transition event.

## Versioned denial result evolution

Requests remain the strict v0.1 single/batch contracts. Successful results evolve
to v0.2 and add one required `run_transition` object. Refused v0.2 results have no
transition because no mutation occurred. V0.1 result schemas remain packaged for
reading historical artifacts.

Proposed success field:

```json
{
  "run_transition": {
    "outcome": "terminalized",
    "trigger": "required_action_providerless_denial",
    "prior_status": "AUTHORING",
    "resulting_status": "BUDGET_EXHAUSTED",
    "terminal_outcome": "budget_exhausted",
    "terminal_reason": "external_spend_authority_denied",
    "denied_action_ids": ["paid_0123456789abcdef01234567"],
    "required_action_ids": ["paid_0123456789abcdef01234567"]
  }
}
```

Closed `outcome` values:

- `terminalized`;
- `optional_stage_skipped`;
- `delivery_status_preserved`; and
- `no_run_transition` for a successful denial whose reviewed semantics require no
  run/status change.

Closed `trigger` values:

- `required_action_providerless_denial`;
- `optional_action_providerless_denial`; and
- `accepted_delivery_precedence`.

`denied_action_ids` is every accepted member in exact request order.
`required_action_ids` is the ordered subset whose locked native requiredness
caused terminalization. This preserves full batch audit without making optional
members appear causal. The transition contains no API authority reference, policy
detail, subject PII, provider payload, or provider credentials. Exact authority
references remain in the action-local result/provenance.

## Durable native record

The run will retain an append-only terminal transition record containing:

- schema/version;
- prior and resulting run status;
- terminal outcome and closed reason;
- exact triggering action IDs and their negative-authorization artifact hashes;
- single request identity or batch request digest;
- decision revision and result revision;
- transition timestamp; and
- route/profile identities sufficient to verify the frozen requiredness decision.

Positive authorization, action binding, denial reason/reference, provider absence,
accepted attempt evidence, and delivery evidence remain monotonic. Public state
receives only the bounded status/outcome/reason and revision—not private bindings or
authority references.

## Inspection and closeout result

After a pre-delivery required external-spend denial:

```text
terminal.terminal = true
terminal.outcome = budget_exhausted
terminal.terminal_reason = external_spend_authority_denied
terminal.delivery_package_complete = false
terminal.delivery_publishable = false
terminal.provider_continuation_remains = false
terminal.local_continuation_remains = false
quiescence.state = quiescent
local_dependencies = []
unresolved_action_ids = []
closeout.disposition = closed
```

This meets the supplied `provider_local_dependency_count = 0` intent by making
both provider continuation and local dependency collections empty. It does not
claim successful delivery. The API maps the machine terminal outcome to its own
failed/policy-stopped job state and may release capacity under API policy.

## Runner behavior

Exact and bounded resume must check native terminal status after snapshot
validation and before authorization application, action preparation, controller
construction that can submit, or provider invocation. A terminal denial returns
the durable state normally and emits no awaiting-authorization event.

Optional-stage denial uses the frozen skip policy to mark the exact stage skipped
and resumes deterministic downstream work. It must not silently skip a required
action.

## Retained 0.4.1 recovery

New denials will terminalize in the denial mutation itself. Existing 0.4.1
workspaces already contain a valid denial artifact and snapshot, so mutating exact
replay would violate its byte-stability guarantee.

Proposed supported recovery is a one-time automatic native reconciliation at the
start of normal resume or closeout:

1. validate the complete snapshot and stable logical path;
2. identify exact `DENIED_PROVIDERLESS` evidence with a final denial reason;
3. cryptographically verify its action binding, negative-authorization artifact,
   batch digest if present, absence of all provider evidence, frozen profile, and
   then-current requiredness;
4. refuse if delivery/review/ambiguity/optional semantics are not deterministic;
5. persist the narrowly derived terminal record, private/public state, and one new
   snapshot revision; and
6. return the same terminal behavior as a new denial.

No inspection-only call mutates. No arbitrary snapshot bytes are blessed. Exact
denial replay remains non-mutating. The API may call normal resume or closeout on
the retained workspace; it does not edit native files or construct a synthetic
denial request.

## Events

First application retains existing action/batch denial events, followed by one
`terminal.transitioned` event after the authoritative checkpoint. Proposed bounded
data:

```json
{
  "outcome": "budget_exhausted",
  "terminal_reason": "external_spend_authority_denied"
}
```

Exact replay emits no second terminal transition. Retained-run reconciliation may
emit one transition observation. Events remain non-authoritative, redacted, and
failure-isolated.

## API review questions

The API accepted all seven questions on 2026-08-15: status/cause mapping,
`POLICY_STOPPED`, final reservation denial, v0.2 transition results, mixed-batch
precedence, narrow retained reconciliation, and closed non-delivery capacity
release. It requested one provenance clarification, now incorporated: transition
evidence carries both all ordered `denied_action_ids` and the exact causal
`required_action_ids` subset.

## Confidence

- Core required-denial terminal rule: high.
- `BUDGET_EXHAUSTED` with distinct external cause: high, following the handoff.
- Optional-stage and accepted-delivery precedence: high.
- V0.2 result evolution: high; strict compatibility is clearer than silently
  extending v0.1.
- `POLICY_STOPPED` name and mixed-batch precedence: high after API acceptance.
- Dual denied/required batch provenance: high after API request and acceptance.
- Automatic retained-workspace reconciliation: high as a contract; implementation
  confidence remains pending recovery and failure-injection evidence.
