# Operator Stuck-Run Native Retirement Patch — Sprint 1

Date: 2026-08-24

Status: Slices 0-4 complete; paused for final API review before release preparation

## Objective

Add one narrow, auditable SBE lifecycle operation that terminalizes an exact-Natal
workspace only when native evidence proves it is retirement-quiescent,
non-deliverable, and free of provider custody or ambiguity.

The API can then pair that truthful native transition with its separately
authoritative release of job, lease, capacity, and unspent-reservation state. This
is not a generic force-state, resume, retry, cancellation, or repair command. The
motivating QA run is problem evidence, not a development fixture to mutate.

## Frozen ownership boundary

SBE owns:

- complete workspace restoration and snapshot validation;
- native run identity, route, revision, lifecycle facts, and action history;
- native quiescence, provider custody, ambiguity, consumption, and local-work facts;
- the retirement contract and single-writer mutation;
- append-only retirement evidence and sealed native result/receipt publication;
- exact replay and already-retired interpretation.

The API owns:

- product job/run identity and operator authorization;
- active lease and worker-claim truth;
- capacity, global reservations, quotas, entitlements, and billing;
- external operator-decision persistence and retention;
- release of API-owned resources after validating SBE evidence; and
- the audited decision to apply the operation to a retained workspace.

SBE must not claim API leases, capacity, or reservations are absent. The API must
not infer native quiescence or manufacture native terminal state.

## Proposed lifecycle semantics

Approved v1 representation:

```text
status: POLICY_STOPPED
terminal cause: operator_retired
delivery publishable: false
provider continuation: false
local continuation: false
```

The public result must carry both `POLICY_STOPPED` and `operator_retired`
explicitly; consumers validate the semantic pair. Successful retirement is a real
authoritative mutation and must publish a normal journal range, complete snapshot,
native result, and receipt. Dry-run and refusal are nonmutating and publish no
native transition.

## Eligibility proposal

All conditions must hold under SBE's native single-writer fence:

- exact supported run contract and exact run identity;
- complete unchanged snapshot at the stable logical absolute path;
- nonterminal native state explicitly eligible for retirement;
- strict lifecycle and action-inventory validation;
- no provider identity requiring retrieval or custody;
- no provider result awaiting native ingestion;
- no provider ambiguity or identity conflict;
- no consumed/submitting action lacking a safe terminal disposition;
- no active local mutation or action-backed continuation already in progress;
- no completed or publishable delivery;
- no competing terminal transition or review condition;
- all remaining providerless actions have a supported final disposition; and
- exact request binding to the current native checkpoint.

Every unresolved providerless action must receive an existing supported
providerless-denial disposition first. Retirement refuses with
`providerless_action_unresolved` until that evidence exists. This patch does not
combine denial and retirement.

For this contract, `retirement_quiescent` does not mean that ordinary resume could
never derive future local work from the run's status. Current SBE deliberately
projects `AWAITING_SPEND_AUTHORIZATION` as `retry_preparation` even when the ledger
contains no action. That status-derived possibility is the continuation the
operator is explicitly abandoning. Eligibility instead requires a complete stable
checkpoint, exclusive native writer, no provider work/evidence/ambiguity, no
unresolved action, and no local mutation already in progress. The post-transition
result must still prove that no local continuation remains.

## Request, dry-run, and result model

The closed request should bind:

- native `run_id`, route contract, expected status, revision, and snapshot SHA-256;
- logical workspace root and lifecycle/checkpoint-basis identity;
- requested disposition `operator_retired` and closed durable reason
  `operator_abandoned_quiescent_run`;
- opaque API/operator audit reference;
- canonical request digest; and
- contract/schema version.

Dry-run validates the exact snapshot and the same predicate used by execute. It
returns a closed eligible/refused assessment and ordered failed predicates while
performing no mutation, snapshot refresh, journal append, publication, provider
operation, or authority consumption. It is not authorization against a later
checkpoint.

Execute reacquires the native writer, re-reads and revalidates all facts, records
the transition and causal evidence, then publishes one coherent snapshot/journal/
result/receipt protocol. The API consumes only the public typed result.

Proposed outcomes:

- `applied`;
- `exact_replay`;
- `already_retired` for a compatible later request;
- `stale_observation`;
- `not_retirement_quiescent`;
- `provider_custody_present`;
- `provider_ambiguity_present`;
- `providerless_action_unresolved`;
- `delivery_or_terminal_conflict`;
- `binding_mismatch`;
- `snapshot_invalid`; and
- `unsupported_contract`.

Exact replay binds the complete original request digest. A later compatible request
may report `already_retired`, but cannot masquerade as byte-identical replay.

A successful result explicitly binds native run ID, exact-Natal route, logical
root, original request digest, pre/post revision, pre/post snapshot digest,
`POLICY_STOPPED` plus `operator_retired`, complete terminal action-inventory/closure
digest, sealed result/receipt identities and digests, and assertions that no
provider-pending, provider-custody, or runnable local continuation remains.
The three false continuation assertions are freshly derived from post-transition
lifecycle inspection while the native writer remains held. The closure digest
covers every ledger action and disposition, including providerless denials.

Before invocation, the API atomically moves its exact job into an API-owned
operator-retirement-pending custody state that blocks ordinary worker continuation
without releasing resources. SBE fixtures document this required companion fence
but neither implement nor assert API state. If API finalization fails after SBE
success, exact replay of sealed native evidence permits later API finalization.

## Safety invariants

- No provider create, GET, cancel, retry, or status call.
- No provider credentials, payloads, or spend documents accepted.
- No deletion or rewriting of existing native history.
- No blessing of changed workspace bytes.
- No mutation on dry-run or refusal.
- No publication without a complete validated post-mutation snapshot.
- No API resource-release claim in SBE output.
- Event/log sink failure cannot affect native behavior.
- Events remain bounded, redacted, non-authoritative, and failure-isolated.

## Slice 0 — Contract and historical-shape investigation

1. Inspect existing terminal, `POLICY_STOPPED`, closeout, public-run, lifecycle,
   native-transition, providerless-denial, snapshot, and writer surfaces.
2. Build a sanitized provider-free exact-Natal fixture for the motivating class:
   nonterminal, no provider custody/ambiguity, no unresolved action, and only the
   status-derived local continuation that retirement is intended to abandon.
3. Freeze eligibility, request/dry-run/result schemas, refusal vocabulary, terminal
   cause, replay semantics, and ownership.
4. Decide whether unresolved providerless actions must be denied first.
5. Publish lifecycle-level positive and negative fixtures.

Gate: pause for API review before runtime implementation.

The seven planning questions are resolved below. Slice 0 still pauses for review of
the concrete contract and fixtures before Slice 1 implementation.

## Slice 1 — Strict public contract and read-only dry-run

1. Package closed JSON Schemas and strict Python semantic validators.
2. Add a public Python reader/builder and CLI dry-run surface.
3. Validate run, route, root, revision, snapshot, basis, status, inventory, and
   request-digest joins.
4. Return deterministic ordered failed predicates without protected/provider data.
5. Prove dry-run byte identity and zero journal/result/receipt publication.
6. Refuse pending, completed-awaiting-ingestion, ambiguous, consumed/submitting,
   locally runnable, deliverable, terminal-conflicting, stale, and malformed cases.

Gate: API validates the public fixture and persistence mapping.

## Slice 2 — Single-writer native retirement

1. Implement execute under the native lifecycle lock.
2. Revalidate all request and eligibility facts after acquiring the writer.
3. Persist `POLICY_STOPPED`/`operator_retired` or the approved equivalent with
   causal request/reference evidence.
4. Preserve complete prior action/provider history.
5. Publish the journal range, validated snapshot, immutable result, and receipt.
6. Return terminal, non-delivery, quiescence, and checkpoint evidence for the API.

Gate: success is terminal, non-publishable, quiescent, and provider-free; refusals
remain byte-identical.

## Slice 3 — Replay, concurrency, and failure injection

Prove provider-free behavior for:

- exact replay and compatible later `already_retired`;
- stale revision/snapshot/root/request digest;
- concurrent execute attempts;
- provider identity/evidence, ambiguity, consumption, or runnable local work
  appearing before writer acquisition;
- crash after state mutation but before journal/result publication;
- crash after snapshot but before receipt publication;
- deterministic repair where the existing publication protocol permits it;
- event-sink/log failure isolation; and
- protected/payload sentinel absence from diagnostics.

Gate: every interruption is safely replayable/recoverable or retained for review;
none creates provider work, duplicate history, or false API-release authority.

## Slice 4 — Installed-wheel qualification and API handoff

1. Add provider-free installed-wheel qualification using a sanitized real workspace
   and public runtime boundaries.
2. Exercise eligible dry-run, execute, replay, already-retired, stale, pending,
   ambiguous, and unresolved-providerless cases.
3. Validate the sealed result through the installed public reader.
4. Publish schemas, fixtures, hashes, command spelling, exit behavior, and mapping.
5. Document API order: validate dry-run, acquire API authority, execute SBE, ingest
   the exact result transactionally, then release only matching API resources.
6. Pause for API review before release preparation.

Gate: only validated `applied`, `exact_replay`, or `already_retired` evidence permits
the API's paired disposition; refusal retains resources and workspace custody.

## Slice 5 — Patch release and joint QA handoff

1. Run focused and complete source suites.
2. Commit artifact source before building.
3. Build twice at the source-commit epoch and require byte identity.
4. Run generic installed smoke and retirement qualification against the final wheel.
5. Publish a fresh immutable patch only after owner/API authorization.
6. Provide manifest, checksums, consumer handoff, and remote digest proof.
7. Hand off to API Sprint 38 for paired disposition and dry-run-first QA operation.

Gate: release qualification never mutates retained QA. The historical target is
touched only by the later jointly reviewed API operator run.

## Testing strategy

1. Pure schema and semantic-validator tests.
2. Lifecycle-level fixture and cross-object join tests.
3. Byte-identity tests for dry-run and refusals.
4. Single-writer execute/replay/concurrency tests.
5. Publication/snapshot/journal/receipt interruption tests.
6. Installed-wheel public CLI/API qualification.
7. Complete regression and generic release smoke.
8. API-owned joint QA evidence after release.

All SBE qualification is provider-free: credentials, network, retrievals,
submissions, retries, cancellations, and spend remain zero.

## Explicit non-goals

- deleting runs, workspaces, artifacts, or history;
- cancelling or reconciling provider work;
- retiring provider-pending or ambiguous work;
- releasing API leases, capacity, or reservations from SBE;
- repairing arbitrary historical bytes;
- bounded Natal, Batch, delivery-complete, or unknown historical contracts;
- a generic force-state/database cleanup command; or
- directly mutating the motivating QA target during development.

## Resolved Slice 0 decisions

1. `POLICY_STOPPED` plus `operator_retired`; both explicit.
2. Existing providerless denial precedes retirement.
3. Exact Natal only.
4. Outcome vocabulary accepted with the full success bindings specified above.
5. Exact digest replay versus compatible later `already_retired` accepted.
6. One v1 durable reason: `operator_abandoned_quiescent_run`; human explanation is
   separate non-semantic audit material.
7. API establishes an operator-retirement-pending custody fence before invocation
   and releases resources only after validated SBE success.
