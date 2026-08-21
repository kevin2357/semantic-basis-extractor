# Slice 5 — Installed-Wheel Qualification and Handoff

Status: complete and API-approved.

## Delivered

- Preserved the immutable v1 qualification receipt and introduced the closed
  `astrowoof.external_authority_qualification.v2` receipt.
- Extended the real-workspace qualification to prove all request-branch and
  typed-refusal conditional predicates reject contradictory mutations.
- Kept the existing holistic proof of public lifecycle inspection, public request
  reading, external authority outside the workspace, fresh-process constrained
  execution, six durable provider identities, replay refusal, retrieval-only
  reconciliation selection, lineage refusal, and ordinary-action reading.
- Published sanitized fixtures, a passing receipt, and the consumer handoff.
- Improved child-process failures so installed qualification reports the failing
  step and captured diagnostic instead of masking it as `CalledProcessError`.

## Installed artifact

```text
astrowoof_natal_authoring-0.4.14-py3-none-any.whl
SHA-256 59053ac273d21f6d7b252d34b23a0757bacf1420baa855aee2b7612676d3f12b
```

The wheel was installed in an isolated Python 3.11 environment and the advertised
console command was invoked from outside the source package path. Packaged
resources supplied the v2 schema.

## Result

```text
schema_version: astrowoof.external_authority_qualification.v2
status: pass
provider_create_count: 6 (scripted only)
provider_spend_usd: 0
network_required: false
production_authority: false
receipt_sha256: 969867611a7fab84514cf252c552118a5896f3429b356a773b04ed82f0dbdd37
```

Source qualification tests: 2 passed, 1 environment-dependent JSON Schema test
skipped on the lean host interpreter. Installed qualification validated its closed
receipt with the packaged runtime validator.

The combined lifecycle/external-authority matrix ran 97 tests: 91 passed and 6
existing environment-dependent JSON Schema checks skipped on the lean host.

## Safety

- Real provider calls: 0
- Real provider retrievals: 0
- Spend: USD 0
- Credentials/network/production inputs: none
- Retained QA workspace access or mutation: none

The exact retained incident predicate remains unknown. This evidence proves the
candidate's supported classification and validation behavior, not a retroactive
diagnosis of bytes that were never retained.
