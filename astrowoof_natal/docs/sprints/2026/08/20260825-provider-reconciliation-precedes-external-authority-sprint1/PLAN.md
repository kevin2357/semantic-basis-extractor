# Provider Reconciliation Precedes External Authority — Sprint 1 Plan

Date: 2026-08-25  
Status: Slice 6 complete; final API/owner tag-publication approval pending

## Objective

Correct the native next-command ordering defect that can expose or wait for a new
external-authority grant while the same workspace still owns provider-created work
that must be reconciled first.

> Existing provider custody is exhausted through SBE-selected retrieval and
> deterministic local fan-in before SBE exposes authority for any later uncreated
> provider action.

This is a lifecycle-selection correction. It must not redesign provider transport,
spend policy, API scheduling, external-authority bindings, or the frozen QA cohort.

## Current working hypothesis

Current lifecycle selection already gives **due** provider reconciliation priority
over a `PREPARED` action. The suspect gap is the rest of the provider lifecycle:

- a provider-created action whose `resume_not_before` is still in the future is
  classified as scheduled custody;
- completed provider evidence may require deterministic local fan-in; and
- `PREPARED` is currently considered before scheduled custody and completed
  evidence.

That means a mixed workspace can select `await_external_authority` even though it
must first release until an existing provider action is due, retrieve it, or consume
already-reconciled evidence locally. Slice 0 must prove the exact predicate and
public call path before implementation.

## Ownership boundary

SBE owns validated native snapshot/provider lineage, custody and due-time
classification, next-command and bounded-subset selection, retrieval-only
reconciliation, deterministic fan-in, and exact external-authority request
publication after earlier work is exhausted.

API owns worker claims/leases/capacity, trusted scheduling time, global spend
authority, request/grant persistence, API provider/accounting records, and deciding
when to invoke the SBE-selected run-level command. SBE capacity fields remain native
scheduling conclusions and never assert API-global capacity or reservations.

## Frozen invariants

1. Reconciliation is retrieval-only; it cannot authorize, submit, retry, deny, or
   create provider work.
2. A prepared external-authority action never outranks retained provider custody
   from an earlier logical operation.
3. SBE—not API—selects the bounded due subset.
4. Provider identity, binding, inventory, or lineage contradictions fail closed
   before retrieval or authority publication.
5. Historical initial-wave evidence never permits a fresh wave.
6. Provider I/O remains outside the writer; revalidation and native mutation remain
   serialized under it.
7. Unchanged not-due observation performs no provider I/O and mints no new native
   result.
8. Retrieval/fan-in creates a new checkpoint basis; time-only not-due → due remains
   a temporal decision over one unchanged basis.
9. Exact/bounded and Response/Batch identities remain explicit and are never
   silently converted.
10. External-authority v1 initial-wave and v2 ordinary-action bindings remain
    unchanged unless Slice 0 proves a contract gap.
11. Nonblocking critic custody may coexist with publishable delivery, but is not
    permission to create unrelated new provider work.
12. Logs/events explain selection but are never authority.
13. The next SBE artifact pins `semantic-projection-core==0.11.1`; bounded runtime
    admission and release metadata must agree with that exact compatibility identity.

## Proposed precedence contract

Slice 0 will validate or refine this ladder:

1. invalid snapshot, writer/provider ambiguity, binding/inventory contradiction,
   or unjoinable lineage → typed review/refusal;
2. unsupported retained timing/mechanism → typed unsupported/refusal;
3. due provider custody → eligible `provider_reconciliation_cycle`;
4. completed provider evidence requiring fan-in → eligible `ordinary_resume`;
5. known provider custody not yet due → ineligible
   `provider_reconciliation_cycle` until SBE’s `not_before`;
6. other proven local executable work → eligible `ordinary_resume`;
7. only then, valid uncreated prepared work → `await_external_authority`; and
8. otherwise terminal/no-continuation.

Item 6 precedes item 7 only when the local dependency can determine, alter, or
refuse the exact next paid-action inventory. Unrelated optional local work must not
starve safe authority publication.

## Frozen API review decisions

- Retained provider custody always outranks new external authority: due retrieval,
  coherent not-due scheduling, and required completed-provider fan-in.
- Other local work outranks authority only when it can determine, alter, or refuse
  the exact next paid-action inventory.
- Prefer strict in-place v0.5/v0.6 hardening. Version only if existing closed fields
  cannot express a consumer-distinguishable corrected result.
- Nonblocking critic custody never blocks already-publishable delivery, but by
  default suppresses unrelated later optional authority until settled. Any future
  authority-independent coexistence needs an explicit contract.
- Preserve existing reason vocabularies where sufficient; add redacted diagnostics
  rather than a public state for observability alone.
- Frozen-cohort recovery is separate and inaccessible to patch qualification.

## Slice plan

### Slice 0 — Public-path reproduction and selector audit

**Status: complete.** See
`results/SLICE 0 - PUBLIC SELECTOR AUDIT AND PRECEDENCE CONTRACT.md`.

Build a sanitized provider-free fixture matching the observed mixed state:

- one six-member initial wave;
- mixed reported/completed and provider-created members;
- one later `PREPARED` action capable of yielding an authority request;
- complete stable-path snapshot and valid bindings; and
- canonical observation times covering not-due and due.

Exercise real lifecycle v0.5 and temporal v0.6 public inspection. Record capacity,
custody, branch, request/refusal, checkpoint basis, temporal decision, selected
subset, `not_before`, and byte-level nonmutation.

Freeze truth-table cells for provider custody due/not-due/completed, prepared-only,
each custody state mixed with prepared work, ambiguity/integrity plus prepared,
unjoinable lineage plus prepared, ordinary local continuation, and terminal/no-work
controls. Audit every selector and exact/bounded route adapter involved.

The reproducer must additionally prove:

- a mixed not-due state returns nonmutating reconciliation scheduling/deferment,
  never generic external-authority waiting;
- completed evidence produces no new authority request before fan-in emits its new
  checkpoint basis;
- time-only not-due observation leaves the exact next-action inventory/request
  digest unchanged; and
- only newly recorded fan-in evidence/new checkpoint basis may change that digest.

**Gate / voof-paw 1:** API review of the public reproduction, exact defective
predicate, precedence table, v0.5/v0.6 impact, and local-continuation decision. No
runtime patch before this gate.

### Slice 1 — Contract freeze and semantic validation

**Status: complete.** See
`results/SLICE 1 - PRECEDENCE CONTRACT AND SEMANTIC VALIDATION.md`.

Prefer tightening lifecycle v0.5 and temporal v0.6 in place if the defect is an
already-contradictory combination. Add no public state/command unless unavoidable.

Strict semantic validation must reject:

- `await_external_authority` with reconciliable provider custody;
- authority request/inventory while due or scheduled custody precedes it;
- due reconciliation with consumer-selected/reordered members;
- not-due reconciliation without coherent custody schedule/`not_before`;
- fan-in that omits required completed-provider evidence; and
- request/refusal coexistence or route/mechanism/binding mismatch.

Freeze redacted diagnostic predicates for due/not-due reconciliation precedence,
fan-in precedence, custody-integrity refusal, and authority selection after provider
exhaustion. Typed events carry counts/digests only—never payloads, bindings,
credentials, response text, or subject data.

**Gate / voof-paw 2:** API approval of precedence, compatibility/versioning,
semantic predicates, and diagnostic vocabulary.

### Slice 2 — Reconciliation-priority implementation

**Status: complete.** Shared selector order corrected; focused qualification green.

Implement one shared route-neutral classification rule where feasible. It must
classify the complete retained provider inventory before prepared authority,
prioritize due reconciliation, prioritize not-due detach scheduling, prioritize
required completed-evidence fan-in, preserve the four-action retrieval cap, keep
not-due inspection nonmutating, preserve time-stable authority/basis digests, and
fail closed before I/O/publication on contradiction.

Add failure-isolated structured diagnostics and ✨🐶 logs for safe inventory counts,
due/selected counts, prepared count/deferment, command/reason, and refusal category.

**Gate:** focused tests prove selection-only change with zero provider creates,
authorization consumption, or unrelated lifecycle mutation.

### Slice 3 — Multi-cycle 4+2 and fresh-worker recovery

**Status: complete.** Provider-free installed qualification now carries a later
prepared action through custody, 4+2 retrieval, fan-in, and authority exposure.

Prove one six-Response run plus a later prepared action:

1. first due cycle selects/retrieves the first four;
2. restore in a fresh worker;
3. remaining two still outrank prepared authority, due or not-due;
4. second reconciliation retrieves only those two;
5. restore again;
6. deterministic fan-in creates no seventh provider operation;
7. only then may the later authority request appear; and
8. replay duplicates neither retrieval nor request revision.

Inject interruption after retrieval/before checkpoint, interruption between cycles,
stale time, provider identity/binding/inventory mutation, malformed first and
fifth/sixth members, failing event/log sinks, and competing resumers. Whole-cycle
integrity refusal must perform zero GETs.

**Gate:** one run remains the custody unit; provider pending holds no worker lease;
no API-global fact is asserted.

### Slice 4 — Four-route and stage parity

**Status: complete.** Exact/bounded Response and Batch custody cells plus supported
interactive stage matrix are green; deferred Batch optional stages remain refused.

Exercise exact/bounded × interactive/Batch across initial authoring, creative
retry, polish, critic, candidate, restored workspaces, partial provider failure,
usage unavailable, and nonblocking critic custody after delivery.

Batch stays one paid/provider authority per round with member evidence beneath it;
interactive waves retain six identities. Explicitly fail closed any unsupported
cell rather than implying parity.

**Gate:** no fresh wave, seventh create, duplicate GET, changed Batch cardinality,
invented usage/cost, or authority mutation.

### Slice 5 — Public installed-wheel qualification and API handoff

**Status: complete.** Installed candidate and exact SPC 0.11.1 qualification pass;
consumer handoff published for API review.

Add or extend one self-contained provider-free installed-wheel command using real
workspace/snapshot/lifecycle readers, real command selection/reconciliation entry
points, scripted transport, and fresh runtime restoration.

Its closed receipt must prove mixed custody outranks authority, not-due is
nonmutating, due 4+2 selection is SBE-owned, all-six fan-in precedes later
authority, contradiction yields zero retrieval, POST/create/submit/retry is
unreachable, replay is idempotent, and privacy sentinels are absent.

Publish exact v0.5/v0.6 field/value, scheduling, command, refusal, compatibility,
and retained-workspace guidance.

**Gate / voof-paw 3:** API validates packaged fixtures/receipt and confirms worker
routing requires no inference from logs, private `run.json`, provider IDs, or
dashboard state.

### Slice 6 — Closeout and patch release preparation

**Status: complete.** 0.4.22 deterministic artifact and installed/broad-suite
qualification are recorded; tag/publication remain unperformed.

- Run focused lifecycle/temporal/reconciliation/authority suites.
- Run installed qualification and generic release smoke.
- Run the broad suite once at the final gate; narrow reruns first if anything fails.
- Build twice at one epoch and compare exact wheel bytes.
- Record source/artifact/resource/compatibility/privacy/zero-provider evidence.
- Qualify against exact installed SPC 0.11.1 and record it in the fresh release
  manifest; published SBE 0.4.21 remains truthfully recorded against SPC 0.11.0.
- Recommend a fresh immutable patch; never alter 0.4.21.

**Gate / voof-paw 4:** final API review and explicit owner authorization before
tag/publication. Frozen-cohort recovery remains separately authorized operations.

## Testing matrix

- Selection: due/not-due/completed/ambiguous/unsupported custody × prepared/local/
  terminal states, replay, later trusted time, and new checkpoint basis.
- Routes: exact/bounded × interactive/Batch; initial/retry/polish/critic/candidate;
  success/pending/failure/conflict/partial usage.
- Safety: snapshot/path validation, clock regression, malformed first/fifth/sixth
  member, identity/binding mutation, retrieval/checkpoint/fan-in interruption,
  sink failure, and competing writers.
- Negative provider assertions: POST/create/submit/retry = 0; GETs equal only the
  SBE-selected scripted subset; authority consumption = 0; fresh-wave creation = 0;
  frozen QA access/mutation = 0.

## Evidence deliverables

- Public-path reproducer and selector truth table;
- precedence/compatibility contract and mutation corpus;
- 4+2 fresh-worker/failure-injection trace;
- four-route/stage parity matrix;
- installed-wheel qualification schema/receipt/fixture manifest;
- API consumer handoff and privacy/provider-I/O inventory;
- release compatibility/limitations/manifest; and
- continuously updated `LOG.md` and `EVIDENCE.md`.

## Explicitly deferred

- frozen QA recovery or mutation;
- API queue/lease/reservation/database work;
- cost calibration;
- new retries/idempotency claims;
- increased retrieval concurrency;
- new transport/Batch topology;
- product publication policy; and
- automatic repair of contradictory historical workspaces.

## Slice 0 review answers

The API review answered all five planning questions: causal local work only;
in-place v0.5/v0.6 hardening preferred; delivery-independent but custody-first
critic handling; current reasons plus typed diagnostics; and separately authorized
frozen-cohort recovery. Slice 0 should return with evidence, not reopen these
decisions absent contradictory native findings.
