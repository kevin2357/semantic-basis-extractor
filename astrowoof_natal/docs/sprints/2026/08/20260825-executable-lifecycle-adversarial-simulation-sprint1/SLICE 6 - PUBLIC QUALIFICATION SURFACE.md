# Slice 6 — Public Qualification Surface

Status: implemented and installed-wheel qualified; paused for consumer review

## Public boundary

The wheel now packages:

- Python builder/validator/schema reader for
  `astrowoof.lifecycle_adversarial_qualification.v1`; and
- console command `astrowoof-adversarial-qa` with `--schema` and optional
  `--output`.

The command runs the real route-matrix, systematic-explorer, and seeded-campaign
components and emits one concise closed receipt. It binds package identity, schema
and fixture-corpus digests, fixed seeds, route/transition coverage, invariant count,
counterexample references, stable component-contract summaries, and zero-provider
totals.

Invocation-specific temporary-workspace receipt identities are validated internally
but deliberately excluded from the public aggregate. The public receipt is therefore
deterministic across equivalent invocations while still proving the same stable
contract cells.

## Safety

- Provider-free and credential-free.
- External network calls, real provider creates, and spend are exactly zero.
- Output paths inside any native workspace ancestor are refused before qualification
  runs or output is written.
- No prompt, provider payload/ID, workspace path, subject data, or exception text is
  emitted.

## Installed evidence

- Candidate wheel version: `0.4.25` source candidate; a fresh version remains release
  work for Slice 8.
- Wheel SHA-256:
  `b40edcde3026e1bcf3910e9f89d194bd7af0be11f40518c1f905eff628e22fc5`.
- Two isolated installed-console invocations produced byte-identical receipts.
- Receipt-file SHA-256:
  `ae8b988c13723f8447bd1548748320447ac7f63ca4eb020cefae96413133435a`.

