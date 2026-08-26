# Post-Fan-In Retry Matrix Contract — Sprint 1

Date: 2026-08-25
Status: Slices 0–5 complete; paused for final owner/API review before release work
Starting release: SBE 0.4.24
Expected release: fresh immutable patch version if runtime or packaged-contract changes are required

## Objective

Close the public lifecycle-proof gap after initial six-pass fan-in. An API worker
must be able to distinguish concrete, presently executable native work from a
quiescent self-loop without reading `run.json`, logs, response IDs, or private
workspace artifacts.

The sprint will publish provider-free, installed-wheel evidence for the complete
creative-retry matrix and enforce this invariant:

```text
ordinary_resume + no retained provider work
  requires a non-empty, snapshot-bound public local-work inventory
```

## Current understanding

The Crumpet cohort successfully crossed the qualified initial-wave boundary, then
entered an unqualified post-fan-in route:

```text
six initial actions reported
  -> creative retry #1 provider-bound
  -> creative retry #2 prepared/authorized but not provider-bound
  -> ordinary_resume with no provider custody
  -> repeated quiescent local cycles
```

The API followed SBE's supported branch and did not invent provider authority.
Current SBE inspection derives `local_dependencies` largely from broad run status.
`_execution_branch()` treats any such dependency as sufficient evidence for
`ordinary_resume`. The contract therefore proves that a generic continuation
reason exists, but not necessarily that a concrete native operation is executable
against the inspected checkpoint.

Slice 0 must determine whether this is the complete cause or whether retry state
transition/dispatch logic contributes an additional defect. No production behavior
will change before that characterization is reviewed.

## Authority and safety invariants

1. SBE remains authoritative for native state, exact next native operation,
   provider custody, retry lineage, snapshot identity, and terminal disposition.
2. API remains authoritative for job scheduling, leases, global spend/admission,
   reservations, persistence, and product policy.
3. A run status is not by itself proof that local work is executable.
4. `ordinary_resume` may be selected only from a nonempty closed inventory of
   concrete local operations valid for the exact inspection checkpoint.
5. Provider custody outranks local work and new authority under the already
   released precedence rules.
6. A prepared paid action requiring external authority must not be represented as
   ordinary local work.
7. A durable call-entry boundary without a provider identity remains ambiguity and
   review custody; it is never replayable create work.
8. Provider-bound work remains retrieval-only. The API never selects members or
   reconstructs SBE commands from IDs.
9. Retry exhaustion and unjoinable lineage produce closed terminal/refusal evidence,
   not an empty local loop or invented retry.
10. Public inventory and qualification artifacts contain no prompt, payload,
    authorization document, protected subject data, or credentials.
11. Crumpet remains frozen throughout development and qualification.

## Proposed public contract

### Local-work inventory

The next lifecycle inspection version should own a new closed
`local_work_inventory` projection. Lifecycle v0.5 remains immutable and readable
for historical consumers; it must not be widened. Temporal lifecycle should commit
that exact projection into the immutable
checkpoint basis. It must not be reconstructed in, or vary as part of, the
time-relative temporal decision.

Proposed top-level shape:

```json
{
  "schema_version": "astrowoof.local_work_inventory.v1",
  "run_id": "native-run-id",
  "state_revision": 42,
  "snapshot_sha256": "...",
  "ordering_semantics": "sbe_selected_execution_order",
  "operations": [
    {
      "operation_id": "local_...",
      "kind": "provider_result_fan_in",
      "route_family": "exact_natal",
      "stage": "creative_retry",
      "source_action_ids": ["paid_..."],
      "reason_code": "provider_evidence_ingestion_required"
    }
  ],
  "inventory_sha256": "..."
}
```

The exact fields and vocabularies are Slice 1 decisions. At minimum, every member
must bind the native run/checkpoint, one closed operation kind, its route/stage,
and the exact native action lineage needed to prove executability. It is evidence
for the supported run-level `ordinary_resume` command; it is not permission for
the API to invoke internal functions or choose an operation.

### Branch requirements

| Selected command | Required local-work shape |
| --- | --- |
| `ordinary_resume` | nonempty valid inventory; branch remains run-level |
| `provider_reconciliation_cycle` | empty local-work inventory; provider custody owns continuation |
| `await_external_authority` | empty local-work inventory; exact authority request owns continuation |
| `none` terminal/refusal/review | empty inventory unless a reviewed future contract explicitly says otherwise |

Any contradictory combination must fail strict Python validation even when the
optional `jsonschema` dependency is absent.

## Slice 0 — Characterize the real post-fan-in state machine

- Build provider-free production-shaped exact and bounded fixtures from supported
  runtime code through initial six-pass fan-in.
- Drive creative retry #1 through preparation, constrained authority, scripted
  create, provider-pending, retrieval, and deterministic ingestion.
- Drive the decision that either accepts retry #1, prepares retry #2, or exhausts
  retry policy.
- Reproduce the Crumpet structural shape without accessing Crumpet:
  retry #1 provider history, retry #2 prepared/authorized without provider identity,
  zero retained provider dependencies, and selected `ordinary_resume`.
- Record the actual durable fields and exact code path responsible for every branch.
- Determine whether an authorized-but-unsubmitted retry is:
  - valid constrained dispatch work;
  - a state requiring fresh external authority;
  - a pre-submit refusal/recovery posture; or
  - ambiguity/review.
- Inventory every currently emitted `provider_pending_lifecycle_qualification.v1`
  identifier/schema/fixture/reader/CLI reference and classify immutable legacy v1
  versus substantively v2-but-mislabeled material.

Gate / voof-paws 1: owner and API review the characterization, concrete local-work
operation vocabulary, and v1/v2 inventory before schema freeze.

Result: complete. See `SLICE 0 - POST-FAN-IN CHARACTERIZATION AND CONTRACT
INVENTORY.md`. Both routes reproduce completed retry evidence masking the next
prepared retry. A providerless authority refusal can republish a new revision while
returning the same semantic ordinary-resume decision. Schema work remains paused.

## Slice 1 — Freeze the retry and local-work contracts

- Define a closed `local_work_inventory.v1` schema and strict Python validator.
- Freeze operation kinds for only work SBE can prove executable, expected initially:
  - provider-result ingestion/fan-in;
  - deterministic retry evaluation/preparation;
  - final assembly/QA;
  - delivery construction.
- Decide whether retry evaluation and retry preparation are one atomic local
  operation or two separately checkpointed operations based on Slice 0 evidence.
- Bind every member to route, stage, action lineage, state revision, and snapshot.
- Give every member a basis-independent semantic `operation_key`; bind the
  basis-specific invocation separately as `operation_id`.
- Require a successor that remains on `ordinary_resume` to seal at least one prior
  semantic key in `consumed_operation_keys`. A different typed disposition may
  advance without such a claim.
- Make `consumed_operation_keys` cumulative and append-only across the checkpoint
  lineage, and forbid any consumed semantic key from being advertised as current
  work again.
- Define deterministic member ordering and inventory digest rules.
- Tighten lifecycle v0.5 branch semantics and JSON Schema conditionals.
- Carry the immutable inventory into temporal v0.6 checkpoint-basis canonicalization
  and keep it outside the temporal decision.
- Define the complete post-fan-in outcome matrix:
  - no retry;
  - retry authority required;
  - retry provider-pending due/not-due;
  - retry result requires deterministic local fan-in;
  - second retry authority required;
  - exhaustion/terminal;
  - lineage ambiguity/refusal;
  - authorized/no-provider and call-entered/no-provider boundary cases.
- Publish sanitized proposed fixtures for API review.

Gate / voof-paws 2: API approves exact schemas, vocabularies, joins, refusal
precedence, and scheduling interpretation before runtime behavior changes.

Result: complete as a contract-only proposal. The new identities are
`astrowoof.local_work_inventory.v1` and
`astrowoof.authoring_lifecycle_inspection.v0.7`; released v0.5/v0.6 remain
unchanged. See `SLICE 1 - LOCAL WORK AND LIFECYCLE V0.7 CONTRACT PROPOSAL.md`.
Runtime selection still emits the released contracts and has not changed.
The API-requested no-op republish correction is incorporated: snapshot/revision
changes cannot rename semantic work, and continued local work requires sealed
consumption evidence. The consumed-key history is cumulative, so a semantic
operation cannot reappear after falling out of the immediate predecessor.

## Slice 2 — Enforce truthful local execution selection

- Replace status-only local readiness with construction of the closed concrete
  inventory from validated native state.
- Permit `ordinary_resume` only when that inventory is nonempty and executable.
- Ensure each ordinary resume cycle either:
  - consumes at least one advertised local operation and creates a new checkpoint;
  - advances to another truthful branch; or
  - returns a typed refusal/review outcome.
- Never return the same eligible `ordinary_resume` decision for the same basis
  after a successful no-op invocation.
- Correct the retry #1 → retry #2 transition according to the frozen matrix.
- Preserve provider-custody precedence, bounded 4+2 retrieval selection, v2
  authority fences, ambiguity posture, and optional-stage policy.
- Emit redacted, failure-isolated diagnostics for inventory construction, branch
  selection, operation consumption, and refusal reason.

Gate: focused source tests prove progress-or-refusal and zero provider calls for
all characterization and mutation cases.

Result: complete. The runtime now exposes `inspect_post_fan_in_lifecycle()` and
`commit_local_work_progress()` as the native v0.7 selection/progress boundary.
It constructs concrete inventory from validated provider/dependency evidence,
persists cumulative consumption only after underlying native truth advances, and
refuses a no-op without changing run or snapshot bytes. Exact and bounded retry
shapes are covered; provider-pending custody and ambiguity retain precedence.
The public lifecycle CLI exposes this as `inspect-local-work`; legacy `inspect` and
`inspect-temporal` fail closed rather than advertise unversioned local execution.
Normal exact and bounded resume checkpoint paths invoke progress commitment only
after their real native operation advances or reaches a spend-boundary detach.
Slice 3 exercises this boundary through the complete route/outcome matrix.

## Slice 3 — Build the complete provider-free retry matrix

Publish provider-free fixtures and assertions for:

| Case | Required proof |
| --- | --- |
| A — no retry | deterministic next route or terminal outcome; no create authority |
| B — retry #1 needed | one exact `await_external_authority` action |
| C — retry #1 provider-bound | due/not-due reconciliation, exact custody inventory |
| D — retry #1 completed; retry #2 needed | local fan-in consumes its advertised operation, then one exact retry-#2 authority request |
| E — retry exhausted | typed terminal/refusal, empty provider/local/authority inventories |
| F — unjoinable lineage | typed review/refusal; no invented recovery |
| G — authorized, no provider identity | exact frozen disposition; never generic no-op resume |
| H — call entered, no provider identity | ambiguity/review; no create or replay |

For every cell assert command, eligibility, reason, action order, capacity, custody,
local inventory, time gate, terminal/quiescence projection, request/refusal join,
snapshot identity, and provider-create/retrieval counts.

Include exact and bounded Natal where the production retry topology applies.
Interactive routes are required. Batch routes must be parity-supported or explicitly
fail closed/deferred; no simulated miniature may stand in for production code.

Gate / voof-paws 3: API reviews the fixture matrix and confirms its disposition
oracle can consume it without private-state inference.

Result: complete and paused at voof-paws 3. The sanitized eight-cell matrix covers
exact and bounded interactive routes, due/not-due reconciliation, concrete local
fan-in, retry authority, exhaustion, unjoinable lineage, native AUTHORIZED without
provider identity, and call-entry ambiguity. Batch remains governed by its existing
round contracts and fails closed where concrete local work cannot be proven. See
`SLICE 3 - PROVIDER-FREE RETRY MATRIX AND API HANDOFF.md`.

Post-review integration correction: the original direct-helper-only implementation
was not release-capable. Production integration is now present: the public CLI reads
v0.7 explicitly, legacy public readers fail closed for concrete local work, and the
ordinary exact/bounded runtime checkpoints seal real progress. A public CLI plus
normal semantic-closure resume regression proves retry #1 fan-in reaches retry #2
authority without provider creation.

## Slice 4 — Public installed-wheel qualification and v2 naming correction

- Extend or supersede the installed provider-pending qualification through the
  full post-fan-in retry matrix using real public/native runtime boundaries and a
  scripted provider.
- Reopen the workspace in fresh runtime contexts between create, reconciliation,
  local fan-in, next authority, and terminal/refusal checkpoints.
- Prove no duplicate create/retrieval and no quiescent ordinary-resume loop.
- Publish a closed concise receipt, schema, packaged reader, and provider-free CLI.
- If the v1 inventory confirms the current receipt is substantively incomplete or
  mislabeled, publish `astrowoof.provider_pending_lifecycle_qualification.v2` as a
  new contract. Preserve the immutable v1 reader/schema/fixture and document that
  v1 proves only initial fan-out/fan-in through first authority selection.
- Update emitting code, packaged schema/fixtures, CLI, exports, and handoff
  atomically. Do not rename unrelated legacy v1 contracts.
- Add privacy-sentinel and malformed/extra-key/unsupported-version tests.

Gate: installed isolated wheel passes the public qualification with no credentials,
network, provider work, spend, or retained-run access.

Result: source implementation complete. V1 remains unchanged. The new closed v2
receipt runs v1 and then proves exact/bounded v0.7 local-work selection, durable
consumption, fresh-process reopening, retry-2 authority selection, and exact replay
refusal. The qualification also found and closed an already-consumed-operation
replay edge in `commit_local_work_progress()`. See `SLICE 4 - INSTALLED V2
QUALIFICATION AND API HANDOFF.md`.

## Slice 5 — Compatibility, handoff, and release qualification

- Document exact API mapping for every matrix outcome and the rule that the API
  invokes only SBE's selected run-level command.
- Document v1/v2 compatibility and fail-closed behavior for consumers that lack
  local-work inventory support.
- Confirm lifecycle v0.5 and temporal v0.6 compatibility or explicitly justify a
  fresh schema version if strict closed-world shapes cannot safely evolve in place.
- Run focused lifecycle, temporal, reconciliation, v2 authority, exact/bounded
  retry, privacy, snapshot, installed-wheel, and broad release suites.
- Build twice from one committed source identity with fixed `SOURCE_DATE_EPOCH` and
  prove byte-identical artifacts.
- Record source, dependency, resource, fixture, wheel, and receipt hashes.
- Pause for owner/API final review before any tag or publication.

Gate / voof-paws 4: final consumer review and explicit release authorization.

Result: compatibility and handoff complete. Lifecycle v0.5 and temporal v0.6
remain readable and unchanged, but fail closed when concrete post-fan-in local work
requires v0.7. The isolated 0.4.24 source wheel passed the public v2 qualification.
Release versioning, deterministic final builds, tag, and publication remain gated
on final owner/API review.

## Failure-injection and negative matrix

- stale state revision or snapshot digest;
- empty, duplicated, reordered, malformed, or wrong-route local inventory;
- status claims local work but no concrete operation can be built;
- concrete operation disappears before ordinary resume obtains the writer;
- interruption before and after local-operation checkpoint;
- retry #1 evidence joined to retry #2 action incorrectly;
- authorized action without durable intent;
- `CALL_ENTERED` without provider identity;
- provider identity or completion evidence appears between inspection and resume;
- exhausted retry policy with another prepared action;
- malformed/unjoinable retry lineage;
- Batch member/round authority confusion;
- exact/bounded route mismatch;
- event sink failure and protected-data sentinel leakage.

Every negative cell must prove either byte-identical authoritative state or one
coherent fail-closed checkpoint. It must also prove zero unauthorized create and
no duplicate retrieval.

## Compatibility posture

- No new API-global scheduling, capacity, reservation, or product-policy fact is
  introduced.
- Existing lifecycle state names should remain unchanged if the corrected branch
  can be expressed by stricter evidence.
- Because lifecycle inspection v0.5 is closed-world, Slice 1 must decide explicitly
  whether adding `local_work_inventory` requires v0.6 rather than silently widening
  v0.5. Temporal lifecycle v0.6 must likewise be versioned if its exact public shape
  cannot accept the new immutable basis member compatibly.
- Existing v1 qualification evidence remains historically true and readable; it
  must not be overwritten to imply post-fan-in coverage it never proved.

## Exit criteria

- Crumpet's structural shape is reproducible provider-free and its cause is proven.
- `ordinary_resume` always carries a nonempty, snapshot-bound concrete local-work
  inventory.
- Repeating a supported ordinary resume cannot produce a quiescent self-loop on an
  unchanged checkpoint.
- The complete retry matrix is available through closed packaged fixtures and an
  installed-wheel qualification receipt.
- API can route every outcome without inspecting private SBE state.
- No duplicate provider create/retrieval is possible across the tested boundaries.
- Naming/version compatibility is explicit and no blanket v1 rename occurs.
- Full release evidence is reproducible and provider-free.
