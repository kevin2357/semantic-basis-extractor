# API Worker Integration — AstroWoof Natal Authoring v0.1

## Pin the immutable artifact

After the annotated tag and GitHub release are published, copy
`requirements-api-worker.txt` into the API worker build context and install it
with hash enforcement:

```text
python -m pip install --no-deps --require-hashes -r requirements-api-worker.txt
```

For a pre-release private image, copy the local wheel from `dist/` into the
image, verify SHA-256
`58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`,
and install that exact file. Do not install from a moving Git branch.

The image build must run:

```text
astrowoof-release-smoke --work-dir /tmp/astrowoof-smoke --require-installed
```

Promotion requires `status: pass` and resource-set SHA-256
`67be96ba08fbd89ab379d1ebf247ef011d595bd4446c4534edd5072a503dcdf2`.

## Durable initial invocation

The API creates a unique durable run directory, provides the normalized input
package, acquires a lease for the run ID, and launches:

```text
astrowoof-semantic-closure \
  --input-package /work/inputs/<run-id> \
  --subject <subject-slug> \
  --run-dir /work/runs/<run-id> \
  --provider openai \
  --service-level batch \
  --batch-detach \
  --batch-poll-interval-seconds 30 \
  --routing-policy cost_optimized \
  --model gpt-5.6-luna \
  --reasoning-effort medium \
  --retry-model gpt-5.6-terra \
  --retry-reasoning-effort medium \
  --polish \
  --polish-model gpt-5.6-luna \
  --polish-reasoning-effort low \
  --split-assignment-policy stratified-v1 \
  --full-chart-basis-format compact-v2 \
  --prompt-cache-mode explicit \
  --prompt-cache-ttl 30m \
  --max-attempts 3 \
  --max-workers 6 \
  --max-polish-attempts 2
```

Model IDs and profile options are release configuration owned by the API, not
end-user inputs. A later authoring release may intentionally revise them.

## Resume and polling

Batch submission returns quickly. A scheduler periodically reacquires the same
run lease and invokes:

```text
astrowoof-semantic-closure \
  --resume \
  --run-dir /work/runs/<run-id> \
  --provider openai \
  --service-level batch \
  --batch-detach \
  --batch-poll-interval-seconds 30 \
  --routing-policy cost_optimized \
  --model gpt-5.6-luna \
  --reasoning-effort medium \
  --retry-model gpt-5.6-terra \
  --retry-reasoning-effort medium \
  --polish \
  --polish-model gpt-5.6-luna \
  --polish-reasoning-effort low \
  --prompt-cache-mode explicit \
  --prompt-cache-ttl 30m \
  --max-attempts 3 \
  --max-workers 6 \
  --max-polish-attempts 2
```

An HTTP status request must never execute this command. It reads the persisted
`public-run.json` only. `run.json` is operator-only recovery/audit state and
must not be returned to users.

Only one process may mutate a run at a time. The API must provide a database or
queue-backed lease; atomic JSON replacement is not a distributed lock.

## Terminal handling

- `DELIVERY_COMPLETE`: promote the five-file delivery ZIP and immutable deck
  to object storage, persist artifact hashes, then mark the reading ready.
- `FAILED_REQUIRES_REVIEW`: retain run state and QA evidence, alert operators,
  and do not deliver a deck.
- Provider/transient interruption: release the worker but retain the run
  directory; the scheduler may resume under the normal retry policy.

After artifact promotion and the configured debugging TTL, use the runner's
cleanup command to remove reconstructable expanded workspaces while retaining
operator state, public state, QA, accepted evidence, and final delivery.

## Service ownership

The API owns users, dogs, authorization, idempotency, queues, leases, quotas,
cost caps, object storage, notifications, and product status mapping. This
wheel owns extraction, authoring, acceptance, retry/resume, assembly, polish,
provenance, accounting, and final delivery construction.
