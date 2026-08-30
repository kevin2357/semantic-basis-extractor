# Retry external-authority v2 dispatch handoff — sprint plan

## Status

Slice 0, the bounded Diffie follow-up, Slice 1 implementation/API review, and the
lean release-candidate gate are complete. Fresh immutable candidate `0.4.31` is
paused for final owner/API commit, tag, and publication approval.
Voof-paws 1 classified
Hellman as an API terminal-result ingestion/routing defect. Diffie's exact rejected
document remains unavailable; a provider-free source-compatible strict-consumer
seam is frozen without claiming it reproduces the missing live bytes. No provider
work, retained-run mutation, deployment, recovery, release, or QA worker resume
occurred.

## Objective

Establish and qualify the exact public handoff by which a post-fan-in creative
retry that is admitted by API but not yet provider-created crosses SBE's
external-authority v2 dispatch fence exactly once. Eliminate generic-resume
inference, incomplete lifecycle consumption, and capacity-holding retry loops
without weakening provider-create fencing or conflating API spend admission with
native SBE authority.

The sprint is evidence-led. Slices after Slice 0 are provisional until retained
evidence and a provider-free production-boundary reproduction identify the actual
gap.

## Frozen incident identities

| Pup | API run | Native run | Observed posture |
| --- | --- | --- | --- |
| Diffie | `9cbc3c0c-9a5f-42ff-8fc0-cc23f08b75df` | `ee69cb149c4e533ff9e1341355ef2ce13246a5e8a2617b387da903ecfd58fa60` | failed strict ordinary-resume lifecycle consumption; two retained retry provider identities |
| Hellman | `bababdec-3f3d-4315-8dfc-e70c46dd6288` | `856e9c41085e954a964edc2963d2de64ccafbedfee81c5805a779abee2faf550` | retry-wait; one retained retry provider identity plus `paid_bfce7b3ea385abe55a5045d1` authorized/providerless |

Candidate baseline is immutable SBE `0.4.30`. The OpenAI dashboard observation
that three retry Responses completed is diagnostic only and must not be treated as
native completion or recovery authority.

## Immediate containment

- Keep QA SBE worker `srv-da12sktbedkc73btpu00` suspended.
- Do not invoke ordinary resume, provider reconciliation, v2 dispatch, denial,
  retirement, closeout, repair, deletion, or recovery against either retained run.
- Do not create, retrieve, cancel, or otherwise touch provider operations.
- Preserve API leases, reservations, action rows, and retained native bytes as
  incident evidence unless separately authorized by the owner.
- Do not select any dashboard-visible provider result as canonical.

## Scope

### In scope

- Read-only examination of exact retained Diffie/Hellman checkpoints when useful.
- Public lifecycle v0.8, temporal v0.6, local-work, reconciliation, generic
  refusal, and external-authority v2 contract/source analysis.
- Exact API-to-SBE joins among request, grant, ordinary authorization document,
  action, binding, checkpoint basis, invocation, result, and receipt.
- Provider-free production-boundary characterization and failure injection.
- A narrow native correction if Slice 0 proves the current public inspection or
  dispatcher cannot express the required handoff.
- Route/stage parity classification without assuming support.
- Consumer fixtures, installed-wheel qualification, and API handoff documents.

### Out of scope unless explicitly added after review

- Retained-run recovery or mutation.
- Real provider calls, retrievals, cancellation, or spend.
- API database, queue, lease, reservation, capacity, or deployment changes.
- Changes to retry editorial policy, prompt construction, attempt limits, costs,
  or deterministic QA.
- Batch or bounded runtime changes unless the proven primitive is shared and a
  later reviewed slice explicitly admits them.
- Reinterpreting an old API authorization as a current SBE v2 grant.

## Authority and safety invariants

1. API owns global spend admission, reservations, entitlements, leases, and
   capacity; SBE does not assert those facts.
2. SBE owns the native checkpoint, paid-action inventory, exact binding,
   provider custody, dispatch eligibility, and single-writer mutation.
3. An API authorization row is not a provider-create command. Provider creation
   requires the exact current SBE request, a compatible closed v2 grant, and all
   complete ordinary authorization documents.
4. Retained provider custody outranks new provider authority. API invokes only the
   SBE-selected run-level reconciliation command and never chooses members.
5. Completed provider evidence may enable bounded local fan-in; it does not itself
   authorize a successor provider create.
6. A successor retry can be dispatched only from a fresh checkpoint whose exact
   paid-action inventory and binding are public and stable.
7. Generic resume remains non-create-capable and must return a typed, nonmutating
   refusal when v2 dispatch is required.
8. Provider identity durability makes an action retrieval-only. Identity-less
   call entry remains ambiguity and cannot be replayed as create work.
9. Repeated request/grant/dispatch invocations are exact replay or typed refusal,
   never duplicate provider creation.
10. Unjoinable historical evidence is review/refusal evidence, not permission to
    synthesize native state or authority.
11. Safe refusal must not be interpreted as successful completion or an
    indefinitely retryable capacity-holding no-op.

## Evidence hierarchy

1. Snapshot-validated native run/action ledger, lifecycle inspection, journal,
   sealed result, publication receipt, and command-result envelope.
2. API-owned paid-action, admission/grant, provider-operation, invocation, lease,
   reservation, and ingestion records.
3. Structured SBE/API events and sanitized logs.
4. Source-path analysis and provider-free reproduction.

Dashboard observations and absence of log lines remain diagnostic only.

## Slice 0 — Freeze and reproduce the missing handoff

### Purpose

Determine whether Diffie/Hellman expose an SBE lifecycle/contract defect, an API
consumer/routing defect, or a joint seam mismatch. Freeze the exact transition
sequence before choosing a schema or runtime change.

### 0A — Freeze evidence coordinates

- Obtain an API-owner-produced, sanitized coordinate packet for each retained run
  containing the exact checkpoint object key, version/generation if available,
  size, ETag/checksum, archive SHA-256, snapshot generation/digest, logical root,
  native run ID, deployed SBE/image/profile identities, and relevant API record
  identifiers.
- Hash all supplied coordinate packets, API exports, and log extracts.
- Record which facts predate the retained checkpoint and which were observed
  later; never project later dashboard/API facts backward into native state.
- Record the exact Diffie exception-bearing invocation and every Hellman repeated
  refusal invocation available from authoritative API evidence.

### 0B — Bounded read-only retained-workspace inspection

If retained bytes are needed:

- issue only exact object `HEAD` and exact object `GET` calls for the two frozen
  checkpoints; no bucket listing, prefix discovery, writes, copies, repair, or
  deletion;
- download into a fresh temporary directory outside the repository;
- validate object hash, archive safety, logical root, complete snapshot inventory,
  member hashes, receipt namespace, and result/journal joins before interpreting
  state;
- inspect only the minimum declared members needed for the action/custody/handoff
  join: run state, action ledger, lifecycle/temporal inspection, retry lineage,
  local-work evidence, authorization/consumption facts, result index/results,
  receipts, journal, and command-result envelopes;
- avoid prompt, authored-content, payload-body, credential, and unrelated subject
  artifacts;
- produce a sanitized access receipt with exact object/member hashes and explicit
  zero-write, zero-provider, and zero-mutation assertions; and
- remove temporary credentials and downloaded protected bytes after sanitized
  evidence and hashes are verified.

### 0C — Reconstruct each native timeline

For every creative-retry action, determine:

- stable pass/attempt and retry-lineage identity;
- action ID, complete public binding or binding digest, state, requiredness, and
  provider evidence;
- request/grant/authorization-document identity and native consumption state;
- call-entry intent and provider-identity durability;
- retrieval status, reported completion, usage settlement, and result persistence;
- fan-in/local-work operation advertised and consumed;
- checkpoint, lifecycle branch, external-authority request, and refusal/result
  published after each transition; and
- whether the providerless successor action was merely API-authorized or also had
  an exact current SBE v2 grant and authorization document.

Treat Diffie and Hellman as separate timelines. Explain why one produced strict
consumer failure while the other produced a retry loop.

### 0D — Reconstruct the API handoff

- Join API rows to native actions by exact native run/action/binding identity, not
  stage or count.
- Identify which lifecycle/request/refusal/result/receipt documents API actually
  received and validated for each invocation.
- Determine whether API persisted a true SBE v2 grant or only its own spend
  authorization/admission.
- Map the branch that converted generic refusal into retry-wait and retained
  capacity, and the branch that rejected Diffie's ordinary-resume evidence.
- Establish whether a current v2 request was available but ignored, never
  generated, invalid, or stale after reconciliation/fan-in.

### 0E — Trace production source boundaries

Create a function-level map for:

- lifecycle precedence among provider reconciliation, local work,
  `await_external_authority`, ordinary resume, review, and terminal branches;
- retry preparation and stable attempt/action identity;
- v2 request construction and checkpoint/binding joins;
- API grant/authorization-document validation;
- generic provider dispatch refusal construction/publication;
- constrained v2 intent, call entry, identity durability, and replay;
- reconciliation 4+2 selection and fan-in/local-work consumption; and
- API branch mapping, slot release/retention, and retry scheduling.

### Competing hypotheses

Test rather than assume:

1. SBE produced a correct v2 request, but API invoked generic resume because its
   router did not adopt that request.
2. SBE selected `ordinary_resume` while retained provider custody should have
   selected reconciliation or bounded local fan-in first.
3. API's persisted authorization was valid API spend evidence but no current SBE
   v2 grant was ever created.
4. A v2 request/grant existed but became stale when reconciliation or fan-in
   advanced the checkpoint basis.
5. The providerless retry inventory was not yet stable, so SBE correctly withheld
   authority and API incorrectly treated the intermediate local branch as
   create-capable.
6. Diffie and Hellman reached materially different native states and require
   different consumer mappings.
7. The evidence identifies another cause; record it instead of forcing the above.

### 0F — Provider-free production-boundary reproduction

Build the smallest provider-free scenario through supported runtime/public
boundaries that includes:

1. a completed initial wave;
2. one creative retry with a scripted durable provider identity;
3. pending then completed retrieval and native fan-in;
4. preparation of the next exact retry action;
5. API-shaped spend admission without pretending it is an SBE grant;
6. lifecycle inspection and public request selection;
7. an attempted generic resume and typed zero-I/O refusal;
8. a fresh exact v2 request/grant/authorization-document dispatch;
9. exactly one scripted provider create and durable detach; and
10. replay/re-entry proving no duplicate create.

Where current behavior cannot complete this sequence, freeze the precise failing
boundary instead of mocking through it. Include a mixed state with retained
provider custody and providerless successor work so precedence is tested directly.

### 0G — Bounded Diffie tributary after Voof-paws 1

- Keep Diffie separate from Hellman's proven terminal-result ingestion defect.
- Exhaust retained checkpoint, API sprint evidence, repository logs, and public
  consumer predicates for the exact rejected lifecycle document.
- Characterize provider-free any concrete public shape that reaches the same
  strict-consumer predicate, but label synthetic evidence as source-compatible
  rather than retained reproduction.
- Record the historical cause as unavailable if the exact document or complete
  predicate projection was not retained.
- Do not reopen R2, touch the provider, or propose native runtime work merely to
  explain missing historical bytes.

### Slice 0 deliverables

- `SLICE 0 - EVIDENCE MAP AND READ-ONLY INSPECTION PROTOCOL.md`
- `SLICE 0 - DIFFIE AND HELLMAN SANITIZED TIMELINES.md`
- machine-readable sanitized transition/join matrix
- read-only access receipt if R2 is used
- `SLICE 0 - SOURCE BOUNDARY AND CAUSAL ASSESSMENT.md`
- provider-free characterization fixture/test
- updated `LOG.md` and `EVIDENCE.md`

### Slice 0 gates

- No provider access, retained mutation, recovery, or broad R2 discovery occurs.
- Every causal claim cites a retained member/hash, exact API record, event/log
  identity, source location, or provider-free test and states its confidence.
- API authorization and SBE grant are never conflated.
- Provider custody, completed-but-unconsumed evidence, local work, providerless
  authority, and review are distinguished.
- The first failing selection/ingestion/dispatch boundary is identified, or the
  evidence is explicitly insufficient.
- Reproduction proves provider create count and public branch/result identities.
- Focused tests and `git diff --check` pass.

## Voof-paws 1 — Causal review

Pause for owner and API review. Select exactly one primary correction class:

- API consumer/routing correction using existing SBE contracts;
- SBE public inspection/request correction plus API adoption;
- joint contract evolution; or
- typed retained-review posture because the historical join is unprovable.

No schema or runtime mutation begins before this review.

## Slice 1 — Typed terminal-result availability preflight

API Slice 2 identified one narrow SBE reader gap needed for Hellman's
terminal-result-first correction. Add a versioned, provider-free discovery surface
that distinguishes:

- no sealed result available;
- one exact latest sealed result ID available; and
- invalid/conflicting discovery evidence.

The surface is discovery-only. It exposes no lifecycle state, provider fact,
action authority, or terminal meaning. API must carry the returned exact ID into
the existing strict explicit-result reader and terminal ingress.

Implement the contract frozen in
`SBE RESPONSE TO API SLICE 2 - TERMINAL RESULT AVAILABILITY.md`, including strict
Python validation, schema/resource packaging, a read-only CLI, malformed/orphaned
evidence tests, output containment, and installed-wheel provider-free smoke.

### Gate

API approved the closed schema with a restored snapshot-digest refinement. The
implementation and installed-wheel check are complete. Pause for API fixture and
consumer review before release preparation. This additive reader patch does not
reopen Diffie's historical causal classification or alter provider/lifecycle
behavior.

## Slice 2 — Freeze the public handoff contract (provisional and presently unnecessary)

Prefer the existing external-authority v2 ordinary-action-set contract if Slice 0
shows it is sufficient for one retry action. Define and test:

- exact checkpoint/basis, route, mechanism, action, binding, and request identity;
- canonical action ordering and one-action cardinality;
- API grant and ordinary authorization-document joins;
- distinction between API admission reuse and a fresh SBE request-bound grant;
- provider-custody and local-work precedence before request availability;
- generic refusal's exact next supported action and non-dispatching semantics;
- no-grant quiescence without assertions about API-global capacity;
- exact replay, stale basis, binding mismatch, provider evidence, ambiguity, and
  unjoinable-history refusals; and
- API behavior for slot/lease release versus retained provider/spend custody.

Version only public shapes that genuinely change. Do not widen a closed schema in
place or invent a new state if existing vocabulary is sufficient.

### Gate

Publish strict schemas/validators and sanitized fixtures. Pause for API review
before runtime implementation.

## Slice 3 — Native selection/dispatch correction (conditional)

Only if Slice 0/1 prove SBE work is required:

- correct lifecycle precedence or request publication at the exact identified
  boundary;
- revalidate current request/grant/documents and native custody under the writer;
- persist one complete authorization/intent checkpoint before provider I/O;
- release the writer for slow provider create;
- durably checkpoint each returned identity immediately;
- preserve ambiguity for entered calls without identity;
- keep result observation reconciliation-only; and
- make generic-resume refusal nonmutating and replay-stable.

Add exact and bounded classification; implement only routes proven to share the
same safe primitive. Keep Batch explicitly supported or fail-closed/deferred.

### Gate

Provider-free runtime tests pass and public evidence is sufficient for an API
consumer without private workspace access. Pause for API review.

## Slice 4 — Failure, replay, and mixed-custody matrix

Exercise at minimum:

- retained provider pending/not-due and due 4+2 retrieval;
- completed evidence awaiting local fan-in;
- fan-in producing one providerless retry;
- API admission present but no SBE v2 grant;
- exact one-action request/grant/dispatch;
- stale request/grant after checkpoint advancement;
- binding/action/inventory mismatch;
- provider identity appearing before create;
- call-entered ambiguity;
- exact replay after durable identity;
- generic refusal repeated without mutation or create;
- unjoinable historical authorization;
- Diffie-shaped strict incomplete evidence; and
- Hellman-shaped refusal/slot-loop evidence.

Require typed redacted events/logs at branch selection and refusal boundaries;
event-sink failure must not affect authority, state, or provider behavior.

## Slice 5 — Public consumer fixtures and installed-wheel qualification

- Package schemas, readers/validators, sanitized fixtures, and a provider-free
  installed-wheel command/receipt.
- Exercise real public lifecycle, request, grant, constrained dispatch,
  reconciliation, fan-in, generic refusal, and replay boundaries in fresh runtime
  contexts.
- Prove exact provider create/retrieve counts, sealed result/receipt joins,
  immutable predecessor continuity, and no protected sentinel leakage.
- Provide an API handoff with exact examples, route matrix, migration notes, and
  explicit statement that an API authorization row is not an SBE grant.

### Gate

Pause for API fixture/consumer review before joint qualification.

## Slice 6 — Joint provider-free campaign

SBE proves its installed runtime semantics; API separately proves:

- ingestion of the exact public request/refusal/result artifacts;
- creation and persistence of the compatible v2 grant/documents;
- invocation of constrained dispatch instead of generic resume;
- release of local capacity while provider work is pending or authority is
  quiescent;
- no slot-holding no-op loop;
- exact replay and duplicate-create refusal; and
- stable operator review for unjoinable history.

Run a two-deck/one-slot starvation witness if the API scheduling correction is in
scope. Retained Diffie/Hellman recovery remains separately authorized.

## Slice 7 — Release preparation (conditional)

- Reconcile docs, changelog, compatibility manifest, and package resources.
- Bump to a fresh immutable version before the broad/full release suite.
- Run focused tests, installed-wheel smoke/qualification, broad suite, full suite
  if required by the release runbook, deterministic double build, and
  `git diff --check`.
- Record exact source commit, wheel SHA-256, dependency compatibility identities,
  fixture/receipt hashes, and zero-provider/zero-retained-mutation evidence.
- Pause for owner and final API consumer approval before commit/tag/publication.

## Testing strategy

Testing proceeds from the seam outward:

1. contract/schema mutation tests;
2. provider-free lifecycle/selection unit tests;
3. production-boundary runtime characterization;
4. exact mixed-custody integration tests;
5. fresh-process restore/replay tests;
6. installed-wheel qualification;
7. API consumer fixtures and joint scheduling campaign; and
8. release regression/reproducibility gates.

No test may require provider credentials, network, real spend, or retained QA
mutation. Scripted transports must count every create and retrieve separately.

## Review map

| Point | Review purpose |
| --- | --- |
| Before Slice 0 | owner approval of investigative scope and read-only posture |
| Voof-paws 1 | causal classification and decision whether SBE contract/runtime work is needed |
| Before Slice 1 implementation | terminal-result availability schema/absence semantics |
| After Slice 2, if activated | cross-repo handoff and authority freeze |
| After Slice 3, if activated | runtime safety and route-scope review |
| After Slice 5 | API fixture/consumer acceptance |
| After Slice 6 | joint campaign acceptance |
| Before release | explicit owner and API release approval |
