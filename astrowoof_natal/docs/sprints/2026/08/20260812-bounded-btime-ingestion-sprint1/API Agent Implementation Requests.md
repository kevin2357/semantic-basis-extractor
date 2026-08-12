# API Agent Implementation Requests

```yaml
status: input-for-sprint-planning
author: astrowoof-api-agent
date: 2026-08-12
target: semantic-basis-extractor
sprint: 20260812-bounded-btime-ingestion-sprint1
evidence_run: Sarah exact-time staging WoofMap
```

## Purpose and evidence boundary

These requests accompany the planned bounded-birth-time ingestion work. They are
grounded in the first unassisted staging WoofMap run for Sarah, but they are not a
request to reshape SBE around one accidental trace. The run proved that the
API/worker/SBE boundary can autonomously reach a legitimate authoring limit, fail
closed, release all execution leases, preserve durable checkpoints, and withhold
publication. The remaining findings concern making that safe outcome explicit,
reconcilable, and easier for a coordinator to interpret.

The observed run had:

- six reported initial Responses with approximately `$0.783256` total actual cost;
- one reported creative-retry Response with approximately `$0.236302` actual cost;
- one creative-retry action externally authorized but never associated with a
  provider operation;
- a `$4.00` creative-retry category ceiling enforced against maximum authorized
  commitments rather than optimistic actual cost;
- a subsequent action rejected by the API with `paid action exceeds category
  ceiling`;
- an outer reading, generation run, and SBE job correctly marked failed;
- zero active leases and no publication authority; and
- a latest native SBE checkpoint whose status remained
  `AWAITING_SPEND_AUTHORIZATION` rather than recording the outer terminal denial.

A subsequent global read-only audit established that the terminal reconciliation
gap is not unique to Sarah:

- the queue had zero active leases and zero available, leased, or retry-wait jobs;
- eight provider-less actions remained `authorized` across three terminal runs;
- those included six actions on one failed run, one action on a successful/ready
  run, and Sarah's one action; and
- all twelve execution jobs had zero corresponding API `worker_workspaces` rows.

The first two facts show that these are inert reconciliation records, not hidden
work. The latter two show that API terminal-action release and scratch-registration
integration need systematic correction rather than one-off Sarah cleanup.

## Request 1 - Supported negative-authorization and terminal-closeout contract

### Problem

SBE has a strong positive authorization boundary: it prepares paid work and waits
for the caller to authorize it. The Sarah run demonstrated the complementary case:
the caller can permanently refuse an otherwise valid prepared action because a
hard category or run ceiling has been reached.

At present, the API can fail its execution job, but the newest durable native
checkpoint still describes an actionable wait for spend authorization. Both facts
are locally accurate from their owners' perspective, yet the combined state is
misleading. A future operator or recovery process could reasonably ask whether the
native run is resumable, denied, abandoned, or still awaiting a decision.

### Requested behavior

Provide a supported, provenance-preserving way for an exclusive coordinator to
report a final negative authorization decision back into SBE. The exact interface
may be a command, Python API, or resume input, but it should:

1. identify the exact native run, prepared action, authorization-request revision,
   and external lease/fencing authority;
2. accept a stable denial reason such as `category_spend_ceiling_exceeded`,
   `run_spend_ceiling_exceeded`, `owner_quota_exceeded`, `policy_disabled`, or
   `operator_declined`;
3. refuse to deny an action that already has durable provider-created evidence;
4. preserve all earlier provider IDs, responses, usage, accounting, accepted
   passes, retries, and QA evidence;
5. mark the denied prepared action unconsumed through an explicit native state,
   rather than deleting its history;
6. determine whether other already-authorized or prepared actions can still
   produce a valid deck;
7. if no valid continuation remains, publish a quiescent terminal native status
   such as `FAILED_SPEND_AUTHORIZATION_DENIED` or `AUTHORING_EXHAUSTED`; and
8. produce a fresh complete snapshot that can be validated and retained without
   implying that more authorization is expected.

The terminal outcome should distinguish “the provider failed,” “the response was
creatively rejected,” “the configured retry policy was exhausted,” and “the
external coordinator refused further spend.” They have different operational and
product meanings.

### Why SBE involvement is appropriate

The API owns the ceiling and the decision to deny spend. SBE owns whether the
remaining accepted and rejected work can still form a valid deck and how a denied
action affects its native closure state. Neither system can authoritatively infer
the complete terminal result alone.

## Request 2 - Clarify and harden multiple outstanding paid-action ordering

### Observation

The Sarah ledger ended with two creative-retry actions of interest:

- one action at maximum authorization `$1.604170`, state `authorized`, with no
  provider operation; and
- one later action at maximum authorization `$1.603055`, state `reported`, with a
  Response ID and actual cost `$0.236302`.

The evidence available to the API does not establish whether these actions belong
to independent pass retries that may validly proceed out of order, whether the
first action was superseded, or whether an external-authorization handoff selected
the newer action while leaving the older action stranded. This is a request for
contract clarification first, not an assertion of an SBE defect.

### Requested analysis and contract

Please determine and document:

1. whether multiple provider-less authorized actions may validly coexist for one
   live SBE run;
2. whether a later action may be submitted while an earlier authorized action
   remains unconsumed;
3. whether ordering is global, per pass, per subject, or intentionally unordered;
4. how SBE exposes supersession, cancellation, or continued necessity;
5. whether every authorization request carries enough stable pass/attempt identity
   for the API to present this safely; and
6. which system is responsible for releasing an authorized but never-submitted
   commitment after terminal closeout.

If actions are independent, expose that independence and their remaining necessity
machine-readably. If the older action had been superseded, SBE should publish an
explicit release/cancel instruction before requesting newer paid work. If ordering
was accidental, add a regression that prevents a newer provider submission until
the older authorization is consumed or explicitly released.

The API will continue to count every reserved or authorized maximum against the
hard ceiling until it receives a safe exact-action release instruction. It must not
infer release merely from low actual cost elsewhere.

## Request 3 - Machine-readable terminal outcome and failure taxonomy

The API's final classification was `worker_contract_failure`, because the spend
authority raised an exception while reconciling SBE's next prepared action. That is
safe but far too broad. The meaningful outcome was closer to:

```text
initial authoring completed
-> creative acceptance rejected some work
-> one creative retry completed
-> more retry work requested
-> external creative-retry ceiling denied further authorization
-> no publishable deck produced
```

Please expose a stable native outcome envelope that lets the API persist and log:

- terminal versus resumable versus review-required;
- terminal reason and responsible boundary;
- last successfully completed native stage;
- whether a valid deck exists;
- whether provider work remains active or ambiguous;
- prepared, externally authorized, provider-created, reported, and denied action
  counts;
- whether local continuation is required;
- whether the workspace is quiescent and checkpointable; and
- whether any exact action may safely be released externally.

This should supplement, not replace, `run.json`, the spend ledger, public state, or
checkpoint validation. The API should not have to translate exception text into
product state.

## Request 4 - Explicit quiescence and local-dependency summary

AstroWoof's API owns worker scratch registration, cleanup authority, R2 custody,
and the `worker_workspaces` table. SBE should not implement or write that API table.
The Sarah run had no `worker_workspaces` rows; that is an API integration gap and
will be handled by the API repository.

Please nevertheless confirm that SBE exposes, or add if necessary, a concise
machine-readable summary at every supported exit boundary containing:

- `workspace_quiescent`;
- `local_continuation_required`;
- provider actions depending exclusively on local state;
- provider actions with durable external identities;
- latest complete snapshot revision and digest;
- stable logical restore-path requirement; and
- terminal/resumable disposition.

This is the SBE half of the cleanup gate. It informs API authority but never grants
filesystem deletion by itself.

## Request 5 - Spend-denial and failure-closeout qualification

Add deterministic qualification for at least these paths:

1. the first prepared initial action is denied;
2. some initial passes are reported and a later initial action is denied;
3. a creative retry is reported and the next retry is denied by category ceiling;
4. a provider-less authorization exists when another action completes;
5. denial arrives after a matching provider identity became durable and must be
   rejected as unsafe;
6. terminal closeout is repeated idempotently;
7. a restored terminal checkpoint cannot resubmit denied work; and
8. all prior usage and provider evidence remains monotonic through closeout.

One installed-runtime fixture should reproduce the important shape of the Sarah
run without making paid provider calls.

## Bounded-ingestion implications

These closeout behaviors should be input-kind-neutral. An exact projected-graph
package and a bounded projected-graph package may produce different claim decks,
but they should use the same paid-action authority, negative-authorization,
terminal-outcome, checkpoint, and logging contracts unless a demonstrated semantic
reason requires otherwise.

The bounded claim deck should itself remain a distinct schema. Do not flatten
bounded evidence into the exact claim-deck schema merely to reuse authoring code.
Canonical bounded claims, conditional/evidence-only material, prerequisites,
root-owner evidence families, unavailable features, and inconclusive features need
explicit dispositions through extraction and selection.

## API-owned follow-up, not an SBE request

The API repository must separately:

- register one durable `worker_workspaces` row per execution job;
- perform terminal reconciliation of exact provider-less actions;
- retain failed-run checkpoints under an explicit retention policy;
- map spend denial to a more precise API failure classification; and
- ensure public status remains safely coarse while operator state preserves the
  detailed reason.

The current records do not block new runs because action authority is scoped to one
authoring run and no jobs or leases remain actionable. They should nevertheless be
reconciled through an implemented, tested terminal-closeout path rather than by
manual row edits. In particular, the successful run with a stranded authorization
proves that cleanup cannot be limited to failure handling.

SBE should provide the native evidence needed by those decisions but should not
take ownership of queues, leases, R2, database lifecycle, or scratch deletion.
