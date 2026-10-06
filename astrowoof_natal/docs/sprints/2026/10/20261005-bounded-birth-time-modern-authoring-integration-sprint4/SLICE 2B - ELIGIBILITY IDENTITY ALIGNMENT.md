# Slice 2B — eligibility identity alignment

## Decision

The pre-workspace under-floor result cannot truthfully contain a
`native_invocation_id`: no native publication has occurred, and SBE only mints
that identity while sealing an ordinary result/receipt.

The eligibility result therefore advances from
`astrowoof.bounded_eligibility_command_result.v1` to **v2** and replaces
`native_invocation_id` with API-issued `command_attempt_id`.

- `native_run_id`: API-issued, persisted run identity shared by eligible and
  under-floor branches.
- `command_attempt_id`: API-issued, pre-workspace idempotency/correlation key;
  strict form `bca_` plus 24 lowercase hexadecimal characters.
- `native invocation ID`: SBE-minted only at receipt-backed publication, and
  never claimed by an under-floor eligibility result.

This avoids reusing one field name for incompatible ownership/lifecycle
meanings. It is a candidate-only public-contract correction; v1 was never
published.

## Required API change

For the new wheel, API must invoke the under-floor branch with
`--command-attempt-id`, validate v2 only, and persist/compare the same
API-issued attempt identity at eligibility ingress. It must not require a
native receipt or terminal-publication invocation from this provider-free path.
