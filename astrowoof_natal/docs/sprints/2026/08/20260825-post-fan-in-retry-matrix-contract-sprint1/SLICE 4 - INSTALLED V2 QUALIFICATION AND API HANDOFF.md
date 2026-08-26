# Slice 4 — Installed v2 Qualification and API Handoff

Status: implemented and installed-wheel qualified; final consumer review pending

## Public surfaces

- Command: `astrowoof-provider-pending-qa-v2`
- Python runner: `run_provider_pending_lifecycle_qualification_v2()`
- Python validator: `validate_provider_pending_lifecycle_qualification_v2()`
- Schema reader: `read_provider_pending_lifecycle_qualification_v2_schema()`
- Contract: `astrowoof.provider_pending_lifecycle_qualification.v2`

The existing `astrowoof-provider-pending-qa` command and v1 receipt are retained
unchanged. V1 honestly proves initial six-create detach, bounded 4+2 retrieval,
durable fan-in evidence, and first external-authority selection. It does not claim
post-fan-in retry progress.

V2 runs the complete v1 qualification, then opens exact and bounded
production-shaped retry workspaces through the public v0.7 lifecycle CLI in fresh
Python processes. It consumes completed retry evidence through the supported
writer-fenced progress API, reopens the workspace again, and proves the successor
selects the one exact retry-2 external-authority action.

## Consumer interpretation

- `ordinary_resume` is supported only with a nonempty, validated v0.7 local-work
  inventory.
- API invokes the run-level ordinary command; it does not invoke inventory members.
- After native execution, the prior semantic operation must appear in cumulative
  `consumed_operation_keys`, or a different typed disposition must be selected.
- Exact replay of an already-consumed operation is refused and publishes no new
  progress checkpoint.
- Lifecycle v0.5/v0.6 consumers must fail closed on concrete local work and upgrade
  before routing this branch.
- The receipt is qualification evidence only. It grants no provider, reservation,
  lease, capacity, or production authority.

The v2 command accepts no run directory, provider configuration, credentials,
authorization, request payload, or production input. Its provider interactions are
scripted by v1; the post-fan-in cells perform zero provider I/O. Temporary
workspaces are destroyed after qualification.

## API disposition mapping

| v0.7 selected command | Required consumer behavior |
| --- | --- |
| `ordinary_resume` | Require a nonempty valid inventory, invoke only the run-level ordinary command, then ingest a successor that consumes prior semantic work or changes disposition. |
| `provider_reconciliation_cycle` | Invoke only SBE's run-level reconciliation command when due; SBE owns the bounded member subset. |
| `await_external_authority` | Ingest and validate the exact SBE request; API alone decides whether to grant global authority. |
| `none` | Consume the typed terminal/review/refusal evidence; do not infer native work from private files or logs. |

An API consumer that supports only lifecycle v0.5/temporal v0.6 must not route
post-fan-in local work. The released legacy readers deliberately return
`local_work_contract_upgrade_required` at this boundary. This is a consumer
upgrade requirement, not a new API-global scheduling state.
