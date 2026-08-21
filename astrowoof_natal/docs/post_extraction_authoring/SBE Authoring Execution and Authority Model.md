# SBE Authoring Execution and Authority Model

Status: canonical conceptual model for SBE 0.4.14 and compatible consumers

## Purpose

This document explains the complete authoring process model in one place. It is the
orientation layer above the versioned schemas and route-specific handoffs. When a
precise field, vocabulary, digest, or command conflicts with this overview, the
packaged contract and its specialist handoff are authoritative.

The central separation is:

```text
semantic work       provider work       local capacity       consumer authority
what SBE must do    what OpenAI has      whether a worker     what the API must
next                accepted or owes     must run now         retain or decide
```

These are related facts, not interchangeable states. In particular:

- provider-pending work does not require a worker to remain occupied;
- releasing local capacity does not release provider custody or API authority;
- a provider operation becoming terminal does not prove its cost is settled;
- a native action being prepared does not authorize provider creation; and
- absence of a provider ID does not prove the provider accepted nothing.

## Ownership boundary

SBE is authoritative for:

- native run, action, binding, wave, pass, attempt, and Batch-round identity;
- semantic/editorial progression and required versus optional work;
- provider-visible request construction and disclosure minimization;
- native spend commitments and the immutable per-run policy;
- provider submission intent, returned provider identities, ambiguity, and
  reconciliation evidence;
- workspace integrity, snapshots, journals, native results, and receipts;
- lifecycle classification and the supported next native command; and
- delivery, review, budget, policy-stop, ambiguity, and closeout outcomes.

The AstroWoof API is authoritative for:

- product jobs/readings and public product state;
- worker leases, queueing, capacity, and scheduling later than SBE's lower bound;
- transactional cross-run reservations and account-wide quotas;
- global circuit breakers, product entitlements, and external policy decisions;
- PostgreSQL/R2 persistence and transactionality; and
- authoritative billing reconciliation and reservation release.

Neither side should reconstruct the other's authority from logs, subprocess exit
codes, private files, or coincidental absence of work.

## The route-neutral lifecycle

The common process is:

```text
prepare native work
  → expose snapshot-bound next action
  → obtain external authority or denial
  → commit native pre-submit intent
  → perform provider create
  → persist returned identity or ambiguity
  → detach while provider work is pending
  → reconcile a bounded due subset
  → perform deterministic local continuation
  → prepare retry/optional work or finish
  → deliver, review, exhaust budget, stop by policy, or retain ambiguity
```

Every arrow that crosses a durable boundary must be resumable from native evidence.
Every provider-capable arrow requires explicit authority. No general `resume`
operation is permission to invent or repeat provider work.

## Work units and authority cardinality

| Work unit | Native shape | Provider shape | API authority shape |
|---|---|---|---|
| Interactive initial wave | Six independent ordered pass actions | Six Responses creates | One all-or-none decision over six exact ordinary authorizations |
| Batch initial wave | Six logical members | One Batch round | One paid action and one reservation for the round |
| Creative retry | One failed pass/attempt | One Response unless Batch retry policy groups it | One independently bound action |
| Polish | One optional deck-level stage | One Response | One independently bound action |
| Qualitative critic | One optional deck-level stage | One Response | One independently bound action |
| Qualitative candidate | One optional finding/candidate action | One Response | One independently bound action |

The six interactive initial passes are editorially independent and submitted
concurrently, but remain one deck-level native run. They are not six API jobs or six
workspaces. Batch changes transport and reservation cardinality; it does not change
the six-pass editorial topology.

Creative retries are classified separately from initial authoring. Polish, critic,
and candidate work remain distinct optional stages controlled by the immutable
generation profile.

## Prepared work is not provider permission

A prepared paid action contains a complete immutable binding, including at least:

- native run and profile identity;
- prepared state revision;
- stage, route, pass/attempt where applicable;
- exact request digest;
- model, service level, and maximum output;
- maximum monetary commitment; and
- versioned price book.

The binding says exactly what SBE is ready to do. It does not say that the API has
reserved global authority or that SBE may contact the provider.

Lifecycle inspection v0.5 exposes one of two mutually exclusive objects when
external authority is the next boundary:

- `external_authority_request`: a complete snapshot-bound request; or
- `external_authority_refusal`: a closed native reason why no safe request exists.

Consumers must use this public projection. They must not derive an authorization
request from `run.json`, packets, response IDs, logs, or their own product record.

## Initial-wave admission fence

The interactive initial wave has the strongest aggregate fence because partial API
authorization could otherwise begin only part of the intended six-pass wave.

The safe sequence is:

1. SBE prepares exactly six actions and one joinable wave without provider work.
2. Lifecycle inspection v0.5 publishes `initial_wave_admission`, its semantic member
   order, six complete bindings, and the exact native observation.
3. The API transactionally grants or declines the exact entire six-action set.
4. A positive decision supplies six ordinary authorization documents plus one
   aggregate grant bound to the request, ordered members, bindings, snapshot, wave,
   profile, and API decision identity.
5. Under native single-writer control, SBE re-reads and revalidates the workspace,
   request, grant, and all documents.
6. SBE authorizes all six actions, marks all six `SUBMITTING`, and commits one
   durable constrained-submission intent before provider I/O.
7. SBE releases the writer while the six provider creates run concurrently.
8. SBE reacquires native control to persist each returned identity or ambiguity
   outcome.
9. Once the six outcomes are durable, SBE publishes a coherent detached checkpoint.

A generic resume against a stored wave awaiting authority, authorized, or
submitting cannot become create permission. A retained wave with provider IDs is
reconciliation-only. Historical evidence that cannot prove one exact reusable wave
is `initial_wave_lineage_unjoinable`, not permission to manufacture a replacement.

## Ordinary later actions

Creative retry, polish, critic, candidate, and other independently prepared work use
`ordinary_action_set`. Actions are presented in deterministic lexical `action_id`
order; that order is canonical presentation, not an instruction to execute them
serially.

Each ordinary authorization must match the complete native binding and document
digest/reference. A prepared action is request-eligible only while it remains:

- exactly `PREPARED`;
- providerless;
- unconsumed and unreported;
- binding-identical to the public request; and
- part of the same validated snapshot observation.

Later actions do not inherit initial-wave aggregate semantics. They retain
independent authority unless a route-specific Batch round intentionally groups
them. Existing providerless-denial operations remain the supported negative
decision path.

## Provider submission and the irreducible atomicity gap

SBE can make native intent durable before contacting the provider and can persist a
returned provider ID immediately afterward. It cannot atomically transact its
filesystem with the provider's service.

Therefore three outcomes are materially different:

| Evidence | Meaning | Permitted continuation |
|---|---|---|
| No provider attempt occurred | Definitely unsubmitted | May submit only under current exact authority |
| Durable provider ID exists | Provider-bound | Retrieve/reconcile only; never create again |
| Provider may have accepted but no durable ID exists | Ambiguous submission | Fail closed for review; never assume retry is safe |

Deterministic local keys are useful correlation evidence. They are not proof of
provider idempotency and never erase the ambiguous-submission state.

## Detach, scheduling, and reconciliation

After provider identities are durable and no local executable work remains, SBE
classifies the run as provider-pending and releases local execution capacity until
`resume_not_before`.

The API may schedule later, but must not poll earlier. If inspected before the lower
bound, the result is nonmutating and selects no early retrieval. When due, lifecycle
inspection selects the run-level provider-reconciliation command.

SBE—not the API—chooses the bounded due subset. Interactive reconciliation currently
retrieves at most four due Responses per cycle. The API must not construct a command
from action IDs or choose preferred members. A six-member wave can therefore settle
in a 4+2 sequence while requiring no duplicate creates.

Reconciliation performs only retrieval of known provider operations. It consumes no
new create authority. After each bounded retrieval cycle, SBE persists provider
facts, exhausts immediately runnable deterministic local work, and then either:

- detaches again with a new lower bound;
- exposes a new external-authority request;
- reaches delivery/review; or
- reaches a terminal budget, policy, or ambiguity outcome.

## Capacity, custody, and consumer authority

Lifecycle inspection reports these independently:

| Projection | Question answered |
|---|---|
| Execution capacity | Does native work need a worker now, or may the lease be released? |
| Provider custody | Does a known provider operation still require retrieval or retained identity custody? |
| Consumer authority | Which API reservations/financial authorities must remain retained? |
| Execution branch | Which supported native command, if any, may run next? |

A terminal Batch whose files were retrieved may require no further provider polling
while still retaining consumer authority because usage is unavailable or output is
under review. Conversely, a delivery-complete reading may be publishable while a
nonblocking critic remains provider-pending; its action authority remains retained
without blocking reader delivery.

## Spend states and semantic budget

Dollar spend is separate from SBE's fifty-claim semantic selection budget.

The spend ledger distinguishes:

- committed maximum exposure before submission;
- provider-reported or locally estimated usage after work;
- unavailable usage requiring billing reconciliation; and
- no provider work consumed.

Polling an existing provider operation creates no new SBE commitment. Batch member
usage settles beneath one round-level paid action; it does not multiply API global
reservations. Partial member usage cannot masquerade as complete round settlement or
zero cost.

SBE enforces its immutable per-run ceiling. The API separately owns authoritative
cross-run reservations, quotas, circuit breakers, entitlements, and billing.

## Denial, optional work, and terminalization

Providerless denial is allowed only when provider identity, consumption, reported
cost, and ambiguity are absent and the exact binding remains eligible.

- An optional stage configured to skip remains a skip and does not fail the run.
- A required action denied for external spend authority reaches
  `BUDGET_EXHAUSTED` with a distinct external cause.
- A required action denied by product policy or cancellation reaches
  `POLICY_STOPPED`.
- Once `reservation_unavailable` is submitted as an accepted denial, it is final;
  temporary scheduling delay must instead retain the action and authority.

Atomic batch providerless denial validates every member before mutating any member.
Its result distinguishes the full ordered `denied_action_ids` from the narrower
`required_action_ids` that caused terminalization.

## Native persistence and publication

The complete native workspace is the durable recovery unit. It must be restored at
its stable logical absolute path, with every authoritative snapshot member present
and unchanged. Incomplete or arbitrarily modified snapshots cannot resume.

Native state, journal records, result artifacts, full snapshots, and immutable
publication receipts form an atomic publication protocol: no literal multi-file
filesystem transaction is claimed. A public result is valid only when its bounded
journal range, checkpoint basis, result hash, complete snapshot, and receipt all
validate together. Interrupted partial publication fails closed and may be repaired
only through the supported provenance-bound orphan-repair path.

The API ingests a validated native result transactionally into API-owned state.
HTTP status endpoints read persisted API authority; they do not execute SBE or read
a live worker filesystem.

## Machine-distinguishable outcomes

Consumers must preserve distinctions among:

- awaiting external authority;
- provider-pending but not due;
- provider reconciliation due;
- ordinary local continuation;
- warning or retryable transport observation;
- native review required;
- hard budget exhaustion;
- policy stop;
- ambiguous provider submission;
- final QA failure or review;
- delivery complete; and
- closed non-delivery terminal outcome.

Do not flatten these into a generic pending/failed flag. The lifecycle inspection,
native transition result, snapshot, journal range, and receipt are authoritative;
structured logs and execution events are diagnostic and failure-isolated.

## Operator and maintainer rules

When changing this system:

1. Identify which authority owns each fact before changing a state or command.
2. Freeze the public crossing and failure outcomes before concurrent API/SBE work.
3. Test every seam around authorization, durable intent, provider return, identity
   persistence, snapshot publication, and result ingestion.
4. Prove both success and refusal make the expected number of provider creates.
5. Qualify fresh-process restore, not merely in-memory replay.
6. Exercise the installed wheel and supported commands, not only source helpers.
7. Keep logs redacted and useful, but never promote them into authority.
8. Release a fresh immutable version for consumer-contract changes.
9. Deploy and attest each runtime, register a fresh immutable generation profile,
   and prove a newly created run binds the intended released identities.

## Normative and detailed references

- `Authoring Lifecycle Consumer Handoff.md`: lifecycle commands, capacity, custody,
  denial, terminalization, and API sequence.
- `Initial Authoring Wave Consumer Handoff.md`: six-pass topology, wave artifacts,
  route parity, crash outcomes, and external-authority continuation.
- `Spend Authorization Consumer Handoff.md`: binding, commitment, authorization,
  ledger, and ownership rules.
- `Provider Spend Enforcement.md`: detailed durable spend accounting and provider
  atomicity limitations.
- `Native Worker Change Playbook.md`: native and joint development process.
- Sprint 20260820 `EXTERNAL AUTHORITY REQUEST AND GRANT CONTRACT PROPOSAL.md`:
  lifecycle v0.5 request/grant/refusal schemas and semantic joins.
- Sprint 20260820 `EXTERNAL AUTHORITY CONSUMER HANDOFF.md`: exact consumer sequence,
  qualification command, and compatibility guidance.
- The packaged contract catalog: exact supported schema identities and resources.

## Compact mental model

```text
SBE says what exact native action exists and what may safely happen next.
API says whether product-wide authority is granted and when a worker may run.
Provider IDs turn creation into retrieval-only custody.
Snapshots and receipts make native truth portable.
Neither absence, logs, nor generic resume confer authority.
```
