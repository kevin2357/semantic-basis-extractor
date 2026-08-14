# API Request Reconciliation

```yaml
status: planning-input
date: 2026-08-14
baseline_sbe_release: astrowoof-natal-authoring 0.3.0
target_sprint: 20260812-bounded-btime-ingestion-sprint1
```

## Purpose

This document reconciles the three API-agent inputs retained in this sprint
directory against the authoring lifecycle and structured-event work subsequently
published in SBE 0.3.0. Its purpose is to prevent historical requests from silently
reopening completed work or expanding bounded ingestion beyond its semantic and
consumer boundary.

Classifications used below are:

- **satisfied**: released SBE 0.3.0 provides the requested common behavior;
- **bounded qualification**: the common behavior exists and requires bounded-route
  integration or regression evidence, not a new contract;
- **new bounded work**: the request concerns semantics or observations that do not
  exist until bounded ingestion is implemented;
- **optional**: advisory improvement accepted only when low-risk and independently
  justified by SBE design;
- **API-owned**: explicitly outside SBE authority; and
- **deferred**: intentionally outside the first invariant-only bounded product.

## Source documents

- `API Agent Implementation Requests.md`
- `API Agent Logging Requests.md`
- `API Agent Thoughts for SBE Ingestion of Bounded Birthtime Graphs.md`

The first two contain concrete consumer requests. The third is advisory. Per
product-owner direction, items from the advisory document are optional unless they
are required for the accepted bounded contract or are low-risk improvements that
SBE independently judges valuable.

## Implementation-request reconciliation

### Request 1: negative authorization and terminal closeout

**Classification:** satisfied; bounded qualification required.

SBE 0.3.0 provides supported provider-less denial for exact `PREPARED` and
`AUTHORIZED` actions, immutable action binding, closed denial reasons, monotonic
history, typed refusals after provider identity or ambiguity, fresh snapshots, and
idempotent closeout. These are authoring-run lifecycle operations rather than
exact-chart semantic operations.

Bounded work must reuse the same prepare/authorize/execute and lifecycle surfaces.
Qualification must prove that a bounded run can be denied, closed out, restored,
and inspected without resubmission or loss of bounded selection/provenance. No new
bounded denial vocabulary is planned absent evidence that bounded semantics require
one.

### Request 2: multiple outstanding paid-action ordering

**Classification:** satisfied; bounded regression required.

SBE 0.3.0 action inventory separates deterministic presentation order from
execution dependency and reports necessity, independence, supersession, blocking,
eligibility, provider identity/evidence, and exact ineligibility reasons. Exact
multi-action targeting and provider-less denial are covered by released tests.

Bounded authoring must use the same action inventory and single-writer mutation
rules. The bounded sprint will add only an integration regression showing that
route-specific semantic input does not alter paid-action ordering, release
eligibility, or commitment accounting.

### Request 3: machine-readable terminal outcome and failure taxonomy

**Classification:** satisfied; bounded qualification required.

SBE 0.3.0 lifecycle inspection and closeout expose terminal/resumable/review state,
last completed work, deck and delivery existence, publishability, provider and
local continuation, action counts/states, quiescence, snapshot identity, and typed
failure/review reasons. Consumers do not need to parse exception text.

Bounded integration must populate the same common outcome envelope while preserving
the distinct bounded claim/final-card contract identity. A bounded semantic-basis
failure such as `insufficient_invariant_basis` may require one new closed reason,
but does not justify a parallel terminal-state system.

### Request 4: quiescence and local-dependency summary

**Classification:** satisfied; bounded qualification required.

SBE 0.3.0 reports typed local dependencies, workspace quiescence, logical restore
path, complete snapshot revision/digest, provider identity state, and native
terminal/resumable disposition. API scratch registration, cleanup authorization,
R2 custody, and database rows remain outside SBE.

The bounded sprint must verify that its additional disposition, candidate, claim,
and authoring artifacts are included in authoritative snapshots and that every
bounded provider/spend boundary remains safely restorable.

### Request 5: spend-denial and closeout qualification

**Classification:** common cases satisfied; bounded provider-free fixture required.

Released SBE coverage includes first-action denial, authorized/unconsumed denial,
provider identity and consumption races, ambiguous identity-less submission,
multi-action targeting, idempotent denial, restart-safe closeout, monotonic accepted
delivery, and installed provider-free lifecycle smoke.

The bounded sprint will not repeat the entire lifecycle test matrix under a second
input kind. It will retain focused bounded integration cases proving:

- bounded selected evidence remains monotonic through denial and closeout;
- terminal restore cannot resubmit denied work;
- provider identity or ambiguous submission still fails closed; and
- the installed bounded fixture exercises common lifecycle commands without a paid
  provider call.

## Structured-logging reconciliation

### Event envelope, transport, authority, and redaction

**Classification:** satisfied.

SBE 0.3.0 packages `sbe.execution_event.v1`, a closed event/payload catalog,
allow-listed structured fields, deterministic envelopes, JSONL/stdout adapters,
sink-failure isolation, recursive protected-field rejection, and the invariant that
events never authorize or determine native execution.

Bounded work must extend the existing catalog rather than create another event
schema.

### Common provider, authorization, retry, QA, checkpoint, and terminal events

**Classification:** satisfied; bounded route wiring required.

SBE 0.3.0 emits typed events around provider preparation, authorization,
submission, durable identity, waiting/completion, denial, closeout, and representative
authoring lifecycle transitions. The bounded route must travel through these same
emitters and preserve the same run/action correlation.

### Bounded input and admission events

**Classification:** new bounded work.

Add event/catalog coverage for:

- bounded contract and exact four-context validation;
- shared source-artifact and proof identity;
- capability, limitation, and feature-disposition summaries;
- invariant object/relationship and evidence-family counts;
- admission rejection with closed safe reasons; and
- exact-versus-bounded route identity.

No event may include full graphs, evidence records, birth datetimes, interval
endpoints, coordinates, location evidence, names, or protected paths.

### Bounded extraction and selection events

**Classification:** new bounded work.

Add compact events for:

- invariant admission and candidate-family construction;
- root-owner/evidence-family collapse;
- configuration synthesis;
- foundational policy identity;
- selected counts and editorial tiers;
- exclusions by closed disposition/reason;
- exactly-fifty validation or insufficient-invariant-basis failure; and
- bounded claim-deck, disposition-report, and authoring-packet digests.

Counts are operational descriptions, never confidence, probability, source
strength, or independent evidentiary weight.

### Bounded event privacy and installed qualification

**Classification:** new bounded qualification.

Use a sanitized bounded fixture that seeds protected birth facts, source paths, and
large evidence shapes, then prove those values do not enter events. Truncation,
loss, duplication, sink failure, and replay must not affect bounded native state.

## Advisory bounded-ingestion reconciliation

The API agent's `Thoughts` document is useful design guidance rather than an
acceptance checklist.

### Accepted as necessary to the product contract

- distinct bounded input, claim-deck, and final-card contracts;
- no midpoint, noon-reference, majority-duration, or representative chart;
- invariant-only authored material in the initial release;
- preservation of source artifact, proof scope, prerequisites, capabilities,
  limitations, evidence families, and dispositions;
- strict exact four-context admission with opaque source identity;
- root-owner/evidence-family anti-inflation;
- explicit dependency closure for invariant syntheses; and
- fail-closed mixed-source, mixed-contract, mixed-context, or exact/bounded input.

### Accepted as low-risk and useful

- a separate private bounded disposition report;
- closed exclusion reasons and family-level selection audit;
- compact admission/selection summaries for orchestration;
- minimized provider-visible bounded subject/evidence view; and
- deterministic reorder and family-duplication regressions.

### Optional and evidence-gated

- detailed UI-oriented uncertainty summaries beyond the private disposition report;
- advanced marginal-coverage diagnostics not required to explain selection;
- additional synthesized configuration families beyond those needed to handle the
  demonstrated topology safely; and
- reader-facing display recommendations beyond stable editorial tiers.

Optional items may enter only when they are low-risk, deterministic, fully tested,
and do not delay the bounded acceptance boundary.

### Deferred

- authored conditional or alternative uncertainty narratives;
- probability, frequency, rectification, or most-likely interpretations;
- bounded Synastry, bounded Transit, or bounded temporal combinations;
- Quick/Complete product redesign;
- broad exact-Natal scoring redesign beyond the isolated angle-policy experiment;
  and
- frontend page design or public uncertainty messaging.

## API-owned boundary retained

The bounded sprint does not take ownership of:

- queue claims, attempts, leases, fencing authority, or job scheduling;
- transactional spend reservations across runs, account quotas, or circuit
  breakers;
- PostgreSQL persistence or API public-status mapping;
- worker scratch registration, deletion authority, R2 custody, or retention;
- product entitlement, publication authority, or billing reconciliation; or
- frontend presentation and user-input validation.

SBE supplies native semantic, lifecycle, disposition, quiescence, and provenance
evidence required by those owners. It does not mutate or supersede their authority.

## Planning conclusion

The historical API requests do not require another lifecycle sprint inside bounded
ingestion. The bounded implementation must reuse SBE 0.3.0's released lifecycle and
event contracts, add bounded admission/selection semantics and events, and qualify
the shared operations with one provider-free installed fixture. Everything else is
already satisfied, optional, deferred, or API-owned.

## Slice 9 delivery reconciliation

The candidate delivers the required separate bounded contracts, strict admission,
invariant-only exact-fifty selection, anti-inflation, private disposition evidence,
provider-minimized authoring, shared lifecycle/spend/snapshot behavior, bounded
events, installed CLI, schemas, provenance, consumer handoff, and exact pins.

The advisory event list was implemented at bounded route/admission/basis/selection/
compilation boundaries and supplemented by the shared lifecycle/provider/spend
events. More granular diagnostic events remain optional because native state and
artifacts—not event delivery—are authoritative.

API-owned queue/lease/fencing, cross-run reservation, quota, circuit-breaker,
PostgreSQL, billing, entitlement, worker-scratch, publication, and frontend-policy
responsibilities remain unchanged. The API-agent review packet requests explicit
confirmation of those seams. The final-candidate installed Linux rerun passes, and
the API consumer subsequently accepted all requested seams and recommended release.
