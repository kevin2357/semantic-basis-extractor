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

## Superseding candidate qualification

| Field | Value |
| --- | --- |
| Source commit | `f540574eb6619b3aa3511daec40104085bd2ce5b` |
| Retained wheel | `C:\tmp\sbe-0.4.70-bounded-slice2b-candidate\astrowoof_natal_authoring-0.4.70-py3-none-any.whl` |
| SHA-256 | `58c9ba4c616aa4d62d906aeee1f385aefb8e8cb03fd512c9566b016a219d6094` |
| Bytes | `1,439,081` |

The wheel was installed with `--no-index --no-deps` into an isolated local
target. It emitted and validated the v2 provider-free result with
`command_attempt_id`, and rejected the former field by absence from the closed
schema. The same installed wheel also reran the API four-context family to a
50-card `DELIVERY_COMPLETE` result/receipt terminal command; altered receipt
identity was refused.

## Required API change

For the new wheel, API must invoke the under-floor branch with
`--command-attempt-id`, validate v2 only, and persist/compare the same
API-issued attempt identity at eligibility ingress. It must not require a
native receipt or terminal-publication invocation from this provider-free path.
