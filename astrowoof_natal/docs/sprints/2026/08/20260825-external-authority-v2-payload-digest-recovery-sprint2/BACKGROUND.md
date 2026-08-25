# External-authority v2 request-payload digest recovery

## Trigger

The first fresh QA cohort to exercise the full v2 ordinary external-authority
continuation completed its initial six-member authoring waves and reconciled all
twelve provider results. API then supplied SBE with an exact v2 inspection,
request, grant, and member authorization set for one next ordinary action per
run.

SBE sealed both commands as `pre_provider_refusal`:

```text
reason_code=request_payload_digest_mismatch
provider_io_disposition=not_attempted
grant_invocation_disposition=refused
```

Affected native runs:

- `6755b4793434c9e000e890fc4c5f5d64529e813ff678ca65068c05c5a7f04e7a`
  (API run `7653fc15-e6da-4869-a375-307db37bf7d3`, Cosmo Crumpet)
- `bd00c6d9c00fac31de60b54aca998a60bcecdee815ee3610bc23d7f78e7df0d4`
  (API run `8388d8fb-ee86-4276-8015-ea97c2638ef4`, Miso Moonbeam)

## What succeeded

- The initial-wave v1 fan-out occurred once per run.
- All six resulting provider identities were durably recorded and reconciled
  per run.
- Temporal lifecycle inspection selected `await_external_authority` only after
  provider-local dependency count reached zero.
- API constructed, persisted, and supplied v2 grant material matching the
  selected request under its own custody and spend controls.

## What failed

SBE's final pre-provider payload integrity check derives a request-payload
digest that does not match the payload digest represented by the API-issued
v2 authority material. This is a contract/canonicalization problem at the
fenced command boundary, not a reason to relax the fence. A successful fix must
make a valid API-issued exact request/grant pass the check; a genuinely altered
payload must continue to fail closed.

## Required properties

1. No provider create may occur before all request, grant, action binding, and
   payload-digest checks agree.
2. The public request/grant contract must have one unambiguous canonical digest
   definition, with cross-repository positive and negative fixtures.
3. The original refusal must remain truthful: it was pre-provider and carries
   no ambiguity or provider identity for the blocked action.
4. A compatible released patch must allow the retained workspace to make a new
   exact scheduling decision or safely consume a new exact request; it must not
   replay initial-wave work or revive the refused grant as though it had created
   provider work.
5. SBE must preserve typed refusal for genuinely mismatched payloads.

## API/SBE coordination

API will use the released public contract and its existing v2 admission/receipt
records. It will not reverse-engineer a private SBE payload. Before recovery it
will revalidate the retained checkpoint, inspect current custody, and ensure
the next request is a permitted post-refusal continuation with no ambiguous
provider operation. The two repositories should add an exchanged fixture that
uses the actual public request, inspection, grant, and authorization documents
rather than independently constructed lookalikes.
