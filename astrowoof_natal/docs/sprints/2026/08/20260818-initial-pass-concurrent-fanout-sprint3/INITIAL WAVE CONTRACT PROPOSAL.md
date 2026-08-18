# Initial Authoring Wave Contract Proposal

Date: 2026-08-18
Status: Slice 1 proposal for SBE/API review; not admitted by runtime

## Decision summary

Exact and bounded interactive initial authoring adopt one versioned six-member
wave. SBE prepares all six paid actions in one native mutation, exposes the complete
immutable member inventory, and performs no provider create until it validates:

1. one exact wave authorization envelope representing API transactional approval
   of the complete reservation set; and
2. all six existing exact member spend authorizations.

After preflight, six create-only Responses calls may overlap. Each returned provider
ID is durably serialized into the ledger and native transition journal immediately.
The command detaches after all create tasks close and publishes one aggregate
checkpoint. Provider completion is handled by the released bounded reconciliation
path, at most four due Responses per cycle.

Batch remains one paid action and one API reservation containing six logical
members. The interactive wave contract does not change Batch authority cardinality.

## Contract identities

| Artifact | Proposed identity |
|---|---|
| Prepared initial wave | `astrowoof.initial_authoring_wave.v1` |
| Wave authorization envelope | `astrowoof.initial_authoring_wave_authorization.v1` |
| Wave execution result | `astrowoof.initial_authoring_wave_result.v1` |
| Proposal schema | `astrowoof.initial_authoring_wave_contract_proposal.v1` |

The identities are route-neutral. Every artifact carries the exact semantic route
and route contract; exact and bounded packet bytes and authority remain separate.

## Fixed topology and timing

The v1 constants are:

| Constant | Value |
|---|---:|
| ordered initial members | 6 |
| maximum concurrent interactive creates | 6 |
| per-create provider transport timeout | 15 seconds |
| complete submission-cycle provider-I/O bound | 20 seconds |
| maximum due interactive retrievals per cycle | 4 |
| maximum parallel interactive retrievals | 4 |

The 20-second bound covers create I/O, not unbounded local checkpoint hashing or
provider completion. Deterministic work after I/O must proceed promptly and remain
observable, but it is not falsely presented as provider-I/O time. A create that
does not produce a safely classified outcome within its 15-second transport bound
is conservative ambiguity unless the transport proves no request was attempted.

Retrieval remains four-at-a-time. Create concurrency and retrieval concurrency are
independent controls.

## Cache policy

Interactive initial waves do not complete one Response as a cache warmer before
starting the other five. All six initial creates are eligible in the same wave.
No cache hit is assumed by spend authorization. Provider-reported cached-input
usage remains settlement/calibration evidence.

A future create-only cache priming strategy requires a new reviewed contract and
must not delay other wave members. The v1 policy is `no_serial_cache_warmer`.

## Prepared wave identity

The prepared wave binds:

- `wave_id`, derived from the immutable wave body;
- `wave_sha256`, the canonical digest of that body excluding the digest field;
- run ID, route family, route contract, assignment identity, profile SHA-256,
  price-book version, and one shared `preparation_basis_revision`;
- exactly six ordered initial members;
- each member's action ID, binding SHA-256, pass ID, pass number, route, attempt,
  stage, request SHA-256, model, service level, maximum output, commitment, and
  price book;
- aggregate maximum commitment; and
- the frozen timing/cache policy.

All members have `attempt=1`, `stage=authoring_initial`, and
`service_level=interactive`. Pass numbers are exactly 1 through 6. Every action
binding is computed against the same preparation basis and all six actions are
appended in one locked state mutation followed by one persistence step. Later
state-revision increments do not alter their immutable preparation basis.

The aggregate maximum commitment is the exact sum of member commitments. It is
evidence for the API reservation transaction; it does not replace SBE's per-action
or per-run ceilings.

## API transactional envelope

The API owns the transaction that either reserves the entire exact set or exposes
no executable wave. Its envelope binds:

- wave ID and SHA-256;
- run, route, profile, preparation basis, price book, member count, ordered action
  IDs/binding digests, and aggregate commitment copied exactly from the prepared
  wave;
- six member authorization SHA-256 values in the same order;
- an opaque API reservation-set reference;
- authorization issuer and timestamp; and
- envelope SHA-256.

The envelope is not a substitute for member authorization documents. Each member
document continues to use `astrowoof.provider_spend_authorization.v0.1` and must
match its complete action binding. SBE does not inspect API database rows or infer
transactionality from six unrelated references.

## All-or-none SBE preflight

Before the first create, SBE validates under exclusive native access:

1. complete snapshot/path and supported run/route contract;
2. prepared-wave digest and immutable member order;
3. current run/profile/assignment/price-book identity;
4. exactly six known unique actions, all providerless and unconsumed;
5. exact member binding and member authorization equality;
6. exact member authorization file digests and envelope inventory;
7. aggregate commitment and frozen per-run/stage budget classification;
8. envelope digest, reservation-set reference, and preparation basis; and
9. absence of ambiguity, denial, provider evidence, consumption evidence, terminal
   state, review state, or conflicting active work.

Any failure creates no provider operation and consumes no member authorization.
The refusal is typed and nonmutating except for failure-isolated redacted
observational events. The API may delay or deny a wave before this boundary without
leaving a partially executable native set.

## Execution and per-member states

After successful preflight, each task receives one immutable member request. Native
mutation remains serialized:

1. immediately before POST, consume that member authorization and persist
   `SUBMITTING` with its consumer/reference evidence;
2. perform the create outside the native mutation lock;
3. when an ID returns, acquire the writer lock, record the exact provider identity,
   persist ledger plus journal projection, and release the lock immediately; and
4. classify the task outcome without waiting for provider completion.

Closed member outcomes are:

| Outcome | Meaning | Resubmission |
|---|---|---|
| `provider_bound` | durable Response ID exists | prohibited; reconcile only |
| `authorized_unstarted` | create was provably never attempted | eligible only through reviewed replay of the same wave authority |
| `ambiguous_submission` | provider may have accepted but no durable ID exists | prohibited; review/reconciliation required |
| `create_refused` | provider definitively rejected before accepting work and evidence proves no operation exists | policy-controlled; not automatic in v1 |

The aggregate result is `detached_provider_pending` if one or more IDs are durable
and no ambiguity exists; `ambiguous_submission` if any member is ambiguous; or a
typed refusal if preflight performed zero creates. Mixed provider-bound and
authorized-unstarted members are permitted only after an execution interruption;
the exact replay rules must never resubmit provider-bound members.

There is no claim of provider atomicity or idempotency across the six creates.

## Immediate durability and publication protocol

Per-ID durability does not wait for all tasks. Each provider identity is persisted
with its ledger and journal transition as soon as its create returns.

The aggregate workspace snapshot, command result, and immutable publication receipt
are emitted only after all tasks unwind and their member outcomes are classified.
The result is visible/valid only when its journal range, member evidence, snapshot,
hashes, and receipt validate together. Interrupted partial publication fails closed.

## Reconciliation and fan-in

The existing provider-pending policy remains:

- no new commitment for polling known work;
- maximum four due Responses retrieved concurrently in one cycle;
- completed member evidence ingested monotonically through exact or bounded route
  adapters;
- local validation runs for completed members;
- unresolved members remain provider-pending with durable `resume_not_before`;
- accepted passes are never regenerated because another member remains pending;
  and
- canonical deck fan-in occurs only when all required initial members have closed
  successfully.

Pass-local creative retry remains a later independent action and is not part of
the initial six-member wave.

## Batch compatibility

Exact and bounded Batch preserve:

- one paid round action and one API global reservation;
- six ordered logical member bindings;
- one File/Batch provider identity;
- member-level output/error/usage audit beneath the round;
- usage-unavailable billing reconciliation when any potentially billable member
  lacks complete usage; and
- later retry rounds containing only eligible failed members.

Batch may reuse the logical ordered member inventory but does not accept an
interactive wave authorization envelope and does not create six reservation rows.

## Lifecycle and public vocabulary

No new public lifecycle outcome is required. The wave composes through:

- `awaiting_external_authority` before complete envelope/member authority;
- `detached_provider_pending` after safe provider-ID durability;
- `not_due` for early reconciliation;
- `progressed_local` when completed members are ingested;
- `ambiguous_submission` for any unsafe create boundary;
- existing review, budget, policy-stop, provider-failure, and delivery outcomes.

Inspection v0.3 already identifies route, mechanism, native operation, custody, and
consumer-authority facts per action. Slice 2 may add a separately versioned wave
projection/result rather than altering v0.3's strict top-level shape. If runtime
implementation proves an API decision cannot be made from the proposed artifacts
plus v0.3, contract work pauses rather than smuggling fields into an unvalidated
payload.

## Refusal precedence

The leading closed precedence is:

1. provider evidence or ambiguity conflict;
2. invalid snapshot/path or unsupported route/run contract;
3. terminal/review/native competing work;
4. stale wave/preparation observation;
5. binding, digest, member, aggregate, or envelope mismatch;
6. denied/budget-exhausted member;
7. missing/partial authorization; and
8. valid complete authorization.

Provider-safety evidence outranks generic staleness so operators receive the most
actionable and conservative classification.

## Proposed review questions

1. Are the prepared-wave, authorization-envelope, and result identities suitable
   for strict API persistence and rejection?
2. Does one API transaction/reference plus six existing exact member authorization
   documents preserve the correct authority split?
3. Is one native preparation mutation against a shared basis revision the right
   replay and stale-observation boundary?
4. Are 6 concurrent creates, 15 seconds per create, and a 20-second provider-I/O
   cycle acceptable frozen v1 limits?
5. Is `no_serial_cache_warmer` accepted for v1?
6. Are the four member outcomes sufficient, and should `create_refused` remain
   non-automatic?
7. Is preserving four-at-a-time retrieval correct for six-member waves?
8. Is a separate wave projection preferable to changing strict inspection v0.3?
9. Is the refusal precedence correct, especially provider safety over staleness?
10. Does Batch compatibility remain unambiguous at one reservation per round?

