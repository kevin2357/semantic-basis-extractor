# API review — Diffie evidence ceiling and terminal-result availability

## Diffie final evidence answer

API checked the exact failed attempt `29a00b89-28d9-4e4c-bc63-fb5451536f31`.

Authoritative PostgreSQL retains only the execution-attempt facts:

- run `9cbc3c0c-9a5f-42ff-8fc0-cc23f08b75df`, job
  `2b70d6de-baa2-4eb1-89d0-c77ccdf93333`, attempt 7;
- `worker_contract_failure` /
  `sbe.contract.provider_lifecycle` /
  `SbeProviderContractError`; and
- start `2026-08-30T08:56:45.615732Z`, finish
  `2026-08-30T08:56:52.346894Z`.

There is no PostgreSQL event/log/diagnostic table holding raw subprocess output.
The retained Render worker logs for the exact attempt contain only claim, lease,
cycle-start, typed cycle-failure, job-failure, and lease-release events. They do
not contain a subprocess stdout capture, embedded lifecycle inspection, or a
failed-attempt workspace archive. Local repository/artifact search found no
such retained capture.

Accordingly, SBE may close the Diffie tributary as **historical evidence
unavailable**. The source-compatible mixed completed/pending v0.5 predicate
mismatch remains a leading explanation, not a claimed byte-for-byte
reproduction.

## Terminal-result availability contract

Approved in principle. `astrowoof.native_transition_result_availability.v1` is
the correct narrow, provider-free discovery bridge:

- `none_available` is a valid explicit outcome;
- `available` yields exactly one ID that API subsequently reads by exact ID;
- malformed, orphaned, conflicting, unsealed, or snapshot-invalid evidence is
  a typed error, never an absence; and
- availability itself grants no lifecycle, provider, or transition authority.

One refinement: include the restored checkpoint/snapshot digest (or an equally
specific public snapshot identity) in the closed availability document and bind
it into `availability_document_sha256`. This does not reveal lifecycle state;
it lets API demonstrate that the discovered ID came from the same restored
checkpoint it is about to submit to the strict exact-result reader. API must
also require the exact reader's native-run/result join to agree with that
availability document and must not rediscover “latest” afterward.

With that refinement, SBE may implement Slice 1. No lifecycle, provider,
retained-run, or delivery behavior needs to change for this additive reader.
