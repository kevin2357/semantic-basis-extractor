# External Authority v2 Execution Bridge — Sprint 1 Plan

Date: 2026-08-24
Status: complete; SBE 0.4.20 published and digest-verified

## Objective

Complete the deliberately missing executable half of temporal lifecycle v0.6.
A validated `astrowoof.external_authority_request.v2` must become executable only
through one supported constrained native continuation supplied with an exact,
closed API v2 grant and complete public authorization documents. It must never be
downgraded into v1 authority, reconstructed from private state, or passed through
generic resume.

The completed pair should support this lifecycle:

```text
validated v0.6 inspection
  -> stable external_authority_request.v2
  -> API-owned admission/reservation/custody decision
  -> exact external_authority_grant.v2
  -> SBE writer-fenced validation and durable dispatch intent
  -> provider I/O outside the writer
  -> durable provider identity or typed ambiguity
  -> provider-pending capacity release
  -> supported reconciliation only
  -> new checkpoint basis / next temporal decision
```

The sprint must also make “waiting for a compatible grant” a coherent quiescent
native decision so API workers do not consume attempts or retain capacity merely
by observing the same request again.

## Background and confirmed incident

A fresh QA cohort completed the six-member initial authoring create wave and the
subsequent retrieval-cap 4+2 provider reconciliation. Its next v0.6 decision correctly
reported `await_external_authority`, `spend_authorization_required`, and an
`astrowoof.external_authority_request.v2` reference.

The API can validate and persist that reference but no released SBE command can
consume it with a matching v2 grant. The API correctly refuses to synthesize a v1
grant or invoke generic resume. Its current inert handling nevertheless allows the
job to reclaim a slot on the retry cadence without provider work.

The retained QA cohort and all retained provider work are evidence only. Nothing
in this sprint authorizes resumption, retrieval, cancellation, or mutation of it.

## Ownership boundary

### SBE owns

- validated native workspace and checkpoint-basis truth;
- exact action inventory, order, route, mechanism, bindings, custody, and state;
- construction and validation of the v2 request;
- validation and native consumption of v2 grants and authorization documents;
- native single-writer mutation and durable pre-dispatch intent;
- provider-identity/ambiguity checkpointing;
- provider-pending classification and supported reconciliation; and
- typed native refusal, result, journal, snapshot, and receipt evidence.

### API owns

- global/cross-run spend authority, reservations, quotas, and circuit breakers;
- product entitlement and admission policy;
- worker lease, slot, attempt, and queue behavior;
- grant construction/persistence after API admission;
- PostgreSQL/R2 transactionality and authoritative account billing;
- deciding when to invoke the constrained command; and
- preventing slot/attempt churn while SBE truthfully awaits a grant.

Neither side may reconstruct the other's authority from logs, subprocess exit
codes, private workspace bytes, or provider identifiers.

## Frozen design principles

1. **The v2 request is reference-only.** Execution requires the exact request, its
   validated current v0.6 inspection/checkpoint basis, a v2 grant, and complete
   ordinary authorization documents.
2. **No v1/v2 inference.** Neither version can satisfy or be transformed into the
   other version's authority contract.
3. **All-or-none API admission.** The grant covers the complete exact ordered
   inventory before any native dispatch begins.
4. **Serialized mutation; slow I/O outside the writer.** The writer protects
   revalidation, authorization, and a durable intent checkpoint, then is released.
   There is no atomicity claim across provider I/O.
5. **Provider results remain reconciliation-owned.** Dispatch records only provider
   identity or ambiguity; it does not ingest editorial/provider results.
6. **Provider identity is the replay fence.** Deterministic local IDs do not prove
   provider idempotency. Identity-less interrupted submission is ambiguous.
7. **Quiescence is native/local only.** SBE does not assert API-global capacity,
   reservation, or admission state.
8. **No new public product state unless necessary.** Prefer existing closed states
   with richer typed reasons/results.

## Proposed slices

### Slice 0 — Contract, command, and lineage audit

Inventory v1 request/grant/constrained execution, v2 request/basis surfaces, and
every exact/bounded interactive/Batch path that can prepare, authorize, create,
retrieve, retry, polish, critic, candidate, or reconcile provider work. Trace the
actual fresh-QA 4+2 reconciliation into its v2 request and identify generic-resume
bypass risks and current awaiting-authority capacity semantics.

Produce a route/stage applicability matrix. Every cell is classified as:

- parity-supported by the new v2 command;
- served by the existing initial-wave v1 command and not applicable;
- reconciliation-only; or
- explicitly fail-closed/deferred.

Add a provider-free public-boundary reproduction of the missing-command condition
with zero provider calls.

Gate / 🧇🐶 review paws: API reviews request kind, complete-public-binding source,
ordering, applicability matrix, refusals, and command boundary before schema work.

### Slice 1 — Closed v2 grant and constrained command contract

Define and package:

- `astrowoof.external_authority_grant.v2` JSON Schema;
- a strict Python validator independent of optional `jsonschema`;
- canonical grant digest and closed grant/member vocabularies;
- public provider-free builder/readers;
- constrained-command request/result schemas and CLI argument contract; and
- typed refusals and exit behavior.

The grant binds the request digest/schema, native run and checkpoint-basis digest,
   request kind, validated route/mechanism, exact ordered action IDs, every
   authorization-document digest/reference, and API grant identity/issuer/time.
   The ordinary authorization documents are the single normative carrier of each
   complete public binding. SBE rederives each binding digest and joins it to the
   current inspection. The grant does not duplicate complete bindings. Any validity
   window must be explicitly meaningful, never incidental inspection time.

Fixtures cover valid ordinary actions, exact replay, cross-version misuse, stale
basis, wrong run/route/mechanism/kind/order/action/binding/document/grant, missing or
duplicate members, unsupported matrix cells, and privacy sentinels.

Gate / 🧇🐶 review paws: joint schema/ownership freeze before mutation code. API
confirms it can construct the grant without private SBE state or a database
transaction spanning SBE/provider execution.

### Slice 2 — Native single-writer revalidation and intent fence

Status: **complete; awaiting API review.**

Under exclusive native access:

1. restore the run at its stable logical root;
2. validate the complete workspace snapshot;
3. build a fresh v0.6 inspection;
4. join the request to the current checkpoint basis;
5. validate route, mechanism, request kind, ordered inventory, complete bindings,
   action state, provider evidence, consumption, custody, and requiredness;
6. validate the grant and all authorization documents;
7. apply all authorizations and mark every selected member with submission intent
   in one candidate state; and
8. publish one complete checkpoint binding the exact aggregate grant, exact selected
   inventory, all authorization consumption, and submission intent before provider
   I/O.

The checkpoint is the atomic native publication unit. A valid workspace proves
either no grant/intent was applied, or the complete grant+inventory+intent unit is
durable. Partial member authorization, authorization without intent, or intent
without the exact grant must fail snapshot/state validation and cannot be
reinterpreted by a later runtime.

Contradictions refuse before mutation/I/O. Provider-safety facts take precedence
over generic staleness when provider or ambiguity evidence newly appears.

Failure injection covers every boundary from writer acquisition through complete
intent snapshot publication and the instant before provider I/O.

Gate: stale/partial authority causes zero mutation, result publication, or provider
I/O; exact replay of committed intent never silently grants another create.

### Slice 3 — Dispatch, replay taxonomy, and quiescent waiting

Status: **complete; awaiting API review.**

Release the writer after intent and execute only SBE-selected provider work.
Reacquire native control for each returned provider identity or ambiguity. Provider
result ingestion remains reconciliation-only.

Freeze this replay model:

| Durable native evidence | Permitted behavior |
|---|---|
| Authorized and definitively unattempted | constrained dispatch may begin |
| Intent committed; call provably not entered | resume exact frozen intent |
| Provider ID durably recorded | no create; reconciliation only |
| Provider may have accepted; no durable ID | ambiguous; fail closed |
| Provider/consumption/identity conflict | review refusal; no I/O |
| Basis or inventory changed | stale refusal unless stronger safety reason applies |
| Same completed constrained request/result | exact idempotent replay |

No-grant v0.6 inspection must coherently report `await_external_authority`,
`spend_authorization_required`, a complete joined request, no local work ready, no
provider retrieval due, and no native local continuation requiring execution. It
must not assert consumer authority, API capacity, reservations, leases, or admission
facts. Repeated inspection creates no new native artifact. API separately maps this
native/local decision to blocked waiting and manages its own authority and capacity.

Scripted tests prove one create per action, immediate identity durability, no
duplicate after crash/restore, no provider I/O under writer, fast responses still
reconciled separately, exact replay, ambiguity/refusal behavior, and diagnostic
sink failure isolation.

Gate / 🧇🐶 review paws: API reviews command/result and quiescent fixtures before
cross-route qualification.

### Slice 4 — Applicable-route and lifecycle qualification

Status: **complete; awaiting API review.**

Exercise every Slice 0 parity-supported cell. Initial-wave v1 remains unchanged;
reconciliation-only/deferred cells refuse rather than falling into generic resume.

The holistic provider-free scenario must use real supported boundaries:

1. prepare a real six-member initial wave;
2. apply existing constrained initial-wave authority;
3. create six scripted operations once;
4. detach and restore from a complete snapshot;
5. reconcile SBE-selected four, then two;
6. reach a real v0.6 authority request;
7. read the v2 request through public code;
8. persist grant/documents outside the workspace;
9. invoke constrained v2 execution in a fresh runtime;
10. prove identity durability and provider-pending release;
11. invoke supported reconciliation; and
12. prove a new checkpoint basis and valid next decision.

Also cover wrong adapters, reordering, provider-bound/ambiguous actions, optional
skip versus required denial, Batch authority where applicable, fresh-worker replay,
and generic resume making zero calls while a v2 grant is required.

Gate / 🧇🐶 review paws: API reviews route traces, fixtures, refusals, and the final
supported/deferred matrix before installed-wheel packaging.

### Slice 5 — Public handoff, installed-wheel qualification, and release preparation

Status: **complete; installed-wheel and deterministic-build evidence recorded,
awaiting final API/owner release review.**

Package schemas/catalog entries, Python builders/readers/validators/executor, a
provider-free CLI with closed receipt, sanitized fixtures/mutations, events and
redaction inventory, API invocation examples, compatibility notes, retained-run
guidance, and exact paired adoption/deployment order.

Installed qualification uses a real sanitized workspace and real public runtime
boundaries—not a miniature model—and accepts no API key, network endpoint,
production input, provider payload, or retained workspace.

Release checks include affected suites, Python 3.11 installed-wheel smoke, holistic
4+2 qualification, no-provider/spend proof, privacy scan, deterministic hashes,
`pip check`, schema/catalog checks, `git diff --check`, and final API review.

Gate / 🧇🐶 review paws: explicit owner/API approval before version bump, tag,
publication, or retained paid-run operation.

## Refusal categories to freeze in Slice 1

- unsupported version/route/mechanism;
- request unavailable/not current;
- stale checkpoint basis;
- run/root/snapshot mismatch;
- inventory/order/binding mismatch;
- provider identity/evidence or consumption appeared;
- ambiguous submission;
- action state/custody/requiredness mismatch;
- partial/duplicate/unknown authorization member;
- grant/request/document mismatch;
- explicit grant validity failure if adopted;
- generic resume forbidden / compatible grant required; and
- exact replay or reconciliation-only disposition.

Refusals are closed and machine-readable. Logs/events may explain but never
authorize.

## Testing strategy

The minimum matrix covers exact/bounded × interactive/Batch applicability; initial
wave versus ordinary actions; reachable retry/polish/critic/candidate stages;
required versus optional actions; fresh through terminal action states; replay and
new grants; stale/change mutations; missing/extra/duplicate documents; concurrent
resumers; every intent/identity crash boundary; sink failure; stable-path fresh
restore; incomplete snapshots; real 4+2 reconciliation; no duplicate I/O; no
generic-resume escape; no I/O under writer; and privacy sentinels across all public
artifacts and diagnostics.

## Deliverables

- authority/command/route applicability matrix;
- closed v2 grant schema and mutations;
- strict public Python surface;
- constrained provider-capable Python/CLI boundary;
- writer-fence and failure-injection evidence;
- quiescent awaiting-grant contract;
- holistic provider-free fixture and installed receipt;
- API handoff and examples;
- compatibility/retained-run guidance; and
- sprint log, evidence, and release recommendation.

## Explicitly deferred

- API queue/lease/retry/reservation implementation;
- global spend policy, quotas, entitlements, or billing;
- unsupported provider-idempotency claims;
- operation on suspended/retained paid QA;
- bounded Batch support merely because a matrix cell exists;
- unrelated editorial/prompt/scoring/state redesign; and
- release without explicit authorization.
