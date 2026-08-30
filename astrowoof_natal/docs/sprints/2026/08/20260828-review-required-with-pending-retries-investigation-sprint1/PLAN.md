# Review-required with pending retries — investigation plan

## Status

Slices 0–8 complete; Voof-paws 6 and owner release approval recorded. The fresh
`0.4.29` candidate passed release qualification and is ready for immutable tag
and publication. No provider work, retained-run mutation, deployment, or
retained-run recovery is authorized.

## Objective

Determine, from exact native and API provenance, why the Pippin and Duchess QA
runs reached `native.review.requires_review` while creative-retry actions remained
in mixed custody. Decide whether the outcome was editorially valid, prematurely
selected, based on incorrect retry lineage/fan-in, or accompanied by an incorrect
provider-custody projection.

Deliver a sanitized provenance timeline, causal assessment, confidence statement,
and public-contract recommendation. Add implementation slices only if the evidence
demonstrates a concrete gap.

## Frozen scope

### In scope

- Exact-Natal interactive runs for Pippin and Duchess.
- Read-only API/PostgreSQL, worker-log, R2 checkpoint, snapshot, journal, action
  ledger, pass, retry, QA, lint, validation, and final-deck evidence.
- Provider-free reproduction using scripted transports and sanitized fixtures.
- Existing retry selection, attempt-limit, fan-in, final-QA, review, lifecycle,
  and custody-projection rules.
- Documentation or regression-only closeout if behavior is correct.
- A narrowly justified runtime/public-contract patch if behavior is incorrect.

### Out of scope unless separately planned and approved

- Provider calls or retrievals.
- Resume, reconciliation, repair, denial, recovery, deletion, or mutation of the
  retained Pippin/Duchess workspaces.
- API reservation release or retained-run terminalization.
- Batch, bounded Natal, polish, critic, or candidate-policy redesign.
- New retry policy, changed attempt limits, or editorial-quality tuning.
- Deployment, paid QA, release, or publication.

## Core invariants

1. Retained workspaces are immutable evidence.
2. Every action conclusion joins native run ID, action ID, complete binding,
   route, stage, pass, attempt, and provider identity where applicable.
3. `review_required` may end editorial execution without erasing provider custody.
4. Once editorial review is terminal, no new provider create may be permitted.
5. A provider-created action cannot be treated as providerless merely because its
   response was not yet reported to the API.
6. Missing evidence remains unknown; zero, absent, unresolved, and contradictory
   are not interchangeable.
7. No conclusion relies on action counts alone.
8. Diagnostic reports contain no prompts, authored content, protected subject
   data, credentials, or provider payloads.

## Evidence hierarchy

Use evidence in this order, recording disagreements rather than flattening them:

1. Snapshot-validated native authoritative members and immutable public artifacts.
2. API-owned PostgreSQL action/provider/reservation records.
3. Native journal and structured execution events.
4. Worker logs.
5. Provider-free reproduction and source-code interpretation.

## Slice 0 — Freeze the evidence map and inspection protocol

**Status:** complete; paused at Voof-paws 1 before retained access.

### Work

- Reconcile the two sprint backgrounds and the completed 0.4.28 handoff findings.
- Freeze exact API/native run IDs, retained checkpoint generations, archive and
  inventory hashes, known action/provider identities, and relevant timestamps.
- Enumerate the minimum snapshot members needed to resolve pass lineage, attempt
  lineage, retry feedback, final QA, validation/lint disposition, and lifecycle
  projection.
- Define a read-only R2 procedure with path containment, archive/inventory/hash
  validation, bounded extraction, access logging, and cleanup.
- Define a sanitization inventory before reading content-bearing files.
- Add a manifest that hashes this protocol and the incident background.

### Tests/gates

- Procedure cannot invoke an SBE runner, provider transport, or workspace writer.
- Exact R2 objects and expected hashes are fixed before download.
- Extraction refuses path traversal, duplicate members, undeclared members used
  as authority, or hash mismatch.
- No credentials or protected bytes enter committed artifacts.

### Deliverables

- `SLICE 0 - EVIDENCE MAP AND READ-ONLY INSPECTION PROTOCOL.md`
- frozen inspection manifest
- provider-free protocol tests where useful

### Voof-paws 1

Owner/API review before retained R2 bytes are read. R2 credentials may be restored
only for the bounded inspection window and removed afterward.

## Slice 1 — Read-only retained-workspace provenance reconstruction

**Status:** complete; paused at Voof-paws 2.

### Work

- Download only the two frozen checkpoint objects.
- Verify archive bytes, archive hash, manifest generation, logical root, complete
  inventory identity, and every accessed member hash before interpretation.
- Reconstruct, for each run:
  - six initial pass assignments;
  - every creative-retry action and its pass/attempt/stage/binding lineage;
  - preparation, authorization, call-entry/provider identity, retrieval/reporting,
    acceptance/rejection, and successor relationships;
  - exact retry feedback and retry-selection reason;
  - validation, lint, final-QA, and review-required evidence available at the
    retained checkpoint;
  - native provider-custody inventory and its relationship to API facts.
- Produce a sanitized chronological and lineage-oriented timeline.
- Record any decisive evidence known to have occurred after the retained snapshot
  as unavailable rather than reconstructing it as historical fact.

### Tests/gates

- Zero provider calls, creates, retrievals, spend, workspace writes, or R2 writes.
- Every reported fact cites an authoritative member/hash or a clearly identified
  diagnostic/API source.
- API/native action joins are exact; unresolved joins remain explicit.
- Temporary archives and credential variables are removed after inspection.

### Deliverables

- `SLICE 1 - SANITIZED RETAINED PROVENANCE TIMELINE.md`
- machine-readable sanitized lineage inventory
- inspection receipt recording files/hashes accessed and zero side effects

### Voof-paws 2 — Causal evidence review

Pause for owner/API review. Classify the evidence as one of:

- sufficient to prove valid editorial review;
- sufficient to prove an SBE retry/fan-in/final-QA defect;
- sufficient to prove a custody-projection defect;
- contradictory across native/API authority;
- insufficient because the decisive transition was never retained.

Do not freeze a fix before this classification.

## Slice 2 — Provider-free causal reproduction

**Status:** complete; paused at Voof-paws 3.

### Work

- Construct sanitized, production-shaped fixtures reproducing the exact observed
  pass/action topology without provider access.
- Drive the real retry-selection, fan-in, validation, final-QA, lifecycle, and
  review branch through supported runtime boundaries.
- Inject the relevant custody combinations:
  - reported retry;
  - durable provider identity without reported result;
  - providerless authorized successor;
  - pass-local exhaustion or fatal QA evidence where observed.
- Determine whether current released behavior can reach the historical trace and
  whether it does so only under valid or contradictory inputs.
- Compare SBE 0.4.27 historical behavior with current main only where necessary
  to separate the original defect from later lifecycle changes.
- Preserve `theme_group_coverage` only where needed to reproduce the historical
  trace, then prove the same transition invariants with a generic legitimate QA
  rejection so the correction cannot depend on one failure modality.

### Tests/gates

- Zero external network/provider use and zero spend.
- Deterministic fixture and outcome digests.
- No provider create after editorial review becomes terminal.
- Provider-custody projection exactly matches durable native provider evidence.
- A pass cannot consume or exhaust another pass's attempt lineage.
- Final QA cannot silently treat required unresolved fan-in as completed evidence.

### Deliverables

- `SLICE 2 - PROVIDER-FREE CAUSAL REPRODUCTION.md`
- sanitized fixtures and focused regression tests
- causal matrix with direct, inferred, and unknown findings

### Voof-paws 3 — Investigation conclusion

Pause for owner/API review. Freeze the conclusion and confidence level before
adding any later slice.

## Implementation continuation after Voof-paws 3

The investigation proved both a retry/action-lineage defect and a custody
projection defect. The following slices are the proposed SBE-led correction.
They remain unimplemented until the Voof-paws 3 owner/API review approves the
contract direction.

## Slice 3 — Freeze stable retry-lineage and mixed-custody contracts

**Status:** complete; paused at Voof-paws 4.

### Work

- Define the canonical semantic identity of an authored attempt independently of
  mutable revision/snapshot and binding identity: native run, route family,
  stage, pass, and attempt number only. Model/mechanism, action ID, request
  digest, binding digest, and request artifact are evidence attached to that key.
- Require one authoritative action lineage per semantic attempt. Multiple action
  IDs or request digests for one lineage are a closed contradiction, never a
  newest-row-wins condition.
- Define exact predecessor-feedback selection: only completed prior attempts
  contribute feedback; the current incomplete attempt cannot erase that history.
- Define re-entry rules for `PREPARED`, `AUTHORIZED`, call-entered, provider-bound,
  reported, denied, and terminal action states.
- Define a closed mixed-custody inspection projection in which:
  - provider-bound custody remains the selected reconciliation command;
  - providerless lineage conflict remains visible as native safety evidence;
  - after provider custody clears, unresolved incompatible authority becomes a
    typed non-dispatching review/refusal;
  - no API consumer reconstructs or selects actions.
- Prefer a fresh closed lifecycle version (provisionally v0.8) if the new lineage
  evidence changes the exact public document shape. Preserve v0.7 as historical;
  do not widen it silently.
- Freeze typed reason vocabulary, exact action/binding joins, canonical ordering,
  replay rules, and compatibility behavior for impossible historical workspaces.

### Tests/gates

- Schema plus strict Python semantic validation without optional `jsonschema`.
- Mutation tests for duplicate route, changed request digest, wrong pass/attempt,
  mismatched action pointer, reordered inventory, stale snapshot, and provider
  evidence appearing after observation.
- Same basis/time is exact replay; changed native truth creates a new basis.
- A valid document can expose provider reconciliation plus a secondary lineage
  contradiction without implying that the contradiction is safe to dispatch.

### Deliverables

- Contract proposal and API handoff with complete JSON examples.
- Closed schemas/fixtures and source-level validators/builders.
- Compatibility matrix for v0.7 and the new contract.

### Voof-paws 4 — API contract freeze

Pause for API review before runtime mutation work. API may begin its companion
schema/ingestion plan from the frozen fixtures, but must not infer from v0.7.

## Slice 4 — Make pass-attempt preparation and re-entry idempotent

**Status:** complete.

### Work

- Persist the exact paid action ID and complete request-binding identity on the
  pass attempt at first preparation.
- Derive retry feedback from completed predecessors before creating the current
  attempt and preserve the resulting request payload artifact/digest immutably.
- On re-entry, reuse and validate that exact persisted action/payload/binding;
  never rebuild a new paid action for the same attempt.
- Route a compatible authorized action only through its exact constrained
  authority executor. Generic resume must not consume or replace it.
- If persisted attempt/action/payload evidence cannot join exactly, fail closed
  before provider I/O or authorization mutation.
- Preserve provider identity immediately and make all later result observation
  retrieval-only.

### Tests/gates

- First preparation → authority wait → exact replay produces one action ID and
  byte-identical request binding.
- Fresh authorization → constrained dispatch creates exactly once.
- Re-entry before/after authorization, call entry, provider identity, response,
  QA rejection, and process interruption cannot create a second action.
- QA feedback contains all completed predecessors and excludes the current
  incomplete attempt, for a generic rejection vocabulary.
- No provider call occurs in mismatch/refusal tests.

## Slice 5 — Enforce whole-ledger lineage integrity and custody precedence

**Status:** complete.

### Work

- Add a whole-ledger preflight that detects duplicate/conflicting semantic attempt
  lineages before local retry progression or any provider create.
- Permit safe retrieval/reconciliation of exact durable provider identities even
  while a separate providerless lineage contradiction remains.
- Block new provider creation for every conflicted semantic lineage.
- After retained provider custody settles, expose the remaining providerless
  conflict through the frozen typed review/refusal path.
- Keep editorial status, provider custody, consumer authority, and local execution
  capacity as distinct facts.
- Add bounded structured diagnostics without payloads, prompts, bindings,
  credentials, or subject prose; sink failure remains behaviorally isolated.

### Tests/gates

- Pippin/Duchess-shaped mixed inventory selects bounded reconciliation first.
- Fifth/later conflicting member cannot escape whole-inventory validation.
- Not-due and due custody retain exact 4+2 bounded selection semantics.
- After fan-in, the orphaned authority is visible and non-dispatching.
- Exact replay produces no create, retrieval duplication, or new action rows.

## Slice 6 — Production-shaped provider-free end-to-end qualification

**Status:** complete; paused at Voof-paws 5.

### Work

- Build sanitized exact-interactive fixtures using the generic QA-rejection path:
  initial fan-out, rejected pass, retry preparation, authority, dispatch, detach,
  reconciliation, second rejection, next retry, and final resolution.
- Exercise crashes around preparation, authorization, intent, call entry, identity
  durability, retrieval, fan-in, QA persistence, and next-action selection.
- Include a historical contradictory-workspace fixture proving retrieval-only
  custody handling followed by typed review, with no repair-by-inference.
- Assess bounded-interactive applicability explicitly. Reuse shared behavior only
  if its route-specific binding and state contracts remain intact.
- Preserve exact/Bounded Batch behavior or fail closed explicitly; do not broaden
  this patch into Batch topology redesign.

### Tests/gates

- Zero external network, credentials, or spend.
- No duplicate create/action for any pass attempt.
- No spin: every advertised command changes native truth or yields a different
  typed disposition.
- Deterministic fixture and receipt hashes across fresh workspaces/processes.
- Privacy sentinel absent from fixtures, receipts, events, logs, and stdout.

### Voof-paws 5 — API fixture and runtime review

Pause with schemas, fixtures, traces, and qualification receipt. API companion
work must prove its mapper preserves reconciliation custody, invokes only exact
constrained authority, and does not terminalize a nonterminal safety review.

## Slice 7 — Public installed-wheel surface and consumer handoff

**Status:** complete; paused at Voof-paws 6.

### Work

- Package the new schema/readers/validators and provider-free qualification CLI.
- Publish exact examples for normal retry progression, mixed custody with lineage
  conflict, post-custody review/refusal, stale replay, and exact replay.
- Document API responsibilities for reservations, leases, capacity, and durable
  action admission without asserting them as SBE facts.
- Document historical v0.7 behavior and fail-closed compatibility.
- Require API companion evidence for request/grant/binding joins and queue mapping.

### Tests/gates

- Clean Python 3.11 installed-wheel qualification.
- Public CLI refuses production inputs, credentials, network configuration, and
  output paths inside its fixture workspace.
- Packaged fixture manifest hashes every consumer artifact.
- API review explicitly accepts the final public surface.

### Voof-paws 6 — Joint adoption review

Pause before release preparation until API confirms its companion implementation
and joint provider-free campaign consume the packaged contract correctly.

## Slice 8 — Broad regression and release preparation

**Status:** complete; immutable tag/publication authorized.

### Work

- Run focused lifecycle/retry/external-authority suites, installed smoke, full
  release suite, deterministic wheel rebuild, and dependency/manifest checks.
- Reconcile sprint status, evidence, release notes, and consumer handoff.
- Record exact artifact source commit and candidate wheel SHA-256.
- Confirm retained QA workspaces remain untouched and no provider traffic/spend
  occurred.

### Final release gate

Version bump, tag, publication, deployment, API pinning, and any retained-run
recovery each require explicit later approval. Investigation or implementation
completion alone authorizes none of them.

## Final deliverables

- Sanitized two-run provenance timeline.
- Per-pass/per-attempt action lineage and custody inventory.
- Exact review/QA reason where provable, or explicit unknown classification.
- Causal assessment with confidence level for every material conclusion.
- Public-contract assessment for distinguishing normal review from broken handoff.
- Regression/qualification evidence appropriate to the selected continuation path.
- Consumer handoff if—and only if—a public/runtime contract changes.
