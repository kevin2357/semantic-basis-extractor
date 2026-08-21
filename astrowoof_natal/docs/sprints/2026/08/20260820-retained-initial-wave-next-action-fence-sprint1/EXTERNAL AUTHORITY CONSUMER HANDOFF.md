# External Authority Consumer Handoff

Status: Slice 7 candidate for AstroWoof API review.

## Supported boundary

SBE owns native action preparation, exact bindings, wave lineage, single-writer
mutation, provider identities, ambiguity, snapshots, and lifecycle truth. The API
owns transactional cross-run reservation, global quota/circuit policy, leases,
capacity, product entitlement, PostgreSQL/R2 persistence, and billing
reconciliation.

The API must use lifecycle inspection v0.5 and the embedded
`external_authority_request` or `external_authority_refusal`. It must not reconstruct
the decision from `run.json`, packets, logs, response IDs, or subprocess exit codes.

## Initial interactive wave sequence

1. Invoke ordinary create/resume once to let SBE prepare the exact six-member wave.
2. Inspect lifecycle v0.5. Require `execution_branch.command` =
   `await_external_authority` and validate the embedded request.
3. Atomically decide the whole six-action reservation set in API authority.
4. For a grant, persist the exact request, six complete ordinary authorization
   documents, and one aggregate grant joining all identities and digests.
5. Invoke the same route command with the exact request, grant, and ordered six
   authorization documents.
6. Ingest the resulting native checkpoint before releasing a worker lease.

Exact command arguments:

```text
astrowoof-semantic-closure --run-dir RUN --resume --provider openai \
  --service-level interactive \
  --external-authority-request REQUEST.json \
  --external-authority-grant GRANT.json \
  --spend-authorization MEMBER-1.json ... MEMBER-6.json
```

Bounded uses the equivalent inputs on `astrowoof-run-bounded-natal`.

Generic resume against an awaiting, authorized, or submitting constrained wave is
not create permission and fails closed. Once provider identities are durable, use
the lifecycle-selected provider reconciliation command; never reconstruct a member
subset in the API.

## Ordinary actions and Batch

- Exact/Bounded Batch retain one paid action and one API reservation per Batch
  round; member rows are audit/settlement evidence.
- Creative retry, polish, critic, and candidate actions retain their existing
  complete per-action authorization boundary.
- `ordinary_action_set` is the closed public selection/binding projection. The
  aggregate grant is specifically required for six-member interactive initial-wave
  admission.
- Optional policy skip remains distinct from external denial.

## Refusal and compatibility

- `initial_wave_lineage_unjoinable` means retained evidence cannot prove one exact
  reusable wave. Retain for native review; do not prepare or submit another wave.
- Stale observation, changed binding, incomplete grant, provider evidence,
  consumption, or ambiguity all refuse before new provider create.
- Lifecycle v0.4 remains readable but is not authorizing for this continuation.
- The retained Aster cohort is not mutated by qualification. Its eligibility must
  be decided from restored, snapshot-valid native evidence using the released
  implementation.

## Installed-wheel qualification

Run without credentials, network, production input, or spend authority:

```text
astrowoof-external-authority-qa --output receipt.json --fixtures-dir fixtures
```

The closed receipt is qualification evidence only. It never constitutes native
execution authority or an API reservation decision. The command constructs a real
snapshot-valid exact-Natal workspace through SBE runtime code, obtains the embedded
lifecycle v0.5 request, persists authority outside the workspace, and reopens the
workspace in fresh Python processes for constrained execution, retained replay, and
the real provider-reconciliation entry point. The scripted Responses transport
proves exactly six creates, durable provider identities, no seventh create, and a
bounded retrieval-only reconciliation subset.

Separate snapshot-valid workspaces exercise `initial_wave_lineage_unjoinable`
through lifecycle inspection and `ordinary_action_set` through the public request
reader. The four stable contract fixtures remain sanitized synthetic examples;
their hashes do not depend on a temporary logical workspace path.

Lifecycle inspection binds a request to its own `observed_at`. The constrained
executor therefore revalidates that exact supplied observation against current
revision, snapshot digest, logical root, completeness, inventory, and writer
claims. Only observation time may differ from the snapshot-state timestamp; a
change to any safety-bearing field is `stale_observation` before provider I/O.

Consumer fixtures and their exact hashes are in the Slice 7 receipt under
`fixture_hashes`. Consumers should validate fixture content against those hashes,
the packaged v1 schemas, and their own strict closed-world models.

## Review gate

API review should confirm:

- lifecycle v0.5 request/refusal ingestion and strict identity joins;
- all-or-none six-action reservation/grant persistence;
- terminal-first native result ingestion before lease/capacity decisions;
- no generic-resume fallback for constrained wave states;
- reconciliation selection remains run-level and SBE-owned; and
- the transition oracle requires no new public product states.
