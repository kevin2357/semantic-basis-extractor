# API Worker Integration - AstroWoof Natal Authoring v0.2

## Install and qualify

After publication, install `requirements-api-worker.txt` with `--no-deps
--require-hashes`. Private GitHub credentials must be short-lived build secrets
and must never enter this file, image layers, logs, runtime state, or delivery.
Before publication, install the local wheel only after verifying SHA-256
`cbc8e82da546c1dd4a13a60544f31c5627365167c8c7c48f3114b5fd1f4c03e4`.

Run `astrowoof-release-smoke --require-installed` in the deployed image.
Promotion requires `status: pass` and resource aggregate
`439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.

## Worker contract

The API creates one durable input and run directory, acquires an exclusive
lease, freezes a generation profile and real spend policy, then invokes
`astrowoof-semantic-closure` with `--input-package`, `--run-dir`, provider and
profile options, and `--spend-policy`. Batch workers may use `--batch-detach`.

When `public-run.json` reports `AWAITING_SPEND_AUTHORIZATION`, read
`spend-authorization-requests.json`, transactionally reserve account budget,
and issue an envelope whose binding is copied exactly. Resume under the same
lease with `--spend-authorization <file>`. Authorization is bound to request
digest, run, profile, prepared revision, stage, route, model/service level,
maximum output, commitment, and versioned price book. Never edit `run.json` or
reuse an authorization.

Polling a recorded provider ID needs no new reservation. An ambiguous
submission must stop for provider/operator reconciliation; deterministic keys
are not proof of OpenAI idempotency. Persist API billing correlation through
SBE's append-only reconciliation references.

Status endpoints read `public-run.json`; they never execute the runner. Resume
requires the complete workspace snapshot restored at the recorded stable
logical absolute path. One API lease and SBE's local consumption lock together
enforce the single-writer contract.

## Ownership

SBE owns exact per-run ceilings, action bindings, local commitment/reporting,
resume safety, disclosure minimization, acceptance, QA, provenance, snapshots,
and delivery construction. The API owns transactional reservations across
runs, users/accounts and quotas, global circuit breakers, entitlements/product
policy, authoritative billing reconciliation, queues, leases, storage, and
promotion policy.
