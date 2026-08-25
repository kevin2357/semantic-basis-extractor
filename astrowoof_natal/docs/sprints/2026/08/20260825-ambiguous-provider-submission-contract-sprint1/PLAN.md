# Ambiguous Provider Submission Contract — Saunter 1 Plan

Date: 2026-08-25  
Status: Scenic Waypoint 0 complete; paused at Waffle Checkpoint 0 for API review  
Working branch: `main`  
Trigger: API Sprint 45 and the frozen Vafle-hund/Zultan QA cohort

## Objective

Make SBE's external-authority v2 provider-create boundary precise enough for a
consumer to preserve native custody safely. A sealed public result must
distinguish:

1. a failure proven to have occurred before provider I/O became possible;
2. a create-entered condition for which provider acceptance cannot be disproven;
3. normal detached provider-pending work with durable provider identity;
4. exact replay; and
5. malformed or contradictory native/public evidence.

The correction must prevent duplicate paid work, keep provider I/O outside the
native single writer, preserve exact request/grant/action/binding lineage, and
give the API a closed result it can persist without reading private native
state, request payloads, logs, or workspace internals.

## Current boundary hypothesis to prove, not assume

The v2 dispatcher currently persists `CALL_ENTERED` before invoking the caller's
`create(action)` callback. The production CLI callback still performs local work:

- resolve the exact snapshot-bound request payload;
- verify the action/request digest join;
- read binding/model/output policy;
- construct the OpenAI transport;
- derive the deterministic local request key; and
- finally call `create_response_only()`.

The dispatcher catches every exception from that callback and conservatively
marks the action ambiguous. This is safe against duplicate provider work, but it
can misclassify a proven local/pre-provider failure as a provider submission
ambiguity. Scenic Waypoint 0 must identify the exact last point at which SBE can
prove no provider request was attempted and the exact first point after which it
cannot.

Classification must be based on explicit execution phases and durable facts,
not on an exception-class allowlist. An HTTP exception may prove that provider
I/O was entered; a payload-resolution exception does not.

## Frozen invariants

- No Vafle-hund, Zultan, Aster, or other retained QA workspace may be resumed,
  reconciled, retired, rewritten, or used as a mutable fixture.
- No real provider request, credential, spend authorization, or network access is
  permitted during implementation or qualification.
- Once SBE has crossed the durable provider-create boundary without recording a
  provider identity, the action is ambiguous and cannot become create-eligible.
- Absence of a provider ID does not prove absence of provider submission.
- Deterministic local request keys do not prove provider idempotency.
- Pre-provider refusal must be supported only where SBE can positively prove
  provider I/O did not occur.
- SBE owns native action state, create-phase evidence, snapshot/revision truth,
  provider identity, ambiguity, and the public native result.
- API owns admission, grants, reservations, worker scheduling, product state,
  capacity, operator workflow, and its durable consumption of SBE evidence.
- SBE results must not assert API-global capacity, reservation, or billing facts.
- API must not reconstruct a submission conclusion from missing IDs, logs, or
  subprocess exit codes.
- Logs/events explain decisions but never authorize mutation or retry.
- Existing initial-wave v1 behavior, Batch transport, spend policy, route
  topology, and provider reconciliation remain out of scope unless a regression
  proves this correction necessarily touches them.

## Proposed native execution phases

Scenic Waypoint 0 may refine the names, but the contract must preserve these
semantic boundaries:

| Phase | Permitted work | Provider I/O possible? | Failure meaning |
|---|---|---:|---|
| `native_revalidation` | Load/validate snapshot, intent, action, request, grant, binding, state, and cursor | No | Typed native/contract refusal |
| `request_materialization` | Resolve the unique prepared payload, verify digest, derive provider configuration and request metadata | No | Proven pre-provider refusal |
| `provider_call_fenced` | Under the writer, revalidate and durably record the exact action as entering provider create | Not yet, but next operation is provider I/O | Crash after checkpoint is ambiguous |
| `provider_call_in_progress` | Execute the one provider create outside the writer | Yes | Ambiguous unless a stronger provider guarantee proves otherwise |
| `identity_checkpoint` | Reacquire writer and durably bind the returned provider ID or persist ambiguity/conflict | Provider call complete | Provider-pending, conflict, or ambiguity |
| `detached` | Seal result/checkpoint for later reconciliation | No create permitted | Retrieval-only continuation |

The filesystem cannot make the provider request and native identity checkpoint
atomic. The public contract must state this irreducible gap explicitly.

## Candidate public outcome model

The final vocabulary is a Scenic Waypoint 1 contract decision. The design target
is a closed distinction equivalent to:

| Outcome class | Provider I/O assertion | Custody meaning | Create permitted afterward? |
|---|---|---|---:|
| pre-provider refusal | positively `false` | no provider custody created by this invocation | only through a new supported authority decision, never implicit replay |
| ambiguous submission | entered/unknown | retain native/API review authority; provider acceptance unresolved | No |
| detached provider pending | provider identity durable | retain provider reconciliation custody | No; retrieval only |
| exact replay | no new I/O | return the already sealed decision | No |
| invalid evidence | unknown/fail closed | retain for review | No |

Whether pre-provider refusal is a new outcome, a typed refusal result, or a
versioned enrichment of the command result must be decided against the current
schemas/readers and API adoption needs. It must not be encoded only as free text.

## Approved API contract direction

The API review before Scenic Waypoint 0 approved SBE-first implementation and
froze the following direction for the Scenic Waypoint 1 proposal:

- Publish a fresh closed command-result schema version.
- Add `pre_provider_refusal` as an explicit top-level outcome; do not encode it
  through CLI exit status or a separate side assessment.
- Replace the current provider-I/O boolean as the authoritative conclusion with
  a closed assertion equivalent to:
  - `not_attempted`;
  - `create_entered_unknown`; and
  - `provider_identity_durable`.
- Treat the API reservation/admission identity as an API-owned join from its
  durable record. SBE binds native request/grant/action evidence but never
  asserts API-global reservation truth.
- Keep every planned review checkpoint; API adoption begins only after a
  released, fixture-backed SBE contract exists.

The approved API disposition target is:

| Native result | API execution capacity | API authority/custody | Retry/create posture |
|---|---|---|---|
| `pre_provider_refusal` + `not_attempted` | release | release the action reservation only from exact validated proof; preserve grant/audit record | no implicit regrant or retry |
| `ambiguous_submission` + `create_entered_unknown` | release | retain ambiguity/review custody | prohibit provider create |
| `detached_provider_pending` + `provider_identity_durable` | release | retain ordinary retrieval-only custody | reconcile only |
| `exact_replay` | unchanged | unchanged | no new work |
| malformed/contradictory evidence | release according to API failure policy | preserve relevant authority for review | fail closed |

API should expose recognized ambiguity with a specific product/operational
classification such as `provider_submission_ambiguous_requires_review`, not as
generic blocked or artifact-integrity failure.

## Scenic Waypoints

### Scenic Waypoint 0 — Execution-boundary inventory and provider-free reproducer

Trace the actual external-authority v2 path end to end:

- request and inspection readers;
- aggregate grant and authorization-document validation;
- intent commit and durable state/snapshot publication;
- request-payload resolution;
- provider construction and transport configuration;
- provider call entry;
- exception mapping;
- provider-ID durability;
- result building, command wrapping, and CLI exit behavior;
- lifecycle/native-transition projection; and
- API Sprint 45's current accepted/refused result matrix.

Build a provider-free production-shaped fixture using supported SBE code. Inject
failures at every meaningful boundary, including:

- before payload lookup;
- no payload, duplicate payload, and digest mismatch;
- invalid local provider configuration;
- immediately before the provider transport is called;
- after the transport is entered but before it returns;
- invalid/missing returned provider ID;
- after return but before identity persistence;
- identity conflict; and
- after durable identity checkpoint.

Record, for each cell: state revision, snapshot digest, action state, intent
phase, provider-call count, provider identity, sealed/public result, CLI exit,
and whether any subsequent create is reachable.

Deliverables:

- `SLICE 0 - EXECUTION BOUNDARY INVENTORY AND TRUTH TABLE.md`
- provider-free reproducer tests
- explicit recommended ambiguity line
- proposed compatibility/versioning decision inputs

Waffle checkpoint 0 — owner and API review:

- the exact pre-provider/provider-entered boundary is demonstrated;
- the frozen QA cohort remains untouched;
- every truth-table classification follows evidence, not exception type; and
- no schema/runtime design is frozen before this review.

### Scenic Waypoint 1 — Closed contract, schemas, and sealed evidence

Freeze the public result model after Waffle Checkpoint 0.

Define or revise, as required:

- result schema identity/version;
- closed top-level outcomes;
- closed reason/cause vocabulary;
- execution-phase and provider-I/O assertions;
- custody/review disposition;
- replay semantics;
- contradiction/refusal precedence; and
- compatibility behavior for older result versions.

Successful or safely recognized results must bind at least:

- native run ID and logical workspace root;
- route family and provider mechanism;
- external-authority request and grant identities/digests;
- exact ordered action inventory;
- affected/ambiguous/provider-bound action IDs;
- complete public binding identity or joined binding digest for each relevant
  action;
- pre/post state revision as applicable;
- post-snapshot digest;
- intent/checkpoint identity;
- provider-I/O assertion;
- terminal/nonterminal custody conclusion; and
- result digest plus any sealed native result/receipt identity used by the
  supported reader.

The contract must make contradictions impossible or reject them semantically.
Examples include:

- pre-provider refusal with `provider_io_performed: true`;
- ambiguity without an exact ambiguous action inventory;
- detached provider-pending without durable provider identities;
- exact replay that advances revision or reports new I/O;
- mismatched request/grant/action/binding identities; and
- an ambiguous action presented as create-eligible.

Add strict Python validation independent of optional `jsonschema`, packaged JSON
Schema validation, mutation tests, fixture hashes, and public import/export smoke.

Deliverables:

- `AMBIGUOUS PROVIDER SUBMISSION CONTRACT PROPOSAL.md`
- packaged schemas and sanitized fixtures
- strict builders/readers/validators or a documented existing supported join
- API consumer decision table

Waffle checkpoint 1 — joint schema/authority freeze:

- API confirms it can persist every accepted outcome without private inference;
- SBE and API agree on capacity/custody/reservation implications;
- versioning and legacy behavior are explicit; and
- no execution-path implementation proceeds before approval.

### Scenic Waypoint 2 — Pre-provider preparation and durable call fence

Refactor the production external-authority v2 dispatch path so all deterministic
local work that can safely occur before ambiguity is completed before the native
provider-call fence.

Expected shape:

1. Under the single writer, re-read and validate current snapshot, intent,
   request/grant, ordered actions, bindings, state, cursor, and provider absence.
2. Outside provider I/O, materialize and validate the exact provider request and
   transport/configuration inputs without submitting it.
3. Reacquire the single writer, revalidate that the same checkpoint and action
   remain current, then durably publish the exact call-entered fence.
4. Release the writer for the one slow provider operation.
5. Reacquire it immediately to persist either the returned provider identity or
   the ambiguity/conflict conclusion.
6. Seal the public result only after the resulting snapshot validates.

The design must not hold the writer across network I/O. It must also avoid a
time-of-check/time-of-use hole between local preparation and provider call entry:
the second writer revalidation must bind the prepared material to the unchanged
native checkpoint before publishing the call fence.

Tests must prove:

- payload/preflight/configuration failures perform zero scripted creates and
  return the typed pre-provider classification;
- the workspace/result accurately records whether any mutation occurred;
- an injected failure after the durable fence is ambiguous;
- invalid provider return shape is ambiguous after call entry;
- a returned identity is persisted before any next member can dispatch;
- a crash after provider return but before identity checkpoint remains
  ambiguous;
- an ambiguous action cannot be dispatched by generic resume, constrained
  replay, or a newly supplied grant;
- exact replay performs zero provider calls and does not mutate; and
- a failing diagnostic sink changes no native/provider behavior.

Deliverables:

- corrected exact and bounded applicable interactive dispatch adapters
- shared implementation where it reduces route drift safely
- focused failure-injection and concurrency tests
- structured redacted boundary diagnostics

Waffle checkpoint 2 — SBE implementation review:

- the public contract and runtime behavior agree byte-for-byte;
- provider call cardinality is proven at every failure point;
- existing single-writer and snapshot invariants remain intact; and
- no initial-wave, Batch, or reconciliation regression is present.

### Scenic Waypoint 3 — Consumer surfaces and API handoff

Expose the completed contract through supported installed-package surfaces:

- root-level Python reader/validator exports;
- a provider-free read/validate/export CLI operation;
- closed sanitized fixtures for every accepted/refused outcome;
- precise CLI exit-code guidance without making exit code authoritative;
- redacted structured events and `✨🐶` text logging at classification and branch
  selection; and
- an API handoff describing persistence, scheduling, reservation, capacity,
  replay, and operator-review obligations.

The handoff must state explicitly:

- pre-provider refusal is not provider ambiguity;
- ambiguity retains the relevant API authority and is never an automatic retry;
- provider-pending work is reconciliation-only;
- exact replay cannot create new work;
- malformed evidence remains distinct from recognized ambiguity;
- logs are diagnostic only; and
- the frozen QA cohort is evidence, not a recovery target.

The published sanitized fixture set must include at least:

- payload/materialization failure before the fence;
- invalid local provider configuration before the fence;
- failure immediately after durable call entry;
- transport-entered failure;
- malformed returned provider identity;
- conflicting returned provider identity;
- normal detached provider-pending;
- exact replay; and
- malformed public or sealed evidence.

Deliverables:

- `AMBIGUOUS PROVIDER SUBMISSION API CONSUMER HANDOFF.md`
- public Python and CLI examples
- fixture manifest with canonical/file hashes
- API-shaped provider-free ingestion/replay qualification

Waffle checkpoint 3 — API fixture/adoption review:

- API validates and maps the packaged fixtures;
- recognized ambiguity no longer becomes generic artifact-integrity failure;
- repeated ingestion and scheduling remain idempotent;
- no ambiguous action becomes claimable for provider create; and
- operator diagnostics name the safe next authority without offering retry.

### Scenic Waypoint 4 — Installed-wheel and release qualification

Prepare a fresh immutable patch only after Waffle Checkpoint 3.

Qualification must include:

- focused contract, dispatch, lifecycle, native-transition, and CLI suites;
- exact/bounded applicable interactive routes;
- explicit confirmation that ordinary Batch and initial-wave behavior are
  unchanged or fail closed according to their existing contracts;
- the complete pre-provider/ambiguous/provider-pending/replay/invalid matrix;
- installed-wheel provider-free qualification through the advertised commands;
- fresh-process workspace restore and replay;
- package/schema/fixture discovery checks;
- privacy sentinel and credential/payload non-disclosure checks;
- `pip check` with exact dependency identities;
- deterministic double build;
- broad release regression suite;
- `git diff --check`; and
- explicit evidence that no frozen QA workspace, provider credential, network,
  or spend was accessed.

Deliverables:

- installed qualification receipt
- release candidate manifest and hashes
- release notes and consumer handoff links
- exact source commit versus release-evidence-lock commit

Waffle checkpoint 4 — final owner/API review:

- API confirms the candidate contract is adoptable;
- owner authorizes the version bump/tag/publication separately;
- immutable tag and publication occur only after that authorization; and
- any later recovery or fresh paid QA cohort requires its own explicit approval.

## Test strategy

### Lean development loop

- focused external-authority v2 execution and intent-fence tests;
- schema/semantic-validator mutations;
- provider-free scripted transport call-count assertions;
- exact/bounded interactive route tests;
- native lifecycle/result projection tests; and
- diff/format checks after each waypoint.

### Failure-injection matrix

Every meaningful boundary must record:

- whether provider I/O was possible and whether the scripted transport ran;
- pre/post run and snapshot identity;
- action and intent states;
- public outcome/reason;
- result/receipt publication behavior;
- replay behavior; and
- whether any seventh or duplicate create can occur.

### Release gate

The broad suite is reserved for Scenic Waypoint 4 after contract and consumer
review. Development waypoints should use the smallest sufficient suites and must
not repeatedly pay the full Windows line-ending/full-suite tax.

## Compatibility posture

- Prefer a fresh versioned public result contract if existing schema semantics
  cannot express pre-provider refusal without contradiction.
- Do not silently reinterpret historical `ambiguous_submission` artifacts as
  pre-provider failures; they lack the new proof.
- Older recognized ambiguity remains fail-closed and reviewable.
- API may adopt the new classification only for a pinned compatible SBE release
  and validated schema/fixture identity.
- No release may mutate or retag 0.4.22.

## Explicit questions for ze Zultan's review

1. Does API prefer pre-provider refusal as a new dispatch outcome, a typed
   command refusal, or a separate sealed assessment object?
2. Which API authority should be retained/released for each closed result class,
   especially a refusal after grant consumption but before provider I/O?
3. Does the proposed evidence set fully support API idempotency, reservation,
   capacity, and operator-review decisions?
4. Should recognized ambiguity have a more specific API product/job disposition
   than the current generic blocked/review state?
5. Is a new public result schema version preferred over an additive compatible
   revision, given the existing exact-key validators?
6. Are the review pauses correctly placed after boundary proof, schema freeze,
   runtime correction, and consumer fixtures?
7. Is any additional API-side fixture needed before installed-wheel release
   qualification?

## Completion criteria

The saunter is complete only when:

- pre-provider refusal and provider submission ambiguity are machine-distinct;
- the distinction is proven by explicit phase/call evidence;
- ambiguous actions cannot create again;
- public results remain snapshot/revision/request/grant/action/binding joined;
- API can ingest every supported outcome without private reconstruction;
- installed-wheel provider-free qualification covers the complete matrix;
- broad release evidence is green;
- frozen QA remained untouched; and
- any patch release was separately approved, tagged immutably, published, and
  remotely digest-verified.
