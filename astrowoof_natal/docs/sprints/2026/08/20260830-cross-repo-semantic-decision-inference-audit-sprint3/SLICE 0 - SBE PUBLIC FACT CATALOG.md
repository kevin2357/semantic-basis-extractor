# Slice 0 — SBE public fact catalog

## Catalog basis

This catalog describes the public SBE boundary shipped in
`astrowoof-natal-authoring==0.4.32`, with exact dependency identity
`semantic-projection-core==0.11.1`. It was derived from package exports,
validators, schemas, fixtures, installed commands, and consumer handoffs. It is
not a claim about any API mapper yet.

The central finding is structural: SBE does not have one total state whose name
answers every consumer question. Native status, evidence integrity, local work,
provider custody, temporal eligibility, review, terminality, delivery, and API
resource state are separate dimensions.

## Lifecycle inspection family

| Contract | Native facts it adds | Positive permission available | It does **not** mean |
|---|---|---|---|
| `astrowoof.authoring_lifecycle_inspection.v0.5` | Native status, terminal summary, quiescence, dependencies, action inventory, review reasons, capacity conclusion, provider custody, route, consumer-authority classification, external-authority request/refusal, and closed execution branch | Invoke only the exact supported command named by `execution_branch.command` when its complete branch predicate and `eligible_now` allow it | Status alone selects a command; empty dependencies mean terminal; custody means retrieval due; capacity disposition releases API authority |
| `astrowoof.authoring_lifecycle_inspection.v0.6` | Splits immutable checkpoint basis from API-time-relative temporal decision | Invoke the SBE-selected temporal command/subset for the exact validated `(checkpoint_basis, observed_at)` decision | Time advancement changes native truth; API may choose reconciliation members; a later inspection invalidates an otherwise basis-bound authority request |
| `astrowoof.authoring_lifecycle_inspection.v0.7` | Adds closed local-work inventory, basis-independent operation keys, and cumulative consumed-operation history | Invoke `ordinary_resume` only for an advertised eligible operation joined to this exact inspection; prior operation inventory becomes unusable after progress | Local continuation exists merely because release-until-due is false; snapshot churn proves work consumption; local work existence means every local operation is runnable |
| `astrowoof.authoring_lifecycle_inspection.v0.8` | Adds retry-lineage inventory, conflict classification, forward-dispatch permission, and reconciliation permission | Reconcile durable provider custody when permitted; forward dispatch only when lineage explicitly permits it and the selected branch independently authorizes it | Lineage conflict erases custody; review forbids retrieval of already-durable provider work; request binding belongs in logical-attempt identity |

### Version-selection rule

These versions are not a ladder for blind fallback and not interchangeable
spelling variants.

- Use the minimum version that explicitly carries the fact required by the API
  decision.
- v0.5 remains valid for decisions fully represented by v0.5.
- Decisions about consumable local-work identity require v0.7.
- Decisions about retry-lineage conflict or mixed lineage/custody require v0.8.
- Time-relative due/not-due sequencing uses v0.6's checkpoint/decision split.
- A consumer that lacks the version required for a decision must retain/refuse
  through a typed unsupported path; it must not reinterpret an older document.

## Meanings of high-risk lifecycle fields

| Fact | Narrow normative meaning | Required companions | Forbidden inference |
|---|---|---|---|
| `terminal.terminal` | SBE native execution has reached the terminal posture described by the complete terminal object | terminal outcome/reason, continuation flags, delivery flags, custody and closeout evidence | API job is fully settled, reservations released, or delivery publishable |
| `terminal.outcome` | Closed native outcome classification at this checkpoint | `terminal.terminal`, reason, continuation and delivery assertions | Any outcome word alone controls API state |
| `terminal.delivery_publishable` | Native delivery evidence satisfies the SBE publishability assertion | validated terminal/delivery package and API publication policy | terminal necessarily implies publishable |
| `terminal.local_continuation_remains` | Native local continuation still exists | branch/local inventory needed to know whether work is executable now | `false` means terminal; `true` names a runnable command |
| `terminal.provider_continuation_remains` | Native provider-related continuation/custody remains | provider-custody inventory and temporal decision | retrieval is due or new creation is permitted |
| `execution_branch.command` | SBE-selected supported next command for the exact inspection | complete branch predicate, `eligible_now`, reason, action inventory, version | API may substitute a semantically similar command |
| `execution_branch.eligible_now` | Selected native command is or is not executable under this inspection | exact command, basis/observation, capacity and custody joins | general job claimability or API admission |
| `execution_branch.action_ids` / v0.6 `due_action_ids` | SBE-selected ordered/bounded members for the named command | command and inspection identity | API may rebuild, expand, reorder, or independently select members |
| `execution_capacity.disposition` / v0.6 temporal `capacity_disposition` | SBE's native/local worker-capacity conclusion | checkpoint safety, command eligibility, local work and custody | API lease, slot, reservation, or consumer-authority disposition |
| `checkpoint_safe_for_worker_release` | Native bytes form a safe checkpoint for relinquishing local execution | API must still persist/ingest and apply its own lease policy | provider identity, reservation, custody, or financial authority may be released |
| `provider_custody.actions` | Exact known provider-bound actions and native custody classification | route/mechanism/action/binding/provider identity and schedule | every member is due; absence proves no provider work ever occurred |
| `consumer_authority` | Native classification of which actions require consumer-side authority retention | API's own reservation/admission records | SBE has released or settled API-global money |
| `local_dependencies` | Native dependency presentation for the represented contract | local-work inventory in v0.7 when operation identity is needed | empty means no deterministic fan-in or no local continuation |
| `review_reasons` / conflict classification | Closed native evidence that requires review | custody and branch precedence remain independently authoritative | review is terminal or permits API resource release |

## Sealed native execution evidence

### Contracts

- `astrowoof.native_execution_result.v0.1`
- `astrowoof.native_execution_result.v0.2` for terminal-review evidence
- `astrowoof.native_publication_receipt.v0.1`
- `astrowoof.native_transition_result_availability.v1`

### Meaning of sealed

There is no standalone `sealed == terminal` contract. In this model, “sealed”
means the result and canonical receipt validate together and bind:

- native run and invocation;
- result ID and digest;
- journal range;
- checkpoint basis;
- complete workspace snapshot; and
- logical workspace root.

That is evidence-integrity finality for those exact bytes. It does not assert
native terminality. The v0.1 outcome vocabulary explicitly includes nonterminal
states such as `provider_pending`, `continuation_required`, and
`awaiting_external_authority`, as well as `review_required` and terminal outcomes.
A later native transition may publish an immutable successor without modifying
the earlier result.

### Result-selection authority

1. If an invocation returns an exact result ID, validate and ingest that exact
   result and receipt. Its typed outcome outranks the process exit code.
2. `latest_native_transition_result` is a convenience reader, not generic
   transition authority.
3. `native_transition_result_availability.v1` discovers one exact result ID from
   a snapshot-valid complete publication inventory. Its own contract explicitly
   grants no transition authority.
4. Availability discovery is valid only under a named recovery/preflight flow
   where no exact invocation result ID was returned. The discovered result still
   requires its full result/receipt/snapshot/invocation joins.

## External authority and provider dispatch

### Initial-wave v1

- `astrowoof.external_authority_request.v1`
- `astrowoof.external_authority_grant.v1`
- `astrowoof.external_authority_refusal.v1`

The complete request binds ordered actions and public bindings to the snapshot
observation. A positive aggregate grant authorizes only that exact request. Grant
presence is not provider-create proof; writer-fenced native intent and the
route-specific constrained executor remain required.

### Ordinary-action v2

- `astrowoof.external_authority_request.v2`
- `astrowoof.external_authority_grant.v2`
- `astrowoof.external_authority_dispatch_result.v2`
- `astrowoof.external_authority_intent_result.v2`
- `astrowoof.external_authority_provider_dispatch_result.v2` / `v3`
- `astrowoof.external_authority_v2_command_result.v1` / `v2`
- `astrowoof.generic_provider_dispatch_refusal.v1`

The v2 request is an inspection-joined reference, not enough by itself to
reconstruct authorization. Complete public binding lives in each ordinary spend
authorization document; the grant binds ordered document references/digests.

Positive permissions are separate:

- request available: API may decide whether to grant;
- compatible grant validated: SBE may commit exact authorization/intent;
- `provider_create_permitted`: constrained executor may cross the create fence;
- `provider_io_disposition=not_attempted`: provider creation is proven not to
  have been entered for that invocation;
- `create_entered_unknown`: ambiguity/review custody, never create retry;
- durable provider identity: reconciliation-only custody for that action.

Neither a prepared action, an authorization record, nor `await_external_authority`
alone permits generic provider creation.

## Provider reconciliation

The public lifecycle branch/temporal decision selects
`provider_reconciliation_cycle`, its eligibility, lower-bound `not_before`, and
SBE's bounded due subset. The consumer invokes the supported run-level command;
it does not construct a member command from IDs.

Key distinctions:

- provider custody present ≠ retrieval due;
- retrieval due ≠ provider creation permitted;
- provider terminal ≠ cost settled;
- missing usage ≠ `$0`;
- not-due result ≠ new checkpoint;
- retrieval completion may unblock exact deterministic local work; and
- nonblocking optional custody may coexist with publishable delivery without
  losing action/financial authority.

## Terminal review, denial, closeout, and retirement

### Terminal review v0.2

`astrowoof.native_execution_result.v0.2` carries the closed review cause and
complete terminal action dispositions. Its command-result envelope binds the
invocation to the exact result/publication. Exit 2 is not the review authority;
the sealed typed result is.

A review-required result may retain provider custody. Its predecessor remains
immutable while later reconciliation/denial publishes traceable custody-only
successors. Review-required is not inherently terminal and must not silently
reopen editorial work.

### Providerless denial

Successful denial evidence, exact member/binding/reference joins, and
`release_eligible` determine whether an API reservation may be released. In a
batch, no member releases when the top-level batch is refused. `required_action_ids`
are the terminal causal set; the full ordered denied-action inventory is audit
history.

### Closeout

Closeout combines terminal summary, quiescence, dependencies, unresolved actions,
and delivery flags. A terminal native outcome does not independently authorize
API job terminalization, reservation settlement, or publication.

### Operator retirement

The retirement result can establish native `POLICY_STOPPED / operator_retired`
with fresh post-transition assertions that provider custody, pending provider
work, and runnable local continuation are absent. API must still apply its own
pending fence and finalize its resources only after validating the sealed result
and exact request/replay relationship.

## Identity and digest join map

| Boundary | Required join |
|---|---|
| Lifecycle versions | native run, route, operator revision, snapshot digest, logical root; action/binding/provider inventory where represented |
| v0.6 temporal decision | `checkpoint_basis_sha256` in both basis and decision plus canonical API-supplied `observed_at` |
| v0.7 local operation | inspection basis, `operation_id`, stable `operation_key`, source action IDs, cumulative consumed keys |
| v0.8 retry lineage | logical attempt key, action ID, binding evidence, pass/attempt pointer, provider custody inventory, conflict classification |
| External authority | request digest, run/basis or observation, ordered action IDs, full authorization-document bindings, grant member references/digests |
| Invocation result | invocation ID → exact result ID; result digest → receipt; receipt → journal/checkpoint/snapshot/root |
| Availability recovery | restored snapshot digest, complete result index/inventory, discovered result ID, then full result/receipt validation |
| API action persistence | native run/action ID and complete binding/provider identity; API reservation/admission identity stays API-owned |

## Closed unknown/absent/contradictory posture

| Condition | Required consumer posture |
|---|---|
| Required evidence absent | Typed unavailable/retain path; do not convert absence to false permission |
| Evidence structurally or semantically contradictory | Integrity/review refusal; preserve relevant custody/authority; do not choose a fallback command |
| Unsupported authoritative schema version | Fail closed as unsupported; do not reinterpret through a nearby version |
| Required newer dimension absent from an older valid version | Typed contract-upgrade/unsupported path for that decision; the old document may remain valid for narrower decisions |
| Event/log/exit code disagrees with sealed typed result | Sealed validated result wins; diagnostics record the disagreement |
| Availability discovery conflicts with exact invocation-returned result | Exact invocation result wins; retain conflict for review rather than choosing “latest” |

## Catalog conclusion

The current public surface already provides explicit facts for most high-risk
decisions. The API audit should therefore begin with a presumption that mapper
shortcuts—not missing SBE booleans—are the likely issue. A new SBE field is
justified only when a registry row proves that no existing validated field or
join can express the required native permission.
