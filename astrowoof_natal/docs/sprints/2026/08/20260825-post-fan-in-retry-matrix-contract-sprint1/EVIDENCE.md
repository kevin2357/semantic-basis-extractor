# Evidence — Post-Fan-In Retry Matrix Contract Sprint 1

Status: complete; SBE 0.4.25 published and independently digest-verified

## Reviewed native surfaces

- `astrowoof_natal_authoring.lifecycle._local_dependencies`
- `astrowoof_natal_authoring.lifecycle._capacity_and_custody`
- `astrowoof_natal_authoring.lifecycle._execution_branch`
- `astrowoof_natal_authoring.lifecycle.inspect_lifecycle`
- `astrowoof_natal_authoring.lifecycle_contracts.validate_lifecycle_inspection_v04`
- `astrowoof_natal_authoring.lifecycle_contracts.validate_lifecycle_inspection_v05`
- `astrowoof_natal_authoring.pending_lifecycle_qa.run_provider_pending_lifecycle_qualification`

## Pre-sprint findings

1. `local_dependencies` are substantially derived from broad run statuses.
2. `ordinary_resume` validation requires a nonempty dependency list, but the public
   contract does not prove a specific currently executable local operation.
3. The current installed qualification proves six creates, 4+2 retrieval, local
   fan-in, and first external-authority selection; it does not prove post-fan-in
   creative retries or exhaustion.
4. `astrowoof.provider_pending_lifecycle_qualification.v1` is the leading naming
   candidate for the requested v1/v2 audit; no rename decision has been made.
5. No retained Crumpet bytes were accessed and no provider work occurred.

## Evidence gate

No source claim in this document authorizes implementation. Slice 0 must reproduce
the production-shaped post-fan-in state and freeze its actual native transition
before public schemas or runtime behavior change.

## Slice 0 evidence

- Test: `test_post_fan_in_retry_matrix_slice0.py`
- Result: 4 passed in 0.285 seconds on the bundled Python runtime.
- Exact and bounded routes reproduced the same masking transition.
- No production source or public schema changed.
- No external provider call, retrieval, credential, spend, or retained-run access.
- `git diff --check` passed for the sprint/test changes.

## Slice 1 evidence

Public proposal surfaces:

- `post_fan_in_contracts.py`
- `local-work-inventory.v1.schema.json`
- `temporal-lifecycle-contracts.v2.schema.json`
- root-level Python builders, validators, progress validator, and schema readers
- sanitized `local-work-inventory.ordinary-resume.proposal.json`

Focused command result:

```text
Ran 10 tests in 0.520s
OK (skipped=1)
```

Original breakdown: 4 Slice 0 tests plus 5 passing Slice 1 tests and one optional
`jsonschema` skip on the lean bundled runtime. Strict Python validation ran in all
cases. Public package import smoke passed. `git diff --check` passed.

After API review, Slice 1 added three passing semantic no-spin regressions. Current
combined focused total: 12 passed, 1 optional `jsonschema` skip. The new evidence
proves that a no-op snapshot/revision republish changes `operation_id` but preserves
`operation_key`, and is refused; continued ordinary work requires an explicitly
sealed consumed prior key; consumed-key history cannot shrink; and a semantic
operation consumed earlier in the lineage cannot be advertised again.

Safety totals remain:

- external provider/network calls: 0;
- real creates/retrievals: 0;
- spend: USD 0;
- retained Crumpet/QA access or mutation: 0.

## Slice 2 evidence

Runtime surfaces:

- `inspect_post_fan_in_lifecycle()` constructs the closed inventory from a real,
  snapshot-validated workspace.
- `commit_local_work_progress()` holds the native writer while it revalidates,
  proves semantic advancement, appends consumption history, checkpoints, and
  validates the successor.
- `lifecycle.local_work_selected` and `lifecycle.local_work_consumed` are bounded,
  non-authoritative, failure-isolated diagnostic events.

Focused Slice 0–2 command result:

```text
Ran 17 tests in 3.599s
OK (skipped=1)
```

That is 16 passing tests plus one optional `jsonschema` skip. A broader run adding
execution-event and lifecycle contract/inspection coverage produced:

```text
Ran 55 tests in 3.381s
OK (skipped=1)
```

The runtime matrix proves:

- exact and bounded completed retry evidence selects the exact source action;
- provider-pending custody never advertises local work;
- no-op progress is refused with byte-identical `run.json` and snapshot;
- successful fan-in seals cumulative consumption and exposes retry #2 authority;
- a failing diagnostic sink cannot change the native result;
- provider creates, retrievals, network calls, spend, and retained-QA access are
  all zero.

## Slice 3 evidence

Published evidence:

- `fixtures/post-fan-in-retry-matrix.v1.json`
- `SLICE 3 - PROVIDER-FREE RETRY MATRIX AND API HANDOFF.md`
- `test_post_fan_in_retry_matrix_slice3.py`

The three matrix tests use route/case subtests to prove all eight dispositions,
both exact and bounded interactive topology where applicable, plus provider
reconciliation before and after its due time. They also prove the external
authority refusal identity for unjoinable lineage and the non-dispatching native
AUTHORIZED/providerless fence.

Combined focused/lifecycle/event result:

```text
Ran 58 tests
57 passed, 1 optional jsonschema skip
```

Safety totals remain zero for provider create, provider retrieval, external
network, credentials, spend, and retained Crumpet/QA access.

## Production-path correction evidence

The release-blocking direct-helper gap is closed by one regression that enters
through both supported public commands:

1. `astrowoof-lifecycle ... inspect` returns v0.5 and fails closed with
   `local_work_contract_upgrade_required`;
2. `astrowoof-lifecycle ... inspect-local-work` returns v0.7 with the exact fan-in
   operation;
3. normal `astrowoof-run-semantic-closure --resume` executes the local mutation;
4. the real spend-boundary checkpoint calls writer-fenced consumption commitment;
5. the successor is `await_external_authority` for retry #2 with the prior key in
   cumulative consumed history and no retry-#2 provider identity.

Post-integration focused result:

```text
Ran 59 tests in 5.041s
OK (skipped=1)
```

This is 58 passing tests plus one optional `jsonschema` skip. The test uses a fake
provider and performs zero provider create/retrieval/network/spend activity.

The bounded production checkpoint hook was additionally exercised through the
existing bounded lifecycle resume subset:

```text
Ran 5 tests in 30.890s
OK
```

## Slice 4 source evidence

Public additions:

- `astrowoof-provider-pending-qa-v2`
- `astrowoof.provider_pending_lifecycle_qualification.v2`
- strict Python validator and packaged schema reader
- `provider-pending-lifecycle-qualification.v2.schema.json`

The new runner preserves and invokes v1, then crosses the public v0.7 CLI in fresh
Python processes for exact and bounded retry workspaces. It verifies one semantic
operation is consumed, the successor selects retry #2 external authority, and a
replay of the consumed prior inspection is refused.

Focused combined result:

```text
Ran 22 tests in 13.244s
OK (skipped=1)
```

The single skip is the existing optional `jsonschema` check. Strict Python
validation ran. External network/provider calls, real spend, credentials, retained
QA access, and post-fan-in provider I/O were zero. V1's six provider creates and six
retrievals remain scripted, local qualification operations only.

## Installed-wheel evidence

Candidate source version: `0.4.24` (not a release recommendation; a fresh patch
version is required if approved).

Build/install/invocation sequence:

```text
pip wheel . --no-deps --no-build-isolation
python -m venv --system-site-packages .tmp/post-fan-in-slice4-venv
pip install --no-deps --force-reinstall astrowoof_natal_authoring-0.4.24-py3-none-any.whl
astrowoof-provider-pending-qa-v2
```

Result:

```text
schema_version: astrowoof.provider_pending_lifecycle_qualification.v2
status: pass
receipt_sha256: 24ebfbc47d4f46966c473ba8e46377115849b7441617348c0522638dd04ca43b
routes: exact_natal, bounded_natal
successor: await_external_authority / paid_000000000000000000000102
replay_refused: true / true
```

The installed command accepted no production input and used no credentials. The
temporary qualification workspaces were discarded. The local `.tmp` build and
virtual-environment directories are untracked qualification material and are not
release source.
