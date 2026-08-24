# Legacy Provider-Pending Bridge Compatibility — Sprint 1 Plan

Date: 2026-08-24
Status: complete; SBE 0.4.17 tagged, published, and remotely digest-verified

## Objective

Determine whether the immutable SBE 0.4.16 wheel already supports one narrowly
defined recovery operation for an exact-Natal v0.5-era retained workspace with six
durable provider Response identities and no reconciled provider result.

The intended operation is retrieval-only:

```text
astrowoof-semantic-closure --run-dir RUN \
  --resume --provider openai \
  --provider-reconciliation-cycle \
  --observed-at <canonical UTC instant>
```

The API request's `astrowoof-authoring-lifecycle` spelling is not the provider
reconciliation command and will be corrected in the final handoff.

The preferred result is qualification of the existing 0.4.16 artifact. Source
changes, version bumps, tags, publication, live provider work, and retained-QA
workspace mutation are out of scope unless the provider-free evidence proves a
specific compatibility gap.

## Frozen ownership boundary

SBE owns:

- validation of the restored native workspace and complete snapshot;
- native route, provider identity, action binding, due-member selection, and
  reconciliation eligibility;
- bounded GET-only retrieval;
- reconciliation evidence, native checkpoint mutation, result publication, and
  subsequent lifecycle/temporal projection.

The API owns:

- the audited operator decision to grant one worker claim;
- durable worker/job records, leases, capacity, and retention;
- the trusted canonical UTC observation instant;
- ingestion of supported SBE public evidence; and
- the decision whether the qualified bridge may be used for the named retained
  target.

Neither side may reprofile the historical run, reconstruct provider identity,
invent external authority, authorize new paid work, or mutate private native state.

## Invariants

1. No provider create, submit, retry, Batch create, spend authorization, external
   authority request, or external authority grant may be accepted.
2. The fixture contains exactly six durable Response identities joined to six
   native actions and no completed provider-response artifact.
3. SBE chooses the bounded due subset; the caller supplies no action IDs.
4. A retrieval response ID must exactly match its durable native provider ID.
5. A due pending result persists one attempt/backoff checkpoint and publishes a
   sealed native reconciliation result.
6. An immediate pre-due replay is typed `not_due`, nonmutating, and does not claim
   to publish a new checkpoint.
7. Completed-provider behavior may be exercised provider-free for contract
   completeness, but the retained target must not be contacted or mutated.
8. Logs/events remain diagnostic. Snapshot, reconciliation result, native result,
   publication receipt, and lifecycle/temporal documents are authoritative.
9. No claim is made that historical v0.5 inspection bytes become v0.6. A new v0.6
   temporal observation is derived only from the validated checkpoint after the
   supported reconciliation command.

## Slice 0 — Freeze the historical fixture and command contract

Status: complete; paused at the planned owner/API review gate.

Create a sanitized, production-shaped exact-interactive workspace using supported
SBE fixture/runtime builders. Freeze:

- current run/snapshot schema identities;
- six ordered actions with canonical IDs, complete bindings, authorizations,
  consumption evidence, Response IDs, and v0.2 reconciliation timing;
- `WAITING_FOR_RESPONSE` native state;
- absence of provider-response evidence and create-capable external authority;
- corrected public CLI spelling and required arguments; and
- the expected pending, not-due, refusal, and completed outcomes.

Add a fixture manifest with hashes and a concise compatibility contract document.
Do not copy protected subject data or bytes from the retained QA workspace.

Gate: owner and API review of the frozen fixture semantics, command spelling,
receipt shape, and API ingestion expectations before qualification execution.

## Slice 1 — Installed-wheel retrieval-only qualification

Status: complete; installed 0.4.16 wheel passed the real public command gate.

Install the exact published 0.4.16 wheel in an isolated environment. Drive the
real public semantic-closure CLI/dispatcher against a disposable copy of the
frozen fixture with a scripted provider transport.

The scripted transport must fail the test on every POST/create/submit/retry path
and record each GET. Prove:

- exactly the SBE-selected bounded subset is retrieved;
- no caller-selected member inventory is accepted;
- no authorization or external-authority document is accepted;
- provider IDs and route bindings remain unchanged;
- pending retrieval writes a coherent attempt/backoff checkpoint;
- the public cycle result is strict and ingestible;
- the native execution result and publication receipt validate together with the
  complete snapshot; and
- provider calls, credentials, network, and spend are zero.

Gate: all retrieval-only and sealed-publication assertions pass against the exact
installed 0.4.16 wheel.

## Slice 2 — Replay, refusal, and temporal bridge matrix

Status: complete; one narrow 0.4.16 binding-validation gap found

Against fresh disposable fixture copies, prove:

- immediate replay before due is typed `not_due`, byte-identical, and performs no
  retrieval;
- a later trusted instant becomes due without changing native/provider facts;
- malformed/missing provider identity, binding mismatch, incomplete snapshot,
  unsupported historical timing, identity conflict, and attempted authority input
  fail closed;
- a scripted completed response is durably reconciled without a seventh create;
- completed evidence produces a new checkpoint basis; and
- current public readers can validate the reconciliation output and derive a
  lifecycle v0.6 temporal observation only after the command checkpoint.

Gate: the compatibility bridge never converts uncertainty or malformed historical
evidence into create or recovery authority.

Result: create authority remained impossible, but a binding/run-identity mismatch
did not refuse the affected provider GET. The conditional patch gate is therefore
active; runtime changes remain paused for owner/API review.

## Slice 3 — Decision receipt and API handoff

Status: candidate receipt published; final immutable artifact coordinates pending

Publish a concise closed qualification receipt containing:

- exact SBE version and wheel SHA-256;
- fixture manifest/schema/hash identities;
- invoked command shape;
- GET/create/authorization counts;
- selected action count without provider-sensitive payloads;
- pre/post snapshot and checkpoint-basis hashes;
- native result/receipt identities and hashes;
- assertion inventory; and
- final decision: `supported_now`, `narrow_patch_required`, or
  `unsupported_review_only`.

Document that `not_due` is intentionally nonmutating and has no new sealed result,
whereas a due pending GET is a persisted attempt with a new schedule/checkpoint and
sealed reconciliation publication.

Gate: API confirms the evidence is sufficient for its dry-run-first audited bridge
without reading private SBE state or broadening provider authority.

## Slice 4 — Conditional patch decision only

Status: activated and source-qualified

This slice is entered only if Slices 0–3 expose a concrete 0.4.16 incompatibility.
Record the smallest public correction, its safety contract, regression boundary,
and whether a fresh immutable patch release is necessary. Return to owner/API
review before changing runtime source.

Decision: API selected whole-cycle refusal. The implementation validates the full
provider-backed inventory before due-subset selection and returns nonmutating typed
review with zero GETs for any binding/native-run contradiction. A fresh immutable
patch is required after installed-wheel qualification.

If qualification succeeds, close this slice as `not_needed`; do not rebuild or
republish SBE.

## Test strategy

- Provider-free and credential-free throughout.
- Disposable workspace copies only; no retained QA workspace access.
- Installed-wheel execution from outside the source tree.
- Scripted transport that records GET and raises immediately on all create methods.
- Hash workspace state before and after nonmutating cases.
- Validate complete snapshot membership before and after mutating cases.
- Validate the cycle result, lifecycle inspection, native result, publication
  receipt, and temporal v0.6 projection through supported public readers.
- Include failure injection at result/snapshot/publication boundaries if the
  installed path exposes those hooks without source modification.
- Run only focused compatibility/lifecycle tests unless source changes become
  necessary.

## Stop conditions

Stop and return for review if:

- the fixture cannot be represented without private/manual state blessing;
- installed 0.4.16 reaches any create-capable branch;
- the historical action inventory lacks required native identity/timing evidence;
- the command cannot publish API-ingestible evidence;
- the bridge would require reinterpreting v0.5 as v0.6; or
- qualification suggests touching the retained QA workspace.
