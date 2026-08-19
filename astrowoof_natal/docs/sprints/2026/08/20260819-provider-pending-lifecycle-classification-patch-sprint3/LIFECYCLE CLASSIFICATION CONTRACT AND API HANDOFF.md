# Lifecycle Classification Contract and API Handoff

Status: API approved; no implementation has begun  
Proposed contract: `astrowoof.authoring_lifecycle_inspection.v0.4`

## Consumer problem

Lifecycle inspection v0.3 exposes validated capacity and provider custody, but it
does not unambiguously identify which supported SBE command should run when a
provider operation is due. It also reports provider result reconciliation as local
continuation. API Sprint 29 consequently selected ordinary semantic closure
`--resume` repeatedly instead of `--provider-reconciliation-cycle`.

The API must not infer the command from private `run.json`, workspace paths,
snapshots, logs, provider IDs, or historical subprocess outcomes. v0.4 makes the
branch a closed native projection.

## v0.4 shape

v0.4 preserves all v0.3 top-level members and adds exactly one required member:

```json
{
  "execution_branch": {
    "command": "provider_reconciliation_cycle",
    "eligible_now": false,
    "reason_code": "provider_reconciliation_not_due",
    "action_ids": ["paid_..."],
    "not_before": "2026-08-19T12:00:15Z"
  }
}
```

Closed fields:

| Field | Values / rule |
|---|---|
| `command` | `ordinary_resume`, `provider_reconciliation_cycle`, `await_external_authority`, `none` |
| `eligible_now` | Boolean; whether the named command may execute at `observation.observed_at` |
| `reason_code` | Closed values listed below |
| `action_ids` | Ordered unique native paid-action IDs selected by SBE for the next bounded operation; maximum four for due interactive reconciliation; empty for ordinary local/terminal cases |
| `not_before` | UTC instant only for not-due provider reconciliation; otherwise `null` |

Closed branch reasons:

- `ordinary_local_continuation_ready`
- `provider_reconciliation_not_due`
- `provider_reconciliation_due`
- `spend_authorization_required`
- `terminal_or_no_continuation`
- `native_review_or_ambiguity`
- `unsupported_native_evidence`

The full v0.4 object remains closed-world (`additionalProperties: false`). The
canonical contract catalog and packaged fixtures bind its exact schema.

## Required tuples

### A. Provider-only pending, not due

| Field | Required value |
|---|---|
| `terminal.provider_continuation_remains` | `true` |
| `terminal.local_continuation_remains` | `false` |
| `local_dependencies` | `[]` |
| `quiescence.state` | `not_quiescent` |
| `quiescence.reasons` | `['provider_continuation_remains']` |
| `execution_capacity.disposition` | `release_until_due` |
| `execution_capacity.local_work_ready_now` | `false` |
| `execution_capacity.checkpoint_safe_for_worker_release` | `true` |
| `execution_capacity.resume_not_before` | exact earliest pending-action due time |
| `execution_capacity.reason_code` | `known_provider_work_pending` |
| `provider_custody.state` | `known_operations_pending` |
| `provider_custody.earliest_resume_not_before` | same exact due time |
| `execution_branch.command` | `provider_reconciliation_cycle` |
| `execution_branch.eligible_now` | `false` |
| `execution_branch.reason_code` | `provider_reconciliation_not_due` |
| `execution_branch.action_ids` | exact ordered pending provider action IDs |
| `execution_branch.not_before` | same exact due time |
| `consumer_authority.state` | `retain` |

The due time must be strictly later than `observation.observed_at`; otherwise tuple
B applies. Inspection is read-only and performs zero provider creates/retrievals.

### B. Provider-only pending, due now

| Field | Required value |
|---|---|
| `terminal.provider_continuation_remains` | `true` |
| `terminal.local_continuation_remains` | `false` |
| `local_dependencies` | `[]` |
| `execution_capacity.disposition` | `continue_local_cycle` |
| `execution_capacity.local_work_ready_now` | `true` |
| `execution_capacity.resume_not_before` | `null` |
| `execution_capacity.reason_code` | `provider_reconciliation_due` |
| `provider_custody.state` | `known_operations_pending` |
| `execution_branch.command` | `provider_reconciliation_cycle` |
| `execution_branch.eligible_now` | `true` |
| `execution_branch.reason_code` | `provider_reconciliation_due` |
| `execution_branch.action_ids` | exact ordered due provider action IDs (bounded by the supported cycle selection) |
| `execution_branch.not_before` | `null` |
| `consumer_authority.state` | `retain` |

This tuple is sufficient to choose reconciliation even if the first inspection
occurs after the initial delay and no earlier `release_until_due` inspection exists.

`execution_branch.action_ids` is evidence of SBE's native bounded selection, not a
consumer command-building interface. The API invokes the route-neutral supported
reconciliation command against the run. It must not choose members, pass member
IDs as an override, or rebuild the operation from those IDs. SBE remains solely
responsible for revalidating current native state and selecting the due subset at
execution time.

### C. Ordinary local continuation

| Field | Required value |
|---|---|
| `terminal.local_continuation_remains` | `true` |
| `local_dependencies` | one or more non-provider local dependencies |
| `execution_capacity.disposition` | `continue_local_cycle` |
| `execution_capacity.local_work_ready_now` | `true` |
| `execution_capacity.resume_not_before` | `null` |
| `execution_capacity.reason_code` | `local_work_ready` |
| `execution_branch.command` | `ordinary_resume` |
| `execution_branch.eligible_now` | `true` |
| `execution_branch.reason_code` | `ordinary_local_continuation_ready` |
| `execution_branch.action_ids` | `[]` |
| `execution_branch.not_before` | `null` |

Provider custody may coexist with genuine local work, but due provider
reconciliation retains the current precedence. The branch must be derived from the
closed native policy, never consumer guesswork.

### D. Awaiting external spend authority

`execution_capacity.disposition=await_external_authority`, branch command
`await_external_authority`, `eligible_now=false`, reason
`spend_authorization_required`, and exact prepared action IDs. Provider create is
forbidden until the existing authorization contract is satisfied.

### E. Review, ambiguity, unsupported, or terminal

Branch command is `none`; it cannot authorize ordinary resume or reconciliation.
The existing capacity/review/terminal evidence remains authoritative and
consumer authority remains retained where already required.

## Contradictions that must be rejected

At minimum, schema/semantic validation rejects:

- provider-only pending plus `local_continuation_remains=true`;
- `release_until_due` with local work ready, missing/expired due time, unsafe
  checkpoint, non-pending custody, or eligible branch;
- provider reconciliation due with `ordinary_resume`;
- ordinary resume without a non-provider local dependency;
- reconciliation branch action IDs outside provider custody;
- not-due branch time unequal to capacity/custody earliest due time;
- due branch with a future selected action;
- missing reconciliation timing or unsupported route represented as runnable;
- ambiguous/conflicting provider evidence represented as either runnable branch;
- any unknown field or vocabulary value.

Refusal is a contract error/review outcome. It never falls back to ordinary resume.

## API command-selection rule

After strict v0.4 validation and persistence:

```text
execution_branch.command == provider_reconciliation_cycle
  and eligible_now == false
    -> atomically release local capacity until not_before;
       retain provider and consumer authority

execution_branch.command == provider_reconciliation_cycle
  and eligible_now == true
    -> invoke --provider-reconciliation-cycle;
       never ordinary --resume

execution_branch.command == ordinary_resume
  and eligible_now == true
    -> invoke ordinary semantic closure --resume

await_external_authority or none
    -> do not invoke either execution command
```

The API remains authoritative for its queue, lease, capacity allocation,
reservations, quotas, billing, and product state. SBE remains authoritative for
native classification, timing, provider custody, snapshots, and command safety.

## Diagnostic events and logs

Proposed non-authoritative structured events:

### `lifecycle.classification.selected`

- native run ID and state revision in correlation;
- lifecycle schema version;
- route family and provider mechanism;
- capacity disposition;
- recommended command, eligibility, and reason;
- provider action count, due count, and non-provider local dependency count;
- resume-not-before when applicable.

### `execution.branch.invoked`

- actual public command (`ordinary_resume` or `provider_reconciliation_cycle`);
- recommended command from the immediately validated inspection when available;
- match/mismatch classification;
- reason code and bounded action counts.

The ordinary ✨🐶 logs carry the same concise facts for operators. Events/logs are
failure-isolated and cannot authorize work. Provider IDs may be omitted or reduced
to counts in diagnostics; no credentials, request bodies, prompts, outputs, or
protected subject parameters are allowed.

## Compatibility and retained workspace

- v0.3 remains historically readable but is not sufficient for the corrected API
  branch selection. New production admission requires v0.4.
- Native exact run schema `astrowoof.semantic_closure_run.v0.9`, spend ledger,
  provider reconciliation timing v0.2, provider IDs, snapshots, and authoring pass
  records do not require migration.
- A complete 0.4.12 retained workspace with six durable IDs and valid timing should
  be inspectable by the patch release without mutation and should emit v0.4.
- The API must ingest a fresh v0.4 inspection and must not reinterpret or edit the
  older persisted inspection.
- If the due time has passed, tuple B selects reconciliation directly. Poll existing
  IDs only; never submit replacements.
- If exact snapshot/path, route, timing, provider binding, or exclusive access
  validation fails, retain the workspace for review. There is no manual blessing
  or run.json rewrite procedure.
- The paused cohort remains untouched until both SBE and API implementations pass
  provider-free installed-wheel qualification and Kevin explicitly authorizes
  recovery.

## Requested API review questions

1. Is v0.4 with one closed `execution_branch` object preferable to deriving the
   command from multiple v0.3 fields?
2. Are tuples A–E sufficient for strict API command selection and capacity release?
3. Does direct due selection in tuple B remove the requirement for a historically
   persisted release inspection?
4. Resolved: `execution_branch.action_ids` contains only SBE's next bounded due
   selection (maximum four) for tuple B, while provider custody retains the complete
   inventory. API does not select or override members.
5. Does the retained-workspace procedure preserve API authority and no-resubmit
   guarantees?
6. Are the proposed diagnostic event facts sufficient without provider IDs?

## API approval

The AstroWoof API agent approved the v0.4 plan and both root-cause corrections.
Review evidence is recorded at API commit `4455acc`. Its sole clarification—the
non-authoritative/non-command-building role of the next bounded action subset—is
incorporated above.
