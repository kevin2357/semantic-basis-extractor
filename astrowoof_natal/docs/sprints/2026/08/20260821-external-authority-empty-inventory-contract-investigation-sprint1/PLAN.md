# External-Authority Empty-Inventory Contract Investigation — Sprint 1 Plan

Date: 2026-08-21
Status: complete; 0.4.15 tagged, published, and independently verified
Mode: provider-free, retained-workspace read prohibition, contract-first

## Objective

Determine exactly why the retained QA lifecycle inspection failed the API's
external-authority branch validation, then make the SBE public contract reject or
classify every empty, inadmissible, or contradictory authority inventory before a
consumer must infer the problem.

The sprint must preserve native authority and provider safety. It must not touch the
retained QA workspace, submit/retrieve provider work, relax the API validator, or
infer authority from logs.

## Frozen invariants

- `await_external_authority` names a nonempty exact ordered action inventory.
- The branch inventory exactly equals the embedded request inventory.
- Every request action has a complete validated public binding.
- No admissible inventory means typed refusal/review, never an empty authorization
  request and never an ordinary provider-capable resume.
- Providerless investigation cannot authorize, consume, submit, retrieve, deny, or
  reconcile paid work.
- The retained QA workspace is immutable incident evidence and outside test scope.
- API remains authoritative for its scheduling validation, reservations, database,
  and global spend policy.

## Slice 0 — Exact failure-shape reconnaissance

- Inventory all native and API predicates collapsed into the observed error.
- Build a provider-free production-shaped state family representing the retained
  post-initial-wave/recovery class without copying protected or provider content.
- Exercise the real `inspect_lifecycle()` and API-equivalent validation boundary.
- Determine whether any supported 0.4.14 path can expose an empty branch, or identify
  the actual differing predicate.
- If exact incident evidence cannot be recovered, record that limitation and keep
  conclusions bounded to the reproducer.

Gate: evidence distinguishes proven root cause from defense-in-depth hardening.
Pause for API review before freezing contract changes.

## Slice 1 — Contract and diagnostic proposal

- Freeze the explicit semantic rule that `await_external_authority` action IDs are
  nonempty and exactly joined to the request.
- Define typed outcomes for valid request, request unavailable/native inconsistency,
  and initial-wave lineage refusal.
- Specify redacted structured diagnostics for classification and failed predicate:
  command, disposition, reason, eligibility, action count/IDs, request/refusal
  presence and digest, without bindings, documents, prompts, subject data, or
  credentials.
- Decide whether the existing schema version can be tightened compatibly or a new
  lifecycle/request version is required.

Gate: joint SBE/API contract approval.

## Slice 2 — Native validator and classification hardening

- Add the explicit nonempty branch invariant to schema and semantic validation.
- Ensure request-building failures deterministically produce a closed typed refusal
  or native-review outcome.
- Prevent preliminary `await_external_authority` branch shapes from escaping when
  final request construction fails.
- Preserve valid ordinary action-set and six-member initial-wave behavior.

Gate: every invalid inventory fails or refuses before provider-capable execution.

## Slice 3 — Structured observability

- Emit failure-isolated, redacted typed events at lifecycle classification and
  external-request/refusal selection.
- Add concise `✨🐶` logs naming the selected branch and predicate-level reason.
- Keep logs/events non-authoritative and prove sink failure cannot alter inspection,
  snapshots, native state, or provider-call behavior.

Gate: a repeat incident identifies the exact failed predicate without exposing
protected/provider payload content.

## Slice 4 — Provider-free regression matrix

Exercise the real inspection and public validators for:

- valid nonempty ordinary prepared action set;
- valid exact six-member initial-wave request;
- valid bounded six-member initial-wave request;
- no prepared actions;
- empty, duplicate, unknown, or binding-mismatched inventory;
- stored wave with inadmissible action state;
- unjoinable historical initial-wave lineage;
- contradictory eligibility, reason, disposition, or `not_before`;
- request/branch run, observation, digest, and ordered-ID mismatches; and
- concurrent/read-race or incomplete-snapshot refusal.

Assert zero provider create/retrieve calls and byte-identical native state/snapshot
for read-only inspection and refusal cases.

Gate: targeted native and API-equivalent semantic matrices pass.

## Slice 5 — Installed-wheel qualification and consumer handoff

- Add a provider-free installed-wheel command or extend the existing qualification
  surface to exercise real workspace, snapshot, inspection, and validator paths.
- Publish sanitized positive/refusal/mutation fixtures and a closed receipt.
- Document exact API selection requirements, compatibility implications, and the
  supported disposition for the retained state class.
- Pause for API fixture/consumer review.

Gate: the installed wheel proves the public behavior without source-tree helpers,
network, credentials, spend authority, or production inputs.

## Slice 6 — Closeout and release decision

- Run affected lifecycle/external-authority suites, privacy scans, installed-wheel
  qualification, release smoke, and platform-appropriate packaging checks.
- Record whether the change is contract tightening, runtime correction, diagnostics
  only, or a combination.
- Recommend a fresh immutable patch only after API and owner approval.

Gate: explicit authorization before version bump, tag, or publication.

## Testing strategy

Use deterministic provider-free fixtures and scripted transports whose create and
retrieve methods fail the test if called. Prefer the real public inspection and
validation entry points over direct helper-only tests. Mutation tests must change
one safety-critical field at a time so diagnostic reason precision is provable.

Test failure injection around snapshot validation, request construction, event/log
sinks, and observation races. No test may accept a manually blessed snapshot or
derive authority from private state after public validation fails.

## Deliverables

- exact failure-shape/reproducer report;
- lifecycle/request contract decision;
- schema and semantic-validator changes if required;
- structured diagnostic vocabulary and privacy inventory;
- provider-free regression corpus;
- installed-wheel qualification receipt;
- API consumer/recovery handoff; and
- completed sprint log, evidence, and release recommendation.

## Explicit non-goals

- mutating or retrying the retained QA run;
- submitting, cancelling, or retrieving OpenAI work;
- weakening API validation;
- adding a force-resume or manual inventory override;
- redesigning capacity, queueing, spend policy, or initial-wave topology; and
- repairing historical evidence by inference from logs.

## Review pauses

1. Owner approval before Slice 0.
2. API review after Slice 0 reproduction/evidence.
3. Joint schema/semantics approval after Slice 1.
4. API fixture review after Slice 5.
5. Final consumer review before any release recommendation.
