# Slice 1: Contract Freeze Proposal

Status: contract frozen; API-approved after one compatibility correction.

## Result

The proposed native journal and immutable per-invocation result contracts are
published for cross-repository freeze. No packaged schema, runtime behavior,
provider path, public API, CLI, or release metadata changed.

The proposal preserves lifecycle inspection v0.3 and reconciliation-cycle result
v0.2 as compatible projections. It adds only the missing cross-invocation authority:

- compact append-only native transition/provider observations;
- immutable invocation identity and result artifact;
- exact journal range/digest and run/checkpoint binding;
- terminal/review meaning published before command exit;
- refusal of conflicting second provider operations; and
- a read-only bounded ingestion target for API transactional persistence.

## Key decisions

### Immutable authority

Each invocation receives an immutable `ninv_*` identity and one immutable
`native-results/<nres_*>.json` artifact. Any latest-result index is derived and
non-authoritative. API replay keys to run ID, result ID, and journal-range digest.

### Provider observations

Every observation has its own `ntr_*` SBE identity distinct from action and provider
IDs, a closed kind, `observed_at`, native revision, route/mechanism/operation
binding, and exact action binding. Provider external identity remains null before it
is actually received. Missing usage never becomes reported zero.

### No supersession

One action may have many observations of one external operation. A second distinct
external ID is refused. Supersession/recovery remains unsupported; the API review
will decide whether future-only null fields belong in v0.1 or should wait.

### Publication without a hash cycle

The immutable result cannot embed the hash of a snapshot manifest that contains the
result itself. The proposal defines `checkpoint_basis_sha256` over state/journal
members while excluding only the publication namespace from that *basis digest*.
The ordinary full workspace snapshot still inventories and protects the journal,
result, and derived index.

Validity therefore requires all of the following together:

1. result identity/hash;
2. journal chain/range/digest;
3. post-state revision and recomputed checkpoint basis;
4. exact result member/hash in the full snapshot; and
5. complete snapshot validation at the stable logical path.

Interrupted partial publication fails closed. No literal multi-file filesystem or
provider atomicity is claimed.

## Closed API mapping

A valid delivery, review, terminal failure, pending, continuation, authority wait,
budget, policy, or ambiguity result is ingested before exit-code fallback. In
particular, a valid `review_required` result forbids generic retry even when the
command exits 2.

Invalid range/hash/snapshot, route/action mismatch, fork/gap, or stale evidence is
an atomic ingestion refusal and review retention—not retry authority. A missing
result permits generic fallback only when the API independently proves the command
failed before any valid native result could exist.

## Draft schema evidence

The non-packaged proposal schema strictly validates:

- the closed record/outcome/cause/route/stage/cost vocabularies;
- additional-property refusal;
- absent provider ID at submission start;
- present provider ID for known-ID observations;
- versioned usage/price evidence for reported amounts; and
- null estimated amount when usage is unavailable or no provider work occurred.

Canonical review-terminal and completed-provider examples validate. Negative tests
reject unknown outcome, consumer-added fields, fabricated pre-identity provider ID,
and `$0` normalization of unavailable usage.

## Tests

- Proposal schema tests: 3 passed in 0.020 seconds.
- Proposal plus current lifecycle contract/inspection compatibility: 33 passed in
  0.377 seconds.
- `jsonschema` was installed only into a generated isolated `.tmp` target because
  the lean source-test Python omits SPC's transitive dependency. The target was
  removed after the gate.
- Provider operations: 0. Paid spend: `$0`.
- `git diff --check`: pass.

## API decision resolution

1. Checkpoint basis plus complete full-snapshot validation: accepted.
2. `(run_id, result_id, range_sha256)` idempotency: accepted, with canonical
   `result_sha256` also validated and persisted.
3. API acknowledgement field: omitted entirely.
4. Closed native outcomes/causes: accepted.
5. Permanent no-compaction for journal v0.1: accepted.
6. Future predecessor/supersession fields: omitted until a real later contract.

The one required compatibility correction is complete: journal evidence reuses the
exact reconciliation v0.2 cost dispositions, including
`provider_usage_unavailable_billing_reconciliation_pending` and
`not_applicable_provider_pending`.

## Gate assessment

The API agent approved the corrected contract for implementation. Slice 2 may begin
after Kevin approves and commits this frozen Slice 1 package.
