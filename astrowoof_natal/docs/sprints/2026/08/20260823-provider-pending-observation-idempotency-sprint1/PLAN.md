# Provider-Pending Observation Idempotency Sprint 1 Plan

Date: 2026-08-23
Status: complete; SBE 0.4.16 tagged, published, and independently verified
Mode: provider-free reproduction and contract work first

## Purpose

Define and implement the SBE side of the temporal lifecycle contract exposed by
two fresh QA runs. SBE validly performed one six-member initial-wave create
cycle per run. A later API claim failed because a clock-later inspection for the
same native snapshot no longer matched a previously stored full inspection JSON.

SBE must make explicit which inspection evidence is immutable native checkpoint
basis and which is a clock-relative scheduling decision. Actual provider facts
cannot change under the same checkpoint: they require supported retrieval and a
new durable native checkpoint. The API must be able to persist and validate
that distinction without reconstructing SBE private state.

## Boundaries

- Do not resume, reconcile, retrieve, cancel, or recreate provider actions for
  the retained QA runs.
- Do not make generic resume provider-capable merely to accommodate an old run.
- Preserve exact external-authority request/grant fences, single-writer
  validation, and typed fail-closed handling of ambiguous provider lineage.
- Keep `inspect_lifecycle()` provider-free, read-only, and incapable of creating
  a native observation journal merely because time was inspected.
- Keep the trusted ordering clock API-owned. SBE must not substitute its wall
  clock or accept an untrusted caller's time as authoritative sequencing input.
- Keep API persistence of decision-relevant temporal history bounded by an
  explicit retention policy; harmless repeated polling is not automatically an
  immortal authoritative record.
- Preserve SBE ownership of the bounded due-action subset; the API invokes a
  run-level supported command and never selects reconciliation members.

## Proposed public model

Prefer a fresh strict lifecycle contract version rather than teaching consumers
an undocumented list of mutable v0.5 paths. The candidate structure has two
explicitly hashed parts:

### Immutable checkpoint basis

- native run ID, operator state revision, snapshot SHA-256, logical root, and
  snapshot/inventory validation;
- native route and provider mechanism;
- local dependencies, terminal/quiescence facts, action inventory, provider
  operation identities, bindings/digests, custody schedule including
  `resume_not_before`, and authority facts;
- an exact canonical `checkpoint_basis_sha256`.

### Temporal scheduling decision

- caller-supplied `observed_at`;
- checkpoint-basis digest;
- capacity disposition, due/not-due eligibility, selected supported command,
  SBE-selected bounded action subset, `not_before`, and closed reason code;
- an exact canonical `temporal_decision_sha256`.

`capacity_disposition` is SBE's native/local lifecycle scheduling conclusion
only. It does not encode API-global admission, worker-slot availability,
reservations, account limits, circuit breakers, entitlements, or spend capacity.
Those facts are not reproducible from `(checkpoint basis, observed_at)` and
remain exclusively API-owned.

`observed_at` must use one exact canonical normalized-UTC representation. The
API supplies the trusted value used for persisted sequencing. SBE deterministically
derives the same decision bytes for an exact `(checkpoint basis, observed_at)`
pair, but does not claim that its own wall clock establishes API ordering.

Exact basis plus exact `observed_at` must reproduce exact decision bytes. A
later observation may make scheduled reconciliation due; it may not alter the
provider identity, action inventory, binding, route, or authority represented by
the checkpoint basis.

The API owns persistence and current-observation selection. It retains
append-only validated decisions that actually drive durable routing or explain a
deferral/refusal, subject to a defined retention policy; it need not preserve
every identical polling observation forever. The authoritative current view is
the latest valid decision for one basis under API-owned monotonic ordering. SBE
may provide a pure sequence validator for a prior/current pair, but inspection
itself remains nonmutating and does not attest to the API's clock.

Repeated identical due decisions are idempotent evidence, not proof that only
one worker will act. API lease/custody controls remain responsible for preventing
duplicate command invocation.

## Slices

### Slice 0 — Incident reproduction and temporal field classification

Status: complete; review gate pending.

Build a provider-free fixture that obtains two valid lifecycle inspections from
one unchanged native snapshot: `t0 < resume_not_before` and
`t1 >= resume_not_before`. Prove no provider I/O or workspace mutation occurs.
Publish a field-by-field classification: immutable checkpoint basis,
clock-relative decision, or prohibited change.

Define the candidate transition matrix:

- exact basis + exact time is byte-identical replay;
- same basis may progress from reconciliation not-due to due;
- observation time cannot regress in an API-owned sequence;
- provider IDs, action inventory/order, route, binding, custody schedule, and
  authority cannot change under one basis digest;
- actual provider status/result/usage requires a new checkpoint; and
- contradictory or impossible evolution is a typed refusal.

Also classify repeated `await_external_authority` inspections and the effect of
`observed_at` on exact request/grant digests. The preferred correction is for an
authority request to bind the immutable basis and exact ordered action inventory,
not incidental inspection time. Reinspection of one basis should reproduce one
request digest. Any future time-sensitive authority rule must use an explicit
validity/expiry field rather than implicit `observed_at` churn.

Gate: SBE/API review of the field classification, proposed hashes, timestamp
ownership, and transition matrix before schema implementation.

### Slice 1 — Versioned checkpoint/temporal-decision public contract

Status: complete; review gate pending.

Publish the smallest strict public schema/API needed to expose the immutable
checkpoint basis and its temporal scheduling decision. Prefer lifecycle
inspection v0.6 if adding the explicit sections/top-level digests would violate
v0.5's closed-world shape.

Define canonical digest construction, pure single-document validation, and pure
prior/current sequence validation. Include closed refusals for changed route,
binding, provider identity, action inventory, authority, clock regression,
impossible eligibility regression, or checkpoint mismatch. Keep sensitive
provider payloads and workspace internals out of the artifact.

Lifecycle v0.5 and older inputs fail closed at this boundary. They are not
silently reinterpreted as the split contract.

Gate: joint schema, digest, refusal-vocabulary, and compatibility approval.

### Slice 2 — Provider-free native fixture and replay invariants

Status: complete.

Use scripted provider transport to prove: initial create intent, pending
release, not-due inspection, due inspection, the real reconciliation boundary,
new durable provider evidence/new checkpoint, exact repeated observation, and
contradictory/reordered/regressive refusal. Verify no duplicate provider create
or retrieval occurs.

The fixture must not represent provider result availability as changing before
the supported reconciliation operation observes and persists it.

### Slice 3 — Cross-route compatibility and release support

Status: complete; API review gate pending.

Assess ordinary, initial-wave, bounded, Batch, retry, polish, critic, and
candidate routes. Add supported reader/validator/CLI fixtures and release tests
for the public contract. Every route must either prove parity or fail closed
with an explicit compatibility classification; no legacy inspection is silently
reinterpreted.

Gate: four-route and optional-stage matrix, installed-wheel provider-free smoke,
privacy scan, and API fixture review.

### Slice 4 — Consumer handoff and release-pair qualification

Status: complete; final review gate pending.

Publish exact checkpoint/decision examples, ordering rules, API persistence
recommendations, v0.5 compatibility behavior, external-authority digest behavior,
and operator diagnostics. Qualify the installed wheel across the actual
subprocess boundary with no provider credentials or network.

Gate: one exact SBE/API release pair rejects incompatible behavior before paid
QA is authorized.

### Final review — API consumption contract

Review exact public fields, schema versioning, digest construction, and examples
with the API implementation before release. No API may infer temporal behavior
from status-name strings or raw workspace state.

Retained-run disposition remains separate. Read-only inspection may be proposed
after release-pair qualification, but any provider retrieval, native mutation,
cancellation, or resubmission requires explicit owner authorization.

## Testing and gating strategy

Minimum provider-free cases:

- same checkpoint/same time exact replay;
- same checkpoint/not-due then due;
- backward time and due-to-not-due regression refusal;
- changed snapshot without a new basis digest refusal;
- changed provider ID, action inventory/order, route, binding, custody schedule,
  or external authority refusal;
- SBE-selected four-of-six due subset with API unable to choose members;
- real reconciliation creates a new checkpoint and no seventh provider create;
- exact and bounded interactive parity;
- exact and bounded Batch parity;
- retry, polish, critic, and candidate parity or explicit fail-closed support;
- repeated external-authority inspection and stale exact grant refusal;
- stable external-authority request digest across later observations of one
  unchanged basis;
- repeated identical due decisions with lease/custody—not inspection
  uniqueness—protecting command invocation;
- event/log sink failure isolation; and
- protected subject/prompt/credential sentinel absence.

No Slice may use a retained paid QA workspace as a fixture. No test may accept
credentials, submit provider work, retrieve a retained operation, or mutate API
capacity/spend authority.
